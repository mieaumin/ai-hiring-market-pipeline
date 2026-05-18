"""Validate status values and allowed transitions."""

from __future__ import annotations

from pathlib import Path

from src.standards.classification_loader import DecisionResult, load_yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATUS_PATH = ROOT / "configs/status_standards.yaml"


def load_status_standards(path: str | Path = DEFAULT_STATUS_PATH) -> dict:
    """Load status standards."""
    return load_yaml(path)


def status_values(group: str, standards: dict | None = None) -> set[str]:
    """Return allowed status values for a group."""
    standards = standards or load_status_standards()
    group_data = standards.get(group, {})
    if isinstance(group_data, dict):
        return set(group_data.get("values", []))
    return set(group_data or [])


def validate_status_value(group: str, value: str, standards: dict | None = None) -> DecisionResult:
    """Validate one status value."""
    normalized = str(value or "").strip()
    allowed_values = status_values(group, standards)
    if normalized in allowed_values:
        return DecisionResult(
            decision="valid",
            allowed=True,
            reasons=[f"{group}:{normalized} is allowed"],
            confidence="high",
        )
    return DecisionResult(
        decision="invalid",
        allowed=False,
        reasons=[f"{group}:{normalized} is not allowed"],
        blockers=["invalid_status_value"],
        confidence="high",
    )


def validate_transition(
    group: str,
    current_status: str,
    next_status: str,
    standards: dict | None = None,
) -> DecisionResult:
    """Validate a status transition."""
    standards = standards or load_status_standards()
    group_data = standards.get(group, {})
    transitions = group_data.get("transitions", {}) if isinstance(group_data, dict) else {}
    current = str(current_status or "").strip()
    next_value = str(next_status or "").strip()

    if current not in status_values(group, standards):
        return DecisionResult(
            decision="invalid_transition",
            allowed=False,
            reasons=[f"{current} is not a valid {group} status"],
            blockers=["invalid_current_status"],
            confidence="high",
        )
    if next_value not in status_values(group, standards):
        return DecisionResult(
            decision="invalid_transition",
            allowed=False,
            reasons=[f"{next_value} is not a valid {group} status"],
            blockers=["invalid_next_status"],
            confidence="high",
        )
    if next_value in transitions.get(current, []):
        return DecisionResult(
            decision="transition_allowed",
            allowed=True,
            reasons=[f"{group}:{current}->{next_value} is allowed"],
            confidence="high",
        )
    return DecisionResult(
        decision="transition_blocked",
        allowed=False,
        reasons=[f"{group}:{current}->{next_value} is not allowed"],
        blockers=["invalid_status_transition"],
        confidence="high",
    )
