"""Safe public Lever endpoint skeleton."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from src.collectors.base_collector import BaseCollector


class LeverCollector(BaseCollector):
    """Collector skeleton for public Lever postings endpoints."""

    def build_jobs_url(self, company_slug: str) -> str:
        return f"https://api.lever.co/v0/postings/{company_slug}?mode=json"

    def fetch_company_jobs(self, company_slug: str) -> str:
        """Fetch public Lever postings only after source registry approval."""
        return self.fetch(self.build_jobs_url(company_slug))

    def parse(self, payload: str) -> list[dict]:
        return json.loads(payload)

    def normalize(self, records) -> list[dict]:
        normalized = []
        collected_at = datetime.now(timezone.utc).isoformat()
        for record in records:
            normalized.append(
                {
                    "source_url": record.get("hostedUrl", ""),
                    "source_type": "lever",
                    "company": "",
                    "title": record.get("text", ""),
                    "location": (record.get("categories") or {}).get("location", ""),
                    "description": record.get("descriptionPlain", ""),
                    "raw_payload": json.dumps(record, ensure_ascii=False),
                    "collected_at": collected_at,
                }
            )
        return normalized

