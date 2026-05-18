from src.processing.jd_promotion import validate_jd_master_promotion


LONG_TEXT = "AI Engineer role builds LLM and RAG production systems. " * 10


def test_jd_without_title_fails_promotion():
    result = validate_jd_master_promotion(
        {
            "company_name": "Korea AI",
            "source_url": "https://example.com",
            "job_url": "https://example.com/job",
            "jd_text_clean": LONG_TEXT,
            "role_group": "AI Engineer",
            "validation_status": "labeled",
            "duplicate_cluster_id": "dup-1",
            "canonical_source_id": "src-1",
            "source_approval_status": "approved",
        }
    )

    assert not result.allowed
    assert "missing_title" in result.blockers


def test_short_jd_text_fails_promotion():
    result = validate_jd_master_promotion(
        {
            "job_title": "AI Engineer",
            "company_name": "Korea AI",
            "source_url": "https://example.com",
            "job_url": "https://example.com/job",
            "jd_text_clean": "short",
            "role_group": "AI Engineer",
            "validation_status": "labeled",
            "duplicate_cluster_id": "dup-1",
            "canonical_source_id": "src-1",
            "source_approval_status": "approved",
        }
    )

    assert not result.allowed
    assert "jd_text_clean_too_short" in result.blockers
