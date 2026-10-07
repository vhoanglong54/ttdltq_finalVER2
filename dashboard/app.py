"""Two-page OULAD learning analytics dashboard.

Page 1 explores academic outcomes and learning behaviour. Page 2 combines a
multivariate risk matrix with the verified Logistic Regression early-warning
output. The app reads reproducible processed artifacts; it never trains the
model or joins the multi-million-row VLE table while rendering.
"""

from __future__ import annotations

import html
import json
from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard_data import (
    REGION_GEOJSON_PATH,
    compute_kpis,
    filter_attempts,
    load_analysis_data,
    load_dashboard_mart,
    load_feature_snapshot,
    load_model_table,
    load_predictions,
)


PAGE_OPTIONS = ["Academic Insight & Behavior", "Risk Matrix & Early Warning"]
PAGE_LABELS = {
    "Academic Insight & Behavior": "1 · Học tập & hành vi",
    "Risk Matrix & Early Warning": "2 · Rủi ro & cảnh báo",
}
ATTEMPT_KEY = ["code_module", "code_presentation", "id_student"]
RESULT_ORDER = ["Distinction", "Pass", "Fail", "Withdrawn"]
RESULT_COLORS = {
    "Distinction": "#0F766E",
    "Pass": "#2563EB",
    "Fail": "#F97316",
    "Withdrawn": "#DC2626",
}
RISK_COLORS = {"Not-At-Risk": "#2563EB", "At-Risk": "#DC2626"}
LEVEL_ORDER = ["High", "Medium", "Low"]
LEVEL_LABELS = {
    "High": "High · Nguy hiểm",
    "Medium": "Medium · Cảnh báo",
    "Low": "Low · An toàn",
}
INK = "#0F172A"
MUTED = "#475569"
GRID = "#E2E8F0"
PANEL = "#FFFFFF"
RISK_SCALE = ["#ECFDF5", "#FEF3C7", "#FDBA74", "#EF4444", "#991B1B"]


st.set_page_config(
    page_title="OULAD Learning Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_dashboard_css() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #F8FAFC; }
        .block-container { padding-top: 1.35rem; padding-bottom: 3rem; max-width: 1520px; }
        h1, h2, h3 { color: #0F172A; letter-spacing: -0.025em; }
        p, label, .stCaption { color: #334155; }
        [data-testid="stSidebar"] { border-right: 1px solid #E2E8F0; }
        [data-testid="stMetric"] {
            background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
            padding: 0.85rem 1rem; box-shadow: 0 1px 2px rgba(15,23,42,.04);
        }
        [data-testid="stMetricLabel"] { color: #475569; }
        [data-testid="stMetricValue"] { color: #0F172A; }
        [data-testid="stPlotlyChart"] {
            background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px;
            padding: .3rem; box-shadow: 0 1px 3px rgba(15,23,42,.05);
        }
        .page-kicker {
            color: #2563EB; font-size: .78rem; font-weight: 800;
            letter-spacing: .08em; text-transform: uppercase; margin-bottom: .15rem;
        }
        .page-subtitle { color: #475569; font-size: 1.02rem; margin-top: -.35rem; }
        .scope-note {
            display: inline-block; background: #EFF6FF; color: #1E40AF;
            border: 1px solid #BFDBFE; border-radius: 999px; padding: .28rem .7rem;
            font-size: .82rem; font-weight: 650; margin: .2rem 0 .8rem 0;
        }
        .story-card {
            background: linear-gradient(135deg,#EFF6FF 0%,#FFFFFF 100%);
            border: 1px solid #BFDBFE; border-left: 5px solid #2563EB;
            border-radius: 12px; padding: .9rem 1.05rem; margin: .55rem 0;
        }
        .story-card h3 { margin: 0 0 .35rem 0; font-size: 1.1rem; }
        .story-card ul { margin: .15rem 0 0 1.1rem; padding: 0; }
        .story-card li { margin: .22rem 0; color: #1E293B; }
        .active-filter {
            background: #FFF7ED; color: #9A3412; border: 1px solid #FDBA74;
            border-radius: 9px; padding: .55rem .75rem; margin: .15rem 0 .65rem 0;
        }
        .definition-box {
            background: #F0FDFA; border: 1px solid #99F6E4; border-left: 5px solid #0F766E;
            border-radius: 12px; padding: .9rem 1.05rem; margin: .4rem 0 .9rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def polish_figure(
    figure: go.Figure,
    *,
    height: int,
    legend: str = "top",
    hovermode: str | bool = "closest",
) -> go.Figure:
    figure.update_layout(
        template="plotly_white",
        height=height,
        margin={"l": 60, "r": 35, "t": 78, "b": 60},
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font={"family": "Arial, sans-serif", "size": 13, "color": INK},
        title={"x": .02, "xanchor": "left", "font": {"size": 19, "color": INK}},
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
                "bgcolor": "rgba(255,255,255,.88)",
            }
        )
    elif legend == "none":
        figure.update_layout(showlegend=False)
    return figure


def render_header(kicker: str, title: str, subtitle: str, scope: str) -> None:
    st.markdown(
        f'<div class="page-kicker">{html.escape(kicker)}</div>',
        unsafe_allow_html=True,
    )
    st.title(title)
    st.markdown(
        f'<div class="page-subtitle">{html.escape(subtitle)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="scope-note">{html.escape(scope)}</div>',
        unsafe_allow_html=True,
    )


def render_story(title: str, bullets: list[str]) -> None:
    items = "".join(f"<li>{html.escape(item)}</li>" for item in bullets)
    st.markdown(
        f'<div class="story-card"><h3>{html.escape(title)}</h3><ul>{items}</ul></div>',
        unsafe_allow_html=True,
    )


def format_percent(value: float) -> str:
    return "—" if pd.isna(value) else f"{value:.1%}"


def chart_points(event: Any) -> list[Any]:
    if event is None:
        return []
    try:
        return list(event.selection.points)
    except (AttributeError, KeyError, TypeError):
        try:
            return list(event["selection"]["points"])
        except (KeyError, TypeError):
            return []


def point_value(point: Any, field: str) -> Any:
    try:
        return point.get(field)
    except AttributeError:
        try:
            return point[field]
        except (KeyError, TypeError):
            return None


@st.cache_data(show_spinner=False)
def analysis_data() -> pd.DataFrame:
    return load_analysis_data()


@st.cache_data(show_spinner=False)
def feature_snapshot() -> pd.DataFrame:
    return load_feature_snapshot()


@st.cache_data(show_spinner=False)
def predictions() -> pd.DataFrame:
    return load_predictions()


@st.cache_data(show_spinner=False)
def model_table(filename: str) -> pd.DataFrame:
    return load_model_table(filename)


@st.cache_data(show_spinner=False)
def dashboard_mart(filename: str, required: tuple[str, ...]) -> pd.DataFrame:
    return load_dashboard_mart(filename, set(required))


def filter_mart(
    frame: pd.DataFrame,
    modules: list[str],
    presentations: list[str],
    genders: list[str],
    regions: list[str],
) -> pd.DataFrame:
    mask = pd.Series(True, index=frame.index)
    for column, values in (
        ("code_module", modules),
        ("code_presentation", presentations),
        ("gender", genders),
        ("region", regions),
    ):
        if values and column in frame:
            mask &= frame[column].isin(values)
    return frame.loc[mask].copy()


def page_navigation() -> str:
    st.sidebar.title("OULAD Dashboard")
    st.sidebar.caption("Python · Streamlit · Plotly")
    page = st.sidebar.radio(
        "Điều hướng",
        PAGE_OPTIONS,
        format_func=lambda value: PAGE_LABELS[value],
    )
    st.sidebar.divider()
    with st.sidebar.expander("Định nghĩa nhanh"):
        st.markdown(
            "- **At-Risk:** kết quả cuối là Fail hoặc Withdrawn.\n"
            "- **Lượt học:** một sinh viên trong một module–presentation.\n"
            "- **Ngày 105:** thời điểm chốt dữ liệu đầu vào cho model.\n"
            "- Kết quả thể hiện liên hệ, không khẳng định nhân quả."
        )
    return page


def page_one_filters(frame: pd.DataFrame) -> tuple[list[str], list[str], list[str]]:
    st.subheader("Bộ lọc phân tích")
    columns = st.columns(3)
    modules = columns[0].multiselect(
        "Môn học · code_module",
        sorted(frame["code_module"].dropna().unique()),
        key="academic_modules",
        placeholder="Tất cả môn học",
    )
    available = frame.loc[frame["code_module"].isin(modules)] if modules else frame
    presentations = columns[1].multiselect(
        "Học kỳ · code_presentation",
        sorted(available["code_presentation"].dropna().unique()),
        key="academic_presentations",
        placeholder="Tất cả học kỳ",
    )
    genders = columns[2].multiselect(
        "Giới tính · gender",
        sorted(frame["gender"].dropna().unique()),
        key="academic_genders",
        placeholder="Tất cả giới tính",
    )
    return modules, presentations, genders


def render_academic_kpis(frame: pd.DataFrame) -> None:
    kpis = compute_kpis(frame)
    pass_rate = frame["final_result"].isin(["Pass", "Distinction"]).mean()
    cards = st.columns(4)
    cards[0].metric("Tổng sinh viên", f"{kpis.learners:,}")
    cards[1].metric("Điểm trung bình", f"{kpis.average_assessment_score:.1f}")
    cards[2].metric("Tỷ lệ qua môn", format_percent(pass_rate))
    cards[3].metric("Tỷ lệ At-Risk", format_percent(kpis.at_risk_rate))


def render_region_map(base_frame: pd.DataFrame, active_region: str | None) -> None:
    stats = (
        base_frame.groupby("region", observed=True)
        .agg(
            attempts=("id_student", "size"),
            at_risk_count=("At_Risk", "sum"),
            at_risk_rate=("At_Risk", "mean"),
        )
        .reset_index()
    )
    with REGION_GEOJSON_PATH.open("r", encoding="utf-8") as handle:
        geojson = json.load(handle)
    figure = px.choropleth(
        stats,
        geojson=geojson,
        locations="region",
        featureidkey="properties.region",
        color="at_risk_rate",
        color_continuous_scale=RISK_SCALE,
        range_color=(0, 1),
        custom_data=["region", "attempts", "at_risk_count", "at_risk_rate"],
        title="1 · Tỷ lệ At-Risk theo vùng cư trú",
    )
    figure.update_geos(fitbounds="locations", visible=False, bgcolor="#FFFFFF")
    figure.update_traces(
        marker_line_color="#FFFFFF",
        marker_line_width=1.0,
        hovertemplate=(
            "Vùng=%{customdata[0]}<br>At-Risk=%{customdata[3]:.1%}"
            "<br>Lượt học=%{customdata[1]:,}<br>Số At-Risk=%{customdata[2]:,}<extra></extra>"
        ),
    )
    figure.update_layout(
        coloraxis_colorbar={"title": "At-Risk", "tickformat": ".0%"}
    )
    polish_figure(figure, height=565, legend="none")
    event = st.plotly_chart(
        figure,
        width="stretch",
        on_select="rerun",
        selection_mode="points",
        key=f"academic_region_map_{st.session_state.get('map_key_version', 0)}",
    )
    points = chart_points(event)
    if points:
        selected = point_value(points[0], "location")
        if selected is None:
            custom = point_value(points[0], "customdata")
            selected = custom[0] if custom else None
        if selected and str(selected) != active_region:
            st.session_state["academic_region"] = str(selected)
            st.rerun()
    st.caption(
        "Bấm một vùng để lọc KPI và bốn biểu đồ còn lại. Màu đậm hơn = tỷ lệ At-Risk cao hơn; "
        "màu không phản ánh quy mô mẫu."
    )


def outcome_percentages(frame: pd.DataFrame, group_column: str) -> pd.DataFrame:
    counts = (
        frame.groupby([group_column, "final_result"], observed=True)
        .size()
        .rename("attempts")
        .reset_index()
    )
    counts["share"] = counts["attempts"] / counts.groupby(group_column)[
        "attempts"
    ].transform("sum")
    counts["final_result"] = pd.Categorical(
        counts["final_result"], RESULT_ORDER, ordered=True
    )
    return counts.sort_values([group_column, "final_result"])


def render_outcome_drill(frame: pd.DataFrame) -> None:
    valid_modules = set(frame["code_module"].astype(str))
    selected_module = st.session_state.get("outcome_drill_module")
    if selected_module not in valid_modules:
        selected_module = None
        st.session_state["outcome_drill_module"] = None

    if selected_module:
        top = st.columns([4, 1])
        top[0].markdown(
            f"**Drill-down:** Tất cả môn học → `{selected_module}` → Học kỳ"
        )
        if top[1].button(
            "↑ Quay lại môn học", key="reset_outcome_drill", width="stretch"
        ):
            st.session_state["outcome_drill_module"] = None
            st.session_state["outcome_key_version"] = (
                st.session_state.get("outcome_key_version", 0) + 1
            )
            st.rerun()
        chart_frame = frame.loc[frame["code_module"].eq(selected_module)]
        group_column = "code_presentation"
        title = f"2 · Cơ cấu kết quả theo học kỳ của {selected_module}"
        y_label = "Học kỳ"
    else:
        st.caption(
            "Drill-down: Tất cả môn học. Bấm một thanh để xem các học kỳ bên trong."
        )
        chart_frame = frame
        group_column = "code_module"
        title = "2 · Cơ cấu kết quả theo môn học"
        y_label = "Môn học"

    data = outcome_percentages(chart_frame, group_column)
    figure = px.bar(
        data,
        x="share",
        y=group_column,
        color="final_result",
        orientation="h",
        barmode="stack",
        category_orders={"final_result": RESULT_ORDER},
        color_discrete_map=RESULT_COLORS,
        custom_data=["attempts"],
        labels={
            "share": "Tỷ trọng kết quả",
            group_column: y_label,
            "final_result": "Kết quả",
        },
        title=title,
    )
    figure.update_traces(
        texttemplate="%{x:.0%}",
        textposition="inside",
        hovertemplate=(
            f"{y_label}=%{{y}}<br>Kết quả=%{{fullData.name}}"
            "<br>Tỷ trọng=%{x:.1%}<br>N=%{customdata[0]:,}<extra></extra>"
        ),
    )
    figure.update_xaxes(tickformat=".0%", range=[0, 1])
    polish_figure(figure, height=470)
    event = st.plotly_chart(
        figure,
        width="stretch",
        on_select="rerun" if not selected_module else "ignore",
        selection_mode="points",
        key=(
            f"outcome_drill_{selected_module or 'module'}_"
            f"{st.session_state.get('outcome_key_version', 0)}"
        ),
    )
    if not selected_module:
        points = chart_points(event)
        if points:
            module = point_value(points[0], "y")
            if module in valid_modules:
                st.session_state["outcome_drill_module"] = str(module)
                st.rerun()


def render_vle_timeline(
    frame: pd.DataFrame,
    modules: list[str],
    presentations: list[str],
    genders: list[str],
    regions: list[str],
) -> tuple[float, float]:
    daily = dashboard_mart(
        "vle_daily_profile.csv.gz",
        (
            "code_module",
            "code_presentation",
            "gender",
            "region",
            "At_Risk",
            "date",
            "sum_click",
        ),
    )
    daily = filter_mart(daily, modules, presentations, genders, regions)
    totals = frame.groupby("At_Risk").size().rename("attempts")
    daily = daily.groupby(["At_Risk", "date"], as_index=False)["sum_click"].sum()
    if daily.empty:
        st.info("Không có sự kiện VLE trong phạm vi lọc.")
        return float("nan"), float("nan")

    dates = np.arange(int(daily["date"].min()), int(daily["date"].max()) + 1)
    statuses = sorted(totals.index.tolist())
    grid = pd.MultiIndex.from_product(
        [statuses, dates], names=["At_Risk", "date"]
    ).to_frame(index=False)
    daily = grid.merge(daily, on=["At_Risk", "date"], how="left").fillna(
        {"sum_click": 0}
    )
    daily = daily.merge(totals, on="At_Risk", how="left")
    daily["avg_sum_click"] = daily["sum_click"] / daily["attempts"]
    daily = daily.sort_values(["At_Risk", "date"])
    daily["avg_click_7d"] = daily.groupby("At_Risk")["avg_sum_click"].transform(
        lambda values: values.rolling(7, min_periods=1).mean()
    )
    daily["Nhóm"] = daily["At_Risk"].map(
        {0: "Not-At-Risk", 1: "At-Risk"}
    )

    figure = px.line(
        daily,
        x="date",
        y="avg_click_7d",
        color="Nhóm",
        category_orders={"Nhóm": ["Not-At-Risk", "At-Risk"]},
        color_discrete_map=RISK_COLORS,
        labels={
            "date": "Ngày tương đối từ khi môn học bắt đầu",
            "avg_click_7d": "Clicks trung bình / lượt học / ngày",
        },
        title="3 · Nhịp tương tác VLE: At-Risk so với Not-At-Risk",
    )
    figure.update_traces(
        line={"width": 3},
        hovertemplate="Ngày=%{x}<br>TB 7 ngày=%{y:.2f} clicks<extra></extra>",
    )

    deadlines = dashboard_mart(
        "assessment_deadlines.csv",
        (
            "code_module",
            "code_presentation",
            "assessment_type",
            "due_date",
            "weight",
        ),
    )
    if modules:
        deadlines = deadlines.loc[deadlines["code_module"].isin(modules)]
    if presentations:
        deadlines = deadlines.loc[
            deadlines["code_presentation"].isin(presentations)
        ]
    milestones = (
        deadlines.dropna(subset=["due_date"])
        .groupby("due_date", as_index=False)["weight"]
        .sum()
        .sort_values("weight", ascending=False)
        .head(3)
        .sort_values("due_date")
    )
    for row in milestones.itertuples(index=False):
        figure.add_vline(
            x=float(row.due_date),
            line_dash="dot",
            line_color="#64748B",
            line_width=1.2,
        )
    polish_figure(figure, height=505, hovermode="x unified")
    st.plotly_chart(figure, width="stretch")
    milestone_days = ", ".join(str(int(value)) for value in milestones["due_date"])
    st.caption(
        "Đường là trung bình trượt 7 ngày; mẫu số gồm mọi lượt học trong từng nhóm, kể cả ngày không click. "
        f"Vạch chấm đánh dấu ba hạn nộp trọng số lớn nhất: ngày {milestone_days}."
    )
    means = frame.groupby("At_Risk")["vle_total_clicks_all_time"].mean()
    return float(means.get(1, np.nan)), float(means.get(0, np.nan))


def render_submission_scatter(
    modules: list[str],
    presentations: list[str],
    genders: list[str],
    regions: list[str],
) -> float:
    submissions = dashboard_mart(
        "assessment_submissions.csv.gz",
        (
            "code_module",
            "code_presentation",
            "id_student",
            "gender",
            "region",
            "num_of_prev_attempts",
            "At_Risk",
            "submission_delay",
            "score",
        ),
    )
    submissions = filter_mart(
        submissions, modules, presentations, genders, regions
    ).dropna(subset=["submission_delay", "score"])
    if submissions.empty:
        st.info("Không có bài nộp có đủ ngày hạn và điểm trong phạm vi lọc.")
        return float("nan")

    sample = submissions.sample(min(4500, len(submissions)), random_state=42)
    figure = go.Figure()
    for at_risk, label in ((0, "Not-At-Risk"), (1, "At-Risk")):
        group = sample.loc[sample["At_Risk"].eq(at_risk)]
        custom = np.column_stack(
            [
                group["id_student"],
                group["num_of_prev_attempts"],
                group["code_module"],
                group["code_presentation"],
            ]
        )
        figure.add_trace(
            go.Scattergl(
                x=group["submission_delay"],
                y=group["score"],
                mode="markers",
                name=label,
                customdata=custom,
                marker={
                    "size": 7 + 2 * group["num_of_prev_attempts"].clip(upper=6),
                    "color": RISK_COLORS[label],
                    "opacity": .42,
                    "line": {"color": "#FFFFFF", "width": .4},
                },
                hovertemplate=(
                    "Student=%{customdata[0]}<br>Module=%{customdata[2]}-%{customdata[3]}"
                    "<br>Trễ=%{x:.0f} ngày<br>Điểm=%{y:.1f}"
                    "<br>Lần học trước=%{customdata[1]:.0f}<extra></extra>"
                ),
            )
        )
    correlation = float(
        submissions[["submission_delay", "score"]].corr().iloc[0, 1]
    )
    if submissions["submission_delay"].nunique() > 1:
        slope, intercept = np.polyfit(
            submissions["submission_delay"], submissions["score"], 1
        )
        x_line = np.array(
            [
                submissions["submission_delay"].min(),
                submissions["submission_delay"].max(),
            ]
        )
        figure.add_trace(
            go.Scatter(
                x=x_line,
                y=intercept + slope * x_line,
                mode="lines",
                name="Trendline toàn bộ",
                line={"color": INK, "width": 3, "dash": "dash"},
                hoverinfo="skip",
            )
        )
    figure.add_vline(
        x=0,
        line_color="#64748B",
        line_dash="dot",
    )
    figure.update_layout(
        title="4 · Độ trễ nộp bài và điểm assessment",
        xaxis_title="Số ngày nộp trễ (âm = nộp sớm)",
        yaxis_title="Điểm assessment",
    )
    figure.update_yaxes(range=[-2, 102])
    polish_figure(figure, height=535)
    st.plotly_chart(figure, width="stretch")
    st.caption(
        f"Trendline và hệ số tương quan dùng toàn bộ {len(submissions):,} bài hợp lệ; "
        f"đồ thị lấy mẫu cố định {len(sample):,} điểm để dễ đọc. Vạch dọc tại 0 là đúng hạn; "
        "kích thước điểm tăng theo số lần học trước."
    )
    return correlation


def render_activity_treemap(
    modules: list[str],
    presentations: list[str],
    genders: list[str],
    regions: list[str],
) -> tuple[str, float]:
    activity = dashboard_mart(
        "vle_activity_summary.csv.gz",
        (
            "code_module",
            "code_presentation",
            "gender",
            "region",
            "activity_type",
            "sum_click",
        ),
    )
    activity = filter_mart(activity, modules, presentations, genders, regions)
    activity = activity.groupby("activity_type", as_index=False)["sum_click"].sum()
    if activity.empty:
        st.info("Không có click VLE trong phạm vi lọc.")
        return "—", float("nan")
    total = activity["sum_click"].sum()
    activity["share"] = activity["sum_click"] / total
    figure = px.treemap(
        activity,
        path=[px.Constant("Tất cả tài nguyên VLE"), "activity_type"],
        values="sum_click",
        color="sum_click",
        color_continuous_scale=["#DBEAFE", "#2563EB", "#1E3A8A"],
        custom_data=["sum_click", "share"],
        title="5 · Tài nguyên nào thu hút nhiều tương tác nhất?",
    )
    figure.update_traces(
        marker={"line": {"color": "#FFFFFF", "width": 1.5}},
        texttemplate="<b>%{label}</b><br>%{customdata[1]:.1%}",
        hovertemplate=(
            "Loại=%{label}<br>Clicks=%{customdata[0]:,}"
            "<br>Tỷ trọng=%{customdata[1]:.1%}<extra></extra>"
        ),
    )
    figure.update_layout(coloraxis_showscale=False)
    polish_figure(figure, height=520, legend="none")
    st.plotly_chart(figure, width="stretch")
    st.caption(
        "Diện tích và độ đậm đều biểu diễn tổng lượt click; tỷ trọng tính trong phạm vi lọc hiện tại."
    )
    top = activity.sort_values("sum_click", ascending=False).iloc[0]
    return str(top["activity_type"]), float(top["share"])


def render_academic_page() -> None:
    render_header(
        "Trang 1 · Academic Insight & Behavior",
        "Khám phá yếu tố học tập và hành vi",
        "Nhận diện diện mạo người học, địa bàn cư trú và các hành vi liên quan đến kết quả học tập.",
        "Phạm vi mô tả toàn khóa · một dòng dữ liệu chính = một learning attempt",
    )
    frame = analysis_data()
    modules, presentations, genders = page_one_filters(frame)
    base = filter_attempts(
        frame, modules=modules, presentations=presentations, genders=genders
    )
    if base.empty:
        st.warning("Bộ lọc hiện tại không có lượt học.")
        return

    active_region = st.session_state.get("academic_region")
    valid_regions = set(base["region"].dropna().astype(str))
    if active_region not in valid_regions:
        active_region = None
        st.session_state["academic_region"] = None
    effective = filter_attempts(
        base, regions=[active_region] if active_region else None
    )

    if active_region:
        notice = st.columns([4, 1])
        notice[0].markdown(
            f'<div class="active-filter"><b>Cross-filter từ bản đồ:</b> {html.escape(active_region)}</div>',
            unsafe_allow_html=True,
        )
        if notice[1].button(
            "Bỏ lọc vùng", key="clear_academic_region", width="stretch"
        ):
            st.session_state["academic_region"] = None
            st.session_state["map_key_version"] = (
                st.session_state.get("map_key_version", 0) + 1
            )
            st.rerun()
    render_academic_kpis(effective)
    st.caption(
        f"Phạm vi hiện tại: {len(effective):,} lượt học · "
        f"{effective['id_student'].nunique():,} sinh viên"
        + (f" · vùng {active_region}" if active_region else " · tất cả vùng")
    )

    st.subheader("Địa bàn và kết quả học tập")
    render_region_map(base, active_region)
    render_outcome_drill(effective)

    st.subheader("Hành vi học tập")
    selected_regions = [active_region] if active_region else []
    at_risk_clicks, not_risk_clicks = render_vle_timeline(
        effective, modules, presentations, genders, selected_regions
    )
    correlation = render_submission_scatter(
        modules, presentations, genders, selected_regions
    )
    top_activity, top_share = render_activity_treemap(
        modules, presentations, genders, selected_regions
    )

    risk_rate = effective["At_Risk"].mean()
    pass_rate = effective["final_result"].isin(["Pass", "Distinction"]).mean()
    click_message = (
        f"At-Risk trung bình {at_risk_clicks:,.0f} clicks/lượt học, so với "
        f"{not_risk_clicks:,.0f} ở Not-At-Risk."
        if pd.notna(at_risk_clicks) and pd.notna(not_risk_clicks)
        else "Chưa đủ dữ liệu VLE để so sánh hai nhóm."
    )
    corr_message = (
        f"Độ trễ và điểm có tương quan Pearson r={correlation:.2f}; đây là liên hệ, không phải quan hệ nhân quả."
        if pd.notna(correlation)
        else "Chưa đủ bài nộp để tính tương quan độ trễ–điểm."
    )
    render_story(
        "Câu chuyện dữ liệu · Trang 1",
        [
            f"Trong phạm vi đang xem, tỷ lệ qua môn là {pass_rate:.1%} và At-Risk là {risk_rate:.1%}.",
            click_message,
            f"{corr_message} Tài nguyên dẫn đầu là {top_activity} ({top_share:.1%} tổng click).",
        ],
    )


def prepare_risk_frame() -> pd.DataFrame:
    prediction = predictions().loc[
        lambda data: data["dataset_split"].eq("test")
    ].copy()
    snapshot = feature_snapshot()[
        ATTEMPT_KEY
        + [
            "highest_education",
            "num_of_prev_attempts",
            "assessment_weighted_score_cutoff",
        ]
    ]
    frame = prediction.merge(
        snapshot, on=ATTEMPT_KEY, how="left", validate="one_to_one"
    )
    frame["imd_band"] = (
        frame["imd_band"].replace({"10-20": "10-20%"}).fillna("Không xác định")
    )
    frame["highest_education"] = frame["highest_education"].fillna(
        "Không xác định"
    )
    frame["risk_level"] = np.select(
        [frame["risk_probability"].ge(.7), frame["risk_probability"].ge(.4)],
        ["High", "Medium"],
        default="Low",
    )
    return frame


def imd_sort_key(value: str) -> tuple[int, str]:
    if value == "Không xác định":
        return (999, value)
    try:
        return (int(value.split("-")[0].replace("%", "")), value)
    except ValueError:
        return (998, value)


def page_two_filters(frame: pd.DataFrame) -> tuple[list[str], list[str]]:
    st.subheader("Bộ lọc can thiệp")
    columns = st.columns(2)
    levels = columns[0].multiselect(
        "Risk Level",
        LEVEL_ORDER,
        format_func=lambda value: LEVEL_LABELS[value],
        key="risk_levels",
        placeholder="Tất cả mức rủi ro",
    )
    imd_options = sorted(
        frame["imd_band"].astype(str).unique(), key=imd_sort_key
    )
    imd_bands = columns[1].multiselect(
        "Thu nhập khu vực · imd_band",
        imd_options,
        key="risk_imd_bands",
        placeholder="Tất cả nhóm IMD",
    )
    return levels, imd_bands


def render_model_kpis(frame: pd.DataFrame) -> tuple[float, float, int]:
    accuracy = frame["actual_at_risk"].eq(frame["predicted_at_risk"]).mean()
    actual_positive = frame["actual_at_risk"].eq(1)
    recall = (
        frame.loc[actual_positive, "predicted_at_risk"].eq(1).mean()
        if actual_positive.any()
        else float("nan")
    )
    high_count = int(frame["risk_level"].eq("High").sum())
    cards = st.columns(3)
    cards[0].metric("Model Accuracy", format_percent(accuracy))
    cards[1].metric("Recall At-Risk", format_percent(recall))
    cards[2].metric("Cần can thiệp khẩn cấp", f"{high_count:,}")
    return float(accuracy), float(recall), high_count


def render_interaction_heatmap(
    frame: pd.DataFrame,
) -> tuple[str, str, float, int]:
    grouped = (
        frame.groupby(["highest_education", "imd_band"], observed=True)
        .agg(
            at_risk_rate=("actual_at_risk", "mean"),
            attempts=("id_student", "size"),
        )
        .reset_index()
    )
    education_order = [
        value
        for value in [
            "No Formal quals",
            "Lower Than A Level",
            "A Level or Equivalent",
            "HE Qualification",
            "Post Graduate Qualification",
            "Không xác định",
        ]
        if value in set(grouped["highest_education"])
    ]
    imd_order = sorted(
        grouped["imd_band"].astype(str).unique(), key=imd_sort_key
    )
    rate = grouped.pivot(
        index="highest_education", columns="imd_band", values="at_risk_rate"
    ).reindex(index=education_order, columns=imd_order)
    count = (
        grouped.pivot(
            index="highest_education", columns="imd_band", values="attempts"
        )
        .reindex(index=education_order, columns=imd_order)
        .fillna(0)
    )
    text = np.empty(rate.shape, dtype=object)
    for row in range(rate.shape[0]):
        for column in range(rate.shape[1]):
            value = rate.iloc[row, column]
            text[row, column] = (
                "—"
                if pd.isna(value)
                else f"{value:.0%}<br>N={int(count.iloc[row, column]):,}"
            )
    figure = go.Figure(
        go.Heatmap(
            z=rate.values,
            x=rate.columns,
            y=rate.index,
            text=text,
            texttemplate="%{text}",
            customdata=count.values,
            colorscale=RISK_SCALE,
            zmin=0,
            zmax=1,
            colorbar={"title": "At-Risk", "tickformat": ".0%"},
            hovertemplate=(
                "Học vấn=%{y}<br>IMD=%{x}<br>At-Risk=%{z:.1%}"
                "<br>N=%{customdata:,}<extra></extra>"
            ),
        )
    )
    figure.update_layout(
        title="6 · Tương tác giữa học vấn trước đó và kinh tế khu vực",
        xaxis_title="Mức thu nhập khu vực · imd_band",
        yaxis_title="Học vấn trước đó",
    )
    polish_figure(figure, height=535, legend="none")
    st.plotly_chart(figure, width="stretch")
    st.caption(
        "Mỗi ô là một tổ hợp hai yếu tố; màu = tỷ lệ At-Risk thực tế, nhãn N giúp tránh kết luận từ nhóm quá nhỏ."
    )
    eligible = grouped.loc[grouped["attempts"].ge(30)].sort_values(
        "at_risk_rate", ascending=False
    )
    top = (
        eligible.iloc[0]
        if not eligible.empty
        else grouped.sort_values("at_risk_rate", ascending=False).iloc[0]
    )
    return (
        str(top["highest_education"]),
        str(top["imd_band"]),
        float(top["at_risk_rate"]),
        int(top["attempts"]),
    )


def render_attempt_boxplot(frame: pd.DataFrame) -> tuple[float, float]:
    data = frame.dropna(subset=["assessment_weighted_score_cutoff"]).copy()
    data["previous_attempt_group"] = np.where(
        data["num_of_prev_attempts"].ge(3),
        "3+",
        data["num_of_prev_attempts"].astype(int).astype(str),
    )
    order = [
        value
        for value in ["0", "1", "2", "3+"]
        if value in set(data["previous_attempt_group"])
    ]
    figure = px.box(
        data,
        x="previous_attempt_group",
        y="assessment_weighted_score_cutoff",
        color="previous_attempt_group",
        category_orders={"previous_attempt_group": order},
        color_discrete_sequence=["#93C5FD", "#60A5FA", "#F59E0B", "#DC2626"],
        points="outliers",
        labels={
            "previous_attempt_group": "Số lần học module trước đó",
            "assessment_weighted_score_cutoff": "Điểm assessment có trọng số đến ngày 105",
        },
        title="7 · Phân bố điểm theo số lần học trước",
    )
    figure.update_traces(
        hovertemplate="Nhóm=%{x}<br>Điểm=%{y:.1f}<extra></extra>"
    )
    polish_figure(figure, height=500, legend="none")
    st.plotly_chart(figure, width="stretch")
    st.caption(
        "Nhóm 3+ gộp các giá trị từ 3 đến 6 để giữ cỡ mẫu; điểm chỉ dùng dữ liệu có trước hoặc tại ngày 105."
    )
    medians = data.groupby("previous_attempt_group", observed=True)[
        "assessment_weighted_score_cutoff"
    ].median()
    return float(medians.get("0", np.nan)), float(medians.get("3+", np.nan))


def render_risk_gauge(frame: pd.DataFrame) -> float:
    mean_probability = float(frame["risk_probability"].mean())
    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=mean_probability * 100,
            number={"suffix": "%", "valueformat": ".1f", "font": {"size": 44}},
            title={"text": "Xác suất At-Risk trung bình", "font": {"size": 18}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickvals": [0, 20, 40, 60, 80, 100],
                    "ticktext": ["0%", "20%", "40%", "60%", "80%", "100%"],
                },
                "bar": {"color": INK, "thickness": .28},
                "steps": [
                    {"range": [0, 40], "color": "#BBF7D0"},
                    {"range": [40, 70], "color": "#FDE68A"},
                    {"range": [70, 100], "color": "#FCA5A5"},
                ],
                "threshold": {
                    "line": {"color": "#7C3AED", "width": 4},
                    "thickness": .8,
                    "value": 41.5,
                },
            },
        )
    )
    figure.update_layout(title="8 · Mức rủi ro dự báo của nhóm đang xem")
    polish_figure(figure, height=430, legend="none")
    figure.update_layout(margin={"l": 50, "r": 60, "t": 78, "b": 45})
    st.plotly_chart(figure, width="stretch")
    st.caption(
        "Dải can thiệp: Low <40%, Medium 40–<70%, High ≥70%. Vạch tím 41,5% là threshold phân loại của model; "
        "risk level phục vụ ưu tiên can thiệp, không thay đổi nhãn dự báo đã công bố."
    )
    return mean_probability


def render_error_donut(frame: pd.DataFrame) -> tuple[int, int, int, int]:
    counts = frame["error_type"].value_counts()
    order = ["TP", "TN", "FP", "FN"]
    labels = {
        "TP": "Phát hiện đúng At-Risk",
        "TN": "Nhận diện đúng Not-At-Risk",
        "FP": "Cảnh báo nhầm",
        "FN": "Bỏ sót At-Risk",
    }
    colors = {
        "TP": "#DC2626",
        "TN": "#2563EB",
        "FP": "#F59E0B",
        "FN": "#7F1D1D",
    }
    data = pd.DataFrame(
        {"error_type": order, "count": [int(counts.get(value, 0)) for value in order]}
    )
    data["label"] = data["error_type"].map(labels)
    figure = px.pie(
        data,
        values="count",
        names="label",
        hole=.56,
        color="error_type",
        color_discrete_map=colors,
        category_orders={"error_type": order},
        title="9 · Thực tế và dự báo khớp nhau ra sao?",
    )
    figure.update_traces(
        textposition="inside",
        texttemplate="%{percent:.0%}",
        hovertemplate=(
            "%{label}<br>N=%{value:,}<br>Tỷ trọng=%{percent:.1%}<extra></extra>"
        ),
        marker={"line": {"color": "#FFFFFF", "width": 2}},
    )
    polish_figure(figure, height=470)
    st.plotly_chart(figure, width="stretch")
    tp, tn, fp, fn = (int(counts.get(value, 0)) for value in order)
    st.caption(
        f"TP={tp:,} · TN={tn:,} · FP={fp:,} · FN={fn:,}. "
        "Sai số cần chú ý nhất là FN: người At-Risk bị bỏ sót."
    )
    return tp, tn, fp, fn


def render_action_table(frame: pd.DataFrame) -> None:
    title, action = st.columns([4, 1])
    title.subheader("Bảng hỗ trợ hành động · Student Action List")

    def select_high_risk() -> None:
        st.session_state["risk_levels"] = ["High"]

    action.button(
        "Chỉ xem High Risk",
        key="select_high_risk_action",
        on_click=select_high_risk,
        width="stretch",
        help="Một click để lọc toàn bộ Trang 2 và danh sách về nhóm xác suất ≥70%.",
    )
    candidates = frame.loc[frame["risk_level"].eq("High")].sort_values(
        "risk_probability", ascending=False
    )
    if candidates.empty:
        st.info("Bộ lọc hiện tại không có sinh viên High Risk (xác suất ≥70%).")
        return
    table = candidates[
        [
            "id_student",
            "code_module",
            "code_presentation",
            "imd_band",
            "risk_probability",
            "predicted_status",
        ]
    ].head(100).rename(
        columns={
            "id_student": "student_id",
            "code_module": "module",
            "code_presentation": "presentation",
            "imd_band": "IMD",
            "predicted_status": "model_status",
        }
    )
    table["Cảnh báo"] = table["risk_probability"].map(
        lambda value: "🟥" * max(1, int(round(value * 10)))
    )
    st.dataframe(
        table,
        width="stretch",
        hide_index=True,
        height=420,
        column_config={
            "risk_probability": st.column_config.NumberColumn(
                "risk_probability", format="percent"
            ),
            "Cảnh báo": st.column_config.TextColumn(
                "Data bar",
                help="Mỗi ô đỏ tương ứng khoảng 10 điểm phần trăm rủi ro.",
            ),
        },
    )
    st.caption(
        f"Hiển thị tối đa 100/{len(candidates):,} lượt High Risk trong phạm vi IMD/risk filter. "
        "Dùng Risk Level = High để toàn bộ trang và danh sách cùng tập trung vào nhóm can thiệp."
    )


def render_risk_page() -> None:
    render_header(
        "Trang 2 · Risk Matrix & Early Warning",
        "Ma trận rủi ro và mô hình dự báo can thiệp",
        "Phân tích tương tác đa biến và dùng Logistic Regression để ưu tiên cảnh báo sớm.",
        "Test split · cutoff ngày 105 · model lr-oulad-c105-s42-v4 · không huấn luyện lại trong dashboard",
    )
    st.markdown(
        """
        <div class="definition-box"><b>Model dự báo gì?</b><br>
        Từ dữ liệu có đến ngày 105, Logistic Regression ước lượng xác suất một <b>lượt học</b>
        kết thúc bằng <b>Fail hoặc Withdrawn</b>. Đây là phân loại At-Risk, không phải dự báo điểm.</div>
        """,
        unsafe_allow_html=True,
    )
    try:
        verification = model_table("model_verification.csv")
        if "status" not in verification or not verification["status"].eq("PASS").all():
            st.error("Model verification chưa PASS toàn bộ; dashboard không công bố dự báo.")
            return
        base = prepare_risk_frame()
    except (FileNotFoundError, ValueError) as exc:
        st.error(str(exc))
        return

    levels, imd_bands = page_two_filters(base)
    mask = pd.Series(True, index=base.index)
    if levels:
        mask &= base["risk_level"].isin(levels)
    if imd_bands:
        mask &= base["imd_band"].isin(imd_bands)
    frame = base.loc[mask].copy()
    if frame.empty:
        st.warning("Bộ lọc Risk Level/IMD hiện tại không có lượt học trong test split.")
        return

    accuracy, recall, high_count = render_model_kpis(frame)
    st.caption(
        f"KPI tính trên {len(frame):,} lượt thuộc test split trong bộ lọc hiện tại. "
        "Metric công bố toàn test: Accuracy 82,7% · Recall At-Risk 73,5%."
    )

    st.subheader("Tương tác đa biến và phân bố điểm")
    education, imd, top_rate, top_n = render_interaction_heatmap(frame)
    median_zero, median_three = render_attempt_boxplot(frame)

    st.subheader("Kết quả dự báo và ưu tiên can thiệp")
    left, right = st.columns(2)
    with left:
        mean_probability = render_risk_gauge(frame)
    with right:
        _tp, _tn, _fp, fn = render_error_donut(frame)
    render_action_table(frame)

    median_message = (
        f"Điểm trung vị đến ngày 105 là {median_zero:.1f} ở nhóm chưa học trước và "
        f"{median_three:.1f} ở nhóm 3+ lần."
        if pd.notna(median_zero) and pd.notna(median_three)
        else "Một số nhóm số lần học trước chưa đủ dữ liệu điểm để so sánh trung vị."
    )
    render_story(
        "Câu chuyện dữ liệu · Trang 2",
        [
            f"Tổ hợp có rủi ro cao nhất với N≥30 là {education} × IMD {imd}: {top_rate:.1%} (N={top_n:,}).",
            median_message,
            f"Xác suất At-Risk trung bình {mean_probability:.1%}; có {high_count:,} lượt High Risk. "
            f"Model đúng {accuracy:.1%}, phát hiện {recall:.1%} At-Risk và bỏ sót {fn:,} lượt.",
        ],
    )
    st.info(
        "Danh sách là công cụ ưu tiên hỗ trợ; không dùng model để tự động quyết định kết quả hay xử phạt người học."
    )


def main() -> None:
    apply_dashboard_css()
    page = page_navigation()
    if page == "Academic Insight & Behavior":
        render_academic_page()
    else:
        render_risk_page()


if __name__ == "__main__":
    main()
