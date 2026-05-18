"""JD promotion validation helpers."""

from __future__ import annotations

from src.standards.promotion_validator import validate_jd_to_master


def validate_jd_master_promotion(row: dict):
    """Validate JD staging to master promotion."""
    return validate_jd_to_master(row)
