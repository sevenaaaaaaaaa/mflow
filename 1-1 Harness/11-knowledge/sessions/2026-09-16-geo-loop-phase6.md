---
type: session-log
session_date: 2026-09-16
session_slug: geo-loop-phase6
status: ready
---

# Session Log — Phase 6 GEO Content Loop（首批全链路）

## 目标
用户拍板：把 MFlow 升级为「GEO 时代内容 LOOP 形态的创新工具」。核心形态变化：回流信号从"排名/点击"换成"AI 引用"，引用缺口直接驱动下一轮选题与改稿，形成感知→归因→缺口→选题/改稿→发布→感知的真闭环。

## 交付（P6.2 → P6.1 → P6.3/4/5/6，同批全链路）

1. **P6.2 GEO 门禁**：`1-4 Dev/scripts/hooks/geo-check.sh` 五项检查——①可分块结构（H2 密度+最长章节 3500 字符阈值）②统计密度（每千字≥1 数据点，0 个即 BLOCK）③问答式标题/FAQ④外部来源≥2⑤墙式段落占比（>25% BLOCK）。默认宽松（WARN 为主）+ `--strict` 全升 BLOCK。**接入**：HOOKS 注册表（质量钩子页可手动跑）、loop_engine 双钩子级联（post-write + geo 任一 BLOCK 带反馈重试）、/api/generate 返回 geo_rc/geo_out、gen_prompt 注入 GEO_RULES（生成端从源头保证可引用）。
2. **P6.1 引用感知**：meta.geo{brand/competitors/queries} 配置（设置页 GEO 卡）→ `/api/geo/probe`（admin）逐条查询走 OpenAI 兼容 chat API（项目 Key 覆盖生效）→ 品牌提及/竞品提及/来源 URL 提取 → `run/projects/{id}/citations.jsonl`。**fail-clean**：demo 模式（无 Key）拒绝探测——演示稿不代表真实 AI 引擎行为，防止假数据污染引用库。只走官方 API，不爬引擎（铁律边界）。
3. **P6.3 归因**：/api/impact 并入 geo_summary（查询级提及率/竞品份额），GSC 点击 × AI 引用同屏。
4. **P6.4 缺口→选题**：GEO 卡缺口行「→ 选题队列」按钮（复用 /api/topics/add，自动排程消化）。
5. **P6.5 缺口→改稿**：「→ 改稿 Loop」按钮（item_id=refresh-{slug}，brief 内置 GEO 重写指令：问答式 H2/数据点/FAQ/短段/来源），复用既有 Loop 引擎全链路。
6. **P6.6 GEO 仪表**：GEO 卡渲染品牌提及率 + 竞品份额 + 近 14 日趋势迷你柱图（实心=被提及日）+ 缺口清单。

## 踩坑
- geo-check.sh 第一版：`$VAR` 后紧跟全角括号导致 bash 变量解析错乱（unbound variable）——多字节邻接必须 `${VAR}` 花括号
- `set -o pipefail` 下 `grep -oE | wc -l` 在 grep 无匹配时整管道 exit 1 → 命令替换内也要 `|| true`
- probe 首次 e2e 暴露 demo 模式数据污染问题 → 加 fail-clean 守卫（比事后清洗数据便宜）

## 验证（服务器真实执行）
- geo-check 服务器正例 PASS(0) / 反例 BLOCK(1e2w)，strict 模式 PASS→BLOCK 升级正确
- geo config 保存/读取 ✓；probe 无 Key fail-clean 400 语义 ✓；citations 汇总含 trend14(14 点) ✓
- console 双端语法校验（python ast + node --check）✓
- 测试数据清理：citations.jsonl 清空重置

## Loop 闭环形态（自 P6 起）
```
设置页配置(品牌/竞品/查询) → 探测(官方API) → citations.jsonl
→ 缺口(0提及查询) → [选题队列] / [改稿Loop]
→ 自动排程消化 → 生成(geo-check 级联) → 人工审 → 发布
→ 归因(impact×geo) → 再探测 → …
```

## 下一步（P6 二批候选）
- 定时探测（挂 schedule_executor 或独立 timer，每日一次）
- Perplexity sonar 等真带 citations 的引擎接入（model 名区分）
- citations × 已发布 URL 精确归因（哪个页面被哪次回答引用）
- GEO 分数进自我迭代仪表第三曲线
