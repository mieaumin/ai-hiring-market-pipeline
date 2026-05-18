# ATS Intelligence Layer

ATS intelligence is a core operational layer, not just a source type field.

An Applicant Tracking System can determine how a job source is structured, how stable its pages are, whether public endpoints exist, and what kind of collector strategy may eventually be appropriate after approval.

## Why ATS Fingerprinting Matters

ATS fingerprinting matters because:

- multiple companies can share the same ATS infrastructure
- one collector strategy may support many companies if the ATS is stable and approved
- ATS patterns affect maintenance cost
- ATS patterns influence deduplication and canonical source priority
- ATS infrastructure can expose JSON, RSS, sitemap, or structured HTML endpoints
- ATS behavior can affect anti-bot risk and request limits

Examples of ATS infrastructure include:

- Greenhouse
- Lever
- Ashby
- Workday
- SmartRecruiters
- SAP SuccessFactors

These are infrastructure patterns only. They do not expand this project into foreign-market collection.

## ATS Metadata Fields

The ATS intelligence layer should preserve:

- `ats_type`
- `ats_confidence`
- `ats_detection_method`
- `collector_strategy`
- `json_endpoint_detected`
- `rss_detected`
- `sitemap_detected`
- `structure_stability`
- `maintenance_risk`
- `anti_bot_risk`

## ATS-Aware Collection vs Generic Scraping

ATS-aware collection is different from generic scraping.

Generic scraping treats every page as an isolated HTML target. ATS-aware collection first asks whether the source belongs to a known, policy-compatible infrastructure pattern. If a public endpoint exists and the source is approved, the future collector can use a more stable and auditable strategy.

This project still blocks collection until source approval exists. ATS detection only helps explain the source and plan future work.

## Operational Use

ATS fingerprints should be recorded in `runtime/ats_fingerprints.csv`.

A source should not be promoted because an ATS was detected. It still needs:

- scope relevance
- policy evidence
- source grade review
- approval status
- collection eligibility
- source relationship metadata
