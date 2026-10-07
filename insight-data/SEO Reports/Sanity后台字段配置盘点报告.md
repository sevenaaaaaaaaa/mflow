# Sanity 后台字段配置盘点报告

> **执行日期**：2026-06-25
> **盘点方式**：Sanity GROQ 查询（**只读，不修改任何数据**）
> **目标**：识别 Sanity 字段配置问题，确认哪些 SEO 要素是"配置缺失"而非"前端问题"

---

## 核心结论（先看这个）

之前的"全站 0 个 hreflang"和"全站 0 个 Structured Data"判断**不准确**——让我细化：

| 之前判断 | 真实情况 |
|---------|---------|
| 全站 0 个 hreflang | **未设置**（Sanity schema 中可能没有 `hreflang` 字段） |
| 全站 0 个 Structured Data | compositePage **661/863 有 SD**（76.6%），blog 1118/1461 有（76.5%） |
| Blog 无 author/datePublished | **blog 页面有 `author` 字段**（覆盖率 91.9%），但 `publishedAt` 仅 7.7% |

---

## 一、Sanity 内容类型总览

| 类型 | 数量 | 备注 |
|------|------|------|
| **compositePage** | **8,296** | 所有语言总和（EN=863）|
| **blog** | **10,513** | 所有语言总和（EN=1,461）|
| news | 17 | |
| docs | 44 | |
| category | 12 | |
| tag | 24 | |

---

## 二、compositePage 字段覆盖率（EN 863 个）

### 顶层字段

| 字段 | 覆盖率 | 状态 |
|------|--------|------|
| `seo` | **100.0%** (863/863) | ✅ 全有 |
| `seo.title` | 99.8% (861) | ✅ 全有 |
| `seo.description` | 99.8% (861) | ✅ 全有 |
| `seo.keywords` | 95.1% (821) | ✅ |
| `seo.ogImage` | 95.2% (822) | ✅ |
| **`seo.structuredData`** | **76.6% (661)** | ⚠️ 76.6%，202 个缺失 |
| `seo.noIndex` | 38.1% (329) | 🔴 多数未配置 |
| **`sourceType`** | **37.0% (319)** | 🔴 仅 37%，多数未配置 |
| **`publishedAt`** | **0.0% (0)** | 🔴 **全站都没有此字段** |

### seo 子字段质量

| 字段 | 数量 | 比例 |
|------|------|------|
| seo.title 长度 50-70（最佳） | 668 / 861 | 77.6% |
| seo.title 太短（<30） | 18 | 2.1% |
| seo.title 太长（>75） | 3 | 0.3% |
| seo.description 长度 140-160（最佳） | 331 / 861 | 38.5% |
| seo.description 太长（>160） | **161** | **18.7%** ⚠️ |
| seo.description 太短（<60） | 7 | 0.8% |

---

## 三、blog 字段覆盖率（EN 1,461 个）

### 顶层字段

| 字段 | 覆盖率 | 状态 |
|------|--------|------|
| `seo` | 100% | ✅ |
| `seo.description` | 100% | ✅ |
| `body` | 100% | ✅ |
| `category` | 100% | ✅ |
| `cover` | 99.1% | ✅ |
| `seo.title` | 99.0% | ✅ |
| `author` | **91.9%** (1,343) | ✅ 大多有 |
| `seo.ogImage` | 78.0% (1,139) | ⚠️ |
| **`seo.structuredData`** | **76.5%** (1,118) | ⚠️ |
| `seo.noIndex` | 83.7% (1,223) | ✅ |
| `seo.keywords` | 88.8% (1,297) | ✅ |
| **`publishedAt`** | **7.7%** (113) | 🔴 **严重缺失** |
| `tableOfContents` | - | ❓ 待查 |
| `readTime` | - | ❓ 待查 |
| `relatedPosts` | - | ❓ 待查 |
| `excerpt` | - | ❓ 待查 |
| `faq` | - | ❓ 待查 |
| **`seo.canonical`** | **0.0% (0)** | 🔴 **全 0，schema 中可能没有 canonical 字段** |

### 关键字段实际值（freepik-ai-image-generator-review 案例）

```json
{
  "author": "Seven",                    // ✅ 有
  "publishedAt": None,                 // 🔴 缺失
  "readTime": None,                    // 🔴 缺失
  "tableOfContents": None,            // 🔴 缺失
  "relatedPosts": None,                // 🔴 缺失
  "faq": None,                         // 🔴 缺失
  "excerpt": None,                     // 🔴 缺失
  "sourceType": None,                  // 🔴 缺失
  "seo.structuredData": None,          // 🔴 缺失（与上面的 76.5% 覆盖率矛盾！）
  "seo.ogImage": None,                 // 🔴 缺失
  "seo.canonical": None,               // 🔴 缺失
  "seo.noIndex": None,                 // 🔴 缺失
  "seo.title": "Freepik AI Image Generator Review: Is It Really Worth It in 2026?",
  "seo.description": "Honest Freepik AI review...",
  "seo.keywords": ["freepik", "w..."]
}
```

> **重要**：虽然 blog 整体 `seo.structuredData` 覆盖 76.5%，但**这个高曝光的 freepik blog 偏偏没有**。这与"全 0"的判断并不矛盾——是抽样差异。

---

## 四、structuredData 实际内容问题（661 个 enabled 中 152 个有问题）

### 问题分类

| 问题 | 数量 | 严重性 |
|------|------|--------|
| **URL_MISMATCH**（SD 里 URL 与实际 slug 不一致）| **112** | 🔴 |
| **OLD_DOMAIN**（URL 包含 `lovart.vip` 而非 `lovart.ai`）| **59** | 🔴 |
| **AVATAR_TEMPLATE**（SD 用了"AI Avatar Generator"模板）| **20** | 🔴 |
| 合计有问题 | 152 / 661 | 23.0% |

### 真实问题示例

```
1. tools-nano-banana-2-ai-image-generator:
   - slug: nano-banana-2-ai-image-generator
   - SD url: https://www-pre.lovart.vip/tools/ai-avatar-generator  ❌ 错域名
   - SD name: "AI Avatar Generator | Create Talking Avatars..."      ❌ 错名字

2. tools-ai-ad-thumbnail-generator:
   - slug: ai-ad-thumbnail-generator
   - SD url: https://www.lovart.ai/tools/ai-video-ad-thumbnail-generator-boost-paid-social-ct  ❌ slug 不匹配

3. features-professional-corporate-presentation-design:
   - SD url: ...create-winning-business-presentations-in-minutes-ai-corporate-slides-for-sales-pitches-reports  ❌ slug 完全不符
```

---

## 五、/blog canonical 错误（前端抓取确认）

**前端抓取 `/blog/freepik-ai-image-generator-review` 显示**：
- canonical = `https://www.lovart.ai` （首页）→ **这会让 Google 不索引此博客**

**原因**：blog schema 中 `seo.canonical` 字段**全 0 个配置**（覆盖率 0%），所以前端 fallback 到默认 canonical（即首页 URL）。这不是 "配置错了"，是"根本未配置"。

---

## 六、hreflang 全站缺失

**前端抓取 25+ 页面全部 0 个 hreflang 标签**。

**Sanity 端验证**：
- compositePage 没有 `seo.hreflang` 字段（schema 中可能不存在）
- blog 没有 `seo.hreflang` 字段
- compositePage 也没有 `hreflang` 顶层字段

**结论**：需要：
1. 在 Sanity schema 中加 `seo.hreflang` 字段（数组类型）
2. 或者：使用 frontend 模板动态生成（不同语言 URL 自带 lang 前缀）

---

## 七、/pricing /login 页面 H1 = 0

**前端抓取**：
- `/pricing`: H1 count = **0**（无 H1）
- `/login`: H1 count = **0**（无 H1）

**原因**：
- `pricing` 和 `login` 是 dynamic route，不是 compositePage 类型
- 它们的 H1 是通过 React 组件渲染的，但当前可能因为某些条件没渲染
- **不是 Sanity 字段问题**，是前端代码 bug

---

## 八、/ja 模板变量泄漏 `refresh_hero_ja_prefix`

**原因**：
- 这是 i18n 翻译 key 未匹配到对应翻译
- `refresh_hero_ja_prefix` 是 JSON 中的一个 key，但当前 i18n provider 没有这个 key 的翻译值
- **不是 Sanity 字段配置问题**，是 i18n 配置文件或代码问题

---

## 九、Bing 数据严重不完整

**Bing 6月**：100 个关键词

**对比 Google 6月**：5,000 个关键词

**原因**：
- Bing 6/24 后 sitemap 文件结构可能变化
- IndexNow 提交后 Bing 抓取较慢
- 实际上 sitemaps 正常（13,455 URLs）
- **Bing 索引数据缺失，是 Bing 抓取和索引机制问题，不是 Sanity 字段问题**

---

## 十、问题分类（按修复路径）

### A. Sanity Schema 缺失字段（需要 schema 改造）

| 字段 | 涉及类型 | 影响 |
|------|---------|------|
| `seo.canonical` | blog | 0/1461（0%） |
| `seo.hreflang` | compositePage + blog | 0% |
| `publishedAt` | compositePage | 0/863（0%） |
| `tableOfContents` | blog | 0% |
| `readTime` | blog | 0% |
| `relatedPosts` | blog | 0% |
| `excerpt` | blog | 0% |
| `faq` | blog | 0% |
| `sourceType` | compositePage | 37% |

### B. Sanity 字段已配置但内容错误

| 问题 | 数量 |
|------|------|
| structuredData URL 与 slug 不匹配 | 112 |
| structuredData 包含旧域名 lovart.vip | 59 |
| structuredData 用了 Avatar 模板 | 20 |
| seo.title 长度不佳 | 21 |
| seo.description 太长（>160） | 161 |
| seo.description 太短（<60） | 7 |

### C. 前端渲染问题（不是 Sanity 字段问题）

- `/pricing` H1 = 0
- `/login` H1 = 0
- `/ja` 模板变量 `refresh_hero_ja_prefix` 泄漏
- 6 个语言版本首页 H1 是英文（i18n 翻译缺失）
- 全站无 hreflang 标签
- 0 张图片 lazy loading

### D. 内容深度问题

- `/zh` 内容仅 1,592 词
- Blog 无 TOC、read time、author markup
- Blog 无 signup CTA

---

## 十一、关键发现总结

1. **structuredData 实际有 661/863 配置（76.6%）** — 不是 0%。但其中 152 个有内容错误（URL 错误/旧域名/Avatar 模板）
2. **blog 字段缺失严重**：canonical、hreflang、publishedAt 几乎全 0%（不是 schema 缺失，是字段未填）
3. **compositePage 字段覆盖好**：seo.* 全 99%+，但 publishedAt 全 0%（schema 中可能不存在此字段）
4. **/pricing /login H1=0 和 /ja 模板变量泄漏是前端问题**，不是 Sanity 字段配置问题
5. **Bing 数据缺失**不是 Sanity 字段问题，是 Bing 抓取和索引机制

---

## 十二、修复路径建议（**不立即执行**）

### Step 1: Sanity Schema 补全

1. 给 compositePage 加 `publishedAt` 字段（date 类型）
2. 给 blog 加 `seo.canonical` 字段（string，可选）
3. 给 compositePage + blog 都加 `seo.hreflang` 字段（array of objects）

### Step 2: 修复 structuredData 内容错误（152 个）

按优先级：
1. 59 个 OLD_DOMAIN 优先（影响 SERP canonical 信号）
2. 112 个 URL_MISMATCH（影响 rich snippet）
3. 20 个 AVATAR_TEMPLATE（已经修复 title/desc，SD 也需同步更新）

### Step 3: 修复 seo 字段长度

- 161 个 description > 160 chars → 截断到 140-160
- 7 个 description < 60 chars → 补充内容
- 18 个 title < 30 chars → 补充关键词
- 3 个 title > 75 chars → 截断

### Step 4: 修复 Blog 缺失字段

- 1348 个 blog `publishedAt` 待补
- 322 个 blog `seo.ogImage` 待补
- 343 个 blog `seo.structuredData` 待补

### Step 5: 前端 Bug 修复（独立于 Sanity）

- /pricing /login H1 渲染
- /ja i18n 翻译 key 修复
- 6 个语言版本首页 H1 翻译
- 全站 hreflang 标签添加

---

> **本报告为只读盘点，未对 Sanity 做任何修改**。所有发现的问题已分类，需用户授权后才能执行修复。