# infra/gates · 质量门禁基建（v1.0）

> **成熟度**：基建抽取第一批（最成熟）——四钩子已被 Lovart（生产管线）与 Moodio（接入实测）双品牌验证。
> **定位**：门禁是品牌无关机制，品牌差异**只存在于 brand-profiles/*.json**。物理代码保留在 `dev/scripts/hooks/`（服务器部署路径依赖 sync.sh，不移动）；本目录是机制契约与品牌差异的唯一声明处。

## 契约：四道硬门禁

| 钩子 | 查什么 | BLOCK 条件 | 调用 |
|---|---|---|---|
| `post-write-check.sh` | 词数（CJK 词当量）/结构完整性/占位符 | 词数超预算、IMAGE PLACEHOLDER | `--file x.md [--target-words N]` |
| `geo-check.sh` | GEO 可摘录性 | 数据点密度 0（无统计=AI 引擎不引用） | `--file x.md --lang en [--strict]` |
| `quota-check.sh` | RULES-70 预算 | 字数超上限/H2·FAQ 越界/重复句/模板过渡词 | `--file x.md --type blog\|landing --lang xx` |
| `lang-check.sh` | 语言规范 | 简繁混用/en 稿中文标点（unicode 正则判定） | `--file x.md --lang xx` |

退出码：0=PASS / 1=BLOCK / 2=engine error。生成链路（loop 引擎）自动执行，BLOCK 带反馈重写 ≤3 轮；手动写稿交付前必跑。

## 判据来源（品牌差异 → brand profile）

| 判据 | 默认（RULES-70） | 品牌覆盖字段 |
|---|---|---|
| 字数预算 | blog 1200–1800（max 2160）/ landing 600–1000 | `contentBudget.*` |
| 长文铁律 | ≥7,500 词（Lovart 生产线） | `contentBudget.blogLongform`（Moodio=null 不启用） |
| 语种表 | RULES-80 十语种 | `languages.*` |
| FAQ/H2 数 | 3–5 / 4–7 | 通用（未品牌化） |

## brand profile schema（v1.0）

见 `brand-profiles/lovart.json`（生产线范式）与 `moodio.json`（内测期范式）。字段 = 品牌差异点清单：
`deploy`（部署树/console 项目）· `contentBudget` · `languages` · `kb`（目录/kb_intent 防污染/能力词表/事实规则/表达红线）· `strategy`（四份策略文件路径）· `cta`（口径与 URL）· `templates`（行业模板）· `publishTarget`（CMS）· `quality`。

## 新品牌接入 checklist（门禁部分）

1. 复制任一 brand profile → `brand-profiles/{brand}.json`，填 9 组字段
2. 字数/语种如与 RULES-70 默认不同，写入 `contentBudget`/`languages`（钩子以 `--max-words`/`--lang` 参数消费，无需改钩子）
3. 跑 `hooks/tests/smoketest_hooks.sh`（16 断言）确认钩子本体健康
4. 试跑一轮生成校准门禁（首稿 BLOCK 是正常校准过程——Moodio 首轮即靠模板写入门禁规则一轮自修）

## 演进记录

- 2026-10-03 lang-check en 分支 CJK 判定改 python unicode 正则（C locale grep 字节匹配把 em-dash 误判中文标点）
- 2026-10-04 双品牌验证完成（Lovart 生产 + Moodio 接入），晋升 infra 资产
