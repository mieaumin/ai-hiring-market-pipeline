from src.registry.source_promotion import validate_source_collection, validate_source_master_promotion


def _approved_source(**overrides):
    row = {
        "source_id": "src-1",
        "source_url": "https://example.com/jobs",
        "source_grade": "A",
        "source_approval_status": "not_required",
        "approval_status": "not_required",
        "decision": "approved",
        "robots_target_path_status": "allowed",
        "terms_collection_policy": "allowed",
        "login_required": "false",
        "captcha_required": "false",
        "anti_bot_risk": "low",
        "public_html_access": "true",
    }
    row.update(overrides)
    return row


def test_approved_grade_a_source_can_collect_only_without_blockers():
    result = validate_source_collection(_approved_source())

    assert result.allowed


def test_approved_grade_b_and_c_sources_can_collect_without_blockers():
    for grade in ["B", "C"]:
        result = validate_source_collection(
            _approved_source(source_grade=grade, source_approval_status="approved")
        )

        assert result.allowed


def test_pending_source_cannot_collect():
    result = validate_source_collection(_approved_source(source_approval_status="pending"))

    assert not result.allowed
    assert "approval pending" in result.blockers


def test_grade_d_requires_review_and_cannot_collect():
    result = validate_source_collection(
        _approved_source(source_grade="D", source_approval_status="approved")
    )

    assert not result.allowed
    assert "source grade not allowed" in result.blockers


def test_grade_e_and_f_sources_are_rejected_for_collection():
    for grade in ["E", "F"]:
        result = validate_source_collection(
            _approved_source(source_grade=grade, source_approval_status="approved")
        )

        assert not result.allowed


def test_source_master_promotion_requires_no_blockers_and_evidence():
    result = validate_source_master_promotion(
        {
            "source_grade": "C",
            "approval_status": "approved",
            "collection_eligibility": "eligible",
            "screening_decision": "approved",
            "robots_target_path_status": "allowed",
            "terms_collection_policy": "allowed",
            "login_required": "false",
            "captcha_required": "false",
            "anti_bot_risk": "low",
            "evidence_traceable": "true",
        }
    )

    assert result.allowed
