"""
Lovart Sentinel - GSC Weekly Report
Reads latest SEO weekly report markdown
"""
from pathlib import Path
from ._common import banner

WEEKLY_DIR = Path(__file__).resolve().parents[4] / "1-2 Insight" / "Trident Insights" / "reports"


def collect() -> dict:
    data = dict(banner("GSC Weekly Report"))
    md_files = sorted(WEEKLY_DIR.glob("SEO*.md"))
    data["available_reports"] = [str(f.name) for f in md_files]

    if md_files:
        latest = md_files[-1]
        content = latest.read_text(encoding="utf-8")
        data["latest_report_file"] = str(latest.name)
        # 提取关键数字
        import re
        metrics = {}
        patterns = {
            "organic_users": r"Organic\s*Users[:\s]*([\d,]+)",
            "organic_returning_users": r"Returning\s*Users[:\s]*([\d,]+)",
            "organic_new_user_pct": r"New\s*User%[:\s]*([\d.]+)%",
            "gsc_total_clicks": r"Total\s*Clicks[:\s]*([\d,]+)",
            "gsc_total_impressions": r"Total\s*Impressions[:\s]*([\d,]+)",
            "brand_clicks": r"Brand\s*Keyword\s*Clicks[:\s]*([\d,]+)",
            "nonbrand_ctr": r"Non-Brand\s*CTR[:\s]*([\d.]+)%",
            "bing_clicks": r"Bing\s*Total\s*Clicks[:\s]*([\d,]+)",
        }
        for key, pattern in patterns.items():
            m = re.search(pattern, content)
            if m:
                metrics[key] = m.group(1).replace(",", "")
        data["extracted_metrics"] = metrics
    return data
