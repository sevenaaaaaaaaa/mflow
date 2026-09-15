---
sample_id: i18n-ja-bad-001
verdict: bad
content_type: i18n
language: ja
focus_query: ai ロゴ ジェネレーター
rubric_score: 38
block_triggered: yes
dimension_scores:
  reader_scenario: 6
  serp_intent: 7
  information_density: 5
  evidence_trust: 5
  conversion_next: 4
  structure: 5
  anti_slop_language: 4
  localization: 2
  completeness: 5
preflight:
  pass: false
  codes: [AS_BANNED_PHRASE]
reusable_pattern: null
anti_patterns:
  - Chinese sentence order in Japanese
  - EN title structure kept (Unlock seamless...)
  - FAQ copied from EN without local objections
  - CTA is literal translation of "Get started"
  - No local search term in title
source: internal_synthetic
tags: [i18n, ja, translation-slop, BLOCK]
---

# Sample: Japanese localization slop (bad)

## Excerpt

> **Title（坏）**: Unlock seamless AI logo generation — 今すぐ始める
>
> **Hero（坏）**  
> ビジネス名を入力して、AIはあなたのブランドのためのロゴを生成します。これは非常に簡単で、誰でも使えます。
>
> （中文语序直译感：「输入商业名称，AI 为你的品牌生成 logo」）
>
> **FAQ（坏）**  
> Q: Is commercial use allowed?  
> A: Please check our terms.

## Why this verdict

| Dimension | Score | Note |
|---|---:|---|
| Localization | 2 | EN headline + 中文式语序 + EN FAQ |
| SERP intent | 7 | Japanese users search 「AI ロゴ メーカー」「商用利用」— not addressed |
| Conversion | 4 | CTA/title not rewritten for local hesitation |

**BLOCK (i18n Rubric)**: 日语明显中文语序；FAQ 未本地化。

## Reuse for Lovart

- **Fix pattern**: Rewrite title to local query; FAQ on 商用利用・編集・ファイル形式; hero with 入力→出力 in natural Japanese.
- **Ledger**: Fill i18n Ledger `Local query / term` column before batch ja.

## Related

- i18n Ledger: Content-Production-Ledger.md §5
- Pair with: `tool-en-gold-001` (rewrite ja from structure, not translate)
