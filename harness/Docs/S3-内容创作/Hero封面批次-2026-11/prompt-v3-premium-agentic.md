# Prompt v3 · 高级感与 Agent 定位升级

> 基于 v2 全量 387 条的实测诊断。v2 解决的是「不丑、不雷同」；v3 解决「不平庸、有身份」。
> 诊断数据见文末。

---

## 一、v2 的三个致命短板

### 短板 1：模板疲劳 —— 四句话覆盖所有图

| 短语 | 出现率 |
|---|---:|
| `seamless` | 83% |
| `one flat (tone/backdrop)` | 77% |
| `bottom 25% clean for label scrim` | 77% |
| `hero fills about 70% of frame` | 77% |

**后果**：生成模型对这类高频模板词会自动"平均化"，产出安全但无记忆点的图。

### 短板 2：编辑级语汇完全缺失

实测 `atelier` / `museum` / `still life` / `chiaroscuro` / `medium format` / `golden hour` / `artisan` / `bespoke` / `archive` / `bauhaus` **出现次数均为 0**。

这些词才是"高级感"的真实载体——它们指向具体的**工艺传统**与**观看方式**，而不只是形容词。

### 短板 3：Agent 定位零体现

`agent` / `autonomous` / `orchestrate` / `delegate` / `intent` **全部 0 次**。

我们的核心差异是「全球首个 AI 设计 agent」——但 387 张图里没有一张在讲这件事。画面全是"单个物件静静放着"，这恰恰是**非 agent** 的视觉语言（单一产出、静止、无人）。

---

## 二、v3 框架：三层锚定 + 四层变量

风格一致性不能靠"所有图都写同一句话"，那样会变成同质化。正确做法是：**锚定在不可见的层面，放开可见的层面。**

### 三层锚定（全站永不变，保证一致性）

| # | 锚点 | 定义 | 为什么 |
|---|---|---|---|
| A1 | **材质真实** | 所有材质必须"可触摸"，有毛孔、纤维、磨损、厚度；禁止 CGI 塑料感 | 高级感的物理基础 |
| A2 | **单一焦点** | 每画面只有一个视觉重心，其余元素降到 20% 权重以下 | 编辑级摄影的构图纪律 |
| A3 | **克制配色** | 低饱和打底 + **至多一个**高饱和点睛；点睛面积不超过画面 8% | 奢侈品/编辑类视觉的通则 |

> 这三条不进 prompt 的自由发挥区，而是写死在模板尾部，任何条目都不得违反。

### 四层变量（同组内放开，制造个性）

| # | 变量 | 取值范围 |
|---|---|---|
| V1 | **机位 / 景别** | 正视 / 3-4 侧角 / 微距贴面 / 正俯 / 低角度仰 / 侧剖面 / 越过前景 / 偏心大留白 |
| V2 | **叙事瞬间** | 静止陈列 / 正在成形 / 半完成 / 刚交付 / 被使用中 / 归档封存 |
| V3 | **材质主体** | 见「材质词库」，不再只用 matte ceramic |
| V4 | **场景语境** | 见「编辑级场景库」，从"无缝背景"升级为"有环境记忆的空间" |

---

## 三、v3 新增词库

### 3.1 材质词库（替换单一 `matte ceramic`）

| 材质 | 英文 | 指向 |
|---|---|---|
| 冷压水彩纸 | cold-pressed watercolor paper | 手作、纤维可见 |
| 未漂白亚麻 | raw unbleached linen | 自然、厚度 |
| 磨砂阳极氧化铝 | bead-blasted anodized aluminum | 精密、科技 |
| 哑光陶土 | unglazed terracotta | 质朴、温度 |
| 大理石灰泥 | marble plaster | 建筑感、微颗粒 |
| 绒面皮革 | nubuck leather | 触感、昂贵 |
| 拉丝青铜 | brushed bronze | 时间感、重量 |
| 半透明硫酸纸 | translucent vellum | 叠层、透光 |
| 丝网印油墨 | silkscreen ink with visible halftone | 印刷工艺 |
| 实木橡木皮 | solid oak veneer with visible grain | 工艺、耐用 |

### 3.2 布光词库（替换单一 `soft key light`）

| 布光 | 英文 | 效果 |
|---|---|---|
| 北窗散射 | north-facing window light, soft and directional | 编辑摄影标准光 |
| 单源明暗对照 | single-source chiaroscuro with deep falloff | 戏剧性、绘画感 |
| 柔光箱侧逆 | softbox rim light defining the silhouette | 高级产品摄影 |
| 掠射侧光 | raking sidelight revealing surface texture | 材质特写必备 |
| 黄金时刻逆光 | golden-hour backlight with lens bloom | 温度、叙事 |
| 博物馆展柜光 | museum vitrine light, tight and clinical | 珍藏感 |
| 阴天自然光 | overcast daylight, even and shadowless | 极简、冷静 |
| 局部灯光池 | a single practical lamp pooling on the subject | 工作现场感 |

### 3.3 编辑级场景库（替换 `seamless backdrop`）

| 场景 | 英文 | 语境 |
|---|---|---|
| 设计师工作室 | a designer's atelier with tools pushed to the edges | 创作现场 |
| 印刷工坊 | a print workshop with ink-stained felt | 工艺现场 |
| 档案抽屉 | an archive drawer of filed material samples | 积累、体系 |
| 博物馆展柜 | a museum vitrine with a glass edge catching light | 珍藏、权威 |
| 材料图书馆 | a material library of labelled swatch boards | 专业、体系 |
| 画廊展墙 | a gallery wall with a single hung piece | 审美认证 |
| 校样间 | a proofing room with colour charts pinned up | 精确、专业 |

> ⚠ 使用场景时要同时保留「四边 ≥5% 裁切余量」和「单一焦点」，否则会变杂乱。

### 3.4 Agent 定位的物理隐喻库（关键新增）

**不能画 UI**（会乱码），必须用**物理隐喻**表达 agent 性。五种可选：

| # | 隐喻 | 画面 | 传达 |
|---|---|---|---|
| M1 | **并行产出** | 一张 brief 卡片旁立着 3–4 个**不同媒介**的成品（纸、布、陶、金属），暗示一次指令、跨媒介交付 | Agent 的统筹力 |
| M2 | **转化序列** | 同一物件在画面中呈现「原始 → 半成 → 完成」三种状态，沿一条线排布 | 从意图到交付 |
| M3 | **无人值守** | 物件处于「自行完成中」：一张纸正被折起、一滴墨正在落定、一个封套正在合拢 | 自主性 |
| M4 | **跨媒介并置** | 同一视觉语言同时出现在纸面、织面、陶面、金属面上 | 多模型协同 |
| M5 | **迭代层叠** | 同一主体的「早期草稿」与「最终版」叠放在一起，间距精确 | 思考与迭代 |

> **推荐配比**：每 10 张里至少 3 张用 M 系列隐喻。否则整批图会退回"静物陈列"。

---

## 四、v3 Prompt 结构模板

```text
[lane token]
[材质：从 3.1 选 1]
[布光：从 3.2 选 1]
[场景：从 3.3 选 1，或 "a seamless tonal field" 保留极简]
[主体 + 叙事瞬间：静止 / 成形中 / 半完成 / 刚交付 / 使用中 / 封存]
[agent 隐喻：M1–M5 择一，或省略]
[机位 / 景别]
[三层锚定声明：tactile material truth, one focal point only, muted base with at most one accent]
[安全区 + no-text 约束]
```

### 三层锚定声明（固定尾句，替换 v2 的松散约束）

```text
material truth with visible surface texture, one focal point only, muted base palette with at most one accent, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

---

## 五、高级感的具体判据（可验收）

| 判据 | 不合格表现 | 合格表现 |
|---|---|---|
| 材质可触摸 | 光滑塑料感、均匀无瑕 | 可见纤维 / 毛孔 / 磨损 / 厚度 |
| 光有方向 | 平光、环形光、无影 | 能看出光源方向与衰减 |
| 配色克制 | 三色以上等权、高饱和撞色 | 低饱和底 + 单点睛，点睛占比 <8% |
| 单一焦点 | 三四个元素都在抢 | 一眼只有一个重心 |
| 有环境记忆 | 纯无缝背景 + 无上下文 | 有场景线索（工具一角、台面材质、墙面） |
| 有 agent 痕迹 | 只放一个物件静静陈列 | 多媒介并行 / 成形中 / 迭代层叠 |

---

## 六、诊断数据（v2 实测 387 条）

### 模板疲劳

```
322/387 (83%)  seamless
300/387 (77%)  one flat
300/387 (77%)  bottom 25%
300/387 (77%)  70% of frame
227/387 (58%)  swiss grid
226/387 (58%)  riso-print ink edges
227/387 (58%)  flat even lighting
```

### 情绪词分布（共 929 次）

```
406  warm      ← 独占 44%
270  editorial
 75  precise
 36  restrained / calm
 34  bold
 18  ornate / quiet / structured / expressive
```

### 高级感信号

```
atelier · museum · still life · chiaroscuro · medium format
golden hour · artisan · bespoke · archive · bauhaus
→ 全部 0 次
```

### Agent 信号

```
agent · autonomous · thinking · reasoning · orchestrate · delegate · intent
→ 全部 0 次
```

### 主体类型

```
387  abstract shape      ← 全部
336  print / paper       ← 87%
181  device / screen
 57  product
 23  human               ← 仅 6%
```

---

## 七、v2 → v3 差异示例（同一 brief：S-PLA platform）

**v2**
```text
Soft-body 3D render, matte ceramic materials: a single index card with a folded corner
slides into a rounded slot on a minimalist matte console, three small finished artworks
— a photo print, a tiny canvas, a glossy cube — resting on a shallow tray beside the slot,
warm-grey palette with one coral accent, macro 50mm look, soft key light from upper left
with gentle contact shadows, seamless warm-grey paper backdrop, hero scene fills about
65% of frame, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark,
no screens
```

**v3**
```text
Soft-body 3D render in bead-blasted anodized aluminum and unglazed terracotta,
single-source chiaroscuro with deep falloff from the upper left,
the scene set on a designer's atelier bench with tools pushed to the edges of frame,
one folded-corner brief card entering a machined slot while three finished pieces stand
beside it in different media — a cotton-paper print, a linen swatch panel, a bronze-edged
plaque — one brief, three deliverables (M1 parallel output),
rendered at an equivalent 50mm perspective, material truth with visible surface texture,
one focal point only, muted warm-grey base with at most one coral accent,
4:3, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens,
no UI windows
```

**差异**：材质从单一陶瓷 → 铝+陶土双材质；布光从泛泛"soft key light" → 明确的明暗对照；背景从"seamless 色场" → 有环境记忆的工作台；新增 M1 并行产出隐喻。同时保留了原有的一致性锚点（暖灰底、单点睛色、单焦点）。
