import sys
import os
import json
import pandas as pd
from seo.detector import load_csv, detect

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <export_dir>")
        sys.exit(1)

    export_dir = sys.argv[1]

    # Stage 1: Load CSV
    # Assuming the CSV is located in the export_dir as internal_all.csv
    csv_path = os.path.join(export_dir, 'internal_all.csv')
    print(f"Stage 1: Loading CSV from {csv_path}...")
    try:
        df = load_csv(csv_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)

    # Stage 2: Detect Issues
    print("Stage 2: Detecting issues...")
    issues = detect(df)

    # Stage 3: Sort and Recommendations
    print("Stage 3: Prioritizing issues and generating recommendations...")
    # Sort by severity: High > Medium > Low
    severity_map = {"high": 0, "medium": 1, "low": 2}
    sorted_issues = sorted(issues, key=lambda x: severity_map.get(x['severity'].lower(), 3))

    # Generate top 5 recommendations based on the most frequent High/Medium issues
    # For simplicity, we'll take a sample of high-severity issue types
    high_issues = [i for i in sorted_issues if i['severity'].lower() == 'high']
    rec_candidates = {}
    for i in high_issues:
        rec_candidates[i['issue_type']] = rec_candidates.get(i['issue_type'], 0) + 1

    top_issue_types = sorted(rec_candidates, key=rec_candidates.get, reverse=True)[:5]
    recommendations = [f"Prioritize fixing {ity} issues" for ity in top_issue_types]
    if not recommendations:
        recommendations = ["No high-priority issues found. Perform a general SEO health check."]

    # Stage 4: Save outputs/report.json
    print("Stage 4: Saving report...")
    output_dir = os.path.join(export_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'report.json')

    # Simple summary
    summary = {
        "total_issues": len(issues),
        "high": len([i for i in issues if i['severity'].lower() == 'high']),
        "medium": len([i for i in issues if i['severity'].lower() == 'medium']),
        "low": len([i for i in issues if i['severity'].lower() == 'low']),
    }

    report = {
        "site": export_dir, # Approximation
        "urls_crawled": len(df),
        "summary": summary,
        "issues": sorted_issues,
        "fixes": [], # To be filled by fixer agent later
        "recommendations": recommendations,
        "run_meta": {
            "tool": "SEO Command Center",
            "version": "1.0"
        }
    }

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)

    # Stage 5: Print summary to terminal
    print("\n--- SEO Audit Summary ---")
    print(f"URLs Crawled: {report['urls_crawled']}")
    print(f"Total Issues Found: {summary['total_issues']}")
    print(f"  - High: {summary['high']}")
    print(f"  - Medium: {summary['medium']}")
    print(f"  - Low: {summary['low']}")
    print("\nTop Recommendations:")
    for rec in recommendations:
        print(f"- {rec}")
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()
