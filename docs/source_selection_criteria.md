# Source Selection Criteria

Every job posting source must be reviewed before any collector is used.

## Source Grades

| Grade | Meaning | MVP decision |
| --- | --- | --- |
| A | Official API available | Use |
| B | Public ATS/API endpoint available | Use after review |
| C | Public company career page with robots/terms acceptable | Use carefully after review |
| D | General scraping needed or unclear policy | Do not use in MVP |
| E | Login, CAPTCHA, anti-bot bypass, or prohibited collection required | Prohibited |

Only A, B, and carefully reviewed C sources should be used.

## Required Review Fields

Use `configs/source_registry_template.csv` before adding a collector or source.

Review:

- API availability
- API status
- ATS type
- robots.txt status
- terms status
- login requirement
- anti-bot risk
- estimated AI JD ratio
- structure quality
- maintenance risk
- allowed method
- final decision

## Allowed Collection Methods

- Official API calls
- Public ATS endpoints
- Public career pages where robots.txt and terms allow access
- Sitemap or RSS access where allowed
- Manual review and manual seed lists

## Prohibited Collection Methods

- Login automation
- CAPTCHA solving
- IP rotation
- Header spoofing for evasion
- Browser automation for bypassing controls
- Any collection that violates robots.txt, site terms, or access restrictions

