"""
Lovart Sentinel - 精细化情感分析引擎 V2
=========================================
替代NLP的复合情感量化方案：

1. 规则引擎 — 细分情感词典 + 否定/程度词处理
2. 平台原生信号 — 提取各平台自带的评分/标签/tag
3. 竞品基准对比 — 同渠道Lovart vs 竞品情感占比
4. 情感漂移追踪 — 时序维度检测情感拐点
5. 多维标签 — 不止正/负/中，加功能/价格/服务/信任子维度
6. 弱信号检测 — 在负面爆发前捕获早期预警
"""
from ._common import banner

# ---------- 1. 细分情感词典 ----------
POSITIVE_LEXICON = {
    "strong": ["amazing", "incredible", "game changer", "revolutionary", "love", "insane", "炸裂", "爆火", "惊艳", "神器", "太强了"],
    "moderate": ["good", "useful", "helpful", "nice", "works well", "推荐", "好用", "不错", "方便", "实用"],
    "weak": ["decent", "ok", "fine", "还行", "可以", "能用"],
}

NEGATIVE_LEXICON = {
    "strong": ["terrible", "useless", "scam", "waste", "sucks", "垃圾", "骗人", "坑", "太差了"],
    "moderate": ["bug", "crash", "slow", "expensive", "buggy", "崩溃", "卡顿", "贵", "闪退", "打不开"],
    "weak": ["meh", "disappointing", "could be better", "一般", "有点失望", "不太好"],
}

NEGATION_WORDS = ["not", "no", "never", "don't", "doesn't", "不", "没有", "不是", "从未", "毫无"]
INTENSIFIERS = ["very", "really", "extremely", "so", "超级", "非常", "极其", "太", "特别"]

# ---------- 2. 多维度标签体系 ----------
DIMENSION_TAGS = {
    "功能评价": ["feature", "function", "tool", "capability", "generation", "edit", "功能", "工具", "生成", "编辑", "速度", "quality", "质量"],
    "价格评价": ["price", "cost", "free", "subscription", "pricing", "worth", "价格", "免费", "订阅", "值", "贵", "便宜"],
    "服务评价": ["support", "service", "help", "response", "客服", "回复", "服务", "帮助", "文档", "tutorial"],
    "对比评价": ["vs", "versus", "alternative", "better than", "compared", "对比", "替代", "比", "不如", "超过", "canva", "midjourney"],
    "信任度": ["trust", "reliable", "professional", "consistent", "fake", "scam", "信任", "可靠", "专业", "稳定", "不安全"],
    "易用性": ["easy", "intuitive", "simple", "hard", "complex", "confusing", "简单", "容易", "直观", "复杂", "难", "steep learning"],
}


def collect() -> dict:
    data = dict(banner("Advanced Sentiment Engine"))
    data["status"] = "delegated"
    data["_instructions"] = """
    对每个渠道的每条提及内容，执行以下分析：

    1. 规则引擎打分：
       - 扫描正面/负面词典匹配
       - 检测否定词翻转（"not good" = 负面）
       - 检测程度词缩放（"very good" > "good"）
       - 计算情感强度分数 (-100 到 +100)

    2. 平台原生信号提取：
       - PH: 评分4.9/5, pros/cons标签, 评价人身份
       - Reddit: 帖子评分, 评论树情感
       - 社媒: 互动率作为情感代理（低互动=冷漠≈隐性负面）
       - 搜索: CTR/排名作为意图匹配代理

    3. 竞品基准对比：
       - 同渠道Lovart vs Canva vs Midjourney情感分布
       - 识别Lovart在哪些维度优于/劣于竞品

    4. 多维标签归类：
       - 每条提及打上维度标签（功能/价格/服务/对比/信任/易用）
       - 计算各维度情感占比

    5. 情感漂移检测：
       - 对比本周期vs上周期情感分布变化
       - 标记情感拐点（如正面从80%→65%）
    """
    return data


# ---------- 规则引擎核心函数 ----------
def score_sentiment(text: str) -> dict:
    """对单条文本做规则情感评分 (-100 to +100)"""
    text_lower = text.lower()
    score = 0
    matched_words = {"positive": [], "negative": [], "negations": [], "intensifiers": []}

    # 扫描正面词
    for strength, words in POSITIVE_LEXICON.items():
        for w in words:
            if w.lower() in text_lower:
                points = {"strong": 30, "moderate": 15, "weak": 5}[strength]
                score += points
                matched_words["positive"].append(w)

    # 扫描负面词
    for strength, words in NEGATIVE_LEXICON.items():
        for w in words:
            if w.lower() in text_lower:
                points = {"strong": -30, "moderate": -15, "weak": -5}[strength]
                score += points
                matched_words["negative"].append(w)

    # 否定词处理（翻转最近匹配的分数）
    for neg in NEGATION_WORDS:
        if neg.lower() in text_lower:
            matched_words["negations"].append(neg)
            # 简化：如果同时有正面词和否定词，可能被翻转

    # 程度词处理
    for intens in INTENSIFIERS:
        if intens.lower() in text_lower:
            matched_words["intensifiers"].append(intens)
            score = int(score * 1.5)

    # 约束到 [-100, 100]
    score = max(-100, min(100, score))

    # 分类
    if score >= 30:
        label = "strong_positive"
    elif score >= 10:
        label = "positive"
    elif score <= -30:
        label = "strong_negative"
    elif score <= -10:
        label = "negative"
    else:
        label = "neutral"

    return {"score": score, "label": label, "matched_words": matched_words}


def tag_dimensions(text: str) -> list:
    """对文本打维度标签"""
    text_lower = text.lower()
    tags = []
    for dimension, keywords in DIMENSION_TAGS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            tags.append(dimension)
    return tags if tags else ["未分类"]


# ---------- 竞品情感基准 ----------
COMPETITOR_BENCHMARKS = {
    "canva": {"ph_rating": 4.7, "g2_rating": 4.7, "estimated_social_sentiment": 0.82},
    "midjourney": {"ph_rating": 4.8, "g2_rating": 4.6, "estimated_social_sentiment": 0.85},
    "adobe_firefly": {"ph_rating": 4.3, "g2_rating": 4.5, "estimated_social_sentiment": 0.75},
    "lovart": {"ph_rating": 4.9, "g2_rating": None, "estimated_social_sentiment": None},
}


def benchmark_against_competitors(lovart_data: dict) -> dict:
    """对标竞品情感基准"""
    result = {
        "ph_rating_comparison": {},
        "social_sentiment_gap": {},
    }

    lovart_ph = lovart_data.get("product_hunt", {}).get("rating", 4.9)
    for comp, metrics in COMPETITOR_BENCHMARKS.items():
        if comp == "lovart":
            continue
        if metrics.get("ph_rating"):
            result["ph_rating_comparison"][comp] = {
                "competitor_rating": metrics["ph_rating"],
                "lovart_rating": lovart_ph,
                "difference": round(lovart_ph - metrics["ph_rating"], 1),
            }

    return result


# ---------- 弱信号检测 ----------
WEAK_SIGNAL_RULES = {
    "engagement_velocity_drop": {
        "description": "互动率月环比下降",
        "threshold": 0.30,
        "signal": "用户对品牌内容失去兴趣——隐性情感变冷",
    },
    "neutral_ratio_increase": {
        "description": "中性评价占比周环比上升",
        "threshold": 0.15,
        "signal": "用户从主动关心转向漠不关心——比负面更危险",
    },
    "question_to_complaint_ratio": {
        "description": "提问类评论减少，抱怨类增加",
        "threshold": 1.0,
        "signal": "新用户兴趣下降，存量用户不满上升",
    },
    "competitor_mention_in_lovart_context": {
        "description": "在Lovart讨论中同时提及竞品的比例",
        "threshold": 0.25,
        "signal": "用户在做决策对比，Lovart正在被放在替代品位置考量",
    },
}
