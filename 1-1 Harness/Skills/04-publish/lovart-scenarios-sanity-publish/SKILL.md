---
name: lovart-scenarios-sanity-publish
description: 将本地 Scenarios 试点 JSON（composite-v2，category scenario，draft-*，noIndex）安全同步到 Sanity production。用于 Scenarios 发布、scenarios-storyline、import-scenarios-drafts、marketing-director、brand-manager、ecommerce-operator 试点稿。
disable-model-invocation: true
---

# Lovart Scenarios → Sanity 发布

> Support-only：本 skill 只作为 `lovart-sanity-publish` 的内部 Scenarios 执行管道，不直接响应用户发布请求。用户提到发布/同步/import Scenarios 时，先进入 `lovart-sanity-publish` 父入口。

## 铁律（与 Product/Features/Tools 一致）

- 只用 **`import --missing`**（批量经 `import-scenarios-drafts.js --import`；单篇经 `import-page.js --import`）
- ❌ 不 `sanity deploy`、不改 schema、不 `--replace`、不删文档
- projectId **`o11tm2qe`** · dataset **`production`**
- 试点稿保持 **`seo.noIndex: true`**，slug 前缀 **`draft-`**
- `url_path` 使用 **`/scenario/`**（单数，非 `/scenarios/`）

## SSOT

- 生产指南：[`SCENARIOS-PRODUCTION.md`](../../../../1-3 Content Gen/Page Gen/Refresh-Page/SCENARIOS-PRODUCTION.md)
- 故事线：[`scenarios-storylines.json`](../../../../1-3 Content Gen/Page Gen/Refresh-Page/scenarios-storylines.json)
- Step 0：[`PAGE-BRIEF.md`](../../../../1-3 Content Gen/Page Gen/Refresh-Page/PAGE-BRIEF.md)
- 路由：[`scenarios-routing.md`](../lovart-content-creation-orchestrator/references/scenarios-routing.md)

## 试点范围

**14 篇 canonical**（每条故事线 × 1 选题）— 见 `MANIFEST-PILOT.md` / `scenarios-storylines.json` → `pilotAssignments`。  
不做 5×14 全矩阵；各主题新建页时优先用该主题的首选故事线即可。

## 快速流程

```bash
cd "1-4 Dev/lovart.sanity.studio"
DRAFTS="../../1-3 Content Gen/Page Gen/Pages/drafts/scenarios-storyline/Scenarios"
DRAFTS_EN="$DRAFTS/en"

# 1. 批量预检（试点稿需 --include-drafts）
node scripts/preflight-content.js --type composite-v2 --dir "$DRAFTS" --include-drafts

# 2. 仅 14 篇 canonical dry-run / 导入
node scripts/import-scenarios-drafts.js --pilot-only --dry-run
node scripts/import-scenarios-drafts.js --pilot-only --import
```

## 单篇导入

```bash
node scripts/import-page.js "$DRAFTS_EN/draft-ecommerce-operator-scenarios-a-en.json" --dry-run
node scripts/import-page.js "$DRAFTS_EN/draft-brand-manager-scenarios-cinematic-en.json" --import
```

## 导入后 url_path 修补（仅 patch 字段）

已导入但 `url_path` 仍为 `/scenarios/` 时：

```bash
node scripts/patch-scenarios-draft-urls.js --dry-run
node scripts/patch-scenarios-draft-urls.js --apply
```

## 门禁话术

先输出 dry-run 摘要（篇数、slug 样例、noIndex）→ 等用户 **`import confirmed`** → 再 `--import`。

## 试点规模

| 类型 | 篇数 | 清单 |
|------|------|------|
| **Canonical 试点** | **14** | `MANIFEST-PILOT.md` |
| 历史矩阵扩展（可选） | 70 | `MANIFEST.md`（不再新增） |

## 线上验证

```groq
count(*[_type=="compositePage" && category=="scenario" && slug.current match "draft-*"])
*[_type=="compositePage" && category=="scenario" && slug.current match "draft-*"]{_id,slug,url_path,"noIndex":seo.noIndex}[0...5]
```
