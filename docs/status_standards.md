# Status Standards

The project uses shared status standards to preserve state management across discovery, screening, collection, and quality gates.

The standards live in `configs/status_standards.yaml`.

## Status Groups

Defined status groups include:

- `site_review_status`
- `collection_eligibility`
- `source_approval_status`
- `source_health_status`
- `screening_decision`
- `jd_validation_status`
- `run_status`

## Important Transition Rules

- A discovered site cannot go directly to approved source.
- A source cannot be approved without evidence.
- JD collection cannot run from rejected, pending, or unknown sources.
- A JD cannot go to master without validation and deduplication.
- E/F grade sources must be rejected.
- D grade sources must require manual or legal review.
- Only A/B/carefully reviewed C can be approved.

## Why This Matters

Biz-Voyager-style pipelines are useful because they track operational states instead of treating discovery as collection. This repository applies that principle to the Korean AI hiring market, where legal and policy review must happen before collection.
