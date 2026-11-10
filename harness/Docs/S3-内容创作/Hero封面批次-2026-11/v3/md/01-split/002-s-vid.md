# S-VID · video

| 项 | 值 |
|---|---|
| ID | `S-VID` |
| 分组 | hero-split · 左文右图（20 条） |
| section type | `hero-split` |
| 来源字段 | 段首 `media.src` |
| 尺寸 | 2160 × 1620 |
| 比例 | 4:3 |
| 主题 / 品类 | video |
| 风格航道 | `L2-cinematic-still` |
| 优先级 | P0 |

## Prompt（V3）

```text
Cinematic still shot on 35mm film with subtle grain, strictly a two-colour teal-and-amber palette, golden-hour backlight with a faint lens bloom, laid on a print workshop bench with ink-stained felt, a single film strip held by hand-sanded oak pegs showing three progressive states of the same scene — raw frame, graded frame, finished frame — shallow depth of field at 50mm, material truth with visible surface texture, one focal point only, muted base with at most one accent, 4:3, edges safe for rounded-corner crop, no text, no letters, no watermark, no screens, no UI windows
```

## Alt 文案

`Lovart video agent grading one scene from raw frame to finished frame`

## 风格锚定

**三层锚定**：材质真实（可触摸的表面肌理）· 单一焦点（只有 1 个视觉重心）· 克制配色（低饱和底 + 至多 1 个点睛色）

## 本模块纪律

- 视觉重心落在中右 60%（左侧是页面文案栏）
- 四边 ≥5% 裁切余量（圆角卡片渲染）
- 主视觉 ×1 + 支撑元素 ≤2 + 背景 ×1；禁止画界面

## 交付

| 项 | 要求 |
|---|---|
| 命名 | `s-vid-v1.png` |
| 体积 | ≤1.5MB（视频 ≤8MB） |
| 图内文字 | 零。含可读字符即废稿 |
| 安全区 | 四边 ≥5% 裁切余量 |

