"""Normalize raw JD records into a common cleaned schema."""

from __future__ import annotations

from bs4 import BeautifulSoup

from src.utils.text_cleaning import clean_text


def strip_html(value: str) -> str:
    """Strip HTML while preserving readable text."""
    if not value:
        return ""
    return BeautifulSoup(value, "html.parser").get_text(" ", strip=True)


def normalize_jd(record: dict) -> dict:
    """Normalize a raw JD record into the cleaned JD schema."""
    raw_description = (
        record.get("jd_text_raw")
        or record.get("description")
        or record.get("description_raw")
        or record.get("content")
        or ""
    )
    description = clean_text(strip_html(raw_description))
    normalized = dict(record)
    normalized.update(
        {
            "source_url": record.get("source_url", ""),
            "company": clean_text(record.get("company") or record.get("company_name", "")),
            "company_name": clean_text(record.get("company_name") or record.get("company", "")),
            "title": clean_text(record.get("title") or record.get("job_title", "")),
            "job_title": clean_text(record.get("job_title") or record.get("title", "")),
            "location": clean_text(record.get("location", "")),
            "description_clean": description,
            "jd_text_clean": description,
            "jd_text_raw": raw_description,
            "description_length": len(description),
            "collected_at": record.get("collected_at", ""),
        }
    )
    return normalized
