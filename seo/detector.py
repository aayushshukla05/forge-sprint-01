import pandas as pd
import numpy as np
from collections import defaultdict

# Severity Mapping from CLAUDE.md
SEVERITY = {
    "high": [
        "missing_title", "duplicate_title", "broken_link",
        "server_error", "redirect_chain", "redirect_loop"
    ],
    "medium": [
        "title_too_long", "missing_meta_description", "duplicate_meta_description",
        "missing_h1", "redirect", "missing_image_alt",
        "orphan_page", "non_indexable_but_linked", "canonical_mismatch"
    ],
    "low": [
        "title_too_short", "meta_description_too_long", "duplicate_h1",
        "thin_content", "slow_page"
    ]
}

def get_severity(issue_type):
    for sev, issues in SEVERITY.items():
        if issue_type in issues:
            return sev
    return "low"

def load_csv(path: str) -> pd.DataFrame:
    """Loads Screaming Frog internal_all.csv into a pandas DataFrame."""
    return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)

def detect(df: pd.DataFrame) -> list:
    """
    Detects SEO issues based on the provided DataFrame.
    Returns a list of dicts with keys: url, issue_type, severity, detail.
    """
    issues = []

    # Standard Screaming Frog internal_all export column names
    col_url = 'Address'
    col_title = 'Title 1'
    col_meta = 'Meta Description 1'
    col_status = 'Status Code'
    col_h1 = 'H1-1'
    col_index = 'Indexability'
    col_canonical = 'Canonical'
    col_words = 'Word Count'
    col_time = 'Response Time'
    col_inlinks = 'Inlinks'
    col_alt = 'Img Alt Text'
    col_chain = 'Redirect Chain'
    col_loop = 'Redirect Loop'

    # Pre-calculate duplicates for efficient lookup
    titles = df[col_title].fillna('') if col_title in df.columns else pd.Series([], dtype=str)
    metas = df[col_meta].fillna('') if col_meta in df.columns else pd.Series([], dtype=str)
    h1s = df[col_h1].fillna('') if col_h1 in df.columns else pd.Series([], dtype=str)

    dup_titles = set(titles[titles.duplicated()].unique())
    dup_metas = set(metas[metas.duplicated()].unique())
    dup_h1s = set(h1s[h1s.duplicated()].unique())

    for _, row in df.iterrows():
        url = row.get(col_url, "Unknown")
        title = str(row.get(col_title, "")) if pd.notnull(row.get(col_title)) else ""
        meta = str(row.get(col_meta, "")) if pd.notnull(row.get(col_meta)) else ""
        status = row.get(col_status)
        h1 = str(row.get(col_h1, "")) if pd.notnull(row.get(col_h1)) else ""
        indexability = row.get(col_index)
        canonical = str(row.get(col_canonical, "")) if pd.notnull(row.get(col_canonical)) else ""
        words = row.get(col_words)
        resp_time = row.get(col_time)
        inlinks = row.get(col_inlinks)

        # Rule definitions
        checks = [
            ("missing_title", not title, "Page is missing a title tag"),
            ("duplicate_title", title and title in dup_titles, f"Duplicate title: {title}"),
            ("broken_link", isinstance(status, (int, float)) and 400 <= status < 500, f"Broken link with status {status}"),
            ("server_error", isinstance(status, (int, float)) and status >= 500, f"Server error with status {status}"),
            ("redirect_chain", row.get(col_chain) if col_chain in df.columns else False, "Page is part of a redirect chain"),
            ("redirect_loop", row.get(col_loop) if col_loop in df.columns else False, "Page is in a redirect loop"),
            ("title_too_long", len(title) > 60, f"Title length ({len(title)}) exceeds 60 characters"),
            ("missing_meta_description", not meta, "Meta description is missing"),
            ("duplicate_meta_description", meta and meta in dup_metas, "Duplicate meta description detected"),
            ("missing_h1", not h1, "H1 tag is missing"),
            ("redirect", isinstance(status, (int, float)) and status in [301, 302], f"Page is a redirect ({status})"),
            ("missing_image_alt", (col_alt in df.columns and (pd.isnull(row.get(col_alt)) or not str(row.get(col_alt)).strip())), "Image missing alt text"),
            ("orphan_page", isinstance(inlinks, (int, float)) and inlinks == 0, "Page has 0 inlinks (orphan page)"),
            ("non_indexable_but_linked", indexability != "Indexable", f"Page is non-indexable ({indexability}) but present in crawl"),
            ("canonical_mismatch", canonical and canonical != url, f"Canonical mismatch: {canonical}"),
            ("title_too_short", title and len(title) < 30, f"Title length ({len(title)}) is too short (below 30)"),
            ("meta_description_too_long", meta and len(meta) > 155, f"Meta description length ({len(meta)}) exceeds 155 characters"),
            ("duplicate_h1", h1 and h1 in dup_h1s, f"Duplicate H1 detected: {h1}"),
            ("thin_content", isinstance(words, (int, float)) and words < 300, f"Thin content: only {words} words"),
            ("slow_page", isinstance(resp_time, (int, float)) and resp_time > 2000, f"Page response time is slow: {resp_time}ms"),
        ]

        for issue_type, condition, detail in checks:
            if condition:
                issues.append({
                    "url": url,
                    "issue_type": issue_type,
                    "severity": get_severity(issue_type),
                    "detail": detail
                })

    return issues

def summarize(issues: list) -> dict:
    by_sev = defaultdict(int)
    for i in issues:
        by_sev[i["severity"].capitalize()] += 1
    return {
        "total_issues": len(issues),
        "by_severity": {
            "High": by_sev["High"],
            "Medium": by_sev["Medium"],
            "Low": by_sev["Low"]
        }
    }
