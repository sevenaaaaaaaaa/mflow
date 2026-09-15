"""
Lovart Sentinel - Product Hunt Monitor
爬取 producthunt.com/products/lovart 数据
"""
from ._common import banner


def collect() -> dict:
    data = dict(banner("Product Hunt Monitor"))
    data["ph_url"] = "https://www.producthunt.com/products/lovart"
    data["reviews_url"] = "https://www.producthunt.com/products/lovart/reviews"
    data["status"] = "delegated"
    data["instructions"] = """
    1. 使用 webfetch 访问 Product Hunt Lovart 页面
    2. 提取：rating, review_count, follower_count, upvotes, launch_date
    3. 获取最新评价（内容、评分、日期）
    4. 对比上次：新增评价数、评分变化
    5. 告警阈值：60天无新评价
    """
    data["_note"] = "需 opencode agent 使用 webfetch 工具采集"
    return data
