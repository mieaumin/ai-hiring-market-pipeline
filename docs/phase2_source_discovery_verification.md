# Phase 2 - Source Discovery and Verification

Phase 2 finds and verifies each approved company's job posting source.

This phase is schema-first and review-first. It does not implement live collection, scraping, browser automation, API integration, hidden endpoint probing, CAPTCHA solving, or anti-bot bypass.

## Goal

Find and verify each approved company's job posting source.

## Flow

```text
company_registry_master
-> source_discovery
-> source_policy_evidence
-> source_verification
-> source_registry_staging
-> master/source_registry_master
```

## Source Types

- official company career page
- Greenhouse
- Lever
- Ashby
- Work24
- public ATS endpoints
- RSS/sitemap job feeds

## Verification Checks

- official domain match
- robots compatibility
- ToS compatibility
- ATS identification
- public access
- HTML structure quality
- AI JD availability
- maintenance risk

## Source Grades and Approval

| Grade | Meaning | Use policy |
| --- | --- | --- |
| A | Publicly accessible official source with no approval required | Usable after basic automated checks |
| B | Public ATS or public endpoint | Requires human review before use |
| C | Public company career page with acceptable robots.txt and Terms of Service | Requires human review and explicit approval before use |
| D | Official API or source requiring manual application, approval, contract, institutional access, or API key issuance | Approval pending / manual approval required |
| E | General scraping required or policy unclear | Avoid in MVP |
| F | Login required, CAPTCHA required, anti-bot bypass required, robots blocked, or Terms of Service prohibit collection | Prohibited |

Only Grade A can be considered directly usable without manual approval. Grades B, C, and D require human `approval_status = approved` before use. Grade E is rejected for the MVP unless later re-reviewed. Grade F is prohibited.

## Outputs

- `runtime/source_discovery.csv`
- `runtime/source_policy_evidence.csv`
- `runtime/source_verification.csv`
- `staging/source_registry_staging.csv`
- `master/source_registry_master.csv`

## Acceptance Criteria

- Source discovery starts only from approved company records.
- Source policy evidence is traceable.
- Source grades are explainable.
- Grade B, C, and D sources do not move forward until human approval is recorded.
- Grade E and F sources do not move forward in the MVP.
- Source registry staging is separate from source registry master.

