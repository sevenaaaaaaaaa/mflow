"""
Lovart Sentinel - Competitor Social & Keyword Monitor
监测竞品社媒声量和非品牌关键词排名变化
"""
from ._common import banner

COMPETITOR_QUERIES = {
    "canva_social": "canva ai new features site:instagram.com OR site:tiktok.com OR site:youtube.com",
    "midjourney_social": "midjourney v7 update site:reddit.com OR site:youtube.com",
    "ai_design_ranking": "best ai design tools 2026",
    "ai_image_ranking": "best ai image generators 2026",
    "ai_video_ranking": "best ai video generators 2026",
    "logo_design_ranking": "best ai logo makers 2026",
}


def collect() -> dict:
    data = dict(banner("Competitor Social & Keyword Monitor"))
    data["status"] = "delegated"
    data["queries"] = COMPETITOR_QUERIES
    data["_instructions"] = """
    1. webfetch Bing/DDG 搜索竞品社媒动态
    2. 搜索"best ai design tools 2026"类排名文章
    3. 检查Lovart是否出现在排名中、排第几
    4. 对比竞品在排名文章中的出现频率
    5. 发现新上榜竞品
    """
    return data
