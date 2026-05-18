"""Company classification helpers for Korean AI hiring likelihood."""

from __future__ import annotations

from src.standards.classification_loader import DecisionResult, validate_classification_value


AI_TRANSFORMATION_INDUSTRIES = {
    "finance",
    "banking",
    "healthcare",
    "manufacturing",
    "commerce",
    "retail",
    "mobility",
    "robotics",
}


def classify_company_category(row: dict) -> DecisionResult:
    """Classify a company category without approving the company."""
    explicit = str(row.get("company_category", "")).strip()
    if explicit:
        validation = validate_classification_value("company_category", explicit)
        allowed = validation.allowed and explicit != "unknown"
        return DecisionResult(
            decision=explicit,
            allowed=allowed,
            reasons=validation.reasons,
            blockers=[] if allowed else ["company_category_unknown"],
            confidence="high" if validation.allowed else "unknown",
        )

    industry = str(row.get("industry", "")).strip().lower()
    company_type = str(row.get("company_type", "")).strip().lower()
    notes = " ".join(str(row.get(field, "")) for field in ["company_name", "review_notes", "notes"]).lower()

    if "llm" in notes or "rag" in notes or "ai native" in notes:
        category = "ai_native_company"
    elif "solution" in notes or company_type == "ai_solution":
        category = "ai_solution_company"
    elif any(keyword in notes for keyword in ["mlops", "cloud", "data platform"]):
        category = "data_cloud_mlops_company"
    elif "health" in industry:
        category = "healthcare_ai_company"
    elif "finance" in industry or "bank" in industry:
        category = "finance_ai_company"
    elif "manufacturing" in industry or "robot" in industry:
        category = "manufacturing_robotics_ai_company"
    elif "commerce" in industry or "marketing" in industry or "retail" in industry:
        category = "commerce_marketing_ai_company"
    elif "enterprise" in company_type or "large" in company_type:
        category = "large_enterprise_ai_org"
    elif industry in AI_TRANSFORMATION_INDUSTRIES:
        category = "ai_transformation_company"
    else:
        category = "unknown"

    return DecisionResult(
        decision=category,
        allowed=category != "unknown",
        reasons=[f"inferred company_category={category}"],
        blockers=[] if category != "unknown" else ["company_category_unknown"],
        confidence="medium" if category != "unknown" else "unknown",
    )
