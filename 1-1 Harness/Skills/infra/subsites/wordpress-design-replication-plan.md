# blogs.lovart.ai 设计复刻规划（lovart.ai 首页 + 模块化页面 → WordPress）

> **目标**：让 blogs 子站获得主站同款设计语言与模块化能力——但走**设计系统复刻**（tokens + 组件规范 + 数据对接），不是像素搬运。
> **系统化的兑现点**：MFlow 内容契约层产出 composite-v2 JSON → WP 侧适配器转成区块 → 同一份 JSON 在主站（Next.js）与子站（WordPress）渲染出同构设计。子站不再手排页面。
> **状态**：规划稿 v1.0（2026-10-04），待品牌方拍板技术路线后进入阶段 1。

## 一、设计源（复刻什么、从哪取）

| 源 | 内容 | 用途 |
|---|---|---|
| `Refresh-Page/preview-data.json` | **33 组件完整定义**（结构/内容/媒体） | 组件规范的唯一 SSOT |
| `Refresh-Page/landing-examples/en/` | 4+ 份完整页面 JSON（brand-trust / vs-competitor / gallery-funnel / full） | 页面级组装样例 |
| `FULL-STORYLINE-ORDERS.md` + `landing-storylines.json` | 模块顺序逻辑（O1-O4 + 7 故事线） | 页面骨架复刻 |
| lovart.ai 线上 | 设计 tokens（色/字/间距/断点/动效）+ 组件视觉细节 | **需从前端 CSS/设计稿提取一次**（唯一需要设计方配合的动作） |

## 二、技术路线（待拍板的唯一大决策）

| 路线 | 做法 | 优点 | 代价 | 适配度 |
|---|---|---|---|---|
| **R1 · Gutenberg 原生区块**（推荐） | 每组件一个自定义区块（block.json + React 编辑端 + PHP 渲染端） | 原生、无插件锁定、编辑体验与未来一致 | 33 组件开发量最大（但分期做） | ★★★★★ |
| R2 · ACF Blocks | ACF Pro 字段组 + PHP 区块渲染 | 开发快一半、编辑表单友好 | 依赖 ACF Pro 授权 | ★★★★ |
| R3 · 页面构建器（Elementor/Bricks） | 构建器搭模板 | 最快 | 样式漂移、数据不可编程——违背系统化初衷 | ★★ |
| R4 · 混合 | FSE 区块模板（首页/归档）+ 文章内嵌精简区块集 | 平衡 | 两套体系维护 | ★★★ |

> 推荐逻辑：R1 与 MFlow 的对接最干净——**composite-v2 JSON 的字段结构与 Gutenberg 区块属性一一映射**（适配器最薄）；R2 次之；R3 否决。

## 三、范围分层（33 组件不全做）

| 优先级 | 范围 | 组件 |
|---|---|---|
| **P0 骨架** | 主题基座：header/footer/文章模板/归档页对齐主站设计语言 + blogs **首页**（模块化聚合：blog-grid + tool-grid 型布局 + CTA） | 设计 tokens + 版式系统 |
| **P1 核心组件**（约 12 个） | 文章内嵌 + 落地式页面主力 | hero-split · bento-4/6 · capability-tabs · tool-grid · blog-grid · comparison-table · proof-block · stats · testimonial · faq · cta-default · workflow-horizontal |
| **P2 补全** | 按内容需求逐个加 | 其余 21 个（hero 系 4/对比 before-after/pricing/review-grid/showcase 系/portrait 系/media-marquee/prompt-launcher/logo-loop/canvas-wall/feature-detail/workflow-vertical/cluster-block-dense） |

## 四、与 MFlow 管线对接（系统化的核心交付）

```
MFlow 内容契约层（composite-v2 JSON，34 型注册表已验证）
   → 新增适配器 publish_adapters/wp_blocks.py：
      JSON section[] → Gutenberg block markup（区块名映射 + 属性映射 + 图片入媒体库）
   → publish-to-wp.py 扩展：REST 创建 block 编辑页面（沿用凭证/dry-run 闸）
   → WP 端区块渲染端输出与主站同构设计
```

- 图片：`/api/assets/*` 素材管线产出 → WP 媒体库（适配器上传 + 引用替换）
- 门禁：四钩子在 JSON 阶段照常跑（过门禁才转区块）；发布闸 dry-run 不变
- 体验层：WP 页面纳入 page-experience 每周清单（URL 扫描含 blogs 域）

## 五、子项目配置落地

brand profile `subSites[blogs]` 更新：
```json
{"techStack": "WordPress + Gutenberg 自定义区块（设计系统复刻自 lovart.ai）",
 "designSystem": {"source": "preview-data.json + 主站 tokens", "components": "P0 骨架 + P1 12 组件起步", "adapter": "publish_adapters/wp_blocks.py"},
 "capabilities.site": {"mode": "independent", "site": {"id": "blogs", "sections": ["home", "blog", "article", "archive"]}}}
```

## 六、阶段计划

| 阶段 | 内容 | 产出 | 规模 |
|---|---|---|---|
| 0 | 设计 tokens 提取（主站 CSS/设计稿）+ 组件映射表定稿（33 → P0/P1/P2）+ 路线拍板 | tokens.json + 映射表 | 小（需设计方一次配合） |
| 1 | 主题基座：header/footer/文章模板/归档 + blogs 首页模块化 | 设计一致的可视骨架 | 中 |
| 2 | P1 12 组件区块 | 组件库 v1 | 大（核心投入） |
| 3 | MFlow 适配器 wp_blocks.py + 管线打通（dry-run 验证） | JSON→WP 直通 | 中 |
| 4 | P2 组件按需 + page-experience 纳管 | 体验闭环 | 按需 |

## 七、开放决策（品牌方拍板）

1. **路线**：R1 原生区块 vs R2 ACF？（推荐 R1）
2. **主题基座**：现有主题子主题化，还是 block theme（如基于 Spectra/自主）重建？
3. **设计配合**：tokens 提取由设计方出一份，还是从线上 CSS 反推（可做但精度略低）？
4. **首页范围**：blogs 首页是否承载营销模块（hero/canvas-wall），还是纯内容聚合（blog-grid 为主）？
