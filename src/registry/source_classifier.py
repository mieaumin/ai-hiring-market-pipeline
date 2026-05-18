"""Source classification helpers for approved-source-only workflows."""

from __future__ import annotations

from src.standards.classification_loader import DecisionResult, validate_classification_value


def classify_source_category(row: dict) -> DecisionResult:
    """Classify a source into a conservative source category."""
    explicit = str(row.get("source_category", "")).strip()
    if explicit:
        validation = validate_classification_value("source_category", explicit)
        allowed = validation.allowed and explicit != "unknown"
        return DecisionResult(
            decision=explicit,
            allowed=allowed,
            reasons=validation.reasons,
            blockers=[] if allowed else ["source_category_unknown"],
            confidence="high" if validation.allowed else "unknown",
        )

    source_type = str(row.get("source_type", "")).strip().lower()
    ats_type = str(row.get("ats_type", "")).strip().lower()
    allowed_method = str(row.get("allowed_method", "")).strip().lower()

    if "api" in allowed_method or source_type == "official_api":
        category = "official_api"
    elif ats_type in {"greenhouse", "lever", "ashby", "workday", "smartrecruiters", "sap_successfactors"}:
        category = "official_ats"
    elif source_type in {"company_career_page", "career_page", "official_career_page"}:
        category = "official_career_page"
    elif source_type in {"job_site", "approved_job_site"}:
        category = "approved_job_site"
    elif source_type in {"aggregator", "job_portal"}:
        category = "aggregator"
    elif source_type in {"community_repost", "community_jobs"}:
        category = "community_repost"
    else:
        category = "unknown"

    return DecisionResult(
        decision=category,
        allowed=category != "unknown",
        reasons=[f"inferred source_category={category}"],
        blockers=[] if category != "unknown" else ["source_category_unknown"],
        confidence="medium" if category != "unknown" else "unknown",
    )


def classify_source_grade(row: dict) -> DecisionResult:
    """Classify a source grade without approving collection."""
    explicit = str(row.get("source_grade", "")).strip().upper()
    if explicit:
        validation = validate_classification_value("source_grade", explicit)
        allowed = validation.allowed and explicit in {"A", "B", "C"}
        return DecisionResult(
            decision=explicit,
            allowed=allowed,
            reasons=validation.reasons,
            blockers=[] if allowed else [f"grade_{explicit}_not_collectable"],
            confidence="high" if validation.allowed else "unknown",
        )

    login_required = str(row.get("login_required", "")).lower() == "true"
    captcha_required = str(row.get("captcha_required", "")).lower() == "true"
    anti_bot_risk = str(row.get("anti_bot_risk", "")).lower()
    robots = str(row.get("robots_target_path_status", row.get("robots_allowed", ""))).lower()
    terms = str(row.get("terms_collection_policy", "")).lower()

    if robots in {"blocked", "disallowed", "false"}:
        grade = "F"
    elif login_required or captcha_required or anti_bot_risk in {"high", "critical", "bypass_required"}:
        grade = "E"
    elif terms in {"prohibited", "not_allowed", "disallowed"}:
        grade = "E"
    elif str(row.get("api_available", "")).lower() == "true" and str(row.get("source_type", "")).lower() == "official_api":
        grade = "A"
    elif str(row.get("ats_type", "")).strip():
        grade = "B"
    elif str(row.get("public_html_access", "")).lower() == "true":
        grade = "C"
    else:
        grade = "D"

    return DecisionResult(
        decision=grade,
        allowed=grade in {"A", "B", "C"},
        reasons=[f"inferred source_grade={grade}; approval still requires promotion rules"],
        blockers=[] if grade in {"A", "B", "C"} else [f"grade_{grade}_not_collectable"],
        confidence="medium",
    )
