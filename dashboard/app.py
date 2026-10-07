"""Interactive OULAD story dashboard built with Streamlit and Plotly.

The application follows ``docs/plan_approved.md``:

* RQ1–RQ5 and six data-derived insights are kept separate from model RQ6;
* descriptive and cutoff-safe data scopes are labelled explicitly;
* nine non-map chart types are present;
* the geographic gate is never claimed without validated geometry;
* model metrics come from verified artifacts rather than being retrained here.
"""

from __future__ import annotations

import json
from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from dashboard_data import (
    REGION_GEOJSON_PATH,
    cascading_options,
    compute_kpis,
    filter_attempts,
    load_analysis_data,
    load_eda_table,
    load_feature_snapshot,
    load_model_table,
    load_predictions,
)


RESULT_ORDER = ["Distinction", "Pass", "Fail", "Withdrawn"]
STATUS_ORDER = ["Not-At-Risk", "At-Risk"]
QUARTILE_ORDER = ["Q1 — Lowest", "Q2", "Q3", "Q4 — Highest"]
PAGE_OPTIONS = ["Overview", "Factor Analysis", "Risk Analysis", "Prediction"]
PAGE_SLUGS = {
    "Overview": "overview",
    "Factor Analysis": "factor",
    "Risk Analysis": "risk",
    "Prediction": "prediction",
}
INK = "#0F172A"
MUTED = "#475569"
GRID = "#E2E8F0"
PANEL = "#FFFFFF"
RISK_SCALE = ["#FFF7ED", "#FED7AA", "#FB923C", "#DC2626", "#991B1B"]
HEAT_SCALE = ["#FFF7ED", "#FFEDD5", "#FED7AA", "#FDBA74", "#F87171"]
RISK_COLORS = {"At-Risk": "#DC2626", "Not-At-Risk": "#2563EB"}
RESULT_COLORS = {
    "Distinction": "#0F766E",
    "Pass": "#2563EB",
    "Fail": "#F97316",
    "Withdrawn": "#DC2626",
}


st.set_page_config(
    page_title="OULAD Learning Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_dashboard_css() -> None:
    """Apply a restrained visual system without hiding Streamlit controls."""

    st.markdown(
        """
        <style>
        .stApp { background: #F8FAFC; }
        .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px; }
        h1, h2, h3 { color: #0F172A; letter-spacing: -0.02em; }
        p, label, .stCaption { color: #334155; }
        [data-testid="stSidebar"] { border-right: 1px solid #E2E8F0; }
        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 0.85rem 1rem;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }
        [data-testid="stMetricLabel"] { color: #475569; }
        [data-testid="stMetricValue"] { color: #0F172A; }
        [data-testid="stPlotlyChart"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 0.35rem;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        }
        .page-kicker {
            color: #2563EB;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }
        .page-subtitle { color: #475569; font-size: 1.02rem; margin-top: -0.35rem; }
        .scope-note {
            display: inline-block;
            background: #EFF6FF;
            color: #1E40AF;
            border: 1px solid #BFDBFE;
            border-radius: 999px;
            padding: 0.28rem 0.7rem;
            font-size: 0.82rem;
            font-weight: 600;
            margin: 0.15rem 0 0.9rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(kicker: str, title: str, subtitle: str, scope: str) -> None:
    st.markdown(f'<div class="page-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="scope-note">{scope}</div>', unsafe_allow_html=True)


def polish_figure(
    figure: go.Figure,
    *,
    height: int,
    legend: str = "top",
    hovermode: str | bool = "closest",
) -> go.Figure:
    """Give every Plotly visual consistent spacing, type and interaction."""

    figure.update_layout(
        template="plotly_white",
        height=height,
        margin={"l": 55, "r": 35, "t": 78, "b": 55},
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font={"family": "Arial, sans-serif", "size": 13, "color": INK},
        title={"x": 0.02, "xanchor": "left", "font": {"size": 19, "color": INK}},
        hoverlabel={"bgcolor": "#FFFFFF", "font_size": 13, "font_color": INK},
        hovermode=hovermode,
    )
    figure.update_xaxes(
        showgrid=False,
        linecolor=GRID,
        tickfont={"color": MUTED},
        title_font={"color": MUTED},
        automargin=True,
    )
    figure.update_yaxes(
        gridcolor=GRID,
        zerolinecolor=GRID,
        linecolor=GRID,
        tickfont={"color": MUTED},
        title_font={"color": MUTED},
        automargin=True,
    )
    if legend == "top":
        figure.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.01,
                "xanchor": "right",
                "x": 1,
                "title_text": "",
                "bgcolor": "rgba(255,255,255,0.85)",
            }
        )
    elif legend == "none":
        figure.update_layout(showlegend=False)
    return figure


@st.cache_data(show_spinner=False)
def cached_analysis_data() -> pd.DataFrame:
    return load_analysis_data()


@st.cache_data(show_spinner=False)
def cached_snapshot() -> pd.DataFrame:
    """Load day-105 features and assign global, reproducible analysis bands."""

    frame = load_feature_snapshot()
    frame["module_presentation"] = (
        frame["code_module"].astype(str)
        + "-"
        + frame["code_presentation"].astype(str)
    )
    frame["engagement_quartile"] = pd.qcut(
        frame["vle_total_clicks_cutoff"].rank(method="first"),
        q=4,
        labels=QUARTILE_ORDER,
    )

    score = frame["assessment_weighted_score_cutoff"]
    has_score = score.notna()
    score_band = pd.Series(
        "No scored assessment by cutoff", index=frame.index, dtype="object"
    )
    score_band.loc[has_score] = pd.qcut(
        score.loc[has_score].rank(method="first"),
        q=4,
        labels=QUARTILE_ORDER,
    ).astype(str)
    frame["assessment_score_quartile"] = pd.Categorical(
        score_band,
        categories=QUARTILE_ORDER + ["No scored assessment by cutoff"],
        ordered=True,
    )
    frame["previous_attempt_band"] = np.where(
        frame["num_of_prev_attempts"].eq(0),
        "0 lần học trước",
        "1+ lần học trước",
    )
    frame["credit_band"] = pd.cut(
        frame["studied_credits"],
        bins=[-np.inf, 60, 120, 180, np.inf],
        labels=["≤60 credits", "61–120 credits", "121–180 credits", ">180 credits"],
    )
    for column in ("highest_education", "imd_band", "age_band", "disability"):
        frame[column] = frame[column].fillna("Không xác định")
    return frame


@st.cache_data(show_spinner=False)
def cached_predictions() -> pd.DataFrame:
    return load_predictions()


@st.cache_data(show_spinner=False)
def cached_model_table(filename: str) -> pd.DataFrame:
    return load_model_table(filename)


@st.cache_data(show_spinner=False)
def cached_insights() -> pd.DataFrame:
    return load_eda_table(
        "insight_evidence.csv",
        {
            "insight_id",
            "rq",
            "comparison",
            "group_a",
            "group_a_n",
            "group_a_rate",
            "group_b",
            "group_b_n",
            "group_b_rate",
            "risk_difference_pp",
            "limitation",
        },
    )


def format_percent(value: float) -> str:
    return "—" if pd.isna(value) else f"{value:.1%}"


def format_number(value: float | int, decimals: int = 0) -> str:
    if pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}"


def render_kpis(frame: pd.DataFrame) -> None:
    kpis = compute_kpis(frame)
    first_row = st.columns(3)
    first_row[0].metric("Lượt học", format_number(kpis.attempts))
    first_row[1].metric("Người học duy nhất", format_number(kpis.learners))
    first_row[2].metric("Lượt học At-Risk", format_number(kpis.at_risk_count))
    second_row = st.columns(3)
    second_row[0].metric("Tỷ lệ At-Risk", format_percent(kpis.at_risk_rate))
    second_row[1].metric(
        "Điểm assessment trung bình", format_number(kpis.average_assessment_score, 1)
    )
    second_row[2].metric("Tổng VLE clicks", format_number(kpis.vle_total_clicks))


def render_snapshot_kpis(frame: pd.DataFrame) -> None:
    first_row = st.columns(3)
    first_row[0].metric("Lượt học đủ điều kiện", f"{len(frame):,}")
    first_row[1].metric("Tỷ lệ At-Risk", format_percent(frame["At_Risk"].mean()))
    first_row[2].metric(
        "Trung vị VLE clicks",
        format_number(frame["vle_total_clicks_cutoff"].median()),
    )
    second_row = st.columns(2)
    second_row[0].metric(
        "Trung vị ngày tương tác", format_number(frame["vle_active_days_cutoff"].median())
    )
    second_row[1].metric(
        "Trung vị tỷ lệ hoàn thành assessment",
        format_percent(frame["assessment_completion_rate_cutoff"].median()),
    )


def selection_values(event: Any, axis: str = "x") -> set[str]:
    """Extract selected Plotly point values across Streamlit return variants."""

    if event is None:
        return set()
    try:
        points = event.selection.points
    except (AttributeError, KeyError):
        try:
            points = event["selection"]["points"]
        except (KeyError, TypeError):
            return set()
    return {
        str(point[axis]) for point in points if point.get(axis) is not None
    }


def render_filter_context(
    modules: list[str], presentations: list[str], regions: list[str], rows: int
) -> None:
    parts = [
        f"Module: {', '.join(modules) if modules else 'Tất cả'}",
        f"Presentation: {', '.join(presentations) if presentations else 'Tất cả'}",
        f"Region: {', '.join(regions) if regions else 'Tất cả'}",
        f"N={rows:,} lượt học",
    ]
    st.caption(" | ".join(parts))


def render_insight(insight_id: str, *, map_pending: bool = False) -> None:
    evidence = cached_insights()
    rows = evidence.loc[evidence["insight_id"].eq(insight_id)]
    if rows.empty:
        st.warning(f"Không tìm thấy bằng chứng {insight_id}.")
        return
    row = rows.iloc[0]
    suffix = " Geographic Map vẫn chờ geometry hợp lệ." if map_pending else ""
    st.info(
        f"**{insight_id} · {row['rq']}** — {row['group_a']} "
        f"({row['group_a_rate']:.1%}, N={int(row['group_a_n']):,}) so với "
        f"{row['group_b']} ({row['group_b_rate']:.1%}, "
        f"N={int(row['group_b_n']):,}); chênh "
        f"{row['risk_difference_pp']:.1f} điểm %. "
        f"Giới hạn: {row['limitation']}{suffix}"
    )


def sidebar_filters(frame: pd.DataFrame) -> tuple[str, list[str], list[str], list[str]]:
    st.sidebar.title("OULAD Dashboard")
    requested_slug = st.query_params.get("page", "overview")
    slug_to_page = {slug: page for page, slug in PAGE_SLUGS.items()}
    requested_page = slug_to_page.get(str(requested_slug), "Overview")
    page = st.sidebar.radio(
        "Điều hướng",
        PAGE_OPTIONS,
        index=PAGE_OPTIONS.index(requested_page),
        format_func=lambda value: {
            "Overview": "Tổng quan",
            "Factor Analysis": "Phân tích yếu tố",
            "Risk Analysis": "Phân tích rủi ro",
            "Prediction": "Dự báo",
        }[value],
    )
    st.query_params["page"] = PAGE_SLUGS[page]
    st.sidebar.divider()
    st.sidebar.subheader("Bộ lọc nhiều cấp")

    module_options, _, _ = cascading_options(frame)
    modules = st.sidebar.multiselect(
        "Module", module_options, key="filter_modules", placeholder="Tất cả module"
    )
    _, presentation_options, _ = cascading_options(frame, modules=modules)

    valid_presentations = [
        value
        for value in st.session_state.get("filter_presentations", [])
        if value in presentation_options
    ]
    if valid_presentations != st.session_state.get("filter_presentations", []):
        st.session_state["filter_presentations"] = valid_presentations
    presentations = st.sidebar.multiselect(
        "Presentation",
        presentation_options,
        key="filter_presentations",
        placeholder="Tất cả presentation",
    )

    _, _, region_options = cascading_options(
        frame, modules=modules, presentations=presentations
    )
    valid_regions = [
        value
        for value in st.session_state.get("filter_regions", [])
        if value in region_options
    ]
    if valid_regions != st.session_state.get("filter_regions", []):
        st.session_state["filter_regions"] = valid_regions
    regions = st.sidebar.multiselect(
        "Region", region_options, key="filter_regions", placeholder="Tất cả region"
    )

    if st.sidebar.button("Đặt lại bộ lọc", width="stretch"):
        for key in ("filter_modules", "filter_presentations", "filter_regions"):
            st.session_state.pop(key, None)
        st.rerun()

    st.sidebar.caption(
        "Module → Presentation → Region. Bộ lọc áp dụng cho biểu đồ mô tả và "
        "tập dự báo đang hiển thị; metric model công bố không bị tính lại theo bộ lọc."
    )
    with st.sidebar.expander("Định nghĩa nhanh"):
        st.markdown(
            "- **Learning attempt:** một lượt học theo Module–Presentation–Student.\n"
            "- **At-Risk:** kết quả cuối là Fail hoặc Withdrawn.\n"
            "- **VLE clicks:** tương tác trên nền tảng, không phải giờ học/điểm danh.\n"
            "- **Cutoff 105:** model chỉ dùng dữ liệu đến hết ngày 105."
        )
    return page, modules, presentations, regions


def render_overview(frame: pd.DataFrame) -> None:
    render_page_header(
        "RQ1 · Tổng quan",
        "Kết quả học tập đang phân bố như thế nào?",
        "So sánh bốn kết quả cuối khóa và khác biệt giữa module–presentation.",
        "Phạm vi: bảng mô tả toàn khóa · một dòng = một learning attempt",
    )
    render_kpis(frame)

    outcome = (
        frame.groupby("final_result", observed=True)
        .size()
        .reindex(RESULT_ORDER, fill_value=0)
        .rename("attempts")
        .reset_index()
    )
    left, right = st.columns([0.8, 1.7])
    with left:
        donut = px.pie(
            outcome,
            names="final_result",
            values="attempts",
            hole=0.55,
            color="final_result",
            color_discrete_map=RESULT_COLORS,
            category_orders={"final_result": RESULT_ORDER},
            title="Tỷ trọng kết quả cuối khóa",
        )
        donut.update_traces(
            textinfo="percent+label",
            textposition="inside",
            insidetextorientation="horizontal",
            marker={"line": {"color": "#FFFFFF", "width": 2}},
            hovertemplate="Kết quả=%{label}<br>N=%{value:,}<br>Tỷ trọng=%{percent}<extra></extra>",
        )
        donut.add_annotation(
            text=f"<b>{len(frame):,}</b><br>lượt học",
            x=0.5,
            y=0.5,
            showarrow=False,
            font={"size": 16, "color": INK},
        )
        polish_figure(donut, height=470, legend="none")
        st.plotly_chart(donut, width="stretch")

    distribution = frame.assign(
        module_presentation=(
            frame["code_module"].astype(str)
            + "-"
            + frame["code_presentation"].astype(str)
        )
    )
    stacked = (
        distribution.groupby(
            ["module_presentation", "final_result"], observed=True
        )
        .size()
        .rename("attempts")
        .reset_index()
    )
    stacked["share"] = stacked["attempts"] / stacked.groupby(
        "module_presentation"
    )["attempts"].transform("sum")
    with right:
        stacked_fig = px.bar(
            stacked,
            x="module_presentation",
            y="share",
            color="final_result",
            color_discrete_map=RESULT_COLORS,
            category_orders={"final_result": RESULT_ORDER},
            custom_data=["attempts"],
            labels={
                "module_presentation": "Module-presentation",
                "share": "Tỷ trọng trong khóa",
                "final_result": "Kết quả cuối",
            },
            title="Cơ cấu kết quả theo module–presentation",
        )
        stacked_fig.update_layout(barmode="stack")
        stacked_fig.update_yaxes(tickformat=".0%", range=[0, 1])
        stacked_fig.update_xaxes(tickangle=-45)
        stacked_fig.update_traces(
            hovertemplate=(
                "Module–presentation=%{x}<br>Tỷ trọng=%{y:.1%}<br>"
                "N=%{customdata[0]:,}<extra></extra>"
            )
        )
        polish_figure(stacked_fig, height=470)
        event = st.plotly_chart(
            stacked_fig,
            width="stretch",
            key="overview_module_selection",
            on_select="rerun",
            selection_mode="points",
        )
        st.caption("Chọn một hoặc nhiều cột để lọc chéo biểu đồ drill-down bên dưới.")

    selected = selection_values(event)
    drill_frame = (
        distribution.loc[distribution["module_presentation"].isin(selected)]
        if selected
        else distribution
    )
    if selected:
        st.caption(
            "Lọc chéo: "
            + ", ".join(sorted(selected))
            + f" · N={len(drill_frame):,} lượt học"
        )
    hierarchy = (
        drill_frame.groupby(
            ["code_module", "code_presentation", "final_result"], observed=True
        )
        .size()
        .rename("attempts")
        .reset_index()
    )
    sunburst = px.sunburst(
        hierarchy,
        path=["code_module", "code_presentation", "final_result"],
        values="attempts",
        color="final_result",
        color_discrete_map=RESULT_COLORS,
        title="Drill-down: Module → Presentation → Kết quả cuối",
    )
    sunburst.update_traces(
        marker={"line": {"color": "#FFFFFF", "width": 1.5}},
        hovertemplate="%{label}<br>N=%{value:,}<br>% cha=%{percentParent:.1%}<extra></extra>",
    )
    polish_figure(sunburst, height=580)
    st.plotly_chart(sunburst, width="stretch")
    render_insight("INS-01")
    st.caption(
        "Story transition: chênh lệch giữa khóa học đặt ra câu hỏi liệu tín hiệu "
        "VLE và assessment trước ngày 105 có giúp giải thích risk profile hay không."
    )


def render_factor_analysis(snapshot: pd.DataFrame) -> None:
    render_page_header(
        "RQ2–RQ5 · Phân tích yếu tố",
        "Những tín hiệu sớm nào liên hệ với At-Risk?",
        "Theo dõi VLE, assessment và tương tác đa yếu tố trước thời điểm dự báo.",
        "Phạm vi: eligible attempts · chỉ dữ liệu quan sát đến ngày 105",
    )
    render_snapshot_kpis(snapshot)

    trajectory_source = snapshot[["actual_status"]].copy()
    trajectory_source["Ngày 50–77"] = snapshot["vle_clicks_previous_28_days"] / 28
    trajectory_source["Ngày 78–91"] = (
        snapshot["vle_clicks_last_28_days"]
        - snapshot["vle_clicks_previous_7_days"]
        - snapshot["vle_clicks_last_7_days"]
    ).clip(lower=0) / 14
    trajectory_source["Ngày 92–98"] = snapshot["vle_clicks_previous_7_days"] / 7
    trajectory_source["Ngày 99–105"] = snapshot["vle_clicks_last_7_days"] / 7
    period_order = ["Ngày 50–77", "Ngày 78–91", "Ngày 92–98", "Ngày 99–105"]
    trajectory = (
        trajectory_source.melt(
            id_vars=["actual_status"],
            value_vars=period_order,
            var_name="period",
            value_name="daily_clicks",
        )
        .groupby(["period", "actual_status"], observed=True)
        .agg(mean_daily_clicks=("daily_clicks", "mean"), attempts=("daily_clicks", "size"))
        .reset_index()
    )
    trajectory["period"] = pd.Categorical(
        trajectory["period"], period_order, ordered=True
    )
    trajectory = trajectory.sort_values("period")
    line = px.line(
        trajectory,
        x="period",
        y="mean_daily_clicks",
        color="actual_status",
        markers=True,
        color_discrete_map=RISK_COLORS,
        category_orders={"actual_status": STATUS_ORDER},
        custom_data=["attempts"],
        labels={
            "period": "Cửa sổ thời gian",
            "mean_daily_clicks": "VLE clicks/ngày/attempt",
            "actual_status": "Kết quả thực tế",
        },
        title="Xu hướng tương tác VLE trước cutoff",
    )
    line.update_traces(
        line={"width": 3},
        marker={"size": 10, "line": {"color": "#FFFFFF", "width": 1.5}},
        hovertemplate="Cửa sổ=%{x}<br>Clicks/ngày/attempt=%{y:.2f}<br>N=%{customdata[0]:,}<extra></extra>",
    )
    polish_figure(line, height=450, hovermode="x unified")
    st.plotly_chart(line, width="stretch")
    st.caption("Bốn cửa sổ không chồng lấp; mỗi điểm là clicks trung bình mỗi ngày trên toàn bộ eligible attempts, kể cả attempt có 0 click.")

    left, right = st.columns(2)
    with left:
        box = px.box(
            snapshot,
            x="actual_status",
            y="assessment_weighted_score_cutoff",
            color="actual_status",
            color_discrete_map=RISK_COLORS,
            category_orders={"actual_status": STATUS_ORDER},
            points=False,
            labels={
                "actual_status": "Kết quả thực tế",
                "assessment_weighted_score_cutoff": "Điểm assessment có trọng số tại ngày 105",
            },
            title="Phân bố điểm assessment trước cutoff",
        )
        box.update_traces(
            marker={"opacity": 0.7},
            hovertemplate="Trạng thái=%{x}<br>Điểm=%{y:.1f}<extra></extra>",
        )
        polish_figure(box, height=480, legend="none")
        st.plotly_chart(box, width="stretch")

    profile = (
        snapshot.groupby(
            ["code_module", "code_presentation"], observed=True
        )
        .agg(
            attempts=("id_student", "size"),
            median_score=("assessment_weighted_score_cutoff", "median"),
            median_clicks=("vle_total_clicks_cutoff", "median"),
            at_risk_rate=("At_Risk", "mean"),
        )
        .reset_index()
    )
    with right:
        bubble = px.scatter(
            profile,
            x="median_score",
            y="median_clicks",
            size="attempts",
            color="at_risk_rate",
            color_continuous_scale=RISK_SCALE,
            range_color=[0, 1],
            hover_name="code_module",
            hover_data={
                "code_presentation": True,
                "attempts": ":,",
                "at_risk_rate": ":.1%",
                "median_score": ":.1f",
                "median_clicks": ":.0f",
            },
            labels={
                "median_score": "Trung vị điểm assessment",
                "median_clicks": "Trung vị VLE clicks",
                "at_risk_rate": "Tỷ lệ At-Risk",
            },
            title="Hồ sơ tín hiệu sớm theo module–presentation",
        )
        bubble.update_traces(
            marker={"line": {"color": "#FFFFFF", "width": 1.2}, "opacity": 0.88}
        )
        bubble.update_layout(coloraxis_colorbar={"title": "At-Risk", "tickformat": ".0%"})
        bubble.update_yaxes(type="log")
        polish_figure(bubble, height=480, legend="none")
        st.plotly_chart(bubble, width="stretch")

    heat_source = snapshot.loc[
        snapshot["assessment_score_quartile"].isin(QUARTILE_ORDER)
    ]
    heat = (
        heat_source.groupby(
            ["engagement_quartile", "assessment_score_quartile"],
            observed=True,
        )
        .agg(attempts=("id_student", "size"), at_risk_rate=("At_Risk", "mean"))
        .reset_index()
    )
    rate_matrix = (
        heat.pivot(
            index="engagement_quartile",
            columns="assessment_score_quartile",
            values="at_risk_rate",
        )
        .reindex(index=QUARTILE_ORDER, columns=QUARTILE_ORDER)
    )
    count_matrix = (
        heat.pivot(
            index="engagement_quartile",
            columns="assessment_score_quartile",
            values="attempts",
        )
        .reindex(index=QUARTILE_ORDER, columns=QUARTILE_ORDER)
        .fillna(0)
    )
    heatmap = go.Figure(
        go.Heatmap(
            z=rate_matrix.values,
            x=rate_matrix.columns.astype(str),
            y=rate_matrix.index.astype(str),
            customdata=count_matrix.values,
            colorscale=HEAT_SCALE,
            zmin=0,
            zmax=1,
            text=np.where(
                rate_matrix.notna(),
                np.vectorize(lambda value: f"{value:.1%}")(
                    rate_matrix.fillna(0).values
                ),
                "—",
            ),
            texttemplate="%{text}",
            textfont={"color": INK, "size": 14},
            hovertemplate=(
                "VLE=%{y}<br>Assessment=%{x}<br>At-Risk=%{z:.1%}<br>"
                "N=%{customdata:,}<extra></extra>"
            ),
            colorbar={"title": "At-Risk", "tickformat": ".0%", "len": 0.8},
        )
    )
    heatmap.update_layout(
        title="Ma trận risk profile: VLE × assessment",
        xaxis_title="Nhóm điểm assessment",
        yaxis_title="Nhóm VLE clicks",
    )
    polish_figure(heatmap, height=570, legend="none")
    st.plotly_chart(heatmap, width="stretch")
    st.caption(
        "Heatmap chỉ gồm attempts có điểm assessment trước cutoff; nhóm chưa có điểm được giữ riêng trong EDA, không bị coi là 0 điểm."
    )

    render_insight("INS-02")
    render_insight("INS-03")
    render_insight("INS-04")
    st.caption(
        "Story transition: sau khi thấy các tín hiệu kết hợp, trang Risk Analysis "
        "đặt chúng trong context lịch sử học và không gian."
    )


def render_region_map(region_stats: pd.DataFrame) -> None:
    st.subheader("Geographic Map — phân bố không gian của At-Risk")
    if not REGION_GEOJSON_PATH.exists():
        st.warning(
            "CHƯA HOÀN THÀNH: chưa có geometry có nguồn/giấy phép cho 13 vùng "
            "lịch sử của OULAD. Bar chart không được dùng thay cho Geographic Map."
        )
        return

    with REGION_GEOJSON_PATH.open(encoding="utf-8") as geojson_file:
        geojson = json.load(geojson_file)
    feature_regions = {
        str(feature.get("properties", {}).get("region"))
        for feature in geojson.get("features", [])
    }
    expected_regions = set(region_stats["region"].astype(str))
    missing_regions = sorted(expected_regions.difference(feature_regions))
    if missing_regions:
        st.error("GeoJSON chưa khớp region: " + ", ".join(missing_regions))
        return

    map_fig = px.choropleth(
        region_stats,
        geojson=geojson,
        locations="region",
        featureidkey="properties.region",
        color="at_risk_rate",
        color_continuous_scale=RISK_SCALE,
        range_color=[0, 1],
        custom_data=["attempts", "at_risk_count"],
        labels={"at_risk_rate": "Tỷ lệ At-Risk"},
        title="Tỷ lệ At-Risk theo vùng OULAD",
    )
    map_fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        bgcolor=PANEL,
    )
    map_fig.update_traces(
        marker_line_color="#FFFFFF",
        marker_line_width=0.8,
        hovertemplate=(
            "Region=%{location}<br>At-Risk=%{z:.1%}<br>"
            "N=%{customdata[0]:,}<br>Số At-Risk=%{customdata[1]:,}<extra></extra>"
        )
    )
    map_fig.update_layout(
        coloraxis_colorbar={"title": "At-Risk", "tickformat": ".0%", "len": 0.75}
    )
    polish_figure(map_fig, height=650, legend="none")
    st.plotly_chart(map_fig, width="stretch")
    st.caption(
        "Geometry là xấp xỉ có kiểm soát từ ranh giới ONS; màu thể hiện rate, không phải số lượng. Xem nguồn và giới hạn trong dashboard/assets/README.md."
    )


def render_risk_analysis(
    analysis: pd.DataFrame, snapshot: pd.DataFrame
) -> None:
    render_page_header(
        "RQ4–RQ5 · Phân tích rủi ro",
        "Những nhóm nào cần được chú ý hơn?",
        "Đặt risk profile vào bối cảnh lịch sử học, giáo dục và phân bố không gian.",
        "Rate luôn đi kèm N · khác biệt nhóm không phải quan hệ nhân quả",
    )
    render_snapshot_kpis(snapshot)

    dimension_options = {
        "Trình độ học vấn": "highest_education",
        "Nhóm IMD": "imd_band",
        "Số credits đăng ký": "credit_band",
        "Nhóm tuổi": "age_band",
        "Tình trạng disability": "disability",
    }
    selected_dimension_label = st.selectbox(
        "Phân tầng risk profile",
        list(dimension_options),
        index=0,
        help="Giữ tầng đầu là số lần học trước; chọn tầng thứ hai để đối chiếu các đặc điểm RQ4.",
    )
    selected_dimension = dimension_options[selected_dimension_label]
    profile = (
        snapshot.groupby(
            ["previous_attempt_band", selected_dimension], observed=True
        )
        .agg(
            attempts=("id_student", "size"),
            at_risk_count=("At_Risk", "sum"),
            at_risk_rate=("At_Risk", "mean"),
        )
        .reset_index()
    )
    treemap = px.treemap(
        profile,
        path=[
            px.Constant("Lượt học đủ điều kiện"),
            "previous_attempt_band",
            selected_dimension,
        ],
        values="attempts",
        color="at_risk_rate",
        color_continuous_scale=RISK_SCALE,
        range_color=[0, 1],
        custom_data=["attempts", "at_risk_count", "at_risk_rate"],
        title=f"Quy mô risk profile: Lần học trước → {selected_dimension_label}",
    )
    treemap.update_traces(
        marker={"line": {"color": "#FFFFFF", "width": 1.5}},
        texttemplate="<b>%{label}</b><br>N=%{value:,}",
        hovertemplate=(
            "%{label}<br>N=%{customdata[0]:,}<br>Số At-Risk=%{customdata[1]:,}"
            "<br>Tỷ lệ At-Risk=%{customdata[2]:.1%}<extra></extra>"
        )
    )
    treemap.update_layout(coloraxis_colorbar={"title": "At-Risk", "tickformat": ".0%"})
    polish_figure(treemap, height=540, legend="none")
    st.plotly_chart(treemap, width="stretch")
    st.caption(
        "Diện tích = số lượt học; màu = tỷ lệ At-Risk trên miền 0–100%. "
        "Đổi lựa chọn phía trên để xem education, IMD, credits, age hoặc disability."
    )
    render_insight("INS-05")

    region_stats = (
        analysis.groupby("region", observed=True)
        .agg(
            attempts=("id_student", "size"),
            at_risk_count=("At_Risk", "sum"),
            at_risk_rate=("At_Risk", "mean"),
        )
        .reset_index()
        .sort_values("at_risk_rate", ascending=True)
    )
    bar = px.bar(
        region_stats,
        x="at_risk_rate",
        y="region",
        orientation="h",
        color="at_risk_rate",
        color_continuous_scale=RISK_SCALE,
        range_color=[0, 1],
        text="attempts",
        custom_data=["attempts", "at_risk_count"],
        labels={"at_risk_rate": "Tỷ lệ At-Risk", "region": "Vùng OULAD"},
        title="So sánh tỷ lệ At-Risk theo vùng",
    )
    bar.update_traces(
        texttemplate="N=%{text:,}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "Region=%{y}<br>At-Risk=%{x:.1%}<br>"
            "N=%{customdata[0]:,}<br>Số At-Risk=%{customdata[1]:,}<extra></extra>"
        )
    )
    bar.update_xaxes(tickformat=".0%", range=[0, 1])
    bar.update_layout(coloraxis_showscale=False)
    polish_figure(bar, height=610, legend="none")
    st.plotly_chart(bar, width="stretch")
    render_region_map(region_stats)
    render_insight("INS-06", map_pending=not REGION_GEOJSON_PATH.exists())
    st.caption(
        "Story transition: RQ1–RQ5 kết thúc ở các pattern quan sát. Trang Prediction "
        "tiếp theo đánh giá riêng liệu Logistic Regression có nhận diện sớm được hay không."
    )


def render_model_curves(split: str) -> None:
    curves = cached_model_table("model_curve_points.csv")
    curves = curves.loc[curves["dataset_split"].eq(split)].copy()
    curves["curve_key"] = (
        curves["curve"].astype(str).str.strip().str.lower().str.replace("-", "_", regex=False)
    )
    if curves.empty:
        st.info(f"Artifact ROC/PR hiện không có cho split={split}; bản công bố dùng test.")
        return
    figure = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("ROC curve", "Precision–Recall curve"),
    )
    roc = curves.loc[curves["curve_key"].eq("roc")]
    pr = curves.loc[curves["curve_key"].eq("precision_recall")]
    if roc.empty or pr.empty:
        st.error(
            "model_curve_points.csv thiếu ROC hoặc Precision-Recall cho split "
            f"{split}."
        )
        return
    figure.add_trace(
        go.Scatter(
            x=roc["x"],
            y=roc["y"],
            mode="lines",
            name="ROC",
            line={"color": "#2563EB", "width": 3},
            hovertemplate="FPR=%{x:.3f}<br>TPR=%{y:.3f}<extra>ROC</extra>",
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Mốc ngẫu nhiên",
            line={"color": "#94A3B8", "dash": "dash", "width": 2},
            hoverinfo="skip",
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Scatter(
            x=pr["x"],
            y=pr["y"],
            mode="lines",
            name="Precision–Recall",
            line={"color": "#DC2626", "width": 3},
            hovertemplate="Recall=%{x:.3f}<br>Precision=%{y:.3f}<extra>PR</extra>",
        ),
        row=1,
        col=2,
    )
    figure.update_xaxes(title_text="Tỷ lệ dương tính giả (FPR)", range=[0, 1], row=1, col=1)
    figure.update_yaxes(title_text="Tỷ lệ dương tính thật (TPR)", range=[0, 1], row=1, col=1)
    figure.update_xaxes(title_text="Độ bao phủ (Recall)", row=1, col=2)
    figure.update_yaxes(title_text="Độ chính xác cảnh báo (Precision)", row=1, col=2)
    figure.update_xaxes(range=[0, 1], row=1, col=2)
    figure.update_yaxes(range=[0, 1], row=1, col=2)
    figure.update_layout(title=f"Khả năng phân hạng — tập {split}")
    polish_figure(figure, height=500)
    figure.update_layout(
        margin={"l": 60, "r": 35, "t": 88, "b": 105},
        legend={
            "orientation": "h",
            "yanchor": "top",
            "y": -0.20,
            "xanchor": "center",
            "x": 0.5,
            "title_text": "",
        },
    )
    st.plotly_chart(figure, width="stretch")
    st.caption(
        "ROC đánh giá phân biệt trên mọi threshold; Precision–Recall tập trung hơn vào lớp At-Risk. Đường càng gần góc trên càng tốt."
    )


def render_prediction(
    modules: list[str], presentations: list[str], regions: list[str]
) -> None:
    render_page_header(
        "RQ6 · Dự báo",
        "Logistic Regression nhận diện sớm At-Risk tốt đến đâu?",
        "Đánh giá xác suất, threshold, lỗi phân loại, khả năng xếp hạng và calibration.",
        "Mặc định: test split · cutoff ngày 105 · không huấn luyện lại trong dashboard",
    )
    try:
        predictions = cached_predictions()
        metrics = cached_model_table("model_metrics.csv")
        verification = cached_model_table("model_verification.csv")
        intervals = cached_model_table("model_confidence_intervals.csv")
        calibration = cached_model_table("model_calibration.csv")
    except (FileNotFoundError, ValueError) as exc:
        st.error(str(exc))
        st.code("python -m src.at_risk_model", language="powershell")
        return

    if "status" not in verification or not verification["status"].eq("PASS").all():
        st.error("Model verification chưa PASS toàn bộ; không dùng output để nghiệm thu.")
        st.dataframe(verification, width="stretch", hide_index=True)
        return

    split = st.selectbox(
        "Tập đánh giá",
        ["test", "validation", "train"],
        index=0,
        help="Bằng chứng cuối và rubric mặc định dùng test split.",
    )
    model_rows = metrics.loc[
        metrics["model_name"].eq("logistic_regression")
        & metrics["dataset_split"].eq(split)
    ]
    if model_rows.empty:
        st.error(f"Không có metric Logistic Regression cho split={split}.")
        return
    metric = model_rows.iloc[0]
    first_metrics = st.columns(3)
    first_metrics[0].metric("Accuracy", format_percent(metric["accuracy"]))
    first_metrics[1].metric("Precision At-Risk", format_percent(metric["precision_at_risk"]))
    first_metrics[2].metric("Recall At-Risk", format_percent(metric["recall_at_risk"]))
    second_metrics = st.columns(3)
    second_metrics[0].metric("F1 At-Risk", format_percent(metric["f1_at_risk"]))
    second_metrics[1].metric("ROC-AUC", f"{metric['roc_auc']:.3f}")
    second_metrics[2].metric("PR-AUC", f"{metric['pr_auc']:.3f}")
    st.caption(
        f"Metric công bố cho {split} · model={metric['model_version']} · "
        f"cutoff={int(metric['cutoff_day'])} · threshold={metric['threshold']:.3f} · "
        f"N={int(metric['rows']):,}. Sidebar filters không viết lại metric này."
    )

    display = predictions.loc[predictions["dataset_split"].eq(split)].copy()
    display = filter_attempts(
        display, modules=modules, presentations=presentations, regions=regions
    )
    if display.empty:
        st.warning("Không có prediction row trong filter context hiện tại.")
        return
    st.caption(f"Tập dự báo đang trực quan: N={len(display):,} lượt học.")

    histogram = px.histogram(
        display,
        x="risk_probability",
        color="actual_status",
        color_discrete_map=RISK_COLORS,
        category_orders={"actual_status": STATUS_ORDER},
        nbins=30,
        barmode="overlay",
        opacity=0.7,
        labels={
            "risk_probability": "Xác suất At-Risk dự báo",
            "actual_status": "Kết quả thực tế",
            "count": "Số attempts",
        },
        title="Phân bố xác suất dự báo theo kết quả thực tế",
    )
    threshold = float(display["prediction_threshold"].iloc[0])
    histogram.add_vline(
        x=threshold,
        line_dash="dash",
        line_color=INK,
        line_width=2,
        annotation_text=f"Threshold = {threshold:.3f}",
        annotation_position="top right",
    )
    histogram.update_traces(
        marker={"line": {"color": "rgba(255,255,255,0.75)", "width": 0.5}},
        hovertemplate="Xác suất=%{x:.1%}<br>Số attempts=%{y}<extra></extra>",
    )
    histogram.update_xaxes(range=[0, 1], tickformat=".0%")
    polish_figure(histogram, height=500)
    st.plotly_chart(histogram, width="stretch")
    st.caption(
        "Đường đứt là threshold chọn trên validation. Bên phải threshold được phân lớp At-Risk; biểu đồ đang dùng filter context hiện tại."
    )

    confusion = (
        display.groupby(["actual_status", "predicted_status"], observed=True)
        .size()
        .rename("count")
        .reset_index()
    )
    matrix = (
        confusion.pivot(
            index="actual_status", columns="predicted_status", values="count"
        )
        .reindex(index=STATUS_ORDER, columns=STATUS_ORDER, fill_value=0)
        .fillna(0)
        .astype(int)
    )
    heatmap = go.Figure(
        data=go.Heatmap(
            z=matrix.values,
            x=matrix.columns,
            y=matrix.index,
            text=matrix.values,
            texttemplate="%{text:,}",
            textfont={"size": 18, "color": INK},
            colorscale=[[0, "#EFF6FF"], [1, "#60A5FA"]],
            showscale=False,
            hovertemplate="Thực tế=%{y}<br>Dự báo=%{x}<br>N=%{z:,}<extra></extra>",
        )
    )
    heatmap.update_layout(
        title="Ma trận nhầm lẫn trong filter hiện tại",
        xaxis_title="Dự báo",
        yaxis_title="Thực tế",
    )
    polish_figure(heatmap, height=470, legend="none")
    st.plotly_chart(heatmap, width="stretch")
    st.caption("Ô ngoài đường chéo là lỗi: False Positive và False Negative; N thay đổi theo sidebar filter.")

    render_model_curves(split)
    split_calibration = calibration.loc[calibration["dataset_split"].eq(split)]
    if split_calibration.empty:
        st.info(
            f"Artifact calibration hiện không có cho split={split}; bản công bố dùng test."
        )
    else:
        calibration_fig = px.scatter(
            split_calibration,
            x="mean_predicted_probability",
            y="observed_at_risk_rate",
            size="rows",
            text="probability_bin",
            labels={
                "mean_predicted_probability": "Xác suất dự báo trung bình",
                "observed_at_risk_rate": "Tỷ lệ At-Risk quan sát",
                "rows": "Số attempts",
            },
            title="Calibration: xác suất dự báo so với tỷ lệ quan sát",
        )
        calibration_fig.update_traces(
            selector={"mode": "markers+text"},
            marker={"color": "#2563EB", "line": {"color": "#FFFFFF", "width": 1.2}},
            textposition="top center",
            hovertemplate=(
                "Bin=%{text}<br>Xác suất TB=%{x:.1%}<br>At-Risk quan sát=%{y:.1%}"
                "<br>N=%{marker.size:,}<extra></extra>"
            ),
        )
        calibration_fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="lines",
                name="Calibration lý tưởng",
                line={"color": "#64748B", "dash": "dash", "width": 2},
                hoverinfo="skip",
            )
        )
        calibration_fig.update_xaxes(range=[0, 1], tickformat=".0%")
        calibration_fig.update_yaxes(range=[0, 1], tickformat=".0%")
        polish_figure(calibration_fig, height=520)
        st.plotly_chart(calibration_fig, width="stretch")
        st.caption("Điểm càng gần đường chéo, xác suất model càng gần tỷ lệ At-Risk quan sát trong từng bin.")

    split_intervals = intervals.loc[intervals["dataset_split"].eq(split)].copy()
    if not split_intervals.empty:
        st.subheader("Khoảng tin cậy bootstrap 95%")
        interval_display = split_intervals[
            ["metric", "point_estimate", "lower_95", "upper_95"]
        ].copy()
        interval_display.columns = ["Metric", "Ước lượng", "CI 95% thấp", "CI 95% cao"]
        st.dataframe(
            interval_display.style.format(
                {"Ước lượng": "{:.3f}", "CI 95% thấp": "{:.3f}", "CI 95% cao": "{:.3f}"}
            ),
            width="stretch",
            hide_index=True,
        )

    st.info(
        "Accuracy mô tả tỷ lệ dự đoán đúng; Precision mô tả độ đúng của cảnh báo; "
        "Recall mô tả tỷ lệ At-Risk được bắt; F1 cân bằng Precision/Recall; ROC/PR-AUC "
        "đánh giá xếp hạng; calibration kiểm tra xác suất. Model hỗ trợ ưu tiên theo dõi, "
        "không tự động quyết định một người sẽ thất bại."
    )


def main() -> None:
    apply_dashboard_css()
    try:
        analysis = cached_analysis_data()
    except (FileNotFoundError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

    page, modules, presentations, regions = sidebar_filters(analysis)
    filtered_analysis = filter_attempts(
        analysis, modules=modules, presentations=presentations, regions=regions
    )
    render_filter_context(modules, presentations, regions, len(filtered_analysis))
    if filtered_analysis.empty:
        st.warning("Filter context không có learning attempt.")
        st.stop()

    if page == "Overview":
        render_overview(filtered_analysis)
    elif page == "Factor Analysis":
        try:
            snapshot = cached_snapshot()
        except (FileNotFoundError, ValueError) as exc:
            st.error(str(exc))
            st.code("python -m src.at_risk_model", language="powershell")
            st.stop()
        filtered_snapshot = filter_attempts(
            snapshot, modules=modules, presentations=presentations, regions=regions
        )
        if filtered_snapshot.empty:
            st.warning("Filter context không có eligible attempt tại ngày 105.")
            st.stop()
        render_factor_analysis(filtered_snapshot)
    elif page == "Risk Analysis":
        try:
            snapshot = cached_snapshot()
        except (FileNotFoundError, ValueError) as exc:
            st.error(str(exc))
            st.code("python -m src.at_risk_model", language="powershell")
            st.stop()
        filtered_snapshot = filter_attempts(
            snapshot, modules=modules, presentations=presentations, regions=regions
        )
        if filtered_snapshot.empty:
            st.warning("Filter context không có eligible attempt tại ngày 105.")
            st.stop()
        render_risk_analysis(filtered_analysis, filtered_snapshot)
    else:
        render_prediction(modules, presentations, regions)


if __name__ == "__main__":
    main()
