---
title: "OpenLess：开源语音输入，口述需求整理成 AI Prompt"
slug: openless
date: 2026-06-15
updated: 2026-06-15
tags: [语音输入, Prompt整理, 开源]
categories: [AI工具]
summary: "OpenLess：开源语音输入，口述需求整理成 AI Prompt。平台：Mac/Win/Linux。"
focus_keyword: "OpenLess"
source: https://github.com/Open-Less/openless
author: ""
status: draft
---

# OpenLess：开源语音输入，口述需求整理成 AI Prompt

> 2.4k+ stars | Rust | MIT | 按住说话，松开即得 AI 润色后的文字

## 这是什么

OpenLess 是一个开源的跨平台语音输入应用（macOS 和 Windows），核心功能是：**按住快捷键说话，松开后 AI 自动将语音转录并润色为结构化文字，直接插入到当前光标位置**。它是 Typeless、Wispr Flow、Superwhisper 等商业语音输入工具的全开源替代方案。

OpenLess 的核心差异化在于"AI Prompt 模式"。普通语音输入工具只做逐字转录（你说的每个字都原样输出），而 OpenLess 的 AI 润色引擎能将松散的口语转化为结构清晰、上下文完整的高质量文本——尤其适合口述 AI Prompt。例如，你喃喃自语一段模糊需求，松开按键后，光标处出现的是带有编号、分点说明、措辞得体的完整 Prompt，可直接粘贴到 ChatGPT、Claude 或 Cursor 中使用。

OpenLess 坚持开源本地优先（MIT 协议），数据保留在你的机器上，你可以自带火山引擎 ASR + Ark/DeepSeek/OpenAI 等任意兼容的 LLM 进行润色。它还支持 Style Pack 市场——你可以创建、分享和安装社区风格包，让 AI 按照特定语气（如简洁的提交信息、热情的客服回复、小红书风格文案）来润色你的语音输入。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 经常需要向 ChatGPT/Claude/Cursor 描述需求的开发者 | ✅ 推荐 | AI Prompt 模式专为此设计，口述需求自动整理成结构化 Prompt，大幅减少打字和思考组织时间 |
| 需要大量文字输出但不想打字的写作者 | ✅ 推荐 | 按住说话即出润色后文字，适用于邮件、文档、长消息、代码注释等场景 |
| 注重隐私、不想语音数据上传商业服务器的用户 | ✅ 推荐 | 开源、数据本地存储、可自选 ASR 和 LLM 服务商，无供应商锁定 |
| 只需要简单逐字转录的用户 | ⚠️ 酌情 | OpenLess 的强项是 AI 润色，纯转录场景可能有更轻量的替代方案 |
| 仅需移动端语音输入的用户 | ⚠️ 酌情 | 主力平台为 macOS/Windows 桌面端，Android 版有实验性 APK 但功能不完整 |
| Linux 用户 | ❌ 不推荐 | 尚未正式支持 Linux（README 提及但实际未发布） |

## 安装

### macOS（Apple Silicon / Intel）

从 [GitHub Releases](https://github.com/appergb/openless/releases/latest) 下载 DMG 安装包，拖入 `/Applications`。首次启动后在终端执行（绕过未公证签名警告）：

```bash
xattr -cr /Applications/OpenLess.app
```

或通过 Homebrew 安装：

```bash
brew tap appergb/openless https://github.com/appergb/openless
brew install --cask openless
xattr -cr /Applications/OpenLess.app
```

### Windows

从 [GitHub Releases](https://github.com/appergb/openless/releases/latest) 下载 `OpenLess_<version>_x64-setup.exe` 运行安装程序。

### 首次配置

启动后需要：
1. macOS：授予麦克风权限 + 辅助功能权限（**授予后必须退出并重新打开应用**）
2. 在设置中填入火山引擎 ASR 凭证（APP ID / Access Token / Resource ID）+ Ark API Key
3. 可选：配置 OpenAI/DeepSeek/Anthropic 兼容 API 作为替代润色后端

### 从源码构建

```bash
git clone https://github.com/Open-Less/openless --recursive
cd openless/openless-all/app
npm ci
npm run tauri dev
```

## 核心用法

1. **基础语音输入**：将光标放在任意文本输入框（ChatGPT、Cursor、Notion、邮件、微信等），按住全局快捷键说话，松开后润色文本自动插入。如果应用不支持直接插入，自动降级为剪贴板粘贴。
2. **四种输出模式**：
   - **Raw**：原样转录，不做润色
   - **Light polish**：轻度润色，修正口语中的重复和口癖
   - **Structured（AI Prompt 模式）**：将松散口语整理为结构化、带编号和约束的 Prompt——这是 OpenLess 的招牌功能
   - **Formal**：转为正式书面语
3. **翻译热键**：按住翻译快捷键说话，输出直接翻译为配置的目标语言。
4. **Style Pack 市场**：在 Style 页面创建自定义风格包（如"小红书文案"、"Git 提交信息"），从 Marketplace 一键安装社区风格包，通过快捷键切换活跃风格。
5. **选中提问面板**：选中任意应用中的文本，按专用快捷键呼出浮动 QA 面板，对选中内容进行语音提问。
6. **词典管理**：在 Dictionary 页面添加专有名词、产品名、人名等，ASR 识别时将优先匹配，润色时也会智能替换。

## 注意事项与风险

- **需要自备 API Key**：OpenLess 不提供内置 ASR/LLM 服务，你需要自己注册火山引擎（ASR）和 Ark/DeepSeek（润色）的账号并获取 API Key。有相应 API 调用费用。
- **macOS 辅助功能权限**：必须在系统设置中授予并重启应用，否则热键和文本插入功能不工作。
- **自签名证书导致的安装警告**：macOS 可能需要执行 `xattr -cr` 命令绕开 Gatekeeper，Windows 可能有 SmartScreen 警告。
- **Beta 版本稳定性**：项目仍在快速迭代（当前 v1.3.8），部分功能（如翻译模式）标注为计划中或 beta 阶段。
- **不支持 iOS**：桌面端主力开发，Android APK 为实验性版本，无 iOS 支持计划。

## 与你现有工具的关系

- 与 [[SpokenType：支持自动润色的 AI 语音输入工具]] 互为替代：两者功能高度重合（语音输入 + AI 润色），OpenLess 是全开源桌面应用，SpokenType 也有类似定位，可根据平台和喜好选择。
- 与 [[../03-效率生产力/AirTranslate：Mac 系统音频实时翻译，悬浮字幕]] 互补：AirTranslate 专注实时转录翻译，OpenLess 专注语音转润色文字插入，场景不同。
- 与 [[HumanizeAI：AI文本人性化工具]] 协作：OpenLess 输出初步润色文本后，如果需要进一步消除 AI 痕迹，可送入 Humanizer-zh 进行二次处理。
- 与 [[Privacy Filter：本地隐私脱敏，发给 AI 前清理敏感文本]] 协作：如果语音中提到敏感信息，在 OpenLess 润色前后可用 Privacy Filter 检查和清理。
- 与 [[../01-AI-Agent生态/Claude Code + Obsidian：Claude Code + Obsidian Visual Skills 全自动]] 协同：用 OpenLess 口述 Claude Code 指令，快速将语音需求转化为可执行的 AI 命令。

## FAQ

### Q: OpenLess 和 Typeless / Wispr Flow 有什么本质区别？
A: OpenLess 完全开源（MIT），你可以审计代码、自选 ASR/LLM 服务商，数据不会发送到你不信任的服务器。Typeless 和 Wispr Flow 是闭源商业产品，按月订阅，音频数据上传到他们的服务器。

### Q: 语音数据和文本会离开我的设备吗？
A: 语音数据会发送到你配置的 ASR 服务商（如火山引擎），润色文本会发送到你配置的 LLM 服务商。但 OpenLess 本身不收集数据，所有凭证存储在 macOS Keychain 或 Windows 凭据管理器中，不会写入明文文件。

### Q: AI 会代替我回答问题吗？
A: 不会。润色模型只负责清理和结构化你的文本，不会回答你的问题或执行任何任务。例如你说"这个应用还需要什么功能"，输出会是"I need suggestions for features this app still needs"——一个干净的提问，而不是一份功能清单。

## 相关链接

- 官方网站：https://openless.top
- GitHub：https://github.com/Open-Less/openless
- 用户文档：https://github.com/Open-Less/openless/blob/beta/USAGE.md
- Discord：https://discord.gg/vTZHTFGFm
- QQ 群：1078960553
- 来源：https://www.ahhhhfs.com/81036/
