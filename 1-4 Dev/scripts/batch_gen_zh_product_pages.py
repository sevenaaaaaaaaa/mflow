#!/usr/bin/env python3
"""Generate 36 Chinese product landing page JSONs (composite-v2)."""

import json
import os

OG_FALLBACK = (
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/"
    "d3e44c9edfb1a44f386973e9b3c23fcffddc8008.png"
)

FULL_SECTIONS = ["hero-cinematic", "bento-4", "capability-tabs", "tool-grid",
    "workflow-vertical", "comparison-table", "cluster-block-dense",
    "showcase-stacked", "testimonial", "pricing-block", "faq", "cta-default"]

VARIANT_SECTIONS = ["hero-cinematic", "bento-4", "workflow-vertical",
    "showcase-stacked", "comparison-table", "faq", "cta-default"]

# ── Section builders ──────────────────────────────────────────────

def sec_hero(title, description, pn):
    return {
        "type": "hero-cinematic", "tag": "AI设计产品",
        "title": title, "highlightedText": "", "description": description,
        "buttons": [
            {"text": "免费试用", "href": "https://lovart.ai/signup", "variant": "primary"},
            {"text": "了解更多", "href": "", "variant": "secondary"},
        ],
        "media": {"src": OG_FALLBACK, "alt": pn},
    }

def sec_bento4(cards):
    return {"type": "bento-4", "title": "核心能力", "description": "四大核心优势", "cards": cards}

def sec_capability_tabs(pn, tabs):
    return {"type": "capability-tabs", "title": "技术能力", "description": f"{pn} 的核心技术支撑", "tabs": tabs}

def sec_tool_grid(pn, tools):
    return {"type": "tool-grid", "title": "功能矩阵", "description": f"{pn} 的全部能力", "tools": tools}

def sec_workflow(pn, steps):
    return {"type": "workflow-vertical", "title": "使用流程", "description": f"三步完成{pn}", "steps": steps}

def sec_comparison(headers, rows):
    return {"type": "comparison-table", "title": "对比传统方式", "description": "与传统工作流对比",
        "headers": headers, "rows": rows}

def sec_cluster(pn, items):
    return {"type": "cluster-block-dense", "title": "适用场景", "description": f"{pn} 的最佳使用场景", "items": items}

def sec_showcase(showcases):
    return {"type": "showcase-stacked", "title": "应用案例", "description": "实际应用场景", "showcases": showcases}

def sec_testimonial():
    return {
        "type": "testimonial", "title": "用户评价", "description": "来自真实用户的体验分享",
        "testimonials": [
            {"content": "用了Lovart之后，每月设计成本从3万降到3千，产出翻了三倍。最关键是品牌一致性比以前找外包还要稳定。", "author": "陈明辉", "role": "某消费品牌市场总监", "avatar": ""},
            {"content": "一个人运营三个社媒账号，以前每天花两小时做图。Lovart说一句出十版让我挑，五分钟搞定一天的素材。", "author": "林小艺", "role": "30万粉丝科技博主", "avatar": ""},
            {"content": "我们团队试过市面上所有AI设计工具，Lovart是唯一真正理解设计流程的平台。Brand Kit加ChatCanvas的组合解决了团队协作的核心问题。", "author": "张一鸣", "role": "创意设计机构创始人", "avatar": ""},
        ],
    }

def sec_pricing():
    return {
        "type": "pricing-block", "title": "选择适合你的方案", "description": "从免费版到专业版，按需选择",
        "plans": [
            {"name": "免费版", "price": "$0", "features": ["每日免费生成额度", "基础风格模板", "标准分辨率输出", "社区支持"], "cta": "免费开始"},
            {"name": "Starter", "price": "$15/月", "features": ["更多生成额度", "高清输出", "品牌管理套件", "邮件支持"], "cta": "选择Starter"},
            {"name": "Pro", "price": "$72/月", "features": ["无限生成", "4K/8K输出", "团队协作", "优先支持"], "cta": "选择Pro"},
        ],
    }

def sec_faq(items):
    return {"type": "faq", "title": "常见问题", "items": items}

def sec_cta(pn, desc=None):
    return {
        "type": "cta-default",
        "title": f"开始使用{pn}",
        "description": desc or "无需信用卡。免费额度让您亲身体验Lovart的设计能力。",
        "buttons": [{"text": "免费试用", "href": "https://lovart.ai/signup", "variant": "primary"}],
    }

# ── Build one product ─────────────────────────────────────────────

def build_page(p):
    is_variant = p.get("variant", False)
    pn = p["pn"]
    sections = [sec_hero(p["t"], p["d"], pn)]
    sections.append(sec_bento4(p["bento"]))
    if not is_variant:
        sections.append(sec_capability_tabs(pn, p.get("tabs", [])))
        sections.append(sec_tool_grid(pn, p.get("tools", [])))
    sections.append(sec_workflow(pn, p.get("steps", [])))
    if not is_variant:
        sections.append(sec_cluster(pn, p.get("clusters", [])))
    sections.append(sec_showcase(p.get("showcases", [])))
    sections.append(sec_comparison(p.get("comp_h", []), p.get("comp_r", [])))
    if not is_variant:
        sections.append(sec_testimonial())
        sections.append(sec_pricing())
    sections.append(sec_faq(p.get("faqs", [])))
    sections.append(sec_cta(pn))

    return {
        "slug": p["slug"],
        "language": "zh",
        "category": "product",
        "schemaVersion": "composite-v2",
        "storyline": "product-标准",
        "title": p["t"],
        "description": p["d"],
        "bodyJson": json.dumps(sections, ensure_ascii=False),
        "seo": {
            "title": p["st"],
            "description": p["sd"],
            "keywords": p["kw"],
            "noIndex": False,
            "ogImage": {"url": OG_FALLBACK, "alt": p["pn"]},
        },
    }

# ── Main ──────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "zh_product_data.json")
    out_dir = os.path.join(script_dir,
        "../../1-3 GenFlow/Page Gen/Pages/Products/zh/")
    out_dir = os.path.normpath(out_dir)

    with open(data_path) as f:
        products = json.load(f)

    os.makedirs(out_dir, exist_ok=True)

    count = 0
    errors = []
    for p in products:
        try:
            page = build_page(p)
            fname = f"{p['slug']}.json"
            fpath = os.path.join(out_dir, fname)
            with open(fpath, "w") as f:
                json.dump(page, f, ensure_ascii=False, indent=2)
            count += 1
        except Exception as e:
            errors.append(f"{p['slug']}: {e}")

    print(f"Generated {count}/{len(products)} files -> {out_dir}")
    if errors:
        print("Errors:")
        for e in errors:
            print(f"  {e}")

if __name__ == "__main__":
    main()
