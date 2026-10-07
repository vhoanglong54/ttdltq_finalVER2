# Wireframe dashboard hai trang

## Trang 1 — Academic Insight & Behavior

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Module slicer │ Presentation slicer │ Gender slicer                 │
├───────────────┬─────────────────────┬───────────────┬───────────────┤
│ Total Students│ Avg Score           │ Pass Rate     │ At-Risk Rate  │
├─────────────────────────────────────────────────────────────────────┤
│ 1. FILLED MAP — click region để cross-filter                       │
├─────────────────────────────────────────────────────────────────────┤
│ 2. 100% STACKED BAR — Module → click → Presentation                 │
├─────────────────────────────────────────────────────────────────────┤
│ 3. MULTI-LINE — VLE At-Risk vs Not-At-Risk + deadline markers       │
├─────────────────────────────────────────────────────────────────────┤
│ 4. SCATTER + TRENDLINE — submission delay × score                   │
├─────────────────────────────────────────────────────────────────────┤
│ 5. TREEMAP — activity_type × clicks                                 │
├─────────────────────────────────────────────────────────────────────┤
│ STORY CARD — 3 insight ngắn, định lượng, cập nhật theo filter        │
└─────────────────────────────────────────────────────────────────────┘
```

## Trang 2 — Risk Matrix & Early Warning

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Risk Level slicer                 │ IMD band slicer                  │
├──────────────────────┬──────────────────────┬───────────────────────┤
│ Model Accuracy       │ Recall At-Risk       │ High Risk Count       │
├─────────────────────────────────────────────────────────────────────┤
│ 6. HEATMAP — highest_education × imd_band                           │
├─────────────────────────────────────────────────────────────────────┤
│ 7. BOX PLOT — score ngày 105 × previous attempts                    │
├───────────────────────────────┬─────────────────────────────────────┤
│ 8. GAUGE — mean probability   │ 9. DONUT — TP/TN/FP/FN             │
├─────────────────────────────────────────────────────────────────────┤
│ STUDENT ACTION LIST — High Risk + red bar + nút lọc High một-click  │
├─────────────────────────────────────────────────────────────────────┤
│ STORY CARD — 3 insight ngắn + giới hạn sử dụng model                │
└─────────────────────────────────────────────────────────────────────┘
```

## Quy tắc UX

- Slicer và KPI luôn đứng trước visual.
- Insight đặt cuối mỗi story page, không che chart và không lặp mô tả trục.
- Caption giải thích grain, sample, threshold và limitation ngay nơi cần.
- Không hiển thị hierarchy nhiều cấp đồng thời; drill chỉ mở một cấp.
- Action list là hỗ trợ ưu tiên, không phải quyết định tự động.
