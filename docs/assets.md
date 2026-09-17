# 图片物料台账与批量替换（落地页 / Blog）

> 目标：把「落地页模块里配置的图片物料」变成可盘点、可批量替换的资产操作，并保留 dry-run 与审计。

## 物料在哪（实测结论）

| 位置 | 结构 | 规模 |
|------|------|------|
| `compositePage.cover` | `{_type:"imageSource", sourceType:"external", url, alt}` | 2,053 页 |
| `compositePage.bodyJson[].media` | 版块内 `{src, alt}`（另有 `image`/`backgroundImage` 兼容） | 9,265 页 |
| `blog.coverUrl` | 字符串 URL | 2,087 篇 |

**重要事实（首次全量扫描）**：17,538 个页面只引用 **208 个素材 URL** —— 最高复用的单张图被用 **7,204 次**（cover 1,654 + media 5,550），是默认占位图；另有 blog 封面集中在 `liblibai-online.liblib.cloud`（213/173 次复用）。→ 批量替换正是针对这种"占位图泛滥"的场景。

## 三步流程

```bash
# ① 扫描：生成台账 run/library/{site}/assets.json
python3 "1-4 Dev/scripts/library/asset_tools.py" scan --site lovart-global [--sections tools,features] [--max 100]

# ② 计划：按规则匹配 + 过滤（不改任何东西）
python3 "1-4 Dev/scripts/library/asset_tools.py" plan --site lovart-global \
  --mode exact|prefix|regex --match "<URL 或前缀/正则>" \
  --new-url "https://新的图.png" --new-alt "新 alt" \
  [--section tools --lang zh --page-type feature --slugs a,b,c] \
  [--url-map map.json]        # 逐页映射：{"旧URL": "新URL"}

# ③ 应用：默认 dry-run（Sanity 原生 dryRun，返回 transactionId 不落库）
python3 "1-4 Dev/scripts/library/asset_tools.py" apply --site lovart-global --plan <plan.json> [--yes] [--max-docs 500]
```

## 台账结构（assets.json）

```json
{"stats": {"pages": 17538, "urls": 208, "with_cover": 10680, "with_media": 8608},
 "pages": {"<doc_id>": {"slug","lang","pageType","section","title","rev","cover":{"url","alt"},"media":[{"idx","sect","field","src","alt"}]}},
 "urls":  {"<url>": {"n", "roles": {"cover":n,"media":n}, "pages":[doc_id...], "alt"}}}
```
- `pages`：页面 → 物料清单（含 `_rev`，用于并发保护）
- `urls`：素材 → 使用方反查（谁在用、用了几次、什么角色）

## 安全设计

| 项 | 做法 |
|----|------|
| 默认只读 | `plan` 不改任何数据；`apply` 默认 dry-run |
| 并发保护 | 真写前重取 `_rev`，patch 带 `ifRevisionID`（并发编辑不会覆盖） |
| 分批 | 每批 ≤50 个 patch；`--max-docs` 限制单次规模 |
| 审计 | 真写后写 `run/approvals.log`（`ASSET-PATCH …`） |
| bodyJson 整串回写 | 版块内的 media 需重写整个 `bodyJson` 字符串（JSON 字段），因此必须带 `ifRevisionID` |

## 工作台入口

「内容库」页 → **图片物料** 卡：
- **扫描物料**（后台，进度轮询）
- 台账列表（URL × 次数 × 角色 × alt，可按 URL/角色/语言过滤）
- **批量替换**：模式（前缀/精确/正则）+ 匹配 + 新 URL/alt + 过滤（段落/语言/类型/slug）→ ① 生成计划 → ② Dry-run 预览 → ③ 应用（真写库，admin）

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/assets/inventory?site=&q=&role=&section=&lang=` | 台账（素材反查） |
| GET | `/api/assets/plan?site=` | 当前替换计划 |
| GET | `/api/assets/result?site=&cmd=scan|plan|apply` | 后台任务结果 |
| POST | `/api/assets/scan` | 扫描台账（admin） |
| POST | `/api/assets/plan` | 生成计划（admin） |
| POST | `/api/assets/apply` | 执行计划（admin；`dry_run` 默认 true） |

## 实测记录（2026-09-17）

- 扫描：17,538 页 / 208 素材 URL / 90 秒 / 台账 8.8MB
- 计划：`exact` 匹配占位图 + 限定 3 个 slug → 命中 3 处 cover
- dry-run：3 个 patch → `transactionId: dZ9OtxTg3BJgkSl5q0gDfx`，operations=update，**Sanity 侧 URL 保持不变（零副作用）**
