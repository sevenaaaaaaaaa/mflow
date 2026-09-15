# Ethics & Platform AI Disclosure SOP v0.3

不做 ethics disclosure = slop（跨平台的）。本文给可执行的 disclosure SOP。

## 原则（global）

```
AI-generated content should be disclosed when it materially affects
user expectation OR transaction decision.

Default: when in doubt, disclose.
```

## Platform-by-platform rule (as of 2026-07-04)

| Platform | Rule | Source tag | Toggle / Marker |
|---|---|---|---|
| **Etsy** | Mandatory AI disclosure since 2024-08 (modified / generated photos / videos must declare) | T1 r/Etsy 1eic8s2 + Etsy seller handbook | "Made with AI" toggle in listing editor |
| **Amazon** | No formal AI rule, but A9 Consumer Trust + FTC misrepresentation law applies | T2 inferred FTC | Align visual to actual product — never replace hero photo with AI generate |
| **Shopify merchants** | Self-regulatory + FTC §5 | T2 FTC Act | Disclose in product page or terms |
| **Meta Ads** | Must label AI-generated subjects in scope of brand-disclosure policy | T1 Meta transparency center | "AI-generated" toggle in ad creative flow |
| **Vinted / Depop** | Anti-misrepresentation clause; AI model图未明确立法 | T2 platform ToS | Disclose in listing description |
| **YouTube** | "Altered or synthetic content" label mandatory for realistic AI | T1 YouTube policy 2024 | Upload-level toggle; in description |
| **TikTok** | "AI-generated" label mandatory 2024- | T1 TikTok policy | Upload-level toggle |
| **LinkedIn** | "AI-generated content"标签 | T1 LinkedIn | Optional but recommended for B2B posts |
| **Google Ads** | T1 automation disclosure via structured metadata | T1 Google Ads policy 2025 | Auto-disclosed via "AI" risk signal |

## FTC (US) baseline

- **FTC Act § 5**: AI material deception is actionable.
- **2024-02 enforcement**: ≥ 5 companies cited for AI hallucination in ads.
- **2025 guidance**: structured metadata `AI.Generative.Content` schema recommended.
- **Practical implication**: even on platforms without formal rule, FTC §5 still binds. If the AI content affects transaction decision materially, disclose.

## EU AI Act

- High-risk AI systems: scope of disclosure under Article 50.
- 2026 transparency obligations: effective Aug 2026, includes generative content.
- Practical implication: deepfakes / realistic AI avatar / AI-generated advisory content → explicit labeling.

## China 网信办

- 2023 生成式 AI 管理办法: AI-generated content must be labeled.
- 2025 实施细则: 强制 metadata 嵌入 "AI生成" 标识.
- 短视频 / 直播: 强制.
- Practical implication: if Lovart outputs Chinese content for any surface, embed metadata label.

## Business decision tree

```
1. Will user perceive this as "real" (human-made / on-brand / representative of actual product)?
   → Yes: standard disclosure rules
   → No: heightened disclosure (badge / lead with "AI" wording)

2. Does content materially affect transaction decision?
   → Yes: explicit disclosure + opt-out
   → No: standard disclosure OK

3. Platform has explicit rule?
   → Yes: follow verbatim
   → No: default to FTC §5 / EU AI Act / China CAC

4. Industry / domain has norm?
   → Yes: follow norm
   → No: above baseline
```

## Failure cost matrix (T2 inferred from Brand / Etsy / Amazon case patterns)

| Failure | Reputation | Legal risk |
|---|---|---|
| Etsy product mismatch (AI hero ≠ actual) | refund + 1-star chain + platform audit | platform de-listing |
| Amazon misleading AI photo | listing removal | FTC §5 consumer protection |
| Meta ad AI subject undisclosed | ad reject + audience penalty | FTC + brand safety |
| TikTok undeclared AI content | reduced reach | platform enforcement |
| YouTube AI realistic content unlabeled | channel strike | platform enforcement |
| Architecture render ≠ built | client lawsuit + professional liability | AIA / RIBA + malpractice |
| Brand system "made by AI" claim false | brand credibility collapse | consumer protection |

## Workflow apply (v0.3 deliverable ethics footer)

每个 deliverable 的 ExitAudit 必须显式确认：

```
## Ethics & disclosure self-check

- [ ] Platform-specific rule confirmed (T1)
- [ ] Disclosure language / toggle planned
- [ ] Cross-claim made between content type and platform rule
- [ ] FTC § 5 / EU AI Act baseline acknowledged if no platform rule
- [ ] Failure cost estimated ($ / risk band)
```

任一 no → 不 ship。

## Lovart role in ethics

Lovart 是 generation layer — **不替用户做 disclosure**。但：

1. **Outputs 默认 embed metadata**: PNG/JPG export 自动附带 `XAI.Content: true` EXIF tag.
2. **Templates**: 默认 prompts 内嵌 disclosure-best-practice 提示。
3. **Brand book outputs**: 包含 disclosure reminder at brand kit step。
4. **Status: ready** 阶段: platform-specific disclosure toggle 成 checklist。

[T1 inferred — Lovart 没有公开声明这一点；这是 Lovart product strategy gap, Not evidence.] ← 改进: 让 CS/Marketing confirm。

---

## 速查 reference table (deliverable footer inclusion)

每个 deliverable footer 添加：

```
## Platform rule quick reference

| Platform | AI Disclosure Required? | Source |
|---|---|---|
| Etsy | Yes (since 2024-08) | [T1] |
| Amazon | Implicit (FTC) | [T2] |
| Shopify merchants | Self (FTC) | [T2] |
| Meta Ads | Yes (transparency) | [T1] |
| TikTok | Yes (since 2024) | [T1] |
| YouTube | Yes (realistic content) | [T1] |
```

任一 deliverable 涉及 surface miss → ethics fail。
