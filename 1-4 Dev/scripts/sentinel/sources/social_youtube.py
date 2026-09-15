"""
Lovart Sentinel - YouTube Monitor via DuckDuckGo/Bing
搜索 YouTube 上关于 Lovart 的视频内容
"""
from ._common import banner

QUERIES = {
    "channel": "lovart_ai site:youtube.com",
    "tutorial": "lovart ai tutorial site:youtube.com",
    "review": "lovart ai review 2025 2026 site:youtube.com",
    "competitor": "lovart vs canva vs midjourney site:youtube.com",
}


def collect() -> dict:
    data = dict(banner("YouTube Monitor (DDG proxy)"))
    data["method"] = "duckduckgo"
    data["url"] = "https://duckduckgo.com/html/?q=lovart_ai+site:youtube.com"
    data["status"] = "delegated"
    data["queries"] = QUERIES
    data["_instructions"] = """
    1. webfetch DDG: https://duckduckgo.com/html/?q=lovart_ai+site:youtube.com
    2. 提取：频道名称、视频标题、发布日期、播放量估算
    3. 检测是否有第三方创作者评测（非官方内容）
    4. 记录高播放量视频的标题和主题
    """
    return data


def parse_youtube_ddg(markdown: str) -> dict:
    import re
    result = {
        "channel_info": {},
        "videos_found": [],
        "third_party_content": False,
    }

    videos = re.findall(r'(?:youtube\.com/watch[^\s]*)[^#]*#?\s*[–-]?\s*(.*?)(?=\n\n|\Z)', markdown, re.DOTALL)
    for v in videos[:10]:
        result["videos_found"].append(v.strip()[:200])

    if any("review" in v.lower() or "tutorial" in v.lower() for v in result["videos_found"]):
        result["third_party_content"] = True

    return result
