# 05 — Đặc tả dashboard Python bốn trang

**Đề tài:** Nghiên cứu và phân tích các yếu tố ảnh hưởng đến kết quả học tập của sinh viên đại học

## 1. Mục tiêu và mạch Story

Dashboard trả lời tuần tự bốn câu hỏi:

1. **Bức tranh kết quả học tập:** sinh viên đang đạt kết quả thế nào và khác biệt xuất hiện ở đâu?
2. **Các yếu tố học tập:** mức tham gia học trực tuyến, tiến độ làm bài và thời điểm nộp bài liên quan thế nào đến kết quả?
3. **Kết hợp nhiều yếu tố:** khi mức tham gia và điểm bài tập cùng thấp, nguy cơ thay đổi ra sao?
4. **Dự đoán nguy cơ:** mô hình dự đoán trượt/bỏ học tốt đến đâu và ai cần được ưu tiên hỗ trợ?

Insight dữ liệu nằm ở ba trang đầu. Logistic Regression là phần riêng ở Trang 4; metric model không thay thế insight phân tích.

## 2. Kiến trúc

```text
7 bảng OULAD đã clean
  ├─ clean_dataset.csv ───────────────► KPI, outcome, map
  ├─ dashboard marts ─────────────────► VLE, submission, activity
  └─ feature_snapshot + predictions ──► interaction, model, action list
                                           │
                                           ▼
                                Streamlit + Plotly (4 trang)
```

- Entry point: `dashboard/app.py`.
- Loader/schema/KPI: `dashboard/dashboard_data.py`.
- Data mart builder: `src/dashboard_features.py`.
- App chỉ đọc artifact; không train model hoặc join bảng VLE nhiều triệu dòng khi render.

## 3. Thuật ngữ bắt buộc hiển thị

| Thuật ngữ | Giải thích trên dashboard |
|---|---|
| OULAD | Open University Learning Analytics Dataset |
| VLE | Hệ thống học trực tuyến; số lượt tương tác không phải giờ học hay điểm danh |
| AAA–GGG | Mã học phần đã được ẩn danh; không phải tên môn thật |
| B/J | Đợt mở lớp bắt đầu tháng 2/tháng 10 |
| Có nguy cơ không đạt | Kết quả cuối là trượt hoặc bỏ học |
| Bài đánh giá | Bài kiểm tra hoặc bài tập được chấm điểm |
| Ngày 105 | Chỉ dùng thông tin có sẵn đến ngày 105 cho dự đoán sớm |
| IMD | Nhóm mức khó khăn kinh tế–xã hội của khu vực cư trú |
| Tỷ lệ phát hiện | Trong 100 lượt thực sự có nguy cơ, mô hình tìm được bao nhiêu lượt |
| Bỏ sót | Lượt thực sự có nguy cơ nhưng mô hình không cảnh báo |

## 4. Trang 1 — Bức tranh kết quả học tập

- Filter: học phần ẩn danh, đợt mở lớp và giới tính.
- KPI: tổng sinh viên, điểm trung bình, tỷ lệ qua môn, tỷ lệ có nguy cơ không đạt.
- **Story đầu trang:** nói rõ cứ 100 lượt học có bao nhiêu lượt trượt/bỏ học; học phần và vùng chỉ là bối cảnh có chênh lệch.
- **Filled Map:** 13 vùng, màu theo tỷ lệ có nguy cơ không đạt; click vùng lọc KPI và biểu đồ kết quả.
- **100% Stacked Bar:** bốn kết quả; nhãn cuối thanh gộp trượt + bỏ học; click học phần để xem từng đợt mở.
- Mỗi thanh bắt buộc hiển thị đủ miền 0–100%; caption giải thích AAA–GGG và B/J.

## 5. Trang 2 — Các yếu tố học tập

- Dùng cùng filter học phần–đợt mở–giới tính.
- **Story đầu trang:** nêu ngay hoàn thành bài là yếu tố liên quan rõ nhất, sau đó đến mức tham gia học trực tuyến.
- **Multi-Line:** mức tương tác trực tuyến trung bình của nhóm có nguy cơ và nhóm không nguy cơ; đánh dấu hạn nộp quan trọng.
- **Completion Bar:** tỷ lệ có nguy cơ không đạt theo bốn mức hoàn thành bài đến hạn.
- **Scatter + Trendline:** số ngày nộp sớm/trễ và điểm; kích thước điểm theo số lần từng học học phần.
- **Treemap:** tỷ trọng sử dụng theo loại tài nguyên học trực tuyến.

VLE click chỉ là dấu vết tương tác nền tảng, không được gọi là attendance, thời gian học hoặc chất lượng học.

## 6. Trang 3 — Kết hợp nhiều yếu tố

- Dùng dữ liệu có đến ngày 105 và cùng bộ lọc học phần–đợt mở–giới tính.
- **Mức tham gia × Điểm Heatmap:** bốn nhóm mức tương tác × bốn nhóm điểm; từng ô có tỷ lệ và N.
- **Education × IMD Heatmap:** học vấn trước đó × nhóm IMD; từng ô có rate và N.
- **Box Plot:** điểm assessment có trọng số theo số lần học trước `0,1,2,3+`.
- **Story đầu trang:** so sánh nhóm thấp ở cả mức tham gia và điểm với nhóm cao ở cả hai; nêu chênh lệch nguy cơ giữa nhóm từng học lại và nhóm học lần đầu.

Trang này chỉ mô tả tương tác quan sát; không gán nguyên nhân hoặc định kiến cá nhân từ education, IMD hay region.

## 7. Trang 4 — Dự đoán nguy cơ

- Filter: mức nguy cơ dự đoán và nhóm hoàn cảnh kinh tế–xã hội của khu vực.
- KPI: tỷ lệ dự đoán đúng, tỷ lệ phát hiện nhóm nguy cơ, số lượt cần ưu tiên hỗ trợ.
- Caption diễn giải kết quả toàn tập kiểm tra: mô hình đúng khoảng 83/100 lượt và phát hiện khoảng 74/100 lượt thực sự có nguy cơ.
- **Gauge:** nguy cơ không đạt trung bình; thấp `<40%`, trung bình `40–<70%`, cao `≥70%`; vạch `41,5%` là ngưỡng phân lớp.
- **Donut:** dự đoán đúng nhóm nguy cơ, đúng nhóm không nguy cơ, cảnh báo nhầm và bỏ sót.
- **Danh sách hỗ trợ:** chỉ nhóm nguy cơ cao, xếp xác suất giảm dần, tối đa 100 dòng.
- **Story đầu trang:** nói rõ mô hình dự đoán khả năng trượt/bỏ học, không dự đoán điểm; chuyển kết quả thành bước ưu tiên hỗ trợ.

Danh sách chỉ ưu tiên hỗ trợ; không tự động quyết định kết quả hoặc xử phạt người học.

## 8. Inventory biểu đồ

Có 11 visual và đủ ít nhất **8 loại biểu đồ không phải map**: 100% stacked bar, multi-line, bar, scatter, treemap, heatmap, box plot, gauge và donut. Geographic Map là cổng bắt buộc độc lập.

## 9. Tương tác và cổng chất lượng

- Map render 13/13 vùng, click tạo cross-filter và có reset.
- Outcome bar drill học phần → đợt mở; breadcrumb và nút quay lại hoạt động.
- Filter học phần → đợt mở là cascade và dùng chung cho Trang 1–3.
- Risk Level/IMD cập nhật KPI, gauge, donut và Action List.
- AppTest: Trang 1 = 2 chart/4 metric; Trang 2 = 4 chart; Trang 3 = 3 chart; Trang 4 = 2 chart/3 metric/1 table; tất cả 0 exception.
- Model verification, 17 unit test, `git diff --check` phải PASS.
- Browser QA và ảnh mới phải được tạo lại sau thay đổi bố cục bốn trang.
- Không sửa `02-rubric-traceability.md` và `source/TTDLTQ_script.docx`.
- Không commit/push trước khi leader duyệt.
