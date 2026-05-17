# Korean Job-Site Universe Discovery

This document defines the current Phase 0 priority: build the Korean job-site universe before company discovery, company career-page discovery, or JD collection.

The goal is maximum source recall. At this stage, a discovered site is only a candidate. It is not approved for collection until evidence review, screening, staging, and master promotion are completed.

## Phase 0 Flow

```text
broad source discovery
-> source evidence collection
-> source screening
-> staging
-> master/job_source_registry
```

This follows the Biz-Voyager-style operating philosophy:

```text
broad discovery
-> evidence review
-> screening
-> staging
-> master
```

## What This Phase Is

- building the Korean job-site source universe
- collecting source-level evidence
- preparing future source screening
- preserving discovery route, keyword, source, and timestamp
- keeping raw discovery separate from approved registry data

## What This Phase Is Not

- not filtering to AI-only sites
- not collecting JDs
- not performing large-scale crawling
- not restricting discovery to developer-only sites
- not discovering individual company career pages yet
- not treating discovered sources as approved sources

## Raw Discovery Schema

`runtime/raw_job_site_discovery.csv` stores header-only or manually reviewed candidate rows with:

- `site_id`
- `site_name`
- `site_url`
- `site_domain`
- `site_type`
- `discovery_route`
- `discovery_query`
- `discovery_source_url`
- `country`
- `confidence`
- `review_status`
- `collection_eligibility`
- `notes`
- `discovered_at`

Allowed `site_type` examples:

- `job_portal`
- `startup_jobs`
- `developer_jobs`
- `public_jobs`
- `intern_jobs`
- `headhunting_platform`
- `career_platform`
- `community_jobs`
- `company_jobs`
- `unknown`

## Initial Korean Job-Site Candidate Categories

The discovery universe should include:

- general job portals
- startup hiring platforms
- public/government job platforms
- university/internship job boards
- career communities
- headhunting/recruiting platforms
- developer hiring platforms
- company hiring aggregators

These categories are intentionally broad. They do not imply approval, AI relevance, or collection eligibility.

## Initial Seed List Status

The initial Korean job-site seed list is stored in:

- `config/job_site_candidates.csv`
- `runtime/raw_job_site_discovery.csv`

This seed list is not an approved source list. Inclusion in `config/job_site_candidates.csv` or `runtime/raw_job_site_discovery.csv` only means the source is part of the broad discovery universe and should be reviewed later.

Seeded sources must remain unapproved until evidence review is complete. Robots.txt, Terms of Service, API requirements, login requirements, CAPTCHA risk, anti-bot risk, public HTML access, and reuse restrictions must be reviewed before any source can move to `master/job_source_registry.csv`.

Every seeded site starts as `needs_manual_review` or equivalent unreviewed status. No seeded source should be used for JD collection until it passes source screening.

## Evidence Review

Before a site can be screened, reviewers should collect source evidence in `runtime/site_policy_evidence.csv`.

Review evidence should cover:

- robots.txt
- Terms of Service
- API requirement
- login requirement
- CAPTCHA
- anti-bot controls
- public HTML access
- reuse restrictions
- copyright and database-right risks
- personal-data risk

## Screening Boundary

Only after evidence is collected should a site move into `staging/job_site_registry_staging.csv`.

Only after screening should a site move into `master/job_source_registry.csv`.

No row should enter master merely because it was discovered.
