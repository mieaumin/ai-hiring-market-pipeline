# Phase 5 - JD Master Dataset

The master dataset is the final output of Phase 5 after JD normalization, deduplication, labeling, and quality gate review.

## Goal

Promote only validated high-quality AI JDs.

## Flow

```text
jd_staging
-> quality_gate
-> master/jd_master_dataset.csv
```

## Promotion Conditions

- source is approved under the strict source gate
- schema is valid
- AI role is classified
- duplicate is removed
- quality score threshold is passed
- traceability to source and company is preserved

## Outputs

- `master/jd_master_dataset.csv`
- `data/labeled/labeled_jds.csv`
- `runtime/quality_gate_report.csv`

## Acceptance Criteria

- Master contains no raw unvalidated JD rows.
- Every master JD has a `source_id`, `company_id`, `job_url`, `content_hash`, and `quality_score`.
- Every promoted JD has a valid source approval state.
- Master promotion reason is auditable through quality gate outputs.
