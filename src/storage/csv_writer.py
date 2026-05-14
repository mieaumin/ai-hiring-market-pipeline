"""CSV writing helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_csv(records: list[dict], path: str | Path) -> None:
    """Write records to CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(path, index=False)


def append_csv(records: list[dict], path: str | Path) -> None:
    """Append records to CSV, writing a header only for new files."""
    if not records:
        return
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()
    pd.DataFrame(records).to_csv(path, mode="a", header=not file_exists, index=False)

