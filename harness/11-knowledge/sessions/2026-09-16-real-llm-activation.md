---
type: session-log
session_date: 2026-09-16
session_slug: real-llm-activation
status: ready
---

# Session Log — 真实引擎激活（DeepSeek），GEO LOOP 脱离 demo

## 事件
用户配置 DeepSeek Key（存 run/llm.json 600，git-ignore，不入库不入日志）→ base https://api.deepseek.com/v1。llm/test 连通 ✓。

## 首次真实探测（2026-09-16 22:00 窗口）
- 4 条查询全跑真实引擎（auto=deepseek-chat），共 2507 tokens
- **品牌 0/4 被提及**——四条查询全是引用缺口（诚实基线）
- 竞品提及：Canva ×4 / Figma ×2 / Recraft ×2
- 竞品被引源 TOP：adobe.com ×5、canva.com ×4、midjourney.com ×3、spline.design/v0.dev ×2 → 对标选题素材
- GEO 综合分 0/100（提及 0 + 覆盖 0 + 份额 0 + 结构健康 0——7 篇衰减页拉满扣分，如实反映）

## 首条真实改稿 Loop（缺口闭环 e2e）
- refresh-best-ai-design-tool（缺口查询 #1 + 竞品被引源上下文）
- DeepSeek 1737 字符 / 1460 tokens，round 1 即 PASS：post-write ✓ + geo-check ✓ → S3-draft→S3-done→S4-qa
- 草稿质量抽查：真实数据点（Canva 2.2 亿月活 / Adobe 200 亿收购案）、问答式 H2、来源标注（canva.com/adobe.com/midjourney.com）、Lovart 定位自然（"解决生成与可编辑画布断层"）——GEO 门禁在真实稿上首次生效
- 状态：S4-qa 等人工审（发布仍走人工授权铁律）

## 配置现状
- probe_daily = ON（每日 09:30 后自动探测 4 查询）
- auto_refresh = OFF（改稿烧 token，待用户显式开启）
- 引擎 = auto（deepseek）；Perplexity 留位（有 Key 即可加多引擎交叉）

## 意义
GEO Content Loop 从 demo 全链路转为**真实运转**：探测→缺口→改稿→门禁→人工审已全绿；综合分从 0 起步（基线），后续曲线看收敛。
