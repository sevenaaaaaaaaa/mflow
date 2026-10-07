# Solution 故事线文档同步清单

> 当 iCloud 锁定 `Refresh-Page/` 时，先在 `Pages/Solution/` 维护 SSOT；解锁后运行 `sync-solution-ssot.js` 并按下表手工合并 Markdown。

## 已在本目录完成（2026-06-07）

- `solution-storylines-v2.json` — 12 条故事线 SSOT，行业轴 6/6 有 JSON
- `SOLUTION-TAXONOMY.md` — 双轴选型说明
- `SOLUTION-PRODUCTION.md` — 生产指南与范例索引
- `lovart-solution-page.md` — Agent skill（镜像至 Harness）
- `en/ai-design-solution-for-saas-en.json`
- `en/ai-design-solution-for-creators-en.json`

## 待同步到 Refresh-Page（解锁后）

| 目标文件 | 操作 |
|----------|------|
| `solution-storylines.json` | `node sync-solution-ssot.js` |
| `STORYLINE-BY-DIRECTION.md` §1.1、§4.5 | Solution 6→12 条；故事线合计 36→42 |
| `STORYLINES.md` A4 | 替换为 P1–P6 + I1–I6 表 |
| `SOLUTION-PRODUCTION.md` | 以 `Pages/Solution/SOLUTION-PRODUCTION.md` 为准覆盖 |

## 待同步到 Harness

| 目标 | 操作 |
|------|------|
| `1-5 Harness/Skills/lovart-solution-page.md` | 复制 `lovart-solution-page.md` |
| `page-routing.md` / `lovart-page-serp-writer/SKILL.md` | 见 `HARNESS-PATCHES.md` |

## 待同步到角色手册

| 目标 | 操作 |
|------|------|
| `1-1 GEO Readme/文档/03-角色手册/For-Landing-Page-制作人.md` §4.5 | 1 条→12 条双轴说明 |
