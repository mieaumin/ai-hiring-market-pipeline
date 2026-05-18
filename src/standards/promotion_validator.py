"""Promotion-rule validators for source, company, and JD records."""

from __future__ import annotations

from pathlib import Path

from src.standards.classification_loader import DecisionResult, load_yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROMOTION_RULES_PATH = ROOT / "configs/promotion_rules.yaml"
TARGET_AI_ROLES = {"AI Analyst", "AI Engineer", "AI Researcher", "AI Scientist"}


def load_promotion_rules(path: str | Path = DEFAULT_PROMOTION_RULES_PATH) -> dict:
    """Load promotion rules."""
    return load_yaml(path)


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in {"true", "yes", "1", "y"}


def _value(row: dict, *fields: str) -> str:
    for field in fields:
        value = str(row.get(field, "")).strip()
        if value:
            return value
    return ""


def source_approval_blockers(row: dict) -> list[str]:
    """Return strict source approval blockers."""
    blockers: list[str] = []
    robots = _value(row, "robots_target_path_status", "robots_status", "robots_allowed").lower()
    terms = _value(row, "terms_collection_policy", "terms_status").lower()
    anti_bot = _value(row, "anti_bot_risk").lower()
    reuse = _value(row, "reuse_restriction_risk").lower()

    if robots in {"disallow", "disallowed", "blocked", "false", "not_allowed"}:
        blockers.append("robots_disallow")
    if terms in {"prohibited", "not_allowed", "disallowed", "blocked"}:
        blockers.append("terms_prohibit_automated_collection")
    if _truthy(row.get("login_required")):
        blockers.append("login_required")
    if _truthy(row.get("captcha_required")):
        blockers.append("captcha_required")
    if anti_bot in {"high", "critical", "prohibited", "bypass_required"}:
        blockers.append("high_anti_bot_risk")
    if reuse in {"critical", "prohibited"}:
        blockers.append("critical_reuse_restriction")
    if not _truthy(row.get("evidence_traceable", row.get("traceable_evidence", ""))):
        blockers.append("missing_traceable_evidence")
    return blockers


def validate_raw_site_to_screening(row: dict) -> DecisionResult:
    """Validate raw job-site discovery promotion into screening."""
    required = ["site_id", "site_url", "site_domain", "discovery_route"]
    missing = [field for field in required if not row.get(field)]
    blockers = missing[:]
    if str(row.get("review_status", "")).strip().lower() == "approved":
        blockers.append("raw_discovery_cannot_already_be_approved")
    return DecisionResult(
        decision="promote_to_site_screening" if not blockers else "blocked",
        allowed=not blockers,
        reasons=["raw job-site candidate has minimum discovery fields"] if not blockers else [],
        blockers=blockers,
        confidence="high",
    )


def validate_site_screening_to_master(row: dict) -> DecisionResult:
    """Validate site screening promotion into master job source registry."""
    blockers = source_approval_blockers(row)
    grade = _value(row, "source_grade").upper()
    approval = _value(row, "approval_status", "source_approval_status").lower()
    eligibility = _value(row, "collection_eligibility").lower()
    decision = _value(row, "screening_decision", "decision").lower()

    if grade not in {"A", "B", "C"}:
        blockers.append("source_grade_not_promotable")
    if approval not in {"approved", "not_required"}:
        blockers.append("source_approval_not_valid")
    if eligibility not in {"eligible", "limited"}:
        blockers.append("collection_eligibility_not_promotable")
    if decision not in {"approved", "limited"}:
        blockers.append("screening_decision_not_promotable")

    return DecisionResult(
        decision="promote_to_master_job_source" if not blockers else "blocked",
        allowed=not blockers,
        reasons=["source satisfies strict promotion rules"] if not blockers else [],
        blockers=sorted(set(blockers)),
        confidence="high" if not blockers else "medium",
    )


def validate_company_to_master(row: dict, threshold: int = 15) -> DecisionResult:
    """Validate company candidate promotion to master."""
    blockers: list[str] = []
    try:
        total_score = float(row.get("total_score", ""))
    except ValueError:
        total_score = -1
    if total_score < threshold:
        blockers.append("total_score_below_threshold")
    if row.get("validation_status") != "approved_for_source_discovery":
        blockers.append("validation_status_not_approved_for_source_discovery")
    if row.get("evidence_quality_score") in {"", None}:
        blockers.append("missing_evidence_quality_score")
    country = str(row.get("country", "")).strip().lower()
    korea_relevant = _truthy(row.get("korea_relevant"))
    if country not in {"kr", "korea", "south korea", "republic of korea", "대한민국", "한국"} and not korea_relevant:
        blockers.append("company_not_korean_or_korea_relevant")

    return DecisionResult(
        decision="promote_company_to_master" if not blockers else "blocked",
        allowed=not blockers,
        reasons=["company meets AI hiring likelihood promotion rules"] if not blockers else [],
        blockers=blockers,
        confidence="high" if not blockers else "medium",
    )


def validate_jd_to_master(row: dict) -> DecisionResult:
    """Validate JD staging promotion to master dataset."""
    blockers: list[str] = []
    if not _value(row, "job_title", "title"):
        blockers.append("missing_title")
    if not _value(row, "company_name", "company"):
        blockers.append("missing_company")
    if not row.get("source_url"):
        blockers.append("missing_source_url")
    if not row.get("job_url"):
        blockers.append("missing_job_url")
    if len(str(row.get("jd_text_clean", ""))) < 200:
        blockers.append("jd_text_clean_too_short")
    if row.get("role_group") not in TARGET_AI_ROLES:
        blockers.append("role_group_not_target_ai_role")
    if str(row.get("validation_status", "")).lower() not in {
        "valid",
        "labeled",
        "normalized",
        "promoted_to_master",
    }:
        blockers.append("validation_status_not_ready_for_master")
    if not row.get("duplicate_cluster_id") and not _truthy(row.get("duplicate_cluster_resolved")):
        blockers.append("duplicate_cluster_not_resolved")
    if not row.get("canonical_source_id") and not _truthy(row.get("accepted_source_lineage")):
        blockers.append("missing_canonical_or_accepted_source_lineage")
    if str(row.get("source_approval_status", "")).lower() not in {"approved", "not_required"}:
        blockers.append("source_not_approved")

    return DecisionResult(
        decision="promote_jd_to_master" if not blockers else "blocked",
        allowed=not blockers,
        reasons=["JD satisfies master promotion rules"] if not blockers else [],
        blockers=blockers,
        confidence="high" if not blockers else "medium",
    )
