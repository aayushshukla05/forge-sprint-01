import pandas as pd
from collections import defaultdict

def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)

def detect(df: pd.DataFrame) -> list:
    issues = []
    return issues

def summarize(issues: list) -> dict:
    by_sev = defaultdict(int)
    for i in issues:
        by_sev[i["severity"]] += 1
    return {
        "total_issues": len(issues),
        "by_severity": {
            "High": by_sev["High"],
            "Medium": by_sev["Medium"],
            "Low": by_sev["Low"]
        }
    }
