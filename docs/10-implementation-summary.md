# 10 — Tổng kết triển khai và bàn giao toàn bộ dự án

**Ngày tổng kết:** 07/10/2026  
**Hướng triển khai đã duyệt:** Python cho toàn bộ pipeline, EDA, model và dashboard; Streamlit + Plotly cho ứng dụng tương tác.  
**Người thực hiện chính:** Leader dự án.  
**Repo phát hành mới:** `https://github.com/vhoanglong54/ttdltq_finalVER2.git`  
**Nguồn yêu cầu được bảo vệ:** không chỉnh sửa `docs/02-rubric-traceability.md` và `docs/source/TTDLTQ_script.docx`.

Tài liệu này ghi lại toàn bộ hiện vật đã triển khai, quyết định kỹ thuật, kết quả kiểm tra, cách tái tạo và phần còn phải hoàn thành trước khi nộp. Chi tiết chuyên sâu của model vẫn nằm tại [04-model.md](04-model.md); tài liệu này đóng vai trò bản tổng kết/bàn giao, không thay thế nguồn giải thích model đó.

## 1. Kết quả tổng thể

Luồng dự án hiện tại:

```text
7 bảng OULAD chính thức
  → xác minh nguồn và audit
  → cleaning theo từng bảng
  → aggregate assessment/VLE đúng hạt
  → join thành bảng phân tích
  → EDA + 10 giả thuyết
  → 6 insight có số liệu và giới hạn
  → Logistic Regression cảnh báo sớm tại ngày 105
  → dashboard Streamlit 4 trang
  → Geographic Map + tương tác + model diagnostics
  → automated QA + visual QA
```

Các phần đã có hiện vật chạy được:

- Pipeline dữ liệu có audit, cleaning, aggregate, join và báo cáo chất lượng.
- Bảng processed chuẩn 32.593 learning attempts, 35 cột và không trùng khóa attempt.
- Notebook/script EDA, 6 hình tĩnh Matplotlib/Seaborn, 13 bảng bằng chứng.
- 10/10 giả thuyết có trạng thái và bằng chứng; 6 insight tách biệt với model.
- Logistic Regression v4 có leakage guard, group split, tuning, threshold, bootstrap CI và verification.
- Dashboard Streamlit gồm 4 trang, 9 loại biểu đồ không phải map và 1 Geographic Map riêng.
- Filter nhiều cấp, reset, filter context, tooltip, drill-down và cross-filtering.
- QA tự động 15/15 test PASS và QA trực quan bằng trình duyệt thật.

## 2. Các quyết định đã chốt

### 2.1 Công nghệ

| Phần | Công nghệ cuối cùng |
|---|---|
| Xử lý dữ liệu | Python, Pandas, NumPy |
| EDA tĩnh | Matplotlib, Seaborn |
| Model | scikit-learn Logistic Regression |
| Dashboard | Streamlit + Plotly |
| Geographic Map | Plotly Choropleth + GeoJSON có nguồn |
| Kiểm thử | `unittest`, Streamlit AppTest, Playwright/Edge cho visual QA |

Các hướng Power BI/Tableau cũ đã được dọn khỏi code và tài liệu đang sử dụng. Nội dung còn nhắc Tableau trong tài liệu rubric được bảo vệ vẫn giữ nguyên theo yêu cầu không sửa rubric.

### 2.2 Phạm vi nghiệp vụ

- Đơn vị phân tích là một **learning attempt** có khóa `(code_module, code_presentation, id_student)`.
- `At_Risk = 1` khi `final_result` là `Fail` hoặc `Withdrawn`.
- `At_Risk = 0` khi `final_result` là `Pass` hoặc `Distinction`.
- OULAD là dữ liệu quan sát; kết luận chỉ dùng các từ **liên hệ**, **khác biệt**, **xu hướng**, không tuyên bố nhân quả.
- VLE clicks là tương tác trên nền tảng, không phải attendance, study hours hoặc chất lượng học.
- Metric model là bằng chứng dự báo riêng, không được dùng thay cho insight phân tích dữ liệu.

## 3. Dữ liệu và pipeline

### 3.1 Nguồn dữ liệu

Pipeline sử dụng đủ bảy bảng OULAD có khóa nối tự nhiên:

1. `studentInfo`
2. `studentRegistration`
3. `studentAssessment`
4. `assessments`
5. `studentVle`
6. `vle`
7. `courses`

Raw được giữ ngoài Git và không sửa bằng spreadsheet. File nguồn được xác minh header, số dòng/checksum trước khi pipeline xử lý.

### 3.2 Cleaning và aggregate

Các bước chính đã triển khai trong `src/oulad_pipeline.py`:

- Chuẩn hóa schema/kiểu dữ liệu và kiểm tra khóa.
- Chuẩn hóa hiển thị `imd_band` nhưng không thay đổi ý nghĩa raw.
- Tách rõ count bằng 0 với score/ngày bị thiếu.
- Aggregate assessment về đúng hạt attempt trước khi join.
- Consolidate `studentVle` theo learner–resource–day và cộng `sum_click`.
- Không xóa cơ học 787.170 dòng `studentVle` trùng toàn dòng vì chúng có thể là đóng góp click hợp lệ.
- Bảo toàn toàn bộ 39.605.099 clicks: 10.655.280 dòng raw thành 8.459.320 sự kiện logic.
- Join từ `studentInfo`; kiểm soát cardinality để không nhân dòng.

### 3.3 Bảng phân tích cuối

`data/processed/clean_dataset.csv`:

| Thuộc tính | Giá trị |
|---|---:|
| Số learning attempts | 32.593 |
| Số cột | 35 |
| Duplicate attempt key | 0 |
| Người học duy nhất | 28.785 |
| At-Risk count | 17.208 |
| At-Risk rate | 52,7966% |
| Tổng VLE clicks | 39.605.099 |
| SHA-256 | `70db1ff19a1dc8553005b0e3801786d20ab1488cc3420a2fe15c5a2254d80f9a` |

Định nghĩa cột, grain, missingness và công thức KPI nằm tại [09-data-dictionary.md](09-data-dictionary.md), [processed README](../data/processed/README.md) và [Data Quality Report](../reports/data-quality-report.md).

## 4. EDA, giả thuyết và insight

### 4.1 Hiện vật EDA

- Script tái tạo: `src/eda_analysis.py`.
- Notebook trình bày: `notebooks/03_eda.ipynb`.
- Bảng bằng chứng: `reports/eda/`.
- Hình tĩnh: `reports/figures/eda/`.

Sáu hình EDA tĩnh đã tạo:

1. Outcome theo module–presentation.
2. Xu hướng VLE theo tuần.
3. Box plot VLE sớm theo trạng thái.
4. Assessment completion và risk.
5. Heatmap VLE × assessment.
6. At-Risk rate theo region.

### 4.2 Kết quả 10 giả thuyết

| ID | Kết quả chính |
|---|---|
| H01 | Chênh lệch At-Risk giữa module–presentation đạt 38,34 điểm %. |
| H02 | VLE clicks Q1 so với Q4 chênh 45,74 điểm %. |
| H03 | Active days Q1 so với Q4 chênh 50,36 điểm %. |
| H04 | Mean weekly clicks của At-Risk thấp hơn ở 15/15 tuần đầy đủ. |
| H05 | Completion 0% so với 100% chênh 71,85 điểm %. |
| H06 | Assessment-score Q1 so với Q4 chênh 51,78 điểm %. |
| H07 | Có 1+ previous attempts so với 0 chênh 19,73 điểm %. |
| H08 | Regional range đạt 14,71 điểm %, phải nêu confounding. |
| H09 | Low-VLE + low-assessment so với high-high chênh 65,07 điểm %. |
| H10 | Độ lớn low-vs-high engagement khác theo module: 27,68–63,49 điểm %. |

Tất cả kết quả trên là mô tả liên hệ, không phải bằng chứng nhân quả.

### 4.3 Sáu insight cuối

| Insight | Bằng chứng chính |
|---|---|
| INS-01 | `CCC-2014B`: 65,75%, N=1.936; `AAA-2013J`: 27,42%, N=383; chênh 38,34 điểm %. |
| INS-02 | VLE Q1: 64,41%, N=6.283; Q4: 18,67%, N=6.283; chênh 45,74 điểm %. |
| INS-03 | Completion 0%: 96,60%, N=1.677; 100%: 24,75%, N=18.969; chênh 71,85 điểm %. |
| INS-04 | Low-low: 73,33%, N=1.680; high-high: 8,26%, N=2.385; chênh 65,07 điểm %. |
| INS-05 | 1+ previous attempts: 56,05%, N=3.140; 0 previous: 36,32%, N=21.992; chênh 19,73 điểm %. |
| INS-06 | North Western: 59,81%, N=2.906; Ireland: 45,10%, N=1.184; chênh 14,71 điểm %. |

Nguồn diễn giải đầy đủ, scope và limitation của từng insight nằm tại [insight-log.md](insight-log.md).

## 5. Model cảnh báo sớm

### 5.1 Bài toán và cutoff

- Thuật toán chính: Logistic Regression theo yêu cầu rubric.
- DummyClassifier chỉ là baseline kỹ thuật.
- Model dự báo xác suất một attempt sẽ kết thúc `Fail/Withdrawn`.
- Cutoff cuối: ngày 105.
- Cohort eligible: 25.132 attempts, At-Risk rate 38,78%.
- Chỉ event/submission có ngày không vượt cutoff được phép làm feature.
- Attempt đăng ký sau cutoff hoặc đã rút trước/tại cutoff bị loại.

### 5.2 Chống leakage và split

- Cấm dùng `id_student`, `final_result`, `At_Risk`, `Performance_Level`, `date_unregistration`, aggregate `*_all_time` hoặc dữ liệu sau cutoff làm feature.
- Split theo nhóm `id_student`; một người học không xuất hiện ở nhiều tập.
- Train: 17.952 attempts; validation: 3.590; test: 3.590.
- Preprocessing chỉ fit trên train.
- Grid search 5-fold StratifiedGroupKFold chọn theo PR-AUC.
- Threshold chỉ chọn trên validation, không chọn bằng test.
- Threshold cuối: `0,415`, với ràng buộc Recall At-Risk validation tối thiểu 0,75.

### 5.3 Kết quả test v4

Model version: `lr-oulad-c105-s42-v4`.

| Metric | Kết quả test |
|---|---:|
| Accuracy | 82,70% |
| Balanced Accuracy | 81,01% |
| Precision At-Risk | 80,24% |
| Recall At-Risk | 73,49% |
| F1 At-Risk | 76,72% |
| ROC-AUC | 0,8906 |
| PR-AUC | 0,8701 |
| Brier Score | 0,1237 |

Confusion matrix: TN=1.946, FP=252, FN=369, TP=1.023. Accuracy cao hơn dummy baseline 21,48 điểm %. Khoảng tin cậy bootstrap 95% của Accuracy là 81,46%–83,84%, cận dưới vẫn vượt 80%.

`model_verification.csv` có 9/9 cổng PASS: checksum artifact, Accuracy, CI, Recall, F1, PR-AUC, Brier, margin so với dummy và minimum presentation accuracy.

### 5.4 Output model dùng cho dashboard

Bundle công bố trong `data/processed/model/` gồm snapshot ngày 105, predictions, metrics, confusion matrix, ROC/PR points, calibration, confidence interval, subgroup QA, coefficients, threshold selection, CV results, metadata và verification.

Ứng dụng không train lại model khi render và không đọc file pickle/joblib. App chỉ đọc artifact đã kiểm tra, mặc định hiển thị test split và luôn công bố model version, cutoff, threshold và `N`.

## 6. Dashboard Streamlit

### 6.1 Kiến trúc

- Entry point: `dashboard/app.py`.
- Data contract/loader/KPI: `dashboard/dashboard_data.py`.
- UI/state/filter: Streamlit.
- Biểu đồ/selection event: Plotly.
- App không join raw event và không huấn luyện model trong request render.

### 6.2 Bốn trang storytelling

#### Overview — RQ1

- KPI toàn khóa.
- Donut phân bố Distinction/Pass/Fail/Withdrawn.
- 100% stacked bar theo module–presentation.
- Sunburst drill Module → Presentation → Result.
- INS-01 và câu chuyển sang tín hiệu VLE/assessment.

#### Factor Analysis — RQ2, RQ3, RQ5

- KPI snapshot ngày 105.
- Line chart bốn cửa sổ VLE không chồng lấp: ngày 50–77, 78–91, 92–98 và 99–105.
- Box plot assessment score trước cutoff.
- Bubble chart assessment × VLE × At-Risk rate.
- Heatmap quartile VLE × quartile assessment.
- INS-02, INS-03 và INS-04.

#### Risk Analysis — RQ4, RQ5

- Treemap previous attempts → dimension được chọn.
- Cho phép đổi dimension: education, IMD, credits, age hoặc disability.
- Bar chart rate theo region, luôn đi kèm `N`.
- Geographic Choropleth Map.
- INS-05 và INS-06.

#### Prediction — RQ6

- Accuracy, Precision, Recall, F1, ROC-AUC và PR-AUC.
- Histogram risk probability và đường threshold.
- Confusion matrix Actual × Predicted.
- ROC và Precision–Recall curve.
- Calibration plot và bootstrap confidence intervals.
- Giải thích ý nghĩa metric và giới hạn sử dụng model.

### 6.3 Inventory biểu đồ

Dashboard có 9 loại không phải map:

1. Donut
2. Stacked bar
3. Sunburst
4. Line
5. Box plot
6. Scatter/Bubble
7. Heatmap
8. Treemap
9. Histogram

Ngoài ra có 1 Geographic Choropleth Map độc lập. Confusion matrix, ROC/PR và calibration là bằng chứng model bổ sung, không được dùng để cộng khống số loại.

### 6.4 Tương tác và UI/UX

- Filter cascade: Module → Presentation → Region.
- Reset filter và caption filter context.
- Tooltip có metric, context và `N`.
- Chọn segment stacked bar để cross-filter sunburst.
- Sunburst drill-down theo ba tầng.
- Empty state khi filter không có dữ liệu.
- Điều hướng bốn trang qua sidebar và query parameter.
- Màu semantic nhất quán; At-Risk dùng đỏ/cam, Not-At-Risk dùng xanh.
- Title, axis title, đơn vị, caption và limitation được ghi trực tiếp.
- Rate/color scale dùng miền 0–100% để không phóng đại khác biệt.
- Bố cục card sáng, khoảng cách, chiều cao biểu đồ và tương phản được chuẩn hóa cho màn hình demo 1440 × 1000.

## 7. Geographic Map

- Geometry gốc: ONS, *Counties and Unitary Authorities (December 2025) Boundaries UK BGC*.
- Giấy phép: Open Government Licence v3.0.
- Script dựng: `src/build_oulad_regions_geojson.py`.
- Output: `dashboard/assets/oulad_regions.geojson`.
- Bảng audit: `dashboard/assets/oulad_regions_mapping.csv`.
- Coverage: 13/13 nhãn OULAD, 218 đơn vị ONS được ánh xạ một lần, geometry hợp lệ.
- Tooltip: Region, At-Risk rate, learning attempts và At-Risk count.

`Ireland` dùng Northern Ireland làm proxy có công bố rõ. Geometry là xấp xỉ có kiểm soát theo vùng OU lịch sử, không dùng để suy luận ranh giới hành chính chi tiết hoặc cá nhân.

## 8. QA đã thực hiện

### 8.1 Automated QA

- `python -m py_compile`: PASS cho app, data layer, EDA, map builder và model.
- `python -m unittest discover -s tests -v`: **15/15 PASS**.
- Streamlit AppTest: Overview 3 chart, Factor 4, Risk 3, Prediction 4; 0 exception.
- Risk dimension selector: IMD, credits, age và disability đều render 3 chart, 0 exception.
- Baseline KPI không filter khớp bảng processed.
- Prediction artifact khớp model version/cutoff/threshold và verification PASS.
- GeoJSON khớp 13/13 region và geometry hợp lệ.
- Markdown relative link check: 0 liên kết thiếu.
- `git diff --check`: không có whitespace error.

### 8.2 Visual QA

Kiểm tra bằng Microsoft Edge tại viewport 1440 × 1000:

- Tooltip stacked bar xuất hiện và có module–presentation, tỷ trọng, `N`.
- Chọn `AAA-2013J` trả `N=383`; sunburst chỉ còn nhánh tương ứng.
- Click `BBB` drill đúng subtree BBB.
- Heatmap có số đọc trực tiếp và scale 0–100%.
- Map render geometry thật, có legend và tooltip.
- ROC/PR có trục, đường chuẩn và legend không chồng tiêu đề.

Bằng chứng: [automated QA](../dashboard/evidence/automated-qa-2026-10-06.md) và [visual QA](../dashboard/evidence/visual-qa-2026-10-07.md).

### 8.3 Bảo vệ rubric

Tại vòng QA cuối:

- Hash working tree của `docs/02-rubric-traceability.md` trùng `HEAD`.
- Hash working tree của `docs/source/TTDLTQ_script.docx` trùng `HEAD`.
- Không còn tham chiếu Power BI/Tableau trong tài liệu/code đang sử dụng ngoài hai nguồn được bảo vệ.

## 9. Cấu trúc hiện vật chính

```text
dashboard/
  app.py
  dashboard_data.py
  chart-inventory.md
  qa-t09.md
  assets/
  evidence/
data/
  processed/clean_dataset.csv
  processed/model/
docs/
  plan_approved.md
  04-model.md
  05-dashboard-spec.md
  09-data-dictionary.md
  10-implementation-summary.md
  insight-log.md
notebooks/
  03_eda.ipynb
reports/
  data-quality-report.md
  eda/
  figures/eda/
src/
  oulad_pipeline.py
  eda_analysis.py
  at_risk_features.py
  at_risk_experiments.py
  at_risk_model.py
  build_oulad_regions_geojson.py
tests/
  test_at_risk_model.py
  test_dashboard_contract.py
```

## 10. Cách tái tạo và chạy

### 10.1 Cài môi trường

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 10.2 Tái tạo pipeline từ raw

```powershell
python src/verify_oulad_source.py data/raw
python src/oulad_pipeline.py audit data/raw
python src/oulad_pipeline.py clean data/raw
python src/oulad_pipeline.py build data/raw
python src/oulad_pipeline.py report
```

### 10.3 Tái tạo EDA

```powershell
python src/eda_analysis.py
```

### 10.4 Tái tạo model

```powershell
python src/at_risk_model.py audit-cutoffs
python src/at_risk_experiments.py --n-jobs -1
python src/at_risk_model.py train --cutoff 105 --n-jobs -1
python src/at_risk_model.py validate
```

### 10.5 Chạy dashboard

```powershell
streamlit run dashboard/app.py
```

### 10.6 Chạy kiểm thử

```powershell
python -m unittest discover -s tests -v
```

## 11. Chính sách file trong Git

Được đưa vào repo mới:

- Toàn bộ source, test, notebook, tài liệu, report và ảnh QA.
- `clean_dataset.csv` để tái tạo EDA/KPI ngay.
- Bundle artifact model CSV/JSON/TXT cuối để dashboard chạy ngay sau khi clone.
- GeoJSON và mapping audit có nguồn/giấy phép.

Không đưa vào Git:

- `data/raw/` và `data/interim/`: dữ liệu nguồn/trung gian dung lượng lớn, tái tạo theo hướng dẫn.
- `models/**`: file nhị phân joblib không được dashboard sử dụng và có thể tái tạo.
- `feature_snapshot_weighted_experiment.csv`: snapshot thí nghiệm trung gian, không phải artifact cuối.
- `.venv/`, cache Python/Jupyter và Streamlit secrets.

## 12. Phần còn lại trước khi nộp cuối

Những mục dưới đây chưa được tuyên bố hoàn thành chỉ vì code/dashboard đã có:

- Chạy dashboard thủ công lần cuối trên đúng máy dùng để demo.
- Chốt báo cáo khoa học tối thiểu 40 trang và tài liệu tham khảo IEEE.
- Chèn ảnh dashboard/model/insight cùng caption vào báo cáo.
- Làm slide thuyết trình và kịch bản demo theo story bốn trang.
- Quay video backup và kiểm tra link truy cập.
- Luyện giải thích data grain, cleaning, insight, cutoff, threshold, metric và giới hạn model.

## 13. Checklist bàn giao

- [x] Pipeline dữ liệu và processed contract.
- [x] EDA, 10 giả thuyết và 6 insight.
- [x] Logistic Regression v4 và verification.
- [x] Dashboard bốn trang.
- [x] 9 loại biểu đồ và Geographic Map.
- [x] Filter, tooltip, drill-down và cross-filter.
- [x] Automated QA và visual QA.
- [x] Tài liệu chạy/tái tạo và bản tổng kết này.
- [ ] Leader chạy review thủ công trên máy demo.
- [ ] Hoàn thành báo cáo, slide, video và link demo cuối.

Thông điệp sử dụng cuối cùng: model hỗ trợ ưu tiên theo dõi sớm, không tự động quyết định người học nào sẽ thất bại.
