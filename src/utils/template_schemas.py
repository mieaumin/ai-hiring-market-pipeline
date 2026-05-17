"""Central CSV template schemas for the safe pipeline scaffold.

This module contains headers only. It does not fetch, crawl, or collect data.
"""

from __future__ import annotations

from pathlib import Path


SOURCE_REGISTRY_COLUMNS = [
    "source_id",
    "company_id",
    "company_name",
    "source_name",
    "source_url",
    "source_type",
    "source_grade",
    "manual_review_required",
    "human_approval_required",
    "approval_status",
    "approval_reviewer",
    "approval_reviewed_at",
    "approval_notes",
    "robots_txt_url",
    "robots_target_path_status",
    "terms_url",
    "terms_collection_policy",
    "api_required",
    "login_required",
    "captcha_required",
    "anti_bot_risk",
    "public_html_access",
    "dynamic_rendering_risk",
    "personal_data_risk",
    "copyright_risk",
    "reuse_restriction_risk",
    "allowed_method",
    "decision",
    "decision_reason",
    "last_checked_at",
    "notes",
]

JD_COLUMNS = [
    "jd_id",
    "company_id",
    "company_name",
    "source_id",
    "source_url",
    "job_url",
    "job_title",
    "job_category",
    "job_category_confidence",
    "role_group",
    "required_skills",
    "preferred_skills",
    "responsibilities",
    "qualifications",
    "preferred_qualifications",
    "experience_level",
    "education",
    "employment_type",
    "location",
    "jd_text_raw",
    "jd_text_clean",
    "language",
    "collected_at",
    "last_checked_at",
    "source_grade",
    "source_approval_status",
    "validation_status",
    "failure_reason",
    "quality_score",
    "content_hash",
    "duplicate_key",
    "notes",
]

SOURCE_POLICY_EVIDENCE_COLUMNS = [
    "evidence_id",
    "source_id",
    "company_id",
    "company_name",
    "source_name",
    "source_url",
    "evidence_category",
    "evidence_url",
    "evidence_text_excerpt",
    "policy_keyword_found",
    "risk_level",
    "reviewer",
    "reviewed_at",
    "source_grade",
    "approval_status",
    "decision",
    "notes",
]

QUALITY_GATE_REPORT_COLUMNS = [
    "run_id",
    "jd_id",
    "source_id",
    "company_id",
    "validation_status",
    "quality_score",
    "passed_quality_gate",
    "failure_reason",
    "checked_at",
    "notes",
]

JD_COLLECTION_LOG_COLUMNS = [
    "run_id",
    "source_id",
    "source_url",
    "collector_name",
    "started_at",
    "finished_at",
    "status",
    "request_count",
    "records_found",
    "records_saved",
    "error_count",
    "notes",
]

JD_VALIDATION_ERRORS_COLUMNS = [
    "error_id",
    "jd_id",
    "source_id",
    "job_url",
    "error_type",
    "error_reason",
    "detected_at",
    "review_status",
    "notes",
]

RUNS_COLUMNS = [
    "run_id",
    "phase_name",
    "started_at",
    "finished_at",
    "status",
    "input_count",
    "output_count",
    "error_count",
    "notes",
]

ERRORS_COLUMNS = [
    "error_id",
    "run_id",
    "phase_name",
    "record_id",
    "error_type",
    "error_message",
    "retryable",
    "created_at",
    "notes",
]

TEMPLATE_FILES = {
    "configs/source_registry_template.csv": SOURCE_REGISTRY_COLUMNS,
    "runtime/source_discovery.csv": SOURCE_REGISTRY_COLUMNS,
    "runtime/source_verification.csv": SOURCE_REGISTRY_COLUMNS,
    "staging/source_registry_staging.csv": SOURCE_REGISTRY_COLUMNS,
    "master/source_registry_master.csv": SOURCE_REGISTRY_COLUMNS,
    "runtime/source_policy_evidence.csv": SOURCE_POLICY_EVIDENCE_COLUMNS,
    "runtime/raw_jd_collection.csv": JD_COLUMNS,
    "data/raw/raw_jds.csv": JD_COLUMNS,
    "data/cleaned/cleaned_jds.csv": JD_COLUMNS,
    "data/labeled/labeled_jds.csv": JD_COLUMNS,
    "staging/jd_staging.csv": JD_COLUMNS,
    "master/jd_master_dataset.csv": JD_COLUMNS,
    "runtime/jd_collection_log.csv": JD_COLLECTION_LOG_COLUMNS,
    "runtime/jd_validation_errors.csv": JD_VALIDATION_ERRORS_COLUMNS,
    "runtime/quality_gate_report.csv": QUALITY_GATE_REPORT_COLUMNS,
    "runtime/runs.csv": RUNS_COLUMNS,
    "runtime/errors.csv": ERRORS_COLUMNS,
}


def read_header(path: Path) -> list[str]:
    """Read the first CSV line as a header list."""
    if not path.exists():
        return []
    first_line = path.read_text(encoding="utf-8").splitlines()
    if not first_line:
        return []
    return [column.strip() for column in first_line[0].split(",")]


def missing_columns(path: Path, required_columns: list[str]) -> list[str]:
    """Return required columns missing from a CSV header."""
    header = read_header(path)
    return [column for column in required_columns if column not in header]


def write_header_if_missing(path: Path, columns: list[str]) -> bool:
    """Create a header-only CSV when it is missing or empty."""
    if path.exists() and path.stat().st_size > 0:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(",".join(columns) + "\n", encoding="utf-8")
    return True
