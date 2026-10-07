---
title: "Open-XiaoAI：解锁小爱音箱 AI 潜力"
slug: open-xiaoai-xiaomi-speaker-ai
date: 2026-05-29
updated: 2026-05-29
tags: [Open-XiaoAI, 小爱音箱, 智能家居, MiGPT, 已停更]
categories: [AI工具]
summary: Open-XiaoAI 通过刷机与 Client/Server 接管小爱音箱听与说，接入小智 AI、MiGPT、Gemini Live 等。仅支持小爱音箱 Pro 等指定机型，项目已停止维护，使用前请读免责声明。
focus_keyword: Open-XiaoAI
source: https://github.com/idootop/open-xiaoai
author: idootop (Del Wang)
status: draft
---

# Open-XiaoAI：让小爱音箱「听见你的声音」

> 2,491+ stars | MIT | ⚠️ **项目已停止维护**

## 这是什么

[Open-XiaoAI](https://github.com/idootop/open-xiaoai) 在作者上一代 [MiGPT](https://github.com/idootop/mi-gpt) 基础上**再次进化**：不只接 ChatGPT，而是**直接接管小爱音箱的「耳朵」和「嘴巴」**，用多模态大模型与 AI Agent 释放硬件潜力。

架构：**Client 端（音箱补丁）+ Server 端（能力演示）**，你可自行编写功能。

> [!WARNING]  
> 仓库声明：**已停止维护**，不再提供更新与支持。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 已有指定机型、愿刷机折腾 | ⚠️ 自行评估 | 停更后风险自担 |
| 小爱音箱 Pro（LX06）/ 小米智能音箱 Pro（OH2P） | ✅ 仅这两类 | 其它型号勿直接用 |
| 其它型号小爱 / 不想刷机 | ❌ 看「相关项目」 | mi-gpt、xiaogpt、xiaomusic 等 |
| 商业部署 / 大规模售卖改造 | ❌ 禁止 | 免责声明明确学术研究/个人测试 |

## 安装与前置条件

> **仅适用于：小爱音箱 Pro（LX06）、Xiaomi 智能音箱 Pro（OH2P）**

1. [刷机](https://github.com/idootop/open-xiaoai/blob/main/docs/flash.md) 开启 SSH  
2. 音箱安装 [Client 端](https://github.com/idootop/open-xiaoai/tree/main/packages/client-rust)  
3. 运行示例 Server：  
   - [接入小智 AI](https://github.com/idootop/open-xiaoai/tree/main/examples/xiaozhi)  
   - [自定义唤醒词](https://github.com/idootop/open-xiaoai/tree/main/examples/kws)  
   - [MiGPT 完美版](https://github.com/idootop/open-xiaoai/tree/main/examples/migpt)  
   - [Gemini Live API](https://github.com/idootop/open-xiaoai/tree/main/examples/gemini)  
   - [立体声组合](https://github.com/idootop/open-xiaoai/tree/main/examples/stereo)  

演示视频见仓库（B 站：小智 / 唤醒词 / MiGPT）。

## 核心用法

### 能力方向

- 替换默认语音助手链路，接入自定义 LLM / Agent  
- 自定义唤醒词（KWS 示例）  
- 多音箱组立体声  
- 与 MiGPT、小智等生态对接  

### 不刷机的替代

仓库 TIP 列出：mi-gpt、migpt-next、xiaogpt、xiaomusic 等。

## 注意事项与风险

- **已停更**：新系统/新固件可能导致失效，无官方修复。  
- **刷机风险**：变砖、失去保修、账号封禁等需自行承担。  
- **非官方**：与小米无任何隶属关系；商标与云服务归权利方。  
- **法律**：严禁用于商业服务、攻击、窃密等；继续下载即视为同意[用户协议](https://github.com/idootop/open-xiaoai/blob/main/agreement.md)。  
- **机型**：其它型号误刷可能损坏设备。

## 与你现有工具的关系

- 与 [[DeepSeek GUI：桌面智能体工作台]]、[[Hermes Slate Desk：Hermes Agent 桌面 GUI 客户端]] 同为「语音入口」实验，但 Open-XiaoAI 绑定**小米硬件**。  
- 内容生产仍可用 [[AIMedia：全自动 AI 媒体创作与多平台发布]] 等，与小爱播放链路独立。

## FAQ

### Q: 还值得 2026 年上手吗？
A: 仅建议已有经验、接受无维护；新用户优先评估 mi-gpt 等活跃替代。

### Q: 和 MiGPT 区别？
A: Open-XiaoAI 更底层接管音频通路；MiGPT 偏应用层接 GPT（见作者两篇项目）。

### Q: 必须 Linux 服务器吗？
A: Server 端按示例跑在你控制的机器上，Client 在音箱；细节见各 example README。

## 相关链接

- GitHub：https://github.com/idootop/open-xiaoai  
- MiGPT：https://github.com/idootop/mi-gpt  
- 刷机教程：仓库 `docs/flash.md`  
- 免责声明：`agreement.md`
