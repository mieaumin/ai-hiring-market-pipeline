# Phase 1 - Company Discovery

Phase 1 identifies companies that are relevant to the AI hiring market before any JD source registry or JD collection work begins.

The goal is not to collect job posts at scale. The goal is to create an explainable candidate company pool with evidence-backed signals.

## Why This Comes Before JD Collection

Company Discovery is intentionally placed before JD collection because the project must first define which companies are relevant to the AI hiring market before attempting to identify job posting sources or collect JDs.

This protects the project from unfocused crawling and keeps the MVP research process explainable.

## Inputs

- `configs/company_seed.csv`
- Public company websites
- Public company career pages
- News, public records, investment articles, tech blogs, and product pages
- Manually reviewed evidence

## Outputs

- `runtime/company_candidates.csv`
- `runtime/company_evidence.csv`

## Signal Groups

| Signal | Meaning |
| --- | --- |
| `hiring_signal` | Evidence that the company currently hires or has hired AI, ML, data, or research talent |
| `business_ai_signal` | Evidence that AI or data is part of the business, product, or service |
| `tech_signal` | Evidence of technical depth such as tech blogs, GitHub, papers, patents, or ML infrastructure |
| `market_signal` | Evidence that the market context supports AI hiring, such as funding, public AI projects, or industry fit |
| `evidence_quality` | Reliability, freshness, and reviewability of the evidence |

## Candidate Status

| Status | Meaning |
| --- | --- |
| `seeded` | Initial company seed only |
| `needs_review` | Evidence is incomplete or uncertain |
| `candidate` | Evidence suggests possible relevance |
| `approved_for_source_discovery` | Ready for Phase 2 source registry review |
| `rejected` | Not relevant enough for the MVP |

## Review Checklist

- Does the company have a plausible AI hiring need?
- Is there evidence beyond a vague AI keyword?
- Is the company domain clear?
- Are evidence URLs public and reviewable?
- Does the evidence support the assigned signal category?
- Is the company ready for source registry evaluation?

## MVP Rule

Only companies with clear evidence and a useful score should move to Phase 2. The project should prefer smaller, high-quality candidate pools over large unverified lists.
