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
