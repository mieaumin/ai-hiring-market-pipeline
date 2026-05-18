from src.registry.source_status_machine import can_transition_source_approval


def test_source_status_blocks_direct_not_checked_to_approved():
    result = can_transition_source_approval("not_checked", "approved")

    assert not result.allowed


def test_source_status_allows_pending_to_approved():
    result = can_transition_source_approval("pending", "approved")

    assert result.allowed
