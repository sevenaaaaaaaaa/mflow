# Sanity 内容管道 — 模块上手

| 项 | 内容 |
|----|------|
| **适用角色** | 内容工程、SEO 发布 |
| **前置** | `npx sanity login`、`check-sanity-auth.js` PASS |
| **Studio SSOT** | `1-4 Dev/lovart.sanity.studio` |
| **Skill** | `lovart-sanity-publish`、`lovart-sanity-content-publish` |

---

## 工作目录

```bash
cd "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-4 Dev/lovart.sanity.studio"
```

---

## 首次运行

```bash
node scripts/check-sanity-auth.js
npx sanity exec scripts/sync-blog-taxonomy.js --with-user-token
node scripts/convert-features.js --dry-run
node scripts/convert-tools.js --dry-run
```

---

## 每次 import 流程

```
preflight L1 → convert（限定范围）→ preflight NDJSON → import --missing → verify L2
```

```bash
node scripts/preflight-content.js --type blog-md
node scripts/convert.js --lang en --dry-run
node scripts/preflight-content.js --ndjson ~/lovart/import-blog-en-batch01.ndjson
npx sanity dataset import ~/lovart/import-blog-en-batch01.ndjson production --missing
npx sanity exec scripts/verify-blog-publish.js --with-user-token
```

---

## 铁律

- 禁止 `sanity deploy`、`--replace`、改 `schemaTypes/`
- 线上已有 `_id` → patch，不指望二次 import 覆盖（AB-P02/P03）
- 详见 [文档/04-质量治理/Anti-Bugs.md](../04-质量治理/Anti-Bugs.md)

---

## 脚本速查

| 操作 | 脚本 |
|------|------|
| Blog | `convert.js` → `verify-blog-publish.js` |
| Features | `convert-features.js` → `verify-composite.js` |
| Tools | `convert-tools.js` → `verify-composite.js` |
| 单页 | `import-page.js` |
| taxonomy | `sync-blog-taxonomy.js` |

---

## 常见坑

| 坑 | AB-ID |
|----|-------|
| cd 到错误 studio 副本 | AB-E01 |
| token 401 未 API ping | AB-E03 |
| 未来 releaseDate 置顶 | AB-S07 |
