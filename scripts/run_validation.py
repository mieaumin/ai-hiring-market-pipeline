"""Validate local cleaned JD rows using MVP rules."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.processing.validator import validate_jd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    path = ROOT / "data/cleaned/cleaned_jds.csv"
    if not path.exists():
        print(f"No cleaned JD file found: {path}")
        return

    df = pd.read_csv(path).fillna("")
    if df.empty:
        print("No cleaned JD rows to validate.")
        return

    results = [validate_jd(row) for row in df.to_dict(orient="records")]
    valid_count = sum(1 for is_valid, _ in results if is_valid)
    print(f"Validated {len(results)} rows. Valid rows: {valid_count}")


if __name__ == "__main__":
    main()

