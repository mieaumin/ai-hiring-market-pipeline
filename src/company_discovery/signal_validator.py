"""Validation helpers for company discovery signals."""

from __future__ import annotations

VALID_SIGNAL_CATEGORIES = {
    "hiring_signal",
    "business_ai_signal",
    "tech_signal",
    "market_signal",
    "evidence_quality",
}

VALIDATION_STATUSES = {
    "seeded",
    "needs_review",
    "candidate",
    "approved_for_source_discovery",
    "rejected",
}


def is_valid_signal_category(signal_category: str) -> bool:
    """Return True when a signal category belongs to the MVP schema."""
    return signal_category in VALID_SIGNAL_CATEGORIES


def is_valid_validation_status(status: str) -> bool:
    """Return True when a validation status belongs to the MVP schema."""
    return status in VALIDATION_STATUSES


def validate_evidence_row(row: dict) -> tuple[bool, str]:
    """Validate the minimum fields needed for a company evidence row."""
    required_fields = ("evidence_id", "company_id", "signal_category", "evidence_url")
    missing = [field for field in required_fields if not row.get(field)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    if not is_valid_signal_category(row["signal_category"]):
        return False, f"Invalid signal_category: {row['signal_category']}"
    return True, "ok"

