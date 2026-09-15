#!/usr/bin/env python3
"""
三引擎统一情报摘要 — 从 GSC + GA4 + Bing JSON 生成全渠道分析报告

摘要须支持报告标准：关键词点击/曝光/CTR；若用于正式 SEO 报告须配环比期数据。
见 seo_report_standards.py / AGENTS.md Part A0。
"""
import json, re
from trident_paths import DATA_INGESTION_DIR

BASE = DATA_INGESTION_DIR

def fm(n):
    return f"{n:,}"

def load(name):
    return json.loads((BASE / name).read_text())

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lovart_brand_match import is_brand, partition_keywords

def generate():
    gsc = load("gsc-full.json")
    ga4 = load("ga4-full.json")
    bing = load("bing-full.json")

    # Normalize GSC fields
    gk = [{'query': k.get('q',''), 'clicks': k.get('clicks',0), 'impressions': k.get('impr',0),
           'ctr': k.get('ctr',0), 'position': k.get('pos',0)} for k in gsc.get('top100_keywords',[])]
    bk = bing.get('keywords',[])

    g_brand = [k for k in gk if is_brand(k['query'])]
    g_non = [k for k in gk if not is_brand(k['query'])]
    b_brand = [k for k in bk if is_brand(k['query'])]
    b_non = [k for k in bk if not is_brand(k['query'])]
    g_cl = sum(k['clicks'] for k in gk); g_impr = sum(k['impressions'] for k in gk)
    b_cl = sum(k['clicks'] for k in bk); b_impr = sum(k['impressions'] for k in bk)
    g_brand_cl = sum(k['clicks'] for k in g_brand)
    b_brand_cl = sum(k['clicks'] for k in b_brand)
    g_non_cl = sum(k['clicks'] for k in g_non)
    b_non_cl = sum(k['clicks'] for k in b_non)
    g_ctr = g_cl/g_impr*100 if g_impr else 0
    b_ctr = b_cl/b_impr*100 if b_impr else 0
    g_qs = {k['query'] for k in gk}
    b_qs = {k['query'] for k in bk[:200]}
    common = g_qs & b_qs
    g_only = g_qs - b_qs

    org = ga4['organic_summary']
    seg = {r['dims']['newVsReturning']: r['metrics'] for r in ga4['user_segments']}
    tw = ga4['trend_weekly']; tm = ga4['trend_monthly']
    
    crawl = bing.get('crawl_daily',[])
    cl = crawl[-1] if crawl else {}
    cp = crawl[-8] if len(crawl)>=8 else {}
    idx_delta = cl.get('InIndex',0) - cp.get('InIndex',0) if cp else 0

    lines = []
    L = lines.append

    L("# Lovart 全渠道情报摘要")
    L(f"\n**数据源**: GSC(28d) + GA4(30d) + Bing(全部历史) — lovart.ai\n")
    
    L("## 1. 关键词对比: Google vs Bing\n")
    L(f"| 指标 | Google (GSC) | Bing | 合计 |")
    L(f"|------|-------------|------|------|")
    L(f"| 关键词数 | {len(gk)} | {len(bk)} | — |")
    L(f"| 总点击 | {fm(g_cl)} | {fm(b_cl)} | {fm(g_cl+b_cl)} |")
    L(f"| 总展示 | {fm(g_impr)} | {fm(b_impr)} | {fm(g_impr+b_impr)} |")
    L(f"| 整体CTR | {g_ctr:.1f}% | {b_ctr:.1f}% | {(g_cl+b_cl)/(g_impr+b_impr)*100:.1f}% |")
    L(f"| 品牌词占比 | {g_brand_cl/g_cl*100:.1f}% | {b_brand_cl/b_cl*100:.1f}% | — |")
    L(f"| 非品牌词占比 | {g_non_cl/g_cl*100:.1f}% | {b_non_cl/b_cl*100:.1f}% | — |")
    L(f"| 非品牌词数 | {len(g_non)} | {len(b_non)} | — |")
    L(f"| 重叠关键词 | {len(common)} / {len(g_qs)} | — | — |")

    L(f"\n### Top 10 品牌词 (Google)\n")
    for k in g_brand[:10]:
        L(f"- {k['query']}: {fm(k['clicks'])} clicks, pos {k['position']:.1f}")

    L(f"\n### Top 10 品牌词 (Bing)\n")
    for k in b_brand[:10]:
        L(f"- {k['query']}: {fm(k['clicks'])} clicks")

    L(f"\n## 2. GA4 自然搜索全景\n")
    L(f"| 指标 | 值 |")
    L(f"|------|-----|")
    L(f"| Sessions (30d) | {fm(org['sessions'])} |")
    L(f"| Users | {fm(org['users'])} |")
    L(f"| New Users | {fm(org['new_users'])} ({org['new_users']/org['users']*100:.1f}%) |")
    L(f"| Avg Duration | {org['avg_duration_sec']}s |")
    L(f"| Pages/Session | {org['pages_per_session']} |")
    L(f"| Bounce Rate | {org['bounce_rate']}% |")
    L(f"| 周环比 | {tw['change_pct']:+.1f}% |")
    L(f"| 月环比 | {tm['change_pct']:+.1f}% |")

    L(f"\n## 3. Bing 爬虫健康\n")
    L(f"| 指标 | 值 |")
    L(f"|------|-----|")
    L(f"| 索引数 | {fm(cl.get('InIndex','?'))} (周变化 {idx_delta:+}) |")
    L(f"| 日爬取量 | {fm(cl.get('CrawledPages','?'))} |")
    L(f"| 爬虫错误 | {fm(cl.get('CrawlErrors','?'))} |")
    L(f"| Code 4xx | {fm(cl.get('Code4xx','?'))} |")
    L(f"| Code 5xx | {fm(cl.get('Code5xx','?'))} |")
    L(f"| robots拦截 | {fm(cl.get('BlockedByRobotsTxt','?'))} |")
    L(f"| InLinks | {fm(cl.get('InLinks','?'))} |")

    L(f"\n## 4. 核心洞察 & TODO\n")
    bing_mult = b_cl/g_cl if g_cl else 0
    L(f"1. **Bing 是 Google 的 {bing_mult:.1f}x 点击量** — 词库 {len(bk)//len(gk)}x 更大 ({len(bk)} vs {len(gk)} 词)，仅 {len(common)} 个重叠词，两平台独立运营")
    L(f"2. **非品牌词在 Bing 上空间更大** — {len(b_non)} 词 vs Google {len(g_non)} 词 ({len(b_non)//max(len(g_non),1)}x)，Google 品牌词占比 {g_brand_cl/g_cl*100:.0f}% 极度集中")
    L(f"3. **爬虫健康需关注** — {cl.get('CrawlErrors',0)} 错误/天，{cl.get('Code4xx',0)} 个 4xx，{cl.get('BlockedByRobotsTxt',0)} 被 robots 拦截")

    L(f"\n### TODO\n")
    for i, t in enumerate([
        f"P0 | Bing 4xx {cl.get('Code4xx',0)}/天 → 排查404页面并301重定向",
        f"P0 | Bing {len(b_non)} 非品牌词 → 优先Bing长尾词SEO",
        f"P0 | 两平台重叠仅{len(common)}词 → 为{len(g_only)}个Google独有词建Bing内容",
        f"P1 | 非品牌占比: G {g_non_cl/g_cl*100:.1f}% / B {b_non_cl/b_cl*100:.1f}% → 目标各+5pp",
        f"P1 | GA4 周环比 {tw['change_pct']:+.1f}% → 跟踪下周趋势",
        f"P2 | Bing 4421词长尾挖掘 → 回填GSC策略",
        f"P2 | robots拦截 {cl.get('BlockedByRobotsTxt',0)} → 区分AI bot vs 合法爬虫",
    ], 1):
        L(f"{i}. {t}")

    (BASE / "intelligence-brief.md").write_text("\n".join(lines) + "\n")
    print(f"✅ {BASE}/intelligence-brief.md")

if __name__ == "__main__":
    generate()
