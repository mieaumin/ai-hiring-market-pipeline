"""Company signal status helpers."""

from __future__ import annotations

from src.standards.classification_loader import validate_classification_value


ALLOWED_COMPANY_SIGNAL_TRANSITIONS = {
    "seeded": {"discovered", "evidence_collected", "needs_review", "rejected"},
    "discovered": {"evidence_collected", "needs_review", "rejected"},
    "evidence_collected": {"scored", "needs_review", "rejected"},
    "scored": {"approved_for_source_discovery", "needs_review", "rejected"},
    "needs_review": {"evidence_collected", "scored", "approved_for_source_discovery", "rejected"},
    "approved_for_source_discovery": {"needs_review", "rejected"},
    "rejected": set(),
}


def validate_company_signal_status(status: str):
    """Validate company signal status."""
    return validate_classification_value("company_signal_status", status)


def can_transition_company_signal(current_status: str, next_status: str):
    """Validate a company signal status transition."""
    current = str(current_status or "").strip()
    next_value = str(next_status or "").strip()
    current_result = validate_company_signal_status(current)
    next_result = validate_company_signal_status(next_value)
    if not current_result.allowed:
        return current_result
    if not next_result.allowed:
        return next_result
    allowed = next_value in ALLOWED_COMPANY_SIGNAL_TRANSITIONS.get(current, set())
    return current_result.__class__(
        decision="transition_allowed" if allowed else "transition_blocked",
        allowed=allowed,
        reasons=[f"company_signal_status:{current}->{next_value}"] if allowed else [],
        blockers=[] if allowed else ["invalid_company_signal_transition"],
        confidence="high",
    )
