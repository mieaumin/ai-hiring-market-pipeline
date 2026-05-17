from src.registry.site_risk_scoring import has_blocking_risk, score_evidence_rows


KEYWORDS = {
    "scraping_prohibited": {
        "english": ["scraping prohibited"],
        "korean": ["스크래핑 금지"],
    },
    "api_required": {
        "english": ["api approval required"],
        "korean": ["API 승인 필요"],
    },
}


def test_scraping_prohibited_keyword_creates_critical_risk():
    score = score_evidence_rows(
        [{"evidence_text_excerpt": "scraping prohibited"}],
        keyword_registry=KEYWORDS,
    )

    assert score["risk_level"] == "critical"
    assert has_blocking_risk(score)


def test_api_required_keyword_creates_medium_risk():
    score = score_evidence_rows(
        [{"evidence_text_excerpt": "API approval required"}],
        keyword_registry=KEYWORDS,
    )

    assert score["risk_level"] == "medium"
    assert not has_blocking_risk(score)
