---
track: native
platform: zhihu
language: zh-CN
offsite_title: "2026 年 GitHub 上最火的 4 个 AI 设计开源项目：不会画画、不会写代码、不会剪视频的人也能交付"
approved: false
content_id: github-ai-design-tools-2026-06-09__zhihu
---

# 2026 年 GitHub 上最火的 4 个 AI 设计开源项目：不会画画、不会写代码、不会剪视频的人也能交付

做自由职业和自媒体这几年，我最大的体感是：**AI 已经不太会「只聊天」了**。今年 GitHub 上蹿得最快的一批仓库，共同点极其明显——它们输出的不是散文，而是能直接交差的产物：网页原型、React 组件、PDF 提案、甚至一条能发的短片。

我筛了 2026 年上半年 star 增速最夸张、且真正在**打破技能壁垒**的四款开源工具。下面每一款我都会按「它解决什么痛 → 怎么工作 → 我会上怎么用」讲清楚。你可以当成一份可执行的试用清单。

---

## 一、screenshot-to-code：会截图，就能拿到 React 代码（72k+ Star）

很多产品人、运营、甚至刚入门的前端，卡死的地方从来不是「有没有想法」，而是**设计到代码的最后一公里**。Figma 里图很漂亮，工程师还原两天，改一版间距又半天。外包贵，自己抠像素又不会。

[screenshot-to-code](https://github.com/abi/screenshot-to-code) 干的事极度直白：**拖一张截图进去，选技术栈，拿可运行代码出来**。它支持 HTML + Tailwind、React + Tailwind、Vue、Bootstrap 等；后端是 FastAPI，前端是 React/Vite，MIT 协议，可自托管，也有在线版 [screenshottocode.com](https://screenshottocode.com)。

更狠的是实验能力：**录屏转原型**——你录一段现有 App 的操作流程，它尝试还原成交互代码。对独立开发者来说，这几乎是「技能壁垒粉碎机」：你不必先学三年 CSS，也能把脑海里的界面变成能部署的组件骨架。当然，生成代码一定要人工 Review，但它把 **0 到 60 分** 从数天压到数分钟。

* **具体场景**：我在 Dribbble 看到一款心仪的 SaaS 仪表盘布局，截图上传，选 React + Tailwind，拿到基础布局后丢给 Cursor 补状态管理和 API，一个周末出内测版 landing + 后台壳子。
* **仓库**：https://github.com/abi/screenshot-to-code

---

## 二、Open Design：开源版 Claude Design，把 Cursor 变成设计部（61k+ Star）

2026 年 4 月 Anthropic 推出 Claude Design，第一次让大众看到「大模型可以直接吐设计产物」。但闭源、绑云、绑自家模型，对很多开发者并不友好。

GitHub 上 **61,758 Star** 的 [Open Design](https://github.com/nexu-io/open-design)（Apache-2.0）走了另一条路：**本地优先 + BYOK + Agent 原生**。它不重新发明 Agent——你已经在用的 Claude Code、Cursor、Codex、Copilot、Gemini CLI、OpenCode、Qwen 等 21+ CLI 都能接。Open Design 做的是 **Skill 路由 + 沙箱 iframe 预览 + 多格式导出**。

核心抽象是一份便携的 **`DESIGN.md`** 设计系统（内置 150+ 套，Linear、Vercel、Stripe、Apple 等风格）。你要 SaaS landing，调 `saas-landing` skill；要数据看板，走 `dashboard`；要周报 PPT，切 deck 模式。生成结果不是只能截图的 Demo，而是能导出的 **HTML / PDF / PPTX / MP4**，甚至 HyperFrames 动效。对「已经会用编码 Agent 的人」来说，这是把「做原型」从设计师专属变成了工程师顺手就能完成的事。

* **具体场景**：我给 side project 做官网，在 Open Design 选 Vercel 风格 `DESIGN.md`，用 Cursor CLI 输入「生成带定价表、FAQ、邮件订阅区的 SaaS landing」，三分钟拿到可导出 HTML，直接进 Next.js 仓库改文案和埋点。
* **仓库**：https://github.com/nexu-io/open-design  
* **体验**：https://open-design.ai

---

## 三、Open CoDesign：90 秒上手的桌面设计 Agent，订阅锁不住你（6k Star）

如果你要的不是「全栈设计系统」，而是**今晚就要出三版给客户选**，[Open CoDesign](https://github.com/OpenCoworkAI/open-codesign) 可能更对味。MIT 协议的 Electron 桌面应用，2026 年 4 月创建，强调 **local-first** 和 **多模型 BYOK**。

它最打动我的是上手路径：一键导入已有 Claude Code / Codex 配置，或直接 ChatGPT 订阅登录；也能接 DeepSeek、Kimi、GLM、Ollama、OpenRouter。Prompt 之后侧边栏**流式**吐出 HTML/JSX，在设备端沙箱 iframe 里实时预览，生成过程可中断——不像黑盒一次性吐完。导出支持 HTML、PDF、PPTX、ZIP、Markdown，同一份产物既能给老板看 PDF，也能给工程师改 HTML。

和 Open Design 比，它更像**个人创作者的工作台**：安装快、界面轻、不逼你理解整套 Skill 体系，适合自由职业设计师、独立站长、小团队运营。

* **具体场景**：接了一个茶饮品牌的视觉提案，晚上用 Kimi 连 Open CoDesign 连出三版不同排版的首页草案，并排预览，客户视频通话时当场圈选方向，当晚收定金，第二天再精修导出 PDF 定稿。
* **仓库**：https://github.com/OpenCoworkAI/open-codesign

---

## 四、libtv-skills：在终端里「拍短片」，Agent 当你的虚拟摄制组（737+ Star）

视频一直是 Personal Agent 的盲区：会写稿，不会分镜；会生图，不会剪辑。做自媒体的人对此感同身受——写脚本、找素材、对齐角色脸、配乐剪辑，一个人根本干不完。

[libtv-skills](https://github.com/libtv-labs/libtv-skills) 把 [LibTV](https://www.liblib.tv/) 的节点式视频能力封成 **Agent Skill**（MIT，Python）。`npx skills add` 挂到 OpenClaw 或 Claude Code 之后，你可以在终端说：「做一条 30 秒的 AI 工具科普短片，科技风，6 个分镜。」Agent 在后台调 LibTV：脚本节点 → 分镜图 → 主体库锁脸 → 视频节点渲染。返回的不只是 MP4，还有**可编辑画布链接**——第三镜光影不对？双击节点改灯光预设，不必整条重跑。

这是 2026 年「打破视频技能壁垒」最典型的姿势：**人定创意，Agent 跑制片，画布保底控质量**。

* **具体场景**：技术博主日更短视频，早上把提纲扔给 Agent，中午只在画布上改一个镜头，下午定时发布，全程不打开 Premiere。
* **仓库**：https://github.com/libtv-labs/libtv-skills  
* **产品**：https://www.liblib.tv/

---

## 怎么选？一张表说清楚

| 你的痛点 | 优先试 | 关键词 |
|----------|--------|--------|
| 有图没代码、还原 UI 慢 | screenshot-to-code | 设计 → 代码 |
| 要系统化原型 / Deck / 多形态交付 | Open Design | DESIGN.md + Skill |
| 要桌面、轻量、多模型、今晚出稿 | Open CoDesign | BYOK + 流式预览 |
| 要 Agent 自动做视频、还能改分镜 | libtv-skills | Skill + 画布 |

四款可以**叠用**：screenshot-to-code 还原关键页，Open Design 生成其余营销页，Open CoDesign 快速出客户提案 PDF，libtv-skills 把同一主题做成短视频引流。开源链解决的是 **0→60 分**；如果你后面要做品牌级 Campaign、跨媒介严格统一，可以再上层的 Design Agent 工具补 **60→90 分**。

---

## 写在最后

以上数据来自 2026 年 6 月 GitHub 公开信息，Star 会变动，建议以仓库为准 star 一下再试用。

若你关心的是**品牌视觉一致性**和 Campaign 级交付，而不仅是开源工具链，可以了解 [Lovart](https://www.lovart.ai?utm_source=zhihu&utm_medium=native&utm_campaign=github_ai_tools_2026) 的 MCoT 创意推理工作流——和本文四款开源工具是互补关系，不是替代关系。

**你用过哪一款？** 欢迎在评论区说说场景，我会按反馈更新这篇清单。
