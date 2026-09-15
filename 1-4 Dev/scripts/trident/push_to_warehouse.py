#!/usr/bin/env python3
"""
Trident → 数据仓库 (SQLite + 结构化导出)
将 GSC/GA4/Bing 数据写入本地 SQLite 数仓，同时导出 Parquet/CSV 供云数仓摄入。

架构:
  trident_data.db (SQLite)
    ├── snapshots        ← 每日指标快照
    ├── gsc_keywords     ← GSC 关键词详情
    ├── ga4_organic      ← GA4 自然搜索日趋势
    ├── ga4_channels     ← GA4 全渠道
    ├── ga4_geo          ← GA4 分国家
    ├── bing_keywords    ← Bing 关键词详情
    ├── bing_pages       ← Bing 页面详情
    └── bing_crawl       ← Bing 爬虫日统计

  Output/Warehouse/ (Parquet/CSV 导出)
    └── YYYY-MM-DD/
        ├── snapshot.parquet
        ├── gsc_keywords.parquet
        ├── ...
        └── README.md
"""
import json, sqlite3, os, sys, csv
from pathlib import Path
from datetime import date, timedelta, datetime
from io import StringIO
from trident_paths import DATA_INGESTION_DIR, WAREHOUSE_DIR

# ── 路径 ──────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR = DATA_INGESTION_DIR
DB_PATH = WAREHOUSE_DIR / "trident_data.db"

WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

# ── 工具函数 ──────────────────────────────────────────────
def load_json(name):
    f = OUT_DIR / name
    if not f.exists():
        print(f"  ⚠️  {name} 不存在，跳过")
        return None
    return json.loads(f.read_text())

def safe_int(v, default=0):
    try: return int(v)
    except: return default

def safe_float(v, default=0.0):
    try: return float(v)
    except: return default

# ── SQLite Schema ─────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    source TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value TEXT,
    metric_numeric REAL,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(date, source, metric_name)
);

CREATE TABLE IF NOT EXISTS gsc_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    query TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    ctr REAL DEFAULT 0,
    position REAL DEFAULT 0,
    kw_type TEXT,
    UNIQUE(date, query)
);

CREATE TABLE IF NOT EXISTS gsc_countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    country TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    ctr REAL DEFAULT 0,
    position REAL DEFAULT 0,
    UNIQUE(date, country)
);

CREATE TABLE IF NOT EXISTS ga4_organic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    sessions INTEGER DEFAULT 0,
    total_users INTEGER DEFAULT 0,
    new_users INTEGER DEFAULT 0,
    avg_duration_sec REAL DEFAULT 0,
    pages_per_session REAL DEFAULT 0,
    bounce_rate REAL DEFAULT 0,
    UNIQUE(date)
);

CREATE TABLE IF NOT EXISTS ga4_trend (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    period TEXT NOT NULL,
    recent_sessions INTEGER DEFAULT 0,
    prior_sessions INTEGER DEFAULT 0,
    change_pct REAL DEFAULT 0,
    UNIQUE(date, period)
);

CREATE TABLE IF NOT EXISTS ga4_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    channel TEXT NOT NULL,
    sessions INTEGER DEFAULT 0,
    total_users INTEGER DEFAULT 0,
    bounce_rate REAL DEFAULT 0,
    avg_duration_sec REAL DEFAULT 0,
    UNIQUE(date, channel)
);

CREATE TABLE IF NOT EXISTS ga4_geo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    country TEXT NOT NULL,
    sessions INTEGER DEFAULT 0,
    total_users INTEGER DEFAULT 0,
    new_users INTEGER DEFAULT 0,
    avg_duration_sec REAL DEFAULT 0,
    pages_per_session REAL DEFAULT 0,
    bounce_rate REAL DEFAULT 0,
    UNIQUE(date, country)
);

CREATE TABLE IF NOT EXISTS bing_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    query TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    ctr REAL DEFAULT 0,
    position REAL DEFAULT 0,
    UNIQUE(date, query)
);

CREATE TABLE IF NOT EXISTS bing_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    url TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    UNIQUE(date, url)
);

CREATE TABLE IF NOT EXISTS bing_crawl (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    in_index INTEGER DEFAULT 0,
    crawled_pages INTEGER DEFAULT 0,
    crawl_errors INTEGER DEFAULT 0,
    code_4xx INTEGER DEFAULT 0,
    code_5xx INTEGER DEFAULT 0,
    blocked_robots INTEGER DEFAULT 0,
    in_links INTEGER DEFAULT 0,
    UNIQUE(date)
);

CREATE INDEX IF NOT EXISTS idx_snapshots_date ON snapshots(date);
CREATE INDEX IF NOT EXISTS idx_snapshots_source ON snapshots(source);
CREATE INDEX IF NOT EXISTS idx_gsc_kw_date ON gsc_keywords(date);
CREATE INDEX IF NOT EXISTS idx_ga4_org_date ON ga4_organic(date);
CREATE INDEX IF NOT EXISTS idx_bing_kw_date ON bing_keywords(date);
CREATE INDEX IF NOT EXISTS idx_bing_crawl_date ON bing_crawl(date);
"""

# ── 数据库写入 ────────────────────────────────────────────
def init_db():
    db = sqlite3.connect(str(DB_PATH))
    db.executescript(SCHEMA)
    db.commit()
    return db

def ingest_gsc(db, gsc_data, today):
    if not gsc_data:
        return
    # Snapshots
    tiers = {t["label"]: t for t in gsc_data.get("keyword_tiers", [])}
    metrics = [
        ("总点击", tiers.get("Top 100", {}).get("clicks", 0)),
        ("总展示", tiers.get("Top 100", {}).get("impressions", 0)),
        ("整体CTR", tiers.get("Top 100", {}).get("ctr", 0)),
        ("品牌词占比", tiers.get("品牌词", {}).get("share", 0)),
        ("非品牌词占比", tiers.get("非品牌词", {}).get("share", 0)),
        ("页面收录数", gsc_data.get("pages", {}).get("indexed_count", 0)),
    ]
    for name, val in metrics:
        db.execute(
            "INSERT OR REPLACE INTO snapshots (date, source, metric_name, metric_value, metric_numeric) VALUES (?,?,?,?,?)",
            (today, "GSC", name, str(val), safe_float(val)),
        )
    # Keywords
    for k in gsc_data.get("top100_keywords", []):
        db.execute(
            "INSERT OR REPLACE INTO gsc_keywords (date, query, clicks, impressions, ctr, position, kw_type) VALUES (?,?,?,?,?,?,?)",
            (today, k.get("q", ""), k.get("clicks", 0), k.get("impr", 0),
             k.get("ctr", 0), k.get("pos", 0), k.get("type", "")),
        )
    # Countries
    for c in gsc_data.get("country_summary", []):
        db.execute(
            "INSERT OR REPLACE INTO gsc_countries (date, country, clicks, impressions, ctr, position) VALUES (?,?,?,?,?,?)",
            (today, c.get("country", ""), c.get("clicks", 0),
             c.get("impressions", 0), c.get("ctr", 0), c.get("pos", 0)),
        )
    cnt_kw = len(gsc_data.get("top100_keywords", []))
    cnt_geo = len(gsc_data.get("country_summary", []))
    print(f"  GSC: {cnt_kw} 关键词 + {cnt_geo} 国家 入仓")

def ingest_ga4(db, ga4_data, today):
    if not ga4_data:
        return
    org = ga4_data.get("organic_summary", {})
    metrics = [
        ("Sessions (30d)", org.get("sessions", 0)),
        ("Users (30d)", org.get("users", 0)),
        ("New Users (30d)", org.get("new_users", 0)),
        ("Avg Duration (s)", org.get("avg_duration_sec", 0)),
        ("Pages/Session", org.get("pages_per_session", 0)),
        ("Bounce Rate (%)", org.get("bounce_rate", 0)),
    ]
    for name, val in metrics:
        db.execute(
            "INSERT OR REPLACE INTO snapshots (date, source, metric_name, metric_value, metric_numeric) VALUES (?,?,?,?,?)",
            (today, "GA4", name, str(val), safe_float(val)),
        )
    # Organic daily trends
    for r in ga4_data.get("organic_daily", []):
        d = r.get("dims", {}).get("date", today)
        m = r.get("metrics", {})
        db.execute(
            "INSERT OR REPLACE INTO ga4_organic (date, sessions, total_users, new_users, avg_duration_sec, pages_per_session, bounce_rate) VALUES (?,?,?,?,?,?,?)",
            (d, safe_int(m.get("sessions")), safe_int(m.get("totalUsers")),
             safe_int(m.get("newUsers")), safe_float(m.get("averageSessionDuration")),
             safe_float(m.get("screenPageViewsPerSession")), safe_float(m.get("bounceRate")) * 100),
        )
    # Trends
    for period, key in [("weekly", "trend_weekly"), ("monthly", "trend_monthly")]:
        t = ga4_data.get(key, {})
        if t:
            db.execute(
                "INSERT OR REPLACE INTO ga4_trend (date, period, recent_sessions, prior_sessions, change_pct) VALUES (?,?,?,?,?)",
                (today, period, t.get("recent", 0), t.get("prior", 0), t.get("change_pct", 0)),
            )
    # Channels
    for c in ga4_data.get("channel_summary", []):
        d = c.get("dims", {})
        m = c.get("metrics", {})
        db.execute(
            "INSERT OR REPLACE INTO ga4_channels (date, channel, sessions, total_users, bounce_rate, avg_duration_sec) VALUES (?,?,?,?,?,?)",
            (today, d.get("sessionDefaultChannelGroup", ""),
             safe_int(m.get("sessions")), safe_int(m.get("totalUsers")),
             safe_float(m.get("bounceRate")) * 100, safe_float(m.get("averageSessionDuration"))),
        )
    # Geo
    for g in ga4_data.get("geo_top10", []):
        db.execute(
            "INSERT OR REPLACE INTO ga4_geo (date, country, sessions, total_users, new_users, avg_duration_sec, pages_per_session, bounce_rate) VALUES (?,?,?,?,?,?,?,?)",
            (today, g.get("country", ""),
             safe_int(g.get("sessions")), safe_int(g.get("totalUsers")),
             safe_int(g.get("newUsers")), safe_float(g.get("averageSessionDuration")),
             safe_float(g.get("screenPageViewsPerSession")), safe_float(g.get("bounceRate")) * 100),
        )
    org_cnt = len(ga4_data.get("organic_daily", []))
    ch_cnt = len(ga4_data.get("channel_summary", []))
    geo_cnt = len(ga4_data.get("geo_top10", []))
    print(f"  GA4: {org_cnt} 天 + {ch_cnt} 渠道 + {geo_cnt} 国家 入仓")

def ingest_bing(db, bing_data, today):
    if not bing_data:
        return
    kw = bing_data.get("keywords", [])
    total_cl = sum(k.get("clicks", 0) for k in kw)
    total_impr = sum(k.get("impressions", 0) for k in kw)
    b_ctr = total_cl / total_impr * 100 if total_impr else 0
    metrics = [
        ("总关键词数", len(kw)),
        ("总点击", total_cl),
        ("总展示", total_impr),
        ("整体CTR", round(b_ctr, 1)),
    ]
    for name, val in metrics:
        db.execute(
            "INSERT OR REPLACE INTO snapshots (date, source, metric_name, metric_value, metric_numeric) VALUES (?,?,?,?,?)",
            (today, "Bing", name, str(val), safe_float(val)),
        )
    # Keywords
    for k in kw[:500]:
        db.execute(
            "INSERT OR REPLACE INTO bing_keywords (date, query, clicks, impressions, ctr, position) VALUES (?,?,?,?,?,?)",
            (today, k.get("query", ""), k.get("clicks", 0),
             k.get("impressions", 0), k.get("ctr", 0), k.get("position", 0)),
        )
    # Pages
    for p in bing_data.get("pages", []):
        db.execute(
            "INSERT OR REPLACE INTO bing_pages (date, url, clicks, impressions) VALUES (?,?,?,?)",
            (today, p.get("url", ""), p.get("clicks", 0), p.get("impressions", 0)),
        )
    # Crawl
    crawl = bing_data.get("crawl_daily", [])
    for c in crawl[-30:]:
        d = today  # Bing API doesn't return dates, use today
        db.execute(
            "INSERT OR REPLACE INTO bing_crawl (date, in_index, crawled_pages, crawl_errors, code_4xx, code_5xx, blocked_robots, in_links) VALUES (?,?,?,?,?,?,?,?)",
            (d, c.get("InIndex", 0), c.get("CrawledPages", 0),
             c.get("CrawlErrors", 0), c.get("Code4xx", 0),
             c.get("Code5xx", 0), c.get("BlockedByRobotsTxt", 0),
             c.get("InLinks", 0)),
        )
    print(f"  Bing: {len(kw)} 关键词 + {len(bing_data.get('pages',[]))} 页面 + {len(crawl)}天爬虫 入仓")

# ── 导出 ──────────────────────────────────────────────────
def export_tables(db, today):
    export_dir = WAREHOUSE_DIR / today
    export_dir.mkdir(parents=True, exist_ok=True)

    tables = [
        "snapshots", "gsc_keywords", "gsc_countries",
        "ga4_organic", "ga4_trend", "ga4_channels", "ga4_geo",
        "bing_keywords", "bing_pages", "bing_crawl",
    ]

    for table in tables:
        rows = db.execute(f"SELECT * FROM {table} WHERE date = ?", (today,)).fetchall()
        if not rows:
            continue
        cols = [desc[0] for desc in db.execute(f"PRAGMA table_info({table})").fetchall()]

        # CSV 导出 (通用，所有数仓都支持)
        csv_path = export_dir / f"{table}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)
        print(f"  📄 {csv_path.name} ({len(rows)} rows)")

    # 尝试 Parquet 导出 (需要 pyarrow)
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq

        for table in tables:
            rows = db.execute(f"SELECT * FROM {table} WHERE date = ?", (today,)).fetchall()
            if not rows:
                continue
            cols = [desc[0] for desc in db.execute(f"PRAGMA table_info({table})").fetchall()]
            data = {col: [row[i] for row in rows] for i, col in enumerate(cols)}
            pa_table = pa.table(data)
            pq_path = export_dir / f"{table}.parquet"
            pq.write_table(pa_table, str(pq_path))
            print(f"  📦 {pq_path.name} ({len(rows)} rows)")
    except ImportError:
        print("  ⚠️  pyarrow 未安装，跳过 Parquet 导出 (CSV 已生成)")
        print("  💡 安装: pip3 install pyarrow")

    # README
    readme = export_dir / "README.md"
    readme.write_text(f"""# Warehouse Export — {today}

## 表结构

| 表 | 说明 | 入仓方式 |
|---|------|---------|
| snapshots | 每日指标快照 (GSC/GA4/Bing) | CSV |
| gsc_keywords | GSC 关键词排名 | CSV |
| gsc_countries | GSC 分国家 | CSV |
| ga4_organic | GA4 自然搜索日趋势 | CSV |
| ga4_trend | GA4 周/月环比 | CSV |
| ga4_channels | GA4 全渠道 | CSV |
| ga4_geo | GA4 分国家 | CSV |
| bing_keywords | Bing 关键词 | CSV |
| bing_pages | Bing 页面 | CSV |
| bing_crawl | Bing 爬虫日统计 | CSV |

## 云数仓摄入示例

### BigQuery
```bash
bq load --source_format=CSV \\
  lovart_trident.snapshots \\
  gs://my-bucket/{today}/snapshots.csv
```

### Snowflake
```sql
COPY INTO lovart_trident.snapshots
FROM @my_stage/{today}/snapshots.csv
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```

### PostgreSQL
```sql
\\copy snapshots FROM '{today}/snapshots.csv' CSV HEADER;
```

## 本地查询
```bash
sqlite3 trident_data.db "SELECT * FROM snapshots ORDER BY date DESC LIMIT 20"
```
""")
    print(f"  📋 {readme.name}")

# ── main ──────────────────────────────────────────────────
def main():
    today = date.today().isoformat()
    print(f"🗄️  Trident → Warehouse — {today}")
    print(f"   DB: {DB_PATH}")

    # Init
    print("\n📂 初始化 SQLite 数仓...")
    db = init_db()

    # Ingest
    print("\n📥 数据入仓:")
    gsc = load_json("gsc-full.json")
    ga4 = load_json("ga4-full.json")
    bing = load_json("bing-full.json")

    if not any([gsc, ga4, bing]):
        print("  ❌ 无数据文件，请先运行 gsc_fetch.py / ga4_fetch.py / bing_fetch.py")
        sys.exit(1)

    ingest_gsc(db, gsc, today)
    ingest_ga4(db, ga4, today)
    ingest_bing(db, bing, today)

    db.commit()

    # Stats
    total = db.execute("SELECT COUNT(*) FROM snapshots WHERE date = ?", (today,)).fetchone()[0]
    print(f"\n📊 本日共 {total} 条快照记录入仓")

    # Export
    print(f"\n📤 导出到 {WAREHOUSE_DIR / today}/")
    export_tables(db, today)

    db.close()
    print(f"\n✅ 数仓更新完成")

if __name__ == "__main__":
    main()
