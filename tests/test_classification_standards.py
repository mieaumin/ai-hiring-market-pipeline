from src.standards.classification_loader import load_classification_standards, validate_classification_value


def test_classification_groups_include_required_values():
    standards = load_classification_standards()

    assert "official_api" in standards["source_category"]
    assert "A" in standards["source_grade"]
    assert "ai_transformation_company" in standards["company_category"]
    assert "AI Engineer" in standards["jd_role_group"]
    assert "canonical_jd" in standards["jd_lineage_type"]


def test_invalid_classification_value_fails():
    result = validate_classification_value("source_category", "foreign_market")

    assert not result.allowed
    assert "invalid_enum_value" in result.blockers
