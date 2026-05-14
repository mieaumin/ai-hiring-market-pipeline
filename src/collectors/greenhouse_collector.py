"""Safe public Greenhouse endpoint skeleton."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from src.collectors.base_collector import BaseCollector


class GreenhouseCollector(BaseCollector):
    """Collector skeleton for public Greenhouse job board endpoints."""

    def build_jobs_url(self, board_token: str) -> str:
        return f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"

    def fetch_company_jobs(self, board_token: str) -> str:
        """Fetch a public board only after the source registry approves it."""
        return self.fetch(self.build_jobs_url(board_token))

    def parse(self, payload: str) -> list[dict]:
        data = json.loads(payload)
        return data.get("jobs", [])

    def normalize(self, records) -> list[dict]:
        normalized = []
        collected_at = datetime.now(timezone.utc).isoformat()
        for record in records:
            normalized.append(
                {
                    "source_url": record.get("absolute_url", ""),
                    "source_type": "greenhouse",
                    "company": "",
                    "title": record.get("title", ""),
                    "location": (record.get("location") or {}).get("name", ""),
                    "description": record.get("content", ""),
                    "raw_payload": json.dumps(record, ensure_ascii=False),
                    "collected_at": collected_at,
                }
            )
        return normalized

