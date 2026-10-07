## 会话汇总：Blog列表页描述/标题质量问题

### 一、质量问题（排查发现）

| # | 问题 | 范围 | 根因 |
|---|------|------|------|
| Q1 | `description` 字段被写入GSC搜索意图模板文本（`{keyword} explained through real GSC search intent...`） | EN 789篇 | SEO重构管线污染 |
| Q2 | `seo.description` 同样被模板污染 | EN 459篇 | 同上，未同步清理 |
| Q3 | `description` 字段完全缺失 | IT 680篇 / ZH 27篇 | 翻译管线未填充 |
| Q4 | `description` 含markdown残留（`## `、`**`） | DE ~1篇、多语言误报 | 翻译时把正文markdown带入 |
| Q5 | `description` 含写作指令残留（`钩子：`） | ZH 9篇 | 生成流程未清理 |
| Q6 | `description` 含 `[IMAGE PLACEHOLDER]` | IT 15篇 | 正文占位符泄漏 |
| Q7 | **EN正文body是模板复制**（1,311/1,338篇body完全相同） | EN 1,311篇 | 批量生成管线故障 |
| Q8 | 标题过短（你最初投诉点） | 未系统审计 | 未排查 |

**结论**：前端代码正确读取了 `description` 字段，**字段映射没错，错的是数据本身**。这不是"本地修好忘同步"，而是数据一直就在Sanity里被污染着。

---

### 二、修复进度

| 语言 | 修复量 | 状态 |
|------|--------|------|
| EN | 789 desc重写 + 459 seo.desc同步 | ✅ |
| IT | 599 seo→desc复制 + 81 标题生成 + 15 清PLACEHOLDER | ✅ |
| ZH | 27 标题生成 + 9 清钩子 + 1 空值补写 | ✅ |
| DE | markdown清理 | ✅ |
| JA/KO/FR/PT/RU | 本就正常 | ✅ |

**最终验证**：9语言、6,815篇博客，`description` 问题 = **0**。

---

### 三、修复手段

1. **GROQ识别** — 用 `description match "*GSC search intent*"` / `!defined(description)` 等条件精准定位
2. **规则生成description** — 从 `title` 按模式提取（vs对比/指南/榜单/教程/副标题），非AI生成，批量可控
3. **seo→description复制** — IT有599篇seo.description是好的，直接复制到description
4. **正则清洗** — 去 `## `、`**`、`[IMAGE PLACEHOLDER]`、`钩子：` 等残留
5. **批量Mutation** — 每批20条PATCH，Sanity API `v2024-01-01/data/mutate`

---

### 四、潜在风险

1. **EN描述质量偏低** — 从标题规则生成，句式模板化（"Practical guidance based on real creative workflows"），可能被视为slop。比SEO垃圾好，但不是最优。
2. **EN正文仍是模板**（Q7未修） — 列表页描述好了，但点进去正文1,311篇是同一段"Template-based tools like Canva..."，这是更大的内容危机。
3. **CDN缓存延迟** — 前端列表页可能需要几分钟到几小时才刷新，肉眼验证需等。
4. **seo.title/ogImage等未审计** — 可能同样被污染，本次只修description。
5. **IT的seo.description质量** — 复制来源本身可能不够好，未做二次校验。
6. **标题过短（Q8）未排查** — 你最初提到的"标题过短"我们没有系统审计，可能仍存在。

---

### 五、还能做哪些

1. **重写EN正文模板**（最高优先级）— 1,311篇body是复制的，需要重新生成或标记。
2. **审计seo.title / ogImage / structuredData** — 确认是否同源污染。
3. **审计其他内容类型** — compositePage、tool pages、features是否也有同样description污染。
4. **标题长度审计** — 按你最初投诉，系统排查"标题过短"的博客。
5. **加preflight守卫** — 在发布/翻译管线加description校验，防止再次污染（RULE 5已有preflight，但显然没挡住）。
6. **前端验证** — CDN刷新后肉眼确认列表页显示正常。
7. **翻译管线修复** — 找出为什么IT 680篇没填description，从根上修翻译脚本。

需要我继续哪一项？我建议优先 **Q7（EN正文模板）** 和 **标题长度审计**，这两个是你最初投诉的核心，目前还没碰。