from src.processing.ai_role_filter import is_ai_related_jd, match_ai_keywords


def test_match_ai_keywords_with_explicit_list():
    matches = match_ai_keywords("We need an LLM Engineer with Python.", ["LLM", "Python", "SQL"])

    assert matches == ["LLM", "Python"]


def test_is_ai_related_jd():
    record = {"title": "AI Engineer", "description_clean": "Build RAG services with Python."}

    assert is_ai_related_jd(record, ["AI Engineer", "RAG"])


def test_korean_ai_keyword_match():
    record = {
        "job_title": "\ub370\uc774\ud130 \ubd84\uc11d\uac00",
        "jd_text_clean": "SQL\uacfc \ub370\uc774\ud130 \ubd84\uc11d \uc5ed\ub7c9\uc774 \ud544\uc694\ud569\ub2c8\ub2e4.",
    }

    assert is_ai_related_jd(
        record,
        ["\ub370\uc774\ud130 \ubd84\uc11d\uac00", "\ub370\uc774\ud130 \ubd84\uc11d"],
    )
