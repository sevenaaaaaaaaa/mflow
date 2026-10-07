# Lovart Landing Page JSON 模板参考（legacy 六区块）

> **适用范围**：Features 等仍使用 `heroSection` 多语言 key 的页面。  
> **Tools 页勿用本文档** → 见 [`tools-v2-template.md`](./tools-v2-template.md)（composite-v2，每语言单文件）。  
> 基于 9 份真实落地页 JSON 归纳。

## 强制要求

1. **语言**：必须包含全部 10 种语言，不得缺失任何一种
2. **区块**：必须包含全部 6 种区块类型，不得缺失任何一种

## 语言 key

| 语言 | key |
|------|-----|
| 英文 | `section` |
| 简中 | `section_zh-CN` |
| 繁中 | `section_zh-TW` |
| 日语 | `section_ja` |
| 韩语 | `section_ko` |
| 德语 | `section_de` |
| 法语 | `section_fr` |
| 俄语 | `section_ru` |
| 葡萄牙语 | `section_pt` |
| 意大利语 | `section_it` |

## 区块骨架（6 种必须全部出现）

```json
{
  "section": [
    { "type": "heroSection",        ... },
    { "type": "contentSection",      ... },   <!-- 至少 1 次，可多次 -->
    { "type": "textImageSection",   ... },   <!-- 至少 1 次，可多次 -->
    { "type": "threeColumnSection", ... },   <!-- 固定 1 次 -->
    { "type": "testimonialSection", ... },  <!-- 至少 1 次 -->
    { "type": "faqSection",         ... }
  ],
  "section_zh-CN": [ /* 同上 6 种区块 */ ],
  "section_zh-TW":  [ /* 同上 6 种区块 */ ],
  "section_ja":     [ /* 同上 6 种区块 */ ],
  "section_ko":    [ /* 同上 6 种区块 */ ],
  "section_de":     [ /* 同上 6 种区块 */ ],
  "section_fr":     [ /* 同上 6 种区块 */ ],
  "section_ru":     [ /* 同上 6 种区块 */ ],
  "section_pt":     [ /* 同上 6 种区块 */ ],
  "section_it":     [ /* 同上 6 种区块 */ ]
}
```

## 区块排序规则

- **第 1 位**：`heroSection`
- **第 2-N 位**：`contentSection`、`textImageSection`、`threeColumnSection`、`testimonialSection`（可各出现多次，顺序可据主题调整）
- **最后位**：`faqSection`

## 各区块字段定义

### heroSection
```json
{
  "type": "heroSection",
  "title": "...",
  "description": "...",
  "input_placeholder": "...",
  "system_prompt": "...",
  "button_text": "...",
  "image_url": "https://assets-persist.lovart.ai/...",
  "suggestion": [{ "value": "...", "label": "..." }],
  "tip": "..."
}
```

### contentSection（可重复出现多次）
```json
{
  "type": "contentSection",
  "sections": [
    {
      "title": "...",
      "description": "...",
      "button_text": "...",
      "button_link": "...",
      "image_url": "https://assets-persist.lovart.ai/..."
    }
  ]
}
```

### textImageSection
```json
{
  "type": "textImageSection",
  "title": "...",
  "description": "...",
  "button_text": "...",
  "button_link": "...",
  "image_url": "https://assets-persist.lovart.ai/..."
}
```

### threeColumnSection
```json
{
  "type": "threeColumnSection",
  "title": "...",
  "columns": [
    { "title": "描述", "description": "...", "image_url": "https://assets-persist.lovart.ai/agent_images/98800dc8-d644-40b1-8442-3865137b6ecc.png" },
    { "title": "生成",  "description": "...", "image_url": "https://assets-persist.lovart.ai/agent_images/da4b4705-9802-4e60-b637-ffed65818da1.png" },
    { "title": "导出",  "description": "...", "image_url": "https://assets-persist.lovart.ai/agent_images/8f3f2384-8495-4075-b6d6-b90dd0cc6373.png" }
  ]
}
```

### testimonialSection
```json
{
  "type": "testimonialSection",
  "title": "...",
  "description": "...",
  "image_url": "https://assets-persist.lovart.ai/...",
  "button_link": "...",
  "button_text": "..."
}
```

### faqSection（无 title 字段）
```json
{
  "type": "faqSection",
  "faq": [
    { "question": "...", "answer": "..." }
  ]
}
```

## image_url 规则

- 必须使用 `https://assets-persist.lovart.ai/...` 前缀
- 严禁编造图片 URL，必须从 `references/image-library.md` 中选取
- threeColumnSection 的三张图片固定为通用流程图（Describe/Generate/Export），不可替换
- 无本地化素材的语种 → 降级使用对应主题的英文版图片
