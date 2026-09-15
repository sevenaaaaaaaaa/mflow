# SEO 报告 — 模块上手

| 项 | 内容 |
|----|------|
| **适用角色** | SEO 负责人、数据分析师 |
| **前置** | GSC/GA4 凭据、Python 依赖 |
| **脚本 SSOT** | `1-4 Dev/scripts/seo_monthly_v2.py`、`weekly_review_v3.py`、`1-4 Dev/scripts/seo_monthly_extras.py` |
| **Skill** | `lovart-trident-data-engine` |
| **规则 SSOT** | [AGENTS.md Part A](../../AGENTS.md) |

---

## 最小命令

```bash
# 月报
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month 2026-05

# 自然周报
python3 "1-4 Dev/scripts/weekly_review_v3.py" --type natural

# 复盘周报
python3 "1-4 Dev/scripts/weekly_review_v3.py"
```

---

## 产出路径

- 月报：`1-2 Insight/Trident Insights/reports/monthly/Lovart-SEO-YYYY-MM.md`
- 周报：`1-2 Insight/Trident Insights/reports/weekly/`

---

## 验收标准

- 报告含环比（见 AGENTS A0）
- 关键词表：点击 + 曝光 + CTR + 三者环比
- `## 四、关键词分层明细` 顶部包含 **Multi SEO 渠道全貌（收口监测）**，说明 Google、Bing/IndexNow、DuckDuckGo/Yahoo Japan、Naver、百度、Brave/Yandex 等渠道的当前口径。
- i18n 内页不单列进 `other`（页面分类与 `classify_page()` 一致）
- 跑月报前确认 OKR 版本（默认 2026-05）

---

## 常见坑

| 坑 | AB-ID / 说明 |
|----|--------------|
| GSC 2 天延迟未标注 | 窗口末尾拉至最后可用日 |
| 只出 snapshot 无环比 | 违反 AGENTS A0 |
| 页面 92% 落入 other | 检查 `classify_page` 与 i18n 章节 |
| 把 Multi SEO 样本当官方 KPI | 只有 Google/GSC 与 Bing/Bing Webmaster 是官方数据；DuckDuckGo/Yahoo Japan 走 Bing+IndexNow 覆盖说明，Brave/国内搜索/Yandex 不进近期执行 KPI |

---

## 进阶

- `--resume` / `--render-only` 断点续跑
- Multi SEO 收口结论见 `1-1 Harness/Skills/multi-seo-closeout-2026-06-07.md`
- 详见 [使用说明-各环节.md §二](../../使用说明-各环节.md)
