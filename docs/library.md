# 多站点内容库（站点档案驱动的 CMS 镜像）

> 目的：让 MFlow 支持**不同网站的目录结构**，把 CMS（Sanity 等）内容镜像到本地库，供检索、对标、改稿与 GEO 闭环使用。

## 核心概念

**站点档案（site profile）** = 一个 JSON，描述该站的目录结构与数据源。MFlow 的所有内容动作（库浏览/同步/发布/URL 生成）都由档案驱动，因此换站点只换档案，不改代码。

`run/sites/{site}.json`
```json
{
  "id": "lovart-global",
  "name": "Lovart Global",
  "domain": "www.lovart.ai",
  "default_lang": "en",
  "source": {"type": "sanity", "project": "o11tm2qe", "dataset": "production"},
  "sections": [
    {"key": "blog",     "dir": "blog",     "docType": "blog",          "engine": "portable-text", "route": "/{lang}/blog/{slug}"},
    {"key": "features", "dir": "features", "docType": "compositePage", "pageType": "feature", "engine": "body-json", "route": "/{lang}/features/{slug}"},
    ...（tools / topics / scenarios / solutions / products / news）
  ]
}
```
- `docType` / `pageType`：Sanity 里的类型与子类型（落地页都是 `compositePage`，用 `pageType` 区隔）
- `dir`：本地库目录 + 站点路径段
- `route`：URL 规则（`{lang}`/`{dir}`/`{slug}` 占位；`default_lang` 不带语言前缀——不同站点可配不同规则）
- `engine`：正文形态（`portable-text`=富文本 / `body-json`=版块 JSON）

## 本地库布局

```
run/library/{site}/{dir}/{lang}/{slug}.md     # frontmatter（site/section/lang/slug/url/sanity_id/status…）+ 可读正文
run/library/{site}/index.json                 # 段落计数 + 语言分布 + 同步时间
run/library/{site}/sync-status.json           # 后台同步进度（UI 轮询）
```
URL 由档案规则自动生成（含本地化前缀），例：`https://www.lovart.ai/zh/blog/xxx`、`https://www.lovart.ai/tools/xxx`。

## 同步（Sanity → 库）

```bash
python3 "1-4 Dev/scripts/library/sanity_pull.py" --site lovart-global --dry-run
python3 "1-4 Dev/scripts/library/sanity_pull.py" --site lovart-global --sections blog --max 20   # 试跑
python3 "1-4 Dev/scripts/library/sanity_pull.py" --site lovart-global                            # 全量
```
- 分页 100/批，剔除 `drafts.**`
- 正文转换：`pt_to_md.py`（Portable Text → Markdown，支持标题/列表/链接/图片/代码/表格）+ `bodyjson_to_md`（落地页版块 JSON → 可读文本）
- 工作台「内容库」页可视化：站点选择 / 段落 chips（计数）/ 语言过滤 / 全文搜索 / 阅读 / 一键同步（后台 + 进度）

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/library/sites` | 站点档案列表 |
| GET | `/api/library/tree?site=` | 段落 + 计数 + 语言分布 + 同步时间 |
| GET | `/api/library/list?site=&section=&lang=&q=` | 条目列表（≤200） |
| GET | `/api/library/status?site=` | 后台同步进度 |
| POST | `/api/library/sync` | 启动同步（admin；`{site, sections, max}`）——审计入 approvals.log |

## 与其它能力的关系

- **发布**（`docs/publish.md`）：发布走同一套 slug/URL 规则；`createIfNotExists` 保护存量
- **GEO 闭环**：库是"我们已有什么"的底账——引用缺口 × 库内已有 → 判断「改稿」还是「新写」
- **多项目**：项目（run/projects/{id}）是"任务/管线"空间；站点档案（run/sites）是"内容资产"空间；两者解耦，一个站点可被多个项目引用

## 换站点的做法（不同网站目录结构）

1. 在 Sanity/CMS 摸清类型与路径（`pageType` 分布、URL 规律）
2. 写 `run/sites/{newsite}.json`（sections 的 dir/route 按该站规则）
3. 工作台「内容库」选该站点 → 同步 → 浏览
4. 发布时也按该档案生成 URL —— 零代码改动

## 首次同步实况（2026-09-17）

| 段落 | 拉取/总数 | 体积 | 主要语言 |
|------|----------|------|---------|
| blog | 8,864/8,884 | 105 MB | en 1499 / zh 958 / it 824 / ja 753 |
| features | 6,400/6,400 | 32 MB | en 827 / ja 715 / de 714 / pt 712 |
| tools | 1,661/1,661 | 11 MB | en 385 / fr 164 / zh 162 |
| topics | 409/409 | 1.9 MB | zh 133 / ja 34 / ko 34 |
| solutions / scenarios / products / news | 201 | 0.9 MB | — |
| **合计** | **17,535** | **215 MB** | 3 分钟 |
