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
        record.get("job_url") or record.get("source_url", ""),
        normalize_key_part(record.get("company_name") or record.get("company", "")),
        normalize_key_part(record.get("job_title") or record.get("title", "")),
    )
    if include_text_hash:
        description = (
            record.get("jd_text_clean")
            or record.get("description_clean")
            or record.get("description")
            or ""
        )
        return (*key, text_hash(description))
    return key


def duplicate_cluster_id(record: dict) -> str:
    """Return a stable duplicate cluster id for one JD record."""
    source_key = "|".join(str(part) for part in dedupe_key(record, include_text_hash=True))
    return f"dup_{hashlib.sha256(source_key.encode('utf-8')).hexdigest()[:16]}"


def deduplicate(records: list[dict], include_text_hash: bool = False) -> list[dict]:
    """Remove duplicate JD records while preserving order."""
    seen = set()
    unique_records = []
    for record in records:
        key = dedupe_key(record, include_text_hash=include_text_hash)
        if key in seen:
            continue
        seen.add(key)
        next_record = dict(record)
        next_record.setdefault("duplicate_cluster_id", duplicate_cluster_id(next_record))
        unique_records.append(next_record)
    return unique_records


def mark_duplicates(records: list[dict]) -> list[dict]:
    """Return records with duplicate flags and duplicate cluster ids assigned."""
    seen = set()
    marked = []
    for record in records:
        key = dedupe_key(record, include_text_hash=True)
        next_record = dict(record)
        next_record["duplicate_cluster_id"] = duplicate_cluster_id(next_record)
        next_record["is_duplicate"] = str(key in seen).lower()
        if key in seen and not next_record.get("validation_status"):
            next_record["validation_status"] = "duplicate"
        seen.add(key)
        marked.append(next_record)
    return marked
