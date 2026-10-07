# Category-Specific Anti-Slop Triggers v0.3

每类的 anti-slop trigger 不同。通用 `04-voice-rules.md` 不够。本文件按 category 给硬 trigger 列表。

## SaaS UI 类（Mantlr 7-pattern 衍生 + Devian + real founder pain）

| Trigger（出现即 reject） | 来源 |
|---|---|
| Top-left = logo 或 装饰图（非可操作 KPI） | Mantlr Pattern 1 actionable-first [T2] |
| 12+ KPI tiles on main view | Mantlr Pattern 7 density [T2] |
| Empty state = "Welcome! Click here to add your…" | r/SaaS rywswo 量化的 step 1→2 drop [T2] |
| Pricing = 5+ tiers | Gogochimp [T2] 30% penalty vs 3-tier |
| Setup flow ≥ 15 min before value | r/SaaS qoawys [T2] |
| Email verification = gate（before value delivery） | r/indiehackers pmzg1g 60% drop data [T2] |
| 12-step product tour | r/SaaS rywswo [T2] |
| ≥ 1 multi-step flow without "Step 2 of 4" indicator | r/SaaS rywswo 1/3 abandonment reduction [T2] |
| Onboarding ends without "first meaningful action" | r/Entrepreneur qi5rvc [T2] |
| Sample data = blank | cross-cite [T2] |

## Brand / Logo 类（r/nocode 5 fingerprints + Michal Malewicz manifesto + Brainy paper）

| Trigger | 来源 |
|---|---|
| Default = purple/blue gradient stack | r/nocode + Eidos Design [T2 cross] |
| Pillow buttons on every CTA | same [T2] |
| Container-in-container nesting (≥ 3 levels) | r/nocode [T2] |
| Decorative emoji wrapping plain copy | r/nocode [T2] |
| Vertical stacking as default composition | r/nocode [T2] |
| Wordmark default Inter / Geometric Sans 没改 | Brainy paper [T2] |
| Round corners in cascade (parent-child same radius) | r/nocode [T2] |
| "Generic globe / lightning / handshake" 符号 | LogoDesignValley 2026 [T2] depletion list |
| AI-generated logo 没 disclose | r/artificial designer rejection [T3 dissent] |
| Ultra-thin (100/200) wordmark | Lucky Graphics 2026 [T2 trend out] |

## Social Media 类（r/FacebookAds + Pipeline Monk + DoWhatWorks）

| Trigger | 来源 |
|---|---|
| Hero 1 of 5 fixed templates | r/nocode 5 hero fingerprint [T2] (cross-cite) |
| Same ad running 30+ days | r/FacebookAds 1r67bvt [T2] |
| AI verbiage in hero header | DoWhatWorks [T2] top brands repeatedly 输 |
| "One perfect creative" workflow | r/FacebookAds 1r67bvt [T2] anti-pattern |
| UGC videos no refresh for 7-10 days | r/FacebookAds 1kr3t72 [T2] |
| Same 3 creatives from 6 months ago | r/FacebookAds 1r67bvt [T2] |
| Catalog ads "no creative refresh schedule" | r/FacebookAds 1r3ezx1 [T2] |
| Container stacking cascade | r/nocode [T2] |
| Emoji-as-design-element in copy | r/nocode [T2] |

## Advertising 类（Pipeline Monk + DoWhatWorks + Prompt Engines Lab）

| Trigger | 来源 |
|---|---|
| AI in hero header (not subhead) | DoWhatWorks [T2] 明证 heads 输 |
| Frame "AI assistant for X" without unique value | DoWhatWorks [T2] GoDaddy case |
| Visual-only variants (no copy framework shift) | Prompt Engines Lab [T2] |
| Single-test decisions (no statistical plan) | aitoolsguidebook [T2] |
| Test < 1000 visitors/variant | Pipeline Monk [T2] statistical baseline |
| Same image copy < 5 variants in batch | DoWhatWorks / Pipeline Monk [T2] |
| Feature tour > 1 step in ad creative | SaaS ad convention [T2 inferred] |
| Unrealistic numbers in copy（"+500% conversion" no source） | Eidos Design + Brainy [T2] |
| "Loved by 10M+" without traceability | Brainy paper [T2] |

## E-commerce Listing 类（r/Etsy + r/Entrepreneur + ethics)

| Trigger | 来源 |
|---|---|
| AI-generated 主图 replace 实拍 | r/Etsy 1t5n5os "85-90% don't match" [T2] |
| AI disclosure missing | r/Etsy 1eic8s2 [T1 Etsy policy] |
| Hero imagery 在 zoom 下融化 | r/Etsy 1qgktjg cord disappears [T2] |
| Dropshipping cover-up with AI model | r/GirlGamers 1r40wee [T2] |
| Returns policy 在 footer 反 show | r/micro_saas 1rbwef9 [T2] explicit "kill conversion" |
| Lifestyle hero ≠ actual product texture | r/Etsy 1t5n5os [T2] |
| Misleading fabric/cord details | r/Etsy 1qgktjg [T2] |
| Amazon listing without actual photo | r/Entrepreneur 1r2dfka [T2] |
| AI model generate (no parallel实拍) | r/Entrepreneur 1r2dfka [T2] |
| Platform 立法时候 hide AI use | r/Etsy 1eic8s2 [T1] violation |

## Print on Demand 类（r/Etsy + Trendlytic + POD specifics）

| Trigger | 来源 |
|---|---|
| Same design across mockups 看起来 inconsistent | implied from Etsy 1qgktjg [T2] |
| Mockup ≠ actual print color/texture | r/Etsy 1t5n5os [T2] reused |
| Bulk design w/o niche specificity | Trendlytic [T1] - generic = 0 sell |
| Generic globe / lightning cliché | shared brand anti-pattern [T2] |
| 30-design batch but quality drift within | Recraft V4 cross-cite [T2] |
| Uniform style, but no token lock | Recraft V4 brand kit [T2] |
| AI disclosure 没 declare | r/Etsy 1eic8s2 [T1] cross-platform |

## Architecture & Interior 类（nuit.archi pattern + mnml.ai review + Veras）

| Trigger | 来源 |
|---|---|
| "AI replaces architect" claim | nuit.archi explicit "documentation stays traditional" [T1] |
| Midjourney 非-arch context | nuit.archi tier 4 photo-restyle marginal [T1] |
| Plant / 水 / 大气 lighting claim as "solved" | nuit.archi "through 2027 ... improvement ongoing" [T1] |
| Geometry flexibility without BIM integration | mnml.ai review "no native plugin" [T2] |
| Single AI render vs multi-tool stack | nuit.archi explicit "2-3 tools" [T1] |
| Hero claim of <$100/mo工具 stack | many practitioners [T2] vs nuit $100-400 |
| Architectural Digest / Dezeen cite without verification | industry convention [T2 implicit] |

---

## Category × Trigger 检验 checklist

每个 deliverable 出稿前：

```
[ ] Walk through applicable triggers for THIS category
[ ] Check each applicable trigger against the deliverable
[ ] Mark each [PASS / FAIL / N/A] explicitly in the deliverable's anti-slop gate table
```

Failure → 重做对应 section。

---

## 触发 trigger 来源标注

每个 trigger 必带 `[T1/T2/T3]` 来源标注。  
**未标注 trigger = 未验证抗 slop 假设，禁止用于 deliverable**。
