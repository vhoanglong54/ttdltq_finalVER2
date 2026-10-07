# Hướng dẫn phát triển dashboard Python

## 1. Tạo dữ liệu

```powershell
python src/dashboard_features.py
```

Script tạo:

- `assessment_deadlines.csv`
- `assessment_submissions.csv.gz`
- `vle_daily_profile.csv.gz`
- `vle_activity_summary.csv.gz`

Không sửa các file này bằng spreadsheet. Muốn thay logic phải sửa script và chạy lại.

## 2. Chạy ứng dụng

```powershell
streamlit run dashboard/app.py
```

## 3. Chạy kiểm thử

```powershell
python -m py_compile dashboard/app.py dashboard/dashboard_data.py src/dashboard_features.py
python -m unittest discover -s tests -v
```

Expected AppTest:

- Trang 1: 2 Plotly charts, 4 metrics, 0 exception.
- Trang 2: 4 Plotly charts, 0 exception.
- Trang 3: 3 Plotly charts, 0 exception.
- Trang 4: 2 Plotly charts, 3 metrics, 1 dataframe, 0 exception.

## 4. Quy tắc tính

- Không cộng trùng người học và lượt học; mọi join model dùng đủ ba khóa attempt.
- Avg Score = tổng score / số score hợp lệ.
- VLE daily average chia cho toàn bộ attempts của nhóm, kể cả ngày không click.
- Scatter chỉ sample để render; correlation/trendline phải dùng toàn subset.
- Chỉ Trang 4 dùng test split. Published metrics toàn test không bị thay bằng subgroup metric.
- Risk band can thiệp 40%/70% khác với classification threshold 41,5%.
- App không load joblib và không train model.

## 5. Cổng map

- 13/13 region khớp `properties.region`.
- Nguồn ONS và OGL v3.0 được giữ trong `assets/README.md`.
- Click region phải tạo active filter; nút reset phải xóa cả state và Plotly selection.

## 6. Trước khi bàn giao

- Kiểm tra title, axis, unit, tooltip, caption và `N`.
- Chụp ảnh 1440×1000 cho cả bốn trang và các tương tác map/drill.
- Chạy link check, `git diff --check` và kiểm tra hai file rubric không đổi.
- Không commit/push khi chưa có duyệt của leader.
