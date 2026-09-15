# SOP — Lovart Sanity Blog·Features·Tools 换设备交接与首次运行

> **文件名**：`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`  
> **一页速查**：[`Sanity-Blog-最小交接包.md`](./Sanity-Blog-最小交接包.md)  
> **搜索别名**：`handoff-and-onboarding` · `Sanity 交接` · `Blog Sanity 换设备`  
> **给接手人 / 新机器的第一份 Sanity 文档**。三条管道 SSOT 入口：[`lovart-sanity-content-publish`](../../lovart-sanity-content-publish/SKILL.md)。  
> **增量策略**：[`first-run-and-incremental-policy.md`](./first-run-and-incremental-policy.md)  
> **GROQ 速查**：[`groq-snippets-sanity-blog-features-tools.md`](./groq-snippets-sanity-blog-features-tools.md)  
> **P1**：[`sanity-es-language-policy.md`](./sanity-es-language-policy.md) · [`sanity-frontend-apps-lovart.md`](./sanity-frontend-apps-lovart.md)

---

## 1. 交接包：你需要复制什么

> **只复制 `1-1 Harness/Skills/` 不够**。必须同时有 `1-4 Dev/lovart.sanity.studio/`（脚本）、`1-4 Dev/lovart.sanity.studio/Sanity Blog/`、`1-4 Dev/Pages/`（Features/Tools JSON），否则 convert / preflight 找不到文件。

### 1.1 必须复制

| 路径（相对 vault `1-Project/`） | 说明 |
|--------------------------------|------|
| `1-4 Dev/lovart.sanity.studio/` | Blog/Features/Tools 脚本、`.env.example`；**勿复制他人 `.env`** |
| `1-4 Dev/lovart.sanity.studio/Sanity Blog/` | Blog MD 源 |
| `1-3 Content Gen/Page Gen/Pages/Features/`、`1-3 Content Gen/Page Gen/Pages/Tools/` | Features / Tools JSON（Tools：**composite-v2 正式源**） |
| `1-1 Harness/Skills/lovart-sanity-*`、`1-1 Harness/Skills/lovart-content-quality-gates/` | Agent Skills |
| `1-1 Harness/Skills/lovart-features-sanity-publish/`、`1-1 Harness/Skills/lovart-tools-sanity-publish/` | |
| `Lovart/.cursor/rules/lovart-sanity-content-pipeline.mdc` | Cursor 规则（强烈建议） |

### 1.2 勿复制 / 勿提交 git

| 项 | 说明 |
|----|------|
| `.env` | 含 API token；每人各自在 manage.sanity.io 申请 |
| `~/lovart/*.ndjson` | 本地生成物，新机重新 convert |
| `blog-taxonomy.json` | 新机 `sync-blog-taxonomy` 重新生成 |
| `node_modules/` | 新机 `npm install` |

### 1.3 Sanity 账号与 Token 权限（交接人必办）

| 步骤 | 动作 |
|------|------|
| 1 | [manage.sanity.io](https://www.sanity.io/manage) 项目 **`o11tm2qe`** 邀请接手人（Developer 或 Editor） |
| 2 | 接手人创建 **Editor API Token** → `.env` 的 `SANITY_STUDIO_API_TOKEN`（`dataset import` 写 production） |
| 3 | 接手人 `npx sanity login`（`sanity exec`、verify、sync-taxonomy 用 OAuth，与 API token **不同**） |

| 操作 | 认证 |
|------|------|
| `npx sanity dataset import … --missing` | `.env` → `SANITY_STUDIO_API_TOKEN` |
| `npx sanity exec … --with-user-token` | `npx sanity login` |
| 只读 GROQ / 部分 verify | 可选 `SANITY_STUDIO_READ_TOKEN` |

---

## 2. 新机环境（第一次打开终端）

```bash
node -v    # ≥ 18，推荐 LTS 20/22
npm -v     # sanity-studio 用 npm（有 package-lock.json，勿混 pnpm）

cd "…/1-4 Dev/lovart.sanity.studio"
npm install

cp .env.example .env
# 填入 SANITY_STUDIO_API_TOKEN

npx sanity login
node scripts/check-publish-deps.js
```

**vault 不在默认 iCloud 路径时**（见 §3）：

```bash
export LOVART_ROOT="/你的路径/1-Project/Lovart"
export LOVART_OUT_DIR="$HOME/lovart"   # 可选
node scripts/check-publish-deps.js
```

可选：Features/Tools 机器翻译 → `~/.mavis/config.yaml`（`minimax-cn`）

---

## 3. LOVART_ROOT 与路径（换设备必看）

脚本通过 `scripts/lib/lovart-paths.js` 解析路径：

| 变量 | 默认 | 作用 |
|------|------|------|
| `LOVART_ROOT` | `…/1-Project/Lovart Dev` | Blog MD（`Sanity Blog/`） |
| Tools 正式源 | `…/1-Project/1-3 Content Gen/Page Gen/Pages/Tools/` | composite-v2；`lovart-paths.pagesTools()`；换设备后跑 `sync-tools-from-production.js` |
| ~~pages-legacy/Tools~~ | **已弃用** | 勿再作发布输入 |
| `LOVART_OUT_DIR` | `~/lovart` | NDJSON、manifest、report |

**若 vault 不在默认路径**：设置 `export LOVART_ROOT=…` 后再跑 convert / preflight / check-publish-deps。

输出目录 `~/lovart/` 与 vault 位置无关；**不要**从旧机复制 NDJSON。

---

## 4. Sanity Blog·Features·Tools 首次运行顺序（勿跳步）

```
.env + sanity login
    → check-publish-deps
    → check-sanity-auth（勿加 --require-taxonomy）
    → sync-blog-taxonomy（Blog：拉线上 category/tag 映射到本地）
    → check-sanity-auth --require-taxonomy（Blog convert 前验收，可选）
    → convert-* --dry-run（本地缺口报告；Features/Tools 非整库拉 production）
    → 小批量 convert + import --missing
    → 日常：仅增量
```

### Blog 试跑

```bash
cd sanity-studio
npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token
node scripts/check-sanity-auth.js --require-taxonomy

node convert.js --lang en --batch-size 10 --dry-run
node convert.js --lang en --batch-size 10
npx sanity dataset import ~/lovart/import-blog-en-batch01.ndjson --dataset production --missing
SINCE_MINUTES=30 npx sanity exec scripts/verify-blog-publish.js --with-user-token
```

### Features / Tools 试跑

```bash
node scripts/convert-features.js --dry-run    # 或 convert-tools.js
# 读 ~/lovart/import-features-report.json（本地缺口，非线上正文）
node scripts/import-page.js "../Pages/Features/en/graphic-design-en.json" --dry-run
node scripts/import-page.js "../Pages/Features/en/graphic-design-en.json" --import
```

import 前可用 [GROQ](./groq-snippets-sanity-blog-features-tools.md) 查线上是否已有 `_id`。

---

## 5. 日常增量（默认模式）

| ✅ 做 | ❌ 不做（除非用户明确要求） |
|-------|---------------------------|
| 只 convert **本轮变更** 或 `--lang xx` / 单篇 | 无 `--lang` 全库 4000+ MD + 全 manifest import |
| `import --missing` | `--replace` |
| 线上已有 `_id` → 跳过 | 重复 import「以防万一」 |
| import 后 fix-category-refs、link-translations | `sanity deploy`、改 `schemaTypes/` |

---

## 6. 双 Studio 架构（Sanity 勿 deploy 错目录）

| 目录 | 角色 | 内容发布 Agent |
|------|------|----------------|
| **`1-4 Dev/lovart.sanity.studio/`** | Blog/Features/Tools **convert·import cwd** | ✅ 在此跑脚本 |
| **`1-4 Dev/lovart.sanity.studio/`** | 线上 **Schema Studio**（compositePage 等） | ❌ 勿 `sanity deploy`（除非 schema 团队授权） |

- 数据集唯一目标：**`production` @ `o11tm2qe`**
- Studio 列表导航以 **`category`** 为准（`feature` / `tool` …）；`sourceType` 为 legacy 字段
- 前端 `apps/lovart` **不在本 vault**；主站渲染契约需另取前端仓库

---

## 7. Skills 同步（opencode ↔ vault）

若使用 OpenCode 软链同步 Skills：

```bash
cd "…/1-Project/Skills"
bash sync-skills.sh --dry-run
bash sync-skills.sh              # vault → opencode
# bash sync-skills.sh --to-opencode  # 按脚本注释方向调整
```

Sanity **内容**不通过 sync-skills 同步；内容在 `1-4 Dev/lovart.sanity.studio/Sanity Blog/` 与 `1-4 Dev/Pages/`。

---

## 8. 文档阅读顺序（约 30 分钟）

1. **本文件**（Sanity Blog·Features·Tools 换设备）  
2. [`first-run-and-incremental-policy.md`](./first-run-and-incremental-policy.md)  
3. [`sanity-cli-setup.md`](./sanity-cli-setup.md) + [`blog-taxonomy-sync.md`](./blog-taxonomy-sync.md)  
4. [`groq-snippets-sanity-blog-features-tools.md`](./groq-snippets-sanity-blog-features-tools.md)  
5. [`lovart-sanity-content-publish/SOP`](../../lovart-sanity-content-publish/SOP-Lovart-Sanity-内容发布总指南.md) §1 选管道  
6. 子 Skill：`lovart-sanity-publish` / `lovart-features-sanity-publish` / `lovart-tools-sanity-publish`  
7. [`LOVART-SANITY-BACKLOG.md`](../../../1-4 Dev/lovart.sanity.studio/LOVART-SANITY-BACKLOG.md)

---

## 9. 常见问题

| 现象 | 处理 |
|------|------|
| `check-publish-deps` FAIL login | `npx sanity login` |
| `--require-taxonomy` 在 sync 前 FAIL | 先 `sync-blog-taxonomy`，再加 `--require-taxonomy` |
| category ref 全空 | 先 sync-blog-taxonomy，再 convert Blog |
| convert 找到 0 个文件 | 检查 `LOVART_ROOT` 或 vault 路径 |
| import 条数 0 / 很快结束 | `--missing` 跳过已有 `_id`（正常） |
| unknown categories | Studio 补 category 或改 MD 标准名 + `fix-category-refs` |
| OOM | `convert.js --lang en --batch-size 50` |

---

## 10. 接手验收（第一天结束前）

- [ ] `node scripts/check-publish-deps.js` PASS  
- [ ] Blog：`sync-blog-taxonomy` + `check-sanity-auth --require-taxonomy` PASS  
- [ ] 单篇 `import-page.js --dry-run` 或 Blog 单批 `--missing` 试跑成功  
- [ ] `verify-blog-publish` 或 `verify-composite --sample 5` PASS  
- [ ] 已读 first-run policy，确认**默认不全量重导**  
- [ ] 已被邀请进 `o11tm2qe`，能打开 https://lovart.sanity.studio  

---

## 11. 误导入与 `--missing` 语义

| 情况 | 说明 |
|------|------|
| import 0 条 | `--missing` 跳过已有 `_id`，不是失败 |
| 误 import 错误文档 | Agent **禁止** delete / `--replace`；Studio 或管理员处理 |
| 覆盖 Studio 手改 | 仅 `--replace` 会覆盖；日常 `--missing` **不会** |

可选备份：`npx sanity dataset export production backup-$(date +%Y%m%d).tar.gz`

---

## 12. 已知不一致（勿踩坑）

| 项 | 正确做法 |
|----|----------|
| `sanity exec` 自定义 flag | Features/Tools verify：`npx sanity exec scripts/verify-composite.js --with-user-token -- --type tools --sample 5` |
| `link-translations.js` | `LINK_I18N_TYPE=blog npx sanity exec link-translations.js --with-user-token` |
| `es` 语言 | 线上约 859 篇；新稿禁止 `es` — 见 [`sanity-es-language-policy.md`](./sanity-es-language-policy.md) |
| 前端 `apps/lovart` | 不在 vault — 见 [`sanity-frontend-apps-lovart.md`](./sanity-frontend-apps-lovart.md) |
| 线上存量债 | ~241 blog 无 category 等 — **勿因此全量重导**（见 BACKLOG） |

---

## 13. 非阻塞待办

见 [`LOVART-SANITY-BACKLOG.md`](../../../1-4 Dev/lovart.sanity.studio/LOVART-SANITY-BACKLOG.md)。
