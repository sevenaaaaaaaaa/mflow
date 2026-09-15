#!/usr/bin/env python3
"""竞品词深度匹配: 提取真实竞品词库 + GSC 5000词全量拉取 + 匹配分析 + 报告更新"""
from __future__ import annotations
import json, re, sys, datetime
from pathlib import Path
from collections import defaultdict

import sys
from pathlib import Path as _Path
_SCRIPT_DIR = _Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
_TRIDENT_SCRIPT_DIR = _SCRIPT_DIR / "trident"
if str(_TRIDENT_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_TRIDENT_SCRIPT_DIR))
from lovart_brand_match import is_brand
from credential_paths import credential_file

TRIDENT = Path(__file__).resolve().parents[2] / "1-2 Insight/Trident Insights"

# ============================================================
# Step 1: 提取竞品词库
# ============================================================
def extract_competitor_keywords():
    """从两个 .md 文件提取所有竞品关键词"""
    kw_dir = TRIDENT / "竞品核心非品牌词"
    
    # 从表格中提取关键词（第一个列为英文关键词）
    keywords = set()
    keywords_by_category = defaultdict(set)
    current_category = "Unknown"
    
    for md_file in [kw_dir / "lovart_competitors_core_keywords.md", kw_dir / "lovart_competitors_keywords.md"]:
        text = md_file.read_text(encoding="utf-8")
        
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            
            # Track section headers
            if line.startswith("## "):
                current_category = line.replace("## ", "").strip()
                continue
            if line.startswith("### "):
                current_category = line.replace("### ", "").strip()
                continue
            
            # Parse table rows
            if line.startswith("|") and "---" not in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 1:
                    kw = parts[0]
                    # Skip headers and non-English only entries
                    if any(h in kw.lower() for h in ["关键词", "keyword", "模型", "优先级", "---", "分类"]):
                        continue
                    # Extract English keyword (may contain Chinese translation after / or （)
                    eng_kw = re.split(r'\s*[/／（(]\s*', kw)[0].strip()
                    # Skip purely Chinese keywords
                    if re.search(r'[\u4e00-\u9fff]', eng_kw) and not re.search(r'[a-zA-Z]', eng_kw):
                        continue
                    # Clean up
                    eng_kw = eng_kw.strip().strip('"').strip("'")
                    if len(eng_kw) >= 3 and not eng_kw.startswith("```"):
                        keywords.add(eng_kw.lower())
                        keywords_by_category[current_category].add(eng_kw.lower())
    
    # Also extract from priority matrices and code blocks
    all_text = ""
    for md_file in [kw_dir / "lovart_competitors_core_keywords.md", kw_dir / "lovart_competitors_keywords.md"]:
        all_text += md_file.read_text(encoding="utf-8") + "\n"
    
    # Extract from markdown code blocks
    for block in re.findall(r'```(.*?)```', all_text, re.DOTALL):
        for line in block.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and len(line) >= 3:
                kw = re.split(r'\s*[/／（(]\s*', line)[0].strip()
                if not re.search(r'^[\u4e00-\u9fff]+$', kw) and len(kw) >= 3:
                    keywords.add(kw.lower())
    
    # Manual additions from priority matrices
    extra_core = [
        "ai image generator", "ai video generator", "ai photo generator", "ai design generator",
        "workflow automation", "background remover", "text to video", "text to image", "image to video",
        "lip sync", "talking avatar", "ai avatar", "motion control", "character consistency",
        "cinematic video", "ai commercial", "marketing video ai", "ai ad generator", "ugc generator",
        "ai shorts", "product video", "social media video", "brand video", "logo design",
        "ai logo generator", "ai poster", "ai banner", "graphic design",
    ]
    keywords.update(k.lower() for k in extra_core)
    
    # Classify: core keywords (short, high-priority) vs full keywords
    core_set = set(k.lower() for k in extra_core)
    core_set.update(["sora", "kling", "veo 3", "midjourney", "flux", "seedance", "seedream", "dall-e",
                     "ai avatar", "talking avatar", "lip sync", "motion control", "character consistency"])
    
    result = {
        "total_unique": len(keywords),
        "core_count": len(core_set),
        "full_count": len(keywords),
        "keywords": sorted(keywords),
        "core_keywords": sorted(core_set),
        "by_category": {k: sorted(v) for k, v in keywords_by_category.items()}
    }
    
    out_path = TRIDENT / "reports" / "competitor_keywords.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"📋 竞品词库: {result['full_count']} 全量词, {result['core_count']} 核心词")
    print(f"   {len(keywords_by_category)} 个分类")
    print(f"   → {out_path}")
    return result


# ============================================================
# Step 2: GSC 5000 关键词拉取
# ============================================================
def fetch_gsc_5k(start_date, end_date, label):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    
    token = json.loads(credential_file("gsc-token.json", "LOVART_GSC_TOKEN_FILE").read_text())
    creds = Credentials.from_authorized_user_info(token, ["https://www.googleapis.com/auth/webmasters.readonly"])
    svc = build("searchconsole", "v1", credentials=creds)
    search = svc.searchanalytics()
    SITE = "https://www.lovart.ai/"
    
    body = {
        "startDate": start_date, "endDate": end_date,
        "dimensions": ["query"], "rowLimit": 5000
    }
    resp = search.query(siteUrl=SITE, body=body).execute()
    rows = resp.get("rows", [])
    
    results = [{"q": r["keys"][0], "clicks": r["clicks"], "impr": r["impressions"],
                "ctr": round(r["ctr"]*100, 1), "pos": round(r["position"], 1)} for r in rows]
    
    total_clicks = sum(r["clicks"] for r in results)
    print(f"📊 GSC {label} ({start_date}~{end_date}): {len(results):,} keywords, {total_clicks:,} clicks")
    return results


# ============================================================
# Step 3: 匹配分析
# ============================================================

def match_competitor(gsc_keywords, competitor_keywords, core_keywords, label):
    """将 GSC 关键词与竞品词库匹配"""
    nonbrand_gsc = [k for k in gsc_keywords if not is_brand(k["q"])]
    
    # Full match: any competitor keyword is a substring of the GSC keyword
    comp_full = [kw for kw in competitor_keywords if len(kw) >= 3]
    matched_full = []
    for gk in nonbrand_gsc:
        gql = gk["q"].lower()
        matched_comps = set()
        for ck in comp_full:
            if ck in gql:
                matched_comps.add(ck)
        if matched_comps:
            matched_full.append({**gk, "matched_comps": sorted(matched_comps)})
    
    # Core match: core keywords only
    comp_core = [kw for kw in core_keywords if len(kw) >= 3]
    matched_core = []
    for gk in nonbrand_gsc:
        gql = gk["q"].lower()
        matched_comps = set()
        for ck in comp_core:
            if ck in gql:
                matched_comps.add(ck)
        if matched_comps:
            matched_core.append({**gk, "matched_comps": sorted(matched_comps)})
    
    # Unique competitor keywords that have traffic
    uniq_comp_full = set()
    uniq_comp_core = set()
    for m in matched_full:
        uniq_comp_full.update(m["matched_comps"])
    for m in matched_core:
        uniq_comp_core.update(m["matched_comps"])
    
    # Tier analysis
    def tier_stats(matched_list, tier_n):
        top = matched_list[:tier_n]
        return {
            "count": len(top),
            "clicks": sum(k["clicks"] for k in top),
            "impressions": sum(k["impr"] for k in top),
            "unique_competitors": len(set(c for k in top for c in k["matched_comps"]))
        }
    
    total_nb_clicks = sum(k["clicks"] for k in nonbrand_gsc)
    
    result = {
        "label": label,
        "total_gsc_keywords": len(gsc_keywords),
        "nonbrand_keywords": len(nonbrand_gsc),
        "total_nonbrand_clicks": total_nb_clicks,
        "competitor_keywords_in_list": len(comp_full),
        "core_keywords_in_list": len(comp_core),
        "matched_gsc_keywords_full": len(matched_full),
        "matched_gsc_keywords_core": len(matched_core),
        "unique_competitors_matched_full": len(uniq_comp_full),
        "unique_competitors_matched_core": len(uniq_comp_core),
        "full_match_rate": round(len(uniq_comp_full)/len(comp_full)*100, 1) if comp_full else 0,
        "core_match_rate": round(len(uniq_comp_core)/len(comp_core)*100, 1) if comp_core else 0,
        "competitor_click_share": round(sum(k["clicks"] for k in matched_full)/total_nb_clicks*100, 1) if total_nb_clicks else 0,
        "competitor_impr_share": round(sum(k["impr"] for k in matched_full)/sum(k["impr"] for k in nonbrand_gsc)*100, 1) if nonbrand_gsc and sum(k["impr"] for k in nonbrand_gsc) else 0,
        "tier_stats_full": {
            "top10": tier_stats(matched_full, 10),
            "top50": tier_stats(matched_full, 50),
            "top100": tier_stats(matched_full, 100),
        },
        "tier_stats_core": {
            "top10": tier_stats(matched_core, 10),
            "top50": tier_stats(matched_core, 50),
            "top100": tier_stats(matched_core, 100),
        },
        "matched_keywords_full": matched_full[:100],
        "matched_keywords_core": matched_core[:50],
    }
    
    print(f"\n🔍 {label} 匹配结果:")
    print(f"  Full: {result['matched_gsc_keywords_full']} GSC keys → {result['unique_competitors_matched_full']} competitors ({result['full_match_rate']}%)")
    print(f"  Core: {result['matched_gsc_keywords_core']} GSC keys → {result['unique_competitors_matched_core']} competitors ({result['core_match_rate']}%)")
    print(f"  Competitor click share: {result['competitor_click_share']}%")
    print(f"  Top 10 full: {result['tier_stats_full']['top10']['count']} words, {result['tier_stats_full']['top10']['clicks']:,} clicks")
    print(f"  Top 10 core: {result['tier_stats_core']['top10']['count']} words, {result['tier_stats_core']['top10']['clicks']:,} clicks")
    
    return result


# ============================================================
# Step 4: 更新报告
# ============================================================
def update_report(comp_data):
    """读取现有月报，替换第4节（竞品非品牌词）"""
    report_path = TRIDENT / "reports" / "monthly" / "Lovart-SEO-2026-05.md"
    report = report_path.read_text()
    
    # Find section 4 boundaries
    sec4_start = report.find("## 四、竞品非品牌词覆盖")
    sec5_start = report.find("## 五、页面目录流量")
    
    if sec4_start < 0 or sec5_start < 0:
        print("⚠️ Cannot find sections 4/5 boundaries in report")
        return False
    
    before = report[:sec4_start]
    after = report[sec5_start:]
    
    may = comp_data["may"]
    apr = comp_data["april"]
    kw_list = comp_data["keyword_list"]
    
    def chg_str(a, m): 
        d = m-a
        p = round(d/a*100,1) if a else 0
        arrow = "↑" if d>0 else ("↓" if d<0 else "→")
        return f"{arrow}{d:+,} / {p:+.1f}%"
    
    new_sec4 = f"""## 四、竞品非品牌词覆盖

> 竞品词库: 从 `竞品核心非品牌词/` 目录提取 {kw_list['full_count']} 个竞品关键词 (core {kw_list['core_count']} 词)
> GSC 拉取: 5,000 关键词全量 (替代此前 100 词限制)

### 4.1 总览

| 指标 | 4月 | 5月 | 变化 |
|------|-----|-----|------|
| 竞品词库规模 | {kw_list['full_count']} 词 | {kw_list['full_count']} 词 | → |
| Core 核心词 | {kw_list['core_count']} 词 | {kw_list['core_count']} 词 | → |
| GSC 命中 (Full/5K) | {apr['unique_competitors_matched_full']} 竞品词 | {may['unique_competitors_matched_full']} 竞品词 | {chg_str(apr['unique_competitors_matched_full'], may['unique_competitors_matched_full'])} |
| GSC 命中 (Core/5K) | {apr['unique_competitors_matched_core']} 核心词 | {may['unique_competitors_matched_core']} 核心词 | {chg_str(apr['unique_competitors_matched_core'], may['unique_competitors_matched_core'])} |
| Full 覆盖率 | {apr['full_match_rate']}% | {may['full_match_rate']}% | {may['full_match_rate']-apr['full_match_rate']:+.1f}% |
| Core 覆盖率 | {apr['core_match_rate']}% | {may['core_match_rate']}% | {may['core_match_rate']-apr['core_match_rate']:+.1f}% |
| 竞品词点击 | {sum(k['clicks'] for k in may['matched_keywords_full']):,} | 全 GSC 非品牌点击 {may['total_nonbrand_clicks']:,} 中 | 占比 {may['competitor_click_share']}% |

### 4.2 分层表现 (5月)

| 分层 | Full 命中词数 | Full Clicks | Core 命中词数 | Core Clicks | 竞品词去重数 |
|------|:-----------:|------------:|:-----------:|------------:|:----------:|
| Top 10 内 | {may['tier_stats_full']['top10']['count']} | {may['tier_stats_full']['top10']['clicks']:,} | {may['tier_stats_core']['top10']['count']} | {may['tier_stats_core']['top10']['clicks']:,} | {may['tier_stats_full']['top10']['unique_competitors']} |
| Top 50 内 | {may['tier_stats_full']['top50']['count']} | {may['tier_stats_full']['top50']['clicks']:,} | {may['tier_stats_core']['top50']['count']} | {may['tier_stats_core']['top50']['clicks']:,} | {may['tier_stats_full']['top50']['unique_competitors']} |
| Top 100 内 | {may['tier_stats_full']['top100']['count']} | {may['tier_stats_full']['top100']['clicks']:,} | {may['tier_stats_core']['top100']['count']} | {may['tier_stats_core']['top100']['clicks']:,} | {may['tier_stats_full']['top100']['unique_competitors']} |

### 4.3 命中的核心竞品词 (Core, 5月)

| # | 竞品词 | 匹配的 GSC 关键词 (示例) | 点击 | 曝光 | CTR |
|---|--------|------------------------|------|------|-----|
"""
    # Add core matched keywords
    core_adjust = {}
    for m in may['matched_keywords_core'][:40]:
        matches = m["matched_comps"]
        for comp in matches:
            if comp not in core_adjust or m["clicks"] > core_adjust[comp]["clicks"]:
                core_adjust[comp] = {"q": m["q"], "clicks": m["clicks"], "impr": m["impr"], "ctr": m["ctr"]}
    
    for i, (comp, data) in enumerate(sorted(core_adjust.items(), key=lambda x: x[1]["clicks"], reverse=True)[:20]):
        new_sec4 += f"| {i+1} | {comp} | {data['q'][:35]} | {data['clicks']:,} | {data['impr']:,} | {data['ctr']}% |\n"
    
    new_sec4 += """
### 4.4 命中的全量竞品词 (Full, 5月, Top 30 按点击)

| # | GSC 关键词 | 匹配到的竞品词 | 点击 | 曝光 | CTR | 排名 |
|---|-----------|-------------|------|------|-----|------|
"""
    for i, m in enumerate(may['matched_keywords_full'][:30]):
        comps_str = ", ".join(m["matched_comps"][:5])
        new_sec4 += f"| {i+1} | {m['q'][:30]} | {comps_str[:45]} | {m['clicks']:,} | {m['impr']:,} | {m['ctr']}% | {m['pos']} |\n"

    new_sec4 += f"""
### 4.5 未覆盖的核心竞品词 (Top 20 缺失)

以下高优先级竞品词在 GSC 5,000 关键词中**完全没有排名**:
"""
    all_matched_core = set()
    for m in may['matched_keywords_core']:
        all_matched_core.update(m["matched_comps"])
    missing_core = [kw for kw in kw_list['core_keywords'] if kw not in all_matched_core]
    for i, kw in enumerate(missing_core[:20]):
        new_sec4 += f"- {kw}\n"

    new_sec4 += """
> **关键洞察**: 竞品词覆盖从早期的"0/252 假词库"升级为真实数据分析。Full 匹配代表宽口径（所有竞品词的变体/组合表现），Core 匹配代表严口径（核心高价值词的实际排名）。两者差异越大，说明 Lovart 的 SEO 长尾主要来自模型名称/品牌变体蹭流量，而非真正行业词。
"""
    
    updated_report = before + new_sec4 + "\n" + after
    report_path.write_text(updated_report)
    print(f"\n✅ Report section 4 updated in {report_path}")
    return True


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    # Step 1: Extract keywords
    print("=" * 60)
    print("[1/4] 提取竞品词库")
    kw_list = extract_competitor_keywords()
    
    # Step 2: Fetch GSC
    print("\n[2/4] GSC 5000 关键词拉取")
    may_kw = fetch_gsc_5k("2026-05-01", "2026-05-30", "May")
    apr_kw = fetch_gsc_5k("2026-04-01", "2026-04-30", "April")
    
    # Step 3: Match
    print("\n[3/4] 竞品词匹配")
    may_result = match_competitor(may_kw, kw_list["keywords"], kw_list["core_keywords"], "May")
    apr_result = match_competitor(apr_kw, kw_list["keywords"], kw_list["core_keywords"], "April")
    
    # Save match results
    match_data = {
        "keyword_list_stats": {k: v for k, v in kw_list.items() if k != "keywords" and k != "core_keywords" and k != "by_category"},
        "may": {k: v for k, v in may_result.items() if k not in ("matched_keywords_full", "matched_keywords_core")},
        "april": {k: v for k, v in apr_result.items() if k not in ("matched_keywords_full", "matched_keywords_core")},
    }
    (TRIDENT / "reports" / "competitor_match_result.json").write_text(json.dumps(match_data, indent=2, ensure_ascii=False))
    
    # Step 4: Update report
    print("\n[4/4] 更新月度报告")
    comp_data = {
        "may": may_result,
        "april": apr_result,
        "keyword_list": kw_list,
    }
    update_report(comp_data)
    
    print("\n" + "=" * 60)
    print("✅ Done!")
