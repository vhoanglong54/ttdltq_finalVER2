# 07 — Báo cáo, demo và vấn đáp

Một người thực hiện chính chịu trách nhiệm hiểu và trình bày toàn bộ pipeline.

## Cấu trúc báo cáo

| Phần | Nội dung cần chứng minh |
|---|---|
| Introduction & Related Work | Bối cảnh, mục tiêu, RQ, phạm vi và tài liệu tham khảo IEEE |
| Data & Method | 7 bảng OULAD, nguồn, khóa/hạt, audit, cleaning, calculated fields và giới hạn |
| EDA & Insights | Sáu chart tĩnh, H01–H10, tương tác đa biến, sáu insight và story |
| Prediction | Target/cutoff, leakage guard, split, Logistic Regression, metric/CI, lỗi và giới hạn |
| Interactive Dashboard | Streamlit + Plotly, 8 loại chart thường, Geographic Map riêng, tương tác và QA |
| Conclusion | Trả lời RQ, khuyến nghị thận trọng, hạn chế và hướng tiếp theo |
| Installation & Demo | Cách tái tạo data/model, chạy app, kịch bản demo và video backup |

Báo cáo phải đạt **ít nhất 40 trang** và dùng trích dẫn IEEE. Sơ đồ pipeline: **bài toán → OULAD → audit/cleaning → join/feature → EDA/hypothesis → insight/risk profile → Logistic Regression → dashboard Python → báo cáo/demo**.

## Kịch bản storytelling khi demo

1. Nêu câu hỏi trung tâm, hạt lượt học và giới hạn dữ liệu quan sát.
2. Trang Academic Insight & Behavior trả lời kết quả, không gian, VLE, độ trễ nộp bài và loại tài nguyên.
3. Demo map cross-filter và drill từ module xuống presentation.
4. Trang Risk Matrix & Early Warning trình bày interaction education × IMD, lịch sử học lại, xác suất và sai số.
5. Student Action List chuyển output model thành danh sách High Risk để ưu tiên hỗ trợ.
6. Phân biệt threshold model 41,5% với dải can thiệp Low/Medium/High 40%/70%.
7. Kết luận sáu insight động, hành động thận trọng và giới hạn.

## Nội dung phải tự giải thích được

- Nguồn, giấy phép, 7 bảng, khóa và grain.
- Quy tắc cleaning, missing, outlier và aggregation.
- RQ/H, cách tính KPI, lý do chọn từng loại chart.
- Geometry/mapping của Geographic Map.
- Filter, drill-down, tooltip và cross-filtering.
- Target, cutoff, feature, split, threshold và các metric model.
- Vì sao insight chỉ là mối liên hệ, không phải kết luận nhân quả.

## Bằng chứng nộp

- PDF báo cáo, slide, link/code demo và video backup.
- Inventory 8 chart thường và Geographic Map được kiểm tra riêng.
- Insight Log 5–7 mục.
- Model verification và dashboard QA.
- Lệnh tái tạo, requirements, checksum input và ảnh/video interaction.
