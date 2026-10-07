# Nghiên cứu và phân tích các yếu tố ảnh hưởng đến kết quả học tập của sinh viên đại học

Đồ án cuối kỳ môn **Tương tác dữ liệu trực quan (IDV)** do một người thực hiện chính. Câu hỏi trung tâm: **yếu tố học tập nào liên quan rõ nhất đến khả năng qua môn, trượt hoặc bỏ học?** Phần dự đoán dùng dữ liệu 105 ngày đầu để nhận diện sớm lượt học có nguy cơ kết thúc bằng **trượt hoặc bỏ học**; mô hình không dự đoán điểm chính xác. Bộ dữ liệu là **Open University Learning Analytics Dataset (OULAD)**; công nghệ đã chốt là **Python + Logistic Regression + Streamlit + Plotly**.

Repo VER2 đã có pipeline dữ liệu/mô hình, phân tích tái tạo được, sáu insight và dashboard Streamlit bốn trang. Các kết luận trọng tâm hiện tại là: **hoàn thành bài đến hạn** liên quan rõ nhất đến kết quả; **mức tham gia học trực tuyến** là yếu tố cảnh báo quan trọng; hai yếu tố bất lợi xuất hiện cùng lúc làm nhóm nguy cơ nổi bật hơn; **lịch sử học lại** là bối cảnh cần chú ý. Học phần, khu vực và hoàn cảnh kinh tế–xã hội chỉ được dùng làm bối cảnh so sánh, không được gọi là nguyên nhân.

## Đọc theo thứ tự

1. [Phạm vi và quyết định đã chốt](docs/01-project-charter.md)
2. [Phương án đã duyệt — nguồn kế hoạch chính](docs/plan_approved.md)
3. [Checklist đối chiếu rubric](docs/02-rubric-traceability.md)
4. [Nguồn, bảng, khóa nối và biến](docs/03-data-plan.md)
5. [Model Logistic Regression](docs/04-model.md)
6. [Câu hỏi nghiên cứu, giả thuyết, insight và dashboard Python](docs/05-dashboard-spec.md)
7. [Thứ tự thực hiện và quan hệ phụ thuộc](docs/06-tasks-and-dependencies.md)
8. [Báo cáo, video và vấn đáp](docs/07-report-and-defense.md)
9. [Quy tắc làm việc](CONTRIBUTING.md)

Nguồn yêu cầu gốc: [TTDLTQ_script.docx](docs/source/TTDLTQ_script.docx). Khi ví dụ trong đề cương không phù hợp với cột thực tế của OULAD, [sổ quyết định](docs/08-decisions-and-open-questions.md) ghi rõ phương án thay thế; không chế dữ liệu.

`docs/02-rubric-traceability.md` giữ nguyên barem, điểm số và tiêu chí chấm. Streamlit + Plotly là một lựa chọn được nêu trực tiếp trong danh sách công cụ hợp lệ của rubric.

## Bố cục

```text
TTDLTQ_FINAL/
├── data/                    # Raw/interim không commit; clean_dataset.csv dùng chung
├── notebooks/               # 01 audit, 02 cleaning, 03 EDA
├── src/                     # Pipeline dữ liệu, kiểm tra và Logistic Regression
├── dashboard/               # Ứng dụng Streamlit, module hỗ trợ, QA và bằng chứng
├── reports/                 # Báo cáo >= 40 trang, slide, kịch bản và video
├── docs/                    # Yêu cầu, thiết kế, dữ liệu, model, quyết định
├── AGENTS.md                # Quy tắc cho trợ lý làm việc trong repo
└── CONTRIBUTING.md          # Quy tắc thực hiện project
```

## Chạy local

```powershell
python -m pip install -r requirements.txt
python src/eda_analysis.py
python src/build_oulad_regions_geojson.py
streamlit run dashboard/app.py
```

Hai script đầu tái tạo bảng/hình EDA và geometry bản đồ đã audit. Ứng dụng phải cảnh báo rõ khi thiếu output model hoặc geometry; không được thay bằng dữ liệu tự tạo.

## Mốc hoàn thành theo đề bài

- Dữ liệu có nguồn và giấy phép rõ, ít nhất **5.000 dòng** và **3 bảng** thực sự liên kết; có data dictionary, audit, cleaning, join và calculated fields.
- EDA Python có ít nhất **3–5 biểu đồ tĩnh**; kiểm tra 8–10 giả thuyết khả thi và chốt **5–7 insight** có bằng chứng.
- Dashboard Python gồm **4 trang**, có ít nhất 8 loại biểu đồ không phải bản đồ và 1 Geographic Map bắt buộc; bản đồ lọc chéo, học phần có drill-down, tooltip và danh sách ưu tiên hỗ trợ.
- Logistic Regression dự đoán một lượt học có kết thúc bằng trượt/bỏ học hay không; Trang 4 trình bày xác suất, dự đoán đúng/sai, số trường hợp bỏ sót và nhóm cần ưu tiên hỗ trợ.
- Báo cáo **tối thiểu 40 trang**, trích dẫn IEEE, demo trực tiếp, video backup; người thực hiện phải giải thích được toàn bộ pipeline.

Nguồn dữ liệu chính: [Open University OULAD](https://research.stem.open.ac.uk/ouanalyse/dataset/); mô tả cấu trúc và phương pháp: [Kuzilek et al., Scientific Data (2017)](https://www.nature.com/articles/sdata2017171); bản phát hành và giấy phép: [UCI OULAD](https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset).
