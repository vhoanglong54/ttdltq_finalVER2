"""Verify the local OULAD source files for task T01.

Example:
    python src/verify_oulad_source.py data/raw

The script streams every CSV, so it can count the large studentVle.csv file
without loading it into memory. It does not modify source data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path


EXPECTED_COLUMNS = {
    "assessments.csv": ["code_module", "code_presentation", "id_assessment"],
    "courses.csv": ["code_module", "code_presentation"],
    "studentAssessment.csv": ["id_assessment", "id_student"],
    "studentInfo.csv": [
        "code_module",
        "code_presentation",
        "id_student",
        "final_result",
        "region",
    ],
    "studentRegistration.csv": ["code_module", "code_presentation", "id_student"],
    "studentVle.csv": [
        "code_module",
        "code_presentation",
        "id_student",
        "id_site",
        "date",
    ],
    "vle.csv": ["id_site", "code_module", "code_presentation"],
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_csv(path: Path) -> tuple[list[str], int]:
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"{path.name} is empty") from exc
        return header, sum(1 for _ in reader)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw_dir", type=Path, help="Directory containing the 7 OULAD CSV files")
    args = parser.parse_args()

    raw_dir = args.raw_dir
    failed = False
    total_rows = 0
    print("# T01 local OULAD source verification")
    print()
    print("| File | Rows | Columns | SHA-256 | Required header test |")
    print("|---|---:|---:|---|---|")

    for filename, required_columns in EXPECTED_COLUMNS.items():
        path = raw_dir / filename
        if not path.is_file():
            print(f"| `{filename}` | — | — | — | FAIL: file missing |")
            failed = True
            continue

        header, rows = inspect_csv(path)
        total_rows += rows
        missing = [column for column in required_columns if column not in header]
        header_test = "PASS" if not missing else f"FAIL: missing {', '.join(missing)}"
        failed = failed or bool(missing)
        print(f"| `{filename}` | {rows:,} | {len(header)} | `{sha256(path)}` | {header_test} |")

    print()
    print(f"- Expected CSV files: {len(EXPECTED_COLUMNS)}")
    print(f"- CSV rows across all seven files: {total_rows:,}")
    print(f"- Dataset size rule (at least 5,000 rows): {'PASS' if total_rows >= 5000 else 'FAIL'}")
    print("- Join-key evidence: required join columns are tested by the table above; uniqueness, cardinality and unmatched-row tests belong to T02/T05/T07.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
