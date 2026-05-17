# Source Discovery Routes

Phase 0 uses broad, recall-first discovery routes to build a Korean job-site universe. These routes are for source discovery only. They do not collect JDs and do not approve sources.

## Route A - Search-Engine-Based Discovery

Purpose:
Find Korean job posting websites broadly through manual or documented search queries.

Example query themes:

- Korean job portal
- Korean startup hiring platform
- developer jobs Korea
- public job platform Korea
- internship jobs Korea
- recruiting platform Korea
- career community jobs Korea

Output:
Candidate job-site rows in `runtime/raw_job_site_discovery.csv`.

Acceptance criteria:

- The row captures the query or keyword in `discovery_keyword`.
- The row captures the search route in `discovery_route`.
- The row does not imply approval or collection eligibility.

## Route B - Reverse-Reference Discovery

Purpose:
Discover job sites that are referenced by public pages, articles, community posts, university career pages, startup resources, or hiring guides.

Process:

- Record the referenced job-site URL.
- Record the page or note that led to the discovery in `discovery_source`.
- Classify the broad `site_type` without judging compliance.

Output:
Candidate rows that explain how the source was found.

Acceptance criteria:

- Discovery evidence is traceable.
- The site is still treated as unreviewed.
- No JD pages are collected.

## Route C - JD-Source Reverse Discovery

Purpose:
Identify recurring job-posting sources from already-known public references to job postings, without collecting JD content.

Process:

- Use manually observed job links or known public references only as source hints.
- Extract only the source identity, site URL, and route notes.
- Do not fetch or parse JD content during this route.

Output:
Candidate source rows for later policy evidence review.

Acceptance criteria:

- The route records source identity, not JD content.
- The discovered source still requires robots.txt and Terms review.
- No source moves directly to staging or master from this route.

## Discovery Policy

At this stage, the pipeline maximizes source recall.

We are not:

- filtering AI-only sites
- collecting JDs
- performing large-scale crawling
- restricting to developer-only sites
- discovering company career pages as the main task

We are:

- building the Korean job-site source universe
- collecting source evidence
- preparing future source screening
- keeping source approval separate from discovery
