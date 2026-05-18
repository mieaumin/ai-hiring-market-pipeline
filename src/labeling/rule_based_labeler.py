"""Explainable MVP rule-based JD labeler."""

from __future__ import annotations

from datetime import datetime, timezone

from src.processing.ai_role_filter import match_ai_keywords


ROLE_RULES = {
    "AI Engineer": [
        "AI Engineer",
        "ML Engineer",
        "Machine Learning Engineer",
        "LLM Engineer",
        "MLOps",
        "RAG",
        "Docker",
        "Kubernetes",
        "AI \uc5d4\uc9c0\ub2c8\uc5b4",
        "\uba38\uc2e0\ub7ec\ub2dd \uc5d4\uc9c0\ub2c8\uc5b4",
        "LLM \uc5d4\uc9c0\ub2c8\uc5b4",
    ],
    "AI Researcher": [
        "AI Researcher",
        "ML Researcher",
        "Research Scientist",
        "NLP",
        "Computer Vision",
        "benchmark",
        "paper",
        "\ub17c\ubb38",
        "\uc2e4\ud5d8",
        "AI \uc5f0\uad6c\uc6d0",
        "AI \ub9ac\uc11c\ucc98",
    ],
    "AI Scientist": [
        "Data Scientist",
        "AI Scientist",
        "Applied Scientist",
        "PyTorch",
        "TensorFlow",
        "Deep Learning",
        "\ub370\uc774\ud130 \uc0ac\uc774\uc5b8\ud2f0\uc2a4\ud2b8",
        "\ub525\ub7ec\ub2dd",
    ],
    "AI Analyst": [
        "AI Analyst",
        "Data Analyst",
        "Business Analyst",
        "SQL",
        "Tableau",
        "Power BI",
        "KPI",
        "\ub370\uc774\ud130 \ubd84\uc11d\uac00",
        "\ub370\uc774\ud130 \ubd84\uc11d",
    ],
}

SENIORITY_RULES = {
    "Intern": ["intern", "internship", "\uc778\ud134"],
    "Junior": ["junior", "entry", "\uc2e0\uc785", "\uc8fc\ub2c8\uc5b4"],
    "Mid": ["mid", "3 years", "3\ub144", "\uacbd\ub825"],
    "Senior": ["senior", "5 years", "5\ub144", "\uc2dc\ub2c8\uc5b4"],
    "Lead": ["lead", "leader", "\ub9ac\ub4dc"],
    "Principal": ["principal", "staff", "\uc218\uc11d"],
}

SKILL_RULES = [
    "Python",
    "SQL",
    "PyTorch",
    "TensorFlow",
    "scikit-learn",
    "LLM",
    "RAG",
    "NLP",
    "Computer Vision",
    "MLOps",
    "Docker",
    "Kubernetes",
    "AWS",
    "GCP",
    "Azure",
    "LangChain",
    "LangGraph",
]


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


def assign_skills(text: str) -> list[str]:
    """Assign known skills from transparent keyword rules."""
    lower_text = text.lower()
    return [skill for skill in SKILL_RULES if skill.lower() in lower_text]


def assign_seniority(text: str) -> str:
    """Assign seniority if detectable."""
    lower_text = text.lower()
    for seniority, keywords in SENIORITY_RULES.items():
        if any(keyword.lower() in lower_text for keyword in keywords):
            return seniority
    return ""


def label_jd(record: dict) -> dict:
    """Label one JD with role group and matched keywords."""
    text = " ".join(
        str(record.get(field, ""))
        for field in ["title", "job_title", "description_clean", "jd_text_clean", "jd_text_raw"]
    )
    role_group, role_matches = assign_role_group(text)
    keyword_matches = match_ai_keywords(text)
    skills = assign_skills(text)
    seniority = assign_seniority(text)
    confidence = min(1.0, (len(role_matches) + len(keyword_matches) + len(skills)) / 10)
    return {
        "source_url": record.get("source_url", ""),
        "company": record.get("company") or record.get("company_name", ""),
        "title": record.get("title") or record.get("job_title", ""),
        "role_group": role_group or "Other/Unknown",
        "matched_keywords": "|".join(sorted(set(role_matches + keyword_matches))),
        "skills": "|".join(skills),
        "seniority": seniority,
        "domain": "",
        "label_confidence": round(confidence, 2),
        "labeled_at": datetime.now(timezone.utc).isoformat(),
    }
