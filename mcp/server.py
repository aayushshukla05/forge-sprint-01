from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import json
from pathlib import Path

app = FastAPI()

# Use pathlib to define paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "outputs" / "report.json"

@app.get("/", response_class=HTMLResponse)
async def root():
    if not REPORT_PATH.exists():
        return HTMLResponse(
            content="""
            <html>
                <head><title>SEO Command Center</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                    <h1>🚀 SEO Command Center</h1>
                    <p style="color: #666;">No report found. Please run the pipeline first to generate <code>outputs/report.json</code>.</p>
                </body>
            </html>
            """,
            status_code=200
        )

    try:
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return HTMLResponse(content=f"Error reading report: {str(e)}", status_code=500)

    site_name = data.get("site", "Unknown Site")
    urls_crawled = data.get("urls_crawled", 0)
    severity_counts = data.get("summary", {}).get("by_severity", {})
    top_issues = data.get("issues", [])[:20]

    total_issues = sum(severity_counts.values())

    # Build issues table rows
    table_rows = ""
    for issue in top_issues:
        table_rows += f"""
        <tr>
            <td>{issue.get('url', 'N/A')}</td>
            <td>{issue.get('issue_type', 'N/A')}</td>
            <td>{issue.get('severity', 'N/A')}</td>
            <td>{issue.get('detail', 'N/A')}</td>
        </tr>
        """

    html_content = f"""
    <html>
        <head>
            <title>SEO Dashboard - {site_name}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f7f6; }}
                .container {{ max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .stat-card {{ padding: 20px; background: #edf2f7; border-radius: 8px; text-align: center; }}
                .stat-card h3 {{ margin: 0; color: #4a5568; font-size: 0.9rem; text-transform: uppercase; }}
                .stat-card p {{ margin: 10px 0 0; font-size: 1.8rem; font-weight: bold; color: #2d3748; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
                th {{ background-color: #f8fafc; color: #64748b; font-weight: 600; }}
                tr:hover {{ background-color: #f9fafb; }}
                .sev-high {{ color: #e53e3e; font-weight: bold; }}
                .sev-medium {{ color: #dd6b20; font-weight: bold; }}
                .sev-low {{ color: #38a169; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SEO Report: {site_name}</h1>

                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>URLs Crawled</h3>
                        <p>{urls_crawled}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Total Issues</h3>
                        <p>{total_issues}</p>
                    </div>
                    <div class="stat-card">
                        <h3>High Severity</h3>
                        <p class="sev-high">{severity_counts.get('High', 0)}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Medium Severity</h3>
                        <p class="sev-medium">{severity_counts.get('Medium', 0)}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Low Severity</h3>
                        <p class="sev-low">{severity_counts.get('Low', 0)}</p>
                    </div>
                </div>

                <h2>Top 20 Issues</h2>
                <table>
                    <thead>
                        <tr>
                            <th>URL</th>
                            <th>Issue Type</th>
                            <th>Severity</th>
                            <th>Detail</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows if table_rows else "<tr><td colspan='4' style='text-align:center;'>No issues found.</td></tr>"}
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/report")
async def get_report():
    if not REPORT_PATH.exists():
        raise HTTPException(status_code=404, detail="Report not found. Please run the pipeline first.")

    try:
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading report: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7700)
