# Sanity 内容管道 ↔ 前端 `apps/品牌` 边界

> **Canonical**：说明本 vault **不包含**主站前端 repo，接手人应如何理解发布与渲染的关系。

---

## 三个目录，三种角色

| 目录 | 在 vault 内？ | 角色 | 内容 Agent |
|------|--------------|------|------------|
| **`dev/品牌.sanity.studio/`** | ✅ | Blog/Features/Tools **convert · import** cwd | ✅ 在此跑脚本 |
| **`dev/品牌.sanity.studio/`** | ✅（schema 镜像） | 线上 Studio **schema / deskStructure** 参照 | ❌ 勿 `sanity deploy`（除非 schema 团队授权） |
| **`apps/品牌/`**（monorepo） | ❌ **不在本 vault** | **example.com 主站** Next.js 渲染、GROQ、Portable Text | ❌ 无法在本交接包内改前端 |

---

## 线上地址

| 类型 | URL |
|------|-----|
| Studio | https://品牌.sanity.studio |
| Blog | `https://www.example.com/{lang}/blog/{slug}` |
| Features | `https://www.example.com/{lang}/features/{slug}` |
| Tools | `https://www.example.com/{lang}/tools/{slug}` |
| Dataset | `production` @ project `your-project-id` |

---

## 内容发布能验证什么 / 不能验证什么

| ✅ 本包可验证 | ❌ 需前端 repo |
|--------------|-------------|
| GROQ 文档存在、字段、category ref | 页面实际 HTML/CSS 渲染 |
| `verify-blog-publish.js` / `verify-composite.js` | PortableText 组件对 `table` / `compositePage` 块的支持 |
| Studio 抽查文档 | Presentation 多语言预览是否串稿 |
| preflight URL 抽样 HTTP 200 | hreflang、sitemap、draft mode |

---

## 接手人如何取得前端仓库

1. 向 **品牌方 前端 / 平台负责人** 申请 `apps/品牌`（或含该目录的 monorepo）只读权限  
2. 本地 clone 后重点文件（名称以实际 repo 为准）：  
   - Blog 列表/详情 GROQ  
   - `PortableText` / `compositePage` 渲染  
   - `i18n/locales.ts` 与路由中间件  
3. **不要**假设 vault 内 `CLAUDE.md` 与线上一致 — 以 clone 后的 repo 为准

---

## 与 Sanity 发布的关系

```
本 vault：MD/JSON → convert → import --missing → production
                                    ↓
前端 repo：production → GROQ → example.com 页面（vault 外）
```

内容管道 **只写 production 数据**；页面样式、路由 bug、locale 404 需在前端 repo 排查。

---

## 相关文档

- [`SOP-品牌方-Sanity-Blog-Features-Tools-换设备交接与首次运行.md`](./SOP-品牌方-Sanity-Blog-Features-Tools-换设备交接与首次运行.md) §6 双 Studio  
- [`MFLOW-SANITY-BACKLOG.md`](../../../dev/品牌.sanity.studio/MFLOW-SANITY-BACKLOG.md) 阶段 4  
- [`sanity-es-language-policy.md`](./sanity-es-language-policy.md) — locale 不一致案例
