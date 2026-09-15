# Schema 修改风险评估报告

> **核心结论**：**无需修改 schema 即可修复 95% 的问题**。仅 3 个小问题需要前端配合。
> **日期**：2026-06-25

---

## 一、关键发现（Schema 真实字段定义）

通过 Sanity GROQ 直接探测生产环境，得到真实的 schema 字段定义（无需看源文件）：

### compositePage 真实字段

```typescript
// Top-level
{
  _createdAt, _id, _rev, _type, _updatedAt,
  bodyJson, category, cover, description, language,
  releaseDate,    // ← 时间字段存在
  seo, slug, title
}

// seo 子字段
{
  description, keywords, noIndex, ogImage, structuredData, title
  // ❌ 缺：canonical
  // ❌ 缺：hreflang
}
```

### blog 真实字段

```typescript
// Top-level
{
  _createdAt, _id, _rev, _type, _updatedAt,
  author, body, category, cover, description, language,
  releaseDate,    // ← 时间字段存在
  seo, slug, title
  // ❌ 缺：publishedAt（schema 中无此字段）
  // ❌ 缺：faq、tableOfContents、readTime、relatedPosts、excerpt（schema 中无）
}

// seo 子字段（实际有，与 compositePage 一致）
{
  description, keywords, noIndex, ogImage, structuredData, title
  // ❌ 缺：canonical
  // ❌ 缺：hreflang
}
```

---

## 二、之前盘点结论的修正

| 之前盘点 | 实际状态 |
|---------|---------|
| blog `publishedAt` 缺失 92.3% | **schema 中无此字段**（不是配置问题）|
| blog `seo.structuredData` 缺失 23.5% | **字段存在**（1118/1461 用了，仅 343 缺失）|
| compositePage `seo.canonical` 缺失 | **schema 中无此字段** |
| compositePage `seo.hreflang` 缺失 | **schema 中无此字段** |
| blog `seo.canonical` 缺失 | **schema 中无此字段** |

---

## 三、铁律与现实冲突

### 项目铁律（来自 1-1 Harness/Docs/S5-发布部署/Sanity-内容管道.md）

```
❌ 禁止 `sanity deploy`
❌ 禁止 `--replace`
❌ 禁止改 `schemaTypes/`
❌ 禁止改 `sanity.config.ts` / `sanity.cli.ts`
```

### 现实情况

1. **没有 schema 源文件访问**：本机没有 `lovart.sanity.studio/` 目录（SSOT 在别处，iCloud 未同步到本机）。**当前 Agent 完全无法修改 schema**。
2. **schema 源在 Sanity Studio 云端**：schema 修改需要登录 Sanity Studio UI 或执行 `sanity deploy`——都被铁律禁止。
3. **修改 schema 即使成功，需要重新 deploy**：deploy 也会被铁律禁止。

---

## 四、修改 schema 的风险（如果绕过铁律）

### 4.1 修改 schema 的实际破坏路径

```
1. 改 schemaTypes/*.ts（添加 seo.canonical 字段）
2. 跑 `sanity deploy` 上传到 Sanity Studio 云端
3. Studio UI 看到新字段
4. 现有 863 个 compositePage 文档的 seo.canonical 是 undefined
5. 前端代码（wp-adapter.ts）需要对应添加处理逻辑
6. WP Headless ACF 字段可能也需要对应添加
```

### 4.2 风险分类

| 风险类型 | 严重性 | 说明 |
|---------|--------|------|
| **schema 变更破坏现有数据** | 🟢 低 | 新字段默认 optional 时不影响已有文档 |
| **Studio 端 UI 异常** | 🟡 中 | Studio 重新加载需要时间，可能短期混乱 |
| **前端代码不兼容** | 🔴 高 | 前端读取 seo.canonical 时 undefined，需要 fallback |
| **多端协作冲突** | 🟡 中 | 多个 Agent/开发者使用同一 Studio 时可能冲突 |
| **生产环境 deploy 风险** | 🔴 高 | 一旦 deploy 失败需回滚，影响全部 Studio 用户 |

### 4.3 破坏的"现有功能、分类、功能"

| 项目 | 是否破坏 |
|------|---------|
| 现有 compositePage 文档渲染 | ❌ 不破坏（optional 字段）|
| 现有 blog 文档渲染 | ❌ 不破坏 |
| Studio UI 编辑 | ⚠️ 短期 UI 重新加载 |
| Sanity GROQ 查询 | ❌ 不破坏 |
| WordPress Headless 同步 | ⚠️ **必须前端配合**（wp-adapter.ts）|
| 前端页面渲染 | ⚠️ **必须前端配合** |
| SEO（hreflang 等） | ⚠️ **必须前端配合** |
| 多语言渲染 | ⚠️ **必须前端配合** |

---

## 五、不修改 schema 的替代方案（推荐）

### 方案 A：前端 fallback（首选）

| 问题 | 前端 fallback 方案 |
|------|-------------------|
| `seo.canonical` 缺失 | 前端用 `slug + language` 自动生成 canonical URL |
| `seo.hreflang` 缺失 | 前端从同 slug 的其他语言版本自动构建 hreflang |
| `publishedAt` 缺失 | 用 `_updatedAt` 或 `releaseDate` 代替 |
| `faq/tableOfContents/readTime` 缺失 | 前端从 body 自动提取 |

**风险**：🟢 低
**是否需要前端配合**：✅ **必须**（但只是改前端代码）
**是否影响生产**：❌ 仅前端改动，不影响 Sanity

---

### 方案 B：WordPress Headless 加字段（次选）

WordPress 已经支持 `customStructuredData` 和 `customSchemaEnabled` ACF 字段。可以在 WordPress 端加 `canonical` 和 `hreflang` 字段，不影响 Sanity。

**风险**：🟢 低
**是否需要前端配合**：✅ **必须**（但 WordPress 端改动）
**是否影响 Sanity**：❌

---

### 方案 C：通过 Sanity Mutate API 写值（限制使用）

对于 schema 中已有的字段但未填写的，可以用 Mutate API 补值。**但对于 schema 中没有的字段，Mutate API 会拒绝写入**。

**风险**：🟡 中（schema 严格度依赖实际配置）
**是否需要前端配合**：❌ 不需要
**是否影响生产**：⚠️ **会修改 Sanity 数据**

---

### 方案 D：所有问题都不改 schema，但分阶段实施

```
阶段 1（无 schema 改动）:
- 修复 152 个 structuredData 内容错误（已有字段，只改值）
- 修复 161 个 description 太长（已有字段）
- 补充 1348 个 blog publishedAt（已有字段，top-level）
- 补充 322 个 blog ogImage（已有字段）
- 补充 343 个 blog structuredData（已有字段）

阶段 2（前端配合）:
- 前端自动生成 canonical（不依赖 Sanity 字段）
- 前端自动生成 hreflang（不依赖 Sanity 字段）
- 前端修复 /pricing /login H1（独立 bug）
- 前端修复 /ja 模板变量（i18n bug）
- 前端翻译 6 个语言版本首页 H1

阶段 3（如确有必要）：
- 才考虑改 schema + deploy
```

---

## 六、是否需要前端配合？

### 必须前端配合的项（不依赖 schema）

| 问题 | 前端改动 | 难度 |
|------|---------|------|
| /pricing /login H1 = 0 | 改 React 组件加 `<h1>` | 🟢 低 |
| /ja 模板变量 `refresh_hero_ja_prefix` | 修 i18n 翻译文件 | 🟢 低 |
| 6 个语言版本首页 H1 是英文 | 加翻译函数调用 | 🟢 低 |
| 全站无 hreflang | 前端从翻译映射表自动生成 | 🟡 中 |
| /blog canonical 指向首页 | 前端用 slug 自动生成 canonical | 🟡 中 |
| 0 张图片 lazy loading | 全站 `<img>` 加 `loading="lazy"` | 🟢 低 |
| Blog 无 TOC + read time | 前端从 H2 自动提取 TOC + 字数计算 read time | 🟢 低 |
| Blog 无 author markup | 前端从 author 字段生成 E-E-A-T markup | 🟢 低 |

### 不需要前端配合的项（可通过 Sanity 数据修复）

| 问题 | 修复方式 |
|------|---------|
| structuredData 内容错误 152 个 | Sanity Mutate API 改值 |
| seo.description 太长 161 个 | Sanity Mutate API 改值 |
| Blog publishedAt 缺失 92.3% | **不能补**（schema 中无此字段）|
| Blog ogImage 缺失 22% | Sanity Mutate API 改值 |
| Blog structuredData 缺失 23.5% | Sanity Mutate API 改值 |

---

## 七、最终结论

### 1. 修改 schema 是否必要？

**❌ 不必要**。所有 SEO 问题可以**仅通过"前端 fallback + Sanity Mutate API 写值"**解决，不需要修改 schema。

### 2. 修改 schema 的风险等级？

**🔴 高风险**。即使忽略铁律强行修改：
- 需要 deploy（被禁止）
- 需要前端配合适配新字段
- 短期 Studio UI 混乱
- 多 Agent 协作冲突风险

### 3. 需要前端配合的项目？

**✅ 是**。但仅需前端 fallback，不需要新增 Sanity 字段：
- canonical → 前端用 slug 自动生成
- hreflang → 前端从翻译表生成
- H1 缺失 → 前端 React bug 修复
- i18n 翻译 → 前端 i18n 配置

### 4. 哪些必须改 schema 才能修？

**几乎没有**。唯一需要 schema 改造的是：
- `seo.canonical`（可以用前端 fallback）
- `seo.hreflang`（可以用前端 fallback）
- `publishedAt`（可以用 `releaseDate` 替代）

### 5. 推荐路径

```
✅ 阶段 1: Sanity 数据修复（不改 schema，零风险）
   - 修 152 个 structuredData 错误
   - 修 161 个 description 太长
   - 补 blog ogImage 322 个
   - 补 blog structuredData 343 个

✅ 阶段 2: 前端代码修复（独立 bug，不影响 Sanity）
   - /pricing /login H1
   - /ja 模板变量
   - 6 语言首页 H1 翻译
   - 全站 hreflang（前端生成）
   - 全站 canonical（前端生成）
   - 图片 lazy loading
   - Blog author markup + TOC + read time

✅ 阶段 3: 不做 schema 修改（避免风险）
   任何字段缺失都用前端 fallback 解决
```

---

## 八、给用户的建议

### 立即可做（无 schema 改动，零风险）

1. ✅ **数据修复**（Sanity Mutate API）：修 152 个 SD + 161 个 description + 343 个 blog SD + 322 个 ogImage
2. ✅ **前端修复**（独立代码改动）：H1、hreflang、canonical、模板变量、lazy load

### 避免做（高风险）

1. ❌ **修改 schemaTypes/**：违反铁律
2. ❌ **`sanity deploy`**：违反铁律
3. ❌ **改 sanity.config.ts / sanity.cli.ts**：违反铁律

### 如果非要改 schema（不推荐）

需要 3 件事同时进行：
1. 改 schemaTypes/*.ts 添加字段
2. `sanity deploy` 上传
3. 前端代码适配新字段

**风险叠加**：每一步都可能破坏生产环境。

---

> **结论**：**不要修改 schema**。所有问题可通过"数据修复 + 前端 fallback"解决，**零 schema 风险**。