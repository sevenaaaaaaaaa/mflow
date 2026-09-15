#!/usr/bin/env python3
from pathlib import Path
"""
Batch 3: generate 60 Chinese design category topic landing page JSONs (composite-v2).

Output: 1-3 GenFlow/Page Gen/Pages/topic/zh/{slug}.json
"""

import json
import os
import sys
import re

OUT_DIR = str(Path(__file__).resolve().parents[2] / "1-3 GenFlow/Page Gen/Pages/topic/zh")

IMG_HERO = "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/4573c61a748407d72a79a8f1baabd7ae19b41f2c.png"
IMG_CARD = "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d3e44c9edfb1a44f386973e9b3c23fcffddc8008.png"
IMG_BRAND = "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/55b94439550ff0fefec6a09ca160df04a9a3b27b.png"

BANNED = [
    "赋能", "闭环", "抓手", "链路", "底层逻辑", "方法论", "心智",
    "对齐", "颗粒度", "打法", "痛点", "破局", "深挖", "见证",
    "颠覆性", "前沿",
]

BASE_BUTTONS = [
    {"text": "免费试用", "href": "https://lovart.ai/signup", "variant": "primary"},
    {"text": "了解更多", "href": "", "variant": "secondary"},
]

BASE_BUTTONS_PRIMARY = [
    {"text": "免费试用", "href": "https://lovart.ai/signup", "variant": "primary"},
]

CARD_POOL = [
    {"title": "快速出图", "desc": "输入需求AI即刻生成，告别漫长等待和反复沟通。"},
    {"title": "批量生产", "desc": "一次操作批量生成100张图，设计效率提升10倍。"},
    {"title": "精准编辑", "desc": "Touch Edit点触编辑，一句话改图不用重画。"},
    {"title": "品牌一致", "desc": "Brand Kit自动保持品牌调性一致性。"},
    {"title": "全格式输出", "desc": "PNG/PSD/SVG/PDF/MP4一键导出。"},
    {"title": "零门槛上手", "desc": "自然语言交互，无需任何设计经验。"},
    {"title": "团队协作", "desc": "多人在线协作，审稿修改实时同步。"},
    {"title": "商用授权", "desc": "付费方案含完整商业授权，版权无忧。"},
]

CAPABILITY_TABS = [
    {
        "label": "MCoT 引擎",
        "title": "思维链推理引擎",
        "desc": "不像普通AI直接生成——Lovart先理解你的业务场景、品牌调性、目标受众，再进行策略性设计。相当于你的专属创意总监。",
    },
    {
        "label": "Touch Edit",
        "title": "点触编辑：精准修改每一个元素",
        "desc": "不满意局部？直接选中修改。支持文字替换、元素移动、风格调整。无需重画，精度达像素级。",
    },
    {
        "label": "Brand Kit",
        "title": "品牌资产统一管理",
        "desc": "将Logo、色彩、字体存入Brand Kit，所有设计内容自动应用品牌规范。一人搭建，全队复用。",
    },
    {
        "label": "批量生成",
        "title": "一次操作 = 100张图",
        "desc": "设置好模板和规则，AI批量生成多尺寸、多语言的素材变体。适合电商大促和社媒矩阵运营。",
    },
]

GALLERY_ITEMS = [
    {"label": "商旅出行", "img": IMG_HERO},
    {"label": "国潮插画", "img": IMG_CARD},
    {"label": "极简商务", "img": IMG_BRAND},
    {"label": "食品餐饮", "img": IMG_HERO},
    {"label": "科技数码", "img": IMG_CARD},
    {"label": "时尚美妆", "img": IMG_BRAND},
    {"label": "教育培训", "img": IMG_HERO},
    {"label": "医疗健康", "img": IMG_CARD},
    {"label": "房地产", "img": IMG_BRAND},
    {"label": "电商零售", "img": IMG_HERO},
    {"label": "文化创意", "img": IMG_CARD},
    {"label": "金融保险", "img": IMG_BRAND},
]


def make_hero_gallery(title, desc, tag="AI设计智能体"):
    return {
        "type": "hero-gallery",
        "tag": tag,
        "title": title,
        "highlightedText": "",
        "description": desc,
        "buttons": BASE_BUTTONS,
        "media": {"src": IMG_HERO, "alt": title},
        "gallery": GALLERY_ITEMS,
    }


def make_hero_split(title, desc, badge="AI设计智能体"):
    return {
        "type": "hero-split",
        "badge": badge,
        "title": title,
        "highlightedText": "",
        "description": desc,
        "buttons": BASE_BUTTONS_PRIMARY,
        "media": {"src": IMG_HERO, "alt": title},
    }


def make_bento(title, desc, cards, bento_type="bento-6"):
    return {
        "type": bento_type,
        "title": title,
        "description": desc,
        "cards": [
            {
                "title": c["title"],
                "description": c["desc"],
                "media": {"src": IMG_CARD, "alt": ""},
            }
            for c in cards
        ],
    }


def make_capability_tabs():
    return {
        "type": "capability-tabs",
        "title": "核心技术能力",
        "description": "Lovart 的独家技术，让AI设计真正可用",
        "tabs": [
            {
                "label": t["label"],
                "content": {
                    "title": t["title"],
                    "description": t["desc"],
                    "media": {"src": IMG_HERO, "alt": t["label"]},
                },
            }
            for t in CAPABILITY_TABS
        ],
    }


def make_tool_grid(topic):
    return {
        "type": "tool-grid",
        "title": f"用Lovart实现{topic}",
        "description": "AI设计智能体给你全新的工作方式",
        "tools": [
            {
                "title": "AI智能体",
                "description": "理解你的意图，自动完成设计",
                "icon": "sparkles",
                "media": {"src": IMG_CARD, "alt": ""},
            },
            {
                "title": "智能模板",
                "description": "海量设计模板，快速启动",
                "icon": "template",
                "media": {"src": IMG_CARD, "alt": ""},
            },
            {
                "title": "在线编辑器",
                "description": "拖拽式操作，所见即所得",
                "icon": "edit",
                "media": {"src": IMG_CARD, "alt": ""},
            },
            {
                "title": "品牌资产",
                "description": "统一管理品牌视觉元素",
                "icon": "brand",
                "media": {"src": IMG_CARD, "alt": ""},
            },
        ],
    }


def make_canvas_wall(topic_for):
    return {
        "type": "canvas-wall",
        "title": "看看用户用Lovart做的设计",
        "description": "来自真实用户的" + topic_for + "作品展示",
        "items": [
            {"src": IMG_HERO, "alt": "设计作品1"},
            {"src": IMG_CARD, "alt": "设计作品2"},
            {"src": IMG_BRAND, "alt": "设计作品3"},
            {"src": IMG_HERO, "alt": "设计作品4"},
            {"src": IMG_CARD, "alt": "设计作品5"},
            {"src": IMG_BRAND, "alt": "设计作品6"},
        ],
    }


def make_workflow_horizontal(topic, steps):
    return {
        "type": "workflow-horizontal",
        "title": f"{topic}的工作流程",
        "description": "三步完成专业设计",
        "steps": steps,
    }


DEFAULT_WORKFLOW_STEPS = [
    {
        "title": "描述需求",
        "description": "用自然语言描述你想要的风格、内容和使用场景",
    },
    {
        "title": "AI生成方案",
        "description": "Lovart AI根据你的需求生成多个设计方案供选择",
    },
    {
        "title": "微调导出",
        "description": "Touch Edit精修细节，确认后导出所需格式",
    },
]


def make_comparison_table():
    return {
        "type": "comparison-table",
        "title": "为什么选择Lovart",
        "description": "和传统设计方式对比，Lovart的优势在哪里",
        "headers": ["对比项", "Lovart AI设计", "传统设计方式"],
        "rows": [
            ["设计速度", "30秒生成方案", "1-3天出初稿"],
            ["设计成本", "订阅制，低至每天几元", "每项目数千至数万元"],
            ["修改次数", "无限次实时修改", "有限次修改，加收费用"],
            ["设计质量", "AI+人工双保险", "依赖设计师个人水平"],
            ["品牌一致性", "Brand Kit自动维护", "需要人工记忆和比对"],
            ["多尺寸适配", "一键生成所有尺寸", "逐个手动调整"],
        ],
    }


def make_cluster_block_dense(topic, items):
    return {
        "type": "cluster-block-dense",
        "title": f"{topic}的应用场景",
        "description": "满足不同场景的设计需求",
        "clusters": [
            {
                "title": item["title"],
                "description": item["desc"],
                "media": {"src": IMG_CARD, "alt": ""},
                "tags": item.get("tags", []),
            }
            for item in items
        ],
    }


def make_feature_detail(topic):
    features = [
        {
            "title": "AI智能生成",
            "desc": f"输入描述即可生成专业的{topic}方案，无需任何设计经验。",
            "img": IMG_HERO,
        },
        {
            "title": "品牌资产管理",
            "desc": "将品牌元素存入Brand Kit，所有设计自动保持一致性。",
            "img": IMG_BRAND,
        },
        {
            "title": "多格式导出",
            "desc": "支持PNG、SVG、PDF、PSD等多种格式，满足印刷和数字需求。",
            "img": IMG_CARD,
        },
    ]
    return {
        "type": "feature-detail-list",
        "title": f"Lovart {topic}核心功能",
        "description": "专业级AI设计能力，让创意落地更快",
        "features": features,
    }


def make_faq(questions):
    return {
        "type": "faq",
        "title": "常见问题",
        "description": "关于Lovart" + "的常见疑问",
        "questions": [{"title": q["q"], "content": q["a"]} for q in questions],
    }


DEFAULT_FAQ = [
    {
        "q": "Lovart适合没有设计经验的人使用吗？",
        "a": "非常适合。Lovart用自然语言交互，输入文字描述即可生成专业设计。内置AI引导流程，零基础用户也能快速上手。",
    },
    {
        "q": "Lovart生成的图片可以商用吗？",
        "a": "Lovart所有付费方案均包含完整商业授权。生成的图片可用于商业用途，包括企业品牌宣传、产品包装、广告投放等。",
    },
    {
        "q": "Lovart支持哪些输出格式？",
        "a": "支持PNG、JPG、SVG、PDF、PSD等格式输出。SVG矢量格式适合Logo等需要缩放的场景，PDF适合印刷品。",
    },
    {
        "q": "免费版和付费版有什么区别？",
        "a": "免费版可使用基础AI功能并生成标准分辨率图片。付费版解锁高清输出、全量模板、Brand Kit品牌管理和批量生成等高级功能。",
    },
    {
        "q": "Lovart和Canva/稿定设计有什么不同？",
        "a": "Lovart是AI设计智能体，不只是模板编辑器。它能理解你的业务需求并自主完成设计，而传统工具需要手动拖拽排版。",
    },
]

DEFAULT_FAQ_SHORT = DEFAULT_FAQ[:3]


def make_cta_default(topic_for):
    return {
        "type": "cta-default",
        "title": f"开始使用Lovart进行{topic_for}",
        "description": "免费试用，无需信用卡。30秒注册开始设计。",
        "buttons": [
            {"text": "免费试用", "href": "https://lovart.ai/signup", "variant": "primary"}
        ],
    }


# ── Page definitions ──────────────────────────────────────────────────────

PAGES = []

# ── D1 Logo Design (5) ──
PAGES.append({
    "slug": "zh-topic-logo-design",
    "t": "AI Logo设计 - 在线免费Logo生成器 | Lovart",
    "d": "使用Lovart AI在线设计Logo。输入品牌信息，自动生成多风格Logo方案。免费使用，无需设计经验。",
    "kw": ["AI Logo设计", "在线Logo生成器", "免费Logo设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI Logo设计：输入品牌名，30秒生成专业Logo",
    "hero_d": "告别昂贵的设计费和漫长的等待。Lovart AI根据品牌名称、行业属性和风格偏好，30秒内生成多个高品质Logo方案。",
    "tag": "AI Logo设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-logo-design-free",
    "t": "免费Logo设计 - 在线免费制作品牌Logo | Lovart",
    "d": "免费AI Logo设计工具。无需设计经验，输入品牌信息即可生成专业Logo。下载高清PNG和SVG格式。",
    "kw": ["免费Logo设计", "免费Logo生成", "Logo制作免费"],
    "tmpl": "landing-trial-now",
    "hero_t": "免费Logo设计：不花一分钱拥有专业品牌标识",
    "hero_d": "创业初期预算有限？免费AI Logo设计工具帮你搞定品牌形象。高清矢量格式，商用终身授权。",
    "tag": "AI Logo设计",
    "faq": DEFAULT_FAQ_SHORT,
})
PAGES.append({
    "slug": "zh-topic-logo-design-online",
    "t": "在线Logo生成 - 浏览器打开即用的Logo工具 | Lovart",
    "d": "在线Logo生成器。免安装免下载，浏览器打开即可使用AI设计Logo。支持团队协作和实时编辑。",
    "kw": ["在线Logo生成", "网页版Logo设计", "浏览器Logo工具"],
    "tmpl": "landing-trial-now",
    "hero_t": "在线Logo生成器：打开浏览器就能设计Logo",
    "hero_d": "无需安装任何软件。打开浏览器，描述你的品牌，AI即刻生成多款Logo方案。在线编辑、实时预览、一键下载。",
    "tag": "AI Logo设计",
    "faq": DEFAULT_FAQ_SHORT,
})
PAGES.append({
    "slug": "zh-topic-logo-design-enterprise",
    "t": "企业Logo设计 - 公司品牌标识专业设计 | Lovart",
    "d": "企业Logo设计服务。AI辅助生成+人工精调，适合中大型企业的品牌标识系统建设。",
    "kw": ["企业Logo设计", "公司标志设计", "品牌标识设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "企业Logo设计：打造经得起时间考验的品牌标识",
    "hero_d": "企业Logo不止是一个图形，它是品牌资产的核心。Lovart AI从企业战略和行业属性出发，设计有辨识度的专业标识。",
    "tag": "企业品牌设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-logo-design-restaurant",
    "t": "餐饮Logo设计 - 餐厅品牌标识AI生成 | Lovart",
    "d": "餐饮行业Logo设计。适合餐厅、咖啡馆、奶茶店、烘焙坊等餐饮品牌。AI快速生成多种风格。",
    "kw": ["餐饮Logo设计", "餐厅标志设计", "咖啡馆Logo"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "餐饮Logo设计：用美食气质打动顾客",
    "hero_d": "餐饮Logo要传递的是味道和氛围。Lovart AI分析餐饮品类和目标客群，生成与菜品风格一致的品牌标识。",
    "tag": "餐饮品牌设计",
    "faq": DEFAULT_FAQ,
})

# ── D2 Poster Design (5) ──
PAGES.append({
    "slug": "zh-topic-poster-design",
    "t": "AI海报设计 - 免费在线海报制作工具 | Lovart",
    "d": "AI海报设计工具。输入文案自动生成促销海报、活动海报、招聘海报。海量模板免费使用。",
    "kw": ["AI海报设计", "在线海报制作", "海报生成器"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI海报设计：输入文案自动生成专业海报",
    "hero_d": "再也不用从空白画布开始。输入海报主题和文案，Lovart AI自动完成版面布局、配色方案和字体搭配。",
    "tag": "AI海报设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-poster-design-free",
    "t": "免费海报制作 - 不花钱做专业促销海报 | Lovart",
    "d": "免费海报制作工具。海量模板免费使用，拖拽式编辑。适合中小企业日常营销使用。",
    "kw": ["免费海报制作", "免费海报模板", "促销海报免费"],
    "tmpl": "landing-trial-now",
    "hero_t": "免费海报制作：小预算也能做好营销物料",
    "hero_d": "营销预算有限但海报不能少。免费海报制作工具提供丰富的模板库，输入内容即可完成设计。",
    "tag": "AI海报设计",
    "faq": DEFAULT_FAQ_SHORT,
})
PAGES.append({
    "slug": "zh-topic-poster-design-online",
    "t": "在线海报设计 - 免安装网页版海报工具 | Lovart",
    "d": "在线海报设计工具。浏览器打开即可用，支持团队协作。适用于电商促销、品牌活动等场景。",
    "kw": ["在线海报设计", "网页海报制作", "海报设计平台"],
    "tmpl": "landing-trial-now",
    "hero_t": "在线海报设计：浏览器打开就能做专业海报",
    "hero_d": "不用下载Photoshop，不用学设计。在线海报设计工具，模板改文字换图片，几分钟出图。",
    "tag": "AI海报设计",
    "faq": DEFAULT_FAQ_SHORT,
})
PAGES.append({
    "slug": "zh-topic-poster-design-promotion",
    "t": "促销海报设计 - 提升转化率的电商海报 | Lovart",
    "d": "促销海报设计工具。适合电商大促、节日营销、新品上市等场景。AI优化文案和视觉布局。",
    "kw": ["促销海报设计", "活动海报设计", "电商促销海报"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "促销海报设计：让每一场活动都有爆款视觉",
    "hero_d": "促销海报的核心是传递优惠信息并激发购买欲望。Lovart AI自动强化促销信息层级，提升海报转化效果。",
    "tag": "电商海报设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-poster-design-event",
    "t": "活动海报设计 - 会议展览演出海报制作 | Lovart",
    "d": "活动海报设计工具。适合演唱会、展览、会议、发布会等各类活动宣传海报制作。",
    "kw": ["活动海报设计", "会议海报模板", "演出海报制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "活动海报设计：让你的活动在朋友圈刷屏",
    "hero_d": "活动海报是吸引参与的第一张名片。Lovart AI根据活动类型和目标受众，生成符合活动调性的高质量海报。",
    "tag": "活动宣传设计",
    "faq": DEFAULT_FAQ,
})

# ── D3 Cover Design (4) ──
PAGES.append({
    "slug": "zh-topic-cover-design",
    "t": "AI封面设计 - 在线封面制作工具 | Lovart",
    "d": "AI封面设计工具。适合公众号封面、视频封面、电子书封面。智能推荐最佳文字排版和配色方案。",
    "kw": ["AI封面设计", "封面制作工具", "在线封面设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI封面设计：点击率提升300%的封面制作方法",
    "hero_d": "封面决定内容的打开率。Lovart AI分析内容主题和目标平台，智能推荐最吸引眼球的封面布局和配色。",
    "tag": "AI封面设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-cover-design-video",
    "t": "视频封面设计 - YouTube/B站视频缩略图制作 | Lovart",
    "d": "视频封面设计工具。适合YouTube、Bilibili、抖音的视频缩略图制作。提升视频点击率。",
    "kw": ["视频封面设计", "视频缩略图制作", "YouTube封面"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "视频封面设计：一张封面决定视频播放量",
    "hero_d": "视频封面是内容的第一印象。Lovart AI根据视频内容和平台特性，自动生成高点击率的视频缩略图。",
    "tag": "视频封面设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-cover-design-wechat",
    "t": "公众号封面设计 - 微信文章封面图制作 | Lovart",
    "d": "微信公众号封面设计工具。适合文章头图、次图、引导关注图。模板适配微信官方尺寸。",
    "kw": ["公众号封面设计", "微信封面图", "公众号配图"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "公众号封面设计：一眼就让读者想点进来",
    "hero_d": "公众号封面是打开率的决定因素之一。Lovart AI生成与文章主题贴合的封面图片，适配微信所有封面位尺寸。",
    "tag": "新媒体封面设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-cover-design-xiaohongshu",
    "t": "小红书封面设计 - 提高笔记点击率的方法 | Lovart",
    "d": "小红书封面设计。适合笔记配图、合集封面、个人主页。实测封面点击率提升300%。",
    "kw": ["小红书封面设计", "小红书配图", "笔记封面模板"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "小红书封面设计：流量密码藏在封面里",
    "hero_d": "小红书封面是流量的第一道门。Lovart AI分析小红书热门封面规律，生成适合平台的吸睛封面。",
    "tag": "小红书封面设计",
    "faq": DEFAULT_FAQ,
})

# ── D4 Ecommerce Main Image (5) ──
PAGES.append({
    "slug": "zh-topic-ecommerce-main-image",
    "t": "AI电商主图设计 - 商品主图制作工具 | Lovart",
    "d": "AI电商主图设计工具。自动生成白底图、场景图和卖点标签图。支持批量处理和A/B测试。",
    "kw": ["AI电商主图", "商品主图设计", "电商主图制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI电商主图设计：商品点击率翻倍的主图制作法",
    "hero_d": "电商主图决定用户是否点击进入详情页。Lovart AI自动生成高质量主图，突出产品卖点和差异化优势。",
    "tag": "电商视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-ecommerce-main-image-taobao",
    "t": "淘宝主图设计 - 提升淘宝点击率的商品图片 | Lovart",
    "d": "淘宝主图设计工具。适配淘宝平台规范，自动添加促销标签。适合天猫淘宝店铺使用。",
    "kw": ["淘宝主图设计", "天猫主图制作", "淘宝商品图"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "淘宝主图设计：搜索页面前三屏的点击秘诀",
    "hero_d": "淘宝主图在搜索结果页直接影响点击率。Lovart AI生成符合淘宝平台规范的主图，突出促销信息和产品卖点。",
    "tag": "电商视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-ecommerce-main-image-jd",
    "t": "京东主图设计 - 京东商品主图优化制作 | Lovart",
    "d": "京东主图设计工具。适配京东平台尺寸规范，支持多图轮播制作。提升京东搜索排名。",
    "kw": ["京东主图设计", "京东商品图制作", "电商主图生成"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "京东主图设计：专业商品主图提升搜索排名",
    "hero_d": "京东对主图规范要求严格。Lovart AI自动适配京东800×800尺寸规范，生成清晰的商品展示主图和功能说明图。",
    "tag": "电商视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-ecommerce-main-image-pdd",
    "t": "拼多多主图设计 - 引流款主图批量制作 | Lovart",
    "d": "拼多多主图设计工具。适合拼多多爆款商品的引流主图，批量生成多SKU主图。",
    "kw": ["拼多多主图设计", "PDD商品图", "拼多多主图制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "拼多多主图设计：低价引流款也能有高级感",
    "hero_d": "拼多多主图需要在低价感中突出品质。Lovart AI平衡价格信息传递与视觉品质感，生成高点击率主图。",
    "tag": "电商视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-ecommerce-main-image-douyin",
    "t": "抖音电商主图设计 - 抖店商品主图制作 | Lovart",
    "d": "抖音电商主图设计工具。适配抖音电商平台规范。适合直播引流款和日常动销款。",
    "kw": ["抖音主图设计", "抖店商品图", "抖音电商图片"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "抖音电商主图设计：在信息流里一秒抓住注意力",
    "hero_d": "抖音电商主图在信息流中竞争用户的注意力。Lovart AI生成适合抖音平台视觉风格的商品主图。",
    "tag": "电商视觉设计",
    "faq": DEFAULT_FAQ,
})

# ── D5 Product Detail Design (3) ──
PAGES.append({
    "slug": "zh-topic-product-detail-design",
    "t": "AI详情页设计 - 电商商品详情页制作 | Lovart",
    "d": "AI电商详情页设计工具。自动生成商品描述、卖点图、对比图和实拍图排版。支持批量生成。",
    "kw": ["AI详情页设计", "商品详情页制作", "电商详情页模板"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI详情页设计：告别套模板，每款商品都有专属详情",
    "hero_d": "详情页是转化的临门一脚。Lovart AI根据商品属性和卖点，自动生成产品参数、功能说明、使用场景等模块化的详情页。",
    "tag": "电商详情设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-product-detail-design-taobao",
    "t": "淘宝详情页设计 - 高转化淘宝详情制作 | Lovart",
    "d": "淘宝详情页设计工具。适配淘宝详情页规范，自动生成卖点展示、产品参数和好评模块。",
    "kw": ["淘宝详情页设计", "天猫详情页制作", "电商详情设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "淘宝详情页设计：从用户顾虑到下单的完整转化路径",
    "hero_d": "淘宝详情页要解决用户所有顾虑。Lovart AI按用户疑问、产品参数、使用效果、售后保障的递进结构生成详情页。",
    "tag": "电商详情设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-product-detail-design-jd",
    "t": "京东详情页设计 - 专业京东商品描述制作 | Lovart",
    "d": "京东详情页设计工具。适配京东平台规范，自动生成产品参数表格、功能对比和使用说明。",
    "kw": ["京东详情页设计", "京东商品描述", "产品详情页制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "京东详情页设计：专业参数展示打动理性消费者",
    "hero_d": "京东用户更看重产品参数和专业性。Lovart AI生成结构清晰的参数展示、材质说明和功能对比模块。",
    "tag": "电商详情设计",
    "faq": DEFAULT_FAQ,
})

# ── D6 Social Media Design (6) ──
PAGES.append({
    "slug": "zh-topic-social-media-design",
    "t": "AI社媒图片设计 - 社交媒体配图制作 | Lovart",
    "d": "AI社媒图片设计工具。适合微信公众号、小红书、微博、抖音等平台配图。一键调整各平台尺寸。",
    "kw": ["AI社媒图片设计", "社交媒体配图", "新媒体图片制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI社媒图片设计：多平台内容运营的视觉利器",
    "hero_d": "每个平台都有不同的图片尺寸和风格要求。Lovart AI一键适配主流社媒平台，保持品牌视觉统一性。",
    "tag": "社媒视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-social-media-design-xiaohongshu",
    "t": "小红书配图设计 - 提高笔记赞藏率的图片 | Lovart",
    "d": "小红书配图设计工具。适合爆款笔记封面、图文详情和合集封面。掌握小红书视觉流量密码。",
    "kw": ["小红书配图设计", "小红书图片制作", "笔记配图模板"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "小红书配图设计：每一张图都是流量入口",
    "hero_d": "小红书的图片质量直接影响笔记表现。Lovart AI生成本地化、生活化的配图风格，帮助提升笔记互动率。",
    "tag": "小红书视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-social-media-design-douyin",
    "t": "抖音配图设计 - 提升短视频互动率的配图 | Lovart",
    "d": "抖音配图设计工具。适合抖音商品卡、直播预告、短视频封面。适配抖音竖屏规范。",
    "kw": ["抖音配图设计", "抖音图片制作", "短视频配图"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "抖音配图设计：让用户在划走之前停下来",
    "hero_d": "抖音配图需要在极短时间内抓住注意力。Lovart AI生成视觉冲击力强、信息明确的竖屏配图。",
    "tag": "短视频视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-social-media-design-wechat",
    "t": "微信配图设计 - 公众号朋友圈配图制作 | Lovart",
    "d": "微信配图设计工具。适合公众号文章配图、朋友圈素材、视频号封面。适配微信生态尺寸。",
    "kw": ["微信配图设计", "公众号配图制作", "朋友圈素材"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "微信配图设计：朋友圈和公众号的视觉升级方案",
    "hero_d": "微信生态中的配图需要兼顾专业度和社交感。Lovart AI生成适配公众号文章、朋友圈和视频号的视觉素材。",
    "tag": "微信视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-social-media-design-weibo",
    "t": "微博配图设计 - 热搜话题配图制作 | Lovart",
    "d": "微博配图设计工具。适合微博头条文章配图、九宫格内容、话题头图。适配微博尺寸。",
    "kw": ["微博配图设计", "微博图片制作", "社交平台配图"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "微博配图设计：在信息洪流中脱颖而出",
    "hero_d": "微博信息更新快，配图需要一眼传递核心信息。Lovart AI生成高对比度、信息明确的微博配图。",
    "tag": "微博视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-social-media-design-bilibili",
    "t": "B站配图设计 - 视频封面和专栏配图 | Lovart",
    "d": "B站配图设计工具。适合B站视频封面、专栏头图、动态配图。风格偏年轻化和二次元。",
    "kw": ["B站配图设计", "哔哩哔哩封面", "B站专栏头图"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "B站配图设计：年轻化视觉语言吸引Z世代",
    "hero_d": "B站用户喜欢个性鲜明的视觉风格。Lovart AI生成适合B站社区的二次元风格和年轻化配图。",
    "tag": "B站视觉设计",
    "faq": DEFAULT_FAQ,
})

# ── D7 PPT Design (4) ──
PAGES.append({
    "slug": "zh-topic-ppt-design",
    "t": "AI PPT设计 - 在线演示文稿制作工具 | Lovart",
    "d": "AI PPT设计工具。输入主题自动生成专业演示文稿。支持商务汇报、教育培训、路演融资等场景。",
    "kw": ["AI PPT设计", "在线PPT制作", "演示文稿生成"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI PPT设计：10分钟完成一天的PPT制作工作",
    "hero_d": "告别熬夜做PPT。输入主题和要点，Lovart AI自动生成结构清晰、视觉统一的专业演示文稿。",
    "tag": "AI PPT设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-ppt-design-business",
    "t": "商务PPT设计 - 企业汇报演示文稿制作 | Lovart",
    "d": "商务PPT设计工具。适合公司周报、季度汇报、年度总结和产品发布。专业商务风格。",
    "kw": ["商务PPT设计", "企业汇报PPT", "商业演示制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "商务PPT设计：汇报演示中的专业感从何而来",
    "hero_d": "商务PPT代表公司形象。Lovart AI采用专业商务配色和排版，确保数据清晰可读、信息层次分明。",
    "tag": "商务演示设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-ppt-design-education",
    "t": "教育PPT设计 - 课程教学演示课件制作 | Lovart",
    "d": "教育PPT设计工具。适合在线课程课件、培训教材、学术报告演示。支持公式和图表展示。",
    "kw": ["教育PPT设计", "教学课件制作", "培训PPT模板"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "教育PPT设计：让知识点一目了然的课件制作法",
    "hero_d": "教育PPT的核心是知识传递效率。Lovart AI自动梳理内容结构，用图表、图示和递进式排版提升学习效果。",
    "tag": "教育演示设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-ppt-design-pitch",
    "t": "融资路演PPT设计 - 打动投资人的商业计划书 | Lovart",
    "d": "融资路演PPT设计工具。适合商业计划书、BP演示、投资人汇报。专业投资机构认可的设计风格。",
    "kw": ["融资PPT设计", "路演PPT制作", "商业计划书设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "融资路演PPT设计：每一页都在为估值加分",
    "hero_d": "路演PPT是投资人了解项目的第一窗口。Lovart AI按照投资机构阅读习惯设计逻辑清晰的演示结构。",
    "tag": "融资演示设计",
    "faq": DEFAULT_FAQ,
})

# ── D8 Banner Design (3) ──
PAGES.append({
    "slug": "zh-topic-banner-design",
    "t": "AI Banner设计 - 网页横幅广告制作 | Lovart",
    "d": "AI Banner设计工具。适合网站横幅、社交媒体封面、广告投放图。智能适配多种Banner尺寸。",
    "kw": ["AI Banner设计", "网页横幅制作", "广告Banner模板"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI Banner设计：品牌横幅广告的高效制作方式",
    "hero_d": "Banner是品牌在线展示的核心载体。Lovart AI从品牌资产中提取配色和字体，生成风格统一的横幅系列。",
    "tag": "广告横幅设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-banner-design-ad",
    "t": "广告Banner设计 - 信息流广告投放素材制作 | Lovart",
    "d": "广告Banner设计工具。适合Google Ads、Facebook Ads、抖音信息流等广告投放素材制作。",
    "kw": ["广告Banner设计", "信息流广告素材", "投放图片制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "广告Banner设计：提升广告点击率和ROI的素材方法",
    "hero_d": "广告投放素材直接影响广告效果。Lovart AI生成符合各平台规范的广告Banner，优化CTA位置和视觉层次。",
    "tag": "广告投放设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-banner-design-ecommerce",
    "t": "电商Banner设计 - 店铺首页轮播图制作 | Lovart",
    "d": "电商Banner设计工具。适合淘宝天猫京东店铺首页轮播图、促销活动页头图等场景。",
    "kw": ["电商Banner设计", "店铺首页轮播图", "促销活动头图"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "电商Banner设计：店铺首页的黄金3秒法则",
    "hero_d": "电商Banner是店铺的流量入口。Lovart AI根据促销信息和品牌调性设计高转化的店铺Banner。",
    "tag": "电商横幅设计",
    "faq": DEFAULT_FAQ,
})

# ── D9 Business Card Design (3) ──
PAGES.append({
    "slug": "zh-topic-business-card-design",
    "t": "AI名片设计 - 在线商务名片制作工具 | Lovart",
    "d": "AI名片设计工具。智能生成商务名片、创意名片。支持多语言和数字名片格式。",
    "kw": ["AI名片设计", "商务名片制作", "在线名片工具"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI名片设计：第一印象从一张好名片开始",
    "hero_d": "名片是商务社交的起点。Lovart AI根据行业属性和个人风格设计有辨识度的商务名片。",
    "tag": "商务形象设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-business-card-design-online",
    "t": "在线名片制作 - 网页版名片设计工具 | Lovart",
    "d": "在线名片制作工具。打开浏览器就能设计名片。支持多人协作编辑，适合团队统一名片模板。",
    "kw": ["在线名片制作", "网页版名片设计", "名片模板编辑"],
    "tmpl": "landing-trial-now",
    "hero_t": "在线名片制作：团队名片统一管理的便捷方案",
    "hero_d": "团队成员的名片需要统一品牌规范。在线名片制作工具支持团队模板管理和批量编辑，确保名片风格一致。",
    "tag": "商务形象设计",
    "faq": DEFAULT_FAQ_SHORT,
})
PAGES.append({
    "slug": "zh-topic-business-card-design-free",
    "t": "免费名片模板 - 商务名片设计模板下载 | Lovart",
    "d": "免费名片模板库。涵盖商务、创意、极简、中式等多种风格。免费下载SVG和PDF格式。",
    "kw": ["免费名片模板", "名片设计模板", "商务名片下载"],
    "tmpl": "landing-trial-now",
    "hero_t": "免费名片模板：专业的商务名片设计参考",
    "hero_d": "不需要从零开始设计名片。免费名片模板库提供了丰富的行业分类模板，选择喜欢的风格直接自定义内容。",
    "tag": "商务形象设计",
    "faq": DEFAULT_FAQ_SHORT,
})

# ── D10 Brochure Design (3) ──
PAGES.append({
    "slug": "zh-topic-brochure-design",
    "t": "AI宣传册设计 - 企业画册产品手册制作 | Lovart",
    "d": "AI宣传册设计工具。适合企业画册、产品手册、招商手册。AI自动生成版式和图文搭配。",
    "kw": ["AI宣传册设计", "企业画册制作", "产品手册设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI宣传册设计：专业画册不再是大型企业专属",
    "hero_d": "宣传册是企业实力的纸质名片。Lovart AI根据企业画像和行业特性自动生成结构完整的宣传册版面。",
    "tag": "企业画册设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-brochure-design-corporate",
    "t": "企业画册设计 - 公司宣传册VI应用制作 | Lovart",
    "d": "企业画册设计工具。适用于企业形象宣传、产品目录、招商手册。融合VI系统规范。",
    "kw": ["企业画册设计", "公司宣传册制作", "VI画册设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "企业画册设计：用视觉语言讲好品牌故事",
    "hero_d": "企业画册是品牌形象的集中展示。Lovart AI将VI系统融入画册设计，确保每一页都符合品牌视觉规范。",
    "tag": "企业画册设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-brochure-design-trifold",
    "t": "三折页设计 - 企业宣传三折页制作 | Lovart",
    "d": "三折页设计工具。适合公司宣传、产品介绍、活动邀请。自动适配印刷出血和折页规范。",
    "kw": ["三折页设计", "企业宣传折页", "产品折页制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "三折页设计：折叠之间承载品牌全部信息",
    "hero_d": "三折页是性价比最高的宣传物料之一。Lovart AI按照阅读顺序设计封面、内页和封底的完整信息流。",
    "tag": "企业画册设计",
    "faq": DEFAULT_FAQ,
})

# ── D11 Illustration Design (3) ──
PAGES.append({
    "slug": "zh-topic-illustration-design",
    "t": "AI插画设计 - 智能插画生成工具 | Lovart",
    "d": "AI插画设计工具。根据描述自动生成各种风格的插画。适合绘本、广告、品牌形象等场景。",
    "kw": ["AI插画设计", "智能插画生成", "AI绘画创作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI插画设计：不会手绘也能创作专业插画",
    "hero_d": "插画创作门槛大幅降低。Lovart AI理解文字描述生成对应风格的插画作品，支持水彩、扁平、国潮等多种风格。",
    "tag": "AI插画创作",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-illustration-design-ai",
    "t": "AI生成插画 - 用文字描述创作专业插画 | Lovart",
    "d": "AI生成插画工具。输入关键词或描述语句，AI理解意图并生成符合需求的原创插画。商业可用。",
    "kw": ["AI生成插画", "文字生成插画", "AI插画创作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI生成插画：文字描述变原创插画的完整流程",
    "hero_d": "输入描述文本、选择风格和色板，Lovart AI生成多张符合需求的插画。支持多次迭代微调，直到满意为止。",
    "tag": "AI插画创作",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-illustration-design-commercial",
    "t": "商业插画设计 - 品牌营销插画制作 | Lovart",
    "d": "商业插画设计工具。适合品牌形象插画、营销海报插画、产品包装插画。商用授权保障。",
    "kw": ["商业插画设计", "品牌插画制作", "营销插画创作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "商业插画设计：品牌调性和创意的完美结合",
    "hero_d": "商业插画要兼顾品牌调性和艺术表现力。Lovart AI理解品牌指南后生成符合品牌风格的原创商业插画。",
    "tag": "商业插画设计",
    "faq": DEFAULT_FAQ,
})

# ── D12 Brand Visual Identity (3) ──
PAGES.append({
    "slug": "zh-topic-brand-visual-identity",
    "t": "AI品牌VI设计 - 品牌视觉识别系统 | Lovart",
    "d": "AI品牌VI设计工具。自动生成Logo、色彩系统、字体规范和品牌应用模板。一站式品牌建设。",
    "kw": ["AI品牌VI设计", "品牌视觉识别", "VI设计系统"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI品牌VI设计：从零开始搭建专业品牌视觉系统",
    "hero_d": "品牌VI是企业的视觉语言体系。Lovart AI从品牌战略出发，生成完整的Logo、色彩、字体和应用规范。",
    "tag": "品牌设计系统",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-brand-visual-identity-system",
    "t": "VI视觉识别系统 - 品牌形象设计规范 | Lovart",
    "d": "VI视觉识别系统设计工具。包括Logo规范、色彩管理、字体规范和应用延展。适合品牌升级。",
    "kw": ["VI视觉识别系统", "品牌形象规范", "视觉设计手册"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "VI视觉识别系统：品牌一致性的底层架构",
    "hero_d": "VI系统确保品牌在多渠道传播中保持一致性。Lovart AI生成包含基础规范和应用规范的完整VI体系。",
    "tag": "品牌设计系统",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-brand-visual-identity-upgrade",
    "t": "品牌视觉升级 - 品牌形象焕新设计 | Lovart",
    "d": "品牌视觉升级服务。AI辅助诊断现有品牌问题，提出视觉升级方案。适合品牌年轻化和转型。",
    "kw": ["品牌视觉升级", "品牌形象焕新", "品牌年轻化设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "品牌视觉升级：老品牌换新颜的正确方式",
    "hero_d": "品牌视觉升级不是推倒重来。Lovart AI分析现有品牌资产，在保留核心DNA的基础上做视觉优化和现代化改造。",
    "tag": "品牌设计系统",
    "faq": DEFAULT_FAQ,
})

# ── D13 Video Thumbnail (4) ──
PAGES.append({
    "slug": "zh-topic-video-thumbnail",
    "t": "AI视频封面设计 - 视频缩略图制作工具 | Lovart",
    "d": "AI视频封面设计工具。适合YouTube、B站、抖音等视频平台的封面缩略图。提升视频播放量。",
    "kw": ["AI视频封面设计", "视频缩略图制作", "视频封面工具"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI视频封面设计：决定视频命运的那张图",
    "hero_d": "视频封面是内容在搜索结果和推荐流中的展示窗口。Lovart AI根据视频内容生成高点击率的缩略图。",
    "tag": "视频封面设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-video-thumbnail-youtube",
    "t": "YouTube封面设计 - 提高视频点击率的缩略图 | Lovart",
    "d": "YouTube封面设计工具。适配YouTube平台规范。AI优化文字大小和视觉层次提升点击率。",
    "kw": ["YouTube封面设计", "视频缩略图制作", "YTB缩略图"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "YouTube封面设计：在海量视频中被选中的秘诀",
    "hero_d": "YouTube缩略图决定了观众是否点进你的视频。Lovart AI生成符合YouTube最佳实践的封面，优化文字可读性。",
    "tag": "视频封面设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-video-thumbnail-bilibili",
    "t": "B站封面设计 - 哔哩哔哩视频封面制作 | Lovart",
    "d": "B站封面设计工具。适配B站封面规范。风格偏二次元和创意设计，适合UP主使用。",
    "kw": ["B站封面设计", "哔哩哔哩视频封面", "UP主封面工具"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "B站封面设计：年轻化封面吸引Z世代观众",
    "hero_d": "B站UP主的封面需要兼顾创意和信息传递。Lovart AI生成符合B站社区风格的封面，帮助视频获得更多推荐。",
    "tag": "视频封面设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-video-thumbnail-douyin",
    "t": "抖音封面设计 - 短视频封面吸引点击的方法 | Lovart",
    "d": "抖音封面设计工具。适配抖音竖屏封面。适合带货视频、剧情号和知识分享类内容。",
    "kw": ["抖音封面设计", "短视频封面", "抖音视频缩略图"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "抖音封面设计：0.5秒决定用户是否观看",
    "hero_d": "抖音封面在推荐流中只有极短的展示时间。Lovart AI生成视觉冲击力强的竖屏封面，快速传递核心内容。",
    "tag": "视频封面设计",
    "faq": DEFAULT_FAQ,
})

# ── D14 Packaging Design (2) ──
PAGES.append({
    "slug": "zh-topic-packaging-design",
    "t": "AI包装设计 - 产品包装外观设计工具 | Lovart",
    "d": "AI包装设计工具。适合食品包装、化妆品包装、电子产品包装。AI生成多个包装方案供选择。",
    "kw": ["AI包装设计", "产品包装设计", "包装外观设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI包装设计：让产品在货架上自己说话",
    "hero_d": "包装是产品的无声销售员。Lovart AI分析产品卖点、目标客群和渠道特性，生成在货架上最具吸引力的包装方案。",
    "tag": "产品包装设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-packaging-design-product",
    "t": "产品包装设计 - 新品上市包装视觉方案 | Lovart",
    "d": "产品包装设计工具。适合新品上市、产品线扩展和老品包装升级。AI辅助完成包装结构设计。",
    "kw": ["产品包装设计", "新品包装制作", "包装视觉方案"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "产品包装设计：新品上市的第一张名片",
    "hero_d": "新品包装决定了消费者第一次接触时的品牌印象。Lovart AI生成与产品定位一致的包装视觉方案。",
    "tag": "产品包装设计",
    "faq": DEFAULT_FAQ,
})

# ── D15 Font Design (2) ──
PAGES.append({
    "slug": "zh-topic-font-design",
    "t": "AI字体设计 - 在线艺术字体生成器 | Lovart",
    "d": "AI字体设计工具。智能生成品牌定制字体和艺术标题字。支持中英文和多种字体风格。",
    "kw": ["AI字体设计", "在线字体生成", "艺术字体制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI字体设计：品牌专属字体的低成本方案",
    "hero_d": "定制字体是品牌识别度最高的视觉资产之一。Lovart AI根据品牌调性生成专属中英文字体方案。",
    "tag": "字体设计创作",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-font-design-chinese",
    "t": "中文艺术字设计 - AI毛笔字和创意字体 | Lovart",
    "d": "中文艺术字设计工具。支持毛笔字、书法字、创意标题字。适合海报标题和品牌Logo使用。",
    "kw": ["中文艺术字设计", "毛笔字在线生成", "创意字体设计"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "中文艺术字设计：汉字美学的数字化表达",
    "hero_d": "中文艺术字是汉字文化的视觉呈现。Lovart AI理解和运用汉字结构美学，生成富有文化韵味的中文艺术字。",
    "tag": "字体设计创作",
    "faq": DEFAULT_FAQ,
})

# ── D16 Infographic (1) ──
PAGES.append({
    "slug": "zh-topic-infographic-design",
    "t": "AI信息图表设计 - 数据可视化图表制作 | Lovart",
    "d": "AI信息图表设计工具。自动将数据转化为可视化图表，适合数据报告、行业分析和自媒体内容。",
    "kw": ["AI信息图表设计", "数据可视化制作", "信息图生成器"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI信息图表设计：复杂数据的可视化表达",
    "hero_d": "信息图表让复杂数据一目了然。Lovart AI理解数据结构和叙事逻辑，自动生成视觉层次清晰的信息图表。",
    "tag": "数据可视化设计",
    "faq": DEFAULT_FAQ,
})

# ── D17 Menu Design (2) ──
PAGES.append({
    "slug": "zh-topic-menu-design",
    "t": "AI菜单设计 - 餐厅菜单制作工具 | Lovart",
    "d": "AI菜单设计工具。适合餐厅、咖啡馆、奶茶店的菜单设计。AI推荐菜品排列和定价策略布局。",
    "kw": ["AI菜单设计", "餐厅菜单制作", "菜单模板工具"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI菜单设计：提升客单价的菜单排列秘密",
    "hero_d": "菜单设计直接影响顾客的点单决策。Lovart AI根据价格策略和菜品热度，设计引导顾客选择高利润菜品的菜单布局。",
    "tag": "餐饮视觉设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-menu-design-restaurant",
    "t": "餐厅菜单设计 - 餐饮门店菜单模板 | Lovart",
    "d": "餐厅菜单设计工具。适合正餐、快餐、火锅等各类餐饮业态。支持中英文双语菜单。",
    "kw": ["餐厅菜单设计", "餐饮菜单模板", "门店菜单制作"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "餐厅菜单设计：从菜品排列到视觉吸引的完整方案",
    "hero_d": "餐厅菜单是顾客体验的一部分。Lovart AI根据餐饮品类设计合理的菜品分类和视觉焦点分布。",
    "tag": "餐饮视觉设计",
    "faq": DEFAULT_FAQ,
})

# ── D18 Resume Design (2) ──
PAGES.append({
    "slug": "zh-topic-resume-design",
    "t": "AI简历设计 - 求职简历模板在线制作 | Lovart",
    "d": "AI简历设计工具。智能生成专业求职简历，支持多种行业风格。自动优化简历排版和内容结构。",
    "kw": ["AI简历设计", "求职简历模板", "简历制作工具"],
    "tmpl": "landing-gallery-detail",
    "hero_t": "AI简历设计：HR筛选中脱颖而出的简历设计法",
    "hero_d": "简历是第一轮面试的入场券。Lovart AI根据行业特点和岗位要求生成结构清晰、重点突出的专业简历。",
    "tag": "个人品牌设计",
    "faq": DEFAULT_FAQ,
})
PAGES.append({
    "slug": "zh-topic-resume-design-online",
    "t": "在线简历制作 - 网页版简历编辑器 | Lovart",
    "d": "在线简历制作工具。浏览器打开即用，多行业模板可选。支持PDF导出和一键投递。",
    "kw": ["在线简历制作", "网页版简历", "简历编辑器"],
    "tmpl": "landing-trial-now",
    "hero_t": "在线简历制作：随时随地更新求职简历",
    "hero_d": "在线简历制作工具让你随时随地对简历进行更新和调整。支持多种模板风格，适配不同行业求职场景。",
    "tag": "个人品牌设计",
    "faq": DEFAULT_FAQ_SHORT,
})

assert len(PAGES) == 60, f"Expected 60 pages, got {len(PAGES)}"


# ── Section builders ──────────────────────────────────────────────────────

def build_full_sections(p):
    tag = p.get("tag", "AI设计智能体")
    topic_noun = p["d"][:10]

    cluster_items = [
        {"title": "初创企业", "desc": "新品牌快速建立完整视觉体系", "tags": ["品牌创建"]},
        {"title": "电商卖家", "desc": "批量制作商品主图和促销素材", "tags": ["电商"]},
        {"title": "市场运营", "desc": "多平台社媒内容的日常输出", "tags": ["运营"]},
        {"title": "自媒体人", "desc": "个人品牌统一视觉形象打造", "tags": ["自媒体"]},
        {"title": "设计师", "desc": "用AI加速方案产出和客户沟通", "tags": ["设计师"]},
        {"title": "教育培训", "desc": "课件、宣传物料的一站式制作", "tags": ["教育"]},
    ]

    sections = [
        make_hero_gallery(p["hero_t"], p["hero_d"], tag=tag),
        make_bento(
            f"Lovart 在{topic_noun}中的价值",
            "AI设计智能体给你全新的工作方式",
            CARD_POOL[:6],
            "bento-6",
        ),
        make_capability_tabs(),
        make_tool_grid(topic_noun),
        make_bento(
            f"{topic_noun}的常见挑战与解决方案",
            "AI帮你绕过设计中的常见障碍",
            CARD_POOL[2:6],
            "bento-4",
        ),
        make_canvas_wall(topic_noun),
        make_workflow_horizontal(topic_noun, DEFAULT_WORKFLOW_STEPS),
        make_comparison_table(),
        make_cluster_block_dense(topic_noun, cluster_items),
        make_feature_detail(topic_noun),
        make_faq(p["faq"]),
        make_cta_default(topic_noun),
    ]
    return sections


def build_trial_sections(p):
    tag = p.get("tag", "AI设计智能体")
    topic_noun = p["d"][:10]

    sections = [
        make_hero_split(p["hero_t"], p["hero_d"], badge=tag),
        make_capability_tabs(),
        make_bento(
            f"{topic_noun}的核心优势",
            "为什么选择Lovart",
            CARD_POOL[:4],
            "bento-4",
        ),
        make_canvas_wall(topic_noun),
        make_workflow_horizontal(topic_noun, DEFAULT_WORKFLOW_STEPS),
        make_feature_detail(topic_noun),
        make_faq(p["faq"]),
        make_cta_default(topic_noun),
    ]
    return sections


# ── Main ──────────────────────────────────────────────────────────────────

def banned_check(text, slug):
    hits = []
    for b in BANNED:
        if b in text:
            hits.append(b)
    return hits


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    errors = []
    written = 0

    for p in PAGES:
        slug = p["slug"]
        if p["tmpl"] == "landing-gallery-detail":
            sections = build_full_sections(p)
        else:
            sections = build_trial_sections(p)

        body_json = json.dumps(sections, ensure_ascii=False)

        # banned phrase check
        hits = banned_check(body_json + p["t"] + p["d"] + " ".join(p["kw"]), slug)
        if hits:
            errors.append(f"BANNED in {slug}: {hits}")
            continue

        page = {
            "slug": slug,
            "language": "zh",
            "category": "topic",
            "schemaVersion": "composite-v2",
            "storylineTemplate": p["tmpl"],
            "title": p["t"],
            "description": p["d"],
            "bodyJson": body_json,
            "seo": {
                "title": p["t"],
                "description": p["d"],
                "keywords": p["kw"],
                "noIndex": False,
            },
        }

        fpath = os.path.join(OUT_DIR, f"{slug}.json")
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(page, f, indent=2, ensure_ascii=False)
            f.write("\n")
        written += 1

    print(f"Written: {written}")
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    print("All pages clean of banned phrases.")


if __name__ == "__main__":
    main()
