from src.processing.deduplicator import deduplicate, mark_duplicates


def test_deduplicate_by_url_company_and_title():
    records = [
        {"source_url": "https://example.com/1", "company": "A Corp", "title": "AI Engineer"},
        {"source_url": "https://example.com/1", "company": "A Corp", "title": "AI Engineer"},
        {"source_url": "https://example.com/2", "company": "A Corp", "title": "AI Engineer"},
    ]

    unique = deduplicate(records)

    assert len(unique) == 2
    assert unique[0]["duplicate_cluster_id"].startswith("dup_")


def test_mark_duplicates_detects_duplicate_jd():
    records = [
        {
            "job_url": "https://example.com/1",
            "company_name": "A Corp",
            "job_title": "AI Engineer",
            "jd_text_clean": "Build AI systems.",
        },
        {
            "job_url": "https://example.com/1",
            "company_name": "A Corp",
            "job_title": "AI Engineer",
            "jd_text_clean": "Build AI systems.",
        },
    ]

    marked = mark_duplicates(records)

    assert marked[0]["is_duplicate"] == "false"
    assert marked[1]["is_duplicate"] == "true"
    assert marked[1]["validation_status"] == "duplicate"
