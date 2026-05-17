# Company Screening Policy

This policy defines how raw company candidates become reviewed company registry records.

Company discovery is recall-first, but approval is evidence-first. A raw company does not equal an approved company. Raw discovery is only the first step in building an explainable AI hiring company registry.

This project follows Biz-Voyager's broad discovery -> evidence review -> screening -> staging -> master philosophy. For company discovery, that means broad candidate discovery is allowed, but promotion requires traceable evidence and an explainable screening decision.

## Core Rules

- Companies must have evidence before promotion.
- Evidence must be traceable to a public or reviewable source.
- Weak signals alone should not approve a company.
- Company candidates should move through raw -> evidence -> staging -> screening -> master.
- Approval must be explainable.
- No fake companies or invented evidence should be added.
- Company candidates are not approved until reviewed.

## Registry Flow

```text
runtime/raw_company_discovery.csv
-> runtime/company_evidence.csv
-> company_evidence_review
-> staging/company_registry_staging.csv
-> company_screening
-> master/company_registry_master.csv
```

## Evidence Expectations

Evidence should explain why a company belongs in the AI hiring market universe. A company must not be approved only because its name sounds AI-related.

Company evidence categories:

- `hiring_signal`
- `business_ai_signal`
- `tech_signal`
- `market_signal`
- `research_signal`
- `evidence_quality`

Useful evidence may include:

- AI job posting
- AI product or service
- AI research lab
- Tech blog
- GitHub organization
- Investment signal
- Government AI program
- AI partnership
- Press release
- Career page

Evidence should include:

- source URL when available
- short excerpt or summary
- signal category
- signal strength
- checked timestamp
- reviewer
- confidence level

## Approved

Approve a company only if:

- company has at least 2 reliable evidence rows
- at least one evidence row is `hiring_signal` or `business_ai_signal`
- total score meets threshold
- reviewer can explain why this company belongs in the AI hiring market universe
- evidence is traceable in `runtime/company_evidence.csv`

Approved companies may move from staging to `master/company_registry_master.csv`.

## Needs Manual Review

Use `needs_manual_review` if:

- company looks relevant but evidence is weak
- evidence source is outdated
- company name/domain matching is ambiguous
- AI relevance is unclear

Manual review means the company is not approved yet.

## Excluded

Exclude a company if:

- no AI hiring relevance is found
- no reliable evidence is available
- company is unrelated to the target market
- evidence cannot be verified

Excluded companies should remain explainable. The review reason should say why the company was excluded.

## Weak Signal Guidance

Weak signals can support discovery but should not drive approval by themselves. Examples of weak signals include vague AI marketing language, one outdated article, unverified social posts, or generic tech hiring without AI/Data/ML relevance.

Weak signals should usually lead to `candidate` or `needs_manual_review`, not `approved`.

## Staging to Master Rule

A company may move to master only after:

- evidence rows are reviewed
- signal scores are assigned
- screening status is `approved`
- approval reason is documented
- approver and approval timestamp are recorded
- company evidence remains traceable and reviewable

Master is the approved registry. Staging is the review workspace.
