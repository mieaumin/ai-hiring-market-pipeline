"""Approved-source-only public ATS collector skeleton."""

from __future__ import annotations

from src.collectors.public_html_collector import PublicHtmlCollector


class ATSPublicCollector(PublicHtmlCollector):
    """Public ATS collector placeholder.

    This first implementation fetches only the approved registry URL. Future
    ATS-specific JSON or HTML parsing may be added after explicit approval.
    """

    collector_name = "ats_public"
