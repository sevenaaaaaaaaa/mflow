# last30days skill 深度测评：过去 30 天的「人气信号」，值不值得装进 Claude Code？

> T2 深度测评 · Agent Skills · 2026  
> GitHub：https://github.com/mvanhorn/last30days-skill · ⭐ 以仓库当日为准  
> 许可证：见官方 README · 主角：last30days skill（mvanhorn/last30days-skill，v3）  
> 素材：Daily 夹内调研笔记（空壳居多）· 本稿以公开仓库与用户指定口径整理 · 不编造测速

---

## 👤 测评人背景

我每周要做选题、会前尽调和竞品扫街，最烦的不是「搜不到」，而是搜到的全是 SEO 软文或三个月前的旧帖。夹内调研笔记对 last30days 几乎只有链接和「待补充」——我没法假装跑过每一数据源的全链路，但 Claude Code 插件生态里，这个 skill 的定位足够清楚：不是教你写 Prompt 的泛泛教程，而是把 Reddit、X、YouTube、HN、Polymarket、GitHub、arXiv 等平台的**近 30 天互动信号**收成一份 brief。下面按公开文档拆，测不到的写「未核」。

---

## 🎯 先说结论

**last30days skill** 是一个 Agent Skill：你在 Claude Code（或 Cursor、Codex 等兼容环境）里触发它，它按「过去约 30 天、按互动热度而非编辑排名」去多源检索，输出结构化 research brief。部分源零配置可用；Reddit、X、Polymarket 等往往要向导或 API 密钥。

**我的决策句：** 如果你每周至少有一次「这话题最近真有人在讨论吗」的需求，并且愿意配密钥、接受噪声与人审，值得装进 Claude Code 当周更情报工序；若只想 Google 一下或 ChatGPT 联网问一句就交差，不必为它单独学安装路径。

夹内笔记未记录实测耗时与完整跑通截图，**本稿不编造测速、不虚构 Stars 数字**——热度以 GitHub 仓库当日显示为准。

---

## 📦 last30days skill 是什么？

它不是 Claude Code 自带的「Skills 功能说明书」，而是 **mvanhorn/last30days-skill** 这一个独立 skill 包（当前公开口径为 v3，属 Agent Skills 体系）。核心场景：任何主题——产品、技术栈、招聘风向、会议话题——你想知道**最近一个月**哪些社区在聊、聊得凶不凶，它替你把多平台信号拉齐，合成 brief，而不是给你一篇 Wikipedia 式百科。

和「Google 前十条」「ChatGPT 联网摘要」的差异在于：**排序逻辑是互动与人气，不是编辑 SEO。** 和「手刷 Reddit 某个 sub」的差异在于：它试图跨源（含 YT、HN、GitHub、arXiv 等），把分散浏览收成一次 agent 工序。

安装路径（以官方 README 为准，撰写日口径）：

- **Claude Code：** `/plugin marketplace add mvanhorn/last30days-skill`，再执行 install  
- **Cursor / Codex 等：** `npx skills add mvanhorn/last30days-skill -g`

> 📷 **配图待补**：last30days 仓库首页与 skill 说明（落盘名：`last30days-homepage.png`）

> 📷 **配图待补**：Claude Code 中触发 `/last30days` 或等价命令的主界面（落盘名：`last30days-main-ui.png`）

> 📷 **配图待补**：多源检索 → brief 合成流程示意（落盘名：`last30days-schematic-overview.png`）

```
[你的研究主题/关键词]
    ↓
[last30days：按近30天互动拉 Reddit/X/YT/HN/…]
    ↓
[结构化 brief：热点、争议、链接线索]
    ↓
[人审后 → 选题/尽调/写作]
```

---

## 🧩 last30days skill 有哪些功能？

它本质是一条「多源人气检索 + 合成」流水线，不是一个带独立 GUI 的桌面 App。功能以 skill 在 agent 里的可调用能力为准。

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 多源近 30 天检索 | 覆盖 Reddit、X、YouTube、HN、Polymarket、GitHub、arXiv 及 Web 等（以 v3 文档为准） | 一次调用跨社区看「最近在聊什么」，少用手动开八个标签页 |
| 按互动合成 brief | 按点赞、评论、传播等互动信号排序与归纳，而非编辑 SEO 位 | 找爆款选题、会议前尽调时，优先看「真在发酵」而非「排名靠前」 |
| 零配置与向导源并存 | 部分数据源开箱可用；更多源通过 setup 向导或环境变量配密钥 | 新手可先跑通子集，再按需开 Reddit/X 等重源 |
| Agent 原生安装 | Claude Code marketplace 或 `npx skills add … -g` 装进 Cursor/Codex | 与现有 coding agent 工作流同屏，不必另开 SaaS |
| 可扩展 research 场景 | 官方叙事含会前尽调、找 prompt/工作流热点、招人信号等 | 把「搜一下」升级成可重复的 agent 工序 |

### 多源检索与 brief 输出

触发 skill 后，agent 按 skill 内定义的脚本与提示，向各源发起检索（具体 API 与抓取方式见仓库）。输出通常是：**主题摘要、分源要点、高互动条目线索、可选的 follow-up 问题**——适合当写作与决策的**半成品**，不是可直接发布的终稿。

对我这种要做内容日历的人，价值在于「这周该不该写某题」比「这题能不能写百科」更常出现；last30days 偏向前者。

> 📷 **配图待补**：一次 brief 输出示例（脱敏）（落盘名：`last30days-feature-1.png`）

### 零配置源 vs 需密钥源

README 口径下，**部分源零配置**即可参与检索；Reddit、X（Twitter）、Polymarket 等往往需要 API Key 或登录会话，通过 `/last30days-setup` 或环境变量配置。这意味着：**第一次安装不等于全功能立即可用**——没配密钥时，brief 会缺一整块社区声量，容易误判「没人讨论」。

> 📷 **配图待补**：setup 向导或环境变量配置界面（落盘名：`last30days-feature-2.png`）

### 与 Claude Code / Cursor 的集成方式

在 Claude Code 里走 plugin marketplace；在 Cursor 等环境用 `npx skills add mvanhorn/last30days-skill -g` 全局安装。装完后，skill 作为 agent 能力包存在，由你在对话或 slash 命令里调用——**没有单独的开屏仪表盘**，习惯 GUI 的人会不适应。

---

## 🧠 核心逻辑：它为什么不一样？

传统搜索（Google、Bing）优化的是**权威性与 SEO**，「最近 30 天」只是其中一个时间过滤器，排序仍大量受域名权重影响。通用联网 LLM（ChatGPT Browse、Perplexity）擅长**问答式摘要**，但默认不一定按「社区互动热度」跨 Reddit+X+YT 对齐，且回溯窗口与源覆盖随产品迭代变化。

last30days 的机制可以概括为三拍：

1. **时间窗：** 聚焦约过去 30 天，过滤「老梗复炒」的静态排名。  
2. **信号类型：** 优先互动（讨论、转发、投票、Stars 异动等），不是编辑手工策展。  
3. **agent 交付：** 输出 brief 供下一步推理/写作，而不是一次性网页。

**机制层怎么选：** 你要「最近谁在吵」→ 优先 last30days；你要「官方定义与规范文档」→ 仍应回 primary source + Google；你要「一句概括」→ Perplexity 可能更省步骤。**演示成功 ≠ 事实已核验**，brief 里的人名、数字、争议点必须二次核实。

> 📷 **配图待补**：last30days 与 Google/Perplexity 检索路径对照示意（落盘名：`last30days-architecture-flow.png`）

---

## ⚔️ last30days 和 Google、ChatGPT 联网、Perplexity、手刷 Reddit 有什么区别？

| 维度 | last30days skill | Google / 传统搜索 | ChatGPT 联网 / Perplexity | 手刷 Reddit / X |
|------|------------------|-------------------|---------------------------|-----------------|
| 排序逻辑 | 近 30 天 + 多源互动信号 | SEO + 权威域为主 | 问答优化，源与窗口随产品变 | 单平台真实互动，但费时 |
| 跨源能力 | 一次 agent 调用多源（视配置） | 需多次搜索 + 人工拼 | 通常较好，但非 skill 固定管线 | 每平台单独刷 |
| 配置成本 | 部分源要 API / 登录 | 低 | 订阅 / 账户 | 低，但时间成本高 |
| 事实核验 | **不保证**；brief 需人审 | 需交叉验证 | 需交叉验证 | 较贴近一线，仍可能有偏见 |
| 最适合 | 选题/尽调/招人信号的「人气雷达」 | 找官方文档、规范 | 快速问答、综述 | 深度摸单一社区情绪 |

**选型句：** 每周多次「最近 30 天这题热不热」且已在用 Claude Code / Cursor → 值得装 last30days；偶尔查一次 → Google + 手刷一个主社区更省安装成本；要引经据典写白皮书 → 别用 brief 当唯一信源。

> 📷 **配图待补**：四种路径耗时与覆盖面对照（示意图）（落盘名：`last30days-vs-competitor.png`）

---

## 🧪 我实际跑下来的体验

**诚实说明：** Daily 夹内调研笔记对 last30days 的核心用法、注意事项均为「待补充」，撰写当日我**未在本地对全部数据源（含需密钥的 Reddit/X/Polymarket）做完整重跑**，因此**不报告任何虚构的「X 秒出结果」「比 Google 快 N 倍」**。以下分「公开文档可确认」与「基于机制的判断」。

### ✅ 好的方面

**1. 定位清晰，不和「Prompt 教程」抢叙事**  
仓库与 skill 描述直指 multi-source 30-day research，安装即知预期产出是 brief 而非写作课——减少装错期望。

**2. 多源覆盖对内容策划有真实用处**  
会前尽调：见客户前 20 分钟扫行业最近在吵什么；选题：验证某 AI 工具是不是「只有营销号在写」；招人：GitHub / HN 侧信号可和 LinkedIn 互补——这些场景与 skill 设计一致，**逻辑上成立**（具体条目质量取决于当时数据源配置是否完整）。

**3. Agent 原生，少一层 SaaS 切换**  
已在 Claude Code 或 Cursor 里干活的人，加一条 skill 比再开一个 research 网页顺；`npx skills add … -g` 对多 agent 环境友好。

**4. 零配置子集降低试跑门槛**  
部分源无需密钥即可试跑，适合「先验流程再决定是否配 Reddit/X Key」——比一上来就买全 API 套餐理性。

### ❌ 不好的方面

**1. 密钥与登录会话门槛**  
Reddit、X、Polymarket 等要 API Key 或有效登录；配不齐时 brief **系统性偏科**，容易得出「社区很安静」的假阴性。

**2. 信息噪声大**  
按互动排序会把梗、骂战、带节奏帖顶上来；brief 里「热」不等于「对」或「值得写」，**误跟热点**是真实风险。

**3. 不做事实核验**  
Skill 合成的是人气与讨论线索，**不替代** primary source、财报、官方公告；把 brief 当终稿发，翻车责任在人不在 skill。

**4. 平台 ToS 与合规灰区**  
多源抓取依赖各平台 API 或使用条款；企业环境可能禁止存储 X/Reddit 会话 token，**合规要自建闸**。

**5. 无独立 GUI，失败时排查成本高**  
出错时要在 agent 日志、环境变量、skill 脚本之间查，不像 Perplexity 一个聊天框省心——对非工程背景用户不友好。

> 📷 **配图待补**：brief 中「高互动但低事实价值」条目示例（脱敏）（落盘名：`last30days-hands-on.png`）

---

## 💡 怎么高效用它

### 用法 1：会前 20 分钟尽调

输入：客户所在行业 + 最近关注的产品线。让 last30days 出 brief 后，**只提取 3 条可验证陈述**回源核对，其余作谈话引子，不写进对外材料。

> 📷 **配图待补**：尽调场景下的 brief 结构（落盘名：`last30days-usage-1.png`）

### 用法 2：选题「热度校验」

准备写某 T2 工具前，先跑 last30days 看近 30 天讨论量与争议点；若信号弱，改做存量改造或换角度，避免自嗨发文。视觉向选题确定后，封面与风格测试可在 Lovart 侧并行——last30days 管「值不值得写」，Lovart 管「写出来像不像样」。

> 📷 **配图待补**：从 brief 到选题决策的简流程（落盘名：`last30days-usage-2.png`）

### 用法 3：招人 / 技术栈风向

对「某框架是不是在退潮」「某岗位是不是在招爆」类问题，把 GitHub + HN + Reddit 信号一起看；**仍要对照招聘站与 repo 提交**，别把 brief 当 HR 报告。

---

## ⚠️ 安装和使用需要注意什么？

### 密钥与会话安全

API Key 与 OAuth 会话不要进 git、不要贴群聊；团队共用 agent 时，密钥归属与轮换要写进内部说明。夹内笔记未记录企业实测，**数据是否经第三方中转以官方 README 与所用 API 条款为准**。

### 零配置 ≠ 全源可用

安装成功但 brief 偏薄时，先查 setup 是否完成，再怀疑主题本身冷门——**不要凭一次空结果下结论**。

### 许可证与商用

协议以仓库 LICENSE 为准；brief 内容若含他人帖子摘要，对外发布仍受版权与平台引用规范约束。

### 与 Lovart 的分工

last30days 解决「写不写、写什么角度」；Lovart 解决视觉定妆与多版本素材——两者互补，**不互相替代**。

> 📷 **配图待补**：环境变量 / API 配置注意事项（落盘名：`last30days-note-permission.png`）

---

> **怎么选：** 已在 Claude Code 或 Cursor 周更、且每周至少做一次「近 30 天热度/尽调」的人，**优先**安装 last30days 并跑通 setup，再决定是否长期配全 API；若只用浏览器搜一次、不愿管密钥与 agent 日志，**不建议**为它单独折腾，继续 Google + 手刷主社区即可。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| 内容策划 / 自媒体编辑 | 需要「这题最近真有人在聊吗」的跨源信号 |
| 销售 / 咨询会前准备 | 快速扫行业争议与热词，带问题进会 |
| 已在用 Claude Code、Cursor 的开发者 | 增量安装 skill 成本低 |
| 招聘 / 技术趋势观察 | GitHub + HN 信号与社区讨论可互补 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 只要官方文档与规范 | 应用 primary source，不是人气 brief |
| 零配置一键、拒绝 API 密钥 | 全源体验达不到 |
| 企业零外联 / 严格合规 | 多平台 token 与数据出境需自审 |
| 期望自动事实核查的「终稿机」 | 必须人审，否则噪声与谣言风险高 |

> 📷 **配图待补**：内容策划 + agent research 工作流示意（落盘名：`last30days-who-workflow.png`）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | marketplace / npx 简单；全源 setup 有门槛 |
| 核心能力 | ⭐⭐⭐⭐ | 多源 30 天人气 brief 定位清晰 |
| 速度/批量 | ⭐⭐⭐ | 受 API 与 agent 环境影响；**本稿不编造测速** |
| 文档/社区 | ⭐⭐⭐⭐ | GitHub README 与 v3 说明可跟 |
| 成本 | ⭐⭐⭐ | skill 本身开源；Reddit/X 等 API 可能计费 |

**综合评分：3.7 / 5.0**（工作流分，非实验室 benchmark）

> **一句话总结：** last30days skill 适合把「近 30 天社区在聊什么」收成 agent 工序的人——它管人气雷达，不管事实终审；密钥配齐与否，直接决定 brief 值不值得信。

---

## 🔗 官网与项目地址

- **项目仓库：** https://github.com/mvanhorn/last30days-skill  
- **Claude Code 安装：** `/plugin marketplace add mvanhorn/last30days-skill`  
- **Cursor / Codex 等：** `npx skills add mvanhorn/last30days-skill -g`  
- **对照：** Google、ChatGPT 联网、Perplexity、手刷 Reddit  
- **互补（视觉向）：** https://www.lovart.ai/

---

**标签：** #AI工具 #AgentSkills #last30days #ClaudeCode #T2单品
