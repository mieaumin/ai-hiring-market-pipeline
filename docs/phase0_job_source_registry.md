# Phase 0 - Korean Job Source Registry Construction

Phase 0 builds a compliance-first registry of Korean job posting sources before any JD collection begins.

This is not a crawling phase. It does not collect job postings, scrape pages, call live APIs, automate browsers, or bypass access controls. Its output is an approved source registry created only after source discovery, evidence collection, and compliance review.

## Phase 0 Pipeline

```text
0-0 Source Discovery Strategy Definition
0-1 Raw Job Site Discovery
0-2 Site Canonicalization
0-3 Site Profiling
0-4 Policy Evidence Collection
0-5 Compliance Review
0-6 Eligibility Decision
0-7 Approved Source Registry
0-8 Source Monitoring
```

## 0-0 Source Discovery Strategy Definition

Purpose:
Define how Korean job posting sources will be discovered, grouped, reviewed, and moved through the registry workflow.

Input:
- Project scope
- Target AI JD discovery needs
- Existing company-first pipeline goals
- Legal and ethics policy

Process:
- Define source categories such as public job boards, company career pages, public ATS pages, government/public job portals, and manually discovered sources.
- Define acceptable discovery methods such as manual search, public directories, company career links, sitemap references, official documentation, and public policy pages.
- Define minimum evidence required before any source can become approved.

Output:
- A documented discovery strategy
- Review criteria for source eligibility
- CSV templates for raw discovery, staging, evidence, candidates, and master registry

Acceptance Criteria:
- The strategy explicitly says Phase 0 is not a crawling phase.
- Discovery methods are explainable and auditable.
- Compliance review is required before approval.

## 0-1 Raw Job Site Discovery

Purpose:
Capture potential Korean job posting sources without deciding whether they are allowed for collection.

Input:
- Manual search results
- Company career page references
- Public job portal names
- Public ATS references
- Research notes

Process:
- Record each discovered source in `runtime/raw_job_site_discovery.csv`.
- Keep only descriptive metadata and evidence links.
- Do not collect job postings.
- Do not infer approval from discovery alone.

Output:
- Header-based raw discovery dataset
- Source candidates ready for canonicalization

Acceptance Criteria:
- Each row has a source name or URL.
- Discovery method is recorded.
- Evidence link or notes explain why the source was found.
- No fake rows or collected JD data are added.

## 0-2 Site Canonicalization

Purpose:
Normalize discovered sources so duplicate sites, alternate URLs, and subdomains can be reviewed consistently.

Input:
- `runtime/raw_job_site_discovery.csv`
- Source URLs
- Public domain information

Process:
- Identify canonical domains.
- Normalize URLs to a stable site-level reference.
- Group duplicate entries that refer to the same source.
- Assign or prepare stable `site_id` values.

Output:
- Canonical source records ready for staging
- Reduced duplicate source candidates

Acceptance Criteria:
- Each staged source has one canonical domain.
- Duplicate source entries are identified or merged.
- The canonical URL is reviewable by a human.

## 0-3 Site Profiling

Purpose:
Describe each job source in terms of coverage, AI relevance, access pattern, and operational risk.

Input:
- Canonical source records
- Public source pages
- Manual review notes

Process:
- Record site type, country, job coverage, tech job density, and AI job relevance.
- Review whether search and keyword search are supported.
- Record visible access characteristics such as login requirements, public HTML access, and dynamic rendering risk.
- Save the profile in `staging/job_site_registry_staging.csv`.

Output:
- Staged job source registry records

Acceptance Criteria:
- Site profile fields are filled from public, reviewable evidence.
- No source is marked approved during profiling.
- Unknown or ambiguous fields remain reviewable rather than guessed.

## 0-4 Policy Evidence Collection

Purpose:
Collect evidence needed to decide whether a source is legally and operationally eligible for future collection.

Input:
- Staged source records
- robots.txt URLs
- Terms of Service pages
- Public access observations
- API documentation or approval requirement notes

Process:
- Record evidence in `runtime/site_policy_evidence.csv`.
- Use evidence types such as `robots_txt`, `terms_of_service`, `login_requirement`, `captcha`, `anti_bot`, `public_html_access`, `api_requirement`, and `dynamic_rendering`.
- Store short excerpts and review notes.
- Mark policy status as `allowed`, `not_allowed`, `unclear`, or `not_checked`.

Output:
- Evidence records for compliance review

Acceptance Criteria:
- Evidence is tied to a `site_id`.
- Evidence source URLs are recorded when available.
- The policy status is explicit.
- Ambiguous evidence is not treated as approval.

## 0-5 Compliance Review

Purpose:
Apply compliance-first rules before any source is considered eligible for collection.

Input:
- `staging/job_site_registry_staging.csv`
- `runtime/site_policy_evidence.csv`
- Legal and ethics policy
- Source selection criteria

Process:
- Review robots.txt, Terms of Service, login requirements, CAPTCHA risk, anti-bot risk, public HTML access, and API requirements.
- Exclude sources when access is blocked or prohibited.
- Use `needs_manual_review` when policy wording or access behavior is ambiguous.
- Document the review reason.

Output:
- Reviewed source candidate records in `config/job_site_candidates.csv`

Acceptance Criteria:
- A source is not eligible unless its planned collection method can be explained and audited.
- A source is excluded if automated collection would require bypass, prohibited access, login, CAPTCHA solving, or API approval without a public non-API route.
- Review status is never left implicit.

## 0-6 Eligibility Decision

Purpose:
Decide whether a source can be used in future JD collection phases.

Input:
- Reviewed candidate records
- Policy evidence
- Compliance review notes

Process:
- Assign `collection_eligibility` as `eligible`, `needs_manual_review`, or `excluded`.
- Assign `review_status` as `not_checked`, `checked`, or `needs_manual_review`.
- Record the review reason and unresolved risks.

Output:
- A compliance-reviewed source candidate table

Acceptance Criteria:
- `eligible` is used only when public access, robots.txt, Terms of Service, and operational risk checks are acceptable.
- `needs_manual_review` is used for ambiguity.
- `excluded` is used for blocked, prohibited, login-only, CAPTCHA-protected, anti-bot, or API-approval-only sources.

## 0-7 Approved Source Registry

Purpose:
Create the master registry of sources approved for future collection.

Input:
- `config/job_site_candidates.csv`
- Policy evidence records
- Reviewer decision

Process:
- Promote only eligible sources to `master/job_source_registry.csv`.
- Record approved collection scope, approval reason, approver, approval timestamp, and monitoring status.
- Keep staging and master separated.

Output:
- `master/job_source_registry.csv`

Acceptance Criteria:
- Only compliance-reviewed eligible sources are included.
- Approval scope is explicit.
- The master registry contains no unreviewed or fake rows.

## 0-8 Source Monitoring

Purpose:
Keep approved sources auditable over time as policies, access behavior, and site structure change.

Input:
- Master source registry
- Last checked timestamps
- New policy evidence
- Manual monitoring notes

Process:
- Re-check source policy and access assumptions on a recurring schedule.
- Update monitoring status when a source becomes stale, changed, blocked, or needs manual review.
- Do not continue using a source if approval evidence becomes invalid.

Output:
- Updated master registry and policy evidence records

Acceptance Criteria:
- Each approved source has `last_checked_at`.
- Monitoring status identifies whether the source is active, stale, changed, paused, or needs review.
- Sources are removed or paused if compliance requirements are no longer met.

