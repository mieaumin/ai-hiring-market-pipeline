"""Initialize runtime company discovery templates."""

from __future__ import annotations

from pathlib import Path
from shutil import copyfile


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    targets = {
        ROOT / "configs/company_candidates.csv": ROOT / "runtime/company_candidates.csv",
        ROOT / "configs/company_evidence.csv": ROOT / "runtime/company_evidence.csv",
    }
    for source, target in targets.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        copyfile(source, target)
        print(f"Initialized {target}")


if __name__ == "__main__":
    main()

