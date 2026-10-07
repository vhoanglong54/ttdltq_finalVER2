# Baseline và checklist QA dashboard Python

Các giá trị dưới đây được tính từ `data/processed/clean_dataset.csv` khi **không có filter**. App phải khớp trước khi nghiệm thu visual hoặc story.

## Baseline toàn bộ dữ liệu

| Measure | Expected |
|---|---:|
| Learning Attempts | 32.593 |
| Distinct Learners | 28.785 |
| At-Risk Count | 17.208 |
| At-Risk Rate | 52,7966% |
| Pass Count | 15.385 |
| Pass Rate | 47,2034% |
| Assessment Scored Count | 173.739 |
| Assessment Score Sum | 13.169.342 |
| Average Assessment Score | 75,7996 |
| VLE Total Clicks | 39.605.099 |
| Average VLE Clicks per Attempt | 1.215,1413 |

Input đã ghi nhận: SHA-256 `70db1ff19a1dc8553005b0e3801786d20ab1488cc3420a2fe15c5a2254d80f9a`, 32.593 dòng, 35 cột. Nếu file thay đổi hợp lệ, cập nhật checksum và baseline cùng bằng chứng pipeline; không sửa số để che sai lệch.

## Baseline theo region

| Region | Attempts | At-Risk Count | At-Risk Rate |
|---|---:|---:|---:|
| East Anglian Region | 3.340 | 1.704 | 51,0180% |
| East Midlands Region | 2.365 | 1.284 | 54,2918% |
| Ireland | 1.184 | 534 | 45,1014% |
| London Region | 3.216 | 1.854 | 57,6493% |
| North Region | 1.823 | 902 | 49,4789% |
| North Western Region | 2.906 | 1.738 | 59,8073% |
| Scotland | 3.446 | 1.759 | 51,0447% |
| South East Region | 2.111 | 1.024 | 48,5078% |
| South Region | 3.092 | 1.472 | 47,6067% |
| South West Region | 2.436 | 1.223 | 50,2053% |
| Wales | 2.086 | 1.144 | 54,8418% |
| West Midlands Region | 2.582 | 1.464 | 56,7002% |
| Yorkshire Region | 2.006 | 1.106 | 55,1346% |

## Checklist kỹ thuật

- [x] `streamlit run dashboard/app.py` khởi động headless; health endpoint trả HTTP 200/`ok`.
- [x] Schema guard kiểm tra bảng sạch, snapshot và output model.
- [x] KPI không filter khớp baseline.
- [x] Cascading filter Module → Presentation → Region hoạt động và không làm sai mẫu số.
- [x] Drill-down có state/breadcrumb và số liệu đúng.
- [x] Tooltip có metric, `N` và context.
- [x] Cross-filter selection cập nhật visual liên quan.
- [x] Prediction mặc định test split; version/cutoff/threshold khớp artifact.
- [x] Inventory có đủ 9 loại chart không phải map, mỗi chart gắn RQ/H/insight.
- [x] Geographic Map dùng geometry có nguồn/giấy phép, mapping đủ 13/13 region và được kiểm tra độc lập.
- [x] Sáu insight tạo thành story và có giới hạn.
- [x] Version package, checksum và ảnh kiểm thử lưu trong `evidence/`.

## Bằng chứng QA local ngày 06/10/2026

- `python -m unittest discover -s tests -v`: **15/15 PASS**.
- Streamlit AppTest: Overview 3 Plotly charts, Factor 4, Risk 3, Prediction 4; cả bốn trang không có exception.
- Filter test: `AAA → 2013J` trả `N=383`, đúng bảng sạch; option Presentation được cascade còn `2013J`, `2014J`.
- Baseline tự động: 32.593 attempts, 28.785 learners, 17.208 At-Risk, 52,7966%, average score 75,7996 và 39.605.099 VLE clicks.
- Prediction artifact: test=3.590 rows, model `lr-oulad-c105-s42-v4`, cutoff 105, threshold 0,415; verification PASS.
- GeoJSON: 13 feature hợp lệ, 218 đơn vị ONS được mapping một lần, 13/13 nhãn khớp OULAD; file khoảng 1,4 MB.

## Bằng chứng visual QA ngày 07/10/2026

- Microsoft Edge headless tại viewport `1440 × 1000` render đủ bốn trang; ảnh nằm trong `dashboard/evidence/screenshots/`.
- Tooltip stacked bar xuất hiện đúng một hover label, có module–presentation, tỷ trọng và `N`.
- Click `AAA-2013J` trả caption `N=383 lượt học`; sunburst đích chỉ còn `AAA → 2013J → Result`.
- Click `BBB` trên sunburst drill vào đúng subtree BBB; không còn module ngoài BBB trong state đang xem.
- Map, heatmap và ROC/PR đã được kiểm tra riêng về thang màu, nhãn, kích thước và chú giải.
- Treemap đổi tầng sang `Nhóm IMD` bằng control, vẫn render 3 chart và không phát sinh exception.
- Biên bản và liên kết ảnh: `dashboard/evidence/visual-qa-2026-10-07.md`.
