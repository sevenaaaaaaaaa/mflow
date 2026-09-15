# Content Voice Rules v0.1

Voice mode 决定「用多少 evidence 能说多少话」。

## Mode 1 — Synthesis（合成）

**允许 when**：合成 ≥ 3 个 T2+ sources 成 coherent 整体。

**禁用句型**：
- "always / never / best / worst"
- "every / no one / all"
- "studies show" / "the data shows"

**健康句型**：
- "X said this; Y said that; the picture looks roughly like Z"
- "Multi-source consensus direction is X; the spread between sources is Y"
- "Sources [T1], [T2], [T3] agree on..."

**For example**：State of AI Design 2026；landscape reports；tool category overview。

## Mode 2 — Prescription（处方）

**允许 when**：≥ 5 真实用户原话支持方向（含 caveat）。

**禁用句型**：
- "the right way is / you must / everyone should"
- "the best practice is"
- "obviously / clearly / simply"

**健康句型**：
- "If you're in situation X, one approach we saw several teams use: Y"
- "We've also seen W fail when…"
- "One team's report: Q. Worth trying, with caveat R."

**For example**：How-to guides、playbook、framework templates。

## Mode 3 — Authoritative Voice（受限）

**默认禁止**。这是 **最易 fabrication** 的 mode。

**允许 ONLY when ALL FOUR true**：

1. Domain expert 具名 attribution（可联系 / 可核验）
2. Review trail 公开 + 可质询
3. Failure cases 与 success 并列
4. SOP 可被 3rd party 复现（步骤完整到能照抄）

**违反任一 → 自动降 Mode 2 + 重写**。

**Even when allowed, must include**："*This reflects one team's view as of [date].*"

## Voice upgrade gate（防漂移）

写完 Mode 1 / 2 后问：

> "如果这是错的，谁会打脸？"

如无法具名指出来 → 你已经默认在 Authoritative voice mode，但没满足 4 项豁免条件。**降 Mode 2 + 重写**。

## Mixing modes in one deliverable

每个子 section header 标 mode：

```
## Section 1: Landscape
mode: Synthesis [T1, T2]

## Section 2: Workflow playbook
mode: Prescription [T2, multi-source, ≥5 user voices]

## Section 3: Market gaps
mode: Mixed [T3, illustrative of unsolved questions]
```

每个 section 内部一致。

## Voice traps — auto-reject

触发即重写：

- "Most experts say..."
- "Studies show..."
- "It is well-known that..."
- "Obviously..."
- "The best practice is..."
- "Everyone knows..."
- "Any expert will tell you..."

这些都隐含 authority 我没赚到。

## Counter-evidence requirement

**任何 continuous claim** 后面必须至少有 1 个 counter-evidence：

| Claim | Counter-evidence 形态 |
|-------|---------------------|
| "Recraft 是 logo SVG 的 leader" | "r/artificial 用户原话：'from a logo design perspective they are all bad'" [URL] |
| "dashboards 是 superdesign 数据第一品类" | "Superdesign = dashboard builder 自带 ±20% 偏差" [T4] |
| "三档 pricing 比单档转化高 1.4×" | "Studies cited first-hand，绝大部分未发表；视为假设" [Gap #X] |

## Anti-fabrication trigger phrases

写完每个 section 前 grep：

```
must / always / never / obvious / everyone / best / worst / simply / clearly / the truth is
```

每命中一次 → 检查：这条 claim 是不是降 Mode 2 的候选？降了就改写。
