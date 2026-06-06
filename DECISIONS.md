# Decision Log

## 12:30 - Fresh start
- Deleted old project, starting clean
- Architecture: 3 agents (extract, analyse, report) + 1 SKILL.md orchestrator
- Detection in Python, model only for rewrites

## 2026-06-06
- Switched from nemotron to gemma4:31b-cloud — nemotron was breaking file edit tools
- Used ollama launch claude instead of manual env vars — fixes context window issues
- Write tool fails on Ollama 0.30.5, Edit tool works — prompt model to use Edit only
- Committed after each file to maintain incremental git history

## 2026-06-06 — fixer.py
Used gemma4:31b-cloud as model name in fixer.py API calls. Edit tool worked without issues.

## 2026-06-06 — mcp/server.py
Fixed key mismatch: site_name→site, severity_counts→summary.by_severity, top_issues→issues, issue→issue_type. All paths use pathlib relative to project root.

## 2026-06-06 — detector.py fixes
Brief specifies slow_page > 1.0s, thin_content < 200 words, and all title/meta rules scoped to indexable 200 pages only. Duplicate detection must also be scoped to indexable pages to match grader ground truth.

## 2026-06-06 — run.py rewrite
Used cat instead of Claude Code model to rewrite run.py — faster and more reliable for full file rewrites. Grouped issues by type into affected_urls[] to match grader schema.

## 2026-06-06 — run.py rewrite
Used cat instead of Claude Code model to rewrite run.py — faster and more reliable for full file rewrites. Grouped issues by type into affected_urls[] to match grader schema.

## 2026-06-06 — reporter.py rewrite
Old reporter.py had wrong field names from session 1. Rewriting to match run.py which calls to_html(report, path). Correct keys: report["site"], report["summary"]["by_severity"], report["issues"][].type/severity/count/explanation.

## 2026-06-06 — detector.py pixel width fix
Official brief requires Title 1 Pixel Width > 561 OR Length > 60 for title_too_long. Fixed to match grader ground truth.

## 2026-06-06 14:57 — run.py
Capped fixer at 20 URLs. Original code looped all flat_issues causing 100+ Ollama calls. Decision: detect everything, fix representative sample only. Saves quota and improves efficiency score.

## 2026-06-06 14:57 — seo/detector.py
Severity keys were lowercase (high/medium/low). Fixed to High/Medium/Low using sed to match grader schema exactly.

## 2026-06-06 15:01 — scripts/export_fixes.py
Created export script to generate titles_fixes.csv and redirect_map.csv from report.json fixes block. Champion tier requirement.

## 2026-06-06 15:18 — mcp/server.py
Dashboard table showed N/A. Root cause: reading issue.get('url') and issue.get('issue_type') but schema uses issue.get('type') and issue.get('affected_urls'). Fixed field names.

## 2026-06-06 16:10 — run.py
redirect_map was pulling 404 broken images with empty destinations. Changed to pull redirect issue type (301/302 pages) with real from/to pairs. Grader checks redirect targets resolve in export.

## 2026-06-06 16:15 — run.py
titles_fixes was including image and CSS URLs. Added text/html content type filter before rewrite_title call. report.schema.json copied from starter bundle, report.json validated VALID.
