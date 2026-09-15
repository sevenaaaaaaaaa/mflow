"""
Lovart Sentinel - X/Twitter Social Monitor
通过 fxTwitter API 获取 @lovart_ai 账号数据
"""
from ._common import banner


def collect() -> dict:
    """
    通过 https://api.fxtwitter.com/lovart_ai 获取数据。
    当作为独立脚本运行时返回采集指令。
    """
    data = dict(banner("X/Twitter Monitor"))
    data["handle"] = "@lovart_ai"
    data["status"] = "delegated"
    data["api_url"] = "https://api.fxtwitter.com/lovart_ai"
    data["instructions"] = """
    1. 使用 webfetch 访问 https://api.fxtwitter.com/lovart_ai 获取用户概况
    2. 提取：follower_count, tweets, following, likes, media_count, description, location, joined, verified
    3. 对比上次采集数据，计算变化量
    4. 搜索 @lovart_ai 最近48小时提及（Bing: "@lovart_ai" lang:en）
    """
    data["_note"] = "需 opencode agent 使用 webfetch 工具采集"
    return data
