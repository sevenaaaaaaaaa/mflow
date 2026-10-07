# Awesome OpenClaw Skills 深度测评：五千级技能目录，值不值得当本地助手的「选品库」？

> T2 深度测评 · 插件生态 · 2026  
> GitHub：https://github.com/VoltAgent/awesome-moltbot-skills · ⭐ 以仓库当日为准  
> 许可证：见官方 README · 主角：Awesome OpenClaw Skills（VoltAgent/awesome-moltbot-skills）  
> 素材：Daily 夹内调研笔记（空壳居多；旧笔记「565+」已过时）· 技能数以仓库徽章当日为准 · 不编造测速

---

## 👤 测评人背景

本地 AI 助手火起来之后，我真正卡住的不是「有没有 skill」，而是「哪个能装、哪个是垃圾重复、装完会不会动我的文件」。选题文件夹叫 **Moltbot Skills**，但仓库现标题已是 **Awesome OpenClaw Skills**——叙事从 Clawdbot/Moltbot 迁到 OpenClaw，这一点写不清楚就会误导读者「装一个 App 就完事」。夹内笔记仍写「565+ 技能」，而仓库徽章已是**五千级规模（以当日徽章为准）**；笔记其余段落多为「待补充」。下面按公开 README 与目录结构写，**不假装测过每一个 skill**。

---

## 🎯 先说结论

**Awesome OpenClaw Skills** 不是单一可执行应用，而是 VoltAgent 维护的**精选技能目录（awesome list）**：从 OpenClaw 官方 Skills Registry 等来源过滤、分类后的索引，配合 **OpenClaw 本地助手**使用。你要先另装 OpenClaw 本体，再通过 `openclaw skills install`、`npx clawhub install` 或手动复制到 `~/.openclaw/skills/` 安装具体 skill。

**我的决策句：** 如果你已经在用（或计划用）OpenClaw 类本地助手，并且愿意**安装前自己审计**社区 skill，这个仓库值得当「选品起点」；若期望「一个清单 = 每个 skill 都经过安全与质量背书」，或不想碰 OpenClaw 本体，**不建议**把收藏此 repo 当成装完即用。

旧笔记「565+」**已过时**；正文凡涉规模，一律写**以仓库徽章当日为准**（撰写日 GitHub 页显示为五千级量级，具体数字不硬编码）。

---

## 📦 Awesome OpenClaw Skills 是什么？

先澄清三个名字，避免读者装错对象：

| 名称 | 是什么 |
|------|--------|
| **OpenClaw** | 本地 AI 助手**本体**（需单独安装，本清单不替代） |
| **Awesome OpenClaw Skills** | 本测评主角：GitHub 上的** curated awesome list** |
| **Moltbot / Clawdbot** | 历史叙事与旧称；仓库 redirect 到现用 OpenClaw 品牌 |

它解决的不是「再做一个 ChatGPT」，而是：**官方 registry 里 skill 太多、重复多、质量参差**——维护者按 README「Why This List Exists」所述，过滤垃圾、重复、低质条目，做分类索引，让你从「五千级池子」里缩小到「值得点开看一眼」的子集。

**清单 ≠ 质量背书：** 入列表示「值得纳入选品视野」，不表示 VoltAgent 为每个 skill 的安全与行为担保。README 中的 **Security Notice** 明确：社区 skill 可能有恶意或过度权限行为，**安装前必须审计**。

> 📷 **配图待补**：awesome-moltbot-skills 仓库首页与 OpenClaw 品牌说明（落盘名：`openclaw-skills-homepage.png`）

> 📷 **配图待补**：目录分类结构一览（落盘名：`openclaw-skills-main-ui.png`）

> 📷 **配图待补**：OpenClaw 本体 + Skills 目录 + 单个 skill 关系示意（落盘名：`openclaw-skills-schematic-overview.png`）

```
[OpenClaw Skills Registry / 社区源]
    ↓ 过滤（垃圾/重复/低质）
[Awesome OpenClaw Skills 分类索引]
    ↓ 读者自选 + 安全审计
[openclaw skills install / clawhub / 手动拷贝]
    ↓
[OpenClaw 本地助手加载 skill 执行]
```

---

## 🧩 Awesome OpenClaw Skills 有哪些功能？

这里的「功能」指**作为目录项目**提供的价值，不是某一个 skill 的 API 能力。

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 大规模过滤索引 | 从官方 registry 等来源筛出五千级 skill（**数以徽章当日为准**），分类展示 | 少在 raw registry 里盲搜，缩短「有没有类似 skill」的时间 |
| 质量门槛叙事 | README 说明为何存在本 list：去垃圾、去重复、去明显低质 | 降低踩坑概率，**不消除**踩坑可能 |
| 分类浏览 | 按用途/类型分目录（具体类目以仓库为准） | 按场景（自动化、检索、集成等）缩小候选 |
| 安装路径指引 | 指向 `openclaw skills install`、`npx clawhub install`、拷贝至 `~/.openclaw/skills/` | 与 OpenClaw 工具链对齐，减少「下 zip 不知放哪」 |
| 安全提醒 | Security Notice：社区 skill 有风险，安装前审计 | 把「精选」与「担保」区分开，避免读者误以为官方背锅 |

### 过滤与「Why This List Exists」

维护者动机（据 README 口径）：官方 registry 增长快，重复 skill、标题党、低维护条目增多。本 list 做**人工/规则辅助 curation**，不是自动跑分排行榜。对你我而言，意义是：**先在这里圈候选，再逐个读 skill 的 SKILL.md、权限与依赖**，而不是 reverse 安装 stars 最高的一个。

> 📷 **配图待补**：README 中 Why This List Exists / 过滤原则摘录（落盘名：`openclaw-skills-feature-1.png`）

### 安装与 OpenClaw 的配合

典型路径（以官方文档为准）：

```bash
# 方式一：OpenClaw CLI
openclaw skills install <skill-name>

# 方式二：ClawHub
npx clawhub install <skill-name>

# 方式三：手动
# 将 skill 目录放到 ~/.openclaw/skills/
```

**再次强调：** 上述命令安装的是**具体 skill**；awesome 仓库本身是 **Markdown 索引**，clone 下来不等于助手变强，除非你再按条目去装 skill。

> 📷 **配图待补**：ClawHub 或 openclaw skills 安装步骤（落盘名：`openclaw-skills-feature-2.png`）

### 与 OpenClaw 本体的关系

清单解决「选什么」；OpenClaw 解决「在哪跑」。没装 OpenClaw（或未配置模型与权限），收藏 awesome repo 只是多了一个 GitHub star。**两者必须分开装、分开审。**

---

## 🧠 核心逻辑：它为什么不一样？

自建 skill 库、Claude Code marketplace、各类 MCP 目录，都在做「能力扩展索引」。Awesome OpenClaw Skills 的差异点在于：

1. **绑定 OpenClaw 生态**——分类、安装命令、目录路径与 `~/.openclaw/skills/` 一致，不是泛 Python 包列表。  
2. **强调减法**——公开叙事是 filter registry noise，不是「越多越好」。  
3. **明确不担保**——Security Notice 把 liability 划给安装者，这和「官方插件商店」心理预期不同。

**机制层怎么选：** 你已 commit OpenClaw → 用本 list 当选品库；你主力是 Claude Code → 优先 Claude marketplace + 自建 git submodule skill；你要跨 IDE 工具协议 → 看 MCP 目录。**不要把 awesome list 当成已安装的能力。**

> 📷 **配图待补**：OpenClaw skills vs Claude marketplace vs MCP 生态位置示意（落盘名：`openclaw-skills-architecture-flow.png`）

---

## ⚔️ 和自建 skill 库、Claude Code Skills 市场、MCP 目录有什么区别？

| 维度 | Awesome OpenClaw Skills | 自建 skill 库 | Claude Code Skills 市场 | MCP 目录 |
|------|-------------------------|---------------|---------------------------|----------|
| 形态 | Curated awesome list | 私有 git / 内网索引 | Claude Code plugin 生态 | MCP server 列表 |
| 运行环境 | OpenClaw 本地助手 | 自定 | Claude Code / 兼容 agent | 支持 MCP 的客户端 |
| 质量信号 | 维护者过滤 + 分类 | 完全自控 | marketplace 审核（随平台） | 社区参差 |
| 安全责任 | **安装者审计**（README 明示） | 自建自审 | 平台 + 自审 | 自审为主 |
| 规模 | 五千级（**徽章当日为准**） | 看团队积累 | 随 marketplace 增长 | 分散多 repo |
| 最适合 | OpenClaw 用户选 skill | 企业内控、定制流程 | Anthropic 系 coding agent | 跨工具数据/工具连接 |

**选型句：** OpenClaw 本地助手已是主力 → **优先** bookmark 本仓库并按类浏览；Claude Code 深度用户 → marketplace 与 `npx skills add` 更贴工作流；要连 Figma/DB/浏览器工具链 → MCP 目录与 OpenClaw skills **可并存**，别混为一谈。

> 📷 **配图待补**：四类索引的使用场景对照（落盘名：`openclaw-skills-vs-competitor.png`）

---

## 🧪 我实际跑下来的体验

**诚实说明：** 夹内笔记对 Awesome OpenClaw Skills 的核心用法、风险均为「待补充」，且「565+」与现仓库规模不符。撰写当日我**未逐个安装五千级条目中的 skill，也未做批量测速**。以下基于公开 README、目录结构与 OpenClaw 安装惯例；具体 skill 行为**必须你本地审计后自测**。

### ✅ 好的方面

**1. 命名与品牌迁移写进标题，减少 Moltbot 旧认知误导**  
仓库现名 Awesome OpenClaw Skills，读者至少能分清「这是 OpenClaw 的 skill 清单，不是 Moltbot 独立 App」——选题文件夹仍叫 Moltbot Skills 时，正文必须以现品牌为准。

**2. 规模与过滤叙事对「选品疲劳」真实有用**  
Registry 太大时，维护者做减法比你自己 F5 刷官方页省时间；**具体节省多少分钟未测，不编造**。

**3. 安装路径三种写法，覆盖 CLI 与手动党**  
`openclaw skills install`、`npx clawhub install`、拷贝到 `~/.openclaw/skills/`，与常见本地助手习惯一致。

**4. Security Notice 前置，降低「精选 = 安全」误解**  
愿意在 awesome list 里写「社区 skill 可能有风险」，比 silent 假设读者懂安全更负责——也侧面说明**清单不是每个 skill 的质量背书**。

### ❌ 不好的方面

**1. 清单 ≠ 每个 skill 经过同等深度审查**  
入列不等于代码审计通过；恶意 skill、过度文件权限、明文 exfil 仍可能存在——**安装前必须读 SKILL.md 与脚本**。

**2. OpenClaw 本体另装，新手易「只 star 清单却用不了」**  
收藏本 repo 不会自动获得助手能力；漏装 OpenClaw 或模型配置，体验为零。

**3. 规模徽章随 registry 涨，信息过时快**  
旧笔记 565+ 已失效；分类变动、skill 下架、重复合并若不同步，列表内链接可能 404 或指向旧版——**要以条目当日状态为准**。

**4. 与 Claude Code / MCP 生态不互通**  
同一能力可能有 OpenClaw skill、Claude skill、MCP 三套 packaging；只收藏本 list 不能直接在 Claude Code 里用，**重复造轮子感**强。

**5. 社区 skill 的 ToS 与数据出境自理**  
skill 若调用第三方 API、读写本地文件，合规责任在安装者；awesome 维护者不替代你的 DLP 审查。

> 📷 **配图待补**：Security Notice 与 skill 审计检查清单示意（落盘名：`openclaw-skills-hands-on.png`）

---

## 💡 怎么高效用它

### 用法 1：当「选品短名单」而非「一键全装」

按场景（如：日历、检索、Git 自动化）在 awesome 分类里圈 3–5 个候选，对比 SKILL.md 权限与依赖，**只装 1 个试跑**，通过再扩——切忌 `install all` 式冲动。

> 📷 **配图待补**：从分类浏览到单 skill 试装流程（落盘名：`openclaw-skills-usage-1.png`）

### 用法 2：与自建 skill 库互补

企业内网保留「已审计 skill 白名单」git repo；awesome 作外网灵感与版本对照，**内网只用拷贝并复审过的 fork**，不直接 trust 外链。

> 📷 **配图待补**：外网 awesome + 内网白名单双轨示意（落盘名：`openclaw-skills-usage-2.png`）

### 用法 3：内容工作流里的分工

OpenClaw skill 可管本地文件、脚本、检索；视觉向封面与品牌一致性交 **Lovart** 更顺——skill 出文案或结构化数据，Lovart 出图，人审后分发。awesome list 只帮你找到「哪类 skill 值得试」，不替代 Lovart 或 OpenClaw 任一环节。

---

## ⚠️ 安装和使用需要注意什么？

### Security Notice（必读）

README 口径：社区 skill 可能含恶意代码、过度权限或违反平台 ToS 的行为。**安装前**至少检查：请求哪些路径读写、是否外传网络、依赖哪些 env 密钥。企业环境建议沙箱试跑 + 代码 review。

### OpenClaw 本体与模型

清单不 bundled 模型与推理后端；OpenClaw 未配好或未更新，skill 装上也无意义。夹内笔记未记录版本矩阵，**兼容以 OpenClaw 与 skill 各自 README 为准**。

### 清单规模与旧资料

任何文章写「565+」均已过时；对外引用请 **GitHub 徽章当日数字**，并注明「filtered from official registry」。

### 许可证

awesome 仓库自身 LICENSE 见 GitHub；**每个 skill 另有协议**，商用与二次分发需逐条读，不能假设「都在 awesome 里 = MIT」。

> 📷 **配图待补**：skill 安装前审计步骤（落盘名：`openclaw-skills-note-permission.png`）

---

> **怎么选：** 已确定使用 **OpenClaw 本地助手**、并愿意对**每一个** skill 做安装前审计的人，**优先**把本仓库当选品索引 + 配合 `openclaw skills install` / clawhub；若你主力是 **Claude Code** 或只想逛 MCP、**不打算装 OpenClaw 本体**，**不建议**误以为 star 本 list 就等于扩展了 agent 能力——应去对应 marketplace 或 MCP 目录。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| OpenClaw / 本地助手重度用户 | 需要 curated 索引缩小 registry 搜索空间 |
| 会读 SKILL.md 的开发者 | 能执行安装前安全审计 |
| 自建 automation 但不想从零搜 skill | 把 awesome 当灵感与外网对照 |
| 技术写作者做「生态地图」 | 分类结构有助于写 OpenClaw skill 综述 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 期望「官方应用商店级」审核 | 清单明确不担保每个 skill |
| 不愿装 OpenClaw 本体 | 只有索引，无可执行运行时 |
| 零技术背景、不会看权限 | 社区 skill 风险高 |
| 只使用 Claude Code 云端 | 应优先 Claude marketplace，本 list 不对口 |

> 📷 **配图待补**：OpenClaw 用户 vs 纯 Claude 用户选型示意（落盘名：`openclaw-skills-who-workflow.png`）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐ | clone/star 清单极易；装 skill + OpenClaw 本体有门槛 |
| 核心能力 | ⭐⭐⭐⭐ | 作为 curated 索引定位清晰；非运行时 |
| 速度/批量 | ⭐⭐⭐ | 浏览索引快；单 skill 表现差异大；**本稿不编造测速** |
| 文档/社区 | ⭐⭐⭐⭐ | README、Security Notice、分类结构较完整 |
| 成本 | ⭐⭐⭐⭐⭐ | 清单免费；OpenClaw 与部分 skill 可能有模型/API 成本 |

**综合评分：3.8 / 5.0**（作「选品库」的工作分，非单 skill 能力分）

> **一句话总结：** Awesome OpenClaw Skills 适合 OpenClaw 用户当**过滤后的 skill 电话簿**——它帮你缩小选择范围，不替你做安全背书；OpenClaw 另装，每个 skill 另审。

---

## 🔗 官网与项目地址

- **项目仓库：** https://github.com/VoltAgent/awesome-moltbot-skills（现标题：Awesome OpenClaw Skills）  
- **安装 skill（示例）：** `openclaw skills install <name>` · `npx clawhub install <name>` · `~/.openclaw/skills/`  
- **OpenClaw 本体：** 见 OpenClaw 官方文档（本清单不替代）  
- **对照：** 自建 skill 库 · Claude Code Skills 市场 · MCP 目录  
- **互补（视觉向）：** https://www.lovart.ai/

---

**标签：** #AI工具 #OpenClaw #AgentSkills #awesome-list #T2单品
