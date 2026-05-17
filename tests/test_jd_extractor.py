from src.processing.jd_extractor import extract_jd_from_html


def _source_row(**overrides):
    row = {
        "company_id": "cmp-001",
        "company_name": "Example AI",
        "source_id": "src-001",
        "source_url": "https://example.com/jobs/ai-engineer",
        "source_grade": "A",
        "approval_status": "not_required",
    }
    row.update(overrides)
    return row


def test_extract_jd_from_html_builds_traceable_raw_jd_row():
    html = """
    <html>
      <body>
        <h1>AI Engineer</h1>
        <p>Build LLM, RAG, and machine learning systems with Python.</p>
      </body>
    </html>
    """

    row = extract_jd_from_html(html, _source_row())

    assert row["company_id"] == "cmp-001"
    assert row["company_name"] == "Example AI"
    assert row["source_id"] == "src-001"
    assert row["job_title"] == "AI Engineer"
    assert row["role_group"] == "AI Engineer"
    assert row["source_approval_status"] == "not_required"
    assert row["validation_status"] == "raw"
    assert row["content_hash"]
    assert row["duplicate_key"]


def test_jd_without_title_is_marked_failed_by_extractor():
    row = extract_jd_from_html("<p>Machine learning role details.</p>", _source_row())

    assert row["validation_status"] == "failed"
    assert "missing_title" in row["failure_reason"]
