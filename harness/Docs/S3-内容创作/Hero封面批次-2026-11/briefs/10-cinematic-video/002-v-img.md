# V-IMG · image-gen

| 项 | 值 |
|---|---|
| ID | `V-IMG` |
| 分组 | hero-cinematic · 视频版（5 条） |
| section type | `hero-cinematic` |
| 来源字段 | `media.src`（type: video） |
| 尺寸 | 2400 × 1500 |
| 比例 | 16:10 · 8s 循环 |
| 主题 / 品类 | image-gen |
| 风格航道 | `L2-cinematic-still` |
| 优先级 | P3 |
| 时长 | 8s 循环 |

> 8s 静音循环 MP4 ≤8MB；需与对应 C-* 静帧同构图，用静帧作 poster

## Prompt

```text
Cinematic still, shot on 35mm film, strictly a two-color teal-and-amber palette with soft volumetric light and subtle film grain — A slow lateral truck across a sunlit painter's studio: window light sweeps over one large landscape painting on an easel as brushes in the foreground drift softly out of focus, warm neutral palette with one saturated accent inside the painting, 85mm, 8 seconds, no text, no letters, no watermark, composed in three depth layers (foreground, midground, background) with at most one hero element per layer, 16:10, top and bottom 8% fading to a neutral backdrop to match the static poster frame
```

## Alt 文案

`Lovart image-gen — cinematic hero motion`

## 本模块纪律

- 与 02 批对应静帧**同构图**，静帧作 poster
- 8 秒、循环、无音轨、≤8MB
- iOS 自动播放必须静音

## 交付

| 项 | 要求 |
|---|---|
| 命名 | `v-img-v1.png` |
| 体积 | ≤1.5MB（视频 ≤8MB） |
| 图内文字 | 零。含可读字符即废稿 |
| 安全区 | 四边 ≥5% 裁切余量 |
