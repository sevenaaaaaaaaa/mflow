# MFlow

> **Lovart GEO 全自动内容营销工作流** —— 一套跑在真实生产环境的"情报监测 → 内容生产 → 质量门禁 → 发布分发 → 数据回流"闭环系统。
> 当前管理 Sanity CMS 生产库 8,200+ 文档、10 种语言、3,000+ 落地页资产；核心编排组件带 70+ 个自动化测试。

---

## 这是什么

MFlow 不是"AI 写文章的脚本"。它是一套**内容工厂的治理系统**：

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
效果回测 (SEO 周报/月报（强制环比）· 舆情日报 · 审计回流)
```

它解决三个 AI 内容生产的经典失控问题：

- **跑偏** —— 多 agent 接力时"上一步是谁、下一步该谁"全靠猜。MFlow 用 12 阶段状态机（`pipeline_state.py`，原子写、非法转换 exit 2）把进度变成共享事实。
- **自降质量** —— 模型会"善意绕过"文本规则。MFlow 把铁律做成可执行钩子：写前/写后/import 前四道 bash gate + 23 条决策矩阵路由器，BLOCK 就是 BLOCK。
- **知识流失** —— 会话结束经验归零。MFlow 用知识树 + 项目记忆 + 每夜梦境整理（consolidate/audit）让事实沉淀、让五个 AI 工具入口互相不打架。

## 真实生产数据（截至 2026-09）

- Sanity production：**8,247 文档**（EN 991 + i18n 多语言），Blog/News 10 语全量
- 管线吞吐：单批次 43 篇 P0 刊文、404 修复战役累计 169+ 页（全部 HTTP 200 验证）
- 编排三件套测试：状态机 39/39 · hooks 16/16 · 路由器 15/15
- 路由器实测：相比单档案全量加载**节省 86.7% token，0 步骤漏失**
- 每日管线：GSC 拉数 → Sentinel 22 源采集 → 舆情日报 → 规则同步，launchd 无人值守

## 仓库结构

```
MFlow/
├── 1-1 Harness/     控制中枢：7 份 RULES 铁律 · 45 个 Skill · 状态机/路由器/治理
│   └── 11-knowledge/   知识树 · 项目记忆 · 梦境审计 · 会话日志（SSOT）
├── 1-2 Insight/     情报资产：SEO 报告 · 舆情 · 关键词 · 页面分析
├── 1-3 GenFlow/     创作层：内容日历 · 落地页生成 · 分发队列
├── 1-4 Dev/         工程层：脚本 · 质量钩子 · 自动化管线 · 部署
├── deploy/          服务器部署约定（独立目录/URL，见下）
└── secrets/         凭证（git 永不跟踪）
```

## 快速开始

```bash
# 0) 依赖：Python 3.12+（推荐 uv venv，装 google-auth/googleapiclient/pyyaml/requests）
# 1) 会话启动门禁 —— 任何操作前先跑，4 道门禁全过才开工
bash "1-4 Dev/scripts/session-init.sh"

# 2) 看管线状态
python3 "1-1 Harness/Skills/06-orchestrate/lovart-pipeline-state/pipeline_state.py" summary

# 3) 问路由器：这个任务该谁干、加载什么技能
python3 "1-1 Harness/Skills/06-orchestrate/lovart-router/router.py" decide --stage S3 --scenario blog

# 4) 跑每日管线（GSC + Sentinel + 规则同步）
bash "1-4 Dev/automation/run-daily-pipeline.sh"
```

所有脚本按自身位置推导路径，clone 到任意平铺目录即可运行，无需改硬编码。

## 调度

本机 launchd（macOS）：每日管线 08:00 / 每周管线 周一 07:00 / 梦境整理 02:30，plist 源在 `1-4 Dev/automation/plists/`。服务器形态为 systemd timer（同一张时间表），部署约定见 [`deploy/server.md`](deploy/server.md)。

## 文档

- [产品介绍](docs/product.md) —— 面向业务：为什么做、给谁看、值多少钱
- [帮助中心](docs/help-center.md) —— 面向操作者：会话协议、创作 SOP、质量门禁、发布铁律、故障排查
- [部署接线](deploy/server.md) —— 服务器目标、隔离要求、形态约定
- 内部深水区：`1-1 Harness/00-INDEX.md`（控制中枢索引）→ `11-knowledge/`（知识/记忆/审计 SSOT）

## 状态与边界

- 当前为**私有仓库**，服务于 Lovart 内容团队生产环境
- 凭证一律不入库：Sanity/Notion token 在 `secrets/`（已 git-ignore），Trident/Sentinel 凭证目录同理
- 通用内核（状态机/路由器/钩子/治理）与品牌配置解耦中，开源抽取路线见 docs/product.md 结语
