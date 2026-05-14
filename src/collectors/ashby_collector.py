"""Safe public Ashby endpoint skeleton."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from src.collectors.base_collector import BaseCollector


class AshbyCollector(BaseCollector):
    """Collector skeleton for public Ashby job board endpoints."""

    def build_jobs_url(self, organization_slug: str) -> str:
        return f"https://api.ashbyhq.com/posting-api/job-board/{organization_slug}"

    def fetch_company_jobs(self, organization_slug: str) -> str:
        """Fetch a public Ashby board only after source registry approval."""
        return self.fetch(self.build_jobs_url(organization_slug))

    def parse(self, payload: str) -> list[dict]:
        data = json.loads(payload)
        return data.get("jobs", [])

    def normalize(self, records) -> list[dict]:
        normalized = []
        collected_at = datetime.now(timezone.utc).isoformat()
        for record in records:
            normalized.append(
                {
                    "source_url": record.get("jobUrl", ""),
                    "source_type": "ashby",
                    "company": "",
                    "title": record.get("title", ""),
                    "location": record.get("location", ""),
                    "description": record.get("descriptionHtml", ""),
                    "raw_payload": json.dumps(record, ensure_ascii=False),
                    "collected_at": collected_at,
                }
            )
        return normalized

