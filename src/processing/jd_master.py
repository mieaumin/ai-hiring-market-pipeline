"""JD master promotion helpers."""

from __future__ import annotations

from src.processing.jd_quality_gate import evaluate_quality_gate


def can_promote_to_master(record: dict) -> bool:
    """Return True when a staged JD can move to master."""
    return evaluate_quality_gate(record).passed and record.get("validation_status") in {"valid", "approved"}


def promote_rows(records: list[dict]) -> list[dict]:
    """Return rows eligible for master dataset promotion."""
    return [record for record in records if can_promote_to_master(record)]

