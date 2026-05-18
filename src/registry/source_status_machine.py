"""Source status transition helpers."""

from __future__ import annotations

from src.standards.status_validator import validate_status_value, validate_transition


def validate_source_approval_status(status: str):
    """Validate source approval status."""
    return validate_status_value("source_approval_status", status)


def can_transition_source_approval(current_status: str, next_status: str):
    """Validate source approval status transition."""
    return validate_transition("source_approval_status", current_status, next_status)


def can_transition_site_review(current_status: str, next_status: str):
    """Validate site review status transition."""
    return validate_transition("site_review_status", current_status, next_status)
