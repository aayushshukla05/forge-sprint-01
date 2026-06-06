
## Session 1 — 2026-06-06
Model: gemma4:31b-cloud via ollama launch claude

### Step 1: detector.py
- Prompted model to write 20 SEO rules using pandas
- Model used Edit tool successfully
- All 20 rules implemented: missing_title through slow_page

### Step 2: run.py  
- Prompted model to write 5-stage pipeline
- Accepts export_dir as sys.argv[1]
- Saves outputs/report.json
