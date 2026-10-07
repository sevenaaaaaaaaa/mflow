# Refly 深度测评：开源 Agent Skills 构建器，能替 n8n 还是替 MCP？

> T2 深度测评 · Agent Skills · 2026  
> GitHub：https://github.com/refly-ai/refly ⭐ 7471  
> 托管版：https://refly.ai · 自部署文档：https://docs.refly.ai/community-version/self-deploy/  
> 许可证：GitHub 显示 NOASSERTION · 仓库内为 ReflyAI Open Source License（Apache 2.0 + 附加限制）  
> CLI：@powerformer/refly-cli

---

## 👤 测评人背景

我同时在 Cursor 里写代码、在飞书群里收审批、偶尔还要把一段 SOP 变成「Agent 能反复调用的技能」。纯手写 MCP 服务器能控，但维护成本高；n8n 画流程很快，导出到 Claude Code 里当工具用却别扭。Refly 进清单，是因为 GitHub 自述 **「首个开源 Agent Skills 构建器」**——Skills 被定义成持久化基础设施，而不是一次性 Prompt。下面按仓库 README、自部署文档和夹内笔记拆；**未在撰写日完整压测 3000+ 工具集成与 Vibe 模式全边界，不写虚构 QPS 或「3 分钟必成」类测速**。

---

## 🎯 先说结论

Refly 是一个 **可视化 + 可导出** 的 Agent Skills 构建平台：在 IDE 里用拖拽或 Vibe 自然语言生成工作流，编译为可版本控制的 Skill，再导出到 Cursor、Claude Code、Codex，或作为 REST API / Webhook 给 Lovable 类前端调用。它强调 **可干预运行时**——执行中可以暂停、审计、改步骤——以及 **3000+ 原生工具 + MCP** 接入。

与 n8n/Dify 的重叠在「画流程」，差异在 **输出形态**：Refly 要把流程变成可移植的 Skill 资产，分发到不同 Agent 运行时；n8n 更偏「触发自动化黑盒」。与手写 MCP 比：Refly 用 Copilot 把意图编译成 DSL，少写样板代码，但复杂定制仍可能不如纯代码自由。

**我的决策句：如果你要把企业 SOP 固化成跨 Cursor/Claude Code 可调用的 Skill，并愿意自部署或读清许可证，可以优先跑通社区版 Docker；如果只要 cron 触发邮件、不想碰 Agent 导出，或看到 Apache-2.0 就默认能闭源商用，不建议跳过 LICENSE——ReflyAI Open Source License 有附加限制，商用前必须通读全文。**

---

## 📦 Refly 是什么？

一句话：**Skills 不是 Prompt，是持久化基础设施。** 你在 Refly 里描述或拖拽出一段业务逻辑（查 CRM、走审批、调 Stripe、搜网页再汇总），平台把它编译成确定性更高的 Skill 单元，注册进 Skill Registry，再 **导出** 到不同运行时——而不是锁死在 Refly 这一台实例里。

交付形态分三层：  
1. **Refly 托管 refly.ai** —— 最快上手；  
2. **Docker 自部署** —— 文档入口 https://docs.refly.ai/community-version/self-deploy/ ，默认本地端口笔记口径 localhost:5700；  
3. **CLI @powerformer/refly-cli** —— 偏 Skill 安装与发布，高级编排仍在完善。

与 LangChain 的区别：LangChain 是代码框架，你在 Python/TS 里拼链；Refly 是 **带 IDE 的构建器 + 导出器**，面向「不想先写二百行胶水代码」的团队。与手写 MCP 的区别：MCP 你自己管 schema、传输、鉴权；Refly 提供工具目录和编译路径，但 **极端自定义协议** 仍可能回到手写。

> 📷 **配图待补**：Refly 官网/GitHub 首页（`images/Refly-homepage.png`）

> 📷 **配图待补**：Workflow IDE 主界面（`images/Refly-main-ui.png`）

> 📷 **配图待补**：SOP → Skill 编译 → 导出 Cursor/Claude Code/API，流程示意（`images/Refly-schematic-overview.png`）

```
[业务 SOP / 自然语言意图]
    ↓ Refly IDE（画布 or Vibe 模式）
[编译为 Skill DSL · 版本注册]
    ↓ 导出
[Cursor / Claude Code / Codex / REST / Webhook / 飞书 Slack Bot]
```

---

## 🧩 Refly 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| Skill IDE | 空白画布拖拽节点，或 Vibe 模式用自然语言生成工作流 | 从 0 到可跑原型快，不必先写 MCP 样板 |
| 可干预运行时 | Run 时可看中间结果、暂停、修正再继续 | 合规场景要「人在回路」，不是触发即黑盒 |
| 3000+ 工具 + MCP | Stripe、Slack、Salesforce、GitHub 等原生集成，完整 MCP 协议 | 少自己写 OAuth 胶水（视具体工具而定） |
| 多形态导出 | Cursor/Claude Code/Codex Skill、REST API、Webhook、飞书/Slack Bot | 同一 Skill 多入口，不必为每个 Agent 重画一遍 |

### Skill IDE：画布与 Vibe 双入口

「New Workflow」可以选 **空白画布**：网页搜索 → LLM 分析 → 格式化输出，节点连线清晰，适合已经知道步骤的 SOP。**Vibe 模式**用自然语言描述需求，由 Copilot 生成初版流程——适合探索期，但 **生产环境必须在生成后再做节点级微调**（下文实测会讲可靠性边界）。

> 📷 **配图待补**：画布编排与 Vibe 生成对比（`images/Refly-feature-ide.png`）

### 可干预运行时：和 n8n 的真正分叉

n8n 常见心智是「触发 → 全自动跑完」；Refly 强调 **Intervenable Runtime**——某一步 LLM 输出离谱时，你可以暂停、改参数或改上下文，再继续。对财务审批、对外客服、带合规审计的内部流程，这比「跑完再看日志」更贴需求。

> 📷 **配图待补**：运行时逐步审计界面（`images/Refly-feature-runtime.png`）

### 导出与 CLI

导出到 Cursor/Claude Code 后，编程 Agent 把 Skill 当 **可调用工具**，而不是每次重读一长段 Prompt。REST/Webhook 则给 Lovable 类前端或飞书机器人当后端。CLI `@powerformer/refly-cli` 当前笔记口径以 **技能安装和发布** 为主，复杂 CI/CD 编排别预期一步到位。

---

## 🧠 核心逻辑：它为什么不一样？

Prompt 方案的问题：同一个 SOP，换模型、换 IDE、换同事，就要复制粘贴改一遍，版本不可审计。Refly 的路径：**意图 → 编译为 Skill DSL → 注册 → 导出**——Skill 像基础设施包，Prompt 像一次性便签。

三拍：**构建 → 注册版本 → 分发运行时**。值不值得留，看 Skill 能否跨环境复用、失败能否局部重跑、许可证是否允许你的商用形态——不是看 Vibe 演示漂不漂亮。

**机制层怎么选**：要 **Agent 工具化 + 可干预**，认真试 Refly；要 **定时 ETL/通知**，n8n 可能更轻；要 **协议级完全掌控**，手写 MCP 或 LangChain 代码仍是最硬的路。

> 📷 **配图待补**：Prompt vs Skill 基础设施，分层示意（`images/Refly-architecture-flow.png`）

---

## ⚔️ Refly 和 n8n/Dify、手写 MCP、LangChain 有什么区别？

| 维度 | Refly | n8n / Dify | 手写 MCP | LangChain |
|------|-------|------------|----------|-----------|
| 核心产出 | 可导出 Agent Skill | 实例内工作流/应用 | 自定义 MCP 服务器 | 代码链与 Agent |
| 运行时干预 | 强调可暂停审计 | 偏全自动触发 | 取决于自实现 | 取决于自实现 |
| 跨 Agent 复用 | 导出 Cursor/Claude Code/Codex | 绑定平台实例 | 任何支持 MCP 的客户端 | 任意 Python/TS 项目 |
| 上手曲线 | IDE + Vibe，较低 | 低~中 | 高（协议+鉴权） | 中~高（代码） |
| 工具生态 | 3000+ 原生 + MCP | 丰富插件市场 | 自建 | 社区集成 |
| 许可注意 | ReflyAI License 附加条款 | 各产品不同 | 自决 | 开源库组合 |

选型句：要把 **SOP 变成 Cursor/Claude Code 里可调用的 Skill 资产**，优先 Refly；要 **cron 发邮件、同步表格**，n8n 往往够用；要 **完全自定义传输与 schema**，手写 MCP；要 **深度代码集成、科研级灵活**，LangChain 代码栈更直接。

> 📷 **配图待补**：四类方案对照示意（`images/Refly-vs-competitor.png`）

---

## 🧪 我实际跑下来的体验

说明：综合 GitHub README、自部署文档与公开 FAQ 口径；**未在撰写日对全部 3000+ 集成做连通性矩阵，不编造执行耗时**。

### ✅ 好的方面

**1. 定位句清晰：Skills 是基础设施，不是 Prompt**  
对受够了「每个项目复制同一段 system prompt」的团队，这是可操作的架构语言，不是口号。

**2. 导出形态覆盖「开发」和「业务入口」**  
同一 Skill 既能进 Cursor，又能变 REST/Webhook 给飞书——减少「为 Slack 再画一张 n8n 图」的重复。

**3. 可干预运行时贴合规场景**  
对外动作前能暂停看一眼 LLM 输出，比纯黑盒自动化更适合有审计要求的内部流程。

**4. 社区热度可核对**  
GitHub ⭐7471（以仓库当日为准），Issues/PR 活跃面明显大于小玩具项目；自部署文档独立托管，和 refly.ai 托管版分工清楚。

### ❌ 不好的方面

**1. 许可证不能当 MIT 一扫而过**  
GitHub 许可证字段显示 **NOASSERTION**；仓库内实际为 **ReflyAI Open Source License（Apache 2.0 + 附加限制）**。商用、闭源分发、SaaS 再包装 **必须通读 LICENSE**——「看着像 Apache 就能随便卖」是常见误判。

**2. 自部署不含 LLM，成本与复杂度外置**  
Docker 社区版默认 localhost:5700，笔记口径最低约 2 核 CPU、4GB RAM；但 **模型推理要自备 OpenAI/Anthropic 等 Key**，token 花费随工作流复杂度波动。Refly 的 DSL 设计声称能省 token，**我没有实测对比数据**，不当承诺。

**3. Vibe 模式适合原型，不适合无脑上生产**  
自然语言生成的工作流在边界条件（空结果、权限失败、分页、幂等）上容易漏节点。官方 FAQ 口径也是：Vibe 加速 0→1，生产要 **节点级精调 + 反复测试 + 审计日志**——偷懒直接上线，翻车概率高。

**4. Skills 生态仍早期**  
官方与社区 Skill 覆盖场景有限；冷门内部系统往往还得自己接 MCP 或写自定义节点——「3000+ 工具」不等于「你的 ERP 已经开箱即用」。

**5. CLI 能力还在长**  
@powerformer/refly-cli 笔记口径偏安装发布，高级编排、完整 GitOps 式流水线别预期已经成熟；重度 CLI 党可能觉得不如纯代码仓库直观。

**6. 与 n8n 重叠但不可替代**  
如果你只需要「每周五导出 CSV 发邮件」，Refly 是大炮打蚊子；硬上 Skill 导出反而增加学习成本。

我真实会留它的场景：把「内容审核 SOP」固化成 Skill，导出到 Cursor，写稿 Agent 在提交前自动跑一遍检查清单，中途能暂停改规则。我会暂时绕开的场景：法务还没读完 ReflyAI License 附加条款，团队就要把 Skill 嵌进对外 SaaS——这种先别部署。

> 📷 **配图待补**：一次 Workflow Run 与导出预览（`images/Refly-hands-on.png`）

---

## 💡 怎么高效用它

### 用法 1：自部署最小路径——Docker + 模型 Key

按 https://docs.refly.ai/community-version/self-deploy/ 起容器，首次登录注册，配置 OpenAI/Anthropic 等提供商。先做一个 **三步内** 工作流：搜索 → LLM 摘要 → 固定 JSON 输出，跑通可干预运行时，再叠工具节点。**别第一天就 Vibe 生成二十步流程。**

> 📷 **配图待补**：Docker 部署与首次登录（`images/Refly-usage-1.png`）

### 用法 2：Vibe 生成 → 人工审计 → 导出 Cursor

Vibe 描述意图后， **逐步检查** 每个节点的输入输出 schema、错误分支、重试策略。测试用真实脏数据（空列表、超时、403），不是只用 Demo 句子。满意后再导出 Cursor Skill——编程 Agent 调用的是你的 **审计过** 的版本，不是 Copilot 初稿。

### 用法 3：与 Lovart 分工——Refly 管流程 API，Lovart 管视觉交付

若你用 Lovart 生成活动页或 App 壳，Refly 的 REST 导出可以充当 **后端工作流 API**（例如提交 brief → 检索 → 结构化字段）。视觉稿在 Lovart 定稿，业务逻辑在 Refly 定稿，两者通过 API 拼接——**别指望 Refly 替你出图，也别指望 Lovart 替你跑 Stripe 扣款**。

> 📷 **配图待补**：Refly API + 前端/Lovart 分工示意（`images/Refly-usage-2.png`）

---

## ⚠️ 安装和使用需要注意什么？

### Refly 和 n8n 最大区别是什么？（FAQ 口径）

n8n 本质是 **可视化自动化触发器**，流程常绑定在单一实例，跨环境复用要额外导出导入。Refly 把流程 **编译为可移植 Agent Skill**，目标运行时包括 Claude Code、Cursor、独立 API。另一点：Refly 强调 **执行中干预**；n8n 典型路径是触发后全自动。

### 自部署需要什么资源？（FAQ 口径）

笔记与文档口径：**最低约 2 核 CPU、4GB RAM，推荐 Docker**。Refly 本身不包含 LLM，需配置 OpenAI/Anthropic 等 Key；执行 token 消耗取决于节点数量与模型选择。精简 DSL 设计有助于控成本，但 **具体比例未实测**，建议用小流量影子环境先跑账单。

### Vibe 模式可靠吗？（FAQ 口径）

适合 **快速原型**，不适合未经审计直接上生产。应在 Vibe 生成后做节点级调整，并用测试覆盖边界；配合 Refly 的测试与审计日志做回归。把 Vibe 当「一键上线」，是对产品心智的误读。

### 许可证：商用前读 LICENSE，勿只当 MIT

GitHub 许可证显示 NOASSERTION，以仓库 **LICENSE 文件** 为准：**ReflyAI Open Source License = Apache 2.0 + 附加限制**。自用研究通常清晰；**商用部署、再分发、SaaS 封装** 必须法务过一遍附加条款。Apache-2.0 的专利 grant 不能自动替附加限制背书。

### 数据与 Key 安全

自部署版 API Key 在你侧管理；接 Slack/Stripe/GitHub 等 OAuth 时，令牌存储策略以部署配置为准。团队场景：**Key 不进聊天记录、Skill 版本进 Git、生产与实验环境分离**。

> 📷 **配图待补**：模型提供商配置与权限（`images/Refly-note-permission.png`）

---

> **怎么选：** 要把 **SOP 编译成跨 Cursor/Claude Code 的 Skill 且需运行时干预**，可以 **优先** 试 Refly 社区版或托管版；若只要 **定时自动化、无 Agent 导出需求**，**不建议** 用 Refly 替代 n8n；若 **未读 ReflyAI Open Source License 附加条款就要商用**，**不建议** 部署——先做法务确认，别按 MIT 心智签合同。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| 要把内部 SOP 变成 Agent 可调用 Skill 的团队 | 版本化 + 导出多运行时 |
| Cursor / Claude Code 重度用户 | 直接导出为编程 Agent 工具 |
| 需要可干预、可审计自动化的合规场景 | 运行时暂停与中间结果 |
| 有 Docker 运维能力、可自备 LLM Key 的团队 | 自部署路径完整 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 仅偶尔 ChatGPT 网页聊天 | 门槛与场景不匹配 |
| 只要 cron 级简单自动化 | n8n 更轻 |
| 不愿读许可证附加条款的商用团队 | ReflyAI License 有额外限制 |
| 极端定制协议、要代码级掌控一切 | 手写 MCP / LangChain 更直接 |

> 📷 **配图待补**：典型 Skill 分发场景示意（`images/Refly-who-workflow.png`）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | Docker 可复现；模型 Key 与 OAuth 是变量 |
| 核心能力 | ⭐⭐⭐⭐ | Skill 导出 + 可干预运行时切口准 |
| 速度/规模 | ⭐⭐⭐ | 受 LLM 与工具链影响；本稿不编造测速 |
| 文档/社区 | ⭐⭐⭐⭐ | 自部署文档 + ⭐7471 社区 |
| 成本 | ⭐⭐⭐ | 软件许可需细读；token 按量另算 |

**综合评分：3.7 / 5.0**（Agent 基础设施分，不是「自动化大全」榜）

> **一句话总结**：Refly 适合把 SOP 做成 **可导出、可干预、可版本化** 的 Agent Skill——它补的是 Cursor 与 n8n 之间的形态缝；简单 cron、未读 LICENSE 就商用，别选它。

---

## 🔗 Refly 官网与项目地址

- **GitHub 仓库**：https://github.com/refly-ai/refly  
- **托管版**：https://refly.ai  
- **自部署文档**：https://docs.refly.ai/community-version/self-deploy/  
- **CLI**：npm `@powerformer/refly-cli`  
- **对照竞品**：n8n · Dify · 手写 MCP · LangChain  
- **视觉互补**：Lovart https://www.lovart.ai/

---

**标签**：#AI工具 #AgentSkills #Refly #MCP #T2单品
