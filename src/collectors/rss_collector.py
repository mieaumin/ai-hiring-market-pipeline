"""Approved RSS feed collector skeleton."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from src.collectors.base_collector import BaseCollector
from src.processing.jd_extractor import build_jd_record
from src.utils.text_cleaning import clean_text


class RssCollector(BaseCollector):
    """Collect only from approved RSS feeds."""

    collector_name = "rss"

    def parse(self, payload: str, source_row: dict | None = None) -> list[dict]:
        """Parse RSS item metadata."""
        root = ET.fromstring(payload)
        records = []
        for item in root.findall(".//item"):
            records.append(
                {
                    "title": item.findtext("title", default=""),
                    "link": item.findtext("link", default=""),
                    "description": item.findtext("description", default=""),
                }
            )
        return records

    def normalize(self, records, source_row: dict | None = None) -> list[dict]:
        source_row = source_row or {}
        rows = []
        for record in records:
            title = clean_text(record.get("title", ""))
            description = clean_text(record.get("description", ""))
            rows.append(
                build_jd_record(
                    source_row=source_row,
                    job_url=record.get("link") or source_row.get("source_url", ""),
                    job_title=title,
                    jd_text_raw=description,
                    jd_text_clean=description,
                )
            )
        return rows
