# Features 页面生产指南

> 依据 [STORYLINE-BY-DIRECTION.md](./STORYLINE-BY-DIRECTION.md) §4.1 四条 Features 故事线，生成 13 段 `bodyJson` 草稿。

---

## composite-v2 生产基线（2026-06-05）

项目 `o11tm2qe` / `production`，审计报告：[`1-7 Output/composite-v2-audit-2026-06-05.md`](../../../1-7 Output/composite-v2-audit-2026-06-05.md)

| 范围 | 状态 |
|------|------|
| **Features 全语言** | **1943** 篇全部 **composite-v2**（legacy **0**） |
| **英文 Features** | **247** 篇 v2（含 `ai-video-generator-en` 与 `ai-video-generator-v2-en` 双文档，均已 v2） |
| **Tools 全语言** | **528** 篇全部 v2；英文 6 篇 `draft-*` 测试页已 `seo.noIndex` |
| **跨语言结构对齐** | **1696** 对 slug×语言与英文 section `type` 序列一致（`crosslang-verify.json`） |
| **多语言文案在地化** | 残留英文段落各语言降至 **~0.2%**（zh 7.7%，基数小）；串级同 EN 约 6–8%（品牌词/英文示例 prompt/人名等合理保留） |

### 多语言在地化做法（2026-06-05 补完）

首轮 i18n reflow 仅叠回 legacy 旧页已有译文（5 段式），v2 新增 8 类段落残留英文（段落残留 ~61%）。补完方案：

1. **复用已有译文**：`hero-split` 标题/描述 ← 本地化页面 `title`/`description`；`capability-tabs`/`bento-2` ← 主网格（`bento-6`/`cluster-block-dense`）已译条目按 EN 标题→索引映射回填。
2. **固定模板套用词表**：`feature-detail`/`comparison-table`/用例 `cluster-block-dense`/`pricing-block`/`cta-default`/段落标题 ← [`scripts/lib/i18n-glossary.json`](../../../dev/lovart.sanity.studio/scripts/lib/i18n-glossary.json)（9 语言固定模板串 + `{FEATURE}` 特性名插值；品牌词 Lovart / Brand Kit / AI Design Agent 保留英文）。
3. 脚本：[`scripts/localize-residual-sections.js`](../../../dev/lovart.sanity.studio/scripts/localize-residual-sections.js)（原地修复 i18n 草稿）→ 同 `_id` patch。

```bash
node scripts/localize-residual-sections.js --lang ja,zh-TW,zh,de,fr,it,ko,pt,ru
node scripts/patch-composite-bodyjson-batch.js --manifest "../../1-7 Output/composite-v2-audit/i18n-patch-ja.json" --apply
```

### 数量缺口（推进中，2026-06-05 更新）

SSOT 基准修正为**可索引 EN 237 篇**（剔除 9 篇 `noIndex` 的 `draft-*` 测试页，不应复制到多语言）。缺口清单：[`1-7 Output/composite-v2-audit/i18n-gap-manifest.json`](../../../1-7 Output/composite-v2-audit/i18n-gap-manifest.json)。

| 语言 | 现有/SSOT | 剩余缺口 | 备注 |
|---|---|---|---|
| **zh-TW 繁中** | **237/237 ✅** | 0 | 9 篇简→繁 S2T 转换（opencc twp + 台湾用词覆盖）+ 3 新译 |
| **ja 日文** | **237/237 ✅** | 0 | 15 篇 EN→ja（video-agent 簇共享词典 + 7 独立页） |
| pt 葡文 | 208/237 | 29 | video-agent 簇 8 篇已上线，余 29 待译 |
| zh 简中 | 46/237 | 194 | Tier1 41 篇全完（见下）；待 Tier2 103 / Tier3 91 |
| it 意 | 196/237 | 41 | 待译 |
| ru 俄 | 205/237 | 32 | 待译 |
| fr 法 | 210/237 | 27 | 待译 |
| de 德 | 216/237 | 21 | 待译 |
| ko 韩 | 220/237 | 17 | 待译 |

- 非 zh 语言缺口并集仅 **50 个唯一 slug**（多为新增 video-agent/seedance/nano-banana 等 storyline 页），其中 18 个 zh 已译可借力。
- **zh 简体中文** Tier1 全部 41 篇已上线（zh feature **2→46**，含本轮 3 篇 `ai-video-optimization`/`mcot-engine`/`quick-poster-generation-by-lovart`）。后续待补 Tier2（103）/Tier3（91）。高优先级候选：[`1-7 Output/composite-v2-audit/zh-priority-candidates.json`](../../../1-7 Output/composite-v2-audit/zh-priority-candidates.json)。
  - 泛化翻译流水线：`derive-skeleton.js --lang <L>`（任意语言骨架+glossary 模板+`_names.json` 本地化特性名+抽取真实 EN 串）→ 人工译 `_dict/<slug>.json`（高重叠簇用 `_shared/<cluster>.json`，如 video-agent 簇 87 串覆盖 8 变体）→ `apply-translations.js --lang <L>`（套用共享+逐页词典，按目标文字脚本/对 EN 源做残留校验）→ `create-composite-docs.js --apply`。
  - 繁中专用：`convert-zh-to-twp.js`（简中成品页 → 繁中，opencc cn→twp + 台湾营销用词覆盖 `scripts/lib/s2t.js`）。
- Tools 各语言均 52，实质已对齐（英文多出 6 篇为 `noIndex` draft）。
- **图片**：当前复用 legacy 旧图（`assets-persist.lovart.ai`），填充率 ~98%，但每页唯一图/图槽仅 ~44.7%（同图复用），差异化图片为后续缺口。

脚本根目录：`dev/lovart.sanity.studio/scripts/`

```bash
STUDIO="dev/lovart.sanity.studio"
cd "$STUDIO"

# 审计（线上导出 + 本地 preflight + 合并报告）
node scripts/export-composite-production.js
node scripts/audit-composite-v2-production.js --input "../../1-7 Output/composite-v2-audit/production-export.json"
node scripts/merge-composite-v2-audit.js

# 英文：同 _id patch bodyJson（features-reflow 草稿）
node scripts/build-composite-v2-id-map.js
node scripts/patch-composite-bodyjson-batch.js --manifest "../../1-7 Output/composite-v2-audit/en-features-id-map.json" --apply

# 多语言：EN 结构 SSOT + 本地化文案 overlay
node scripts/reflow-feature-pages-i18n.js --lang ja,zh-TW,zh,de,fr,it,ko,pt,ru
node scripts/patch-composite-bodyjson-batch.js --manifest "../../1-7 Output/composite-v2-audit/i18n-patch-ja.json" --apply

# 跨语言验收
node scripts/verify-composite-v2-crosslang.js
```

i18n 草稿输出：`$LOVART_PULL_DIR/i18n-reflow/Features/{lang}/`

> ⚠️ `_pull/` 已从 `Pages/drafts/` 迁移到 `~/Documents/Lovart Local Dev/Output/Page Gen/_pull/`。
> 脚本通过 `LOVART_PULL_DIR` 环境变量读取，默认值由 `local-dev-env.sh` 提供。

---

## A. 线上英文版全量重排（做法 A：内容重排）

把线上 **现存** 英文 Features 页（legacy 五段式）重排成新的 13 段故事线，**复用原文案/图片**，缺口派生或占位。**全程本地，不触线上。**

### 流水线

在 `dev/lovart.sanity.studio/` 下（输出落在工作区内，避免沙箱写 `~/lovart`）：

```bash
# _pull 已外置到运行层，通过 LOVART_PULL_DIR 环境变量引用
source "$(cd ../.. && pwd)/1-Project/Lovart MFlow/dev/automation/local-dev-env.sh"
PULL="$LOVART_PULL_DIR"

# 1) 只读拉取线上全量英文 Features 页（含 bodyJson + seo）
LOVART_PULL_DIR="$PULL" node scripts/export-feature-pages.js --lang en

# 2) 全量重排为新 13 段故事线（本地草稿，noIndex，不导入）
LOVART_PULL_DIR="$PULL" node scripts/reflow-feature-pages.js
#   --limit 5            只跑前 5 篇
#   --slug ai-logo-maker 只跑某页
#   --storyline features-main  强制统一故事线
```

- 输入：`$LOVART_PULL_DIR/composite/features-full/*.json`
- 输出：`$LOVART_PULL_DIR/features-reflow/Features/en/<slug>-en.json` + `_manifest.json` + `_report.md`

### 现状基线（2026-06-05，已上线）

- 线上英文 Features **247** 篇已全部 **composite-v2**（13 段故事线）。
- 本地 `features-reflow/Features/en/` **290** 篇 v2 草稿；**287** 篇已按同 `_id` patch `bodyJson` 上线。
- ⚠️ **重复 slug**：`ai-video-generator` 仍有 `ai-video-generator-en` 与 `ai-video-generator-v2-en` 两个文档（均已 v2）；合并/下线其一需单独决策。

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
export LOVART_PULL_DIR="${LOVART_PULL_DIR:-$HOME/Documents/Lovart Local Dev/Output/Page Gen/_pull}"

# 冒烟批（默认前 2 篇）
node scripts/prepare-overwrite-batch.js --limit 2
# 指定页
node scripts/prepare-overwrite-batch.js --slug ai-ad-thumbnail-generator,nano-banana-concept-art-workflow
# 全量 229
node scripts/prepare-overwrite-batch.js --all
```

输出：`$LOVART_PULL_DIR/features-reflow/_overwrite/overwrite-*.ndjson`（`noIndex:false`、`_id` 已对齐）。脚本会打印下面 3 条命令但**不执行**。

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

在 `dev/lovart.sanity.studio/` 下：

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
| `scripts/audit-composite-v2-production.js` | 线上 compositePage v2/legacy 审计 |
| `scripts/reflow-feature-pages-i18n.js` | 多语言 EN 结构 SSOT + 文案 overlay |
| `scripts/patch-composite-bodyjson-batch.js` | 同 `_id` 批量 patch `bodyJson` |
| `scripts/verify-composite-v2-crosslang.js` | 跨语言 section 序列对齐验收 |
| `scripts/lib/i18n-en-ssot.js` | EN→i18n 结构 overlay 逻辑 |
| `scripts/generate-features-storyline-drafts.js` | 新主题草稿生成入口 |
| `scripts/lib/features-storylines.js` | 故事线 type 序列 |
| `scripts/lib/features-theme-content.js` | 主题文案与 section 组装 |
| `preview-data.json` | 字段参考 |
| `README.md` | 字段字典 |
