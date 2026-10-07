# 01 — Phạm vi đồ án

## Bài toán và kết quả mong muốn

Đề tài theo `TTDLTQ_script.docx`: **Nghiên cứu và phân tích các yếu tố ảnh hưởng đến kết quả học tập của sinh viên đại học**. Luồng nghiên cứu: mô tả kết quả → tìm yếu tố liên quan → xem tương tác đa biến → nhận diện nhóm rủi ro → dự báo `At_Risk` → kể chuyện bằng dashboard Python. Vì OULAD là dữ liệu quan sát, phần phân tích dùng từ **liên hệ/khác biệt**, không khẳng định tác động nhân quả.

Đơn vị phân tích là một **lượt học module-presentation của một sinh viên**. Kết quả gốc `final_result` gồm `Pass`, `Distinction`, `Fail`, `Withdrawn`; nhãn model là `At_Risk = 1` cho `Fail/Withdrawn`, `0` cho `Pass/Distinction`. Dự báo sớm chỉ dùng thông tin xuất hiện trước hoặc tại cutoff đã công bố.

## Quyết định công nghệ

| Thành phần | Quyết định |
|---|---|
| Dữ liệu | OULAD, 7 bảng CSV liên kết, hơn 5.000 dòng, có `region`, nguồn học thuật rõ |
| Xử lý/EDA | Python, Pandas/NumPy, Matplotlib/Seaborn |
| Dự báo | scikit-learn Logistic Regression, xác suất rủi ro và phân lớp |
| Trực quan tương tác | Python với Streamlit + Plotly; bốn trang Bức tranh kết quả, Các yếu tố học tập, Kết hợp nhiều yếu tố, Dự đoán nguy cơ |
| Trọng tâm | Tương tác các yếu tố, risk profile, hành vi VLE theo thời gian, độ tin cậy và sai số model |
| Thực hiện | Một người chịu trách nhiệm toàn bộ data, EDA, insight, model, dashboard, báo cáo và demo |
| Điều phối | Theo thứ tự kỹ thuật và cổng kiểm tra; không phân công theo thành viên; commit cần chủ dự án duyệt |

Streamlit + Plotly nằm trong danh sách công cụ hợp lệ của rubric. Việc đổi công nghệ triển khai không thay đổi bất kỳ điểm số hay tiêu chí chấm nào.

## Phạm vi nghiên cứu thực tế với OULAD

OULAD có thông tin nhân khẩu học, vùng, `imd_band` (mức thiếu thốn của khu vực), lượt học, bài đánh giá, đăng ký và VLE clicks. `region` chỉ dùng cho map sau khi có geometry/mapping được dẫn nguồn và kiểm tra đủ 13 nhãn. Dữ liệu **không ghi trực tiếp** sleep, stress, motivation, physical activity, attendance trên lớp, study hours hay điểm học phần trước; không tạo các cột này. Xem biến thay thế tại [kế hoạch dữ liệu](03-data-plan.md) và [đặc tả nghiên cứu/dashboard](05-dashboard-spec.md).

Không gọi VLE clicks là attendance hoặc study hours. Không tự tạo `Average Score` hay `Grade_Change` với ý nghĩa điểm cuối khóa; mọi calculated field phải có tên, tử số, mẫu số và cửa sổ thời gian tường minh.

## Tiêu chí hoàn tất

Đối chiếu từng hạng mục với [rubric](02-rubric-traceability.md). Mỗi mục phải có hiện vật, kiểm tra và xác nhận. Báo cáo tối thiểu 40 trang, demo trực tiếp, video backup và khả năng giải thích toàn bộ pipeline là đầu ra bắt buộc.

## Nguồn

- Đề bài, barem và phương án dự án: [TTDLTQ_script.docx](source/TTDLTQ_script.docx).
- [Trang OULAD của Open University](https://research.stem.open.ac.uk/ouanalyse/dataset/).
- [Bài công bố OULAD](https://www.nature.com/articles/sdata2017171), DOI: `10.1038/sdata.2017.171`.
- [OULAD tại UCI](https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset), DOI: `10.24432/C5KK69`, CC BY 4.0.
