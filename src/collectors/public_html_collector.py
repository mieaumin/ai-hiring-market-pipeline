"""Approved-source-only public HTML collector."""

from __future__ import annotations

from typing import Iterable

from src.collectors.base_collector import BaseCollector
from src.processing.jd_extractor import extract_jd_from_html


class PublicHtmlCollector(BaseCollector):
    """Collect one approved public HTML source URL without link crawling."""

    collector_name = "public_html"

    def parse(self, payload: str, source_row: dict | None = None) -> list[dict]:
        return [{"payload": payload, "job_url": (source_row or {}).get("source_url", "")}]

    def normalize(self, records: Iterable[dict], source_row: dict | None = None) -> list[dict]:
        source_row = source_row or {}
        return [
            extract_jd_from_html(
                record.get("payload", ""),
                source_row,
                job_url=record.get("job_url") or source_row.get("source_url", ""),
            )
            for record in records
        ]
