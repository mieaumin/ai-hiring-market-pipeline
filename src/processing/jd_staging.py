"""JD staging helpers."""

from __future__ import annotations

from src.processing.deduplicator import deduplicate
from src.processing.jd_quality_gate import split_rows_by_quality_gate


def build_staging_rows(records: list[dict]) -> list[dict]:
    """Return records that pass the quality gate, deduplicated by key."""
    unique_records = deduplicate(records)
    staged, _errors = split_rows_by_quality_gate(unique_records)
    return staged
