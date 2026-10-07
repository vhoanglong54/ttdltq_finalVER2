# 06 — Thứ tự thực hiện và quan hệ phụ thuộc

Toàn bộ project do **một người thực hiện chính**. Tài liệu này chỉ quản lý thứ tự kỹ thuật và cổng kiểm tra, không phân công theo thành viên.

## Trạng thái

- **Đã có hiện vật:** code/data/tài liệu tồn tại và đã qua kiểm tra cơ bản.
- **Đang làm local:** có thay đổi chưa được duyệt để commit.
- **Chờ đầu vào:** không được nghiệm thu trước phần phụ thuộc.
- **Chưa làm:** chưa có hiện vật đủ dùng.

## Lộ trình

| Bước | Nội dung | Đầu ra | Phụ thuộc | Trạng thái |
|---:|---|---|---|---|
| 1 | Nguồn và data contract | Nguồn/checksum, dictionary 7 bảng, khóa và grain | — | Đã có hiện vật |
| 2 | Audit, cleaning, processed | Pipeline, Data Quality Report, `clean_dataset.csv` tái tạo được | Bước 1 | Đã có hiện vật |
| 3 | Câu hỏi và giả thuyết | RQ1–RQ6, H01–H10 phù hợp OULAD | Bước 1 | Đã có hiện vật local |
| 4 | EDA và interaction analysis | Sáu chart tĩnh, kết quả H01–H10 | Bước 2–3 | Đã có hiện vật local |
| 5 | Insight và storytelling | Sáu insight đạt mẫu, mạch chuyện hoàn chỉnh | Bước 4 | Đã có hiện vật local |
| 6 | Logistic Regression | Feature cutoff-safe, metric/CI, prediction CSV, verification | Bước 2 | Đã có hiện vật kỹ thuật |
| 7 | Dashboard Python | App hai trang, 8 loại chart thường, map riêng, interaction và action list | Bước 2, 5, 6 | Đã triển khai local; chờ leader duyệt |
| 8 | Geographic Map | Geometry ONS, mapping 13/13, tooltip/filter/QA | Bước 2, 7 | Đã có hiện vật local và audit tự động |
| 9 | QA tích hợp | KPI baseline, filter/drill/cross-filter, model/version, map coverage | Bước 5–8 | Tự động PASS; chờ ảnh/video interaction |
| 10 | Báo cáo và demo | Báo cáo ≥40 trang, IEEE, slide, video, kịch bản | Bước 9 | Chưa hoàn tất |

## Thứ tự làm tiếp

1. Mở app và QA thủ công drill-down, tooltip, cross-filtering ở từng trang.
2. Lưu ảnh/video và trạng thái trước–sau vào `dashboard/evidence/`.
3. Chốt theme, nhãn tiếng Việt/Anh và kiểm tra layout ở màn hình trình chiếu.
4. Đối chiếu lần cuối KPI, model output và map coverage sau mọi chỉnh sửa UI.
5. Viết báo cáo ≥40 trang, slide, kịch bản demo và video backup.
6. Chỉ commit/push sau khi chủ dự án duyệt danh sách thay đổi local.

## Điểm chặn bắt buộc

- Không khóa insight/story trước EDA.
- Không chọn chart chỉ để đủ số lượng.
- Không nghiệm thu Geographic Map khi chưa có geometry/mapping dẫn nguồn đủ 13 region.
- Không nghiệm thu Prediction nếu verification chưa PASS hoặc dùng sai split/version/threshold.
- Không thay đổi nội dung rubric để khớp hiện vật.
- Không commit/push trước khi chủ dự án duyệt danh sách thay đổi và kết quả kiểm tra.
