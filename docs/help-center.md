# MFlow 帮助中心

> 面向日常操作者（人类）与 agent。每节都可直接执行；深水区链接指向 `1-1 Harness/` 内部 SSOT。

---

## 目录

1. [快速开始](#1-快速开始)
2. [会话协议（启动门禁 / 路由 / 收尾）](#2-会话协议)
3. [内容创作 SOP](#3-内容创作-sop)
4. [质量门禁](#4-质量门禁)
5. [发布与 Sanity 铁律](#5-发布与-sanity-铁律)
6. [分发（四轨道）](#6-分发四轨道)
7. [数据、报告与监控](#7-数据报告与监控)
8. [调度与运维](#8-调度与运维)
9. [治理：加脚本 / 加技能 / 改规则](#9-治理)
10. [故障排查 FAQ](#10-故障排查-faq)

---

## 1. 快速开始

**环境**：macOS 或 Linux；Python 3.12+（推荐 `uv venv`，装 `google-auth googleapiclient pyyaml requests`，即 trident-venv 复刻）；gh CLI（GitHub 操作，可选）。

**首次检查清单**：

```bash
bash "1-4 Dev/scripts/session-init.sh"     # 4 道门禁全过 = 环境健康
python3 "1-4 Dev/scripts/harness_sync.py"  # 从 vault 真相同步规则到各 agent 运行时
```

**路径契约**：所有脚本按自身位置推导路径；两个可选环境变量：`LOVART_LOCAL_DEV_ROOT`（运行时输出，默认 `~/Documents/Lovart Local Dev`）、`LOVART_PYTHON`（数据拉取用 venv 解释器）。禁止硬编码绝对路径。

**凭证**：`secrets/`（Sanity/Notion token）、`1-1 Harness/Skills/01-strategy/lovart-trident-data-engine/credentials/`（GSC/GA4/飞书）、`1-4 Dev/scripts/sentinel/*_credentials/`。全部 git-ignore，丢失时参照 `secrets/README.md` 恢复。

## 2. 会话协议

**一条会话只做一类事**：调研→清单→关闭→创作；不在调研会话里发布，不在创作会话里跑报告（`02-rules/SESSION-ROUTING.md`）。

**启动（必做）**：

```bash
bash "1-4 Dev/scripts/session-init.sh"
```

GATE 1 pipeline-state 存在 / GATE 2 路由器合法 / GATE 3 下一步建议 / GATE 4 治理（手动）。任何一门失败先修复再开工。

**接任务先问路由器**：

```bash
python3 "1-1 Harness/Skills/06-orchestrate/lovart-router/router.py" decide --stage S3 --scenario blog
# 返回：该用哪个 profile、加载哪些 skill、下一步动作
```

**收尾（必做）**：触发条件 = 用户说"收尾/log this"，或触碰 ≥5 文件 / ≥1 schema 改动 / ≥1 新 skill。写结构化 log 到 `1-1 Harness/11-knowledge/sessions/{YYYY-MM-DD}-{slug}.md`（frontmatter 带 `session_date`/`session_slug`），status: draft → 用户确认 → ready。**不写日志 = silent loss，不允许跳过。**

## 3. 内容创作 SOP

**唯一入口铁律**：

- 所有语言的所有 Blog → `lovart-blog-signal-writer`（不翻译、不走 i18n-pipeline、没有例外）
- 所有落地页 → `lovart-landing-page`
- 10 语言（en/zh/zh-TW/ja/ko/de/fr/pt/ru/it）全部是**信号驱动重写**，不是 EN 翻译

**≥5,000 词 Blog 强制状态机**（RULES-20 v1.1）：

```
OUTLINE（读信号数据 + KB + 立场 + 反方观点 + 字数预算 → 等确认）
  → DRAFT_PART1..N（每部分 ≤2,500 词，含第一人称经历/数字≥3/真实场景）
  → INTEGRATE_QA（banned phrase 25 触发器检测 + 段落唯一度 + ≥7,500 词）
  → Cascade（writer→critic 最多 3 轮）
```

**红线**：脚本扩字数灌出来的模板文是已被归档的事故（781 篇 sludge），25 个 Banned Template-Phrase Registry 触发词直接 BLOCK。

**管线状态**：每篇内容是一个 pipeline item，从 S0-todo 一路推进到 done：

```bash
python3 ".../lovart-pipeline-state/pipeline_state.py" upsert --id blog-xxx --category blog
python3 ".../pipeline_state.py" advance --id blog-xxx --to S3-creating
python3 ".../pipeline_state.py" next      # 我下一步该干什么
```

非法跳步会被 exit 2 拒绝——这是特性不是故障。

## 4. 质量门禁

四道 bash 钩子（`1-4 Dev/scripts/hooks/`），BLOCK 即停：

| 钩子 | 时机 | 查什么 |
|------|------|--------|
| `pre-write-check.sh` | 写文件前 | 文件名 slug 格式 / 目录白名单 / frontmatter 必填 / 占位符 |
| `post-write-check.sh` | 写完后 | H2 密度 / 词数达标 / fluff 检测 / AI 自介 / 模板残留 |
| `pre-import-check.sh` | Sanity 导入前 | 状态机在 S4-ready / QA BLOCK 全 0 / 日期双写 |
| `post-generation-check.sh` | 生成后统一门 | 图片 404 / SEO 字段 / 结构化质量 / 脚本约束 / 质量自降 |

**Anti-Slop 底线**（RULES-00）：每段回答"谁会读/为什么现在读/读完改变什么/下一步"；禁编造产品数据、禁可见占位符、禁关键词堆砌；用户对 AI 味零容忍。

**三层门禁**（RULES-30）：L1 convert 前 preflight → L2 import 后 verify → L3 发布前 5 维审计。唯一质检父入口 `lovart-content-quality-gates`（sanity-preflight 已废弃并入）。

## 5. 发布与 Sanity 铁律

九条铁律全文见 `02-rules/RULES-00-iron.md`，最高频的五条：

1. 禁 `sanity deploy`
2. 禁 `--replace`——必须 `--missing` + patch 增量导入
3. 禁改 `schemaTypes/`、禁删 production 文档
4. **每次 import 前 preflight 必须 BLOCK=0**
5. **Blog 日期双写**：`releaseDate` + `publishedAt` 必须同时设（前端只读 releaseDate）

其他：修复优先于删除；多语言页面是需求不是垃圾；正文不进 LLM 上下文（NDJSON 磁盘流，CLI > MCP）。

**发布原则**：发布类动作停在 ready 等人工授权，不做无人值守自动发布。

**Sanity ID 对账**：`1-3 GenFlow/CONTENT_LINK_INDEX.md` 是 SSOT（注意：当前实际覆盖有限，Blog 对账以 `Lovart-Blog-Pipeline/BLOG_PUBLISHED_INDEX.md` 为准——两账合一在路线图上）。

## 6. 分发（四轨道）

轨道定义在 RULES-50，平台注册表 `1-3 GenFlow/Content Distribution/config/platforms.json`：

- **国内 Wechatsync**（知乎/百家号等）：浏览器扩展人工通道，不上服务器
- **海外 API**（DEV.to / GitHub Discussions / Blogger）：`scripts/publish-*.js`，需对应 API key 在 `.env`
- **海外爱贝壳**（Medium / X）：扩展草稿箱，人工确认
- **人工**（HackerNews 等）

**标准流程**：组 dispatch 单（`queue/dispatch-*.json`，参考 `dispatch-restart-2026-09-14-batch1.json`）→ `node scripts/dispatch-publish.js --manifest ... --dry-run` 干跑 → preflight 全过 → 用户把 `approved` 设 true → 去 `--dry-run` 真发。

**preflight 会拦什么**：正文缺 `utm_source={platform}` 追踪链接（AD-Tracking SSOT 要求）、缺 canonical、字数异常。稿件 UTM 化是发布前最后一公里，批量加工工具在 `1-3 GenFlow/AD-Tracking/url-builder/`。

## 7. 数据报告与监控

- **Trident**（`1-4 Dev/scripts/trident/`）：GSC/GA4/Bing 拉数。日拉 `gsc_fetch.py --daily`；数据落 `~/Documents/Lovart Local Dev/Output/Data Ingestion/`
- **Sentinel**（`1-4 Dev/scripts/sentinel/`）：每日 22 源舆情采集 + 日报，产出 `1-2 Insight/Lovart ORM/`
- **报告铁律**（RULES-10）：任何报告任何维度**必须有环比**（绝对变化+百分比）；不等长窗口用日均值；品牌词用 `lovart_brand_match.is_brand()` 精确分类；每节必须有 💡 洞察（问题/根源/缓解）
- **SSOT 归属**：SEO 月报 → `1-2 Insight/Trident Insights/reports/monthly/`；舆情 → `Lovart ORM/`；关键词 → `Keywords Research/`

## 8. 调度与运维

**macOS launchd**（当前生产）：`com.lovart.daily-pipeline`（08:00）/ `com.lovart.weekly-pipeline`（周一 07:00）/ `com.lovart.dream`（02:30）。plist 源在 `1-4 Dev/automation/plists/`，安装：

```bash
cp "1-4 Dev/automation/plists/com.lovart.daily-pipeline.plist" ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.lovart.daily-pipeline.plist
```

**每日管线步骤**（`run-daily-pipeline.sh`）：GSC 日拉 → Sentinel 采集+日报 → 飞书摘要（需凭据，可选）→ harness 学习报告 → 规则跨工具同步。

**Linux 服务器**：systemd timer 同一张时间表；MFlow 必须独立目录（`/var/www/mflow`）+ 独立 URL/server block，与 XMP/OpenFlow 完全隔离——详见 `deploy/server.md`。部署需用户明示授权。

**梦境（dream）**：每夜 consolidate（事实入记忆）+ audit（六维一致性审计，A1-A6）。手动跑：`bash "1-1 Harness/11-knowledge/dream/audit.sh" --no-write-today`。

## 9. 治理

**加新脚本（强制流程）**：先搜 `1-1 Harness/09-scripts/TOOLS-REGISTRY.md` 防重复 → 走 `lovart-new-tool-governance` skill → governance_check 6 门（命名/shebang/位置/docstring/无违规/smoke）→ 注册。不注册的脚本会在下次治理清理中归档。

**加/改技能**：改 `1-1 Harness/Skills/`（真相源）→ 跑 `harness_sync.py` 再生各工具运行时副本（.cursor/rules、~/.hermes 等）。每场景只有一个父入口，support-only 子技能标 `disable-model-invocation`。

**改规则**：RULES-00 是全局铁律，任何会话必载；工作线规则 RULES-10~60 按路由器指示加载。改规则后跑一次 audit 确认五个工具入口不打架。

**知识固化**：重要事实写 `11-knowledge/MEMORY-PROJECT.md`（带 ⚙️/✋/📌 来源标注）；会话结束写 session log；每夜 dream 自动整理。图查询：`bash "1-1 Harness/11-knowledge/scripts/kg" stats`。

## 10. 故障排查 FAQ

**Q：session-init 门禁挂了？**
GATE 1 挂 = `.pipeline/pipeline-state.json` 丢失 → `pipeline_state.py init` 重建。GATE 2 挂 = 路由器状态异常 → `router.py validate` 看明细。

**Q：gsc_fetch 报 ModuleNotFoundError: google？**
数据拉取必须用 trident-venv：`export LOVART_PYTHON=~/Documents/Lovart\ Local\ Dev/trident-venv/bin/python`，管线脚本会自动消费。

**Q：Sentinel 采集失败？**
看 `1-2 Insight/Lovart ORM/raw/{当日}/` 缺哪个源；个别源失败不阻塞其他源；凭证在 `sentinel/*_credentials/`。

**Q：launchd 任务没跑？**
`launchctl list | grep lovart` 看在册与上次退出码；日志 `~/Documents/Lovart Local Dev/Logs/com.lovart.*.log` 或 /tmp 对应 plist 的 StandardOutPath。

**Q：飞书推送 SKIP？**
正常降级——未配 feishu.json（`trident-data-engine/credentials/`），非致命。

**Q：报告断档了（某天没产出）？**
优先怀疑环境级事故：路径搬家 / launchd 被卸载 / python 被换。历史教训：fm-check 夜报断档 12 天才发现调度全停。恢复步骤见 session log `2026-09-14-harness-pipeline-restore.md`。

**Q：怎么确认我没把秘密提交进 git？**
`git grep -iE "ntn_|sk-[a-z0-9]{20}|BEGIN.*PRIVATE KEY"` 应零命中；secrets/ 与 credentials 目录已在 .gitignore，新增凭证位置记得同步 .gitignore。
