"""
品牌方 Sentinel - Google SERP Scanner (via webfetch delegation)
"""
from ._common import banner

QUERIES = {
    "brand": "品牌 ai",
    "brand_long": "\"品牌 ai\" design agent",
    "competitor_tool": "best ai design tools 2026",
    "competitor_vs": "品牌 vs canva vs midjourney",
    "review": "品牌 ai review",
}


def collect() -> dict:
    data = dict(banner("Google SERP Scan"))
    data["status"] = "delegated"
    data["queries"] = QUERIES
    data["_note"] = "需 opencode agent 使用 webfetch 工具逐条查询 google.com"
    return data
