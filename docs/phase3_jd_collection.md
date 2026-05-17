# Phase 3 - JD Collection

Phase 3 is the approved-source-only collection phase for AI-related public JD candidates.

This repository implements a first conservative collection-ready runner. It does not perform broad crawling. It reads only `master/source_registry_master.csv` and stops safely when no approved crawl-eligible source exists.

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
- no collection from Grade E or Grade F sources
- no collection from pending, rejected, or expired approvals
- no API use unless the source approval status is `approved`
- stop on HTTP 401, 403, 407, 429, or CAPTCHA-like responses

## Collection Guard

`src/registry/collection_guard.py` blocks collection unless:

- `decision = approved`
- `source_grade` is A, B, C, or D
- `approval_status` is `not_required` or `approved`
- `robots_target_path_status` is `allowed` or `partially_allowed`
- `terms_collection_policy` is `allowed` or `limited`
- `login_required = false`
- `captcha_required = false`
- `anti_bot_risk` is `low` or `none`
- `public_html_access = true`

If no approved crawl-eligible source exists, `scripts/run_approved_collection.py` prints:

```text
No approved crawl-eligible sources found. Collection skipped.
```

and no network collection is attempted.

## Collectors

- `base_collector.py`
- `public_html_collector.py`
- `work24_public_collector.py`
- `ats_public_collector.py`
- `company_career_collector.py`

## Outputs

- `data/raw/raw_jds.csv`
- `data/logs/collection_log.csv`
- `runtime/errors.csv`

## Acceptance Criteria

- The source exists in `master/source_registry_master.csv`.
- The source is Grade A with automated checks passed, or Grade B/C/D with human `approval_status = approved`.
- Collection scope is documented.
- JD records preserve source links.
- Request volume remains conservative.
- The collector never attempts login, CAPTCHA solving, anti-bot bypass, or access-control bypass.
