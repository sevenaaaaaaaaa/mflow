# comparison-before-after · 前后对比滑块

> **section type**：`comparison-before-after`  
> **图片来源字段**：`before.media.src` + `after.media.src`  
> **尺寸 / 比例**：1600 × 900 · 16:9  
> **每实例图片数**：2  
> **站内覆盖页面**：约 614 个文档

## 模块形态

单图分左右两半（带可拖动竖杠），各贴 label；`aspect` 支持 1:1 / 4:3 / 3:4 / 9:16 / 16:9。

**用途**：用于「改造前 vs 改造后」的强对比证明。

## 本模块专属纪律

1. **before 与 after 必须同主体、同构图、同机位**——只有「状态」不同，否则滑块会跳
2. 分割线在正中；两半的分辨率、亮度基线要一致
3. 这是唯一「拖拽交互」的模块，图片质量直接决定说服力

## 通用规范

| 项 | 要求 |
|---|---|
| 图内文字 | **零**。含可读字符即废稿；如模块自带排版，用抽象灰色条块表达层级 |
| 多语言 | 同页面 10–11 语言版本共用同一套图，按模块做、不按语言做 |
| 安全区 | 四边 ≥5% 裁切余量，主体不触边 |
| 体积 | JPG q85 或优化 PNG ≤1.5MB |
| 禁用元素 | 紫蓝渐变 / 玻璃拟态 / 悬浮 3D 球 / 等距插画 / 光轨 / floating chips / 多点拼贴 |

---

## 提示词（6 条）

> 同一个页面里同模块的多张图**必须同会话 + 锁 seed + 同风格参考**，只换对象。

### 01 · 草稿 vs 成品

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a rough pencil sketch on the left half transforming into a polished printed artwork on the right half, the subject fills about 70% of frame, 16:9, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 草稿 vs 成品 — comparison-before-after visual`
- **命名**：`comparison-before-after-01-vs-v1.png`

### 02 · 低清 vs 4K

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, one photo print with a blurred left half and a razor-sharp right half, the subject fills about 70% of frame, 16:9, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 低清 vs 4K — comparison-before-after visual`
- **命名**：`comparison-before-after-02-vs-4k-v1.png`

### 03 · 杂乱 vs 整洁

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a cluttered work desk left half and a clean organized right half, the subject fills about 70% of frame, 16:9, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 杂乱 vs 整洁 — comparison-before-after visual`
- **命名**：`comparison-before-after-03-vs-v1.png`

### 04 · 普通 vs 品牌化

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, the same layout left half without brand treatment and right half with a coherent brand system, the subject fills about 70% of frame, 16:9, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 普通 vs 品牌化 — comparison-before-after visual`
- **命名**：`comparison-before-after-04-vs-v1.png`

### 05 · 灰调 vs 调色

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, one photo with a flat desaturated left half and a richly graded right half, the subject fills about 70% of frame, 16:9, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 灰调 vs 调色 — comparison-before-after visual`
- **命名**：`comparison-before-after-05-vs-v1.png`

### 06 · 空背景 vs 场景

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a product on plain white left half and the same product in a styled scene right half, the subject fills about 70% of frame, 16:9, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 空背景 vs 场景 — comparison-before-after visual`
- **命名**：`comparison-before-after-06-vs-v1.png`
