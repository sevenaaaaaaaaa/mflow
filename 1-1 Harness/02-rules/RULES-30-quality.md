---
type: rule
version: 1.0
updated: 2026-07-05
scope: "profile-quality-active"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-30-quality.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart RULES — 30 质量类（Quality）

> 适用路线：质检、Anti-Slop、i18n 优化
> 加载 Profile：`lovart-quality`

---

## 三层质量门禁

**入口收敛**：`lovart-content-quality-gates` 是质检唯一父入口；`lovart-content-audit` 只处理人工/深度审计维度；`lovart-sanity-preflight` 是兼容别名，不得维护独立命令表。

| 层级 | 时机 | 脚本 | 决策 |
|:---:|------|------|------|
| L1 | convert 前 | `preflight-content.js` | BLOCK>0 → 停止 |
| L2 | import 后 | `verify-blog-publish.js` | 抽查确认 |
| L3 | 发布前 | 5 维审计 | PASS/CONDITIONAL |

## Anti-Slop 检测（10 项）

| # | 检查项 | 触发条件 |
|---|--------|---------|
| 1 | 首人称 | Blog 须有真实用户视角（"我用了 X"） |
| 2 | 翻车 | 必须有至少一个"踩坑/翻车"段落 |
| 3 | 搭档 | 必须提及工具搭配使用场景 |
| 4 | 金句 | 每篇至少 1 个可引用的观点句 |
| 5 | H2 密度 | 每 500 字至少 1 个 H2 |
| 6 | 禁用词 | 无 "unlock" "revolutionize" "game-changer" 等空泛词 |
| 7 | AI tell | 无 "as an AI" "I cannot" "in this article" 等 |
| 8 | noIndex | 确认 slug 未被 noindex |
| 9 | 正文占位 | 禁止 IMAGE PLACEHOLDER / [REAL SCREENSHOT REQUIRED] |
| 10 | slug 规范 | kebab-case，禁止下划线 `_` |
| **11** | **body Portable Text** | Blog `body` 必须为 Portable Text 数组，禁止 Markdown 字符串（AB-LP22） |
| **12** | **结构化数据** | Blog @type 必须为 Article；compositePage json 不可为空；description 禁止模板串用（AB-LP23） |

## 禁用词注册表（机器可更新）

`harness_auto_optimize.py` 只能在本区块内追加候选词；不得改写其他规则正文。

<!-- HARNESS_BANNED_EN_START -->
- `unlock`
- `revolutionize`
- `game-changer`
- `leverage`
- `streamline`
- `empower`
- `seamless`
- `seamlessly`
- `delve`
- `testament`
- `unprecedented`
- `the future of`
- `pave the way`
<!-- HARNESS_BANNED_EN_END -->

<!-- HARNESS_BANNED_ZH_START -->
- `赋能`
- `闭环`
- `抓手`
- `链路`
- `底层逻辑`
- `方法论`
- `心智`
- `对齐`
- `颗粒度`
- `打法`
- `痛点`
- `破局`
- `深挖`
- `见证`
- `颠覆性`
- `前沿`
<!-- HARNESS_BANNED_ZH_END -->

## 内容审计维度

| 维度 | 检查项 |
|------|--------|
| 合规 | 无虚假产品数据、无未授权竞品贬低 |
| 文化 | 多语言版本无文化冒犯内容 |
| 可读性 | EN Flesch ≤12，ZH 无机翻腔 |
| SEO | Title/Description 在截断阈值内（75/160 chars） |
| 品牌 | 品牌术语一致（Lovart L 大写、MCoT/ChatCanvas/Touch Edit） |
| **i18n 比例门禁** | **多语言翻译字数比例对齐**：绝对禁止翻译缩水。中文版字符数必须 **≥ 英文版单词数的 1.6 倍**（例如英文版 7,500 词，中文版至少需要 12,000 汉字）。任何低于 1.5 倍比例的翻译，直接判定为“翻译缩水”，触发 BLOCK。 |
| **图片实时拦截** | **图片 URL 实时 HEAD 404 拦截**：在生成或修改 Markdown/JSON 时，Agent 必须对所有新引入的图片 URL 进行 HEAD 请求验证（或在 preflight 中强制增加 HTTP 状态码检测），任何返回 404/403/500 的图片 URL 必须立即 BLOCK，禁止写入文件。 |

## Anti-Bugs 高频速查

| ID | 症状 | 正确做法 |
|----|------|---------|
| AB-P02 | 线上已有仍全量 import | `--missing`；差量走 patch |
| AB-A01 | 无 dry-run 直接 apply | dry-run → 确认 → apply |
| AB-S01 | IMAGE PLACEHOLDER 入正文 | image_briefs 提取 + strip 正文 |
| AB-C02 | zh/zh-TW 机翻低质量 | translate-zh-rewrite.py pilot |
| AB-U01 | Features URL 写成 /tools/ | convert 时 composite-seo-url.js |
| AB-I04 | liblib 封面 404 | blogcover-011~065 池 + --only-broken |
| **AB-LP22** | Blog body Markdown 字符串 | 检测 body[0]._type==null；修复为 Portable Text |
| **AB-LP23** | 结构化数据类型错/空壳 | Blog @type→Article；compositePage json 非 null |

## Sanity 发布前检查

- [ ] `check-sanity-auth.js` API ping 通过
- [ ] `preflight-content.js` BLOCK=0
- [ ] patch/import 已 `--dry-run`
- [ ] **Blog body Portable Text 检测** — 全语言 `body[0]._type != null`（GROQ 一键扫描，AB-LP22）
- [ ] **结构化数据完整性** — Blog `seo.structuredData.json` 非空 + @type=Article + 含 headline/author/datePublished（AB-LP23）
- [ ] **compositePage structuredData** — `seo.structuredData.json` 非 null（AB-LP23）
- [ ] `audit-blog-covers` + `audit-composite-images-404` = 0
- [ ] `audit-blog-future-release-dates.js` = 0
- [ ] GROQ 抽样 SEO url_path、cover.url
