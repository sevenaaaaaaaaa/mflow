---
name: landing-writer
description: >-
  品牌落地页/页面创作唯一入口（2026-10-03 整合：landing-page 主技能 + page-serp-writer 文案支撑 +
  refresh-page 生成器 + features legacy 四合一）。故事线为总纲，六维绑定，composite-v2 / legacy 双轨，
  止步发布前（发布走 sanity-publish）。
  Use for 「生成/修复/重写/刷新 Tools、Features、Product、Solution、Scenario、Topic、Landing Page、页面 JSON」、
  页面 SERP 文案、composite-v2、页面 SEO/JSON-LD、配图选取。
---

## 预算（RULES-70 强制）

- 字数：Blog 1200–1800（**绝不超 2160**）；落地页文案 600–1000；摘要/分发稿 ≤600
- H2 4–7 · FAQ 3–5 · 每千字 1–3 数据点（同数据不重复）· 外部来源 2–5 条（完整 URL）
- 列表块 ≤4 处且不连续；单段 ≤300 字符；禁止同义反复 / 复述式总结 / 模板过渡词堆砌 / 形容词堆叠
- 字数不足时**优先删冗余**，绝不补形容词
- 交付前必须过：`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`

## 定位与边界

本 skill 是 **品牌落地页/页面创作唯一入口**。2026-10-03 起以下技能已并入，不再独立存在：
`landing-page`（→ references/landing-master.md + references/landing-ssot/）、`page-serp-writer`（→ references/page-copy-serp.md）、`refresh-page-page-generator`（→ references/pages/refresh-page-generator.md）、`features-page.md`（→ references/pages/features-legacy.md）。

- 博客请求 → `blog-writer`（博客唯一入口），不在本 skill
- 发布（Sanity import/校验/上线）→ `sanity-publish` 父入口及各类 sanity publish；本 skill 止步于页面 JSON + 元数据 + 自检通过
- 故事线 SSOT 的机器可读文件在 `1-3 GenFlow/Page Gen/Refresh-Page/`（landing/solution/scenarios-storylines.json、page-copy-bindings.json）

## 页面类型路由（Step 0 必判）

| 页面类型 | 输出格式 | 模板文档（references/） | 禁止 |
|----------|----------|----------|------|
| **Tools**（category: tool） | 每语言 1 个 composite-v2 JSON → `Page Gen/Pages/Tools/{lang}/` | `tools-v2-template.md` + `landing-master.md` §轨道C | legacy 六区块 |
| **Landing Page**（投放向） | composite-v2 JSON · 12–15 段 | `landing-ssot/landing-v2-template.md` + 故事线 JSON | 混用 Tools 故事线 |
| **Features / 其他 legacy** | 单文件 10 个 `section_xx` key | `json-template.md` + `pages/features-legacy.md` | 把 Tools 写成 legacy |
| **页面文案/刷新**（storyline-driven） | composite-v2 bodyJson/type 序列 | `pages/refresh-page-generator.md` + `page-copy-serp.md` | 绕开故事线自定义 |

默认：用户说「工具页 / Tools」→ composite-v2（轨道 C）；未说明类型先问或按 category 判断。

## 故事线为总纲（第一原则，RULES-20 硬条款）

选定故事线后，6 个维度全部以该故事线为准：文案绑定 / 模块 sections / 个性化（audience+intent）/ 配图（image_pool）/ CRO（ctaStyle）/ 质检（COPY-PREFLIGHT）。
强制顺序：`PAGE-BRIEF → 选故事线 → 读全维度绑定 → 生成 → COPY-PREFLIGHT`。**禁止**绕开故事线自定义 intent/模块/文案；迭代就改故事线绑定本身（`1-3 GenFlow/Page Gen/Refresh-Page/` 的 JSON + page-copy-bindings.json）。

- 故事线选型与 copy 规则：`references/landing-master.md` §轨道C/D（T1–T5 / T-long / landing-trial-now 等 7 条投放故事线）
- 文案 SSOT 与写作约束：`references/landing-ssot/landing-copy-constraints-ssot.md`；立场 `PAGE-BRIEF.md`
- intent 以故事线为准；缺任一步禁止直接写 Hero 或 CTA

## 全类型文案总则（七要素，缺一不可）

1. Buyer / audience 2. Input 3. Output 4. Edit path 5. Proof 6. CTA 7. FAQ / objection

- **Hero** 必须覆盖：主语 + 输入 + 输出 + 风险降低点/buyer（禁抽象口号）
- **Proof**：logo wall 只算弱 proof，至少一类强 proof（deliverable / workflow / output format / before-after / verified example / limitation）
- **CTA** 跟流量阶段：Search→free/no credit card；Competitor→compare/switch；Brand trust→explore/watch；Offer→claim/upgrade
- **FAQ** ≥3 条，优先高意图异议（商用版权 / 输入输出格式 / 编辑协作 / 适用边界 / 与竞品区别）

## 核心产品术语（官方表述）

MCoT Engine · ChatCanvas · Nano Banana Pro · Agentic Intelligence · Touch Edit · Text Edit。
品牌定位：AI Design Partner，Thinking in Systems。核心钩子：零门槛、自动化流、商业级 4K、全图层可编辑。

## 知识溯源协议（零幻觉）

所有产品事实按优先级溯源：① 已验证图片库（`references/image-library.md` + 自动选图 `references/landing-ssot/image_pool.py`）② 用户参考 JSON ③ 官方文档 ④ 网络核实 → 均无法确认时标注 `[待考证：… — 建议联系产品团队确认]`，不跳过输出。
技术参数/价格/兼容平台/集成/用户数据/竞品对比六类信息必须先查证（详见 `references/landing-master.md` §溯源协议）。

**配图自动选图**：不手动查表，用 `references/landing-ssot/image_pool.py`（match_title/get_image/assign_images_to_features）；四约束：hash 不截断、英文词边界正则、CJK 精确子串、同页同语言共用一套 URL。

## 三轨工作流（详法见 references/landing-master.md）

| 轨道 | 输入 → 输出 |
|---|---|
| **A** legacy | 主题文本 → 六区块 JSON（10 语言，第六步分批协议，第八步 TDK+OG+FAQPage JSON-LD） |
| **B** 修复 | JSON 代码 → 诊断报告（Critical/Copy/Resource/Language）→ 重建 |
| **C** Tools | 主题/slug → composite-v2（选 T1–T5/T-long 故事线；"单 job 页面"原则；每批 ≤3 语言 ×4 批；C5 自检 `preflight-content.js --strict` + `convert-tools.js --dry-run`） |
| **D** Landing 投放 | 投放意图 → 7 条 landing 故事线之一（vs-competitor/trial-now/brand-trust/offer-close/gallery-*；landing-full 仅内部 QA） |

## 元数据输出（JSON 后必须）

SEO TDK（slug/title≤60/description≤160/keywords 5–8）+ OG/Twitter Card + FAQPage JSON-LD（仅英文，name/text 与 section 原文完全一致）。

## 质量自检（交付前逐项）

Tools v2：schemaVersion=composite-v2 · storylineTemplate 合法 · bodyJson 无 legacy type · 模块序列与故事线一致 · 10 语言齐全 · media.src 来自图库或 [待考证]。
Legacy：6 种区块齐 · heroSection 第 1 位 faqSection 末位 · 10 语言齐 · image_url 全来自图库 · 无 Banned Patterns · Persona 已声明 · FAQ 覆盖商用版权+操作门槛 · JSON-LD 与正文一致 · 分批格式正确。
跨轨道：`1-3 GenFlow/Page Gen/Refresh-Page/COPY-PREFLIGHT.md`（storyline-driven）。

## 关键路径

```
1-3 GenFlow/Page Gen/Refresh-Page/          ← 故事线 SSOT（JSON + README + COPY-PREFLIGHT + PAGE-BRIEF）
1-4 Dev/品牌.sanity.studio/scripts/（Lovart 生产环境专属）          ← Sanity 脚本
1-1 Harness/Skills/03-review/sanity-preflight  ← 发布前结构校验
```
