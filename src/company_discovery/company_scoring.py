"""Company scoring helpers for Phase 1 company discovery."""

from __future__ import annotations

from dataclasses import dataclass


SIGNAL_FIELDS = (
    "hiring_signal_score",
    "business_ai_signal_score",
    "tech_signal_score",
    "market_signal_score",
    "evidence_quality_score",
)


@dataclass(frozen=True)
class CompanyScore:
    """Structured company discovery score."""

    total_score: int
    priority_tier: str


def clamp_score(value: int | float | str | None, minimum: int = 0, maximum: int = 100) -> int:
    """Convert a score-like value into a bounded integer."""
    if value in (None, ""):
        return 0
    score = int(float(value))
    return max(minimum, min(maximum, score))


def calculate_total_score(row: dict) -> int:
    """Calculate total company score from signal score fields."""
    return sum(clamp_score(row.get(field)) for field in SIGNAL_FIELDS)


def assign_priority_tier(total_score: int) -> str:
    """Assign a simple MVP priority tier."""
    if total_score >= 75:
        return "high"
    if total_score >= 50:
        return "medium"
    return "low"


def score_company(row: dict) -> CompanyScore:
    """Return total score and priority tier for a company candidate row."""
    total_score = calculate_total_score(row)
    return CompanyScore(total_score=total_score, priority_tier=assign_priority_tier(total_score))

