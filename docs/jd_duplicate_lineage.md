# JD Duplicate Lineage

The same JD can appear in multiple places:

- company official page
- ATS page
- aggregator site
- mirrored repost
- community repost

Duplicate handling should therefore track lineage, not just remove rows.

## Lineage Types

Lineage types are defined in `configs/jd_lineage_types.yaml`:

- `canonical_jd`
- `mirrored_jd`
- `aggregator_jd`
- `reposted_jd`
- `unknown`

## Why Lineage Matters

Lineage matters because:

- the canonical source should usually outrank aggregators
- duplicate rows can inflate market demand signals
- reposts can make old roles look active
- mirrored pages may omit or alter job details
- freshness tracking needs to know which source changed
- JD-resume matching quality depends on clean, deduplicated JD records

## Suggested Fields

`runtime/jd_lineage.csv` records:

- `lineage_id`
- `jd_id`
- `canonical_jd_id`
- `duplicate_cluster_id`
- `canonical_source_id`
- `observed_source_id`
- `source_priority_score`
- `lineage_type`
- `lineage_confidence`
- `first_seen_at`
- `last_seen_at`
- `content_hash`
- `title_company_hash`
- `url_hash`

## Canonical Source Priority

A conservative priority order is:

1. approved official API
2. approved official ATS endpoint
3. approved official company career page
4. approved Korean job-site source
5. aggregator, mirrored, or reposted source

This priority does not override compliance rules. A source must still be approved before collection.

## Timing

Duplicate lineage should run before final JD normalization and matching. Normalization can lose small details that help detect duplicates, so raw hashes and source metadata should be preserved first.
