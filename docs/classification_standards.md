# Classification Standards

The project uses shared classification standards so Korean AI hiring-market records can move through the pipeline without ad hoc labels.

The standards live in `configs/classification_standards.yaml`.

## Source Classification

Source categories:

- `official_api`
- `official_ats`
- `official_career_page`
- `approved_job_site`
- `aggregator`
- `community_repost`
- `unknown`

Source grades:

- A: official API available; collection may be allowed only when policy and evidence are valid.
- B: public ATS/API endpoint available; collection may be allowed only when policy and evidence are valid.
- C: public company career page or public job page with acceptable robots and terms; requires careful review.
- D: unclear policy or general scraping needed; not collectable until manual/legal review.
- E: login, CAPTCHA, anti-bot bypass, or prohibited automated collection required; not collectable.
- F: unusable, blocked, or rejected; not collectable.

## Company Classification

Company categories are designed around Korean AI hiring likelihood, not foreign-market targeting and not generic AI company classification.

Examples include:

- `ai_native_company`
- `data_cloud_mlops_company`
- `large_enterprise_ai_org`
- `ai_transformation_company`

## JD Classification

Target role groups are:

- AI Analyst
- AI Engineer
- AI Researcher
- AI Scientist

Anything outside the target taxonomy remains `Other/Unknown` until reviewed.

## Decision Objects

Classifier modules return structured decision objects with:

- `decision`
- `allowed`
- `reasons`
- `blockers`
- `confidence`

No classifier silently approves a source, company, or JD.
