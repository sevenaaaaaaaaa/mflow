# Lovart Skills & 规范汇总

> 生成日期：2026-05-28 | 汇总所有与 Lovart.ai 相关的本地 Skills、项目规范、知识资产和配置

---

## 一、内容生产管线（4 Skills，串联运行）

| Skill                       | 版本    | 位置                                                   | 职责                                                    |
| --------------------------- | ----- | ---------------------------------------------------- | ----------------------------------------------------- |
| **Keywords Intake**         | 1.0.0 | `4-Archive/Skills/lovart-keywords-intake.md`         | 扫描 Daily Raw/ 中 GSC/Bing CSV → 解析评分 P0/P1/P2 → 自动更新日历 |
| **Content Writer**          | 4.0.0 | `4-Archive/Skills/lovart-content-writer.md`          | 12 种内容类型 × 11 种叙事框架 → 写作 → SEO → Sanity 导出            |
| **Production Orchestrator** | 1.0.0 | `4-Archive/Skills/lovart-production-orchestrator.md` | 薄编排层，串联 3 个子 Skill，输出链接汇总                             |
| **Sanity Publish**          | 3.0.0 | `Skills/lovart-sanity-publish/`                      | Blog MD → Sanity；7 步门控；增量 import --missing                       |

**已弃用**：`lovart-blog-production-workflow.md`（旧版单体 v1.3.0 → 被 Orchestrator + 子 Skills 取代）

### 生产流水线

```
Daily Raw/ CSV → ① keywords-intake (评分 P0/P1/P2 → 更新日历)
               → ② content-writer (按类型写文章 → Sanity 导出)
               → ③ sanity-publish (Schema sync → convert → preview → 确认 → import)
```

---

## 二、落地页生成（2 Skills）

| Skill | 版本 | 用途 | 语言覆盖 |
|---|---|---|---|
| **Landing Page Generator** | — | 6 区块 × 10 语言 × 5 维度个性化 | en/zh-CN/zh-TW/ja/ko/de/fr/ru/pt/it |
| **Features Page Generator** | 2.3.0 | 5 组件 × 11 语言 × 6 Persona | en/zh-CN/zh-TW/ja/ko/de/ru/fr/pt/it/es |

### 附带资产库

- `image-library.md` — 87 张已验证 Lovart CDN 图片
- `URL_REGISTRY.md` — 44+ 图标 + 3 通用流程图片

### Landing Page 6 区块架构

| 序号 | 区块类型 | 允许次数 | 说明 |
|---|---|---|---|
| 1 | `heroSection` | 1 | 首位 |
| 2-N | `contentSection` | ≥1 | 痛点标题 + 行业适配 |
| 2-N | `textImageSection` | ≥1 | 左右图文 |
| 中段 | `threeColumnSection` | 1 | 3 张通用流程图片 |
| 倒二 | `testimonialSection` | ≥1 | Social Proof |
| 最后 | `faqSection` | 1 | 末尾 |

### Features Page 5 组件架构

| 组件 | 内容 | 数量约束 |
|---|---|---|
| `centeredInputSection` | 大标题、subtitle、system_prompt、input_placeholder、4 suggestions | 1 |
| `threeColumnSection` | 三步工作流（Input→Interact→Deliver） | 1 |
| `featureGridSection` | 6 个痛点 feature，各含 icon_url + title + description | 1 |
| `testimonialSection` | 3 个带具体业务数据的真实 testimonial | 1 |
| `faqSection` | 9 个 FAQ | 1 |

---

## 三、API 调用 Skill（Lovart 官方 API）

| Skill | 位置 | 用途 |
|---|---|---|
| **lovart-api** (clawx-openclaw) | `skills/clawx-openclaw/skills/lovart-skill/SKILL.md` | 图片/视频/音频/音乐生成，项目管理 |
| **lovart-api** (mavis-skill-full) | `skills/opencode/mavis-skills/lovart-skill-full/skills/lovart-skill/SKILL.md` | 同上（完整版） |
| `lovart-agent_skill.py` | `skills/opencode/mavis-skills/wechat-mp-workflow/scripts/` | Python 客户端（AK/SK HMAC-SHA256） |
| `generate-cover-lovart.sh` | `skills/opencode/mavis-skills/wechat-mp-workflow/scripts/` | 微信封面生成脚本 |

**环境变量**：`LOVART_ACCESS_KEY` + `LOVART_SECRET_KEY`

### 可用命令

`chat` / `send` / `watch` / `confirm` / `result` / `status` / `config` / `projects` / `project-add` / `project-switch` / `project-rename` / `project-remove` / `threads` / `thread-remove` / `upload` / `upload-artifact` / `download` / `set-mode` / `query-mode` / `create-project`

---

## 四、数据同步 SOP（已统合）

| 层级 | 文件 | 用途 |
|---|---|---|
| **L0 总索引** | `Skills/lovart-sanity-content-publish/SOP-Lovart-Sanity-内容发布总指南.md` | Blog / Features / Tools 三条管道入口 |
| **L0.5 质量门禁** | `Skills/lovart-content-quality-gates/` + `scripts/preflight-content.js` | SEO/URL/i18n/JSON·MD 创建·翻译·发布前预检 |
| **L1 Features SSOT** | `Skills/lovart-features-sanity-publish/SOP-Lovart-Features-Sanity-发布统合指南.md` | 功能页发布完整流程 |
| **L1 Tools SSOT** | `Skills/lovart-tools-sanity-publish/SOP-Lovart-Tools-Sanity-发布统合指南.md` | 工具页发布完整流程 |
| **L1 Blog SSOT** | `sanity-studio/SOP-Sanity同步指南.md` | 博客 Markdown 发布 |
| Agent Skills | `lovart-features-sanity-publish` / `lovart-tools-sanity-publish` | 触发词 + 门禁 |
| 历史简版 | `SOP-PageJSON导入指南.md` | 已并入 L1，仅作跳转 |

### 同步流程

1. **转换**：遍历 `{lang}/*.json` → NDJSON（清洗 `(section_xx)` marker）
2. **导入本休**：`npx sanity dataset import --dataset production --missing`
3. **缺失翻译**：MiniMax-CN (`MiniMax-M2.7`) 翻译 en → 目标语言
4. **zh 简体中文**：从 zh-TW 源用 `zhconv` 繁转简
5. **SEO + 封面修复**：非 en 文档分配随机封面，SEO 取本地化标题

---

## 五、项目规则（.mdc）

| 文件 | 内容 |
|---|---|
| `skills/project-notes/lovart-sanity-content-pipeline.mdc` | Sanity 内容管道约束 |

### 安全规则

| 规则 | 违反时动作 |
|---|---|
| ❌ 不运行 `npx sanity deploy` | 拒绝执行 |
| ❌ 不修改 `sanity.config.ts` / `sanity.cli.ts` / `schemaTypes/` | 拒绝执行 |
| ❌ 不使用 `--replace` 导入模式 | 强制使用 `--missing` |
| ❌ 不删除 production 文档 | 拒绝执行 |
| ❌ 不修改 `.env` 中的 projectId / dataset | 拒绝执行 |
| ✅ 只做 MD → `node convert.js` → `import --missing` | 允许 |

### Sanity 项目信息

| 项目 | 值 |
|---|---|
| Project ID | `o11tm2qe` |
| 数据集 | `production` |
| 账号 | `sevena@lovart.ai` |
| 在线 Studio | `https://lovart.sanity.studio` |

---

## 六、内容策略 & 规划文档

| 文件 | 内容 |
|---|---|
| `lovart-academy-content-calendar-v1.md` | 统一内容日历（12 类型 × 4 漏斗 × 8 行业 × 多语言） |
| `lovart-skills-and-norms-index.md` | 全量索引（537 行，统合 9 大板块） |
| `Lovart-Content-Production-Skills.md` | 团队操作手册（374 行，935 篇内容运营规范） |

### 内容类型矩阵（12 种）

| # | 内容类型 | 分类 | 漏斗 | 长度 | 多语言 |
|---|---|---|---|---|---|
| 1 | Narrative / Insight | Insight & Trend | TOFU | 2500-4000w | EN+CN+JA+zh-TW |
| 2 | Tutorial (How-To) | How-To | MOFU | 1500-3000w | EN+CN+JA |
| 3 | Awesome Prompt Tutorial | How-To | MOFU | 1500-3000w | EN+CN+JA |
| 4 | Comparison / Alternative | How-To | MOFU-BOFU | 2000-3500w | EN+CN+JA+zh-TW |
| 5 | Case Study | Segment | BOFU | 1500-2500w | EN+CN |
| 6 | Best Practice | Best Practice | Post-Purchase | 800-1500w | EN+CN+JA |
| 7 | Pillar Page / 101 | Lovart 101 | TOFU-MOFU | 3000-5000w | EN+CN+JA+zh-TW |
| 8 | Better Design | Better Design | TOFU | 1500-3000w | EN+CN |
| 9 | Segment Deep-Dive | Segment | MOFU | 2000-3500w | EN+CN+JA |
| 10 | Podcast Show Notes | Podcast | TOFU | 800-1500w | EN+CN |
| 11 | Lovart Digest | Digest | Post-Purchase | 1000-2000w | EN+CN |
| 12 | Glossary Entry | Glossary | TOFU | 300-800w | EN+CN+JA |

---

## 七、核心规范速查

### 产品术语（官方）

| 术语 | 译法 | 说明 |
|---|---|---|
| **MCoT Engine** | 思维链引擎 | 推理型多模态生成引擎 |
| **ChatCanvas** | AI 画布交互界面 | 人机协同设计界面 |
| **Nano Banana Pro** | 专业设计模型 | 核心图片生成模型 |
| **Agentic Intelligence** | 代理式 AI | 自主设计决策能力 |
| **Touch Edit** | 触控式精准编辑 | 指触式调整 |
| **Text Edit** | 文本级指令编辑 | 自然语言编辑 |
| **Seedance 2.0** | — | AI 视频生成模型 |

### 品牌定位

- 角色：**AI Design Partner**
- 理念：**Thinking in Systems**（系统化思考）
- 核心钩子：零门槛、自动化流、商业级 4K 输出、全图层可编辑

### 图片 URL 强制规则

- 必须以 `https://assets-persist.lovart.ai/` 开头
- 必须从 `image-library.md` 或 `URL_REGISTRY.md` 中选取
- **严禁编造 URL**
- threeColumnSection 的三张流程图片固定不可替换

### 反 AI 写作规则（主要）

- ❌ 禁止 "Part 1/2/3" 作为章节标签
- ❌ 禁止 "There are three reasons..." 等列表标记开头
- ❌ 禁止三明治段落（topic sentence + 3 支撑点 + conclusion）
- ❌ 禁止 AI trope（"fast-paced digital landscape" / "Let's dive in" 等）
- ✅ 场景化开头（非数据开头）
- ✅ 段落节奏多变（短 + 长交替）
- ✅ 每篇 ≥3 内链，描述性锚文本
- ✅ 数据必须有上下文说明

### 多语言层级

| 层级 | 语言 | 本地化深度 |
|---|---|---|
| Tier 1 | EN（规范语言） | 完整原创写作 |
| Tier 2 | CN | 本地化（适配隐喻、案例、文化参考） |
| Tier 3 | JA, zh-TW | 直译 + 小幅文化适配 |

**强制规则**：每篇文章至少产出 EN + CN 两个版本。

### 内容衰减模型

| 内容类型 | 半衰期 | 更新触发 |
|---|---|---|
| 工具评测 | 6-9 个月 | 竞品重大更新 |
| 对比文章 | 6-12 个月 | 功能更新/价格变化 |
| How-To 教程 | 12-18 个月 | 产品界面变更 |
| Insight & Trend | 6-12 个月 | 行业重大变化 |
| Pillar Page | 6 个月 | 新 Cluster 需链接 |
| Glossary | 24 个月 | 新术语 |

---

## 八、微信渠道关联

| 文件 | 用途 |
|---|---|
| `references/lovart-covers.md` | 公众号封面使用 Lovart OpenAPI 替代方案 |
| `scripts/generate-cover-lovart.sh` | 从文章 MD + STYLE 生成公众号封面 prompt 并调用 Lovart OpenAPI |
| `scripts/lovart-agent_skill.py` | Lovart Agent OpenAPI Python 客户端（1009 行） |

---

## 九、线上可用 Skill

| Skill | 用途 |
|---|---|
| `lovart-api` | Lovart AI 图片/视频/音频/音乐生成（官方 API） |

---

## 十、维护约定

- Lovart 写作/生成 Skills 位于 `4-Archive/Skills/lovart-*.md`
- Sanity 备份备忘位于 `1-Project/Lovart/灾备备忘.md` <!-- TODO: 该文件在重构中已删除，如仍需请确认新落点 -->
- 新发现的 Lovart 相关 AI 规范/总结应补充到汇总文档
- 图片库和 URL 注册表按新增图片增量
