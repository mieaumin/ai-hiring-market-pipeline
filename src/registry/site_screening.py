"""Explainable site screening for Phase 0.5.

This module screens local site rows and manually supplied evidence only. It
does not crawl job postings, fetch policy pages, call APIs, or approve sources
without evidence.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.registry.site_risk_scoring import score_evidence_rows


APPROVABLE_GRADES = {"A", "B", "C"}
REJECTED_GRADES = {"E", "F"}


@dataclass(frozen=True)
class SiteScreeningResult:
    site_id: str
    site_name: str
    source_grade: str
    collection_eligibility: str
    screening_decision: str
    screening_reason: str
    manual_review_required: bool
    human_approval_required: bool
    approval_status: str

    def to_row(self) -> dict:
        """Return a CSV-friendly row."""
        return {
            "site_id": self.site_id,
            "site_name": self.site_name,
            "source_grade": self.source_grade,
            "collection_eligibility": self.collection_eligibility,
            "screening_decision": self.screening_decision,
            "screening_reason": self.screening_reason,
            "manual_review_required": str(self.manual_review_required).lower(),
            "human_approval_required": str(self.human_approval_required).lower(),
            "approval_status": self.approval_status,
        }


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"true", "yes", "1", "required"}


def _value(row: dict, field: str) -> str:
    return str(row.get(field, "")).strip().lower()


def detect_blockers(site_row: dict, evidence_rows: list[dict] | None = None) -> list[str]:
    """Return hard blockers that prevent approval."""
    blockers: list[str] = []
    robots_status = _value(site_row, "robots_status") or _value(site_row, "robots_target_path_status")
    terms_status = _value(site_row, "terms_status") or _value(site_row, "terms_collection_policy")
    anti_bot_risk = _value(site_row, "anti_bot_risk")
    reuse_risk = _value(site_row, "reuse_restriction_risk")

    if robots_status in {"disallow", "disallowed", "blocked", "not_allowed"}:
        blockers.append("robots_disallow_detected")
    if terms_status in {"prohibited", "not_allowed", "disallowed", "blocked"}:
        blockers.append("terms_prohibit_automated_collection")
    if _truthy(site_row.get("captcha_required")):
        blockers.append("captcha_required")
    if _truthy(site_row.get("login_required")):
        blockers.append("login_required")
    if anti_bot_risk in {"high", "critical", "prohibited", "bypass_required"}:
        blockers.append("high_anti_bot_risk")
    if reuse_risk in {"critical", "prohibited"}:
        blockers.append("critical_reuse_restriction")

    if evidence_rows:
        score = score_evidence_rows(evidence_rows)
        categories = set(score.get("matched_categories", []))
        if "robots_disallow" in categories:
            blockers.append("robots_disallow_detected")
        if categories.intersection(
            {
                "scraping_prohibited",
                "automated_collection_prohibited",
                "bot_prohibited",
            }
        ):
            blockers.append("terms_prohibit_automated_collection")
        if "captcha" in categories:
            blockers.append("captcha_required")
        if "login_required" in categories:
            blockers.append("login_required")
        if "anti_bot" in categories:
            blockers.append("high_anti_bot_risk")
        if categories.intersection({"redistribution_prohibited", "commercial_use_prohibited"}):
            blockers.append("critical_reuse_restriction")

    return sorted(set(blockers))


def infer_source_grade(site_row: dict, evidence_rows: list[dict] | None = None) -> str:
    """Infer conservative source grade for a screened site."""
    blockers = detect_blockers(site_row, evidence_rows=evidence_rows)
    if blockers:
        return "E" if any(blocker != "robots_disallow_detected" for blocker in blockers) else "F"

    if _truthy(site_row.get("official_api_available")) or _truthy(site_row.get("api_available")):
        return "A"
    if _truthy(site_row.get("public_ats_endpoint_available")) or _truthy(
        site_row.get("public_api_endpoint_available")
    ):
        return "B"

    robots_status = _value(site_row, "robots_status") or _value(site_row, "robots_target_path_status")
    terms_status = _value(site_row, "terms_status") or _value(site_row, "terms_collection_policy")
    public_html_access = _truthy(site_row.get("public_html_access"))
    if robots_status in {"allowed", "partially_allowed"} and terms_status in {
        "allowed",
        "limited",
    } and public_html_access:
        return "C"

    if _truthy(site_row.get("unusable")) or _value(site_row, "access_status") == "blocked":
        return "F"
    return "D"


def screen_site(site_row: dict, evidence_rows: list[dict] | None = None) -> SiteScreeningResult:
    """Generate an explainable Phase 0.5 screening decision."""
    evidence_rows = evidence_rows or []
    blockers = detect_blockers(site_row, evidence_rows=evidence_rows)
    grade = str(site_row.get("source_grade") or infer_source_grade(site_row, evidence_rows)).upper()

    reasons: list[str] = []
    if blockers:
        reasons.extend(blockers)

    if grade in REJECTED_GRADES:
        decision = "rejected"
        eligibility = "excluded"
        approval_status = "rejected"
        manual_review_required = grade == "E"
        human_approval_required = False
        reasons.append(f"grade_{grade}_not_collectable")
    elif grade == "D":
        decision = "needs_legal_review"
        eligibility = "needs_review"
        approval_status = "pending"
        manual_review_required = True
        human_approval_required = True
        reasons.append("grade_D_unclear_policy_or_general_scraping_needed")
    elif grade in APPROVABLE_GRADES:
        decision = "needs_manual_review"
        eligibility = "needs_review"
        approval_status = "pending" if grade in {"B", "C"} else "not_required"
        manual_review_required = grade in {"B", "C"}
        human_approval_required = grade in {"B", "C"}
        reasons.append(f"grade_{grade}_requires_final_evidence_review_before_approval")
    else:
        decision = "needs_manual_review"
        eligibility = "needs_review"
        approval_status = "pending"
        manual_review_required = True
        human_approval_required = True
        reasons.append("unknown_grade_requires_review")

    screening_reason = "; ".join(reasons) or "screening_requires_evidence_review"
    return SiteScreeningResult(
        site_id=site_row.get("site_id", ""),
        site_name=site_row.get("site_name", ""),
        source_grade=grade,
        collection_eligibility=eligibility,
        screening_decision=decision,
        screening_reason=screening_reason,
        manual_review_required=manual_review_required,
        human_approval_required=human_approval_required,
        approval_status=approval_status,
    )
