"""Rule-based AI role filtering."""

from __future__ import annotations

from pathlib import Path

import yaml

from src.utils.text_cleaning import clean_text


DEFAULT_KEYWORD_PATH = Path("configs/ai_keywords.yaml")


def load_keywords(path: str | Path = DEFAULT_KEYWORD_PATH) -> list[str]:
    """Load Korean and English AI keywords from YAML."""
    path = Path(path)
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    keywords: list[str] = []
    for language_group in data.values():
        for keyword_group in language_group.values():
            keywords.extend(keyword_group)
    return sorted(set(keywords), key=str.lower)


def match_ai_keywords(text: str, keywords: list[str] | None = None) -> list[str]:
    """Return AI keywords found in text."""
    keywords = keywords or load_keywords()
    normalized_text = clean_text(text).lower()
    return [keyword for keyword in keywords if keyword.lower() in normalized_text]


def is_ai_related_jd(record: dict, keywords: list[str] | None = None) -> bool:
    """Return True when title or description matches AI keyword rules."""
    searchable = f"{record.get('title', '')} {record.get('description_clean', '')} {record.get('description', '')}"
    return bool(match_ai_keywords(searchable, keywords))

