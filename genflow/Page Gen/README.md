# Tools 正式源（composite-v2）

> **修订：2026-05-29**  
> **SSOT 路径**：`1-3 Content Gen/Page Gen/Pages/Tools/`（**编辑工作区**；**线上真相源** = Sanity production）  
> **线上状态**：**528/528 Tools 均为 composite-v2**（2026-05-29 重导出审计）；6 篇 `draft-*` 仅线上 noIndex，不参与 sync  
> **故事线**：[`STORYLINES.md`](../Refresh-Page/STORYLINES.md)（T1–T5、N5）；线上 reflow 长链用 **`T-long`**  
> **发布**：`convert-tools.js`（仅 v2）→ `import --missing`  
> **弃用**：`pages-legacy/Tools/`、`Lovart Dev/Pages/Tools/` — 不再作为输入

## 目录约定

```
Pages/Tools/
├── _index.json              # slug + language → 数字 id（沿用现网 _id）
├── {lang}/{slug}-{lang}.json
└── README.md
```

语言目录：`en`、`zh`、`zh-TW`、`de`、`fr`、`it`、`ja`、`ko`、`pt`、`ru`

## JSON 必填（composite-v2）

| 字段 | 说明 |
|------|------|
| `schemaVersion` | 固定 `"composite-v2"` |
| `storylineTemplate` | `T1`–`T5`、`N5` 或线上 reflow 的 **`T-long`** |
| `category` | `"tool"` |
| `slug` / `language` | 与文件名 `{slug}-{lang}.json` 一致 |
| `bodyJson` | Refresh-Page v2 section 数组（`prompt-launcher`、`hero-split`、`faq` 等） |

**不再接受** legacy 模块：`heroSection`、`contentSection`、`threeColumnSection`、`textImageSection`、`testimonialSection`、`faqSection`。

## 与线上对齐（production → 本地）

**原则**：本地 JSON 是草稿与批量编辑区；**以 production 为准**。发布前改本地、发布后或定期 **pull 回本地**，避免线下迁移与线上漂移。

### 何时执行

| 场景 | 动作 |
|------|------|
| 换设备 / 首次克隆 | 必跑（见下） |
| **发布 Tools 到 production 之后** | 建议同会话内 sync 一次 |
| **每周或 Sprint 开始前** | 定期 sync（无本地未提交改动时） |
| Studio 手改、他人 import、线上 reflow | 先 sync 再改本地 |

### 命令（顺序固定）

**推荐（单入口）**：

```bash
bash "1-4 Geo Dev/automation/tools-pull/pull-tools-from-production.sh"
# 或 studio 内：node scripts/pull-tools-from-production.js
```

等价分步：

```bash
cd "…/1-4 Geo Dev/lovart.sanity.studio"
node scripts/export-composite-production.js   # 刷新 production-export.json
node scripts/sync-tools-from-production.js    # 覆盖写入 Page Gen/Pages/Tools/
```

**macOS 每周定时**：`1-4 Geo Dev/automation/tools-pull/install.sh`  
**Cursor Automation**：`1-5 Harness/automation/cursor-tools-pull-automation.md`

可选核对：`node scripts/audit-composite-v2-production.js --input "…/production-export.json"`（`tool:*:legacy` 应为 0）。

**最近一次 sync**：**522** 篇 v2 写入本地；跳过 **6** 篇 `draft-*`（`seo.noIndex`）；**0** legacy。

## 常用命令

```bash
node scripts/preflight-content.js --type tools --strict
node scripts/convert-tools.js --lang en --dry-run
node scripts/import-page.js "../1-3 Content Gen/Page Gen/Pages/Tools/en/{slug}-en.json" --import
```
