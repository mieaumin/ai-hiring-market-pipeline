"""Approved public JSON endpoint collector skeleton."""

from __future__ import annotations

import json

from src.collectors.base_collector import BaseCollector
from src.processing.jd_extractor import build_jd_record
from src.utils.text_cleaning import clean_text


class PublicJsonCollector(BaseCollector):
    """Collect only from approved public JSON endpoints."""

    collector_name = "public_json"

    def parse(self, payload: str, source_row: dict | None = None) -> list[dict]:
        """Parse common public JSON shapes without probing hidden endpoints."""
        data = json.loads(payload)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for key in ["jobs", "postings", "results", "data", "items"]:
                value = data.get(key)
                if isinstance(value, list):
                    return value
        return []

    def normalize(self, records, source_row: dict | None = None) -> list[dict]:
        """Normalize JSON records into raw JD rows."""
        source_row = source_row or {}
        rows = []
        for record in records:
            title = clean_text(
                record.get("title")
                or record.get("job_title")
                or record.get("text")
                or record.get("name")
                or ""
            )
            description = clean_text(
                record.get("description")
                or record.get("content")
                or record.get("descriptionPlain")
                or record.get("descriptionHtml")
                or ""
            )
            job_url = (
                record.get("job_url")
                or record.get("absolute_url")
                or record.get("hostedUrl")
                or record.get("url")
                or source_row.get("source_url", "")
            )
            rows.append(
                build_jd_record(
                    source_row=source_row,
                    job_url=job_url,
                    job_title=title,
                    jd_text_raw=description,
                    jd_text_clean=description,
                )
            )
        return rows
