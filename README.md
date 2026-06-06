# SEO Command Center

An autonomous SEO auditor built as a Claude Code plugin. Feed it a Screaming Frog CSV export and it detects 20 types of SEO issues, prioritizes them by severity, rewrites bad titles and meta descriptions using AI, and outputs a client-ready HTML report, PDF, PPTX deck, and a live dashboard.

---

## Stack

- Claude Code v2.1.167
- Ollama (gemma4:31b-cloud) — AI title/meta rewriter
- Python 3, pandas, fpdf2, python-pptx, fastapi, uvicorn
- Screaming Frog SEO Spider (for crawl export)

---

## Project Structure

    seo-command-center/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── .claude/
    │   ├── audit.jsonl
    │   ├── hooks/audit.sh
    │   └── settings.json
    ├── agents/
    │   ├── extract.md
    │   ├── analyse.md
    │   └── report.md
    ├── mcp/
    │   └── server.py
    ├── outputs/
    │   ├── report.json
    │   ├── report.html
    │   ├── report.pdf
    │   ├── report.pptx
    │   ├── titles_fixes.csv
    │   └── redirect_map.csv
    ├── sample-export/
    ├── scripts/
    │   └── export_fixes.py
    ├── seo/
    │   ├── detector.py
    │   ├── fixer.py
    │   └── reporter.py
    ├── run.py
    ├── SKILL.md
    ├── CLAUDE.md
    ├── PROMPTS.md
    ├── DECISIONS.md
    └── agent-log.md

---

## Install

    git clone https://github.com/aayushshukla05/forge-sprint-01.git
    cd forge-sprint-01
    pip install pandas fpdf2 python-pptx fastapi uvicorn jsonschema
    ollama signin
    export OLLAMA_CONTEXT_LENGTH=65536
    ollama launch claude --model gemma4:31b-cloud

---

## Run

    python3 run.py sample-export/

The pipeline runs 5 stages:
1. Load CSV from export directory
2. Detect all 20 SEO issue types
3. Prioritize by severity (High / Medium / Low)
4. Generate AI fixes for up to 20 URLs (titles and metas)
5. Write report.json, report.html, report.pdf, report.pptx

---

## Live Dashboard

Start the MCP server in a separate terminal:

    python3 mcp/server.py

Then open: http://localhost:7700

The dashboard shows:
- URLs crawled
- Total issues found
- Issues by severity (High / Medium / Low)
- Full issues table with type, severity, and affected URL count

---

## Outputs

| File | Description |
|------|-------------|
| outputs/report.json | Machine-readable audit report matching the output contract schema |
| outputs/report.html | Client-ready HTML audit report with issue table and recommendations |
| outputs/report.pdf | PDF version of the audit report |
| outputs/report.pptx | PowerPoint presentation deck |
| outputs/titles_fixes.csv | AI-rewritten title tags (url, old, new) |
| outputs/redirect_map.csv | Redirect recommendations for 301/302 pages |

---

## The 20 SEO Rules

| Issue | Rule | Severity |
|-------|------|----------|
| missing_title | Title 1 empty on indexable 200 HTML page | High |
| duplicate_title | Same Title 1 on 2+ indexable URLs | High |
| broken_link | Status Code 400-499 | High |
| server_error | Status Code 500+ | High |
| redirect_chain | Redirect Chain column truthy | High |
| redirect_loop | Redirect Loop column truthy | High |
| title_too_long | Title length > 60 or pixel width > 561 | Medium |
| missing_meta_description | Meta Description 1 empty on indexable 200 page | Medium |
| duplicate_meta_description | Same meta on 2+ indexable URLs | Medium |
| missing_h1 | H1-1 empty on 200 HTML page | Medium |
| redirect | Status Code 300-399 | Medium |
| missing_image_alt | Image content type with empty alt text | Medium |
| orphan_page | Inlinks = 0 on indexable 200 page | Medium |
| non_indexable_but_linked | Non-indexable page with inlinks > 0 | Medium |
| canonical_mismatch | Canonical URL does not match page URL | Medium |
| title_too_short | Title length < 30 | Low |
| meta_description_too_long | Meta description length > 155 | Low |
| duplicate_h1 | H1 duplicated across indexable pages | Low |
| thin_content | Word count < 200 on indexable page | Low |
| slow_page | Response time > 1.0 second | Low |

---

## Validate Output Schema

    python3 -c "import json, jsonschema; jsonschema.validate(json.load(open('outputs/report.json')), json.load(open('report.schema.json'))); print('VALID')"

---

## Generate Fix CSVs

    python3 scripts/export_fixes.py

---

## Plugin Manifest

The plugin is declared in `.claude-plugin/plugin.json`:
- **skill**: SKILL.md - master orchestrator
- **command**: seo-audit
- **agents**: extract, analyse, report
- **mcp_server**: mcp/server.py
- **dashboard**: http://localhost:7700

---

## Process Audit

Every Claude Code tool use is automatically logged to `.claude/audit.jsonl` via hooks configured in `.claude/settings.json`. The log records timestamps, tool names, files edited, and results forming a tamper-evident build history verified against git commits.

---

## Competition

Built for Forge Sprint 01 by NMG Technologies, Gurgaon - 6 June 2026.
