# Better Design Skill — v0.3

> v0.2 → v0.3: 加 category-anti-slop (07) + ethics-disclosure (08) + quota 软化 + buyer-side voice + authoritative auto-detect。
> v0.1 → v0.2: 关键词消歧, quota 提升, counter-evidence pre-flight, 价格 mini-refresh。

## 硬约束

**没有证据 = 没有 claims**。这不是 slogan，是掉一切 deliverable 的闸门。

## 适用场景

用于以下内容生产：
- Tool comparison / review / "X vs Y"
- 「Best AI for [垂直]」 列举型
- "How to / Why" 行业指南
- 趋势报告
- 工作流指南

不用于：寒暄、hard news、纯内部备忘（这些不需要 Source Grading）。

## 工作流（必须按顺序跑）

1. **Pre-research** — 锁问题。谁读？读这篇会改变什么决定？
2. **Pain mining** — 按 `02-research-protocol.md` 跑 query。≥5 真实用户原话。
3. **Three-source gathering** — 用 `03-source-grading.md` 给每条事实在 [T1]–[T4] 中贴标。
4. **Counter-evidence** — 至少搜 1 条反向观点。标 dissent。
5. **Voice mode** — 按 `04-voice-rules.md` 选 register（synthesis / prescription / authoritative）。
6. **Deliverable** — 按 `05-deliverable-template.md` 填 metadata + Evidence Gaps 段。
7. **Self-audit** — 6 项 anti-slop gate 全过 / 部分过 / 标缺口。

## 这不是

- 不是写作模板（它限制写法，不自动写）
- 不是 domain expert 替代品
- 不是保证正确性（源本身可能错）

## 哪些动作直接 break 这个 Skill

- 「Pain mining 太慢 / 直接写吧」
- 把 affiliate / 赞助贴当 evidence
- 写 always / never / best / worst 但 source < 3
- 用「工具自家排行榜」证「工具自家强」
- 不写 Evidence Gaps 直接交稿

## 测试实例

`brand-v2-test.md` — 用本 Skill 跑 Brand / Logo 类的示例输出。它是 meta-validate 工具：用 Skill 跑一次发现 Skill 哪里卡，再回头修 Skill。
