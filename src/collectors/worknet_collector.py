"""Safe skeleton for a WorkNet-style official API collector."""

from __future__ import annotations

import os

from src.collectors.base_collector import BaseCollector


class WorknetCollector(BaseCollector):
    """Official API collector skeleton.

    TODO: Add the approved WorkNet public API endpoint after reviewing API
    documentation, terms, rate limits, and required attribution.
    """

    def build_url(self, keyword: str) -> str:
        api_key = os.getenv("WORKNET_API_KEY", "")
        if not api_key:
            raise ValueError("WORKNET_API_KEY is not set.")
        raise NotImplementedError("WorkNet endpoint must be added after source review.")

    def parse(self, payload: str) -> list[dict]:
        raise NotImplementedError("WorkNet response parsing is not implemented yet.")

    def normalize(self, records) -> list[dict]:
        raise NotImplementedError("WorkNet normalization is not implemented yet.")

