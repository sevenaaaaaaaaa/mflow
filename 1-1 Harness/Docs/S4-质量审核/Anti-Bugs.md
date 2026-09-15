# Anti-Bugs — 发布事故防护

> **SSOT**：[ANTI-BUGS-REGISTRY.md](../../ANTI-BUGS-REGISTRY.md)（全量 AB-* 条目）  
> **Agent 摘要**：[AGENTS.md Part B7](../../AGENTS.md#b7-内容-anti-bugs强制)

---

## 是什么

Anti-Bugs 记录 production 上已发生、且可能复发的问题。每条含：**症状 → 根因 → 禁止 → 正确 → 验收**。

不是单元测试框架，而是**操作纪律 + 审计脚本 + Registry 登记**。

---

## 发布前最小验收

- [ ] `node scripts/check-sanity-auth.js`
- [ ] `preflight-content.js` BLOCK=0
- [ ] patch/import 已 `--dry-run`
- [ ] `audit-blog-covers` / `audit-composite-images-404` → 0 broken
- [ ] `audit-blog-future-release-dates` → 0（AB-S07）

详见 [定期任务/01-发布后必做.md](../../定期任务/01-发布后必做.md)。

---

## 高频 AB-ID

| ID | 场景 |
|----|------|
| AB-P02 | 线上已有仍全量 import |
| AB-P03 | 只改 convert 指望线上变 |
| AB-I01 | 404 URL 模糊匹配换图 |
| AB-S07 | 未来 releaseDate 污染排序 |
| AB-E03 | token 未 API ping |

---

## 守门脚本（Geo Dev）

```bash
cd "1-4 Dev/lovart.sanity.studio"
node scripts/audit-blog-future-release-dates.js
node scripts/audit-blog-covers.js --check-http
node scripts/audit-composite-images-404.js
```

新 Bug：production 修复后 **24h 内**登记 AB-*（Registry 附录 D）。

---

## Skill 交叉引用

各 publish/audit Skill 的 `## Anti-Bugs` 小节链接回本 Registry，勿在 Skill 内重复全文。
