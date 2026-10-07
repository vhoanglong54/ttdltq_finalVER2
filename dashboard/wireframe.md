# Wireframe dashboard bốn trang

## Trang 1 — Bức tranh kết quả học tập

```text
FILTER: Học phần ẩn danh │ Đợt mở lớp │ Giới tính
KPI: Sinh viên │ Điểm TB │ Tỷ lệ qua môn │ Tỷ lệ có nguy cơ không đạt
STORY: cứ 100 lượt học có bao nhiêu lượt trượt/bỏ học; học phần/vùng là bối cảnh
1. FILLED MAP — click region để cross-filter
2. 100% STACKED BAR — học phần → đợt mở; nhãn nguy cơ không đạt cuối thanh
```

## Trang 2 — Các yếu tố học tập

```text
FILTER: Học phần ẩn danh │ Đợt mở lớp │ Giới tính
STORY: hoàn thành bài là yếu tố rõ nhất + mức tham gia trực tuyến
3. MULTI-LINE — mức tham gia trực tuyến của nhóm nguy cơ và không nguy cơ
4. BAR — hoàn thành bài đến ngày 105 × nguy cơ không đạt
5. SCATTER + TRENDLINE — submission delay × score
6. TREEMAP — activity_type × clicks
```

## Trang 3 — Kết hợp nhiều yếu tố

```text
FILTER: Học phần ẩn danh │ Đợt mở lớp │ Giới tính
7. HEATMAP — nhóm mức tham gia trực tuyến × nhóm điểm bài tập
8. HEATMAP — highest_education × imd_band
9. BOX PLOT — score ngày 105 × previous attempts
STORY: thấp–thấp/cao–cao + lịch sử học lại + giới hạn của yếu tố bối cảnh
```

## Trang 4 — Dự đoán nguy cơ

```text
FILTER: Mức nguy cơ │ Nhóm hoàn cảnh khu vực
KPI: Tỷ lệ dự đoán đúng │ Tỷ lệ phát hiện │ Số lượt cần ưu tiên
10. GAUGE — nguy cơ không đạt trung bình
11. DONUT — dự đoán đúng │ cảnh báo nhầm │ bỏ sót
DANH SÁCH HỖ TRỢ — nguy cơ cao + thanh cảnh báo + nút lọc
STORY: dự đoán trượt/bỏ học + độ chính xác dễ hiểu + hành động
```

## Quy tắc UX

- VLE, IMD, AAA–GGG, B/J và các chỉ số mô hình được giải thích bằng tiếng Việt trước biểu đồ.
- Story dùng ngôn ngữ ngắn, có số liệu và giới hạn; không lặp mô tả trục.
- Không hiển thị hierarchy dày đặc; drill chỉ mở một cấp.
- Action List hỗ trợ ưu tiên, không phải quyết định tự động.
