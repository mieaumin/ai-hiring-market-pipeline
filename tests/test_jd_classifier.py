from src.processing.jd_classifier import classify_jd_role


def test_jd_classifier_assigns_ai_engineer():
    result = classify_jd_role(
        {"job_title": "AI Engineer", "jd_text_clean": "Build RAG and MLOps systems with Python."}
    )

    assert result.decision == "AI Engineer"
    assert result.allowed
