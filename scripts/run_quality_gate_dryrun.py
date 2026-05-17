"""Run a local quality gate dry run against data/raw/raw_jds.csv.

This script does not collect or fetch data. It only evaluates local rows if any
exist and writes valid rows to staging plus invalid rows to validation errors.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.processing.jd_quality_gate import split_rows_by_quality_gate
from src.utils.template_schemas import JD_COLUMNS, JD_VALIDATION_ERRORS_COLUMNS


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_error_rows(records: list[dict]) -> list[dict]:
    checked_at = datetime.now(timezone.utc).isoformat()
    errors = []
    for index, record in enumerate(records, start=1):
        errors.append(
            {
                "error_id": f"jd_validation_error_{index:05d}",
                "jd_id": record.get("jd_id", ""),
                "source_id": record.get("source_id", ""),
                "job_url": record.get("job_url", ""),
                "error_type": "quality_gate_failed",
                "error_reason": record.get("failure_reason", ""),
                "detected_at": checked_at,
                "review_status": "not_reviewed",
                "notes": "",
            }
        )
    return errors


def main() -> int:
    raw_path = ROOT / "data/raw/raw_jds.csv"
    staging_path = ROOT / "staging/jd_staging.csv"
    errors_path = ROOT / "runtime/jd_validation_errors.csv"

    rows = read_rows(raw_path)
    if not rows:
        write_rows(staging_path, JD_COLUMNS, [])
        write_rows(errors_path, JD_VALIDATION_ERRORS_COLUMNS, [])
        print("No raw JD rows found. Quality gate skipped safely.")
        return 0

    valid_rows, invalid_rows = split_rows_by_quality_gate(rows)
    write_rows(staging_path, JD_COLUMNS, valid_rows)
    write_rows(errors_path, JD_VALIDATION_ERRORS_COLUMNS, build_error_rows(invalid_rows))

    print(f"Quality gate dry run: {len(valid_rows)}/{len(rows)} rows passed.")
    print(f"Valid rows written to {staging_path.relative_to(ROOT)}")
    print(f"Failed rows written to {errors_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
