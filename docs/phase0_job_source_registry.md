# Phase 0 - Korean Job Site Registry Construction

Phase 0 builds a strict, compliance-first Korean job site registry before any JD collection begins.

This project follows Biz-Voyager's broad discovery -> evidence review -> screening -> staging -> master philosophy, but applies stricter legal and policy gates before any JD collection. Phase 0 is not a crawling phase. It does not collect job postings, scrape pages, call live APIs, automate browsers, or bypass access controls.

## Required Flow

```text
raw_job_site_discovery
-> site_policy_evidence
-> job_site_registry_staging
-> site_screening
-> master/job_source_registry
```

Raw discovery is intentionally broad. Approval is intentionally strict. A discovered site is not an approved source.

## Source Grades

| Grade | Meaning | Use policy |
| --- | --- | --- |
| A | Publicly accessible official source with no approval required | Usable after basic automated checks |
| B | Public ATS or public endpoint | Requires human review before use |
| C | Public company career page with acceptable robots.txt and Terms of Service | Requires human review and explicit approval before use |
| D | Official API or source requiring manual application, approval, contract, institutional access, or API key issuance | Approval pending / manual approval required |
| E | General scraping required or policy unclear | Avoid in MVP |
| F | Login required, CAPTCHA required, anti-bot bypass required, robots blocked, or Terms of Service prohibit collection | Prohibited |

Only Grade A can be considered directly usable without manual approval. "Carefully reviewed" means human approval is required.

Allowed `approval_status` values:

- `not_required`
- `pending`
- `approved`
- `rejected`
- `expired`

Master promotion rule:

- Grade A can move forward only after automated checks pass.
- Grades B, C, and D can move forward only when human `approval_status` is `approved`.
- Grade E is rejected for the MVP unless later re-reviewed.
- Grade F is prohibited.

## Strict Eligibility Gates

A site can be approved only if:

- target job pages are not blocked by robots.txt
- Terms of Service do not prohibit crawling, scraping, automated collection, copying, extraction, reuse, or redistribution
- no login is required
- no CAPTCHA is required
- no anti-bot bypass is required
- no API approval is required
- public HTML access is available
- collection can be done conservatively with low request volume
- collected data can be limited to necessary JD fields and source links

If any gate is unclear, the site should not be approved. Use Grade E unless a later review can resolve the uncertainty.

## Terms of Service Review Checklist

Reviewers should check whether the Terms of Service mention or imply:

- automated collection prohibited
- scraping/crawling/bot/spider prohibited
- copying/extraction/storage prohibited
- redistribution prohibited
- derivative or secondary use prohibited
- commercial use prohibited
- database reproduction prohibited
- API approval required
- abnormal access prohibited
- access-control bypass prohibited

Any prohibitive wording should be captured in `runtime/site_policy_evidence.csv` with the relevant excerpt and risk level.

## 0-0 Source Discovery Strategy Definition

Purpose:
Define how Korean job sites are discovered, grouped, evidenced, screened, and promoted.

Input:
- Project scope
- Target AI JD discovery needs
- Legal and ethics policy
- Source compliance review policy

Process:
- Define broad discovery methods such as manual search, public directories, company career links, sitemap references, official documentation, and public policy pages.
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
- Company career page references
- Public job portal names
- Public ATS references
- Research notes

Process:
- Record discovered sources in `runtime/raw_job_site_discovery.csv`.
- Keep source name, URL, discovery method, discovery evidence, and notes.
- Do not collect job postings.
- Do not infer approval from discovery.

Output:
- Raw source discovery records

Acceptance Criteria:
- Each row is a candidate only.
- Evidence link or notes explain why the source was discovered.
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
- Assign `source_grade`, `manual_review_required`, `human_approval_required`, and `approval_status`.
- Document decision reason, reviewer, and review timestamp.

Output:
- Screened site registry decisions

Acceptance Criteria:
- Grade A is directly usable only after basic automated checks pass.
- Grades B, C, and D require human approval before use.
- Grade E and Grade F sources do not move to master for MVP use.

## 0-6 Eligibility Decision

Purpose:
Convert site screening results into a final registry decision.

Input:
- Site screening decision
- Policy evidence rows
- Staging record
- Reviewer notes

Process:
- Confirm `source_grade`, manual review requirement, human approval requirement, and approval status.
- Confirm the decision reason is supported by evidence.
- Confirm Grade A has passed basic automated checks or Grade B/C/D has human `approval_status = approved`.
- Keep blocked, ambiguous, or legally unclear sources out of master.

Output:
- Final source eligibility decision

Acceptance Criteria:
- Decision is explicit and traceable.
- Approval is not inferred from discovery or staging.
- Non-approved states do not move to master.

## 0-7 Approved Source Registry

Purpose:
Promote only Grade A sources with automated checks passed, or Grade B/C/D sources with human `approval_status = approved`, into the master registry.

Input:
- Screened staging records
- Policy evidence records
- Reviewer decision

Process:
- Promote eligible records to `master/job_source_registry.csv`.
- Preserve collection scope, allowed method, decision reason, reviewer, and last reviewed timestamp.
- Preserve approval status, approval reviewer, approval reviewed timestamp, and approval notes.
- Keep staging and master separated.

Output:
- `master/job_source_registry.csv`

Acceptance Criteria:
- Master contains only reviewed sources with traceable evidence.
- Master does not contain Grade E, Grade F, pending, rejected, or expired approvals.
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
