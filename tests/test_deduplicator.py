from src.processing.deduplicator import deduplicate


def test_deduplicate_by_url_company_and_title():
    records = [
        {"source_url": "https://example.com/1", "company": "A Corp", "title": "AI Engineer"},
        {"source_url": "https://example.com/1", "company": "A Corp", "title": "AI Engineer"},
        {"source_url": "https://example.com/2", "company": "A Corp", "title": "AI Engineer"},
    ]

    unique = deduplicate(records)

    assert len(unique) == 2

