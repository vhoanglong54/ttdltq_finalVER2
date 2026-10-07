# Automated QA — 06/10/2026

Đây là bằng chứng tự động cho bản local chưa commit. Ảnh/video interaction thủ công vẫn phải bổ sung riêng.

## Môi trường

| Thành phần | Phiên bản |
|---|---:|
| Python | 3.12.10 |
| pandas | 2.3.3 |
| NumPy | 2.3.5 |
| scikit-learn | 1.8.0 |
| Streamlit | 1.65.0 |
| Plotly | 7.1.0 |
| Matplotlib | 3.10.8 |
| Seaborn | 0.13.2 |
| Shapely | 2.1.2 |

Input `clean_dataset.csv` SHA-256: `70db1ff19a1dc8553005b0e3801786d20ab1488cc3420a2fe15c5a2254d80f9a`.

## Kết quả

```text
python -m unittest discover -s tests -v
Ran 15 tests
OK
```

- `python -m py_compile` PASS cho app, data layer, EDA và map builder.
- `streamlit run dashboard/app.py --server.headless true` khởi động; `/_stcore/health` trả HTTP 200 và `ok`.
- AppTest không exception: Overview 3 chart, Factor 4, Risk 3, Prediction 4.
- Filter `AAA → 2013J` trả N=383; Presentation options sau chọn AAA chỉ còn `2013J`, `2014J`.
- KPI không filter khớp baseline: 32.593 attempts, 28.785 learners, 17.208 At-Risk, 52,7966%, score 75,7996, 39.605.099 clicks.
- Model artifact: `lr-oulad-c105-s42-v4`, cutoff 105, threshold 0,415; train 17.952, validation 3.590, test 3.590; verification PASS.
- Map build PASS: 13/13 region, 218 ONS areas, geometry hợp lệ; mapping code không trùng.
- Markdown link check: 0 relative link bị thiếu.
- Rubric Markdown và DOCX nguồn không có thay đổi local.

## Còn cần kiểm tra thủ công

1. Ảnh trước/sau của cascading filter.
2. Ảnh drill sunburst Module → Presentation → Result.
3. Ảnh tooltip có metric và N.
4. Video selection trên stacked bar cập nhật sunburst.
5. Kiểm tra layout ở độ phân giải dùng khi demo.
