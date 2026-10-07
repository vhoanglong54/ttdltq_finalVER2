# Hướng dẫn phát triển dashboard Python

## 1. Môi trường

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run dashboard/app.py
```

Không đưa secrets vào code. Nếu sau này cần secrets, đặt ở `.streamlit/secrets.toml`; file này bị Git ignore.

## 2. Đầu vào

### Nội dung mô tả

- `data/processed/clean_dataset.csv`
- Hạt: một lượt học theo `(code_module, code_presentation, id_student)`
- Schema/công thức: `data/processed/README.md` và `docs/09-data-dictionary.md`

### Nội dung dự báo

- `data/processed/model/feature_snapshot.csv` cho Factor/Risk tại cutoff ngày 105
- `data/processed/model/model_predictions.csv`
- `model_metrics.csv`, `model_confusion_matrix.csv`, `model_calibration.csv`
- `model_confidence_intervals.csv`, `model_curve_points.csv`, `model_subgroup_metrics.csv`
- `model_verification.csv`

App không đọc `.joblib` và không train lại theo filter. Nếu output model thiếu hoặc verification không PASS, phần Prediction phải báo lỗi rõ thay vì tạo số thay thế.

## 3. Luồng phát triển

1. Chạy pipeline/model để tạo đúng input.
2. Kiểm tra baseline không filter trong `qa-t09.md`.
3. Chạy `python src/eda_analysis.py` để tái tạo sáu hình và sáu insight.
4. Kiểm tra inventory 9 loại chart không phải map trong `chart-inventory.md`.
5. Chạy `python src/build_oulad_regions_geojson.py` để tái tạo GeoJSON và mapping audit.
6. Kiểm thử filter nhiều cấp, drill-down, tooltip và cross-filtering.
7. Chụp evidence, ghi version package/checksum và chạy từ môi trường sạch.

## 4. Map contract

Asset: `dashboard/assets/oulad_regions.geojson`; audit: `oulad_regions_mapping.csv`; nguồn/giấy phép/giới hạn: `assets/README.md`. Mỗi feature có `properties.region` khớp 13 giá trị OULAD. Geometry được union từ ONS CUA, không vẽ tay polygon/centroid.

## 5. Model contract

Trang Prediction mặc định dùng test split và model Logistic Regression. Luôn hiển thị `model_version`, `cutoff_day`, `prediction_threshold` và số dòng. Metric toàn test lấy từ artifact; khi filter theo subgroup phải gọi đó là số liệu subgroup, không giả làm metric toàn test.

## 6. Điều kiện hoàn tất

- Lệnh chạy từ repo root thành công.
- KPI khớp baseline; schema guard báo lỗi hữu ích.
- Đủ 9 loại chart không phải map, có lý do chọn và không đếm trùng biến thể hình thức.
- Geographic Map đạt cổng riêng: geometry thật có nguồn/giấy phép, mapping đủ 13/13 region, tooltip và filter hoạt động.
- Có evidence trước/sau cho filter, drill-down và cross-filter; ảnh hover cho tooltip.
- Story nối 5–7 insight, có số liệu/`N`/giới hạn.
- Không đánh dấu đạt trước khi có bằng chứng và chủ dự án xác nhận.
