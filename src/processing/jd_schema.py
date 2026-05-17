"""JD schema validation helpers."""

from __future__ import annotations

from src.utils.template_schemas import JD_COLUMNS


REQUIRED_JD_FIELDS = [
    "jd_id",
    "company_id",
    "company_name",
    "source_id",
    "source_url",
    "job_url",
    "job_title",
    "jd_text_clean",
    "collected_at",
    "source_grade",
    "source_approval_status",
]


def missing_jd_columns(columns: list[str]) -> list[str]:
    """Return required JD schema columns missing from a header."""
    return [column for column in JD_COLUMNS if column not in columns]


def validate_required_jd_fields(record: dict) -> tuple[bool, list[str]]:
    """Validate required fields on a JD record."""
    missing = [field for field in REQUIRED_JD_FIELDS if not record.get(field)]
    return not missing, missing

