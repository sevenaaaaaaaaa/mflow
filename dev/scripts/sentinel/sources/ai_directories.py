"""
品牌方 Sentinel - AI Directories & Review Sites Monitor
监测 AI工具目录和评测网站上的 品牌方 收录状态
"""
from ._common import banner

DIRECTORIES = {
    "futurepedia": "https://www.futurepedia.io/ai-tools/品牌",
    "theresanaiforthat": "https://theresanaiforthat.com/s/品牌/",
    "alternativeto": "https://duckduckgo.com/html/?q=品牌+site:alternativeto.net",
    "slant": "https://duckduckgo.com/html/?q=品牌+site:slant.co",
    "aitoolhunt": "https://www.aitoolhunt.com/search?q=品牌",
}

REVIEW_SITES = {
    "g2": "https://www.g2.com/products/品牌/reviews",
    "capterra": "https://www.capterra.com/p/品牌/",
    "trustpilot": "https://www.trustpilot.com/review/example.com",
    "getapp": "https://www.getapp.com/search/?q=品牌",
    "smzdm": "https://www.baidu.com/s?wd=品牌+%E4%BB%80%E4%B9%88%E5%80%BC%E5%BE%97%E4%B9%B0",
    "woshipm": "https://www.baidu.com/s?wd=品牌+%E4%BA%BA%E4%BA%BA%E9%83%BD%E6%98%AF%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86",
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
    4. 检测品牌方在AlternativeTo上的替代关系
    5. 中国评测站：什么值得买、人人都是产品经理
    """
    return data
