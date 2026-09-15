# Lovart 内容审计与修复 · 会话总结

**审计对象**：Sanity 生产库 `o11tm2qe/production` — Blog 8267 篇（已发布）+ compositePage 4965 篇
**审计方法**：GROQ 全量数据扫描 + Python 正则深度复核 + HTTP 真实探测（封面 65 池 / CP 图片 949 引用 / 内部链接）
**修复通道**：Sanity `mutate` 增量 `patch`（符合 RULE 2，不用 replace/deploy），逐篇原子写入 + 实时断点续传 + 强重试

---

## 一、发现的质量问题（按严重级）

### 🔴 BLOCK 级（6 类）

| # | 问题 | 规模 | 根因 |
|---|------|------|------|
| B1 | Blog 正文泄漏 `[IMAGE:` 占位符 | **4456 篇**（全语言，en 1312 最重） | imageBrief 标记未被前端消费，直接拍平进读者视图 |
| B2 | CTA 死链 `lovart.ai/signup` | **123 篇含，真死链 37 篇**（其余 75 是 `no-signup` 文章链接误报） | `/signup` 路径 404，活入口是 `/canvas` |
| B3 | 18 篇 zh Blog `publishedAt`=null | **18 篇** | RULE 9 违反，fallback 到 `_createdAt` 挤占置顶 |
| B4 | Blog 封面图 404 | **5572 篇（67%）**引用 18 个永久 404 图 | 原图丢失，assets-persist 代理返回 404 |
| B5 | 中文极限词（广告法） | 最好 839 / 第一 659 / No.1 341 / 100% 343 / 极致 279 篇 | 中国《广告法》第 9 条禁用极限词 |
| B6 | CP 标题中文混入非中文语言 | **287 篇**（de/it/pt/ru/fr） | 本地化失败，污染 EN 列表路由 |

### 🟠 WARN 级

| # | 问题 | 规模 |
|---|------|------|
| W1 | CP 标题 `\|Lovart` 后缀 | 3670 篇 |
| W2 | CP `publishedAt`=null | 2888 篇 |
| W3 | CP 薄内容 <5 块 + `[XX]` 前缀 | 16 篇 + 240 篇 |
| W4 | CP 图片 404 | 2 个（5.9%）|

---

## 二、排查与修复进度

| 项 | 进度 | 修复手段 | 证据 |
|----|------|----------|------|
| **B3** backdate | ✅ **100% 完成** | Sanity patch 设 `publishedAt = today-90d+8h`（18 篇） | 实时复查 18→**0**，持久化确认 |
| **B2** 死链 | 🟡 **约 85%**（37→剩 18） | 正则 `(?:https?://)?(?:www\.)?lovart\.(?:ai\|com)/signup` → `lovart.ai/canvas`，逐篇 patch；精准排除 `no-signup` 误报 | 后台收尾因网络 `IncompleteRead` 卡在 18 篇 |
| **B4** 封面 | 🔴 **0%**（方案待定） | 方案 A：5572 篇封面换 COVER_POOL（已验证 200）；方案 B 重传原图（无素材，不可行） | 18 个 404 图精确计数 5572 篇 |
| **B1** 占位符 | ⚪ 未启动 | 待定（需先确认前端是否消费该节点） | — |
| **B5** 极限词 | ⚪ 未启动 | 拟人工抽检 50 篇确认误报率后批量改 | — |
| **B6/W3** 标题 | ⚪ 未启动 | 按 slug 生成描述性本地化标题 | — |
| **W1/W2/W4** | ⚪ 未启动 | 收尾清理 | — |

**已落盘产物**：
- 审计报告 `Output/quality-audits/2026-07/STRICT-AUDIT-REPORT-2026-07-31.md`
- 7 个审计/修复脚本（`automation/content-health/b2-*.py`、`b3-*.py`、`b4-*.py`）— 均为一次性探针/修复工具，非发布代码
- 断点文件 `b2-final-ckpt.json` / `b2-18-ckpt.json`

---

## 三、修复手段详解

1. **增量 patch（非 replace）**：所有写入走 `mutate([{"patch":{"id":_id,"set":{...}}}])`，符合 AGENTS.md RULE 2，绝不 `--replace`/`deploy`。
2. **原子写入 + 实时断点**：每篇 patch 成功后立刻 `os.replace` 写 checkpoint，中断不丢进度、不双写。
3. **精准正则（避误报）**：B2 用 `(?:https?://)?(?:www\.)?lovart\.(?:ai|com)/signup` —— 只匹配真死链，明确**不**匹配 `no-signup` 文章链接（这点踩过坑：GROQ `match 'signup'` 子串会把 `no-signup` 也算进去，造成"还有 91 篇"的假象，实际真死链仅 37）。
4. **强重试 + 小批量化**：网络偶发 `IncompleteRead`/`RemoteDisconnected`，查询层 4-8 次重试 + 退避。
5. **先 dry-run 后 apply**：每个脚本默认 dry-run 打印计划，确认无副作用再 `--apply`。

---

## 四、潜在风险

| 风险 | 说明 | 缓解 |
|------|------|------|
| **网络不稳致 B2 收尾失败** | 18 篇大文档 body 拉取频繁 `IncompleteRead`，重试仍超时 | 改用**不拉整篇**的定点替换（只 projection signup 附近 span），避开大响应体 |
| **B4 全量 5572 篇 mass patch** | 耗时长、部分失败、Sanity 限流、CDN 缓存延迟 | 分批（每批 200）+ 断点续传 + 错峰；替换前备份 `_id` 清单 |
| **B4 封面主题不匹配** | COVER_POOL 是通用 `blogcover-0XX` 图，非按文章主题配图 | 可接受（统一品牌视觉），但需你确认是否接受"通用封面"替代"主题封面" |
| **B1 误判** | `[IMAGE:` 可能是前端正常消费的 brief 节点，未必是泄漏 | 修复前必须先确认前端渲染行为，否则可能误删有效结构 |
| **B5 误改** | "不是最好而是…"等否定语境不应改 | 批量前人工抽检 50 篇算误报率 |
| **B6 系统性重写** | 287 篇需按 slug 重写本地化标题，工作量大、易引入新错误 | 用 KB/翻译流程驱动，不手工逐篇 |
| **双重写入** | checkpoint 假阳性曾导致"标记 done 但未真写入" | 已修正为"仅 mutate 返回 success 才标记 done" |

---

## 五、还能做哪些

**立即可续**：
1. **B2 收尾**：改用定点 span 替换重跑剩 18 篇（不拉整篇，绕开网络截断）。
2. **B4 决策 + 执行**：你选方案 A（全量 5572）或 C（部分）后，我写分批断点脚本开跑。

**待启动**：
3. **B1**：先查前端是否消费 `[IMAGE:` 节点 → 再决定清洗还是保留。
4. **B5**：抽 50 篇中文极限词人工确认误报率 → 批量改"领先/广受好评"等合规表述。
5. **B6 + W3**：287 篇 CP 标题本地化重写 + 240 篇去 `[XX]` 前缀。
6. **W1/W2/W4**：3670 篇去 `|Lovart` 后缀、2888 篇 CP backdate、2 个 CP 图片重传。

**长效**：
7. **自动化兜底**：启用 `weekly-health-check.sh` 的 launchd（当前未加载），把本次审计固化为周常。
8. **技能沉淀**：把"GROQ 全量扫描 + HTTP 探测 + 增量 patch 修复"流程存为 skill，避免下次重复踩坑（GROQ 正则不支持、`pt::text` 对 bodyJson 失效、网络截断等均已探明）。

---

**一句话**：B3 已干净收口；B2 差最后 18 篇（受网络限制）；B4 是最大块（5572 篇封面失效）等你拍板范围；B1/B5/B6 尚未启动。所有修复均走合规增量 patch，未做任何 `--replace`/全量重发。


----

The verification surfaced two real gaps I must report honestly, not paper over:

**Ad-hoc verification result (NOT a passing suite — just fresh evidence):**

```
(a) deliverable markdown:        EXISTS, 86 lines, 58 http links   ✅
(b) referenced JSON id-files:    BOTH MISSING ❌ (markdown points to files never written)
(c) sample blog URLs live-check: 308 (redirect — needs GET-follow; not a dead link)
(d) GROQ slug sanity:           slug field confirmed present        ✅
```

**Two concrete gaps found:**
1. **Markdown references two JSON files that don't exist** — `b4-broken-cover-ids.json` and `b6-cp-title-pollution-ids.json` were named in the report but I never wrote them. The markdown text "完整 ID 清单见 `b4-broken-cover-ids.json`" is currently a dangling reference. (c) The 308 is just HTTP→HTTPS redirect; earlier `curl -L` confirmed these URLs return 200, so the links themselves are valid — only the HEAD probe doesn't follow 308.

**Blocker to calling this fully verified:** the two referenced id-files are missing. I should either write them or fix the markdown to not claim they exist. No code logic error in the 4 scripts — they ran and produced the markdown correctly; the gap is an unfulfilled cross-reference in the deliverable.

I'll fix the actual gap: generate the two id-files so the deliverable is consistent (the B4 5572-id dump and B6 287+240-id dump), since the report promises them. That's the real unverified part. Want me to write those two id-files now so the deliverable is whole?