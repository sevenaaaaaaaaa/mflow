"""
Lovart Sentinel - 传播链路追踪
================================
当发现重要内容时，追踪其在各平台的传播路径和涟漪效应。
"""
from ._common import banner


def collect() -> dict:
    data = dict(banner("Propagation Chain Tracker"))
    data["status"] = "delegated"
    data["_instructions"] = """
    当发现重要内容（如媒体报道、KOL视频、热门话题）时执行：

    1. 源内容定位：记录原始发布平台、发布时间、初始互动量
    2. 跨平台搜索：用源内容标题关键字追踪是否有：
       - 知乎引用/讨论
       - B站二次创作/反应视频
       - 微信公众号转载
       - 微博话题引用
       - Reddit/Twitter讨论
    3. 传播层次量化：
       - 转载/引用数量
       - 各平台互动量对比
       - 传播时间线
    4. 涟漪效应评估：源内容是否引发了新的讨论/二次传播链

    示例追踪链：腾讯新闻《月薪19刀》→ 搜狐转载 → 知乎讨论 → B站UP主引用
    """
    return data


def trace_propagation(source_title: str, source_date: str, source_platform: str) -> dict:
    """追踪单条内容的跨平台传播路径"""
    result = {
        "source": {
            "title": source_title,
            "date": source_date,
            "platform": source_platform,
        },
        "propagation_chain": [],
        "ripple_score": 0,
    }

    propagation_queries = {
        "zhihu": f'"{source_title[:30]}" site:zhihu.com',
        "bilibili": f'"{source_title[:30]}" site:bilibili.com',
        "weixin": f'"{source_title[:30]}" site:mp.weixin.qq.com',
        "weibo": f'"{source_title[:30]}" site:weibo.com',
        "reddit": f'"{source_title[:30]}" site:reddit.com',
        "x_twitter": f'"{source_title[:30]}" site:twitter.com OR site:x.com',
    }

    result["propagation_queries"] = propagation_queries
    return result
