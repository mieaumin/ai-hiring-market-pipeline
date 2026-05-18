"""Safe public Ashby endpoint skeleton."""

from __future__ import annotations

import json

from src.collectors.base_collector import BaseCollector, SourceNotCollectableError
from src.processing.jd_extractor import build_jd_record
from src.registry.collection_guard import validate_source_before_collection
from src.utils.text_cleaning import clean_text


class AshbyCollector(BaseCollector):
    """Collector skeleton for public Ashby job board endpoints."""

    def build_jobs_url(self, organization_slug: str) -> str:
        return f"https://api.ashbyhq.com/posting-api/job-board/{organization_slug}"

    def fetch_company_jobs(self, organization_slug: str, source_row: dict | None = None) -> str:
        """Fetch a public Ashby board only after source registry approval."""
        if source_row is None:
            raise SourceNotCollectableError("source_row is required before collection")
        allowed, reasons = validate_source_before_collection(source_row)
        if not allowed:
            raise SourceNotCollectableError("; ".join(reasons))
        return self.fetch(self.build_jobs_url(organization_slug))

    def parse(self, payload: str, source_row: dict | None = None) -> list[dict]:
        data = json.loads(payload)
        return data.get("jobs", [])

    def normalize(self, records, source_row: dict | None = None) -> list[dict]:
        source_row = source_row or {}
        normalized = []
        for record in records:
            normalized.append(
                build_jd_record(
                    source_row=source_row,
                    job_url=record.get("jobUrl", "") or source_row.get("source_url", ""),
                    job_title=clean_text(record.get("title", "")),
                    jd_text_raw=record.get("descriptionHtml") or json.dumps(record, ensure_ascii=False),
                    jd_text_clean=clean_text(record.get("descriptionHtml", "")),
                )
            )
        return normalized
