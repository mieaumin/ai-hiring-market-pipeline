"""Source registry decision helpers.

These helpers are intentionally policy-only. They do not perform network
access, crawling, API calls, or browser automation.
"""

from __future__ import annotations

from src.registry.source_grading import can_move_to_master, default_approval_status


def grade_source(row: dict) -> str:
    """Assign a conservative Grade A-F source grade from local fields.

    This is only a helper for reviewed records. It must not be used as a
    substitute for compliance review.
    """
    login_required = str(row.get("login_required", "")).lower() == "true"
    captcha_required = str(row.get("captcha_required", "")).lower() == "true"
    anti_bot_risk = str(row.get("anti_bot_risk", "")).lower()
    api_required = str(row.get("api_required", "")).lower() == "true"
    source_type = str(row.get("source_type", "")).lower()
    robots_status = str(row.get("robots_target_path_status", "")).lower()
    terms_status = str(row.get("terms_collection_policy", "")).lower()
    public_html_access = str(row.get("public_html_access", "")).lower()

    if robots_status in {"blocked", "disallowed"} or str(row.get("access_status", "")).lower() == "blocked":
        return "F"
    if (
        login_required
        or captcha_required
        or anti_bot_risk in {"high", "prohibited", "bypass_required"}
        or terms_status in {"prohibited", "not_allowed"}
    ):
        return "E"
    if api_required:
        return "D"
    if source_type in {"official", "official_public_source"}:
        return "A"
    if source_type in {"ats", "public_ats", "public_endpoint"}:
        return "B"
    if (
        source_type in {"company_career_page", "career_page"}
        and robots_status in {"allowed", "not_blocked"}
        and terms_status in {"allowed", "not_prohibited"}
        and public_html_access == "true"
    ):
        return "C"
    return "D"


def is_source_allowed(row: dict, automated_checks_passed: bool = False) -> bool:
    """Return True only when strict Grade A-F policy permits use."""
    return can_move_to_master(row, automated_checks_passed=automated_checks_passed)


def is_source_master_eligible(row: dict, automated_checks_passed: bool = False) -> bool:
    """Return True when strict Grade A-F approval policy permits promotion."""
    return can_move_to_master(row, automated_checks_passed=automated_checks_passed)


def apply_default_approval_status(row: dict) -> dict:
    """Return a copy with the default approval status for its source grade."""
    next_row = dict(row)
    if not next_row.get("approval_status") and next_row.get("source_grade"):
        next_row["approval_status"] = default_approval_status(next_row["source_grade"])
    return next_row
