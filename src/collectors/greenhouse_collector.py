"""Safe public Greenhouse endpoint skeleton."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from src.collectors.base_collector import BaseCollector, SourceNotCollectableError
from src.registry.collection_guard import validate_source_before_collection


class GreenhouseCollector(BaseCollector):
    """Collector skeleton for public Greenhouse job board endpoints."""

    def build_jobs_url(self, board_token: str) -> str:
        return f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"

    def fetch_company_jobs(self, board_token: str, source_row: dict | None = None) -> str:
        """Fetch a public board only after the source registry approves it."""
        if source_row is None:
            raise SourceNotCollectableError("source_row is required before collection")
        allowed, reasons = validate_source_before_collection(source_row)
        if not allowed:
            raise SourceNotCollectableError("; ".join(reasons))
        return self.fetch(self.build_jobs_url(board_token))

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
                    "source_url": record.get("absolute_url", ""),
                    "source_type": "greenhouse",
                    "company": "",
                    "title": record.get("title", ""),
                    "location": (record.get("location") or {}).get("name", ""),
                    "description": record.get("content", ""),
                    "raw_payload": json.dumps(record, ensure_ascii=False),
                    "collected_at": collected_at,
                    "source_grade": source_row.get("source_grade", ""),
                    "source_approval_status": source_row.get("approval_status", ""),
                }
            )
        return normalized
