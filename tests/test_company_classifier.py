from src.company_discovery.company_classifier import classify_company_category


def test_company_classifier_detects_ai_transformation_company():
    result = classify_company_category({"industry": "finance", "review_notes": "building LLM systems"})

    assert result.decision in {"finance_ai_company", "ai_native_company"}
    assert result.allowed
