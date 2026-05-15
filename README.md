# AI Hiring Market JD Pipeline

This repository contains a safe, company-first MVP data pipeline for the HEDING x ModuLabs AIFFELTHON Korean AI talent matching project.

The long-term goal is to legally collect, validate, normalize, structure, and prepare AI-related job descriptions (JDs) from approved job posting sources so they can later be matched with AI candidate resumes.

The first goal is not massive crawling. The first goal is to build a clean research MVP architecture for:

- Company discovery
- Source evaluation
- Legal and policy-compliant source selection
- JD normalization and labeling readiness

## Why Company Discovery Comes First

Company Discovery is intentionally placed before JD collection because the project must first define which companies are relevant to the AI hiring market before attempting to identify job posting sources or collect JDs.

This means the project starts by asking:

- Which companies are likely to hire AI talent?
- What evidence supports that decision?
- Which companies should be prioritized for source registry review?

Only after this company candidate pool is reviewed should the project evaluate job posting sources or collect public JDs.

## Pipeline Order

```text
Phase 1 — Company Discovery
↓
Phase 2 — Source Registry
↓
Phase 3 — JD Collection
↓
Phase 4 — JD Normalization and Labeling
↓
Phase 5 — Future JD-Resume Matching
```

Expanded operating flow:

```text
company seed discovery
-> source discovery
-> source verification
-> evidence collection
-> JD staging
-> quality gate
-> master dataset
```

## Legal and Ethical Collection Policy

This project prioritizes legal and policy-compliant data collection.

Allowed and preferred sources:

- Official APIs
- Public APIs
- Public ATS job board endpoints
- Public company career pages where robots.txt and terms allow access
- Sitemap or RSS sources where allowed
- Manual seed lists where necessary

This project does not implement:

- Illegal scraping
- Bot bypass
- CAPTCHA solving
- Login automation
- IP rotation
- Anti-bot evasion
- Autonomous browser agents
- LLM API integration
- Google Sheets API integration

## Source Grading System

Every JD source should be reviewed in the source registry before any collector is added.

| Grade | Meaning | Use policy |
| --- | --- | --- |
| A | Official API available | Preferred |
| B | Public ATS/API endpoint available | Allowed after review |
| C | Public company career page with robots/terms acceptable | Use carefully after review |
| D | General scraping needed or unclear policy | Do not use in MVP |
| E | Login, CAPTCHA, anti-bot bypass, or prohibited collection required | Prohibited |

Only A, B, and carefully reviewed C sources should be used.

## MVP Scope

Phase 1 — Company Discovery:

- Build a candidate company pool related to AI hiring.
- Collect evidence signals showing whether a company is likely hiring AI talent.
- Score companies using structured signal categories.
- Save validated company candidate datasets.

Phase 2 — Source Registry:

- Identify each company's job posting source.
- Evaluate API availability, public access, robots.txt, login requirement, anti-bot risk, and data quality.
- Approve only sources that meet the legal and quality policy.

Phase 3 — JD Collection:

- Collect public AI-related job descriptions only from approved sources.
- Use safe public API or public ATS endpoint skeletons.

Phase 4 — JD Processing:

- Normalize collected JDs into a common schema.
- Filter AI-related roles.
- Save raw, cleaned, and validated datasets.

Phase 5 — Future JD-Resume Matching:

- Connect structured JDs to AI resume data using a shared role and skill taxonomy.

## Folder Structure

```text
ai-hiring-market-pipeline/
  README.md
  .gitignore
  requirements.txt
  pyproject.toml

  data/
    raw/
    cleaned/
    labeled/
    logs/

  docs/
    phase1_company_discovery.md
    source_selection_criteria.md
    legal_and_ethics_policy.md
    jd_schema.md
    taxonomy_v1.md

  configs/
    company_signal_schema.yml
    company_seed.csv
    company_candidates.csv
    company_evidence.csv
    source_registry_template.csv
    ai_keywords.yaml
    taxonomy_v1.yaml

  runtime/
    company_candidates.csv
    company_evidence.csv

  src/
    company_discovery/
    registry/
    collectors/
    processing/
    labeling/
    storage/
    utils/

  notebooks/
  tests/
  scripts/
```

## Setup

```bash
python -m venv .venv
pip install -r requirements.txt
```

Optional environment variables should be placed in a local `.env` file. Do not commit real API keys.

```bash
CONTACT_EMAIL=your-email@example.com
WORKNET_API_KEY=optional-public-api-key
```

## Starter Commands

Initialize company registry templates:

```bash
python scripts/init_company_registry.py
```

Initialize source registry template:

```bash
python scripts/init_source_registry.py
```

Validate existing local CSV outputs:

```bash
python scripts/run_validation.py
```

`scripts/run_collection.py` is intentionally conservative in this MVP scaffold. It does not run broad crawling. It exists as a future entry point for approved sources only.

## Future Roadmap

- Expand manually reviewed company candidates.
- Review and grade source registry entries.
- Add source-specific collectors only for A, B, and carefully reviewed C sources.
- Add stronger JD validation and role taxonomy matching.
- Add dataset quality reports.
- Prepare JD embeddings and matching features for future JD-resume matching.
