# Key Prompts Log

cat > README.md << 'EOF'
# SEO Command Center

Autonomous SEO auditor powered by Claude Code + Ollama.

## Install
pip install pandas fpdf2 python-pptx

## Run
python3 run.py <export_dir>

## Output
- outputs/report.html
- outputs/report.pdf  
- outputs/report.pptx
- outputs/report.json

## Prompt 1 — detector.py
Asked gemma4:31b-cloud to write all 20 SEO detection rules using pandas.
Result: Worked after switching from Write tool to Edit tool.

## Prompt 2 — run.py
Asked gemma4:31b-cloud to write 5-stage pipeline accepting export_dir as sys.argv[1].
Result: Written successfully.

## Prompt 3 — fixer.py
Asked gemma4:31b-cloud to write rewrite_title, rewrite_meta, get_call_count using Ollama API.
Result: Written successfully using Edit tool.

## Prompt 4 — reporter.py
Asked gemma4:31b-cloud to write to_html, to_pdf, to_pptx functions.
Result: Written successfully. Still gave summary despite instruction.

## Prompt 11 — mcp/server.py
Built FastAPI dashboard on port 7700 with /, /report, /health. Fixed field keys to match report.json schema. Result: success.

## Prompt 12 — detector.py fixes
Fixed: canonical column name, slow_page threshold, indexability filters for title/meta checks, duplicate detection scoped to indexable pages only, thin_content threshold 200, image alt via Content Type. Result: success.

## Prompt 13 — run.py rewrite
Rewrote run.py via cat to fix: grouped issues schema, correct output path, proper summary structure, fixes block, run_meta with model/calls/duration, calls fixer and reporter. Result: success.

## Prompt 13 — run.py rewrite
Rewrote run.py via cat to fix: grouped issues schema, correct output path, proper summary structure, fixes block, run_meta with model/calls/duration, calls fixer and reporter. Result: success.

## Prompt 14 — reporter.py rewrite
Asked model to replace all functions with correct (report: dict, path: str) signatures and correct field names. No report_dict, no site_name, no severity_counts, no top_issues. Result: in progress.

## Prompt 15 — detector.py pixel width
Added pixel width > 561 check to title_too_long rule alongside length > 60. Handles missing column gracefully. Result: success.

## Prompt 16 — mcp/server.py dashboard fix
Fix table_rows loop to use correct field names from report.json: type, affected_urls, count. Result: success, dashboard now shows real URLs and issue types.

## Prompt 17 — scripts/export_fixes.py
Write script to read report.json and export titles_fixes.csv and redirect_map.csv. Result: success.

## Prompt 18 — run.py content type filter
Add text/html check before rewrite_title in Stage 4 loop to exclude images and CSS from titles_fixes. Result: success.

## Prompt 19 — run.py redirect_map fix
Change redirect_map to use redirect issue type instead of broken_link, with real 301/302 from/to pairs. Result: success.
