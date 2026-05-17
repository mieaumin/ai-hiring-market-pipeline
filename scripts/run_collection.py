"""Compatibility wrapper for approved-source-only collection."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_approved_collection import main as run_approved_collection


def main() -> int:
    return run_approved_collection()


if __name__ == "__main__":
    raise SystemExit(main())
