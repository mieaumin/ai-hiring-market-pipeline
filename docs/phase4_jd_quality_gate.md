# Phase 5 - JD Normalization, Deduplication, Labeling

Phase 5 filters unusable, non-AI, duplicate, and low-quality JDs before master dataset promotion.

This phase protects the master dataset from raw or weak JD records. It does not fetch live pages or call external APIs.

## Goal

Filter unusable, non-AI, duplicate, and low-quality JDs.

## Flow

```text
raw_jds
-> validation
-> normalization
-> AI role filtering
-> deduplication
-> staging/jd_staging.csv
```

## Validation Rules

- required fields exist
- minimum description length
- AI keyword match
- taxonomy match
- source approved
- duplicate removal

## AI Role Groups

- AI Engineer
- AI Researcher
- AI Scientist
- AI Analyst

## Outputs

- `data/cleaned/cleaned_jds.csv`
- `staging/jd_staging.csv`
- `runtime/jd_validation_errors.csv`

## Acceptance Criteria

- JDs without required fields fail validation.
- JDs from invalid source approval states fail validation.
- Non-AI JDs do not move to staging.
- Duplicate JDs are removed before staging.
- Each staged JD links back to an approved source.
- Staging remains separate from the master dataset.
