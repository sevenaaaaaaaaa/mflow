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

## 一之二、落地页（compositePage，T1 已上线）

**⚠ 关键差异**：`compositePage` **没有 `status` 草稿字段**（实测 9,303 篇 0 个）→ **真实写入立即前台可见**。
因此落地页发布比 blog 更保守：默认 dry-run · 真实写入必须显式勾选「确认公开可见」· 更新优先用 patch 模式。

| 能力 | 说明 |
|------|------|
| md → composite 版块 | `md_to_sections()`：hero-split（标题/描述/CTA/封面）→ feature-detail（按 H2 归组）→ proof-block（≥2 个含数字句）→ faq（`## FAQ` 或问句 H2/H3）→ cta-default；自动去重避免文案重复计数 |
| 结构校验 | `validate_sections()`：必须有 hero · 内容版块 ≥2 · FAQ ≤8 · 有 cta · 文案总长 200–1200（RULES-70 落地页档） |
| 两种写入 | `create`（createIfNotExists，新建页）· **`patch`（带 ifRevisionID，只改指定字段；更新既有页首选）** |
| 批量 | 批量任务类型 `publish_sanity`（items 带 doctype/mode/page_type/...），走配额（真实写入计量）与熔断 |
| 安全闸 | 未勾选确认 → API 直接拒绝（"写入即上线"提示） |

CLI：
```bash
python3 "1-4 Dev/scripts/publish_adapters/sanity_publisher.py" ...   # 见 publish_landing()/build_composite_doc()
```
API：`POST /api/publish/sanity {doctype:"composite", page_type, mode, cover_url, confirm_public, dry_run}`

实测（线上 dry-run，零副作用）：create 模式 5 版块 tx 返回；patch 模式更新既有页 tx 返回；Sanity 文档 `_updatedAt` 未变。

## 一之三、落地页闭环（改稿 → 发布，T1 延伸）

**预设「🔁 落地页闭环（改稿→发布）」**：一次把「存量落地页改稿 + 校验 + patch 上线」串成任务链。

```
landing_refresh 任务（批量任务页 → 预设，或 Agent 对话）
  ├─ 读 Sanity 现有页面内容（bodyJson → 文本）
  ├─ 按落地页结构重写：H1 → 3-4 非问句 H2（含数据点）→ FAQ → CTA
  ├─ 四门禁（结构/反slop · GEO 可引用性 · 配额 · 语言规范）+ **composite 结构校验**（词当量 ≤1200）
  ├─ 不过则带反馈重写（≤3 轮，自愈收敛）
  └─ 通过的项 → **自动链出 publish_sanity 任务**（patch 模式，dry-run 默认）
        → 再次人工确认后关闭 dry-run 即真实上线
```

关键设计：
- **只链通过项**：`gates_blocked` 或 `struct_errors` 非空的稿件不会进入发布链（审计记 `CHAIN-SKIP`）
- **链式发布默认 dry-run**：落地页写入即上线，所以链式发布必须显式 `chain.dry_run=false` 才真写
- **patch 用真实 `_id`**：内容库 `sanity_id` 是 UUID，patch 必须以它命中（slug ≠ _id）
- **发布失败即失败**：`publish_sanity` 失败会抛错 → 条目 failed（不再"假 done"）

实测（线上 dry-run）：
```
landing_refresh 1 项 → ready=True（四门禁+结构全过）
  → 自动链出 publish_sanity（patch）→ tx=NngiCiCmzwd6fOe1vYPa7V  ✅
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
