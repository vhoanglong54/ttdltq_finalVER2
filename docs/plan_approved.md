# PLAN APPROVED — Phương án thực hiện đồ án

**Trạng thái:** Đã được chủ dự án duyệt ngày 06/10/2026.  
**Phạm vi:** Một người thực hiện chính toàn bộ data, EDA, insight, model, dashboard, báo cáo và demo.  
**Quy tắc Git:** Tài liệu này được lưu local; chỉ commit/push khi chủ dự án cho phép rõ ràng.  
**Nguồn yêu cầu được bảo vệ:** Không chỉnh sửa `docs/02-rubric-traceability.md` hoặc PHẦN II của DOCX nguồn.

## 1. Mục tiêu

Phân tích các yếu tố có **liên hệ** với kết quả học tập trên OULAD và xây dựng mô hình nhận diện sớm một lượt học có nguy cơ:

- `At_Risk = 1`: `Fail` hoặc `Withdrawn`.
- `At_Risk = 0`: `Pass` hoặc `Distinction`.

Luồng project:

> OULAD → audit → cleaning → aggregate/join → EDA → kiểm tra giả thuyết → insight → storytelling → Logistic Regression → trực quan dự báo → dashboard Python → báo cáo/demo.

OULAD là dữ liệu quan sát. Kết luận chỉ dùng từ **liên hệ, khác biệt, xu hướng**, không khẳng định quan hệ nhân quả.

## 2. Công nghệ

- Xử lý dữ liệu: Python, Pandas, NumPy.
- EDA tĩnh: Matplotlib, Seaborn.
- Model: scikit-learn Logistic Regression.
- Dashboard: Streamlit + Plotly.
- Geographic Map: GeoJSON có nguồn và giấy phép.
- Môi trường: `requirements.txt`.

## 3. Data contract

Nguồn là Open University Learning Analytics Dataset — OULAD, gồm bảy bảng liên kết:

1. `studentInfo`
2. `studentRegistration`
3. `studentAssessment`
4. `assessments`
5. `studentVle`
6. `vle`
7. `courses`

Hạt phân tích:

```text
(code_module, code_presentation, id_student)
```

Một dòng là một **learning attempt**, không nhất thiết là một sinh viên duy nhất.

Quy tắc bắt buộc:

- Giữ nguyên raw; không sửa CSV thủ công.
- Aggregate assessment/VLE về đúng hạt trước khi join.
- Không tạo dữ liệu giả về sleep, stress, motivation, attendance hoặc study hours.
- VLE clicks là tương tác trên nền tảng, không phải giờ học hoặc điểm danh.
- `imd_band` là mức thiếu thốn của khu vực, không phải thu nhập cá nhân.
- Mọi tỷ lệ ghi tử số, mẫu số, filter context và `N`.

## 4. Câu hỏi nghiên cứu

### Câu hỏi phân tích dữ liệu

- **RQ1 — Phân bố kết quả:** `Pass/Distinction/Fail/Withdrawn` và `At_Risk` khác nhau thế nào theo module/presentation?
- **RQ2 — Tương tác VLE:** mức độ, tần suất và xu hướng VLE liên hệ thế nào với kết quả?
- **RQ3 — Assessment:** tiến độ, completion và điểm assessment liên hệ thế nào với kết quả?
- **RQ4 — Đặc điểm và không gian:** prior attempts, credits, education, age, disability, IMD và region có khác biệt gì về `At_Risk`?
- **RQ5 — Tương tác đa yếu tố:** tổ hợp VLE, assessment và đặc điểm học tập nào tạo thành risk profile rõ nhất?

### Câu hỏi model độc lập

- **RQ6 — Dự báo:** Logistic Regression nhận diện sớm `At_Risk` tốt đến đâu, threshold nào phù hợp và model thường sai ở đâu?

RQ6 thuộc phần model, không thay thế insight phân tích của RQ1–RQ5.

## 5. EDA và giả thuyết

EDA phải có ít nhất 3–5 biểu đồ tĩnh Matplotlib/Seaborn và kiểm tra các giả thuyết:

1. Kết quả khác nhau giữa module/presentation.
2. VLE clicks thấp liên hệ với `At_Risk` cao hơn.
3. Active days thấp liên hệ với `At_Risk` cao hơn.
4. Tương tác VLE giảm hoặc gián đoạn gần cutoff liên hệ với rủi ro.
5. Assessment completion thấp liên hệ với rủi ro.
6. Điểm assessment trước cutoff thấp liên hệ với rủi ro.
7. Prior attempts liên hệ với kết quả.
8. Education, credits, IMD hoặc region có khác biệt.
9. VLE thấp kết hợp assessment thấp tạo risk profile rõ hơn.
10. Mối liên hệ thay đổi theo module/presentation.

Mỗi giả thuyết được ghi một trong ba trạng thái: **Ủng hộ / Không ủng hộ / Chưa đủ bằng chứng**.

## 6. Insight phân tích

Chọn 5–7 insight, mục tiêu là sáu insight. Insight phải được rút ra từ dữ liệu và biểu đồ; metric model không được tính là insight.

| ID | Chủ đề cần tìm | Bằng chứng trực quan dự kiến |
|---|---|---|
| INS-01 | Chênh lệch kết quả theo module/presentation | Donut, stacked bar, sunburst |
| INS-02 | Mức độ và xu hướng tương tác VLE | Line, box plot |
| INS-03 | Tiến độ/completion/điểm assessment | Box plot, stacked bar |
| INS-04 | Tương tác VLE × assessment | Scatter/bubble, heatmap |
| INS-05 | Risk profile từ lịch sử và đặc điểm học tập | Treemap, heatmap, stacked bar |
| INS-06 | Phân bố không gian của rủi ro | Geographic Map và bar đối chiếu nếu cần |

Đây là hướng tìm insight, chưa phải kết luận. Nội dung cuối chỉ được chốt sau EDA.

Mỗi insight hợp lệ phải có:

- RQ và giả thuyết liên quan.
- Biểu đồ/bảng bằng chứng tái tạo được.
- Số liệu, tử số, mẫu số và `N`.
- Nhóm so sánh và filter context.
- Diễn giải bằng ngôn ngữ liên hệ.
- Missingness, yếu tố gây nhiễu và giới hạn.
- Ý nghĩa thực tế hoặc bước phân tích tiếp theo.

## 7. Inventory biểu đồ

Phương án an toàn gồm **9 loại biểu đồ không phải map** và **1 Geographic Map bắt buộc riêng**.

| STT | Loại biểu đồ | Nội dung | Liên kết phân tích |
|---:|---|---|---|
| 1 | Donut chart | Tỷ trọng bốn lớp kết quả | RQ1 / INS-01 |
| 2 | Stacked bar chart | Kết quả theo module/presentation | RQ1 / INS-01 |
| 3 | Sunburst chart | Drill-down Module → Presentation → Kết quả | RQ1 / INS-01 |
| 4 | Line chart | VLE/active days theo thời gian | RQ2 / INS-02 |
| 5 | Box plot | Phân bố VLE hoặc assessment theo kết quả | RQ2–RQ3 / INS-02–03 |
| 6 | Scatter/Bubble chart | Assessment × VLE × kết quả | RQ5 / INS-04 |
| 7 | Heatmap | Tương tác VLE × assessment/đặc điểm | RQ5 / INS-04–05 |
| 8 | Treemap | Quy mô và tỷ lệ risk profile | RQ4–RQ5 / INS-05 |
| 9 | Histogram | Phân bố xác suất dự báo | RQ6 / Model |
| Map | Choropleth Geographic Map | Phân bố không gian của `At_Risk` | RQ4 / INS-06 |

Confusion matrix, ROC/PR curve và calibration plot vẫn phải làm cho model nhưng không tính thành loại mới nếu trùng cấu trúc heatmap, line hoặc scatter.

Sau EDA có thể thay một chart không phù hợp, nhưng vẫn phải giữ ít nhất chín loại không phải map và Geographic Map độc lập.

## 8. Geographic Map — cổng bắt buộc riêng

Map không được dùng để bù vào số loại biểu đồ thông thường.

- Loại: Choropleth Map.
- Đơn vị: 13 `region` của OULAD.
- Measure chính: `At-Risk Rate`.
- Tooltip: Region, learning attempts, At-Risk count, At-Risk rate.
- Filter: Module và Presentation.
- Geometry phải có nguồn và giấy phép.
- Mapping phải khớp 13/13 region.
- Cách xử lý `Ireland` phải được giải thích.
- Không tự tạo centroid hoặc polygon.
- Tổng `N` trên map phải khớp filter context.
- Phân biệt vùng không có dữ liệu với tỷ lệ bằng 0.

Nếu chưa có geometry hợp lệ, map phải ghi **chưa hoàn thành**, không được thay bằng bar chart.

## 9. Bốn phần dashboard

### Overview

- KPI tổng quan.
- Phân bố kết quả.
- So sánh module/presentation.
- Donut, stacked bar, sunburst.

### Factor Analysis

- VLE clicks, active days và xu hướng theo thời gian.
- Assessment completion và score.
- Tương tác VLE × assessment.
- Line, box plot, scatter/bubble, heatmap.

### Risk Analysis

- Prior attempts, credits, education, IMD.
- Risk profile.
- Phân bố không gian.
- Treemap, heatmap và Geographic Map.

### Prediction

- Xác suất `At_Risk`, risk band và threshold.
- Actual vs Predicted.
- False Positive/False Negative.
- Metric, confidence interval và calibration.
- Histogram, confusion matrix, ROC/PR và calibration plot.

## 10. Tương tác bắt buộc

- Filter nhiều cấp: Module → Presentation → Region.
- Drill-down: Module → Presentation → Kết quả.
- Tooltip hover có metric, mẫu số và `N`.
- Cross-filtering giữa các biểu đồ.
- Reset filter và hiển thị filter context.
- Empty state khi không có dữ liệu.
- Prediction mặc định dùng test split.
- Không lấy metric của subgroup đã filter rồi gắn nhãn là metric toàn test.

## 11. Model — phần độc lập với insight

Chỉ dùng Logistic Regression vì target là phân loại nhị phân và thuật toán này phù hợp rubric.

- Target: `At_Risk`.
- Cutoff: ngày 105.
- Chỉ dùng dữ liệu xuất hiện trước hoặc tại cutoff.
- Split theo `id_student` để tránh cùng sinh viên xuất hiện ở nhiều tập.
- Tune/CV trên train.
- Chọn threshold trên validation.
- Đánh giá cuối trên test.
- Threshold hiện tại: khoảng `0,415`.

Metric test hiện tại:

| Metric | Giá trị |
|---|---:|
| Accuracy | 82,7% |
| Precision At-Risk | 80,2% |
| Recall At-Risk | 73,5% |
| F1 At-Risk | 76,7% |
| ROC-AUC | 0,891 |
| PR-AUC | 0,870 |

Các số trên là kết quả đánh giá model, **không phải insight phân tích**.

Phần model phải giải thích feature, leakage guard, split, threshold, metric, confidence interval, calibration, sai số và giới hạn sử dụng.

## 12. Storytelling

### Story phân tích

1. Kết quả học tập đang phân bố thế nào?
2. Chênh lệch tập trung ở module/presentation nào?
3. VLE cho thấy dấu hiệu gì?
4. Assessment bổ sung bằng chứng gì?
5. Khi VLE và assessment kết hợp, risk profile nào xuất hiện?
6. Risk profile liên hệ thế nào với lịch sử và đặc điểm học tập?
7. Rủi ro phân bố theo không gian ra sao?
8. Tổng hợp 5–7 insight và giới hạn.

### Chuyển sang model

> Từ các dấu hiệu quan sát được, Logistic Regression có thể nhận diện sớm `At_Risk` đến mức nào?

### Story model

1. Model dự báo điều gì và tại thời điểm nào?
2. Threshold được chọn thế nào?
3. Model đúng bao nhiêu và bỏ sót bao nhiêu trường hợp At-Risk?
4. Xác suất có đáng tin cậy không?
5. Model nên và không nên được sử dụng thế nào?

Thông điệp cuối:

> Model là công cụ cảnh báo sớm để ưu tiên theo dõi, không phải công cụ tự động quyết định sinh viên nào sẽ thất bại.

## 13. QA và bằng chứng

### Data QA

- Số dòng/cột, checksum, duplicate key.
- Join cardinality, missing, outlier và grain.

### Insight QA

- Có 5–7 insight thực tế.
- Mỗi insight có biểu đồ, số liệu, `N` và giới hạn.
- Không dùng metric model thay cho insight.
- Không suy diễn nhân quả.

### Dashboard QA

- Đủ 9 loại biểu đồ không phải map.
- Geographic Map được nghiệm thu riêng.
- Filter nhiều cấp, drill-down, tooltip, cross-filtering.
- Reset, empty state và KPI khớp baseline Python.

### Model QA

- Verification PASS.
- Đúng model version, cutoff, threshold và test split.
- Metric khớp artifact; Actual vs Predicted đúng.
- Không leakage.

## 14. Thứ tự thực hiện

1. Giữ ổn định data contract và model hiện tại.
2. Hoàn thành EDA.
3. Ghi kết quả H01–H10.
4. Chọn 5–7 insight phân tích.
5. Chốt story phân tích.
6. Chốt inventory biểu đồ dựa trên insight.
7. Hoàn thiện bốn phần Streamlit.
8. Bổ sung Geographic Map có nguồn.
9. Hoàn thiện interaction.
10. Đối chiếu KPI và model output.
11. Chạy app từ môi trường sạch.
12. Ghi evidence.
13. Viết báo cáo, slide, video và kịch bản demo.

## 15. Nguyên tắc nghiệm thu

- Không sửa rubric để khớp hiện vật.
- Không đánh dấu hoàn thành chỉ vì file tồn tại hoặc app khởi động.
- Insight, model và trực quan dự báo là ba nhóm bằng chứng riêng.
- Geographic Map là cổng độc lập với tiêu chí đa dạng biểu đồ.
- Chỉ commit/push khi chủ dự án duyệt rõ ràng.
