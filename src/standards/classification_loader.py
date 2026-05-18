"""Load and validate shared classification standards."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CLASSIFICATION_PATH = ROOT / "configs/classification_standards.yaml"


@dataclass(frozen=True)
class DecisionResult:
    """Structured, explainable decision object."""

    decision: str
    allowed: bool
    reasons: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    confidence: str = "unknown"


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file from disk."""
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_classification_standards(path: str | Path = DEFAULT_CLASSIFICATION_PATH) -> dict[str, Any]:
    """Load classification standards."""
    return load_yaml(path)


def allowed_values(group: str, standards: dict[str, Any] | None = None) -> set[str]:
    """Return allowed values for one classification group."""
    standards = standards or load_classification_standards()
    values = standards.get(group, {})
    if isinstance(values, dict):
        return set(values)
    return set(values or [])


def validate_classification_value(
    group: str,
    value: str,
    standards: dict[str, Any] | None = None,
) -> DecisionResult:
    """Validate that a value belongs to a classification group."""
    normalized = str(value or "").strip()
    allowed = allowed_values(group, standards)
    if normalized in allowed:
        return DecisionResult(
            decision="valid",
            allowed=True,
            reasons=[f"{group}:{normalized} is allowed"],
            confidence="high",
        )
    return DecisionResult(
        decision="invalid",
        allowed=False,
        reasons=[f"{group}:{normalized} is not in standards"],
        blockers=["invalid_enum_value"],
        confidence="high",
    )
