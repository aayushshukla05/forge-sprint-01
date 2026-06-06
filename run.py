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
    seen_redirects = set()
    for issue in flat_issues:
        if issue["issue_type"] == "redirect" and issue["url"] not in seen_redirects:
            seen_redirects.add(issue["url"])
            redirect_map.append({"from": issue["url"], "to": issue["url"].rstrip("/"), "reason": "301/302 redirect - update internal links to final destination"})

    print("Stage 5: Writing report...")
    duration = round(time.time() - start, 1)
    # Actionable recommendations mapping
    RECS = {
        "missing_title": "{} pages are missing title tags - add unique, descriptive titles under 60 characters",
        "duplicate_title": "{} pages share duplicate titles - each page needs a unique title tag",
        "broken_link": "{} broken links (4xx) found - redirect or remove these URLs to avoid crawl waste",
        "title_too_long": "{} titles exceed 60 chars or 561px - shorten to improve SERP display",
        "title_too_short": "{} titles under 30 chars - expand to be more descriptive",
        "missing_meta_description": "{} pages missing meta descriptions - add unique summaries under 155 chars",
        "duplicate_meta_description": "{} pages share meta descriptions - write unique ones per page",
        "meta_description_too_long": "{} meta descriptions exceed 155 chars - shorten to avoid truncation",
        "missing_h1": "{} pages missing H1 tags - add one clear H1 per page",
        "duplicate_h1": "{} pages share duplicate H1s - make each H1 unique",
        "redirect": "{} redirect chains found - update internal links to point directly to final URLs",
        "redirect_chain": "{} redirect chains - fix to reduce crawl depth",
        "redirect_loop": "{} redirect loops detected - resolve immediately",
        "missing_image_alt": "{} images missing alt text - add descriptive alt attributes for accessibility and SEO",
        "orphan_page": "{} orphan pages with no inlinks - add internal links to make them discoverable",
        "non_indexable_but_linked": "{} non-indexable pages have inlinks - remove links or fix indexability",
        "canonical_mismatch": "{} canonical mismatches - align canonical tags with the intended URL",
        "thin_content": "{} pages under 200 words - expand content or consolidate with stronger pages",
        "slow_page": "{} pages respond slowly - investigate server or asset performance",
        "server_error": "{} server errors (5xx) - fix immediately to prevent crawl and ranking loss",
    }

    report = {
        "site": site,
        "urls_crawled": urls_crawled,
        "summary": summary,
        "issues": grouped,
        "fixes": {"titles": titles_fixes, "redirect_map": redirect_map},
        "recommendations": [RECS.get(g['type'], f"Fix {g['count']} {g['type']} issues").format(g['count']) for g in grouped],
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
