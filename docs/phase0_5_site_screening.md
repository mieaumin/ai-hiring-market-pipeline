# Phase 0.5 - Job-Site Evidence Review and Source Screening

Phase 0.5 reviews discovered Korean job sites before any company discovery or JD collection depends on them.

## Goal

Convert raw discovered job-site candidates into screened source candidates through evidence-based review.

## Why Screening Matters

Some sites are technically accessible but still unsuitable for this MVP. A source may be rejected because its Terms of Service prohibit automated collection, because robots.txt blocks target paths, because login or CAPTCHA is required, because anti-bot systems would need bypassing, or because reuse restrictions make the data unsuitable for research.

## Evidence Requirements

Reviewers should collect evidence for:

- robots.txt
- Terms of Service
- privacy policy
- API policy
- login requirement
- CAPTCHA requirement
- anti-bot signals
- public HTML access
- dynamic rendering
- reuse restrictions
- copyright notice

Evidence rows belong in `runtime/site_policy_evidence.csv`.

## Why Traceability Is Required

Every screening decision must explain:

- what evidence was reviewed
- which policy or access risk was found
- why the site is eligible, limited, needs review, or excluded
- who reviewed it and when

Without traceable evidence, a site must stay in `needs_review`.

## Screening Outputs

`runtime/site_screening_results.csv` records source grade, manual review requirement, human approval requirement, approval status, robots and Terms status, access risks, collection eligibility, screening decision, and screening reason.

## Conservative Grade Rules

- Grade A: official API available
- Grade B: public ATS/API endpoint available
- Grade C: public career/job page with acceptable robots.txt and Terms of Service
- Grade D: unclear policy or general scraping needed
- Grade E: login/CAPTCHA/anti-bot/prohibited collection
- Grade F: unusable or blocked

Only A, B, and carefully reviewed C can be approved. D requires manual or legal review. E and F must be rejected.

## Hard Approval Blockers

Never approve a site if:

- robots disallow is detected
- CAPTCHA is required
- login is required
- anti-bot risk is high
- Terms prohibit automated collection
- reuse restriction is critical

## Promotion Boundary

```text
raw discovery
-> policy evidence
-> screening result
-> staging
-> master/job_source_registry
```

No site should move to master merely because it was discovered.
