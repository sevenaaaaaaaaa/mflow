# Sanity Composite Page Sections

为运营同学和 AI 提供完整的 section 组件清单。

- 渲染入口：`CompositeSectionRenderer.tsx`，按 `section.type` 字符串 dispatch。
- 数据来源：Sanity `compositePage` document 的 `bodyJson` 字段（顶层数组），每条 `{ type, ...其它字段 }`。
- 在线预览：访问 `/internal/composite-page-all` 查看所有新 type 的真实渲染。预览数据源 `apps/lovart/src/views/compositePage/internal/preview-data.json`。

## 预览页右侧 Variants 面板

桌面端（≥1024px）打开预览页时右侧会浮出 **Variants** 面板：

- **One each**（默认）：每个组件大类只渲染当前选中变体（比如 Hero 系列 5 个变体里只显示 1 个），点变体按钮切换
- **Show all**：33 个 section 全部展开
- 点变体按钮自动平滑滚动定位到对应 section，方便定向 review
- 移动端隐藏面板，全部 section 顺序铺开

## 写法约定

- 顶层数组：`bodyJson` 是 JSON 数组，每个元素一个 section
- 字段全部铺顶层：包括 `title` / `media` / `buttons[]` 等，**不要嵌套 `params`**
- 字段名严格按下表，常见错配会渲染空或显示占位灰块

### Sanity bodyJson 一条示例

```json
[
  {
    "type": "hero-split",
    "title": "Turn one product brief into",
    "highlightedText": "a full conversion funnel",
    "description": "Lovart helps Shopify teams ship a full creative funnel from one brief.",
    "buttons": [{ "text": "Design the funnel", "href": "/start", "variant": "primary" }],
    "media": { "src": "https://...", "alt": "..." }
  },
  { "type": "faq", "title": "FAQ", "items": [{ "question": "...", "answer": "..." }] }
]
```

## 共用类型

很多组件复用这几个基础对象：

### SectionHeading（标题/描述/小标签）

几乎所有组件都支持：

| 字段                      | 类型   | 说明                                                             |
| ------------------------- | ------ | ---------------------------------------------------------------- |
| `tag` / `badge` / `label` | string | 标题上方小字标签（"AI design agent" / "Buyer journey map" 之类） |
| `title`                   | string | 主标题                                                           |
| `highlightedText`         | string | 标题第 2 行（hero 类强调文字）                                   |
| `description`             | string | 标题下方描述段                                                   |

### SectionMedia（图片 / 视频）

图片和视频共用同一个 `media` 对象，由统一的 `<SectionMedia>` 渲染（`shared/index.tsx`）。**不传任何视频字段、且 `src` 不是视频后缀，就是纯图片** —— 旧数据零改动。

```ts
{
  src: string;            // 图片或视频 URL（CDN / 站内 /assets 路径都行）
  alt?: string;           // 缺省时多用 title 兜底
  objectPosition?: 'center'|'top'|'bottom'|'left'|'right'|'top-left'|'top-right'|'bottom-left'|'bottom-right';

  // —— 视频（全部可选）——
  type?: 'image' | 'video'; // 不传时按 src 后缀推断（.mp4 / .webm / .mov / .m4v 视为视频）
  poster?: string;          // 视频封面：未播放时占位 + 首屏 LCP，建议填
  autoplay?: boolean;       // 默认 true
  loop?: boolean;           // 默认 true
  muted?: boolean;          // 默认 true（iOS 自动播放必须静音）
  controls?: boolean;       // 默认 false
}
```

**视频默认静音自动循环播放**（营销页惯例），可逐条用上面字段覆盖（如 `"controls": true, "autoplay": false` 做点击播放的长演示）。把任意 `media` 的 `src` 换成视频 URL 即可，其余字段不变：

```json
{
  "type": "hero-cinematic",
  "title": "...",
  "media": { "type": "video", "src": "https://.../demo.mp4", "poster": "https://.../demo-cover.jpg" }
}
```

**支持视频的 section**：所有用 `media` 的内容位都支持 —— `hero-split` / `hero-cinematic` / `hero-mosaic` / `hero-gallery`、`feature-grid`（含 `bento-2/4/6`）、`feature-detail`、`portrait-grid-3/4`、`showcase-stacked` / `showcase-horizontal`、`capability-tabs`、`canvas-wall`、`blog-grid`、`workflow-vertical`。

**仅图片**：`comparison-before-after`（前后对比靠拖拽，图片语义）、`media-marquee`（横向跑马灯，多视频自动播放有性能问题）。

### SectionButton（按钮）

```ts
{ text: string; href?: string; variant?: 'primary' | 'secondary' | 'outline'; action?: 'openLogin' }
```

- `variant: 'primary'` 是实心主按钮，`secondary` / `outline` 是描边按钮
- 空 `href` 渲染为 `#`
- `action: 'openLogin'`：点击唤起登录弹窗（跳 `/home`），同时上报 `lovart.get.started.button.click`（埋点 `source: 'cta_section'`）— 仅 `cta-default` 当前支持；不传 action 则按 `href` 正常跳转

### Icon key 字典

`icon` 字段（cluster / proof / tool / journey 等多处用）支持下列 key（其它值会渲染为空）：

`chat` / `image` / `flask` / `brand` / `globe` / `refresh` / `search` / `pointer` / `video` / `sparkle` / `social` / `remove-bg`

---

# 组件清单（33 种）

按用途分组。所有示例直接复制即可用，把 `media.src` 换成真实图片 URL。

## Hero 区（5 种，页面首屏用）

### `hero-split` — 左文右图

视觉：左侧 tag + 标题 + 描述 + buttons，右侧 4:3 大图。

```json
{
  "type": "hero-split",
  "badge": "Shopify Growth System",
  "title": "Turn one product brief into",
  "highlightedText": "a full conversion funnel",
  "description": "...",
  "buttons": [
    { "text": "Design the funnel", "href": "/start", "variant": "primary" },
    { "text": "See product visuals", "href": "/showcase", "variant": "secondary" }
  ],
  "media": { "src": "https://...", "alt": "..." }
}
```

### `hero-cinematic` — 居中标题 + 全宽剧院图

视觉：标题居中（两行 + tag），下方 16:10 大图横铺。

字段同 `hero-split`（`tag` / `title` / `highlightedText` / `description` / `buttons` / `media`）。

### `hero-journey` — 居中标题 + 横向 step 卡片条

视觉：标题居中，下方一排 step 卡（每个含编号 + 标题 + 副标题 + 图标），中间穿插箭头。

```json
{
  "type": "hero-journey",
  "badge": "Buyer journey map",
  "title": "Design for every step",
  "highlightedText": "from click to repeat purchase",
  "description": "...",
  "buttons": [...],
  "journeyCards": [
    { "step": "01", "title": "Traffic hook", "subtitle": "...", "icon": "social" },
    { "step": "02", "title": "Landing page", "subtitle": "...", "icon": "pointer" }
  ]
}
```

`icon` 用上面的 icon key 字典。

### `hero-mosaic` — 居中标题 + 拼贴瓦片

视觉：4 块 mosaic 瓦片（图 + 小标题 + 副标题），桌面端不规则拼贴，移动端单列。

```json
{
  "type": "hero-mosaic",
  "title": "Fix the creative leaks",
  "highlightedText": "without restarting",
  "buttons": [...],
  "mosaicTiles": [
    { "title": "Touch Edit", "subtitle": "...", "media": { "src": "...", "alt": "..." } }
  ]
}
```

### `hero-gallery` — 居中标题 + 6 宫格工具瓦片

视觉：6 块 1:1 工具瓦（图 + label + sublabel），强调"产品矩阵入口"。

```json
{
  "type": "hero-gallery",
  "title": "Start anywhere in the stack,",
  "highlightedText": "keep one agent context",
  "buttons": [...],
  "toolTiles": [
    { "label": "Product Image Set", "sublabel": "PDP + marketplace + ads", "media": { "src": "...", "alt": "..." } }
  ]
}
```

---

## Bento / 网格 / Cluster（5 种）

### `bento-2` — 两栏特性卡

视觉：2 等宽大卡，每卡含 title + description + 大图。

```json
{
  "type": "bento-2",
  "title": "Two conversion jobs Lovart owns end-to-end",
  "description": "...",
  "features": [
    {
      "title": "Higher product-page confidence",
      "description": "...",
      "media": { "src": "...", "alt": "..." }
    }
  ]
}
```

### `bento-4` — 2×2 不规则四宫格

视觉：上排两等宽，下排左小右大（4:8 比例），共 4 个特性卡。字段同 `bento-2`。

### `bento-6` — bento 6 卡

视觉：左大 + 右上下 + 底排三等分，共 6 个特性卡。字段同 `bento-2`。

> `bento-2/4/6` 内部都复用 `feature-grid`，传不同的 `columns`（2/4/3）。如果想要纯 3 列对称网格，用下面的 `feature-grid`。

### `feature-grid` — 通用特性网格

视觉：N 列等宽网格，每卡 icon 或图 + 标题 + 描述。

```json
{
  "type": "feature-grid",
  "title": "...",
  "description": "...",
  "columns": 3,
  "features": [
    {
      "title": "Brand Kit",
      "description": "...",
      "media": { "src": "...", "alt": "...", "objectPosition": "top" }
    }
  ]
}
```

`columns` 支持 2/3/4，默认 3。`objectPosition` 控制图片裁剪位置（默认 `center`）。

### `cluster-block-dense` — 紧凑信息卡墙

视觉：3 列网格，每卡左 icon + 标题 + 描述。适合"6 个痛点 / 6 个能力"这类信息密集场景。

```json
{
  "type": "cluster-block-dense",
  "title": "Where Shopify funnels leak creative performance",
  "description": "...",
  "cards": [{ "icon": "chat", "title": "Ad-to-page mismatch", "description": "..." }]
}
```

---

## Tabs / Tool / Blog / 详情（4 种）

### `capability-tabs` — Tab 切换 + 大内容区

视觉：左 4 列 tab list（label + icon），右 8 列内容区（图 + 标题 + 描述 + bullets + cta）。可自动轮播。

```json
{
  "type": "capability-tabs",
  "title": "Four Lovart capabilities",
  "autoplayIntervalMs": 0,
  "tabs": [
    {
      "label": "Research context",
      "icon": "search",
      "content": {
        "title": "Use Web Search and uploads",
        "description": "...",
        "media": { "src": "...", "alt": "..." },
        "cta": { "text": "Map the category", "href": "/" },
        "points": ["bullet 1", "bullet 2"]
      }
    }
  ]
}
```

### `tool-grid` — 工具卡网格

视觉：3 列网格，每张工具卡含 icon + 名称 + 分类 + 描述 + tag 列表 + 评分。

```json
{
  "type": "tool-grid",
  "title": "Lovart tools mapped to Shopify growth tasks",
  "description": "...",
  "tools": [
    {
      "icon": "image",
      "name": "AI Product Image Generator",
      "category": "PDP / Catalog",
      "description": "...",
      "tags": ["Product", "PDP", "Catalog"],
      "href": "/tools/product-image",
      "rating": 4.9
    }
  ]
}
```

### `blog-grid` — 博客文章网格

视觉：3 列卡片，封面图 + 标题 + 摘要 + 日期。

```json
{
  "type": "blog-grid",
  "title": "Content hub for creative teams",
  "description": "...",
  "articles": [
    {
      "title": "How AI design agents differ from generators",
      "slug": "shopify-ai-design-agent-vs-generator",
      "excerpt": "...",
      "image": "https://...",
      "date": "Mar 12, 2026"
    }
  ]
}
```

`href` 可替代 `slug`；`media: {src, alt}` 可替代 `image`。

### `feature-detail` — 图文左右交错（多条）

视觉：N 个图文块，第 0 条图在右；`reverse: true` 让图在左。

```json
{
  "type": "feature-detail",
  "title": "Four building blocks",
  "description": "...",
  "items": [
    {
      "title": "Start with product and market context",
      "description": "...",
      "media": { "src": "...", "alt": "..." },
      "cta": { "text": "Build the brief", "href": "/", "variant": "primary" }
    },
    {
      "title": "Create product visuals that sell the use case",
      "description": "...",
      "reverse": true,
      "media": { "src": "...", "alt": "..." }
    }
  ]
}
```

### `canvas-wall` — 10 卡 bento 画布墙

视觉：左上 1 大卡 + 右上 5 小卡 + 底排 4 卡，每卡可显示作者 / likes / caption。

```json
{
  "type": "canvas-wall",
  "title": "A full Shopify asset wall",
  "description": "...",
  "cta": { "text": "Open the asset wall", "href": "/" },
  "items": [
    { "media": { "src": "...", "alt": "..." }, "author": "pdp.hero", "likes": 248, "caption": "PDP hero image" }
  ]
}
```

至少 10 条 item 视觉才完整。

---

## Portrait Grid（2 种）

### `portrait-grid-3` — 3 列方形卡（1:1）

视觉：3 张 1:1 卡片，每卡上图下文（title + subtitle + cta）。

```json
{
  "type": "portrait-grid-3",
  "title": "Three asset families every product launch needs",
  "description": "...",
  "cards": [
    {
      "title": "PDP and catalog visuals",
      "subtitle": "Hero shots, clean cutouts, lifestyle scenes.",
      "media": { "src": "...", "alt": "..." },
      "cta": { "text": "Generate PDP images", "href": "/" }
    }
  ]
}
```

### `portrait-grid-4` — 4 列竖版卡（3:4）

视觉：4 张 3:4 竖版卡片，字段同 `portrait-grid-3`（`aspect` 默认 `3:4`，可用 `1:1` / `9:16`）。

---

## Showcase（2 种，"产品流程"叙事）

### `showcase-stacked` — 上下堆叠展示

视觉：垂直堆叠 N 个图文块，每块大图 + 标题 + 描述 + cta。

```json
{
  "type": "showcase-stacked",
  "title": "From flat SKU photo to conversion-ready creative",
  "items": [
    {
      "media": { "src": "...", "alt": "..." },
      "title": "Product visuals — Generate desire",
      "description": "...",
      "cta": { "text": "Create product visuals", "href": "/" }
    }
  ]
}
```

### `showcase-horizontal` — 横向滚动展示

视觉：横向 carousel，每卡 16:10 大图 + 标题 + 描述 + cta，桌面端含左右箭头，移动端含上下导航。字段同 `showcase-stacked`。

---

## 跑马灯 / 输入 / Logo（3 种）

### `media-marquee` — 媒体横向跑马灯

视觉：图片不停横向滚动，每张图含 caption + 作者。

```json
{
  "type": "media-marquee",
  "title": "Creative range across the Shopify stack",
  "description": "...",
  "ctaText": "Explore more",
  "items": [{ "src": "...", "alt": "...", "caption": "USB", "author": "@mathidle", "width": 400, "height": 400 }]
}
```

### `prompt-launcher` — 居中输入框 + prompt 标签

视觉：居中输入框 + 下方 prompt pill 列表，点击 pill 填入 prompt。

```json
{
  "type": "prompt-launcher",
  "title": "Start from a real Shopify brief",
  "description": "...",
  "prompts": [{ "label": "PDP image refresh", "prompt": "I run a Shopify store selling..." }],
  "cta": { "text": "Generate" }
}
```

也支持 `suggestions: string[]`（简单字符串列表）、`input_placeholder`、`tip`。

> 触发"Generate"会唤起登录弹窗，跳 `/home`。

### `logo-loop` — 客户/品牌 logo 跑马灯

视觉：一行 logo 循环滚动，logo 列表写死在前端（27b / Huge / Deliveroo / Linktree / Spotify / TikTok）。

```json
{ "type": "logo-loop", "text": "Lovart is trusted by millions of designers, creatives, and brands." }
```

`text` 是 logo 上方一句话标题，可省略。

---

## CTA / 流程（3 种）

### `cta-default` — 居中 CTA 横幅

视觉：渐变背景中央卡片 + 大标题 + 描述 + 两按钮。

```json
{
  "type": "cta-default",
  "title": "Ready to turn one SKU into a full Shopify launch system?",
  "description": "...",
  "buttons": [
    { "text": "Design a Shopify launch", "href": "/", "variant": "primary" },
    { "text": "See the workflow", "href": "/", "variant": "secondary" }
  ]
}
```

支持登录按钮 — 把按钮的 `action` 设成 `openLogin`，点击就唤起登录弹窗（跳 `/home`），等同于以前 `CTAFooter` 的行为：

```json
{
  "type": "cta-default",
  "title": "Start designing with Lovart",
  "description": "...",
  "buttons": [{ "text": "Get started", "action": "openLogin", "variant": "primary" }]
}
```

> 用 `action: 'openLogin'` 时，`href` 会被忽略；同时会上报 `lovart.get.started.button.click` 埋点（source=`cta_section`）。

### `workflow-horizontal` — 横向 N 步流程

视觉：横向一排 step 卡（编号 + 标题 + 描述），适合简短"3 步搞定"。

```json
{
  "type": "workflow-horizontal",
  "title": "How-to workflow",
  "description": "...",
  "steps": [{ "step": 1, "title": "Upload context", "description": "..." }]
}
```

### `workflow-vertical` — 纵向 N 步流程（带图）

视觉：纵向 step 列表，每步附图，适合详细叙述。字段同 `workflow-horizontal`，每个 step 多一个 `media`。

```json
{
  "type": "workflow-vertical",
  "title": "Detailed Shopify launch workflow",
  "description": "...",
  "steps": [{ "step": 1, "title": "Research category", "description": "...", "media": { "src": "...", "alt": "..." } }]
}
```

---

## 对比（2 种）

### `comparison-table` — 多列对比表

视觉：表头一排，多行 feature，可高亮某一列。

```json
{
  "type": "comparison-table",
  "title": "Lovart vs common Shopify creative workflows",
  "description": "...",
  "headers": ["Need", "Single-purpose AI generator", "Manual design workflow", "Lovart AI Design Agent"],
  "highlightColumn": 3,
  "rows": [
    {
      "feature": "Start from business context",
      "values": [
        "Usually starts from one prompt",
        "Requires strategist + designer alignment",
        "Uses SKU, audience, offer, brand"
      ]
    }
  ]
}
```

`highlightColumn` 是 0-based 列索引（不含 feature 列）。

### `comparison-before-after` — 前后对比滑块

视觉：单图分左右两半（带可拖动竖杠），各贴 label。

```json
{
  "type": "comparison-before-after",
  "title": "Before & after",
  "description": "...",
  "aspect": "16:9",
  "before": { "media": { "src": "...", "alt": "..." }, "label": "Before" },
  "after": { "media": { "src": "...", "alt": "..." }, "label": "After Lovart" }
}
```

`aspect` 可用 `1:1` / `4:3` / `3:4` / `9:16` / `16:9`（默认 16:9）。

---

## 证言 / 评价（3 种）

### `testimonial` — 客户证言（轮播或卡片组）

```json
{
  "type": "testimonial",
  "testimonials": [
    {
      "quote": "We stopped treating every PDP image as a separate task.",
      "author": "Maya Lin",
      "role": "Founder, DTC wellness brand"
    }
  ]
}
```

> 也兼容旧字段 `quotes: [{ content, name, role }]`。

### `review-grid-3col` — 3 列评价网格

```json
{
  "type": "review-grid-3col",
  "title": "What changes when ecommerce teams work with an agent",
  "reviews": [
    {
      "title": "From SKU photo to campaign system",
      "body": "...",
      "author": "Lena Brooks",
      "role": "Founder, Glow Pantry"
    }
  ]
}
```

### `review-grid-4col` — 4 列评价网格

字段同 `review-grid-3col`，渲染为 4 列。

---

## 数据 / 信任 / 价格 / FAQ（4 种）

### `stats` — 数字统计条

视觉：一排大数字 + 小标签。

```json
{
  "type": "stats",
  "stats": [
    { "value": "1", "label": "Agent context" },
    { "value": "10+", "label": "Shopify asset surfaces" }
  ]
}
```

### `proof-block` — 4 卡信任 / 证据块

视觉：标题 + 2×2 卡片网格，每卡 icon + title + description。

```json
{
  "type": "proof-block",
  "title": "Why use Lovart for Shopify conversion work?",
  "description": "...",
  "cards": [{ "icon": "search", "title": "Context before pixels", "description": "..." }]
}
```

### `pricing-block` — 定价卡（接产品后端价格数据）

视觉：标题 + 描述 + 自动渲染的 Sku 价格列表（来自登录 / commercial SDK）。

```json
{
  "type": "pricing-block",
  "title": "Choose the level of Shopify creative workflow you need",
  "description": "..."
}
```

> 字段只需标题/描述；价格表自动从后端取，无需在 Sanity 里维护具体价格。

### `faq` — 问答列表

视觉：手风琴形式的 FAQ 列表。

```json
{
  "type": "faq",
  "title": "Frequently asked questions",
  "items": [{ "question": "Is Lovart a Shopify app or a design workflow?", "answer": "..." }]
}
```

---

# 常见错配排查

1. **写了组件但页面空白**：检查 `type` 字符串是否精确匹配（注意短横线 vs 驼峰）；不在表里的 type 直接返回 `null`。
2. **图片不显示**：`media.src` 必须是可访问的绝对 URL（CDN）或 `/assets/...` 站内路径。`object-cover` 默认裁剪，需要露顶部信息时给 `objectPosition: "top"`。
3. **按钮跳错**：`href` 留空会渲染成 `#`（停留当前页）。要触发登录弹窗的按钮在 `cta-default` 里用 `action: 'openLogin'`；`prompt-launcher` 的 Generate 按钮默认也走登录。
4. **icon 不出来**：`icon` 字段只认 [icon 字典](#icon-key-字典) 里的 key，自定义图标走 `media.src` 而非 `icon`。
5. **Bento variant 想要其它列数**：直接用 `feature-grid` + `columns: 2/3/4`，`bento-2/4/6` 只是预设别名。

---

# 老 8 种 type（兼容线上历史数据）

线上已存在的 features/tools 文章用的是早期 8 种 type，字段约定不同，由 `legacy/*.tsx` 渲染。新文档不要用这 8 种，**仅作向后兼容用途**：

`heroSection` · `contentSection` · `faqSection` · `textImageSection` · `threeColumnSection` · `testimonialSection` · `centeredInputSection` · `featureGridSection`

字段定义见 `types.ts` 的 `LegacySectionProps`。

---

# 维护备注（给开发者）

- 本目录是 section 组件的**唯一来源**。
- 新增 type 时：1) 在本目录添加组件文件；2) 在 `CompositeSectionRenderer.tsx` 的 `SECTIONS_MAP` 注册；3) 更新本 README + `views/compositePage/internal/preview-data.json`。
- 预览页 `/internal/composite-page-all` 和 Sanity bodyJson 现在使用**同一份**扁平格式（字段铺顶层，没有嵌套 `params`），由 `CompositeSectionRenderer` 统一渲染。
