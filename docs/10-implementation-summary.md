# 10 — Tổng kết triển khai và bàn giao toàn bộ dự án

**Cập nhật:** 07/10/2026

**Trạng thái Git:** đã được leader duyệt để commit/push

**Repo đích:** `https://github.com/vhoanglong54/ttdltq_finalVER2.git`

**Công nghệ cuối:** Python, Pandas, scikit-learn, Streamlit và Plotly
**Nguồn được bảo vệ:** `02-rubric-traceability.md` và `source/TTDLTQ_script.docx` không bị chỉnh sửa.

Tài liệu này là bản bàn giao tổng hợp. Giải thích chuyên sâu duy nhất của model nằm ở [04-model.md](04-model.md); thiết kế dashboard cuối nằm ở [plan_approved.md](plan_approved.md) và [05-dashboard-spec.md](05-dashboard-spec.md).

## 1. Kết quả tổng thể

```text
7 bảng OULAD
  → audit nguồn
  → clean từng bảng
  → aggregate đúng grain
  → join bảng phân tích 32.593 attempts
  → EDA + 10 giả thuyết + 6 insight dữ liệu
  → Logistic Regression cảnh báo sớm ngày 105
  → 4 data marts cho dashboard
  → dashboard Streamlit hai trang
  → 8 chart type + Geographic Map + action list
  → automated QA + browser visual QA
```

Hiện vật local đã có:

- Pipeline dữ liệu tái tạo được và báo cáo chất lượng.
- `clean_dataset.csv`: 32.593 attempts, 35 cột, 0 duplicate attempt key.
- EDA: 10 giả thuyết, 6 insight, 13 bảng bằng chứng và 6 hình tĩnh.
- Logistic Regression v4: leakage guard, group split, tuning, threshold, bootstrap CI và verification.
- Dashboard hai trang theo đặc tả mới, có map cross-filter, module drill-down và High-Risk Action List.
- 17 unit tests, AppTest và kiểm tra bằng Microsoft Edge.

## 2. Dữ liệu

### 2.1 Bảy bảng nguồn

1. `studentInfo`
2. `studentRegistration`
3. `studentAssessment`
4. `assessments`
5. `studentVle`
6. `vle`
7. `courses`

Raw được giữ bất biến. Pipeline đọc raw, ghi interim và build processed; không sửa CSV bằng spreadsheet.

### 2.2 Hạt và target

- Learning attempt key: `(code_module, code_presentation, id_student)`.
- `At_Risk=1`: `Fail` hoặc `Withdrawn`.
- `At_Risk=0`: `Pass` hoặc `Distinction`.
- VLE click là proxy tương tác nền tảng, không phải thời gian học/attendance.
- `imd_band` là chỉ số khu vực, không phải thu nhập cá nhân.

### 2.3 Cleaning và join

- Chuẩn hóa schema/type và kiểm tra khóa.
- Giữ missing có ý nghĩa; không ép score thiếu về 0.
- Aggregate assessment về attempt trước join.
- Consolidate VLE theo learner–resource–day và cộng `sum_click`.
- Bảo toàn 39.605.099 clicks: 10.655.280 dòng raw thành 8.459.320 sự kiện logic.
- Join từ `studentInfo` và kiểm soát cardinality để không nhân dòng.

### 2.4 Bảng phân tích cuối

| Thuộc tính | Giá trị |
|---|---:|
| Attempts | 32.593 |
| Columns | 35 |
| Unique students | 28.785 |
| Duplicate attempt key | 0 |
| At-Risk count | 17.208 |
| At-Risk rate | 52,7966% |
| VLE clicks | 39.605.099 |
| SHA-256 | `70db1ff19a1dc8553005b0e3801786d20ab1488cc3420a2fe15c5a2254d80f9a` |

Chi tiết cột/grain/missingness: [09-data-dictionary.md](09-data-dictionary.md).

## 3. EDA và insight dữ liệu

### 3.1 Hiện vật

- Script: `src/eda_analysis.py`.
- Notebook: `notebooks/03_eda.ipynb`.
- Tables: `reports/eda/`.
- Figures: `reports/figures/eda/`.

### 3.2 Kết quả 10 giả thuyết

| ID | Kết quả mô tả |
|---|---|
| H01 | Module–presentation chênh At-Risk 38,34 điểm %. |
| H02 | VLE clicks Q1–Q4 chênh 45,74 điểm %. |
| H03 | Active days Q1–Q4 chênh 50,36 điểm %. |
| H04 | At-Risk có mean weekly clicks thấp hơn ở 15/15 tuần đủ dữ liệu. |
| H05 | Assessment completion 0%–100% chênh 71,85 điểm %. |
| H06 | Assessment score Q1–Q4 chênh 51,78 điểm %. |
| H07 | Có previous attempts–không có chênh 19,73 điểm %. |
| H08 | Regional range 14,71 điểm %, cần nêu confounding. |
| H09 | Low-low so với high-high chênh 65,07 điểm %. |
| H10 | Chênh engagement theo module dao động 27,68–63,49 điểm %. |

### 3.3 Sáu insight cố định

1. Rủi ro khác mạnh giữa module–presentation.
2. VLE thấp đi cùng At-Risk cao hơn.
3. Tiến độ assessment là tín hiệu phân tách mạnh.
4. Kết hợp VLE và assessment cho risk profile rõ hơn.
5. Lịch sử học lại là context cần chú ý.
6. At-Risk có khác biệt theo region.

Số liệu, `N`, nguồn tái tạo và giới hạn nằm tại [insight-log.md](insight-log.md). Model là phần riêng, không dùng thay insight dữ liệu.

## 4. Model cảnh báo sớm

### 4.1 Mục tiêu

Tại ngày 105, model ước lượng xác suất một learning attempt kết thúc bằng `Fail/Withdrawn`. Đây là phân loại nhị phân, không dự báo điểm.

### 4.2 Phương pháp

- Thuật toán chính: Logistic Regression đúng yêu cầu rubric.
- DummyClassifier chỉ làm baseline.
- Eligible cohort: 25.132 attempts; At-Risk 38,78%.
- Split theo `id_student`: train 17.952, validation 3.590, test 3.590.
- Feature chỉ dùng event/submission `date <= 105`.
- Cấm target, identifier, withdrawal date, aggregate all-time và thông tin sau cutoff.
- Preprocessing fit trên train; grid search dùng StratifiedGroupKFold.
- Threshold chọn trên validation với recall floor; test chỉ dùng đánh giá cuối.

### 4.3 Model công bố

Model version: `lr-oulad-c105-s42-v4`; threshold: `0,415`.

| Metric test | Giá trị |
|---|---:|
| Accuracy | 82,70% |
| Balanced Accuracy | 81,01% |
| Precision At-Risk | 80,24% |
| Recall At-Risk | 73,49% |
| F1 At-Risk | 76,72% |
| ROC-AUC | 0,8906 |
| PR-AUC | 0,8701 |
| Brier Score | 0,1237 |

Confusion matrix toàn test: TN=1.946, FP=252, FN=369, TP=1.023. Accuracy CI 95%: 81,46%–83,84%. Verification 9/9 gate PASS.

### 4.4 Output dùng trong app

Dashboard đọc CSV/JSON/TXT trong `data/processed/model/`; không đọc joblib và không train lại. Mặc định luôn dùng test split. Published test metric được giữ riêng với subgroup metric phát sinh từ filter.

Risk Level cho ưu tiên can thiệp:

- Low `<40%`
- Medium `40–<70%`
- High `≥70%`

Dải này không thay thế classification threshold 41,5%.

## 5. Data marts mới cho dashboard

`src/dashboard_features.py` tạo:

| File | Grain | Mục đích |
|---|---|---|
| `assessment_deadlines.csv` | assessment | deadline markers |
| `assessment_submissions.csv.gz` | valid submission | delay–score scatter |
| `vle_daily_profile.csv.gz` | filter dims × At-Risk × day | VLE multi-line |
| `vle_activity_summary.csv.gz` | filter dims × activity type | treemap |

Lý do: app không được đọc/join `studentVle.csv` 259 MB trong mỗi request. Hai VLE marts đều bảo toàn tổng 39.605.099 clicks. Submission mart có 170.874 bài hợp lệ và `submission_delay = date_submitted - due_date`.

## 6. Dashboard cuối — hai trang

Rubric được giữ nguyên. Bốn phần logic trước đây được gom thành hai trang vật lý để story ngắn và dễ demo hơn.

### 6.1 Trang 1 — Academic Insight & Behavior

**Slicers:** module, presentation, gender.
**KPI:** Total Students, Avg Score, Pass Rate, At-Risk Rate.

1. Filled Geographic Map theo At-Risk rate; click region cross-filter KPI và chart 2–5.
2. 100% Stacked Bar cơ cấu result; click module drill xuống presentation.
3. Multi-Line VLE At-Risk vs Not-At-Risk, rolling mean 7 ngày và deadline markers.
4. Scatter delay–score, bubble size previous attempts, trendline và Pearson r.
5. Treemap tổng clicks theo activity type.

Card story cuối trang có ba insight động: result context, chênh VLE, delay–score và tài nguyên dẫn đầu.

### 6.2 Trang 2 — Risk Matrix & Early Warning

**Slicers:** Risk Level, IMD.
**KPI:** Accuracy context, Recall context, High Risk Count.

6. Heatmap `highest_education × imd_band`, màu At-Risk rate, mỗi ô có `N`.
7. Box Plot score ngày 105 theo previous attempts `0/1/2/3+`.
8. Gauge mean risk probability với ba dải và threshold marker.
9. Donut TP/TN/FP/FN.
10. Student Action List: top 100 High Risk, probability, data bar đỏ và nút một-click lọc toàn Trang 2 về High.

Card story cuối trang có ba insight động: top education–IMD cell với `N≥30`, score median theo previous attempts, và hiệu quả/cảnh báo model.

### 6.3 Inventory và UI

- 8 loại chart không phải map: stacked bar, multi-line, scatter, treemap, heatmap, box, gauge, donut.
- 1 Geographic Map riêng.
- Màu semantic: xanh an toàn, cam cảnh báo, đỏ At-Risk/High.
- Title, axis, unit, caption, hover và `N` được ghi trực tiếp.
- Scatter lấy mẫu 4.500 điểm để render nhưng thống kê dùng toàn subset.
- Insight chỉ ba câu/trang; không còn Sunburst hoặc hierarchy dày đặc.

## 7. Geographic Map

- Asset: `dashboard/assets/oulad_regions.geojson`.
- Audit: `dashboard/assets/oulad_regions_mapping.csv`.
- Nguồn ONS Counties and Unitary Authorities, OGL v3.0.
- Coverage 13/13 OULAD region; 218 ONS areas ánh xạ duy nhất.
- `Ireland` dùng Northern Ireland làm proxy có công bố.
- Map dùng cho phân bố vùng, không suy luận cá nhân/nhân quả.

## 8. Tương tác đã triển khai

- Slicer module → presentation cascade và gender.
- Map click → region state → rerun → cập nhật KPI/chart; nút reset xóa state/selection.
- Module click → presentation drill; breadcrumb và nút quay lại.
- Risk Level/IMD filter cập nhật KPI, 4 chart và action list.
- Tooltip có metric, context và `N`.
- Empty state có thông báo, không tạo số giả.

## 9. QA

### 9.1 Automated

- Compile app, data layer, mart builder, EDA, map builder và model: PASS.
- `python -m unittest discover -s tests -v`: **17/17 PASS**.
- AppTest Page 1: 5 chart, 4 metric, 0 exception.
- AppTest Page 2: 4 chart, 3 metric, 1 table, 0 exception.
- AppTest High only: 4 chart, 0 exception, High count 810.
- Markdown links: 0 missing.
- `git diff --check`: PASS.

### 9.2 Browser

- Microsoft Edge, viewport 1440×1000.
- Map render 13 paths; click tạo active cross-filter.
- Stacked bar click tạo drill module → presentation.
- Timeline, scatter, treemap, heatmap, box, gauge, donut và action list đều render.
- Bằng chứng: [visual QA](../dashboard/evidence/visual-qa-2026-10-07.md).

### 9.3 Bảo vệ rubric

`git diff` không có thay đổi ở:

- `docs/02-rubric-traceability.md`
- `docs/source/TTDLTQ_script.docx`

## 10. Cách tái tạo

### Cài môi trường

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Pipeline dữ liệu

```powershell
python src/verify_oulad_source.py data/raw
python src/oulad_pipeline.py audit data/raw
python src/oulad_pipeline.py clean data/raw
python src/oulad_pipeline.py build data/raw
python src/oulad_pipeline.py report
```

### EDA, model và dashboard marts

```powershell
python src/eda_analysis.py
python src/at_risk_model.py audit-cutoffs
python src/at_risk_experiments.py --n-jobs -1
python src/at_risk_model.py train --cutoff 105 --n-jobs -1
python src/at_risk_model.py validate
python src/dashboard_features.py
```

### Chạy app và tests

```powershell
streamlit run dashboard/app.py
python -m unittest discover -s tests -v
```

## 11. Cấu trúc hiện vật chính

```text
dashboard/
  app.py
  dashboard_data.py
  chart-inventory.md
  wireframe.md
  qa-t09.md
  assets/
  evidence/
data/processed/
  clean_dataset.csv
  dashboard/
  model/
docs/
  plan_approved.md
  04-model.md
  05-dashboard-spec.md
  09-data-dictionary.md
  10-implementation-summary.md
  insight-log.md
src/
  oulad_pipeline.py
  eda_analysis.py
  at_risk_model.py
  dashboard_features.py
tests/
  test_at_risk_model.py
  test_dashboard_contract.py
```

## 12. Phần chưa hoàn thành tự động

- Leader review UI và nội dung cuối trên máy demo.
- Báo cáo tối thiểu 40 trang, tài liệu tham khảo IEEE.
- Slide, kịch bản demo và video backup.
- Link deploy cuối.
- Luyện giải thích grain, cleaning, insight, cutoff, threshold, metric, FN/FP và giới hạn model.
- Commit/push chỉ được thực hiện sau khi leader duyệt.

Thông điệp sử dụng cuối: model dùng để **ưu tiên hỗ trợ sớm**, không tự động quyết định hay xử phạt người học.
