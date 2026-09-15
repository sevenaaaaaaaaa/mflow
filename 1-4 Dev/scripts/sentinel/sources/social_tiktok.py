"""
Lovart Sentinel - TikTok via DuckDuckGo Proxy
通过 DuckDuckGo 搜索引擎穿透 TikTok 反爬
"""
from ._common import banner


def collect() -> dict:
    data = dict(banner("TikTok Monitor (DuckDuckGo proxy)"))
    data["method"] = "duckduckgo"
    data["url"] = "https://duckduckgo.com/html/?q=lovart+site:tiktok.com"
    data["status"] = "delegated"
    data["_instructions"] = """
    1. webfetch DuckDuckGo: https://duckduckgo.com/html/?q=lovart+site:tiktok.com
    2. 提取：@lovart.ai粉丝数(749)、@lovart_ai粉丝数(270)
    3. 从搜索结果摘要提取：视频标题、播放量、日期
    4. 检测是否有UGC内容（非官方账号发布的Lovart视频）
    """
    return data


def parse_tiktok_ddg(markdown: str) -> dict:
    """从 DuckDuckGo TikTok 搜索结果中提取数据"""
    import re
    result = {
        "official_accounts": {},
        "ugc_content": [],
        "total_search_results": 0,
    }

    # 提取官方账号数据
    for match in re.finditer(r'@(\w+\.?\w*)\s*\)\s*on\s*TikTok\s*\|\s*(\d+[\d,]*)\s*Followers', markdown):
        handle = match.group(1)
        followers = int(match.group(2).replace(",", ""))
        result["official_accounts"][handle] = {"followers": followers}

    # 提取视频标题和描述
    videos = re.findall(r'TikTok\s*[–-]\s*(.*?)(?=TikTok|tiktok\.com|\n\n)', markdown, re.DOTALL | re.IGNORECASE)
    for v in videos[:5]:
        clean = " ".join(v.split())[:200]
        result["ugc_content"].append({"summary": clean})

    return result
