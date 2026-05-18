from src.standards.status_validator import validate_status_value, validate_transition


def test_invalid_status_value_fails():
    result = validate_status_value("source_approval_status", "unknown")

    assert not result.allowed
    assert "invalid_status_value" in result.blockers


def test_invalid_state_transition_fails():
    result = validate_transition("site_review_status", "not_checked", "screened")

    assert not result.allowed
    assert "invalid_status_transition" in result.blockers


def test_valid_source_approval_transition_passes():
    result = validate_transition("source_approval_status", "pending", "approved")

    assert result.allowed
