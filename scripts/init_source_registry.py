"""Initialize a local source registry CSV from the template."""

from __future__ import annotations

from pathlib import Path
from shutil import copyfile


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = ROOT / "configs/source_registry_template.csv"
    target = ROOT / "runtime/source_registry.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    copyfile(source, target)
    print(f"Initialized {target}")


if __name__ == "__main__":
    main()

