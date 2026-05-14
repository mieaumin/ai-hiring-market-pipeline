"""Source registry decision helpers."""

from __future__ import annotations


ALLOWED_GRADES = {"A", "B", "C"}
BLOCKED_GRADES = {"D", "E"}


def grade_source(row: dict) -> str:
    """Assign a conservative source grade from source registry fields."""
    login_required = str(row.get("login_required", "")).lower() == "true"
    anti_bot_risk = str(row.get("anti_bot_risk", "")).lower()
    api_available = str(row.get("api_available", "")).lower() == "true"
    source_type = str(row.get("source_type", "")).lower()
    robots_allowed = str(row.get("robots_allowed", "")).lower()

    if login_required or anti_bot_risk in {"high", "prohibited"}:
        return "E"
    if api_available and source_type == "official_api":
        return "A"
    if api_available or source_type in {"ats", "public_ats"}:
        return "B"
    if source_type in {"company_career_page", "career_page"} and robots_allowed == "true":
        return "C"
    return "D"


def is_source_allowed(row: dict) -> bool:
    """Return True for A, B, and carefully reviewed C source decisions."""
    decision = str(row.get("decision", "")).upper()
    if decision:
        return decision in ALLOWED_GRADES
    return grade_source(row) in ALLOWED_GRADES

