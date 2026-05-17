"""Conservative public company career page collector."""

from __future__ import annotations

from typing import Iterable

from src.collectors.public_html_collector import PublicHtmlCollector


class CompanyCareerCollector(PublicHtmlCollector):
    """HTML career page skeleton for carefully reviewed C-grade sources."""

    collector_name = "company_career"

    def parse(self, payload: str, source_row: dict | None = None) -> list[dict]:
        # TODO: Add source-specific job card selectors only after manual review.
        return super().parse(payload, source_row)

    def normalize(self, records: Iterable[dict], source_row: dict | None = None) -> list[dict]:
        # TODO: Add source-specific field mapping only after manual review.
        return super().normalize(records, source_row)
