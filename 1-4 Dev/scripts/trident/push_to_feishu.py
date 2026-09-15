#!/usr/bin/env python3
"""
Trident → Feishu Bitable 推送
将 GSC/GA4/Bing 关键指标写入飞书多维表，支持看板 + 仪表盘视图。
使用 Feishu Open API (Bitables v1)，不依赖 lark-cli。

认证方式: Feishu 应用凭据 (app_id + app_secret)
配置: 环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET，或同目录 credentials/feishu.json
"""
import json, os, sys, time
from pathlib import Path
from datetime import date, timedelta

import requests
from trident_paths import DATA_INGESTION_DIR, WAREHOUSE_DIR

# ── 路径 ──────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
CRED_DIR = SCRIPT_DIR.parent / "credentials"
OUT_DIR = DATA_INGESTION_DIR

# ── 飞书配置 ──────────────────────────────────────────────
BASE_TOKEN = os.getenv("FEISHU_BASE_TOKEN", "ZLWgbi6VIaCRiNsb22jcNpPRnfh")
APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")

def load_feishu_credentials():
    """优先环境变量，fallback 到 credentials/feishu.json"""
    global APP_ID, APP_SECRET
    if APP_ID and APP_SECRET:
        return
    cred_file = CRED_DIR / "feishu.json"
    if cred_file.exists():
        cred = json.loads(cred_file.read_text())
        APP_ID = cred.get("app_id") or cred.get("APP_ID")
        APP_SECRET = cred.get("app_secret") or cred.get("APP_SECRET")
    if not APP_ID or not APP_SECRET:
        print("❌ 缺少 Feishu 凭据。设置方式:")
        print("   1. export FEISHU_APP_ID=cli_xxx")
        print("   2. export FEISHU_APP_SECRET=xxx")
        print(f"   3. 或创建 {CRED_DIR}/feishu.json 包含 app_id, app_secret")
        sys.exit(1)

def get_tenant_token():
    """获取 tenant_access_token"""
    r = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET},
        timeout=10,
    )
    data = r.json()
    if data.get("code") != 0:
        print(f"❌ 飞书认证失败: {data.get('msg', data)}")
        sys.exit(1)
    return data["tenant_access_token"]

# ── 数据读取 ──────────────────────────────────────────────
def load_json(name):
    f = OUT_DIR / name
    if not f.exists():
        print(f"⚠️  {name} 不存在，跳过")
        return None
    return json.loads(f.read_text())

# ── 飞书 API helpers ──────────────────────────────────────
def feishu_request(token, method, path, body=None):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"https://open.feishu.cn/open-apis/bitable/v1{path}"
    if method == "GET":
        r = requests.get(url, headers=headers, timeout=15)
    elif method == "POST":
        r = requests.post(url, headers=headers, json=body, timeout=15)
    elif method == "PATCH":
        r = requests.patch(url, headers=headers, json=body, timeout=15)
    else:
        raise ValueError(f"Unknown method: {method}")
    return r.json()

def list_tables(token):
    r = feishu_request(token, "GET", f"/apps/{BASE_TOKEN}/tables")
    return r.get("data", {}).get("items", [])

def create_table(token, table_name, fields):
    body = {"table": {"name": table_name}, "fields": fields}
    r = feishu_request(token, "POST", f"/apps/{BASE_TOKEN}/tables", body)
    if r.get("code") != 0:
        print(f"⚠️  建表失败: {r.get('msg', r)}")
        return None
    table_id = r["data"]["table_id"]
    print(f"✅ 表 '{table_name}' 创建成功 (table_id={table_id})")
    return table_id

def upsert_records(token, table_id, records):
    """批量写入记录，每次最多 200 条"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BASE_TOKEN}/tables/{table_id}/records/batch_create"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    total = len(records)
    for i in range(0, total, 200):
        chunk = records[i : i + 200]
        body = {"records": [{"fields": r} for r in chunk]}
        r = requests.post(url, headers=headers, json=body, timeout=30)
        resp = r.json()
        if resp.get("code") != 0:
            print(f"⚠️  批次写入失败 [{i}:{i+len(chunk)}]: {resp.get('msg', resp)}")
            return False
        if i + len(chunk) < total:
            time.sleep(0.5)
    print(f"✅ 写入 {total} 条记录")
    return True

# ── 记录构建 ──────────────────────────────────────────────
def build_records():
    today = date.today().isoformat()
    records = []

    # GSC
    gsc = load_json("gsc-full.json")
    if gsc:
        tiers = {t["label"]: t for t in gsc.get("keyword_tiers", [])}
        records.append({
            "日期": today,
            "来源": "GSC",
            "指标名称": "总点击",
            "指标值": str(tiers.get("Top 100", {}).get("clicks", 0)),
            "对比基准": "",
            "趋势": "",
            "备注": "28天汇总",
        })
        records.append({
            "日期": today, "来源": "GSC",
            "指标名称": "总展示", "指标值": str(tiers.get("Top 100", {}).get("impressions", 0)),
            "对比基准": "", "趋势": "", "备注": "28天汇总",
        })
        records.append({
            "日期": today, "来源": "GSC",
            "指标名称": "整体CTR", "指标值": f"{tiers.get('Top 100', {}).get('ctr', 0):.1f}%",
            "对比基准": "", "趋势": "", "备注": "28天汇总",
        })
        brand = tiers.get("品牌词", {})
        nonbrand = tiers.get("非品牌词", {})
        records.append({
            "日期": today, "来源": "GSC",
            "指标名称": "品牌词占比", "指标值": f"{brand.get('share', 0):.1f}%",
            "对比基准": "", "趋势": "", "备注": f"品牌词{len(gsc.get('top100_keywords',[]))}个中{len([k for k in gsc.get('top100_keywords',[]) if k.get('type')=='brand'])}个",
        })
        records.append({
            "日期": today, "来源": "GSC",
            "指标名称": "非品牌词占比", "指标值": f"{nonbrand.get('share', 0):.1f}%",
            "对比基准": "", "趋势": "", "备注": f"竞品非品牌词 {tiers.get('竞品非品牌词', {}).get('count', 0)}个",
        })
        records.append({
            "日期": today, "来源": "GSC",
            "指标名称": "Top 10 点击",
            "指标值": str(tiers.get("Top 10", {}).get("clicks", 0)),
            "对比基准": str(tiers.get("Top 10", {}).get("impressions", 0)),
            "趋势": "",
            "备注": f"Top 10 CTR: {tiers.get('Top 10', {}).get('ctr', 0):.1f}%",
        })
        # Top keywords as individual records
        for k in gsc.get("top100_keywords", [])[:20]:
            records.append({
                "日期": today, "来源": "GSC",
                "指标名称": f"关键词: {k.get('q','')}",
                "指标值": str(k.get("clicks", 0)),
                "对比基准": str(k.get("impr", 0)),
                "趋势": f"pos={k.get('pos',0):.1f}",
                "备注": k.get("type", "nonbrand"),
            })
        # Country summary
        for c in gsc.get("country_summary", [])[:5]:
            records.append({
                "日期": today, "来源": "GSC",
                "指标名称": f"国家: {c.get('country','')}",
                "指标值": str(c.get("clicks", 0)),
                "对比基准": str(c.get("impressions", 0)),
                "趋势": f"CTR={c.get('ctr',0):.1f}%",
                "备注": f"pos={c.get('pos',0):.1f}",
            })

    # GA4
    ga4 = load_json("ga4-full.json")
    if ga4:
        org = ga4.get("organic_summary", {})
        tw = ga4.get("trend_weekly", {})
        tm = ga4.get("trend_monthly", {})
        records.append({
            "日期": today, "来源": "GA4",
            "指标名称": "Sessions (30d)",
            "指标值": str(org.get("sessions", 0)),
            "对比基准": "",
            "趋势": f"周:{tw.get('change_pct',0):+.1f}% 月:{tm.get('change_pct',0):+.1f}%",
            "备注": "Organic Search",
        })
        records.append({
            "日期": today, "来源": "GA4",
            "指标名称": "Users (30d)",
            "指标值": str(org.get("users", 0)),
            "对比基准": "",
            "趋势": f"New: {org.get('new_users',0)}({org.get('new_users',0)/max(org.get('users',1),1)*100:.1f}%)",
            "备注": f"Avg Dur: {org.get('avg_duration_sec',0)}s, Pages/S: {org.get('pages_per_session',0)}",
        })
        records.append({
            "日期": today, "来源": "GA4",
            "指标名称": "Bounce Rate",
            "指标值": f"{org.get('bounce_rate', 0)}%",
            "对比基准": "", "趋势": "", "备注": "Organic Search",

        })
        # Channel summary
        for ch in ga4.get("channel_summary", [])[:6]:
            m = ch.get("metrics", {})
            records.append({
                "日期": today, "来源": "GA4",
                "指标名称": f"渠道: {ch.get('dims',{}).get('sessionDefaultChannelGroup','')}",
                "指标值": m.get("sessions", "0"),
                "对比基准": m.get("totalUsers", "0"),
                "趋势": f"bounce={float(m.get('bounceRate',0))*100:.1f}%",
                "备注": "",
            })

    # Bing
    bing = load_json("bing-full.json")
    if bing:
        kw = bing.get("keywords", [])
        total_cl = sum(k.get("clicks", 0) for k in kw)
        total_impr = sum(k.get("impressions", 0) for k in kw)
        b_ctr = total_cl / total_impr * 100 if total_impr else 0
        records.append({
            "日期": today, "来源": "Bing", "指标名称": "总关键词数",
            "指标值": str(len(kw)), "对比基准": "", "趋势": "", "备注": "全部历史",
        })
        records.append({
            "日期": today, "来源": "Bing", "指标名称": "总点击",
            "指标值": str(total_cl), "对比基准": "", "趋势": "", "备注": "全部历史",
        })
        records.append({
            "日期": today, "来源": "Bing", "指标名称": "总展示",
            "指标值": str(total_impr), "对比基准": "", "趋势": "", "备注": "全部历史",
        })
        records.append({
            "日期": today, "来源": "Bing", "指标名称": "整体CTR",
            "指标值": f"{b_ctr:.1f}%", "对比基准": "", "趋势": "", "备注": "全部历史",
        })
        # Crawl stats
        crawl = bing.get("crawl_daily", [])
        if crawl:
            cl = crawl[-1]
            records.append({
                "日期": today, "来源": "Bing", "指标名称": "索引数",
                "指标值": str(cl.get("InIndex", "?")), "对比基准": "",
                "趋势": "", "备注": "最新",
            })
            records.append({
                "日期": today, "来源": "Bing", "指标名称": "日爬取量",
                "指标值": str(cl.get("CrawledPages", "?")), "对比基准": "",
                "趋势": "", "备注": "最新",
            })
            records.append({
                "日期": today, "来源": "Bing", "指标名称": "爬虫错误",
                "指标值": str(cl.get("CrawlErrors", "?")), "对比基准": "",
                "趋势": "", "备注": "最新",
            })
        # Top Bing pages
        for p in bing.get("pages", [])[:10]:
            url_short = p.get("url", "").replace("https://www.lovart.ai", "")[:80]
            records.append({
                "日期": today, "来源": "Bing",
                "指标名称": f"页面: {url_short}",
                "指标值": str(p.get("clicks", 0)),
                "对比基准": str(p.get("impressions", 0)),
                "趋势": "", "备注": "",
            })

    return records


# ── main ──────────────────────────────────────────────────
def main():
    load_feishu_credentials()
    print("🔑 获取飞书 access token...")
    token = get_tenant_token()

    # 1. 查表
    print(f"\n📋 检查 Base {BASE_TOKEN} 中的表...")
    tables = list_tables(token)
    target = None
    for t in tables:
        if t.get("name") == "SEO 数据看板":
            target = t["table_id"]
            print(f"  找到现有表: SEO 数据看板 (table_id={target})")
            break

    # 2. 建表
    if not target:
        print("\n🛠  创建新表 'SEO 数据看板'...")
        fields = [
            {"field_name": "日期", "type": 1},          # 文本
            {"field_name": "来源", "type": 3},          # 单选
            {"field_name": "指标名称", "type": 1},       # 文本
            {"field_name": "指标值", "type": 1},         # 文本 (含数字+单位)
            {"field_name": "对比基准", "type": 1},       # 文本
            {"field_name": "趋势", "type": 1},           # 文本
            {"field_name": "备注", "type": 1},           # 文本
        ]
        target = create_table(token, "SEO 数据看板", fields)
        if not target:
            print("❌ 无法创建表，退出")
            sys.exit(1)
        # 给 API 一点时间
        time.sleep(2)

    # 3. 构建记录
    print("\n📊 构建数据记录...")
    records = build_records()
    print(f"  共 {len(records)} 条记录")

    # 4. 写入
    print(f"\n📤 写入飞书多维表...")
    upsert_records(token, target, records)

    # 5. 查看链接
    print(f"\n🔗 飞书表格: https://resonate.feishu.cn/base/{BASE_TOKEN}?table={target}")
    print("   → 打开后可在飞书里创建看板视图 / 仪表盘")

    return target


if __name__ == "__main__":
    main()
