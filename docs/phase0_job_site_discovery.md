# Phase 0 - Korean Job-Site Discovery

Phase 0 discovers Korean job posting websites, not job postings.

The goal is to build a broad Korean job-site universe before company discovery, company-specific source discovery, JD collection, or resume matching research.

## Why This Phase Exists

Unlike Biz-Voyager, this project first expands the source universe. Biz-Voyager-style pipelines can start from narrower known sources, but Korean AI hiring-market research needs a broader upstream map of job portals, startup hiring platforms, public portals, developer platforms, career communities, recruiting platforms, and foreign platforms with Korean job pages.

## What Phase 0 Does

- discovers possible Korean job posting websites
- records discovery route, query, source URL, and confidence
- uses Korean search keywords and related keywords
- allows manual research and approved search APIs when allowed
- keeps raw discovery separate from approval

## What Phase 0 Does Not Do

- does not collect job postings
- does not collect JD text
- does not crawl job pages
- does not approve sites automatically
- does not bypass robots.txt, login, CAPTCHA, anti-bot systems, or access controls
- does not use browser automation, LLM APIs, or Google Sheets APIs

## Discovery Inputs

Discovery can use:

- Korean job-site keywords
- related keyword expansion
- public directories
- government or public portals
- curated articles or reports
- existing known job-site references
- official/public search APIs if policy allows their use

Discovery must not use:

- scraping Google, Naver, or Bing result pages when not allowed
- bot bypass
- CAPTCHA bypass
- login automation
- aggressive crawling
- IP rotation
- hidden API abuse

## Raw Discovery Output

`runtime/raw_job_site_discovery.csv` captures raw site candidates with:

- `site_id`
- `site_name`
- `site_url`
- `site_domain`
- `site_type`
- `discovery_route`
- `discovery_query`
- `discovery_source_url`
- `country`
- `confidence`
- `review_status`
- `collection_eligibility`
- `notes`
- `discovered_at`

Default values:

- `review_status = not_checked`
- `collection_eligibility = needs_review`

## Discovery Is Not Approval

Inclusion in raw discovery does not mean collection is allowed. Every site must pass Phase 0.5 evidence review and source screening before it can become an approved source.

Discovered sites should be treated as candidates only until robots.txt, Terms of Service, API requirements, login requirements, CAPTCHA risk, anti-bot risk, public HTML access, and reuse restrictions are reviewed.
