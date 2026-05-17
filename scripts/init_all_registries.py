"""Initialize all known registry and JD CSV templates.

This script is safe: it creates missing header-only CSV files and never performs
network access or live collection.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.template_schemas import TEMPLATE_FILES, write_header_if_missing


def main() -> None:
    for relative_path, columns in TEMPLATE_FILES.items():
        path = ROOT / relative_path
        created = write_header_if_missing(path, columns)
        status = "created" if created else "exists"
        print(f"{status}: {relative_path}")


if __name__ == "__main__":
    main()

