"""Conservative public company career page collector skeleton."""

from __future__ import annotations

from bs4 import BeautifulSoup

from src.collectors.base_collector import BaseCollector


class CompanyCareerCollector(BaseCollector):
    """HTML career page skeleton for carefully reviewed C-grade sources."""

    def parse(self, payload: str) -> list[dict]:
        soup = BeautifulSoup(payload, "html.parser")
        # TODO: Implement source-specific parsing only after manual source review.
        title = soup.title.get_text(strip=True) if soup.title else ""
        return [{"page_title": title, "html_text": soup.get_text(" ", strip=True)}]

    def normalize(self, records) -> list[dict]:
        # TODO: Source-specific selectors are required before production use.
        return []

