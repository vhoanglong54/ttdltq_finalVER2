# Dashboard Streamlit

Dashboard cuối gồm hai trang:

1. **Academic Insight & Behavior:** 4 KPI, Filled Map, 100% stacked bar có drill, VLE multi-line, submission scatter + trendline và activity treemap.
2. **Risk Matrix & Early Warning:** 3 KPI model, education × IMD heatmap, previous-attempt box plot, probability gauge, TP/TN/FP/FN donut và High-Risk Action List.

## Chạy local

```powershell
python src/dashboard_features.py
streamlit run dashboard/app.py
```

App cần:

- `data/processed/clean_dataset.csv`
- `data/processed/dashboard/*`
- `data/processed/model/*`
- `dashboard/assets/oulad_regions.geojson`

## Cấu trúc

| File | Vai trò |
|---|---|
| `app.py` | Giao diện, state, filter, chart, story |
| `dashboard_data.py` | Loader, schema guard, filter và KPI |
| `chart-inventory.md` | 8 loại chart thường + map |
| `wireframe.md` | Bố cục hai trang |
| `qa-t09.md` | Baseline và cổng QA |
| `assets/` | GeoJSON, mapping audit, nguồn/giấy phép |
| `evidence/` | Automated QA và screenshot browser thật |

Chi tiết logic ở [đặc tả dashboard](../docs/05-dashboard-spec.md), model ở [04-model.md](../docs/04-model.md), tổng kết ở [10-implementation-summary.md](../docs/10-implementation-summary.md).
