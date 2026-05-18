"""Source promotion and collection eligibility decisions."""

from __future__ import annotations

from src.registry.collection_guard import explain_blocking_reason, is_source_collectable
from src.standards.classification_loader import DecisionResult
from src.standards.promotion_validator import validate_site_screening_to_master


def validate_source_master_promotion(row: dict) -> DecisionResult:
    """Validate source promotion to master registry."""
    return validate_site_screening_to_master(row)


def validate_source_collection(row: dict) -> DecisionResult:
    """Validate approved-source-only collection eligibility."""
    blockers = explain_blocking_reason(row)
    return DecisionResult(
        decision="collect" if not blockers else "skip",
        allowed=not blockers and is_source_collectable(row),
        reasons=["source passed approved-source collection guard"] if not blockers else [],
        blockers=blockers,
        confidence="high" if not blockers else "medium",
    )
