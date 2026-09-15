# Tools 页面内容模板 & SEO 优化方案

> 适用: 15 个新增 Tools 页面 | 框架: 14-section 生产标准 | 更新: 2026-06-15

---

## 一、页面结构总览

```
section 1-2:    抓取层 (hero-split + bento-4)       → 吸引 + 功能总览
section 3-6:    说服层 (bento-2 + tabs + prompt + logo) → 信任建立
section 7-8:    转化层 (cta + workflow)              → 首次 CTA
section 9-13:   论证层 (comparison + cluster + detail + proof + faq) → 深说服
section 14:     收口层 (cta)                         → 最终 CTA
```

SEO 权重分布: hero (H1) > bento (H2×6) > tabs (H2×4) > faq (H2×N)

---

## 二、逐 Section 内容模板

### S1: hero-split — 最重要的 SEO 锚点

```json
{
  "type": "hero-split",
  "badge": "[品类名称]",
  "title": "[主关键词] — [价值主张] | Lovart",
  "highlightedText": "[差异化亮点, 5-8词]",
  "description": "[120-160字符]. 覆盖: [功能1], [功能2], [功能3]. [目标用户]的理想选择.",
  "buttons": [
    {"text": "Create [品类] now", "href": "/home", "variant": "primary"},
    {"text": "See examples", "href": "", "variant": "secondary"}
  ],
  "media": {"src": "[hero-image-url]", "alt": "[主关键词]"}
}
```

**SEO 规则**:
- `title` ≤ 60 字符, 含主关键词 + `| Lovart`
- `description` 120-160 字符, 含 1-2 个长尾词
- `badge` 用品类名 (如 "AI Poster Maker", "AI Video Generator")
- `alt` = 主关键词 (精简)

### S2: bento-4 — 4 大功能亮点

```json
{
  "type": "bento-4",
  "title": "[数字] ways Lovart handles [品类]",
  "description": "[概括性一句话, 50-80字符]",
  "columns": 4,
  "features": [
    {
      "title": "[功能名, 3-6词]",
      "description": "[功能描述, 40-60字符]. [包含1个长尾词]",
      "media": {"src": "[url]", "alt": "[功能名]"}
    }
    // ×4
  ]
}
```

**SEO 规则**: 每个 `features[N].title` 是 H2/H3 级别标题, 含品类长尾词。

### S3: bento-2 — 2 大使用方式

```json
{
  "type": "bento-2",
  "title": "[数字] approaches to [品类]",
  "description": "For [用户场景A] and [用户场景B].",
  "columns": 2,
  "features": [
    {"title": "[方式A, 含关键词]", "description": "...", "media": {...}},
    {"title": "[方式B, 含关键词]", "description": "...", "media": {...}}
  ]
}
```

### S4: capability-tabs — 4 大核心能力

```json
{
  "type": "capability-tabs",
  "title": "Everything [品类] can do",
  "tabs": [
    {
      "id": "[tab-id]",
      "label": "[能力名, 1词]",
      "content": {
        "title": "[能力标题, 含关键词]",
        "description": "[描述, 50-80字符]",
        "media": {"src": "[url]", "alt": "[能力名]"}
      }
    }
    // ×4 (Design, Edit, Brand, Export 是通用四件套)
  ]
}
```

**SEO 规则**: tabs 是 Google 可能抓取的内容块, `content.title` 和 `content.description` 需要含关键词。

### S5: prompt-launcher — 交互入口

```json
{
  "type": "prompt-launcher",
  "title": "Try [品类] now",
  "description": "Describe what you want and let AI handle the rest.",
  "prompts": [
    {"text": "[场景1 prompt, 含品类关键词]"},
    {"text": "[场景2 prompt, 含品类关键词]"},
    {"text": "[场景3 prompt, 含品类关键词]"}
  ],
  "cta": {"text": "Generate", "href": "/home", "variant": "primary"}
}
```

**SEO 规则**: 3 个 prompt 各覆盖一个搜索意图:
1. 功能型 (如 "Create a professional poster for...")
2. 风格型 (如 "Design a modern poster with...")
3. 平台型 (如 "Generate a poster optimized for Instagram")

### S6: logo-loop — 社交证明

```json
{"type": "logo-loop", "text": "Trusted by millions of creators worldwide"}
```

### S7: cta-default — 首次转化

```json
{
  "type": "cta-default",
  "title": "Start Creating Free",
  "description": "No credit card. 50 free designs per month.",
  "buttons": [{"text": "Start Free", "href": "/home", "variant": "primary"}]
}
```

### S8: workflow-horizontal — 使用流程

```json
{
  "type": "workflow-horizontal",
  "title": "How [品类] works",
  "description": "Simple steps to professional results.",
  "layout": "horizontal",
  "steps": [
    {"title": "1. [动作动词]", "description": "[操作说明, 含关键词]"},
    {"title": "2. [动作动词]", "description": "[操作说明, 含关键词]"},
    {"title": "3. [动作动词]", "description": "[操作说明, 含关键词]"}
  ]
}
```

**SEO 规则**: 3 步流程覆盖 "how to" 搜索意图。`steps[N].title` 和 `description` 是 Google 可能提取为 Featured Snippet 的内容。

### S9: comparison-table — 竞品对比

```json
{
  "type": "comparison-table",
  "title": "[品类]: Lovart vs traditional tools",
  "description": "See why creators switch to Lovart for [品类].",
  "headers": ["Feature", "Lovart", "Traditional tools"],
  "highlightColumn": 1,
  "rows": [
    {"feature": "[维度1]", "lovart": "[优势1]", "traditional": "[劣势1]"},
    {"feature": "[维度2]", "lovart": "[优势2]", "traditional": "[劣势2]"},
    {"feature": "[维度3]", "lovart": "[优势3]", "traditional": "[劣势3]"},
    {"feature": "[维度4]", "lovart": "[优势4]", "traditional": "[劣势4]"},
    {"feature": "[维度5]", "lovart": "[优势5]", "traditional": "[劣势5]"}
  ]
}
```

**SEO 规则**: 5 行对比数据覆盖 "vs" 和 "alternative" 搜索意图。`rows[N].feature` 是关键词锚点。

### S10: cluster-block-dense — 价值卡片

```json
{
  "type": "cluster-block-dense",
  "title": "Why [品类] matters for [目标用户]",
  "description": "Key benefits of AI [品类].",
  "cards": [
    {"icon": "[icon-name]", "title": "[价值1]", "description": "[一句话解释]"},
    // ×6
  ]
}
```

**icon 可用值**: sparkle, refresh, brand, layout, download, zap, image, video, globe

### S11: feature-detail — 深度功能

```json
{
  "type": "feature-detail",
  "title": "Advanced [品类] features",
  "description": "Professional capabilities for [目标用户].",
  "items": [
    {"title": "[功能名]", "description": "[详细说明, 80-120字符]", "media": {...}},
    // ×4
  ]
}
```

**SEO 规则**: 4 个 feature 可以覆盖 4 个不同的长尾关键词。

### S12: proof-block — 社会证明

```json
{
  "type": "proof-block",
  "title": "Why creators choose Lovart",
  "description": "Join millions of creators who switched.",
  "cards": [
    {"icon": "sparkle", "title": "10x faster", "description": "..."},
    {"icon": "refresh", "title": "Unlimited variations", "description": "..."},
    {"icon": "brand", "title": "Always on-brand", "description": "..."}
  ]
}
```

### S13: faq — 长尾 SEO 金矿

```json
{
  "type": "faq",
  "title": "Frequently Asked Questions",
  "items": [
    {"question": "[含长尾关键词的问题]", "answer": "[答案, 80-150字符]"}
    // ×5-7
  ]
}
```

**SEO 规则 — FAQ 是最重要的长尾词覆盖层**:
每页至少 5-7 个 FAQ, 每个覆盖一个搜索意图:
1. 价格/免费相关 ("Is [品类] free?")
2. 新手相关 ("Do I need design experience for [品类]?")
3. 版权相关 ("Can I use [品类] outputs commercially?")
4. 格式相关 ("What formats can I export [品类] in?")
5. 对比相关 ("How is [品类] different from [竞品]?")
6. 技术相关 ("How does AI generate [品类]?")
7. 平台相关 ("Can I use [品类] on mobile?")

### S14: cta-default — 收口转化

```json
{
  "type": "cta-default",
  "title": "Ready to create [品类]?",
  "description": "Join millions of creators. Free 50 designs/month.",
  "buttons": [{"text": "Get Started Free", "href": "/home", "variant": "primary"}]
}
```

---

## 三、SEO 优化清单

### 3.1 页面级 SEO

| 要素 | 规范 | 示例 |
|------|------|------|
| **Slug** | `ai-[品类]-[差异化词]` | `ai-poster-maker`, `ai-video-generator-free` |
| **Title (Sanity)** | `[主关键词] — [价值主张] \| Lovart` | `AI Poster Maker — Create Professional Posters Instantly \| Lovart` |
| **Meta Description** | 120-160字符, 含主关键词+1个长尾词 | (由 Sanity `seo.description` 控制) |
| **H1** | = hero.title (≤60字符) | 同 title |
| **H2 来源** | bento.title + tabs.label + feature.title + faq.question | 至少 15+ 个 H2 |
| **图片 alt** | = section 标题或功能名 | `AI Poster Maker - Event Poster Design` |
| **Canonical** | 指向英文版 (如多语言) | `<link rel="canonical" href="https://www.lovart.ai/tools/ai-poster-maker">` |

### 3.2 关键词密度策略

| 层级 | 关键词 | 出现位置 |
|------|--------|----------|
| **主关键词** | `ai [品类]` | title, slug, H1, hero.description, cta.title, 至少 3 个 H2 |
| **次关键词** | `free ai [品类]`, `ai [品类] generator` | hero.description, bento, workflow |
| **长尾关键词** | `[品类] for [场景]`, `how to [品类]` | faq, workflow, comparison |
| **竞品关键词** | `[品类] vs [竞品]`, `[竞品] alternative` | comparison-table, faq |

### 3.3 搜索意图覆盖检查

| 意图 | 覆盖 Section | 状态 |
|------|-------------|------|
| 信息型 "what is" | hero.description | ☐ |
| 功能型 "can it do X" | bento-4, capability-tabs | ☐ |
| 操作型 "how to" | workflow-horizontal | ☐ |
| 对比型 "vs / alternative" | comparison-table, faq | ☐ |
| 价格型 "free / pricing" | faq | ☐ |
| 平台型 "for Instagram/YouTube" | prompt-launcher | ☐ |

### 3.4 页面内容质量评分 (自查)

| 维度 | 标准 | 权重 |
|------|------|------|
| 字数 | ≥800 词 (全页正文) | ★★★ |
| H2 数量 | ≥12 个 | ★★★ |
| 图片数 | ≥12 张 (slot 填充) | ★★ |
| FAQ 数量 | ≥5 条 | ★★★ |
| 关键词密度 | 主关键词出现在 ≥5 个 section | ★★ |
| 内链 | faq 中 1-2 个内部链接 | ★ |
| 外链 | faq 中 1 个权威引用 (可选) | ★ |

---

## 四、15 页执行模板

### 模板 A: 品类工具页 (如 Poster Maker, Flyer Maker, Banner Maker)

```
Slug:      ai-[品类]-maker
主关键词:  AI [品类] Maker
次关键词:  free ai [品类] generator, ai [品类] creator
长尾词:    [品类] for [场景], [品类] design online

Section 调整:
  S2 bento-4: 4 种品类类型 (如 Poster: Event, Business, Sale, Motivational)
  S3 bento-2: 2 种创建方式 (From scratch vs Upload reference)
  S4 tabs:    标准四件套 (Design, Edit, Brand, Export)
  S8 workflow: 3 步创建流程
  S9 comparison: Lovart vs Canva/Figma
  S13 faq:    5 条 — 价格/新手/版权/格式/vs竞品
```

### 模板 B: AI 能力页 (如 3D Texture, Consistent Character, Image-to-Image)

```
Slug:      ai-[能力名]
主关键词:  AI [能力名]
次关键词:  [能力名] generator, [能力名] ai tool
长尾词:    [能力名] for [行业], how to [能力名]

Section 调整:
  S2 bento-4: 4 种应用场景
  S3 bento-2: 技术方案对比 (Text-to-X vs Upload-to-X)
  S4 tabs:    技术四件套 (Generate, Refine, Style Transfer, Batch)
  S8 workflow: 3 步技术流程
  S9 comparison: Lovart vs standalone tools
  S13 faq:    6 条 — 技术原理/质量/格式/批量/场景/限制
```

### 模板 C: 平台专属页 (如 Instagram, YouTube, TikTok)

```
Slug:      ai-[平台]-[品类]
主关键词:  AI [平台] [品类]
次关键词:  [平台] [品类] maker, free [平台] [品类]
长尾词:    [平台] [品类] template, [平台] [品类] for [用户]

Section 调整:
  S2 bento-4: 4 种 [平台] 特定场景
  S3 bento-2: 尺寸/格式对比
  S4 tabs:    平台四件套 (Design, Resize, Schedule, Brand)
  S8 workflow: 3 步创作→发布流程
  S9 comparison: Lovart vs [平台] native tools
  S13 faq:    6 条 — 尺寸/格式/排期/品牌/分析/vs原生工具
```

---

## 五、Slug 命名规范

| 规则 | 示例 |
|------|------|
| `ai-` 前缀 | `ai-poster-maker` |
| 品类用名词 | `maker` > `generator` > `creator` > `designer` |
| 避免冗余 | `ai-poster-maker` ✓ / `ai-poster-maker-tool` ✗ |
| 免费版加 `-free` | `ai-poster-maker-free` |
| 竞品版用原名 | `canva-alternative`, `figma-alternative` |
| 平台版加平台名 | `ai-instagram-poster-maker` |

---

## 六、交付检查清单

每页上线前自查:

- [ ] slug 符合命名规范
- [ ] hero.title ≤60 字符, 含主关键词 + `| Lovart`
- [ ] hero.description 120-160 字符
- [ ] 14 个 section 全部有内容 (非空占位)
- [ ] ≥12 个 H2 标题
- [ ] FAQ ≥5 条, 每条覆盖不同搜索意图
- [ ] 所有 media.src 已填充图片
- [ ] comparison-table 有 5 行, 含具体数据
- [ ] feature-detail 有 4 个 item, 各有独立描述
- [ ] cluster-block-dense 有 6 个 card, 各有 icon
- [ ] alt 属性已填写 (非空)
- [ ] 多语言版本同步 (如有)
