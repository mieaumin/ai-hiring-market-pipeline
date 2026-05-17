# Source Compliance Review

This document defines the compliance-first review policy for the Korean Job Source Registry.

The registry exists to prevent premature or unsafe JD collection. A source must pass review before it can be promoted from staging to the master source registry.

## Core Rule

If robots.txt, Terms of Service, login wall, CAPTCHA, anti-bot controls, API approval requirements, or lack of public HTML access block automated collection, the source must not be treated as approved.

## Exclude a Source When

A source should be excluded if:

- robots.txt explicitly disallows relevant access
- Terms of Service prohibits scraping, crawling, automated access, or data extraction
- login is required for job detail access
- CAPTCHA or anti-bot bypass would be required
- API approval is mandatory and there is no non-API public route
- public HTML access is not available

Excluded sources must not be used for automated JD collection in this MVP.

## Use `needs_manual_review` When

Use `needs_manual_review` if:

- policy wording is ambiguous
- robots.txt is unclear
- Terms page cannot be found
- access behavior is inconsistent
- collection may be possible only manually

Manual review status means the source is not approved yet.

## Use `eligible` Only When

Use `eligible` only if:

- relevant pages are publicly accessible
- robots.txt does not block relevant access
- Terms of Service does not prohibit the planned collection
- no login, CAPTCHA bypass, or anti-bot bypass is required
- the collection method can be explained and audited

Eligibility should be tied to a clear collection scope. For example, a source may be eligible for a public API but not for unrestricted HTML page collection.

## Evidence Requirements

Compliance decisions should be supported by evidence in `runtime/site_policy_evidence.csv`.

Recommended evidence types:

- `robots_txt`
- `terms_of_service`
- `login_requirement`
- `captcha`
- `anti_bot`
- `public_html_access`
- `api_requirement`
- `dynamic_rendering`

Allowed policy status values:

- `allowed`
- `not_allowed`
- `unclear`
- `not_checked`

## Staging to Master Rule

Sources should move to `master/job_source_registry.csv` only after:

- site profile fields are reviewed
- policy evidence is collected
- collection eligibility is set to `eligible`
- approval reason and collection scope are documented
- reviewer and approval timestamp are recorded

Staging rows are candidates. Master rows are approved sources.

