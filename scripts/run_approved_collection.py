"""Run approved-source-only JD collection.

This runner reads master/source_registry_master.csv, filters through the local
collection guard, and only then instantiates collectors. If no eligible source
exists, no network call is made.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.registry.collection_guard import explain_blocking_reason, is_source_collectable
from src.utils.template_schemas import ERRORS_COLUMNS, JD_COLLECTION_LOG_COLUMNS, JD_COLUMNS


NO_ELIGIBLE_MESSAGE = "No approved crawl-eligible sources found. Collection skipped."


def read_csv_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, fieldnames: list[str], rows: list[dict], append: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists() and path.stat().st_size > 0
    mode = "a" if append and file_exists else "w"
    with path.open(mode, encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if mode == "w":
            writer.writeheader()
        writer.writerows(rows)


def filter_collectable_sources(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    eligible = []
    blocked = []
    for row in rows:
        if is_source_collectable(row):
            eligible.append(row)
        else:
            blocked.append({**row, "blocking_reason": "|".join(explain_blocking_reason(row))})
    return eligible, blocked


def make_collector(source_row: dict):
    source_type = str(source_row.get("source_type", "")).strip().lower()
    if "work24" in source_type or "worknet" in source_type:
        from src.collectors.work24_public_collector import Work24PublicCollector

        return Work24PublicCollector()
    if source_type in {"ats", "public_ats", "public_endpoint", "greenhouse", "lever", "ashby"}:
        from src.collectors.ats_public_collector import ATSPublicCollector

        return ATSPublicCollector()
    if source_type in {"company_career_page", "career_page"}:
        from src.collectors.company_career_collector import CompanyCareerCollector

        return CompanyCareerCollector()

    from src.collectors.public_html_collector import PublicHtmlCollector

    return PublicHtmlCollector()


def build_log_row(
    run_id: str,
    source_row: dict,
    collector_name: str,
    started_at: str,
    finished_at: str,
    status: str,
    records_found: int,
    records_saved: int,
    error_count: int,
    notes: str,
) -> dict:
    return {
        "run_id": run_id,
        "source_id": source_row.get("source_id", ""),
        "source_url": source_row.get("source_url", ""),
        "collector_name": collector_name,
        "started_at": started_at,
        "finished_at": finished_at,
        "status": status,
        "request_count": "1" if status in {"success", "failed"} else "0",
        "records_found": str(records_found),
        "records_saved": str(records_saved),
        "error_count": str(error_count),
        "notes": notes,
    }


def build_error_row(run_id: str, source_row: dict, message: str) -> dict:
    created_at = datetime.now(timezone.utc).isoformat()
    return {
        "error_id": f"collection_error_{uuid4().hex[:12]}",
        "run_id": run_id,
        "phase_name": "phase3_jd_collection",
        "record_id": source_row.get("source_id", ""),
        "error_type": "collection_failed",
        "error_message": message,
        "retryable": "false",
        "created_at": created_at,
        "notes": source_row.get("source_url", ""),
    }


def run_collection() -> tuple[int, int]:
    sources_path = ROOT / "master/source_registry_master.csv"
    raw_jds_path = ROOT / "data/raw/raw_jds.csv"
    log_path = ROOT / "data/logs/collection_log.csv"
    errors_path = ROOT / "runtime/errors.csv"

    sources = read_csv_rows(sources_path)
    eligible_sources, _blocked_sources = filter_collectable_sources(sources)

    if not eligible_sources:
        print(NO_ELIGIBLE_MESSAGE)
        return 0, 0

    run_id = f"collection_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    all_rows: list[dict] = []
    log_rows: list[dict] = []
    error_rows: list[dict] = []

    for source_row in eligible_sources:
        started_at = datetime.now(timezone.utc).isoformat()
        collector_name = "unresolved"
        try:
            collector = make_collector(source_row)
            collector_name = collector.collector_name
            rows = collector.collect_source(source_row)
            finished_at = datetime.now(timezone.utc).isoformat()
            all_rows.extend(rows)
            log_rows.append(
                build_log_row(
                    run_id,
                    source_row,
                    collector_name,
                    started_at,
                    finished_at,
                    "success",
                    len(rows),
                    len(rows),
                    0,
                    "approved-source-only collection completed",
                )
            )
        except Exception as exc:  # noqa: BLE001 - record and stop per source.
            finished_at = datetime.now(timezone.utc).isoformat()
            message = str(exc)
            error_rows.append(build_error_row(run_id, source_row, message))
            log_rows.append(
                build_log_row(
                    run_id,
                    source_row,
                    collector_name,
                    started_at,
                    finished_at,
                    "failed",
                    0,
                    0,
                    1,
                    message,
                )
            )

    if all_rows:
        write_csv_rows(raw_jds_path, JD_COLUMNS, all_rows, append=True)
    if log_rows:
        write_csv_rows(log_path, JD_COLLECTION_LOG_COLUMNS, log_rows, append=True)
    if error_rows:
        write_csv_rows(errors_path, ERRORS_COLUMNS, error_rows, append=True)

    print(f"Approved-source collection completed: {len(all_rows)} JD row(s) saved.")
    return len(eligible_sources), len(all_rows)


def main() -> int:
    run_collection()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
