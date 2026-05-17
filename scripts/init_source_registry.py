"""Initialize source registry templates without live collection."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.template_schemas import SOURCE_POLICY_EVIDENCE_COLUMNS, SOURCE_REGISTRY_COLUMNS, write_header_if_missing


def main() -> None:
    targets = {
        ROOT / "configs/source_registry_template.csv": SOURCE_REGISTRY_COLUMNS,
        ROOT / "runtime/source_discovery.csv": SOURCE_REGISTRY_COLUMNS,
        ROOT / "runtime/source_verification.csv": SOURCE_REGISTRY_COLUMNS,
        ROOT / "staging/source_registry_staging.csv": SOURCE_REGISTRY_COLUMNS,
        ROOT / "master/source_registry_master.csv": SOURCE_REGISTRY_COLUMNS,
        ROOT / "runtime/source_policy_evidence.csv": SOURCE_POLICY_EVIDENCE_COLUMNS,
    }
    for path, columns in targets.items():
        created = write_header_if_missing(path, columns)
        status = "created" if created else "exists"
        print(f"{status}: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
