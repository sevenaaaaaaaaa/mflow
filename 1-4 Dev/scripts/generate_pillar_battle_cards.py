#!/usr/bin/env python3
"""
Auto-generate SERP evidence card + upgrade brief for all pillar_candidate articles.
Output: `1-2 Insight/Page Analytic/Lovart Blog 作战卡/{slug}.md` per article.
SERP analysis is initial/candidate-grade — flag `needs_serp_verify` for human validation.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(
    str(Path(__file__).resolve().parents[2])
)
QUEUE_JSON = ROOT / "tmp" / "blog-upgrade-queue-2026-07-13.json"
CARDS_DIR = ROOT / "1-2 Insight" / "Page Analytic" / "Lovart Blog 作战卡"
MANIFEST = CARDS_DIR / "MANIFEST.csv"

# ── Query derivation ──────────────────────────────────────────────

PREFIX_RE = re.compile(r"^\d{2}-(cluster-|industry-|pillar-)?")
REMOVE_SUFFIX = [
    "a practical lovart workflow guide",
    "2026 complete guide",
    "2026 guide",
    "review 2025",
    "review 2026",
]


def derive_queries(slug: str, title: str) -> tuple[str, list[str]]:
    raw = slug.replace("-", " ").strip()
    raw = PREFIX_RE.sub("", raw)
    for suffix in REMOVE_SUFFIX:
        raw = raw.replace(suffix, "").strip()
    main = raw.replace("  ", " ").strip()
    if not main or len(main) < 5:
        main = slug.replace("-", " ")
    secondary: list[str] = []
    words = main.split()
    # Skip leading number for secondary queries ("10 best" → "best")
    start = 1 if words and words[0].isdigit() else 0
    rest = words[start:]
    if len(words) >= 2:
        # Secondary: the core 2-3 word topic
        if rest:
            core = rest[0]
            if len(rest) >= 2:
                core = " ".join(rest[:2])
        else:
            core = words[0]
            if len(words) >= 3:
                core = " ".join(words[:2])
        if "review" in main or "alternative" in main or "alternatives" in main:
            secondary.append(f"{core} review")
            secondary.append(f"{core} alternative")
            secondary.append(f"best {core} 2026")
        elif "guide" in main or "complete" in main:
            secondary.append(f"{core} guide")
            secondary.append(f"{core} how to")
            secondary.append(f"{core} tutorial")
        elif "how" in main and "to" in main:
            secondary.append(f"{core} guide")
            secondary.append(f"{core} tutorial")
            secondary.append(f"{core} step by step")
        elif "best" in main:
            secondary.append(f"{core} review")
            secondary.append(f"{core} comparison")
            secondary.append(f"top {core} 2026")
        else:
            secondary.append(f"best {core}")
            secondary.append(f"{core} guide")
            secondary.append(f"{core} 2026")
    if len(secondary) == 0:
        secondary = [main]
    return main, secondary[:4]


# ── Target audience / role per writer type ────────────────────────

AUDIENCE_MAP: dict[str, str] = {
    "Review": "正在对比工具的创作者/营销团队，需要真实评测数据做购买决策",
    "How-To": "需要具体步骤完成某项设计任务的实操型读者",
    "Complete Guide": "想系统性了解某个领域的深度学习者或专业创作者",
    "Lovart 101": "刚接触 AI 设计或 Lovart 的新用户，需要入门指引",
    "Best Practice": "已有基础但想提升工作效率的中级用户",
    "Insight & Trend": "关注行业趋势的策略型读者或管理者",
}

CLUSTER_ROLE_MAP: dict[str, str] = {
    "AI Image": "支柱页 — AI Image 大类的通用需求入口，上接品牌设计，下接各工具对比",
    "AI Video": "支柱页 — AI Video 大类的选择框架入口",
    "Brand System": "支柱页 — Brand System 板块的方法论入口",
    "Character Consistency": "支柱页 — Character Consistency 板块的权威入口",
    "General Creative Workflow": "支柱页 — 作为品类通用入口，通过具体话题吸引泛流量再分流到子 cluster",
    "AI Design Agent": "支柱页 — 定义 AI Design Agent 品类认知的关键页",
    "Lovart Canvas": "支柱页 — Lovart Canvas 产品能力的内容载体",
}

# ── Common patterns / gaps by cluster ────────────────────────────

CLUSTER_ANALYSIS: dict[str, dict[str, str]] = {
    "AI Image": {
        "common": "SERP 主流文章走「评测 + 功能列表 + 定价 + vs 竞品」四段式；对工作流整合讲得很少；大部分是工具单点对比而非组合方案",
        "patterns": "评测类文章集中在 Top 5 工具（Midjourney/Canva/DALL-E/Firefly/Leonardo），对新兴工具和垂直场景覆盖不够",
        "gaps": "没有文章从「AI 图像在工作流中的角色」而非「AI 图像工具本身」出发；生成后的审校/修改/品牌一致性链是 SERP 空白",
        "angle": "把 AI 图像定位为「设计工作流中的产出一环」而非终点 —— Lovart 的 MCoT+ChatCanvas+Touch Edit 覆盖了所有工具都缺失的审校和修改层",
    },
    "AI Video": {
        "common": "SERP 以工具榜单为主（Zapier/BuildMVPFast/Pickaxe），排名核心维度是画质和速度；不讨论工作流集成和场景匹配",
        "patterns": "Veo 3.1 被默认 leader，但实际选型需要考虑场景匹配度（广告/品牌/社媒/短剧）而不仅是画质排名",
        "gaps": "没有文章从「视频生产管线」角度写 —— 从 brief → 生成 → 审校 → 修改 → 发布，各模型在每步的匹配度",
        "angle": "Lovart 不是又一个视频模型，而是视频资产的管线管理人 —— 在生成前做 Brief/Storyboard，生成后做 Review/Refine",
    },
    "Brand System": {
        "common": "趋势分析文和工具清单文各占一半；概念化强（AI 时代品牌怎么变），实操弱（到底怎么搭建品牌系统）",
        "patterns": "多数文章集中在「AI 品牌趋势」「AI 品牌工具」，没有人从「品牌规则 → 设计生成 → 跨渠道一致性」三层工作流写",
        "gaps": "Brand Kit 作为品牌规则的载体这个概念在 SERP 上几乎不存在",
        "angle": "Lovart Brand Kit 是品牌规则的执行引擎 —— 不是生成单个 LOGO，而是守住全部品牌输出的规则",
    },
    "Character Consistency": {
        "common": "character sheet + reference image + prompt lock 是主流三件套，几乎所有文章走这个结构",
        "patterns": "大量文章绑定插画/漫画场景，很少有人从品牌资产（品牌角色、IP 形象）角度写",
        "gaps": "从 production roll-out 角度写角色一致的几乎没有；video 场景下的角色一致缺乏覆盖",
        "angle": "角色一致性不是 prompt 技巧而是一个身份系统：Lovart Character Lock + MCoT + Touch Edit 构成完整管线",
    },
    "General Creative Workflow": {
        "common": "SERP 内容以泛讲和工具列表为主，对「用 AI 完成实际设计工作」的具体流程覆盖浅",
        "patterns": "大部分站外内容停留在概念层面（AI 能做什么），很少到执行层面（具体怎么做）",
        "gaps": "缺少从「设计工作流」而非「单点工具」角度指导读者的深度内容",
        "angle": "Lovart 定位在设计推理层而非生成层，这个差别是 SERP 上没人讲清楚的 — 用每个具体话题展示「推理 + 生成 + 修正」完整链条",
    },
    "AI Design Agent": {
        "common": "SERP 上的「AI design agent」结果还很杂乱，有定义文、有榜单、有工具页",
        "patterns": "品类定义不清晰：AI design agent 被泛化为 AI 设计工具，跟 AI image generator 混为一谈",
        "gaps": "Lovart 的「AI Design Agent = MCoT + ChatCanvas + Brand Kit」概念还没有 SERP 上的专门文章来定义",
        "angle": "定义这个品类：AI Design Agent 不是生成器，而是理解设计意图、推理设计方案、管理品牌规则的智能体",
    },
    "Lovart Canvas": {
        "common": "SERP 上关于 AI canvas/设计画布的内容主要是 Canva 模板和一般概念",
        "patterns": "没有人把「对话式画布」作为 AI 设计的交互范式来阐述",
        "gaps": "ChatCanvas 的设计推理 + 迭代 + 输出管线是独有概念",
        "angle": "画布作为设计推理的交互层——不只是布局工具，而是设计对话的空间",
    },
}

# ── Per-cluster SERP top 5 results (2026-07-15, DDG Lite) ────────

CLUSTER_SERP: dict[str, list[dict[str, str]]] = {
    "General Creative Workflow": [
        {"name": "Guideflow — 15 best AI design tools", "url": "https://www.guideflow.com/blog/ai-design-tools"},
        {"name": "Toolradar — Best AI Design Tools 2026 (Ranked)", "url": "https://toolradar.com/guides/best-ai-design-tools"},
        {"name": "Muz.li — 15 AI Design Tools That Actually Change How You Work", "url": "https://muz.li/blog/best-ai-design-tools-for-ui-ux-designers-in-2026/"},
        {"name": "AI Designer — Best AI UI Design Tools (2026 Tested)", "url": "https://www.aidesigner.ai/blog/best-ai-ui-design-tools"},
        {"name": "DesignRise — 10 Best AI Tools for Designers 2026", "url": "https://design-rise.com/10-ai-tools-every-designer-should-try-in-2026/"},
    ],
    "AI Video": [
        {"name": "LLM-Stats — Best AI for Video Generation (Blind Votes)", "url": "https://llm-stats.com/leaderboards/best-ai-for-video-generation"},
        {"name": "Perfect Corp — 23 Best AI Video Generators 2026", "url": "https://www.perfectcorp.com/consumer/blog/video-editing/best-ai-video-generators"},
        {"name": "AtlasCloud — Best AI Video Generation Models Comparison", "url": "https://www.atlascloud.ai/blog/guides/best-ai-video-generation-models-2026"},
        {"name": "Zapier — 16 best AI video generators 2026", "url": "https://zapier.com/blog/best-ai-video-generator/"},
        {"name": "Synthesia — 18 Best AI Video Generators 2026", "url": "https://www.synthesia.io/post/best-ai-video-generators"},
    ],
    "AI Image": [
        {"name": "PCMag — The Best AI Image Generators We've Tested 2026", "url": "https://www.pcmag.com/picks/the-best-ai-image-generators"},
        {"name": "AIComparison — 12 Tools Tested & Ranked", "url": "https://aicomparison.ai/best-ai-image-generators/"},
        {"name": "LLM-Stats — Best for Image Generation (Blind Votes)", "url": "https://llm-stats.com/leaderboards/best-ai-for-image-generation"},
        {"name": "BitsFromBytes — Free and Paid Options Ranked", "url": "https://bitsfrombytes.com/best-ai-image-generator-2026-tested/"},
        {"name": "AIToolsRecap — Best AI Image Generator Tools 2026", "url": "https://aitoolsrecap.com/Blog/best-ai-image-generators-2026"},
    ],
    "Brand System": [
        {"name": "DesignRush — Top 5 AI Branding Tools", "url": "https://www.designrush.com/agency/logo-branding/trends/ai-branding-tools"},
        {"name": "SpintaDigital — AI Visual Branding 2026", "url": "https://spintadigital.com/blog/ai-visual-branding-2026/"},
        {"name": "Ebaq Design — 10 Best AI Tools for Branding 2026", "url": "https://www.ebaqdesign.com/blog/ai-branding-tools"},
        {"name": "DesignShack — How Generative AI Is Redefining Brand Identity", "url": "https://designshack.net/articles/trends/generative-branding/"},
        {"name": "DigitalConvey — 10 Best AI Tools for Branding and Visual Identity", "url": "https://digitalconvey.com/ai-tools-for-branding-and-visual-identity/"},
    ],
    "Character Consistency": [
        {"name": "NeoLemon — Best AI Character Generator (2026)", "url": "https://www.neolemon.com/blog/best-ai-character-generator-for-consistent-characters/"},
        {"name": "AIConsistentCharacter — Best AI Tools for Character Consistency", "url": "https://www.aiconsistentcharacter.net/blog/best-ai-tools-for-character-consistency"},
        {"name": "ToonyStory — 7 Tools Tested on 140 Images", "url": "https://toonystory.com/blog/best-ai-for-character-consistency-2026"},
        {"name": "HiggsField — 7 Tools for Consistent AI Characters", "url": "https://higgsfield.ai/blog/tools-for-consistent-ai-characters"},
        {"name": "AIDemos — Best AI Character Consistency Tools (Tested)", "url": "https://aidemos.com/best/consistent-ai-characters"},
    ],
    "AI Design Agent": [
        {"name": "Lovart — World's First AI Design Agent", "url": "https://www.lovart.ai/"},
        {"name": "Superdesign — AI Product Design Agent", "url": "https://superdesign.dev/"},
        {"name": "DesignRush — 5 AI Design Agents", "url": "https://www.designrush.com/agency/graphic-design/trends/ai-design-agents"},
        {"name": "OpenDesign — Best AI Design Agents in 2026 (Tested)", "url": "https://open-design.ai/blog/ai-design-agents/"},
        {"name": "Figma — AI Design Agent native to the canvas", "url": "https://www.figma.com/solutions/ai-design-agent/"},
    ],
    "Lovart Canvas": [
        {"name": "占位 — 此类查询极少，暂时参考 General Creative Workflow", "url": ""},
    ],
}

# ── Must-add modules by writer type ───────────────────────────────

MODULES_MAP: dict[str, list[str]] = {
    "Review": [
        "实测矩阵：同一 prompt 在 3-5 个工具/设置下的输出对比",
        "决策框架：什么场景选工具 A vs 工具 B vs Lovart",
        "ROI 分析：免费层 → 付费层的时间/成本/产出权衡",
        "30 天评估 plan",
        "反推荐：什么时候不适合用该工具",
    ],
    "How-To": [
        "四步或多步工作流（分场景类型）",
        "可复用的 prompt 模板/框架",
        "不同难度的多档方案（入门/进阶/批量）",
        "常见错误与修复",
        "30 天养成 plan",
    ],
    "Complete Guide": [
        "Framework / 决策框架",
        "场景分类 + 各场景方法",
        "实测 walkthrough",
        "反推荐 / When This Is Not The Right Fit",
        "30 天 Rollout Plan",
        "Pre-Publish Checklist",
    ],
    "Lovart 101": [
        "核心概念区分（设计推理 vs 生成）",
        "Lovart 核心功能串讲（MCoT/ChatCanvas/Touch Edit/Brand Kit）",
        "最快上手路径",
        "常见新手坑",
    ],
    "Best Practice": [
        "核心原则提炼（3-5 条）",
        "每种实践的适用 / 不适用场景",
        "Lovart 各功能的最佳组合方式",
        "效果衡量方法",
    ],
    "Insight & Trend": [
        "数据/市场趋势引用",
        "Lovart 在趋势中的位置",
        "不同读者（creator/manager/investor）的 takeaway",
        "下一步建议",
    ],
}

# ── Success criteria patterns ─────────────────────────────────────

SUCCESS_CRITERIA = (
    "不再只是 Phase 1 template 的结构填充，而是属于该话题的独特内容；"
    "读者读完能带走一个可执行的判断或操作框架；"
    "集群角色清晰，能自然引导读者到 cluster 内其他相关页"
)


# ── Build card text ───────────────────────────────────────────────

def build_card(c: dict[str, Any]) -> str:
    slug: str = c["slug"]
    title: str = c.get("title", "")
    writer: str = c.get("writer_type", "How-To")
    cluster: str = c.get("content_cluster", "General Creative Workflow")
    skill: str = c.get("target_skill", "lovart-blog-signal-writer")
    chars: int = c.get("chars", 0)
    impr: float = c.get("impressions_28d", 0)
    clicks: float = c.get("clicks_28d", 0)
    pos = c.get("position_28d")
    pos_str = f"{pos}" if pos else "暂无"
    depth: str = c.get("recommended_depth", "")
    rationale: str = c.get("rationale", "")
    current: str = c.get("current_state", "signal_refresh_complete")

    main_query, secondary = derive_queries(slug, title)
    cluster_info = CLUSTER_ANALYSIS.get(cluster, CLUSTER_ANALYSIS["General Creative Workflow"])
    serp_results = CLUSTER_SERP.get(cluster, CLUSTER_SERP["General Creative Workflow"])
    serp_lines = "\n".join(
        f"{i}. **{r['name']}** — {r['url']}"
        for i, r in enumerate(serp_results[:5], 1)
    )

    audience = AUDIENCE_MAP.get(writer, "AI 设计工具的使用者和潜在购买者")
    cluster_role = CLUSTER_ROLE_MAP.get(cluster, "支柱页 — 作为品类入口")
    modules = MODULES_MAP.get(writer, MODULES_MAP["How-To"])

    return f"""---
slug: {slug}
card_type: battle_card
status: draft-auto
date: 2026-07-15
---

# 作战卡：{slug}

## SERP 证据卡

**主 query：** {main_query}
**次级 query：** {" / ".join(secondary)}

**当前 GSC 信号（最近 28d）：** 曝光 {int(impr):,} / 点击 {int(clicks):,} / 排名 {pos_str}

**SERP 前排 3-5 结果（品类通用，DDG Lite 2026-07-15）：**

{serp_lines}

**共同套路（基于品类 SERP 分析）：**
{cluster_info['common']}
{cluster_info['patterns']}

**缺口（还没讲透的）：**
{cluster_info['gaps']}

**Lovart 最有机会切入的角度：**
{cluster_info['angle']}

---

## 升级 brief

**文章类型 / 目标 sub-skill：** {writer} → {skill}

**目标读者：**
{audience}

**cluster 角色：**
{cluster_role}

**当前状态：**
Phase 1 {current}。字符 {chars:,}。

**当前版本的问题（模板级，待人工确认）：**
- Phase 1 template 填充感明显，缺少属于该话题的独特判断框架
- 对 {main_query} 的真实搜索意图覆盖不深
- FAQ 不足（当前 ≤1 组），需要扩到 ≥3-5 组
- Internal Links 仅 1-3 条通用链，缺少 cluster 相关内链
- 尚未按 writer type 补齐该类型应有的必补模块

**必补模块（Round 3 Deep Rewrite 的交付物）：**
{chr(10).join(f'- {m}' for m in modules)}

**升级后成功标准：**
{SUCCESS_CRITERIA}。
"""


# ── Manifest helpers ──────────────────────────────────────────────

def load_manifest() -> list[dict[str, str]]:
    if not MANIFEST.exists():
        return []
    with MANIFEST.open() as fh:
        lines = [l.strip() for l in fh if l.strip()]
        if not lines:
            return []
        headers = lines[0].split(",")
        return [dict(zip(headers, l.split(","))) for l in lines[1:]]


def save_manifest(rows: list[dict[str, str]]) -> None:
    headers = ["slug", "upgrade_label", "tier", "card_evidence", "card_brief",
               "body_deep_rewrite", "cluster", "qa_i18n"]
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(row.get(h, "") for h in headers))
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_manifest(pillars: list[dict[str, Any]], existing: list[dict[str, str]]) -> None:
    existing_slugs = {r["slug"] for r in existing}
    for p in pillars:
        slug = p["slug"]
        if slug not in existing_slugs:
            existing.append({
                "slug": slug,
                "upgrade_label": p.get("upgrade_label", ""),
                "tier": p.get("tier", ""),
                "card_evidence": "ready-auto",
                "card_brief": "ready-auto",
                "body_deep_rewrite": "pending",
                "cluster": "pending",
                "qa_i18n": "pending",
            })


# ── Main ──────────────────────────────────────────────────────────

def main() -> None:
    data = json.loads(QUEUE_JSON.read_text(encoding="utf-8"))
    candidates: list[dict[str, Any]] = data.get("candidates", data if isinstance(data, list) else [])
    pillars_raw = [c for c in candidates if c.get("upgrade_label") == "pillar_candidate"]
    seen: set[str] = set()
    pillars: list[dict[str, Any]] = []
    for c in pillars_raw:
        s = c.get("slug", "")
        if s not in seen:
            seen.add(s)
            pillars.append(c)

    print(f"Pillar candidates: {len(pillars)}")
    by_type = Counter(c.get("writer_type", "?") for c in pillars)
    print(f"By writer_type: {dict(by_type)}")

    CARDS_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing manifest (preserve manually written cards)
    existing = load_manifest()
    existing_slugs = {r["slug"] for r in existing}

    written = 0
    skipped = 0
    for c in pillars:
        slug = c["slug"]
        target = CARDS_DIR / f"{slug}.md"
        if slug in existing_slugs and target.exists():
            print(f"  SKIP (already exists) {slug}")
            skipped += 1
            continue
        content = build_card(c)
        target.write_text(content.strip() + "\n", encoding="utf-8")
        written += 1
        print(f"  WRITE {slug}")

    # Update manifest
    update_manifest(pillars, existing)
    save_manifest(existing)

    print(f"\nDone: {written} written, {skipped} skipped (existing). Total manifest entries: {len(existing)}")


if __name__ == "__main__":
    main()
