# 08 — Quyết định và điểm cần xác nhận

Tài liệu này tách quyết định đã chốt khỏi giả định phải kiểm chứng trên OULAD. Không sửa rubric để khớp hiện vật; khi đổi cách triển khai phải giữ nguyên tiêu chí và cập nhật bằng chứng.

| ID | Trạng thái | Nội dung và lý do | Phần liên quan |
|---|---|---|---|
| D01 | Chốt | OULAD; Python; Logistic Regression; `At_Risk = 1` cho Fail/Withdrawn. | Data, model |
| D02 | Chốt | Hạt phân tích là `(code_module, code_presentation, id_student)` để tránh đếm/merge sai. | Data, dashboard |
| D03 | Chốt | OULAD không có trực tiếp sleep, stress, motivation, physical activity, attendance, study hours hoặc previous grade; dùng biến thật có tên đúng hoặc bỏ, không chế dữ liệu. | RQ, EDA |
| D04 | Đã triển khai, cần giữ đồng bộ | Cutoff ngày 105, tính event tại biên (`date <= 105`). Mọi dashboard/report phải dùng đúng cutoff ghi trong output model. | Model, Prediction |
| D05 | Đã triển khai, cần nghiệm thu cuối | Threshold và risk band lấy từ artifact model, không hard-code một bản khác trong dashboard. Metric chính gồm Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, Brier và CI. | Model, QA |
| D06 | Đã triển khai local | Geographic Map dùng ONS CUA theo OGL v3.0, union theo vùng OU lịch sử, mapping đủ 13/13. `Ireland` dùng Northern Ireland; mọi xấp xỉ được công bố trong `dashboard/assets/README.md`. | Dashboard |
| D07 | Chốt | **Average Assessment Score** = tổng score / số assessment được chấm trong filter context; không average các mean attempt. | KPI |
| D08 | Đã chốt inventory | EDA đã hoàn tất; inventory gồm 9 loại chart không-map và 1 Geographic Map. Theme/layout vẫn cần QA trình chiếu. | EDA, dashboard |
| D09 | Đã triển khai, cần công bố giới hạn | Split theo `id_student` để một sinh viên không xuất hiện ở nhiều tập; tune/CV train, threshold validation, đánh giá test. Lịch sử đã xem test nên báo cáo cần nêu giới hạn hoặc dùng holdout độc lập nếu có. | Model |
| D10 | Chốt | Người thực hiện tự quản lý lịch/deadline; repo quản lý theo thứ tự kỹ thuật và phụ thuộc. | Điều phối |
| D11 | Cần xác nhận nguồn | Số dòng dùng theo file thực; chênh lệch giữa metadata công bố và file local phải nêu trong Data Quality Report. | Data |
| D12 | Chốt | `?` là missing ở interim; không impute tùy tiện; raw giữ nguyên. | Cleaning |
| D13 | Chốt | `date_unregistration` không hoàn toàn đồng nghĩa Withdrawn và bị cấm khỏi feature dự báo sớm. | Cleaning, model |
| D14 | Chốt | Chỉ theo dõi `data/processed/clean_dataset.csv`; raw/interim/output tự sinh khác không commit nếu chưa có quyết định mới. | Git, data |
| D15 | Chốt | `studentVle` được gom theo khóa logic và cộng `sum_click`; không xóa exact duplicate riêng lẻ làm mất click. | Cleaning, model |
| D16 | Chốt ngày 06/10/2026 | Dashboard dùng **Python với Streamlit + Plotly**, một lựa chọn có trong rubric. Pandas/NumPy xử lý, Matplotlib/Seaborn EDA, scikit-learn model. Giữ nguyên toàn bộ điểm và tiêu chí rubric. | Toàn dự án |
| D17 | Chốt theo yêu cầu chủ dự án | Mọi thay đổi phải báo cáo để duyệt trước khi commit/push. | Git, điều phối |
| D18 | Chốt | Một người thực hiện chính toàn bộ project; tài liệu triển khai không chia vai trò theo thành viên. Rubric gốc không thay đổi. | Toàn dự án |
| D19 | Chốt | Phương án visual an toàn gồm 9 loại chart không phải map và 1 Geographic Map bắt buộc riêng; map có cổng nghiệm thu độc lập. | Dashboard, QA |

## Điểm còn mở

1. Cần lưu ảnh/video QA thật cho drill-down, tooltip và cross-filtering.
2. Cần chốt theme/layout sau khi xem trên màn hình dùng để demo.
3. Cần chủ dự án duyệt model version `lr-oulad-c105-s42-v4` là bản cuối cho báo cáo/demo.
4. Cần hoàn thiện báo cáo, slide, video và kịch bản vấn đáp.

## Mẫu quyết định mới

`Ngày — ID — Bối cảnh — Phương án chọn — Bằng chứng — Phần bị ảnh hưởng — Trạng thái duyệt`.
