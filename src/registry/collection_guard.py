"""Approved-source-only collection guard.

This module performs local registry checks only. It does not fetch robots.txt,
Terms pages, APIs, or live websites.
"""

from __future__ import annotations


ALLOWED_SOURCE_GRADES = {"A", "B", "C", "D"}
ALLOWED_APPROVAL_STATUS = {"not_required", "approved"}
ALLOWED_ROBOTS_STATUS = {"allowed", "partially_allowed"}
ALLOWED_TERMS_STATUS = {"allowed", "limited"}
ALLOWED_ANTI_BOT_RISK = {"none", "low"}


def _normalized(row: dict, field: str) -> str:
    return str(row.get(field, "")).strip().lower()


def _is_true(row: dict, field: str) -> bool:
    return _normalized(row, field) in {"true", "yes", "1"}


def _is_false(row: dict, field: str) -> bool:
    return _normalized(row, field) in {"false", "no", "0"}


def explain_blocking_reason(row: dict) -> list[str]:
    """Return all blocking reasons for a source registry row."""
    reasons: list[str] = []
    decision = _normalized(row, "decision")
    grade = str(row.get("source_grade", "")).strip().upper()
    source_type = _normalized(row, "source_type")
    approval_status = _normalized(row, "approval_status")
    robots_status = _normalized(row, "robots_target_path_status")
    terms_status = _normalized(row, "terms_collection_policy")
    anti_bot_risk = _normalized(row, "anti_bot_risk")

    if decision != "approved":
        reasons.append("not approved")
    if approval_status in {"pending", "expired"}:
        reasons.append("approval pending")
    if approval_status == "rejected":
        reasons.append("rejected source")
    if grade not in ALLOWED_SOURCE_GRADES:
        reasons.append("source grade not allowed")
    if robots_status not in ALLOWED_ROBOTS_STATUS:
        reasons.append("robots disallowed")
    if terms_status not in ALLOWED_TERMS_STATUS:
        reasons.append("terms disallowed")
    if _is_true(row, "login_required"):
        reasons.append("login required")
    if _is_true(row, "captcha_required"):
        reasons.append("captcha required")
    if anti_bot_risk not in ALLOWED_ANTI_BOT_RISK:
        reasons.append("anti-bot high")
    if not _is_true(row, "public_html_access"):
        reasons.append("public HTML unavailable")
    if (
        grade == "D" or _is_true(row, "api_required") or "api" in source_type
    ) and approval_status != "approved":
        reasons.append("API approval pending")
    if approval_status not in ALLOWED_APPROVAL_STATUS:
        if "approval pending" not in reasons and "rejected source" not in reasons:
            reasons.append("approval pending")

    return reasons


def is_source_collectable(row: dict) -> bool:
    """Return True only when a source is eligible for collection."""
    return not explain_blocking_reason(row)


def validate_source_before_collection(row: dict) -> tuple[bool, list[str]]:
    """Validate one source row before collection starts."""
    reasons = explain_blocking_reason(row)
    return not reasons, reasons
