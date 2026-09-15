# Lovart Blog 封面制作计划

> 版本：v1.5 | 日期：2026-06-22 | 状态：v1.5 液态玻璃 + 黑线白填版
> 执行路径：第一步撰写提示词 → 第二步交给 Lovart 制作
>
> **v1.5 变更摘要**（基于 v1.4 实践效果不佳修复）：
> 1. 背景质感：从"有机流动光晕"升级为"苹果 Liquid Glass 液态玻璃"——半透明材质、折射反射、动态光效、层次感、光泽感
> 2. 元素线条：从"Shade 深色 6px 粗线条"改为"黑色（#000000）流动手绘线条勾边"——更灵动、不死板
> 3. 元素填充：核心要素用白色（#FFFFFF）填充——形成黑线白填的鲜明对比
> 4. 配色逻辑：分类差异体现在背景液态玻璃的色调上，元素统一为黑线白填
>
> **v1.4 变更摘要**（保留）：
> 1. 背景纹理：有机流动光晕（radial + multi-point light overlay）
> 2. 质感定义：中低饱和度、柔和哑光、丝绸/云雾质感
>
> **v1.3 变更摘要**（保留）：
> 1. 线条粗细：2px → 6px
> 2. 居中约束：exactly centered, symmetrically composed, bullseye center
> 3. 对比度：≥ 7:1（AAA 级）

---

## 一、基础盘点：Sanity 线上 Blog 现状

### 1.1 总量概览

| 指标 | 数量 |
|------|------|
| Blog 总数 | **10,231** |
| 有分类标签 | 9,579 |
| 无分类标签 | 652 |
| 有封面 (cover) | 9,446 |
| 无封面 | **785** |
| 有 OG Image | 9,260 |

### 1.2 语言分布

| 语言 | 数量 | 备注 |
|------|------|------|
| 英文 (en) | 1,343 | 优先制作 |
| 中文 (zh) | 898 | 后续按需 |
| 日文 (ja) | 895 | 后续按需 |
| 其他 | ~7,095 | Lovart 101 批量生成内容 |

### 1.3 分类分布（线上实际有效分类）

| 分类 | 数量 | 占比 | 封面策略优先级 |
|------|------|------|---------------|
| **Lovart 101** | 6,394 | 66.7% | P2 — 数量大，可按子主题分批 |
| **How-To** | 1,158 | 12.1% | P1 — 核心流量分类 |
| **Best Practice** | 832 | 8.7% | P1 — 产品使用技巧 |
| **Better Design** | 260 | 2.7% | P1 — 设计知识 |
| **Topics** | 232 | 2.4% | P2 — 精选/置顶 |
| **Insight & Trend** | 138 | 1.4% | P1 — 行业洞察 |
| **Branding** | 49 | 0.5% | P2 — 品牌相关 |
| **无分类** | 652 | 6.8% | P3 — 需先补分类 |
| Design / Video / Canvas | 0 | — | 线上无文章，跳过 |

### 1.4 现有封面问题

当前 9,446 篇有封面的 blog，封面来源为：
- **liblib 占位图池**：56 张随机分配的通用图片，与文章内容无关
- **blogcover 池**：55 张 (blogcover-011 ~ blogcover-065)，同样与内容无直接关联
- **核心问题**：封面与文章主题脱节，缺乏统一设计语言，无法通过封面区分分类

---

## 二、设计风格定义

### 2.1 风格参考

融合 **Anthropic** 与 **Linear** 的设计语言：

| 维度 | Anthropic 参考 | Linear 参考 | 我们的取值 |
|------|---------------|-------------|-----------|
| **背景** | 暖白/奶油色 (#F5F3EF) | 近黑 (#0A0A0A) | **双模式：浅色底 + 深色底** |
| **构图** | 极致留白，非对称布局 | 三栏网格，卡片式 | **中心锚点 + 30-40% 负空间** |
| **图形** | 几乎零装饰，粗下划线强调 | 抽象几何图形（圆、线、节点） | **2-3 个抽象几何元素组合** |
| **色彩** | 黑白为主，零渐变 | 深灰层次，微弱蓝紫调 | **每分类独立配色，克制使用** |
| **字体** | 几何无衬线 + 经典衬线 | 现代无衬线，紧凑字距 | **不在封面放文字，留白给标题叠加** |
| **情绪** | 学术感、可信、克制 | 科技感、精致、前沿 | **简洁、灵动、有实际意义** |

### 2.2 核心设计原则

1. **背景 + 中心抽象符号**：整体构图 = **液态玻璃背景** + **精确居中**的 2-3 个抽象几何元素
2. **分类即色彩**：每个分类的液态玻璃背景有不同的色调倾向，用户一眼识别文章类型
3. **元素即语义**：抽象元素从文章主题中提取核心场景，用流动手绘线条表达
4. **克制即高级**：不超过 3 种颜色，不超过 3 个元素，不少于 30% 负空间
5. **系列即品牌**：同分类封面构成视觉系列，统一中有变化
6. **可见性优先**：元素必须清晰可辨、精确居中——任何"优雅但看不见"的设计都是失败的
7. **液态玻璃美感**（v1.5 新增）：背景参考苹果 Liquid Glass 设计语言——半透明材质、折射反射、动态光效、层次感、光泽感；不是死板的色块，而是有物理质感的玻璃
8. **灵动线条**（v1.5 新增）：元素用黑色流动手绘线条勾边，核心要素用白色填充——线条要灵动不死板，像手写笔触而非机械直线

### 2.3 禁止元素

- 写实照片（stock photo）
- 卡通/漫画风格
- 纯扁平图标堆砌
- 渐变文字
- 超过 3 种主打色
- 满版构图（无负空间）
- 文字（封面不含任何文字，文字由前端叠加）
- **几何渐变**（v1.4 新增）：禁止 linear gradient、diagonal gradient、radial gradient 等任何几何渐变——背景必须是有机流动的光晕
- **噪点/颗粒纹理**（v1.4 新增）：禁止 film grain、noise、颗粒感纹理——背景必须是高斯模糊的色块流动
- **硬边色块**（v1.4 新增）：禁止色块之间有清晰的硬边过渡——所有色彩过渡必须极度柔和
- **高饱和度**（v1.4 新增）：禁止鲜艳刺眼的颜色——饱和度保持中低，柔和哑光

---

## 三、分类配色方案（基于 Lovart 官方 VI 系统 v1.0）

### 3.0 Lovart 官方 VI 色彩体系总览

封面配色严格遵循 Lovart Brand Guidelines v1.0 中定义的色彩体系，不引入任何品牌外的颜色。

**主色（Primary）**：
| 名称 | HEX | RGB | 用途 |
|------|-----|-----|------|
| Cloud | `#F0F0F0` | 240/240/240 | 浅色模式基础背景 |
| Charcoal | `#1B1B1A` | 27/27/26 | 深色模式基础背景 / 主文字色 |

**辅色（Secondary，4 组 × 3 级）**：

| 色系 | Light（浅） | Theme（饱和） | Shade（深） |
|------|------------|-------------|------------|
| Lime 绿 | `#E8FF8D` | `#D0FC16` | `#6B6D02` |
| Rose 粉 | `#FFCDEE` | `#FF51C7` | `#670547` |
| Azure 蓝 | `#C7E0FF` | `#197FFF` | `#022754` |
| Flame 橙红 | `#FFE3E0` | `#FF5040` | `#540800` |

**补充色（Supplemental，4 组 × 3 级）**：

| 色系 | Light（浅） | Theme（饱和） | Shade（深） |
|------|------------|-------------|------------|
| Bare 橙 | `#FFDCB9` | `#FF7017` | `#491B00` |
| Cotton 黄 | `#FFF2A8` | `#FFE24E` | `#77562C` |
| Iris 紫 | `#DDC6FE` | `#924AFF` | `#280C51` |
| Mint 翠绿 | `#CEFFED` | `#4BD460` | `#003220` |

**组合色（Color Combinations，13 组 × Light/Theme/Shade）**：

| 组合名 | Light 背景 | Light 前景 | Theme 背景 | Theme 前景 | Shade 背景 | Shade 前景 |
|--------|-----------|-----------|-----------|----------|-----------|----------|
| Neutral | `#F0F0F0` | `#000000` | `#949494` | `#D4FF6A` | `#1A1A1A` | `#F5F5F0` |
| Lime | `#E8F5A0` | `#6B6B00` | `#D0FC16` | `#0D3B2E` | `#6B6B00` | `#F5F5D0` |
| Orange | `#FFD4B8` | `#3D1F00` | `#FF7A1A` | `#3D1F00` | `#3D1F00` | `#FFF4B8` |
| Yellow | `#FEF3C7` | `#6B4423` | `#FCD34D` | `#6B4423` | `#6B4423` | `#FEF3C7` |
| Green | `#CFFFE9` | `#042A24` | `#48D85E` | `#042A24` | `#042A24` | `#CFFFE9` |
| Blue | `#C4DFFF` | `#2E8CFF` | `#1A7AFF` | `#FFF4B8` | `#0A2540` | `#FFC4E0` |
| Purple | `#E6D5F5` | `#8B6914` | `#8B4BF7` | `#F5E6D5` | `#2D1B4E` | `#F5E8A8` |
| Pink | `#F9D6E8` | `#5E0A3C` | `#FA5CB8` | `#FDF0E6` | `#5E0A3C` | `#FDF0E6` |
| Red | `#FFE4E1` | `#6B7B00` | `#FF5A4A` | `#FFF8F0` | `#4A0A00` | `#FFE4D6` |

### 3.1 Blog 分类 → VI 配色映射

每个 blog 分类对应一个 VI 组合色系。关键原则（v1.5 重写）：**分类差异体现在背景液态玻璃的色调上**，元素统一为**黑色（#000000）流动手绘线条勾边 + 白色（#FFFFFF）填充**，不再使用 Shade 深色线条。这样既保证元素在任何色调背景上都清晰可见，又让分类差异集中在背景质感上。

| 分类 | 映射 VI 组合 | 背景液态玻璃色调 (Light) | 背景液态玻璃色调 (Theme) | 元素勾边 | 元素填充 | 色彩温度 |
|------|------------|-------------------------|-------------------------|---------|---------|---------|
| **Lovart 101** | **Lime** | `#E8F5A0` Lime Light | `#D0FC16` Lightning | `#000000` 黑色 | `#FFFFFF` 白色 | 暖-黄绿 |
| **How-To** | **Green** | `#CFFFE9` Mint Light | `#48D85E` Jade | `#000000` 黑色 | `#FFFFFF` 白色 | 冷-绿 |
| **Best Practice** | **Blue** | `#C4DFFF` Haze Light | `#1A7AFF` Azure | `#000000` 黑色 | `#FFFFFF` 白色 | 冷-蓝 |
| **Better Design** | **Orange** | `#FFD4B8` Bare Light | `#FF7A1A` Citrus | `#000000` 黑色 | `#FFFFFF` 白色 | 暖-橙 |
| **Insight & Trend** | **Purple** | `#E6D5F5` Iris Light | `#8B4BF7` Amethyst | `#000000` 黑色 | `#FFFFFF` 白色 | 冷-紫 |
| **Topics** | **Yellow** | `#FEF3C7` | `#FCD34D` Naples | `#000000` 黑色 | `#FFFFFF` 白色 | 暖-金 |
| **Branding** | **Pink** | `#F9D6E8` | `#FA5CB8` Peony | `#000000` 黑色 | `#FFFFFF` 白色 | 暖-粉 |
| **无分类** | **Neutral** | `#F0F0F0` Cloud | `#D4FF6A` Lime Accent | `#000000` 黑色 | `#FFFFFF` 白色 | 中性 |

### 3.2 配色使用规则（v1.5 液态玻璃 + 黑线白填版）

- **元素勾边（黑色 #000000）**：所有抽象元素统一使用黑色流动手绘线条勾边，100% 不透明度，线条粗细适中（约 4-6px），**流动手绘感**而非机械直线
- **元素填充（白色 #FFFFFF）**：核心要素（外框内部、图标主体）用白色填充，形成黑线白填的鲜明对比，在任何色调背景上都清晰可见
- **液态玻璃背景（v1.5 重写）**：参考苹果 Liquid Glass 设计语言，具体规范：
  - **半透明材质**：背景呈现真实玻璃的半透明质感，能折射和反射光线，不是纯色也不是简单渐变
  - **折射反射**：有镜面高光和折射效果，光线穿过玻璃时产生轻微扭曲和汇聚
  - **动态光效**：有明显的光泽感和高光点，光线随玻璃曲面流动
  - **层次感**：多层玻璃叠加，有深度和立体感，不是扁平的
  - **色调倾向**：使用该分类的 Light 色作为玻璃的底色调，Theme 色作为高光和折射色
  - **圆角适配**：玻璃边缘自然圆润，与元素形态呼应
  - **描述词模板**：`Apple Liquid Glass style background, translucent glass material with refraction and reflection, dynamic light effects, glossy specular highlights, layered depth, frosted glass texture with [Light 色] tint, [Theme 色] highlights and refraction, smooth curved edges, realistic optical properties`
  - **禁止**：纯色背景、几何渐变、噪点颗粒、硬边色块、扁平无质感
- **深色背景模式**：使用 Shade 级深色液态玻璃（深色基底 + Theme 级光晕折射）
- **禁止**：使用任何不在上述 VI 体系中的颜色（元素的黑白色除外，黑白是通用的）

---

## 四、抽象元素库

### 4.1 元素设计语法

每个封面由 **1 个核心元素 + 1-2 个辅助元素** 组成，遵循以下语法：

```
[外框几何] + [内部线条图形] + [可选：连接线/光点]
```

**外框几何**（选择其一）：
- **未封闭圆形**：代表完整、循环、入门（Lovart 101、Best Practice）
- **圆角矩形**：代表结构、工具、实用（How-To、Branding）
- **三角形**：代表方向、趋势、洞察（Insight & Trend、Topics）
- **六边形**：代表系统、网络、专业（Better Design）
- **菱形**：代表精选、价值、品牌（Topics、Branding）

**内部线条图形**（根据文章主题选择）：
- 手绘线条手 → 人机协作、AI 交互
- 线条画笔 → 创作工具、设计
- 线条播放键 → 视频、动态内容
- 线条齿轮 → 工作流、效率
- 线条眼睛 → 洞察、趋势、分析
- 线条灯泡 → 创意、灵感、Best Practice
- 线条书本 → 学习、入门、Lovart 101
- 线条对比符号 (VS) → 对比、评测
- 线条节点网络 → 系统思维、行业方案
- 线条盾牌 → 品牌、信任、安全

### 4.2 按分类的元素组合规范

| 分类 | 外框 | 核心线条元素 | 辅助元素 | 示意描述 |
|------|------|-------------|---------|---------|
| **Lovart 101** | 未封闭圆形 | 线条书本 或 线条灯泡 | 小光点 ×3 | "一本打开的书被未封闭的圆环环绕，三个小光点散落在圆环外侧" |
| **How-To** | 圆角矩形 | 线条齿轮 或 线条画笔 | 箭头连接线 | "圆角矩形内有一支线条画笔，右侧用箭头连接到一个小齿轮" |
| **Best Practice** | 未封闭圆形 | 线条灯泡 或 线条手指 | 小圆点轨迹 | "灯泡居中，被未封闭圆环环绕，圆环上有三个等距小圆点" |
| **Better Design** | 六边形 | 线条画笔 或 线条眼睛 | 辅助几何碎片 | "六边形内有一只线条眼睛，周围漂浮着 2-3 个小三角形碎片" |
| **Insight & Trend** | 三角形 | 线条眼睛 或 线条节点网络 | 上升箭头线 | "向上的三角形内是节点网络图，右侧有一条上升趋势箭头" |
| **Topics** | 菱形 | 根据具体主题选择 | 星形光点 | "菱形内是主题相关元素，四个顶点各有一个小星形光点" |
| **Branding** | 菱形 或 圆角矩形 | 线条盾牌 或 线条画笔 | 品牌色块 | "菱形内是线条盾牌，左下角有一个小色块点缀" |

### 4.3 元素风格约束（v1.5 黑线白填版）

- **线条颜色**：黑色（`#000000`），100% 不透明度
- **线条粗细**：约 4-6px，均匀但不死板
- **线条风格**：**流动手绘感**——像手写笔触，有微妙的弧度、粗细变化和不完美感，**禁止机械直线**。线条要灵动、活泼，像毛笔或马克笔的手绘笔触，而非 CAD 制图的僵硬线条
- **填充颜色**：白色（`#FFFFFF`），100% 不透明度，填充核心要素内部
- **填充范围**：外框内部、图标主体用白色填充，辅助元素可不填充或半透明白色
- **光晕**：可选，使用 Theme 色低透明度（10-15%）点缀，不喧宾夺主
- **尺寸**：核心元素占画面 40-50%，辅助元素各占 10-15%
- **居中约束**：所有元素组合必须**精确居中于画布中心**，用 "exactly centered, symmetrically composed, bullseye center of canvas" 强约束，禁止偏移
- **对比度**：黑线白填在任何色调背景上都有极高对比度，确保清晰可辨

---

## 五、提示词模板

### 5.1 通用模板结构

每篇 blog 的提示词由以下部分组成：

```
[全局风格指令] + [分类配色指令] + [文章主题提取] + [元素组合指令] + [构图指令] + [负面约束]
```

### 5.2 全局风格指令（所有封面共用，v1.5 液态玻璃 + 黑线白填版）

```
Create a 16:9 blog cover image (2400x1350px).

STYLE: Minimalist abstract illustration with hand-drawn flowing line art. Clean,
restrained, confident. No photos, no clip art, no cartoons, no text. Elements drawn
with BLACK (#000000) flowing hand-drawn lines — like brush or marker strokes, fluid
and lively, NOT mechanical straight lines. Core elements filled with WHITE (#FFFFFF)
for strong contrast. Soft optional glow at element intersections.

COMPOSITION: EXACTLY CENTERED single focal point. All elements must be symmetrically
composed at the bullseye center of the canvas — no off-center placement, no scattered
layout. 30-40% negative space reserved for text overlay (bottom-left or bottom-center
region). Elements should feel intentionally placed at the exact center, not randomly
distributed.

BACKGROUND (CRITICAL — APPLE LIQUID GLASS STYLE):
The background MUST follow Apple's Liquid Glass design language — translucent glass
material with realistic optical properties. The background must have:
- Translucent material: semi-transparent glass that refracts and reflects light, NOT
  solid color, NOT simple gradient
- Refraction & reflection: specular highlights and light refraction, slight distortion
  and convergence as light passes through glass
- Dynamic light effects: obvious glossiness and highlight points, light flowing along
  glass curves
- Layered depth: multiple glass layers stacked, creating depth and dimensionality,
  NOT flat
- Color tint: use the category's Light color as glass base tint, Theme color for
  highlights and refraction accents
- Smooth curved edges: glass edges naturally rounded, echoing element forms
- Realistic optical properties: like real frosted glass with physical material quality
Absolutely NO solid color, NO geometric gradient, NO noise/grain, NO flat texture.

MOOD: Professional yet approachable. Smart, modern, inspiring. Like Apple's Liquid
Glass UI meets a design tool's brand identity. Glossy, layered, with physical depth.

VISIBILITY REQUIREMENTS (CRITICAL):
- Element lines: BLACK (#000000) flowing hand-drawn strokes, clearly visible
- Element fills: WHITE (#FFFFFF) solid fill, strong contrast against any background
- All elements must be exactly centered on the canvas
- Black lines + white fills ensure maximum visibility on any glass background
```

### 5.3 分类配色指令（按分类替换，v1.5 液态玻璃版）

```
COLOR PALETTE FOR [CATEGORY]:
- Background: APPLE LIQUID GLASS STYLE using [Light 背景色] as glass base tint and
  [Theme 饱和色] for highlights and refraction. Translucent glass material with
  refraction, reflection, dynamic light effects, layered depth, glossy specular
  highlights. Realistic optical properties like frosted glass. NOT solid color,
  NOT geometric gradient, NOT flat texture.
- Element stroke: BLACK (#000000) flowing hand-drawn lines, 100% opacity, fluid
  and lively brush/marker strokes, NOT mechanical straight lines
- Element fill: WHITE (#FFFFFF) solid fill for core elements, strong contrast
- Optional glow: [Theme 饱和色] at 10-15% opacity, subtle accent only
- No other colors. Black lines + white fills + tinted glass background only.
- CRITICAL: Elements must be black-line-white-fill, clearly visible on glass background.
```

### 5.4 元素组合指令（按文章主题定制，v1.5 黑线白填版）

这是每篇文章需要单独定制的部分。根据文章标题和描述，提取核心场景，映射到元素库中的组合。

**模板**：
```
CENTRAL ELEMENTS (ALL EXACTLY CENTERED ON CANVAS, BLACK LINES + WHITE FILLS):
- [外框几何]: A [外框描述], positioned at the EXACT CENTER of the canvas (bullseye
  center, symmetrically composed), sized at ~45% of frame width, outlined with BLACK
  (#000000) flowing hand-drawn lines (fluid brush/marker strokes, NOT mechanical),
  filled with WHITE (#FFFFFF) solid
- [核心线条元素]: Inside the [外框], a hand-drawn line art of [具体描述],
  drawn with BLACK (#000000) flowing hand-drawn lines, positioned at the center of
  the outer shape, filled with WHITE (#FFFFFF) where appropriate
- [辅助元素]: [辅助元素描述], positioned symmetrically around the center
  (balanced left-right and top-bottom), smaller scale (~15% of frame),
  in BLACK (#000000) hand-drawn lines, optional WHITE fill
- Optional subtle glow behind central element: [Theme 饱和色] at 10-12% opacity
- CRITICAL: The entire element group must form a single centered focal point at
  the bullseye center of the canvas. No element may drift off-center.
- CRITICAL: All lines must be flowing hand-drawn style, NOT mechanical straight lines.
  All core elements must be filled with WHITE, outlined with BLACK.
```

### 5.5 负面约束（所有封面共用）

```
DO NOT INCLUDE:
- Any text, letters, numbers, or typography
- Realistic photographs or stock images
- Cartoon or comic-style illustrations
- Flat icon collections or emoji
- More than 3 distinct geometric elements
- More than 2 distinct colors (plus background)
- Gradient fills on shapes (only solid colors with opacity)
- Any element in the bottom-left 30% zone (reserved for text overlay)
```

### 5.6 完整提示词示例

**示例 1：How-To 类文章**
> 文章：*How to Create Facebook Ad Creatives with AI*
> 映射 VI 组合：**Green**（背景液态玻璃色调 `#CFFFE9` Mint Light，高光 `#48D85E` Jade）

```
Create a 16:9 blog cover image (2400x1350px).

STYLE: Minimalist abstract illustration with hand-drawn flowing line art. Clean,
restrained, confident. No photos, no clip art, no cartoons, no text. Elements drawn
with BLACK (#000000) flowing hand-drawn lines — like brush or marker strokes, fluid
and lively, NOT mechanical straight lines. Core elements filled with WHITE (#FFFFFF)
for strong contrast. Soft optional glow at element intersections.

COMPOSITION: EXACTLY CENTERED single focal point. All elements must be symmetrically
composed at the bullseye center of the canvas — no off-center placement, no scattered
layout. 30-40% negative space reserved for text overlay (bottom-left region).

BACKGROUND (CRITICAL — APPLE LIQUID GLASS STYLE):
Apple Liquid Glass style background using #CFFFE9 (Mint Light) as glass base tint and
#48D85E (Jade) for highlights and refraction. Translucent glass material with refraction,
reflection, dynamic light effects, layered depth, glossy specular highlights. Realistic
optical properties like frosted glass with green tint. Multiple glass layers stacked
creating depth. Light flowing along glass curves with bright highlight points.
Absolutely NO solid color, NO geometric gradient, NO noise/grain, NO flat texture.

COLOR PALETTE: How-To category — mapped to Lovart VI "Green" combination.
- Background: APPLE LIQUID GLASS, #CFFFE9 glass tint, #48D85E highlights/refraction
- Element stroke: BLACK (#000000) flowing hand-drawn lines, 100% opacity
- Element fill: WHITE (#FFFFFF) solid fill for core elements
- Optional glow: #48D85E at 10-12% opacity, subtle accent only

CENTRAL ELEMENTS (ALL EXACTLY CENTERED ON CANVAS, BLACK LINES + WHITE FILLS):
- A rounded rectangle (corner radius 24px), positioned at the EXACT CENTER of the canvas
  (bullseye center, symmetrically composed), ~45% of frame width, outlined with BLACK
  (#000000) flowing hand-drawn lines, filled with WHITE (#FFFFFF) solid
- Inside the rectangle: a hand-drawn line art of a megaphone/speaker icon
  (representing ad creative), drawn with BLACK (#000000) flowing hand-drawn lines,
  positioned at the center of the rectangle, filled with WHITE (#FFFFFF)
- A small arrow pointing right, connecting to a tiny circle (representing AI
  transformation), positioned symmetrically to the right of center, in BLACK (#000000)
  hand-drawn lines
- Three small dots positioned symmetrically around the rectangle, in BLACK (#000000)
- Optional subtle glow behind central element, #48D85E at 10% opacity
- CRITICAL: The entire element group must form a single centered focal point at the
  bullseye center of the canvas. No element may drift off-center.
- CRITICAL: All lines must be flowing hand-drawn style, NOT mechanical straight lines.

VISIBILITY REQUIREMENTS (CRITICAL):
- Element lines: BLACK (#000000) flowing hand-drawn strokes, clearly visible
- Element fills: WHITE (#FFFFFF) solid fill, strong contrast against glass background
- All elements must be exactly centered on the canvas
- Black lines + white fills ensure maximum visibility on any glass background

DO NOT INCLUDE: Any text, photos, cartoons, icons, more than 3 elements,
more than 2 colors (black + white only for elements), solid color backgrounds,
geometric gradients, noise, grain, flat textures, mechanical straight lines,
or elements in the bottom-left text zone.
```

**示例 2：Insight & Trend 类文章**
> 文章：*AI Design in 2027: Predictions from the Lovart Research Team*
> 映射 VI 组合：**Purple**（背景液态玻璃色调 `#E6D5F5` Iris Light，高光 `#8B4BF7` Amethyst）

```
Create a 16:9 blog cover image (2400x1350px).

STYLE: Minimalist abstract illustration with hand-drawn flowing line art. Clean,
restrained, confident. No photos, no clip art, no cartoons, no text. Elements drawn
with BLACK (#000000) flowing hand-drawn lines — like brush or marker strokes, fluid
and lively, NOT mechanical straight lines. Core elements filled with WHITE (#FFFFFF)
for strong contrast. Soft optional glow at element intersections.

COMPOSITION: EXACTLY CENTERED single focal point. All elements must be symmetrically
composed at the bullseye center of the canvas — no off-center placement, no scattered
layout. 30-40% negative space reserved for text overlay (bottom-left region).

BACKGROUND (CRITICAL — APPLE LIQUID GLASS STYLE):
Apple Liquid Glass style background using #E6D5F5 (Iris Light) as glass base tint and
#8B4BF7 (Amethyst) for highlights and refraction. Translucent glass material with
refraction, reflection, dynamic light effects, layered depth, glossy specular highlights.
Realistic optical properties like frosted glass with purple tint. Multiple glass layers
stacked creating depth. Light flowing along glass curves with bright highlight points.
Absolutely NO solid color, NO geometric gradient, NO noise/grain, NO flat texture.

COLOR PALETTE: Insight & Trend category — mapped to Lovart VI "Purple" combination.
- Background: APPLE LIQUID GLASS, #E6D5F5 glass tint, #8B4BF7 highlights/refraction
- Element stroke: BLACK (#000000) flowing hand-drawn lines, 100% opacity
- Element fill: WHITE (#FFFFFF) solid fill for core elements
- Optional glow: #8B4BF7 at 10-12% opacity, subtle accent only

CENTRAL ELEMENTS (ALL EXACTLY CENTERED ON CANVAS, BLACK LINES + WHITE FILLS):
- An upward-pointing triangle, positioned at the EXACT CENTER of the canvas
  (bullseye center, symmetrically composed), ~40% of frame width, outlined with BLACK
  (#000000) flowing hand-drawn lines, filled with WHITE (#FFFFFF) solid
- Inside the triangle: a hand-drawn line art of an eye with a node network pattern
  radiating from the pupil (representing insight/foresight), drawn with BLACK (#000000)
  flowing hand-drawn lines, positioned at the center of the triangle, filled with
  WHITE (#FFFFFF) where appropriate
- A subtle upward-trending arrow line positioned symmetrically to the right of center,
  extending from the triangle's right vertex, in BLACK (#000000) hand-drawn lines
- Two small star-like dots positioned symmetrically above the triangle, in BLACK (#000000)
- Optional subtle glow behind central element, #8B4BF7 at 10% opacity
- CRITICAL: The entire element group must form a single centered focal point at the
  bullseye center of the canvas. No element may drift off-center.
- CRITICAL: All lines must be flowing hand-drawn style, NOT mechanical straight lines.

VISIBILITY REQUIREMENTS (CRITICAL):
- Element lines: BLACK (#000000) flowing hand-drawn strokes, clearly visible
- Element fills: WHITE (#FFFFFF) solid fill, strong contrast against glass background
- All elements must be exactly centered on the canvas
- Black lines + white fills ensure maximum visibility on any glass background

DO NOT INCLUDE: Any text, photos, cartoons, icons, more than 3 elements,
more than 2 colors (black + white only for elements), solid color backgrounds,
geometric gradients, noise, grain, flat textures, mechanical straight lines,
or elements in the bottom-left text zone.
```

**示例 3：Lovart 101 类文章**
> 文章：*AI Brand Identity 101: From Logo to Full Visual System*
> 映射 VI 组合：**Lime**（背景液态玻璃色调 `#E8F5A0` Lime Light，高光 `#D0FC16` Lightning）

```
Create a 16:9 blog cover image (2400x1350px).

STYLE: Minimalist abstract illustration with hand-drawn flowing line art. Clean,
restrained, confident. No photos, no clip art, no cartoons, no text. Elements drawn
with BLACK (#000000) flowing hand-drawn lines — like brush or marker strokes, fluid
and lively, NOT mechanical straight lines. Core elements filled with WHITE (#FFFFFF)
for strong contrast. Soft optional glow at element intersections.

COMPOSITION: EXACTLY CENTERED single focal point. All elements must be symmetrically
composed at the bullseye center of the canvas — no off-center placement, no scattered
layout. 30-40% negative space reserved for text overlay (bottom-left region).

BACKGROUND (CRITICAL — APPLE LIQUID GLASS STYLE):
Apple Liquid Glass style background using #E8F5A0 (Lime Light) as glass base tint and
#D0FC16 (Lightning) for highlights and refraction. Translucent glass material with
refraction, reflection, dynamic light effects, layered depth, glossy specular highlights.
Realistic optical properties like frosted glass with lime tint. Multiple glass layers
stacked creating depth. Light flowing along glass curves with bright highlight points.
Absolutely NO solid color, NO geometric gradient, NO noise/grain, NO flat texture.

COLOR PALETTE: Lovart 101 category — mapped to Lovart VI "Lime" combination.
- Background: APPLE LIQUID GLASS, #E8F5A0 glass tint, #D0FC16 highlights/refraction
- Element stroke: BLACK (#000000) flowing hand-drawn lines, 100% opacity
- Element fill: WHITE (#FFFFFF) solid fill for core elements
- Optional glow: #D0FC16 at 10-12% opacity, subtle accent only

CENTRAL ELEMENTS (ALL EXACTLY CENTERED ON CANVAS, BLACK LINES + WHITE FILLS):
- An incomplete circle (open arc, ~300°), positioned at the EXACT CENTER of the canvas
  (bullseye center, symmetrically composed), ~45% of frame width, outlined with BLACK
  (#000000) flowing hand-drawn lines, no fill (open arc)
- Inside the arc: a hand-drawn line art of an open book with a small sparkle above it
  (representing learning/brand knowledge), drawn with BLACK (#000000) flowing hand-drawn
  lines, positioned at the center of the arc, filled with WHITE (#FFFFFF) where appropriate
- Three small dots positioned symmetrically along the arc's gap, in BLACK (#000000)
- Optional subtle glow behind the book icon, #D0FC16 at 10% opacity
- CRITICAL: The entire element group must form a single centered focal point at the
  bullseye center of the canvas. No element may drift off-center.
- CRITICAL: All lines must be flowing hand-drawn style, NOT mechanical straight lines.

VISIBILITY REQUIREMENTS (CRITICAL):
- Element lines: BLACK (#000000) flowing hand-drawn strokes, clearly visible
- Element fills: WHITE (#FFFFFF) solid fill, strong contrast against glass background
- All elements must be exactly centered on the canvas
- Black lines + white fills ensure maximum visibility on any glass background

DO NOT INCLUDE: Any text, photos, cartoons, icons, more than 3 elements,
more than 2 colors (black + white only for elements), solid color backgrounds,
geometric gradients, noise, grain, flat textures, mechanical straight lines,
or elements in the bottom-left text zone.
```

---

## 六、执行计划

### 6.1 阶段划分

| 阶段 | 目标 | 范围 | 产出 |
|------|------|------|------|
| **Phase 0** | 样板验证 | 每个分类 3 篇 = 21 篇 | 21 张样板封面 + 21 条提示词 |
| **Phase 1** | 英文核心分类 | How-To + Best Practice + Better Design + Insight & Trend = ~2,388 篇 | 批量提示词 |
| **Phase 2** | 英文 Lovart 101 | ~6,394 篇（按子主题分批） | 批量提示词 |
| **Phase 3** | 英文剩余 | Topics + Branding + 无分类 = ~933 篇 | 批量提示词 |
| **Phase 4** | 多语言 | zh + ja = ~1,793 篇 | 复用/调整英文提示词 |

### 6.2 Phase 0 样板验证（建议立即执行）

从每个分类选取 3 篇代表性文章，制作样板封面，验证设计方向：

| 分类 | 样板文章 | 核心主题 | 元素组合 |
|------|---------|---------|---------|
| Lovart 101 | AI Brand Identity 101 | 品牌入门 | 未封闭圆 + 线条书本 |
| Lovart 101 | AI Video Creation 101 | 视频入门 | 未封闭圆 + 线条播放键 |
| Lovart 101 | ChatCanvas 101 Getting Started | 产品入门 | 未封闭圆 + 线条手指 |
| How-To | Facebook Ad Creatives with AI | 广告创意 | 圆角矩形 + 线条喇叭 |
| How-To | YouTube Thumbnails That Get Clicks | 缩略图 | 圆角矩形 + 线条眼睛 |
| How-To | Shopify Product Images with AI | 电商图片 | 圆角矩形 + 线条画笔 |
| Best Practice | Brand Kit Setup in 5 Minutes | 品牌套件 | 未封闭圆 + 线条齿轮 |
| Best Practice | Touch Edit 3 Gestures | 触摸编辑 | 未封闭圆 + 线条手指 |
| Best Practice | Nano Banana Consistent Results | 一致性 | 未封闭圆 + 线条灯泡 |
| Better Design | Design Psychology Visuals Convert | 设计心理学 | 六边形 + 线条眼睛 |
| Better Design | Visual Hierarchy Principle | 视觉层级 | 六边形 + 线条画笔 |
| Better Design | AI Copyright Creators Guide | 版权 | 六边形 + 线条盾牌 |
| Insight & Trend | AI Design 2027 Predictions | 趋势预测 | 三角形 + 线条眼睛 |
| Insight & Trend | AI Design Agent vs Image Generator | 范式转变 | 三角形 + 线条VS符号 |
| Insight & Trend | Death of Static Impression | 动态趋势 | 三角形 + 线条节点网络 |
| Topics | (根据实际精选文章选择) | — | 菱形 + 主题元素 |
| Branding | (根据实际文章选择) | — | 菱形 + 线条盾牌 |

### 6.3 批量提示词生成策略

对于 Phase 1-4 的批量制作，提示词生成流程：

1. **从 Sanity 拉取文章列表**：`title` + `category` + `seo.description`（或 `description`）
2. **自动分类映射**：根据 category → 配色方案 + 外框几何
3. **主题关键词提取**：从 title 和 description 中提取核心主题词
4. **元素映射**：主题词 → 核心线条元素（使用预定义映射表）
5. **组装提示词**：全局风格 + 分类配色 + 元素组合 + 负面约束
6. **人工审核**：抽检 10% 的提示词，确认元素选择合理

### 6.4 主题关键词 → 元素映射表

| 主题关键词 | 映射到核心线条元素 |
|-----------|------------------|
| logo, brand, identity | 线条盾牌 |
| video, motion, animation | 线条播放键 |
| image, photo, picture | 线条画笔 |
| social media, post, content | 线条手指（点击/分享） |
| ad, advertising, creative | 线条喇叭/扩音器 |
| website, landing, page | 线条矩形（页面） |
| email, newsletter | 线条信封 |
| packaging, product, box | 线条立方体 |
| print, card, flyer | 线条纸张 |
| font, typography, text | 线条字母 A |
| color, palette, gradient | 线条色环 |
| layout, grid, composition | 线条网格 |
| AI, agent, automation | 线条齿轮 + 线条手指 |
| comparison, vs, alternative | 线条 VS 符号 |
| trend, prediction, future | 线条眼睛 + 上升箭头 |
| insight, analysis, research | 线条眼睛 |
| tutorial, guide, how-to | 线条灯泡 |
| beginner, intro, 101, getting started | 线条书本 |
| restaurant, food, menu | 线条叉勺 |
| real estate, property | 线条房屋 |
| fitness, gym, health | 线条心跳线 |
| education, course, certificate | 线条毕业帽 |
| music, podcast, audio | 线条音符 |
| wedding, event | 线条钻石 |
| nonprofit, donation | 线条心形 |
| dental, clinic, medical | 线条十字 |
| beauty, skincare | 线条花瓣 |
| law, legal | 线条天平 |

---

## 七、质量验收标准

每张封面需通过以下检查：

| 检查项 | 标准 |
|--------|------|
| **比例** | 16:9 (2400×1350px 或 1200×675px) |
| **配色** | 在该分类映射的 Lovart VI 组合色系内，不超过 2 种色相 |
| **风格** | 极简抽象几何，非写实、非卡通、非图标堆砌 |
| **背景质感**（v1.5 重写） | 背景必须是**苹果 Liquid Glass 液态玻璃**：半透明材质、折射反射、动态光效、层次感、光泽感。**禁止**纯色、几何渐变、噪点、颗粒、扁平无质感 |
| **负空间** | ≥ 30%，底部/左侧留足文字叠加区 |
| **元素数量** | 2-3 个，不多不少 |
| **元素线条**（v1.5 重写） | **黑色（#000000）流动手绘线条**，像毛笔/马克笔笔触，灵动不死板，**禁止机械直线** |
| **元素填充**（v1.5 新增） | **白色（#FFFFFF）实心填充**核心要素，与黑色线条形成鲜明对比 |
| **元素居中** | 所有元素组合必须**精确居中于画布中心**，左右对称、上下对称，禁止偏移 |
| **对比度** | 黑线白填在任何色调背景上都有极高对比度，确保清晰可辨 |
| **光晕** | 可选 1 处微光晕，Theme 色 10-15% 透明度，不喧宾夺主 |
| **文字** | 封面上无任何文字 |
| **系列感** | 与同分类其他封面构成一致视觉系列 |

---

## 八、技术实施备注

### 8.1 Sanity 数据查询

- **项目 ID**：`o11tm2qe`
- **Dataset**：`production`
- **API 端点**：`https://o11tm2qe.api.sanity.io/v2026-01-01/data/query/production`
- **Studio URL**：`https://o11tm2qe.sanity.studio`

拉取文章列表的 GROQ 查询：
```groq
*[_type == "blog" && language == "en" && defined(category->value.current) && !defined(cover)]{
  _id, "slug": slug.current, title, description,
  "category": category->value.current,
  "seoTitle": seo.title, "seoDesc": seo.description
} | order(category->value.current asc) [0...100]
```

### 8.2 封面上传

封面制作完成后，需通过 Sanity API 或 Studio 上传至 `cover` 字段（imageSource 类型），同时更新 `seo.ogImage`（推荐 1200×630）。

### 8.3 现有封面处理

- **有 liblib 占位图的**：全部替换为新封面
- **有 blogcover 池图片的**：全部替换为新封面
- **无封面的 785 篇**：优先补全

---

## 九、下一步行动

1. **确认本计划**：审核配色方案、元素库、提示词模板
2. **执行 Phase 0**：为 7 个分类各制作 3 张样板（共 21 张）
3. **审核样板**：验证风格方向是否符合预期
4. **调整规范**：根据样板反馈微调配色/元素
5. **批量生成提示词**：按 Phase 1-4 顺序执行
6. **Lovart 制作**：将提示词批量交给 Lovart 执行
7. **质量验收**：按第七章标准逐批验收
8. **上传替换**：通过 Sanity API 批量更新封面
