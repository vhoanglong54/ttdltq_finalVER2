# PLAN_APPROVED — Phương án triển khai cuối đã duyệt

**Tên đề tài:** Nghiên cứu và phân tích các yếu tố ảnh hưởng đến kết quả học tập của sinh viên đại học

**Cập nhật:** 07/10/2026

**Người thực hiện chính:** Leader dự án

**Công nghệ:** Python, Pandas, scikit-learn, Streamlit và Plotly

**Nguyên tắc Git:** chỉ commit/push sau khi leader xem và cho phép
**Nguồn rubric được bảo vệ:** không chỉnh sửa `02-rubric-traceability.md` và `source/TTDLTQ_script.docx`.

## 1. Mục tiêu nghiên cứu

Phân tích những yếu tố học tập liên quan đến khả năng qua môn, trượt hoặc bỏ học. Sau đó dùng Logistic Regression với dữ liệu có đến ngày 105 để cảnh báo sớm một lượt học có khả năng kết thúc bằng trượt hoặc bỏ học. Mô hình không dự đoán điểm số chính xác.

Đây là dữ liệu quan sát. Kết luận dùng từ **liên hệ**, **khác biệt**, **xu hướng**; không tuyên bố quan hệ nhân quả.

## 2. Câu hỏi phân tích

1. Tỷ lệ qua môn, trượt và bỏ học khác nhau thế nào giữa các học phần và khu vực?
2. Mức tham gia học trực tuyến liên quan thế nào đến kết quả cuối cùng?
3. Mức hoàn thành bài đến hạn và thời điểm nộp bài liên quan thế nào đến kết quả và điểm số?
4. Khi mức tham gia học trực tuyến và điểm bài tập cùng thấp, nguy cơ không đạt thay đổi ra sao?
5. Sinh viên từng học lại học phần có nguy cơ khác nhóm học lần đầu ra sao?
6. Mô hình dự đoán trượt/bỏ học chính xác đến đâu và ai cần được ưu tiên hỗ trợ?

## 3. Quy ước dữ liệu

- Hạt chính: `(code_module, code_presentation, id_student)` — một lượt sinh viên học một học phần trong một đợt mở lớp.
- `At_Risk = 1`: `Fail` hoặc `Withdrawn`; `At_Risk = 0`: `Pass` hoặc `Distinction`.
- Pass Rate: `Pass` hoặc `Distinction` chia tổng learning attempts.
- Điểm trung bình: tổng điểm hợp lệ chia số assessment có điểm, không lấy trung bình chồng trung bình.
- VLE là hệ thống học trực tuyến; số lượt tương tác chỉ phản ánh mức độ sử dụng hệ thống, không phải giờ học hay điểm danh.
- Mô hình chỉ dùng thông tin có ngày `<= 105`; dashboard không huấn luyện lại mô hình.
- Risk Level phục vụ can thiệp: Low `<40%`, Medium `40–<70%`, High `≥70%`.
- Threshold phân loại chính thức của model vẫn là `0,415`; risk level không viết lại nhãn dự báo.

## 4. Story đã chốt — bốn trang vật lý

Dashboard bám cấu trúc bốn trang của rubric và tách insight dữ liệu khỏi model:

1. **Bức tranh kết quả học tập:** quy mô trượt/bỏ học, cơ cấu kết quả, học phần và vùng.
2. **Các yếu tố học tập:** mức tham gia học trực tuyến, hoàn thành bài, thời điểm nộp và tài nguyên được sử dụng.
3. **Kết hợp nhiều yếu tố:** mức tham gia × điểm bài tập; hoàn cảnh đầu vào; lịch sử học lại.
4. **Dự đoán nguy cơ:** khả năng trượt/bỏ học, dự đoán đúng/sai, trường hợp bỏ sót và danh sách ưu tiên hỗ trợ.

Mạch Story: **Kết quả hiện tại ra sao → yếu tố học tập nào liên quan rõ → điều gì xảy ra khi nhiều yếu tố bất lợi cùng xuất hiện → mô hình cảnh báo ai để hỗ trợ.**

## 5. Kết luận trọng tâm phải thể hiện rõ

1. **Hoàn thành bài đến hạn là yếu tố liên quan rõ nhất:** nhóm chưa hoàn thành bài có nguy cơ không đạt 96,6%, trong khi nhóm hoàn thành đủ là 24,8%.
2. **Mức tham gia học trực tuyến có liên hệ mạnh:** nhóm 25% ít tương tác nhất có nguy cơ không đạt 64,4%, còn nhóm 25% tương tác nhiều nhất là 18,7%.
3. **Hai yếu tố bất lợi cùng xuất hiện làm nguy cơ nổi bật hơn:** nhóm vừa ít tương tác vừa có điểm bài tập thấp có nguy cơ 73,3%; nhóm cao ở cả hai chỉ 8,3%.
4. **Lịch sử học lại là bối cảnh cần chú ý:** nhóm từng học học phần trước có nguy cơ 56,1%, nhóm học lần đầu là 36,3%.
5. Học phần, khu vực, học vấn đầu vào và hoàn cảnh kinh tế–xã hội chỉ là **bối cảnh có chênh lệch**, không được khẳng định là nguyên nhân.

## 6. Bố cục biểu đồ

| Trang | Biểu đồ và chức năng |
|---|---|
| 1 · Bức tranh kết quả học tập | Filled Geographic Map; 100% Stacked Bar có drill học phần ẩn danh → đợt mở lớp; 4 KPI; Story về kết quả chung và bối cảnh |
| 2 · Các yếu tố học tập | Multi-Line về mức tham gia trực tuyến; Completion Bar; Scatter + Trendline; Treemap; Story nêu hai yếu tố liên quan rõ nhất |
| 3 · Kết hợp nhiều yếu tố | Heatmap mức tham gia × điểm; Heatmap học vấn × hoàn cảnh khu vực; Box Plot lịch sử học lại; Story nêu kết luận kết hợp |
| 4 · Dự đoán nguy cơ | 3 KPI; Gauge; Donut đúng/sai/bỏ sót; danh sách ưu tiên hỗ trợ; Story nói rõ mô hình dự đoán trượt/bỏ học |

Thuật ngữ OULAD, VLE, IMD, mã AAA–GGG và B/J phải được giải thích ngay trên dashboard. Các chỉ số mô hình phải được diễn giải bằng câu “trong 100 lượt học”. Không dùng nhãn “Câu chuyện”; tên khối kết luận thống nhất là **Story**.

## 7. Insight đặt ở đâu

- Trang 1: tỷ lệ trượt/bỏ học tổng thể; học phần và vùng là bối cảnh so sánh.
- Trang 2: hoàn thành bài và mức tham gia trực tuyến là hai yếu tố học tập nổi bật.
- Trang 3: so sánh nhóm thấp ở cả mức tham gia và điểm với nhóm cao ở cả hai; thêm lịch sử học lại.
- Trang 4: nói rõ mô hình dự đoán trượt/bỏ học, mức đúng, mức phát hiện và số trường hợp bỏ sót.

## 8. Đủ yêu cầu trực quan

Có ít nhất **8 loại biểu đồ không phải map**: 100% stacked bar, multi-line, bar, scatter, treemap, heatmap, box plot, gauge và donut. Geographic Map là cổng bắt buộc độc lập.

Mỗi biểu đồ có tiêu đề, trục/đơn vị, tooltip, phạm vi và `N` khi cần. Màu thống nhất: xanh cho nhóm không nguy cơ; cam cho cảnh báo; đỏ cho nhóm có nguy cơ cao.

## 9. Data mart phục vụ dashboard

`src/dashboard_features.py` tạo bốn bảng nhỏ từ dữ liệu interim đã clean:

- `assessment_deadlines.csv`
- `assessment_submissions.csv.gz`
- `vle_daily_profile.csv.gz`
- `vle_activity_summary.csv.gz`

App không đọc `studentVle.csv` 8,4 triệu dòng trong request render. Hai bảng VLE phải bảo toàn tổng `39.605.099` clicks.

## 10. Cổng nghiệm thu

- Trang 1 render 2 chart/4 KPI; Trang 2 render 4 chart; Trang 3 render 3 chart; Trang 4 render 2 chart/3 KPI/1 table; tất cả không exception.
- Map render 13/13 region, click region tạo cross-filter và có reset.
- Module bar drill xuống presentation; breadcrumb hiển thị đúng cấp.
- Risk Level/IMD filter cập nhật chart, KPI và action list.
- Model verification phải PASS; test metric công bố: Accuracy 82,7%, Recall 73,5%.
- Automated test, visual QA, link check và `git diff --check` phải PASS.
- Không sửa hai file rubric được bảo vệ.
- Không commit/push trước khi leader duyệt.
