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
- [x] Trang 1 AppTest: 2 charts, 4 metrics, 0 exception.
- [x] Trang 2 AppTest: 4 charts, 0 exception.
- [x] Trang 3 AppTest: 3 charts, 0 exception.
- [x] Trang 4 AppTest: 2 charts, 3 metrics, 1 table, 0 exception.
- [x] Model verification: 9/9 quality gates PASS.
- [x] GeoJSON: 13/13 region, geometry valid.
- [x] Markdown links: 0 link tương đối thiếu.
- [x] `git diff --check`: 0 whitespace error.

## Browser QA

- [x] Chụp lại bốn trang ở viewport 1440×1000.
- [x] Filled Map render đủ 13 polygon và cross-filter hoạt động.
- [x] Stacked bar hiển thị đủ 0–100%, giải thích AAA–GGG/B/J và drill hoạt động.
- [x] VLE/assessment/interaction visual không bị tràn ngang hoặc chồng nhãn nghiêm trọng.
- [x] Gauge, donut và Action List hiển thị đúng trên Trang 4.

Chi tiết: [Visual QA bốn trang](evidence/visual-qa-4page-2026-10-07.md). Bản [Visual QA cũ](evidence/visual-qa-2026-10-07.md) chỉ dùng lưu trữ mốc `1499c40`.

## Điều kiện chưa tự động hoàn thành

- Leader vẫn cần chạy lại trên máy demo và duyệt bằng mắt.
- Báo cáo, slide, video và link demo là hiện vật riêng.
- Bản hai trang đã push tại `1499c40`. Bản bốn trang đang local, chưa commit/push và phải được leader duyệt sau browser QA.
