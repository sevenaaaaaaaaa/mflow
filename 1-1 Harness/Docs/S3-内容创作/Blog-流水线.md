---
type: stage-sop/s3
version: 1.0
updated: 2026-07-05
scope: "profile-lovart-creation"
tools: [opencode, claude]
status: active
path: 1-1 Harness/Docs/S3-内容创作/Blog-流水线.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Blog 流水线 — 模块上手

| 项 | 内容 |
|----|------|
| **适用角色** | 内容策略、SEO、编辑 |
| **内容源** | `1-3 Content Gen/Content Calendar/`、`Lovart-Blog-Pipeline/` |
| **脚本 SSOT** | `convert.js`、`verify-blog-publish.js`、`patch-blog-*.js` |
| **Skill** | `lovart-blog-automation`、`lovart-sanity-publish` |

---

## 最小流程

```
Content Calendar MD → preflight blog-md → convert.js → NDJSON preflight → import --missing → verify
```

```bash
cd "1-4 Dev/lovart.sanity.studio"
node scripts/preflight-content.js --type blog-md
node scripts/convert.js --lang en --dry-run
npx sanity dataset import ~/lovart/import-blog-en-batch01.ndjson production --missing
npx sanity exec scripts/verify-blog-publish.js --with-user-token
```

---

## 发布后审计

```bash
node scripts/audit-blog-covers.js --check-http
node scripts/audit-blog-future-release-dates.js
node scripts/audit-content-quality.js
```

---

## 验收

- `releaseDate` 无未来日期（AB-S07，`clampReleaseDate`）
- 封面非 liblib 或已 `--only-broken` patch（AB-I08）
- 无 IMAGE PLACEHOLDER 进正文（AB-S01）

---

## 写作质量

- [Anti-Slop.md](../04-质量治理/Anti-Slop.md)
- Skill：`lovart-content-writer.md`

---

## 常见坑

| 坑 | AB-ID |
|----|-------|
| 全量换封面 | AB-P01 |
| Content Calendar 未来 date | AB-S07 |
| 坏内链 `/cluster/` | preflight `MD_LINK` |
