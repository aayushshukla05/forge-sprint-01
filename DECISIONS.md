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
