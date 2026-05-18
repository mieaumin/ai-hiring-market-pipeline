# Promotion Rules

Promotion rules define when a record can move from raw or staging tables into reviewed outputs.

The rules live in `configs/promotion_rules.yaml`.

## Raw Job-Site Discovery to Site Screening

Required fields:

- `site_id`
- `site_url`
- `site_domain`
- `discovery_route`

Raw discovery must not already have `review_status = approved`.

## Site Screening to Master Job Source Registry

Allowed only if:

- `source_grade` is A, B, or C
- `approval_status` is `approved` or `not_required`
- `collection_eligibility` is `eligible` or `limited`
- `screening_decision` is `approved` or `limited`
- no approval blockers exist
- evidence is traceable

Blockers include:

- `robots_disallow`
- `terms_prohibit_automated_collection`
- `login_required`
- `captcha_required`
- `high_anti_bot_risk`
- `critical_reuse_restriction`
- `missing_traceable_evidence`

## Company Candidate to Company Master

Allowed only if:

- total score meets the threshold
- `validation_status = approved_for_source_discovery`
- evidence quality is present
- company is Korean or Korea-relevant

## JD Staging to JD Master

Allowed only if:

- title, company, source URL, and job URL exist
- cleaned JD text is at least 200 characters
- role group is one of the target AI roles
- validation status is ready for master review
- duplicate cluster is resolved
- canonical or accepted source lineage exists
- source is approved

No raw JD moves directly into master.
