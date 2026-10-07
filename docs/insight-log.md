# Insight Log — các yếu tố liên quan đến kết quả học tập

Đây là nơi nghiệm thu duy nhất cho insight **phân tích dữ liệu**. Sáu insight dưới đây được tạo từ EDA, tách khỏi đánh giá Logistic Regression ở RQ6. Mọi kết luận chỉ mô tả liên hệ/khác biệt trên OULAD, không khẳng định quan hệ nhân quả.

## Bản ngắn dùng trên dashboard

| ID | Phát hiện và bằng chứng | Ý nghĩa |
|---|---|---|
| INS-01 | Tỷ lệ nguy cơ không đạt khác nhau giữa các học phần/đợt mở: `CCC-2014B` 65,8%, `AAA-2013J` 27,4%. | Học phần là bối cảnh có chênh lệch, không phải nguyên nhân đã được chứng minh. |
| INS-02 | Nhóm 25% ít tham gia học trực tuyến nhất có nguy cơ không đạt 64,4%; nhóm tham gia nhiều nhất là 18,7%. | Mức tham gia trực tuyến thấp là yếu tố cảnh báo sớm đáng chú ý. |
| INS-03 | Nhóm chưa hoàn thành bài đến hạn có nguy cơ không đạt 96,6%; nhóm hoàn thành đủ là 24,8%. | Đây là yếu tố liên quan rõ nhất; cần theo dõi tiến độ làm bài. |
| INS-04 | Nhóm vừa ít tham gia trực tuyến vừa có điểm bài tập thấp có nguy cơ 73,3%; nhóm cao ở cả hai chỉ 8,3%. | Nên xem hai yếu tố cùng nhau thay vì chỉ nhìn một chỉ số. |
| INS-05 | Nhóm từng học học phần trước có nguy cơ 56,1%; nhóm học lần đầu là 36,3%. | Lịch sử học lại là bối cảnh để ưu tiên xem xét, không phải nhãn đánh giá cá nhân. |
| INS-06 | North Western 59,8%, Ireland 45,1%. | Khu vực chỉ cho thấy nơi cần xem thêm, không chứng minh nơi ở gây ra kết quả. |

Dashboard đưa INS-02 đến INS-05 thành kết luận chính vì chúng trả lời trực tiếp yếu tố học tập nào liên quan đến kết quả. INS-01 và INS-06 chỉ làm bối cảnh. Tử số/mẫu số, phạm vi và giới hạn đầy đủ vẫn được lưu bên dưới để kiểm chứng.

## Bảng nghiệm thu

| ID | RQ/H | Thông điệp một câu | Bằng chứng | N và tử số/mẫu số | Giới hạn | Vị trí story | Đạt |
|---|---|---|---|---|---|---|:---:|
| INS-01 | RQ1 / H01 | `CCC-2014B` có At-Risk rate 65,8%, cao hơn `AAA-2013J` 27,4% đúng 38,3 điểm %. | `01_outcome_by_module_presentation.png`; `module_presentation_risk.csv` | 1.273/1.936 so với 105/383; toàn khóa N=32.593 | Khác cấu trúc module, assessment và cohort; không phải tác động của module. | Academic · outcome drill | [x] |
| INS-02 | RQ2 / H02–H04 | Nhóm 25% VLE clicks thấp nhất đến ngày 105 có At-Risk 64,4%, cao hơn nhóm 25% cao nhất 18,7% đúng 45,7 điểm %. | `02_vle_weekly_trend.png`; `03_early_vle_boxplot.png`; `engagement_quartiles.csv` | 4.047/6.283 so với 1.173/6.283; snapshot N=25.132 | Click là tương tác nền tảng, không đo chất lượng hay thời gian học. | Academic · VLE line | [x] |
| INS-03 | RQ3 / H05–H06 | Nhóm chưa hoàn thành assessment nào trước cutoff có At-Risk 96,6%, cao hơn nhóm hoàn thành 100% là 24,8% đúng 71,9 điểm %. | `04_assessment_completion_risk.png`; `assessment_completion.csv`; `assessment_score_quartiles.csv` | 1.620/1.677 so với 4.695/18.969; snapshot N=25.132 | Lịch assessment khác theo module; completion tại cutoff không phải nguyên nhân duy nhất. | Academic · submission | [x] |
| INS-04 | RQ5 / H09 | Hồ sơ đồng thời VLE thấp và điểm assessment thấp có At-Risk 73,3%; hồ sơ cả hai cao là 8,3%, chênh 65,1 điểm %. | `05_engagement_assessment_heatmap.png`; `engagement_assessment_matrix.csv` | 1.232/1.680 so với 197/2.385; snapshot N=25.132 | Chỉ gồm attempt có điểm trước cutoff; quartile là nhóm mô tả, không phải ngưỡng can thiệp. | Risk · context đa biến | [x] |
| INS-05 | RQ4 / H07 | Attempt có ít nhất một lần học module trước có At-Risk 56,1%, cao hơn nhóm chưa học trước 36,3% đúng 19,7 điểm %. | `previous_attempts.csv`; box plot dashboard | 1.760/3.140 so với 7.987/21.992; snapshot N=25.132 | Không có kết quả chi tiết của lần học trước; còn khác biệt module/cohort chưa kiểm soát. | Trang 3 · previous attempts | [x] |
| INS-06 | RQ4 / H08 | North Western Region có At-Risk 59,8%, Ireland 45,1%, tạo khoảng chênh mô tả 14,7 điểm %. | `06_region_at_risk_rate.png`; `region_risk.csv`; Geographic Map + mapping audit | 1.738/2.906 so với 534/1.184; toàn khóa N=32.593 | Region lịch sử của OU; map là xấp xỉ công bố từ ONS; không suy ra nguyên nhân cá nhân. | Academic · map | [x] |

## Chi tiết và “so what?”

### INS-01 — Chênh lệch giữa module/presentation

- **Phạm vi:** toàn bộ 32.593 learning attempts, không filter.
- **Tái tạo:** `python src/eda_analysis.py`; xem `build_insight_evidence()` và hình 01.
- **Kết quả giả thuyết:** H01 được ủng hộ ở mức mô tả.
- **Diễn giải:** outcome mix và At-Risk rate thay đổi đáng kể giữa các module/presentation.
- **So what:** dashboard phải cho phép drill Module → Presentation; không dùng một baseline chung để diễn giải mọi khóa.

### INS-02 — Tín hiệu tương tác VLE trước cutoff

- **Phạm vi:** 25.132 attempts đủ điều kiện ở ngày 105; quartile tính trên snapshot này.
- **Tái tạo:** hình 02–03 và `engagement_quartiles.csv`.
- **Kết quả giả thuyết:** H02, H03, H04 được ủng hộ ở mức mô tả; nhóm At-Risk có mean weekly clicks thấp hơn trong 15/15 tuần trọn vẹn.
- **Diễn giải:** tương tác VLE thấp đi cùng tỷ lệ kết quả bất lợi cao hơn.
- **So what:** clicks và active days là tín hiệu cảnh báo sớm hữu ích, nhưng không được gọi là attendance hoặc study hours.

### INS-03 — Tiến độ assessment là tín hiệu phân tách mạnh

- **Phạm vi:** snapshot ngày 105; completion tính theo assessment đã đến hạn tại cutoff.
- **Tái tạo:** hình 04; bảng completion và score quartile.
- **Kết quả giả thuyết:** H05 và H06 được ủng hộ ở mức mô tả. Trong nhóm có điểm, Q1 và Q4 chênh 51,8 điểm % At-Risk; 3.783 attempts chưa có scored assessment được giữ riêng, không ép vào quartile.
- **Diễn giải:** mức hoàn thành và điểm assessment sớm cùng cung cấp tín hiệu rõ, nhưng bị chi phối bởi lịch assessment của từng module.
- **So what:** mọi visual assessment phải hiển thị module/presentation và nhóm thiếu điểm, tránh coi thiếu là 0 điểm.

### INS-04 — VLE và assessment cần được đọc cùng nhau

- **Phạm vi:** snapshot ngày 105; ma trận chỉ gồm attempts có score để tạo assessment quartile.
- **Tái tạo:** hình 05 và `engagement_assessment_matrix.csv`.
- **Kết quả giả thuyết:** H09 được ủng hộ ở mức mô tả; gradient vẫn xuất hiện theo cả hai chiều.
- **Diễn giải:** tổ hợp hai tín hiệu tạo risk profile rõ hơn so với chỉ nhìn một con số.
- **So what:** dashboard dùng heatmap/scatter để người xem kiểm tra đồng thời engagement và assessment, không biến quartile thành quy tắc tự động.

### INS-05 — Lịch sử học lại là context quan trọng

- **Phạm vi:** snapshot ngày 105; `num_of_prev_attempts = 0` so với `>= 1`.
- **Tái tạo:** `previous_attempts.csv` và box plot previous attempts trên Trang 3.
- **Kết quả giả thuyết:** H07 được ủng hộ ở mức mô tả.
- **Diễn giải:** nhóm từng học module trước có tỷ lệ At-Risk cao hơn, nhưng dữ liệu không cho biết đầy đủ nguyên nhân hoặc kết quả từng lần trước.
- **So what:** đây là context để ưu tiên xem xét, không phải nhãn đánh giá cá nhân.

### INS-06 — Khác biệt không gian cần được trình bày thận trọng

- **Phạm vi:** toàn khóa, 13 nhãn region lịch sử của OULAD.
- **Tái tạo:** hình 06 và `region_risk.csv`.
- **Kết quả giả thuyết:** H08 được ủng hộ ở mức mô tả, đồng thời có nguy cơ confounding.
- **Diễn giải:** rate khác nhau theo region, nhưng biến này có thể đồng biến với module mix, cohort, IMD và đặc điểm người học.
- **So what:** Geographic Map kèm N, bar đối chiếu và lưu ý phạm vi; geometry ONS, giấy phép và mapping 13/13 được audit trong `dashboard/assets/README.md`.

## Mạch Story đã chốt

1. Bắt đầu từ outcome tổng thể, rồi drill xuống module/presentation có chênh lệch lớn.
2. Nêu yếu tố rõ nhất: chưa hoàn thành bài đến hạn đi cùng nguy cơ không đạt rất cao.
3. Bổ sung yếu tố thứ hai: mức tham gia học trực tuyến thấp đi cùng nguy cơ cao hơn.
4. Kết hợp mức tham gia × điểm bài tập để cho thấy hai bất lợi xuất hiện cùng lúc.
5. Đặt kết quả trong bối cảnh lịch sử học lại và khu vực, luôn công bố N và giới hạn.
6. Sau phần insight dữ liệu mới chuyển sang mô hình dự đoán trượt/bỏ học.

Model là phần đánh giá riêng trong `docs/04-model.md`; Accuracy, F1, ROC-AUC hoặc PR-AUC không được tính vào sáu insight trên.
