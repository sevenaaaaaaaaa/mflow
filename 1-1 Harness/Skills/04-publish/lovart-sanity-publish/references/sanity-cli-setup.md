# Sanity CLI 认证与 Studio 环境（Blog / Features / Tools 共用）

> **Canonical**：本文件为 `lovart-sanity-publish` 的运维前置步骤。Features/Tools 发布 Skill 引用此处，不重复维护。  
> **换设备首读**：[`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](./SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)

## 1. 新机 30 秒自检

```bash
cd "…/1-4 Dev/lovart.sanity.studio"
npm install
cp .env.example .env    # 填 SANITY_STUDIO_API_TOKEN
npx sanity login
node scripts/check-publish-deps.js
```

## 2. 检查是否已登录

```bash
npx sanity debug --secrets
```

期望 **`User: … (logged in)`**。或使用：

```bash
node scripts/check-sanity-auth.js
node scripts/check-publish-deps.js
```

## 3. 登录（推荐）

```bash
npx sanity login
```

1. 终端打开浏览器，使用**已被邀请进项目 `o11tm2qe`** 的账号登录。
2. token 存本机，**勿提交 git**；与 `.env` API token **不是同一个**。

## 4. `.env` 与 Token 权限矩阵

```bash
cp .env.example .env
```

| 变量 | 值 | 权限 / 用途 |
|------|-----|-------------|
| `SANITY_STUDIO_PROJECT_ID` | `o11tm2qe` | 固定 |
| `SANITY_STUDIO_DATASET` | `production` | 固定 |
| `SANITY_STUDIO_API_TOKEN` | Editor token | **`npx sanity dataset import`** 写 production |
| `SANITY_STUDIO_READ_TOKEN` | 可选 Viewer | 只读 GROQ / 部分 verify |

Token 在 [manage.sanity.io](https://www.sanity.io/manage) → 项目 `o11tm2qe` → API → Tokens → **Editor**。

| 操作 | 认证 |
|------|------|
| `npx sanity exec … --with-user-token` | `npx sanity login` |
| `npx sanity dataset import … --missing` | `.env` → `SANITY_STUDIO_API_TOKEN` |

## 5. 首次运行检查清单（顺序勿错）

> 策略全文：[first-run-and-incremental-policy.md](./first-run-and-incremental-policy.md)

- [ ] `.env` 已配置且 `dataset=production`
- [ ] `npx sanity login`
- [ ] `node scripts/check-publish-deps.js` PASS
- [ ] `node scripts/check-sanity-auth.js` PASS（**勿**先加 `--require-taxonomy`）
- [ ] **Blog 拉线上映射**：`npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token`
- [ ] `node scripts/check-sanity-auth.js --require-taxonomy`（Blog convert 前）
- [ ] 小批量试跑 + `import --missing`
- [ ] 确认：线上已有 `_id` **不要**全量重导

## 6. 路径（换设备）

```bash
# vault 不在默认 iCloud 路径时
export LOVART_ROOT="/你的路径/1-Project/Lovart"
export LOVART_OUT_DIR="$HOME/lovart"
node scripts/check-publish-deps.js
```

详见换设备 SOP §3。

## 7. 日常发布（默认）

- 仅 convert **本轮变更** 或 `--lang` / 单篇  
- `dataset import` **只用 `--missing`**  
- 全量：**禁止**，除非用户明确要求  

## 8. GROQ 与验收

- import 前查线上是否已有：[groq-snippets-sanity-blog-features-tools.md](./groq-snippets-sanity-blog-features-tools.md)
- Blog import 后：`verify-blog-publish.js`
- Features/Tools：`verify-composite.js --sample 20`

## 9. 故障

| 现象 | 处理 |
|------|------|
| `no auth token could be found` | `npx sanity login` |
| `--require-taxonomy` 在 sync 前 FAIL | 先 `sync-blog-taxonomy` |
| import 403 | Editor token + production dataset |
| convert 0 文件 | 检查 `LOVART_ROOT` |
| import 0 条 | `--missing` 跳过已有 `_id`（正常） |
