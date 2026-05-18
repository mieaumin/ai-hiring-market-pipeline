from scripts.run_approved_source_collection import NO_APPROVED_SOURCES_MESSAGE, filter_approved_sources


def _source(**overrides):
    row = {
        "source_id": "src-1",
        "source_url": "https://example.com/jobs.json",
        "source_grade": "A",
        "source_approval_status": "not_required",
        "decision": "approved",
        "robots_target_path_status": "allowed",
        "terms_collection_policy": "allowed",
        "login_required": "false",
        "captcha_required": "false",
        "anti_bot_risk": "low",
        "public_html_access": "true",
        "allowed_method": "public_json",
    }
    row.update(overrides)
    return row


def test_rejected_pending_and_unknown_sources_cannot_collect():
    rows = [
        _source(source_id="pending", source_approval_status="pending"),
        _source(source_id="rejected", source_approval_status="rejected"),
        _source(source_id="unknown", source_approval_status="unknown"),
    ]

    approved, blocked = filter_approved_sources(rows)

    assert approved == []
    assert len(blocked) == 3


def test_runner_filter_exits_safely_when_no_approved_sources_exist():
    approved, blocked = filter_approved_sources([])

    assert approved == []
    assert blocked == []
    assert NO_APPROVED_SOURCES_MESSAGE
