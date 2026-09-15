"""
Lovart Sentinel - Reddit Community Monitor
跨14个相关子版块搜索 Lovart 讨论
"""
from ._common import banner

SUBREDDITS = [
    "r/ai_design", "r/graphic_design", "r/logodesign", "r/web_design",
    "r/UI_Design", "r/smallbusiness", "r/ecommerce", "r/socialmedia",
    "r/marketing", "r/startups", "r/SaaS", "r/ArtificialIntelligence",
    "r/StableDiffusion", "r/midjourney",
]

QUERIES = {
    "lovart_mentions": "lovart ai site:reddit.com",
    "competitor_discussions": "canva vs midjourney ai design tool site:reddit.com",
    "ai_design_tools": "best ai design tools 2025 2026 site:reddit.com",
}


def collect() -> dict:
    data = dict(banner("Reddit Community Monitor"))
    data["method"] = "duckduckgo / bing"
    data["subreddits"] = SUBREDDITS
    data["status"] = "delegated"
    data["queries"] = QUERIES
    data["_instructions"] = """
    1. webfetch DDG: https://duckduckgo.com/html/?q=lovart+ai+site:reddit.com
    2. 提取：帖子标题、子版块、发布时间、评论数
    3. 判断情感倾向 (正面/负面/中性)
    4. 检测是否有"lovart vs"或推荐类帖子（决策影响）
    5. 特别关注 r/smallbusiness, r/ecommerce（核心用户群）
    """
    return data


def parse_reddit_ddg(markdown: str) -> dict:
    import re
    result = {
        "posts_found": 0,
        "subreddits_active": [],
        "sentiment": "neutral",
        "key_posts": [],
    }

    posts = re.findall(r'reddit\.com/r/(\w+)[^\n]*\n[^\n]*', markdown)
    result["posts_found"] = len(posts)
    result["subreddits_active"] = list(set(posts))[:10]

    for p in posts: result["key_posts"].append(p[:200])
    if "great" in markdown.lower() or "love" in markdown.lower():
        result["sentiment"] = "positive"
    elif "sucks" in markdown.lower() or "terrible" in markdown.lower():
        result["sentiment"] = "negative"

    return result
