# Dashboard Python — Streamlit + Plotly

Thư mục này chứa ứng dụng tương tác của đồ án. Streamlit quản lý giao diện/state/filter; Plotly vẽ biểu đồ và nhận selection event; Pandas chỉ đọc các bảng đã được pipeline/model kiểm tra.

## Chạy ứng dụng

Từ thư mục gốc repo:

```powershell
python -m pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Trạng thái

- `app.py` đã triển khai bốn phần Overview, Factor Analysis, Risk Analysis và Prediction theo story đã duyệt.
- Đủ 9 loại chart không phải map; inventory và phạm vi dữ liệu nằm trong `chart-inventory.md`.
- Filter nhiều cấp, tooltip, drill-down và cross-filter đã được chạy bằng trình duyệt thật; ảnh và biên bản nằm trong `evidence/visual-qa-2026-10-07.md`.
- App đọc `data/processed/clean_dataset.csv` và các CSV ở `data/processed/model/`; không train model khi render.
- Geographic Map dùng ONS geometry theo OGL v3.0, mapping đủ 13/13 nhãn và công bố rõ giới hạn xấp xỉ vùng OU lịch sử.
- Sáu insight lấy từ EDA/Insight Log; metric model chỉ xuất hiện ở RQ6.

## Cấu trúc

| File | Vai trò |
|---|---|
| `app.py` | Entry point, điều hướng, filter state và render bốn phần |
| `dashboard_data.py` | Đường dẫn, schema guard, loader, filter và công thức KPI |
| `chart-inventory.md` | Đối chiếu 9 loại chart, map, RQ/insight và interaction |
| `assets/` | GeoJSON, bảng mapping audit, nguồn/giấy phép và giới hạn map |
| `build-guide.md` | Cách chạy, data contract và quy trình phát triển |
| `wireframe.md` | Kiến trúc thông tin/story flow |
| `qa-t09.md` | Baseline và checklist đối chiếu rubric |
| `evidence/` | Ảnh/video/checklist sau khi kiểm thử thật |

## Nguyên tắc

- Hạt phân tích là `(code_module, code_presentation, id_student)`.
- Không đọc raw hoặc join event nhiều dòng trong app.
- Không gọi VLE clicks là attendance/study hours.
- Không vẽ tay geometry hoặc tạo dữ liệu để lấp phần thiếu; mọi phép xấp xỉ map phải tái tạo được và công bố.
- App khởi động được chưa đồng nghĩa dashboard đã nghiệm thu.

Xem [đặc tả RQ/insight/dashboard](../docs/05-dashboard-spec.md) và [tài liệu model](../docs/04-model.md).
