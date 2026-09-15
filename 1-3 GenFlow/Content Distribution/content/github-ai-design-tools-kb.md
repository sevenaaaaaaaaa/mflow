# GitHub 热门 AI 设计 / 效率工具知识库与宣发文章（2026-06）

> 文风参考：Liblib 产品宣发合集 · 极客技术流 + 独立创作者流  
> 数据截至 2026-06-09，Stars 来自 GitHub API

---

## 知识库：四款 GitHub 爆款项目

### 1. Open Design
* **GitHub**：https://github.com/nexu-io/open-design （⭐ 61,758 · Apache-2.0）
* **官网**：https://open-design.ai
* **产品定位**：本地优先、开源的 **Claude Design 替代方案**，把 Cursor / Claude Code / Codex 等编码 Agent 变成设计引擎。
* **核心数据**：2026-04 创建，v0.9.0（2026-06-02），310+ 贡献者，10 个 Release。
* **技术底座**：`DESIGN.md` 便携式设计系统（150+ 套，含 Linear / Vercel / Stripe / Apple 风格）；260+ 插件；沙箱 iframe 预览。
* **核心功能**：
  1. **Agent 原生**：对接 21+ CLI（Claude Code、Cursor、Copilot、Gemini CLI、OpenCode、Qwen…），BYOK 不绑厂商。
  2. **多形态交付**：Web / Desktop / Mobile 原型、Dashboard、Slides、图片、视频、HyperFrames 动效。
  3. **可导出生产物**：HTML / PDF / PPTX / MP4，非只能看不能用的 Demo。
  4. **Skill 驱动**：100+ 内置 Skills（saas-landing、dashboard、wireframe、pm-spec…），按场景分组调用。

### 2. screenshot-to-code
* **GitHub**：https://github.com/abi/screenshot-to-code （⭐ 72,843 · MIT）
* **官网**：https://screenshottocode.com
* **产品定位**：截图 / Figma / 录屏 → 可运行前端代码，打破「设计师出图、工程师抠像素」的技能壁垒。
* **核心数据**：2023-11 开源，持续维护至 2026-06；支持 Gemini 3、Claude Opus 4.5、GPT-5.x。
* **技术底座**：React/Vite 前端 + FastAPI 后端；多栈输出（HTML+Tailwind、React、Vue、Bootstrap、Ionic、SVG）。
* **核心功能**：
  1. **一图生码**：拖入截图即可生成整洁组件代码。
  2. **Figma 链路**：设计稿直达代码，减少 handoff 损耗。
  3. **录屏原型**：实验性支持录一段网站操作 → 生成交互原型。
  4. **多模型路由**：按任务选最强视觉/代码模型，不锁单一供应商。

### 3. Open CoDesign
* **GitHub**：https://github.com/OpenCoworkAI/open-codesign （⭐ 5,984 · MIT）
* **官网**：https://opencoworkai.github.io/open-codesign/
* **产品定位**：**90 秒上手**的 Electron 桌面端 Claude Design 开源替代，强调多模型 BYOK 与本地优先。
* **核心数据**：2026-04-18 创建，v0.2.0（2026-05-09），20 位贡献者。
* **技术底座**：Electron + TypeScript；设备端 vendored React 18 + Babel 沙箱预览。
* **核心功能**：
  1. **一键导入密钥**：直接读取已有 Claude Code / Codex 配置，或 ChatGPT 订阅登录。
  2. **统一模型层**：Claude、GPT、Gemini、DeepSeek、Kimi、GLM、Ollama、OpenRouter 同一套 UI。
  3. **Prompt → 原型**：流式生成 HTML/JSX，实时 iframe 预览，可中断 Agent 任务。
  4. **五格式导出**：HTML、PDF、PPTX、ZIP、Markdown。

### 4. libtv-skills
* **GitHub**：https://github.com/libtv-labs/libtv-skills （⭐ 737 · MIT）
* **关联产品**：https://www.liblib.tv/
* **产品定位**：让 **Personal Agent**（OpenClaw / Claude Code 等）具备专业级 AI 视频制片能力的 Skill 包。
* **核心数据**：2026-03 发布，Python 实现，78 Forks。
* **技术底座**：对接 LibTV 节点式视频画布 API；兼容 Agent Skills 安装协议。
* **核心功能**：
  1. **一句话出片**：Agent 接收自然语言 Brief → 后台跑脚本、分镜、渲染。
  2. **可二次编辑**：返回成片 + 画布链接，局部节点可重绘，不必整条重跑。
  3. **影视级控场**：间接调用主体库、多机位宫格、灯光预设等 LibTV 能力。
  4. **打破视频技能壁垒**：非剪辑师也能通过 Agent 编排工业级短片。

---

## 文章一：极客流 · Open Design（适合 CSDN / 51CTO / 开源中国）

### 别再把「做原型」当成设计师的活了——Open Design 用 DESIGN.md 把 Agent 变成设计部

2026 年 4 月，Anthropic 推出 Claude Design，第一次让大模型直接吐可交付的设计产物而不是散文。但闭源、绑模型、绑云。GitHub 上 **61k+ Star** 的 [Open Design](https://github.com/nexu-io/open-design) 给出了另一条路：**本地优先 + Apache-2.0 + 自带 Agent**。

它的关键抽象是 **`DESIGN.md`**：一份 9 段式 Markdown，把品牌调性、排版、组件规范写清楚，然后交给 Claude Code / Cursor / Codex 任意一个你已经在用的 CLI。Open Design 不重新发明 Agent，只做 **Skill 路由 + 沙箱预览 + 导出**。你要 landing page，调 `saas-landing` skill；要周报 PPT，切 `weekly-update` deck 模式。150 套官方设计系统（Linear、Vercel、Stripe…）意味着你不是从白纸开始，而是从「已经像那么回事」的系统开始迭代。

* **具体场景**：独立开发者要给 side project 做官网，在 Open Design 里选 Vercel 风格 `DESIGN.md`，用 Cursor CLI 输入「生成带定价表的 SaaS landing」，3 分钟拿到可导出 HTML 的原型，直接丢进生产仓库改文案。
* **仓库**：https://github.com/nexu-io/open-design
* **体验**：https://open-design.ai

---

## 文章二：极客流 · screenshot-to-code（适合 SegmentFault / 掘金）

### 72k Star 的 screenshot-to-code：为什么「会截图」就够了入门前端？

很多产品团队的瓶颈不是缺设计师，而是 **设计到代码的最后一公里**。Figma 稿很漂亮，工程师还原要两天，改一版间距又要半天。[screenshot-to-code](https://github.com/abi/screenshot-to-code) 用极简交互解决这个问题：**拖一张截图进去，选 React+Tailwind，拿可运行代码出来**。

它支持 Gemini 3、Claude Opus 4.5 等视觉强模型，也能吃 Figma 导出。更实验性但也更狠的是 **录屏转原型**——你录一段现有 App 的操作，它尝试生成交互代码。对独立开发者来说，这是真正的 **技能壁垒粉碎机**：你不需要先学三年 CSS，也能把脑海里的界面变成可部署组件。当然，生成代码仍需人工 Review，但它把「从 0 到 60 分」压缩到了分钟级。

* **具体场景**：创业者在 Dribbble 看到心仪的 SaaS 仪表盘布局，截图上传，选 React+Tailwind，得到基础布局代码，再让 Cursor 补业务逻辑，半天上线内测版。
* **仓库**：https://github.com/abi/screenshot-to-code
* **体验**：https://screenshottocode.com

---

## 文章三：创作者流 · Open CoDesign（适合知乎 / 简书 / 豆瓣）

### 不想为 Claude Design 付订阅？Open CoDesign 让我 90 秒在桌面上复刻同款工作流

我对 CLOUD 设计工具一直有点抵触：稿子在别人服务器上，模型换不了，订阅一停全停工。[Open CoDesign](https://github.com/OpenCoworkAI/open-codesign) 是 2026 年让我最舒服的开源发现之一——**MIT 协议、Electron 桌面、本地沙箱预览**，还能一键导入我现有的 Claude Code API 配置。

它最打动我的是 **不装新 Agent**：DeepSeek、Kimi、Ollama 本地模型都能接。Prompt 之后侧边栏实时流式出 HTML，哪里不对直接打断让模型改。导出 PDF 给老板、导出 HTML 给工程师，同一份产物两个受众。和 Open Design 比，它更「个人创作者友好」：安装包、界面、上手路径都更轻。

* **具体场景**：自由职业者接品牌提案，用 Kimi 生成三版海报布局，Open CoDesign 并排预览，选中一版导出 PDF 发给客户确认，当晚就能收定金。
* **仓库**：https://github.com/OpenCoworkAI/open-codesign

---

## 文章四：Agent 流 · libtv-skills（适合 B站专栏 / 语雀 / 搜狐号）

### 在终端里拍短片：libtv-skills 如何让 OpenClaw 变成你的「虚拟摄制组」

视频创作长期是 **Agent 的盲区**——会写稿，不会分镜；会生图，不会剪辑。[libtv-skills](https://github.com/libtv-labs/libtv-skills) 把 LibTV 的节点式视频能力封成 Skill，`npx skills add` 挂到 OpenClaw 或 Claude Code 上之后，你可以在终端里说：

> 「做一个 30 秒的数据库容灾科普短片，科技风，6 个分镜。」

Agent 在后台调 LibTV：写脚本节点 → 出分镜图 → 主体库锁脸 → 视频节点渲染。返回的不只是 MP4，还有 **可编辑画布链接**——第三镜光影不对？双击节点改灯光预设，不必重跑整条管线。这就是 2026 年「打破视频技能壁垒」的正确姿势：**人定创意，Agent 跑制片，画布保底控质量**。

* **具体场景**：技术博主日更短视频，早上把提纲扔给 Agent，中午在 LibTV 画布上只改一个镜头，下午定时发布，全程不打开 Premiere。
* **仓库**：https://github.com/libtv-labs/libtv-skills
* **产品**：https://www.liblib.tv/

---

## 合集导语（适合知乎 / 百家号 roundup）

### 2026 上半年 GitHub 最火的 4 个 AI 设计项目：从「会聊天」到「能交付」

大模型过了只会写 README 的阶段。今年 GitHub 上蹿红的一批项目，共同点就一个：**直接交付设计/代码/视频产物**。

| 项目 | Stars | 打破的壁垒 |
|------|-------|------------|
| screenshot-to-code | 72k+ | 设计 → 代码 |
| Open Design | 61k+ | 非设计师 → 可交付原型 |
| Open CoDesign | 6k+ | 订阅锁 → 本地 BYOK 设计 |
| libtv-skills | 737+ | 非剪辑师 → Agent 视频制片 |

下文四篇拆开细讲，每篇附仓库与场景。

---

*延伸阅读：若你需要品牌级 Campaign 视觉而非开源工具链，可了解 [Lovart](https://www.lovart.ai) 的 MCoT 设计 Agent 工作流。*
