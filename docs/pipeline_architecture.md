# Pipeline Architecture

This repository is a Korean-market, evidence-first AI hiring data pipeline for the HEDING x ModuLabs AIFFELTHON research MVP.

The pipeline is designed to create a legally reviewable and explainable dataset for future JD-resume matching. It is not a production scraping service.

## Final Pipeline

```text
Phase 0 - Korean Job-Site Discovery
-> Phase 0.5 - Job-Site Evidence Review and Source Screening
-> Phase 1 - Korean AI Hiring Company Discovery
-> Phase 2 - Company Source Discovery
-> Phase 3 - Source Verification
-> Phase 4 - JD Collection from Approved Sources Only
-> Phase 5 - JD Normalization, Deduplication, Labeling
-> Phase 6 - Future JD-Resume Matching
```

## Phase 0 - Korean Job-Site Discovery

Purpose:
Discover Korean job posting websites broadly.

This is not JD collection and not company discovery. The output is a raw source universe for later screening.

## Phase 0.5 - Job-Site Evidence Review and Source Screening

Purpose:
Review discovered job sites using legal, technical, and operational evidence.

Screening checks include robots.txt, Terms of Service, API requirements, login requirements, CAPTCHA, anti-bot risk, public HTML access, dynamic rendering risk, and reuse restrictions.

## Phase 1 - Korean AI Hiring Company Discovery

Purpose:
Find Korean or Korea-relevant companies likely to hire AI talent.

Company discovery uses AI hiring likelihood signals, not generic company lists.

## Phase 2 - Company Source Discovery

Purpose:
Map reviewed companies to possible job sources such as official career pages, ATS pages, approved Korean job sites, public APIs, feeds, or sitemap-discoverable pages.

## Phase 3 - Source Verification

Purpose:
Verify whether each company-specific source is usable and approved under the strict source grading policy.

## Phase 4 - JD Collection from Approved Sources Only

Purpose:
Collect public AI-related JDs only from approved sources.

Collection must remain blocked when no approved source exists.

## Phase 5 - JD Normalization, Deduplication, Labeling

Purpose:
Clean, normalize, deduplicate, classify, and label JDs using rule-based taxonomy and quality gates.

## Phase 6 - Future JD-Resume Matching

Purpose:
Prepare structured JD data for future matching against AI candidate resumes.

Future matching may use taxonomy alignment, skill normalization, embeddings, semantic similarity, and ranking research.

## Operating Model

The operating model is:

```text
broad discovery
-> evidence review
-> staging
-> quality gate
-> master
```

Every promotion must be explainable. Raw discovery does not imply approval, and approval does not imply unrestricted collection.
