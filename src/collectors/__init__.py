"""Safe approved-source collector modules."""

from src.collectors.ats_public_collector import ATSPublicCollector
from src.collectors.company_career_collector import CompanyCareerCollector
from src.collectors.public_html_collector import PublicHtmlCollector
from src.collectors.work24_public_collector import Work24PublicCollector

__all__ = [
    "ATSPublicCollector",
    "CompanyCareerCollector",
    "PublicHtmlCollector",
    "Work24PublicCollector",
]
