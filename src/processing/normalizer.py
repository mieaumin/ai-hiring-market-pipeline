"""Normalize raw JD records into a common cleaned schema."""

from __future__ import annotations

from src.utils.text_cleaning import clean_text


def normalize_jd(record: dict) -> dict:
    """Normalize a raw JD record into the cleaned JD schema."""
    description = clean_text(record.get("description", ""))
    return {
        "source_url": record.get("source_url", ""),
        "company": clean_text(record.get("company", "")),
        "title": clean_text(record.get("title", "")),
        "location": clean_text(record.get("location", "")),
        "description_clean": description,
        "description_length": len(description),
        "collected_at": record.get("collected_at", ""),
    }

