from src.processing.jd_quality_gate import evaluate_quality_gate, source_approval_is_valid


LONG_AI_TEXT = (
    "This AI Engineer role builds machine learning and LLM systems for production. "
    "The work includes Python services, model evaluation, RAG pipelines, monitoring, "
    "data quality review, and close collaboration with product teams. "
    "The description is intentionally long enough to pass the minimum text threshold."
)


def _jd_record(**overrides):
    record = {
        "jd_id": "jd-001",
        "company_id": "cmp-001",
        "company_name": "Example",
        "source_id": "src-001",
        "source_url": "https://example.com/careers",
        "job_url": "https://example.com/careers/ai-engineer",
        "job_title": "AI Engineer",
        "role_group": "AI Engineer",
        "jd_text_clean": LONG_AI_TEXT,
        "collected_at": "2026-05-17T00:00:00Z",
        "source_grade": "A",
        "source_approval_status": "not_required",
        "content_hash": "abc123",
        "duplicate_key": "example-ai-engineer",
    }
    record.update(overrides)
    return record


def test_grade_a_jd_passes_quality_gate_when_source_checks_are_valid():
    result = evaluate_quality_gate(_jd_record())

    assert result.passed
    assert result.status == "valid"


def test_jd_cannot_pass_quality_gate_if_source_approval_is_invalid():
    record = _jd_record(source_grade="B", source_approval_status="pending")

    assert not source_approval_is_valid(record)

    result = evaluate_quality_gate(record)

    assert not result.passed
    assert "source_approval_invalid" in result.reasons


def test_jd_without_title_fails_quality_gate():
    result = evaluate_quality_gate(_jd_record(job_title=""))

    assert not result.passed
    assert any(reason.startswith("missing_required_fields") for reason in result.reasons)


def test_grades_b_c_need_approved_source_status_for_jd_quality_gate():
    for grade in ["B", "C"]:
        assert source_approval_is_valid(
            _jd_record(source_grade=grade, source_approval_status="approved")
        )


def test_grade_d_e_and_f_sources_never_pass_jd_source_approval():
    for grade in ["D", "E", "F"]:
        assert not source_approval_is_valid(
            _jd_record(source_grade=grade, source_approval_status="approved")
        )


def test_duplicate_jd_fails_quality_gate_after_first_seen_key():
    seen = {"example-ai-engineer"}
    result = evaluate_quality_gate(_jd_record(), seen_duplicate_keys=seen)

    assert not result.passed
    assert "duplicate_jd" in result.reasons
