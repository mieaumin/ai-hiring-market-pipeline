"""JD staging helpers."""

from __future__ import annotations

from src.processing.deduplicator import deduplicate
from src.processing.jd_quality_gate import evaluate_quality_gate


def build_staging_rows(records: list[dict]) -> list[dict]:
    """Return records that pass the quality gate, deduplicated by key."""
    unique_records = deduplicate(records)
    staged = []
    for record in unique_records:
        result = evaluate_quality_gate(record)
        if result.passed:
            row = dict(record)
            row["validation_status"] = "valid"
            row["quality_score"] = result.quality_score
            staged.append(row)
    return staged

