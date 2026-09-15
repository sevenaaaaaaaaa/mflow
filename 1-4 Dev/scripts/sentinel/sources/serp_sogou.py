"""
Lovart Sentinel - Sogou SERP Scanner
搜狗搜索（中国第二大搜索引擎），内置微信文章搜索
"""
from ._common import banner

QUERIES = {
    "brand": "https://www.sogou.com/web?query=lovart+ai",
    "wechat": "https://weixin.sogou.com/weixin?query=lovart+ai&type=2&ie=utf8",
}


def collect() -> dict:
    data = dict(banner("Sogou SERP Scan"))
    data["status"] = "delegated"
    data["queries"] = QUERIES
    data["_instructions"] = """
    1. webfetch 搜狗搜索 "lovart ai"
    2. 提取：首条结果域名（关注是否有寄生域名排第一）
    3. 利用搜狗"微信"tab 搜索微信公众号文章
    4. 提取"相关搜索"和"问过的人"数据（如"lovart ai官网怎么进入"—52人问）
    5. 关键信号：搜狗搜索lovart时lovart.me可能排第一
    """
    return data


def parse_sogou_serp(html_content: str) -> dict:
    """从搜狗搜索结果中提取关键信息"""
    import re
    result = {
        "first_result_domain": None,
        "parasites_found": [],
        "wechat_articles": [],
        "related_searches": [],
        "asked_questions": [],
    }

    # 检测首条结果域名
    first_url = re.search(r'https?://([^/]+)', html_content)
    if first_url:
        result["first_result_domain"] = first_url.group(1)

    # 检测寄生域名
    for parasite in ["lovart-ai.com", "lovart.pro", "lovart.io", "lovart.info", "lovart.me"]:
        if parasite in html_content:
            result["parasites_found"].append(parasite)

    # 提取微信公众号文章标题
    wechat_titles = re.findall(r'<!--B--><!--F-->(.*?)<!--E--><!--/B-->', html_content)
    result["wechat_articles"] = wechat_titles[:10]

    # "问过的人"数据
    asked = re.findall(r'lovart[^"]*[？?].*?(\d+)人在问', html_content)
    result["asked_questions"] = asked

    return result
