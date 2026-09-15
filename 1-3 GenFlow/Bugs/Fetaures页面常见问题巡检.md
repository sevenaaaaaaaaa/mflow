# 当前会话质量审计汇总

## 一、对应的质量问题

本会话源自用户反馈「一批 Features 页面质量很低，标题只是 slug 填充，页面内只有 2-3 个模块」。

经排查，根因是 **2026-07-30 session `20260728_211356_1c7773`（Features 列表页语言混乱修复）** 执行时，作为"语言混搭修复"步骤的一部分，用 `createOrReplace` 覆盖了 566 个 features 页面，但只写了 **3 段式极简 bodyJson**（hero-split → faq → cta-default），覆盖了 7/28 expand 脚本之前修复的完整内容，且标题直接 slug 拆词 + 模板后缀。

具体问题分类：

| # | 问题 | 数量 | 严重度 |
|---|------|------|--------|
| Q1 | 页面仅 3 段（hero+faq+cta），模块残缺 | 54 页 | 🔴 高 |
| Q2 | hero title 过短（<20 字符，纯 slug 拆词） | 86 页 | 🟡 中 |
| Q3 | hero title 含模板后缀（"— AI Design Tool" / "AI Design Agent"） | 51 页 | 🟡 中 |
| Q4 | hero 无图片（media.src 为空） | 54 页（随 Q1 修复） | 🟡 中 |

> 注：Q2 与 Q3 有重叠（部分页面同时满足），实际唯一页面数 = 137 页有标题问题。

---

## 二、排查进度

| 阶段 | 动作 | 结果 |
|------|------|------|
| 1. 定位来源 | 查 Sanity `_createdAt`/`_updatedAt`，确认 54 页全部 2026-07-30 创建 | 确认为当日批量流程覆盖 |
| 2. 确认流程状态 | 查 session 历史 + cron，确认触发源 session 已结束 | 不会再产生新 thin 页 |
| 3. 修复 Q1（3 段→13 段） | 按正常 13-block 模板生成完整 bodyJson，patch 54 页 | ✅ 0 页残留 |
| 4. 修复 Q2（短标题） | 86 页标题重写为利益导向格式 | ✅ 0 页残留 |
| 5. 修复 Q3（模板后缀） | 51 页标题去模板化，改写为具体功能描述 | ✅ 0 页残留 |
| 6. 验证 | 全量审计 hero title 长度 + 模板词 + 段数 | ✅ 全部清零 |

---

## 三、修复手段

**Q1 — 13-block 模板重建**
- 参考正常 features 页（如 `ai-3d-animation`，13 段）的结构
- 脚本 `/tmp/fix_thin_features.py`：对每个 slug 生成 `hero-split → bento-4 → capability-tabs → prompt-launcher → bento-2 → canvas-wall → workflow-horizontal → comparison-table → cluster-block-dense → feature-detail → proof-block → faq → cta-default`
- 用 `slug_to_name()` / `slug_to_action()` 从 slug 推导可读名称填入各模块
- 同步补 `seo.description`（模板改为具体功能描述）

**Q2/Q3 — Hero Title 重写**
- 脚本 `/tmp/fix_short_titles.py`（86 页）+ `/tmp/fix_generic_titles.py`（51 页）
- 手工维护 `TITLE_MAP` / `FIXES` 字典，按 slug 匹配利益导向标题（如 "AI Coupon Maker — Design Professional Coupons in Seconds"）
- 同步更新 `hero.title` + `bodyJson[0].title` + `doc.title` + `seo.title` + `seo.description`
- 未匹配 slug 用 fallback 规则生成

**技术手段**：Python `urllib.request` 直接调 Sanity Mutate API（`/data/mutate/production`，每批 ≤50），绕过 curl（sandbox 中 curl 返回 HTTP 000）。

---

## 四、潜在风险

| 风险 | 说明 | 缓解 |
|------|------|------|
| **R1. 多语言不同步** | 本次只修了 EN。ZH/ZH-TW/JA/KO/RU/DE 等对应 slug 的 features 页若也走了 7/30 的 3 段覆盖，现在 EN 已修、其他语言仍残缺 | 需按语言排查 `features-ai-*` 非 EN 页面的段数 |
| **R2. 内容泛化** | 13-block 模板是"通用填充"，未针对每个 slug 的具体功能深度定制（如 ai-coupon-maker 的 bento 描述和正常页一致但偏泛） | 属"最低可用"修复，SEO 价值有限，后续可针对性重写高流量页 |
| **R3. Tools 镜像页未同步** | 261 对 Tools↔Features 同 slug 页面，之前已做差异化。本次只改了 Features 的 EN，Tools 对应页若也曾被 7/30 覆盖，可能仍是 3 段 | 需排查 `tools-ai-*` 段数分布 |
| **R4. CDN 缓存** | Sanity patch 后前端可能 5-10 分钟才刷新，用户立即看可能以为没修 | 已告知，无需动作 |
| **R5. FAQ 内容浅** | 生成的 FAQ 是通用 6 问（"Is it free?" / "Do I need design experience?"），未针对具体工具 | 高流量页后续可补真实 FAQ |

---

## 五、还能做哪些

1. **多语言补齐（R1）** — 对 ZH/ZH-TW/JA/KO/RU/DE/FR/IT/PT 的 `features-ai-*` 跑同款段数审计，找出被 7/30 覆盖的 3 段非 EN 页，批量重建 13-block（翻译 EN 源）。
2. **Tools 镜像排查（R3）** — 审计 `tools-ai-*` 的段数分布，确认是否也有 54 个被 7/30 覆盖的 thin 页。
3. **高流量页深度重写** — 用 GSC 数据筛出 features 页中 impression/top 流量的 slug，针对性重写 bento/comparison/faq 为真实内容（而非通用模板）。
4. **标题 SEO 二次优化** — 部分标题虽已去模板化，但长度偏长（>60 字符可能被 Google 截断），可按 L2b 规则截断到 50-60 字符。
5. **防回归** — 在 AGENTS.md 或 quality-gates skill 中加入铁律：「任何 createOrReplace features/tools 页面必须 ≥8 段，否则 BLOCK」，防止未来批量流程再次覆盖成 3 段。

---

**当前状态**：EN Features 页面的结构完整性（段数）和标题质量（长度+模板化）均已修复归零。主要遗留风险在多语言同步和 Tools 镜像页，以及内容深度泛化。

需要我继续做哪一块？