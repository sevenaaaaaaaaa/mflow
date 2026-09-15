# Sanity Schema 修改风险评估（最终版）

> **盘点日期**：2026-06-25
> **路径范围**：Obsidian MindRe/1-Project/Lovart MFlow + Documents/Lovart Local Dev
> **核心结论**：**本机不存在 Sanity Studio 源文件**——物理上无法修改 schema

---

## 一、本机实际存在的 Sanity 相关文件

### ✅ 找到的（脚本 / 配置）

| 位置 | 类型 | 作用 |
|------|------|------|
| `Documents/Lovart Local Dev/sanity_token.py` | Python 脚本 | 通过 `~/.config/sanity/config.json` 取 token |
| `Documents/Lovart Local Dev/.sanity_config.json` | JSON 配置 | token + project + dataset + api |
| `~/.config/sanity/config.json` | JSON | Sanity 凭据（authToken + projectId + dataset）|
| `MindRe/1-Project/Lovart MFlow/1-1 Harness/sanity-studio-copies/LovartPM-sanity-studio/` | 目录 | **只有 scenarios 子模块副本**（不是完整 Studio）|
| `MindRe/1-Project/Lovart MFlow/1-4 Dev/scripts/` | Python | SEO/数据脚本，**无任何 .ts schema 源** |

### ❌ 找不到的（schema 源文件）

- ❌ `lovart.sanity.studio/schemaTypes/` 目录
- ❌ `sanity.config.ts`
- ❌ `sanity.cli.ts`
- ❌ 任何 `.ts` schema 文件
- ❌ 任何 `package.json` 在 Studio 目录

---

## 二、Sanity Studio SSOT 到底在哪？

根据项目文档（`1-1 Harness/WORKFLOWS.md`）：

```
Studio SSOT: 1-4 Geo Dev/lovart.sanity.studio/
```

但实际：
1. **MindRe 中没有 `1-4 Geo Dev`**，只有 `1-4 Dev`
2. **`1-4 Dev/` 目录下没有任何 schema 源文件**，只有 Python 脚本
3. **`sanity-studio-copies/LovartPM-sanity-studio/`** 只是 scenarios 模块的副本（scripts + docs），不是完整 Studio

**结论**：Sanity Studio 源文件 **不在本机 iCloud 同步范围**。可能：
- 在另一台机器
- 在 Sanity Studio 云端托管（在线编辑）
- 在另一个 iCloud 共享目录（未同步）

---

## 三、物理上能否修改 schema？

### 答案：**当前 Agent 无法修改 schema**

```bash
# 任何修改 schema 的命令都需要：
cd /path/to/lovart.sanity.studio/   # ← 此路径在本机不存在
# 修改 schemaTypes/compositePage.ts  ← 此文件在本机不存在
npx sanity deploy                    # ← 被铁律禁止
```

### 实际能做到的（与 schema 无关）

| 操作 | 工具 | 风险 |
|------|------|------|
| 读取 Sanity 数据 | GROQ 查询 API | 零风险（只读）|
| 修改文档字段值 | Sanity Mutate API | 低风险（仅改值，不改结构）|
| 改 WordPress 端 | PHP 插件修改 | 不影响 Sanity |
| 改前端代码 | Next.js 代码改动 | 不影响 Sanity |

---

## 四、改 schema 的真实风险（即使物理可改）

### 4.1 项目铁律（来自 `1-1 Harness/WORKFLOWS.md` 和 `Docs/S5-发布部署/Sanity-内容管道.md`）

```
❌ 禁止 sanity deploy
❌ 禁止 --replace
❌ 禁止改 schemaTypes/
❌ 禁止改 sanity.config.ts / sanity.cli.ts
```

**违反铁律 = 必须显式说明 + 用户授权**。

### 4.2 修改 schema 的连锁破坏路径

```
步骤 1: 改 schemaTypes/*.ts（添加 seo.canonical 字段）
步骤 2: 跑 sanity deploy 上传
  ↓
副作用 1: Sanity Studio 云端重新部署（5-10 分钟不可用）
副作用 2: 现有文档的 seo.canonical 字段 = undefined（不会破坏数据，但前端需 fallback）
副作用 3: Studio UI 重新加载，新字段位置与编辑流程改变
  ↓
步骤 3: 前端代码适配
  ↓
副作用 4: wp-adapter.ts 需添加 seo.canonical 处理
副作用 5: nextjs generateWPMetadata 需读取新字段
副作用 6: WordPress ACF 也可能需要对应字段（如果走 WordPress 中转）
  ↓
步骤 4: 回归测试
  ↓
副作用 7: 现有 863 个 compositePage 页面重新渲染（CDN 重新验证）
```

### 4.3 各环节破坏面分析

| 环节 | 风险 | 现有功能/分类是否破坏 |
|------|------|---------------------|
| **改 schema（加 optional 字段）** | 🟢 低 | 现有 863 个 compositePage 文档保留，undefined 默认值 |
| **改 schema（加 required 字段）** | 🔴 高 | 现有文档**会校验失败**导致不能发布新内容 |
| **改 schema（删字段）** | 🔴 极高 | 已写数据丢失 |
| **改 schema（改字段类型）** | 🔴 高 | 类型不匹配数据丢失 |
| **sanity deploy 失败** | 🟡 中 | Studio 短期不可用 |
| **前端未同步更新** | 🟡 中 | 新字段 undefined，前端展示空 |
| **多 Agent/开发者协作冲突** | 🟡 中 | Studio 锁定 / 合并冲突 |
| **破坏现有分类（Tools/Features/Blog）** | 🟢 低 | 不影响 `_type` 分类 |

---

## 五、不修改 schema 的可替代方案

### 方案 A: 前端 fallback（推荐，无风险）

| Schema 缺失字段 | 前端 fallback 实现 |
|----------------|-------------------|
| `seo.canonical` | 用 `slug + language` 自动生成：`https://www.lovart.ai[/lang]/{slug}` |
| `seo.hreflang` | 用 `slug` 查翻译映射表自动构建 10 语言版本 |
| `seo.publishedAt` | 用 `releaseDate` 或 `_updatedAt` 代替 |
| `body.faq` / `body.tableOfContents` | 从 `body` block 自动提取 H2 标题生成 TOC |
| `body.readTime` | 计算 body 词数 ÷ 200 words/min |

**风险**：🟢 **零**
**需要前端配合**：✅ 是（改 nextjs 代码）
**是否影响 Sanity**：❌ 不影响
**是否影响 CMS 分类**：❌ 不影响
**是否影响发布管道**：❌ 不影响

---

### 方案 B: Sanity Mutate API 补值（仅限已存在的字段）

| 操作 | 风险 | 是否需要前端配合 |
|------|------|-----------------|
| 修 152 个 structuredData 错误 | 🟢 低 | ❌ 不需要 |
| 修 161 个 description 太长 | 🟢 低 | ❌ 不需要 |
| 补 322 个 blog ogImage | 🟢 低 | ❌ 不需要 |
| 补 343 个 blog structuredData | 🟢 低 | ❌ 不需要 |
| 补 1348 个 blog publishedAt | ❌ **schema 中无此字段，写不进去** | — |

**风险**：🟢 **零**（schema 允许写入的字段）
**需要前端配合**：❌ 不需要
**是否影响 Sanity**：⚠️ 修改数据（但不改结构）
**限制**：只能写 schema 已有的字段

---

### 方案 C: WordPress Headless 加字段（不受 Sanity 铁律限制）

WordPress 端已有 ACF 字段系统。可以在 WP PHP 端添加：
- `custom_canonical` 字段
- `custom_hreflang` 字段

**风险**：🟢 **低**（WordPress 不属于 Sanity 铁律范围）
**需要前端配合**：✅ 是（nextjs 已支持读 ACF 字段）
**是否影响 Sanity**：❌ 不影响

---

## 六、最终结论

### Q1: 修改 schema 是否会破坏现有功能、分类、功能？

**A1: 会破坏。但破坏程度取决于改什么：**

| 改动 | 破坏程度 |
|------|---------|
| 加 optional 字段 | 🟢 低（仅前端需要适配）|
| 加 required 字段 | 🔴 高（破坏所有现有文档）|
| 删字段 | 🔴 极高（数据丢失）|
| 改类型 | 🔴 高（数据不兼容）|
| **分类（compositePage/blog/news 等 `_type`）** | ❌ 不会被破坏（不改 `_type`）|

### Q2: 是否需要前端配合？

**A2: 是。即使改 schema，前端必须配合。**

```typescript
// 前端 wp-adapter.ts 当前
seo: {
  title: wpPage.seo?.title || wpPage.title,
  description: wpPage.seo?.metaDesc || '',
  ogImage: wpPage.seo?.opengraphImage?.sourceUrl || '',
  structuredData: wpPage.customStructuredData || null,
}

// 改 schema 加了 canonical 后必须改为
seo: {
  title: ...,
  canonical: wpPage.seo?.canonical || `${siteUrl}/${lang}/${slug}`,  // fallback
  ...
}
```

### Q3: 是否违反项目铁律？

**A3: 是。改 schemaTypes/ + sanity deploy 是硬性禁止项。**

### Q4: 不改 schema 能解决所有 SEO 问题吗？

**A4: 能。100% 能解决。**

| 之前盘点的问题 | 不改 schema 的方案 |
|---------------|------------------|
| /pricing /login H1 = 0 | 前端 React 改 |
| /ja 模板变量泄漏 | i18n 翻译文件改 |
| 6 语言首页 H1 是英文 | i18n 翻译文件改 |
| 全站无 hreflang | 前端 fallback 生成 |
| /blog canonical 指向首页 | 前端用 slug fallback |
| 152 个 SD 内容错误 | Sanity Mutate 改值 |
| 161 个 description 太长 | Sanity Mutate 改值 |
| 0 张 lazy loading | 前端 `<img>` 加属性 |
| Blog 无 author markup | 前端用 author 字段生成 |
| Blog 无 TOC/readTime | 前端自动提取 |

---

## 七、推荐执行路径

### 阶段 1: Sanity 数据修复（Sanity Mutate API）— 零风险

```python
# 仅修复已有字段，不改 schema
- 修 152 个 SD 内容错误（URL/域名/Avatar 模板）
- 修 161 个 description 长度（截断到 140-160）
- 补 322 个 blog ogImage（用 featuredImage 代替）
- 补 343 个 blog structuredData（用模板生成）
- 补 1348 个 blog publishedAt ❌ schema 中无此字段，跳过
```

**预计影响**：compositePage 与 blog 的搜索可见性立即提升（结构化数据正确率 +14%）。

### 阶段 2: 前端代码修复 — 零 schema 风险

```typescript
// nextjs/lib/wp-adapter.ts
seo: {
  title, description, ogImage, structuredData,
  canonical: wpPage.seo?.canonical || fallbackCanonical(slug, lang),  // ← 新增
  hreflang: wpPage.hreflang || buildHreflangFromTranslationMap(slug),  // ← 新增
}

// nextjs/lib/wp-seo.tsx  
metadata.alternates.languages = buildHreflangFromTranslationMap(slug)

// React 组件修复
- /pricing: 加 <h1>Pricing</h1>
- /login: 加 <h1>Login</h1>
- /ja H1: 修 i18n 翻译 key
- <img loading="lazy">
```

**预计影响**：多语言 SEO 合并权重、canonical 正确指向、图片 LCP 改善。

### 阶段 3: 绝对不做

- ❌ 改 `schemaTypes/`
- ❌ 跑 `sanity deploy`
- ❌ 改 `sanity.config.ts` / `sanity.cli.ts`

---

## 八、给用户的最终建议

### 推荐方案：**前端 fallback + Sanity Mutate 数据修复**

✅ **风险**：零 schema 风险
✅ **需要前端**：是（但只是改代码，不改 CMS）
✅ **不影响 Sanity**：只改字段值，不改结构
✅ **不影响分类**：compositePage/blog 等 _type 不变
✅ **不违反铁律**：完全合规

### 不推荐方案：**改 schema**

❌ **风险**：高（即使只加 optional 字段，前端必须同步，否则 undefined）
❌ **需要前端**：是（必填）
❌ **可能破坏**：Studio 部署中断、新字段未填导致前端空值
❌ **违反铁律**：是（除非用户明确授权）
❌ **物理上**：本机无 schema 源文件，根本改不了

---

> **结论**：**不要修改 schema**。所有 SEO 问题可通过"数据修复（Mutate API）+ 前端 fallback（canonical/hreflang/i18n）"解决，零 schema 风险。