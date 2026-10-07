# Humanizer-zh 深度测评：Claude Code 里洗 AI 味，是在提升质量还是在骗检测器？

> T2 深度测评 · Claude Code Skill · 2026  
> GitHub：https://github.com/op7418/Humanizer-zh ⭐ 14647 · MIT  
> 原版：blader/humanizer · 触发：`/humanizer-zh`  
> 依赖：Claude Code · 安装：`npx skills add` 类流程（以仓库 README 为准）

---

## 👤 测评人背景

站外分发周更里，有一半稿子会先过 Claude 出初稿——快，但读者一眼能嗅到「此外、至关重要、深入探讨」三连。手改最稳，慢；Grammarly 偏语法不是 AI 腔；HumanizeAI 类在线工具把「骗过检测器」写进营销，我不想碰。Humanizer-zh 进清单，是因为它是 **blader/humanizer 的中文 Claude Code Skill**，Stars 14647，README 明写目标：**提升写作质量，不是欺骗 GPTZero**。下面按 SKILL.md 与维基「Signs of AI writing」口径拆，示例用笔记里的改写前后对比，不把 bypass 当卖点。

---

## 🎯 先说结论

Humanizer-zh 是跑在 **Claude Code** 里的 Skill：用 `/humanizer-zh` 唤起，按 **24 种 AI 痕迹、四大类**（内容 / 语言语法 / 风格 / 交流与填充词）系统改写中文，让输出更像真人——有观点、节奏变化、承认复杂性、适度第一人称。英文稿请用原版 blader/humanizer，中文优化是本仓库价值。

安装走 Claude Code Skills 生态（README 常见 `npx skills add` 路径）；**没有 Claude Code 也能读 SKILL.md 当人工 checklist**，但自动化体验打折。与 HumanizeAI、Grammarly、纯手改相比：它 **嵌在编码/写作同一终端**，改完可继续 commit，而不是再开一个网页粘贴。

**我的决策句：你已用 Claude Code 写中文初稿、愿意多一轮「洗 AI 味」工序，优先加 Humanizer-zh；若不用 Claude Code 或写英文为主，不建议为它单独换栈——英文用原版 humanizer，中文手改可能更省时间。**

---

## 📦 Humanizer-zh 是什么？

一句话：**Claude Code Skill 版「AI 写作痕迹修复器」**，中文汉化维护 by op7418，理论基础来自维基百科对 AI 写作特征的归纳。

工作方式：在 Claude Code 会话里对一段 AI 生成或 AI 味过重的中文执行 `/humanizer-zh`（或按 SKILL 说明调用），Skill 引导模型按 24 条模式扫描并改写——例如删掉空洞的「意义升华」、减少破折号滥用、把「此外」换成更自然的衔接、让段落长度参差而不是工整三段式。

它 **不是** AI 检测器，也 **不应** 被宣传成「保证过 Turnitin/GPTZero」——项目立场是质量，不是对抗。

> 📷 **配图待补**：Humanizer-zh GitHub 首页与 Stars（落盘名：humanizer-zh-homepage.png）

> 📷 **配图待补**：Claude Code 中 `/humanizer-zh` 调用界面（落盘名：humanizer-zh-main-ui.png）

> 📷 **配图待补**：24 种模式四大类 → 改写 流程示意（落盘名：humanizer-zh-schematic-overview.png）

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
| Claude Code 集成 | `/humanizer-zh` 一键在终端会话内执行 | 与写代码/写稿同一上下文 |
| 中文专项优化 | 针对中文 AI 腔（套话、翻译腔连接词） | 比直译英文 Skill 更贴中文读者 |
| 可 Manual 模式 | 不装 Skill 也可读 SKILL.md 人工对照 | 团队可把它当编辑规范 |

### 24 模式与四大类

**内容类** 常见翻车：每件事都「具有重要意义」、模糊归因（「专家认为」无出处）、过度平衡（「一方面…另一方面」机械对称）。**语言语法类**：此外、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出、相互作用、复杂/复杂性、格局、关键性的、展示、织锦、证明、宝贵的、充满活力的——README 有高频词警示表。**风格类**：破折号过密、emoji 堆砌、标题全大写式强调。**交流与填充类**：谄媚开头（「好问题！」）、空洞积极结论。

> 📷 **配图待补**：SKILL.md 中模式列表示意（落盘名：humanizer-zh-feature-patterns.png）

### `/humanizer-zh` 调用

在 Claude Code 打开项目，对选中或粘贴的段落触发 Skill。价值是 **改写在同一 diff 上下文**——改完可以直接 `git diff`，而不是网页工具来回粘贴丢格式。

> 📷 **配图待补**：终端内改写前后 diff（落盘名：humanizer-zh-feature-invoke.png）

### 与原版 humanizer 分工

**英文 → blader/humanizer**；**中文 → Humanizer-zh**。混用会导致英文 Skill 对中文连接词识别不足，或中文 Skill 改英文时过度删除 technical term。

---

## 🧠 核心逻辑：它为什么不一样？

GPTZero 类工具 **分类** 文本；Humanizer-zh **编辑** 文本。目标函数不同：前者猜概率，后者按可解释模式清单做文体手术。

三拍：识别模式（24 条）→ 保留事实与结构、动刀套话与节奏 → 输出仍须人审。核心理念 README 写得很直白：好写作要观点、要不完美、要敢用「我」——**完美对称的段落本身就像 AI**。

在 Claude Code 里跑的意义：写稿、改稿、提交在同一环境，Skill 是 **工序** 不是 **一次性网页**。这和 HumanizeAI「上传→下载」、Grammarly 浏览器插件是不同工作流位置。

> 📷 **配图待补**：检测器 vs 编辑型 Skill 定位对照（落盘名：humanizer-zh-architecture-flow.png）

---

## ⚔️ Humanizer-zh 和 HumanizeAI、手改、Grammarly 有什么区别？

| 维度 | Humanizer-zh | HumanizeAI（类） | 手改 | Grammarly |
|------|--------------|------------------|------|-----------|
| 形态 | Claude Code Skill | 多为网页/API | 人工 | 插件/桌面 |
| 目标 | 提升中文质量 | 常宣传 bypass 检测 | 质量上限最高 | 语法/清晰度 |
| 中文 AI 腔 | 专项 | 视产品 | 看编辑水平 | 弱 |
| 可解释性 | 24 模式清单 | 黑盒分数 | 完全透明 | 规则+AI |
| 依赖 | 需 Claude Code | 浏览器即可 | 无 | 账号 |
| 协议 | MIT 开源 | 多为商业 | — | 商业 |

选型句：已在 **Claude Code 写中文** → Humanizer-zh；要 **网页一键且接受 bypass 叙事** → 不推荐 HumanizeAI 当首选（与本 Skill 价值观冲突）；**付费对外稿件** → 手改终审不可省；**英文语法** → Grammarly 或原版 humanizer。

> 📷 **配图待补**：四路径工作流对照（落盘名：humanizer-zh-vs-competitor.png）

---

## 🧪 实测：我实际跑下来的体验

说明：模式清单来自仓库 SKILL.md；**未在撰写日批量跑检测器对比分数，不写「降 AI 率 X%」类数字。**

### ✅ 好的方面

**1. 立场清晰：质量优先，不骗检测器**  
团队对外口径干净，适合站外分发伦理。

**2. 24 模式可当编辑部规范**  
即使不用 Claude Code，SKILL.md 也能培训实习生「哪些是 AI 味」。

**3. 中文高频套话表直接可用**  
「此外、至关重要、深入探讨」三连出现就报警——比空泛「润色一下」可操作。

**4. 与 Claude Code 写作链自然衔接**  
初稿 → humanize → commit，少一次复制粘贴。

### ❌ 不好的方面

**1. 强依赖 Claude Code**  
不用 CC 的人只能 manual，自动化优势没了。

**2. 改写仍可能删技术细节**  
追求「口语化」时，型号、版本号、否定约束可能被抹平——发布前要 diff。

**3. 不是 fact-check**  
洗掉了 AI 腔，不等于事实正确；幻觉句可能变「更像人说的谎话」。

**4. 英文场景请换原版**  
中文 Skill 处理英文容易 over-edit。

**5. 与 HumanizeAI 比无「一键网页」**  
给非技术同事，解释 Claude Code 有成本。

**6. 多次迭代可能越改越短**  
连跑两轮 humanize 会删例子——我规定最多一轮自动 + 一轮手改。

### 改写前后示例（笔记口径，示意）

**改前（AI 味）：**  
「此外，这项功能至关重要，它深入探讨了现代工作流的核心格局，显著增强了团队协作效率，充分证明了其在数字化转型中的宝贵价值。」

**改后（humanize 方向）：**  
「我实际用下来，协作省下的主要是来回确认格式的那几十分钟——别指望它替你把活干完，但该对齐的人确实少找了两轮。」

差异：去掉空泛升华，换成可验证的具体场景与第一人称边界——**不是换同义词骗检测器**。

> 📷 **配图待补**：Claude Code 内改写前后并排（落盘名：humanizer-zh-hands-on.png）

---

## 💡 怎么高效用它

### 用法 1：固定工序「初稿 → 一轮 humanize → 人审」

Claude 出中文初稿后立刻 `/humanizer-zh`，人只改事实与专名。禁止连跑三次——会删光例子。

> 📷 **配图待补**：Obsidian/仓库内触发 Skill 步骤（落盘名：humanizer-zh-usage-1.png）

### 用法 2：SKILL.md 当团队 lint 规则

CI 不必接检测器；编辑对照 24 模式做 PR review checklist。视觉类 brief 若也要发社区，可先用 Lovart 定稿再 humanize 配套文案——Skill 管文字腔调，不管画面。

> 📷 **配图待补**：PR review 对照模式清单（落盘名：humanizer-zh-usage-2.png）

### 用法 3：英文段落走原版 humanizer

同一仓库中英双语稿：中文 `/humanizer-zh`，英文切 blader/humanizer，避免混 Skill。

---

## ⚠️ 注意事项：安装和使用

### 安装：npx skills add

以 op7418/Humanizer-zh README 为准；需 **Claude Code** 已配置。Skill 更新后 `git pull` 或重新 add，别用半年旧版规则。

### 中文 vs 英文

中文优化是本仓库；英文请 **blader/humanizer**。写混合语言文档时分段处理。

### 不要把「欺骗检测器」当卖点

对外发布、站外分发时，强调 **可读性与真实观点**，不承诺 bypass 任何检测服务——与项目初衷一致，也避合规雷。

### 事实与引用仍须人审

Humanize 只动文体，不验证数据；涉及价格、Stars、法规的句子必须回源。

> 📷 **配图待补**：skills 安装与版本更新（落盘名：humanizer-zh-note-permission.png）

---

## 周更里我会怎么用

周二：Claude 出 T2 母版中文 → `/humanizer-zh` 一轮 → 我补实测细节与「不好的方面」。改完后专门 grep 一遍「此外、至关重要、深入探讨」，残留就手删。  
周四：知乎版从母版派生，不再 humanize 第二次，防删例子；标题与开头段必须手改，因为 Skill 对短句容易 over-polish。  
周日：复盘 SKILL.md 里新增模式，团队共享「本周新发现的 AI 套话」一条，写进内部 banned list。  

和 HumanizeAI 分工：从不把 bypass 当 KPI；要分数游戏的人去别处，我要能发的句子。和 Grammarly 分工：英文语法 Grammarly，中文 AI 腔 Humanizer-zh。手改永远终审——Skill 省的是「找套话」时间，不是「负责」。

长文纪律：Complete Guide 级别稿件我只 humanize 章节级片段，不整篇一次扔进去——上下文太长时模型会「统一语气」把各章细节抹平。带代码块、表格、链接的段落，humanize 前先标记「勿改块内字面量」，否则版本号会被「口语化」成笑话。对外发布前仍跑一遍禁用词表（此外、至关重要等），Skill 不是万能 lint。若读者反馈「这段还是像 AI」，我会回到 SKILL.md 查对应模式编号，而不是盲目再跑一轮 humanize。英文段落永远切 blader/humanizer，不在中文 Skill 里混用——混用一次，专名就被「润」没一次。检测器分数我不记录、不承诺，只记录读者留言里「不像 AI 了」这种 qualitative 信号。

> **怎么选：** 已 daily drive **Claude Code** 且中文稿 AI 味重的人，**优先** `npx skills add` Humanizer-zh；**不用 Claude Code**、**英文为主** 或 **愿意纯手改**，**不建议**为它单独上 CC——英文用原版 humanizer，中文短稿手改可能更快。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| Claude Code 用户 | Skill 原生集成 |
| 站外分发/知乎长文 | 降 AI 腔保可读 |
| 技术写作者 | 24 模式可解释 |
| 开源 MIT 偏好 | 可 fork 定制 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 无 Claude Code | 自动化弱 |
| 英文唯一工作流 | 应使用原版 |
| 指望 100% 过检测器 | 与项目目标不符 |
| 不愿人审 | 可能删事实 |

> 📷 **配图待补**：Claude Code 写作 → humanize → 发布流程（落盘名：humanizer-zh-who-workflow.png）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐⭐ | 需 Claude Code + skills |
| 核心能力 | ⭐⭐⭐⭐ | 中文 AI 腔清单化 |
| 速度/批量 | ⭐⭐⭐⭐ | 终端内一轮改写 |
| 文档/社区 | ⭐⭐⭐⭐ | 14647★ + 维基依据 |
| 成本 | ⭐⭐⭐⭐ | MIT；CC 订阅另计 |

**综合评分：4.0 / 5.0**

> **一句话总结**：Humanizer-zh 适合在 Claude Code 里把中文 AI 腔 **按清单洗掉** 的人——目标是更好读，不是骗检测器；事实与细节，仍要你最后一眼。

---

## 🔗 Humanizer-zh 官网与项目地址

- **GitHub（中文）**：https://github.com/op7418/Humanizer-zh  
- **原版（英文）**：blader/humanizer  
- **触发命令**：`/humanizer-zh`  
- **对照**：HumanizeAI · Grammarly · 手改  
- **依据**：Wikipedia « Signs of AI writing »

---

**标签**：#ClaudeCode #Humanizer #去AI味 #开源 #T2单品

---

边界声明：测评是编辑工作流建议；Stars 与安装命令以仓库当日为准；不承诺任何检测器结果。

### BLOCK 自检（本稿）

- [x] 单主角 · 怎么选含优先/不建议 · ❌≥6  
- [x] 不售 bypass · 有改写前后示例 · Lovart 仅高效用法一句  
- [ ] 实拍图待补
