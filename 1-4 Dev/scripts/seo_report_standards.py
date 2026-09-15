#!/usr/bin/env python3
"""
Lovart SEO 报告强制标准（代码 SSOT）

与以下文档保持同步：
- Lovart/AGENTS.md Part A
- Skills/lovart-trident-data-engine/SKILL.md

Agent 生成任何 SEO 报告前必须遵守；脚本启动时应 print_pre_run_checklist()。
"""

from __future__ import annotations

# 用户于 2026-05 提供的 OKR 目标；每次跑报告前 Agent 须向用户确认是否更新
OKR_EFFECTIVE_MONTH = "2026-05"

# 报告类型 → (当前周期描述, 环比基准描述)
# 原则：同粒度、紧邻上一周期；跨月合法（例：5 月第 1 周 vs 4 月最后 1 周）
COMPARE_BASELINE: dict[str, tuple[str, str]] = {
    "daily": ("报告日 D", "前日 D-1（同等 1 日窗口）"),
    "natural_weekly": ("上周一～上周日", "上上周一～上上周日（同等 7 日）"),
    "review_weekly": ("上周三～本周二", "上上周三～上周二（同等 7 日复盘窗）"),
    "monthly": ("报告月 YYYY-MM 全月", "上一自然月全月（例：2026-05 月报 vs 2026-04）"),
    "bimonthly": (
        "连续两自然月（例：2026-03~04）",
        "紧邻上两自然月（例：2026-03~04 vs 2026-01~02）",
    ),
    "quarterly": ("报告季 YYYY-QX 全季", "上一自然季全季（例：2026-Q2 vs 2026-Q1）"),
    "annual": ("报告年 YYYY 全年", "上一自然年全年（例：2026 vs 2025）"),
}

# GSC 关键词相关：每个时间段必须完整输出 + 环比
KEYWORD_GSC_METRICS = ("clicks", "impressions", "ctr")
KEYWORD_GSC_MOM = ("clicks_mom", "impressions_mom", "ctr_mom")  # 绝对值+百分比

# 任何细分（Top N、地区、目录、品牌/非品牌、竞品分层）必须含占比
SEGMENT_SHARE_COLUMNS = ("click_share", "impression_share")  # 点击占比 + 曝光占比

# 非关键词维度（GA4 等）同样必须环比
ALL_DIMENSIONS_REQUIRE_MOM = True

# i18n 内容生产：日报和周/月报都不能只服务英语主工作流
I18N_TARGET_LOCALES = ("zh", "zh-TW", "ja", "ko", "de", "fr", "ru", "pt", "it")
I18N_DAILY_REQUIRED_FIELDS = (
    "locale",
    "query_count",
    "clicks",
    "impressions",
    "ctr",
    "localized_pages",
    "opportunity_queries",
    "content_tasks",
)
I18N_CONTENT_PRODUCTION_REQUIREMENTS = (
    "每日 SEO/Sentinel 报告必须包含 i18n 内容生产雷达：按 locale 展示查询数、点击、曝光、CTR、可识别本地化页面覆盖。",
    "i18n 内容候选必须引用各自语言或地区的查询证据，不得只由英文页面优先级决定。",
    "高曝光低 CTR 本地语言查询进入翻译/新建页面候选池，并标注 locale、query、impressions、CTR。",
    "有本地语言查询但缺少可识别本地化页面时，标记为 i18n 内容缺口。",
    "中文、繁中、日语、韩语、德语、法语、俄语、葡语、意语均需在日报中保留观察位；无数据也要能解释为 0 或缺口。",
)

# 月报 V2（seo_monthly_v2.py + seo_monthly_extras.py）— 与 AGENTS.md A0d 同步
MONTHLY_REPORT_SCRIPT = "1-4 Dev/scripts/seo_monthly_v2.py"
MONTHLY_EXTRAS_MODULE = "1-4 Dev/scripts/seo_monthly_extras.py"
MONTHLY_SNAPSHOT_DIR = "1-4 Dev/Output/Data Ingestion/monthly-snapshots"
SEO_GEO_DATA_DIR = "1-2 Insight/From Datawork"
SEO_GEO_FILE_PATTERN = "{YYYY-MM} SEO GEO.xlsx"
MONTHLY_METRICS_DIR = "1-2 Insight/Trident Insights/reports/monthly/.metrics"

MONTHLY_V2_REQUIRED_SECTIONS = (
    "一、核心洞察",
    "二、OKR 月达成看板",
    "三、SEO Dashboard",
    "4.4 点击增长",
    "4.5 曝光增长",
    "4.6 CTR 变化",
    "4.7 点击下滑",
    "4.8 Bing 关键词",          # §四 Bing 分渠道
    "4.12–4.15 Bing movers",    # §四 Bing 四节 movers
    "4.16 跨引擎词重叠",         # §四 GSC∩Bing
    "5.4 自然搜索引擎拆分",      # §五 GA4 sessionSource
    "6.4 引擎对比",             # §六 DataWorks Google vs Bing
    "C-Bing/D-Bing/E-Bing",     # §三 Dashboard Bing 卡
    "7B Bing",                  # §七 Bing 品牌/非品牌
    "8.6–8.11 Bing 竞品",       # §八 Bing 竞品明细+对比
    "9.4–9.6 Bing 页面目录",    # §九 Bing 页面目录
    "10B Bing",                 # §十 Bing 页面 Top（双月）
    "11.10 Bing 分地区",        # §十一 GA4 近似
    "引擎差异",                  # 各节引擎对比 💡
    "六、自然搜索产品数据",
    "十一、分地区表现",
    "年均对比",
)

# 固定大标题顺序（一～十三）
MONTHLY_V2_SECTION_ORDER = (
    "一、核心洞察",
    "二、OKR 月达成看板",
    "三、SEO Dashboard",
    "四、关键词分层明细",
    "五、自然搜索用户数据（GA4）",
    "六、自然搜索产品数据（DataWorks 平台拆解）",
    "七、品牌词 vs 非品牌词",
    "八、竞品非品牌词覆盖",
    "九、页面目录流量",
    "十、页面查询明细",
    "十一、分地区表现",
    "十二、TODO",
    "十三、Bing 补充数据",
)

INDEXING_CORPUS_TOTAL = 20_000
INDEXING_FOOTNOTE = (
    "收录主口径：全月有搜索曝光 URL 数 / 语料库总量（默认 20,000）。"
    "禁止用 page API rowLimit=1000 或 sitemap submitted 作分母。"
)

MONTHLY_AGENT_MISTAKES = (
    "章节顺序乱/编号重复 — 须严格按固定顺序 一～十三，子号随大号",
    "核心洞察缺顶部三层 TL;DR（流量/关键词/执行）或每要点首句加粗结论 — 须『一句话结论』可扫读",
    "核心洞察正文密密麻麻堆全量数字 — 每点只留核心数据+环比（≤2 个数），其余『详见 §X / 卡 X』",
    "核心洞察未按三层叙事（产品→收录/词/页→综合下一步）",
    "关键词仅 Top 点击分层，缺曝光/CTR/三者环比及 §4.4–4.7 movers",
    "§四–§十一 仅出 GSC/Google，未分渠道 — 须 整体+Google(GSC)+Bing（§4.8–4.16/5.4/6.4/§三 C-Bing~E-Bing/7B/8.6–8.11/9.4–9.6/10B/11.10），每节带『💡 引擎差异』；Bing 周榜按月聚合；分地区 Google=GSC、Bing=GA4 country×sessionSource 近似",
    "地区仅 Top5 双表，缺每大区分区月报（双月+全环比）与 Top15 词",
    "无 📊 年均对比（2025 月均 vs 2026 YTD 月均）",
    "重跑时手删整份月报而非改脚本 + --render-only",
    "分区 💡 品牌占比恒为 0%（region_stats 传参错误）",
    "收录率固定 1.43%（1000÷70k）— 须 lovart_indexing_metrics 分页口径",
    "lavort 等非品牌 Top10 — 品牌 regex 只改 lovart_brand_match.py",
    "SEO Dashboard 单表混排 — 须 §三 卡 A–F 分开",
)


def print_pre_run_checklist(
    report_type: str,
    curr_period: str,
    prev_period: str,
    *,
    okr_effective: str = OKR_EFFECTIVE_MONTH,
) -> None:
    """脚本启动时打印；Agent 跑报告前应已确认 OKR。"""
    baseline = COMPARE_BASELINE.get(report_type, ("当前周期", "紧邻上一同粒度周期"))
    print("─" * 60)
    print("  SEO 报告标准检查（强制）")
    print(f"  类型: {report_type}")
    print(f"  当前: {curr_period}")
    print(f"  环比: {prev_period}")
    print(f"  规则: {baseline[0]} vs {baseline[1]}")
    print("  关键词: 每段必须含 点击+曝光+CTR + 三者环比")
    print("  细分: Top/地区/目录/品牌拆分 必须含 点击占比+曝光占比")
    print("  i18n: 日报必须含 locale 查询雷达与内容生产候选，不能只优化英语主工作流")
    print(f"  OKR: 当前脚本默认生效月 {okr_effective}（Agent 跑前须问用户是否更新）")
    if report_type == "monthly":
        print("  月报 V2: 固定顺序 一核心洞察→二OKR→三Dashboard→…→十三Bing；编号不重复（见 AGENTS.md A0d）")
        print(f"  脚本: {MONTHLY_REPORT_SCRIPT} [--resume | --render-only | --refresh-indexing]")
        print(f"  DataWorks: {SEO_GEO_DATA_DIR}/{SEO_GEO_FILE_PATTERN} + sheet monthly_dedup")
    if report_type == "bimonthly":
        print("  双月报 V2: 结构同月报 V2；数据=两月快照合并；对比=上两月合并窗")
        print("  脚本: 1-4 Dev/scripts/historical/bimonth_with_tier.py --year YYYY --b N")
        print(f"  批处理: report_batch_runner.sh render-bimonthly --from YYYY-B1 --to YYYY-B3")
    print("─" * 60)


def monthly_post_run_checklist() -> list[str]:
    """生成月报后 Agent 自检项（打印或逐项核对）。"""
    return [
        "固定顺序 一～十三、大/小编号连续不重复",
        "§一 核心洞察：三段结论（全链路/关键词/执行）+（一）（二）展开；GEO 付费率对比、收录暴增、内容池；OKR 在 §二",
        "核心洞察为三层叙事（自然搜索产品→收录/关键词/页面→综合下一步）",
        "§二 OKR 月达成看板（访问 UV 用 all_uv；Sessions 参考行）",
        "§三 SEO Dashboard 为卡 A–F + C-Bing/D-Bing/E-Bing（F 含 Bing 竞品行）",
        "§4.1 含曝光列与曝光/CTR 环比列；§4.4–4.7 Google movers + §4.12–4.15 Bing movers + §4.16 跨引擎词重叠",
        "§四–§十一 分渠道：整体概览 + §4.8–4.16 + 5.4 + 6.4 + 7B + 8.6–8.11 + 9.4–9.6 + 10B + 11.10，每节带「💡 引擎差异」",
        "§十一 Google=GSC 分地区 + §11.10 Bing GA4 近似（脚注口径诚实）",
        "§四~九、十一节含「💡」",
        "含「年均对比」备注行",
        "§11.0 大区最好/持平/最差总览存在",
        "每个大区含「分区月报（双月）」：CTR/占比有环比、Top15 双月表",
        "收录率约 40%+ 量级（非 1.43%）；lavort 不在非品牌 Top10",
        "全文约 1000 行（<600 行多为旧版缩水）",
        "含 §六 DataWorks 平台拆解 或月去重待产出提示",
        "OKR 脚注：GA4 Sessions vs DataWorks UV 不可直接对比",
        "i18n 内容生产：按 locale 给出查询证据、机会词、本地化页面覆盖与候选任务",
    ]


def bimonthly_post_run_checklist() -> list[str]:
    """双月报自检：与月报 V2 同结构，周期为上双月 vs 本双月。"""
    base = monthly_post_run_checklist()
    return [
        "文首为「双月复盘报告」+ 双月周期 vs 上双月",
        "§三/§四 列标签为上双月窗 vs 本双月窗（如 1–2月 vs 3–4月）",
        "GSC/GA4 数值为两月合并（非单月）",
    ] + base


def i18n_daily_report_checklist() -> list[str]:
    """每日 SEO/Sentinel 报告必须满足的 i18n 内容生产检查项。"""
    return [
        "包含「i18n 内容生产雷达」或等价章节",
        "覆盖目标 locale：zh、zh-TW、ja、ko、de、fr、ru、pt、it",
        "每个有数据的 locale 至少包含 query_count、clicks、impressions、CTR",
        "展示高曝光低 CTR 的本地语言机会词，并包含 query、impressions、CTR",
        "对有查询需求但缺少本地化页面覆盖的 locale 输出内容缺口",
        "自动 TODO 中包含 i18n 内容生产候选，且引用对应语言/地区查询证据",
    ]


def okr_confirmation_reminder() -> str:
    return (
        f"OKR 目标默认沿用 {OKR_EFFECTIVE_MONTH} 版本（见 AGENTS.md A4）。"
        " 生成报告前请向用户确认：OKR 是否要更新？"
    )
