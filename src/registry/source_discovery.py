"""Source discovery schema helpers.

No live source discovery is implemented here.
"""

from __future__ import annotations

from src.utils.template_schemas import SOURCE_REGISTRY_COLUMNS


def validate_source_discovery_columns(columns: list[str]) -> list[str]:
    """Return missing required source discovery columns."""
    return [column for column in SOURCE_REGISTRY_COLUMNS if column not in columns]


def build_empty_source_record() -> dict:
    """Return an empty source record using the canonical source schema."""
    return {column: "" for column in SOURCE_REGISTRY_COLUMNS}

