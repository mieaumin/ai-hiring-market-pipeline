# Source Compliance Review

This document defines strict compliance-first review for the Korean Job Site Registry.

The project follows Biz-Voyager's broad discovery -> evidence review -> screening -> staging -> master philosophy, but applies stricter legal, policy, and approval gates before any JD collection. A source must pass source compliance review before it can appear in `master/job_source_registry.csv`.

## Required Source Flow

```text
raw_job_site_discovery
-> site_policy_evidence
-> job_site_registry_staging
-> site_screening
-> master/job_source_registry
```

## Source Grades and Approval Status

| Grade | Meaning | Use policy |
| --- | --- | --- |
| A | Official API available | Can be approved if policy and evidence are valid |
| B | Public ATS/API endpoint available | Can be approved if public access and policy evidence are valid |
| C | Public company career page or public job page with acceptable robots.txt and Terms of Service | Can be approved only after careful human review |
| D | Unclear policy, general scraping needed, or human/legal review required | Must remain `needs_manual_review` or `needs_legal_review` |
| E | Login, CAPTCHA, anti-bot bypass, or prohibited automated collection required | Reject |
| F | Unusable, blocked, or legally/policy-wise rejected | Reject |

Only A, B, and carefully reviewed C can be approved. "Carefully reviewed" means human approval is required.

Allowed `approval_status` values:

- `not_required`
- `pending`
- `approved`
- `rejected`
- `expired`

Rules:

- Grade A: `human_approval_required = false`, `approval_status = not_required`
- Grade B: `human_approval_required = true`, `approval_status = pending` until reviewed
- Grade C: `human_approval_required = true`, `approval_status = pending` until reviewed
- Grade D: `human_approval_required = true`, remains in manual/legal review and cannot be used in the MVP until ambiguity is resolved
- Grade E: `human_approval_required = true`, `approval_status = rejected`
- Grade F: `human_approval_required = false`, `approval_status = rejected`

A source must not move to an approved source registry unless:

- `source_grade` is A and automated checks passed, or
- `source_grade` is B or C and human `approval_status` is `approved`.

## Terms of Service Review Checklist

Reviewers must check for:

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

Relevant text should be recorded as an evidence excerpt, not paraphrased into approval.

## Grade Guidance

Grade A:
Use for official APIs with valid policy and evidence. Grade A can be used after basic automated checks pass and should carry `approval_status = not_required`.

Grade B:
Use for public ATS/API endpoints. Grade B requires human review and `approval_status = approved` before use.

Grade C:
Use for public company career pages or public job pages with acceptable robots.txt and Terms of Service. Grade C requires human review, explicit approval, and `approval_status = approved` before use.

Grade D:
Use when policy is unclear, general scraping appears necessary, or human/legal review is required. Grade D remains in review and is not used for MVP collection.

Grade E:
Use when login, CAPTCHA, anti-bot bypass, or prohibited automated collection is required. Grade E is rejected.

Grade F:
Use when the source is unusable, blocked, or legally/policy-wise rejected. Grade F is rejected.

## Approved Registry Requirements

Approved source registry rows must include:

- source grade
- manual review requirement
- human approval requirement
- approval status
- approval reviewer when applicable
- approval reviewed timestamp when applicable
- approval notes
- collection scope
- allowed method
- decision reason
- reviewer
- last reviewed timestamp

## Evidence Requirements

`runtime/site_policy_evidence.csv` should capture:

- `evidence_id`
- `site_id`
- `site_name`
- `evidence_category`
- `evidence_url`
- `evidence_text_excerpt`
- `policy_keyword_found`
- `risk_level`
- `reviewer`
- `reviewed_at`
- `decision`
- `notes`

Evidence categories may include robots.txt, Terms of Service, login requirement, CAPTCHA, anti-bot, public HTML access, API requirement, dynamic rendering, personal data, database right, copyright, and reuse restriction.
