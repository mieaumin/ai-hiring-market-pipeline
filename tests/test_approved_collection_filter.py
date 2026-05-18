from scripts.run_approved_source_collection import (
    NO_APPROVED_SOURCES_MESSAGE,
    filter_approved_sources,
)


def _source_row(**overrides):
    row = {
        "source_id": "src-001",
        "source_url": "https://example.com/careers",
        "decision": "approved",
        "source_grade": "A",
        "approval_status": "not_required",
        "robots_target_path_status": "allowed",
        "terms_collection_policy": "allowed",
        "login_required": "false",
        "captcha_required": "false",
        "anti_bot_risk": "none",
        "public_html_access": "true",
    }
    row.update(overrides)
    return row


def test_filter_collectable_sources_keeps_only_eligible_rows():
    eligible, blocked = filter_approved_sources(
        [
            _source_row(source_id="src-ok"),
            _source_row(source_id="src-pending", source_approval_status="pending"),
        ]
    )

    assert [row["source_id"] for row in eligible] == ["src-ok"]
    assert [row["source_id"] for row in blocked] == ["src-pending"]
    assert "approval pending" in blocked[0]["blocking_reason"]


def test_no_approved_source_means_collection_skipped_safely():
    eligible, blocked = filter_approved_sources(
        [_source_row(decision="needs_manual_review", source_approval_status="pending")]
    )

    assert eligible == []
    assert blocked
    assert NO_APPROVED_SOURCES_MESSAGE == "No approved sources found. Collection skipped safely."
