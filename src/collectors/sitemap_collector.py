"""Approved sitemap-discoverable job page collector skeleton."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from src.collectors.base_collector import BaseCollector
from src.processing.jd_extractor import build_jd_record


class SitemapCollector(BaseCollector):
    """Parse approved sitemap URLs without broad crawling."""

    collector_name = "sitemap"

    def parse(self, payload: str, source_row: dict | None = None) -> list[dict]:
        """Parse sitemap loc entries."""
        root = ET.fromstring(payload)
        records = []
        for element in root.iter():
            if element.tag.endswith("loc") and element.text:
                records.append({"url": element.text.strip()})
        return records

    def normalize(self, records, source_row: dict | None = None) -> list[dict]:
        """Create conservative raw rows from sitemap-discovered URLs.

        The skeleton does not fetch each URL. Missing titles/descriptions will
        fail later quality gates unless a future approved workflow enriches them.
        """
        source_row = source_row or {}
        return [
            build_jd_record(
                source_row=source_row,
                job_url=record.get("url") or source_row.get("source_url", ""),
                job_title="",
                jd_text_raw="",
                jd_text_clean="",
            )
            for record in records
        ]
