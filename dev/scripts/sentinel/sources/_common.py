"""
品牌方 Sentinel - Banner/Header 共用
"""
from datetime import date

def banner(title: str) -> dict:
    return {
        "generated_at": date.today().isoformat(),
        "generator": "品牌方 Sentinel",
        "title": title,
    }
