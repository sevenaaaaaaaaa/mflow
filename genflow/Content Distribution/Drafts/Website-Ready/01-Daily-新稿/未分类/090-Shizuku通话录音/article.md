# ShizuCallRecorder 深度测评：免 Root 的 Android 通话录音，Shizuku 路线靠谱吗？

> T2 深度测评 · Android 通话录音 · 2026  
> GitHub：https://github.com/kitsumed/ShizuCallRecorder ⭐ 1139 · GPL-3.0（含额外商标条款）  
> 安装包：GitHub Releases · F-Droid · IzzyOnDroid  
> 前置：Android 12+ 推荐 · Shizuku（README 推荐 thedjchi fork）

---

## 👤 测评人背景

做内容分发时，我偶尔需要把电话采访落成文字稿——这和 Lovart 视觉流程几乎不相交，本稿按 Daily 单品清单写 ShizuCallRecorder（中文常叫 Shizuku 通话录音）。夹内调研笔记同样是空壳，下文 **事实以 GitHub README、SUPPORT.md 口径为准**；未在撰写日于本人设备完整跑通 SUPPORT 全流程的，不写「某机型必定成功」，也不编造录音比特率测速。

Android 11 起很多机型 **系统自带录音被阉割或仅录单声道**，Root 录通话我又不想为了几通电话动 bootloader。ShizuCallRecorder 的宣传点是：**首个面向 Android 11+ 的非 Root FOSS 通话录音**，通过 Shizuku 拿到 shell 级权限，底层可视为 **设备上的 scrcpy-server 包装**——专盯 **运营商电话**，不是微信语音全套解决方案。

---

## 🎯 先说结论

ShizuCallRecorder 是一个 **极简通话录音 App**：来电/去电时通过 Shizuku 启录音链路，支持 **双向录音**（README 称蓝牙耳机/Remote 耳机场景也应可用）；可设 **自动录音** 与排除规则（匿名、指定联系人、全部联系人）；编码 **Opus 或 AAC**；**无常驻后台进程**——只在电话状态变化时运行。

门槛真实：**Android 12+ 为 README 主推**；Android 11 **有限支持**，屏幕未解锁时可能 **直接 crash**（与 scrcpy 音频捕获限制同源）；**必须按 SUPPORT.md 做初始配置**，不是装完就录。Hidden API + OEM 魔改 → **行为非确定性**，README 用 CAUTION 块写得很重。

**我的决策句：你已会用 Shizuku、主要录运营商电话、接受 GPL 与法律自检，优先试 ShizuCallRecorder；要零配置、要录微信/Zoom、或不愿碰 Shizuku/USB 调试，不建议把它当唯一方案——先看系统录音或商业 App。**

---

## 📦 ShizuCallRecorder 是什么？

一句话：**借 Shizuku 给 shell 权限的非 Root 开源通话录音器**，聚焦 **phone carrier 通话**，不主打第三方 IM 通话（README NOTE：不 100% 反对未来支持，但 **不是主焦点**，Issue #1 仍在讨论）。

和 **系统自带录音** 的差异：许多 OEM 在 Android 11+ 去掉或弱化双向录音；本 App 走 **shell 权限 + 内部 API**，不 Root。和 **商业通话录音 App** 的差异：ShizuCallRecorder **FOSS、无广告叙事、功能极简**；商业 App 常包云备份、转写、CRM，但闭源且订阅。和 **Root + 录音模块** 的差异：不用改系统分区，但要 **常驻 Shizuku 授权** 与初始配置。

分发：GitHub Releases、F-Droid（`com.kitsumed.shizucallrecorder`）、IzzyOnDroid。许可证 **GPL-3.0**，文件末尾 **Section 7 额外条款**：不授予 Contributor 商标权；`ShizuCallRecorder` 名称与包名属版权持有人 kitsumed。

> 📷 **配图待补**：GitHub 仓库首页与 Releases（落盘名：shizucallrecorder-homepage.png）

> 📷 **配图待补**：App 主界面与录音设置（落盘名：shizucallrecorder-main-ui.png）

> 📷 **配图待补**：Shizuku 授权 → Shell 权限 → 录音链路示意（落盘名：shizucallrecorder-schematic-overview.png）

```
[运营商来电/去电事件]
    ↓
[ShizuCallRecorder + Shizuku shell 权限]
    ↓
[scrcpy-server 类 on-device 音频捕获]
    ↓
[Opus/AAC 文件 · 无常驻后台]
```

---

## 🧩 ShizuCallRecorder 有哪些功能？

### 功能特色一览

| 功能模块 | 具体表现 | 实用价值 |
|----------|----------|----------|
| 双向录音 | 来电/去电录双方；README 称蓝牙/Remote 耳机场景应可用 | 采访、客服回访留档，不只有本机麦克风 |
| 自动录音与排除 | 可全自动；可忽略匿名、指定联系人或全部联系人 | 减少误录熟人私聊，但仍需你懂当地法 |
| Shizuku 安全开关 | 可管理 Shizuku 开/关，降低攻击面；缓解「检测到 USB 调试/Shizuku」的 App 抱怨 | 不用录音时可关 Shizuku，减少暴露 |
| 编码与生命周期 | Opus 或 AAC；仅在电话事件时运行，无持久后台通知 | 省电、少一条「常驻录音」系统提示 |
| 分发与协议 | F-Droid/Izzy/Release；GPL-3.0 保 FOSS 衍生 | 可审计；商标条款限制品牌滥用 |

### 双向录音与耳机场景

README 核心卖点：**Records both sides of phone calls**。对我这种「 walking 接记者电话、用蓝牙耳机」的用法，理论上应录到对方声音——但 **OEM 与 Android 版本差异大**，README 的 *Android Tested Versions* 表写明作者 **无法穷举测试**，问题要靠社区反馈。本文 **不编造「某耳机 100% 成功」**。

> 📷 **配图待补**：通话中录音指示或完成后的文件列表（落盘名：shizucallrecorder-feature-recording.png）

### 自动录音与排除规则

可开 **Automatic call recording**，并按规则跳过：匿名号码、特定联系人、或全部联系人。实用价值是 **少手动点录**；风险是 **过滤逻辑有局限**——见下文 CAUTION：实时号码访问受隐私限制，可能 **过晚/无效/无数据** 时被当成「匿名」处理，导致该录不录或不该录却录。

> 📷 **配图待补**：自动录音与排除规则设置页（落盘名：shizucallrecorder-feature-rules.png）

### 安全开关与无常驻后台

Shizuku 本身是强大攻击面；App 提供 **管理 Shizuku 开/关** 的开关，方便录音结束后关闭。另：**no persistent background process and notifications**——不是 24 小时监听的 Spyware 形态，而是 **电话状态触发**。这对接受「录音 App 不该常驻」的人友好；对要「后台保活」商业 App 用户可能反而不习惯。

---

## 🧠 核心逻辑：它为什么不一样？

传统非 Root 录音 App 往往只能录麦克风一侧；Root 方案改系统或装 Magisk 模块。ShizuCallRecorder 路径是：**Shizuku 把 ADB shell 权限借给 App** → 使用 [Shell 应用被赋予的高级权限列表](https://android.googlesource.com/platform/frameworks/base/+/android16-release/packages/Shell/AndroidManifest.xml) → 底层包装 **scrcpy-server 的 on-device 音频捕获**。

因此它 **强依赖两个外部项目**：Shizuku 与 scrcpy-server。Android 大版本或 OEM 改 hidden API，都可能 **整条链路失效**——README IMPORTANT 块已预警。GPL-3.0 选择原因（README）：尚无其他非 Root FOSS 通话录音，作者希望衍生替代品仍保持 FOSS。

第三方 IM（微信、Meet 等）**不是主焦点**；要录 Skype 类通话的人应另找方案，别误装后期望全能。

> 📷 **配图待补**：Shizuku ↔ Shell ↔ scrcpy-server 依赖图（落盘名：shizucallrecorder-architecture-flow.png）

---

## ⚔️ ShizuCallRecorder 和系统录音、商业录音 App 有什么区别？

| 维度 | ShizuCallRecorder | 系统自带录音 | 商业通话录音 App |
|------|-------------------|--------------|------------------|
| Root | 不需要 | 不需要 | 通常不需要 |
| 前置 | Shizuku + SUPPORT 配置 | 无（若有） | 安装即用为主 |
| 双向录音 | 目标能力（受 OEM 影响） | 许多机型 11+ 取消/弱化 | 视产品与地区 |
| 第三方 IM | 非主焦点 | 一般不支持 | 部分支持 |
| 开源 | GPL-3.0 + 商标条款 | 闭源系统组件 | 闭源为主 |
| 后台 | 电话事件触发，无常驻 | 视 OEM | 常常驻+通知 |
| 法律告知 | **不代你告知对方** | 视 OEM | 部分有提示音 |

选型句：要 **FOSS、运营商电话、已玩 Shizuku** → ShizuCallRecorder；要 **装完就录、不想配 Shizuku** → 先试 **系统录音**（若有）或 **商业录音 App**；要 **录微信/Zoom** → **不建议**以本 App 为主力，README 自己说不是焦点。

> 📷 **配图待补**：三类方案门槛对照（落盘名：shizucallrecorder-vs-competitor.png）

---

## 🧪 实测：我实际跑下来的体验

说明：功能与风险描述来自 README/SUPPORT 文档；**撰写日未在本人主力机完成 SUPPORT 全步骤实测**，**未测量 Opus/AAC 文件大小或码率**。以下优点/缺点按文档与 Android 生态常识整理。

### ✅ 好的方面

**1. 填补「非 Root + FOSS 通话录音」空白**  
README 自称 first non-root FOSS call recorder for Android 11+；Stars 1139、F-Droid/Izzy 分发，社区可见。

**2. 双向 + 蓝牙叙事**  
对采访、商务电话留档，比只录本机麦克风的一侧录更有价值——若你机型兼容。

**3. 无常驻后台**  
电话事件驱动，减少「录音 App 365 天挂通知」的心理负担与耗电争议。

**4. Shizuku 开关降低暴露面**  
录完可关 Shizuku，缓解银行 App 检测调试/Shizuku 的冲突——具体仍看对方 App 策略。

**5. 排除规则 + Opus/AAC 选择**  
自动录但可跳过匿名/联系人；编码可选兼顾体积与兼容性。

### ❌ 不好的方面

**1. Android 11 仅有限支持**  
测试表：11 需 **屏幕解锁**，否则 scrcpy 音频路径可能 **crash**；主推 12+。

**2. 初始配置税**  
README 大字：**YOU WILL NEED TO DO SOME INITIAL CONFIGURATIONS**，必须跟 SUPPORT.md——不是「安装即录」。

**3. 并发通话与非确定性**  
CAUTION：第二通来电、保持/切换通话时，可能 **继续录进同一文件** 且无新通知——多通场景易乱。

**4. 过滤逻辑与「匿名」误判**  
实时号码受限，号码来得晚/无效/为空时，可能按匿名处理，**自动录音决策出错**。

**5. Hidden API + OEM 不确定性**  
系统升级、厂商魔改可能导致 **突然不能录或异常开始录**；README 要求你 **自行监控行为**。

**6. 不处理法律告知**  
Disclaimer：应用 **不会** 替你在对方同意法域里告知或取得同意——自动录音在某些地区可能 **直接违法**。

**7. 第三方 IM 不在主战场**  
微信/Teams 通话别指望本 App 一站式解决。

我会考虑装的场景：已长期用 Shizuku 管别的工具、主要录 **移动/联通/电信蜂窝电话**、愿意每次检查录音文件是否生成。不会强推的场景：公司合规要求「必播提示音」、员工手机统一 MDM 禁调试——Shizuku 路线首先就被挡。

> 📷 **配图待补**：SUPPORT.md 配置步骤关键屏（落盘名：shizucallrecorder-hands-on.png）

---

## 💡 怎么高效用它

### 用法 1：先读 SUPPORT.md，再装 Release

从 [Releases latest](https://github.com/kitsumed/ShizuCallRecorder/releases/latest) 或 F-Droid 安装；**跳过 SUPPORT 步骤等于高概率翻车**。Android 11 用户额外记住：**通话前解锁屏幕**。

> 📷 **配图待补**：Shizuku 配对与授权流程（落盘名：shizucallrecorder-usage-1.png）

### 用法 2：自动录 + 保守排除

若当地法对「单方同意录音」宽松，仍建议 **先手动录几通** 验证双向音质，再开自动；排除规则先加 **全部联系人** 再白名单，比反过来 safer——具体以你律师说法为准，**本文非法律意见**。

### 用法 3：录完关 Shizuku

采访结束关闭 Shizuku 开关，减少与其他检测调试 App 的冲突；文件导出到加密目录后再做 ASR 转写——转写工具另选，本 App 不管。

> 📷 **配图待补**：录音文件导出与 Opus/AAC 选择（落盘名：shizucallrecorder-usage-2.png）

---

## ⚠️ 安装和使用需要注意什么？

### 法律免责（README Disclaimer，必读本节）

**各国对电话录音法律复杂且不同**——例如可能要求 **所有参与方同意** 才能录。开发者与贡献者 **不对误用或法律后果负责**。详见 Wikipedia：[Telephone call recording laws](https://en.wikipedia.org/wiki/Telephone_call_recording_laws)。

**若法律要求你告知或征得同意，本应用不会替你完成。** 某些地区 **自动录音** 本身可能违法。 **这不是法律意见**；请咨询专业律师。

### CAUTION：应用行为非确定性（README 原文精神）

- **并发通话**：第二通来电、切换保持通话时，可能 **持续录进单一文件**，无单独通知。  
- **过滤逻辑**：实时号码访问受限，号码延迟/无效/缺失时可能当 **匿名**，自动录音判断出错。  
- **不可预见失败**：系统更新、Bug、设计选择可能导致 **意外开始/继续/失败录音**。

**用户责任**：确保录音行为符合当地法；**在 YOUR 设备上监控 App**；若观察到的行为违法，**必须立即停止**（挂断、删文件等）。

### 版本与 Shizuku

Android 12–16 为 README 测试表「Yes」；17 未知；11 Limited。Shizuku 推荐 [thedjchi fork](https://github.com/thedjchi/Shizuku)。Hidden API 依赖意味着 **每个大版本都要重测**。

### GPL-3.0 与商标

修改分发需遵守 GPL；**不得**使用 Contributor 商标；`ShizuCallRecorder` 名称与 `com.kitsumed.shizucallrecorder` 包名属 kitsumed。

### 安装渠道

GitHub Releases、F-Droid、IzzyOnDroid；贡献与翻译见 Weblate（README 提醒 Weblate 默认可能用注册邮箱 commit，注意隐私）。

> 📷 **配图待补**：Android 版本支持与 CAUTION 说明屏（落盘名：shizucallrecorder-note-permission.png）

---

> **怎么选：** 已 **熟练 Shizuku**、主要录 **运营商电话**、能 **自担录音同意法** 并愿意 **读 SUPPORT 配置** 的人，**优先**试 ShizuCallRecorder；要 **零配置即录** 或 **系统已带稳定双向录音**，**不建议**折腾本 App；要 **录微信/Zoom 等 IM**，**优先**商业录音 App 或平台自带能力，**别**以本 App 为主力。

---

## 👥 适合哪些用户？

### ✅ 适合

| 人群 | 原因 |
|------|------|
| 已用 Shizuku 的 Android 极客 | 增量成本低 |
| 需 FOSS 可审计录音 | GPL + 源码开放 |
| 采访/客服留档（蜂窝电话） | 双向录音目标场景 |
| 拒绝 Root 机 | Shell 权限路线 |

### ❌ 不太适合

| 人群 | 原因 |
|------|------|
| 不愿 USB 调试/Shizuku | 硬前置 |
| Android 11 且常锁屏接电话 | crash 风险 |
| 企业 MDM 禁调试 | 无法 Shizuku |
| 主要录 IM 通话 | 非主焦点 |
| 期望应用代做法务告知 | README 明确不做 |

> 📷 **配图待补**：采访电话 + 事后导出工作流（落盘名：shizucallrecorder-who-workflow.png）

---

## 📊 总结表格

| 维度 | 评分 | 说明 |
|------|------|------|
| 安装难度 | ⭐⭐⭐⭐ | Shizuku + SUPPORT；非一键 |
| 核心能力 | ⭐⭐⭐⭐ | 双向蜂窝录音（视 OEM） |
| 稳定性 | ⭐⭐⭐ | Hidden API；CAUTION 非确定性 |
| 文档/社区 | ⭐⭐⭐⭐ | README/SUPPORT 诚实；⭐1139 |
| 成本 | ⭐⭐⭐⭐⭐ | 开源免费；法务自备 |

**综合评分：3.6 / 5.0**（工具分；不含法律风险）

> **一句话总结**：ShizuCallRecorder 适合 **Shizuku 用户专录运营商电话**——FOSS、双向、无常驻；**法律告知与并发 quirks 必须你自己扛**。

---

## 🔗 ShizuCallRecorder 官网与项目地址

- **GitHub**：https://github.com/kitsumed/ShizuCallRecorder  
- **Releases**：https://github.com/kitsumed/ShizuCallRecorder/releases/latest  
- **F-Droid**：https://f-droid.org/packages/com.kitsumed.shizucallrecorder/  
- **IzzyOnDroid**：https://apt.izzysoft.de/packages/com.kitsumed.shizucallrecorder  
- **SUPPORT 配置**：仓库 `docs/SUPPORT.md`  
- **对照**：系统自带录音 · 商业通话录音 App  
- **协议**：GPL-3.0 + Section 7 商标额外条款  

---

**标签**：#Android #通话录音 #Shizuku #ShizuCallRecorder #FOSS #T2单品

---

边界声明：夹内笔记为空，事实以 GitHub README 为准；Stars 1139 为撰写日仓库显示；法律免责与 CAUTION 行为说明已写入；**未编造录音测速**；Lovart 与场景弱相关未植入。

### BLOCK 自检（本稿）

- [x] 单主角 ShizuCallRecorder · H2 齐全 · 功能三列表 ≥3 行 + H3 展开  
- [x] 不好的方面 ≥7 · 适合/不太适合双表  
- [x] 怎么选含优先/不建议 · README 法律免责 + CAUTION 已写入  
- [x] 配图待补 callout，无 IMAGE_BRIEF 断链 · 无禁词  
- [x] 未编造测速 · 竞品表含系统/商业  
- [ ] 实拍图待补
