# Phase 4 - JD Collection from Approved Sources Only

Phase 4 is the approved-source-only collection phase for AI-related public JD candidates.

This repository implements a first conservative collection-ready runner. It does not perform broad crawling. It reads only `runtime/source_registry.csv` and stops safely when no approved crawl-eligible source exists.

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
- no collection from Grade D, Grade E, or Grade F sources
- no collection from pending, rejected, expired, suspended, unknown, or missing approvals
- no API use unless the source approval status is `approved`
- stop on HTTP 401, 403, 407, 429, or CAPTCHA-like responses

## Collection Guard

`src/registry/collection_guard.py` blocks collection unless:

- `decision = approved`
- `source_grade` is A, B, or C
- `source_approval_status` or `approval_status` is `not_required` or `approved`
- `robots_target_path_status` is `allowed` or `partially_allowed`
- `terms_collection_policy` is `allowed` or `limited`
- `login_required = false`
- `captcha_required = false`
- `anti_bot_risk` is `low` or `none`
- `public_html_access = true`, unless the approved method is a public JSON, RSS, or sitemap endpoint

If no approved crawl-eligible source exists, `scripts/run_approved_source_collection.py` prints:

```text
No approved sources found. Collection skipped safely.
```

and no network collection is attempted.

## Collectors

- `base_collector.py`
- `public_json_collector.py`
- `rss_collector.py`
- `sitemap_collector.py`
- `greenhouse_collector.py`
- `lever_collector.py`
- `ashby_collector.py`

## Outputs

- `data/raw/raw_jds.csv`
- `runtime/runs.csv`
- `runtime/errors.csv`

## Acceptance Criteria

- The source exists in `runtime/source_registry.csv`.
- The source is Grade A with automated checks passed, or Grade B/C with human `approval_status = approved`.
- Grade D, E, and F sources do not collect JDs.
- Collection scope is documented.
- JD records preserve source links.
- Request volume remains conservative.
- The collector never attempts login, CAPTCHA solving, anti-bot bypass, or access-control bypass.
