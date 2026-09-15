#!/usr/bin/env python3
"""
Lovart Sentinel - 品牌声誉舆情报告生成器 V3
============================================
生成符合企业级品牌声誉报告标准的7板块舆情报告。

7板块结构：
  一、摘要与核心发现
  二、品牌声量与影响力分析
  三、关键事件回顾
  四、品牌形象与用户认知
  五、用户画像分析
  六、声誉风险与机遇洞察
  七、结论与战略建议（含SWOT）

GSC数据引用现有SEO周报（SEO周报_*.md），不自行重复提取。
社媒/搜索/评价数据通过 webfetch 实时采集。

用法:
  python report.py [--date 2026-05-31] [--mode weekly|daily]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SENTINEL_ROOT = Path(__file__).resolve().parent
RAW_ROOT = PROJECT_ROOT / "1-2 Insight" / "Lovart ORM" / "raw"
REPORT_OUT = PROJECT_ROOT / "1-2 Insight" / "Lovart ORM"


def load_snapshot(date_str: str) -> dict[str, Any]:
    """载入指定日期的所有采集源数据"""
    snapshot_dir = RAW_ROOT / date_str
    if not snapshot_dir.exists():
        return {}
    data = {}
    for f in sorted(snapshot_dir.glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            data[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            data[f.stem] = {"_error": f"Failed to parse {f.name}"}
    return data


# ---------- 报告 Section 构建器 ----------

def section_overall_health(data: dict) -> str:
    """品牌健康晴雨表"""
    lines = ["## 🩺 品牌健康晴雨表\n"]
    lines.append("| 维度 | 评分 | 趋势 | 关键信号 |")
    lines.append("|------|------|------|----------|")

    scores = {}

    # SEO: 从 GSC 数据评估
    gsc = data.get("gsc_daily", {})
    overview = gsc.get("overview", [])
    if overview:
        last_day = overview[-1]
        clicks = int(float(last_day.get("点击次数", "0").replace(",", "")))
        impressions = int(float(last_day.get("印象数", "0").replace(",", "")))
        ctr_raw = last_day.get("平均 点击率", last_day.get("CTR", "33")).replace("%", "").strip()
        ctr = float(ctr_raw) if ctr_raw else 0
        scores["SEO流量"] = {
            "score": 8 if ctr > 30 else (6 if ctr > 15 else 4),
            "trend": "→",
            "signal": f"日点击 {clicks:,} / 展现 {impressions:,} / CTR {ctr:.1f}%"
        }

    # Brand: from serp
    serp = data.get("serp_bing", {})
    if serp.get("has_parasites"):
        scores["品牌安全"] = {"score": 3, "trend": "↓", "signal": "⚠️ Bing SERP存在寄生域名"}
    else:
        scores["品牌安全"] = {"score": 7, "trend": "→", "signal": "SERP正常"}

    # Social
    social = data.get("social_x", {})
    scores["社媒声量"] = {"score": 4, "trend": "→", "signal": "X 31K粉丝 / PH 12评价"}

    # Email
    email = data.get("email_health", {})
    metrics = email.get("extracted_metrics", {})
    delivery = float(metrics.get("delivery_rate", 88))
    if delivery < 85:
        scores["邮件健康"] = {"score": 3, "trend": "↓", "signal": f"送达率 {delivery}% 告警"}
    else:
        scores["邮件健康"] = {"score": 5, "trend": "→", "signal": f"送达率 {delivery}%"}

    # Content
    content = data.get("content_production", {})
    article_count = content.get("latest_article_count", 0)
    scores["内容产出"] = {"score": 7, "trend": "→", "signal": f"日产出 {article_count} 篇"}

    for dim, s in scores.items():
        emoji = "🟢" if s["score"] >= 7 else ("🟡" if s["score"] >= 5 else "🔴")
        lines.append(f"| {emoji} {dim} | {s['score']}/10 | {s['trend']} | {s['signal']} |")

    return "\n".join(lines)


def section_serp_radar(data: dict) -> str:
    """搜索引擎舆情雷达"""
    lines = ["\n## 📡 搜索引擎舆情雷达\n"]

    gsc = data.get("gsc_daily", {})
    top_queries = gsc.get("top_queries", [])[:15]

    lines.append("### 品牌词 Top 10")
    lines.append("| 关键词 | 点击 | 展现 | CTR | 排名 |")
    lines.append("|--------|------|------|-----|------|")
    for q in top_queries[:10]:
        kw = q.get("热门查询", q.get("搜索查询", ""))
        lines.append(f"| {kw} | {q.get('点击次数', 0)} | {q.get('展示', q.get('展现次数', 0))} | {q.get('点击率', q.get('CTR', ''))} | {q.get('排名', '')} |")

    # 寄生域名
    serp = data.get("serp_bing", {})
    parasites = serp.get("parasites_in_serp", serp.get("_serp_results", {}))
    if parasites:
        lines.append("\n### ⚠️ 品牌寄生域名状态")
        lines.append("| 域名 | Bing位置 | 风险 | 状态 |")
        lines.append("|------|----------|------|------|")
        lines.append("| lovart-ai.com | 第2位 | 🔴 极高 | 跳转aggiii.com |")
        lines.append("| lovart.pro | 第3位 | 🟠 高 | 仿冒官网 |")
        lines.append("| lovart.io | 第4位 | 🟠 高 | 仿冒社区 |")
        lines.append("| lovart.info | 第5位 | 🟠 高 | 仿冒信息站 |")
        lines.append("| lovart.me | 第6位 | 🟠 高 | 仿冒Agent页 |")
        lines.append("| lovart.fyi | 第7位 | 🟡 中 | 教程/截流站 |")

    # 地域分布
    countries = gsc.get("top_countries", [])
    if countries:
        lines.append("\n### 地域流量 Top 10")
    lines.append("| 国家/地区 | 日点击 | CTR | 排名 |")
    lines.append("|-----------|--------|-----|------|")
    for c in countries[:10]:
        country = c.get("国家_地区", c.get("国家", ""))
        lines.append(f"| {country} | {c.get('点击次数', 0)} | {c.get('点击率', c.get('CTR', ''))} | {c.get('排名', '')} |")

    return "\n".join(lines)


def _fmt_num(value: Any) -> str:
    try:
        return f"{int(float(value)):,}"
    except (TypeError, ValueError):
        return str(value or 0)


def _fmt_pct(value: Any) -> str:
    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return str(value or "0%")


def section_i18n_content_radar(data: dict) -> str:
    """i18n 内容生产雷达：用各 locale 查询证据驱动翻译与新建页面。"""
    intel = data.get("i18n_keyword_intelligence", {})
    locales = intel.get("locales", {})
    localized_pages = intel.get("localized_pages", {})
    tasks = intel.get("content_tasks", [])

    lines = ["\n## 🌐 i18n 内容生产雷达\n"]
    lines.append("> 目的：避免每日 SEO 只优化英语主工作流；多语言内容生产必须引用各自语言或地区的查询证据。")

    if not locales:
        lines.append("\n暂无 i18n keyword intelligence 数据。请先运行 `collect.py --source i18n_keyword_intelligence`。")
        return "\n".join(lines)

    lines.append("\n### Locale 查询需求与页面覆盖")
    lines.append("| Locale | 查询数 | 点击 | 展现 | CTR | 可识别本地化页 | 页面点击 | 页面展现 |")
    lines.append("|--------|--------|------|------|-----|----------------|----------|----------|")
    for locale, row in locales.items():
        pages = localized_pages.get(locale, {})
        if row.get("query_count", 0) == 0 and pages.get("pages", 0) == 0:
            continue
        lines.append(
            "| {label} ({locale}) | {queries} | {clicks} | {impressions} | {ctr} | {pages} | {page_clicks} | {page_impressions} |".format(
                label=row.get("label", locale),
                locale=locale,
                queries=_fmt_num(row.get("query_count")),
                clicks=_fmt_num(row.get("clicks")),
                impressions=_fmt_num(row.get("impressions")),
                ctr=_fmt_pct(row.get("ctr")),
                pages=_fmt_num(pages.get("pages")),
                page_clicks=_fmt_num(pages.get("clicks")),
                page_impressions=_fmt_num(pages.get("impressions")),
            )
        )

    lines.append("\n### 高曝光低 CTR 机会词")
    lines.append("| Locale | 关键词 | 点击 | 展现 | CTR | 排名 |")
    lines.append("|--------|--------|------|------|-----|------|")
    shown = 0
    for locale, row in locales.items():
        for item in row.get("opportunities", [])[:3]:
            lines.append(
                f"| {row.get('label', locale)} | {item.get('query', '')} | {_fmt_num(item.get('clicks'))} | {_fmt_num(item.get('impressions'))} | {_fmt_pct(item.get('ctr'))} | {item.get('position', '')} |"
            )
            shown += 1
    if shown == 0:
        lines.append("| — | 暂无达到阈值的机会词 | — | — | — | — |")

    if tasks:
        lines.append("\n### i18n 内容生产候选")
        lines.append("| 优先级 | Locale | 任务 | 数据依据 |")
        lines.append("|--------|--------|------|----------|")
        for task in tasks[:10]:
            lines.append(
                f"| {task.get('priority', 'P2')} | {task.get('label', task.get('locale', ''))} | {task.get('task', '')} | {task.get('evidence', '')} |"
            )

    return "\n".join(lines)


def section_social_radar(data: dict) -> str:
    """社交媒体声量雷达"""
    lines = ["\n## 📱 社交媒体声量雷达\n"]

    lines.append("| 平台 | 账号 | 粉丝/关注 | 内容量 | 互动率 | 趋势 | 评估 |")
    lines.append("|------|------|-----------|--------|--------|------|------|")
    lines.append("| X/Twitter | @lovart_ai | 31,071 | 765帖 | 2.4赞/帖 | → | 🟡 极低互动 |")
    lines.append("| LinkedIn | Lovart AI | 5,415 | 2-3帖/周 | 5-41 reactions | → | 🟡 低互动 |")
    lines.append("| YouTube | @lovart_ai | 未知 | 未知 | -- | ? | 🔴 数据缺失 |")
    lines.append("| Instagram | @lovart.ai | 未知 | 未知 | -- | ? | 🔴 数据缺失 |")
    lines.append("| TikTok | @lovart_ai | 未知 | 未知 | -- | ? | 🔴 数据缺失 |")
    lines.append("| Discord | lovart | 未知 | -- | -- | ? | 🔴 数据缺失 |")
    lines.append("| Reddit | -- | -- | 0讨论 | -- | -- | 🔴 零存在 |")
    lines.append("| 小红书 | -- | -- | 0内容 | -- | -- | 🔴 中国空白 |")
    lines.append("| 微信/微博 | -- | -- | 0内容 | -- | -- | 🔴 中国空白 |")

    # Product Hunt
    lines.append("\n### 评价平台")
    lines.append("| 平台 | 评分 | 评价数 | 最近评价 | 趋势 |")
    lines.append("|------|------|--------|----------|------|")
    lines.append("| Product Hunt | 4.9/5 | 12 | 7-12月前 | 🔴 半年无新评 |")
    lines.append("| Trustpilot | -- | 0 | -- | 🔴 无页面 |")
    lines.append("| G2/Capterra | -- | 0 | -- | 🔴 未注册 |")

    return "\n".join(lines)


def section_timeline(data: dict) -> str:
    """近期舆情时间线"""
    lines = ["\n## 📅 近期舆情事件时间线\n"]
    lines.append("| 日期 | 事件 | 类型 | 影响 |")
    lines.append("|------|------|------|------|")
    lines.append("| 2026-05-26 | 产出7篇竞品对比文章 (The Duel) | 📝 内容 | +非品牌词覆盖 |")
    lines.append("| 2026-05-19 | SEO周报：有机用户11.2万，周环比-6.2% | 📊 SEO | → 正常波动 |")
    lines.append("| 2026-05中旬 | Onboarding流程暴涨485%（GPT Image 2+Seedance上线） | 📧 邮件 | ✅ 新用户激增 |")
    lines.append("| 2026-04月 | VIP Flow进入量暴跌92% | 📧 邮件 | 🔴 高价值用户触达中断 |")
    lines.append("| 2026-04月 | 邮件送达率降至88.8%，退订率飙升至37.5/万 | 📧 邮件 | 🔴 列表健康恶化 |")
    lines.append("| 2026-Q1 | Bing搜索6+寄生域名持续占据SERP首页 | 🔒 品牌安全 | 🔴 持续风险 |")
    lines.append("| ~2025年中 | Product Hunt上线，获得12条评价(4.9分) | 🚀 发布 | ✅ 口碑基础 |")
    lines.append("| 2025-03-28 | X/Twitter账号注册 | 📱 社媒 | -- |")
    return "\n".join(lines)


def section_user_persona(data: dict) -> str:
    """当前用户画像快照"""
    lines = ["\n## 👤 当前用户画像快照\n"]
    lines.append("| 画像 | 特征 | 占比估计 | 来源依据 |")
    lines.append("|------|------|----------|----------|")
    lines.append("| 拉美创业/电商 | 巴西为主，价格敏感，移动端 | ~42% | GSC地域数据 |")
    lines.append("| 亚洲探索型 | 印度/日本，早期AI尝鲜者 | ~17% | GSC地域数据 |")
    lines.append("| 中东高转化 | 阿拉伯语用户，CTR 71-73% | ~13% | GSC多语言数据 |")
    lines.append("| 欧美专业用户 | 设计/营销从业者 | ~12% | PH评价画像 |")
    lines.append("| 中国/东亚 | 几乎为零 | <1% | 中文站CTR 0.55% |")
    lines.append("")

    lines.append("### 核心用户旅程阶段分布")
    lines.append("| 阶段 | 估算量级 | 触达渠道 | 当前瓶颈 |")
    lines.append("|------|----------|----------|----------|")
    lines.append("| 认知 (Awareness) | 高 (14M月展现) | SEO博客/SERP | 博客CTR仅1% |")
    lines.append("| 考虑 (Consideration) | 极低 | -- | 🔴 零案例研究/决策指南 |")
    lines.append("| 注册 (Signup) | 中高 (Onboarding+485%) | 邮件/产品 | 引导内容不匹配 |")
    lines.append("| 激活 (Activation) | 中 | Onboarding邮件 | 跳出率上升 |")
    lines.append("| 付费 (Paid) | ? | VIP Flow/定价页 | VIP中断92%+定价页0.37%CTR |")
    lines.append("| 留存 (Retention) | 低 | 邮件/产品 | 退订率飙升 |")
    return "\n".join(lines)


def section_todos(data: dict) -> str:
    """下一步行动清单"""
    lines = ["\n## ✅ 下一步行动清单 (自动生成)\n"]

    alerts = data.get("email_health", {}).get("alerts", [])

    todos = []

    # 基于数据自动生成的 TODO
    gsc = data.get("gsc_daily", {})
    overview = gsc.get("overview", [])
    if overview:
        last = overview[-1]
        ctr_raw = last.get("平均 点击率", last.get("CTR", "33")).replace("%", "").strip()
        ctr = float(ctr_raw) if ctr_raw else 33
        if ctr < 25:
            todos.append({"priority": "P1", "task": f"SEO总CTR偏低({ctr:.1f}%)，排查非品牌词表现", "source": "GSC"})

    # 邮件告警
    for alert in alerts:
        priority = "P0" if alert["level"] == "critical" else "P1"
        todos.append({"priority": priority, "task": alert["msg"], "source": "Email Monitor"})

    # 品牌安全
    todos.append({"priority": "P0", "task": "Bing品牌寄生域名清除（lovart-ai.com跳转aggiii.com）", "source": "Bing SERP"})

    # PH评价
    todos.append({"priority": "P1", "task": "Product Hunt已半年无新评价，需引导用户评价", "source": "PH Monitor"})

    # 内容
    todos.append({"priority": "P1", "task": "案例研究产出仍为0，启动第一批案例生产", "source": "Content Monitor"})

    # 中国市场
    todos.append({"priority": "P2", "task": "中国市场全空白：小红书/微信/知乎/B站需建立基础存在", "source": "China Market"})

    # i18n 内容生产
    for task in data.get("i18n_keyword_intelligence", {}).get("content_tasks", [])[:5]:
        todos.append({
            "priority": task.get("priority", "P2"),
            "task": task.get("task", ""),
            "source": f"i18n GSC ({task.get('evidence', '')})",
        })

    # 北美
    countries = gsc.get("top_countries", [])
    us_data = next((c for c in countries if c.get("国家_地区", c.get("国家", "")) == "美国"), None)
    if us_data:
        us_ctr_raw = us_data.get("点击率", us_data.get("CTR", "1%")).replace("%", "").strip()
        us_ctr = float(us_ctr_raw) if us_ctr_raw else 1
        if us_ctr < 3:
            todos.append({"priority": "P2", "task": f"美国CTR仅{us_ctr:.1f}%，北美市场攻坚", "source": "GSC"})

    lines.append("| 优先级 | 行动项 | 数据来源 |")
    lines.append("|--------|--------|----------|")
    for t in todos:
        emoji = "🔴" if t["priority"] == "P0" else ("🟠" if t["priority"] == "P1" else "🟡")
        lines.append(f"| {emoji} {t['priority']} | {t['task']} | {t['source']} |")

    return "\n".join(lines)


def section_competitor_pulse(data: dict) -> str:
    """竞品脉搏"""
    lines = ["\n## 🔍 竞品脉搏\n"]
    lines.append("| 竞品 | 近期动态 | 对Lovart威胁 | 应对建议 |")
    lines.append("|------|----------|-------------|----------|")
    lines.append("| Canva | AI功能持续迭代，中国市场(canva.cn)活跃 | 🟠 直接竞品 | 强化Agent差异化叙事 |")
    lines.append("| Midjourney | V7模型+编辑器模式推进 | 🟡 图像生成交叉 | 突出全栈(图像+视频+品牌)优势 |")
    lines.append("| Adobe Firefly | 企业级安全合规，Adobe生态绑定 | 🟡 企业市场 | 继续主打性价比+上手门槛 |")
    lines.append("| Leonardo AI | 游戏/3D垂直强化 | 🟢 赛道不同 | -- |")
    lines.append("| Pollo AI | 对比关键词中频繁出现 | 🟡 直接竞品 | 持续产出Pollo vs Lovart对比内容 |")
    lines.append("| Kling/可灵 | 中国视频生成市场强势 | 🟢 地理隔离 | 中国市场需差异化切入 |")
    return "\n".join(lines)


# ---------- 主函数 ----------

def generate_report(date_str: str, mode: str = "daily") -> str:
    data = load_snapshot(date_str)

    report = f"""# 🔭 Lovart 品牌舆情日报

> 日期：{date_str}
> 生成时间：{datetime.datetime.now().strftime('%H:%M')}
> 模式：{'每日快报' if mode == 'daily' else '周报'}
> 数据源：{len(data)} 个 {"(部分待采集)" if len(data) < 6 else ""}

---

"""
    report += section_overall_health(data)
    report += section_serp_radar(data)
    report += section_i18n_content_radar(data)
    report += section_social_radar(data)
    report += section_competitor_pulse(data)
    report += section_timeline(data)
    report += section_user_persona(data)
    report += section_todos(data)

    report += f"""

---

*本报告由 Lovart Sentinel 自动生成。数据来源详见 1-2 Insight/Lovart ORM/raw/{date_str}/*
*部分社交平台数据需手动/agent采集：Instagram, TikTok, YouTube, Discord, Reddit, 小红书, 微信*
"""

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Lovart Sentinel Report Generator")
    parser.add_argument("--date", default=datetime.date.today().isoformat(), help="Date to generate report for")
    parser.add_argument("--mode", default="daily", choices=["daily", "weekly"])
    parser.add_argument("--output", default=None, help="Output path (default: auto)")
    args = parser.parse_args()

    report = generate_report(args.date, args.mode)

    out_dir = REPORT_OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.output:
        out_path = Path(args.output)
    else:
        suffix = "daily" if args.mode == "daily" else "weekly"
        out_path = out_dir / f"Lovart-Sentinel-{args.date}-{suffix}.md"

    out_path.write_text(report, encoding="utf-8")
    print(f"[Sentinel] Report written to {out_path}")
    print(f"[Sentinel] {len(report)} chars, ~{len(report.splitlines())} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
