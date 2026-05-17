"""Validate required CSV template columns.

This script is safe: it reads local headers only and never performs network
access or live data collection.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.template_schemas import TEMPLATE_FILES, missing_columns


def main() -> int:
    failures = []
    for relative_path, required_columns in TEMPLATE_FILES.items():
        path = ROOT / relative_path
        missing = missing_columns(path, required_columns)
        if missing:
            failures.append((relative_path, missing))
            print(f"FAIL: {relative_path} missing {missing}")
        else:
            print(f"OK: {relative_path}")

    if failures:
        print(f"Validation failed for {len(failures)} template(s).")
        return 1
    print("All pipeline templates contain required columns.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

