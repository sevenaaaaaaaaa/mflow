# 发布通道（Sanity / WordPress）——服务端能力

> 目标：线上 MFlow 自己能同步内容到 Sanity、WordPress 等平台，不再依赖 Mac 侧凭证。
> **铁律不变**：发布是人工授权动作——门禁（状态机 + 质检）通过后，由 admin 在工作台显式点击；Sanity 写入一律 `status=draft`，前台发布仍需人工在 Sanity 侧确认。

## 一、Sanity（已上线，纯 Python + HTTP API，无需 Node）

- 实现：`1-4 Dev/scripts/publish_adapters/sanity_publisher.py`（stdlib only）+ `md_to_portable_text.py`（598 行 MD→PortableText 转换器，已入仓库）
- 项目：`o11tm2qe` / dataset `production`
- 写入方式：`createIfNotExists`（**不覆盖既有文档**，`_id = slug`）+ 原生 `dryRun` 支持
- 文档结构：`_type=blog`、`slug`、`language`、`category`（reference，映射既有 taxonomy UUID）、`seo.structuredData`（HowTo/Article JSON-LD）、`body`=portable text、`status=draft`

**凭证（三级解析）**
1. 环境变量 `SANITY_TOKEN` / `SANITY_PROJECT` / `SANITY_DATASET`
2. `run/secrets/sanity.json`（600，root-only，**git-ignore**）← 当前线上用这个
3. `~/.config/sanity/config.json` 的 `authToken`（仅 Mac 开发机）

> 服务器凭证已于 2026-09-17 从 Mac 的 sanity-cli 配置同步（写入 `run/secrets/sanity.json`，权限 600/目录 700，未入 git）。

**API（工作台 · 发布通道卡）**
- `GET /api/publish/config`：凭证状态（不回显 token）+ 可发布草稿（S4-qa 及之后）
- `GET /api/publish/ping`：连通探测（返回 blog 总数/最近更新时间）
- `POST /api/publish/sanity {item_id, path, slug, lang, category, title, cluster, dry_run}`：
  - 门禁：条目必须在 **S4-qa / S4-ready / S5-\*** 且 **qa BLOCK 全 0**，否则 400 拒绝
  - `dry_run=true`（默认）：Sanity 原生 dryRun，返回 `transactionId`，**不落库**
  - `dry_run=false`：真写库（status=draft）→ 记 `run/approvals.log`（`SANITY-PUBLISH`）
- `GET /api/publish/history`：最近发布审计

**CLI（服务器/本机均可）**
```bash
python3 "1-4 Dev/scripts/publish_adapters/sanity_publisher.py" ping
python3 "1-4 Dev/scripts/publish_adapters/sanity_publisher.py" dry-run --file x.md --slug s --lang zh
python3 "1-4 Dev/scripts/publish_adapters/sanity_publisher.py" publish  --file x.md --slug s --lang zh --yes
```

## 二、WordPress（通道已通，待配置）

- 实现：既有 `publish_adapters/wordpress.py`（WP REST + Application Password）+ 统一 `cli.py`
- 配置：`run/cms.json`（git-ignore）
```json
{"wordpress": {"base": "https://blog.example.com", "user": "bot", "app_password": "xxxx xxxx xxxx"}}
```
- 调用：工作台发布卡「发 WordPress（草稿）」→ `POST /api/publish/wordpress`

## 三、Webhook（通用出口，已可用）

`publish_adapters/webhook.py`：POST item JSON 到自定义端点（OpenFlow 侧接一个收稿接口即可直连）。
配置同在 `run/cms.json` 的 `webhook.url`。

## 四、安全与边界

| 项 | 设计 |
|----|------|
| 人工授权 | 门禁（stage + qa BLOCK）+ admin-only API + 真实写库前 UI 二次确认 |
| 不覆盖 | Sanity 用 `createIfNotExists`；slug 冲突不会改动线上既有文档 |
| 草稿态 | Sanity `status=draft`——MFlow 负责"进 CMS"，前台发布仍在 Sanity 侧人工确认 |
| 凭证 | 只存服务器 600 文件或环境变量；不入 git；API 不回显 |
| 审计 | 每次真实发布写 `run/approvals.log` |
