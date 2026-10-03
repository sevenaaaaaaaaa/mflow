# Tools 落地页 JSON 模板（composite-v2）

> **适用**：`category: tool` 的 Lovart Tools 页。  
> **正式源**：`1-3 Content Gen/Page Gen/Pages/Tools/{lang}/{slug}-{lang}.json`  
> **故事线**：[`STORYLINES.md`](../../../1-3 Content Gen/Page Gen/Refresh-Page/STORYLINES.md)（T1–T5、N5；线上 reflow 长链用 **T-long**）  
> **发布**：`convert-tools.js` → `sanity dataset import --missing`

## 与 legacy 模板的区别

| 维度 | legacy（`json-template.md`） | Tools v2（本文档） |
|------|------------------------------|-------------------|
| 结构 | 单文件 10 个 `section_xx` key | **每语言一个 JSON 文件** |
| 区块 | `heroSection` 等 6 种 | `hero-split`、`prompt-launcher`、`faq` 等 v2 模块 |
| 图片 | `image_url` | `media.src` + `media.alt` |
| 校验 | 人工 | `validate-tools-v2.js` 强制 |

**禁止** 为 Tools 生成 `heroSection`、`contentSection`、`threeColumnSection`、`textImageSection`、`testimonialSection`、`faqSection`。

## 语言与文件命名

10 种语言，各 1 文件：`en`、`zh`、`zh-TW`、`de`、`fr`、`it`、`ja`、`ko`、`pt`、`ru`

```
Pages/Tools/en/ai-logo-generator-en.json
Pages/Tools/zh/ai-logo-generator-zh.json
…
```

## 顶层字段（必填）

```json
{
  "slug": "ai-logo-generator",
  "language": "en",
  "category": "tool",
  "schemaVersion": "composite-v2",
  "storylineTemplate": "T1",
  "title": "…",
  "description": "…",
  "bodyJson": "[{\"type\":\"hero-split\",…},{\"type\":\"faq\",…}]",
  "seo": {
    "description": "…",
    "keywords": ["…"],
    "noIndex": false
  }
}
```

- `bodyJson`：**字符串化** JSON 数组（与现网 Sanity 一致），勿输出未转义的裸数组。
- `storylineTemplate`：新建页默认 **T1**；竞品对比用 **T4**；线上已 reflow 的完整长链对标 **T-long**（≥12 sections）。

## 故事线 → 模块序列（Tools）

| 编号 | 情景 | 模块序列 |
|------|------|----------|
| **T1** | 标准工具 | `prompt-launcher` → `bento-2` → `workflow-horizontal` → `feature-detail` → `testimonial` → `faq` → `cta-default` |
| **T2** | 单点效用 | `hero-split` → `comparison-before-after` → `workflow-horizontal` → `faq` |
| **T3** | 工具合集 | `hero-cinematic` → `tool-grid` → `comparison-table` → `cta-default` |
| **T4** | 竞品对比 | `hero-split` → `comparison-table` → `proof-block` → `review-grid-4col` → `faq` |
| **T5** | 重 SEO | `hero-cinematic` → `feature-grid` → `blog-grid` → `faq` |
| **T-long** | 线上扩展长链 | 以 production / sync 结果为准，常见 12+ 段（含 `bento-4`、`cluster-block-dense` 等） |

选定故事线后，**section `type` 序列须与菜谱一致或为其超集**；末段建议含 `faq`，转化段含 `cta-default`。

## 常用 v2 模块字段速查

### hero-split
```json
{
  "type": "hero-split",
  "badge": "…",
  "title": "…",
  "highlightedText": "…",
  "description": "…",
  "buttons": [{"text": "…", "href": "", "variant": "primary"}],
  "media": {"src": "https://…", "alt": "…"}
}
```

### prompt-launcher
```json
{
  "type": "prompt-launcher",
  "title": "…",
  "description": "…",
  "prompts": [{"label": "…", "prompt": "…"}],
  "cta": {"text": "…"}
}
```

### faq
```json
{
  "type": "faq",
  "title": "Frequently asked questions",
  "items": [{"question": "…", "answer": "…"}]
}
```

### cta-default
```json
{
  "type": "cta-default",
  "title": "…",
  "description": "…",
  "buttons": [{"text": "…", "href": "", "variant": "primary"}]
}
```

完整模块字典见 [`Refresh-Page/README.md`](../../../1-3 Content Gen/Page Gen/Refresh-Page/README.md)。

## 图片规则

- 优先从 `references/image-library.md` 选取 URL，写入 `media.src`。
- 无合适素材时标注 `[待考证]`，勿编造 CDN 路径。
- `threeColumnSection` 固定三步图规则**不适用于** v2；步骤叙事用 `workflow-horizontal` / `workflow-vertical`。

## 生成批次（10 语言）

每次回复最多 **3 个语言文件**（完整独立 JSON，非 `section_xx` 拼接）。

| 批次 | 语言 |
|------|------|
| 1 | `en`、`zh`、`zh-TW` |
| 2 | `ja`、`ko`、`de` |
| 3 | `fr`、`ru`、`pt` |
| 4 | `it` |

## 质量自检（Tools v2）

- [ ] `schemaVersion` = `composite-v2`，`category` = `tool`
- [ ] `storylineTemplate` 为 T1–T5、N5 或 T-long
- [ ] `bodyJson` 内无 legacy `type`
- [ ] 首屏与故事线菜谱匹配（T1 常以 `prompt-launcher` 或 `hero-split` 起）
- [ ] 含 `faq`；含至少一个 `cta-default`（T2 等短链可仅末尾 CTA）
- [ ] 10 语言文件齐全，slug/language 与文件名一致
- [ ] 发布前：`node scripts/preflight-content.js --type tools --strict`
