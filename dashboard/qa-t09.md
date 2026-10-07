# Baseline và checklist QA dashboard

## Baseline dữ liệu

| Chỉ số | Giá trị |
|---|---:|
| Learning attempts | 32.593 |
| Unique students | 28.785 |
| At-Risk attempts | 17.208 |
| At-Risk rate | 52,7966% |
| Assessment average | 75,8 |
| VLE clicks | 39.605.099 |
| Model test rows | 3.590 |
| Model Accuracy | 82,70% |
| Recall At-Risk | 73,49% |
| High Risk theo dải ≥70% | 810 |

## Automated QA

- [x] Compile app, data layer và mart builder.
- [x] Unit tests: 17/17 PASS.
- [x] Hai VLE marts đều bảo toàn 39.605.099 clicks.
- [x] Submission delay bằng `date_submitted - due_date`.
- [x] Page 1 AppTest: 5 charts, 4 metrics, 0 exception.
- [x] Page 2 AppTest: 4 charts, 3 metrics, 1 table, 0 exception.
- [x] Page 2 với `Risk Level=High`: 4 charts, 0 exception, N=810.
- [x] Model verification: 9/9 quality gates PASS.
- [x] GeoJSON: 13/13 region, geometry valid.
- [x] Markdown links: 0 link tương đối thiếu.
- [x] `git diff --check`: 0 whitespace error.

## Browser QA

- [x] Microsoft Edge, viewport 1440×1000.
- [x] Filled Map render đủ 13 polygon.
- [x] Click map tạo dòng `Cross-filter từ bản đồ` và cập nhật context.
- [x] Click stacked bar tạo breadcrumb Module → Presentation.
- [x] VLE line không chồng annotation deadline.
- [x] Scatter có trendline, mốc đúng hạn và tooltip.
- [x] Gauge hiện đủ 0–100% và ba dải màu.
- [x] Action List có probability và data bar đỏ.

Chi tiết ảnh: [Visual QA](evidence/visual-qa-2026-10-07.md). Kết quả lệnh: [Automated QA](evidence/automated-qa-2026-10-06.md).

## Điều kiện chưa tự động hoàn thành

- Leader vẫn cần chạy lại trên máy demo và duyệt bằng mắt.
- Báo cáo, slide, video và link demo là hiện vật riêng.
- Chưa commit/push cho đến khi leader xác nhận.
