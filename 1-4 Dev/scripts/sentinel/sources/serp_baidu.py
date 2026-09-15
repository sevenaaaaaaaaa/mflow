"""
Lovart Sentinel - Baidu SERP Scanner
通过 webfetch 扫描百度搜索结果页
提取：搜索结果、相关搜索词、百度百科、贴吧内容
"""
from ._common import banner

QUERIES = {
    "brand": "https://www.baidu.com/s?wd=lovart+ai",
    "china_ecosystem": "https://www.baidu.com/s?wd=lovart+ai+%E5%B0%8F%E7%BA%A2%E4%B9%A6+%E5%BE%AE%E4%BF%A1+%E7%9F%A5%E4%B9%8E",
    "baike": "https://baike.baidu.com/item/Lovart/66266116",
}


def collect() -> dict:
    data = dict(banner("Baidu SERP Scan"))
    data["status"] = "delegated"
    data["queries"] = QUERIES
    data["_instructions"] = """
    1. webfetch 百度搜索 "lovart ai"
    2. 提取：首条结果域名、相关搜索词（如"lovart国内版"）
    3. 检测百度百科词条是否存在/更新
    4. 检测是否有竞品广告投放（百度有付费推广）
    5. 关键信号：相关搜索含"lovart.ai为什么打不开了"=中国用户有访问需求
    """
    return data


def parse_baidu_serp(html_content: str) -> dict:
    """从百度搜索结果中提取关键信息"""
    import re
    result = {"lovart_official_position": None, "related_searches": [], "has_baike": False, "has_ad_competitors": False}

    # 检测官网是否在结果中
    if "lovart.ai" in html_content:
        result["lovart_official_position"] = "found"

    # 提取相关搜索词
    related = re.findall(r'<a[^>]*href="[^"]*wd=([^"&]+)[^"]*"[^>]*>([^<]+)</a>', html_content)
    for url, text in related[:20]:
        text_clean = text.strip()
        if text_clean and len(text_clean) > 1:
            result["related_searches"].append(text_clean)

    # 检测百度百科
    if "baike.baidu.com" in html_content or "百度百科" in html_content:
        result["has_baike"] = True

    # 检测竞品广告
    if "广告" in html_content:
        result["has_ad_competitors"] = True

    return result
