# 05 — Đặc tả dashboard Python hai trang

## 1. Kiến trúc

```text
7 bảng OULAD đã clean
  ├─ clean_dataset.csv ───────────────► KPI, outcome, map
  ├─ dashboard marts ─────────────────► VLE timeline, submission scatter, activity treemap
  └─ feature_snapshot + predictions ──► risk matrix, gauge, model performance, action list
                                           │
                                           ▼
                                Streamlit + Plotly (2 trang)
```

- Entry point: `dashboard/app.py`.
- Loader/schema/KPI: `dashboard/dashboard_data.py`.
- Data mart builder: `src/dashboard_features.py`.
- Map: `dashboard/assets/oulad_regions.geojson` và mapping audit.
- App chỉ đọc artifact; không join raw event và không train model khi render.

## 2. Contract chung

| Khái niệm | Định nghĩa |
|---|---|
| Learning attempt | `(code_module, code_presentation, id_student)` |
| At-Risk | `Fail` hoặc `Withdrawn` |
| Not-At-Risk | `Pass` hoặc `Distinction` |
| Pass Rate | `(Pass + Distinction) / attempts` |
| Total Students | `nunique(id_student)` trong filter context |
| Avg Score | `sum(valid assessment scores) / count(valid scores)` |
| Model scope | `dataset_split=test`, cutoff ngày 105 |
| Risk Level | Low `<0,4`; Medium `0,4–<0,7`; High `≥0,7` |

Risk Level là dải ưu tiên can thiệp. Threshold phân lớp chính thức của Logistic Regression là `0,415` và không bị thay đổi trong dashboard.

## 3. Trang 1 — Academic Insight & Behavior

### Slicers

`code_module → code_presentation` là cascade; `gender` độc lập. `region` không nằm trong slicer vì được điều khiển bằng map cross-filter.

### KPI

1. Total Students.
2. Avg Score.
3. Pass Rate.
4. At-Risk Rate.

### Visual

1. **Filled Map:** aggregate attempt theo `region`; color=`At_Risk.mean`; tooltip rate/count/N. Map luôn hiển thị tất cả region trong slicer context để người dùng có thể đổi vùng. Region được chọn chỉ lọc KPI và visual 2–5.
2. **100% Stacked Bar:** mặc định `code_module × final_result`; click module lưu state và đổi grain sang `code_presentation × final_result` của module đó. Nút quay lại xóa drill state.
3. **Multi-Line VLE:** tổng click theo ngày chia tổng attempts của từng nhãn At-Risk, gồm cả ngày không click; dùng rolling mean 7 ngày. Tối đa ba deadline có tổng trọng số lớn nhất được đánh dấu bằng vạch chấm.
4. **Scatter:** một điểm là một assessment submission hợp lệ; `x=submission_delay`, `y=score`, size tăng theo previous attempts, color theo At-Risk. Render sample cố định tối đa 4.500 điểm; Pearson r và trendline dùng toàn bộ subset.
5. **Treemap:** `activity_type`, area/color theo tổng `sum_click`.

### Insight/story

Card cuối trang chỉ có ba câu định lượng, cập nhật theo filter. Mỗi câu nêu phát hiện và giới hạn cần thiết; không nhồi giả thuyết/kỹ thuật vào chart.

## 4. Trang 2 — Risk Matrix & Early Warning

### Slicers

- Risk Level: High, Medium, Low.
- `imd_band`, có nhóm `Không xác định` riêng.

### KPI

- Accuracy trong context.
- Recall At-Risk trong context.
- Số High Risk trong context.

Caption luôn công bố metric toàn test để người xem không nhầm subgroup metric với kết quả model chính thức.

### Visual và table

6. **Heatmap:** `highest_education × imd_band`; `z=actual_at_risk.mean`; mỗi ô có phần trăm và `N`. Story chỉ chọn ô `N≥30` khi tìm tổ hợp cao nhất.
7. **Box Plot:** `assessment_weighted_score_cutoff` theo previous attempts; `3+` gộp 3–6 để tránh nhóm quá nhỏ.
8. **Gauge:** trung bình `risk_probability`; green `<40%`, yellow `40–<70%`, red `≥70%`; marker 41,5% là threshold model.
9. **Donut:** bốn error type TP/TN/FP/FN. Caption giải nghĩa và nêu số tuyệt đối.
10. **Action List:** chỉ High Risk, sort giảm dần probability, tối đa 100 dòng; có thanh đỏ 10 nấc. Nút `Chỉ xem High Risk` cập nhật Risk Level slicer và lọc toàn Trang 2 bằng một click.

## 5. Storytelling và insight

Dashboard có sáu insight động, ba ở mỗi trang. Insight EDA cố định và bằng chứng tái tạo vẫn được lưu tại `insight-log.md`; model là phần riêng, không thay thế insight phân tích dữ liệu.

Story flow:

```text
Kết quả + không gian
  → hành vi VLE + kỷ luật nộp bài + loại tài nguyên
  → tổ hợp education × IMD + lịch sử học lại
  → xác suất dự báo + đúng/sai
  → danh sách ưu tiên hỗ trợ
```

## 6. Map và tương tác

- GeoJSON có 13 feature khớp 13/13 nhãn OULAD.
- Nguồn ONS, giấy phép OGL v3.0; `Ireland` dùng Northern Ireland làm proxy và được công bố.
- Plotly selection trả `location`; app lưu region trong `st.session_state`, rerun và cập nhật toàn trang.
- Reset map tăng key version để xóa selection cũ.
- Module drill cũng dùng selection state riêng và breadcrumb.

## 7. Cổng chất lượng

- `python src/dashboard_features.py` tạo đủ bốn mart.
- Tổng click của `vle_daily_profile` và `vle_activity_summary` đều bằng `39.605.099`.
- AppTest: Page 1 = 5 chart/4 metric; Page 2 = 4 chart/3 metric/1 table; 0 exception.
- Browser QA: map 13 path, cross-filter xuất hiện sau click, drill module xuất hiện sau click.
- Filter High render 4 chart, Accuracy context 92,3%, Recall context 100%, High count 810; đây không phải metric toàn test.
- Rubric gốc và DOCX nguồn không thay đổi.
