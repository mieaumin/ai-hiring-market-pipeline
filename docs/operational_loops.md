# Operational Loops

The pipeline has two different operating loops:

- expansion loop
- freshness loop

They should be separated because they answer different questions and run at different cadences.

## Expansion Loop

The expansion loop grows the known universe.

It discovers:

- new Korean job sites
- new company candidates
- new ATS/source patterns
- new source relationships
- new evidence records

Typical outputs include:

- `runtime/raw_job_site_discovery.csv`
- `runtime/site_policy_evidence.csv`
- `runtime/raw_company_discovery.csv`
- `runtime/company_evidence.csv`
- `runtime/source_relationships.csv`
- `runtime/ats_fingerprints.csv`
- `runtime/operation_runs.csv`

The expansion loop is recall-first. It can include broad discovery, but nothing moves to master without evidence review and screening.

## Freshness Loop

The freshness loop maintains already-approved assets.

It checks:

- whether approved sources still work
- whether robots.txt or Terms changed
- whether source structure changed
- whether JDs changed, disappeared, or became inactive
- whether source health is degrading

Typical outputs include:

- `runtime/source_health.csv`
- `runtime/freshness_checks.csv`
- `runtime/operation_runs.csv`

The freshness loop should not discover broad new sources as its primary purpose.

## Why Separate Them

Expansion and freshness loops should be separate because:

- expansion is exploratory and review-heavy
- freshness is maintenance-oriented and source-specific
- expansion may run less frequently
- freshness may run on a stable schedule for approved sources
- failure metrics mean different things in each loop

This separation makes the pipeline easier to audit and easier to operate as the dataset grows.
