---
name: lovart-sanity-publish
description: Lovart Sanity 发布唯一父入口。Blog/Features/Tools/Product/Scenarios 均先进入本 skill 路由，再内部调用具体 publish 子 skill。First run auth+sync taxonomy; incremental only (--missing). Use for "Sanity push" / "发布" / "换设备" / "Sanity 交接".
---

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-sanity-publish/SKILL.md` |

# Lovart Sanity Publish — 唯一父入口

**Canonical doc**：`Sanity-Blog-发布统合指南.md`

## 父入口职责（必须遵守）

`lovart-sanity-publish` 是所有 Sanity 发布、导入、同步、换设备交接请求的唯一父入口。

- 用户提到 Blog / Features / Tools / Product / Scenarios 发布时，先进入本 skill。
- `lovart-sanity-content-publish` 只作为路由索引，不直接接用户请求。
- `lovart-tools-sanity-publish`、`lovart-features-sanity-publish`、`lovart-product-sanity-publish`、`lovart-scenarios-sanity-publish` 只作为本父 skill 的内部执行子 skill。
- 任何发布前必须先经 `lovart-content-quality-gates`，BLOCK=0 才能继续。

**必读策略（三条管道共用）**：[first-run-and-incremental-policy.md](./references/first-run-and-incremental-policy.md)

| 参考 | 用途 |
|------|------|
| [Sanity-Blog-最小交接包.md](./references/Sanity-Blog-最小交接包.md) | **一页复制清单 + 首日命令** |
| [SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md](./references/SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md) | **Sanity Blog·Features·Tools 换设备 / 复制给他人** |
| [sanity-es-language-policy.md](./references/sanity-es-language-policy.md) | **`es` 语言策略（P1）** |
| [sanity-frontend-apps-lovart.md](./references/sanity-frontend-apps-lovart.md) | **前端 repo 边界（P1）** |
| [handoff-and-onboarding.md](./references/handoff-and-onboarding.md) | 旧文件名别名 → 指向上述 SOP |
| [sanity-cli-setup.md](./references/sanity-cli-setup.md) | 登录、`.env`、Token 权限 |
| [blog-taxonomy-sync.md](./references/blog-taxonomy-sync.md) | 拉取线上 category/tag 到本地 |
| [groq-snippets-sanity-blog-features-tools.md](./references/groq-snippets-sanity-blog-features-tools.md) | import 前/后 GROQ |
| [first-run-and-incremental-policy.md](./references/first-run-and-incremental-policy.md) | **首次运行 vs 日常增量** |

**Scripts**：`1-4 Dev/lovart.sanity.studio/convert.js` · **MD/日历源**：`1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/` + `1-3 Content Gen/Content Calendar/`

## 发布策略（Agent 必须遵守）

1. **首次**：`.env` → login → `check-publish-deps` → `check-sanity-auth` → **`sync-blog-taxonomy`** → `check-sanity-auth --require-taxonomy` → 小批量试跑。
2. **本地已有且线上已有同 `_id`**：不安排全量 convert/import。
3. **日常**：仅 **增量** — `import --missing`；convert 限定范围。
4. **全量 / `--replace`**：仅当用户**明确要求**。

## Triggers

- 「Sanity push」/「发布」/「同步 blog 到 Sanity」
- `lovart-multi-platform-push` Step 5
- content-writer 产出 MD 后

## 内部路由

- Blog → 本 skill 的 Blog 管道（`convert.js`）
- Tools → 内部调用 `lovart-tools-sanity-publish/`
- Features → 内部调用 `lovart-features-sanity-publish/`
- Product → 内部调用 `lovart-product-sanity-publish/`
- Scenarios → 内部调用 `lovart-scenarios-sanity-publish/`
- Studio 部署 → 永不 `npx sanity deploy`

## Workflow

### 首次运行

```bash
cd "1-4 Dev/lovart.sanity.studio"
cp .env.example .env
npx sanity login
node scripts/check-publish-deps.js
node scripts/check-sanity-auth.js
npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token
node scripts/check-sanity-auth.js --require-taxonomy
node convert.js --lang en --batch-size 10 --dry-run
```

### 日常增量（默认）

```bash
node scripts/check-publish-deps.js
node scripts/preflight-content.js --type blog-md
npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token   # Studio 分类有变时

node convert.js --lang zh --batch-size 100
node scripts/preflight-content.js --ndjson ~/lovart/import-blog-zh-batch01.ndjson

npx sanity dataset import ~/lovart/import-blog-zh-batch01.ndjson --dataset production --missing
npx sanity exec fix-category-refs.js --with-user-token
npx sanity exec link-translations.js --with-user-token
SINCE_MINUTES=60 npx sanity exec scripts/verify-blog-publish.js --with-user-token
```

## Safety

- ❌ 默认全量 convert + 全 manifest import / `--replace` / `sanity deploy`
- ✅ `--missing` only · 首次 sync taxonomy · 范围限定 convert

## 7 步门控

`check-publish-deps` → `preflight` → `preflight confirmed` → `convert（限定范围）` → `import confirmed` → `fix refs` → `link-translations` → `verify-blog-publish`

详见统合指南 §6。

## Anti-Bugs（禁止再犯）

> 全量目录：[ANTI-BUGS-REGISTRY.md](../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md)

| ID | 本 Skill 门禁 |
|----|--------------|
| AB-P02 | 线上已有同 `_id` → **禁止**全量 convert+import；仅 `--missing` 或 patch |
| AB-E01 | 命令写全路径：`1-4 Dev/lovart.sanity.studio`，禁止 `…/` 省略号 |
| AB-E03 | 发布前 `check-sanity-auth.js`（API ping）；401 则轮换 WRITE token 或 `sanity exec --with-user-token` |
| AB-E04 | patch / import 须 WRITE token；READ token 只读 |
| AB-S02 | 缺 slug 时 convert 用 `inferSlugFromMdFilename`；改 slug 前 GROQ 核对线上 |
| AB-S03 | 先 `sync-blog-taxonomy` 再 convert；category 走 `blog-taxonomy.js` |
| AB-I04 | Blog 封面 404：仅 `patch-blog-covers --only-broken`，禁止全量换 liblib |
| AB-E02 | `sanity login` 失败时用 `patch-*-env.js` 或 `sanity exec --with-user-token` |
| AB-E05 | 确认 `LOVART_ROOT`；缺 `Sanity Blog/Content Calendar` 勿误报全库 BLOCK |
| AB-U03 | slug 推断与线上一致：GROQ 后再 import |
| AB-P06 | 大批量 repair 配合 `~/lovart/repair-state.json` 去重 |

**工作目录**（可复制）：

```bash
cd "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-4 Dev/lovart.sanity.studio"
```
