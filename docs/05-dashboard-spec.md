# 05 — Nghiên cứu, insight và đặc tả dashboard Python

Dashboard được triển khai bằng **Streamlit + Plotly**, là một lựa chọn được rubric cho phép trực tiếp. Python đảm nhiệm toàn bộ chuỗi dữ liệu → EDA → Logistic Regression → dashboard. Việc đổi công cụ không thay đổi tiêu chí: UI/UX, ít nhất 8 loại biểu đồ, geographic map, filter nhiều cấp, drill-down, tooltip, cross-filtering, 5–7 insight/story và trực quan dự báo vẫn bắt buộc.

Tài liệu này chốt câu hỏi, giả thuyết, story flow, data contract và cổng kiểm tra. EDA đã tạo sáu hình tĩnh, kiểm tra H01–H10 và chốt sáu insight; inventory visual cuối được ghi tại `dashboard/chart-inventory.md`.

## Câu hỏi nghiên cứu

| ID | Câu hỏi phù hợp với OULAD | Kết quả cần có |
|---|---|---|
| RQ1 | Kết quả `Pass/Distinction/Fail/Withdrawn` và tỷ lệ `At_Risk` phân bố ra sao theo module, presentation và thời gian? | Baseline, nhóm có chênh lệch đáng chú ý, mẫu số rõ |
| RQ2 | Mức độ và nhịp tương tác VLE trước cutoff liên hệ thế nào với `At_Risk`? | So sánh click/active days/recency/trend, không gọi là attendance hoặc study hours |
| RQ3 | Tiến độ và kết quả assessment trước cutoff liên hệ thế nào với kết quả cuối khóa? | Submission coverage, điểm weighted, tỷ lệ hoàn thành, nhóm so sánh |
| RQ4 | Prior attempts, studied credits, education, IMD, age, disability và region có khác biệt gì về `At_Risk`? | Tỷ lệ, `N`, missingness và cảnh báo không suy diễn nhân quả |
| RQ5 | Tổ hợp yếu tố nào mô tả rõ các risk profile hơn việc xem từng biến riêng lẻ? | Tương tác ít nhất hai chiều, nhóm đủ cỡ mẫu, thông điệp hành động |
| RQ6 | Logistic Regression nhận diện sớm `At_Risk` tốt đến đâu, ở threshold nào và sai ở nhóm nào? | Metric, confidence interval, confusion matrix, calibration, subgroup QA |

Các câu hỏi tổng quát trong DOCX về attendance, study hours, sleep, lifestyle hoặc điểm học phần trước **không có cột trực tiếp trong OULAD**. RQ2–RQ4 dùng biến thật nêu trên, không chế dữ liệu.

## Giả thuyết cần kiểm tra

Các giả thuyết dưới đây dùng cùng ID với `docs/plan_approved.md`. Kết quả định lượng nằm trong `reports/eda/hypothesis_results.csv`; diễn giải insight nằm trong `docs/insight-log.md`.

| ID | Giả thuyết | RQ |
|---|---|---|
| H01 | Kết quả khác nhau giữa module/presentation. | RQ1 |
| H02 | VLE clicks thấp trước cutoff liên hệ với `At_Risk` cao hơn. | RQ2 |
| H03 | Active days thấp trước cutoff liên hệ với `At_Risk` cao hơn. | RQ2 |
| H04 | Nhóm At-Risk có mức tương tác VLE theo tuần thấp hơn gần cutoff. | RQ2 |
| H05 | Assessment completion thấp trước cutoff liên hệ với rủi ro cao hơn. | RQ3 |
| H06 | Weighted assessment score trước cutoff thấp liên hệ với rủi ro cao hơn. | RQ3 |
| H07 | Prior attempts liên hệ với kết quả. | RQ4 |
| H08 | Education, credits, IMD hoặc region có khác biệt mô tả sau khi công bố `N` và giới hạn. | RQ4 |
| H09 | VLE thấp kết hợp assessment thấp tạo risk profile rõ hơn. | RQ5 |
| H10 | Độ lớn mối liên hệ thay đổi theo module/presentation. | RQ1, RQ5 |

RQ6 và metric Logistic Regression được đánh giá độc lập trong `docs/04-model.md`; không dùng metric model thay cho giả thuyết/insight EDA.

## Mạch storytelling bắt buộc

1. **Điều gì đang xảy ra?** Quy mô, phân bố kết quả và baseline `At_Risk`.
2. **Khi nào dấu hiệu xuất hiện?** Hành vi VLE và assessment trước cutoff.
3. **Yếu tố nào đi cùng nhau?** Tương tác đa biến và khác biệt giữa module/presentation.
4. **Nhóm nào cần chú ý?** Risk profile có đủ `N`, không gán nhãn cá nhân hoặc suy diễn nguyên nhân.
5. **Có thể nhận diện sớm đến đâu?** Xác suất, threshold, metric, confidence interval và loại sai số.
6. **Nên hành động và thận trọng thế nào?** Gợi ý theo dõi/hỗ trợ; nêu giới hạn dữ liệu quan sát, missingness và tính khái quát.

Mỗi trang phải nối với trang trước bằng một câu chuyển ý. Mỗi insight phải trả lời một RQ, trỏ tới H, có số liệu và dẫn đến kết luận/gợi ý cụ thể; không dùng biểu đồ làm vật trang trí.

## Kiến trúc và trách nhiệm

| Lớp | Trách nhiệm |
|---|---|
| Data pipeline | `src/oulad_pipeline.py` tái tạo `clean_dataset.csv`, kiểm tra schema, khóa và hạt một lượt học |
| EDA | Notebook/script tạo ít nhất 3–5 biểu đồ Matplotlib/Seaborn và số liệu cho Insight Log |
| Model | `src/at_risk_model.py` tạo feature tại cutoff, train/evaluate Logistic Regression và xuất artifact kiểm tra |
| Dashboard | `dashboard/app.py` đọc bảng sạch/output model, quản lý state/filter và vẽ Plotly |
| QA | Baseline KPI, test filter/drill/cross-filter, mapping map, ảnh/video và checksum input |

Không đọc 7 bảng raw trực tiếp trong giao diện, không join event table khi render và không train lại model theo mỗi filter. Dashboard chỉ đọc output đã aggregate/kiểm tra. File `.joblib` dùng cho tái tạo model, không phải nguồn trực quan.

## Bốn phần dashboard

| Phần | RQ chính | Nội dung bắt buộc |
|---|---|---|
| Overview | RQ1 | KPI, phân bố kết quả, module/presentation, định nghĩa lượt học và người học |
| Factor Analysis | RQ2–RQ5 | VLE, assessment, đặc điểm nền, tương tác đa biến, số liệu cho insight |
| Risk Analysis | RQ4–RQ5 | Risk profile, region map có nguồn, chênh lệch nhóm và cỡ mẫu |
| Prediction | RQ6 | Xác suất, risk band, Actual vs Predicted, confusion matrix, ROC/PR, calibration, metric/CI |

## Data contract

### Phân tích mô tả

- Nguồn: `data/processed/clean_dataset.csv`.
- Hạt: `(code_module, code_presentation, id_student)`.
- `At_Risk`: `Fail/Withdrawn = 1`; `Pass/Distinction = 0`.
- **Average Assessment Score** = `sum(assessment_score_sum) / sum(assessment_scored_count)` trong filter context; không average các mean theo lượt học.
- VLE clicks là proxy tương tác nền tảng, không phải attendance/study hours.

### Dự báo

- Nguồn chính: `data/processed/model/model_predictions.csv`, hạt một attempt eligible.
- Join/đối chiếu chỉ theo đủ ba khóa; trang đánh giá mặc định `dataset_split = test`.
- Hiển thị `risk_probability`, `predicted_status`, `actual_status`, `risk_band`, `prediction_threshold`, `cutoff_day`, `model_version`.
- Metric đọc từ `model_metrics.csv`; CI từ `model_confidence_intervals.csv`; calibration, curve và subgroup từ output tương ứng.
- Chỉ dùng output khi `model_verification.csv` đạt toàn bộ kiểm tra. Không tính lại metric từ tập đã bị filter mà gắn nhãn như metric toàn test.

### Geographic map

- Geometry: `dashboard/assets/oulad_regions.geojson`, dựng từ ONS Counties and Unitary Authorities theo Open Government Licence v3.0.
- Mapping audit: `dashboard/assets/oulad_regions_mapping.csv`, đủ 13/13 nhãn `region`.
- Đây là xấp xỉ được công bố cho vùng OU lịch sử, không phải polygon chính thức của OU; chi tiết ở `dashboard/assets/README.md`.
- `Ireland` được biểu diễn bằng Northern Ireland như một proxy vì geometry ONS chỉ bao phủ UK, trong khi OULAD dùng nhãn rộng `Ireland`. Channel Islands/Isle of Man và các county bị chia một phần được nêu rõ là giới hạn.
- Không tự đặt centroid hoặc vẽ polygon thủ công. Nếu asset/mapping không đạt kiểm tra, giao diện phải báo **chưa đủ bằng chứng**.

## Tương tác bắt buộc và cách kiểm tra

| Rubric | Thiết kế Python | Bằng chứng tối thiểu |
|---|---|---|
| Filter nhiều cấp | Sidebar lọc Module → Presentation → Region; option sau phụ thuộc option trước | Ảnh/video và kiểm tra số dòng/KPI theo từng bước |
| Drill-down | Chọn/click từ Module xuống Presentation hoặc từ risk band xuống attempt | State trước/sau, breadcrumb và số liệu đúng |
| Tooltip hover | Plotly `hover_data` có metric, mẫu số/`N` và định nghĩa ngắn | Ảnh hover ở ít nhất các visual chính |
| Cross-filtering | Selection event của một chart cập nhật chart/KPI liên quan | Video/ảnh trước-sau và test filter context |

## Inventory visual đã triển khai local

Để không nhập nhằng giữa tiêu chí đa dạng biểu đồ và tiêu chí map, phương án triển khai gồm **9 loại biểu đồ không phải map** và **1 Geographic Map bắt buộc riêng**:

| STT | Loại | Mục đích chính | Phần |
|---:|---|---|---|
| 1 | Donut chart | Tỷ trọng bốn lớp `final_result` | Overview |
| 2 | Stacked bar chart | Kết quả theo module/presentation | Overview |
| 3 | Sunburst chart | Drill-down Module → Presentation → Kết quả | Overview |
| 4 | Line chart | Diễn biến VLE/active days theo thời gian | Factor Analysis |
| 5 | Box plot | Phân bố assessment giữa các nhóm kết quả | Factor Analysis |
| 6 | Scatter/Bubble chart | Quan hệ assessment, VLE và `At_Risk` | Factor Analysis |
| 7 | Heatmap | Tương tác VLE × assessment và tỷ lệ `At_Risk` | Factor/Risk |
| 8 | Treemap | Quy mô và tỷ lệ của các risk profile | Risk Analysis |
| 9 | Histogram | Phân bố xác suất dự báo | Prediction |
| Map | Choropleth Geographic Map | Phân bố không gian của `At_Risk` theo region | Risk Analysis |

Confusion matrix, ROC/PR curve và calibration plot vẫn bắt buộc để giải thích model, nhưng không được dùng để thổi phồng số loại vì chúng lặp cấu trúc heatmap/line/scatter.

Mỗi visual đã được đối chiếu RQ/insight, dữ liệu, tooltip và interaction tại `dashboard/chart-inventory.md`. EDA và inventory hiện giữ đủ chín loại không phải map cùng Geographic Map độc lập.

## Điều kiện nghiệm thu

- Sáu biểu đồ EDA tĩnh và kết quả H01–H10 có đường dẫn trong `reports/eda/`.
- Sáu insight đạt mẫu trong `docs/insight-log.md` và ghép thành story flow.
- KPI không filter khớp `dashboard/qa-t09.md`.
- Đủ 9 loại chart không phải map; Geographic Map đạt cổng riêng; có filter nhiều cấp, drill-down, tooltip và cross-filtering.
- Prediction khớp output model/version/cutoff/threshold và có Actual vs Predicted.
- App chạy từ môi trường sạch bằng lệnh trong README; không chứa secrets hoặc dữ liệu giả.

Không đánh dấu rubric hoàn thành chỉ vì app khởi động hoặc đã chọn thư viện.
