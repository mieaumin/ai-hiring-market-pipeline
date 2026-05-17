# Phase 1 - Company Discovery Registry Construction

Phase 1 builds an evidence-backed AI hiring company registry. It is a recall-first discovery and screening workflow, not a JD collection workflow.

This project follows Biz-Voyager's broad discovery -> evidence review -> screening -> staging -> master philosophy, but applies stricter evidence gates before a company can be treated as relevant to the AI hiring market.

This phase does not collect JDs. It does not crawl company websites, run scrapers, call APIs, automate browsers, use LLM APIs, or perform live collection. It creates a reviewable company candidate registry that can later support source discovery and JD collection.

Companies should only move to master after evidence review. A raw company name is not an approved company record.

## Phase 1 Pipeline

```text
1-0 Company Discovery Strategy Definition
1-1 Raw Company Seed Collection
1-2 Company Canonicalization
1-3 Company Profile Enrichment
1-4 AI Hiring Evidence Collection
1-5 Company Signal Scoring
1-6 Company Screening Decision
1-7 Approved Company Registry
1-8 Company Monitoring
```

Required artifact flow:

```text
raw_company_discovery
-> company_evidence_review
-> company_registry_staging
-> company_screening
-> master/company_registry_master
```

## 1-0 Company Discovery Strategy Definition

Purpose:
Define how company candidates will be discovered, reviewed, scored, and promoted through the registry.

Input:
- HEDING AI matching MVP scope
- Target AI roles and research goals
- Company screening policy
- Signal scoring schema

Process:
- Define recall-first discovery methods such as manual seed lists, public reports, public company directories, public career page references, public AI program references, and manually reviewed evidence.
- Define what counts as reliable evidence.
- Define raw, staging, and master registry boundaries.
- Define screening statuses and review responsibilities.
- Define company evidence categories: `hiring_signal`, `business_ai_signal`, `tech_signal`, `market_signal`, `research_signal`, and `evidence_quality`.

Output:
- A documented company discovery strategy
- Reviewable CSV templates
- Clear promotion rules from raw to staging to master

Acceptance Criteria:
- The strategy explicitly states that this phase does not collect JDs.
- The strategy explicitly states that this phase does not crawl company websites.
- Promotion requires traceable evidence and human review.

## 1-1 Raw Company Seed Collection

Purpose:
Collect broad company candidates that may be relevant to the AI hiring market without treating them as approved.

Input:
- Manual seed lists
- Public articles, reports, directories, and research notes
- Company names and URLs discovered during source or market review
- Public references to AI hiring, AI products, AI research, or AI partnerships

Process:
- Record raw candidates in `runtime/raw_company_discovery.csv`.
- Preserve raw names and raw URLs without forcing early normalization.
- Record discovery method, discovery source, reviewer, and preliminary reason.
- Avoid invented companies and fake rows.
- Do not approve a company because its name sounds AI-related.

Output:
- Header-based raw company discovery table
- Broad company candidate pool for canonicalization

Acceptance Criteria:
- Each row has a raw company name or raw company URL.
- Discovery method and preliminary reason are recorded.
- Raw records are not treated as approved companies.
- No JD collection occurs.

## 1-2 Company Canonicalization

Purpose:
Convert raw company candidates into stable, reviewable company records.

Input:
- `runtime/raw_company_discovery.csv`
- Public company names and URLs
- Manual reviewer notes

Process:
- Normalize company names into canonical company names.
- Identify duplicate candidates.
- Assign stable `company_id` values.
- Record country, company URL, and initial company type when known.
- Track company status as `seeded`, `candidate`, `needs_review`, `approved_for_source_discovery`, or `rejected`.
- Keep ambiguous name/domain matches in review status rather than guessing.

Output:
- Canonical company candidates in `runtime/company_candidates.csv`

Acceptance Criteria:
- Each candidate has a stable `company_id`.
- Canonical names are reviewable.
- Ambiguous company matches are marked for manual review.

## 1-3 Company Profile Enrichment

Purpose:
Add lightweight company profile metadata needed for screening and later source discovery.

Input:
- Canonical company candidates
- Public company profile evidence
- Manual reviewer notes

Process:
- Add country, industry, company size estimate, company type, and AI hiring relevance where evidence supports it.
- Record source discovery status and evidence status.
- Do not use automated crawling or live collection.
- Leave unknown fields blank or reviewable instead of inventing data.

Output:
- Enriched company candidate records
- Profile fields ready for evidence review

Acceptance Criteria:
- Profile fields are based on traceable evidence or marked unknown.
- No company is approved solely from profile enrichment.
- Uncertain fields are documented in notes or review reason.

## 1-4 AI Hiring Evidence Collection

Purpose:
Collect traceable evidence that explains why a company may belong in the AI hiring market universe.

Input:
- Canonical company candidates
- Public evidence sources
- Manual review observations

Process:
- Record evidence rows in `runtime/company_evidence.csv`.
- Use evidence types such as `ai_job_posting`, `ai_product_or_service`, `ai_research_lab`, `tech_blog`, `github_org`, `investment_signal`, `government_ai_program`, `ai_partnership`, `press_release`, `career_page`, and `other`.
- Assign signal categories such as `hiring_signal`, `business_ai_signal`, `tech_signal`, `market_signal`, `research_signal`, and `evidence_quality`.
- Record evidence excerpt, evidence source URL, checked timestamp, reviewer, confidence, and notes.

Output:
- Evidence table linked to company candidates
- Reviewable signal basis for company scoring

Acceptance Criteria:
- Every promoted company candidate has at least one evidence row.
- Master promotion requires at least two reliable evidence rows.
- Evidence source URLs are traceable when available.
- Weak signals alone do not approve a company.
- A company must not move to master unless its evidence is traceable in `runtime/company_evidence.csv`.

## 1-5 Company Signal Scoring

Purpose:
Score company candidates with explainable evidence-based categories.

Input:
- `runtime/company_candidates.csv`
- `runtime/company_evidence.csv`
- `configs/company_signal_schema.yml`

Process:
- Score each company from 0 to 5 for each category:
  - `hiring_signal_score`
  - `business_ai_signal_score`
  - `tech_signal_score`
  - `market_signal_score`
  - `research_signal_score`
  - `evidence_quality_score`
- Sum category scores into `total_signal_score`.
- Store scoring results in `staging/company_registry_staging.csv`.

Output:
- Scored company registry staging table

Acceptance Criteria:
- Scores are supported by evidence rows.
- A high score is explainable from evidence, not intuition.
- Missing or weak evidence lowers score or triggers manual review.

## 1-6 Company Screening Decision

Purpose:
Decide whether a company candidate should be approved, reviewed manually, or excluded.

Input:
- Staging company scores
- Evidence rows
- Company screening policy

Process:
- Assign `screening_status` as `not_reviewed`, `candidate`, `approved`, `needs_manual_review`, or `excluded`.
- Update `company_status` as `seeded`, `candidate`, `needs_review`, `approved_for_source_discovery`, or `rejected`.
- Assign `review_status` as `not_checked`, `checked`, or `needs_manual_review`.
- Record review reason and notes.
- Require evidence-backed reasoning for approval or exclusion.
- Apply company screening after staging and before master promotion.

Output:
- Reviewed staging records
- Clear approval, manual review, or exclusion decisions

Acceptance Criteria:
- `approved` requires evidence review.
- `needs_manual_review` is used for ambiguity.
- `excluded` is used when reliable AI hiring or AI business evidence is absent.

## 1-7 Approved Company Registry

Purpose:
Promote reviewed companies into the master company registry for future source discovery and JD collection planning.

Input:
- Reviewed staging records
- Evidence records
- Screening decisions

Process:
- Promote only approved companies to `master/company_registry_master.csv`.
- Record approval reason, approver, approval timestamp, last checked timestamp, monitoring status, and notes.
- Keep staging and master separated.

Output:
- Master company registry

Acceptance Criteria:
- Master contains only reviewed and approved companies.
- Each master company has traceable evidence.
- Approval reason explains why the company belongs in the AI hiring market universe.
- No company is approved only because of its name, branding, or vague AI wording.

## 1-8 Company Monitoring

Purpose:
Keep company registry decisions current over time.

Input:
- Master company registry
- Updated evidence rows
- Review notes

Process:
- Re-check approved companies on a recurring review schedule.
- Update monitoring status when evidence becomes stale, company relevance changes, or source discovery readiness changes.
- Move companies back to manual review if evidence becomes outdated or invalid.

Output:
- Updated master registry and evidence records

Acceptance Criteria:
- Each approved company has `last_checked_at`.
- Monitoring status is explicit.
- Stale or uncertain companies are not silently treated as approved.
