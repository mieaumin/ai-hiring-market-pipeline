"""Run approved-source-only JD collection from runtime/source_registry.csv.

The runner never discovers sources, approves sources, scrapes search results,
or bypasses restrictions. It exits successfully when no approved source exists.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.registry.source_promotion import validate_source_collection
from src.utils.template_schemas import ERRORS_COLUMNS, JD_COLUMNS, RUNS_COLUMNS


NO_APPROVED_SOURCES_MESSAGE = "No approved sources found. Collection skipped safely."


def read_csv_rows(path: Path) -> list[dict]:
    """Read CSV rows from a local path."""
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, fieldnames: list[str], rows: list[dict], append: bool = True) -> None:
    """Write rows to CSV, preserving headers."""
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists() and path.stat().st_size > 0
    mode = "a" if append and file_exists else "w"
    with path.open(mode, encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if mode == "w":
            writer.writeheader()
        writer.writerows(rows)


def filter_approved_sources(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split source rows into collectable and blocked rows."""
    approved: list[dict] = []
    blocked: list[dict] = []
    for row in rows:
        decision = validate_source_collection(row)
        if decision.allowed:
            approved.append(row)
        else:
            blocked.append({**row, "blocking_reason": "|".join(decision.blockers)})
    return approved, blocked


def select_collector(source_row: dict):
    """Select a conservative collector by allowed method or ATS type."""
    allowed_method = str(source_row.get("allowed_method", "")).strip().lower()
    ats_type = str(source_row.get("ats_type", "")).strip().lower()

    if "greenhouse" in {allowed_method, ats_type}:
        from src.collectors.greenhouse_collector import GreenhouseCollector

        return GreenhouseCollector()
    if "lever" in {allowed_method, ats_type}:
        from src.collectors.lever_collector import LeverCollector

        return LeverCollector()
    if "ashby" in {allowed_method, ats_type}:
        from src.collectors.ashby_collector import AshbyCollector

        return AshbyCollector()
    if "rss" in allowed_method:
        from src.collectors.rss_collector import RssCollector

        return RssCollector()
    if "sitemap" in allowed_method:
        from src.collectors.sitemap_collector import SitemapCollector

        return SitemapCollector()
    if "json" in allowed_method or "api" in allowed_method:
        from src.collectors.public_json_collector import PublicJsonCollector

        return PublicJsonCollector()

    from src.collectors.public_html_collector import PublicHtmlCollector

    return PublicHtmlCollector()


def make_run_row(
    run_id: str,
    started_at: str,
    finished_at: str,
    status: str,
    input_count: int,
    output_count: int,
    error_count: int,
    notes: str,
) -> dict:
    """Build one run-log row."""
    return {
        "run_id": run_id,
        "phase_name": "phase4_approved_source_collection",
        "started_at": started_at,
        "finished_at": finished_at,
        "status": status,
        "input_count": str(input_count),
        "output_count": str(output_count),
        "error_count": str(error_count),
        "notes": notes,
    }


def make_error_row(run_id: str, source_row: dict, error_type: str, message: str) -> dict:
    """Build one runtime error row."""
    return {
        "error_id": f"error_{uuid4().hex[:12]}",
        "run_id": run_id,
        "phase_name": "phase4_approved_source_collection",
        "record_id": source_row.get("source_id", ""),
        "error_type": error_type,
        "error_message": message,
        "retryable": "false",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "notes": source_row.get("source_url", ""),
    }


def run_approved_source_collection() -> tuple[int, int, int]:
    """Run collection for approved source rows only."""
    started_at = datetime.now(timezone.utc).isoformat()
    run_id = f"approved_source_collection_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    registry_path = ROOT / "runtime/source_registry.csv"
    raw_output_path = ROOT / "data/raw/raw_jds.csv"
    runs_path = ROOT / "runtime/runs.csv"
    errors_path = ROOT / "runtime/errors.csv"

    source_rows = read_csv_rows(registry_path)
    approved_sources, blocked_sources = filter_approved_sources(source_rows)
    error_rows = [
        make_error_row(run_id, row, "source_not_collectable", row.get("blocking_reason", "blocked"))
        for row in blocked_sources
    ]

    if not approved_sources:
        finished_at = datetime.now(timezone.utc).isoformat()
        write_csv_rows(
            runs_path,
            RUNS_COLUMNS,
            [
                make_run_row(
                    run_id,
                    started_at,
                    finished_at,
                    "skipped",
                    len(source_rows),
                    0,
                    len(error_rows),
                    NO_APPROVED_SOURCES_MESSAGE,
                )
            ],
        )
        if error_rows:
            write_csv_rows(errors_path, ERRORS_COLUMNS, error_rows)
        print(NO_APPROVED_SOURCES_MESSAGE)
        return 0, 0, len(error_rows)

    collected_rows: list[dict] = []
    for source_row in approved_sources:
        try:
            collector = select_collector(source_row)
            collected_rows.extend(collector.run(source_row))
        except Exception as exc:  # noqa: BLE001 - fail per source and log.
            error_rows.append(make_error_row(run_id, source_row, "collection_failed", str(exc)))

    if collected_rows:
        write_csv_rows(raw_output_path, JD_COLUMNS, collected_rows)
    if error_rows:
        write_csv_rows(errors_path, ERRORS_COLUMNS, error_rows)

    finished_at = datetime.now(timezone.utc).isoformat()
    status = "completed" if not error_rows else "completed_with_warnings"
    write_csv_rows(
        runs_path,
        RUNS_COLUMNS,
        [
            make_run_row(
                run_id,
                started_at,
                finished_at,
                status,
                len(source_rows),
                len(collected_rows),
                len(error_rows),
                "approved-source-only collection finished",
            )
        ],
    )
    print(f"Approved-source-only collection saved {len(collected_rows)} JD row(s).")
    return len(approved_sources), len(collected_rows), len(error_rows)


def main() -> int:
    run_approved_source_collection()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
