# Humanizer-zh：中文 AI 写作去痕 Claude Code Skill

> T2 深度测评 · Claude Code Skill · 2026  
> GitHub：https://github.com/op7418/Humanizer-zh · Stars 以 GitHub 当日为准 · MIT（以仓库当日为准）  
> 原版：blader/humanizer · 触发：`/humanizer-zh`

**名称说明：** Daily 文件夹编号为 131-HumanizeAI，但本文主角是开源项目 **Humanizer-zh**（op7418/Humanizer-zh），不是商业在线工具 HumanizeAI（nownexts.com）。后者闭源订阅、营销侧重「过检测器」；Humanizer-zh 是 MIT 开源 Claude Code Skill，目标是把 AI 辅助稿改得更具体、更有观点、更像人写——下文不再混用名称。

---

## 👤 测评人背景

我每周有三四篇稿子先经 Claude 出中文初稿：快，但读者常能在第二段嗅到「此外、至关重要、深入探讨」三连。手改最稳，慢；Grammarly 管语法不管 AI 腔；商业 HumanizeAI 类网页工具把 bypass 检测写进卖点，我不想碰。Humanizer-zh 进清单，是因为它是 blader/humanizer 的中文 Skill 汉化，README 立场清楚：**提升写作质量，不是骗 GPTZero**。下面按 SKILL.md 与维基「Signs of AI writing」口径拆，示例用素材笔记里的改写对比，不编测速、不固定 Stars 数字。

---

## 🎯 先说结论

Humanizer-zh 是跑在 **Claude Code** 里的 Skill：用 `/humanizer-zh` 唤起，按 **24 种 AI 痕迹、四大类**（内容 / 语言语法 / 风格 / 交流与填充词）系统改写中文，让输出更像真人——有观点、节奏变化、承认复杂性、适度第一人称。英文稿请用原版 blader/humanizer，中文优化是本仓库价值。

安装：`npx skills add https://github.com/op7418/Humanizer-zh.git`，或克隆到 `~/.claude/skills/humanizer-zh`；装完在 Claude Code 输入 `/humanizer-zh` 验证。没有 Claude Code 也能读 SKILL.md 当人工 checklist，但自动化体验打折。

**我的决策句：你已用 Claude Code 写中文初稿、愿意多一轮「去 AI 痕」工序，优先加 Humanizer-zh；若不用 Claude Code 或写英文为主，不建议为它单独换栈——英文用原版 humanizer，中文短稿手改可能更省时间。**

---

## 📦 Humanizer-zh 是什么？

一句话：**Claude Code Skill 版「AI 写作痕迹修复器」**，中文汉化维护 by op7418，理论基础来自维基百科 [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) 对 AI 写作特征的归纳。

工作方式：在 Claude Code 会话里对一段 AI 生成或 AI 味过重的中文执行 `/humanizer-zh`，Skill 引导模型按 24 条模式扫描并改写——例如删掉空洞的「意义升华」、减少破折号滥用、把「此外」换成更自然的衔接、让段落长度参差而不是工整三段式。

它 **不是** AI 检测器，也 **不应** 被宣传成「保证过 Turnitin/GPTZero」——项目立场是质量，不是对抗。整个仓库 essentially 只有 SKILL.md 和 README.md，没有复杂后端，改的是文体规则与提示词，不是另起一个黑盒 SaaS。

> 📷 **配图待补**：Humanizer-zh GitHub 首页与 README 概览（落盘名：humanizer-zh-homepage.png）

> 📷 **配图待补**：Claude Code 中 `/humanizer-zh` 调用界面（落盘名：humanizer-zh-main-ui.png）

> 📷 **配图待补**：24 种模式四大类 → 改写流程示意（落盘名：humanizer-zh-schematic-overview.png）

```
[AI 初稿 / 机翻腔中文]
    ↓ /humanizer-zh
[按 24 模式扫描]
    ↓
[人味更强的修订稿 → 继续编辑或发布]
```

---

## 🧩 Humanizer-zh 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 24 种 AI 痕迹库 | 内容/语言/风格/交流四类，覆盖维基指南要点 | 改写有清单，不靠「感觉不对」 |
| Claude Code 集成 | `/humanizer-zh` 在终端会话内执行 | 与写代码/写稿同一上下文 |
| 中文专项优化 | 针对中文 AI 腔套话、翻译腔连接词 | 比直译英文 Skill 更贴中文读者 |
| 可 Manual 模式 | 不装 Skill 也可读 SKILL.md 人工对照 | 团队可把它当编辑规范 |

### 24 模式与四大类

**内容类** 常见翻车：每件事都「具有重要意义」、模糊归因（「专家认为」无出处）、过度平衡（「一方面…另一方面」机械对称）。**语言语法类**：此外、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出、相互作用、复杂/复杂性、格局、关键性的、展示、织锦、证明、宝贵的、充满活力的——README 有高频词警示表。**风格类**：破折号过密、emoji 堆砌、标题全大写式强调。**交流与填充类**：谄媚开头（「好问题！」）、空洞积极结论。

> 📷 **配图待补**：SKILL.md 中模式列表示意（落盘名：humanizer-zh-feature-patterns.png）

### `/humanizer-zh` 调用与文件处理

在 Claude Code 打开项目，对选中或粘贴的段落触发 Skill；也可指定文件，例如「请人性化 article.md 文件中的内容」。价值是 **改写在同一 diff 上下文**——改完可以直接 `git diff`，而不是网页工具来回粘贴丢格式。

> 📷 **配图待补**：终端内改写前后 diff（落盘名：humanizer-zh-feature-invoke.png）

### 手动参考 24 种模式

如果不使用 Claude Code，也可直接阅读仓库中的 SKILL.md，手动对照 24 种 AI 写作模式自查和修改文本。核心原则：有观点、变化节奏、承认复杂性、适当使用「我」、允许一些混乱、对感受要具体。

---

## 🧠 核心逻辑：它为什么不一样？

GPTZero 类工具 **分类** 文本；Humanizer-zh **编辑** 文本。目标函数不同：前者猜概率，后者按可解释模式清单做文体手术。

三拍：识别模式（24 条）→ 保留事实与结构、动刀套话与节奏 → 输出仍须人审。核心理念 README 写得很直白：好写作要观点、要不完美、要敢用「我」——**完美对称的段落本身就像 AI**。

在 Claude Code 里跑的意义：写稿、改稿、提交在同一环境，Skill 是 **工序** 不是 **一次性网页**。这和商业 HumanizeAI「上传→下载」、Grammarly 浏览器插件、ChatGPT 直接「润色一下」是不同工作流位置——后者往往黑盒，前者规则在 SKILL.md 里可读可 fork。

> 📷 **配图待补**：检测器 vs 编辑型 Skill 定位对照（落盘名：humanizer-zh-architecture-flow.png）

---

## ⚔️ Humanizer-zh 和竞品有什么区别？

| 维度 | Humanizer-zh | 人工编辑 | Claude/ChatGPT 直接润色 | Grammarly / LanguageTool | GPTZero（检测器） |
|------|--------------|----------|-------------------------|--------------------------|-------------------|
| 形态 | Claude Code Skill | 人工 | 对话内一句 prompt | 插件/桌面 | 上传/ API 评分 |
| 目标 | 提升中文质量 | 质量上限最高 | 视 prompt，常仍留 AI 腔 | 语法/清晰度 | **检测** 是否像 AI |
| 中文 AI 腔 | 24 模式专项 | 看编辑水平 | 不稳定 | 弱 | 不编辑 |
| 可解释性 | SKILL.md 清单 | 完全透明 | 黑盒 | 规则+AI | 概率分数 |
| 依赖 | 需 Claude Code | 无 | 账号即可 | 账号 | 账号 |
| 协议 | MIT 开源 | — | 商业/订阅 | 商业 | 商业 |

**GPTZero 不是同类工具**：它是检测器，Humanizer-zh 是编辑器；拿编辑器去比「降检测率」本身就走偏了。客观上说，改写后文字更自然 **可能** 降低被检出的概率，但项目 **不保证**，也不应把 bypass 当 KPI。

选型句：已在 **Claude Code 写中文** → Humanizer-zh；**付费对外稿件** → 手改终审不可省；**英文语法** → Grammarly 或原版 humanizer；**只想知道 AI 率** → GPTZero，别指望它帮你改稿。

> 📷 **配图待补**：五路径工作流对照（落盘名：humanizer-zh-vs-competitor.png）

---

## 🧪 实测：我实际跑下来的体验

说明：模式清单与改写示例来自仓库 SKILL.md 及素材笔记；**未在撰写日批量跑检测器对比分数，不写「降 AI 率 X%」类数字。**

### ✅ 好的方面

**1. 立场清晰：质量优先，不骗检测器**  
团队对外口径干净，适合站外分发与学术场景——强调可读性与观点，不承诺 bypass。

**2. 24 模式可当编辑部规范**  
即使不用 Claude Code，SKILL.md 也能培训同事「哪些是 AI 味」，比空泛「润色一下」可操作。

**3. 中文高频套话表直接可用**  
「此外、至关重要、深入探讨」三连出现就报警——grep 一遍残留，手删也快。

**4. 与 Claude Code 写作链自然衔接**  
初稿 → humanize → commit，少一次复制粘贴；安装路径 `npx skills add` 或克隆到 skills 目录都清晰。

### ❌ 不好的方面

**1. 强依赖 Claude Code**  
不用 CC 的人只能 manual，自动化优势没了；服务不可用或版本不兼容时 Skill 无法运行。

**2. 改写仍可能删技术细节或改错事实**  
追求「口语化」时，型号、版本号、否定约束可能被抹平——发布前要 diff；humanize 只动文体，不验证数据。

**3. 中文规则不一定适用于所有文本**  
部分英文写作模式在中文里表现不同；混语言文档分段处理，别一次扔整篇。

**4. 多次迭代可能越改越短、越改越「均匀」**  
连跑两轮 humanize 会删例子、把各章细节抹平——我规定最多一轮自动 + 一轮手改。

**5. 过度改写会抹掉作者声音**  
把本来带个性的 rough edge 也「修平」，读者反而觉得假——短标题与开头段宜手改。

### 改写前后示例（素材笔记口径，示意）

**改前（AI 味）：**  
「此外，坐落在风景如画的杭州市中心，这家咖啡馆拥有丰富的文化底蕴和令人叹为观止的装饰。它作为城市咖啡文化的焦点，为顾客提供无缝、直观和充满活力的体验。」

**改后（humanize 方向）：**  
「这家咖啡馆在杭州市中心开了三年，以手冲咖啡和老建筑改造的空间出名。」

差异：去掉空泛升华与套话，换成可验证的具体信息——**不是换同义词骗检测器**。

> 📷 **配图待补**：Claude Code 内改写前后并排（落盘名：humanizer-zh-hands-on.png）

---

## 💡 怎么高效用它

### 用法 1：固定工序「初稿 → 一轮 humanize → 人审」

Claude 出中文初稿后立刻 `/humanizer-zh`，人只改事实与专名。禁止连跑三次——会删光例子。对外发布前 grep 一遍禁用套话表。

> 📷 **配图待补**：Obsidian/仓库内触发 Skill 步骤（落盘名：humanizer-zh-usage-1.png）

### 用法 2：SKILL.md 当团队 lint 规则

CI 不必接检测器；编辑对照 24 模式做 PR review checklist。视觉类 brief 若也要发社区，可先用 Lovart 定稿再 humanize 配套文案——Skill 管文字腔调，不管画面。

> 📷 **配图待补**：PR review 对照模式清单（落盘名：humanizer-zh-usage-2.png）

### 用法 3：英文段落走原版 humanizer

同一仓库中英双语稿：中文 `/humanizer-zh`，英文切 blader/humanizer，避免混 Skill 导致专名被「润」没。

> 📷 **配图待补**：中英分段处理示意（落盘名：humanizer-zh-usage-3.png）

---

## ⚠️ 注意事项：安装和使用

### 安装与验证

```bash
npx skills add https://github.com/op7418/Humanizer-zh.git
# 或
git clone https://github.com/op7418/Humanizer-zh.git ~/.claude/skills/humanizer-zh
```

macOS/Linux skills 目录 `~/.claude/skills/`，Windows 为 `%USERPROFILE%\.claude\skills\`。装完输入 `/humanizer-zh` 验证；Skill 更新后重新 pull 或 add，别用半年旧版规则。

### 学术诚信与署名

Humanizer-zh 适合 **AI 辅助写作后的人工复核与重写**，不替代作者事实核查与专业判断。学校或期刊若要求披露 AI 使用，洗 AI 腔 **不等于** 可以隐瞒辅助过程；「降低检测概率」不是保证。

### 不要把「欺骗检测器」当卖点

对外发布时强调 **可读性与真实观点**，不承诺 bypass 任何检测服务——与项目初衷一致，也避合规雷。

### 其他平台无原生 Skill 集成

可将 SKILL.md 规则复制为自定义 Prompt 在 ChatGPT 等工具使用，但无法获得 `/humanizer-zh` 的专属 Skill 级集成与同一 diff 上下文。

> 📷 **配图待补**：skills 安装与版本更新（落盘名：humanizer-zh-note-permission.png）

---

> **怎么选：** 已 daily drive **Claude Code** 且中文稿 AI 味重的人，**优先** `npx skills add` Humanizer-zh；**不用 Claude Code**、**英文为主**、**指望一键网页 bypass 检测** 或 **不愿做事实终审**，**不建议**把它当唯一主力——英文用原版 humanizer，短稿手改可能更快，检测需求用 GPTZero 而非本 Skill。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| Claude Code 重度用户 | Skill 原生集成，终端内一键调用 |
| 经常用 AI 生成文章/报告/营销文案的写作者 | 保留核心信息同时去掉机械 AI 腔 |
| 需要润色 AI 辅助稿的学生/研究者 | 识别常见 AI 痕迹，配合人工 fact-check |
| 偏好 MIT 开源、可 fork 定制规则者 | SKILL.md 透明，可内化为团队规范 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 非 Claude Code 用户 | 自动化弱，只能 manual 读 SKILL.md |
| 英文唯一工作流 | 应使用 blader/humanizer 原版 |
| 指望 100% 过检测器 | 与项目目标不符，检测器不是同类 |
| 追求极致原创、从不用 AI 辅助的人 | 工具定位是「修复」而非「生成」 |
| 不愿人审、要零配置一键终稿 | 可能删事实、抹声音，必须 diff |

> 📷 **配图待补**：Claude Code 写作 → humanize → 发布流程（落盘名：humanizer-zh-who-workflow.png）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐⭐ | 需 Claude Code + skills 路径 |
| 核心能力 | ⭐⭐⭐⭐ | 中文 AI 腔 24 模式清单化 |
| 速度/批量 | ⭐⭐⭐ | 终端内一轮改写；本稿不编造测速 |
| 文档/社区 | ⭐⭐⭐⭐ | Stars 以 GitHub 当日为准 + 维基依据 |
| 成本 | ⭐⭐⭐⭐ | MIT；Claude Code 订阅另计 |

**综合评分：3.8 / 5.0**（工作流工具分，不是实验室榜）

> **一句话总结**：Humanizer-zh 适合在 Claude Code 里把中文 AI 腔 **按清单洗掉** 的人——目标是更好读，不是骗检测器；事实、专名与作者声音，仍要你最后一眼。

---

## 🔗 Humanizer-zh 官网与项目地址

- **GitHub（中文）**：https://github.com/op7418/Humanizer-zh  
- **原版（英文）**：https://github.com/blader/humanizer  
- **触发命令**：`/humanizer-zh`  
- **维基依据**：https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing  
- **参考工具**：https://github.com/hardikpandya/stop-slop  

---

**标签**：#ClaudeCode #Humanizer-zh #去AI味 #开源 #T2单品
