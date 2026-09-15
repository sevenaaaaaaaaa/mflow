"""
Lovart Sentinel - 微博/抖音/快手 中文短视频+社媒采集
通过搜索引擎代理穿透反爬
"""
from ._common import banner

QUERIES = {
    "weibo_bing": "lovart site:weibo.com",
    "weibo_sogou": "https://www.sogou.com/web?query=lovart+site:weibo.com",
    "douyin": "lovart ai site:douyin.com",
    "kuaishou": "lovart ai site:kuaishou.com",
    "weibo_hot": "lovart AI设计 site:weibo.com",
}


def collect() -> dict:
    data = dict(banner("Weibo/Douyin/Kuaishou Monitor"))
    data["status"] = "delegated"
    data["method"] = "Bing + 搜狗 (微博) / Bing (抖音/快手)"
    data["queries"] = QUERIES
    data["_instructions"] = """
    1. 搜狗搜索 lovart site:weibo.com（搜狗对中文站点收录优于Bing）
    2. Bing搜索 lovart site:douyin.com
    3. 提取：提及数量、是否有热门话题、头部内容互动量
    4. 微博特定：是否有#话题标签、热搜相关、是否有KOL转发
    5. 抖音特定：视频标题、创作者、是否有UGC内容
    """
    return data


def parse_weibo_douyin_results(markdown: str, source: str) -> dict:
    """从搜索结果中提取微博/抖音提及数据"""
    import re
    result = {
        "source": source,
        "mentions_found": 0,
        "has_hot_topic": False,
        "has_kol_content": False,
        "items": [],
    }

    # 检测话题标签
    topics = re.findall(r'#([^#]+)#', markdown)
    if topics:
        result["has_hot_topic"] = True
        result["topics_found"] = topics[:10]

    # 检测是否有影响力账号内容
    if any(w in markdown.lower() for w in ["万播放", "万赞", "万评论", "k plays", "k likes", "万次观看"]):
        result["has_kol_content"] = True

    # 统计提及数
    mention_count = len(re.findall(r'(?:lovart|Lovart|LOVART)', markdown))
    result["mentions_found"] = mention_count

    return result
