# PLAN_APPROVED — Phương án triển khai cuối đã duyệt

**Cập nhật:** 07/10/2026

**Người thực hiện chính:** Leader dự án

**Công nghệ:** Python, Pandas, scikit-learn, Streamlit và Plotly

**Nguyên tắc Git:** chỉ commit/push sau khi leader xem và cho phép
**Nguồn rubric được bảo vệ:** không chỉnh sửa `02-rubric-traceability.md` và `source/TTDLTQ_script.docx`.

## 1. Mục tiêu nghiên cứu

Phân tích các yếu tố học tập, hành vi VLE và bối cảnh người học có liên hệ với kết quả học tập; sau đó dùng Logistic Regression tại ngày 105 để cảnh báo sớm một learning attempt có khả năng kết thúc bằng `Fail` hoặc `Withdrawn`.

Đây là dữ liệu quan sát. Kết luận dùng từ **liên hệ**, **khác biệt**, **xu hướng**; không tuyên bố quan hệ nhân quả.

## 2. Câu hỏi phân tích

1. Kết quả và At-Risk phân bố thế nào theo module, presentation và region?
2. Nhịp tương tác VLE của At-Risk khác Not-At-Risk ra sao theo thời gian?
3. Độ trễ nộp bài liên hệ thế nào với điểm assessment và lịch sử học lại?
4. Người học sử dụng những loại tài nguyên VLE nào nhiều nhất?
5. Tổ hợp `highest_education × imd_band` nào có tỷ lệ At-Risk cao?
6. Logistic Regression nhận diện At-Risk tốt đến đâu và ai cần được ưu tiên hỗ trợ?

## 3. Quy ước dữ liệu

- Hạt chính: `(code_module, code_presentation, id_student)` — một learning attempt.
- `At_Risk = 1`: `Fail` hoặc `Withdrawn`; `At_Risk = 0`: `Pass` hoặc `Distinction`.
- Pass Rate: `Pass` hoặc `Distinction` chia tổng learning attempts.
- Điểm trung bình: tổng điểm hợp lệ chia số assessment có điểm, không lấy trung bình chồng trung bình.
- VLE click là proxy tương tác nền tảng, không phải attendance hay study hours.
- Model dùng snapshot chỉ chứa thông tin có ngày `<= 105`; dashboard không train lại model.
- Risk Level phục vụ can thiệp: Low `<40%`, Medium `40–<70%`, High `≥70%`.
- Threshold phân loại chính thức của model vẫn là `0,415`; risk level không viết lại nhãn dự báo.

## 4. Storytelling cuối — hai trang vật lý

Rubric gốc mô tả bốn phần nội dung. Bản triển khai mới **không bỏ nội dung**, mà gom chúng vào hai trang rõ hơn:

1. **Academic Insight & Behavior:** mô tả kết quả + yếu tố/hành vi + không gian.
2. **Risk Matrix & Early Warning:** tương tác đa biến + mô hình + danh sách hành động.

Mạch kể chuyện: **Ai và ở đâu đang gặp rủi ro → hành vi nào đi cùng kết quả → tổ hợp bối cảnh nào đáng chú ý → model cảnh báo ai để hỗ trợ sớm.**

## 5. Trang 1 — Academic Insight & Behavior

### Bộ lọc và KPI

- Slicers: `code_module`, `code_presentation`, `gender`.
- KPI: Total Students, Avg Score, Pass Rate, At-Risk Rate.
- Click một vùng trên map tạo cross-filter cho KPI và bốn chart còn lại; có nút bỏ lọc vùng.

### Năm biểu đồ

| # | Biểu đồ | Nội dung và tương tác |
|---:|---|---|
| 1 | Filled Geographic Map | 13 vùng OULAD, màu theo At-Risk rate, tooltip có rate/count/N, click vùng để cross-filter |
| 2 | 100% Stacked Bar | Cơ cấu Distinction/Pass/Fail/Withdrawn; click module để drill xuống presentation |
| 3 | Multi-Line | VLE clicks trung bình/lượt/ngày, trung bình trượt 7 ngày; At-Risk so với Not-At-Risk; vạch chấm là hạn nộp quan trọng |
| 4 | Scatter + Trendline | `submission_delay` so với `score`; kích thước theo `num_of_prev_attempts`; màu theo At-Risk; trendline tính trên toàn bộ dữ liệu lọc |
| 5 | Treemap | Tỷ trọng tổng click theo `activity_type` |

### Ba insight/story động

1. Pass Rate và At-Risk Rate trong filter context.
2. Chênh lệch VLE clicks trung bình giữa At-Risk và Not-At-Risk.
3. Tương quan Pearson giữa độ trễ–điểm, kèm loại tài nguyên VLE dẫn đầu.

## 6. Trang 2 — Risk Matrix & Early Warning

### Bộ lọc và KPI

- Slicers: Risk Level và `imd_band`.
- KPI: Model Accuracy, Recall At-Risk, High Risk Count.
- KPI theo filter context được ghi rõ `N`; metric công bố toàn test vẫn hiện trong caption để đối chiếu.

### Bốn biểu đồ và một bảng hành động

| # | Biểu đồ | Nội dung |
|---:|---|---|
| 6 | Heatmap Matrix | Hàng `highest_education`, cột `imd_band`, màu At-Risk rate, từng ô có `N` |
| 7 | Box Plot | Điểm assessment có trọng số đến ngày 105 theo số lần học trước `0,1,2,3+` |
| 8 | Gauge | Xác suất At-Risk trung bình với dải Low/Medium/High; vạch tím là threshold model 41,5% |
| 9 | Donut Actual vs Predicted | TP, TN, FP, FN; nhấn mạnh FN là trường hợp At-Risk bị bỏ sót |
| — | Student Action List | `student_id`, module, presentation, IMD, probability, model status và data bar đỏ; nút một-click lọc toàn Trang 2 về High Risk; tối đa 100 dòng |

### Ba insight/story động

1. Tổ hợp education × IMD có At-Risk rate cao nhất trong các ô `N≥30`.
2. So sánh điểm trung vị nhóm chưa học trước với nhóm `3+` lần.
3. Xác suất trung bình, High Risk Count, Accuracy, Recall và số FN trong filter context.

## 7. Đủ yêu cầu trực quan

Có **8 loại biểu đồ không phải map**: 100% stacked bar, multi-line, scatter, treemap, heatmap, box plot, gauge và donut. Geographic Map là loại thứ chín và là cổng bắt buộc độc lập.

Mỗi chart có title, axis/đơn vị, tooltip, chú thích grain/scope và `N` khi cần. Màu semantic thống nhất: xanh cho an toàn/Not-At-Risk; cam cho cảnh báo; đỏ cho At-Risk/High Risk.

## 8. Data mart phục vụ dashboard

`src/dashboard_features.py` tạo bốn bảng nhỏ từ dữ liệu interim đã clean:

- `assessment_deadlines.csv`
- `assessment_submissions.csv.gz`
- `vle_daily_profile.csv.gz`
- `vle_activity_summary.csv.gz`

App không đọc `studentVle.csv` 8,4 triệu dòng trong request render. Hai bảng VLE phải bảo toàn tổng `39.605.099` clicks.

## 9. Cổng nghiệm thu

- Page 1 mặc định render 5 Plotly charts, 4 KPI, không exception.
- Page 2 mặc định render 4 Plotly charts, 3 KPI, 1 action table, không exception.
- Map render 13/13 region, click region tạo cross-filter và có reset.
- Module bar drill xuống presentation; breadcrumb hiển thị đúng cấp.
- Risk Level/IMD filter cập nhật chart, KPI và action list.
- Model verification phải PASS; test metric công bố: Accuracy 82,7%, Recall 73,5%.
- Automated test, visual QA, link check và `git diff --check` phải PASS.
- Không sửa hai file rubric được bảo vệ.
- Không commit/push trước khi leader duyệt.
