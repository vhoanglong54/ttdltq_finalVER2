# Inventory trực quan cuối

Dashboard có **11 visual**, bao phủ ít nhất 8 loại biểu đồ không phải map và một Geographic Map bắt buộc.

| # | Loại | Trang | Câu hỏi trả lời | Tương tác/phạm vi |
|---:|---|---|---|---|
| 1 | Filled Geographic Map | Kết quả | Vùng nào có tỷ lệ nguy cơ không đạt cao? | Click vùng lọc KPI và kết quả |
| 2 | 100% Stacked Bar | Kết quả | Cơ cấu Distinction/Pass/Fail/Withdrawn khác nhau ra sao? | Drill học phần ẩn danh → đợt mở |
| 3 | Multi-Line | Yếu tố học tập | Mức tham gia trực tuyến của hai nhóm khác nhau thế nào? | Hover thống nhất, hạn nộp |
| 4 | Bar | Yếu tố học tập | Hoàn thành bài đến hạn liên quan thế nào đến nguy cơ không đạt? | Tooltip tỷ lệ/N |
| 5 | Scatter + Trendline | Hành vi | Nộp trễ liên hệ với điểm thế nào? | Hover context; size=previous attempts |
| 6 | Treemap | Hành vi | Loại tài nguyên nào chiếm nhiều click VLE? | Hover click/share |
| 7 | Heatmap | Kết hợp yếu tố | Mức tham gia × điểm tạo nhóm nguy cơ nào? | Tỷ lệ và N từng ô |
| 8 | Heatmap | Tương tác | Education × IMD có tổ hợp nào đáng chú ý? | Rate và N từng ô |
| 9 | Box Plot | Tương tác | Điểm phân tán theo lịch sử học lại thế nào? | Outlier/distribution |
| 10 | Gauge | Dự báo | Nguy cơ không đạt trung bình nằm ở mức nào? | Bộ lọc mức nguy cơ/khu vực |
| 11 | Donut | Dự báo | Dự đoán đúng, cảnh báo nhầm và bỏ sót chiếm bao nhiêu? | Hover số lượng/tỷ trọng |

Student Action List là bảng hỗ trợ hành động, không tính như một loại biểu đồ.

## Quy tắc trình bày

- Mỗi trang có một khối **Story** với 2–3 kết luận định lượng.
- Mọi viết tắt và mã ẩn danh được giải thích trong luồng đọc.
- Rate/percentage có `N` trong chart, caption hoặc tooltip.
- 100% stacked bar luôn dùng miền 0–100%, sắp theo nguy cơ không đạt và có nhãn trượt + bỏ học.
- Xanh = không thuộc nhóm nguy cơ; cam = cảnh báo; đỏ = có nguy cơ cao.
- VLE chỉ là tương tác nền tảng; mọi insight là liên hệ, không khẳng định nhân quả.
- Risk Level (`40%/70%`) phục vụ ưu tiên; threshold model (`41,5%`) được hiển thị riêng.
