"""Base collector interface for approved public sources only."""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests


DEFAULT_USER_AGENT = (
    "ai-hiring-market-jd-pipeline/0.1 "
    "(research MVP; contact: {contact_email})"
)


class BaseCollector(ABC):
    """Base class for source-specific collectors.

    Collectors must only be used for source registry entries graded A, B, or
    carefully reviewed C. This class does not implement bypass behavior.
    """

    def __init__(self, rate_limit_seconds: float = 1.0, timeout_seconds: int = 20) -> None:
        contact_email = os.getenv("CONTACT_EMAIL", "research-contact-not-set@example.com")
        self.rate_limit_seconds = rate_limit_seconds
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": DEFAULT_USER_AGENT.format(contact_email=contact_email)}
        )

    def fetch(self, url: str) -> str:
        """Fetch one approved public URL with simple rate limiting."""
        time.sleep(self.rate_limit_seconds)
        response = self.session.get(url, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.text

    @abstractmethod
    def parse(self, payload: str) -> list[dict]:
        """Parse source payload into source-specific records."""

    @abstractmethod
    def normalize(self, records: Iterable[dict]) -> list[dict]:
        """Normalize source-specific records into the raw JD schema."""

    def save_raw(self, records: Iterable[dict], output_path: str | Path) -> None:
        """Save raw records to CSV."""
        records = list(records)
        if not records:
            return
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(records).to_csv(output_path, index=False)

