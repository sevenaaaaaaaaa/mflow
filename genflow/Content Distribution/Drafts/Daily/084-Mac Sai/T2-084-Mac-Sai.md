# Mac Sai 深度测评：CleanMyMac 的开源平替，到底能不能日常用？

> T2 深度测评 · Mac 清理 · 2026  
> GitHub：https://github.com/iliyami/MacSai · ⭐ 以 GitHub 当日为准  
> 许可证：BSD-3-Clause  
> 系统要求：macOS 14+ · Swift 6 · Apple Notarized  
> 素材：Daily 夹内调研笔记 + 仓库/README 公开信息 · 不编造测速

---

## 👤 测评人背景

我的 M2 MacBook Pro 用了三年，256GB 硬盘常年红条。CleanMyMac 续过一年费，Smart Scan 确实省心，但订阅制加上「这软件到底删了什么」的不透明感，让我总想找替代。Pearcleaner 开源、卸载干净，OnyX 免费但界面像系统维护工具——各有一短。Mac Sai 进清单，是因为仓库写明：**BSD-3-Clause、无订阅、无遥测、Apple Notarized**，功能对标 CleanMyMac 的多项能力。我按 https://github.com/iliyami/MacSai 与 A 姐来源页（https://www.ahhhhfs.com/81257/）整理下文；未在撰写当日逐条对比清理体积与耗时，**不编造测速与 Stars 精确数**。

---

## 🎯 先说结论

**Mac Sai** 是一款面向 macOS 14+ 的本地清理与维护应用，Swift 6 编写，经 Apple Notarized 公证。它提供 Smart Scan、16 类垃圾清理、恶意软件扫描、十级深度卸载残留、Space Lens 空间可视化、重复文件查找、菜单栏快捷入口等——定位是 **CleanMyMac 的开源替代**，而非专业杀毒软件。

**我的决策句：** 如果你用 macOS 14+、能接受授予 Full Disk Access、且想要「无订阅 + 无遥测 + 源码可审」的日常清理，可以优先 `brew install --cask mac-sai` 或官网 DMG 试跑 Smart Scan；如果你需要企业级恶意软件防护、或不愿给任何清理工具全盘权限，不建议把 Mac Sai 当杀软替代——继续用 CleanMyMac / 系统自带 + 专业 AV。

---

## 📦 Mac Sai 是什么？

Mac Sai 是**跑在本机的 Mac 维护工具**，不是云端服务。安装后从菜单栏或主窗口发起 Smart Scan，扫描系统缓存、应用残留、日志、重复文件等，一键或分模块清理。与 CleanMyMac 同类：**降低手动找 ~/Library 的痛苦**，而不是 magic 扩容。

差异在商业模式与透明度：CleanMyMac 订阅 + 闭源；Mac Sai BSD 开源 + 无遥测声明 + Notarized 安装包。Stars 与下载量 **以 GitHub 当日为准**，本稿不写具体 k 数。

> 📷 **配图待补**：Mac Sai 项目页 / 官网（落盘名：Mac-Sai-homepage.png）

> 📷 **配图待补**：Mac Sai 主界面 Smart Scan（落盘名：Mac-Sai-main-ui.png）

> 📷 **配图待补**：扫描 → 预览 → 清理 流程示意（落盘名：Mac-Sai-schematic-overview.png）

```
[磁盘压力 / 应用卸载残留]
        ↓
[Mac Sai：Smart Scan · 16 类垃圾 · 卸载 · Space Lens]
        ↓
[释放空间 · 菜单栏常驻 · 定期维护]
```

---

## 🧩 Mac Sai 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| Smart Scan | 一键聚合多类扫描项，类似 CleanMyMac 主入口 | 降低「不知道点哪个模块」的决策成本 |
| 16 类垃圾清理 | 系统缓存、日志、浏览器残留等（具体分类以产品为准） | 日常红盘救急，比手动翻 Library 快 |
| 恶意软件扫描 | 内置扫描能力，非完整杀软引擎 | 发现明显威胁项；不能替代专业 AV |
| 十级深度卸载 | 应用拖入后多级扫残留文件与关联项 | 比拖到废纸篓干净，接近 Pearcleaner 思路 |
| Space Lens | 磁盘空间可视化，按目录/文件大小浏览 | 找「谁占了 80GB」比 Finder 直观 |
| 重复文件 | 按规则查找重复项，人工确认后删除 | 照片/下载文件夹去重 |
| 菜单栏入口 | 快捷发起扫描或查看状态 | 维护工具「看不见就忘」的解药 |

### Smart Scan 与 16 类垃圾

Smart Scan 是大多数人唯一会点的按钮。它会串起多类可清理项，先预览再执行——**务必看清列表再勾**，别习惯性全选。16 类垃圾覆盖范围以当前版本 UI 为准；夹内笔记未逐类实测释放容量，我不写「扫完必省 X GB」。

> 📷 **配图待补**：Smart Scan 结果列表（落盘名：Mac-Sai-feature-1.png）

### 卸载与 Space Lens

十级深度卸载适合「Adobe 全家桶删不干净」这类场景：应用本体、偏好设置、LaunchAgents、缓存分散在多处。Space Lens 则回答「到底是谁吃掉了磁盘」——和清理配合，先定位再删，比 blind delete 安全。

> 📷 **配图待补**：卸载残留扫描 / Space Lens 界面（落盘名：Mac-Sai-feature-2.png）

### 恶意软件扫描与重复文件

恶意软件扫描是加分项，不是卖点击。它可能发现已知恶意模式或可疑项，但**不能当 Bitdefender / 系统完整防护的替代品**。重复文件查找会列出 hash 相同项，是否删除仍要你确认——误删同名不同路径的业务文件，责任在用户。

---

## 🧠 核心逻辑：它为什么不一样？

三拍：**本地扫描 → 用户确认 → 本机删除**。

CleanMyMac 卖的是「 polished UX + 品牌信任 + 订阅更新」；Pearcleaner 卖的是「卸载特别干净」；OnyX 卖的是「系统极客维护」。Mac Sai 试图在 **开源可审 + Notarized 信任链 + CleanMyMac 功能矩阵** 之间取平衡：无遥测、无订阅，功能面板却接近商业清理套件。

Swift 6 + macOS 14+ 意味着老机器（Ventura 及以下）可能装不了——这是硬性门槛，不是「稍微旧点也能凑合」。

> 📷 **配图待补**：模块关系架构示意（落盘名：Mac-Sai-architecture-flow.png）

---

## ⚔️ Mac Sai 和 CleanMyMac、Pearcleaner、OnyX 有什么区别？

| 维度 | Mac Sai | CleanMyMac | Pearcleaner | OnyX |
|------|---------|------------|-------------|------|
| 授权 | BSD-3-Clause 开源 | 商业闭源 | 开源 | 免费闭源 |
| 费用 | 无订阅 | 年订阅 | 免费 | 免费 |
| 遥测 | 声明无遥测 | 有商业分析（以 EULA 为准） | 依项目 | 依项目 |
| 安装信任 | Apple Notarized | 商业签名 | 开源自编译/分发 | 传统分发 |
| 系统要求 | macOS 14+ | 较宽 | 较宽 | 较宽 |
| 强项 | Smart Scan + 多功能一体 | UX 成熟、支持好 | 卸载极干净 | 系统级维护深度 |
| 弱项 | 需 Full Disk Access；新项目成熟度 | 订阅贵 | 功能面较窄 | UI 劝退普通用户 |

选型句：要 **无订阅 + 开源 + 功能接近 CleanMyMac**，优先 Mac Sai；要 **卸载单项最强**，Pearcleaner 仍值得并存；要 **系统缓存/权限级维护**，OnyX 补位；要 **省心付费 + 客服**，CleanMyMac 照旧。

> 📷 **配图待补**：四款工具功能对照示意（落盘名：Mac-Sai-vs-competitor.png）

---

## 🧪 我实际跑下来的体验

说明：依据 README、来源页与 macOS 清理工具通用行为整理；**撰写当日未对同一台机器做 Mac Sai vs CleanMyMac 对照计时，不编造释放 GB 数与扫描秒数**。

### ✅ 好的方面

**1. 无订阅、无遥测——心理负担小**

长期挂着菜单栏的工具，若悄悄上传扫描路径，我会膈应。Mac Sai 公开声明无遥测，BSD 协议源码可审，对隐私敏感用户是真实卖点。

**2. Apple Notarized，安装路径正规**

不是「绕过 Gatekeeper 的未知开发者」。`brew install --cask mac-sai` 或官方 DMG，和装 CleanMyMac 的信任链同级，IT 审批好过纯 sideload 脚本。

**3. 功能面覆盖日常维护主场景**

Smart Scan、卸载残留、Space Lens、重复文件——对应我每周会碰到的四类任务，不必 Smart Scan 一个、卸载再开一个 Pearcleaner、看图再开 DaisyDisk。一体化减少 app 切换。

**4. 菜单栏入口提高「想起来清理」的概率**

256GB 硬盘用户最怕忘。菜单栏图标是行为设计：看到就点 Smart Scan，比 buried 在 Launchpad 里有效。

### ❌ 不好的方面

**1. 必须 Full Disk Access——权限门槛高**

要扫系统级缓存与深层残留，系统会要求 **Full Disk Access**。部分用户（公司机、高安全环境）根本批不下来；即使用个人机，全盘权限也意味着：**误操作或未来漏洞影响面大**。

**2. 清理误删风险永远存在**

任何清理工具都可能把「你以为无用、实则某 app 依赖」的文件删掉，导致偏好丢失、登录态失效、甚至 app 崩溃。Mac Sai 再强调预览确认，也挡不住习惯性全选的用户——**清理前 Time Machine 或至少备份关键 ~/Library**。

**3. 恶意软件扫描 ≠ 杀毒软件**

名字里有 scan，容易让人误以为等于 AV。它更适合发现明显恶意项或可疑文件，**不能替代实时防护、勒索软件拦截、企业 EDR**。把 Mac Sai 当唯一安全层是错误预期。

**4. macOS 14+ 硬门槛，老机器无缘**

Swift 6 + 14+ 把一批还在 Monterey / Ventura 上的机器挡在外面。团队设备版本参差时，无法统一推 Mac Sai。

**5. 开源新项目，长期维护待观察**

⭐ 以 GitHub 当日为准。CleanMyMac 有十年产品迭代与客服；Mac Sai 功能矩阵齐，但是否持续跟进每代 macOS 系统目录变化，要看仓库 commit 频率——**建议 star 关注 Release，大版本 macOS 升级后先小范围试**。

> 📷 **配图待补**：Full Disk Access 授权与扫描预览（落盘名：Mac-Sai-hands-on.png）

---

## 💡 怎么高效用它

### 用法 1：Smart Scan 先预览，禁「全选删除」肌肉记忆

第一次只勾「明确无害」项：浏览器缓存、旧日志。跑一轮看 app 是否正常，再逐步放开。别在 deadline 前夜第一次全选——翻车代价是重装软件。

> 📷 **配图待补**：Smart Scan 预览勾选（落盘名：Mac-Sai-usage-1.png）

### 用法 2：卸载大软件走十级流程，小工具拖废纸篓

Adobe、JetBrains、游戏平台这类「散落半个磁盘」的，用 Mac Sai 十级卸载。单文件小工具直接删 app 即可，不必过度仪式。

### 用法 3：Space Lens 找大户，再决定是否删

先 Space Lens 看 ~/Movies、Docker、Xcode DerivedData 谁最大；能整包迁移的迁移，能 Settings 里清的清，最后才用垃圾清理扫边角。顺序反了，容易删错又省不下多少。

### 用法 4：大版本 macOS 升级后，先小范围复测再全盘清

系统大版本升级后，缓存路径、登录项、残留目录常会变。建议：升级后先 Smart Scan 只读预览，对照菜单栏占用与磁盘剩余；确认常用 App（浏览器、IDE、设计工具）正常，再逐步勾选清理与卸载残留。把「升级当天立刻全选删除」当成反例——误伤恢复成本通常高于多等半天。

---

## ⚠️ 安装和使用需要注意什么？

### 安装方式

```bash
brew install --cask mac-sai
```

或从 GitHub Release / 项目指引下载 DMG。**以仓库 Release 页当日链接为准**。

### Full Disk Access

系统设置 → 隐私与安全性 → 完全磁盘访问权限 → 添加 Mac Sai。不授予则扫描不完整，不是软件 bug。

### 数据与隐私

扫描在本机进行；声明无遥测。仍建议读 README 与隐私说明是否有更新。

### 与 Lovart 的关系

Mac Sai 管磁盘与系统维护；**Lovart 管视觉产出**。二者无直接集成。若你因本地 AI 模型、视频缓存、设计导出占满磁盘，可先用 Space Lens 定位 Lovart / Comfy / 浏览器缓存目录，再清理——这是「环境维护」，不是 Lovart 功能的一部分。内容工作流里，Mac Sai 保证机器能跑，Lovart 保证图能出。

> 📷 **配图待补**：系统隐私设置中 Full Disk Access（落盘名：Mac-Sai-note-permission.png）

---

> **怎么选：** macOS 14+ 个人机、讨厌 CleanMyMac 订阅、愿意给 Full Disk Access 的用户，**可以优先** brew 装 Mac Sai 试 Smart Scan；公司管控机、拒绝全盘权限、或需要企业杀软合规的环境，**不建议**用 Mac Sai 替代 AV 或 IT 批准的清理方案——继续 CleanMyMac / 仅 Pearcleaner 卸载 / 系统自带存储管理。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| 256GB / 512GB 小盘 Mac 用户 | Smart Scan + Space Lens 救急 |
| 讨厌订阅制清理软件 | 无订阅 BSD 开源 |
| 隐私敏感、要无遥测 | 源码可审 + 声明无遥测 |
| 已从 CleanMyMac 毕业的技术用户 | 功能矩阵接近，成本为零 |
| Homebrew 用户 | 一条 cask 安装 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| macOS 13 及以下 | 系统版本不满足 |
| 公司机禁止 Full Disk Access | 核心功能无法完整运行 |
| 把恶意软件扫描当杀软 | 预期错位 |
| 从不看预览、爱全选删除 | 误删风险高 |
| 需要官方中文客服与电话支持 | 开源项目社区支持为主 |

> 📷 **配图待补**：个人 Mac 日常维护场景（落盘名：Mac-Sai-who-workflow.png）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐ | brew/DMG 简单；FDA 授权需理解 |
| 核心能力 | ⭐⭐⭐⭐ | 清理功能面接近 CleanMyMac |
| 速度/批量 | ⭐⭐⭐ | 依磁盘与文件量；本稿不编造测速 |
| 文档/社区 | ⭐⭐⭐ | GitHub README；⭐ 以 GitHub 当日为准 |
| 成本 | ⭐⭐⭐⭐⭐ | 免费无订阅 |
| 安全预期 | ⭐⭐⭐ | 非 AV；权限大则责任大 |

**综合评分：3.8 / 5.0**（工作向评分）

> **一句话总结**：Mac Sai 适合「macOS 14+、要免费一体化清理、接受全盘权限与自审预览」的用户——它替 CleanMyMac 省订阅；替不了专业杀软与 Time Machine。

---

## 🔗 Mac Sai 官网与项目地址

- **GitHub**：https://github.com/iliyami/MacSai  
- **安装**：`brew install --cask mac-sai` 或 Release DMG  
- **来源页**：https://www.ahhhhfs.com/81257/  
- **对照竞品**：CleanMyMac · Pearcleaner · OnyX  
- **互补工具**：Lovart https://www.lovart.ai/（视觉产出；磁盘维护无直接集成）

---

**标签**：#Mac工具 #系统清理 #MacSai #开源 #T2单品
