# Deliverable Template v0.1

每个交付用此结构。无 exception。

## Header（强制）

```markdown
# [Title]

mode:           synthesis | prescription | mixed (per-section)
audience:       [谁读、决定改什么]
valid_from:     YYYY-MM-DD
valid_through:  YYYY-MM-DD
                - default sections: max = valid_from + 90 days
                - pricing-sensitive sections: max = valid_from + 30 days (mandatory 月度 mini-refresh 后才可续)
                - benchmark/version-sensitive: same 30d
sources_count:  T1=N, T2=N, T3=N, T4_dropped=N
counter_ev:     [URL, "what the dissent claimed"]  (or "no dissent found")
pricing_sensitive_sections: [list of section titles needing 30d refresh]
```

## Body 规则

- 每个 claim 句末贴 `[T1]` / `[T2 multi-source]` / `[T3 single]` tag
- 用户 quote 后立即 follow `[URL, date, author if available]`
- 表格必含 `source` column
- 子 section header 写明 voice mode（混合 deliverable 见 `04-voice-rules.md`）
- 数字必须 follow "as of YYYY-MM" 限定（尤其 pricing / benchmark）

## Evidence Gaps section（强制 footer）

```markdown
## Evidence Gaps (acknowledged)

| # | Gap | Why it matters | Action |
|---|---|---|---|
| 1 | e.g. Lovart.ai 专属 Reddit pain voice | User-voice-based differentiation | Pull Lovart 内部 NPS / CS verbatim |
| 2 | ... | ... | ... |
```

**没有 Gap 段 = 视为不诚实**。真实 Gap 永远存在。

## Refresh triggers（强制 footer）

```markdown
## Refresh triggers
- 90 天 elapsed → re-run pain mining
- ≥ 2 T2 sources contradict → drop claim
- 工具出新版本 → re-verify pricing / benchmark
- 新 counter-evidence 浮出 → 改 affected section
- 用户原话 < 10 条 → 重新跑 pain mining（preferable 标签）
```

## Anti-slop gate（强制 footer）

```markdown
## Anti-slop self-audit

| Gate | Check | Pass? |
|---|---|---|
| Specificity | 真具名产品/场景/角色（不是 generic prompt）  | yes / no / partial |
| Source trail | 每个 claim 有 tag | yes / no / partial |
| Three-source rule | strong claim ≥ 3 source | yes / no / partial |
| Counter-evidence | ≥ 1 alternative view | yes / no / partial |
| Time-to-rot | valid_through 标 | yes / no / partial |
| Role-of-frame | voice mode 与 evidence 匹配 | yes / no / partial |
```

**任一 "no" → 该 deliverable 不 ship，回到阶段 2 / 3 / 4 重做。**

## Pain voices table（推荐 included）

```markdown
## Voice-of-user (verbatim, with provenance)

| Pain (verbatim) | Source | Date | Notes |
|---|---|---|---|
| "..." | URL | YYYY-MM | T1/T2/T3 |
| "..." | URL | YYYY-MM | T1/T2/T3 |
```

**≥ 5 行；每行支持 deliverable 中至少一处 claim**。

## Lovart framing requirement

每 deliverable 在 footer 显式标：

```markdown
## Lovart positioning (when applicable)

- Tonal fit:  [matches Lovart's positioning / neutral / mismatch]
- Confidence: [T2 or T3 with explicit rationale]
- Do NOT claim: "Lovart is the best" / "Lovart is unique" without enterprise-internal evidence
```

**避免 Lovart 自吹 / 自贬** 双向 fabrication。  
**只描述** Lovart 已知能力（来自官方文档），**不外推**。

## Failure mode (writing samples)

### ❌ Bad

"Most designers agree that Recraft produces real SVG vector output — this makes it the best choice for logo work in 2026."

Why bad: "Most designers" / "best" / 没有 source；Recraft 自家是 leaderboard owner，externally unverified。

### ✅ Good

"Recraft V4 generates native SVG (no rasterization step). Verified by [T1: Recraft docs] + [T2: Apatero 实测 5 个 prompt + Maginary 测试] + [T3: r/generativeAI 单帖用户证言 'Recraft... treats text like...'。'Best choice' 未独立验证 — many logo designers still reject AI logos in principle (counter-evidence: r/artificial, 'From a logo design perspective they are all bad')."

Why good: 6 tag inline、3 source 标 T1/T2/T3、明确 counter-evidence、不下 "best"。

---
