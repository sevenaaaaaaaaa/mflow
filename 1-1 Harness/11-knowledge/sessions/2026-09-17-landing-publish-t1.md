---
type: session-log
session_date: 2026-09-17
session_slug: landing-publish-t1
status: ready
---

# Session Log — Phase 17 落地页整页发布（T1）

## 关键发现（决定设计）
**`compositePage` 没有 `status` 字段**：实测 9,303 篇中 0 篇有 status → 落地页**无草稿态，真实写入立即前台可见**。
→ 所以 T1 采取比 blog 更保守的三重保险：默认 dry-run · 真实写入需显式 `confirm_public` · 更新优先 patch 模式。

## 交付
1. **生成**：`md_to_sections()` md → composite-v2 版块
   - hero-split（title/description/CTA/cover，highlightedText 取描述首句）→ feature-detail（按 H2 归组）→ proof-block（≥2 含数字句）→ faq（`## FAQ` 容器或问句 H2/H3）→ cta-default
   - **去重**：hero badge 置空、feature-detail 不重复 section/item 标题（首版 1280 字符被校验拦下 → 修后 903 合规）
2. **校验** `validate_sections()`：hero 必备 · 内容版块 ≥2 · FAQ ≤8 · cta 必备 · 文案 200–1200（RULES-70 落地页档）· hero media 需 alt
3. **写入** `publish_composite()`：`create`（createIfNotExists）/ `patch`（读 _rev → set 指定字段 + ifRevisionID；文档不存在则拒绝）
4. **批量**：执行器 `publish_sanity`（blog/composite 通吃，含配额真实写入计量与熔断）
5. **API**：`/api/publish/sanity` 增 doctype/page_type/mode/cover_url/confirm_public/sections_path
6. **UI**：发布通道卡新增「文档类型 / 落地页模式 / 封面 URL / 确认公开可见」；未勾选确认时真实发布被拒
7. **测试**：新增 5 用例（md→版块、薄内容拒绝、缺 hero/alt 拒绝、doc 结构、非法 page_type）→ 共 **26 用例**（GATE 6 线上通过）
8. 文档：`docs/publish.md` 新增落地页章节（含"写入即上线"警告与 patch 优先建议）

## 线上实测（dry-run，零副作用）
- create 模式：5 版块，tx 返回；patch 模式（ai-video-generator-en）：5 版块，tx 返回
- 未勾选确认的真实发布 → 被拒（明确提示"写入即上线"）
- Sanity 侧校验：新建样本不存在、既有页 `_updatedAt` 未变（未被 dry-run 污染）
- 门禁：GATE 6 线上 26 用例通过

## 剩余（矩阵）
T2 内容库增量同步 · T7 执行器端到端测试 · 落地页「批量改稿→patch 上线」闭环预设
