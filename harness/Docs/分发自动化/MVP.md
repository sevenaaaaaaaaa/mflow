# MVP 定义

## 闭环范围

**一条路径跑通**：GA blog S 级页 → Medium + DEV.to 摘要 → 人工确认 → 日志

| 项 | 选择 |
|----|------|
| 内容源 | Trident GA4 `/blog/` 页面 |
| 候选标准 | Distribution Score ≥75（S 级） |
| 平台 | Medium、DEV.to |
| 形态 | 轨道 A 摘要（20–40% 体量） |
| 发布 | API 半自动 + `--dry-run` 默认 |
| 验收 | preflight 100% pass + `logs/` 有记录 |

## 首篇试跑清单

- [ ] `python3 scripts/score-pages-for-distribution.py --days 28`
- [ ] 从 `queue/candidates-*.json` 选 1 篇 S 级 `/blog/`
- [ ] 用 `templates/syndication-excerpt.md` 生成 Medium、DEV.to 草稿
- [ ] `node scripts/preflight-distribution.js` 两篇均通过
- [ ] `publish-medium.js` / `publish-devto.js` 先 `--dry-run`
- [ ] 人工发布后写入 `queue/published.json` 与 `logs/`

## 不做（MVP 阶段）

- Hashnode / LinkedIn / Pinterest API
- Reddit / HN / 知乎 / 百家号 / DeviantArt 自动发
- 轨道 B 站外全文稿（仅 queue 占位）
- n8n / Sanity 发布合并

## 配额

- 本周：≤2 篇 blog × 2 平台 = 4 条
- 同一 URL 本月 ≤2 平台
