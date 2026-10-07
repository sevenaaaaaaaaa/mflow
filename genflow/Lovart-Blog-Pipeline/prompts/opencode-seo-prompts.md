open your Obsidian vault and do the following SEO task using the prompt templates below.

## 1. Content Brief (关键词 → 内容大纲)

当你拿到一个目标关键词或选题时，用这个 prompt：

> 你是一个 SEO 内容策略师。请为我的 WordPress 博客生成一篇针对关键词「{keyword}」的内容大纲（Content Brief）。
>
> 目标受众：{audience}
> 搜索意图：{intent}（informational / commercial / transactional）
> 文章类型：{type}（how-to / listicle / comparison / pillar / case-study）
>
> 请输出：
> 1. 推荐标题（3 个候选，含主关键词，标题 <60 字符）
> 2. Meta Description（150-160 字符，含 CTA）
> 3. Slug 建议
> 4. H2/H3 大纲（至少 5 个 H2，每个 H2 下 2-3 个要点）
> 5. 目标关键词 + 5 个 LSI/长尾关键词
> 6. 内链策略（推荐链接到哪些已有文章，用什么锚文本）
> 7. Featured Snippet 机会点（哪个段落可以直接拿 snippet）
> 8. FAQ 问题列表（5 个，提取自 People Also Ask）
> 9. E-E-A-T 信号建议（如何在这篇文章里建立专业度）
>
> 请直接输出 Markdown，写入 Obisidian 笔记。

---

## 2. Write Full Article (写完整 SEO 文章)

拿到 Content Brief 后，用这个 prompt 生成完整文章：

> 你是一个 SEO 文案写手。请根据以下 Content Brief 写一篇完整的 WordPress 博客文章。
>
> 内容大纲：
> ```
> {粘贴 Content Brief 输出的大纲}
> ```
>
> 写作要求：
> - 标题用 H1，小节用 H2/H3，不要跳级
> - 开头用 Scene Hook（场景痛点法）切入，150 字内抓住读者
> - 每个 H2 小节 200-400 字，要有具体数据、案例、步骤
> - 自然地融入目标关键词和 LSI 关键词，不要 keyword stuffing
> - 段落用短句（<25 字/句），bullet points 穿插，提高可读性
> - 结尾添加 CTA 段落，引导转化
> - FAQ 段落用 Q/A 格式，标注 FAQPage Schema 标记
> - 全文标注 [IMAGE PLACEHOLDER] 标记（至少 4 处，含 alt text 建议）
> - 文章末尾添加内链策略表和 E-E-A-T 信号表
> - 字数：{word_count} 字左右
>
> 输出格式：Markdown + YAML frontmatter（title, slug, meta_description, tags, category, seo_schema）
>
> 请直接写入 Obsidian，文件命名规则：{slug}.md

---

## 3. Keyword Research (关键词研究)

当你需要拓展某个主题的关键词矩阵时：

> 你是一个 SEO 关键词研究专家。请分析我的 WordPress 博客在「{topic}」领域的关键词机会。
>
> 我的博客是：{blog_description}
> 目标市场：{market}（如 US, JP, TW）
> 语言：{language}
>
> 请输出：
> 1. Pillar Keywords（支柱词，3-5 个，高搜索量）
> 2. Cluster Keywords（集群长尾词，每个 Pillar 下属 5-8 个，按搜索意图分组）
> 3. Question Keywords（问题型关键词，提取自 PAA/相关搜索，10-15 个）
> 4. Comparison Keywords（对比型关键词，5-8 个）
> 5. Programmatic Keywords（可程序化生成的关键词模板，如 "best X for Y"）
> 6. 每个关键词标注：搜索量级（高/中/低）、竞争度（高/中/低）、商业价值（高/中/低）
> 7. 内容缺口分析：竞品在写但你没写的话题（5-10 个）
>
> 输出到 Obsidian 的 Keywords Research 文件夹。

---

## 4. Content Refresh（旧文翻新）

当你有旧文章需要刷新以提升排名时：

> 你是一个 SEO 内容优化师。请分析并翻新以下 WordPress 旧文章：
>
> 原文：
> ```
> {粘贴旧文全文}
> ```
>
> 当前排名：{current_ranking}（如有 GSC 数据请附上）
> 目标关键词当前位置：{position}
>
> 翻新策略：
> 1. 标题优化（融入 2026 年份标签或最新趋势词）
> 2. 更新过时数据/工具/年份引用
> 3. 补充竞品已有但我们缺失的内容段落（3-5 处）
> 4. 优化 Meta Description（提升 CTR）
> 5. 内部链接刷新（链接到最近发布的关联文章）
> 6. 添加 FAQ 段落（抢占 PAA snippet）
> 7. E-E-A-T 增强（添加作者背书、引用权威来源、更新日期的 lastmod）
>
> 请直接输出翻新后的完整 Markdown 文档。
> Frontmatter 中保持原 slug 不变，更新 date 和 lastmod，加上 updated_reason 字段。

---

## 5. Programmatic SEO Batch（程序化 SEO 批量生成）

当你需要批量生成程序化页面（如行业品牌套件页）时：

> 你是一个程序化 SEO 内容生成器。请为以下 {N} 个行业垂直领域生成品牌套件登录页。
>
> 模板：
> ```
> {粘贴 programmatic-seo 模板}
> ```
>
> 垂直列表：
> ```
> {粘贴行业列表，每行一个：industry_name, slug, target_keyword}
> ```
>
> 要求：
> - 每个行业生成一篇独立 .md 文件
> - 行业名称自然融入全文（约 3% 密度）
> - 每个行业的 3 个设计工具推荐要保持差异化（不要全部一样）
> - FAQ 问题要针对该行业定制（不要泛用通用问题）
> - slug 格式：{industry}-brand-kit-design-templates
> - 文件名：{industry}-brand-kit-{lang}.md
> - 语言：{language}
>
> 批量写入 Obsidian，目录：{output_directory}

---

## 6. Internal Link Audit & Optimization (内链审计)

当你需要优化已有文章的内链结构时：

> 你是一个 SEO 内链优化专家。请为以下文章列表做内链审计和优化建议：
>
> 文章列表（URL + 标题 + 主关键词）：
> ```
> {粘贴文章列表}
> ```
>
> 请输出：
> 1. 孤儿页面（没有其他文章链向它）— 需要补充入链
> 2. 支柱页面（应该获得最多内链但当前不足）— 需要增加内链
> 3. 每篇文章推荐链接到哪些其他文章（出链建议），表格式输出
> 4. 每篇文章推荐被哪些文章链接（入链建议），表格式输出
> 5. 锚文本优化建议（避免过度使用 exact match anchor）
> 6. 内链拓扑图（支柱 → 集群 → 长尾的层级关系）
>
> 输出到 Obisidian，可用于后续批量操作。
