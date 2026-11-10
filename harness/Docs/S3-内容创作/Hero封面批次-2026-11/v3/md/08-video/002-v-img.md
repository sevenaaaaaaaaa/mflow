# V-IMG · image-gen

| 项 | 值 |
|---|---|
| ID | `V-IMG` |
| 分组 | hero-cinematic · 视频版（5 条） |
| section type | `hero-cinematic` |
| 来源字段 | `media.src`（type: video） |
| 尺寸 | 2400 × 1500 |
| 比例 | 16:10 · 8s |
| 主题 / 品类 | image-gen |
| 风格航道 | `L2-cinematic-still` |
| 优先级 | P3 |

> 8s 静音循环 MP4 ≤8MB；需与对应 C-* 静帧同构图，用静帧作 poster

## Prompt（V3）

```text
Cinematic still shot on 35mm film, strictly a two-colour teal-and-amber palette, softbox rim light defining the silhouette against a darker ground, on against an open archive drawer of filed material samples, A slow lateral truck across a sunlit painter's studio: window light sweeps over one large landscape painting on an easel as brushes in the foreground drift softly out of focus, warm neutral palette with one saturated accent inside the painting, 85mm, 8 seconds, no text, no letters, no watermark, composed three layers deep with at most one hero element per layer, material truth with visible surface texture, one focal point only, muted base with at most one accent, 16:10, 8 seconds, top and bottom 8% fading to a neutral ground, no text, no letters, no watermark, no screens, no UI windows
```

## Alt 文案

`Lovart image-gen — cinematic hero motion`

## 风格锚定

**三层锚定**：材质真实（可触摸的表面肌理）· 单一焦点（只有 1 个视觉重心）· 克制配色（低饱和底 + 至多 1 个点睛色）

## 本模块纪律

- 与静帧同构图，静帧作 poster
- 8s 循环无音轨 ≤8MB

## 交付

| 项 | 要求 |
|---|---|
| 命名 | `v-img-v1.png` |
| 体积 | ≤1.5MB（视频 ≤8MB） |
| 图内文字 | 零。含可读字符即废稿 |
| 安全区 | 四边 ≥5% 裁切余量 |

