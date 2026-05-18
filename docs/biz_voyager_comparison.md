# Biz-Voyager Comparison

This project borrows Biz-Voyager's operating philosophy, but it applies it to a stricter Korean AI hiring market workflow.

## Biz-Voyager Pattern

Biz-Voyager starts from a company-oriented discovery workflow:

```text
company discovery
-> source discovery
-> source verification
-> job collection
-> quality gate
-> master dataset
```

The useful ideas are:

- recall-first discovery
- evidence review before promotion
- staging/master separation
- quality gates
- operational logs
- explainable promotion rules

## This Project's Pattern

This project adds an earlier Korean job-site universe layer:

```text
Korean job-site discovery
-> job-site evidence review and screening
-> Korean AI hiring company discovery
-> company source discovery
-> source verification
-> JD collection from approved sources only
-> JD normalization, deduplication, labeling
-> future JD-resume matching
```

## Key Differences

The biggest differences are:

- The project starts with Korean job-site discovery, not company discovery.
- Korean job-site sources are screened before they can influence downstream collection.
- Source compliance gates are stricter and earlier.
- Company discovery uses AI hiring likelihood, not generic AI company classification.
- JD collection is blocked until source approval exists.
- The final data target is future JD-resume matching research.

## Why This Matters

Korean job data often appears across portals, communities, company pages, and ATS-backed pages. A broad source universe helps with recall, but broad discovery does not imply collection eligibility.

The pipeline therefore separates:

- discovered site
- screened site
- approved source
- company-specific source
- canonical JD source

This separation keeps the system explainable and reduces legal, policy, and data quality risk.
