from pathlib import Path

from src.utils.template_schemas import (
    JOB_SITE_REGISTRY_COLUMNS,
    RAW_JOB_SITE_DISCOVERY_COLUMNS,
    SITE_SCREENING_RESULTS_COLUMNS,
    SITE_POLICY_EVIDENCE_COLUMNS,
    missing_columns,
)


ROOT = Path(__file__).resolve().parents[1]


def test_raw_job_site_discovery_schema_matches_phase0_universe_discovery():
    path = ROOT / "runtime/raw_job_site_discovery.csv"

    assert missing_columns(path, RAW_JOB_SITE_DISCOVERY_COLUMNS) == []


def test_site_policy_evidence_schema_supports_traceable_review():
    path = ROOT / "runtime/site_policy_evidence.csv"

    assert missing_columns(path, SITE_POLICY_EVIDENCE_COLUMNS) == []


def test_job_site_staging_and_master_share_screening_schema():
    for relative_path in [
        "staging/job_site_registry_staging.csv",
        "master/job_source_registry.csv",
    ]:
        assert missing_columns(ROOT / relative_path, JOB_SITE_REGISTRY_COLUMNS) == []


def test_site_screening_results_schema_supports_phase0_5_review():
    path = ROOT / "runtime/site_screening_results.csv"

    assert missing_columns(path, SITE_SCREENING_RESULTS_COLUMNS) == []


def test_job_site_registry_schema_includes_strict_policy_fields():
    required_policy_fields = {
        "robots_txt_url",
        "robots_target_path_status",
        "terms_url",
        "terms_collection_policy",
        "api_required",
        "login_required",
        "captcha_required",
        "anti_bot_risk",
        "public_html_access",
        "reuse_restriction_risk",
        "decision",
        "decision_reason",
    }

    assert required_policy_fields.issubset(set(JOB_SITE_REGISTRY_COLUMNS))
