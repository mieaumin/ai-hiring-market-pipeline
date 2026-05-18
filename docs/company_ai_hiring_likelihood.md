# Company AI Hiring Likelihood

The company discovery goal is AI hiring likelihood, not AI company classification.

An "AI company" is a company whose core product may be AI. An "AI hiring-likely company" is any organization likely to hire AI, data, ML, LLM, research, or analytics talent.

These are not the same.

## Examples

AI hiring-likely organizations can include:

- traditional enterprises with AI divisions
- manufacturing companies hiring ML engineers
- finance companies building LLM systems
- retail companies hiring recommendation-system engineers
- healthcare organizations undergoing AI transformation
- robotics or autonomous systems teams
- platform companies with data infrastructure teams
- public or research organizations with AI programs

## Signal Philosophy

The discovery system should preserve evidence for why a company is likely to hire AI talent.

Suggested signals are defined in `configs/company_ai_hiring_signals.yaml`:

- `ai_hiring_likelihood_score`
- `ai_org_signal`
- `ai_infrastructure_signal`
- `ai_job_presence_signal`
- `ai_transformation_signal`
- `evidence_quality`

## Why This Improves Recall

If the project only searches for companies that describe themselves as AI companies, it will miss many real AI hiring signals.

For example, a bank, manufacturer, retailer, hospital network, or game company may not call itself an AI company, but it may hire AI engineers, data scientists, AI researchers, or AI analysts.

The registry should therefore ask:

- Is this company likely to hire AI talent?
- What evidence supports that likelihood?
- Is the evidence recent and traceable?
- Does the evidence justify promotion to source discovery?

## Promotion Principle

No company should move to master only because its name sounds AI-related.

Promotion requires traceable evidence, scoring, review notes, and an explainable reason.
