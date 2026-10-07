---
type: session-log
session_date: 2026-09-16
session_slug: geo-loop-phase6-batch2
status: ready
---

# Session Log — Phase 6 二批（每日探测 / sonar 真引用 / 精确归因 / GEO 曲线）

## 交付（P6.7-P6.10，全部服务器 e2e）

1. **P6.7 每日自动探测**：`geo_scheduler` 守护线程（与 loop queue/schedule executor 并列，启动即挂载）——每 30 分钟检查每个项目：开了 `meta.geo.probe_daily` 且配置齐全且过了 09:30 且**当日无成功探测记录** → 自动跑 geo_probe；失败时写记账行（`ok` 缺省）不阻塞当日重试。设置页 GEO 卡加开关。
2. **P6.8 Perplexity sonar 真引用**：`llm_chat()` 抽出 `llm_chat_full()` 返回 `(content, meta)`——meta 含 `citations`/`search_results`（Perplexity 官方返回），**探测场景不做 demo 回退**（fail-clean 报错）。DEFAULT_LLM providers 增加 `perplexity`（api.perplexity.ai），设置页 LLM 卡自动出现该行可填 Key。GEO 卡引擎下拉（auto=现有 provider / perplexity=sonar）+ 模型名输入。auto 引擎维持"从答案文本提取 URL"的兜底路径。
3. **P6.9 精确归因**：`_published_canonicals()`（published.json）× citations URLs 路径归一化匹配（协议/子域/尾斜杠/query 全容错）→ `cited_pages`（slug/平台/被引次数/命中查询 TOP5）进 geo_summary → GEO 卡「被 AI 引用的页面」区。单测：utm 参数、尾斜杠、子域差异全部命中，外部源不误配。
4. **P6.10 GEO 曲线**：自我迭代仪表第四曲线 = 近 14 日品牌提及（实心柱=被提及日）+ 「引用缺口 N 条查询」徽标；复用 /api/geo/citations 无新 API。

## 边角修复
- scheduler "今日已探测"初版只看最后一行——失败记录会把当天卡死 → 改为扫当日行内任意 `ok:true`
- probe 失败行不写 citations.jsonl（防污染聚合），仅响应内返回 per-row error
- geo/config 保留 perplexity_model 旧值（body 未传时不丢）

## 验证
- 服务器 e2e：config 持久化 engine/probe_daily/perplexity_model ✓；perplexity 无 Key 时 per-row 明确报错（非静默非 demo）✓；citations 汇总含 cited_pages/trend14 ✓；impact 并入 geo ✓
- 归一化匹配单测 4/4（含 canva.com 不误配）
- 双端语法校验 ✓；测试探测数据已清（total:0）

## 待用户
- 要真探测：设置页 LLM 卡填 Perplexity Key（或项目级覆盖），GEO 卡选「Perplexity sonar」→ 开「每日自动探测」→ 立即探测跑一次看真实引用
