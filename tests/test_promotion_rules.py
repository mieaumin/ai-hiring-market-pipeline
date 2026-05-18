from src.standards.promotion_validator import (
    validate_company_to_master,
    validate_jd_to_master,
    validate_raw_site_to_screening,
    validate_site_screening_to_master,
)


def test_raw_site_cannot_be_already_approved_before_screening():
    result = validate_raw_site_to_screening(
        {
            "site_id": "site-1",
            "site_url": "https://example.com",
            "site_domain": "example.com",
            "discovery_route": "manual",
            "review_status": "approved",
        }
    )

    assert not result.allowed
    assert "raw_discovery_cannot_already_be_approved" in result.blockers


def test_site_screening_requires_traceable_evidence():
    result = validate_site_screening_to_master(
        {
            "source_grade": "A",
            "approval_status": "not_required",
            "collection_eligibility": "eligible",
            "screening_decision": "approved",
            "robots_target_path_status": "allowed",
            "terms_collection_policy": "allowed",
        }
    )

    assert not result.allowed
    assert "missing_traceable_evidence" in result.blockers


def test_company_master_promotion_requires_korean_relevance():
    result = validate_company_to_master(
        {
            "total_score": "20",
            "validation_status": "approved_for_source_discovery",
            "evidence_quality_score": "4",
            "country": "US",
        }
    )

    assert not result.allowed
    assert "company_not_korean_or_korea_relevant" in result.blockers


def test_jd_master_promotion_requires_title_and_long_text():
    result = validate_jd_to_master(
        {
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
    assert "missing_title" in result.blockers
    assert "jd_text_clean_too_short" in result.blockers
