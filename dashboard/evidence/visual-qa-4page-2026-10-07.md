# Visual QA dashboard bốn trang — 07/10/2026

Kiểm tra trên Streamlit thật bằng Microsoft Edge headless, viewport 1440×1000. Bốn trang đều có `scrollWidth = clientWidth = 1440`, không có tràn ngang và không có lỗi runtime.

## Kết quả theo trang

| Trang | Chart | Story | Lỗi runtime | Bằng chứng |
|---|---:|---:|---:|---|
| 1 · Bức tranh kết quả học tập | 2 | 1 | 0 | [Page](screenshots/overview-page-v4.png), [Map](screenshots/overview-map-v4.png), [Outcome](screenshots/overview-outcome-v4.png), [Story](screenshots/overview-story-v4.png) |
| 2 · Các yếu tố học tập | 4 | 1 | 0 | [Page](screenshots/behavior-page-v4.png), [Mức tham gia](screenshots/behavior-vle-v4.png), [Hoàn thành bài](screenshots/behavior-completion-v4.png), [Nộp bài–điểm](screenshots/behavior-scatter-v4.png), [Tài nguyên](screenshots/behavior-treemap-v4.png), [Story](screenshots/behavior-story-v4.png) |
| 3 · Kết hợp nhiều yếu tố | 3 | 1 | 0 | [Page](screenshots/interaction-page-v4.png), [Mức tham gia × điểm](screenshots/interaction-engagement-assessment-v4.png), [Học vấn × khu vực](screenshots/interaction-education-imd-v4.png), [Lịch sử học lại](screenshots/interaction-attempt-box-v4.png), [Story](screenshots/interaction-story-v4.png) |
| 4 · Dự đoán nguy cơ | 2 | 1 | 0 | [Page](screenshots/prediction-page-v4.png), [Mức nguy cơ](screenshots/prediction-gauge-v4.png), [Đúng/sai/bỏ sót](screenshots/prediction-errors-v4.png), [Danh sách hỗ trợ](screenshots/prediction-action-list-v4.png), [Story](screenshots/prediction-story-v4.png) |

## Tương tác xác nhận

- Geographic Map render đủ 13 vùng; click tạo `Cross-filter từ bản đồ` và nút reset hoạt động.
- Outcome bar có 28 segment ở cấp học phần, trục đủ 0–100%, nhãn nguy cơ không đạt cuối thanh; click tạo drill breadcrumb.
- Nút `Chỉ xem mức nguy cơ cao` lọc danh sách về nhóm xác suất từ 70% và không có exception.
- VLE, IMD, mã AAA–GGG/B/J và các chỉ số mô hình đều được giải thích bằng tiếng Việt trong sidebar hoặc đầu trang.
- Story Trang 2–4 được đặt trước biểu đồ để người xem đọc kết luận trước khi xem chi tiết.

## Kết luận

Bố cục bốn trang đạt kiểm tra browser kỹ thuật. Leader vẫn cần xem thẩm mỹ trên máy/độ phân giải dùng để trình chiếu trước khi cho phép commit.
