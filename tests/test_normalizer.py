from src.processing.normalizer import normalize_jd


def test_normalize_jd_strips_html():
    record = {
        "source_url": "https://example.com/job/1",
        "company": " Example AI ",
        "title": " ML Engineer ",
        "location": " Seoul ",
        "description": "<p>Build ML systems.</p>",
        "collected_at": "2026-05-15T00:00:00Z",
    }

    normalized = normalize_jd(record)

    assert normalized["company"] == "Example AI"
    assert normalized["title"] == "ML Engineer"
    assert normalized["description_clean"] == "Build ML systems."

