# Inventory biểu đồ và bằng chứng

Inventory này khóa đúng phương án trong `docs/plan_approved.md`: **9 loại biểu đồ không phải map** và **1 Geographic Map độc lập**. Confusion matrix, ROC/PR và calibration là bằng chứng model, không dùng để cộng thêm số loại.

| STT | Loại | Trang / dữ liệu | RQ / insight | Interaction và tooltip | Trạng thái local |
|---:|---|---|---|---|:---:|
| 1 | Donut | Overview / toàn khóa | RQ1 / INS-01 | Hover kết quả, N, share | Có |
| 2 | Stacked bar | Overview / toàn khóa | RQ1 / INS-01 | Chọn module-presentation để cross-filter sunburst; hover share và N | Có |
| 3 | Sunburst | Overview / toàn khóa | RQ1 / INS-01 | Drill Module → Presentation → Result; N và % parent | Có |
| 4 | Line | Factor / snapshot ngày 105 | RQ2 / INS-02 | Bốn cửa sổ không chồng lấp, actual status, mean clicks/ngày và N | Có |
| 5 | Box plot | Factor / snapshot ngày 105 | RQ3 / INS-03 | Phân bố weighted assessment score theo actual status | Có |
| 6 | Scatter/Bubble | Factor / snapshot ngày 105 | RQ5 / INS-04 | Assessment × VLE; size=N, color=At-Risk rate theo module-presentation | Có |
| 7 | Heatmap | Factor / snapshot ngày 105 | RQ5 / INS-04 | VLE quartile × assessment quartile; rate và N | Có |
| 8 | Treemap | Risk / snapshot ngày 105 | RQ4 / INS-05 | Previous attempts → education/IMD/credits/age/disability; size=N, color=rate | Có |
| 9 | Histogram | Prediction / model predictions | RQ6 | Xác suất theo actual status và threshold | Có |
| Map | Choropleth Geographic Map | Risk / toàn khóa + ONS geometry | RQ4 / INS-06 | Module/Presentation/Region filter; tooltip rate, count, N | Có, xấp xỉ được công bố |

## Bằng chứng model bổ sung

- Confusion matrix: Actual × Predicted trong prediction slice.
- ROC và Precision–Recall: ranking quality theo split.
- Calibration plot: mean predicted probability so với observed At-Risk rate, bubble size=N.
- Confidence-interval table: bootstrap 95% từ artifact.

## Phạm vi và chống diễn giải sai

- Overview và region dùng bảng toàn khóa N=32.593.
- Factor dùng 25.132 eligible attempts tại ngày 105; không dùng aggregate toàn khóa để kể câu chuyện cảnh báo sớm.
- Prediction mặc định test split. Sidebar filter chỉ đổi prediction slice, không đổi nhãn của published test metrics.
- Map dùng geometry ONS được union theo mô tả vùng OU lịch sử. Giới hạn, quy ước `Ireland` và bảng audit nằm trong `dashboard/assets/README.md`.
- Sáu insight và tử số/mẫu số chuẩn nằm trong `docs/insight-log.md`.

## Quy chuẩn trình bày trực quan

- Màu mang ý nghĩa nhất quán: đỏ = At-Risk/Fail/Withdrawn; xanh = Not-At-Risk/Pass; xanh ngọc = Distinction.
- Mọi biểu đồ có tiêu đề mô tả đúng metric, tên trục, đơn vị, tooltip và cỡ mẫu `N` khi so sánh tỷ lệ.
- Tỷ lệ At-Risk trên map, heatmap, bubble, treemap và bar dùng cùng miền màu 0–100%; không co thang màu để làm chênh lệch trông lớn hơn thực tế.
- Biểu đồ có chiều cao cố định theo mật độ nội dung; nhãn dài dùng auto-margin, bar theo vùng để ngang và không cắt tên.
- Không dùng 3D, dual-axis hoặc màu trang trí không mang ý nghĩa dữ liệu.
- Caption nêu rõ grain, cutoff, mẫu số hoặc giới hạn cần thiết; insight quan sát không được diễn giải thành quan hệ nhân quả.
- Dashboard dùng nền sáng, card trắng, chữ đậm tương phản cao và palette thân thiện với trình chiếu; hover không phải cách duy nhất để biết metric chính.
