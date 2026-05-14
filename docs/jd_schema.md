# JD Schema

The MVP stores raw, cleaned, and labeled JD records separately.

## Raw JD Fields

| Field | Description |
| --- | --- |
| `source_url` | Original public URL or API endpoint |
| `source_type` | API, ATS, or public career page |
| `company` | Company name |
| `title` | Job title |
| `location` | Job location if available |
| `description` | Raw job description text |
| `raw_payload` | Optional original payload or serialized source data |
| `collected_at` | Collection timestamp |

## Cleaned JD Fields

| Field | Description |
| --- | --- |
| `source_url` | Original public URL |
| `company` | Normalized company name |
| `title` | Normalized title |
| `location` | Normalized location |
| `description_clean` | Cleaned plain text |
| `description_length` | Character count |
| `collected_at` | Collection timestamp |
| `validation_status` | Validation result |
| `validation_reason` | Human-readable validation reason |

## Labeled JD Fields

| Field | Description |
| --- | --- |
| `source_url` | Original public URL |
| `company` | Normalized company name |
| `title` | Normalized title |
| `role_group` | AI Engineer, AI Researcher, AI Scientist, or AI Analyst |
| `matched_keywords` | Keywords used for rule-based matching |
| `skills` | Extracted or matched skill labels |
| `seniority` | Intern, Junior, Mid, Senior, Lead, or Principal |
| `domain` | Industry domain label |
| `label_confidence` | Rule-based confidence score |
| `labeled_at` | Label timestamp |

## Validation Rules

A JD should be considered valid if:

- `title` exists
- `company` exists
- `source_url` exists
- description length is above a minimum threshold
- `collected_at` exists
- it passes AI keyword filtering or role taxonomy matching

