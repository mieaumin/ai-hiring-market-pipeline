"""JD quality gate logic.

This module evaluates local records only. It does not collect data.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.processing.ai_role_filter import is_ai_related_jd
from src.processing.jd_schema import validate_required_jd_fields


MIN_TEXT_LENGTH = 200
QUALITY_SCORE_THRESHOLD = 70


@dataclass(frozen=True)
class QualityGateResult:
    passed: bool
    status: str
    reasons: list[str]
    quality_score: int


def source_approval_is_valid(record: dict) -> bool:
    """Return whether the JD source approval state is valid."""
    grade = str(record.get("source_grade", "")).strip().upper()
    status = str(record.get("source_approval_status", "")).strip().lower()
    if grade == "A":
        return status in {"not_required", "approved"}
    if grade in {"B", "C"}:
        return status == "approved"
    return False


def calculate_quality_score(record: dict) -> int:
    """Calculate a simple placeholder quality score."""
    score = 0
    if record.get("job_title"):
        score += 15
    if record.get("company_name"):
        score += 10
    if record.get("source_url") and record.get("job_url"):
        score += 15
    if len(record.get("jd_text_clean", "")) >= MIN_TEXT_LENGTH:
        score += 25
    if source_approval_is_valid(record):
        score += 20
    if record.get("role_group") or is_ai_related_jd(record):
        score += 15
    return min(score, 100)


def evaluate_quality_gate(
    record: dict,
    seen_duplicate_keys: set[str] | None = None,
) -> QualityGateResult:
    """Evaluate one JD record against MVP quality gate rules."""
    reasons: list[str] = []
    required_ok, missing = validate_required_jd_fields(record)
    if not required_ok:
        reasons.append(f"missing_required_fields:{'|'.join(missing)}")
    if len(record.get("jd_text_clean", "")) < MIN_TEXT_LENGTH:
        reasons.append("description_too_short")
    if not source_approval_is_valid(record):
        reasons.append("source_approval_invalid")
    if not (record.get("role_group") or is_ai_related_jd(record)):
        reasons.append("not_ai_related")
    if not record.get("content_hash") or not record.get("duplicate_key"):
        reasons.append("missing_deduplication_keys")
    if record.get("validation_status") == "failed":
        reasons.append(record.get("failure_reason") or "extractor_validation_failed")
    if seen_duplicate_keys is not None and record.get("duplicate_key") in seen_duplicate_keys:
        reasons.append("duplicate_jd")

    quality_score = calculate_quality_score(record)
    if quality_score < QUALITY_SCORE_THRESHOLD:
        reasons.append("quality_score_below_threshold")

    passed = not reasons
    return QualityGateResult(
        passed=passed,
        status="valid" if passed else "invalid",
        reasons=reasons,
        quality_score=quality_score,
    )


def split_rows_by_quality_gate(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split raw JD rows into valid staging rows and validation error rows."""
    valid_rows: list[dict] = []
    error_rows: list[dict] = []
    seen_duplicate_keys: set[str] = set()

    for record in records:
        result = evaluate_quality_gate(record, seen_duplicate_keys=seen_duplicate_keys)
        next_record = dict(record)
        next_record["validation_status"] = result.status
        next_record["quality_score"] = str(result.quality_score)
        next_record["failure_reason"] = "|".join(result.reasons)

        duplicate_key = str(record.get("duplicate_key", ""))
        if result.passed:
            valid_rows.append(next_record)
            if duplicate_key:
                seen_duplicate_keys.add(duplicate_key)
        else:
            error_rows.append(next_record)

    return valid_rows, error_rows
