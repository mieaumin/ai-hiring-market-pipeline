# Pipeline Operations

This document describes the safe operational model for the AI Hiring Market Pipeline.

The project follows Biz-Voyager's operating model:

```text
broad discovery
-> evidence review
-> staging
-> quality gate
-> master
```

This project adds a stricter Phase 0 Korean job site compliance registry before any JD collection.

## Operating Rules

- Raw discovery is broad.
- Promotion is evidence-first.
- Master tables are never written directly from raw data.
- Source compliance is checked before source use.
- JD quality is checked before master promotion.
- Live collection is not enabled yet.

## Safe Commands

The current scripts initialize and validate templates only. They never crawl, scrape, fetch live web pages, call APIs, solve CAPTCHA, bypass anti-bot systems, or write to Google Sheets.

Recommended safe workflow:

```bash
python scripts/init_all_registries.py
python scripts/validate_pipeline_templates.py
python scripts/run_quality_gate_dryrun.py
```

## Run Tracking

Future runs should be recorded in:

- `runtime/runs.csv`
- `runtime/errors.csv`
- `runtime/jd_collection_log.csv`
- `runtime/quality_gate_report.csv`

## Promotion Boundaries

Phase 0:
`raw_job_site_discovery -> site_policy_evidence -> job_site_registry_staging -> site_screening -> master/job_source_registry`

Phase 1:
`raw_company_discovery -> company_evidence -> company_registry_staging -> company_screening -> master/company_registry_master`

Phase 2:
`company_registry_master -> source_discovery -> source_policy_evidence -> source_verification -> source_registry_staging -> master/source_registry_master`

Phase 3:
`source_registry_master -> raw_jd_collection -> data/raw/raw_jds.csv`

Phase 4:
`raw_jds -> validation -> normalization -> AI role filtering -> deduplication -> staging/jd_staging.csv`

Phase 5:
`jd_staging -> quality_gate -> master/jd_master_dataset.csv`

