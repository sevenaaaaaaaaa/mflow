#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch generate 30 Chinese industry solution page JSONs (Batch 4)."""

import json, os, hashlib

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(VAULT, "1-3 GenFlow/Page Gen/Pages/Solution/zh")
os.makedirs(OUT, exist_ok=True)

OG_FALLBACK = "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d3e44c9edfb1a44f386973e9b3c23fcffddc8008.png"

STORYLINES = {
    "solution-ecommerce": {
        "sections": ["hero-journey","bento-4","capability-tabs","bento-2","workflow-vertical","comparison-table","cluster-block-dense","showcase-stacked","review-grid-3col","pricing-block","faq","cta-default"],
    },
    "solution-team": {
        "sections": ["hero-cinematic","bento-4","capability-tabs","bento-2","workflow-vertical","comparison-table","cluster-block-dense","showcase-stacked","testimonial","pricing-block","faq","cta-default"],
    },
    "solution-agency": {
        "sections": ["hero-mosaic","bento-4","capability-tabs","feature-detail","workflow-horizontal","comparison-table","cluster-block-dense","showcase-stacked","review-grid-4col","pricing-block","faq","cta-default"],
    },
    "solution-enterprise": {
        "sections": ["hero-cinematic","bento-6","capability-tabs","bento-2","workflow-vertical","comparison-table","cluster-block-dense","showcase-stacked","review-grid-3col","pricing-block","faq","cta-default"],
    },
    "solution-solo": {
        "sections": ["hero-split","bento-4","capability-tabs","feature-detail","workflow-vertical","comparison-before-after","cluster-block-dense","showcase-stacked","testimonial","pricing-block","faq","cta-default"],
    },
    "solution-mission": {
        "sections": ["hero-journey","bento-4","capability-tabs","bento-2","workflow-vertical","comparison-table","cluster-block-dense","showcase-stacked","testimonial","pricing-block","faq","cta-default"],
    }
}

def q(s): return json.dumps(s, ensure_ascii=False)

def hero_cinematic(product_tag, product_title, product_desc, C):
    return q({"type":"hero-cinematic","tag":product_tag,"title":product_title,"description":product_desc,"buttons":[{"text":"免费试用","href":"https://lovart.ai/signup","variant":"primary"}],"media":{"src":OG_FALLBACK,"alt":product_title}})

def hero_split(product_title, product_desc, C):
    return q({"type":"hero-split","title":product_title,"description":product_desc,"buttons":[{"text":"免费试用","href":"https://lovart.ai/signup","variant":"primary"}],"media":{"src":OG_FALLBACK,"alt":product_title}})

def hero_journey(product_title, product_desc, C):
    return q({"type":"hero-journey","title":product_title,"description":product_desc,"journeyCards":[{"step":f"步骤{n}","title":C.get(f"journey_{n}",""),"description":C.get(f"journey_{n}_desc","")} for n in range(1,6)],"buttons":[{"text":"免费试用","href":"https://lovart.ai/signup","variant":"primary"}]})

def hero_mosaic(product_title, product_desc, C):
    return q({"type":"hero-mosaic","title":product_title,"description":product_desc,"mosaicTiles":[{"title":C.get(f"mosaic_{n}",""),"description":C.get(f"mosaic_{n}_desc","")} for n in range(1,5)],"buttons":[{"text":"免费试用","href":"https://lovart.ai/signup","variant":"primary"}]})

def bento_4(title, cards, C):
    return q({"type":"bento-4","title":title,"cards":[{"title":c,"description":C.get(f"b4_{i}",""),"media":{"src":OG_FALLBACK,"alt":""}} for i,c in enumerate(cards)]})

def bento_6(title, cards, C):
    return q({"type":"bento-6","title":title,"cards":[{"title":c,"description":C.get(f"b6_{i}",""),"media":{"src":OG_FALLBACK,"alt":""}} for i,c in enumerate(cards)]})

def bento_2(title, cards, C):
    return q({"type":"bento-2","title":title,"cards":[{"title":c,"description":C.get(f"b2_{i}",""),"media":{"src":OG_FALLBACK,"alt":""}} for i,c in enumerate(cards)]})

def capability_tabs(C):
    return q({"type":"capability-tabs","title":"核心能力","tabs":[{"label":C.get(f"tab_{i}_label",""),"content":{"title":C.get(f"tab_{i}_title",""),"description":C.get(f"tab_{i}_desc",""),"media":{"src":OG_FALLBACK,"alt":""}}} for i in range(1,5)]})

def workflow_vertical(C):
    return q({"type":"workflow-vertical","title":"实施路径","steps":[{"title":C.get(f"wv_{i}",""),"description":C.get(f"wv_{i}_desc",""),"media":{"src":OG_FALLBACK,"alt":""}} for i in range(1,5)]})

def workflow_horizontal(C):
    return q({"type":"workflow-horizontal","title":"工作流程","steps":[{"title":C.get(f"wh_{i}",""),"description":C.get(f"wh_{i}_desc","")} for i in range(1,4)]})

def comparison_table(C):
    return q({"type":"comparison-table","title":"方案对比","rows":[{"label":C.get(f"comp_{i}_label",""),"before":C.get(f"comp_{i}_before",""),"after":C.get(f"comp_{i}_after","")} for i in range(1,6)],"highlightColumn":3})

def comparison_before_after(C):
    return q({"type":"comparison-before-after","title":"效果对比","before":{"title":C.get("ba_before_title",""),"description":C.get("ba_before_desc",""),"media":{"src":OG_FALLBACK,"alt":""}},"after":{"title":C.get("ba_after_title",""),"description":C.get("ba_after_desc",""),"media":{"src":OG_FALLBACK,"alt":""}}})

def cluster_block_dense(C):
    cards = []
    for i in range(1,7):
        t = C.get(f"cl_{i}","")
        d = C.get(f"cl_{i}_desc","")
        if t: cards.append({"title":t,"description":d,"media":{"src":OG_FALLBACK,"alt":""}})
    return q({"type":"cluster-block-dense","title":"应用场景","cards":cards})

def showcase_stacked(C):
    items = []
    for i in range(1,4):
        t = C.get(f"ss_{i}","")
        d = C.get(f"ss_{i}_desc","")
        if t: items.append({"title":t,"description":d,"media":{"src":OG_FALLBACK,"alt":""}})
    return q({"type":"showcase-stacked","title":"效果展示","items":items})

def testimonial_block(C):
    return q({"type":"testimonial","title":"客户故事","items":[{"quote":C.get("test_quote",""),"author":C.get("test_author",""),"role":C.get("test_role",""),"avatar":{"src":OG_FALLBACK,"alt":""}}]})

def review_grid_3col(C):
    return q({"type":"review-grid-3col","title":"用户评价","reviews":[{"rating":5,"text":C.get(f"rev_{i}",""),"author":C.get(f"rev_{i}_author","")} for i in range(1,4)]})

def review_grid_4col(C):
    return q({"type":"review-grid-4col","title":"用户评价","reviews":[{"rating":5,"text":C.get(f"rev_{i}",""),"author":C.get(f"rev_{i}_author","")} for i in range(1,5)]})

def pricing_block(C):
    return q({"type":"pricing-block","title":"定价方案","description":"灵活选择适合你的方案","plans":[{"name":"Starter","price":"$15/月","features":["基础功能","品牌套件","每月100次生成"]},{"name":"Basic","price":"$39/月","features":["全部功能","Brand Kit","每月500次生成"]},{"name":"Pro","price":"$79/月","features":["无限生成","优先支持","商业授权"]}]})

def faq_block(C):
    items = []
    for i in range(1,7):
        qq = C.get(f"faq_{i}","")
        aa = C.get(f"faq_{i}_a","")
        if qq: items.append({"question":qq,"answer":aa})
    return q({"type":"faq","title":"常见问题","items":items})

def cta_default(C):
    return q({"type":"cta-default","title":"开始使用Lovart","description":"免费试用，无需信用卡","buttons":[{"text":"免费试用","href":"https://lovart.ai/signup","variant":"primary"}]})

def feature_detail(C):
    return q({"type":"feature-detail","title":C.get("fd_title",""),"description":C.get("fd_desc",""),"media":{"src":OG_FALLBACK,"alt":""}})

SECTION_GEN = {
    "hero-cinematic": lambda C: hero_cinematic(C.get("product_tag",""),C.get("product_title",""),C.get("product_desc",""),C),
    "hero-split": lambda C: hero_split(C.get("product_title",""),C.get("product_desc",""),C),
    "hero-journey": lambda C: hero_journey(C.get("product_title",""),C.get("product_desc",""),C),
    "hero-mosaic": lambda C: hero_mosaic(C.get("product_title",""),C.get("product_desc",""),C),
    "bento-4": lambda C: bento_4("核心优势",C.get("bento_4_cards",[]).split("|"),C),
    "bento-6": lambda C: bento_6("方案能力",C.get("bento_6_cards",[]).split("|"),C),
    "bento-2": lambda C: bento_2("关键特性",C.get("bento_2_cards",[]).split("|"),C),
    "capability-tabs": capability_tabs,
    "workflow-vertical": workflow_vertical,
    "workflow-horizontal": workflow_horizontal,
    "comparison-table": comparison_table,
    "comparison-before-after": comparison_before_after,
    "cluster-block-dense": cluster_block_dense,
    "showcase-stacked": showcase_stacked,
    "testimonial": testimonial_block,
    "review-grid-3col": review_grid_3col,
    "review-grid-4col": review_grid_4col,
    "pricing-block": pricing_block,
    "faq": faq_block,
    "cta-default": cta_default,
    "feature-detail": feature_detail,
}

ALL_DATA = [
    {"slug":"zh-solution-ecommerce-taobao","storyline":"solution-ecommerce","title":"淘宝天猫AI设计解决方案 - 电商主图详情页批量生成 | Lovart","desc":"淘宝天猫卖家AI设计工具。批量生成主图、详情页、直通车图、大促素材，自动适配平台规范。","kw":["淘宝主图设计","电商AI设计","详情页批量生成"],"tag":"电商解决方案","ht":"淘宝天猫AI设计解决方案","hd":"从主图到详情页，从日常到双11大促。Lovart为淘宝天猫卖家提供全链路AI设计能力。"},
    {"slug":"zh-solution-ecommerce-pdd","storyline":"solution-ecommerce","title":"拼多多AI设计解决方案 - 白底图场景图促销图批量生成 | Lovart","desc":"拼多多卖家AI设计工具。批量生成白底图、场景图、促销标签图，适配拼多多平台风格。"},
    {"slug":"zh-solution-ecommerce-douyin","storyline":"solution-ecommerce","title":"抖音电商AI设计解决方案 - 直播切片图文带货素材批量生成","desc":"抖音电商AI设计工具。生成直播切片、图文带货素材、商品卡，适配抖音推荐流。"},
    {"slug":"zh-solution-ecommerce-cross-border","storyline":"solution-ecommerce","title":"跨境电商AI设计解决方案 - 多语言主图详情页Shopify独立站","desc":"跨境电商AI设计。多语言主图、A+页面、Shopify素材，独立站和亚马逊全覆盖。"},
    {"slug":"zh-solution-ecommerce-jd","storyline":"solution-ecommerce","title":"京东AI设计解决方案 - 京东主图详情页店铺装修批量生成","desc":"京东卖家AI设计。主图、商详、店铺首页装修素材，适配京东平台规范。"},
    {"slug":"zh-solution-xiaohongshu-creator","storyline":"solution-solo","title":"小红书博主AI设计解决方案 - 笔记封面配图批量生成","desc":"小红书博主AI设计。封面、配图、信息图、视频封面，批量提升内容颜值和点击率。"},
    {"slug":"zh-solution-bilibili-creator","storyline":"solution-solo","title":"B站UP主AI设计解决方案 - 视频封面专栏封面直播海报","desc":"B站UP主AI设计。视频封面、专栏头图、直播海报、动态配图一套搞定。"},
    {"slug":"zh-solution-douyin-creator","storyline":"solution-solo","title":"抖音达人AI设计解决方案 - 视频封面直播素材抖音图文","desc":"抖音达人AI设计。视频封面、直播背景、图文素材，快速产出日更内容。"},
    {"slug":"zh-solution-wechat-official-account","storyline":"solution-team","title":"公众号运营AI设计解决方案 - 封面头图配图排版素材","desc":"公众号运营AI设计。封面、头图、配图、信息图、海报，提升推文阅读体验。"},
    {"slug":"zh-solution-online-education","storyline":"solution-team","title":"在线教育AI设计解决方案 - 课件封面海报宣传物料批量生成","desc":"在线教育AI设计。课件封面、课程海报、宣传物料、结业证书，高效出课。"},
    {"slug":"zh-solution-design-training","storyline":"solution-team","title":"设计培训AI设计解决方案 - 课程素材学生作品展示物料","desc":"设计培训机构AI方案。课堂演示素材、学生作品包装、招生海报一套覆盖。"},
    {"slug":"zh-solution-design-education","storyline":"solution-enterprise","title":"高校设计系AI设计解决方案 - 教学演示学生作品科研绘图","desc":"高校设计系AI方案。教学演示素材、学生设计实训、科研可视化一站式。"},
    {"slug":"zh-solution-smb","storyline":"solution-solo","title":"中小企业AI设计解决方案 - 品牌LOGO名片宣传册一条龙","desc":"中小企业AI设计。从Logo到名片到宣传册，一个智能体搞定全部企业视觉需求。"},
    {"slug":"zh-solution-startup","storyline":"solution-team","title":"创业公司AI设计解决方案 - 品牌VI产品物料融资PPT","desc":"创业公司AI设计。品牌创建、产品物料、融资路演PPT，加速从0到1。"},
    {"slug":"zh-solution-ad-agency","storyline":"solution-agency","title":"广告公司AI设计解决方案 - 多客户批量创意素材产出平台","desc":"广告公司AI方案。多客户并行管理、创意素材批量产出、提案加速。"},
    {"slug":"zh-solution-mcn","storyline":"solution-agency","title":"MCN机构AI设计解决方案 - 达人矩阵批量内容素材管理","desc":"MCN机构AI方案。多达人素材管理、批量内容模板、品牌合作物料标准化。"},
    {"slug":"zh-solution-brand-marketing","storyline":"solution-team","title":"品牌方市场部AI设计解决方案 - 整合营销传播物料批量产出","desc":"品牌方市场部AI方案。整合营销传播素材、多平台适配、品牌一致性管理。"},
    {"slug":"zh-solution-food-beverage","storyline":"solution-solo","title":"餐饮行业AI设计解决方案 - 菜单海报外卖图门店物料","desc":"餐饮业AI设计。菜单设计、开业海报、外卖平台图片、门店形象物料全包。"},
    {"slug":"zh-solution-fashion-apparel","storyline":"solution-team","title":"服装时尚AI设计解决方案 - 产品图搭配图品牌LOOKBOOK","desc":"服装时尚AI方案。产品图、搭配图、模特图、LOOKBOOK、品牌视觉全链路。"},
    {"slug":"zh-solution-real-estate","storyline":"solution-enterprise","title":"房地产AI设计解决方案 - 楼盘海报户型图VR看房物料","desc":"房地产AI方案。楼盘海报、户型图、宣传册、现场物料、VR看房配套图。"},
    {"slug":"zh-solution-gaming","storyline":"solution-team","title":"游戏行业AI设计解决方案 - 游戏素材宣发物料社区周边","desc":"游戏AI方案。游戏宣传图、素材、社区海报、周边物料设计。"},
    {"slug":"zh-solution-tech-saas","storyline":"solution-enterprise","title":"科技SaaS AI设计解决方案 - 产品截图落地页博客配图","desc":"科技SaaS AI方案。产品截图优化、官网落地页、博客配图、品牌视觉升级。"},
    {"slug":"zh-solution-healthcare","storyline":"solution-enterprise","title":"医疗健康AI设计解决方案 - 科普海报宣传物料品牌形象","desc":"医疗健康AI方案。科普海报、宣传物料、品牌形象、合规视觉设计。"},
    {"slug":"zh-solution-finance","storyline":"solution-enterprise","title":"金融行业AI设计解决方案 - 投资者关系品牌视觉合规设计","desc":"金融行业AI方案。IR材料、品牌视觉、合规设计、客户沟通物料。"},
    {"slug":"zh-solution-photo-studio","storyline":"solution-solo","title":"摄影工作室AI设计解决方案 - 样片排版客户相册品牌社交","desc":"摄影工作室AI方案。样片排版、客户相册、品牌社交推广素材一条龙。"},
    {"slug":"zh-solution-design-studio","storyline":"solution-agency","title":"设计工作室AI设计解决方案 - 多项目并行客户交付提案","desc":"设计工作室AI方案。多项目管理、客户交付包装、提案加速、产能提升。"},
    {"slug":"zh-solution-printing","storyline":"solution-solo","title":"印刷厂快印店AI设计解决方案 - 客户自助设计模板批量排版","desc":"印刷厂AI方案。客户自助设计模板、批量排版、可变数据印刷对接。"},
    {"slug":"zh-solution-wedding","storyline":"solution-solo","title":"婚庆行业AI设计解决方案 - 婚礼邀请函海报现场物料","desc":"婚庆AI方案。婚礼邀请函、海报、现场物料、照片书模板。"},
    {"slug":"zh-solution-manufacturing","storyline":"solution-enterprise","title":"制造业AI设计解决方案 - 产品目录宣传册展会物料品牌","desc":"制造业AI方案。产品目录、宣传册、展会物料、品牌视觉标准化。"},
    {"slug":"zh-solution-nonprofit","storyline":"solution-mission","title":"非营利组织AI设计解决方案 - 筹款海报宣传物料品牌形象","desc":"非营利AI方案。筹款海报、公益宣传物料、品牌传播素材。"},
]

# Build each industry with enough content for 12 sections
def gen_all(OUT):
    created = 0
    for D in ALL_DATA:
        slug, storyline = D["slug"], D["storyline"]
        title = D.get("title", slug)
        desc = D.get("desc", "")
        kw = D.get("kw", [])
        tag = D.get("tag", "行业解决方案")
        ht = D.get("ht", title)
        hd = D.get("hd", desc)
        
        sections_data = STORYLINES[storyline]["sections"]
        sections = []
        for stype in sections_data:
            if stype == "hero-cinematic":
                sections.append(hero_cinematic(tag, ht, hd, {}))
            elif stype == "hero-split":
                sections.append(hero_split(ht, hd, {}))
            elif stype == "hero-journey":
                sections.append(hero_journey(ht, hd, {"journey_1":"市场洞察","journey_1_desc":"分析行业痛点","journey_2":"方案设计","journey_2_desc":"匹配Lovart能力","journey_3":"落地实施","journey_3_desc":"配置自动化","journey_4":"效果验证","journey_4_desc":"数据对比","journey_5":"持续优化","journey_5_desc":"迭代改进"}))
            elif stype == "hero-mosaic":
                sections.append(hero_mosaic(ht, hd, {"mosaic_1":"方案设计","mosaic_1_desc":"匹配行业需求","mosaic_2":"内容生产","mosaic_2_desc":"批量素材生成","mosaic_3":"品牌管理","mosaic_3_desc":"一致性保障","mosaic_4":"效果追踪","mosaic_4_desc":"数据驱动优化"}))
            elif stype == "bento-4":
                sections.append(bento_4("核心优势",["效率提升","质量保证","成本节约","品牌统一"],{"b4_0":"AI批量处理，效率提升5-10倍","b4_1":"专业级输出，模板质量保证","b4_2":"相比外包节省70%+成本","b4_3":"品牌规范自动保持一致性"}))
            elif stype == "bento-6":
                sections.append(bento_6("方案能力",["品牌视觉","内容生产","多平台适配","团队协作","数据分析","持续优化"],{"b6_0":"统一品牌资产管理","b6_1":"批量化内容生产","b6_2":"一键适配渠道","b6_3":"团队实时协作","b6_4":"效果数据追踪","b6_5":"AI持续学习优化"}))
            elif stype == "bento-2":
                sections.append(bento_2("关键特性",["核心功能","场景覆盖"],{"b2_0":"覆盖该行业所有设计场景","b2_1":"从简单到复杂全覆盖"}))
            elif stype == "capability-tabs":
                sections.append(capability_tabs({"tab_1_label":"方案一","tab_1_title":"需求分析","tab_1_desc":"深入了解行业特性，匹配最佳Lovart能力组合","tab_2_label":"方案二","tab_2_title":"执行流程","tab_2_desc":"从设计到交付的全链路自动化","tab_3_label":"方案三","tab_3_title":"质量保障","tab_3_desc":"AI预检+人工复检双层把关","tab_4_label":"方案四","tab_4_title":"迭代优化","tab_4_desc":"基于反馈持续优化输出质量"}))
            elif stype == "workflow-vertical":
                sections.append(workflow_vertical({"wv_1":"需求整理","wv_1_desc":"明确设计需求和品牌规范","wv_2":"AI生成","wv_2_desc":"Lovart AI批量生成初稿","wv_3":"人工精调","wv_3_desc":"在AI输出基础上微调","wv_4":"交付发布","wv_4_desc":"确认后发布到对应平台"}))
            elif stype == "workflow-horizontal":
                sections.append(workflow_horizontal({"wh_1":"需求梳理","wh_1_desc":"客户需求标准化","wh_2":"AI批处理","wh_2_desc":"批量生成交付物","wh_3":"品控交付","wh_3_desc":"统一质检后交付"}))
            elif stype == "comparison-table":
                sections.append(comparison_table({"comp_1_label":"效率","comp_1_before":"传统方式","comp_1_after":"Lovart方案","comp_2_label":"质量","comp_2_before":"依赖个人水平","comp_2_after":"AI专业输出","comp_3_label":"一致性","comp_3_before":"难以统一","comp_3_after":"规范自动保持","comp_4_label":"成本","comp_4_before":"高额外包","comp_4_after":"工具订阅","comp_5_label":"迭代","comp_5_before":"慢","comp_5_after":"实时调整"}))
            elif stype == "comparison-before-after":
                sections.append(comparison_before_after({"ba_before_title":"传统方式","ba_before_desc":"设计软件操作复杂，改稿周期长，成本高","ba_after_title":"Lovart方案","ba_after_desc":"对话式设计，秒级出稿，低门槛高产出"}))
            elif stype == "cluster-block-dense":
                sections.append(cluster_block_dense({"cl_1":"日常运营","cl_1_desc":"日常内容高效产出","cl_2":"大促活动","cl_2_desc":"活动物料快速准备","cl_3":"品牌升级","cl_3_desc":"品牌视觉迭代升级","cl_4":"多平台","cl_4_desc":"跨平台统一管理","cl_5":"团队协作","cl_5_desc":"多人协作效率","cl_6":"数据分析","cl_6_desc":"效果数据反馈优化"}))
            elif stype == "showcase-stacked":
                sections.append(showcase_stacked({"ss_1":"案例一","ss_1_desc":"某客户使用Lovart后设计效率提升5倍","ss_2":"案例二","ss_2_desc":"品牌一致性从60%提升到95%","ss_3":"案例三","ss_3_desc":"设计成本降低70%同时产出翻倍"}))
            elif stype == "testimonial":
                sections.append(testimonial_block({"test_quote":"Lovart彻底改变了我们的设计工作流。过去一周的工作量现在一天就能完成。","test_author":"张先生","test_role":"设计总监"}))
            elif stype == "review-grid-3col":
                sections.append(review_grid_3col({"rev_1":"效率提升超预期，团队产能翻倍","rev_1_author":"用户A","rev_2":"品牌一致性再也不用担心","rev_2_author":"用户B","rev_3":"AI生成+人工微调的最佳组合","rev_3_author":"用户C"}))
            elif stype == "review-grid-4col":
                sections.append(review_grid_4col({"rev_1":"多客户管理变得简单","rev_1_author":"客户A","rev_2":"交付速度提升显著","rev_2_author":"客户B","rev_3":"客户满意度提高","rev_3_author":"客户C","rev_4":"团队协作更顺畅","rev_4_author":"客户D"}))
            elif stype == "pricing-block":
                sections.append(pricing_block({}))
            elif stype == "faq":
                sections.append(faq_block({"faq_1":"这个方案适合什么规模的团队？","faq_1_a":"从个人到企业团队都适用，不同规模有不同计划","faq_2":"需要多长时间才能看到效果？","faq_2_a":"通常1-2周即可完成部署，当天可看到效果","faq_3":"学习成本高吗？","faq_3_a":"不需要专门培训，对话式交互即学即用","faq_4":"能和我现有的工具集成吗？","faq_4_a":"支持API对接，可与现有工作流集成","faq_5":"内容版权安全吗？","faq_5_a":"生成内容版权归用户所有，数据加密存储","faq_6":"有行业模板吗？","faq_6_a":"覆盖主流行业模板库，持续更新中"}))
            elif stype == "cta-default":
                sections.append(cta_default({}))
            elif stype == "feature-detail":
                sections.append(feature_detail({"fd_title":"差异化能力","fd_desc":"针对该行业场景深度优化的AI设计能力，覆盖从概念到交付的全流程。"}))
            else:
                sections.append(q({"type":stype,"title":"待补充","description":"内容待填充"}))

        body_json_str = "[" + ",".join(sections) + "]"

        page = {
            "slug": slug,
            "language": "zh",
            "category": "solution",
            "schemaVersion": "composite-v2",
            "storyline": storyline,
            "title": title,
            "description": desc,
            "bodyJson": body_json_str,
            "seo": {
                "title": title,
                "description": desc[:200],
                "keywords": kw,
                "noIndex": False,
                "ogImage": {"url": OG_FALLBACK, "alt": title}
            }
        }

        fp = os.path.join(OUT, f"{slug}.json")
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(page, f, ensure_ascii=False, indent=2)
        created += 1
        print(f"  {slug:50s} ✓")

    return created

if __name__ == "__main__":
    total = gen_all(OUT)
    print(f"\nGenerated {total} solution pages")
