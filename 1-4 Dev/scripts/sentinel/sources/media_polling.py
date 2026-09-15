"""
Lovart Sentinel - 媒体库系统化轮询
====================================
定期轮询固定的国际+中文科技/设计媒体站点，检测Lovart报道。
"""
from ._common import banner

# 媒体库：分国际/中文 × 科技/设计
MEDIA_SITES = {
    "international_tech": {
        "sites": "techcrunch.com OR wired.com OR theverge.com OR venturebeat.com OR arstechnica.com",
        "label": "国际科技媒体",
        "query": "lovart ai design agent",
    },
    "international_design": {
        "sites": "creativebloq.com OR designmodo.com OR smashingmagazine.com OR itsnicethat.com OR awwwards.com",
        "label": "国际设计媒体",
        "query": "lovart ai design tool",
    },
    "china_tech": {
        "sites": "36kr.com OR geekpark.com OR ifanr.com OR pingwest.com OR sspai.com OR huxiu.com",
        "label": "中文科技媒体",
        "query": "lovart AI设计",
    },
    "china_design": {
        "sites": "shejipi.com OR logonews.cn OR uisdc.com OR uiiiuiii.com OR zcool.com.cn",
        "label": "中文设计媒体",
        "query": "lovart AI设计工具",
    },
    "china_ai": {
        "sites": "jiqizhixin.com OR liangziben.com OR qbitai.com OR aitechreview.com",
        "label": "中文AI媒体",
        "query": "lovart AI设计Agent",
    },
    "china_marketing": {
        "sites": "socialbeta.com OR meihua.info OR adquan.com OR pangjing.cn",
        "label": "中文营销媒体",
        "query": "lovart AI设计",
    },
}


def collect() -> dict:
    data = dict(banner("Media Library Polling"))
    data["status"] = "delegated"
    data["media_groups"] = MEDIA_SITES
    data["search_engine"] = "Bing (国际) / 百度 (中文)"
    data["_instructions"] = """
    对每个media_group执行1条Bing/百度 webfetch：
      Bing:  site:{sites} lovart ai
      百度:  site:{sites} lovart AI设计
    
    对每条结果提取：
    - 文章标题、发布日期、媒体名称、URL
    - 情感倾向（正面/负面/中性）
    - 是否为主动报道（vs 转载/提及）
    - 文章核心角度（产品评测/行业分析/教程/新闻）
    """
    return data


def parse_media_results(markdown: str, group_name: str) -> dict:
    """从媒体搜索结果中提取报道数据"""
    import re
    result = {
        "group": group_name,
        "articles_found": 0,
        "articles": [],
        "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
    }

    article_blocks = re.findall(r'(\d{4}[年/-]\d{1,2}[月/-]\d{1,2})[^\n]*\n([^\n]*(?:lovart|Lovart|LOVART)[^\n]*)', markdown, re.IGNORECASE)
    for date, title in article_blocks[:20]:
        result["articles_found"] += 1
        article = {"date": date, "title": title.strip()[:200]}

        title_lower = title.lower()
        if any(w in title_lower for w in ["爆火", "惊艳", "推荐", "神器", "great", "amazing", "best"]):
            result["sentiment_distribution"]["positive"] += 1
            article["sentiment"] = "positive"
        elif any(w in title_lower for w in ["争议", "问题", "崩溃", "bug", "issue", "problem"]):
            result["sentiment_distribution"]["negative"] += 1
            article["sentiment"] = "negative"
        else:
            result["sentiment_distribution"]["neutral"] += 1
            article["sentiment"] = "neutral"

        result["articles"].append(article)

    return result
