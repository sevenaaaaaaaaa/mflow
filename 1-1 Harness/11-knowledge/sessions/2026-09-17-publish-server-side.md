---
type: session-log
session_date: 2026-09-17
session_slug: publish-server-side
status: ready
---

# Session Log — 线上发布通道（Sanity 上云 + WordPress 就绪）

## 需求
用户指出"Sanity 凭证在 Mac 侧、服务器没有"是阻塞——要让线上 MFlow 自己能同步内容到 Sanity、WordPress 等平台。

## 关键发现
- Sanity 是 **纯 Python + HTTP API 就能写**（`o11tm2qe` / production / API 2024-01-01），根本不需要 Node（服务器无 node 也不影响）
- 既有 `1-4 Dev/scripts/import_zh_product_blogs_to_sanity.py` 已含完整文档结构（_type=blog / category reference UUID / structuredData / status=draft / createIfNotExists）
- MD→PortableText 转换器 `md_to_portable_text.py`（598 行，纯 stdlib）此前只在 Mac `~/Documents/Lovart Local Dev/scripts/` → **已 vendor 入仓**
- 凭证源：Mac `~/.config/sanity/config.json` 的 authToken（81 字符）；Sanity CLI 本地存储

## 交付（线上 e2e 全过）
1. **`publish_adapters/sanity_publisher.py`**：ping（只读连通）/ build_blog_doc（映射既有 taxonomy UUID + HowTo·Article JSON-LD）/ upsert（createIfNotExists + 原生 dryRun）；CLI 三命令
2. **凭证三级解析**：env → `run/secrets/sanity.json`（600，目录 700，git-ignore）→ 本机 sanity-cli；线上已写入 secrets（未入库、未打印）
3. **发布 API**：`/api/publish/config`（凭证状态+可发布草稿）、`/ping`、`/sanity`（dry_run 默认 true）、`/wordpress`、`/history`；全部 admin-only
4. **人工授权门禁**（铁律落地）：条目须 S4-qa/S4-ready/S5-* 且 qa BLOCK 全 0；真实写库 UI 二次确认；每次真实发布写 approvals.log（SANITY-PUBLISH / WP-PUBLISH）
5. **工作台「发布通道」卡**（分发队列页）：凭证状态 + 草稿选择 + slug/语言/分类/标题 + 连通探测 / Dry-run / 真实发布 / 发 WordPress + 发布历史
6. **WordPress 通道**：复用既有 adapter + cli.py，配置 `run/cms.json`（base/user/app_password）即可用；Webhook 出口通用（OpenFlow 接一个收稿端点即直连）
7. **文档**：`docs/publish.md`（能力/API/安全边界/配置）

## 线上验证
- ping：9034 篇 blog（服务端凭证）✓
- dry-run 试跑稿：doc=ai-poster-generator-2026，33 个 portable text 块，返回 transactionId，**未落库** ✓
- 门禁：S0-todo 条目被拒（"需推进到 S4-qa 并经人工审"）✓；不存在条目被拒 ✓
- admin（mflow/Seven）可调用 ✓

## 边界（诚实）
- Sanity 写入一律 `status=draft` —— MFlow 负责"进 CMS"，**前台发布仍需人工在 Sanity 侧确认**
- `createIfNotExists`：slug 冲突不改线上既有文档（安全，但同 slug 更新需后续加 patch 模式）
- WordPress 未配置（需用户提供站点与应用密码）

## 待用户
- 首篇真实发布授权（建议：dry-run 已过的 geo-gap-ai-poster-generator）
- WordPress：base URL + 用户名 + Application Password
