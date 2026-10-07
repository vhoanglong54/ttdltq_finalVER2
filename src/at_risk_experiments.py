"""Compare Logistic Regression improvements without inspecting the test set.

This script reuses the frozen learner-group split from ``feature_snapshot.csv``.
It tunes each candidate only on train folds, chooses its classification
threshold only on validation, and never computes test metrics.  Its output is
an experiment log, not a final model artifact.

Example:
    python src/at_risk_experiments.py --n-jobs -1
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    KBinsDiscretizer,
    OneHotEncoder,
    PolynomialFeatures,
    SplineTransformer,
    StandardScaler,
)

from at_risk_features import (
    CORE_MODEL_NUMERIC_FEATURES,
    ENGINEERED_NUMERIC_FEATURES as ENGINEERED_NUMERIC,
    MODEL_CATEGORICAL_FEATURES,
    MODEL_INTERACTION_FEATURES,
    MODULE_CODES,
    MODULE_SLOPE_BASES,
    MODULE_SLOPE_FEATURES,
    WEIGHTED_PROGRESS_FEATURES as WEIGHTED_PROGRESS_NUMERIC,
)
from at_risk_model import choose_threshold, evaluate_predictions


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = ROOT / "data" / "processed" / "model" / "feature_snapshot.csv"
DEFAULT_OUTPUT = (
    ROOT / "data" / "processed" / "model" / "logistic_variant_experiments.csv"
)

SAFE_EXTRA_NUMERIC = [
    "assessment_score_min_cutoff",
    "assessment_score_max_cutoff",
    "assessment_type_count_cutoff",
    "vle_first_activity_day",
]
BASELINE_CATEGORICAL = [
    feature
    for feature in MODEL_CATEGORICAL_FEATURES
    if feature != "module_presentation"
]
BASELINE_NUMERIC = [
    feature
    for feature in CORE_MODEL_NUMERIC_FEATURES
    if feature not in SAFE_EXTRA_NUMERIC
]

SPLINE_FEATURES = [
    "assessment_weighted_score_cutoff",
    "assessment_completion_rate_cutoff",
    "assessment_days_since_last_submission",
    "log1p_vle_total_clicks_cutoff",
    "log1p_vle_clicks_last_28_days",
    "vle_active_days_last_28_days",
    "vle_days_since_last_activity",
]

BIN_FEATURES = [
    "assessment_weighted_score_cutoff",
    "assessment_completion_rate_cutoff",
    "assessment_days_since_last_submission",
    "log1p_vle_total_clicks_cutoff",
    "log1p_vle_clicks_last_28_days",
    "vle_active_day_rate_cutoff",
    "vle_days_since_last_activity",
    "num_of_prev_attempts",
]

@dataclass(frozen=True)
class Variant:
    name: str
    add_safe_extras: bool = False
    add_module_presentation: bool = False
    add_splines: bool = False
    add_interactions: bool = False
    add_engineered: bool = False
    add_bins: bool = False
    add_module_slopes: bool = False
    add_weighted_progress: bool = False


VARIANTS = (
    Variant("v2_baseline"),
    Variant(
        "safe_extras_module_presentation",
        add_safe_extras=True,
        add_module_presentation=True,
    ),
    Variant(
        "safe_extras_module_presentation_splines",
        add_safe_extras=True,
        add_module_presentation=True,
        add_splines=True,
    ),
    Variant(
        "safe_extras_module_presentation_interactions",
        add_safe_extras=True,
        add_module_presentation=True,
        add_interactions=True,
    ),
    Variant(
        "engineered_interactions",
        add_safe_extras=True,
        add_module_presentation=True,
        add_interactions=True,
        add_engineered=True,
    ),
    Variant(
        "engineered_interactions_bins",
        add_safe_extras=True,
        add_module_presentation=True,
        add_interactions=True,
        add_engineered=True,
        add_bins=True,
    ),
    Variant(
        "module_slopes_interactions",
        add_safe_extras=True,
        add_module_presentation=True,
        add_interactions=True,
        add_module_slopes=True,
    ),
    Variant(
        "module_slopes_engineered_interactions",
        add_safe_extras=True,
        add_module_presentation=True,
        add_interactions=True,
        add_engineered=True,
        add_module_slopes=True,
    ),
    Variant(
        "weighted_progress_interactions",
        add_safe_extras=True,
        add_module_presentation=True,
        add_interactions=True,
        add_weighted_progress=True,
    ),
    Variant(
        "weighted_progress_module_slopes",
        add_safe_extras=True,
        add_module_presentation=True,
        add_interactions=True,
        add_engineered=True,
        add_module_slopes=True,
        add_weighted_progress=True,
    ),
)


def add_engineered_features(snapshot: pd.DataFrame) -> pd.DataFrame:
    """Add leakage-safe ratios that are fully observable at the cutoff."""
    frame = snapshot.copy()
    cutoff = frame["cutoff_day"].astype(float)
    registration_start = frame["date_registration"].fillna(0).clip(lower=0)
    registration_start = np.minimum(registration_start, cutoff)
    frame["days_observed_at_cutoff"] = (cutoff - registration_start + 1).clip(lower=1)
    frame["vle_active_day_rate_cutoff"] = (
        frame["vle_active_days_cutoff"] / frame["days_observed_at_cutoff"]
    ).clip(0, 1)
    frame["log1p_vle_clicks_per_active_day"] = np.log1p(
        frame["vle_clicks_per_active_day"].clip(lower=0)
    )
    frame["vle_recent_28_click_share"] = np.where(
        frame["vle_total_clicks_cutoff"].gt(0),
        frame["vle_clicks_last_28_days"] / frame["vle_total_clicks_cutoff"],
        0.0,
    )
    frame["vle_recent_7_click_share"] = np.where(
        frame["vle_clicks_last_28_days"].gt(0),
        frame["vle_clicks_last_7_days"] / frame["vle_clicks_last_28_days"],
        0.0,
    )
    frame["vle_active_day_change_28d"] = (
        frame["vle_active_days_last_28_days"]
        - frame["vle_active_days_previous_28_days"]
    ) / 28.0
    frame["assessment_missed_due_count"] = (
        frame["assessment_due_count"]
        - frame["assessment_due_submission_count_cutoff"]
    ).clip(lower=0)
    frame["assessment_on_time_rate_cutoff"] = np.where(
        frame["assessment_submission_count_cutoff"].gt(0),
        1.0
        - frame["assessment_late_count_cutoff"]
        / frame["assessment_submission_count_cutoff"],
        np.nan,
    )
    module_slopes = {
        f"module_{module}_x_{feature}": np.where(
            frame["code_module"].eq(module), frame[feature], 0.0
        )
        for module in MODULE_CODES
        for feature in MODULE_SLOPE_BASES
    }
    frame = pd.concat(
        [frame.drop(columns=list(module_slopes), errors="ignore"),
         pd.DataFrame(module_slopes, index=frame.index)],
        axis=1,
    )
    return frame


def build_candidate(
    variant: Variant, solver: str = "liblinear"
) -> tuple[Pipeline, list[str]]:
    """Build a Logistic Regression candidate and return its input columns."""
    categorical = list(BASELINE_CATEGORICAL)
    numeric = list(BASELINE_NUMERIC)
    if variant.add_safe_extras:
        numeric.extend(SAFE_EXTRA_NUMERIC)
    if variant.add_module_presentation:
        categorical.append("module_presentation")
    if variant.add_engineered:
        numeric.extend(ENGINEERED_NUMERIC)
    if variant.add_module_slopes:
        numeric.extend(MODULE_SLOPE_FEATURES)
    if variant.add_weighted_progress:
        numeric.extend(WEIGHTED_PROGRESS_NUMERIC)

    numeric_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    transformers: list[tuple[str, Pipeline, list[str]]] = [
        ("numeric", numeric_pipeline, numeric),
        ("categorical", categorical_pipeline, categorical),
    ]

    if variant.add_splines:
        spline_pipeline = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "spline",
                    SplineTransformer(
                        n_knots=4,
                        degree=2,
                        knots="quantile",
                        include_bias=False,
                    ),
                ),
                ("scaler", StandardScaler()),
            ]
        )
        transformers.append(("splines", spline_pipeline, SPLINE_FEATURES))

    if variant.add_interactions:
        interaction_pipeline = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "interactions",
                    PolynomialFeatures(
                        degree=(2, 2), interaction_only=True, include_bias=False
                    ),
                ),
            ]
        )
        transformers.append(
            ("pairwise_interactions", interaction_pipeline, MODEL_INTERACTION_FEATURES)
        )

    if variant.add_bins:
        bin_pipeline = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "bins",
                    KBinsDiscretizer(
                        n_bins=6,
                        encode="onehot",
                        strategy="quantile",
                        subsample=None,
                    ),
                ),
            ]
        )
        transformers.append(("quantile_bins", bin_pipeline, BIN_FEATURES))

    preprocessing = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        sparse_threshold=1.0,
    )
    estimator = Pipeline(
        [
            ("preprocessing", preprocessing),
            (
                "model",
                LogisticRegression(
                    solver=solver,
                    max_iter=5_000,
                    tol=1e-3 if solver == "saga" else 1e-4,
                    random_state=42,
                ),
            ),
        ]
    )
    return estimator, categorical + numeric


def run(args: argparse.Namespace) -> None:
    snapshot = add_engineered_features(pd.read_csv(args.snapshot))
    snapshot["module_presentation"] = (
        snapshot["code_module"].astype(str)
        + "_"
        + snapshot["code_presentation"].astype(str)
    )

    train = snapshot["dataset_split"].eq("train")
    validation = snapshot["dataset_split"].eq("validation")
    if not train.any() or not validation.any():
        raise ValueError("Snapshot must contain frozen train and validation splits.")

    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=44)
    scoring = {
        "pr_auc": "average_precision",
        "roc_auc": "roc_auc",
        "precision": make_scorer(precision_score, zero_division=0),
        "recall": make_scorer(recall_score, zero_division=0),
        "f1": make_scorer(f1_score, zero_division=0),
    }
    rows: list[dict[str, object]] = []

    selected_variants = [
        variant for variant in VARIANTS if not args.variants or variant.name in args.variants
    ]
    if not selected_variants:
        raise ValueError("No matching variants were selected.")

    for variant in selected_variants:
        print(f"Running {variant.name} ...", flush=True)
        solver = "saga" if args.elastic_net else "liblinear"
        estimator, columns = build_candidate(variant, solver=solver)
        if args.fixed_c is not None:
            c_grid = [args.fixed_c]
        elif args.elastic_net:
            c_grid = [0.1, 0.3, 1.0]
        else:
            c_grid = (
                [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
                if args.fine_grid
                else [0.1, 1.0, 10.0]
            )
        if args.fixed_l1_ratio is not None:
            l1_ratios = [args.fixed_l1_ratio]
        elif args.elastic_net:
            l1_ratios = [0.25, 0.5, 0.75]
        else:
            l1_ratios = [0.0, 1.0]
        search = GridSearchCV(
            estimator,
            param_grid={
                "model__C": c_grid,
                # scikit-learn 1.8 deprecates ``penalty``; l1_ratio=0/1 is
                # respectively L2/L1 regularization for this estimator.
                "model__l1_ratio": l1_ratios,
                "model__class_weight": [None] if args.fixed_c is not None else [None, "balanced"],
            },
            scoring=scoring,
            refit="pr_auc",
            cv=cv,
            n_jobs=args.n_jobs,
            return_train_score=False,
        )
        search.fit(
            snapshot.loc[train, columns],
            snapshot.loc[train, "At_Risk"].astype(int),
            groups=snapshot.loc[train, "id_student"],
        )
        validation_probability = search.best_estimator_.predict_proba(
            snapshot.loc[validation, columns]
        )[:, 1]
        threshold, _ = choose_threshold(
            snapshot.loc[validation, "At_Risk"].astype(int).to_numpy(),
            validation_probability,
            args.minimum_recall,
        )
        metrics = evaluate_predictions(
            snapshot.loc[validation, "At_Risk"].astype(int).to_numpy(),
            validation_probability,
            threshold,
        )
        transformed_features = search.best_estimator_.named_steps[
            "preprocessing"
        ].get_feature_names_out()
        row = {
            "variant": variant.name,
            "selection_data": "train_cv_and_validation_only",
            "best_cv_pr_auc": float(search.best_score_),
            "best_C": search.best_params_["model__C"],
            "best_regularization": (
                "L1"
                if search.best_params_["model__l1_ratio"] == 1.0
                else (
                    "L2"
                    if search.best_params_["model__l1_ratio"] == 0.0
                    else f"ElasticNet({search.best_params_['model__l1_ratio']:.2f})"
                )
            ),
            "best_class_weight": search.best_params_["model__class_weight"],
            "input_feature_count": len(columns),
            "transformed_feature_count": len(transformed_features),
            **{f"validation_{key}": value for key, value in metrics.items()},
        }
        rows.append(row)
        print(
            f"{variant.name}: cv_pr_auc={row['best_cv_pr_auc']:.4f}; "
            f"validation_accuracy={row['validation_accuracy']:.4f}; "
            f"validation_recall={row['validation_recall_at_risk']:.4f}; "
            f"threshold={row['validation_threshold']:.3f}",
            flush=True,
        )

    results = pd.DataFrame(rows).sort_values(
        ["best_cv_pr_auc", "validation_accuracy"], ascending=False
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output, index=False)
    print("\nComparison (test set not inspected):")
    print(
        results[
            [
                "variant",
                "best_cv_pr_auc",
                "validation_accuracy",
                "validation_recall_at_risk",
                "validation_f1_at_risk",
                "validation_roc_auc",
                "validation_pr_auc",
                "validation_threshold",
            ]
        ].to_string(index=False)
    )
    print(f"Experiment log written to {output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", default=str(DEFAULT_SNAPSHOT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--minimum-recall", type=float, default=0.75)
    parser.add_argument("--n-jobs", type=int, default=-1)
    parser.add_argument(
        "--fine-grid",
        action="store_true",
        help="Use a denser C grid for shortlisted candidates.",
    )
    parser.add_argument(
        "--elastic-net",
        action="store_true",
        help="Use the SAGA solver and search Elastic Net mixing ratios.",
    )
    parser.add_argument(
        "--fixed-c",
        type=float,
        help="Evaluate one preselected C value; useful for a fair threshold audit.",
    )
    parser.add_argument(
        "--fixed-l1-ratio",
        type=float,
        choices=[0.0, 0.25, 0.5, 0.75, 1.0],
        help="Evaluate one preselected regularization mix.",
    )
    parser.add_argument(
        "--variants",
        nargs="*",
        choices=[variant.name for variant in VARIANTS],
        help="Optional subset of variants; default runs every candidate.",
    )
    return parser


if __name__ == "__main__":
    run(build_parser().parse_args())
