"""Taxonomy loading helpers."""

from __future__ import annotations

from pathlib import Path

import yaml


DEFAULT_TAXONOMY_PATH = Path("configs/taxonomy_v1.yaml")


def load_taxonomy(path: str | Path = DEFAULT_TAXONOMY_PATH) -> dict:
    """Load taxonomy YAML."""
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

