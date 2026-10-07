# Wireframe và story flow dashboard Python

## Khung chung

```text
┌──────────────── Sidebar ────────────────┐
│ Navigation                             │
│ Module → Presentation → Region         │
│ Filter context + Reset                 │
└────────────────────────────────────────┘

┌──────────────── Main content ─────────────────────────────┐
│ Page title + câu hỏi nghiên cứu + giới hạn                │
│ KPI strip                                                  │
│ Primary visual / selection → secondary visual (crossfilter)│
│ Insight card: số liệu + N + interpretation + limitation    │
│ Câu chuyển sang phần tiếp theo                              │
└────────────────────────────────────────────────────────────┘
```

## Bốn phần

| Phần | Câu hỏi | Vai trò trong story | Trạng thái |
|---|---|---|---|
| Overview | Điều gì đang xảy ra với kết quả và `At_Risk`? | Thiết lập baseline, outcome mix và drill module/presentation | Đã triển khai local |
| Factor Analysis | VLE và assessment đến ngày 105 liên hệ ra sao? | Line, box, bubble và heatmap cho tín hiệu/tương tác | Đã triển khai local |
| Risk Analysis | Nhóm/risk profile nào đáng chú ý? | Treemap, regional bar và Geographic Map | Đã triển khai local; map có audit |
| Prediction | Nhận diện sớm tốt đến đâu và sai ở đâu? | Xác suất, confusion, ROC/PR, calibration và CI | Đã triển khai local |

## Tương tác

- **Filter nhiều cấp:** module làm hẹp presentation; module/presentation làm hẹp region.
- **Drill-down:** sunburst Module → Presentation → Result; hierarchy và phần trăm parent hiển thị trong tooltip.
- **Tooltip:** metric, mẫu số/`N`, định nghĩa và context.
- **Cross-filtering:** selection trên biểu đồ chính làm đổi KPI/bảng/biểu đồ liên quan.

## Nguyên tắc chọn visual

Mỗi visual gắn RQ/H, kiểu dữ liệu và insight. Inventory đã khóa sau EDA tại `chart-inventory.md`: 9 loại chart không phải map; Geographic Map là visual bắt buộc và được nghiệm thu riêng.
