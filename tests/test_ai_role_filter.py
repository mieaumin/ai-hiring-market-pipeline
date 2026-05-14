from src.processing.ai_role_filter import is_ai_related_jd, match_ai_keywords


def test_match_ai_keywords_with_explicit_list():
    matches = match_ai_keywords("We need an LLM Engineer with Python.", ["LLM", "Python", "SQL"])

    assert matches == ["LLM", "Python"]


def test_is_ai_related_jd():
    record = {"title": "AI Engineer", "description_clean": "Build RAG services with Python."}

    assert is_ai_related_jd(record, ["AI Engineer", "RAG"])

