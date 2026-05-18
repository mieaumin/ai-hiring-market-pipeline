"""JD validation status helpers."""

from __future__ import annotations

from src.standards.status_validator import validate_status_value, validate_transition


def validate_jd_validation_status(status: str):
    """Validate JD validation status."""
    return validate_status_value("jd_validation_status", status)


def can_transition_jd_validation(current_status: str, next_status: str):
    """Validate JD validation status transition."""
    return validate_transition("jd_validation_status", current_status, next_status)
