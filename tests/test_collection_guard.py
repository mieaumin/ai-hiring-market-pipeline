from src.registry.collection_guard import (
    explain_blocking_reason,
    is_source_collectable,
    validate_source_before_collection,
)


def _source_row(**overrides):
    row = {
        "decision": "approved",
        "source_grade": "A",
        "approval_status": "not_required",
        "robots_target_path_status": "allowed",
        "terms_collection_policy": "allowed",
        "login_required": "false",
        "captcha_required": "false",
        "anti_bot_risk": "low",
        "public_html_access": "true",
    }
    row.update(overrides)
    return row


def test_grade_a_not_required_can_collect_if_checks_pass():
    row = _source_row(source_grade="A", approval_status="not_required")

    assert is_source_collectable(row)
    assert validate_source_before_collection(row) == (True, [])


def test_grades_b_c_d_cannot_collect_unless_approved():
    for grade in ["B", "C", "D"]:
        assert not is_source_collectable(_source_row(source_grade=grade, approval_status="pending"))
        assert is_source_collectable(_source_row(source_grade=grade, approval_status="approved"))


def test_grade_e_and_f_cannot_collect():
    for grade in ["E", "F"]:
        row = _source_row(source_grade=grade, approval_status="approved")

        assert not is_source_collectable(row)
        assert "source grade not allowed" in explain_blocking_reason(row)


def test_registry_policy_blocks_collection_risks():
    cases = [
        ("robots_target_path_status", "disallowed", "robots disallowed"),
        ("terms_collection_policy", "not_allowed", "terms disallowed"),
        ("login_required", "true", "login required"),
        ("captcha_required", "true", "captcha required"),
        ("anti_bot_risk", "high", "anti-bot high"),
        ("public_html_access", "false", "public HTML unavailable"),
    ]

    for field, value, reason in cases:
        row = _source_row(**{field: value})

        assert not is_source_collectable(row)
        assert reason in explain_blocking_reason(row)


def test_api_required_blocks_collection_until_approved():
    row = _source_row(api_required="true", approval_status="not_required")

    assert not is_source_collectable(row)
    assert "API approval pending" in explain_blocking_reason(row)


def test_api_source_type_blocks_collection_until_approved():
    row = _source_row(source_type="official_api", approval_status="not_required")

    assert not is_source_collectable(row)
    assert "API approval pending" in explain_blocking_reason(row)
