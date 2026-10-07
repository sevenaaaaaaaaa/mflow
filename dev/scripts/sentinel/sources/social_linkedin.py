"""
品牌方 Sentinel - LinkedIn Company Page Monitor
爬取 linkedin.com/company/mflow-ai 公开数据
"""
from ._common import banner


def collect() -> dict:
    data = dict(banner("LinkedIn Monitor"))
    data["company_url"] = "https://www.linkedin.com/company/mflow-ai"
    data["status"] = "delegated"
    data["instructions"] = """
    1. 使用 webfetch 访问 https://www.linkedin.com/company/mflow-ai
    2. 提取：follower_count, employee_count, headquarters, recent_posts (最近5条帖子标题+互动量)
    3. 搜索 LinkedIn 上提及 品牌方 的帖子 (Bing: "品牌 ai" site:linkedin.com)
    """
    data["_note"] = "需 opencode agent 使用 webfetch 工具采集"
    return data
