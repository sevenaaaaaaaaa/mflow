# media-marquee · 媒体横向跑马灯

> **section type**：`media-marquee`  
> **图片来源字段**：`items[].src`  
> **尺寸 / 比例**：1000 × 1000 · 1:1  
> **每实例图片数**：8  

## 模块形态

图片不停横向滚动，每张图含 caption + 作者 + 宽高。

**用途**：用于「创作多样性」快速证明，视觉上像作品瀑布。

## 本模块专属纪律

1. **8 张必须是 8 个不同品类**，横滚时才有「广度」感
2. 统一背景与光向，横滚时画面不闪
3. 图片按 1:1 裁切，主体居中偏上（下方有 caption）

## 通用规范

| 项 | 要求 |
|---|---|
| 图内文字 | **零**。含可读字符即废稿；如模块自带排版，用抽象灰色条块表达层级 |
| 多语言 | 同页面 10–11 语言版本共用同一套图，按模块做、不按语言做 |
| 安全区 | 四边 ≥5% 裁切余量，主体不触边 |
| 体积 | JPG q85 或优化 PNG ≤1.5MB |
| 禁用元素 | 紫蓝渐变 / 玻璃拟态 / 悬浮 3D 球 / 等距插画 / 光轨 / floating chips / 多点拼贴 |

---

## 提示词（8 条）

> 同一个页面里同模块的多张图**必须同会话 + 锁 seed + 同风格参考**，只换对象。

### 01 · 海报

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a poster standing against a plain backdrop, the subject fills about 70% of frame, 1:1, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 海报 — media-marquee visual`
- **命名**：`media-marquee-01-item-v1.png`

### 02 · 包装

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a small package box at a three-quarter angle, the subject fills about 70% of frame, 1:1, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 包装 — media-marquee visual`
- **命名**：`media-marquee-02-item-v1.png`

### 03 · 名片

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a pair of business cards overlapping, the subject fills about 70% of frame, 1:1, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 名片 — media-marquee visual`
- **命名**：`media-marquee-03-item-v1.png`

### 04 · 社媒图

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a square social card with a bold central shape, the subject fills about 70% of frame, 1:1, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 社媒图 — media-marquee visual`
- **命名**：`media-marquee-04-item-v1.png`

### 05 · 封面

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a book cover standing upright, the subject fills about 70% of frame, 1:1, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 封面 — media-marquee visual`
- **命名**：`media-marquee-05-item-v1.png`

### 06 · 菜单

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, an open menu page at a slight angle, the subject fills about 70% of frame, 1:1, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 菜单 — media-marquee visual`
- **命名**：`media-marquee-06-item-v1.png`

### 07 · 横幅

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a wide banner sample laid flat, the subject fills about 70% of frame, 1:1, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 横幅 — media-marquee visual`
- **命名**：`media-marquee-07-item-v1.png`

### 08 · 标签

```text
High-end commercial photograph, 85mm shallow depth of field, soft key light from the upper left with a gentle contact shadow, a product label on a small bottle, the subject fills about 70% of frame, 1:1, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

- **Alt**：`Lovart 标签 — media-marquee visual`
- **命名**：`media-marquee-08-item-v1.png`
