"""Conservative risk scoring for site policy evidence.

The functions operate on local evidence rows or parsed keyword matches only.
They do not crawl websites or collect job postings.
"""

from __future__ import annotations

from src.registry.site_policy_parser import parse_evidence_rows


RISK_RANK = {
    "unknown": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

KEYWORD_CATEGORY_RISK = {
    "scraping_prohibited": "critical",
    "automated_collection_prohibited": "critical",
    "bot_prohibited": "critical",
    "robots_disallow": "critical",
    "captcha": "critical",
    "login_required": "critical",
    "anti_bot": "critical",
    "redistribution_prohibited": "high",
    "commercial_use_prohibited": "high",
    "api_required": "medium",
}


def max_risk(left: str, right: str) -> str:
    """Return the higher risk level."""
    return left if RISK_RANK.get(left, 0) >= RISK_RANK.get(right, 0) else right


def risk_from_keyword_category(category: str) -> str:
    """Return conservative risk for a matched keyword category."""
    return KEYWORD_CATEGORY_RISK.get(category, "medium")


def score_parsed_policy_matches(parsed_rows: list[dict]) -> dict:
    """Score risk from parsed policy keyword matches."""
    risk_level = "unknown"
    reasons: list[str] = []
    categories: set[str] = set()
    for parsed in parsed_rows:
        for category in parsed.get("matched_categories", []):
            categories.add(category)
            category_risk = risk_from_keyword_category(category)
            risk_level = max_risk(risk_level, category_risk)
            reasons.append(f"{category}:{category_risk}")
    return {
        "risk_level": risk_level,
        "matched_categories": sorted(categories),
        "risk_reasons": reasons,
    }


def score_evidence_rows(rows: list[dict], keyword_registry: dict | None = None) -> dict:
    """Parse and score manually supplied evidence rows."""
    parsed_rows = parse_evidence_rows(rows, keyword_registry=keyword_registry)
    return score_parsed_policy_matches(parsed_rows)


def has_blocking_risk(score: dict) -> bool:
    """Return True for high or critical risk."""
    return RISK_RANK.get(score.get("risk_level", "unknown"), 0) >= RISK_RANK["high"]
