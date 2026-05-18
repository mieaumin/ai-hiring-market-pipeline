"""Central CSV template schemas for the safe pipeline scaffold.

This module contains headers only. It does not fetch, crawl, or collect data.
"""

from __future__ import annotations

from pathlib import Path


RAW_JOB_SITE_DISCOVERY_COLUMNS = [
    "site_id",
    "site_name",
    "site_url",
    "site_domain",
    "site_type",
    "discovery_route",
    "discovery_query",
    "discovery_source_url",
    "country",
    "confidence",
    "review_status",
    "collection_eligibility",
    "notes",
    "discovered_at",
]

SITE_POLICY_EVIDENCE_COLUMNS = [
    "evidence_id",
    "site_id",
    "site_name",
    "site_url",
    "evidence_category",
    "evidence_source_url",
    "evidence_text_excerpt",
    "policy_keyword_found",
    "risk_level",
    "reviewer",
    "reviewed_at",
    "notes",
]

SITE_SCREENING_RESULTS_COLUMNS = [
    "site_id",
    "site_name",
    "site_url",
    "site_type",
    "source_grade",
    "manual_review_required",
    "human_approval_required",
    "approval_status",
    "robots_status",
    "terms_status",
    "api_required",
    "login_required",
    "captcha_required",
    "anti_bot_risk",
    "public_html_access",
    "dynamic_rendering_risk",
    "reuse_restriction_risk",
    "collection_eligibility",
    "screening_decision",
    "screening_reason",
    "reviewer",
    "reviewed_at",
    "notes",
]

JOB_SITE_REGISTRY_COLUMNS = [
    "site_id",
    "site_name",
    "site_url",
    "site_type",
    "country",
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
    "database_right_risk",
    "copyright_risk",
    "reuse_restriction_risk",
    "collection_scope",
    "allowed_method",
    "decision",
    "decision_reason",
    "last_reviewed_at",
    "reviewer",
    "notes",
]

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

ATS_FINGERPRINTS_COLUMNS = [
    "ats_id",
    "source_id",
    "company_id",
    "company_name",
    "ats_type",
    "ats_confidence",
    "ats_detection_method",
    "collector_strategy",
    "json_endpoint_detected",
    "rss_detected",
    "sitemap_detected",
    "structure_stability",
    "maintenance_risk",
    "anti_bot_risk",
    "evidence_url",
    "review_status",
    "reviewer",
    "reviewed_at",
    "notes",
]

SOURCE_RELATIONSHIPS_COLUMNS = [
    "relationship_id",
    "source_node_id",
    "source_node_type",
    "target_node_id",
    "target_node_type",
    "relationship_type",
    "relationship_confidence",
    "discovered_via",
    "evidence_url",
    "is_canonical_candidate",
    "review_status",
    "created_at",
    "updated_at",
    "notes",
]

JD_LINEAGE_COLUMNS = [
    "lineage_id",
    "jd_id",
    "canonical_jd_id",
    "duplicate_cluster_id",
    "canonical_source_id",
    "observed_source_id",
    "source_priority_score",
    "lineage_type",
    "lineage_confidence",
    "first_seen_at",
    "last_seen_at",
    "content_hash",
    "title_company_hash",
    "url_hash",
    "notes",
]

SOURCE_HEALTH_COLUMNS = [
    "source_id",
    "source_url",
    "last_success_at",
    "last_failure_at",
    "failure_count",
    "last_status_code",
    "last_error_type",
    "structure_changed",
    "robots_changed",
    "terms_changed",
    "health_status",
    "next_check_at",
    "notes",
]

FRESHNESS_CHECKS_COLUMNS = [
    "check_id",
    "source_id",
    "jd_id",
    "check_type",
    "previous_hash",
    "current_hash",
    "change_detected",
    "jd_active_status",
    "checked_at",
    "notes",
]

OPERATION_RUNS_COLUMNS = [
    "run_id",
    "loop_type",
    "phase",
    "started_at",
    "finished_at",
    "status",
    "input_count",
    "output_count",
    "new_records",
    "updated_records",
    "failed_records",
    "skipped_records",
    "quality_summary",
    "notes",
]

RUNTIME_SOURCE_REGISTRY_COLUMNS = [
    "source_id",
    "company_id",
    "company_name",
    "source_name",
    "source_url",
    "source_type",
    "source_category",
    "country",
    "api_available",
    "api_status",
    "ats_type",
    "source_grade",
    "source_approval_status",
    "approval_status",
    "allowed_method",
    "robots_checked",
    "robots_allowed",
    "robots_target_path_status",
    "terms_checked",
    "terms_collection_policy",
    "login_required",
    "captcha_required",
    "anti_bot_risk",
    "public_html_access",
    "evidence_traceable",
    "collection_eligibility",
    "screening_decision",
    "ai_jd_ratio_estimate",
    "structure_quality",
    "maintenance_risk",
    "decision",
    "reason",
    "last_checked_at",
]

COMPANY_CANDIDATES_COLUMNS = [
    "company_id",
    "company_name",
    "country",
    "industry",
    "primary_domain",
    "hiring_signal_score",
    "business_ai_signal_score",
    "tech_signal_score",
    "market_signal_score",
    "evidence_quality_score",
    "total_score",
    "priority_tier",
    "validation_status",
    "review_notes",
    "created_at",
    "updated_at",
]

COMPANY_EVIDENCE_COLUMNS = [
    "evidence_id",
    "company_id",
    "company_name",
    "signal_category",
    "evidence_type",
    "evidence_url",
    "evidence_title",
    "evidence_summary",
    "source_type",
    "collected_at",
    "confidence",
    "notes",
]

TEMPLATE_FILES = {
    "runtime/raw_job_site_discovery.csv": RAW_JOB_SITE_DISCOVERY_COLUMNS,
    "runtime/site_policy_evidence.csv": SITE_POLICY_EVIDENCE_COLUMNS,
    "runtime/site_screening_results.csv": SITE_SCREENING_RESULTS_COLUMNS,
    "staging/job_site_registry_staging.csv": JOB_SITE_REGISTRY_COLUMNS,
    "master/job_source_registry.csv": JOB_SITE_REGISTRY_COLUMNS,
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
    "data/logs/collection_log.csv": JD_COLLECTION_LOG_COLUMNS,
    "runtime/jd_validation_errors.csv": JD_VALIDATION_ERRORS_COLUMNS,
    "runtime/quality_gate_report.csv": QUALITY_GATE_REPORT_COLUMNS,
    "runtime/runs.csv": RUNS_COLUMNS,
    "runtime/errors.csv": ERRORS_COLUMNS,
    "runtime/ats_fingerprints.csv": ATS_FINGERPRINTS_COLUMNS,
    "runtime/source_relationships.csv": SOURCE_RELATIONSHIPS_COLUMNS,
    "runtime/jd_lineage.csv": JD_LINEAGE_COLUMNS,
    "runtime/source_health.csv": SOURCE_HEALTH_COLUMNS,
    "runtime/freshness_checks.csv": FRESHNESS_CHECKS_COLUMNS,
    "runtime/operation_runs.csv": OPERATION_RUNS_COLUMNS,
    "runtime/source_registry.csv": RUNTIME_SOURCE_REGISTRY_COLUMNS,
    "configs/company_candidates.csv": COMPANY_CANDIDATES_COLUMNS,
    "configs/company_evidence.csv": COMPANY_EVIDENCE_COLUMNS,
    "runtime/company_candidates.csv": COMPANY_CANDIDATES_COLUMNS,
    "runtime/company_evidence.csv": COMPANY_EVIDENCE_COLUMNS,
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
