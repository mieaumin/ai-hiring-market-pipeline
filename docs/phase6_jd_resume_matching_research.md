# Phase 6 - JD-Resume Matching Research

Phase 6 prepares structured JD datasets for future resume matching research.

This phase is not implemented yet. It is documented so the upstream dataset is shaped for matching from the start.

## Goal

Prepare structured JD datasets for future resume matching.

## Flow

```text
jd_master_dataset
-> taxonomy alignment
-> future matching features
```

## Future Tasks

- taxonomy alignment
- skill normalization
- embedding generation
- semantic similarity
- resume-JD ranking
- candidate recommendation

## Inputs

- `master/jd_master_dataset.csv`
- resume datasets
- `configs/taxonomy_v1.yaml`

## Acceptance Criteria

- JD records use stable role groups and skill taxonomy labels.
- Source and company traceability are preserved.
- Future matching features can be generated without revisiting raw collection.

