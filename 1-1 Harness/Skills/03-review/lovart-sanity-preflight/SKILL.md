---
name: lovart-sanity-preflight
description: >-
  Deprecated alias — use lovart-content-quality-gates for all preflight/import QA.
  Kept for pipeline triggers that mention "sanity-preflight".
---

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-sanity-preflight/SKILL.md` |

# lovart-sanity-preflight（已合并）

**请改用统一入口**：[`lovart-content-quality-gates`](../lovart-content-quality-gates/SKILL.md)

**发布策略（import 前）**：[`first-run-and-incremental-policy.md`](../lovart-sanity-publish/references/first-run-and-incremental-policy.md) — 首次认证+login+拉线上参照；已有 `_id` 不全量重发；日常仅 `--missing`。

本 Skill 仅保留触发词兼容；命令、维度、退出码均以 **quality-gates** 为准。

## 快速跳转

| 场景 | 命令 |
|------|------|
| Blog MD 预检 | `node scripts/preflight-content.js --type blog-md` |
| Blog NDJSON | `node scripts/preflight-content.js --ndjson ~/lovart/import-blog-*.ndjson` |
| 导入后 Blog | `npx sanity exec scripts/verify-blog-publish.js --with-user-token` |
| Tools/Features | quality-gates §L1 |

## 与 Pipeline

```
lovart-content-quality-gates (L1 preflight)
  → lovart-sanity-publish (convert + import)
  → verify-blog-publish (L2)
```

勿再维护本文件中的重复命令表。
