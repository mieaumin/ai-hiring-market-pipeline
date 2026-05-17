from src.registry.site_screening import detect_blockers, screen_site


def test_robots_disallow_blocks_approval():
    result = screen_site({"site_id": "s1", "site_name": "Example", "robots_status": "disallowed"})

    assert result.screening_decision == "rejected"
    assert result.source_grade == "F"
    assert "robots_disallow_detected" in result.screening_reason


def test_captcha_blocks_approval():
    result = screen_site({"site_id": "s1", "captcha_required": "true"})

    assert result.screening_decision == "rejected"
    assert result.source_grade == "E"
    assert "captcha_required" in result.screening_reason


def test_login_requirement_blocks_approval():
    blockers = detect_blockers({"login_required": "true"})

    assert "login_required" in blockers


def test_high_anti_bot_risk_blocks_approval():
    result = screen_site({"anti_bot_risk": "high"})

    assert result.screening_decision == "rejected"
    assert "high_anti_bot_risk" in result.screening_reason


def test_grade_d_requires_manual_or_legal_review():
    result = screen_site({"source_grade": "D", "site_id": "s1"})

    assert result.collection_eligibility == "needs_review"
    assert result.screening_decision == "needs_legal_review"
    assert result.screening_reason


def test_grade_e_and_f_are_rejected():
    for grade in ["E", "F"]:
        result = screen_site({"source_grade": grade, "site_id": f"s-{grade}"})

        assert result.collection_eligibility == "excluded"
        assert result.screening_decision == "rejected"
        assert result.screening_reason


def test_terms_prohibition_from_evidence_blocks_approval():
    result = screen_site(
        {"site_id": "s1", "site_name": "Example"},
        evidence_rows=[{"evidence_text_excerpt": "automated collection prohibited"}],
    )

    assert result.screening_decision == "rejected"
    assert "terms_prohibit_automated_collection" in result.screening_reason
