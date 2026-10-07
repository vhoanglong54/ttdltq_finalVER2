# 04 — Logistic Regression dự báo At-Risk

**Trạng thái:** Model v4 đã có artifact và verification; dashboard sử dụng bản này cho RQ6 cho đến khi chủ dự án duyệt bản thay thế.

**Trạng thái:** đã chạy và kiểm tra local trên dữ liệu OULAD mới nhất; chưa commit trong đợt tái cấu trúc này.

**Thuật toán theo rubric:** Logistic Regression. `DummyClassifier` chỉ là baseline kỹ thuật, không phải mô hình chính thứ hai.

Mục này là nguồn giải thích duy nhất cho toàn bộ model: mục tiêu, dữ liệu, feature, cách train, thí nghiệm, metric, kết quả, artifact và contract dashboard Python. Các README khác chỉ được phép trỏ về đây, không lặp lại nội dung model.

## Mục tiêu dự báo

Tại ngày thứ 105 tính từ đầu một presentation, model ước lượng khả năng một **lượt học** `(code_module, code_presentation, id_student)` sẽ kết thúc bằng `Fail/Withdrawn`:

- `At_Risk = 1`: `Fail` hoặc `Withdrawn`.
- `At_Risk = 0`: `Pass` hoặc `Distinction`.
- Đầu ra chính: `risk_probability`, `predicted_at_risk`, `predicted_status` và `risk_band`.
- Mục đích: ưu tiên hỗ trợ học tập; không dùng để chẩn đoán, xử phạt hoặc ra quyết định tự động.

Đây là phân loại nhị phân, không phải hồi quy dự báo điểm. Vì vậy, Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, Brier và Log Loss là các chỉ số phù hợp. `R²` và RMSE của hồi quy liên tục không phù hợp; khi cần chỉ báo tương tự, phải ghi đúng tên **McFadden pseudo-R²** và **Probability RMSE**.

## Khái niệm cần hiểu

| Khái niệm | Ý nghĩa trong dự án |
|---|---|
| Lượt học / attempt | Một bản ghi có khóa `(code_module, code_presentation, id_student)`; một sinh viên có thể có nhiều lượt học. |
| Target | `At_Risk`, tạo từ kết quả cuối và chỉ dùng làm nhãn huấn luyện/đánh giá. |
| Feature | Thông tin model được phép thấy tại cutoff, như điểm assessment sớm và hoạt động VLE. |
| Cutoff | Ngày chụp dữ liệu; event sau ngày 105 bị che để mô phỏng dự báo khi khóa học chưa kết thúc. |
| Cohort eligible | Lượt đã đăng ký và chưa rút trước hoặc tại cutoff, tức còn phù hợp để cảnh báo. |
| Logistic Regression | Ước lượng log-odds rồi dùng sigmoid chuyển thành xác suất rủi ro từ 0 đến 1. |
| Threshold | Ngưỡng đổi xác suất thành nhãn; xác suất từ 0,415 trở lên được cảnh báo At-Risk. |
| Hệ số / odds ratio | Dấu hệ số thể hiện hướng liên hệ; odds ratio là `exp(coefficient)`, không chứng minh nhân quả. |
| Regularization L1 | Hạn chế overfit và có thể đưa hệ số ít hữu ích về 0. |
| `C` | Nghịch đảo mức regularization; `C` nhỏ phạt mạnh hơn, `C` lớn phạt nhẹ hơn. |
| Train / Validation / Test | Train fit pipeline; validation chọn biến thể và threshold; test chỉ đánh giá cuối. |
| Baseline | `DummyClassifier` dự báo theo tỷ lệ lớp để làm mốc tối thiểu. |

`risk_probability = 0,80` nghĩa là model ước lượng rủi ro 80% theo pattern lịch sử và dữ liệu tại cutoff, không có nghĩa người học chắc chắn thất bại.

## Dữ liệu đầu vào và lý do chọn cutoff 105

Model không đọc `clean_dataset.csv` chứa aggregate toàn thời gian. Snapshot được dựng trực tiếp từ bảy bảng sạch ở `data/interim/`, được tái tạo từ bảy CSV raw chính thức sau khi kiểm checksum và header.

Cleaning mới giữ nguyên tổng **39.605.099** click: 10.655.280 dòng `studentVle.csv` được gom theo learner–resource–day và cộng `sum_click` thành 8.459.320 sự kiện logic. Không xóa 787.170 dòng trùng toàn dòng vì mỗi dòng có thể là một đóng góp click hợp lệ. Báo cáo kiểm chứng dữ liệu nằm tại [Data Quality Report](../reports/data-quality-report.md).

| Cutoff | Eligible attempts | At-Risk rate | Có VLE | Có assessment đã nộp | Ngày học còn lại trung bình |
|---:|---:|---:|---:|---:|---:|
| 28 | 27.522 | 44,12% | 96,71% | 74,13% | 227,95 |
| 42 | 27.012 | 43,06% | 97,39% | 84,36% | 213,96 |
| 56 | 26.513 | 41,98% | 97,76% | 87,67% | 200,00 |
| 84 | 25.720 | 40,19% | 98,03% | 93,18% | 172,01 |
| 98 | 25.349 | 39,31% | 98,09% | 93,41% | 158,01 |
| **105** | **25.132** | **38,78%** | **98,12%** | **93,47%** | **151,01** |
| 112 | 24.930 | 38,29% | 98,16% | 93,58% | 144,00 |

Ngày 98 từng được chọn vì là mốc sớm nhất đạt Accuracy trên 80%. Bản cải tiến chọn ngày 105: chậm hơn 7 ngày nhưng vẫn còn trung bình 151 ngày để can thiệp, CV PR-AUC và chất lượng xác suất tốt hơn, Recall/F1 validation cao hơn, đồng thời toàn bộ metric test chính đều tăng. Chỉ event có `date <= 105` hoặc `date_submitted <= 105` được dùng. Attempt đăng ký sau cutoff hoặc đã rút trước/tại cutoff bị loại; `date_unregistration` chỉ xác định eligibility và không đi vào feature.

## Feature contract và chống leakage

Feature được dùng:

- Bối cảnh: module, presentation, tổ hợp module–presentation, highest education, số lần học trước, tín chỉ, ngày đăng ký và độ dài presentation.
- Assessment đến cutoff: số bài đến hạn/đã nộp/đã chấm, tỷ lệ hoàn thành, mean/weighted score, missing, late, banked và khoảng cách từ lần nộp cuối. V4 bổ sung trọng số đã đến hạn/đã hoàn thành, điểm tích lũy theo trọng số, tỷ lệ điểm dưới 40 và số ngày nộp trễ trung bình.
- VLE đến cutoff: event/click, ngày hoạt động, độ đa dạng resource/activity, click theo loại hoạt động, cửa sổ 7/28 ngày, mức thay đổi, tỷ trọng hoạt động gần đây và khoảng cách từ hoạt động cuối.
- Count lệch mạnh dùng `log1p`; numeric median-impute và standardize; categorical điền `Unknown` và one-hot encode. Hai mươi tám tương tác cặp và 49 hệ số dốc theo module giúp Logistic Regression biểu diễn quan hệ khác nhau giữa các module mà không đổi thuật toán.

Feature trọng số giải quyết một điểm yếu cụ thể của v3: hai sinh viên có thể cùng điểm trung bình 80 nhưng một người đã hoàn thành gần hết phần bài đến hạn, người còn lại mới hoàn thành rất ít. `assessment_weight_completion_rate_cutoff` và `assessment_due_performance_rate_cutoff` giữ lại khác biệt tiến độ này. Tất cả tử số chỉ lấy submission có `date_submitted <= 105`; mẫu số là lịch assessment đã đến hạn nên không nhìn kết quả tương lai.

Cột bị cấm: `id_student`, `final_result`, `At_Risk`, `Performance_Level`, `date_unregistration`, aggregate `*_all_time` và mọi assessment/VLE sau cutoff. `gender`, `region`, `imd_band`, `age_band`, `disability` chỉ dùng QA theo nhóm, không làm feature chính. Toàn bộ preprocessing chỉ được fit trên train.

OULAD không có timestamp công bố điểm. Pipeline giả định điểm của bài nộp trước/tại cutoff đã quan sát được tại cutoff; nếu nghiệp vụ công bố điểm trễ thì phải loại feature điểm hoặc bổ sung timestamp công bố thật rồi train lại.

## Luồng code và trách nhiệm

```text
7 CSV raw chính thức
  → verify_oulad_source.py: checksum/header/số dòng
  → oulad_pipeline.py: audit → clean → interim
  → at_risk_features.py: cohort ngày 105 + snapshot assessment/VLE
  → at_risk_experiments.py: so sánh biến thể bằng train-CV/validation
  → at_risk_model.py: split → preprocessing → tune → threshold → test
  → CSV/JSON/TXT kiểm chứng trong data/processed/model
  → dashboard Streamlit chỉ đọc và trực quan hóa output đã kiểm tra
```

| File | Trách nhiệm |
|---|---|
| `src/at_risk_features.py` | Xác định cohort, feature được phép/cấm và tạo snapshot đúng hạt tại cutoff. |
| `src/at_risk_experiments.py` | So sánh baseline, feature bổ sung, spline và tương tác mà không dùng test để chọn. |
| `src/at_risk_model.py` | Group split, preprocessing, tuning Logistic Regression, threshold, test, bootstrap và xuất artifact. |
| `tests/test_at_risk_model.py` | Kiểm tra bảo toàn click, cohort, split, leakage, threshold và khoảng tin cậy. |

## Split, tuning và chọn phương án

Split theo nhóm `id_student`, bảo đảm một sinh viên chỉ xuất hiện trong một tập:

| Split | Attempts | Sinh viên | At-Risk | At-Risk rate |
|---|---:|---:|---:|---:|
| Train | 17.952 | 16.492 | 6.963 | 38,79% |
| Validation | 3.590 | 3.299 | 1.392 | 38,77% |
| Test | 3.590 | 3.303 | 1.392 | 38,77% |

Grid search trên train dùng 5-fold `StratifiedGroupKFold`, chọn theo PR-AUC với `C ∈ {0.03, 0.1, 0.3, 1, 3, 10}`, `class_weight ∈ {None, balanced}` và L1/L2. Test không tham gia chọn feature, hyperparameter hoặc threshold.

Các biến thể cấu trúc được so sánh tại cutoff 98 trước khi chốt v3:

| Biến thể | CV PR-AUC | Validation Accuracy | Recall | F1 | Validation PR-AUC | Threshold |
|---|---:|---:|---:|---:|---:|---:|
| Baseline v2 | 0,8552 | 0,8122 | 0,7266 | 0,7525 | 0,8643 | 0,435 |
| Thêm feature an toàn + module–presentation | 0,8566 | 0,8158 | 0,7056 | 0,7507 | 0,8667 | 0,465 |
| Phương án trên + spline | 0,8567 | 0,8117 | 0,7041 | 0,7461 | 0,8658 | 0,460 |
| **Phương án trên + tương tác cặp (v3)** | **0,8577** | **0,8210** | **0,7133** | **0,7580** | **0,8687** | **0,465** |
| V3 + feature tỷ lệ/động lượng | 0,8578 | 0,8216 | 0,7013 | 0,7555 | 0,8685 | 0,480 |
| V3 + feature tỷ lệ/động lượng + quantile bins | 0,8576 | 0,8216 | 0,7027 | 0,7559 | 0,8664 | 0,475 |

Hai biến thể tỷ lệ/động lượng đầu tiên ở cutoff 98 bị loại vì mức tăng Accuracy validation chỉ 0,06 điểm phần trăm nhưng Recall/F1 giảm. Vòng cải tiến tại cutoff 105 tiếp tục dùng train-CV/validation, không dùng test để chọn. Kết quả quan trọng:

| Cấu hình cutoff 105 | CV PR-AUC | Validation Accuracy | Recall | F1 | Validation PR-AUC | Brier |
|---|---:|---:|---:|---:|---:|---:|
| V3 hiện hữu | 0,8609 | 0,8198 | 0,7385 | 0,7606 | 0,8685 | 0,1242 |
| Hệ số theo module + tỷ lệ/động lượng | 0,8621 | 0,8231 | 0,7299 | 0,7619 | 0,8716 | 0,1229 |
| Thêm tiến độ assessment theo trọng số, tại cùng mức Recall v3 | **0,8634** | **0,8273** | **0,7392** | **0,7685** | **0,8741** | **0,1215** |

Elastic Net bằng solver SAGA cũng được thử nhưng chi phí cao hơn nhiều và không tạo được bằng chứng thắng ổn định trong thời gian kiểm tra, nên bị loại. V4 chọn Logistic Regression L1/liblinear, `C=0,3`, `class_weight=None`. Threshold được duyệt hoàn toàn trên validation bằng Accuracy cao nhất dưới ràng buộc Recall At-Risk ≥ 0,75; lưới threshold bước 0,001 chọn `0,415`. Validation cuối đạt Accuracy 0,8245, Recall 0,7522 và F1 0,7687. Mức sàn 0,75 cao hơn v3 để ngăn việc tăng Accuracy bằng cách bỏ sót thêm sinh viên At-Risk.

## Kết quả test và cách đọc độ tin cậy

| Metric | Logistic Regression | Dummy baseline |
|---|---:|---:|
| Accuracy | **0,8270** | 0,6123 |
| Balanced Accuracy | **0,8101** | 0,5000 |
| Precision At-Risk | **0,8024** | 0,0000 |
| Recall At-Risk | **0,7349** | 0,0000 |
| F1 At-Risk | **0,7672** | 0,0000 |
| ROC-AUC | **0,8906** | 0,5000 |
| PR-AUC | **0,8701** | 0,3877 |
| Brier Score, thấp hơn tốt hơn | **0,1237** | 0,2374 |

Confusion matrix: TN 1.946, FP 252, FN 369, TP 1.023. Model đúng 82,70% trên 3.590 lượt test và cao hơn baseline 21,48 điểm phần trăm. Chất lượng xác suất: Probability RMSE 0,3517; Probability MAE 0,2491; Log Loss 0,3882; McFadden pseudo-R² 0,4186. Mức đồng thuận nhãn: MCC 0,6315 và Cohen's Kappa 0,6300.

| Metric | Câu hỏi được trả lời |
|---|---|
| Accuracy | Bao nhiêu dự báo đúng trên toàn test? Có thể đẹp giả nếu một lớp chiếm đa số. |
| Balanced Accuracy | Khả năng nhận đúng hai lớp có cân bằng không? |
| Precision | Trong số lượt bị cảnh báo, bao nhiêu thực sự At-Risk? |
| Recall | Trong số lượt thực sự At-Risk, model tìm được bao nhiêu? |
| F1 | Precision và Recall có cân bằng không? |
| ROC-AUC | Model xếp hạng hai lớp tốt đến đâu qua mọi threshold? |
| PR-AUC | Chất lượng Precision–Recall của lớp At-Risk so với baseline 0,3877? |
| Brier/Log Loss | Xác suất có gần kết quả thật và có bị tự tin sai không? |
| MCC/Kappa | Mức đồng thuận khi xét đủ bốn ô confusion matrix và cơ hội ngẫu nhiên? |

Khoảng tin cậy 95% dùng 2.000 bootstrap theo `id_student`:

| Metric | Ước lượng | Cận dưới | Cận trên |
|---|---:|---:|---:|
| Accuracy | 0,8270 | 0,8146 | 0,8384 |
| Balanced Accuracy | 0,8101 | 0,7971 | 0,8229 |
| Precision | 0,8024 | 0,7805 | 0,8229 |
| Recall | 0,7349 | 0,7114 | 0,7577 |
| F1 | 0,7672 | 0,7494 | 0,7844 |
| ROC-AUC | 0,8906 | 0,8790 | 0,9012 |
| PR-AUC | 0,8701 | 0,8560 | 0,8837 |
| Brier | 0,1237 | 0,1173 | 0,1305 |

Kết luận đúng là “điểm ước lượng test đạt 82,70%, khoảng tin cậy bootstrap 95% là 81,46%–83,84%”. Cận dưới đã vượt 80% trên test hiện tại. Độ tin cậy còn đến từ group split, preprocessing chỉ fit trên train, threshold chỉ chọn trên validation, leakage guard, baseline, kiểm thử và khả năng tái tạo.

So với cutoff 105 v3, v4 tăng Accuracy 0,22 điểm %, Precision 0,08 điểm %, Recall 0,65 điểm %, F1 0,39 điểm %, ROC-AUC 0,12 điểm % và PR-AUC 0,32 điểm %, đồng thời Brier giảm 0,0017. Mức tăng nhỏ nhưng nhất quán trên mọi metric chính; cận dưới Accuracy 95% tăng từ 81,28% lên 81,46%. Các khoảng tin cậy v3/v4 vẫn chồng lấn mạnh, nên không được tuyên bố mức tăng này có ý nghĩa thống kê nếu chưa có paired bootstrap hoặc holdout mới. So với cutoff 98, quyết định dùng ngày 105 vẫn có trade-off cảnh báo muộn hơn 7 ngày và giảm 217 lượt eligible.

## Hệ số nổi bật

Hệ số phản ánh liên hệ sau preprocessing, không chứng minh nhân quả:

| Feature | Coefficient | Odds ratio | Hướng liên hệ |
|---|---:|---:|---|
| `code_module_CCC` | -0,5871 | 0,5560 | rủi ro thấp hơn |
| `vle_days_since_last_activity` | 0,5442 | 1,7233 | rủi ro cao hơn |
| `module_CCC_x_assessment_completion_rate_cutoff` | 0,5295 | 1,6981 | hiệu ứng riêng của CCC; phải đọc cùng hệ số chính |
| `assessment_weighted_score_cutoff` | -0,4585 | 0,6322 | rủi ro thấp hơn |
| `assessment_due_weighted_points_cutoff` | -0,4349 | 0,6474 | rủi ro thấp hơn |
| `log1p_vle_resource_count_cutoff` | -0,4059 | 0,6664 | rủi ro thấp hơn |
| `vle_active_days_last_28_days` | -0,3406 | 0,7114 | rủi ro thấp hơn |
| `assessment_weight_completion_rate_cutoff` | -0,3372 | 0,7138 | rủi ro thấp hơn |

## Artifact và contract cho dashboard Python

Các artifact tái tạo được nằm trong `data/processed/model/`; bundle Python ở `models/logistic_regression.joblib`. Ứng dụng Streamlit không đọc `.joblib` và không train model khi render, mà chỉ đọc CSV:

| File | Vai trò |
|---|---|
| `cutoff_audit.csv` | So sánh coverage giữa các cutoff. |
| `feature_snapshot.csv` | Snapshot ngày 105, một dòng mỗi attempt eligible. |
| `model_predictions.csv` | Actual, predicted, probability, risk band, split và error type. |
| `model_metrics.csv` | Metric Logistic/baseline theo split. |
| `model_confusion_matrix.csv` | Dữ liệu dựng confusion matrix. |
| `model_coefficients.csv` | Hệ số và odds ratio. |
| `model_curve_points.csv` | Điểm ROC và Precision–Recall. |
| `model_calibration.csv` | Xác suất dự báo và observed rate theo bin. |
| `model_confidence_intervals.csv` | Khoảng tin cậy bootstrap. |
| `model_subgroup_metrics.csv` | QA theo module, presentation và demographic. |
| `threshold_selection.csv` | Metric theo threshold và dòng được chọn. |
| `cv_results.csv` | Kết quả grid search. |
| `model_metadata.json` | Version, feature contract, cấu hình và SHA-256 artifact. |
| `model_verification.csv` | Chín điều kiện đối chiếu Accuracy, CI, Recall/F1, PR-AUC, Brier, baseline, presentation và checksum. |
| `model_evaluation.txt` | Báo cáo chạy tự sinh cục bộ; không phải tài liệu dự án thứ hai. |

Data source chính của trang Prediction là `model_predictions.csv`, hạt một attempt eligible. Nếu liên kết với bảng phân tích phải dùng đủ ba khóa `(code_module, code_presentation, id_student)` và không join event raw. Trang đánh giá mặc định `dataset_split = test`.

- KPI lấy từ `model_metrics.csv`: Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC.
- Xác suất/danh sách rủi ro lấy từ `model_predictions.csv`.
- Actual vs Predicted dùng `actual_status`, `predicted_status`, `error_type`.
- Confusion matrix, ROC/PR curve, calibration và QA theo nhóm dùng các CSV tương ứng.
- Risk band: `High` nếu probability ≥ 0,415; `Medium` nếu 0,2075 đến dưới 0,415; `Low` nếu thấp hơn 0,2075.
- Tooltip phải ghi cutoff 105, threshold 0,415 và model version `lr-oulad-c105-s42-v4`.

Output đánh giá lịch sử có actual label. Khi chấm một lượt học mới, input chỉ gồm feature quan sát đến cutoff; tuyệt đối không truyền `final_result` hoặc target vào model.

## Tái tạo và kiểm tra

```powershell
python -m pip install -r requirements.txt
python src/verify_oulad_source.py data/raw
python src/oulad_pipeline.py audit data/raw
python src/oulad_pipeline.py clean data/raw
python src/oulad_pipeline.py build data/raw
python src/oulad_pipeline.py report
python src/at_risk_model.py audit-cutoffs
python src/at_risk_experiments.py --n-jobs -1
python src/at_risk_model.py train --cutoff 105 --n-jobs -1
python src/at_risk_model.py validate
python -m unittest discover -s tests -v
```

`validate` tái tính metric từ `model_predictions.csv`, đối chiếu `model_metrics.csv`, confusion matrix, khoảng tin cậy, split và SHA-256. Nó tạo `model_verification.csv` và chỉ PASS khi đồng thời đạt:

| Điều kiện | Ngưỡng | Kết quả hiện tại |
|---|---:|---:|
| Test Accuracy | ≥ 0,80 | 0,8270 |
| Cận dưới 95% của Accuracy | ≥ 0,80 | 0,8146 |
| Recall At-Risk | ≥ 0,70 | 0,7349 |
| F1 At-Risk | ≥ 0,74 | 0,7672 |
| PR-AUC | ≥ 0,85 | 0,8701 |
| Brier | ≤ 0,15 | 0,1237 |
| Accuracy cao hơn dummy | ≥ 0,15 | 0,2148 |
| Accuracy thấp nhất theo presentation | ≥ 0,80 | 0,8187 |
| SHA-256 artifact | Khớp metadata | PASS |

Kết quả local hiện tại: `MODEL_OUTPUT_VALIDATION=PASS`; 9/9 verification check và 9/9 unit test pass. Nếu sửa code/data rồi chạy lại, bất kỳ điều kiện nào không đạt sẽ làm lệnh trả lỗi và ghi rõ dòng FAIL trong `model_verification.csv`.

## Giới hạn và ranh giới nghiệm thu

- Đây là dự báo trên dữ liệu quan sát lịch sử, không phải quan hệ nhân quả hoặc chẩn đoán cá nhân.
- Coverage assessment khác nhau giữa module/presentation; kết quả phụ thuộc cutoff.
- Test split đã được xem ở các vòng cải tiến cutoff 98/105, vì vậy không được gọi đây là test hoàn toàn nguyên sơ. Cần holdout mới theo thời gian/presentation hoặc dữ liệu ngoài OULAD để xác nhận độc lập mạnh hơn.
- Có code, output và metric local không tự động đồng nghĩa model đã nghiệm thu. Chỉ commit/push sau khi chủ dự án duyệt code, lệnh tái tạo, metric, leakage checklist, cutoff/threshold và contract dashboard Python.

## Related Work (Trích dẫn ban đầu)

Tài liệu tham khảo dự kiến (theo chuẩn IEEE) phục vụ cho phần phân tích Learning Analytics:
[1] J. Kuzilek, M. Hlosta, and Z. Zdrahal, "Open university learning analytics dataset," *Scientific Data*, vol. 4, no. 1, p. 170171, 2017. [Online]. Available: https://www.nature.com/articles/sdata2017171. (Mô tả chi tiết OULAD).
[2] M. Hlosta, Z. Zdrahal, and J. Zendulka, "Ouroboros: early identification of at-risk students without models based on legacy data," in *Proceedings of the Seventh International Learning Analytics & Knowledge Conference*, 2017, pp. 6-15. (Cách xác định rủi ro sớm).
[3] A. F. Wise, "Designing pedagogical interventions to support student use of learning analytics," *Proceedings of the Sixth International Conference on Learning Analytics & Knowledge*, 2016, pp. 203-211. (Giá trị của tương tác VLE đối với kết quả học tập).
[4] G. Siemens and R. S. d. Baker, "Learning analytics and educational data mining: towards communication and collaboration," *Proceedings of the 2nd International Conference on Learning Analytics and Knowledge*, 2012, pp. 252-254. (Nền tảng của phân tích học tập dựa trên dữ liệu hệ thống).
