# Tool Keyword Disambiguator v0.2

搜工具名时常常撞名 / 撞产品。Pain mining 或写作之前**先 disambig**。

## 高风险冲突表

| 搜索词 | 常见错配 | 风险 | Filter 规则 |
|---|---|---|---|
| **Lovart** | Lovable.dev（瑞典 AI app builder，完全不同产品） | **HIGH** | URL = `lovable.dev`/`lovable.app` 或 r/lovab* 时**全部 drop**；只保留 `lovart.ai`/`r/LovartAIOfficial` |
| Recraft | — | LOW | 标准 |
| Ideogram | — | LOW | 标准 |
| Maginary | — | LOW | 标准 |
| v0 | v0 Vercel vs "v0 prompt template" 通用名 | MEDIUM | URL = v0.dev 才计为 Vercel；否则视为 prompt 元词 |
| Claude Design | Claude Design vs general Claude | MEDIUM | 必须有 "Claude Design" 字面量或 Anthropic Labs 标识 |
| Brand OS | 营销话术，多家厂商都叫这 | MEDIUM | 必须有 attributing vendor；否则视为概念不引 |
| Generative UI | pattern 不是 product | LOW | 仅作概念用 |
| Magic Patterns | Magic Patterns 设计系统工具 vs Magic Patterns 关键词 | LOW | 唯一 mainstream vendor，是 OK |
| Subframe | Subframe 设计工具 vs 其他 Subframe | LOW | 同上 |

## Lovart.ai vs Lovable.dev — 显式判定法

**Lovable.dev 标志**（不是 Lovart.ai）：
- URL 含 `lovable.dev`、`lovable.app`
- 所属 subreddit：`r/Lovable`、`r/lovable`、`r/lovable_dev`
- 定价模式：$20 / $25 / $50 / 100 credits daily/monthly
- 讨论主体："build an app"、"vibe coding"、"make me a todo app"
- 典型投诉："credits ran out"、"AI won't follow commands"、"refund no response"

**Lovart.ai 标志**：
- URL = `lovart.ai`、`insight.lovart.ai`
- Subreddit：`r/LovartAIOfficial`
- 价格：Free / Basic $23-$29 / Pro $58-$72 / Ultimate $157-$196（年/月）
- 讨论主体："design a logo"、"design a brand"、"create a poster"、"social campaign"
- 信用消耗例子："500+ credits for complete brand identity" [T1 searchmytool]

**Rule**：
> Quote Lovable.dev posts as **Lovable.dev**, NEVER as "Lovart". Fall back to **Gap** if no Lovart.ai-specific voice found.

## 自动 disambig at query time（前置 query）

写 tool claim 之前先跑 3 条 disambig query：

```
"[TOOL]" site:reddit.com
"[TOOL]" pricing 2026
"[TOOL] vs [competitor]" 2026
```

读 3 capture 中至少 1 条的 URL / 价格 / framing。
任一不匹配预期产品 → 标 `[Filtered — disambiguation]`。

## 双品牌场景的特殊处理

用户问题涉及"AI design agent / design canvas"赛道时，搜出大量 Lovable.dev 是常态（更热）。如果目标产品 = Lovart.ai：

1. **先**搜 `Lovart AI design agent`（带 "AI design agent" 同现词限缩）
2. **若仍无结果** → 标 `[no direct Lovart.ai voice found]`
3. **不要**借 Lovable.dev 例子 "类比推断"Lovart.ai 痛点。Lovable ≠ Lovart，引用为 Lovart 痛点是 fabrication。

## 自检问题

每个 deliverable 出题前 ask：

1. 这条 claim 提到哪个工具/品牌？
2. 该词是否在 disambig 表中存在？
3. 如果存在，过滤规则是否应用？
4. 如果过滤后 voice < 5 条 → 是否进 Gap 而不是引用？

**违反任何一条 → pause + 显式声明 gap，不前进。**
