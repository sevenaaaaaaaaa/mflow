# Blog 插图 · 风格航道体系 v2（2026-11）

> SSOT：本文件是 Blog 正文插图的风格与 prompt 规范唯一来源。
> 继承 `Hero封面批次-2026-11/prompt-v2-style-system.md` 的六航道制与负面词体系，针对**文章正文阅读场景**重新调参。
> **v2 升级（同日）**：新增构图原型系统（§9，个性化引擎）、工艺词汇与光签名（§10，高级感引擎）、定位语言（全球首个 AI design agent）、主题兜底扩充（§11）。§2 航道 token 已含工艺词汇版。
> 硬约束（用户钦定）：**按文章内容生成 · 不用过得过时的风格 · 不做嘈杂的布局 · 设计公司调性必须立得住。**

---

## 1. 调性总纲（三条红线 + 一条基调）

| 红线 | 禁止 | 替代做法 |
|---|---|---|
| ❌ 过时风格 | 紫蓝渐变、玻璃拟态、等距 SaaS 插画、霓虹赛博、发光连线、漂浮 3D 球、股票图库脸 | 材质真实感 + 编辑部式布光 + 单点睛色 |
| ❌ 嘈杂布局 | 元素 >3、多对象拼贴、满铺构图、花哨边框、装饰堆叠 | 单主体 + ≤2 支撑元素 + 大留白（主体占 55–65%） |
| ❌ 假 UI | AI 画任何界面/屏幕/窗口/仪表盘 | UI 一律走实测截图管线；AI 只做物理隐喻 |
| ✔ 基调 | 设计公司自证 | 每张图本身就是「我们懂设计」的证据：精确的光、克制的色、可信的材质 |

**统一调色板（全语料冻结）**：`warm ivory + soft greige 底、deep charcoal 墨、one muted coral 点睛`
——11 个语言版本、2,000+ 篇文章共享同一调性；视频/影视主题例外（L2 航道自带 teal-and-amber）。

## 2. 航道（继承 Hero v2，token 冻结不改）

| 航道 | Token（冻结） | 专属负面 |
|---|---|---|
| L1 商业摄影 | `High-end commercial photography, 85-100mm lens, single-source soft key light with one long controlled shadow, true-to-life materials, museum-grade editorial color, seamless paper backdrop` | snapshot look, flat cellphone lighting, stock-photo pose |
| L2 电影剧照 | `Cinematic still, shot on 35mm film, volumetric light, layered depth of field, teal-and-amber cinematic palette, subtle film grain, anamorphic feel` | HDR over-processing, theme-park color, video-game render |
| L3 柔体三维 | `Soft-body 3D render, hand-glazed matte ceramic and clay with visible throwing rings and an eggshell finish, single-source studio light, gentle contact shadows` | glassmorphism, chrome reflections, neon glow, floating holograms |
| L4 图形平面 | `Editorial flat-graphic composition on a Swiss grid, heavyweight cotton paper, precise alignment, riso-print misregistration and ink bleed as texture accents` | gradient mesh, skeuomorphism, drop-shadow stacking, clip-art emoji style |
| L5 材质静物 | `Macro still-life on a seamless backdrop, tactile craft materials — handmade cotton-rag paper with deckled edges, blind emboss, matte ceramic, copper foil — raking side light revealing texture, precise cast shadows` | plastic sheen, busy tabletop, cluttered props |
| L6 纸艺场景 | `Layered paper-craft diorama, heavyweight archival cardstock hand-cut with torn-edge reveals, soft real shadows, warm directional daylight, disciplined composition` | plastic toys, mixed-media mess, glitter |

## 3. 槽位 → 航道映射（固定，不逐张改航道）

| 槽位 imageType | 航道 | 内容语义 | 出自规范 |
|---|---|---|---|
| Persona | L1 | 文章目标读者的真实工作场景（背影/过肩，不露脸） | Narrative 经典 4 图 |
| Diagram | L4 | 概念流程图：空白几何 token + 手绘墨线，节点内零字符 | 同上 |
| RealUI | **截图任务** | 真实产品界面（走 eeat 实测截图管线，**AI 不画**） | 同上 slot 3 |
| CTA | L3 | 品牌收尾：哑光陶瓷 token + 珊瑚芯 | 各类型公共收尾 |
| Output | L5 | 成品实体化（按主题映射实体形态，见 §5） | Tutorial slot 1 |
| StepCompare | L1 | 双联画：左粗糙态 / 右完成态，同机位同光 | Tutorial slot 2 |
| WorkflowCompare | L4 | 双轨对比：上轨碎片化 / 下轨连续三节点 | Comparison slot 2 |
| Principle | L4 | 单一形态表达设计原则 | Better Design slot 1 |
| PillarHero | L1 | Pillar 主视觉：实体化主题 + 展台 | Pillar slot 1 |
| PillarThumb | L5 | 分类缩略：主题的简化材质 token | Pillar slots 2–4 |

## 4. 复杂度预算（防嘈杂的硬数字）

```
主视觉 ×1 ＋ 支撑元素 ≤2 ＋ 背景处理 ×1
主体占画幅 55–65%；四边留白 ≥8%；背景 = 单一无缝色场
双联/双轨构图 = 恰好 2 个半场，中间留一条干净间隙
```

## 5. 主题 → 实体形态映射（Output / PillarHero 槽位用）

| 文章主题（slug 命中） | 实体形态 |
|---|---|
| thumbnail / video | 画架上的一帧装框视频静帧 |
| logo / brand kit / identity | 厚棉纸压印的抽象标志 |
| menu / restaurant | 铜架立起的空白菜单卡 |
| poster / print / flyer | 靠墙立柱上的大装框海报 |
| packaging / box / label | 展台上一个无品牌的哑光盒 |
| banner / cover / social | 带 裁切标记的竖版照片打印稿 + 空白方卡 |
| ppt / deck / slide | 两块空白横板叠放 + 细书脊 |
| resume / cv / portfolio | 纸托上一张硬挺文档纸，光掀起一角 |
| infographic / data / chart | 分层剪纸做出的抽象条形板 |
| mockup / website / landing | 小哑光架上立起的打印页样机 |
| interior / room | 台座上的小型建筑纸模 |
| fashion / apparel | 裁剪人台底座上的一对面料样 |
| product photo / ecommerce | 沙色展台上的哑光陶瓷瓶 |
| （未命中） | 小画架上的一幅装框艺术微喷 |

## 6. 全局负面词（v1，替代旧 negative）

```
text, letters, words, numbers, watermark, signature, logo text, gibberish UI labels,
distorted faces, visible faces, extra fingers, low resolution, jpeg artifacts, frame border,
oversaturated colors, generic purple-blue gradient, glassmorphism cliche, floating 3D blobs,
isometric startup illustration, fake UI screens, gibberish interface text, glowing connection lines,
floating chips, collage of many elements, cluttered composition, busy layout,
dated stock-photo look, neon cyberpunk, trend-chasing gradient mashup, drop-shadow stacking
```

## 7. Step 0 · 风格定调（W0，18 张）

每航道出 3 候选 → 每航道选定 1 张冻结为**风格参考图**，此后该航道所有生成携带参考图。
候选之间只微调「moment + camera」，航道 token 一字不改。

### L1 · 商业摄影 ×3（16:9 · 1600×900）
- **L1-C1**：`High-end commercial photography, 85-100mm lens, soft key light with directional shadow, tangible materials, seamless paper backdrop: a designer seen from behind at a clean oak desk, one large ivory moodboard sheet and one corner of a coral fabric swatch as the only props, front-on eye-level view, warm ivory and soft greige base, deep charcoal ink, one muted coral accent, hero scene fills about 60% of frame, 16:9, generous negative space, uncluttered composition, restrained editorial styling, no text, no letters, no numbers, no watermark, no UI screens`
- **L1-C2**：同 token，moment 改为 `an overhead flat lay of a designer desk: one open sketchbook with blank thumbnail grids, one pencil, one coral sticky note`
- **L1-C3**：同 token，moment 改为 `two designers seen from behind reviewing one large printed poster pinned on a studio wall, low angle`

### L2 · 电影剧照 ×3
- **L2-C1**：`Cinematic still, shot on 35mm film, volumetric light, layered depth of field, teal-and-amber cinematic palette, subtle film grain: a physical film strip curves across a dark editing desk with three golden-hour frames, one frame lifted slightly off, front-on view`
- **L2-C2**：同 token，moment 改为 `a dark studio with one practical light revealing a camera on a tripod and a matte storyboard board`
- **L2-C3**：同 token，moment 改为 `over-the-shoulder view of an editor at dusk, monitor glow replaced by a soft practical lamp on a blank paper storyboard`

### L3 · 柔体三维 ×3
- **L3-C1**：`Soft-body 3D render, matte ceramic and clay materials, studio HDRI lighting, gentle contact shadows: one rounded ceramic token with a subtle coral core resting on a shallow matte tray, warm-grey palette, front-on view`
- **L3-C2**：同 token，moment 改为 `three matte ceramic pebbles ascending like steps with the topmost accented in coral`
- **L3-C3**：同 token，moment 改为 `a matte ceramic card mid-slot into a rounded console groove, one coral bead following`

### L4 · 图形平面 ×3
- **L4-C1**：`Editorial flat-graphic composition on a Swiss grid, textured cotton paper, precise alignment, riso-print texture accents: three blank geometric tokens connected by thin hand-inked lines, one token accented in coral, warm ivory field, wide margins`
- **L4-C2**：同 token，moment 改为 `one large circle counter-balanced by one small square off-axis, single coral accent`
- **L4-C3**：同 token，moment 改为 `two parallel tracks — upper fragmented small tiles, lower one clean continuous line with three nodes, coral accent on the lower`

### L5 · 材质静物 ×3
- **L5-C1**：`Macro still-life on a seamless backdrop, tactile materials — cotton paper, matte ceramic, foil — raking side light revealing texture, precise cast shadows: an embossed abstract mark pressed into a thick cotton-paper card, ivory and charcoal palette with one copper-foil accent`
- **L5-C2**：同 token，moment 改为 `a tall blank menu card standing on a small brass stand, side light`
- **L5-C3**：同 token，moment 改为 `layered cut-paper bar shapes rising on a matte board, coral for the tallest bar`

### L6 · 纸艺场景 ×3
- **L6-C1**：`Layered paper-craft diorama, hand-cut paper layers with soft real shadows, warm daylight, disciplined composition: a minimal paper scene of one large idea-shape rising from layered ivory paper planes, single coral accent`
- **L6-C2**：同 token，moment 改为 `a paper diorama of a tiny studio room with one blank canvas and one lamp`
- **L6-C3**：同 token，moment 改为 `cut-paper arrows ascending three terraced paper levels`

> **冻结后动作**：每航道选定参考图后，把 URL 回填到本文件 §2，生成器输出的 brief 附带该参考图引用。

## 8. 执行纪律（每批通用）

1. **同航道连跑**：一个 chunk 内所有 brief 同航道，不跨航道穿插。
2. **锁 seed**：同一篇文章的所有槽位共用同一 seed（脚本按 slug 生成，确定性可复跑）。
3. **机位互异**：同一篇文章内各槽位机位自动轮换（正视/侧角/微距/俯拍/低角度/侧影）。
4. **原型互异**：同一篇文章内各对象槽位构图原型自动轮换、不重复（brief 带 `archetype` 字段，照抄即可）。
5. **按内容生成**：每条 brief 的 subject 都来自该文章的 slug 主题 + H2 论点锚点 + 实体形态映射——禁止无主题的通用配图。
6. **重 roll 纪律**：不合格只改 [moment]/[camera]，禁止改航道 token 与调色板。
7. **验收**：比例正确 / 四边安全 / 层级达标（材质+光比+点睛色）/ 航道 match / 无禁用元素 / 无文字。

---

## 9. v2 升级 · 构图原型系统（个性化引擎）

> 设计哲学：**一致性来自系统（调色板/光签名/材质/比例——全语料冻结），个性来自构图与叙事（原型/论点/机位——按文章轮换）**。
> 一致性 ≠ 千篇一律；高级感 = 有意的克制 + 精确的工艺语汇 + 每张图都被「单独艺术指导过」的感觉。

8 种摆拍原型（对象槽位：Output / PillarHero / PillarThumb），按文章哈希确定性轮换、篇内不重复：

| 原型 | 构图语法（冻结短语） |
|---|---|
| A1-monolith | 独石：hero 居中独立，纪念碑式平静，四周对称留白 |
| A2-cantilever | 偏置：hero 锚定左三分之一，右侧大片空场呼吸 |
| A3-arrangement | 顶拍排列：两件物体精确的对角静置，其余空场 |
| A4-suspended | 悬停：hero 悬浮于表面上方一点，下方唯一软影做配重 |
| A5-plinth | 展台：低哑光台座、微仰角，安静的美术馆存在感 |
| A6-dialogue | 对话：两件物体隔着一段刻意留白相望，空场讲故事 |
| A7-frame-in-frame | 画中画：作品嵌套第二层框——无酸卡纸装裱 + 细铜压条 |
| A8-lightfall | 光落点：hero 恰好落在单一光带里，四周处于柔和阴影 |

固定语法槽位（有自身构图语言，不参与轮换）：Diagram（3/4 空白 token 流程）、StepCompare（双联）、WorkflowCompare（双轨）、CTA（品牌收尾，3 时刻轮换）、Persona（3 全球中立场景轮换）、Principle（3 图形排列轮换）。

**轮换分布（QC 实测）**：Output 八原型 77–106 张/原型；PillarHero 四原型 178–240；PillarThumb 四原型 610–672；CTA 三时刻 630/706/699；Persona 三场景 15/15/18；篇内原型/机位重复 = 0。

## 10. v2 升级 · 工艺词汇与光签名（高级感引擎）

**工艺词汇（已写入航道 token）**：handmade cotton-rag paper / deckled edges（毛边纸）/ blind emboss（素压印）/ copper foil（铜箔）/ throwing rings（拉坯纹）/ eggshell finish（蛋壳光）/ riso misregistration and ink bleed（孔版错位与洇墨）/ archival mat board + brass lip（无酸装裱 + 铜压条）/ torn-edge reveals（撕边露层）。

**光签名**：全语料统一「single-source 单一光源 + 受控投影/接触影」——读者在信息流里刷到任何一张，都能认出是同一家的图。

**点睛纪律**：`one muted coral accent kept to a small part of the frame`——点睛色 ≤10% 画幅，克制即高级。

**定位语言（全球首个 AI design agent）**：
1. 每张图必须**能独立成为品牌资产**（单独发社媒不丢人）；
2. 拒绝追赶潮流的视觉噱头（negative list 已封杀 trend-chasing gradient mashup）——「第一个」的自信来自稳定，不来自追新；
3. 全球受众中立场景（Persona 三场景：窗边工作台 / 材质图书馆 / 画廊墙），无地域办公刻板印象；
4. 材质诚实：只画可信的真实材质，不画不属于任何工艺的「AI 味」材质。

## 11. v2 升级 · 主题兜底扩充

`framed fine-art print` 万能兜底降频：新增论点型（copyright/ethic/report→亚麻布空白对开本）、工作流型（workflow/agent/pipeline→弧形排布的三张空白工作卡）、展览型（portfolio/gallery→聚光灯下的空画廊架）等映射（生成器 §physical_form）。

---

## 12. v3 升级 · 内容全貌锚定（brief 不再只看标题）

> 用户要求：**每条提示词结合文章更多内容做微调**。落地方式：抓取全量 2,035 篇 master 文章的正文摘要
> （前 35 个内容块 + 全部 H2/H3，存 `inventory/content.json`），为每篇建立**内容画像**，注入 brief：

| 信号 | 提取方式 | 注入到 |
|---|---|---|
| **交付物形态** | 正文全文匹配 32 类设计交付物词典（moodboard/menu/brand kit/deck/画册…） | Output / StepCompare / PillarHero / PillarThumb —— 优先级 **content > slug > fallback** |
| **目标受众** | 正文受众词典（freelancer/small business/marketer/photographer/agency…） | Persona（「谁在工作」用真实受众，不是通用 designer） |
| **实际步骤数** | H2 结构中过程语义小节计数（clamp 3–5） | Diagram 的 token 数量（图示节点 = 文章真实步骤） |
| **提及工具** | 正文中的竞品/工具品牌词 | brief `signals.tools`（审计用，不进画面——图内禁文字） |

**v3 实测**：交付物形态 **98% 来自正文**（1,994/2,035；slug 16；兜底仅 25 = 1.2%）；84% 文章提取出真实受众；1,234 篇提取出真实步骤数。
每条 brief 带 `signals` 字段（form_source / audience / steps / tools），**每张图的内容依据可审计**。

## 13. v3 升级 · 一致性三层模型（质量差异防控）

| 层 | 冻结/机制 | QC 校验 |
|---|---|---|
| **站点层** | 调色板家族（暖中性三微域）、深炭墨、珊瑚点睛 ≤10%、光签名（单一光源+受控投影）、六航道 token、全局负面词、16:9 比例、主体占幅 | 全量逐条校验（禁词/比例/点睛/留白） |
| **分类层** | 航道映射按分类固定；**背景微域**：How-To/Pillar=暖象牙（工作台/美术馆世界）、Reviews/BP/Stack=灰米（评测世界）、Insight/Better Design/其余=纸米白（编辑部世界）——同分类视觉亲缘，跨分类同族不串味 | 分类→微域映射全量校验（v3 修复 245 条漏注后 = 0 错误） |
| **篇内层** | 同篇：锁 seed（可复跑）、机位 6 选轮换互异、原型轮换互异、**全篇槽位共用同一交付物形态**（一篇讲菜单，篇内所有图都是同一张菜单的世界） | 篇内重复 = 0（机位/原型/形态来源三查） |

> 质量差异大的两个根源已被机制性消除：① 兜底滥用（1.2%）② 槽位之间各画各的（篇内形态统一）。
