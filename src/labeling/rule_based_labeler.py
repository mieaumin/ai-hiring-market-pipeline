"""Explainable MVP rule-based JD labeler."""

from __future__ import annotations

from datetime import datetime, timezone

from src.processing.ai_role_filter import match_ai_keywords


ROLE_RULES = {
    "AI Engineer": ["AI Engineer", "ML Engineer", "LLM Engineer", "MLOps", "RAG", "Docker", "Kubernetes"],
    "AI Researcher": ["AI Researcher", "ML Researcher", "NLP", "Computer Vision", "benchmark", "paper"],
    "AI Scientist": ["Data Scientist", "AI Scientist", "Applied Scientist", "PyTorch", "TensorFlow"],
    "AI Analyst": ["AI Analyst", "Data Analyst", "Business Analyst", "SQL", "Tableau", "Power BI"],
}


def assign_role_group(text: str) -> tuple[str, list[str]]:
    """Assign a role group using transparent keyword rules."""
    lower_text = text.lower()
    best_role = ""
    best_matches: list[str] = []
    for role_group, keywords in ROLE_RULES.items():
        matches = [keyword for keyword in keywords if keyword.lower() in lower_text]
        if len(matches) > len(best_matches):
            best_role = role_group
            best_matches = matches
    return best_role, best_matches


def label_jd(record: dict) -> dict:
    """Label one JD with role group and matched keywords."""
    text = f"{record.get('title', '')} {record.get('description_clean', '')}"
    role_group, role_matches = assign_role_group(text)
    keyword_matches = match_ai_keywords(text)
    confidence = min(1.0, (len(role_matches) + len(keyword_matches)) / 10)
    return {
        "source_url": record.get("source_url", ""),
        "company": record.get("company", ""),
        "title": record.get("title", ""),
        "role_group": role_group,
        "matched_keywords": "|".join(sorted(set(role_matches + keyword_matches))),
        "skills": "",
        "seniority": "",
        "domain": "",
        "label_confidence": round(confidence, 2),
        "labeled_at": datetime.now(timezone.utc).isoformat(),
    }

