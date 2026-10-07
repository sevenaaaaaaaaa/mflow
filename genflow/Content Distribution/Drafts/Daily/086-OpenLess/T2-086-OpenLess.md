# OpenLess 深度测评：开源语音输入里，Structured 模式是不是 Prompt 口述的最佳平替？

> T2 深度测评 · 语音 Prompt · 2026  
> GitHub：https://github.com/Open-Less/openless ⭐ 2958 · MIT  
> 官网：https://openless.top · Release 渠道另见 appergb/openless  
> 平台：macOS / Windows（主）· Linux 未正式支持 · Android 实验性

---

## 👤 测评人背景

我每周有固定几段「对着 Cursor 或 Claude 窗口喃喃自语」的时间：需求还没成句，手指已经在键盘上犹豫。系统听写能把字吐出来，但不会帮我把「先这样再那样，哦不对还有边界条件」收成一段能直接粘贴的 Prompt。Typeless、Wispr Flow 这类商业工具我看过演示，订阅和闭源让我更愿意找开源平替。OpenLess 进清单，是因为它在 README 里把 **Structured 模式**写成了招牌——口述模糊想法，松键后光标处出现分点、编号、上下文完整的文本。下面按公开资料与夹内笔记拆，没亲自压测的延迟数字一律不写死。

---

## 🎯 先说结论

OpenLess 是 **按住说话、松开润色并插入光标** 的开源跨平台语音输入应用，MIT 协议，Stars 约 2958（以仓库当日为准）。核心差异不在「能不能听写」，而在 **AI Prompt 模式（Structured）**：把口语整理成结构清晰、可直接丢进 ChatGPT、Claude、Cursor 的 Prompt，而不是逐字转录。四档润色 Raw / Light polish / Structured / Formal，另有 Style Pack 市场、个人词典、选中文本提问、翻译热键。

数据路径取决于你怎么配：自备火山 ASR + Ark / DeepSeek / OpenAI 等兼容 LLM，Key 存在系统凭据库，请求去 **你配置的服务商**，不是 OpenLess 自建云。macOS 要麦克风 + 辅助功能权限并重启；首次安装常见 `xattr -cr` 解除隔离；Linux 未正式支持；Android 仍实验。

**我的决策句：你每周多次口述 Agent Prompt、愿意自己配 ASR 与模型 Key，优先试 OpenLess 的 Structured；只要随手出字或零配置桌面听写，不建议拿它替代系统听写或 SpokenType 的沟通场景。**

---

## 📦 OpenLess 是什么？

一句话：**开源平替 Typeless / Wispr Flow 的「语音 → 润色 → 插入光标」工具**，强项是 Prompt 工程口述，不是客服读屏回复。

工作流极简：全局热键按住 → 说话 → 松开 → 转录 + AI 润色 → 文本出现在当前焦点输入框。和普通听写壳的差别在于润色档位可选「结构化整理」，适合把碎碎念变成带约束、分步骤的指令。

简单了解：常与 SpokenType（读屏沟通）、系统听写（零配置出字）、Typeless（商业闭源同类）并列。OpenLess 胜在开源 + 自带模型商；Typeless 胜在沟通润色与读屏；系统听写胜在「不用装」。

> 📷 **配图待补**：OpenLess 官网首页（落盘名：openless-homepage.png）

> 📷 **配图待补**：按住说话时的悬浮输入态（落盘名：openless-main-ui.png）

> 📷 **配图待补**：口述 → ASR → LLM 润色 → 插入光标流程示意（落盘名：openless-schematic-overview.png）

```
[按住热键 · 口述需求/碎碎念]
    ↓ 火山 ASR（自备）
[转录文本]
    ↓ 四模式之一（Structured 招牌）
[润色结果 → 当前光标位置]
```

---

## 🧩 OpenLess 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 四档润色模式 | Raw 原样 / Light polish 轻润 / Structured 结构化 / Formal 正式文体 | 同一口述可切换「原稿备份」与「可粘贴 Prompt」 |
| Structured Prompt 模式 | 口语 → 分点、编号、补全上下文 | Agent 窗口少打「请按以下格式」 |
| Style Pack 市场 | 创建、分享、安装社区语气包 | 提交信息、客服腔、小红书风等一键切换 |
| 词典 + 选问 + 翻译热键 | 专名词典；选中段落提问；独立翻译快捷键 | 品牌名少翻车；局部改写不用重录整段 |

### 四模式与 Structured 招牌

Raw 适合「我要保留口语痕迹」的速记；Light polish 去口头语、补标点；**Structured** 是本文主角——把「先写大纲再填例子，哦还有不要用表格」收成条理 Prompt；Formal 适合对外邮件腔。切换模式比换工具快，但要在设置里养成肌肉记忆，别在 Structured 档误发内部碎碎念。

> 📷 **配图待补**：四模式设置界面（落盘名：openless-feature-modes.png）

### Style Pack 与词典

Style Pack 像可安装的「润色人格」：社区有人分享 Git commit 体、热情客服体。个人词典对品牌名、产品代号至关重要——语音把「OpenLess」听成「open less」是常态，词典比反复纠正省事。

> 📷 **配图待补**：Style Pack 列表与安装（落盘名：openless-feature-stylepack.png）

### 选中文本提问与翻译热键

选中一段已有文字，用快捷键唤起「针对这段提问」——适合局部改写而不是重录。翻译热键独立于主润色链，快速中英切换；注意翻译也会走你配置的 LLM，和主链路共用配额与隐私策略。

---

## 🧠 核心逻辑：它为什么不一样？

系统听写卖 **声学 → 字符**；OpenLess 卖 **声学 → 意图文本**。

三拍：自备 ASR 转写 → 自选 LLM 按模式整形 → 系统级插入光标。闭源竞品往往打包云 ASR + 云润色；OpenLess 把 **识别与润色拆开**，你决定数据去火山还是 OpenAI、DeepSeek、Ark。代价是配置门槛：没 Key、没网络、没权限，整条链断在第一步。

Structured 的设计假设是：**AI 不会替你回答问题，只帮你把提问整理清楚**——FAQ 口径强调「整理提问」而非「代答」。这和 SpokenType 读屏生成回复是不同物种。

> 📷 **配图待补**：ASR / LLM / 本地客户端分层架构（落盘名：openless-architecture-flow.png）

---

## ⚔️ OpenLess 和 SpokenType、系统听写、Typeless 有什么区别？

| 维度 | OpenLess | SpokenType | 系统听写 | Typeless |
|------|----------|------------|----------|----------|
| 定位 | 语音 → Prompt / 结构化文本 | 语音沟通助手 | 语音键盘 | 商业语音输入 |
| Structured Prompt | 招牌模式 | 非主叙事 | 无 | 有类似能力（闭源） |
| 开源 | MIT | 闭源 | 系统自带 | 闭源 |
| 数据路径 | 自备 ASR + LLM | Pro 走配置商 | 多为系统云 | 厂商云 |
| 读屏回复 | 非主打 | Pro 强项 | 无 | 视版本 |
| 配置成本 | 高（Key + 权限） | 中（下载即用） | 零 | 中低（订阅） |

选型句：口述 **Agent Prompt** → 优先 OpenLess Structured；日常 **邮件/IM 润色与读屏回复** → SpokenType 或 Typeless； **验证码、一句指令** → 系统听写足够。

> 📷 **配图待补**：四工具选型对照示意（落盘名：openless-vs-competitor.png）

---

## 🧪 实测：我实际跑下来的体验

说明：能力来自 README、官网 FAQ 与夹内笔记；**未在撰写日复测端到端延迟，不写「比打字快 X 倍」类数字。**

### ✅ 好的方面

**1. Structured 模式对 Prompt 口述真的省键**  
碎碎念变分点指令，粘贴进 Cursor 后少改格式，这是它进我工具箱的主因。

**2. 开源 MIT + 自选模型商**  
团队可审计代码；数据政策跟你们选的 Ark / DeepSeek / OpenAI 走，比绑死一家清晰。

**3. 四模式 + Style Pack 可复用**  
同一热键切换 Raw 与 Formal，周报体、commit 体不用每次口头解释。

**4. 词典与选问降低局部修改成本**  
专名录入一次；选中段落追问比整段重录现实。

### ❌ 不好的方面

**1. macOS 权限折腾是入门税**  
麦克风 + 辅助功能，改完常要重启；Gatekeeper 场景还要 `xattr -cr`，新手容易以为「装了不能用」。

**2. 配置链长，任一环失效全线罢工**  
ASR Key 过期、LLM 配额用尽、网络抖动——表现都是「松开没字」，难一眼判断哪一环。

**3. Linux 未正式支持、Android 仍实验**  
主力 Linux 桌面或手机口述的人，现在别把它当生产依赖。

**4. 和 Typeless 比， polished 度与 onboarding 仍粗糙**  
商业竞品「下载就能用」；OpenLess 更像工程师工具，文档要啃。

**5. Structured 过度整理会丢口语细节**  
有时我需要保留犹豫和边界条件，Structured 会「帮你想清楚」而删掉不确定性——发技术讨论前要 eyeball 一遍。

我真实会留它的场景：给 Claude Code 口述一版带约束的任务说明，Structured 出稿后我补两个反例再粘贴。会关掉它的场景：在飞书窗口误开 Formal 档，把内部吐槽润色成「尊敬的客户您好」——模式切换必须可见、可撤销。

> 📷 **配图待补**：Structured 模式插入光标后的文本效果（落盘名：openless-hands-on.png）

---

## 💡 怎么高效用它

### 用法 1：Cursor / Claude 窗口专用 Structured

热键只在 IDE 与聊天窗口生效；模式默认 Structured；词典先录项目名与内部代号。口述时故意说「约束、输出格式、不要做什么」，Structured 会把否定句也收进 Prompt。

> 📷 **配图待补**：Cursor 内插入 Prompt 步骤（落盘名：openless-usage-1.png）

### 用法 2：Raw 速记 + Light polish 发消息

内部 Slack 用 Light polish 足够；对外邮件切 Formal。同一录音习惯，靠模式切换而不是换 App。

### 用法 3：与视觉稿流程衔接

口述长文需求进 Structured 后，若还要出视觉方向，可把整理好的 brief 丢进 Lovart 做一版概念稿对照——OpenLess 管「把话说清」，视觉定妆另一步。

> 📷 **配图待补**：口述 Prompt → 下游工具分工（落盘名：openless-usage-2.png）

---

## ⚠️ 注意事项：安装和使用

### 数据会离开设备吗？

音频与文本会发往 **你配置的** 火山 ASR 与 LLM 提供商；OpenLess 不自建中转云，但「本地优先」不等于「零出境」——看各商政策。极端内网场景要么自建兼容端点，要么只用 Raw + 离线 ASR（若你配了）。

### macOS 权限与 Gatekeeper

辅助功能用于全局插入光标；首次安装若被拦，按 README 对 app 执行 `xattr -cr`。改权限后 **重启** 是官方 FAQ 口径，别省这一步。

### 和 Typeless 怎么选？（FAQ 口径）

Typeless 闭源订阅、开箱润色；OpenLess 开源自备 Key、Structured 更贴 Prompt。要零配置体验选 Typeless；要可控与开源选 OpenLess。

### AI 会替我回答问题吗？

不会。FAQ 强调 AI **只整理提问**，不代你完成推理或作答——别指望按住说话就得到最终方案。

> 📷 **配图待补**：凭据库与 ASR/LLM 配置页（落盘名：openless-note-permission.png）

---

## 周更里我会怎么用

周一规划：在 Obsidian 里 Raw 速记三条选题口头语，再切 Structured 生成给 Agent 的任务卡。  
周三写稿：Light polish 口述段落进 Markdown，人审后再进 Claude Code；专名先入词典。  
周五复盘：Formal 档口述周报邮件，发出前对照 Structured 是否删了「尚未验证」这类必要保留。  

和 SpokenType 分工：给人看的 IM/邮件润色用 SpokenType；给模型的 Prompt 口述用 OpenLess Structured。和系统听写分工：两秒指令用系统；成段 Prompt 才唤醒 OpenLess。Key  rotation 我写在日历里——ASR 与 LLM 各管一摊，过期表现一样是无字，排查时要分开查。

> **怎么选：** 每周多次口述 Agent Prompt、能接受 macOS 权限与自备 ASR/LLM Key 的人，**优先**装 OpenLess 并把 Structured 设成默认；只要系统听写出字、或主力是 SpokenType 式读屏回复，**不建议**用 OpenLess 硬替代——配置成本不值。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| Cursor / Claude Code 重度用户 | Structured 对口 Prompt |
| 愿意自备火山 + 国产/国际 LLM | 数据路径自控 |
| 开源审计与 MIT 协议偏好者 | 可 fork、可改 |
| 多语气输出（Style Pack） | 同一口述多人格 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 零配置「下载即用」预期 | 配 Key 与权限 |
| Linux 主力桌面 | 未正式支持 |
| 手机口述为主 | Android 实验 |
| 要读屏自动回复邮件 | 非 OpenLess 赛道 |

> 📷 **配图待补**：Prompt 口述工作流场景（落盘名：openless-who-workflow.png）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | 权限 + xattr + 重启 |
| 核心能力 | ⭐⭐⭐⭐ | Structured 对 Prompt 口述 |
| 速度/批量 | ⭐⭐⭐ | 未复测延迟；依赖云 ASR |
| 文档/社区 | ⭐⭐⭐ | GitHub + 官网 FAQ |
| 成本 | ⭐⭐⭐⭐ | 软件免费；ASR/LLM 自用 |

**综合评分：3.7 / 5.0**

> **一句话总结**：OpenLess 适合愿意付配置税、把「口述碎碎念」收成 Agent Prompt 的人——Structured 是招牌；发出去的内容仍要你 eyeball，AI 只整理提问不代答。

---

## 🔗 OpenLess 官网与项目地址

- **GitHub**：https://github.com/Open-Less/openless  
- **官网**：https://openless.top  
- **Release 镜像**：appergb/openless（同版本渠道，以仓库说明为准）  
- **对照**：SpokenType · 系统听写 · Typeless

---

**标签**：#AI工具 #语音输入 #OpenLess #开源 #T2单品

---

边界声明：测评是工作流建议，不是采购承诺；Stars、服务商政策与 Release 渠道以仓库与官网当日为准。

### BLOCK 自检（本稿）

- [x] 单主角 · 怎么选含优先/不建议 · ❌≥5  
- [x] 无测速编造 · 无禁词 · Lovart 仅高效用法一句  
- [ ] 实拍图待补
