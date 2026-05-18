# Source Relationship Graph

Although the MVP uses CSV files, the pipeline is fundamentally a relationship graph.

The core chain is:

```text
job_site -> company -> career_page -> ATS -> endpoint -> JD
```

Example graph paths:

```text
Korean job portal -> Korean company -> official career page -> ATS -> public endpoint -> AI Engineer JD
Korean startup platform -> startup -> company career page -> custom HTML -> JD page
```

## Canonical Source vs Aggregator Source

A canonical source is the most authoritative source for a JD. It is usually:

- an official company career page
- an approved official API
- an approved ATS endpoint used directly by the company

An aggregator source is a secondary source that lists, mirrors, links to, or summarizes jobs from many organizations.

Aggregators can help discovery, but they should not automatically outrank canonical sources for master data.

## Upstream and Downstream Relationships

Relationship modeling helps answer:

- Which job site discovered the company?
- Which company owns the official source?
- Which ATS infrastructure powers the career page?
- Which endpoint produced the JD?
- Which source is canonical when the same JD appears in multiple places?

## Suggested Relationship Types

Relationship types are defined in `configs/source_relationship_types.yaml`:

- `aggregates`
- `mirrors`
- `links_to`
- `official_source_for`
- `uses_ats`
- `exposes_endpoint`
- `contains_jd`
- `duplicates`
- `canonicalizes_to`

## Runtime Tracking

Relationships should be recorded in `runtime/source_relationships.csv`.

Important fields include:

- source node and target node identifiers
- node types
- relationship type
- confidence
- evidence URL
- canonical candidate flag
- review status

This keeps the CSV-based MVP compatible with a future graph database or network analysis layer.
