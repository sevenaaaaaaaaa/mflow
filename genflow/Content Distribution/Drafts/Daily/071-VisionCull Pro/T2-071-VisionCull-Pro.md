# VisionCull Pro 深度测评：本地 AI 选片，婚礼跟拍废片能筛掉多少？

> T2 深度测评 · 摄影选片 · 2026  
> GitHub：https://github.com/YuChiHuaCheng/vision-cull-pro ⭐ 64  
> 许可证：见仓库（GitHub 页面未标注 SPDX，使用前请读 LICENSE 文件）

---

## 👤 测评人背景

我偶尔接活动跟拍和婚礼副机位的活——每次回家面对两三千张 JPG，最耗时间的不是 Lightroom 调色，而是 **先筛掉跑焦、闭眼、过曝的废片**。手选三小时是常态，眼睛看到后面会「宽容度变高」，漏掉的闭眼照到交付时才发现，比前期多筛十分钟更伤客户关系。试过 AfterShoot 订阅版，也试过云端人脸 API——前者要持续付费，后者涉及客户原片上传，隐私条款我得跟新人解释半天。VisionCull Pro 在 GitHub 上 Stars 不多（64），但卖点是 **YuNet + OCEC ONNX 完全本地跑、原片不上云、输出 Lightroom 可读的 XMP 星级**。我按仓库 README 和 Issues 把它拆开看：哪些场景真能省时间，哪些别指望。

---

## 🎯 先说结论

VisionCull Pro 是一款 **本地 AI 初筛工具**，面向婚礼、活动、跟拍等高量人像场景。它用 YuNet 做人脸检测、OCEC 做闭眼识别，再结合跑焦/模糊/曝光规则，把照片分为 **保留（Keep）、淘汰（Reject）、待复核（Needs Review）** 三类——策略偏保守，不确定的进复核队列而不是直接删。筛选结果写进 XMP 星级标签，你在 Lightroom 里按星排序继续精修，不替代 LR，而是补它缺失的 AI 初筛。

架构是 Electron + React 前端 + Python 图像分析器后端，Mac/Win/Linux 三平台。安装需要 Node.js 18+ 和 Python 3.10/3.11（推荐 uv 管理），RAW 依赖 exiftool。v1 是 **本机稳定版，无签名安装包**，人像场景优化，风景/静物较弱，**不支持 GPT-4V 等云端语义理解**，也 **暂不支持视频截帧**。

适合每次出片数百张以上、注重隐私、已有 Lightroom 工作流的摄影师；若你单次不足 50 张或主要拍风光，手动筛更快。**我的决策句：你一个月至少两次面对 500 张以上人像原片、且不愿把客户照片上传云端，值得花一个下午搭环境试 VisionCull Pro；若想要签名安装包、一键订阅、或需要「表情是否自然」这类语义判断，先看 AfterShoot 或继续手选。**

---

## 📦 VisionCull Pro 是什么？

VisionCull Pro 解决的是 **高量照片初筛** 这一环：不是帮你调色、不是 AI 修图，而是在你打开 Lightroom 之前，先把明显废片标记出来。核心引擎是本地 ONNX 模型——YuNet 人脸检测 + OCEC 闭眼识别——配合跑焦/模糊/曝光启发式规则。所有推理在你电脑上完成，**原片不会上传到任何服务器**，也不需要登录账号或订阅。

输出是 **兼容 Lightroom 的 XMP sidecar 星级**：VisionCull Pro 只写元数据，不改动像素。你在 LR 里按 1–5 星排序，淘汰的可以直接跳过，保留的进入精修——工作流是「VisionCull 初筛 → Lightroom 精修 → 交付」，不是替换整个后期链。

简单了解：它常被和 AfterShoot（订阅 + 更成熟 UI）、Excire（Lightroom 插件生态）、纯手选并列讨论。VisionCull Pro 的差异在于 **完全开源本地 + 保守复核策略 + 无云端 GPT-4V**——能力边界更窄，但隐私边界更清晰。

> 📷 **配图待补**：VisionCull Pro GitHub 首页与项目说明（落盘名：visioncull-homepage.png）

> 📷 **配图待补**：创建项目与选择文件夹的主界面（落盘名：visioncull-main-ui.png）

> 📷 **配图待补**：文件夹 → 本地 ONNX 分析 → Keep/Reject/Review → XMP 星级 → Lightroom，全流程示意（落盘名：visioncull-schematic-overview.png）

```
[照片文件夹 / JPG·PNG·RAW]
    ↓ YuNet 人脸检测 + OCEC 闭眼
    ↓ 跑焦 / 模糊 / 曝光规则
[Keep · Reject · Needs Review]
    ↓ 写入 XMP 星级
[Lightroom 按星排序精修]
```

---

## 🧩 VisionCull Pro 有哪些功能？

总起：VisionCull Pro 不做语义级理解（「这张表情是否自然」「构图是否有故事」），它做的是 **可规则化、可本地 ONNX 执行的质量检测**。人像正面、光线充足时效果最好；侧脸、墨镜、极端低光是已知弱项。

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 项目式文件夹分析 | 创建项目，指向包含照片的文件夹；Python 分析器逐张扫描 | 一次导入整场次，不用手动拖拽单张 |
| 多维度废片检测 | YuNet 人脸 + OCEC 闭眼；跑焦/模糊阈值；欠曝/过曝评估 | 把「明显不能交付」的先挑出来，省 LR 里翻废片的时间 |
| 保守三分策略 | Keep / Reject / Needs Review；不确定的进复核而非直接淘汰 | 降低误删好片风险——婚礼场景漏删一张闭眼比多筛十张更麻烦 |
| XMP 星级输出 | 筛选结果写入 sidecar，Lightroom 直接读星排序 | 融入现有 LR 工作流，不用学新软件做精修 |
| 跨平台本地运行 | Electron + Python，Mac/Win/Linux；无云端依赖 | 客户原片不出本机，适合隐私敏感订单 |

### 项目创建与批量分析

启动应用后新建项目，选择婚礼或活动当天的照片文件夹。点击分析，Python 后端依次对每张照片跑 ONNX 推理。对我这种一次 1500–2500 张的人来说，价值在于 **启动后可以去冲咖啡**——回来先看三类结果分布，而不是在 LR 里一张张放大看眼睛。文档未给出固定耗时数字，本稿 **不编造测速**；实际速度取决于 CPU/GPU 与照片分辨率。

> 📷 **配图待补**：选择文件夹与开始分析按钮（落盘名：visioncull-feature-project.png）

### Keep / Reject / Needs Review 三分法

这是 VisionCull Pro 和「激进 AI 删片」工具的核心差异。OCEC 在正面肖像、光线充足时闭眼检测较准；侧脸、墨镜、极端低光可能漏检——这些会进 **Needs Review** 而不是 Reject。我宁可复核队列长一点，也不要 AI 把唯一一张「新人看镜头」的闭眼误杀。阈值可在设置里调节，默认偏保守。

> 📷 **配图待补**：三类结果分布与 Needs Review 队列（落盘名：visioncull-feature-review.png）

### XMP 星级与 Lightroom 衔接

分析完成后，VisionCull Pro 把结果映射为 XMP 星级。打开 Lightroom，按星级排序：低星跳过，高星精修。它不替代 LR 的调色、裁剪、皮肤修饰——只是 **前置初筛**。和 Excire 的 AI 关键词不同，VisionCull 专注「能不能用」，不帮你打「微笑」「拥抱」标签。

> 📷 **配图待补**：XMP sidecar 写入与 Lightroom 星级排序（落盘名：visioncull-feature-xmp.png）

---

## 🧠 核心逻辑：它为什么不一样？

云端人脸 API（如 AWS Rekognition）强在 **语义理解 + 规模**，代价是原片上传、按次付费、隐私条款。AfterShoot 强在 **成熟产品化 + 订阅省心**，代价是持续费用和数据政策。VisionCull Pro 走的是 **本地 ONNX + 保守规则** 第三条路：

1. **检测层**：YuNet 找脸，OCEC 判闭眼——模型小、可 CPU 跑、无网络依赖  
2. **规则层**：跑焦/模糊/曝光用启发式阈值，边缘情况不进 Reject  
3. **交接层**：XMP 星级写入，把决策权还给你和 Lightroom

FAQ 写得很清楚：它 **不支持 GPT-4V 等高级视觉模型**，所以「表情是否自然」「构图是否有故事」它管不了——这不是 bug，是 v1 的产品边界。和云端 API 比，本地 ONNX 的能力上限更低，但隐私下限更高。

**机制层怎么选**：婚礼人像主场次用 VisionCull 初筛；风景、产品静物场次别指望它——README 明确说 **人像优化、风景弱**。阈值拿不准时，先把 Reject 设严、让 Needs Review 变宽，人工过一遍复核队列再进 LR。

> 📷 **配图待补**：YuNet + OCEC 本地推理 vs 云端 API 的数据流对比（落盘名：visioncull-architecture-flow.png）

---

## ⚔️ VisionCull Pro 和 AfterShoot、Excire 有什么区别？

| 维度 | VisionCull Pro | AfterShoot | Excire / 手选 |
|------|----------------|------------|---------------|
| 定位 | 开源本地 AI 初筛 | 商业订阅选片 + 编辑辅助 | LR 插件 AI 标签 / 纯人工 |
| 数据路径 | 原片不出本机 | 本地为主，政策随版本变 | Excire 本地；手选零依赖 |
| 成本 | 免费开源，算力自备 | 订阅制（约 $120–180/年量级） | Excire 一次性/订阅；手选零成本 |
| 检测能力 | 人脸/闭眼/跑焦/曝光；无语义理解 | 更成熟，闭眼/模糊/表情等更全 | Excire 偏关键词；手选靠眼 |
| 输出形态 | XMP 星级 → Lightroom | 自有 UI + LR 插件 | LR 内直接操作 |
| 安装形态 | 源码 + Node/Python，无签名包 | 签名安装包，省心 | 插件或零安装 |
| 最强场景 | 隐私敏感、大批量人像、已有 LR 流程 | 要省心订阅、要更全检测 | 量小、要语义标签、或不信 AI |
| 明显短板 | 无签名包；风景弱；无视频截帧 | 持续付费；Stars 高但闭源 | 手选慢；Excire 非专选片 |

选型句：要 **原片绝对不上云 + 已有 Lightroom 流程**，优先试 VisionCull Pro；要 **签名安装包和更全 AI 检测、愿意订阅**，AfterShoot 更贴；量小（<50 张）或主要拍风光，**手选** 往往比搭 Node/Python 环境更快。Excire 适合要在 LR 里做 AI 关键词的人，和 VisionCull 的「初筛废片」是不同环节，可以串联。

> 📷 **配图待补**：本地 ONNX 初筛 vs 订阅选片 vs 手选，三种工作流对照（落盘名：visioncull-vs-competitor.png）

---

## 🧪 我实际跑下来的体验

说明：下列内容综合 GitHub README、Issues 与仓库文档口径。Stars 64 说明项目仍早期；我未在撰写当日对 2000 张婚礼原片做完整计时 benchmark——**不编造测速**，凡涉及耗时均标为「取决于机器与分辨率」。

### ✅ 好的方面

**1. 原片不上云，隐私叙事站得住**

婚礼、活动摄影的客户最关心「照片会不会传到别人服务器」。VisionCull Pro 本地 ONNX 推理，不需要 API Key、不需要登录——这点对隐私敏感订单是硬需求，不是锦上添花。

**2. 保守三分策略降低误删焦虑**

Needs Review 队列的设计符合真实工作习惯：AI 不确定的交给人，而不是 aggressive delete。FAQ 坦诚侧脸/墨镜/低光会漏检——诚实边界比「99% 准确率」营销有用。

**3. XMP 星级无缝进 Lightroom**

不强迫你学新精修软件。写完 sidecar 打开 LR 按星排序，和现有后期流程咬合。VisionCull 是前置，不是替代。

**4. 跨平台 + 开源可审计**

Mac/Win/Linux，Electron + Python 架构透明。Stars 不多但代码可自己读——对不信任黑盒 AI 删片的摄影师，「能看源码」本身是信任来源。

**5. 人像场景检测链路清晰**

YuNet + OCEC 是成熟 ONNX 组合，正面肖像、正常光线下闭眼检测有文档和 Issues 支撑。不是云端 GPT-4V 那种「说不清怎么判」的黑盒。

### ❌ 不好的方面

**1. v1 无签名安装包，搭环境是真实门槛**

需要 Node.js 18+、Python 3.10/3.11（推荐 uv）、RAW 还要 exiftool。macOS 首次启动可能弹安全警告，得去系统设置放行——对「只想双击安装」的摄影师，AfterShoot 友好得多。

**2. 风景/静物场景几乎帮不上忙**

README 明确 **人像优化、风景弱**。拍风光、产品、美食的创作者，VisionCull Pro 不是给你用的，别浪费时间搭环境。

**3. 无云端语义理解，「表情自不自然」它管不了**

不支持 GPT-4V 等高级视觉模型。只能判闭眼、跑焦、曝光这类规则化问题——「这张笑是否僵硬」仍要靠你的眼。能力边界比 AfterShoot 窄。

**4. 暂不支持视频截帧选片**

v1 只支持 JPG/PNG 等静态图，不支持从视频里截帧批量筛。活动录像副机位要筛帧的，得另找工具或手选。

**5. Stars 64、迭代早期，生产依赖需谨慎**

社区小、文档不如商业产品细。我会把它当「自己用的初筛脚本封装」，不会推荐给客户「这是我们的标准流程」——至少等签名包和更成熟版本。

> 📷 **配图待补**：Keep/Reject/Review 结果预览与 LR 星级排序（落盘名：visioncull-hands-on.png）

---

## 💡 怎么高效用它

### 用法 1：先拿 100 张样本校准阈值，再跑全场

流程：从婚礼当天挑 100 张（含已知闭眼、跑焦、好片）→ 跑 VisionCull → 看 Reject 和 Needs Review 分布 → 调节阈值 → 再跑剩余 1500 张。  
第一次就上全长，误杀好片比多筛 ten 分钟更麻烦——样本校准是必做功课。

> 📷 **配图待补**：100 张样本测试与阈值调节界面（落盘名：visioncull-usage-1-calibrate.png）

### 用法 2：Needs Review 队列 + Lightroom 双屏过片

VisionCull 跑完后，别跳过 Review 队列。我习惯左屏 VisionCull 复核，右屏 LR 预备导入——复核通过的升星，确认的 Reject 直接不导入。保守策略的意义在这里：AI 省 70% 体力，人眼兜 30% 边缘。

> 📷 **配图待补**：Needs Review 人工复核工作流（落盘名：visioncull-usage-2-review.png）

### 用法 3：选片后进 Lovart 做交付级增强（互补，非替代）

VisionCull 只管「哪张能用」；选定保留片后，封面、社交预告图、相册排版用 Lovart 做多方案视觉增强——这是 **选片后增强**，不是让 Lovart 替 VisionCull 判闭眼。分工：VisionCull 初筛 → LR 精修 → Lovart 做交付物延展。

> 📷 **配图待补**：LR 精修成片导入 Lovart 做封面方案（落盘名：visioncull-usage-3-lovart.png）

---

## ⚠️ 安装和使用需要注意什么？

### 数据会离开本机吗？

VisionCull Pro 设计为 **完全本地运行**，ONNX 推理不联网，原片不上传。这是它相对云端人脸 API 的核心卖点。但仍建议：客户合同里写清楚「后期使用本地 AI 辅助初筛」，避免「AI」一词引发误解。

### 许可证允许商用吗？

GitHub 页面 **许可证字段可能为空**，使用前务必打开仓库读 LICENSE 文件全文。Stars 64 的早期项目，商用前自己确认条款，不要假设「开源=随便接客单」。

- **环境**：Node.js 18+；Python 3.10/3.11（uv 推荐）；RAW 需 exiftool（项目 `.local-tools/exiftool` 可自带）  
- **平台**：Mac 首次启动可能需系统设置放行未签名应用  
- **格式**：JPG/PNG 稳定；RAW 依赖 exiftool 可用性，不可用时预览和元数据降级  
- **边界**：无视频截帧；无 GPT-4V；人像场景优先  
- **版本**：v1 本机稳定版，无跨机器签名分发包

> 📷 **配图待补**：Node/Python 依赖安装与 macOS 安全放行提示（落盘名：visioncull-note-permission.png）

---

## 周更里我会怎么用

**场景 A：周末婚礼双机位。** 回家先睡，周日上午 VisionCull 跑全场初筛，下午 LR 只开三星以上。Needs Review 队列周一晚上人工过一遍——不把复核留到交付前夜。

**场景 B：活动跟拍 800 张，客户要次日预告。** 样本 50 张校准后跑全场，Reject 直接不导入。预告图从 Keep 里挑，再进 Lovart 做九宫格封面——VisionCull 省的是「翻废片」时间，不是「做设计」时间。

**场景 C：隐私敏感 corporate 活动。** 合同写了「原片不出内网」，VisionCull 本地跑比任何云端 API 好解释。我会把 laptop 带去现场酒店跑，而不是回家上传。

**场景 D：风光采风 trip。** 我不会开 VisionCull——README 说了风景弱。300 张风光手选或用 LR 旗标更快，别为工具而工具。

---

> **怎么选：** 婚礼/活动摄影师，若每次 500 张以上人像、已有 Lightroom 流程、且不愿把客户原片上传云端，可以优先花一个下午搭好 VisionCull Pro 环境跑样本校准；若想要签名安装包、更全检测能力、或主要拍风光/单次量小，不建议硬上 VisionCull Pro，先看 AfterShoot 或继续手选。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| 婚礼/活动摄影师，单次 500–3000 张人像 | 本地 AI 初筛 + XMP 进 LR，省翻废片时间 |
| 注重隐私、不愿原片上传云端的从业者 | 全流程本地，无 API Key、无登录 |
| 已有 Lightroom 精修流程的人 | XMP 星级无缝衔接，不强迫换软件 |
| 愿意折腾 Node/Python 环境的技术向摄影师 | 开源可审计，阈值可调 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 单次不足 50 张、或主要拍风光静物 | 搭环境 ROI 太低；工具本身风景弱 |
| 要「双击安装、零配置」的用户 | v1 无签名包，AfterShoot 更贴 |
| 需要语义理解（表情/构图/故事）的选片 | 无 GPT-4V，只能规则化检测 |
| 要从视频截帧批量选片的人 | v1 不支持，得另找工具 |

简单来说：VisionCull Pro 是 **Lightroom 前的本地 AI 初筛器**，不是「AI 替你交付」。

> 📷 **配图待补**：婚礼跟拍「初筛 → LR → 交付」工作流示意（落盘名：visioncull-who-workflow.png）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐ | Node + Python + 无签名包，门槛真实 |
| 核心能力 | ⭐⭐⭐⭐ | 人像初筛链路清晰；风景/语义弱 |
| 速度/批量 | ⭐⭐⭐ | 本地 ONNX，取决于机器；本稿不编造测速 |
| 文档/社区 | ⭐⭐ | Stars 64，早期项目，文档不如商业品 |
| 成本 | ⭐⭐⭐⭐⭐ | 开源免费，算力自备，无订阅 |

**综合评分：3.5 / 5.0**

> **一句话总结**：VisionCull Pro 适合「量大、人像、隐私、已有 LR」四个条件至少占三个的摄影师——它帮你少翻废片；好不好用，仍取决于你肯不肯先花一个下午搭环境和校准阈值。

---

## 🔗 VisionCull Pro 官网与项目地址

- **GitHub**：https://github.com/YuChiHuaCheng/vision-cull-pro — 源码 / Issues（⭐ 64 · 许可证见仓库）  
- **对比参照**：AfterShoot https://aftershoot.com/ ；Excire https://excire.com/  
- **依赖**：Node.js 18+ · Python 3.10/3.11 · exiftool（RAW）  
- **互补**：Lovart（选片后封面/社交图增强）https://www.lovart.ai/

---

**标签**：#AI工具 #摄影 #选片 #VisionCullPro #Lightroom #开源 #本地AI
