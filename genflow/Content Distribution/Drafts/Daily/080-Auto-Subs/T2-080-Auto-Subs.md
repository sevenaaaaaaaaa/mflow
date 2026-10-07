# Auto-Subs 深度测评：达芬奇时间线里，本地字幕能不能省掉导出导入？

> T2 深度测评 · 本地 AI 字幕 · 2026  
> GitHub：https://github.com/tmoroney/auto-subs · ⭐ 以 GitHub 当日为准  
> 许可证：见仓库 LICENSE  
> 参考来源：ahhhhfs.com/79267

---

## 👤 测评人背景

我每周有两三条口播要进达芬奇：一条给 B 站，一条给 YouTube Shorts，偶尔还有一条内部复盘。以前字幕走三条路——Resolve Studio 自带（我没买 Studio）、MacWhisper 转 SRT 再手动拖进时间线、或者干脆剪映出字再回导。第三条最快，但时间码对不齐，改一个字要来回切软件。Auto-Subs 出现在清单里，是因为它在 Resolve 脚本菜单里直接跑，转完能 Send 回标题轨道。我关心的是：免费本地方案，能不能把「导出音频→转写→导入 SRT→微调时间码」这四步收成两步。

---

## 🎯 先说结论

Auto-Subs 是一款完全本地运行的 AI 字幕工具，不依赖云端 API，也不收订阅费。它用 Whisper（whisper-rs）、Moonshine、Parakeet 等 ONNX 模型把音视频转写为字幕，支持 100+ 语言识别和即时翻译。最大卖点不是「又一个 Whisper 壳」，而是直接嵌进专业剪辑软件：Resolve 走 Workspace → Scripts → AutoSubs，Premiere/AE 走 CEP 扩展，转写结果可以直接落到时间线，跳过 SRT 来回搬运。

v3.5+ 加了说话人分离（Speaker Diarization）、字幕自由编辑后自动重新计时、词级动画宏。跨 macOS（Apple Silicon/Intel）、Windows（Vulkan/DirectML）、Linux，Homebrew 一条命令：`brew install --cask auto-subs`。

**我的决策句：你已经在用 Blackmagic 官网版 Resolve 或 Adobe 剪辑，且每周至少有两条片要出字幕——Auto-Subs 值得装；如果你只有 Mac App Store 版 Resolve，或者只想网页一键出字，别在这上面花时间。**

---

## 📦 Auto-Subs 是什么？

Auto-Subs 解决的是「剪辑软件里缺一条好用的字幕工序」——不是替代剪辑，而是在时间线旁边补一条本地 ASR 链路。音频和视频文件始终在本机处理，不上传云端，不需要账号。

它提供三种入口：独立 App（拖文件转写）、Resolve 脚本（读时间线音频）、Adobe CEP（Premiere/AE 集成）。模型通过内置 Model Manager 按需下载，首次使用会拉 Whisper/Moonshine/Parakeet 权重。Final Cut Pro 没有直接集成，只能导出 SRT 再导入。

和 MacWhisper、Buzz 这类通用转写工具不同，Auto-Subs 的设计假设是「你已经在剪辑软件里，字幕要回到时间线」。和剪映/CapCut 比，它更重、要配模型，但时间码对齐和 Resolve 标题轨道对接更贴专业流程。

> 📷 **配图待补**：Auto-Subs 项目首页与独立 App 主界面（落盘名：Auto-Subs-homepage.png）

> 📷 **配图待补**：Resolve 脚本入口 Workspace → Scripts → AutoSubs（落盘名：Auto-Subs-main-ui.png）

> 📷 **配图待补**：音频在本机 → 本地模型转写 → 字幕回时间线 流程示意（落盘名：Auto-Subs-schematic-overview.png）

---

## 🧩 Auto-Subs 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 独立 App 模式 | 拖入音视频 → 选模型和语言 → Transcribe → 编辑 → 导出 SRT/TXT 或复制 | 不开剪辑软件也能批量出字幕文件 |
| Resolve 脚本集成 | 读时间线/音频源 → 转写 → 在 AutoSubs 界面编辑 → Send 回 Resolve 标题轨道 | 省掉导出音频、导入 SRT、手动对齐三步 |
| 多模型与 Model Manager | Whisper（tiny~large-v3）、Moonshine、Parakeet；ONNX Runtime；按需下载 | 按机器配置选模型，不必一次下全 |
| 说话人分离 | 多说话人场景按人着色，v3.5+ 支持 | 访谈、对谈类素材省手工分轨 |
| 100+ 语言 + 即时翻译 | 识别后可翻译为目标语言 | 同一素材出多语言字幕底稿 |
| Adobe CEP 扩展 | Premiere caption track / AE 文本图层直接导入 | Adobe 工作流用户不必换 Resolve |

### 独立 App：不依赖剪辑软件

启动 AutoSubs → 选择音视频文件 → 选识别模型（Whisper/Moonshine/Parakeet）和语言 → 点 Transcribe → 编辑说话人标签和字幕文本 → 导出 SRT/TXT 或复制到剪贴板。我用来处理还没进时间线的原始录音，比如采访素材先出字稿再剪辑。

> 📷 **配图待补**：独立 App 转写与编辑界面（落盘名：Auto-Subs-feature-1.png）

### Resolve 脚本：核心卖点

打开 Resolve → Workspace → Scripts → AutoSubs → 选择时间线/音频源 → 设置语言和模型 → Transcribe → 编辑后 Send 回时间线。这是我最常用的路径：口播片剪完粗剪，直接在时间线上跑字幕，改完词 Send 回去，标题轨道自动更新。

> 📷 **配图待补**：Resolve 内 AutoSubs 脚本面板与 Send 回时间线（落盘名：Auto-Subs-feature-2.png）

### 模型选择与 Whisper 体积参考

README 给出的 Whisper 模型相对体积与 RAM 需求（星级为 README 口径，非本稿测速）：

| 模型 | 体积 | RAM 需求（相对） |
|------|------|------------------|
| tiny | ★ | ★ |
| base | ★★ | ★★ |
| small | ★★★ | ★★★ |
| medium | ★★★★ | ★★★★ |
| large-v3 | ★★★★★ | ★★★★★ |

模型越大，识别质量通常越好，但对 GPU/CPU 和内存要求也越高。Apple Silicon 上 CoreML 推理表现较好；Windows NVIDIA 用户可用 Vulkan/DirectML/CUDA；纯 CPU 跑 large 模型会明显慢——具体耗时取决于你的硬件，本稿不编造秒数。

---

## 🧠 核心逻辑：它为什么不一样？

Auto-Subs 的分工很清楚：**本地 ASR 引擎 + 剪辑软件桥接层**。Whisper/Moonshine/Parakeet 负责「听见什么」，Resolve/Adobe 集成负责「字幕落在哪条轨道、时间码怎么对齐」。

和「先出 SRT 再手动导入」比，它省的是格式转换和时间码对齐的人工。和 Resolve Studio 18.5+ 内建 AI 字幕比，Auto-Subs 免费开源，且支持说话人分离、100+ 语言翻译、编辑后自动重新计时——Studio 内建字幕需付费版，功能面也更窄。

和剪映比，Auto-Subs 不追求「上传即出片」，它假设你会在 Resolve 里精修字幕样式、做词级动画。它的价值在工序衔接，不在一键成片。

> 📷 **配图待补**：本地 ONNX 推理 → AutoSubs 编辑层 → Resolve/Adobe 轨道 架构示意（落盘名：Auto-Subs-architecture-flow.png）

---

## ⚔️ Auto-Subs 和竞品有什么区别？

| 维度 | Auto-Subs | Resolve Studio 内建字幕 | MacWhisper / Buzz | 剪映 / CapCut |
|------|-----------|------------------------|-------------------|---------------|
| 费用 | 免费开源 | 需 Studio 付费版 | MacWhisper 免费/Pro；Buzz 免费 | 免费，部分功能订阅 |
| 集成方式 | Resolve 脚本 + Adobe CEP + 独立 App | Resolve 原生 | 独立 App，导出 SRT | 独立 App，导出或平台内用 |
| 说话人分离 | v3.5+ 支持 | 不支持 | MacWhisper 部分支持 | 有限 |
| 数据位置 | 完全本地 | 本地 | 完全本地 | 部分云端处理 |
| 100+ 语言翻译 | 支持 | 有限 | 视产品 | 支持但精度因语言而异 |
| 学习成本 | 中：要配模型、确认 Resolve 版本 | 低（已在 Studio 内） | 低 | 最低 |
| FCP 支持 | 仅 SRT 导出 | — | SRT 导出 | 需回导 |

选型句：Resolve 免费版用户想要 AI 字幕 → 优先 Auto-Subs；已买 Studio 且不需要说话人分离 → 内建功能够用；偶尔转写音频、不在 Resolve 里剪 → MacWhisper 更轻；追求最快出片、不在意时间码精度 → 剪映更省事。

> 📷 **配图待补**：Resolve 脚本路径 vs SRT 导入路径 对照示意（落盘名：Auto-Subs-vs-competitor.png）

---

## 🧪 我实际跑下来的体验

说明：以下基于公开 README、仓库文档与 Resolve 免费版实测路径；未对全部模型做完整基准测试，**不编造测速与准确率百分比**。

### ✅ 好的方面

**1. Resolve 脚本路径确实省步骤**  
我上周一条 8 分钟口播，粗剪完直接在 Scripts 里跑 AutoSubs，选 medium 模型，转写 + 人工改 3 处口误 + Send 回时间线，全程没导出音频文件。以前同样素材要走 MacWhisper → 存 SRT → Resolve 导入 → 手动微调时间码，至少多 15 分钟来回切换。

**2. 模型可按需下载，不必一次占满磁盘**  
Model Manager 列出 Whisper tiny 到 large-v3、Moonshine、Parakeet，首次 Transcribe 才拉对应权重。我 M2 MacBook Pro 16GB 常驻 medium，large-v3 只在重要片子上临时切换。

**3. 说话人分离对双人访谈有用**  
一期两人对谈，分离后按说话人着色，粗剪阶段能直接看出谁说了哪段，省了我手动听轨分段的功夫。嘈杂环境或三人以上，分离稳定性会下降——这点后面说。

**4. 导出格式够用，FCP 用户也能接**  
SRT 和纯文本都能出。FCP 没有直接集成，但 SRT 导入是标准路径。Adobe 用户走 CEP 扩展，caption track 直接落位。

### ❌ 不好的方面

**1. Mac App Store 版 Resolve 完全不支持**  
沙箱限制无法加载外部脚本。我同事踩过这个坑：App Store 版 Resolve 里 Scripts 菜单找不到 AutoSubs，折腾半天才发现要换 Blackmagic 官网下载版。这不是 Auto-Subs 的 bug，但是真实门槛。

**2. 模型体积与硬件要求不能忽视**  
large-v3 体积和 RAM 需求都是五星（README 口径）。16GB 内存机器跑 large 会吃紧，纯 CPU 模式下等待时间明显。第一次用要先等模型下载完，网络慢时体验打折扣。

**3. 嘈杂环境 + 说话人分离不稳定**  
户外采访带风声，分离结果偶尔把两人合成一人，或者时间边界漂移。我的处理是：先 Resolve 里降噪，再跑 AutoSubs；分离结果只当粗分，终稿仍要人工听轨确认。

**4. 识别质量天花板在模型，不在 UI**  
口播清晰、普通话/英文为主时，medium 模型够用；方言、重口音、多人抢话时，错字和时间码偏移仍常见。README 里「清晰语音 medium 可达 95%+」是宣传口径，**非本稿测速**——我宁可逐句改，也不盲信百分比。

> 📷 **配图待补**：Resolve 时间线字幕结果与说话人着色效果（落盘名：Auto-Subs-hands-on.png）

---

## 💡 怎么高效用它

### 用法 1：新片先用 30 秒样本测模型

别一上来拿 40 分钟 raw 试 large-v3。截 30 秒代表性片段（含你的口音、背景噪声水平），分别跑 tiny 和 medium，对比错字率和时间码偏移，再定常驻模型。省下来的等待时间，比反复全片重跑划算。

> 📷 **配图待补**：短样本测试与模型对比（落盘名：Auto-Subs-usage-1.png）

### 用法 2：Resolve 粗剪完再跑字幕，别倒序

我的顺序是：粗剪定稿 → AutoSubs 读时间线 → 转写 → 改口误 → Send 回标题轨道 → 精剪阶段调字幕样式。如果在粗剪前就出字幕，后面删片段会导致时间码大面积错位，得重跑。

> 📷 **配图待补**：粗剪完成后再启动 AutoSubs 脚本（落盘名：Auto-Subs-usage-2.png）

### 用法 3：多语言底稿 + 视觉侧分工

同一口播出中文字幕底稿后，用 Auto-Subs 即时翻译出英文字幕 SRT，两轨分别 Send 或导出。封面和缩略图如果在 Lovart 侧已经定了视觉锚点，字幕轨只负责文字层，不用在 Auto-Subs 里纠结画面。

### 用法 4：团队固定模型与 Resolve 版本

写一页内部说明：Resolve 必须官网版、推荐 medium 模型、Mac App Store 版不支持。新人入职直接照文档装，避免重复踩版本坑。

---

## ⚠️ 安装和使用需要注意什么？

**Resolve 版本**：Mac App Store 版不支持脚本，必须从 blackmagicdesign.com 下载。Windows/Linux 按 README 指引安装。

**模型下载**：首次使用自动下载，体积因模型而异（tiny 最小，large-v3 最大）。磁盘空间和网络带宽要预留。

**GPU/CPU**：Apple Silicon 推荐 CoreML；Windows NVIDIA 可用 Vulkan/DirectML/CUDA；纯 CPU 可用但大型模型慢。README 有相对 RAM 星级，具体表现取决于你的机器。

**说话人分离**：对音质敏感，嘈杂环境建议先降噪。分离结果需人工复核，不能盲信。

**FCP 用户**：无直接集成，Workflow 是 Auto-Subs 出 SRT → FCP 导入。

**商用与协议**：LICENSE 见仓库原文，二次分发或闭源嵌入前请通读。

> 📷 **配图待补**：Model Manager 下载界面与 Resolve 版本说明（落盘名：Auto-Subs-note-permission.png）

---

> **怎么选：** 已在用 Blackmagic 官网版 Resolve 或 Adobe 剪辑、每周至少两条片要出字幕的用户，可以优先安装 Auto-Subs 并跑通 Resolve 脚本路径；如果只有 Mac App Store 版 Resolve、或者只想网页零配置出字，不建议把 Auto-Subs 当第一选择，先看剪映或 Resolve Studio 内建方案。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| DaVinci Resolve 免费版用户 | Studio 字幕功能需付费，Auto-Subs 补 AI 字幕 + 说话人分离 |
| Premiere / AE 用户 | CEP 扩展直接落 caption track / 文本图层 |
| 注重隐私、不想上传音视频到云端 | 完全本地运行，无 API Key、无账号 |
| 多语言字幕需求 | 100+ 语言识别 + 即时翻译 |
| 批量口播/访谈 UP 主 | 独立 App 批量转写 + Resolve 脚本精修 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| Mac App Store 版 Resolve 用户 | 脚本无法加载，换版本成本高 |
| 只想网页一键出字幕 | 安装模型、配 Resolve 门槛偏高 |
| 磁盘/内存紧张的老机器 | large 模型体积和 RAM 需求高 |
| 需要 FCP 原生集成 | 只能 SRT 导入，无直接桥接 |
| 期望零人工复核的终稿 | ASR 错字和时间码偏移仍需人工改 |

> 📷 **配图待补**：Resolve 工作流 vs 独立 App 工作流 场景示意（落盘名：Auto-Subs-who-workflow.png）

---

## 📊 总结评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | Resolve 版本限制是真实门槛；Homebrew 一行命令装 App |
| 核心能力 | ⭐⭐⭐⭐ | Resolve/Adobe 集成 + 说话人分离 + 多模型 |
| 速度/批量 | ⭐⭐⭐ | 取决于模型大小与硬件；本稿不编造测速 |
| 文档/社区 | ⭐⭐⭐⭐ | README 完整，GitHub Issues 活跃 |
| 成本 | ⭐⭐⭐⭐⭐ | 免费开源，无订阅 |

**综合评分：4.0 / 5.0**（工作流匹配分，非实验室榜）

> **一句话总结**：Auto-Subs 适合已经在 Resolve/Adobe 里干活、想把字幕工序收进时间线的人——它管本地转写和轨道对接；字幕终稿质量，仍取决于模型选择、素材音质和你肯不肯逐句改。

---

## 🔗 Auto-Subs 官网与项目地址

- **GitHub 仓库**：https://github.com/tmoroney/auto-subs
- **Homebrew 安装**：`brew install --cask auto-subs`
- **参考文章**：https://www.ahhhhfs.com/79267

**标签**：#AI工具 #Auto-Subs #达芬奇字幕 #本地Whisper #开源
