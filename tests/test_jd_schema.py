from src.processing.jd_schema import missing_jd_columns, validate_required_jd_fields
from src.utils.template_schemas import JD_COLUMNS


def _valid_jd_record():
    return {
        "jd_id": "jd-001",
        "company_id": "cmp-001",
        "company_name": "Example",
        "source_id": "src-001",
        "source_url": "https://example.com/careers",
        "job_url": "https://example.com/careers/ai-engineer",
        "job_title": "AI Engineer",
        "jd_text_clean": "Build reliable AI systems.",
        "collected_at": "2026-05-17T00:00:00Z",
        "source_grade": "A",
        "source_approval_status": "not_required",
    }


def test_jd_template_columns_are_complete():
    assert missing_jd_columns(JD_COLUMNS) == []


def test_validate_required_jd_fields_reports_missing_values():
    valid, missing = validate_required_jd_fields(_valid_jd_record())

    assert valid
    assert missing == []

    invalid = _valid_jd_record()
    invalid["job_url"] = ""

    valid, missing = validate_required_jd_fields(invalid)

    assert not valid
    assert missing == ["job_url"]
