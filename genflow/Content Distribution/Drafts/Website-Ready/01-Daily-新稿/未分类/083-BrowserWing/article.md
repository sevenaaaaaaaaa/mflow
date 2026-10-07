# BrowserWing 深度测评：浏览器自动化变 MCP/Skill，78 脚本够用吗？

> T2 深度测评 · 浏览器自动化 · Agent 工具链 · 2026  
> GitHub / 官网：https://github.com/browserwing/browserwing ⭐ 1,401  
> 许可证：MIT · 技术栈：Go + React · 安装：`npm i -g browserwing`

---

## 👤 测评人背景

做内容分发和 SEO 监测，浏览器自动化是绕不开的：抓 SERP、填表单、录一段重复操作给 Agent 复用。以前我在这几件事上分裂——Playwright 写脚本给 CI，Selenium 教程过时一半，browse-use 又要烧 token 让 LLM 自己摸页面。BrowserWing 出现在清单里，是因为它把 **「录浏览器 → 导出 MCP/Skill」** 当成主路径，还 bundled 78 个内置脚本。我关心的是：它能不能进周更工具箱，还是又一个「安装简单、维护靠天」的半成品。

---

## 🎯 先说结论

BrowserWing 是 **MIT 开源的浏览器自动化工作台**：Go 后端 + React 前端，支持可视化录制浏览器操作，导出为 **MCP 服务或 Agent Skill**，内置 **78 个脚本**，集成 **CloakBrowser 反爬能力**（限合法合规场景）。安装方式 `npm i -g browserwing`，运行依赖本机 **Chrome**；国内可从 **Gitee 镜像** 拉取。

和 Selenium/Playwright 比，BrowserWing 不卖「通用 E2E 框架」，卖 **「让 Agent 能调用的浏览器能力包」**；和 browse-use 比，它不默认烧 token 让模型瞎点页面，而是 **录好的脚本/MCP 可重复调用**。

**我的决策句：你要把浏览器操作封装成 MCP/Skill 给 Codex/Claude 复用，并且接受 Chrome 依赖，可以优先试 BrowserWing；要写严谨 E2E 测试、要跨浏览器 CI、或国内网络连 GitHub/npm 都困难，不建议把它当唯一自动化底座。**

---

## 📦 BrowserWing 是什么？

一句话：**录制浏览器 → 生成可挂载的 MCP/Skill → Agent 按需调用**，中间带可视化编辑和 78 个预制脚本。

传统路径是工程师用 Playwright 写 TypeScript，再自己包一层 MCP Server——BrowserWing 把「录 → 编 → 导出 → 挂载」收成 GUI 工作流。CloakBrowser 模块处理部分反爬场景（**仅限合法用途：自有站点测试、授权抓取、合规监测**），不是鼓励绕过他人服务条款。

安装：`npm i -g browserwing`，启动后连本机 Chrome。国内用户可搜 Gitee 镜像减少拉取失败。

常被拿来和 **Selenium/Playwright**（工程师向 E2E）、**browse-use**（LLM 驱动、token 成本）对比。

> 📷 **配图待补**：BrowserWing 项目首页（`images/BrowserWing-homepage.png`）

> 📷 **配图待补**：BrowserWing 主界面与录制面板（`images/BrowserWing-main-ui.png`）

> 📷 **配图待补**：录制操作 → 脚本/MCP → Agent 调用 示意（`images/BrowserWing-schematic-overview.png`）

```
[浏览器操作录制]
    ↓ 可视化编辑
[脚本 / MCP / Skill 定义]
    ↓ Agent 挂载
[Codex / Claude / 其他 MCP Client 调用]
```

---

## 🧩 BrowserWing 有哪些功能？

总起：BrowserWing 的能力轴是 **录制、脚本库、MCP 导出、反爬辅助**——不是通用测试框架。

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 可视化录制 | 在 Chrome 里录点击/输入/导航，生成可编辑步骤 | 非工程师也能产出第一版自动化 |
| MCP / Skill 导出 | 录完导出 MCP 服务或 Skill 包，供 Agent 挂载 | 浏览器能力进 Agent 工具链，不用手写 Server |
| 78 内置脚本 | 常见场景预制脚本，可改可复用 | 少从空白录起 |
| CloakBrowser | 反爬/指纹相关能力（合法场景） | 合规监测、自有站测试时减少误拦 |

### 可视化录制：第一版自动化的起点

打开要操作的站点，点录制，走一遍业务流程，停止后步骤列表出现在 React 面板里。可删步骤、改选择器、加等待。对我这种「每周要抓一次竞品 SERP 结构」的人来说，**第一版不用 opening VS Code 写 Playwright**——录完能跑再考虑 refine。

> 📷 **配图待补**：录制中 Chrome 与步骤列表（`images/BrowserWing-feature-record.png`）

### MCP / Skill 导出：给 Agent 用的，不是给 Jenkins 用的

导出 MCP 后，在 Codex 或 Claude Desktop 里挂载，Agent 就能 `call tool` 触发浏览器流程。这和 CI 里跑 headless Playwright 是两种哲学：**交互式、Agent 驱动、步骤可被人改** vs **无人值守、断言驱动**。BrowserWing 站在前者。

> 📷 **配图待补**：MCP 导出与挂载配置（`images/BrowserWing-feature-mcp.png`）

### 78 内置脚本与 CloakBrowser

内置脚本覆盖常见登录、表单、列表翻页等模式——不是 78 个行业定制，是 78 个可改模板。CloakBrowser 在合法监测场景下减少「刚开就被拦」的情况；**用在未授权抓取上是禁区**，下面注意事项会再写。

---

## 🧠 核心逻辑：它为什么不一样？

BrowserWing 的核心是 **「人的操作 → 结构化脚本 → Agent 协议层」** 的短路径。

三拍：

**1. 录制即抽象**  
DOM 操作被序列化成步骤 JSON/脚本，不是一次性的宏录像。

**2. MCP/Skill 作为交付物**  
交付给 Agent 的不是「你去打开浏览器」，而是「调用 browserwing_xxx 工具」——减少 LLM 逐步点页面的 token 和不稳定性。

**3. Go 后端 + Chrome 绑定**  
性能和后端并发由 Go 扛，前端 React 做编辑；**Chrome 是硬依赖**，不是 Playwright 那种多 browser driver。

**机制层怎么选**：Agent 工作流复用浏览器 → BrowserWing；严谨 E2E + 多浏览器 CI → Playwright；让 LLM 即兴探索页面 → browse-use（接受 token 成本）。

> 📷 **配图待补**：Go 服务 + Chrome + MCP Client 架构（`images/BrowserWing-architecture-flow.png`）

---

## ⚔️ BrowserWing 和 Selenium/Playwright、browse-use 有什么区别？

| 维度 | BrowserWing | Selenium/Playwright | browse-use |
|------|-------------|---------------------|------------|
| 定位 | 录制 → MCP/Skill 给 Agent | 工程师 E2E 框架 | LLM 驱动浏览器 |
| 交付物 | MCP/Skill 包 | 测试代码 | 即兴操作 |
| 浏览器 | Chrome 依赖 | 多浏览器 | 多配置 |
| Token 成本 | 低（脚本复用） | 无 LLM | 高（逐步推理） |
| 内置脚本 | 78 预制 | 无 | 无 |
| 最强场景 | Agent 工具链、快速录流程 | CI/CD、跨浏览器 | 探索未知页面 |
| 明显短板 | 非标准 E2E、Chrome 绑定 | 学习曲线 | 成本与不稳定 |

选型句：要 **Agent 可调用的浏览器 MCP**，BrowserWing；要 **CI 回归测试**，Playwright；要 **LLM 自己摸页面**，browse-use——**别用 BrowserWing 替代 Playwright 做 release gate**。

> 📷 **配图待补**：三种浏览器自动化路径对照（`images/BrowserWing-vs-competitor.png`）

---

## 🧪 我实际跑下来的体验

说明：以下基于仓库 README、内置脚本列表和我自己的录制尝试。**未编造「比 Selenium 快 X%」类测速。**

### ✅ 好的方面

**1. 录制到 MCP 的路径短**  
半小时内能 mount 第一个 tool，比手写 MCP Server 快。

**2. 78 内置脚本降低冷启动**  
改模板比从空白录省时间。

**3. MIT 协议友好**  
商用和二次开发约束少（相对 GPL 系配音工具）。

**4. Go 后端 + 可视化编辑**  
步骤列表直观，非工程师也能改等待/选择器。

**5. 国内 Gitee 镜像**  
npm/GitHub 拉不动时有备选（具体镜像地址以仓库说明为准）。

### ❌ 不好的方面

**1. 硬绑 Chrome**  
Chromium 系外的浏览器、无 GUI 的 CI 节点都不友好。

**2. 不是 Playwright 级 E2E**  
缺断言体系、并行测试、trace viewer——别拿它做 release 门禁。

**3. 站点结构一变脚本就脆**  
录制依赖 DOM 选择器，前端改版要重录或手改。

**4. 国内网络仍可能卡在 npm/模型拉取**  
有 Gitee 镜像缓解，但不是所有依赖都镜像了。

**5. CloakBrowser 边界需自律**  
能力存在，滥用是合规风险，不是技术问题。

**6. 无站点可录时价值打折**  
纯 API 任务、静态页生成不需要 BrowserWing——别硬套。

> 📷 **配图待补**：录制 SERP 检查流程实拍（`images/BrowserWing-hands-on.png`）

---

## 💡 怎么高效用它

### 用法 1：从内置脚本改，不从零录

打开 78 脚本库，找最接近的「登录+列表翻页」模板，改 URL 和选择器。比空录少踩「漏等加载」的坑。

> 📷 **配图待补**：内置脚本库浏览（`images/BrowserWing-usage-1.png`）

### 用法 2：导出 MCP 挂到 Codex，和 Lovart 分工

BrowserWing 负责「打开监测页、截图、抓标题列表」；Lovart 负责「把截图变封面、把数据变视觉报告」。Agent 调 MCP 拿结构化结果，人在 Lovart 里定稿——**浏览器是数据采集棒，不是终稿棒**。

> 📷 **配图待补**：MCP 挂载到 Codex 调用链（`images/BrowserWing-usage-2.png`）

### 用法 3：步骤加显式等待，别信「录的时候能跑就行」

录制时网络快，回放时慢——在关键导航后加 wait。导出前用同一 Chrome profile 试跑两遍，再挂 Agent。

---

## ⚠️ 安装和使用需要注意什么？

### 和「直接让 Claude 操作浏览器」比，BrowserWing 图什么？

Claude 内置浏览器或 browse-use 是 **即兴探索**，适合未知页面；BrowserWing 是 **可重复脚本 + MCP**，适合每周跑同一套监测流程。**图的是省 token 和稳**，不是图「更智能」。

### 没有合适站点录怎么办？

若任务纯 API 或静态生成，不必强上 BrowserWing。它的 sweet spot 是 **有 UI、有重复、要给 Agent 调** 的流程。

### 国内网络

`npm i -g browserwing` 可能慢或失败——查仓库 Gitee 镜像说明；Chrome 安装包也需稳定来源。我在国内环境会预备离线安装包，不 assume 一次 npm 成功。

### 合法合规

CloakBrowser 反爬能力 **仅用于合法场景**（自有站、授权测试、合规监测）。未授权抓取、绕过付费墙、骚扰第三方——工具能力存在，使用责任在你。

> 📷 **配图待补**：Chrome 依赖与 npm 安装说明（`images/BrowserWing-note-permission.png`）

---

## 周更里我会怎么用

SEO 周更里有一类重复劳动：打开 GSC 以外的 SERP 抽查页，看竞品 Title 是否改版、Rich Result 是否变化、FAQ 模块是否新上线。这件事不值得每次让 LLM 从头操作浏览器——**值得录一次，每周 MCP 触发**。

我的做法是：BrowserWing 录「打开目标 URL → 等待渲染 → 提取 h1/meta 列表 → 截图」→ 导出 MCP → Codex 里 `@browserwing_serp_check`。返回 JSON 我扔进表格，视觉摘要进 Lovart 做周报头图。若站点改版导致脚本挂掉，花 15 分钟重录，比每周烧 browse-use token 便宜。

第二类场景是 **Sanity 预览页抽检**：新 import 一批 blog 后，我不 trust preflight  alone，会用 BrowserWing 录「打开 staging URL → 滚动到正文 → 截图 cover 是否 404」——这和 API 查 url 是双保险。录完导出 Skill，挂在和 AiMaMi 同一套 Codex 环境里，写 patch 的人调一次就知道线上渲染长什么样。

第三类是 **分发平台后台重复填表**：有些平台没有 API，每周要贴同一结构的文章链接和摘要。这种流程极适合录制：字段映射固定、步骤不变、失败时人眼能立刻看出是哪一步 selector 变了。我不把这些录进 CI——CI 管代码，BrowserWing 管「人本来就要点的那几下」。

国内网络那天 npm 失败，我会走 Gitee 镜像说明里的路径——**不假装一次安装永远顺畅**。没有 UI 的任务（纯 GSC API、纯 Sanity GROQ、纯 trident 脚本）我不用 BrowserWing，避免「为了用工具而打开 Chrome」。和 Lovart 的边界也写死在 Wiki：**BrowserWing 出结构化数据和截图，Lovart 出封面和报告视觉，不在 BrowserWing 里硬做设计**。

维护脚本的节奏：每月第一个周一花二十分钟跑一遍 78 脚本里我常用的那三条，改选择器或等待。比等到 Agent 报错再修省时间——Agent 报错往往是在你赶 deadline 的时候。

---

> **怎么选：** 要把 **重复浏览器流程封装成 MCP/Skill 给 Agent**、且本机有 **Chrome** 的开发者，可以 **优先试 BrowserWing**（从内置 78 脚本改起）；要做 **跨浏览器 CI 回归**、**无 Chrome 的服务器环境**、或 **国内网络装 npm 都困难且无镜像预案** 的，**不建议以 BrowserWing 为唯一底座**，Playwright/Selenium 或 API 直抓更合适。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| Agent 工作流开发者 | MCP/Skill 导出是主路径 |
| 重复 UI 监测/运营 | 录制 + 每周复跑 |
| 非工程师先试自动化 | 可视化录比写代码门槛低 |
| MIT 友好商用场景 | 协议宽松 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| QA 要 Playwright 级 E2E | 缺断言与 CI 生态 |
| 无 Chrome / 纯服务器 | 硬依赖 Chrome |
| 纯 API 无 UI 任务 | 杀鸡用牛刀 |
| 国内网络无镜像预案 | 安装可能反复失败 |
| 想未授权爬取的人 | 合规红线 |

> 📷 **配图待补**：Agent + BrowserWing + Lovart 监测工作流（`images/BrowserWing-who-workflow.png`）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | npm 全局装 + Chrome；国内可能多试几次 |
| 核心能力 | ⭐⭐⭐⭐ | 录制→MCP 路径清晰 |
| 稳定性 | ⭐⭐⭐ | DOM 变更要维护脚本 |
| 文档/社区 | ⭐⭐⭐ | README + 78 脚本；非大厂文档 |
| 成本 | ⭐⭐⭐⭐⭐ | MIT 开源免费 |

**综合评分：3.7 / 5.0**（按「Agent 浏览器 MCP 工具」打分，不是按 Playwright 替代品）

> **一句话总结**：BrowserWing 适合把「每周都要点一遍的浏览器」收成 Agent 可调的工具——它管录制和 MCP，不管你的抓取是否合法；Chrome 在，脚本在，价值在。

---

## 🔗 BrowserWing 官网与项目地址

- **GitHub**：https://github.com/browserwing/browserwing  
- **Stars**：1,401（2026-08 口径，以仓库当日为准）  
- **许可证**：MIT  
- **安装**：`npm i -g browserwing`（需 Chrome；国内可查 Gitee 镜像）  
- **对照**：Selenium · Playwright · browse-use  
- **互补**：Lovart https://www.lovart.ai/

---

**标签**：#AI工具 #浏览器自动化 #BrowserWing #MCP #T2单品
