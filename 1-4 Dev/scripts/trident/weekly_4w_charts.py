#!/usr/bin/env python3
"""Lovart SEO 四周趋势折线图 — W1:7/14-20 W2:7/21-27 W3:7/28-8/3 W4:8/4-10

5 组图:
1. GSC 整体曝光/点击/CTR (country 维度)
2. 品牌 vs 非品牌 曝光/点击/CTR (query 维度)
3. UV→注册、UV→付费 数 (SEO+GEO / SEO / GEO)
4. 点击转UV / UV转注册 / 注册转付费 率 (SEO+GEO / SEO / GEO)
5. 新增付费数趋势 (SEO+GEO / SEO / GEO)
输出: reports/weekly/Lovart-4w-charts-*.png
"""
import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams["font.family"] = ["PingFang SC", "Hiragino Sans GB", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lovart_brand_match import is_brand

GSC = json.load(open("/tmp/gsc_4w.json"))
DW = json.load(open("/tmp/dataworks_4w.json"))
BING = json.load(open(Path(__file__).resolve().parents[3] / "1-2 Insight/Trident Insights/reports/bing-full.json"))

WEEKS = ["W1", "W2", "W3", "W4"]
LABELS = ["7/14-20", "7/21-27", "7/28-8/3", "8/4-10"]
OUT_DIR = Path(__file__).resolve().parents[3] / "1-2 Insight/Trident Insights/reports/weekly"

# ---------- 数据准备 ----------
# GSC country (整体)
gsc_country = {}
for w in WEEKS:
    rows = GSC["data"][w]["country"]
    c = sum(r["clicks"] for r in rows); i = sum(r["impressions"] for r in rows)
    gsc_country[w] = {"clicks": c, "impr": i, "ctr": c / i * 100 if i else 0}

# GSC query 品牌/非品牌
gsc_brand = {}
for w in WEEKS:
    rows = GSC["data"][w]["query"]
    br = [r for r in rows if is_brand(r["keys"][0])]
    nb = [r for r in rows if not is_brand(r["keys"][0])]
    def st(rs):
        c = sum(r["clicks"] for r in rs); i = sum(r["impressions"] for r in rs)
        return {"clicks": c, "impr": i, "ctr": c / i * 100 if i else 0}
    gsc_brand[w] = {"brand": st(br), "nonbrand": st(nb)}

# Bing 点击 (traffic_daily 按窗口)
BING_WIN = [("W1", "2026-07-14", "2026-07-20"), ("W2", "2026-07-21", "2026-07-27"),
            ("W3", "2026-07-28", "2026-08-03"), ("W4", "2026-08-04", "2026-08-10")]
bing_clicks = {}
for name, s, e in BING_WIN:
    bing_clicks[name] = sum(r["clicks"] for r in BING["traffic_daily"] if s <= r["date"] <= e)

# DataWorks 4 周 (日均)
dw = {w: DW[w] for w in WEEKS}

def series(bucket, key):
    return [dw[w][bucket]["daily_avg"][key] for w in WEEKS]

# 转化率
def rates(bucket):
    uv = series(bucket, "uv"); reg = series(bucket, "new_uv"); pay = series(bucket, "pay_uv")
    clicks = [gsc_country[w]["clicks"] + bing_clicks[w] for w in WEEKS]
    c2uv = [uv[i] / clicks[i] * 100 if clicks[i] else 0 for i in range(4)]  # 点击→UV: UV/点击
    uv2reg = [reg[i] / uv[i] * 100 if uv[i] else 0 for i in range(4)]
    reg2pay = [pay[i] / reg[i] * 100 if reg[i] else 0 for i in range(4)]
    return c2uv, uv2reg, reg2pay

# ---------- 图 1: GSC 整体 ----------
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig.suptitle("最近四周 GSC 整体曝光 / 点击 / CTR（country 维度全量）", fontsize=15, fontweight="bold")
axes[0].plot(LABELS, [gsc_country[w]["impr"] for w in WEEKS], "o-", color="#2563eb", linewidth=2.5, markersize=8)
axes[0].set_ylabel("曝光"); axes[0].set_title("曝光 (Impressions)")
for i, v in enumerate([gsc_country[w]["impr"] for w in WEEKS]):
    axes[0].annotate(f"{v:,}", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=10)
axes[1].plot(LABELS, [gsc_country[w]["clicks"] for w in WEEKS], "s-", color="#f59e0b", linewidth=2.5, markersize=8)
axes[1].set_ylabel("点击"); axes[1].set_title("点击 (Clicks)")
for i, v in enumerate([gsc_country[w]["clicks"] for w in WEEKS]):
    axes[1].annotate(f"{v:,}", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=10)
axes[2].plot(LABELS, [gsc_country[w]["ctr"] for w in WEEKS], "^-", color="#dc2626", linewidth=2.5, markersize=8)
axes[2].set_ylabel("CTR %"); axes[2].set_title("点击率 (CTR)")
axes[2].yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
for i, v in enumerate([gsc_country[w]["ctr"] for w in WEEKS]):
    axes[2].annotate(f"{v:.1f}%", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=10)
plt.tight_layout()
f1 = OUT_DIR / "Lovart-4w-chart-1-gsc-overall.png"
plt.savefig(f1, dpi=150, bbox_inches="tight"); plt.close()
print("图1:", f1)

# ---------- 图 2: 品牌 vs 非品牌 ----------
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig.suptitle("最近四周 品牌词 vs 非品牌词（GSC query 维度）", fontsize=15, fontweight="bold")
for ax, key, title in ((axes[0], "impr", "曝光"), (axes[1], "clicks", "点击"), (axes[2], "ctr", "点击率")):
    bv = [gsc_brand[w]["brand"][key] for w in WEEKS]
    nv = [gsc_brand[w]["nonbrand"][key] for w in WEEKS]
    ax.plot(LABELS, bv, "o-", color="#2563eb", linewidth=2.5, markersize=8, label="品牌词")
    ax.plot(LABELS, nv, "s-", color="#f59e0b", linewidth=2.5, markersize=8, label="非品牌词")
    ax.set_ylabel(title); ax.set_title(f"{title} — 品牌 vs 非品牌")
    ax.legend()
    for i, v in enumerate(bv):
        ax.annotate(f"{v:,.0f}" if key != "ctr" else f"{v:.1f}%", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
    for i, v in enumerate(nv):
        ax.annotate(f"{v:,.0f}" if key != "ctr" else f"{v:.1f}%", (i, v), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=9)
    if key == "ctr":
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
plt.tight_layout()
f2 = OUT_DIR / "Lovart-4w-chart-2-brand-nonbrand.png"
plt.savefig(f2, dpi=150, bbox_inches="tight"); plt.close()
print("图2:", f2)

# ---------- 图 3: UV→注册、UV→付费 数 ----------
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig.suptitle("最近四周 UV→注册 与 UV→付费 数（日均）", fontsize=15, fontweight="bold")
for ax, (bucket, label) in zip(axes, (("seo_geo", "SEO+GEO"), ("seo", "SEO"), ("geo", "GEO"))):
    reg = series(bucket, "new_uv"); pay = series(bucket, "pay_uv")
    ax.plot(LABELS, reg, "o-", color="#2563eb", linewidth=2.5, markersize=8, label="注册数 (new_uv)")
    ax.plot(LABELS, pay, "s-", color="#dc2626", linewidth=2.5, markersize=8, label="付费数 (new_pay_uv)")
    ax.set_title(f"{label} — UV→注册 / UV→付费（日均）")
    ax.set_ylabel("人数"); ax.legend()
    for i, v in enumerate(reg):
        ax.annotate(f"{v:,.0f}", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
    for i, v in enumerate(pay):
        ax.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=9)
plt.tight_layout()
f3 = OUT_DIR / "Lovart-4w-chart-3-uv-reg-pay.png"
plt.savefig(f3, dpi=150, bbox_inches="tight"); plt.close()
print("图3:", f3)

# ---------- 图 4: 转化率 ----------
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig.suptitle("最近四周 转化率：点击→UV / UV→注册 / 注册→付费（日均）", fontsize=15, fontweight="bold")
for ax, (bucket, label) in zip(axes, (("seo_geo", "SEO+GEO"), ("seo", "SEO"), ("geo", "GEO"))):
    c2uv, uv2reg, reg2pay = rates(bucket)
    ax.plot(LABELS, c2uv, "o-", color="#2563eb", linewidth=2.5, markersize=8, label="点击→UV")
    ax.plot(LABELS, uv2reg, "s-", color="#f59e0b", linewidth=2.5, markersize=8, label="UV→注册")
    ax.plot(LABELS, reg2pay, "^-", color="#dc2626", linewidth=2.5, markersize=8, label="注册→付费")
    ax.set_title(f"{label} — 转化率（日均）")
    ax.set_ylabel("%"); ax.legend()
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
    for i in range(4):
        ax.annotate(f"{c2uv[i]:.1f}%", (i, c2uv[i]), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
        ax.annotate(f"{uv2reg[i]:.1f}%", (i, uv2reg[i]), textcoords="offset points", xytext=(0, -16), ha="center", fontsize=8)
        ax.annotate(f"{reg2pay[i]:.2f}%", (i, reg2pay[i]), textcoords="offset points", xytext=(-22, -30), ha="center", fontsize=8)
plt.tight_layout()
f4 = OUT_DIR / "Lovart-4w-chart-4-funnel-rates.png"
plt.savefig(f4, dpi=150, bbox_inches="tight"); plt.close()
print("图4:", f4)

# ---------- 图 5: 新增付费数 ----------
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig.suptitle("最近四周 新增付费数（日均 new_pay_uv）", fontsize=15, fontweight="bold")
for ax, (bucket, label) in zip(axes, (("seo_geo", "SEO+GEO"), ("seo", "SEO"), ("geo", "GEO"))):
    pay = series(bucket, "pay_uv")
    ax.plot(LABELS, pay, "o-", color="#dc2626", linewidth=2.5, markersize=8)
    ax.set_title(f"{label} — 新增付费 UV（日均）")
    ax.set_ylabel("付费人数")
    for i, v in enumerate(pay):
        ax.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=10)
plt.tight_layout()
f5 = OUT_DIR / "Lovart-4w-chart-5-new-pay-uv.png"
plt.savefig(f5, dpi=150, bbox_inches="tight"); plt.close()
print("图5:", f5)

# ---------- 数据摘要打印 ----------
print("\n=== 数据摘要 ===")
print("GSC country:", {w: f"{gsc_country[w]['clicks']:,}clicks {gsc_country[w]['ctr']:.1f}%" for w in WEEKS})
print("Bing clicks:", {w: f"{bing_clicks[w]:,}" for w in WEEKS})
for w in WEEKS:
    b, nb = gsc_brand[w]["brand"], gsc_brand[w]["nonbrand"]
    print(f"{w}: 品牌 {b['clicks']:,}clicks {b['ctr']:.1f}% | 非品牌 {nb['clicks']:,}clicks {nb['ctr']:.1f}%")
for bucket, label in (("seo_geo", "SEO+GEO"), ("seo", "SEO"), ("geo", "GEO")):
    c2uv, uv2reg, reg2pay = rates(bucket)
    print(f"{label} 转化率: 点击→UV {[f'{x:.1f}%' for x in c2uv]} | UV→注册 {[f'{x:.1f}%' for x in uv2reg]} | 注册→付费 {[f'{x:.2f}%' for x in reg2pay]}")
