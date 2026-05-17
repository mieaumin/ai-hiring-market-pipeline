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
- Live collection is limited to approved crawl-eligible source rows only.
- If no approved crawl-eligible source exists, collection is skipped safely.

## Safe Commands

Most scripts initialize and validate templates only. `scripts/run_approved_collection.py` is the only collection entry point, and it refuses to run unless a source row has already been approved in `master/source_registry_master.csv` and passes the collection guard. No script solves CAPTCHA, bypasses anti-bot systems, automates login, rotates IPs, calls Google Sheets, or weakens source approval.

Recommended safe workflow:

```bash
python scripts/init_all_registries.py
python scripts/validate_pipeline_templates.py
python scripts/run_approved_collection.py
python scripts/run_quality_gate_dryrun.py
```

When no approved source exists, the collection command prints:

```text
No approved crawl-eligible sources found. Collection skipped.
```

and performs no network collection.

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

Phase 3 can run only after `collection_guard.py` approves the row for collection.

Phase 4:
`raw_jds -> validation -> normalization -> AI role filtering -> deduplication -> staging/jd_staging.csv`

Phase 5:
`jd_staging -> quality_gate -> master/jd_master_dataset.csv`
