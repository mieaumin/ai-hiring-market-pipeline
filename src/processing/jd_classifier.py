"""JD role and lineage classification helpers."""

from __future__ import annotations

from src.labeling.rule_based_labeler import assign_role_group
from src.standards.classification_loader import DecisionResult, validate_classification_value


def classify_jd_role(record: dict) -> DecisionResult:
    """Classify a JD into a role group with transparent rules."""
    text = " ".join(
        str(record.get(field, ""))
        for field in ["job_title", "title", "jd_text_clean", "description_clean", "description"]
    )
    role_group, matches = assign_role_group(text)
    role_group = role_group or "Other/Unknown"
    validation = validate_classification_value("jd_role_group", role_group)
    allowed = validation.allowed and role_group != "Other/Unknown"
    return DecisionResult(
        decision=role_group,
        allowed=allowed,
        reasons=[f"matched:{'|'.join(matches)}"] if matches else ["no target AI role keyword matched"],
        blockers=[] if allowed else ["role_group_unknown"],
        confidence="high" if len(matches) >= 2 else "medium" if matches else "unknown",
    )


def classify_jd_lineage(record: dict) -> DecisionResult:
    """Classify JD lineage type."""
    explicit = str(record.get("lineage_type", "")).strip()
    if explicit:
        return validate_classification_value("jd_lineage_type", explicit)
    if record.get("canonical_source_id"):
        lineage = "canonical_jd"
    elif str(record.get("source_category", "")).strip() == "aggregator":
        lineage = "aggregator_jd"
    else:
        lineage = "unknown"
    return DecisionResult(
        decision=lineage,
        allowed=lineage != "unknown",
        reasons=[f"inferred jd_lineage_type={lineage}"],
        blockers=[] if lineage != "unknown" else ["jd_lineage_unknown"],
        confidence="medium" if lineage != "unknown" else "unknown",
    )
