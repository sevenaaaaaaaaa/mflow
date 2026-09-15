"""
Lovart Sentinel - AI Directories & Review Sites Monitor
监测 AI工具目录和评测网站上的 Lovart 收录状态
"""
from ._common import banner

DIRECTORIES = {
    "futurepedia": "https://www.futurepedia.io/ai-tools/lovart",
    "theresanaiforthat": "https://theresanaiforthat.com/s/lovart/",
    "alternativeto": "https://duckduckgo.com/html/?q=lovart+site:alternativeto.net",
    "slant": "https://duckduckgo.com/html/?q=lovart+site:slant.co",
    "aitoolhunt": "https://www.aitoolhunt.com/search?q=lovart",
}

REVIEW_SITES = {
    "g2": "https://www.g2.com/products/lovart/reviews",
    "capterra": "https://www.capterra.com/p/lovart/",
    "trustpilot": "https://www.trustpilot.com/review/lovart.ai",
    "getapp": "https://www.getapp.com/search/?q=lovart",
    "smzdm": "https://www.baidu.com/s?wd=lovart+%E4%BB%80%E4%B9%88%E5%80%BC%E5%BE%97%E4%B9%B0",
    "woshipm": "https://www.baidu.com/s?wd=lovart+%E4%BA%BA%E4%BA%BA%E9%83%BD%E6%98%AF%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86",
}


def collect() -> dict:
    data = dict(banner("AI Directories & Review Sites"))
    data["status"] = "delegated"
    data["directories"] = DIRECTORIES
    data["review_sites"] = REVIEW_SITES
    data["_instructions"] = """
    1. webfetch 各AI工具目录搜索
    2. 提取：是否收录、评分、排名、用户评价数
    3. 对比竞品在同平台的收录情况
    4. 检测Lovart在AlternativeTo上的替代关系
    5. 中国评测站：什么值得买、人人都是产品经理
    """
    return data
