"""Safe public Ashby endpoint skeleton."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from src.collectors.base_collector import BaseCollector, SourceNotCollectableError
from src.registry.collection_guard import validate_source_before_collection


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
        normalized = []
        collected_at = datetime.now(timezone.utc).isoformat()
        source_row = source_row or {}
        for record in records:
            normalized.append(
                {
                    "company_id": source_row.get("company_id", ""),
                    "company_name": source_row.get("company_name", ""),
                    "source_id": source_row.get("source_id", ""),
                    "source_url": record.get("jobUrl", ""),
                    "source_type": "ashby",
                    "company": "",
                    "title": record.get("title", ""),
                    "location": record.get("location", ""),
                    "description": record.get("descriptionHtml", ""),
                    "raw_payload": json.dumps(record, ensure_ascii=False),
                    "collected_at": collected_at,
                    "source_grade": source_row.get("source_grade", ""),
                    "source_approval_status": source_row.get("approval_status", ""),
                }
            )
        return normalized
