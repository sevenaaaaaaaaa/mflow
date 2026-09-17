---
type: storyline/features
version: 1.0
updated: 2026-07-05
scope: "profile-lovart-creation"
tools: [opencode, claude, cursor]
status: legacy
path: 1-1 Harness/08-storyline/FEATURES-PRODUCTION 2.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Features 页面生产指南

> 依据 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) §4.1 四条 Features 故事线，生成 13 段 `bodyJson` 草稿。

---

## A. 线上英文版全量重排（做法 A：内容重排）

把线上 **现存** 英文 Features 页（legacy 五段式）重排成新的 13 段故事线，**复用原文案/图片**，缺口派生或占位。**全程本地，不触线上。**

### 流水线

在 `1-4 Dev/lovart.sanity.studio/` 下（输出落在工作区内，避免沙箱写 `~/lovart`）：

```bash
PULL="$(cd ../.. && pwd)/Lovart Dev/Pages/drafts/_pull"

# 1) 只读拉取线上全量英文 Features 页（含 bodyJson + seo）
LOVART_PULL_DIR="$PULL" node scripts/export-feature-pages.js --lang en

# 2) 全量重排为新 13 段故事线（本地草稿，noIndex，不导入）
LOVART_PULL_DIR="$PULL" node scripts/reflow-feature-pages.js
#   --limit 5            只跑前 5 篇
#   --slug ai-logo-maker 只跑某页
#   --storyline features-main  强制统一故事线
```

- 输入：`_pull/composite/features-full/*.json`
- 输出：`_pull/features-reflow/Features/en/<slug>-en.json` + `_manifest.json` + `_report.md`

### 现状基线（2026-06-03 拉取）

- 线上英文 Features 页 **239 篇**，其中 **9 篇为 `draft-` 测试页**（已排除），实际重排 **229 篇**。
- 全部为 legacy（无 `schemaVersion`），主流是五段式：`centeredInputSection + threeColumnSection + featureGridSection + testimonialSection + faqSection`。
- ⚠️ **线上重复 slug**：`ai-video-generator` 同时存在 `ai-video-generator-en`（旧）与 `ai-video-generator-v2-en`（6/1 较新）两个文档，slug 相同。重排保留较新的；建议线上删除/合并其一。

### 故事线分配（按页内容自动判定）

| 信号 | 选用故事线 |
|------|------------|
| 特性网格 ≥ 6 项 | `features-grid-bento6`（225 页） |
| 特性网格 3–5 项 | `features-grid-feature`（2 页） |
| 其它 | `features-main`（2 页） |

> `features-tab-b` 为纯布局变体，无内容信号，不自动分配；需要时用 `--storyline features-tab-b` 或逐页指定。

### 复用 vs 占位（13 段）

平均复用率约 **38%（5/13）**，复用的是真实 legacy 内容：

- ✅ **真实复用**：`prompt-launcher`、`workflow-horizontal`、网格位（`bento-6`/`feature-grid`）、`testimonial`、`faq`、部分 `cta-default`
- 🟡 **从特性项派生**（非空，但是重排自原网格）：`capability-tabs`、`bento-2`、`feature-detail`、`hero-split` 标题
- 🔴 **通用占位，需补真实物料**：`hero-split` 配图、`comparison-table`、`pricing-block`、`cluster-block-dense`（用例位）

详见每次生成的 `_report.md` 占位频次表。

### 预检（结构）

```bash
node -e '
const fs=require("fs"),path=require("path");
const {typeSequenceForStoryline}=require("./scripts/lib/features-storylines");
const DIR=process.env.DIR;
for(const f of fs.readdirSync(DIR).filter(x=>x.endsWith(".json"))){
  const p=JSON.parse(fs.readFileSync(path.join(DIR,f)));const s=JSON.parse(p.bodyJson);
  if(s.map(x=>x.type).join()!==typeSequenceForStoryline(p.storyline).join())console.log("ORDER",f);
  if(s.length!==13)console.log("LEN",f,s.length);
}'  # DIR=.../features-reflow/Features/en
```

当前结果：**顺序/长度 0 问题、空内容数组 0**。

### 覆盖线上：备份 + 小批 + 全量（须你单独授权，B4 默认禁止）

线上文档已存在，覆盖须 `sanity dataset import --replace`（按 `_id` 替换）。`AGENTS.md` B4 默认禁止，**须你逐次授权**。

> ⚠️ 线上 `_id` 命名不统一：部分为 `<slug>-en`，部分为 `features-<slug>-en`。
> 重排草稿里带 `reflowSourceId`＝真实线上 `_id`，覆盖脚本据此精确命中，**不要**自行拼 `_id`。

**Step 0 — 生成覆盖 NDJSON（本地，安全，不写线上）**

```bash
export LOVART_PULL_DIR="$(cd ../.. && pwd)/Lovart Dev/Pages/drafts/_pull"

# 冒烟批（默认前 2 篇）
node scripts/prepare-overwrite-batch.js --limit 2
# 指定页
node scripts/prepare-overwrite-batch.js --slug ai-ad-thumbnail-generator,nano-banana-concept-art-workflow
# 全量 229
node scripts/prepare-overwrite-batch.js --all
```

输出：`_pull/features-reflow/_overwrite/overwrite-*.ndjson`（`noIndex:false`、`_id` 已对齐）。脚本会打印下面 3 条命令但**不执行**。

**Step 1 — 备份（必做，可回滚）**

```bash
npx sanity dataset export production "$LOVART_PULL_DIR/features-reflow/_overwrite/backup-prod-$(date +%F).tar.gz"
```

**Step 2 — 小批覆盖（先 2 篇）**

```bash
npx sanity dataset import "<overwrite-smoke/pick.ndjson>" production --replace
```

到 `https://www.lovart.ai/features/<slug>` 验证渲染与 13 段顺序无误。

**Step 3 — 全量覆盖**

确认小批无误后，对 `--all` 的 NDJSON 重复 Step 2。

**回滚**：如有问题，用 Step 1 备份恢复：
`npx sanity dataset import "<backup-prod-*.tar.gz>" production --replace`

> 相关脚本：`scripts/prepare-overwrite-batch.js`（生成）、`scripts/export-feature-pages.js`（备份前的只读快照）。

---

## B. 新主题模板生成（做法 B：手写物料）

## 故事线（4 条）

| ID | 差异点 |
|----|--------|
| `features-main` | 基准：cluster 网格位 + Tab 布局 A |
| `features-tab-b` | Tab 布局 B（tab 顺序 / autoplay 不同） |
| `features-grid-feature` | 序 2 改为 `feature-grid` |
| `features-grid-bento6` | 序 2 改为 `bento-6` |

每条均为 **13 段**，顺序见 `STORYLINE-BY-DIRECTION.md` 全量表。

## 一键生成（脚本）

在 `1-4 Dev/lovart.sanity.studio/` 下：

```bash
# 全部主题 × 全部故事线（当前 2 主题 × 4 线 = 8 页）
node scripts/generate-features-storyline-drafts.js

# 只看将生成什么
node scripts/generate-features-storyline-drafts.js --dry-run

# 单主题
node scripts/generate-features-storyline-drafts.js --theme ai-logo-maker

# 单故事线
node scripts/generate-features-storyline-drafts.js --storyline features-main
```

**输出目录：**

`Lovart Dev/Pages/drafts/features-storyline/Features/en/`

- slug 形如：`draft-ai-logo-maker-features-main`
- `seo.noIndex: true`（不覆盖现网）
- `url_path` 无 `/en/` 前缀

## 生成后流程

```bash
# 1. 预检
node scripts/preflight-content.js --dir "../Pages/drafts/features-storyline/Features/en"

# 2. 单篇 dry-run（不写 Sanity）
node scripts/import-page.js ../Pages/drafts/features-storyline/Features/en/draft-ai-logo-maker-features-main-en.json --dry-run

# 3. 确认后导入（须用户授权）
node scripts/import-page.js ../Pages/drafts/features-storyline/Features/en/draft-ai-logo-maker-features-main-en.json --import
```

## 对话生成（Cursor Skill）

见 `Skills/refresh-page-page-generator/`：先确认故事线 ID 与 type 顺序，再填物料。

## 当前试点主题

| theme | 说明 |
|-------|------|
| `ai-logo-maker` | Logo 功能页 |
| `ai-sales-deck-ppt-generator` | 销售 Deck 功能页 |

新增主题：在 `sanity-studio/scripts/lib/features-theme-content.js` 的 `THEMES` 中注册并实现物料。

## 相关文件

| 文件 | 作用 |
|------|------|
| `scripts/generate-features-storyline-drafts.js` | 生成入口 |
| `scripts/lib/features-storylines.js` | 故事线 type 序列 |
| `scripts/lib/features-theme-content.js` | 主题文案与 section 组装 |
| `preview-data.json` | 字段参考 |
| `README.md` | 字段字典 |
