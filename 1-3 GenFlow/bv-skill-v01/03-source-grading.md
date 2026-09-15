# Source Grading v0.1

每条事实一个 tag。Deliverable 末尾贴 tag 分布。

## T1 — 强（≈ first party）

**真源**：厂商官方文档 / GitHub / 论文 / 学术 benchmark / 监管文件 / 法院记录。

**多个独立 indicator**：
- `recraft.ai/docs/...`
- `lovart.ai/...` 官方域
- `github.com/[厂商]/[官方 repo]`
- arXiv / DergiPark / IEEE / ACM

**Allowed**：
- Core assertion："X 原生导出 SVG"
- 价格（必须带 `valid_through` 日期）

## T2 — 中（≈ second party）

**真源**：独立专业测评 / 长文独立评测 / 大媒体记者稿 / 设计社区共识 / ≥ 3 独立确认的趋势。

**Multiple examples**：
- Forbes / TechCrunch / VentureBeat
- Apatero / Maginary / MytheAi / Apostle 类独立测试
- 多个独立 Reddit 帖共振
- 设计社区（Dribbble 评论 / AIGA / 99designs 论坛）

**Allowed**：
- Prescription 带明确 "(multi-source T2)" 标签
- 趋势 claims "as of YYYY-MM"

## T3 — 弱（≈ single first-hand）

**真源**：单 Substack / 单 Reddit 帖 无下游共鸣 / 个人博客 / 假装中立的 affiliate review。

**Allowed ONLY when**：
- 显式贴 `[T3]` 标签
- 经独立 query 二次确认 → 升 T2
- 或作 illustrative anecdote（不作 evidence）

## T4 — 排除（drop，不引）

**真源**：
- 工具自家 leaderboard / 自评 benchmark
- 无方法论的 self-published benchmark
- 付费 award / 认证
- 厂商赞助的 "research"

**Selection bias 提醒**：
- Recraft 是 HuggingFace Text-to-Image 榜第一 → **T4**（自家参赛）
- Midjourney 自评 "aesthetic ceiling" → **T4**
- Superdesign 自报 "dashboards 第一" → **T4**（Superdesign 就是 dashboard builder）

## 跨级规则

| Pattern | Tag |
|---------|-----|
| "Tool says X" + 0 独立 confirm | T3 |
| "Tool says X" + ≥ 2 独立 confirm | T2 升 |
| "Industry consensus Y" + ≥ 3 独立 confirm | T2 |
| "1 source Y" + 反向 source + 无法 reconcile | drop |

## 日期衰减（date drift）

**易腐烂**：工具价格、模型版本、benchmark、月活
**默认 `valid_through`** = 90 天
**过期未追源** → auto-downgrade T1 → T2；T2 → T3

## 写作时的 tag 表达

- 句子末尾：`[T1]`、`[T2 multi-source]`、`[T3, single source]`
- 表格：Source 列填 tag 简码 `T1` / `T2` / `T3`
- 全部 deliverable 末尾 footer：

```
sources_count: T1=N, T2=N, T3=N, T4_dropped=N
```

## 自检问题

1. 这条 claim 的最强源是 T1？T2？T3？
2. 我能反向找到 ≥ 1 个 ownership 不同的源证实？否则降 T。
3. 这事 90 天后还成立吗？成立 → 标 valid_through，不成立 → 标 "as of YYYY-MM"。
