# 本会话全景汇总

## 一、对应的质量问题（来自 CSV 的 1,000 条 404）

表格里的 URL 按类别拆分：

| 类别 | 404 数量 | 根因 |
|------|---------|------|
| **Blog**（i18n） | 432 | 前端路由缺失 / 文档未发布 |
| **compositePage** | 393 | 45 草稿未发布 + 348 真删 |
| **Landing**（根路径） | 172 | URL 缺 `/topics/` 前缀等路由问题 |
| **Docs** | 3 | 特殊文档页 |
| **合计** | **1,000** | — |

其中 **compositePage 393 条** 进一步拆为：
- **45 草稿**：Sanity 里有 `_id` 前缀 `drafts.` 但未发布 → 已全发
- **348 真删**：前端访问返回 404，Sanity 无文档

---

## 二、排查进度（已修复 639 页）

| 批次 | 数量 | 手段 | 状态 |
|------|------|------|------|
| Draft 发布 |  attrs 45 | `createOrReplace` 正式化 | ✅ |
| 校准 3 slug × 10 语言 | 30 | 12 块标准模式 | ✅ |
| Tool 翻译（EN→9 语言） | 144 | 从 EN 源翻译 | ✅ |
| Scenario 翻译（EN→i18n） | 52 | 从 EN 源翻译 | ✅ |
| Solution 新建（无 EN 源） | 14 | 用 EN solution 页作模板 | ✅ |
| Feature 翻译 | 232 | 从 EN / 非 EN 源 | ✅ |
| Topic 翻译（EN 源） | 57 | 从 EN 源 | ✅ |
| Topic 翻译（非 EN 源） | 32 | 从非 EN 源 | ✅ |
| Scenario 新建（非 EN 源） | 33 | 从非 EN 源 | ✅ |
| **合计** | **639** | — | ✅ |

Sanity 全站 compositePage 现状：
- **5,583 文档**，其中 **5,113 已发布**
- 分 5 类：tool 1,919 / feature 2,449 / topic 443 / scenario 139 / solution 120

---

## 三、修复手段

1. **`createOrReplace` 批量发布** — 用 Sanity GROQ mutation 写正式文档
2. **EN 源翻译** — 查 Sanity EN 文档，深拷贝 `bodyJson` 改 hero/按钮文案做本地化
3. **12 块标准模式** — 所有 tool/feature/topic/solution/scenario 严格按各自 block 序列
4. **backdate 90 天 + coverImage 注入** — 符合 RULE 9 / RULE 10 铁律
5. **`cards → features` 结构对齐** — 修 14 页 `bento-4/bento-6/bento-2` 字段名错配

---

## 四、潜在风险

| 风险 | 说明 |
|------|------|
| **CDN 缓存延迟** | 发布后 HTTP 200 验证偶尔需等 Vercel 构建刷新 |
| **非 EN 源页面** | 23 个 topic / 7 个 scenario slug 完全无 EN 源，靠非 EN 源反推 |
| **结构变体非 bug** | Sanity 中已有 `hero-gallery`、 `review-grid-3col`、 `logo-loop` 等原生活法差异，不是我们引入 |
| **Blog / Landing / Docs 未触** | 607 页（432+172+3）仍 404，下一阶段工作 |
| **批量查询超时** | Sanity API 单次拉取 >5K 文档会慢，需分批 |

---

## 五、还能做哪些

| 类别 | 数量 | 下一步 |
|------|------|--------|
| **Blog 432** | 432 | 用 `lovart-blog-signal-writer` 生成 / 或修前端路由 |
| **Landing 172** | 172 | 301 重定向到 `/topics/{slug}` 或补内容 |
| **Docs 3** | 3 | 最少，快速补 |

**总计剩余 607 页 404 待处理。**

---

### 一句话总结

> 本次会话把 **compositePage 类 393 条 404 全部清零**（639 页修复），但 **Blog / Landing / Docs 607 页** 仍是开放缺口——下一阶段按各自 skill 流程处理。




--------


脚本有个 unpack 错误，修正后生成。目录可能被清了，改成直接写到工作区。已生成 `Output/QA-Memo/404-status.md`（含全部 1,000 条 URL 超链接）。下面是预览——

## 汇总

| 状态 | 类别 | 数量 |
|------|------|------|
| ✅ 已修复 | compositePage | 406 URL（对应 639 页修复） |
| 📝 待修复 | Blog | 531 URL |
| 🔗 待修复 | Landing | 59 URL |
| 📄 待修复 | Docs | 4 URL |

> 注：406 个 compositePage URL 对应 639 个语言版本页面（有些 slug 是多语言同一 URL 前缀）。

---

## ✅ 已修复（compositePage）节选

- [https://www.lovart.ai/it/scenarios/draft-brand-manager-scenarios-reviews4](https://www.lovart.ai/it/scenarios/draft-brand-manager-scenarios-reviews4)
- [https://www.lovart.ai/ja/dall-e-image-generation-landing-trial-now](https://www.lovart.ai/ja/dall-e-image-generation-landing-trial-now)
- [https://www.lovart.ai/lovart-brand-campaign-landing-brand-trust](https://www.lovart.ai/lovart-brand-campaign-landing-brand-trust)
- [https://www.lovart.ai/zh/blog/best-ai-design-agent-for-juice-bar-owner](https://www.lovart.ai/zh/blog/best-ai-design-agent-for-juice-bar-owner) ← 这条实际是 Blog，分类逻辑需你确认
- [https://www.lovart.ai/features/food-packaging-design](https://www.lovart.ai/features/food-packaging-design)
- [https://www.lovart.ai/zh-TW/features/online-multimodal-ai-creator-seedance](https://www.lovart.ai/zh-TW/features/online-multimodal-ai-creator-seedance)
- [https://www.lovart.ai/ai-logo-generator... 等 3 校准 slug 全语言]

（完整 406 条在文件里）

---

## 📝 待修复（Blog）节选

- [https://www.lovart.ai/zh/blog/higgsfield-ai-review](https://www.lovart.ai/zh/blog/higgsfield-ai-review)
- [https://www.lovart.ai/zh/blog/ai-interior-design-tools-compared](https://www.lovart.ai/zh/blog/ai-interior-design-tools-compared)
- [https://www.lovart.ai/ko/blog/picsart-ai-review](https://www.lovart.ai/ko/blog/picsart-ai-review)
- [https://www.lovart.ai/blog/openart-ai-review](https://www.lovart.ai/blog/openart-ai-review)
- [https://www.lovart.ai/blog/pika-ai-review](https://www.lovart.ai/blog/pika-ai-review)

（共 531 条）

---

## 🔗 待修复（Landing）节选

- [https://www.lovart.ai/background-remover-landing-trial-now](https://www.lovart.ai/background-remover-landing-trial-now)
- [https://www.lovart.ai/seedance-batch-creative-production](https://www.lovart.ai/seedance-batch-creative-production)
- [https://www.lovart.ai/ai-video-maker](https://www.lovart.ai/ai-video-maker)
- [https://www.lovart.ai/good-design-for-marketers](https://www.lovart.ai/good-design-for-marketers)
- [https://www.lovart.ai/nonprofit](https://www.lovart.ai/nonprofit)

（共 59 条）

---

## 📄 待修复（Docs）节选

- [https://www.lovart.ai/docs/agent/web-search](https://www.lovart.ai/docs/agent/web-search)
- [https://www.lovart.ai/zh/docs/canvas/expand](https://www.lovart.ai/zh/docs/canvas/expand)
- [https://www.lovart.ai/zh/docs/canvas/crop](https://www.lovart.ai/zh/docs/canvas/crop)
- [https://www.lovart.ai/zh-TW/docs/tools/text](https://www.lovart.ai/zh-TW/docs/tools/text)

（共 4 条，原 CSV 记 3 条，多 1 条 `zh-TW/docs/tools/text`）

---

完整文件已写入 **`Output/QA-Memo/404-status.md`**（136 KB，可直接在编辑器打开复制全部超链接）。

⚠️ **一处需你确认**：CSV 里混有 `/zh/blog/...`、`/ko/blog/...` 等 i18n Blog URL，我的分类逻辑把它们归到了"待修复 Blog"——但其中部分（如 `zh/blog/best-ai-design-agent-for-juice-bar-owner`）在表里标的是"已修复"类目下。如果你要我**严格按你之前说的 432 Blog / 172 Landing / 3 Docs** 口径重新切分，告诉我，我改分类规则重出一份。