"""Conservative JD extraction skeleton for approved public HTML sources."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib

from bs4 import BeautifulSoup

from src.processing.ai_role_filter import is_ai_related_jd
from src.processing.deduplicator import normalize_key_part, text_hash
from src.utils.template_schemas import JD_COLUMNS
from src.utils.text_cleaning import clean_text


def extract_jd_from_html(payload: str, source_row: dict, job_url: str | None = None) -> dict:
    """Extract a single conservative JD candidate from an approved source page."""
    soup = BeautifulSoup(payload or "", "html.parser")
    title = _extract_title(soup)
    raw_text = clean_text(soup.get_text(" ", strip=True))
    return build_jd_record(
        source_row=source_row,
        job_url=job_url or source_row.get("source_url", ""),
        job_title=title,
        jd_text_raw=raw_text,
        jd_text_clean=raw_text,
    )


def build_jd_record(
    source_row: dict,
    job_url: str,
    job_title: str,
    jd_text_raw: str,
    jd_text_clean: str,
) -> dict:
    """Build a raw JD row using the canonical JD schema."""
    collected_at = datetime.now(timezone.utc).isoformat()
    content_hash = text_hash(jd_text_clean)
    duplicate_key = build_duplicate_key(source_row, job_url, job_title, content_hash)
    jd_id = build_jd_id(source_row, job_url, job_title, content_hash)
    role_group = infer_role_group(job_title, jd_text_clean)
    validation_status, failure_reason = _initial_validation(job_title, jd_text_clean)

    row = {column: "" for column in JD_COLUMNS}
    row.update(
        {
            "jd_id": jd_id,
            "company_id": source_row.get("company_id", ""),
            "company_name": source_row.get("company_name", ""),
            "source_id": source_row.get("source_id", ""),
            "source_url": source_row.get("source_url", ""),
            "job_url": job_url,
            "job_title": job_title,
            "job_category": role_group,
            "role_group": role_group,
            "jd_text_raw": jd_text_raw,
            "jd_text_clean": jd_text_clean,
            "language": detect_language(f"{job_title} {jd_text_clean}"),
            "collected_at": collected_at,
            "last_checked_at": collected_at,
            "source_grade": source_row.get("source_grade", ""),
            "source_approval_status": source_row.get("source_approval_status")
            or source_row.get("approval_status", ""),
            "validation_status": validation_status,
            "failure_reason": failure_reason,
            "content_hash": content_hash,
            "duplicate_key": duplicate_key,
        }
    )
    return row


def build_jd_id(source_row: dict, job_url: str, job_title: str, content_hash: str) -> str:
    """Build a stable JD id from source and content identifiers."""
    seed = "|".join(
        [
            source_row.get("source_id", ""),
            job_url or source_row.get("source_url", ""),
            job_title,
            content_hash,
        ]
    )
    return f"jd_{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:16]}"


def build_duplicate_key(source_row: dict, job_url: str, job_title: str, content_hash: str) -> str:
    """Build a duplicate key from source URL, company, title, and content hash."""
    parts = [
        normalize_key_part(job_url or source_row.get("source_url", "")),
        normalize_key_part(source_row.get("company_name", "")),
        normalize_key_part(job_title),
        content_hash[:12],
    ]
    return "|".join(parts)


def infer_role_group(job_title: str, jd_text_clean: str) -> str:
    """Infer one MVP role group using rule-based keywords only."""
    searchable = f"{job_title} {jd_text_clean}".lower()
    if any(keyword in searchable for keyword in ["analyst", "data analyst", "business analyst"]):
        return "AI Analyst"
    if any(keyword in searchable for keyword in ["researcher", "research scientist", "research"]):
        return "AI Researcher"
    if any(keyword in searchable for keyword in ["scientist", "data scientist", "applied scientist"]):
        return "AI Scientist"
    if any(keyword in searchable for keyword in ["engineer", "llm", "rag", "mlops", "machine learning"]):
        return "AI Engineer"
    if is_ai_related_jd({"job_title": job_title, "jd_text_clean": jd_text_clean}):
        return "AI Engineer"
    return ""


def detect_language(text: str) -> str:
    """Return a coarse language tag for Korean/English mixed JD text."""
    return "ko" if any("\uac00" <= character <= "\ud7a3" for character in text or "") else "en"


def _extract_title(soup: BeautifulSoup) -> str:
    for selector in ["h1", "[data-testid='job-title']", ".job-title", "title"]:
        element = soup.select_one(selector)
        if element:
            title = clean_text(element.get_text(" ", strip=True))
            if title:
                return title
    return ""


def _initial_validation(job_title: str, jd_text_clean: str) -> tuple[str, str]:
    missing = []
    if not job_title:
        missing.append("missing_title")
    if not jd_text_clean:
        missing.append("missing_description")
    if missing:
        return "failed", "|".join(missing)
    return "raw", ""
