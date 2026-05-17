from pathlib import Path

from src.utils.template_schemas import TEMPLATE_FILES, missing_columns


ROOT = Path(__file__).resolve().parents[1]


def test_required_csv_templates_exist_and_include_required_columns():
    failures = {}
    for relative_path, required_columns in TEMPLATE_FILES.items():
        path = ROOT / relative_path
        missing = missing_columns(path, required_columns)
        if not path.exists() or missing:
            failures[relative_path] = missing

    assert failures == {}
