## Lovart.ai 内容生产数据总结

**数据来源**：Sanity `o11tm2qe.production` GROQ 直接查询 | **快照**：2026-07-10

---

### 一、Sanity 总存量

| 维度 | 数量 |
|------|------|
| 全类型发布文档（含多语言） | 20,237 |
| Blog 发布总计 | 10,686 |
| Blog EN 唯一 slug | 1,552 |
| CompositePage 发布总计 | 8,536 |
| CompositePage EN 唯一 slug | 1,059 |

**Blog 各语言分布**：EN 1,552 / ZH 960 / IT 941 / PT 924 / RU 924 / JA 911 / ZH-TW 910 / DE 893 / FR 893 / KO 893

**CompositePage 各语言分布**：EN 1,059 / ZH 851 / JA 851 / ZH-TW 848 / KO 833 / DE 831 / PT 821 / RU 819 / FR 823 / IT 810

**CompositePage 分类（全语言）**：tools 4,590 / features 2,230 / topics 920 / scenarios 700 / solutions 100 / products 2 / landing 4

---

### 二、近 30 天日均新增（2026-06-10 → 07-10）

| 类型 | 30天累计 | 日历日均 | 实际模式 |
|------|---------|---------|---------|
| Blog EN slug | 420 篇 | **14/天** | 批量爆发（6/14单日197），非平滑 |
| Blog 全语言 | 1,500 篇 | **50/天** | 同上 |
| Composite EN slug | 632 页 | **21/天** | 6/14(377)+6/30(179)两波，其他天0 |
| Composite 全语言 | 5,793 页 | **193/天** | 同上，6月上中旬集中 |
| **合计文档(全语言)** | **~8,300** | **~278/天** | — |

6月是超级生产月（Blog EN 435 篇），7月至今 10 天已生产 23 篇 EN Blog + 约 200-300 页 Composite。

---

### 三、QA 执行情况

| QA 环节 | 范围 | 状态 | 问题 |
|---------|------|------|------|
| **Backdate 修复** | 10,694/10,695 Blog 已设 publishedAt | ✅ 99.99% | 1 篇残留 |
| **全量更新扫描** | 所有 Blog 和 Composite 在 7/3-10 期间被 patch | ✅ 已执行 | — |
| **图片 404 检测** | 1,055 页 composite 扫描（7/1） | ⚠️ **44% broken** | 239 页 / 1,850 张 persist CDN 403 |
| **Blog cover 检测** | 全量 | ⚠️ **16 篇 broken** | liblibai 图源已挂，全为 zh 语言 |
| **Anti-Slop 深度检测** | 3 篇 actionable | ⚠️ 待扩量 | ai-image-editor-touch-edit, ai-video-generator-review, best-image-to-video-tools |
| **Landing preflight** | 48 个样例 | ✅ 全部通过 | — |
| **Priority Landing QA** | 4 页 | ✅ 通过 | — |
| **Slop 浅层扫描** | loose 45 / pattern 47 | 多数为模板残留 | 需全自动管线 |

---

### 四、QA 整体工作流（6 层管线）

```
1. 情报输入     → GSC / SERP / Sentinel / GitHub Trending
2. 内容生产     → Blog (signal-writer) + Landing (page-serp-writer) + i18n + Image
3. 写中质量     → Anti-Slop 4W + Ledger 密度 + Shrinkage 30/40/30
4. 发布前门禁   → preflight + anti-slop-preflight (21种BLOCK码) +置顶保护
5. 发布执行     → Sanity --missing + IndexNow + 中国爬虫 + 30s自检
6. 上线后监控   → 周度 image audit / 内容健康 / GSC窗口 / Anti-Bugs Registry
```

**独立 CRO 层**：BOFU 内容矩阵（20+转化/留存文章），CTA 设计系统（6 类型 × 10 分类），OKR 追踪转化率

**涉及 Skills（15+）**：`lovart-blog-signal-writer` / `lovart-page-serp-writer` / `lovart-i18n-pipeline` / `lovart-existing-page-rewriting` / `lovart-anti-slop` / `lovart-content-quality-gates` / `lovart-image-generation` / `lovart-seo-reporting` / `lovart-landing-image-audit` 等

---

### 五、关键 URL

| 资源 | 地址 |
|------|------|
| Sanity Studio | `https://lovart-wp-headless.sanity.studio/` |
| Sanity API 项目 | `o11tm2qe.api.sanity.io` (dataset: production) |
| Live site (EN) | `https://lovart.ai/` |
| Live blog | `https://blogs.lovart.ai/` |
| Sanity 配置 | `~/.config/sanity/config.json` |
| Content ledger | MFlow `1-1 Harness/Docs/S4-质量审核/Content-Production-Ledger.md` |
| Anti-Bugs Registry | MFlow `1-1 Harness/Docs/S4-质量审核/Anti-Bugs.md` |
| Anti-Slop 规范 | MFlow `1-1 Harness/Docs/S4-质量审核/Anti-Slop.md` |
| Slop 门禁码表 | MFlow `1-1 Harness/Docs/S4-质量审核/Preflight-Anti-Slop-Gates.md` |

---

**一句话总结**：30 天产出了 1,500 篇 Blog + 5,793 页 Landing（含多语言），日均 ~278 文档；QA 门禁覆盖 6 层管线，但图片 44% broken 是当前最大未解决风险。