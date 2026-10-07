---
type: audit
version: 1.0
updated: 2026-07-05
scope:
  - landing-examples
  - keyword-landing-examples
---

# Copy Preflight Audit 2026-07-05

## 抽样范围

### Landing examples（7/7）

- `draft-lovart-shopify-growth-landing-gallery-detail-en.json`
- `draft-lovart-creative-studio-landing-gallery-funnel-en.json`
- `draft-lovart-brand-campaign-landing-brand-trust-en.json`
- `draft-lovart-tool-trial-landing-trial-now-en.json`
- `draft-lovart-competitor-alt-landing-vs-competitor-en.json`
- `draft-lovart-promo-retarget-landing-offer-close-en.json`
- `draft-lovart-platform-landing-full-en.json`

### Keyword landing examples（41/41）

- 来源：`landing-examples/keyword-manifest.json`

## 审计口径

使用 `scripts/lib/landing-copy-rules.js` 中的 `validateLandingCopyPreflight()` 检查：

- Hero 是否包含 input / output
- 是否存在 proof section
- FAQ 是否至少 3 条
- 是否存在底部 CTA
- `landing-trial-now` / `landing-full` 是否包含 `prompt-launcher`
- 是否命中禁用词候选

## 结果

### Landing examples

- 通过：7 / 7
- 错误：0
- 警告：0

### Keyword landing examples

- 通过：41 / 41
- 错误：0
- 警告：0

## 结论

当前 `generate-landing-examples.js` 与 `generate-keyword-landing-examples.js` 已接入最小 copy preflight，且重生成后的本地样例均通过。

## 后续建议

- 下一轮可把 `product / solution / scenario / topic` 的现网页也纳入同一套 preflight 抽样
- 若后续出现假 proof 或 Hero 空话，优先扩展 `landing-copy-rules.js`，不要回到手工口头约束
