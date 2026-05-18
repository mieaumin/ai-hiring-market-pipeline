# Phase 0 - Korean Job Site Registry Construction

Phase 0 builds the Korean job-site universe before company discovery or JD collection.

This phase follows the Biz-Voyager-style operating model:

```text
broad discovery
-> evidence review
-> screening
-> staging
-> master
```

It adds strict legal and policy gates before any future collection.

## Current Priority

The current priority is Korean job-site discovery, not company career-page discovery.

Phase 0 is:

```text
broad source discovery
-> source evidence collection
-> source screening
-> approved source registry
```

Phase 0 is not:

- company career page discovery
- AI-only source filtering
- JD collection
- large-scale crawling
- developer-only site discovery

## Required Flow

```text
raw_job_site_discovery
-> site_policy_evidence
-> job_site_registry_staging
-> site_screening
-> master/job_source_registry
```

Raw discovery is intentionally broad. Approval is intentionally strict. A discovered site is not an approved source.

## Discovery Routes

Phase 0 supports three discovery routes:

- Route A - search-engine-based discovery
- Route B - reverse-reference discovery
- Route C - JD-source reverse discovery

See `docs/source_discovery_routes.md` for route definitions.

## Candidate Site Categories

Initial Korean job-site candidate categories include:

- general job portals
- startup hiring platforms
- public/government job platforms
- university/internship job boards
- career communities
- headhunting/recruiting platforms
- developer hiring platforms
- company hiring aggregators

These categories are for recall. They do not imply AI relevance, collection eligibility, or approval.

## Raw Discovery Schema

`runtime/raw_job_site_discovery.csv` records broad candidate sites with:

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

## Source Grades

| Grade | Meaning | Use policy |
| --- | --- | --- |
| A | Official API available | Can be approved if policy and evidence are valid |
| B | Public ATS/API endpoint available | Can be approved if public access and policy evidence are valid |
| C | Public company career page or public job page with acceptable robots.txt and Terms of Service | Can be approved only after careful human review |
| D | Unclear policy, general scraping needed, or human/legal review required | Must remain `needs_manual_review` or `needs_legal_review` |
| E | Login, CAPTCHA, anti-bot bypass, or prohibited automated collection required | Reject |
| F | Unusable, blocked, or legally/policy-wise rejected | Reject |

Only A, B, and carefully reviewed C can be approved. Grade D remains in manual or legal review. Grades E and F are rejected.

## Strict Evidence Review

Evidence review must cover:

- robots.txt
- Terms of Service
- API requirement
- login requirement
- CAPTCHA
- anti-bot controls
- public HTML access
- reuse restrictions
- copyright risk
- database-right risk
- personal-data risk

Any unclear or restrictive evidence should prevent approval until reviewed.

## 0-0 Source Discovery Strategy Definition

Purpose:
Define how Korean job sites are discovered, grouped, evidenced, screened, and promoted.

Input:
- Project scope
- Korean job-site discovery categories
- Discovery route definitions
- Legal and ethics policy
- Source compliance review policy

Process:
- Define broad discovery routes.
- Define allowed `site_type` categories.
- Define required policy evidence before screening.
- Define strict source grades, approval status values, and promotion gates.

Output:
- Discovery strategy
- Evidence requirements
- Staging and master registry templates

Acceptance Criteria:
- The strategy explicitly says Phase 0 is not a crawling phase.
- Discovery is broad, but approval is strict.
- Compliance evidence is required before approval.

## 0-1 Raw Job Site Discovery

Purpose:
Capture potential Korean job posting sources without deciding whether they are usable.

Input:
- Manual search results
- Reverse-reference notes
- Public job-site mentions
- Known source references
- Research notes

Process:
- Record discovered sources in `runtime/raw_job_site_discovery.csv`.
- Keep site name, URL, type, discovery route, keyword, source, country, notes, and timestamp.
- Do not collect job postings.
- Do not infer approval from discovery.

Output:
- Raw source discovery records

Acceptance Criteria:
- Each row is a candidate only.
- Discovery route and source explain why the site was discovered.
- No fake source rows or JD data are added.

## 0-2 Site Canonicalization

Purpose:
Normalize discovered sources into stable site-level records.

Input:
- `runtime/raw_job_site_discovery.csv`
- Public site URLs
- Manual review notes

Process:
- Identify canonical site URLs and domains.
- Merge duplicate references.
- Assign stable `site_id` values.
- Keep ambiguous sources in review rather than guessing.

Output:
- Canonicalized source candidates for policy evidence review

Acceptance Criteria:
- Each staged source has a stable `site_id`.
- Duplicate or ambiguous sites are documented.
- Canonicalization does not imply approval.

## 0-3 Policy Evidence Collection

Purpose:
Collect traceable evidence needed for strict source screening.

Input:
- Canonical source candidates
- robots.txt URL and target job paths
- Terms of Service pages
- Public access observations
- API documentation or approval requirement notes

Process:
- Record evidence in `runtime/site_policy_evidence.csv`.
- Capture evidence category, source URL, text excerpt, policy keyword found, risk level, reviewer, reviewed timestamp, decision, and notes.
- Use evidence categories such as robots.txt, terms, login, CAPTCHA, anti-bot, API requirement, public HTML access, dynamic rendering, copyright, database right, personal data, and reuse restriction.

Output:
- Traceable policy evidence table

Acceptance Criteria:
- Evidence is linked to `site_id` and `site_name`.
- Policy excerpts are recorded when available.
- Ambiguous evidence does not become approval.

## 0-4 Job Site Registry Staging

Purpose:
Prepare a review workspace that combines source profile and compliance fields.

Input:
- Raw discovery records
- Policy evidence rows
- Canonical site records

Process:
- Record each site in `staging/job_site_registry_staging.csv`.
- Fill strict review columns such as robots target path status, terms collection policy, API requirement, login, CAPTCHA, anti-bot risk, public HTML access, personal data risk, database right risk, copyright risk, reuse restriction risk, collection scope, allowed method, decision, and decision reason.
- Use conservative defaults for unknown risk.

Output:
- Staged site registry with compliance fields

Acceptance Criteria:
- No source in staging is treated as approved.
- Required risk fields are reviewable.
- Decision reason is traceable to evidence rows.

## 0-5 Site Screening

Purpose:
Apply strict eligibility gates to decide whether a source can move to master.

Input:
- `runtime/site_policy_evidence.csv`
- `staging/job_site_registry_staging.csv`
- `docs/source_compliance_review.md`

Process:
- Check robots.txt, Terms of Service, login requirements, CAPTCHA, anti-bot risk, API approval requirements, public HTML access, dynamic rendering risk, personal data risk, database right risk, copyright risk, reuse restriction risk, and request-volume feasibility.
- Assign a conservative decision.
- Document decision reason, reviewer, and review timestamp.

Output:
- Screened site registry decisions

Acceptance Criteria:
- Discovery alone never approves a site.
- Unclear policy leads to manual or legal review, not approval.
- Prohibited or risky sources do not move to master for MVP use.

## 0-6 Eligibility Decision

Purpose:
Convert site screening results into a final registry decision.

Input:
- Site screening decision
- Policy evidence rows
- Staging record
- Reviewer notes

Process:
- Confirm the decision reason is supported by evidence.
- Confirm robots.txt and Terms do not block the intended collection.
- Keep blocked, ambiguous, or legally unclear sources out of master.

Output:
- Final source eligibility decision

Acceptance Criteria:
- Decision is explicit and traceable.
- Approval is not inferred from discovery or staging.
- Non-approved states do not move to master.

## 0-7 Approved Source Registry

Purpose:
Promote only screened and approved job-site sources into the master registry.

Input:
- Screened staging records
- Policy evidence records
- Reviewer decision

Process:
- Promote eligible records to `master/job_source_registry.csv`.
- Preserve collection scope, allowed method, decision reason, reviewer, and last reviewed timestamp.
- Keep staging and master separated.

Output:
- `master/job_source_registry.csv`

Acceptance Criteria:
- Master contains only reviewed sources with traceable evidence.
- Master does not contain blocked or unclear sources.
- Collection scope is limited to necessary JD fields and source links.

## 0-8 Source Monitoring

Purpose:
Keep approved source decisions current over time.

Input:
- Master source registry
- Updated policy evidence
- Manual monitoring notes

Process:
- Re-check robots.txt, Terms, access behavior, API requirements, and risk fields on a recurring schedule.
- Move a source out of approved use if evidence becomes stale or invalid.
- Update last reviewed timestamp, reviewer, decision, and decision reason.

Output:
- Updated source registry and policy evidence

Acceptance Criteria:
- Each approved source has `last_reviewed_at`.
- Stale or changed sources move back to manual or legal review.
- Approval is never permanent without monitoring.
