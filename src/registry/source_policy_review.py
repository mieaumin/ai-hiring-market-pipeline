"""Policy review helpers for source registry decisions.

This module contains local policy logic only. It does not fetch robots.txt or
Terms pages.
"""

from __future__ import annotations


TERMS_REVIEW_CHECKLIST = [
    "automated collection prohibited",
    "scraping/crawling/bot/spider prohibited",
    "copying/extraction/storage prohibited",
    "redistribution prohibited",
    "derivative or secondary use prohibited",
    "commercial use prohibited",
    "database reproduction prohibited",
    "API approval required",
    "abnormal access prohibited",
    "access-control bypass prohibited",
]


def has_blocking_policy_risk(row: dict) -> bool:
    """Return True when known policy fields indicate a blocking risk."""
    blocking_values = {
        "robots_target_path_status": {"blocked", "disallowed"},
        "terms_collection_policy": {"prohibited", "not_allowed"},
        "login_required": {"true", "yes"},
        "captcha_required": {"true", "yes"},
        "anti_bot_risk": {"high", "prohibited", "bypass_required"},
    }
    for field, blocked in blocking_values.items():
        value = str(row.get(field, "")).strip().lower()
        if value in blocked:
            return True
    return False


def recommended_grade_from_policy(row: dict) -> str:
    """Recommend a conservative grade from local policy fields."""
    if has_blocking_policy_risk(row):
        return "F"
    if str(row.get("api_required", "")).strip().lower() in {"true", "yes"}:
        return "D"
    if str(row.get("terms_collection_policy", "")).strip().lower() in {"unclear", "unknown"}:
        return "E"
    if str(row.get("source_type", "")).strip().lower() in {"ats", "public_ats", "public_endpoint"}:
        return "B"
    if str(row.get("source_type", "")).strip().lower() in {"company_career_page", "career_page"}:
        return "C"
    if str(row.get("source_type", "")).strip().lower() in {"official", "official_source"}:
        return "A"
    return "E"

