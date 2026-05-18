# Phase 2/3 - Company Source Discovery and Source Verification

Phase 2 discovers each approved company's job posting source. Phase 3 verifies whether that company-specific source is usable.

This phase is schema-first and review-first. It does not implement live collection, scraping, browser automation, API integration, hidden endpoint probing, CAPTCHA solving, or anti-bot bypass.

## Goal

Find and verify each approved company's job posting source without collecting JDs.

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
| A | Official API available | Can be approved if policy and evidence are valid |
| B | Public ATS/API endpoint available | Can be approved if public access and policy evidence are valid |
| C | Public company career page or public job page with acceptable robots.txt and Terms of Service | Can be approved only after careful human review |
| D | Unclear policy, general scraping needed, or human/legal review required | Must remain `needs_manual_review` or `needs_legal_review` |
| E | Login, CAPTCHA, anti-bot bypass, or prohibited automated collection required | Reject |
| F | Unusable, blocked, or legally/policy-wise rejected | Reject |

Only A, B, and carefully reviewed C can be approved. Grade D must remain in manual or legal review. Grades E and F are rejected.

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
- Grade B and C sources do not move forward until human approval is recorded.
- Grade D sources remain in manual or legal review and do not move forward in the MVP.
- Grade E and F sources do not move forward in the MVP.
- Source registry staging is separate from source registry master.
