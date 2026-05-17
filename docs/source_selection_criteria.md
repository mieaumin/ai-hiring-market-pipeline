# Source Selection Criteria

Every job posting source must pass strict screening before any collector can be considered in a future phase.

This project follows a Biz-Voyager-inspired broad discovery -> evidence review -> screening -> staging -> master workflow, but uses stricter legal, policy, and approval gates before any JD collection.

## Required Flow

```text
raw_job_site_discovery
-> site_policy_evidence
-> job_site_registry_staging
-> site_screening
-> master/job_source_registry
```

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

## Approval Status

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

## Strict Approval Gates

A source can move forward only when the grade and approval state allow it. Reviewers should still check:

- target job pages are not blocked by robots.txt
- Terms of Service do not prohibit crawling, scraping, automated collection, copying, extraction, reuse, or redistribution
- no login is required
- no CAPTCHA is required
- no anti-bot bypass is required
- public HTML or approved API/endpoint access is available
- collection can be done conservatively with low request volume
- collected data can be limited to necessary JD fields and source links

If policy or access is unclear, assign Grade E and reject it for the MVP unless later re-reviewed.

## Prohibited Collection Methods

- Login automation
- CAPTCHA solving
- IP rotation
- Header or browser behavior spoofing for evasion
- Browser automation for bypassing controls
- Any collection that violates robots.txt, site terms, approval requirements, or access restrictions

