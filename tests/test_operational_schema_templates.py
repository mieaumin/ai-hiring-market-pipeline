import csv
from pathlib import Path

from src.utils.template_schemas import (
    ATS_FINGERPRINTS_COLUMNS,
    COMPANY_CANDIDATES_COLUMNS,
    COMPANY_EVIDENCE_COLUMNS,
    FRESHNESS_CHECKS_COLUMNS,
    JD_LINEAGE_COLUMNS,
    OPERATION_RUNS_COLUMNS,
    RUNTIME_SOURCE_REGISTRY_COLUMNS,
    SOURCE_HEALTH_COLUMNS,
    SOURCE_RELATIONSHIPS_COLUMNS,
    read_header,
)


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_HEADERS = {
    "runtime/ats_fingerprints.csv": ATS_FINGERPRINTS_COLUMNS,
    "runtime/source_relationships.csv": SOURCE_RELATIONSHIPS_COLUMNS,
    "runtime/jd_lineage.csv": JD_LINEAGE_COLUMNS,
    "runtime/source_health.csv": SOURCE_HEALTH_COLUMNS,
    "runtime/freshness_checks.csv": FRESHNESS_CHECKS_COLUMNS,
    "runtime/operation_runs.csv": OPERATION_RUNS_COLUMNS,
    "runtime/source_registry.csv": RUNTIME_SOURCE_REGISTRY_COLUMNS,
    "runtime/company_candidates.csv": COMPANY_CANDIDATES_COLUMNS,
    "runtime/company_evidence.csv": COMPANY_EVIDENCE_COLUMNS,
}


def _non_empty_lines(path: Path) -> list[str]:
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_operational_runtime_templates_exist_with_exact_headers():
    for relative_path, expected_header in EXPECTED_HEADERS.items():
        path = ROOT / relative_path

        assert path.exists(), relative_path
        assert read_header(path) == expected_header


def test_company_candidates_has_validation_status_exactly_once():
    header = read_header(ROOT / "runtime/company_candidates.csv")

    assert header.count("validation_status") == 1


def test_source_registry_contains_no_approved_rows_by_default():
    path = ROOT / "runtime/source_registry.csv"
    with path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert all(row.get("decision") != "approved" for row in rows)


def test_operational_templates_contain_no_fake_sample_rows():
    for relative_path in EXPECTED_HEADERS:
        path = ROOT / relative_path

        assert len(_non_empty_lines(path)) == 1, relative_path
