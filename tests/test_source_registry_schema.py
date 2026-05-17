from src.registry.source_verification import source_is_promotable, validate_source_registry_row
from src.utils.template_schemas import SOURCE_REGISTRY_COLUMNS


def _source_row(**overrides):
    row = {column: "" for column in SOURCE_REGISTRY_COLUMNS}
    row.update(
        {
            "source_id": "src-001",
            "company_id": "cmp-001",
            "company_name": "Example",
            "source_name": "Example Careers",
            "source_url": "https://example.com/careers",
            "source_type": "official",
            "source_grade": "A",
            "manual_review_required": "false",
            "human_approval_required": "false",
            "approval_status": "not_required",
        }
    )
    row.update(overrides)
    return row


def test_source_registry_row_contains_required_schema_fields():
    valid, errors = validate_source_registry_row(_source_row())

    assert valid
    assert errors == []


def test_source_registry_promotion_follows_strict_grade_policy():
    assert source_is_promotable(_source_row(), automated_checks_passed=True)

    pending_grade_b = _source_row(
        source_grade="B",
        manual_review_required="true",
        human_approval_required="true",
        approval_status="pending",
    )
    approved_grade_b = dict(pending_grade_b, approval_status="approved")

    assert not source_is_promotable(pending_grade_b, automated_checks_passed=True)
    assert source_is_promotable(approved_grade_b, automated_checks_passed=False)
