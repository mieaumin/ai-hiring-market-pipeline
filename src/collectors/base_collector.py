"""Base collector interface for approved public sources only."""

from __future__ import annotations

import csv
import os
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

import requests

from src.registry.collection_guard import validate_source_before_collection
from src.utils.template_schemas import JD_COLUMNS


DEFAULT_USER_AGENT = (
    "ai-hiring-market-pipeline/0.2 "
    "(HEDING AI hiring-market research MVP; no bypass; contact: {contact_email})"
)

BLOCKED_STATUS_CODES = {401, 403, 407, 429}
CAPTCHA_MARKERS = (
    "captcha",
    "recaptcha",
    "hcaptcha",
    "cloudflare challenge",
    "access denied",
    "unusual traffic",
    "bot detection",
    "verify you are human",
)


class SourceNotCollectableError(RuntimeError):
    """Raised when a source fails collection guard checks."""


class BlockedResponseError(RuntimeError):
    """Raised when an approved source still blocks conservative collection."""


class BaseCollector(ABC):
    """Base class for source-specific collectors.

    Collectors must only be used for entries already approved in
    runtime/source_registry.csv. This class does not implement bypass,
    aggressive retries, login automation, CAPTCHA solving, or IP rotation.
    """

    collector_name = "base"

    def __init__(self, rate_limit_seconds: float = 3.0, timeout_seconds: int = 20) -> None:
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
        if response.status_code in BLOCKED_STATUS_CODES:
            raise BlockedResponseError(
                f"Collection stopped because the source returned HTTP {response.status_code}."
            )
        response.raise_for_status()
        if looks_like_blocked_or_captcha(response.text):
            raise BlockedResponseError(
                "Collection stopped because the response looks like CAPTCHA or bot blocking."
            )
        return response.text

    @abstractmethod
    def parse(self, payload: str, source_row: dict | None = None) -> list[dict]:
        """Parse source payload into source-specific records."""

    @abstractmethod
    def normalize(self, records: Iterable[dict], source_row: dict | None = None) -> list[dict]:
        """Normalize source-specific records into the raw JD schema."""

    def collect_source(self, source_row: dict) -> list[dict]:
        """Collect one registry-approved source row after guard validation."""
        allowed, reasons = validate_source_before_collection(source_row)
        if not allowed:
            raise SourceNotCollectableError("; ".join(reasons))

        payload = self.fetch(source_row["source_url"])
        records = self.parse(payload, source_row)
        return self.normalize(records, source_row)

    def run(self, source_row: dict, output_path: str | Path | None = None) -> list[dict]:
        """Run fetch, parse, normalize, and optionally save raw JD rows."""
        rows = self.collect_source(source_row)
        if output_path is not None:
            self.save_raw(rows, output_path)
        return rows

    def save_raw(self, records: Iterable[dict], output_path: str | Path, append: bool = True) -> None:
        """Save raw JD records to CSV."""
        records = list(records)
        if not records:
            return
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = JD_COLUMNS
        file_exists = output_path.exists() and output_path.stat().st_size > 0
        mode = "a" if append and file_exists else "w"
        with output_path.open(mode, encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
            if mode == "w":
                writer.writeheader()
            writer.writerows(records)


def looks_like_blocked_or_captcha(payload: str) -> bool:
    """Return True when a response resembles CAPTCHA or access blocking."""
    normalized = (payload or "").lower()
    return any(marker in normalized for marker in CAPTCHA_MARKERS)
