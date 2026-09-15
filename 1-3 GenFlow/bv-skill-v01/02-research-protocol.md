# Research Protocol — Pain Mining v0.1

Pain mining 产生 deliverable 需要的 **真实用户原话**。
模式查询（"best X for Y"）失败；lived-experience 查询成功。

## Tier 1: pain surface（最高信号）

把 `[TOOL]` `[TOPIC]` 换成具体值：

```
"I hate [TOOL/类别]"
"[TOOL] doesn't work"
"[TOOL] broke / blew up"
"spent [hours/days] on [任务] with [TOOL]"
"refund [TOOL]"           ← billing / support 痛点
"tried [TOOL], here's what..."  ← 真 review 标志
```

## Tier 2: 对比摩擦

```
"[X] vs [Y]" real comparison
"alternative to [TOOL]"
"moving away from [TOOL]"
"anyone else [COMPLAINT]"  ← 共鸣检测
"why I left [TOOL]"
```

## Tier 3: edge / fail

```
"[TOOL] + failure"
"[TOOL] + limitations"
"[TOOL] + honest review"
"[TOOL] at scale"        ← 规模化崩点
```

## Tier 4: 工具主动搜索（验证主源）

```
"[TOOL] official / docs / release"
"[TOOL] + benchmark + 2026"
"[TOOL] pricing"
```

## Site 限定（叠加）

- `site:reddit.com`（首选：评论密度高）
- `site:news.ycombinator.com`
- `site:indiehackers.com`
- `site:producthunt.com`（评论≥5 条优先）
- Niche：`r/[domain]` 专属 subreddit
- Discord：直接搜频道（无 web 索引，列在 Gap 里）

## 时间窗口

默认 **180 天内**（约 6 个月）。
> 180 天外 = stale；可作 context，不作 evidence。

## 每个 deliverable 的 quota (v0.2 raised from ≥5)

| Item | Quota v0.1 | Quota v0.2 | Why raised |
|------|------------|------------|------------|
| 真实用户原话（verbatim + URL + date） | ≥ 5 | **≥ 10** | Brand/SaaS 测试发现 ≥5 容易 all-T3，低信号；≥10 allows ≥2nd source corroboration |
| 每条 strong claim 的独立 source | ≥ 3 | ≥ 3 (kept) | — |
| Counter-evidence source（反向观点） | ≥ 1 | **≥ 2 different angles** | "every claim got ≥1 counter" produced shallow dissent; 多角度反向反而 useful |
| T1 自家源（官方 / GitHub / paper） | ≥ 1 | ≥ 1 (kept) | — |
| Pain voices 涵盖 ≥ 2 个 niche community | — | **NEW: ≥ 2** | 单 community 单一类型 lead to 偏样本 |

## 强 claim 强 counter-evidence 要求

新增 **Pre-flight** 流程：写 strong claim 之前**先**跑 reverse query：

```
strong_claim_X = "Recraft V4 默认输出 SVG，logo 选 type 时唯一选项"

preflight_reverses:
  "[strong claim 关键字]" + "doesn't"
  "[strong claim 关键字]" + "limitation"
  "[strong claim 关键字]" + "honest review"
```

若首轮查询返回 ≥ 1 个独立反驳源 → 该 claim enable，但**强制**在 deliverable 中引用该反向观点。
若反向查询失败 = 网络失败 → 标 `[counter-evidence search failure]`，写入 Gap #X。

## Tool 关键词冲突（v0.2 new）

见 `06-tool-disambig.md`。Lovart.ai vs Lovable.dev 是高风险；写作任何 Lovart claim 前必须先 disambig。

---

## Quota softening (v0.3 new)

**Trigger**: pain search returns **< 5 user voices** after **≥ 3 distinct query attempts**, especially from "soft-chit" communities (r/architecture, r/POD, r/printondemand) where 429 / search-fail frequent.

**Allowed fallback to `[T2.5 industry-analogue]`**:

| Source | Reaccept as | Caveat tag |
|---|---|---|
| Industry publications (Architectural Digest, Dezeen, PrintMag) | T2 | "industry-context not first-person" |
| G2 / Capterra / Trustpilot reviews | T2 | "buyer-side post-friction, single-cohort" |
| YouTube interviews with named practitioners | T2 | "self-reported, transcript verbatim" |
| Conference talk / webinar transcript | T2 | "presented for audience, possibly rehearsed" |
| Smashing Magazine / A List Apart class blog post | T2 | "authored, professional editorial" |

**Rule**: tag explicitly `[T2.5 industry-analogue]`; treat downstream as T2 but with explicit caveat in `Evidence Gaps` row.

---

## Buyer-side voice quota (v0.3 new)

**Rule**: every deliverable must include **≥ 1 quote from buyer / user / consumer perspective** — NOT founder / builder / maker.

Recognized buyer-side signals:
- "I bought X and Y happened"
- "I tried X as a customer / visitor / reader"
- Reviews on G2/Capterra/Trustpilot 
- r/[product consumer] (customers, not builders)
- Twitter / LinkedIn complaint or praise from outside the maker community

Why: founder voice carries severe selection bias (people who finished building). User voice closer to real friction in field.

**If buyer-side quota can't be met**: write deliverable as `voice: builder-perspective only (no buyer-side voice)` + add Gap #N9.

---

## Authoritative-voice auto-detect (v0.3 new)

Each section. Grep ≥ 25-word sentences containing:

```
must / never / always / every / best / worst / obviously / simply /
everyone knows / the truth is / any expert will tell you
```

**combined with action verb**: `use`, `do`, `ship`, `deploy`, `must do`, `should`, `is to`.

**Auto-cut flag** if found without T2 multi-source backing. Rephrase as prescription / synthesis.

Example:
- ❌ auto-cut: "The best way to start a brand campaign is to always generate 30 design variants first." (no T2)
- ✅ rewrite: "One approach several teams describe as working: generating 30 variants before listing. We've also seen W fail when…" (prescription with multi-voice)



## 自吹帖鉴别器（强制）

可疑信号 ≥ 1 → 标 `[filtered]` 或弃用：

- 文末 / footer 含 affiliate link（"\[affi\]", "💰", "here's the link"、"yes it's affiliate"）
- `[TOOL]` 是 subreddit 名本身（如 `r/RecraftOfficial`）
- "Built in N minutes" + N < 60
- 单一 1–10 评分无方法论
- Author 只在该工具 subreddit 活动
- 文末"Here is / Try free"等转化 CTA 多于 3 次

## 真痛点的判定

≥ 3 条命中才算：

- **具体时刻** — "升级到 Pro 后我失去了 X"
- **具体 artifact** — "团队等了 3 天"
- **情绪残存** — "this pissed me off" / "I honestly regret..."（编辑器没删的）
- **建议 mitigation** — 痛后尝试的 workaround（往往最高信号）

半 quote 没具体 = marketing copy。**丢**。

## 跨工具连续性检查

发现某工具一次出现 ≥ 2 条强痛 → 进 Tier 2 deep audit：
```
"[TOOL] + quit / canceled / churn"
"[TOOL] + refund"
"[TOOL] + switched to"
```

记录每个工具被抱怨的频次 / 类别 → 写入 deliverable 的 "voice-of-user" 表格。

## Lovart.ai-specific note（v0.1 已知 Gap）

搜 "Lovart" 大量返回 **Lovable.dev**（不同产品）。  
**必须手动过滤**：

- URL 含 `lovable.dev` / `lovable.app` → Lovable.dev（弃）
- URL 含 `lovart.ai` / `insights.lovart.ai` / Reddit `r/LovartAIOfficial` → Lovart.ai（保留）

如搜不出 ≥ 5 条 Lovart.ai 真实用户原话 → **降级到 "absence of public Reddit voice" 标签**，写入 Evidence Gaps。
