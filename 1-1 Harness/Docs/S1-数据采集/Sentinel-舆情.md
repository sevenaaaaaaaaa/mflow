# Sentinel 舆情 — 模块上手

| 项 | 内容 |
|----|------|
| **适用角色** | 品牌/ORM、SEO、内容策略 |
| **前置** | `1-4 Dev/scripts/sentinel/config.yaml` |
| **脚本 SSOT** | `collect.py`、`report.py`、`daily.py` |
| **Skill** | `40-sentinel/lovart-sentinel` |
| **规则** | [AGENTS.md Part D](../../AGENTS.md) |

---

## 最小命令

```bash
# 采集
python3 "1-4 Dev/scripts/sentinel/collect.py" --source all

# 日报
python3 "1-4 Dev/scripts/sentinel/daily.py"

# 报告
python3 "1-4 Dev/scripts/sentinel/report.py"
```

---

## 产出路径

`1-2 Insight/Lovart ORM/{daily,weekly,monthly,quarterly,annual,raw}/`

---

## 验收标准

- 日报 8 板块齐全（摘要、搜索舆情、社媒、品牌、用户画像、风险机遇、SWOT、行动清单）
- 含 i18n 内容生产雷达（`i18n_keyword_intelligence` 数据源）
- 竞品词库 265+36 子串匹配

---

## 常见坑

| 坑 | 说明 |
|----|------|
| 只跑 GSC 当舆情 | Sentinel 需多源（SERP/社媒/评价） |
| 日报缺 i18n 雷达 | 见 `seo_report_standards.py` i18n 检查项 |

---

## 进阶

详见 [使用说明-各环节.md §三](../../使用说明-各环节.md)
