"""Text cleaning helpers."""

from __future__ import annotations

import re
from html import unescape

from bs4 import BeautifulSoup


def strip_html(value: str) -> str:
    """Convert HTML to plain text."""
    if not value:
        return ""
    return BeautifulSoup(value, "html.parser").get_text(" ", strip=True)


def clean_text(value: str) -> str:
    """Normalize whitespace and HTML entities."""
    text = strip_html(unescape(value or ""))
    return re.sub(r"\s+", " ", text).strip()

