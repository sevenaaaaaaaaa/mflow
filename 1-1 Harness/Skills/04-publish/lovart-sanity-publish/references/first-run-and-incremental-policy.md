# Sanity 首次运行与增量发布策略（三条管道共用）

> **Canonical**：Blog / Features / Tools 发布前必读。Agent 与用户均遵守；**默认增量，禁止擅自全量重发**。

---

## Agent 硬性规则

1. **首次运行**：必须先安排 Sanity **认证**（`.env` + API token）、**登录**（`npx sanity login`），并**拉取线上 production 数据集参照到本地**（见 §4.1），再安排批量 import。
2. **已有不重发**：本地已有且线上已有同 `_id` 的内容 → **不得**安排全量 convert + import。
3. **之后仅增量**：除非用户**明确要求**全量 / `--replace` / 无范围扫全库，否则只处理**本轮新增或明确变更**的文件；`import` 必须用 **`--missing`**。

---

## 原则（一句话）

**首次运行：先完成 Sanity 认证与登录，再把线上数据集参照拉到本地；本地已有且线上也已有的内容，不要安排全量发布。之后默认只做增量更新（`--missing`），除非用户明确要求全量或覆盖。**

等价流程：

```
首次 → login + check-auth + 拉线上参照到本地 → 小批量试跑
日常 → 只处理本地新增/明确变更 → convert（限定范围）→ import --missing
禁止 → 无用户授权时，对已有 _id 全库 convert + 全量 import / --replace
```

---

## 一、首次运行（每台机器 / 每位操作者 / 换项目后）

按顺序执行，**未完成前不要**对 production 做大批量 `dataset import`。

| 步骤 | 动作 | 产出 / 目的 |
|------|------|-------------|
| 1 | 复制 `.env.example` → `.env`，填 `o11tm2qe` / `production` / API token | `dataset import` 可用 |
| 2 | `npx sanity login` | `sanity exec` 可用 |
| 3 | `node scripts/check-sanity-auth.js` | 环境与登录 PASS |
| 4 | **拉取线上参照到本地** | 见下表 |

### 4.1 拉取线上内容到本地（参照，非整库导出）

| 管道 | 命令 | 本地缓存 | 作用 |
|------|------|----------|------|
| **Blog** | `npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token` | `scripts/lib/blog-taxonomy.json` | category / tag 的 `_id` 映射，convert 才能写 ref |
| **Blog**（建议） | `npx sanity exec scripts/verify-blog-publish.js --with-user-token` 或 GROQ 抽样 | 心里有数 | 了解线上已有 `_id` / 体量，避免盲目全量 convert |
| **Features / Tools** | `node scripts/convert-features.js --dry-run`（或 `convert-tools.js`） | `~/lovart/import-*-report.json` | **本地**缺口/重复 _id 报告（非从 production 拉正文；线上是否已有用 GROQ，见 groq-snippets） |

**说明**：不把 production 整库 `dataset export` 到本地作为常规步骤；以 **taxonomy 映射 + 发布脚本只写增量** 为准。

### 4.2 首次试跑（小范围）

```bash
# Blog：先 1 个语言、小批量
node convert.js --lang en --batch-size 10 --dry-run
node convert.js --lang en --batch-size 10
npx sanity dataset import ~/lovart/import-blog-en-batch01.ndjson --dataset production --missing
```

Features / Tools：优先 `import-page.js` 单篇或 `--dry-run`，确认字段后再批量。

---

## 二、日常发布：只做增量

### 2.1 导入侧（硬性）

| 允许 | 禁止（除非用户**明确书面/口头授权**） |
|------|--------------------------------------|
| `npx sanity dataset import … --dataset production --missing` | `--replace` 全量覆盖 |
| 单篇 `import-page.js --import` | 对「仅为了对齐」而重导数千篇已存在 `_id` |
| `fix-category-refs` / `link-translations` 等 **patch** | `sanity deploy`、删文档、改 schema |

`--missing`：**仅当 `_id` 在 production 不存在时才写入**；已存在文档不会被 NDJSON 覆盖。

### 2.2 转换侧（Agent 行为）

- **不要**默认 `node convert.js` 无 `--lang` 扫全库 4000+ MD 再让用户 import 三百多个 batch。
- **应**根据任务范围缩小：
  - 指定 `--lang en,zh`
  - 指定目录 / 单篇 / `convert-subset.js`
  - 仅 Content Calendar 本轮新增 slug
- 本地 MD/JSON **未改**且线上 **已有同 `_id`** → **跳过** convert + import（除非用户要求刷新正文）。

### 2.3 如何判断「线上已有」

| 方式 | 适用 |
|------|------|
| import 使用 `--missing` | 导入时自动跳过已有 `_id`（最后一道闸） |
| GROQ `*[_id == "slug-lang"][0]._id` | 发布前确认是否需处理 |
| `verify-blog-publish.js` / `verify-composite.js` | 导入后验收 |
| Studio 搜索 slug | 人工抽查 |

**本地已有、线上也有** → 视为已发布，**不要**再安排全量发布该篇。

---

## 三、何时才允许「全量 / 大范围」

必须同时满足：

1. 用户**明确要求**（例如：「全量重导 en」「用 replace 覆盖」「重建所有 blog NDJSON」）。
2. 已说明风险：`--replace` 覆盖 Studio 手改、耗时长、难回滚。
3. 仍有 `preflight` + 用户 `import confirmed` 门控。

未明确要求时，Agent **不得**提议或执行：

- 无 `--lang` 的全库 `convert.js` + manifest 全部 import  
- `--replace`  
- 对历史已导入批次重复 import「以防万一」

---

## 四、三条管道速查

| 管道 | 首次拉取参照 | 日常导入 |
|------|--------------|----------|
| Blog | `sync-blog-taxonomy` + 可选 verify/GROQ | `convert`（范围限定）→ `--missing` → fix refs → link-translations |
| Features | `convert-features --dry-run` | `convert-features` / `import-page` → `--missing` |
| Tools | `pull-tools-from-production`（或 export+sync）；`convert-tools --dry-run` | **定期 pull**：`1-4 Dev/automation/tools-pull/`（launchd / Cursor Automation）；**push**：`convert-tools` / `import-page` → `--missing` |

---

## 五、Anti-Bug 增量修复（patch vs import）

> 全量 Bug 目录：[ANTI-BUGS-REGISTRY.md](../../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md)

### 5.1 决策树：用 import 还是 patch？

```text
文档在 production 是否已有同 _id？
├─ 否 → convert → import --missing（新稿 / 新语言）
└─ 是 → 字段是否需要更新？
    ├─ 否 → 跳过（AB-P02）
    └─ 是 → 改动类型？
        ├─ SEO url_path / JSON-LD / cover / ogImage / bodyJson 内 URL
        │   → patch-* 脚本（--dry-run → --apply）（AB-P03）
        ├─ category ref 断裂
        │   → fix-category-refs.js
        ├─ 翻译 link
        │   → link-translations.js
        └─ 需覆盖整篇正文且用户明确授权 replace
            → 仅此情况考虑 --replace（极少）
```

**硬性禁止**：线上已有、仅为「对齐本地 JSON」而全量 re-import（AB-P02、AB-A03）。

### 5.2 修复登记册 `~/lovart/repair-state.json`

避免重复劳动（AB-P06）：

```json
{
  "entries": [
    {
      "path": "Pages/Features/en/foo-en.json",
      "repairId": "seo-url-v1",
      "contentHash": "sha256:…",
      "appliedAt": "2026-06-05T12:00:00Z"
    }
  ]
}
```

- patch / repair 脚本写入或读取此文件
- 二次 dry-run 应为 0 条（hash 未变且 repairId 未升级则跳过）
- 人工修 MD/JSON 后 hash 变化 → 可再次进入 repair 队列

### 5.3 图片 / HTTP 404 专项

```text
audit（--check-http）→ 报告 JSON → patch --only-broken --dry-run → --apply → 复验 audit = 0
```

- Blog 封面：`audit-blog-covers.js` → `patch-blog-covers.js --only-broken`（AB-P01、AB-I01）
- Features/Tools 插图：`audit-composite-images-404.js` → `patch-composite-images-404.js`（AB-I05）

### 5.4 发布前最小验收（与 AGENTS B7.3 一致）

- [ ] `node scripts/check-sanity-auth.js`（AB-E03）
- [ ] preflight BLOCK=0 或用户确认 WARN
- [ ] mutate 已 dry-run
- [ ] 图片类 audit 复验为 0

---

## 六、相关文档

- [Sanity-Blog-最小交接包.md](./Sanity-Blog-最小交接包.md) — **一页复制清单**
- [SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md](./SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md) — **复制统合方案 / 换设备（Sanity Blog·Features·Tools）**
- [handoff-and-onboarding.md](./handoff-and-onboarding.md) — 旧文件名别名
- [sanity-es-language-policy.md](./sanity-es-language-policy.md) · [sanity-frontend-apps-lovart.md](./sanity-frontend-apps-lovart.md)
- [groq-snippets-sanity-blog-features-tools.md](./groq-snippets-sanity-blog-features-tools.md) — import 前/后 GROQ
- [sanity-cli-setup.md](./sanity-cli-setup.md) — 登录与 `.env`
- [blog-taxonomy-sync.md](./blog-taxonomy-sync.md) — Blog 分类/标签映射
- `1-4 Dev/lovart.sanity.studio/LOVART-SANITY-BACKLOG.md` — 排期
- [ANTI-BUGS-REGISTRY.md](../../../../1-1%20GEO%20Readme/ANTI-BUGS-REGISTRY.md) — Bug SSOT
