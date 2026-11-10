# C-IMG · image-gen

| 项 | 值 |
|---|---|
| ID | `C-IMG` |
| 分组 | hero-cinematic · 全宽剧院图（5 条） |
| section type | `hero-cinematic` |
| 来源字段 | 段首 `media.src` |
| 尺寸 | 2400 × 1500 |
| 比例 | 16:10 |
| 主题 / 品类 | image-gen |
| 风格航道 | `L1-photo-editorial` |
| 优先级 | P1 |
| 覆盖页面 | 约 2 页 |

## Prompt（V3）

```text
High-end editorial photograph, wide shot in three layers — foreground a blurred jar of brushes catching north window light, midground one large vivid landscape painting on a hand-sanded oak easel in full focus with three earlier studies leaning behind it, background a tall window with soft out-of-focus daylight — the painting still wet at one edge, warm neutral base with one saturated accent living only inside the painting, material truth with visible surface texture, one focal point only, muted base with at most one accent, 16:10, top and bottom 8% fading to a neutral ground, no text, no letters, no watermark, no screens, no UI windows
```

## Alt 文案

`Lovart image agent — studies resolving into one finished painting`

## 风格锚定

**三层锚定**：材质真实（可触摸的表面肌理）· 单一焦点（只有 1 个视觉重心）· 克制配色（低饱和底 + 至多 1 个点睛色）

## 本模块纪律

- 三层深度（前 / 中 / 后），每层最多 1 个主元素
- 上下各 8% 渐隐过渡
- 文字全在图外

## 交付

| 项 | 要求 |
|---|---|
| 命名 | `c-img-v1.png` |
| 体积 | ≤1.5MB（视频 ≤8MB） |
| 图内文字 | 零。含可读字符即废稿 |
| 安全区 | 四边 ≥5% 裁切余量 |

