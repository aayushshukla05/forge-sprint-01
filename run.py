import sys, os, json, time
from pathlib import Path
from seo.detector import load_csv, detect, summarize
from seo.fixer import rewrite_title, rewrite_meta, get_call_count
from seo.reporter import to_html, to_pdf, to_pptx

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

def group_issues(flat_issues):
    grouped = {}
    for i in flat_issues:
        t = i["issue_type"]
        if t not in grouped:
            grouped[t] = {"type": t, "severity": i["severity"], "affected_urls": [], "count": 0, "explanation": ""}
        grouped[t]["affected_urls"].append(i["url"])
        grouped[t]["count"] += 1
    for t, g in grouped.items():
        g["explanation"] = f"{g['count']} URLs affected by {t}."
    return list(grouped.values())

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <export_dir>")
        sys.exit(1)

    export_dir = sys.argv[1]
    csv_path = os.path.join(export_dir, "internal_all.csv")
    start = time.time()

    print("Stage 1: Loading CSV...")
    try:
        df = load_csv(csv_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)

    site = export_dir.rstrip("/\\").split(os.sep)[-1]
    urls_crawled = len(df)
    print(f"  Loaded {urls_crawled} URLs")

    print("Stage 2: Detecting issues...")
    flat_issues = detect(df)
    summary = summarize(flat_issues)
    grouped = group_issues(flat_issues)
    print(f"  Found {summary['total_issues']} issues")

    print("Stage 3: Prioritizing...")
    severity_order = {"High": 0, "Medium": 1, "Low": 2}
    grouped.sort(key=lambda x: severity_order.get(x["severity"], 3))

    print("Stage 4: Generating fixes (capped at 20 URLs)...")
    OUTPUTS_DIR.mkdir(exist_ok=True)

    titles_fixes = []
    seen = 0
    for issue in flat_issues:
        if seen >= 20:
            break
        if issue["issue_type"] in ("missing_title", "title_too_long", "title_too_short"):
            url = issue["url"]
            row = df[df["Address"] == url]
            if not row.empty:
                content_type = str(row.iloc[0].get("Content Type", "")).lower()
                if "text/html" not in content_type:
                    continue
                old_title = str(row.iloc[0].get("Title 1", "")) if "Title 1" in row.columns else ""
                new_title = rewrite_title(url, old_title)
                if new_title:
                    titles_fixes.append({"url": url, "old": old_title, "new": new_title})
                    seen += 1

    redirect_map = []
    for issue in flat_issues:
        if issue["issue_type"] == "broken_link":
            redirect_map.append({"from": issue["url"], "to": "", "reason": "404 - needs redirect target"})

    print("Stage 5: Writing report...")
    duration = round(time.time() - start, 1)
    report = {
        "site": site,
        "urls_crawled": urls_crawled,
        "summary": summary,
        "issues": grouped,
        "fixes": {"titles": titles_fixes, "redirect_map": redirect_map},
        "recommendations": [f"Fix {g['count']} {g['type']} issues ({g['severity']} severity)." for g in grouped[:5]],
        "run_meta": {"model": "gemma4:31b-cloud", "model_calls": get_call_count(), "duration_sec": duration}
    }

    report_path = OUTPUTS_DIR / "report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"  Saved {report_path}")

    to_html(report, str(OUTPUTS_DIR / "report.html"))
    to_pdf(report, str(OUTPUTS_DIR / "report.pdf"))
    to_pptx(report, str(OUTPUTS_DIR / "report.pptx"))
    print("Done.")

if __name__ == "__main__":
    main()
