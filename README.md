<div align="center">

# MFlow

**内容生产管线：情报监测 → 内容生产 → 质量门禁 → 发布分发 → 数据回流（GEO 引用感知）**

![Language](https://img.shields.io/badge/Language-Python%203.12%2B-blue)
![Version](https://img.shields.io/badge/Version-1.2.0-green)
![Tests](https://img.shields.io/badge/%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95-125%2B-brightgreen)
![License](https://img.shields.io/badge/License-%E7%A7%81%E6%9C%89%E9%A1%B9%E7%9B%AE-lightgrey)

[官网](https://nownexts.com) · [快速上手](docs/quickstart.md) · [使用指南](docs/USAGE-GUIDE.md)

</div>

## 这是什么

你让 AI 帮你写内容，最怕三件事：写着写着跑偏了、质量越来越水、这次积累的经验下次归零。MFlow 把「AI 内容工厂」里最容易被糊弄的环节变成机器规则：进度由 12 阶段状态机记录，质量由可执行钩子把关，经验沉淀进知识树和项目记忆。人只看结果、只做一件事——授权发布。

它不是「又一个 AI 写文章工具」。市面工具帮你生成一篇，它管的是整条产线：选题来自真实数据（GSC/GA4/Bing + Sentinel 22 源舆情监控），成稿要过四道质量门禁，发布直接进你的 CMS（Sanity / WordPress / Webhook 多出口），发完还有周报月报告诉你哪篇带来了流量和 AI 引用。每一环都有测试与审计，不是演示脚本。

它正在生产环境干活，已验证的能力规模：

- Sanity production **8,247 篇文档**（EN 991 + i18n 多语言），Blog/News **10 种语言**全量，**3,000+ 落地页资产**
- 管线吞吐：单批次 43 篇 P0 刊文；404 修复战役累计 169+ 页（全部 HTTP 200 验证）
- 编排三件套测试：状态机 39/39 · hooks 16/16 · 路由器 15/15，另有控制台单元测试 55 项，合计 125+
- 路由器实测：相比单档案全量加载节省 86.7% token，零步骤漏失
- 每日管线：GSC 拉数 → Sentinel 22 源采集 → 舆情日报 → 规则同步，定时任务无人值守

整条产线一图看懂：

```
数据采集 (Trident: GSC/GA4/Bing + Sentinel: 22 源舆情监控)
    ↓
分析决策 (信号驱动选题 · 内容缺口 · 竞品覆盖 · 路由器派工)
    ↓
内容生产 (Blog / Landing / Tools / Features / Topic — 10 语言，重写而非翻译)
    ↓
质量门禁 (状态机管控 · 4 个质量 hook · Anti-Slop · 三层 L1/L2/L3)
    ↓
发布上线 (Sanity 增量导入 · Sitemap/IndexNow · 四轨道分发)
    ↓
效果回测 (SEO 周报/月报（强制环比）· 舆情日报 · GEO 引用缺口改稿)
```

## 核心能力

- **12 阶段管线状态机** —— 每篇内容在哪个阶段、下一步该谁，原子写入、非法转换直接拒绝（exit 2），进度从「猜」变成共享事实。
- **四道质量门禁钩子** —— 写前/写后/导入前 bash 检查 + Anti-Slop 规则 + 三层质量关（L1/L2/L3），BLOCK 就是 BLOCK，模型「善意绕过」行不通。
- **任务路由器** —— 23 条决策矩阵回答「这个任务该谁干、加载什么技能」，不用再靠人猜分工。
- **10 语言内容生产** —— Blog / Landing / Tools / Features / Topic 五类体裁，重写而非翻译，各语言按母语表达产出。
- **多出口发布** —— Sanity 增量导入、WordPress、Webhook 适配器，Sitemap / IndexNow 自动提交，四轨道分发。
- **GEO 引用感知回流** —— 探测 AI 引用缺口、生成改稿任务；SEO 周报/月报强制环比，效果说得清。
- **每日无人值守** —— GSC 拉数、22 源舆情采集、舆情日报、规则同步，launchd（macOS）/ systemd（服务器）定时运行；每夜自动整理项目记忆，经验隔夜不丢。
- **MCP 机器接口 + Web 控制台** —— 17 个 MCP 工具（检索内容库/知识库、查任务、跑预设强制 dry-run、看执行画布），Claude/Cursor/自研 Agent 可直接驱动；控制台与 MCP 同机运行（默认 `127.0.0.1:8088`）。
- **知识不流失** —— 知识树 + 项目记忆 + 会话审计，多个 AI 工具入口共享同一份事实，互不打架。

## 仓库结构

```
mflow/
├── 1-1 Harness/     控制中枢：7 份 RULES 铁律 · 45 个 Skill · 状态机/路由器/治理
│   └── 11-knowledge/   知识树 · 项目记忆 · 会话审计（单一事实源）
├── 1-2 Insight/     情报资产：SEO 报告 · 舆情 · 关键词 · 页面分析
├── 1-3 GenFlow/     创作层：内容日历 · 落地页生成 · 分发队列
├── 1-4 Dev/         工程层：脚本 · 质量钩子 · 自动化管线 · 部署
├── deploy/          服务器部署约定（独立目录 / URL / 端口 / 日志）
├── docs/            产品 / 快速上手 / 帮助中心 / MCP / 部署文档
└── secrets/         凭证（git 永不跟踪）
```

## 快速上手

```bash
# 依赖：Python 3.12+（推荐 uv venv，装 google-auth / googleapiclient / pyyaml / requests）
git clone https://github.com/sevenaaaaaaaaa/mflow.git && cd mflow

# 1) 会话启动门禁 —— 任何操作前先跑，4 道门禁全过才开工
bash "1-4 Dev/scripts/session-init.sh"

# 2) 配置凭证（可选：没有 key 也能跑 Demo 闭环）
#    Sanity / Notion token 放 secrets/（已 git-ignore）；
#    Trident / Sentinel 凭证目录同理；机器 token 在 run/env.sh 的 MFLOW_API_TOKEN

# 3) 看管线状态
python3 "1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/pipeline_state.py" summary

# 4) 问路由器：这个任务该谁干、加载什么技能
python3 "1-1 Harness/Skills/06-orchestrate/lovart-router/router.py" decide --stage S3 --scenario blog

# 5) 跑每日管线（GSC + Sentinel 舆情 + 规则同步）
bash "1-4 Dev/automation/run-daily-pipeline.sh"
```

第一件事建议从第 3 步开始：`summary` 会给你整条管线的当前快照。没有 Sanity/LLM API Key 也可以先跑通 Demo 闭环，完整路径见[快速上手 8 步](docs/quickstart.md)（约 30 分钟）。所有脚本按自身位置推导路径，clone 到任意目录即可运行，无需改硬编码。

目录速览：`1-1 Harness/` 控制中枢（铁律、Skill、状态机/路由器/治理）· `1-2 Insight/` 情报资产 · `1-3 GenFlow/` 创作层 · `1-4 Dev/` 脚本/钩子/自动化。

定时调度：本机 launchd 每日管线 08:00 / 每周管线 周一 07:00 / 每夜 02:30 整理项目记忆（plist 源在 `1-4 Dev/automation/plists/`）；服务器用 systemd timer 跑同一张时间表，见 [deploy/server.md](deploy/server.md)。

## 与 OpenFlow 的关系

MFlow 是 **OpenFlow 用户的进阶内容管线，亦可完全独立使用**：

- 只要内容产能 → MFlow 单独跑就成立，不依赖 OpenFlow 存在。
- 已经在用 OpenFlow → 挂在同一台机器上当内容产线：**OpenFlow 账号可直接登录**（账号体系直接继承，已迁移 13 个账号）；机器 API（`X-MFlow-Token`，GET-only）让 OpenFlow 拉取版本/状态/归因/引用缺口等只读数据；业务信号（订单/咨询热词）可喂给选题队列。
- 需要完整 CMS/交易后台 → OpenFlow 管前台与业务，MFlow 管内容产线，两者是同一台机器上的前台与产线，不是二选一。

联动有据可查：身份打通与只读机器 API 已上线；发布回流（成稿直收）、业务信号进选题、CDP 事件进归因属适配层就绪/规划中，逐家联调。三条纪律不因联动松动：机器 API 仅 GET；发布类动作永远人工授权；凭证不入 git。

## 使用指南

完整使用指南见 **[docs/USAGE-GUIDE.md](docs/USAGE-GUIDE.md)**。

配套文档：[产品介绍](docs/product.md)（为什么做、给谁看、值多少钱）· [帮助中心](docs/help-center.md)（会话协议/创作 SOP/质量门禁/发布铁律/故障排查）· [模块扩展](docs/modules.md)（新模块/接 CMS/接数据源/自我迭代）· [部署指南](docs/deploy-guide.md)（本地 / systemd / Docker 三条路径）· [MCP 接入](docs/mcp.md) · [产品路线图](ROADMAP.md)。

## 当前边界

- 当前为**私有仓库**，服务于 Lovart 内容团队生产环境，未附带开源许可证。
- WordPress 分发为骨架实现：发布端各家适配需逐家联调，「兼容度优先」是设计目标，不是已盖棺的测试结论。
- 触达闭环中 SEO 排名、社媒互动等传统指标取决于接入的数据源深度，属持续增强项，尚未满格。
- Sanity / Notion / Trident / Sentinel 凭证一律不入库（`secrets/` 与凭证目录已 git-ignore）。

## License

未附带开源许可证，当前为私有项目。如需授权使用，请联系 [nownexts.com](https://nownexts.com)。
