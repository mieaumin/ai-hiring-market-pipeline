"""Parse manually supplied site policy evidence text for risk keywords.

This module does not crawl websites, fetch robots.txt, or collect job postings.
It only evaluates evidence text that a reviewer or approved workflow provides.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml


DEFAULT_POLICY_KEYWORDS_PATH = Path("configs/policy_keywords.yaml")


def load_policy_keywords(path: str | Path = DEFAULT_POLICY_KEYWORDS_PATH) -> dict:
    """Load policy keyword registry from YAML."""
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def flatten_keywords(keyword_registry: dict) -> dict[str, list[str]]:
    """Flatten Korean/English keyword groups by category."""
    flattened: dict[str, list[str]] = {}
    for category, language_groups in keyword_registry.items():
        keywords: list[str] = []
        if isinstance(language_groups, dict):
            for values in language_groups.values():
                keywords.extend(str(value) for value in values or [])
        elif isinstance(language_groups, list):
            keywords.extend(str(value) for value in language_groups)
        flattened[category] = keywords
    return flattened


def find_policy_keywords(
    text: str,
    keyword_registry: dict | None = None,
) -> dict[str, list[str]]:
    """Return matched policy keywords by category."""
    registry = flatten_keywords(keyword_registry or load_policy_keywords())
    normalized_text = (text or "").lower()
    matches: dict[str, list[str]] = {}
    for category, keywords in registry.items():
        matched = [keyword for keyword in keywords if keyword.lower() in normalized_text]
        if matched:
            matches[category] = matched
    return matches


def parse_evidence_row(row: dict, keyword_registry: dict | None = None) -> dict:
    """Parse one manually provided evidence row."""
    text = " ".join(
        [
            str(row.get("evidence_text_excerpt", "")),
            str(row.get("policy_keyword_found", "")),
            str(row.get("notes", "")),
        ]
    )
    matches = find_policy_keywords(text, keyword_registry=keyword_registry)
    return {
        "evidence_id": row.get("evidence_id", ""),
        "site_id": row.get("site_id", ""),
        "site_name": row.get("site_name", ""),
        "matches": matches,
        "matched_categories": sorted(matches),
    }


def parse_evidence_rows(
    rows: Iterable[dict],
    keyword_registry: dict | None = None,
) -> list[dict]:
    """Parse many manually provided evidence rows."""
    return [parse_evidence_row(row, keyword_registry=keyword_registry) for row in rows]
