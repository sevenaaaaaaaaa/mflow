# infra/CAPABILITY-MATRIX · 能力承载矩阵（Lovart → Moodio 抽象）

> **用途**：回答"Lovart 的每项能力，Moodio 靠什么承载"——三类承载：**A = Skill 承载**（技能文件运行）、**B = MFlow 后台产品能力**（已内置，配置即用）、**C = 需补产品能力**（开发/接入清单）、**D = 不适用**（Lovart 特有）。
> **v1.0（2026-10-04）**：基于 console 实测（107 API + 6 后台线程 + 9 自动化 preset）。

## ① 工程管理类

| 能力 | Lovart | Moodio 承载 | 类 |
|---|---|---|---|
| 会话启动门禁 | session-init（launchd/手动） | 服务器同款 session-init.sh（部署即跑 GATE1-6） | B |
| S0-S6 状态机 | pipeline-state.py | console 内置 + `/api/item/upsert/advance` `/api/state` | B |
| 会话路由 | lovart-router（23 决策） | router 技能 + `/api/router/decide`（API 化） | A+B |
| 创作规则 | RULES-00/20/30/70/80 | 服务器 02-rules（sync 同步） | A |
| 防幻觉 | 溯源协议 + 事实白名单 + [待考证] | KB Moodio 04 白名单 + 模板红线（双保险） | A |
| 自动化调度 | launchd 三任务 | **systemd mflow-daily/weekly/dream + `/api/automations`（剧本编排：schedule daily/weekly + dry_run + enabled）** | B |
| 质量门禁四钩子 | hooks（手动/管线） | **loop 引擎自动执行 + `/api/hook/run`** | B |
| 三层质检 | quality-cascade | content-quality-gates 技能 + `/api/selfcheck` `/api/selfreview` | A+B |
| 自我迭代 | —（Lovart 无） | self-evolve / selfcheck/autofix / qa-history 仪表（**Moodio 反超项**） | B |

## ② 品牌类

| 能力 | Lovart | Moodio 承载 | 类 |
|---|---|---|---|
| brand profile | lovart.json（10 组字段） | moodio.json | A ✓ |
| 知识库 | 历史大库 750+（散落结构） | Moodio/ 9 份 confirmed + kb_intent 防污染 | A ✓ |
| 词群作战地图 | keyword-clusters v1.0（10 簇/3 KR） | v1.0（12 簇/4 KR） | A ✓ |
| 内容选题计划 | strategy-content v1.1（条目矩阵） | v1.1（SD/AD/ST/DEF/VS/EX 系列） | A ✓ |
| 投放策略 + CRO 审计 | paid-strategy / cro-audit | 同（投放待启动） | A ✓ |
| 行业模板 | 原生 prompt（RULES-20） | moodio-film-studio（`/api/templates` 模板市场） | A+B |
| visual 素材/尺寸 | image-library + 封面池 56URL | **C**：官方素材包 TBD（image_briefs 占位） | C |
| 发布目标 | Sanity o11tm2qe + WP 子站 | **C/D**：CMS 未定（自动化止步 S4-qa 人工发布） | C |

## ③ 执行层

| 能力 | Lovart | Moodio 承载 | 类 |
|---|---|---|---|
| 三入口技能 | lovart-blog/landing/hub-writer | 同名无前缀版（服务器已部署） | A ✓ |
| 品牌入口 | —（直用三入口） | moodio-film-content（路由+口径） | A |
| 生成引擎 | agent/管线执行 | **loop 引擎（并发 2，已产 3 篇）** | B |
| 自动排程 | PRODUCTION-PLAN+calendar | **schedule_executor（auto_loop 2/天实跑）+ `/api/loop/create`** | B |
| 批量生产 | 批次管线 | `/api/batch/*` | B |
| 多语言 | content-writer Tier + multilang 管线 | `/api/generate`（10 语种）+ **`/api/multilang/coverage+fill`** | A+B |
| GEO 探针 | —（Lovart 无此设施） | geo_scheduler 每日 09:30（citations.jsonl） | B |
| 素材/配图 | image-generation + 封面池 | **C/D**：素材包 TBD | C |

## ④ 体验层（四条巡查线 → MFlow 承载）

| 巡查 | Lovart | Moodio 承载 | 类 |
|---|---|---|---|
| 内链健康 | link-suggest 技能 | **`/api/links/audit+suggest` + preset `internal-link-audit`（每周只读报告）**——library 驱动 | B |
| 多语言覆盖 | i18n 管线 | **`/api/multilang/coverage+fill`**——library 驱动 | B |
| 字段/资产质量 | — | **preset `qa-scan` / `qa-field-fix` / `asset-alt-fill`（补 alt）** | B |
| 转化/流量巡查 | GSC 基线 | **preset `low-ctr-refresh`（低 CTR 刷新）/ `decay-refresh`（30 天衰减重写）/ `landing-refresh-publish`**——GSC 接入后即通 | B（前置 GSC） |
| GEO 缺口→改稿 | — | **preset `geo-gap-rewrite`**（探针数据自动取） | B |
| **404/死链/图片 URL 存活（线上扫描）** | 生产 sentinel 体系 | **C：唯一需新开发件**——线上 URL 扫描执行器（Moodio 站点上线后建，接 automations 每周触发） | C |
| 巡查编排本身 | — | **`/api/automations` 剧本**：preset 注册为 weekly/daily 任务 + dry_run + enabled 开关 | B |

## 汇总

- **A（Skill 承载）**：品牌知识库、两份策略资产、三入口、品牌入口、规则集、投放/CRO 方法论——已就位
- **B（产品配置，已内置）**：状态机/loop 引擎/自动排程/GEO 探针/内链审计/多语言覆盖/9 preset/automations 剧本/self-evolve——**配置动作 ≤5 分钟/项，但多数依赖数据源接入后才有意义**
- **C（需补，收敛为 4 件）**：① GSC 项目级接入（解锁流量巡查+低 CTR 刷新）② library/CMS 接入（解锁内链审计+多语言覆盖+发布）③ 线上 404/图片扫描器（站点上线后新开发）④ 素材包（品牌方提供）
- **D（不适用）**：WordPress 子站线、7500 词长文线、PSEO 175 篇（Lovart 特有；Moodio 词群成熟后再议）

## 数据源接入 = 解锁开关（C 类的本质）

Moodio 的 B 类能力多数是"数据源未接"而非"能力缺失"：
- 接 **GSC** → 解锁：流量巡查、low-ctr-refresh、decay-refresh、优化信号表全量
- 接 **CMS/library** → 解锁：links/audit、multilang/coverage+fill、发布链、preset 落库
- 接 **Perplexity key** → GEO 探针升级真引用
- 接 **素材包** → 解锁 visual/配图
