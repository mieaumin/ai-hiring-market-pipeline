"""Run a local quality gate dry run against staging/jd_staging.csv.

This script does not collect or fetch data. It only evaluates local rows if any
exist.
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.processing.jd_quality_gate import evaluate_quality_gate


def main() -> int:
    path = ROOT / "staging/jd_staging.csv"
    if not path.exists():
        print(f"No staging file found: {path.relative_to(ROOT)}")
        return 1

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if not rows:
        print("No JD rows found. Dry run passed for header-only template.")
        return 0

    passed = 0
    for row in rows:
        result = evaluate_quality_gate(row)
        if result.passed:
            passed += 1
        print(f"{row.get('jd_id', '<missing jd_id>')}: {result.status} {result.reasons}")

    print(f"Quality gate dry run: {passed}/{len(rows)} rows passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

