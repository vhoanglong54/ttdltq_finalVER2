# Bằng chứng dashboard Python

Thư mục này chỉ nhận bằng chứng sau khi app thực tế được chạy và kiểm tra. Mỗi lần kiểm tra ghi:

- Commit hoặc trạng thái code được kiểm tra; OS và phiên bản Python/Streamlit/Plotly.
- Checksum input, model version, cutoff và threshold.
- Page/filter context, metric, tử số/mẫu số và `N` của mỗi ảnh.
- Evidence Geographic Map, nguồn/giấy phép geometry và coverage 13/13 region.
- Trước/sau cho filter nhiều cấp, drill-down, cross-filtering; ảnh hover cho tooltip.
- Kết quả đối chiếu baseline và lỗi/hạn chế còn lại.

Không lưu raw data, secrets hoặc thông tin định danh ngoài OULAD. Không tích checklist trước khi evidence được xác nhận.

## Bằng chứng hiện có

- [Automated QA — 06/10/2026](automated-qa-2026-10-06.md): unit test, schema, KPI, model artifact và map build.
- [Visual QA — 07/10/2026](visual-qa-2026-10-07.md): bốn trang dashboard, tooltip, cross-filter, drill-down, map, heatmap và model diagnostics.
