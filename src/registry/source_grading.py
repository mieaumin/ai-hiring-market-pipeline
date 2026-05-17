"""Strict source grading and promotion rules.

This module is schema/policy logic only. It does not perform network access.
"""

from __future__ import annotations

from dataclasses import dataclass


APPROVAL_STATUS_VALUES = {"not_required", "pending", "approved", "rejected", "expired"}
SOURCE_GRADES = {"A", "B", "C", "D", "E", "F"}


@dataclass(frozen=True)
class SourceGradePolicy:
    grade: str
    manual_review_required: bool
    human_approval_required: bool
    default_approval_status: str
    use_policy: str


SOURCE_GRADE_POLICIES = {
    "A": SourceGradePolicy(
        grade="A",
        manual_review_required=False,
        human_approval_required=False,
        default_approval_status="not_required",
        use_policy="usable after basic automated checks",
    ),
    "B": SourceGradePolicy(
        grade="B",
        manual_review_required=True,
        human_approval_required=True,
        default_approval_status="pending",
        use_policy="requires human review before use",
    ),
    "C": SourceGradePolicy(
        grade="C",
        manual_review_required=True,
        human_approval_required=True,
        default_approval_status="pending",
        use_policy="requires human review and explicit approval before use",
    ),
    "D": SourceGradePolicy(
        grade="D",
        manual_review_required=True,
        human_approval_required=True,
        default_approval_status="pending",
        use_policy="approval pending / manual approval required",
    ),
    "E": SourceGradePolicy(
        grade="E",
        manual_review_required=True,
        human_approval_required=True,
        default_approval_status="rejected",
        use_policy="avoid in MVP",
    ),
    "F": SourceGradePolicy(
        grade="F",
        manual_review_required=False,
        human_approval_required=False,
        default_approval_status="rejected",
        use_policy="prohibited",
    ),
}


def normalize_grade(value: str | None) -> str:
    """Normalize source grade values to uppercase."""
    return (value or "").strip().upper()


def normalize_status(value: str | None) -> str:
    """Normalize approval status values."""
    return (value or "").strip().lower()


def get_grade_policy(source_grade: str) -> SourceGradePolicy:
    """Return policy for a source grade."""
    grade = normalize_grade(source_grade)
    if grade not in SOURCE_GRADE_POLICIES:
        raise ValueError(f"Unknown source grade: {source_grade}")
    return SOURCE_GRADE_POLICIES[grade]


def default_approval_status(source_grade: str) -> str:
    """Return default approval status for a grade."""
    return get_grade_policy(source_grade).default_approval_status


def requires_human_approval(source_grade: str) -> bool:
    """Return whether a grade requires human approval."""
    return get_grade_policy(source_grade).human_approval_required


def can_move_to_master(row: dict, automated_checks_passed: bool = False) -> bool:
    """Return True when a source row can move to source registry master."""
    grade = normalize_grade(row.get("source_grade"))
    status = normalize_status(row.get("approval_status"))

    if grade == "A":
        return automated_checks_passed and status in {"", "not_required"}
    if grade in {"B", "C", "D"}:
        return status == "approved"
    if grade in {"E", "F"}:
        return False
    return False


def validate_source_approval_fields(row: dict) -> tuple[bool, str]:
    """Validate grade and approval status fields for a source row."""
    grade = normalize_grade(row.get("source_grade"))
    status = normalize_status(row.get("approval_status"))

    if grade not in SOURCE_GRADES:
        return False, "invalid_source_grade"
    if status not in APPROVAL_STATUS_VALUES:
        return False, "invalid_approval_status"

    policy = get_grade_policy(grade)
    human_required = str(row.get("human_approval_required", "")).strip().lower()
    expected_human_required = str(policy.human_approval_required).lower()
    if human_required and human_required != expected_human_required:
        return False, "human_approval_required_mismatch"

    return True, "ok"

