"""
Lovart Sentinel - Banner/Header 共用
"""
from datetime import date

def banner(title: str) -> dict:
    return {
        "generated_at": date.today().isoformat(),
        "generator": "Lovart Sentinel",
        "title": title,
    }
