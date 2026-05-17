# Legal and Ethics Policy

This project is a research MVP. It must prioritize legal, ethical, and policy-compliant collection.

## What We Avoid

We avoid prohibited scraping because the project should be reproducible, explainable, and safe for research use. Data collected through access bypass, login automation, CAPTCHA solving, or anti-bot evasion can create legal, ethical, and data quality risks.

The project does not implement:

- Illegal scraping
- CAPTCHA solving
- Login automation
- IP rotation
- Anti-bot bypass logic
- Autonomous browser agents
- Collection from sources that prohibit automated access

## Why We Prefer Official APIs and Public ATS Endpoints

Official APIs and public ATS endpoints are preferred because they usually provide:

- Stable structured data
- Clear access patterns
- Lower maintenance cost
- Better traceability
- Lower legal and operational risk

Public company career pages may be used only after robots.txt and terms are reviewed.

## Source Registry Requirement

Before adding a new collector, the source must be entered into the source registry and reviewed. The registry decision determines whether the source is allowed for MVP collection.

The approved-source-only runner can collect only from `master/source_registry_master.csv` rows that pass the collection guard. A source is blocked if it is not approved, has pending/rejected/expired approval, is Grade E or F, has robots.txt or Terms restrictions, requires login or CAPTCHA, has high anti-bot risk, lacks public HTML access, or has unresolved API approval requirements.

If no approved crawl-eligible source exists, collection is skipped. The runner must not manually mark sources as approved, reinterpret unclear policy, or collect from risky sources.

## Future JD-Resume Matching

Ethical collection matters because future matching models depend on trustworthy data. Poorly sourced or policy-violating data can harm research quality and make the matching pipeline hard to defend.
