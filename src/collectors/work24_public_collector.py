"""Approved-source-only Work24 public collector skeleton."""

from __future__ import annotations

from src.collectors.public_html_collector import PublicHtmlCollector


class Work24PublicCollector(PublicHtmlCollector):
    """Work24 public HTML collector placeholder.

    This collector only fetches an approved public source URL. Work24-specific
    parsing must be added later after registry approval and policy review.
    """

    collector_name = "work24_public"
