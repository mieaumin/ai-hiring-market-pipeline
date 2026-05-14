"""JD validation rules."""

from __future__ import annotations

from src.processing.ai_role_filter import is_ai_related_jd


MIN_DESCRIPTION_LENGTH = 200


def validate_jd(record: dict, min_description_length: int = MIN_DESCRIPTION_LENGTH) -> tuple[bool, str]:
    """Validate one cleaned JD record."""
    if not record.get("title"):
        return False, "missing_title"
    if not record.get("company"):
        return False, "missing_company"
    if not record.get("source_url"):
        return False, "missing_source_url"
    if not record.get("collected_at"):
        return False, "missing_collected_at"

    description = record.get("description_clean") or record.get("description", "")
    if len(description) < min_description_length:
        return False, "description_too_short"
    if not is_ai_related_jd(record):
        return False, "not_ai_related"
    return True, "valid"

