"""Source verification helpers.

No live verification is performed here.
"""

from __future__ import annotations

from src.registry.source_grading import can_move_to_master, validate_source_approval_fields
from src.utils.template_schemas import SOURCE_REGISTRY_COLUMNS


def validate_source_registry_row(row: dict) -> tuple[bool, list[str]]:
    """Validate required source registry fields and approval fields."""
    missing = [column for column in SOURCE_REGISTRY_COLUMNS if column not in row]
    approval_valid, approval_reason = validate_source_approval_fields(row)
    errors = missing[:]
    if not approval_valid:
        errors.append(approval_reason)
    return not errors, errors


def source_is_promotable(row: dict, automated_checks_passed: bool = False) -> bool:
    """Return whether a source can be promoted to master."""
    return can_move_to_master(row, automated_checks_passed=automated_checks_passed)

