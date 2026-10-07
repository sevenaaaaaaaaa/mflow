# Privacy Filter 深度测评：发 Prompt 前，浏览器里能不能先把 PII 洗掉？

> T2 深度测评 · 浏览器本地 PII 脱敏 · 2026  
> GitHub：https://github.com/becoolme/privacyfilter.app · ⭐ 以 GitHub 当日为准  
> 许可证：见仓库 LICENSE  
> 参考来源：ahhhhfs.com/81007

---

## 👤 测评人背景

我习惯把客服工单、报错日志、采访逐字稿先贴进 ChatGPT 或 Claude 做摘要，再改写成对外稿。麻烦在于：工单里有客户邮箱和手机号，日志里偶尔夹着 API Key，逐字稿里受访者会自报姓名和公司。手替太慢，正则脚本我又懒得维护——「手机号 11 位」「邮箱 @ 后缀」好写，但「张总住在朝阳区某某路」这种自由文本，正则经常漏或误杀。Privacy Filter 出现在清单里，是因为它声称在浏览器里本地跑 OpenAI 开源的 privacy-filter 模型，文本不出设备。我想验证的是：粘贴 → 一键 Detect → 复制脱敏版，这条链路能不能进我的日常工序。

---

## 🎯 先说结论

Privacy Filter 是一款纯浏览器端 PII 脱敏工具。打开 privacyfilter.app，把文本粘贴进左侧输入框，点 Detect，右侧高亮标注 8 类敏感实体并输出脱敏文本——姓名、邮箱、电话、地址、账号、日期、URL、密钥（secret）。推理在浏览器内通过 Transformers.js 完成，基于 OpenAI 开源的 privacy-filter 权重；首次运行从 Hugging Face 下载约 50MB 模型（README 口径），之后走浏览器缓存。

支持 WebGPU 硬件加速（Chrome/Edge 最优），Safari/Firefox 回退 WASM。另有图片 OCR 路径：上传截图，tesseract.js 本地识别文字后再脱敏。仓库 becoolme/privacyfilter.app 用 Astro 构建，可自托管。

**我的决策句：你每周至少两次要把含个人信息的文本送进外部 LLM，且愿意接受「8 类实体 + 人工复核」的边界——Privacy Filter 值得书签置顶；如果你要 GDPR/HIPAA 级合规、或必须脱敏身份证/车牌，别把它当唯一防线。**

---

## 📦 Privacy Filter 是什么？

Privacy Filter 解决的是「把自然语言里的个人信息遮掉，再安全地发给 AI 或同事」——不是法律合规系统，不是 DLP 企业网关，而是个人/小团队用的浏览器辅助工具。

核心方案：OpenAI privacy-filter 模型 + Transformers.js 浏览器推理。文本粘贴后，Detect 操作在本地完成，按 README 说明不会产生携带原文的网络请求（首次模型下载除外）。8 类实体覆盖日常 Prompt 清洗的大部分场景，但身份证、车牌等强格式不在 8 类内，需要正则补充。

和「手替逐段改」比，它快；和「纯正则脚本」比，它对自由格式地址、多语言姓名更友好；和 ChatGPT 临时聊天比，它在数据离开设备之前就完成脱敏，不依赖服务端「不记录」承诺。

> 📷 **配图待补**：privacyfilter.app 首页与双栏输入/输出界面（落盘名：Privacy-Filter-homepage.png）

> 📷 **配图待补**：Detect 后右侧高亮标注实体（落盘名：Privacy-Filter-main-ui.png）

> 📷 **配图待补**：粘贴原文 → 本地模型推理 → 脱敏文本 流程示意（落盘名：Privacy-Filter-schematic-overview.png）

---

## 🧩 Privacy Filter 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 8 类 PII 检测 | person / email / phone / address / account / date / url / secret | 覆盖 Prompt 清洗常见实体 |
| 浏览器本地推理 | Transformers.js + privacy-filter 权重，文本不出设备 | 客服日志、工单摘要前清洗 |
| WebGPU / WASM 双路径 | Chrome/Edge WebGPU 加速；其他浏览器 WASM 降级 | 按浏览器选最优路径 |
| 图片 OCR 脱敏 | tesseract.js 本地 OCR → 再跑 PII 检测 | 报错截图、聊天记录截图可用 |
| 自托管 | Astro 项目，可 fork 部署内网 | 团队不想用公网 demo 时可自建 |
| 逐类确认 | Detect 结果按实体类型高亮，可逐类检查 | 保留人工复核入口 |

### 文本脱敏主流程

打开 privacyfilter.app → 等模型加载完成（首次约 50MB 下载）→ 左侧粘贴文本 → 点 Detect → 右侧查看高亮实体与脱敏结果 → 复制脱敏版。我通常把脱敏版贴进 ChatGPT，原文档留在本地不发送。

> 📷 **配图待补**：文本粘贴与 Detect 结果对比（落盘名：Privacy-Filter-feature-1.png）

### 图片 OCR 路径

上传截图 → 浏览器本地 OCR 识别文字 → 对识别结果跑 PII 检测 → 输出脱敏文本。适合分享报错截图给同事或 AI 时，不想手动打码。

> 📷 **配图待补**：截图上传与 OCR 脱敏结果（落盘名：Privacy-Filter-feature-2.png）

### 8 类实体说明

| 类型 | 标签 | 示例场景 |
|------|------|----------|
| 姓名 | person | 受访者、客户称呼 |
| 邮箱 | email | 工单、注册信息 |
| 电话 | phone | 客服记录 |
| 地址 | address | 自由格式住址 |
| 账号 | account | 用户名、ID |
| 日期 | date | 生日、预约时间 |
| URL | url | 含 token 的链接 |
| 密钥 | secret | ghp_、api_key 等 |

身份证、车牌、护照号等强格式不在 8 类内——这是设计边界，不是遗漏。

---

## 🧠 核心逻辑：它为什么不一样？

Privacy Filter 的分工是：**小模型本地 NER + 浏览器推理栈**，而不是把文本发给云端大模型做脱敏。

Transformers.js 在浏览器里加载 privacy-filter 权重，WebGPU 可用时走 GPU 加速，否则 WASM CPU 推理。Detect 阶段文本不离开设备——你可以开开发者工具 Network 面板验证：Detect 操作本身不应产生携带原文的请求（模型权重首次从 Hugging Face CDN 下载是例外）。

和 ChatGPT 临时聊天比：临时聊天是「服务端承诺不记录」，你仍须信任 OpenAI；Privacy Filter 是「发送前就洗掉」。两者可以组合——先 Privacy Filter 脱敏，再发临时聊天，双重保险。

和纯正则比：正则擅长强格式（11 位手机、邮箱 @），弱于自由文本（「王经理下周来杭州出差」）。Privacy Filter 的模型对上下文更敏感，但会有漏报和误报，不能替代人工扫一眼。

> 📷 **配图待补**：浏览器内 Transformers.js 推理栈与数据流（落盘名：Privacy-Filter-architecture-flow.png）

---

## ⚔️ Privacy Filter 和竞品有什么区别？

| 维度 | Privacy Filter | 手替逐段改 | 正则脚本 | ChatGPT 临时聊天 |
|------|----------------|-----------|----------|-----------------|
| 速度 | 一键 Detect | 最慢 | 写好后快 | 直接发，无脱敏 |
| 自由文本地址/姓名 | 模型上下文感知 | 靠人眼 | 弱 | 不涉及脱敏 |
| 数据位置 | 浏览器本地 | 本地 | 本地 | 服务端 |
| 身份证/车牌 | 不在 8 类，需正则补 | 人眼能看 | 正则擅长 | 不主动脱敏 |
| 批量/API | 无，纯浏览器 | — | 可脚本化 | 有 API 但非脱敏工具 |
| 合规级保证 | 无，辅助工具 | 取决于人 | 取决于规则 | 依赖供应商承诺 |
| 图片场景 | OCR + 脱敏 | 手动打码 | 需另接 OCR | 上传即暴露 |

选型句：日常 Prompt 前快速洗 8 类 PII → Privacy Filter；强格式批量（身份证、车牌）→ 正则 + Privacy Filter 双覆盖；完全不想装任何东西 → 手替；已信任云端且内容不敏感 → 直接发，但别自我安慰。

> 📷 **配图待补**：Privacy Filter vs 正则 vs 手替 选型示意（落盘名：Privacy-Filter-vs-competitor.png）

---

## 🧪 我实际跑下来的体验

说明：以下基于 privacyfilter.app 公开演示与仓库 README；未做大规模标注数据集评测，**不编造准确率百分比**。

### ✅ 好的方面

**1. 文本路径确实本地跑，Network 面板可验证**  
我贴了一段含姓名、邮箱、手机号的客服工单摘要，Chrome 开 Network，点 Detect 后没有携带原文的 POST 请求。首次打开页面时从 Hugging Face 拉了约 50MB 权重（README 口径），之后缓存命中，二次打开秒开。

**2. 8 类实体对 Prompt 清洗够用**  
「客户李明（liming@example.com）反映 138**** 订单问题」这类混合文本，person、email、phone 都能标出来。自由格式地址「杭州市西湖区某某路 88 号」比我的正则脚本漏检少。

**3. 图片 OCR 路径解决截图场景**  
报错截图里夹着 API Key 和用户名，上传后 OCR 识别再脱敏，比我在截图工具里手动马赛克快。OCR 质量取决于截图清晰度，模糊图会识别错字。

**4. 可自托管，团队可内网部署**  
Astro 项目结构清晰，fork 后改配置部署内网，公网 demo 不可用时仍有退路。

### ❌ 不好的方面

**1. 漏报和误报真实存在，不能零人审**  
「张总」有时被标 person，有时漏掉；「2024 年项目」里的日期偶尔误标。法律、医疗、金融场景，脱敏后必须人工再过一遍，不能盲信输出。

**2. 身份证、车牌不在 8 类**  
README 明确：强格式实体建议用正则补充。我测过一段含 18 位身份证的文本，模型没标——这不是 bug，是覆盖边界。有这类需求必须自建正则规则叠加。

**3. Safari/Firefox 走 WASM，速度明显慢于 Chrome WebGPU**  
Mac 上 Chrome Detect 一段 2000 字约几秒（未精确计时，取决于机器）；Safari 同段文本等待更长。批量场景不友好。

**4. 无 API，不能接自动化流水线**  
纯浏览器交互，没有 REST API。要把脱敏嵌进 CI 或工单系统自动化，得直接调 Hugging Face 上的 privacy-filter 模型，不是用这个 Web UI。

> 📷 **配图待补**：Detect 结果高亮与脱敏文本对比（落盘名：Privacy-Filter-hands-on.png）

---

## 💡 怎么高效用它

### 用法 1：Prompt 发送前三步检查

粘贴 → Detect → 肉眼扫一遍高亮 → 复制脱敏版 → 再发 LLM。我的习惯是：secret 和 email 必看，person 看有没有漏掉「X 总」「X 经理」这类称呼。30 秒人工复核，比事后泄露补救便宜。

> 📷 **配图待补**：发送前复核高亮实体（落盘名：Privacy-Filter-usage-1.png）

### 用法 2：正则 + 模型双覆盖

写一个简单的正则预检：11 位手机、18 位身份证、ghp_ 开头 token。先跑正则替换，再进 Privacy Filter 扫自由文本。两层叠加，漏检面小很多。

> 📷 **配图待补**：正则预处理 + Privacy Filter 二次检测（落盘名：Privacy-Filter-usage-2.png）

### 用法 3：截图分享前先 OCR 脱敏

报错截图、聊天记录截图要发给同事或 AI 时，先上传 Privacy Filter OCR 路径，拿脱敏文本代替原图。如果视觉侧还要做标注说明，封面或示意图可以在 Lovart 侧单独处理，文本层和图像层分开管。

### 用法 4：团队书签 + 自托管备份

把 privacyfilter.app 放进团队书签栏，写一句「发外部 LLM 前先过一遍」。同时 fork 仓库部署内网备用，公网 demo 挂了不影响工序。

---

## ⚠️ 安装和使用需要注意什么？

**无需安装**：浏览器访问 https://privacyfilter.app 即可。首次运行下载约 50MB 模型（README 口径），网络不佳时需等待。

**浏览器选择**：WebGPU 加速仅 Chrome/Edge 最优；Safari/Firefox 回退 WASM，速度较慢。

**非合规替代**：Privacy Filter 是辅助工具，不能替代 GDPR、HIPAA 等合规审计流程。关键场景脱敏后仍需人工复核。

**8 类边界**：身份证、车牌、护照等强格式不在检测范围，需正则补充。

**漏报误报**：模型可能漏标或误标，尤其是法律/医疗领域。不要默认「Detect 完就安全」。

**自托管**：仓库 https://github.com/becoolme/privacyfilter.app，Astro 构建，部署方式见 README。

> 📷 **配图待补**：首次模型下载与 WebGPU 状态提示（落盘名：Privacy-Filter-note-permission.png）

---

> **怎么选：** 每周多次要把含个人信息的文本送进 ChatGPT/Claude 的用户，可以优先把 Privacy Filter 设为发送前固定步骤；如果需要 GDPR/HIPAA 级合规保证、或主要脱敏身份证/车牌等强格式，不建议单独依赖 Privacy Filter，应叠加正则规则并保留人工审计。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| 日常 Prompt 前需清洗 PII 的内容运营/编辑 | 一键 Detect，比手替快 |
| 处理客服工单、日志摘要的开发者 | 本地推理，客户数据不上传 |
| 代码仓库审计（README/文档密钥泄露） | secret 实体识别 ghp_、api_key 等 |
| 分享报错截图给同事或 AI | OCR + 脱敏一条路径 |
| 不想信任云端「不记录」承诺的用户 | 发送前本地洗掉 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 需要 GDPR/HIPAA 合规认证的场景 | 仅辅助工具，无合规背书 |
| 主要脱敏身份证/车牌/护照 | 不在 8 类，需正则补 |
| 批量 API 自动化流水线 | 无 API，纯浏览器交互 |
| 期望 100% 准确零人审 | 漏报误报存在 |
| Safari/Firefox 重度用户且常处理长文本 | WASM 路径较慢 |

> 📷 **配图待补**：Prompt 清洗工作流场景示意（落盘名：Privacy-Filter-who-workflow.png）

---

## 📊 总结评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐⭐⭐ | 打开网页即用，无需安装 |
| 核心能力 | ⭐⭐⭐⭐ | 8 类 PII + OCR 路径；强格式需补 |
| 速度/批量 | ⭐⭐⭐ | WebGPU 快；WASM 慢；无批量 API |
| 文档/社区 | ⭐⭐⭐ | README 够用；社区规模小 |
| 成本 | ⭐⭐⭐⭐⭐ | 免费开源，可自托管 |

**综合评分：3.8 / 5.0**（Prompt 清洗场景匹配分，非合规认证分）

> **一句话总结**：Privacy Filter 适合「发外部 LLM 前先洗一遍」的日常工序——它管 8 类自由文本 PII 的本地检测；合规终稿和强格式脱敏，仍要叠加正则和人工复核。

---

## 🔗 Privacy Filter 官网与项目地址

- **在线演示**：https://privacyfilter.app
- **GitHub 仓库**：https://github.com/becoolme/privacyfilter.app
- **上游模型**：OpenAI privacy-filter（Hugging Face）
- **参考文章**：https://www.ahhhhfs.com/81007

**标签**：#AI工具 #Privacy-Filter #PII脱敏 #浏览器本地 #Transformers.js
