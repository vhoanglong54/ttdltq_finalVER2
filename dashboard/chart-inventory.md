# Inventory trực quan cuối

Phương án có **8 loại biểu đồ không phải map** và **1 Geographic Map bắt buộc riêng**.

| # | Loại | Trang | Dữ liệu/grain | Câu hỏi trả lời | Tương tác |
|---:|---|---|---|---|---|
| 1 | Filled Geographic Map | Academic | attempt → region | Vùng nào có At-Risk rate cao? | Click region cross-filter cả trang |
| 2 | 100% Stacked Bar | Academic | module/presentation × result | Cơ cấu kết quả khác nhau ra sao? | Click module drill xuống presentation |
| 3 | Multi-Line | Academic | day × At-Risk label | Nhịp VLE của hai nhóm khác nhau thế nào? | Hover unified, deadline markers |
| 4 | Scatter + Trendline | Academic | assessment submission | Nộp trễ liên hệ với điểm ra sao? | Hover student/context; bubble size=previous attempts |
| 5 | Treemap | Academic | activity type | Tài nguyên nào chiếm nhiều VLE clicks? | Hover clicks/share |
| 6 | Heatmap Matrix | Risk | education × IMD | Tổ hợp hai yếu tố nào có rate cao? | Tooltip rate/N, filter Risk/IMD |
| 7 | Box Plot | Risk | attempt | Điểm phân tán theo lịch sử học lại thế nào? | Hover outlier/distribution |
| 8 | Gauge | Risk | prediction subset | Xác suất At-Risk trung bình nằm ở dải nào? | Risk/IMD filter |
| 9 | Donut | Risk | error type | TP/TN/FP/FN chiếm tỷ lệ bao nhiêu? | Hover count/share |

Student Action List là bảng hỗ trợ hành động, không được tính như một loại biểu đồ.

## Quy tắc trình bày

- Mọi rate/percentage đều có mẫu số hoặc `N` trong chart/caption/tooltip.
- Bản đồ và heatmap dùng miền màu 0–100% để không phóng đại khác biệt.
- Xanh = an toàn/Not-At-Risk; cam = cảnh báo; đỏ = At-Risk/High Risk.
- Scatter render tối đa 4.500 điểm để dễ đọc nhưng trendline/correlation dùng toàn bộ subset.
- Risk Level (`40%/70%`) phục vụ ưu tiên; threshold model (`41,5%`) được hiển thị riêng.
- Không dùng biểu đồ chỉ để đủ số lượng: mỗi visual trả lời một câu hỏi khác nhau.
