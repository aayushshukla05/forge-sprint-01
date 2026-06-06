from pathlib import Path
from fpdf import FPDF
from pptx import Presentation

def to_html(report: dict, path: str):
    site = report.get("site", "Unknown Site")
    urls_crawled = report.get("urls_crawled", 0)
    severity_counts = report.get("summary", {}).get("by_severity", {})
    issues = report.get("issues", [])
    recommendations = report.get("recommendations", [])

    severity_html = "".join([f"<li>{sev}: {count}</li>" for sev, count in severity_counts.items()])

    issues_rows = ""
    for issue in issues:
        issues_rows += f"""
        <tr>
            <td>{issue.get('severity', 'N/A')}</td>
            <td>{issue.get('type', 'N/A')}</td>
            <td>{issue.get('count', 0)}</td>
            <td>{issue.get('explanation', 'N/A')}</td>
        </tr>
        """

    recs_html = "".join([f"<li>{rec}</li>" for rec in recommendations])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>SEO Report - {site}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>SEO Audit Report: {site}</h1>
        <p><strong>URLs Crawled:</strong> {urls_crawled}</p>
        <h2>Issue Summary</h2>
        <ul>{severity_html}</ul>
        <h2>Issues</h2>
        <table>
            <thead><tr><th>Severity</th><th>Type</th><th>Count</th><th>Explanation</th></tr></thead>
            <tbody>{issues_rows}</tbody>
        </table>
        <h2>Recommendations</h2>
        <ul>{recs_html}</ul>
    </body>
    </html>
    """
    Path(path).write_text(html_content, encoding="utf-8")

def to_pdf(report: dict, path: str):
    site = report.get("site", "Unknown Site")
    urls_crawled = report.get("urls_crawled", 0)
    summary = report.get("summary", {})
    by_severity = summary.get("by_severity", {})
    issues = report.get("issues", [])
    recommendations = report.get("recommendations", [])
    total_issues = sum(by_severity.values())

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"SEO Audit Report: {site}", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, f"URLs Crawled: {urls_crawled}", ln=True)
    pdf.cell(0, 10, f"Total Issues: {total_issues}", ln=True)
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Issues", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for issue in issues:
        text = f"[{issue.get('severity', 'N/A')}] {issue.get('type', 'N/A')} - {issue.get('count', 0)} URLs"
        pdf.cell(0, 10, text, ln=True)

    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Recommendations", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for rec in recommendations:
        pdf.multi_cell(0, 10, f"- {rec}")
        pdf.ln(2)

    pdf.output(path)

def to_pptx(report: dict, path: str):
    site = report.get("site", "Unknown Site")
    by_severity = report.get("summary", {}).get("by_severity", {})
    issues = report.get("issues", [])
    recommendations = report.get("recommendations", [])

    prs = Presentation()

    # Slide 1: Title
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "SEO Audit Report"
    slide.placeholders[1].text = f"Site: {site}"

    # Slide 2: Summary
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Summary"
    tf = slide.placeholders[1].text_frame
    for sev, count in by_severity.items():
        p = tf.add_paragraph()
        p.text = f"{sev}: {count}"

    # Slide 3: Top Issues
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Top Issues"
    tf = slide.placeholders[1].text_frame
    for issue in issues[:8]:
        p = tf.add_paragraph()
        p.text = f"[{issue.get('severity', 'N/A')}] {issue.get('type', 'N/A')} ({issue.get('count', 0)})"

    # Slide 4: Recommendations
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Recommendations"
    tf = slide.placeholders[1].text_frame
    for rec in recommendations:
        p = tf.add_paragraph()
        p.text = rec

    prs.save(path)
