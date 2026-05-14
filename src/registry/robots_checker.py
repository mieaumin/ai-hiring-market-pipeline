"""robots.txt review helper.

This module only checks policy visibility. It does not bypass restrictions.
"""

from __future__ import annotations

from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


def build_robots_url(source_url: str) -> str:
    """Build a robots.txt URL from a source URL."""
    parsed = urlparse(source_url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"


def is_allowed_by_robots(source_url: str, user_agent: str) -> bool:
    """Check robots.txt for a URL using Python's standard parser."""
    parser = RobotFileParser()
    parser.set_url(build_robots_url(source_url))
    parser.read()
    return parser.can_fetch(user_agent, source_url)

