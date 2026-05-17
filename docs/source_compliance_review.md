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

Rules:

- Grade A: `human_approval_required = false`, `approval_status = not_required`
- Grade B: `human_approval_required = true`, `approval_status = pending` until reviewed
- Grade C: `human_approval_required = true`, `approval_status = pending` until reviewed
- Grade D: `human_approval_required = true`, `approval_status = pending` until external/API approval is completed
- Grade E: `human_approval_required = true`, `approval_status = rejected` for MVP unless later re-reviewed
- Grade F: `human_approval_required = false`, `approval_status = rejected`

A source must not move to an approved source registry unless:

- `source_grade` is A and automated checks passed, or
- `source_grade` is B, C, or D and human `approval_status` is `approved`.

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
Use only for publicly accessible official sources with no approval required. Grade A can be used after basic automated checks pass and should carry `approval_status = not_required`.

Grade B:
Use for public ATS or public endpoints. Grade B requires human review and `approval_status = approved` before use.

Grade C:
Use for public company career pages with acceptable robots.txt and Terms of Service. Grade C requires human review, explicit approval, and `approval_status = approved` before use.

Grade D:
Use for official APIs or sources requiring manual application, approval, contract, institutional access, or API key issuance. Grade D requires external/API approval completion and human `approval_status = approved` before use.

Grade E:
Use when general scraping is required or policy is unclear. Grade E should be rejected for the MVP unless later re-reviewed.

Grade F:
Use when login, CAPTCHA, anti-bot bypass, robots blocking, or Terms prohibition applies. Grade F is prohibited.

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

