from src.registry.site_policy_parser import find_policy_keywords, parse_evidence_row


KEYWORDS = {
    "scraping_prohibited": {
        "english": ["scraping prohibited"],
        "korean": ["스크래핑 금지"],
    },
    "captcha": {
        "english": ["captcha"],
        "korean": ["보안문자"],
    },
}


def test_scraping_prohibited_keyword_is_detected():
    matches = find_policy_keywords(
        "Automated scraping prohibited for this service.",
        keyword_registry=KEYWORDS,
    )

    assert matches["scraping_prohibited"] == ["scraping prohibited"]


def test_parse_evidence_row_returns_matched_categories():
    parsed = parse_evidence_row(
        {
            "evidence_id": "ev-001",
            "site_id": "site-001",
            "evidence_text_excerpt": "보안문자 is required for access.",
        },
        keyword_registry=KEYWORDS,
    )

    assert parsed["evidence_id"] == "ev-001"
    assert parsed["matched_categories"] == ["captcha"]
