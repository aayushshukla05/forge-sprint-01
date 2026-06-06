# SEO Command Center - Project Memory

## Goal
Autonomous SEO auditor: read Screaming Frog CSV -> detect issues -> prioritize -> fix -> report

## Pipeline
1. extract agent: load internal_all.csv, detect 18 issue types in Python (no model)
2. analyse agent: score and prioritize issues by severity
3. report agent: rewrite titles/metas with model, output HTML + PDF + PPTX

## Rules
- NEVER feed raw CSV rows to the model
- Detect issues in Python code only (pandas/csv)
- Model only for: rewriting titles, rewriting metas, recommendations
- Title limit: 60 chars / 561px. Meta limit: 155 chars. Validate in code.
- Filter to text/html + Indexable before title/meta checks

## SEO Issue Severities
High: missing_title, duplicate_title, broken_link, server_error, redirect_chain, redirect_loop
Medium: title_too_long, missing_meta_description, duplicate_meta_description, missing_h1, redirect, missing_image_alt, orphan_page, non_indexable_but_linked, canonical_mismatch
Low: title_too_short, meta_description_too_long, duplicate_h1, thin_content, slow_page
