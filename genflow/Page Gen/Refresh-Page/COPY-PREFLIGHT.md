---
type: checklist
version: 1.0
updated: 2026-07-05
scope:
  - tool
  - feature
  - product
  - solution
  - scenario
  - topic
  - landing
---

# Copy Preflight

> 这是页面生成链路的轻量文案验收清单。  
> 它不替代结构校验，也不替代 `preflight-content.js`；它只回答一件事：这页的 copy 能不能说明白、能不能转化、会不会重新滑回泛 AI 文案。

## 使用顺序

1. 先做 `PAGE-BRIEF`
2. 选故事线后，先跑 schema 校验，确认故事线绑定本身没漂移
3. 再按 `landing-copy-constraints-ssot.md` 生成 copy
4. 输出前走本清单
5. 过不了时，优先改 page promise / Hero / proof / CTA / FAQ

```bash
node "genflow/Page Gen/Refresh-Page/scripts/validate-storyline-schema.js"
```

---

## P0 阻断项

任一命中即不可交付：

- Hero 没有清楚说出这页卖什么
- Hero 缺少 input 或 output
- 页面没有可见 proof，只剩 slogan / logo wall
- 没有底部 CTA
- FAQ 少于 3 条，或全是弱问题
- 出现无来源数字 / 编造社会证明 / 编造 rights
- 页面类型与 Hero 主语冲突

---

## P1 核心检查

### 1. 一句话承诺

- 是否一句话就能说清这页承诺什么？
- 这句话是否属于这个页面类型，而不是别的类型？

### 2. Hero

- 是否写明主语？
- 是否写明 input？
- 是否写明 output？
- 是否写明 risk reducer？
- 是否知道买家是谁？

### 3. Proof

- 是否至少出现一类强 proof？
- deliverable / workflow / format / rights / before-after / testimonial / limitation 是否可见？
- 有没有只放 logo 但没有解释真实价值？

### 4. CTA

- CTA 是否匹配流量阶段？
- 冷流量是否足够降风险？
- 对比页是否强调切换理由？
- offer 页是否强调 why now？

### 5. FAQ

- 是否回答真实异议，而不是定义题？
- 是否覆盖商用、格式、编辑路径、适用边界、相邻页差异？

---

## 页面类型附加检查

### `tool`

- 是否先卖具体 job？
- 是否给了试用 / prompt start path？

### `feature`

- 是否只解决一个明确 friction？
- 是否写出生成后的控制能力？

### `product`

- 是否解释它在 Lovart 栈中的位置？
- 是否带出协作 / 治理 / 长期价值？

### `solution`

- 是否先卖团队问题，再卖 feature？
- 是否写出 throughput / handoff / governance？

### `scenario`

- Hero 主语是否是角色 / 行业 / 场景？
- 是否避免写成产品总览？

### `topic`

- 是否提供决策框架？
- 是否帮助读者理解“何时适合 Lovart”？

### `landing`

- 是否与具体故事线意图一致？
- trial / competitor / trust / offer 的 CTA 逻辑是否区分开？

---

## 禁用信号

看到这些要立即回改：

- `unlock`, `revolutionize`, `game-changer`, `streamline`, `empower`, `seamless`
- “AI-powered creativity for everyone” 一类空句
- “trusted by creators” 但没有 deliverable / workflow / proof
- 所有页面复用一条 CTA
- FAQ 写成百科词条

---

## 脚本化实现（storyline-driven）

脚本分两层：

- `scripts/validate-storyline-schema.js` — 校验故事线 SSOT / copy 绑定 schema，适合改故事线前后运行
- `scripts/lib/landing-copy-rules.js`

### 1. Storyline Schema 校验

`validate-storyline-schema.js` 会检查：

- 4 个 SSOT JSON 是否可解析
- `masterIntents` 与 `croStageByIntent` 是否一一覆盖
- `intentCrosswalk` 是否只引用合法 intent
- `copy` / `copyDefault` 是否包含必填字段
- `ctaStyle` / `benchmarkPool` 是否在允许枚举内
- `requiredSections` 是否真实存在于该故事线的 `sections`
- `proofTypes` 是否至少命中一个真实 section
- `heroType` 是否与首段 section 一致
- `sectionCount` 是否等于 `sections.length`
- legacy alias 是否指向存在的故事线

### 2. 页面 Copy Preflight

**校验规则从故事线绑定派生**，不再硬编码。lib 启动时把四个 SSOT 合成一个 `storylineId → copy 绑定` 注册表：

- `landing-storylines.json`（每条 storyline 内嵌 `copy`）
- `solution-storylines.json` / `scenarios-storylines.json`（文件级 `copyDefault`）
- `page-copy-bindings.json`（feature / tool / product / topic）

给定一页的 `storylineId`，脚本按其绑定检查：

- Hero 是否覆盖该故事线 `heroMust` 里的 input / output（缺 = BLOCK；缺 editPath/riskReducer = warning）
- 是否存在该故事线 `proofTypes` 中的任一强 proof
- FAQ 是否至少 3 条
- 是否存在底部 CTA
- 是否包含该故事线 `requiredSections`（如 trial→`prompt-launcher`、vs→`comparison-before-after`、offer→`pricing-block`+`review`、product→`pricing-block`+`tool-grid`）
- 是否命中禁用词候选

CTA 文案风格也由绑定的 `ctaStyle` 派生（trial / compare / brand / offer / solution / educate / default）。

> 因此“新增/调整某故事线的文案要求”只需改故事线绑定，脚本与文档自动跟随，不会再出现故事线与文案层各自漂移。
