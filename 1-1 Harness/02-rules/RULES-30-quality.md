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

## 一、硬条款（机器可检查，违反即 BLOCK）

1. **禁止** L1 未过就进入 import：`preflight-content.js` BLOCK>0 必须停下
2. **禁止** Blog `body` 用 Markdown 字符串——必须是 Portable Text 数组（`body[0]._type != null`）
3. **禁止** `seo.structuredData.json` 为空；Blog `@type` 必须为 `Article`；compositePage json 非 null
4. **必须**每篇含：真实用户视角（首人称）1 处 + 踩坑/翻车段落 ≥1 + 金句 ≥1 + 工具搭配场景 ≥1
5. **必须**每 500 字 ≥1 个 H2（与 RULES-70 的 H2 ≤7 同时满足）
6. **禁止**禁用词（见 §三 注册表；机器扫描，命中即 BLOCK）
7. **禁止** AI tell：`as an AI` / `I cannot` / `in this article`
8. **禁止**正文出现占位符（`IMAGE PLACEHOLDER` / `[REAL SCREENSHOT REQUIRED]`）
9. **必须**slug kebab-case（**禁止**下划线）
10. **必须**未 noindex；Title ≤75 / Description ≤160 字符
11. **i18n 比例门禁**：中文版字符数 ≥ 英文版单词数 × 1.6（≥1.5 即判"翻译缩水" BLOCK）
12. **图片 URL 必须实时校验**：新增图片 URL 一律 HEAD 检查，404/403/500 即 BLOCK 禁止写入
13. **禁止**虚假产品数据；**禁止**未授权贬低竞品；多语言版本不得有文化冒犯内容
14. **必须**品牌术语一致：Lovart（L 大写）、MCoT、ChatCanvas、Touch Edit
15. **必须**可读性：EN Flesch ≤12；ZH 无机翻腔（连续「的」≤2、无英文虚词残留）

**机器检查映射**：`preflight-content.js`(L1) · `verify-blog-publish.js`(L2) · 5 维审计(L3) ·
`post-write-check.sh` · `geo-check.sh` · `quota-check.sh` · `lang-check.sh`（MFlow 侧四门禁同源）

## 二、三层门禁

**入口收敛**：`lovart-content-quality-gates` 是质检唯一父入口；`lovart-content-audit` 只处理人工/深度审计维度；`lovart-sanity-preflight` 是兼容别名，不得维护独立命令表。

| 层级 | 时机 | 脚本 | 决策 |
|:---:|------|------|------|
| L1 | convert 前 | `preflight-content.js` | BLOCK>0 → 停止 |
| L2 | import 后 | `verify-blog-publish.js` | 抽查确认 |
| L3 | 发布前 | 5 维审计 | PASS/CONDITIONAL |

## 三、禁用词注册表（机器可更新）

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

## 四、参数表

### Anti-Slop 检测项（12）

| # | 检查项 | 触发条件 |
|---|--------|---------|
| 1 | 首人称 | Blog 须有真实用户视角（"我用了 X"） |
| 2 | 翻车 | 必须有至少一个"踩坑/翻车"段落 |
| 3 | 搭档 | 必须提及工具搭配使用场景 |
| 4 | 金句 | 每篇至少 1 个可引用的观点句 |
| 5 | H2 密度 | 每 500 字至少 1 个 H2 |
| 6 | 禁用词 | 见 §三 |
| 7 | AI tell | 见硬条款 7 |
| 8 | noIndex | 确认 slug 未被 noindex |
| 9 | 正文占位 | 见硬条款 8 |
| 10 | slug 规范 | 见硬条款 9 |
| 11 | body Portable Text | 见硬条款 2（AB-LP22） |
| 12 | 结构化数据 | 见硬条款 3（AB-LP23） |

### 内容审计维度

| 维度 | 检查项 |
|------|--------|
| 合规 | 无虚假产品数据、无未授权竞品贬低 |
| 文化 | 多语言版本无文化冒犯内容 |
| 可读性 | EN Flesch ≤12，ZH 无机翻腔 |
| SEO | Title/Description 在截断阈值内（75/160） |
| 品牌 | 品牌术语一致（Lovart L 大写、MCoT/ChatCanvas/Touch Edit） |
| i18n 比例 | 见硬条款 11 |
| 图片实时拦截 | 见硬条款 12 |

### Anti-Bugs 高频速查

| ID | 症状 | 正确做法 |
|----|------|---------|
| AB-P02 | 线上已有仍全量 import | `--missing`；差量走 patch |
| AB-A01 | 无 dry-run 直接 apply | dry-run → 确认 → apply |
| AB-S01 | IMAGE PLACEHOLDER 入正文 | image_briefs 提取 + strip 正文 |
| AB-C02 | zh/zh-TW 机翻低质量 | translate-zh-rewrite.py pilot |
| AB-U01 | Features URL 写成 /tools/ | convert 时 composite-seo-url.js |
| AB-I04 | liblib 封面 404 | blogcover-011~065 池 + `--only-broken` |
| AB-LP22 | Blog body Markdown 字符串 | 检测 `body[0]._type==null`；修 Portable Text |
| AB-LP23 | 结构化数据类型错/空壳 | Blog @type→Article；compositePage json 非 null |

## 五、发布前检查清单

- [ ] `check-sanity-auth.js` API ping 通过
- [ ] `preflight-content.js` BLOCK=0
- [ ] patch/import 已 `--dry-run`
- [ ] Blog body 全语言 `body[0]._type != null`
- [ ] Blog `seo.structuredData.json` 非空 + @type=Article + 含 headline/author/datePublished
- [ ] compositePage `seo.structuredData.json` 非 null
- [ ] `audit-blog-covers` + `audit-composite-images-404` = 0
- [ ] `audit-blog-future-release-dates.js` = 0
- [ ] GROQ 抽样 SEO `url_path`、`cover.url`
