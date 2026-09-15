---
type: stage-sop/s3
version: 1.0
updated: 2026-07-05
scope: "profile-lovart-creation"
tools: [opencode, claude]
status: active
path: 1-1 Harness/Docs/S3-内容创作/Tools-Features-发布.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Tools / Features 发布 — 模块上手

| 项 | 内容 |
|----|------|
| **适用角色** | 落地页制作、SEO、内容工程 |
| **内容源** | `1-3 Content Gen/Page Gen/Pages/Tools/`、`Pages/Features/` |
| **线上真相源** | Tools：**production**（每周 pull 到本地） |
| **Skill** | `lovart-tools-sanity-publish`、`lovart-features-sanity-publish` |

---

## Tools（composite-v2 only）

```bash
cd "1-4 Dev/lovart.sanity.studio"
node scripts/preflight-content.js --type tools --strict
node scripts/convert-tools.js --lang en --dry-run
npx sanity dataset import ~/lovart/import-tools.ndjson production --missing
npx sanity exec scripts/verify-composite.js --with-user-token -- --type tool --sample 20
```

**本地对齐线上**：

```bash
bash "1-4 Dev/automation/tools-pull/pull-tools-from-production.sh"
```

---

## Features

```bash
node scripts/preflight-content.js --type features --sample-urls 8
node scripts/convert-features.js --lang en --dry-run
# import + verify 同上
```

---

## 验收

- legacy Tools 计数为 0（pull 报告 `legacy: 0`）
- `url_path` 为 `/features/` 非 `/tools/`（Features，AB-U01）
- composite 图 HTTP 404 = 0（`audit-composite-images-404.js`）

---

## 常见坑

| 坑 | AB-ID |
|----|-------|
| legacy Tools 进生产 | AB-S04 / strict preflight |
| Features SEO 写 /tools/ | AB-U01 |
| 221 篇手改 marker | AB-P04 repair-local |
