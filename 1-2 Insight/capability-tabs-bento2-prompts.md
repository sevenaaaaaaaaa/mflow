# Capability-Tabs & Bento-2 图片 Prompt
## capability-tabs: 横版 16:9 (1200×675) | bento-2: 方形 1:1 (1200×1200)
## 目标: capability-tabs 丰富到 150+ 图 | bento-2 扩到 100+ 图

---

# PART 1: Capability-Tabs（4 个 Tab 的内容展示图）

## capability-tabs 结构
- 4 个 tab：Generate / Edit / Brand / Ship
- 每个 tab 需要一张横版大图 (16:9) 展示该能力的使用场景
- 现有 91 张但内容高度重复，需要按品类定制

---

## 通用版（适用于大部分 tool 页面）

### Tab 1: Generate — 从想法到设计
> A Lovart ChatCanvas interface taking up the left 60% of the frame, showing a natural language prompt being typed: "Create a modern tech conference poster with neon blue and purple gradients, featuring a circuit board pattern background, bold sans-serif headline, and space for speaker photos." The right 40% shows the generated result — a stunning, print-ready poster design matching every detail of the prompt. The prompt keywords are subtly highlighted. Clean dark-mode UI on a desk with soft ambient light. 16:9 cinematic ratio.

### Tab 2: Edit — 点哪改哪
> A close-up product shot of a magazine spread open on screen. A hand's finger is touching a specific text element (a headline), which glows with a neon purple outline. A floating context menu near the touch point shows: "Rewrite", "Change font", "Resize", "Change color to brand blue". The preview shows the change happening in real-time. Part UI screenshot, part hand interaction. 16:9.

### Tab 3: Brand — 一次设定，全局一致
> A Lovart Brand Kit dashboard taking the full frame. Left panel: Brand assets organized — logo, color palette (5 swatches), font list. Center: A live preview of how those brand elements auto-apply to various templates — social post, business card, presentation slide, email banner. Every template uses the exact same brand colors and fonts without manual adjustment. Clean SaaS dashboard. 16:9.

### Tab 4: Ship — 一键多格式输出
> A radial design: Center is a single social media post design. Radiating outward with connector lines are 8 different export formats: Instagram Post (1:1), Instagram Story (9:16), Facebook Ad (1.91:1), LinkedIn (1.91:1), Twitter (16:9), Email Header (600px), Print PDF (A4), Website Hero (16:9). Each shows the design perfectly auto-adapted with a download icon. Infographic-meets-UI aesthetic. 16:9.

---

## 品类变体（替换通用版中的设计内容）

### 图像生成品类变体
**Generate**: Prompt → 产品摄影图  **Edit**: 去背景/换场景  **Brand**: 电商品牌视觉  **Ship**: PDP/广告/社交图
> Variations: Replace the generic poster with product photography context. Generate tab shows a product brief → multiple product shots. Edit tab shows background removal and scene replacement. Brand tab shows e-commerce brand system. Ship tab shows PDP images, Amazon A+ content, social ads.

### 视频品类变体
**Generate**: Script → Video  **Edit**: 剪辑/特效  **Brand**: 视频品牌模板  **Ship**: 多平台视频
> Generate tab shows a text script → storyboard → final video. Edit tab shows video timeline with AI editing tools. Brand tab shows video intro/outro templates with brand consistency. Ship tab shows TikTok/Reels/YouTube optimized exports.

### Logo/Brand 品类变体
**Generate**: 品牌名 → 多方案  **Edit**: 微调 logo元素  **Brand**: Brand Kit 系统  **Ship**: 全触点导出
> Generate tab shows brand name input → 12 logo concepts. Edit tab shows individual logo element adjustments (icon size, font weight, spacing). Brand tab shows the complete brand system generated. Ship tab shows logo in SVG/PNG + brand guide PDF + social kit.

### 3D/Mockup 品类变体
**Generate**: 2D草图 → 3D模型  **Edit**: 材质/灯光调整  **Brand**: 产品视觉标准  **Ship**: AR/USDZ/渲染图
> Generate tab shows sketch-to-3D transformation. Edit tab shows material and lighting adjustments on a 3D model. Brand tab shows consistent product visualization standards. Ship tab shows AR preview on phone + turntable video + still renders.

### Upscaler/Restorer 品类变体
**Generate**: 低清图 → 8K  **Edit**: 细节修复  **Brand**: 批量风格统一  **Ship**: Web/Print输出
> Generate tab shows before-after resolution comparison. Edit tab shows scratch removal and color restoration. Brand tab shows batch processing with consistent output. Ship tab shows print-ready TIFF + web-optimized versions.

### Avatar/Portrait 品类变体
**Generate**: 自拍 → 专业头像  **Edit**: 表情/服装调整  **Brand**: 团队统一风格  **Ship**: 多平台部署
> Generate tab shows selfie-to-headshot transformation. Edit tab shows expression slider and outfit change. Brand tab shows team page with unified headshot style. Ship tab shows LinkedIn/Zoom/Slack/email integration.

---

# PART 2: Bento-2（2 卡模式对比）

## bento-2 结构
- 两张等宽大卡，每卡 title + description + 大图
- 通常展示两种工作模式对比或两个核心价值

---

## 通用版：Agent Mode vs Guided Mode

### Card 1: Autonomous Agent（自主代理模式）
> A split-view of a ChatCanvas: Top half shows one brief text input — "Launch a full brand for a sustainable coffee startup called Terra Brew. Modern organic aesthetic, earthy greens, premium feel." Bottom half shows the AI agent autonomously working — a visual sequence of it generating the logo, selecting color palette, creating social templates, designing packaging mockup — all automatically, no human intervention shown. The screen shows completed assets appearing one by one with checkmarks. Sleek dark UI, glowing progress indicators. 1:1 square.

### Card 2: Guided Collaboration（引导式协作）
> A collaborative workspace view: A ChatCanvas showing a dialogue between user and AI — user says "Make the logo more playful," AI responds with 3 revised options. The cursor hovers over option 2. The right side shows a Canvas with the selected logo being refined, with the user manually adjusting element positions. Two visible personas: AI suggestions + human decisions. Warm, collaborative vibe. 1:1 square.

---

## 品类变体

### 图像品类: Speed vs Quality
**Card 1 — Instant Generation**: Stopwatch showing "3 seconds" next to a gallery of 10+ generated images from one prompt, cascading waterfall layout.
**Card 2 — Precision Control**: Zoomed-in view of Touch Edit on a specific image detail, with adjustment sliders (brightness, saturation, structure).

### 视频品类: Script-Driven vs Visual-First
**Card 1 — Script to Video**: A script document on the left transforming into storyboard frames → final video on the right. Text-to-video pipeline.
**Card 2 — Visual Timeline**: A video editing timeline with drag-and-drop clips, AI-suggested transitions highlighted, preview playing.

### Logo品类: Speed vs Customization
**Card 1 — Instant Concepts**: 12 logo thumbnails generated from one brand name, arranged in a grid with timestamps "Generated in 15 seconds".
**Card 2 — Fine-Tune Everything**: Close-up of a logo editor with individual controls for icon size, letter spacing, color, weight.

### 3D品类: Auto-Generate vs Manual Control
**Card 1 — One-Click 3D**: A flat product sketch on the left → fully textured 3D model on the right with an "Auto-Generate" button. Clean, magical transformation.
**Card 2 — Material Studio**: 3D viewport showing the same model with material nodes, lighting rig, and camera controls visible. Professional 3D workflow.

### Upscaler品类: Batch Speed vs Single Precision
**Card 1 — Batch Power**: Dashboard showing "47 images upscaled in 2 minutes" with a gallery of before/after thumbnails scrolling.
**Card 2 — Pixel-Perfect**: Extreme close-up showing a single image being upscaled with a slider that reveals the detail difference between original and enhanced.

### Avatar品类: Volume vs Personality
**Card 1 — Headshot Factory**: Grid of 20 AI headshots from one selfie, different outfits and backgrounds, labeled "1 photo → 20 professional looks".
**Card 2 — Expression Studio**: A single avatar with a slider controlling expression, showing the same face transitioning from serious → smiling → laughing.

---

## 统一质量要求
- Capability-tabs: UI 元素必须看起来真实可用，不能是概念图
- Bento-2: 两张卡有明显对比关系，story telling 通过图片就能传达
- 所有图: 避免纯白背景（死白），用微妙的暖灰/米白
- 光源方向一致（假设左上 45° 主光源）

## 使用策略
- Capability-tabs: 4 tabs × 6 品类变体 + 1 通用版 = 28 张新图 → pool: 91 + 28 = 119 张
- Bento-2: 2 cards × 6 品类变体 + 1 通用版 = 14 张新图 → pool: 51 + 14 = 65 张
