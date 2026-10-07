---
type: session-log
session_date: 2026-09-18
session_slug: plugin-ecosystem
status: ready
---

# Session Log — 插件生态（v2 基座）

## 设计理念
用户洞察：**MFlow 是底层基座，开源工具通过插件协议接入**。不需要硬编码每个集成——只需要做好协议，社区/用户写 manifest + entry 即可。

## 扩展内容

### ① plugin_check.py 扩展（3 种 → 6 种类型）
- 原：source / publisher / template
- 新增：**gate**（质量门禁）/ **transform**（文本处理）/ **analyzer**（报告/仪表）
- 每类的 entry 函数约定：source=collect() / publisher=publish() / gate=check() / transform=transform() / analyzer=analyze()

### ② 已注册的 7 个标准插件

| 插件 | 类型 | 功能 |
|------|:---:|------|
| readability-gate | gate | Flesch Reading Ease 评分（EN ≤12 为通过）|
| schema-generator | transform | 从 md 草稿自动生成 Schema.org JSON-LD |
| link-suggester | analyzer | 从 17.5k 库 TF-IDF 排序找内链建议 |
| geo-check-gate | gate | AI 可引用性检查（统计密度/Q&A/来源）|
| lang-check-gate | gate | 多语言规范（简繁/字形/标点/残留）|
| quota-check-gate | gate | 数量预算检查（字数/H2/FAQ/列表）|
| sample-source | source | 示例数据源 |

### ③ marketplace 可安装包（5 个）
rss-source / webhook-publisher / readability-gate / schema-generator / link-suggester

## 验证
- plugin_check.py 六项检查 → 全部 PASS ✓
- `GET /api/plugins` → installed 7 / available 5 ✓
- 线上部署 ✓
