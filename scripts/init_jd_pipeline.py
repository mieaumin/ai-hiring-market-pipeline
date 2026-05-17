"""Initialize JD pipeline CSV templates without collection."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.template_schemas import (
    JD_COLLECTION_LOG_COLUMNS,
    JD_COLUMNS,
    JD_VALIDATION_ERRORS_COLUMNS,
    QUALITY_GATE_REPORT_COLUMNS,
    write_header_if_missing,
)


def main() -> None:
    targets = {
        ROOT / "runtime/raw_jd_collection.csv": JD_COLUMNS,
        ROOT / "data/raw/raw_jds.csv": JD_COLUMNS,
        ROOT / "data/cleaned/cleaned_jds.csv": JD_COLUMNS,
        ROOT / "data/labeled/labeled_jds.csv": JD_COLUMNS,
        ROOT / "staging/jd_staging.csv": JD_COLUMNS,
        ROOT / "master/jd_master_dataset.csv": JD_COLUMNS,
        ROOT / "runtime/jd_collection_log.csv": JD_COLLECTION_LOG_COLUMNS,
        ROOT / "runtime/jd_validation_errors.csv": JD_VALIDATION_ERRORS_COLUMNS,
        ROOT / "runtime/quality_gate_report.csv": QUALITY_GATE_REPORT_COLUMNS,
    }
    for path, columns in targets.items():
        created = write_header_if_missing(path, columns)
        status = "created" if created else "exists"
        print(f"{status}: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
