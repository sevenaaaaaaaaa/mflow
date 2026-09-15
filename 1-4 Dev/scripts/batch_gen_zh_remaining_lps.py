#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch generate 20 remaining Chinese LP JSONs: 15 scenario + 3 pain + 2 competitor."""

import json, os, hashlib

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OG_FALLBACK = "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d3e44c9edfb1a44f386973e9b3c23fcffddc8008.png"

SCENARIO_OUT = os.path.join(VAULT, "1-3 GenFlow/Page Gen/Pages/Campaign/zh")
TOPIC_OUT = os.path.join(VAULT, "1-3 GenFlow/Page Gen/Pages/topic/zh")
os.makedirs(SCENARIO_OUT, exist_ok=True)
os.makedirs(TOPIC_OUT, exist_ok=True)

def q(s):
    return json.dumps(s, ensure_ascii=False)

def hero_split(title, desc, c):
    return q({"type":"hero-split","title":title,"description":desc,"buttons":[{"text":"免费试用","href":"https://lovart.ai/signup","variant":"primary"}],"media":{"src":OG_FALLBACK,"alt":title}})

def hero_gallery(title, desc, c):
    tiles = [{"label":c.get(f"ht_{i}_label",""),"sublabel":c.get(f"ht_{i}_sub",""),"media":{"src":OG_FALLBACK,"alt":""}} for i in range(1,7)]
    return q({"type":"hero-gallery","title":title,"description":desc,"buttons":[{"text":"免费试用","href":"https://lovart.ai/signup","variant":"primary"},{"text":"了解更多","href":"","variant":"secondary"}],"toolTiles":tiles})

def cluster_block_dense(title, c):
    cards = []
    for i in range(1,7):
        t = c.get(f"cl_{i}","")
        if t: cards.append({"title":t,"description":c.get(f"cl_{i}_desc",""),"media":{"src":OG_FALLBACK,"alt":""}})
    return q({"type":"cluster-block-dense","title":title,"cards":cards})

def capability_tabs(c):
    return q({"type":"capability-tabs","title":"核心能力","tabs":[{"label":c.get(f"tab_{i}_label",""),"content":{"title":c.get(f"tab_{i}_title",""),"description":c.get(f"tab_{i}_desc",""),"media":{"src":OG_FALLBACK,"alt":""}}} for i in range(1,5)]})

def bento_4(title, cards, c):
    return q({"type":"bento-4","title":title,"cards":[{"title":card,"description":c.get(f"b4_{i}",""),"media":{"src":OG_FALLBACK,"alt":""}} for i,card in enumerate(cards)]})

def bento_6(title, cards, c):
    return q({"type":"bento-6","title":title,"cards":[{"title":card,"description":c.get(f"b6_{i}",""),"media":{"src":OG_FALLBACK,"alt":""}} for i,card in enumerate(cards)]})

def workflow_horizontal(c):
    return q({"type":"workflow-horizontal","title":"工作流程","steps":[{"title":c.get(f"wh_{i}",""),"description":c.get(f"wh_{i}_desc","")} for i in range(1,4)]})

def comparison_table(c):
    return q({"type":"comparison-table","title":"方案对比","rows":[{"label":c.get(f"comp_{i}_label",""),"before":c.get(f"comp_{i}_before",""),"after":c.get(f"comp_{i}_after","")} for i in range(1,6)],"highlightColumn":3})

def feature_detail(c):
    return q({"type":"feature-detail","title":c.get("fd_title",""),"description":c.get("fd_desc",""),"media":{"src":OG_FALLBACK,"alt":""}})

def review_grid_3col(c):
    return q({"type":"review-grid-3col","title":"用户评价","reviews":[{"rating":5,"text":c.get(f"rev_{i}",""),"author":c.get(f"rev_{i}_author","")} for i in range(1,4)]})

def faq_block(c):
    items = []
    for i in range(1,7):
        qq = c.get(f"faq_{i}","")
        aa = c.get(f"faq_{i}_a","")
        if qq: items.append({"question":qq,"answer":aa})
    return q({"type":"faq","title":"常见问题","items":items})

def cta_default():
    return q({"type":"cta-default","title":"开始使用Lovart","description":"免费试用，无需信用卡","buttons":[{"text":"免费试用","href":"https://lovart.ai/signup","variant":"primary"}]})

def tool_grid(c):
    tools = []
    for i in range(1,7):
        t = c.get(f"tg_{i}","")
        d = c.get(f"tg_{i}_desc","")
        if t: tools.append({"title":t,"description":d,"media":{"src":OG_FALLBACK,"alt":""}})
    return q({"type":"tool-grid","title":"相关工具","tools":tools})

def canvas_wall(c):
    return q({"type":"canvas-wall","title":"作品展示","description":"看看其他用户用Lovart做出的设计","media":{"src":OG_FALLBACK,"alt":""}})

# ============================================================
# SCENARIO LP DATA (15 items) — category: scenario, storylines-A
# ============================================================
SCENARIOS = [
    {"slug":"zh-campaign-double-11","storyline":"scenarios-A","title":"双11大促AI设计 | 全链路大促素材批量生成","desc":"双11大促设计不用愁。Lovart帮你批量生成主图、详情页、直通车图，全链路大促素材。","kw":["双11设计","大促素材","AI批量生成"],"tag":"场景方案"},
    {"slug":"zh-campaign-618","storyline":"scenarios-A","title":"618大促AI设计 | 年中促素材方案","desc":"618年中促设计素材。批量产出主图、促销海报、直播间背景，抓住618流量红利。","kw":["618设计","年中促素材","AI设计"],"tag":"场景方案"},
    {"slug":"zh-campaign-spring-festival","storyline":"scenarios-A","title":"春节营销AI设计 | 中国年特色视觉方案","desc":"春节营销AI设计。对联、红包封面、年夜饭海报、拜年视频封面，中国年味设计一套搞定。","kw":["春节设计","春节营销","AI设计"],"tag":"场景方案"},
    {"slug":"zh-campaign-product-launch","storyline":"scenarios-A","title":"新品上市AI设计 | 种草预热全流程","desc":"新品上市AI设计。从预热海报到种草图文到开箱视频封面，全流程设计素材一站式生成。","kw":["新品上市","种草设计","AI设计"],"tag":"场景方案"},
    {"slug":"zh-campaign-shop-opening","storyline":"scenarios-A","title":"开店装修AI设计 | 电商小程序开店","desc":"电商新店装修设计。店招、Banner、分类图、商品图全套店铺视觉方案。","kw":["开店装修","店铺设计","电商AI"],"tag":"场景方案"},
    {"slug":"zh-campaign-brand-refresh","storyline":"scenarios-A","title":"品牌升级焕新AI设计","desc":"品牌升级视觉焕新。品牌Logo焕新、VI系统升级、全渠道视觉统一更新。","kw":["品牌升级","品牌焕新","VI设计"],"tag":"场景方案"},
    {"slug":"zh-campaign-daily-content-pipeline","storyline":"scenarios-A","title":"日更内容流水线AI | 自媒体日更素材","desc":"自媒体日更不重样。AI帮你搭建内容流水线，封面、配图、视频封面每天自动产出。","kw":["自媒体","日更素材","内容流水线"],"tag":"场景方案"},
    {"slug":"zh-campaign-promotion","storyline":"scenarios-A","title":"活动促销AI设计 | 限时折扣视觉","desc":"促销活动AI设计。限时折扣海报、促销Banner、活动页面，抓住每一波促销机会。","kw":["促销设计","活动视觉","折扣设计"],"tag":"场景方案"},
    {"slug":"zh-campaign-pitch-deck","storyline":"scenarios-A","title":"融资路演AI设计 | 投资人材料","desc":"融资路演AI设计。BP、路演PPT、Teaser、财务图表，让投资人一眼记住你。","kw":["融资路演","PPT设计","投资人材料"],"tag":"场景方案"},
    {"slug":"zh-campaign-recruitment","storyline":"scenarios-A","title":"招聘宣传AI设计 | 海报+H5","desc":"招聘宣传AI设计。招聘海报、H5页面、长图，吸引优秀人才的第一印象。","kw":["招聘海报","招聘宣传","H5设计"],"tag":"场景方案"},
    {"slug":"zh-campaign-exhibition","storyline":"scenarios-A","title":"展会物料AI设计 | 展板折页名片","desc":"展会物料AI设计。展板设计、宣传折页、名片、展位背景墙，一站搞定参展视觉。","kw":["展会物料","展板设计","参展设计"],"tag":"场景方案"},
    {"slug":"zh-campaign-year-end","storyline":"scenarios-A","title":"年终总结AI设计 | 年报回顾","desc":"年终总结AI设计。年报、年终述职PPT、数据可视化图表，全年成果一目了然。","kw":["年终总结","年报设计","述职PPT"],"tag":"场景方案"},
    {"slug":"zh-campaign-mid-autumn","storyline":"scenarios-A","title":"中秋节营销AI设计","desc":"中秋营销AI设计。月饼包装、中秋海报、社群素材，应节视觉设计快速产出。","kw":["中秋节设计","中秋营销","月饼包装"],"tag":"场景方案"},
    {"slug":"zh-campaign-school-season","storyline":"scenarios-A","title":"开学季/毕业季AI设计","desc":"开学季毕业季设计。招生海报、毕业纪念册、开学物料，教育行业视觉全覆盖。","kw":["开学季","毕业季","教育设计"],"tag":"场景方案"},
    {"slug":"zh-campaign-black-friday","storyline":"scenarios-A","title":"跨境电商旺季（黑五/圣诞）AI设计","desc":"黑五圣诞跨境旺季设计。产品促销图、圣诞主题包装、社媒素材，抓住海外购物季。","kw":["黑五设计","圣诞设计","跨境电商"],"tag":"场景方案"},
]

# ============================================================
# PAIN LP DATA (3 items) — category: topic, storyline: landing-gallery-detail
# ============================================================
PAIN_LPS = [
    {"slug":"zh-pain-collaboration-blocked","storyline":"landing-gallery-detail","title":"国内团队AI协作设计工具推荐","desc":"国内团队好用不卡的AI协作设计工具。支持多人实时协作，不用魔法不用翻墙。","kw":["AI协作工具","团队协作","设计协作"],"tag":"痛点解决"},
    {"slug":"zh-pain-ai-quality-poor","storyline":"landing-gallery-detail","title":"AI生成图质量差怎么办","desc":"AI生成的图片质量不好？问题出在Prompt、模型选择和后期处理。Lovart帮你一键提升出图质量。","kw":["AI生成质量","图片优化","Prompt技巧"],"tag":"痛点解决"},
    {"slug":"zh-pain-asset-management","storyline":"landing-gallery-detail","title":"品牌素材管理方案","desc":"品牌素材管理的混乱你经历过吗？用Lovart Brand Kit统一管理团队品牌素材。","kw":["素材管理","品牌管理","设计系统"],"tag":"痛点解决"},
]

# ============================================================
# COMPETITOR LP DATA (2 items) — category: topic, storyline: landing-gallery-detail
# ============================================================
COMPETITOR_LPS = [
    {"slug":"zh-comparison-best-ai-video-tools","storyline":"landing-gallery-detail","title":"AI视频生成工具对比","desc":"7款主流AI视频生成工具横评。看看哪款最适合你的场景，从文案生成到视频产出全流程。","kw":["AI视频","视频生成","工具对比"],"tag":"工具对比"},
    {"slug":"zh-comparison-best-ai-logo-tools","storyline":"landing-gallery-detail","title":"AI Logo生成工具对比","desc":"6款主流AI Logo生成器深度评测。从设计质量到自定义程度，帮你选最合适的Logo工具。","kw":["AI Logo","Logo生成","设计工具"],"tag":"工具对比"},
]

# ============================================================
# SECTION CONTENT
# ============================================================
SCENARIO_SECTIONS = [
    "hero-split", "cluster-block-dense", "capability-tabs", "bento-4",
    "workflow-horizontal", "comparison-table", "cluster-block-dense",
    "feature-detail", "review-grid-3col", "faq", "cta-default"
]

TOPIC_SECTIONS = [
    "hero-gallery", "bento-6", "capability-tabs", "tool-grid",
    "bento-4", "canvas-wall", "workflow-horizontal", "comparison-table",
    "cluster-block-dense", "feature-detail", "faq", "cta-default"
]

def content_for_scenario(slug):
    base_c = {
        "cl_1":"日常运营","cl_1_desc":"日常内容高效产出",
        "cl_2":"大促活动","cl_2_desc":"大促节点快速准备",
        "cl_3":"品牌升级","cl_3_desc":"品牌视觉迭代升级",
        "cl_4":"多平台","cl_4_desc":"跨平台统一管理",
        "cl_5":"团队协作","cl_5_desc":"多人协作效率提升",
        "cl_6":"数据分析","cl_6_desc":"效果数据反馈优化",
        "tab_1_label":"方案一","tab_1_title":"需求分析","tab_1_desc":"深入了解场景需求，匹配最佳能力组合",
        "tab_2_label":"方案二","tab_2_title":"执行流程","tab_2_desc":"从设计到交付的全链路自动化",
        "tab_3_label":"方案三","tab_3_title":"质量保障","tab_3_desc":"AI预检+人工复检双层把关",
        "tab_4_label":"方案四","tab_4_title":"迭代优化","tab_4_desc":"基于反馈持续优化输出质量",
        "b4_0":"效率提升5-10倍","b4_1":"专业级输出质量","b4_2":"相比外包节省70%+成本","b4_3":"品牌规范自动保持",
        "wh_1":"需求梳理","wh_1_desc":"客户需求标准化处理",
        "wh_2":"AI批处理","wh_2_desc":"批量生成交付物",
        "wh_3":"品控交付","wh_3_desc":"统一质检后交付",
        "comp_1_label":"效率","comp_1_before":"传统手动设计","comp_1_after":"AI批量生成",
        "comp_2_label":"质量","comp_2_before":"依赖个人水平","comp_2_after":"AI专业输出",
        "comp_3_label":"一致性","comp_3_before":"难以统一","comp_3_after":"规范自动保持",
        "comp_4_label":"成本","comp_4_before":"高额外包","comp_4_after":"工具订阅",
        "comp_5_label":"迭代","comp_5_before":"慢","comp_5_after":"实时调整",
        "fd_title":"场景化AI设计能力","fd_desc":"针对该场景深度优化的AI设计能力，覆盖从概念到交付的全流程",
        "rev_1":"效率提升超预期，团队产能翻倍","rev_1_author":"用户A",
        "rev_2":"品牌一致性再也不用担心","rev_2_author":"用户B",
        "rev_3":"AI生成+人工微调的最佳组合","rev_3_author":"用户C",
        "faq_1":"这个方案适用于什么场景？","faq_1_a":"覆盖电商促销、品牌营销、内容创作等多种场景",
        "faq_2":"需要多长时间部署？","faq_2_a":"通常1-2天即可上手，当天可看到效果",
        "faq_3":"学习成本高吗？","faq_3_a":"对话式交互，即学即用",
        "faq_4":"能和我现有的工具集成吗？","faq_4_a":"支持API对接，可与现有工作流集成",
        "faq_5":"内容版权安全吗？","faq_5_a":"生成内容版权归用户所有，数据加密存储",
        "faq_6":"有相关的模板吗？","faq_6_a":"覆盖主流场景模板库，持续更新中",
    }
    return base_c

def content_for_topic(slug):
    return {
        "ht_1_label":"海报设计","ht_1_sub":"活动促销",
        "ht_2_label":"Logo生成","ht_2_sub":"品牌标识",
        "ht_3_label":"封面设计","ht_3_sub":"社媒内容",
        "ht_4_label":"主图设计","ht_4_sub":"电商产品",
        "ht_5_label":"视频封面","ht_5_sub":"B站抖音",
        "ht_6_label":"PPT设计","ht_6_sub":"路演汇报",
        "b6_0":"快速出图","b6_1":"批量处理","b6_2":"品牌统一","b6_3":"多平台适配","b6_4":"团队协作","b6_5":"持续优化",
        "tab_1_label":"初学者","tab_1_title":"一键生成","tab_1_desc":"简单描述需求即可生成专业设计",
        "tab_2_label":"进阶","tab_2_title":"精细调整","tab_2_desc":"丰富的自定义选项满足个性需求",
        "tab_3_label":"专业","tab_3_title":"批量生产","tab_3_desc":"一次性生成大量设计素材",
        "tab_4_label":"企业","tab_4_title":"品牌管理","tab_4_desc":"统一的品牌资产管理平台",
        "tg_1":"海报设计","tg_1_desc":"活动促销海报快速出图",
        "tg_2":"Logo生成","tg_2_desc":"AI智能生成品牌Logo",
        "tg_3":"封面设计","tg_3_desc":"多平台封面一键生成",
        "tg_4":"主图设计","tg_4_desc":"电商主图批量制作",
        "tg_5":"视频封面","tg_5_desc":"YouTube/B站封面设计",
        "tg_6":"PPT设计","tg_6_desc":"路演PPT快速生成",
        "b4_0":"效率提升5-10倍","b4_1":"专业输出质量","b4_2":"品牌一致性","b4_3":"成本节省70%+",
        "wh_1":"输入需求","wh_1_desc":"描述你需要的设计内容",
        "wh_2":"AI生成","wh_2_desc":"AI根据需求生成设计方案",
        "wh_3":"精调交付","wh_3_desc":"微调后导出使用",
        "comp_1_label":"操作门槛","comp_1_before":"传统设计软件复杂","comp_1_after":"对话式即学即用",
        "comp_2_label":"输出效率","comp_2_before":"单张制作","comp_2_after":"批量生成",
        "comp_3_label":"品牌一致性","comp_3_before":"难以保持","comp_3_after":"自动统一",
        "comp_4_label":"成本","comp_4_before":"高额外包","comp_4_after":"工具订阅",
        "comp_5_label":"迭代速度","comp_5_before":"按天计","comp_5_after":"按秒计",
        "cl_1":"快速出图","cl_1_desc":"简单描述，秒出设计稿",
        "cl_2":"批量处理","cl_2_desc":"一次生成大量素材",
        "cl_3":"品牌一致","cl_3_desc":"品牌规范自动保持",
        "cl_4":"多平台适配","cl_4_desc":"一键适配各平台尺寸",
        "cl_5":"团队协作","cl_5_desc":"多人实时协作",
        "cl_6":"持续优化","cl_6_desc":"基于反馈不断改进",
        "fd_title":"核心优势","fd_desc":"AI驱动的高效设计工具，让你不再从零开始",
        "rev_1":"操作简单，出图效率高","rev_1_author":"设计师小王",
        "rev_2":"品牌一致性再也不用担心","rev_2_author":"品牌经理Lily",
        "rev_3":"团队协作功能太实用了","rev_3_author":"运营总监张哥",
        "faq_1":"这个工具收费吗？","faq_1_a":"提供免费版和付费版，免费版即可体验核心功能",
        "faq_2":"生成的图片版权归谁？","faq_2_a":"所有生成内容的版权归用户所有",
        "faq_3":"需要下载安装吗？","faq_3_a":"Web端即开即用，无需下载安装",
        "faq_4":"支持什么尺寸？","faq_4_a":"覆盖主流社交媒体和电商平台标准尺寸",
        "faq_5":"输出分辨率怎么样？","faq_5_a":"支持高清输出，满足打印和数字用途",
        "faq_6":"有模板可以用吗？","faq_6_a":"丰富的模板库持续更新中",
    }

SECTION_GEN_SCENARIO = {
    "hero-split": lambda t,d,c: hero_split(t,d,c),
    "cluster-block-dense": lambda t,d,c: cluster_block_dense("应用场景",c),
    "capability-tabs": lambda t,d,c: capability_tabs(c),
    "bento-4": lambda t,d,c: bento_4("核心优势",["效率提升","质量保证","成本节约","品牌统一"],c),
    "workflow-horizontal": lambda t,d,c: workflow_horizontal(c),
    "comparison-table": lambda t,d,c: comparison_table(c),
    "feature-detail": lambda t,d,c: feature_detail(c),
    "review-grid-3col": lambda t,d,c: review_grid_3col(c),
    "faq": lambda t,d,c: faq_block(c),
    "cta-default": lambda t,d,c: cta_default(),
}

SECTION_GEN_TOPIC = {
    "hero-gallery": lambda t,d,c: hero_gallery(t,d,c),
    "bento-6": lambda t,d,c: bento_6("工具矩阵",["快速出图","批量处理","品牌统一","多平台适配","团队协作","持续优化"],c),
    "capability-tabs": lambda t,d,c: capability_tabs(c),
    "tool-grid": lambda t,d,c: tool_grid(c),
    "bento-4": lambda t,d,c: bento_4("为什么选择Lovart",["效率提升5-10倍","专业输出质量","品牌一致性","成本节省70%+"],c),
    "canvas-wall": lambda t,d,c: canvas_wall(c),
    "workflow-horizontal": lambda t,d,c: workflow_horizontal(c),
    "comparison-table": lambda t,d,c: comparison_table(c),
    "cluster-block-dense": lambda t,d,c: cluster_block_dense("功能亮点",c),
    "feature-detail": lambda t,d,c: feature_detail(c),
    "faq": lambda t,d,c: faq_block(c),
    "cta-default": lambda t,d,c: cta_default(),
}

def build_body(sections_def, gen_map, title, desc, content):
    out = []
    for stype in sections_def:
        fn = gen_map.get(stype)
        if fn:
            out.append(fn(title, desc, content))
        else:
            out.append(q({"type":stype,"title":"待补充","description":"内容待填充"}))
    return "[" + ",".join(out) + "]"

def gen_scenario_lp(d, out_dir):
    slug, storyline = d["slug"], d["storyline"]
    title, desc = d["title"], d["desc"]
    kw = d.get("kw", [])
    c = content_for_scenario(slug)
    body = build_body(SCENARIO_SECTIONS, SECTION_GEN_SCENARIO, title, desc, c)
    page = {
        "slug": slug,
        "language": "zh",
        "category": "scenario",
        "schemaVersion": "composite-v2",
        "storyline": storyline,
        "title": title,
        "description": desc,
        "bodyJson": body,
        "seo": {
            "title": title,
            "description": desc[:200],
            "keywords": kw,
            "noIndex": False,
            "ogImage": {"url": OG_FALLBACK, "alt": title}
        }
    }
    fp = os.path.join(out_dir, f"{slug}.json")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(page, f, ensure_ascii=False, indent=2)
    return 1

def gen_topic_lp(d, out_dir):
    slug, storyline = d["slug"], d["storyline"]
    title, desc = d["title"], d["desc"]
    kw = d.get("kw", [])
    c = content_for_topic(slug)
    body = build_body(TOPIC_SECTIONS, SECTION_GEN_TOPIC, title, desc, c)
    page = {
        "slug": slug,
        "language": "zh",
        "category": "topic",
        "schemaVersion": "composite-v2",
        "storylineTemplate": storyline,
        "title": title,
        "description": desc,
        "bodyJson": body,
        "seo": {
            "title": title,
            "description": desc[:200],
            "keywords": kw,
            "noIndex": False,
            "ogImage": {"url": OG_FALLBACK, "alt": title}
        }
    }
    fp = os.path.join(out_dir, f"{slug}.json")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(page, f, ensure_ascii=False, indent=2)
    return 1

def main():
    total = 0
    print("--- Scenario LPs (15) ---")
    for d in SCENARIOS:
        gen_scenario_lp(d, SCENARIO_OUT)
        total += 1
        print(f"  {d['slug']:50s} ✓")
    print("--- Pain LPs (3) ---")
    for d in PAIN_LPS:
        gen_topic_lp(d, TOPIC_OUT)
        total += 1
        print(f"  {d['slug']:50s} ✓")
    print("--- Competitor LPs (2) ---")
    for d in COMPETITOR_LPS:
        gen_topic_lp(d, TOPIC_OUT)
        total += 1
        print(f"  {d['slug']:50s} ✓")
    print(f"\nTotal LP files generated: {total}")
    return total

if __name__ == "__main__":
    main()
