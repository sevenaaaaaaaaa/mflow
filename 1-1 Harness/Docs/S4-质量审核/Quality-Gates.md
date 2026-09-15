# Quality Gates — 质量门禁（人类可读）

> **执行 SSOT**：`1-1 Harness/Skills/lovart-content-quality-gates/SKILL.md`  
> **脚本 SSOT**：`1-4 Dev/lovart.sanity.studio/scripts/preflight-content.js`

---

## 生命周期

| 阶段 | 层级 | 动作 |
|------|------|------|
| CREATE | L1 | `preflight --type tools\|features\|blog-md` |
| TRANSLATE | L1+L5 | marker 清零、i18n 文件名 |
| PRE-PUBLISH | L1 | `--ndjson ~/lovart/import-*.ndjson` |
| POST-PUBLISH | L2 | `verify-blog-publish` / `verify-composite` |
| DEEP QA | L3 | `lovart-content-audit`、Anti-Slop 人工 |
| 周期 | L1+HTTP | `audit-*` 脚本 |

---

## L1 自动化（preflight）

BLOCK 即不可 import。常用：

```bash
node scripts/preflight-content.js --type tools --strict --sample-urls 5
node scripts/preflight-content.js --type blog-md
```

维度：i18n、JSON 结构、SEO slug、UX placeholder、URL 契约、MD 坏链、**body Portable Text 格式**（AB-LP22）、**structuredData 类型与完整性**（AB-LP23）。

---

## L2 落库抽查

```bash
npx sanity exec scripts/verify-blog-publish.js --with-user-token
npx sanity exec scripts/verify-composite.js --with-user-token -- --type features --sample 20
```

---

## L3 Anti-Slop + 深度审计

- 写作规范：[Anti-Slop.md](./Anti-Slop.md)
- 脚本：`audit-content-quality.js`、`en-readability-backlog.js`
- 未来：SERP alignment gate（见 Insight SERP Copy Intelligence 建议）

---

## L4–L7 摘要

- **L4 URL**：契约路径 + 可选 `--check-urls`
- **L5 i18n**：见 [i18n-多语言.md](../02-模块上手/i18n-多语言.md)
- **L6 代码健康**：convert dry-run、NDJSON 无 `section_` marker
- **L7 合规**：品牌调性、地区敏感表述（人工）

---

## 与 Anti-Bugs 关系

| 机制 | 侧重 |
|------|------|
| Quality Gates | 发布前/后**预防性**检查 |
| Anti-Bugs | 已发生事故的**禁止再犯**登记 |
