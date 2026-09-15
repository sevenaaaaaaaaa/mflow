# tableBlock 空壳 × 本地 MD 覆盖率（2026-08-04）

## 结论（先搞清楚状态，全量 893 不动）

- 线上空壳文档：DE **195** / FR **197**（节点 DE 284 / FR 290）；七语合计约 **846–893**
- **同语言本地 MD 且含表格 → 可修白名单：0**
- 本地几乎没有 `de-*.md` / `fr-*.md` 正文；仅有的 `de-luma-dream-machine-review` 等 **本身无 tableBlock 空壳**
- Sanity EN 兄弟有 rows：DE 80 / FR 80；其中 **badN==enN 数量对齐**：DE **50** + FR **46** = **96**
  - 这接近口头说的「约 34」，但是 **EN 表单元格是英文**，不能直接 patch 进 de/fr
- 同文档混合（既有空壳又有完好表）：**0**
- **本轮不 patch rows**

## 分层

| 层级 | 含义 | DE | FR | 可否 patch |
|---|---|---:|---:|---|
| A 白名单 | 同语言 MD 含表格 | 0 | 0 | ✅ 唯一可修 |
| B 结构对齐 | EN 兄弟 rows 数 = 空壳数 | 50 | 46 | ❌ 语言错 |
| C 有 EN 表 | EN 有 rows（数量未必齐） | 80 | 80 | ❌ |
| D 无本地源 | 无同语言 MD | ~195 | ~197 | ❌ 先补源 |

## A 白名单

（空）

## B 结构对齐清单（仅供对照，禁止直接 patch）

### DE（50）
- `10-ai-design-prompts-that-actually-work` ×1
- `best-ai-design-agent-for-bootstrappers-maximize-creative-output-on-a-budget` ×1
- `best-ai-design-agent-for-boutique-owner` ×1
- `best-ai-design-agent-for-ecommerce-seller` ×1
- `best-ai-design-agent-for-financial-advisor` ×1
- `best-ai-design-agent-for-food-stall-owner` ×1
- `best-ai-design-agent-for-insurance-agent` ×1
- `best-ai-design-agent-for-yoga-studio-owner` ×1
- `best-pixverse-ai-alternatives-in-2025-video-generation-compared` ×1
- `best-sora-alternatives-in-2025-7-ai-video-generators-compared` ×1
- `best-vidu-ai-alternatives-in-2025-top-video-generation-tools-compared` ×1
- `best-ai-design-agent-for-cafe-owner-2` ×1
- `enterprise-agency-playbook-lovart` ×1
- `eye-contact-touch-edit-character-look-at-camera` ×1
- `best-ai-design-agent-for-lifestyle-studio` ×1
- `best-ai-design-agent-for-meal-prep-business` ×1
- `best-ai-design-agent-for-nail-studio-owner` ×1
- `best-ai-design-agent-for-patisserie-owner` ×1
- `best-ai-design-agent-for-personal-trainer` ×1
- `best-ai-design-agent-for-physical-therapist` ×1
- `best-ai-design-agent-for-pizzeria-owner` ×1
- `brand-kit-ecommerce-lovart` ×1
- `brand-kit-electrician-lovart` ×1
- `brand-kit-food-market-lovart` ×1
- `brand-kit-pediatrician-lovart` ×1
- `brand-kit-pharmacy-lovart` ×1
- `brand-kit-podcaster-lovart` ×1
- `lovart-account-enforcement` ×1
- `how-to-build-design-system-with-ai` ×1
- `how-to-create-tiktok-ads-with-brand-kit` ×2
- `how-to-design-flyers-business-cards-invitations-ai` ×1
- `logo-maker-comparison` ×1
- `vidfly-ai-review` ×1
- `best-ai-design-agent-for-chiropractor` ×1
- `best-ai-design-agent-for-course-creator` ×1
- `best-ai-design-agent-for-restaurant-manager` ×1
- `best-ai-design-agent-for-side-hustler` ×1
- `how-to-choose-ai-art-platform` ×1
- `lovart-vs-rentahuman-ai-design-comparison` ×1
- `brand-kit-bakery-lovart` ×1
- `brand-kit-cat-cafe-lovart` ×1
- `brand-kit-cocktail-bar-lovart` ×1
- `brand-kit-course-creator-lovart` ×1
- `brand-kit-juice-bar-lovart` ×1
- `brand-kit-nail-studio-lovart` ×1
- `brand-kit-optometrist-lovart` ×1
- `brand-kit-painter-decorator-lovart` ×1
- `brand-kit-wedding-photographer-lovart` ×1
- `complete-guide-ai-music-video-creation` ×1
- `how-to-create-google-ads-with-brand-kit` ×1

### FR（46）
- `best-ai-design-agent-for-insurance-agent` ×1
- `best-ai-design-agent-for-law-firm` ×1
- `best-ai-design-agent-for-lifestyle-studio` ×1
- `best-ai-design-agent-for-meal-prep-business` ×1
- `best-ai-design-agent-for-nail-studio-owner` ×1
- `best-ai-design-agent-for-streamer` ×1
- `best-pixverse-ai-alternatives-in-2025-video-generation-compared` ×1
- `best-sora-alternatives-in-2025-7-ai-video-generators-compared` ×1
- `best-vidu-ai-alternatives-in-2025-top-video-generation-tools-compared` ×1
- `brand-kit-bakery-lovart` ×1
- `brand-kit-cat-cafe-lovart` ×1
- `https-www-lovart-ai-zh-blog-the-death-of-the-stock-footage-era-a-complete-guide-to-ai-powered-video-creation-in-2026` ×2
- `hyper-personalization-posters-niche-audiences-ai` ×1
- `best-ai-design-agent-for-course-creator` ×1
- `best-ai-design-agent-for-digital-agency-owner` ×1
- `best-ai-design-agent-for-e-book-author` ×1
- `best-ai-design-agent-for-ecommerce-seller` ×1
- `best-ai-design-agent-for-financial-advisor` ×1
- `how-to-create-google-ads-with-brand-kit` ×1
- `pika-alternatives` ×2
- `why-look-for-adobe-premiere-pro-alternatives` ×1
- `brand-kit-cocktail-bar-lovart` ×1
- `brand-kit-ecommerce-lovart` ×1
- `brand-kit-electrician-lovart` ×1
- `brand-kit-fitness-gym-lovart` ×1
- `brand-kit-food-market-lovart` ×1
- `brand-kit-freelancer-lovart` ×1
- `brand-kit-juice-bar-lovart` ×1
- `brand-kit-wedding-photographer-lovart` ×1
- `heygen-review` ×1
- `best-ai-design-agent-for-patisserie-owner` ×1
- `best-ai-design-agent-for-personal-trainer` ×1
- `best-ai-design-agent-for-pizzeria-owner` ×1
- `best-ai-design-agent-for-restaurant-manager` ×1
- `best-ai-design-agent-for-restaurant-owner` ×1
- `brand-kit-nail-studio-lovart` ×1
- `brand-kit-optometrist-lovart` ×1
- `brand-kit-painter-decorator-lovart` ×1
- `brand-kit-pediatrician-lovart` ×1
- `brand-kit-pharmacy-lovart` ×1
- `brand-kit-podcaster-lovart` ×1
- `how-to-chat-generate-instagram-posts-lovart` ×1
- `how-to-choose-ai-art-platform` ×1
- `best-ai-design-agent-for-catering-business` ×1
- `full-funnel-creative-assets-ai-design-2027` ×1
- `how-to-design-flyers-business-cards-invitations-ai` ×1

## 下一步（要修才做）

1. 为白名单补 **同语言 MD**（或从可追溯德/法语源重建表）
2. `md_to_portable_text` 出表后映射为 production 的 `_type: tableBlock`（转换器当前出 `table`）
3. 只 `set` 对应 `body[i].rows`，不动其它节点
4. 仍禁止全量 893 一锅端

机器可读：`~/Documents/Lovart Local Dev/Output/QA-Memo/tableblock-shell-coverage-2026-08-04.json`
