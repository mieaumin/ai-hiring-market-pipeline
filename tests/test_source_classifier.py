from src.registry.source_classifier import classify_source_category, classify_source_grade


def test_source_classifier_detects_ats_category():
    result = classify_source_category({"ats_type": "greenhouse"})

    assert result.decision == "official_ats"
    assert result.allowed


def test_source_grade_d_requires_review_when_policy_is_unclear():
    result = classify_source_grade({"source_url": "https://example.com/jobs"})

    assert result.decision == "D"
    assert not result.allowed
