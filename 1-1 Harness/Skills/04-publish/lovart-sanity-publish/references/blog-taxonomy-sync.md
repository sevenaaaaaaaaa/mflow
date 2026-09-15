# Blog 分类 / 标签 Taxonomy 同步（sync-blog-taxonomy）

> **目的**：把 **production 线上** category/tag 的 `_id` 映射拉到本地 `blog-taxonomy.json`，供 `convert.js` 写正确 reference。  
> **首次运行必做**（见 [SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md](./SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)）：属「拉取线上数据集参照到本地」，**不是**整库 export，也**不能**代替「只增量 import」策略。

## 何时必须 sync

- **首次**在本机跑 Blog `convert.js`
- Studio **新增/改名** category 或 tag
- `convert.js` 警告 `blog-taxonomy.json empty or stale`
- 大量文章 `unknown categories` 统计

## 前置

- 已完成 [sanity-cli-setup.md](./sanity-cli-setup.md)（`sanity login`）

## 标准流程

```bash
cd "…/1-4 Dev/lovart.sanity.studio"

# 1. 从 production 拉取 category.title → _id、tag.title → _id
npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token

# 2. 确认缓存已写入
cat scripts/lib/blog-taxonomy.json | head -20
# 应看到 generatedAt 时间戳与非空 categories

# 3. 转换（建议按语言分批，见统合指南 §5.1）
node convert.js --lang en,zh,zh-TW

# 4. 导入
npx sanity dataset import ~/lovart/import-blog-en-batch01.ndjson --dataset production --missing
# … 对每个 batch 文件重复

# 5. 补未映射分类（MD 里新 display name、Industry Solution 等）
npx sanity exec fix-category-refs.js --with-user-token

# 6. 导入后验收
npx sanity exec scripts/verify-blog-publish.js --with-user-token --since-minutes 120
```

## convert.js 写入规则

| 字段 | 来源 | NDJSON 顺序 |
|------|------|-------------|
| `tag` 文档 | frontmatter `tags[]` → `tag-{slug}` | **先于** blog 行 |
| `blog.tags` | reference → 上表 _id | blog 行 |
| `blog.category` | frontmatter `category` + taxonomy 映射 | blog 行 |
| `seo.keywords` | frontmatter `keywords` | blog 行内 |

**别名**（`scripts/lib/blog-taxonomy.js`）：`BOFU`→`Best Practice`，`TOFU`→`How-To`，`MOFU`→`Insight & Trend`，`Comparison`→`Best Practice`。

## 与 fix-category-refs 的关系

| 脚本 | 时机 | 作用 |
|------|------|------|
| `sync-blog-taxonomy` | convert **前** | 本地 JSON 映射，convert 直接写 ref |
| `fix-category-refs` | import **后** | 扫 MD，patch 仍缺 category 的 blog |

两者互补，不互斥。

## 多语言

- tag / category **按 display title 映射**，与 `language` 无关。
- 同 slug 多语言共用 Studio 侧 category/tag 文档。
