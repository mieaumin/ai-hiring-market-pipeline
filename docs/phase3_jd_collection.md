# Phase 3 - JD Collection

Phase 3 is the future collection phase for AI-related public JD candidates from approved sources only.

The current repository does not implement live collection. This document defines the intended policy and output structure for a future implementation.

## Goal

Collect AI-related public JD candidates only from approved sources.

## Flow

```text
approved source registry
-> JD fetch
-> JD parse
-> JD normalize
-> raw JD storage
```

## Collection Policy

- conservative request rate
- no CAPTCHA solving
- no anti-bot bypass
- no login automation
- no hidden endpoints
- no prohibited scraping
- no collection from unapproved sources

## Collectors

- `base_collector.py`
- `work24_collector.py`
- `greenhouse_collector.py`
- `lever_collector.py`
- `ashby_collector.py`
- `company_career_collector.py`

## Outputs

- `data/raw/raw_jds.csv`
- `runtime/jd_collection_log.csv`

## Acceptance Criteria

- The source exists in `master/source_registry_master.csv`.
- The source is Grade A with automated checks passed, or Grade B/C/D with human `approval_status = approved`.
- Collection scope is documented.
- JD records preserve source links.
- Request volume remains conservative.
