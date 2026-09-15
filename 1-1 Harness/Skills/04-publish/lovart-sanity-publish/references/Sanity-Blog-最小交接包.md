# Sanity Blog·Features·Tools 最小交接包

> **一页速查**。完整步骤见 [`SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](./SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)  
> **搜索别名**：`handoff` · `onboarding` · `换设备` · `Sanity 交接` · `Blog Sanity 首次运行`

---

## 1. 必须复制的目录（相对 vault `1-Project/`）

```
1-Project/
├── 1-4 Dev/lovart.sanity.studio/          ← 脚本（勿复制 .env / node_modules）
├── 1-4 Dev/lovart.sanity.studio/Sanity Blog/            ← Blog MD
├── 1-4 Dev/Pages/Features/         ← Features JSON
├── 1-3 Content Gen/Page Gen/Pages/Tools/  ← Tools JSON（composite-v2 唯一正式源）
├── 1-1 Harness/Skills/lovart-sanity-publish/
├── 1-1 Harness/Skills/lovart-sanity-content-publish/
├── 1-1 Harness/Skills/lovart-sanity-preflight/          （兼容触发词）
├── 1-1 Harness/Skills/lovart-content-quality-gates/
├── 1-1 Harness/Skills/lovart-features-sanity-publish/
├── 1-1 Harness/Skills/lovart-tools-sanity-publish/
└── 1-4 Dev/.cursor/rules/lovart-sanity-content-pipeline.mdc   （建议）
```

**只复制 `1-1 Harness/Skills/` 不够** — 没有 `1-4 Dev/lovart.sanity.studio/` 和内容源无法发布。

**勿复制**：`.env` · `node_modules/` · `~/lovart/*.ndjson`

---

## 2. 交接人必做（Sanity 后台）

1. [manage.sanity.io](https://www.sanity.io/manage) 项目 **`o11tm2qe`** 邀请接手人  
2. 接手人自建 **Editor API Token** → 写入本机 `.env`  
3. 接手人 `npx sanity login`（与 API token 是两套认证）

---

## 3. 接手人首日五条命令

```bash
cd "…/1-4 Dev/lovart.sanity.studio"

cp .env.example .env          # 填入 SANITY_STUDIO_API_TOKEN
npm install
npx sanity login

# vault 不在默认 iCloud 路径时先 export：
# export LOVART_ROOT="/你的路径/1-Project/Lovart"

node scripts/check-publish-deps.js
npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token
node convert.js --lang en --batch-size 10 --dry-run
```

试跑 import（可选）：

```bash
node convert.js --lang en --batch-size 10
npx sanity dataset import ~/lovart/import-blog-en-batch01.ndjson --dataset production --missing
SINCE_MINUTES=30 npx sanity exec scripts/verify-blog-publish.js --with-user-token
```

---

## 4. 三条铁律

| 规则 | 说明 |
|------|------|
| **首次** | login + 拉线上 taxonomy → 小批量试跑 |
| **已有不重发** | 线上已有 `_id` → 只用 `import --missing` |
| **禁止** | `sanity deploy` · `--replace` · 无授权全库 convert |

---

## 5. 相关 P1 文档（换设备常查）

| 主题 | 文件 |
|------|------|
| `LOVART_ROOT` 换路径 | SOP §3 · `lovart-paths.js` |
| `es` 语言策略 | [`sanity-es-language-policy.md`](./sanity-es-language-policy.md) |
| 前端 `apps/lovart` | [`sanity-frontend-apps-lovart.md`](./sanity-frontend-apps-lovart.md) |
| 旧版 Archive Skill | [`4-Archive/1-1 Harness/Skills/lovart-sanity-publish.md`](../../../../4-Archive/1-1 Harness/Skills/lovart-sanity-publish.md)（已废弃） |
