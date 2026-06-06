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
