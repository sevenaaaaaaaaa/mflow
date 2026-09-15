"""
Lovart Sentinel - Instagram via DuckDuckGo Proxy
通过 DuckDuckGo 搜索引擎穿透 Instagram 反爬
"""
from ._common import banner

QUERIES = {
    "main_account": "lovart.ai site:instagram.com",
    "secondary_account": "lovart_ai site:instagram.com",
    "reels": "lovart ai instagram reels",
}


def collect() -> dict:
    data = dict(banner("Instagram Monitor (DuckDuckGo proxy)"))
    data["method"] = "duckduckgo"
    data["url"] = "https://duckduckgo.com/html/?q=lovart.ai+site:instagram.com"
    data["status"] = "delegated"
    data["_instructions"] = """
    1. webfetch DuckDuckGo: https://duckduckgo.com/html/?q=lovart.ai+site:instagram.com
    2. 提取：粉丝数(59K)、帖子数(208)、最新帖子内容/点赞/评论
    3. 从搜索结果摘要中提取最近帖子：日期、主题、互动量
    4. 对比上次数据：粉丝增长、发帖频率变化
    """
    return data


def parse_instagram_ddg(markdown: str) -> dict:
    """从 DuckDuckGo Instagram 搜索结果中提取数据"""
    import re
    result = {
        "follower_count": None,
        "post_count": None,
        "following_count": None,
        "recent_posts": [],
        "total_reels": None,
    }

    # 提取粉丝数: "59K Followers"
    followers = re.search(r'(\d+[\dK,]+)\s*Followers', markdown)
    if followers:
        val = followers.group(1).replace(",", "")
        if "K" in val:
            result["follower_count"] = int(float(val.replace("K", "")) * 1000)
        else:
            result["follower_count"] = int(val)

    # 提取帖子数: "208 Posts"
    posts = re.search(r'(\d+[\d,]+)\s*Posts', markdown)
    if posts:
        result["post_count"] = int(posts.group(1).replace(",", ""))

    # 提取关注数: "7 Following"
    following = re.search(r'(\d+)\s*Following', markdown)
    if following:
        result["following_count"] = int(following.group(1))

    # 提取帖子摘要数据
    posts_data = re.findall(r'(\w+ \d+, \d+)\s*[–-]\s*(.*?)(?=instagram\.com|Insta)', markdown, re.DOTALL)
    for date, desc in posts_data[:5]:
        result["recent_posts"].append({"date": date.strip(), "description": desc.strip()[:200]})

    # 提取 Reels 数量
    reels = re.search(r'(\d+[\dK,]+)\s*reels', markdown, re.IGNORECASE)
    if reels:
        result["total_reels"] = reels.group(1)

    return result
