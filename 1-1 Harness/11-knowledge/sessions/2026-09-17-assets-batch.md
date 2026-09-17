---
type: session-log
session_date: 2026-09-17
session_slug: assets-and-batch-p12-1
status: ready
---

# Session Log — Phase 12.1 落地页图片物料台账与批量替换

## 背景
用户要"通过对话调用 skills/上下文/harness 执行批量生成·修改·QA·图片物料批改"。自评结论：MFlow 当前只支持固定流水线，四项里仅半覆盖。用户确认开工顺序 1→3→2→4，本次做 **1（图片物料）**。

## 关键发现（首次全量扫描）
- 物料位置：`compositePage.cover`（imageSource/external url）2,053 页 · `bodyJson[].media{src,alt}` 9,265 页 · `blog.coverUrl` 2,087 篇
- **17,538 页只引用 208 个素材 URL**：最高复用单图 **7,204 次**（cover 1,654 + media 5,550）= 默认占位图；blog 封面集中在 liblibai CDN（213/173 次）
- 图片多为外部 CDN（imageAsset 仅 18 个）→ **批改只需 patch URL/alt，无需上传资产**

## 交付
1. `1-4 Dev/scripts/library/asset_tools.py`：scan（台账 + URL 反查）/ plan（exact·prefix·regex·url-map + 过滤）/ apply（重取 _rev + ifRevisionID + ≤50/批 + dry-run 默认 + 审计）
2. 工作台「内容库 → 图片物料」卡：扫描（后台+轮询）/ 台账（URL×次数×角色×alt，可过滤）/ 三步替换（计划→dry-run→应用）
3. API：`/api/assets/{inventory,plan,result}`（GET）· `/api/assets/{scan,plan,apply}`（POST，admin）
4. 文档 `docs/assets.md`

## 验证（线上）
- 扫描：17,538 页 / 208 URL / 90s / 台账 8.8MB（无错误）
- 计划：exact 匹配占位图 + 3 slug 限定 → 命中 3 处 cover
- dry-run 应用：3 patch → transactionId 返回、operations=update、**Sanity URL 未变（零副作用）**
- 双端语法门禁 + session-init 全过

## 踩坑
- 批次上限被分页吞掉（PAGE=100 时 \`--max 30\` 实际写 100）→ 两处（sanity_pull / asset_tools）都改为 \`docs[:limit-done]\`
- HTML 里误输入全角 \`＋\` → node --check 逮住（门禁有效）
- `max()` 取元组时误加 `[0]` 导致后续取值错位（脚本内联 python 常见坑）

## 下一步
- 用户给新图 URL / 替换规则 → 真实替换 pilot（3-5 页）→ 放量
- 然后 **P12.3 批量任务执行器**（1 与 4 都依赖它）
