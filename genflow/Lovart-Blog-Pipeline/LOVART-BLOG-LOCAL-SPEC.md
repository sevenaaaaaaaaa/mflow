# Lovart Blog 本地生成规范（01-Drafts）

> 与 `cursor-lovart-blog-system-prompt.md` 正文结构 + Sanity `convert.js` 导入字段对齐。  
> 知识库：`1-Project/Lovart Knowledge Base/`  
> 输出：`1-Project/Lovart-Blog-Pipeline/Lovart-Blogs/01-Drafts/`  
> 封面池：`1-Project/Lovart-Blog-Pipeline/Lovart-Blogs/Cover Url 随机调取.md`（56 张唯一 URL；⚠️ 旧 Lovart/Sanity Blog/ 已删除，需把封面池放到此新位置）

---

## 1. Frontmatter 必填字段（Sanity 兼容）

`convert.js` 读取 YAML frontmatter 后映射为 `blog` 文档。本地稿**必须**包含下列字段：

| 字段 | 类型 | 约束 | 映射到 Sanity |
|------|------|------|----------------|
| `title` | string | ≤70 字符，含主关键词 | `title` |
| `slug` | string | 小写、连字符，与 URL `/blog/{slug}` 一致 | `slug.current` |
| `date` | string | `YYYY-MM-DD`，计划发布日 | `releaseDate` |
| `language` | string | 固定 `en` | `language` |
| `category` | string | **必须是 Sanity 合法 12 类之一**（见下表） | `category`（导入后 `fix-category-refs`） |
| `author` | string | 建议 `Lovart Content Team` | `author` |
| `description` | string | 摘要，≤300 字符；列表页 excerpt | `description` |
| `keywords` | list | 5–8 个 SEO 关键词 | `seo.keywords` |
| `tags` | list | 3–6 个话题标签 | 导入为 tag 引用（若流程支持） |
| `cover_url` | url | 从封面池分配，**勿编造** | `cover.url` + `seo.ogImage.url` |
| `alt_text` | string | 封面 alt，含主题关键词 | `cover.alt` + `seo.ogImage.alt` |
| `seo_title` | string | ≤60 字符，可与 title 相同或略短 | `seo.title` |
| `seo_description` | string | 150–160 字符，含 CTA | `seo.description` |
| `status` | string | 本地阶段：`draft` / `ready` / `published` | 仅本地标记 |
| `content_cluster` | string | 内容集群名（footer 与内链策略用） | 仅本地 / 运营 |

### 1.1 写作类型 → Sanity `category` 映射

System prompt 中的「写作类型」与 Sanity **12 类合法 category** 不一致，导入前按此表填写 `category`：

| 写作类型（prompt） | Sanity `category` | Content Calendar 文件夹 |
|------------------|-------------------|-------------------------|
| Comparison | `How-To` | `02-Comparison/` |
| Lovart 101 | `Lovart 101` | `13-Onboarding/` 或 `01-How-To/` |
| How-To | `How-To` | `01-How-To/` |
| Best Practice | `Best Practice` | `08-Best-Practice/` |
| Segment | `Industry Solution` | `11-Programmatic-SEO/` 或 Segment 专题 |
| Better Design | `Branding` | 设计教育类可放 `01-How-To/` |
| Insight & Trend | `Insight & Trend` | `Insight` 相关目录 |

**禁止**在 frontmatter 写 `Comparison`、`Better Design`、`Segment` 等未在 Sanity 注册的 category 字符串。

Sanity 合法 12 类：`AI Image Tools`、`AI Video Tools`、`Best Practice`、`Branding`、`How-To`、`Insight & Trend`、`Lovart 101`、`Industry Solution`、`Customer Story`、`News`、`Pillar`、`Cluster`。

### 1.2 建议保留的扩展字段（仅本地 / 写作辅助）

| 字段 | 说明 |
|------|------|
| `difficulty` | `beginner` / `intermediate` / `advanced` |
| `tool` | 逗号分隔 Lovart 功能名 |
| `focus_keyword` | 主关键词（= `keywords[0]`） |
| `seo_schema` | `Article` / `FAQ` / `HowTo` — 用于生成 JSON-LD |
| `estimated_read` | 如 `12 min` |
| `page_type` | 固定 `Blog Post` |
| `internal_note` | 如 `Detail Page \| Batch 1 \| Week 2026/05-W4` |

---

## 2. 封面随机分配

- **池文件**：`2-Area/Content Archive/Cover Url 随机调取.md`（56 张唯一 URL；与 `convert.js` 的 `URL_POOL` 同源）
- **规则**：按 `slug` 做稳定哈希选取（同一 slug 永远同一封面；不同 slug 在池内分散）
- **命令**：

```bash
python3 scripts/pick-cover.py adobe-firefly-vs-lovart
python3 scripts/pick-cover.py   # 仅查看池大小
```

- **alt_text 公式**：`{focus_keyword} — Lovart AI Design Agent blog cover`（≤125 字符）

未写 `cover_url` 时，`convert.js` 会按导入顺序轮询池；**本地生成时应显式写入**，避免批量导入时封面撞车。

---

## 3. SEO 与 JSON-LD

### 3.1 字段长度

| 字段 | 上限 |
|------|------|
| `seo_title` | 60 字符（警告线） |
| `seo_description` | 160 字符（警告线） |
| `description` | 300 字符（Sanity excerpt） |

### 3.2 `seo_schema` → `structured_data_json`

在 frontmatter 用 **折叠多行字符串** 写入 `structured_data_json`（合法 JSON，无 `<script>` 包裹）。`convert.js` 当前默认 `json: ''`；若后续脚本支持读取该字段，可直接进 Sanity `seo.structuredData.json`。

| seo_schema | @type | 何时使用 |
|------------|-------|----------|
| `Article` | Article | 默认；Insight、Segment、Better Design |
| `FAQ` | FAQPage | 文末有 4–6 组 FAQ |
| `HowTo` | HowTo | How-To、101 含 numbered steps |

**Article 最小模板**（替换占位符）：

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{seo_title}}",
  "description": "{{seo_description}}",
  "image": "{{cover_url}}",
  "datePublished": "2026-05-25",
  "author": { "@type": "Organization", "name": "Lovart" },
  "publisher": {
    "@type": "Organization",
    "name": "Lovart",
    "logo": { "@type": "ImageObject", "url": "https://www.lovart.ai/favicon.ico" }
  },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://www.lovart.ai/blog/{{slug}}" }
}
```

**og_image**：线上列表/分享用 `cover_url`（CDN 直链），**不要**用 `/images/blog/[slug].webp` 占位路径，除非该文件已上传 CDN。

---

## 4. 正文与导入

- 正文：英文、US spelling；H1 仅标题一行；结构见 system prompt。
- 内链：仅 [Verified Internal Links](cursor-lovart-blog-system-prompt.md) 中的 slug。
- 导入路径（定稿后）：复制到 `Sanity Blog/Content Calendar/{文件夹}/` → `sanity-studio/node convert.js` → `import --missing`。

`01-Drafts` 阶段**不**要求放入 Content Calendar；定稿 `status: ready` 时再迁移。

---

## 5. 文件命名

```
{category-prefix}-{slug}.md
```

示例：`comparison-adobe-firefly-vs-lovart.md`

---

## 6. 单篇生成检查清单

- [ ] `category` 为 Sanity 合法 12 类之一  
- [ ] `cover_url` 来自封面池脚本  
- [ ] `alt_text` / `seo_title` / `seo_description` 长度合规  
- [ ] `keywords` 含 `focus_keyword`  
- [ ] 正文含 Derivative Scenarios、FAQ、E-E-A-T、Internal Links、Image Appendix、footer cluster  
- [ ] **词数 ≥ 7,500**（全分类统一地板，2026-07-17；旧分档已废止；`<7500` 不得 `ready`）  
- [ ] 无编造 `/blog/` 内链  
- [ ] 非脚本灌字 / 无 Banned Template-Phrase  

---

## 7. 相关文件

| 文件 | 作用 |
|------|------|
| `templates/frontmatter.example.yaml` | 可复制 frontmatter 模板 |
| `scripts/pick-cover.py` | 封面 URL 分配 |
| `cursor-lovart-blog-system-prompt.md` | 正文结构与 93 篇任务单 |
| `4-Archive/Skills/lovart-content-writer.md` | 叙事与反 AI 写作 |
