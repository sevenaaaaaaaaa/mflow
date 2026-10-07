# 数据采集（Trident）— 模块上手

| 项 | 内容 |
|----|------|
| **适用角色** | 数据对接分析师、SEO |
| **脚本 SSOT** | `dev/scripts/trident/`（采集）· `seo_monthly_v2.py` / `weekly_review_v3.py`（报告） |
| **Skill** | `trident-data-engine` |
| **产出** | `dev/Output/Data Ingestion/`、`insight-data/` |

---

## GSC 采集示例

```bash
python3 "dev/scripts/seo_monthly_v2.py" --month 2026-05
# 或 Harness Trident 脚本（配置见 gsc-api-setup-guide.md）
```

Trident 原始采集：

```bash
python3 "dev/scripts/trident/gsc_fetch.py" --month 2026-05
```

---

## GA4 / Bing

见 Harness `trident-data-engine/scripts/ga4_fetch.py`、`bing_fetch.py`。

---

## 验收

- 快照 JSON 写入 `Output/Data Ingestion/` 或报告目录
- 月报 `--resume` 可续跑
- 凭据不提交 git

---

## 角色手册

[For-数据对接分析师.md](../03-角色手册/For-数据对接分析师.md)

---

## 常见坑

| 坑 | 说明 |
|----|------|
| 路径指到 Harness 旧副本 | 统一查 `dev/scripts` |
| OAuth 过期 | 重跑 `gsc_auth.py` / 配置指南 |
