"""Simple JD deduplication helpers."""

from __future__ import annotations

import hashlib


def normalize_key_part(value: str) -> str:
    """Normalize a company or title string for duplicate keys."""
    value = (value or "").lower()
    return "".join(character for character in value if character.isalnum())


def text_hash(text: str) -> str:
    """Return a stable SHA-256 hash for optional JD text deduplication."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def dedupe_key(record: dict, include_text_hash: bool = False) -> tuple:
    """Build a duplicate key from source_url, company, title, and optional text hash."""
    key = (
        record.get("source_url", ""),
        normalize_key_part(record.get("company_name") or record.get("company", "")),
        normalize_key_part(record.get("job_title") or record.get("title", "")),
    )
    if include_text_hash:
        description = record.get("description_clean") or record.get("description", "")
        return (*key, text_hash(description))
    return key


def deduplicate(records: list[dict], include_text_hash: bool = False) -> list[dict]:
    """Remove duplicate JD records while preserving order."""
    seen = set()
    unique_records = []
    for record in records:
        key = dedupe_key(record, include_text_hash=include_text_hash)
        if key in seen:
            continue
        seen.add(key)
        unique_records.append(record)
    return unique_records
