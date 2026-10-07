---
title: "纯前端音视频转文字：浏览器端讯飞 API 长音频识别"
slug: 纯前端音视频转文字
date: 2026-06-15
updated: 2026-06-16
tags: [语音转文字, 纯前端, 讯飞, 隐私保护]
categories: [在线工具]
summary: "基于讯飞语音听写 API 的纯前端音视频转文字工具，支持自动分段、长音频处理，API Key 仅保存在浏览器 localStorage，无需后端服务器。每天 500 次免费额度，MIT 协议。"
focus_keyword: "纯前端音视频转文字"
source: https://github.com/aiyoubucuoyou/voice-to-text-tools
status: draft
---

# 纯前端音视频转文字：浏览器端讯飞 API 长音频识别

> 纯前端、零后端、隐私优先 | 32 Stars | MIT | 单 HTML 文件 | 讯飞语音听写 API

## 这是什么

voice-to-text-tools 是一个极简的纯前端音视频转文字工具，整个项目本质上是一个约 2000 行的单文件 HTML 页面（内含 CSS 和 JavaScript）。上传音频或视频文件后，浏览器端的 FFmpeg (WebAssembly) 将音频提取并分段，再通过 WebSocket 直连讯飞语音听写 API 完成识别，最终在页面上显示并支持复制或下载文本结果。

它的核心理念是"隐私优先"：所有文件处理在浏览器本地完成，讯飞 API 的凭据（APPID、API Key、API Secret）仅保存在浏览器 localStorage 中，从不经过任何第三方服务器。代码部署在 GitHub Pages 上（https://zhuan.dlidli.wang），同时也可以直接下载 index.html 本地打开运行（需通过 HTTP 服务器，file:// 协议无法加载 JSON）。

与同类工具（如飞书妙记、讯飞听见客户端）的差异：无需安装任何软件，无需注册第三方平台，完全开源可审计，API Key 由用户自行申请（讯飞每天 500 次免费额度），成本接近于零。但由于依赖讯飞 API，识别语言主要为中文普通话。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 需要快速将中文录音/视频转文字的个体用户 | ✅ 推荐 | 即开即用，每天 500 次免费额度，无需安装 |
| 对隐私敏感的内容创作者 | ✅ 推荐 | 纯前端处理，凭据本地存储，文件不经过任何服务器 |
| 学生/研究者做采访转录 | ✅ 推荐 | 支持自动分段处理长音频，响应式设计手机也能用 |
| 需要多人协作的团队 | ⚠️ 酌情 | 无多用户功能和协作机制，每个用户需自行配置 API Key |
| 需要转写英文/多语言音频的用户 | ⚠️ 酌情 | 讯飞语音听写以中文为主，多语言识别准确率不如 Whisper |
| 完全不想申请任何 API Key 的用户 | ❌ 不推荐 | 必须自行注册讯飞开放平台并获取 API 凭据 |
| 需要极高精度（如法律/医疗场景）的用户 | ❌ 不推荐 | 讯飞通用听写 API 面向日常场景，专业领域需专用模型 |

## 安装与前置条件

- **无需安装任何软件**（浏览器即运行环境）
- **讯飞 API 凭据**：需注册讯飞开放平台并获取 APPID、API Key、API Secret
- **浏览器要求**：支持 WebAssembly 的现代浏览器

```bash
# 本地运行（任选一种）
git clone https://github.com/aiyoubucuoyou/voice-to-text-tools.git
cd voice-to-text-tools
python -m http.server 8000        # Python
# php -S localhost:8000            # PHP
# npx serve .                      # Node.js

# 访问 http://localhost:8000
```

或直接访问在线版：https://zhuan.dlidli.wang/

## 核心用法

### 首次配置

1. 访问页面后，在配置区域填入凭据
- 注册/登录 [讯飞开放平台](https://www.xfyun.cn/)
- 进入 [语音听写服务](https://console.xfyun.cn/services/iat) 控制台
- 创建应用，获取 APPID、API Key、API Secret
- 每天 500 次免费额度
2. 配置自动保存在浏览器 localStorage 中，刷新页面无需重新输入

### 转写流程

1. 点击上传区域或拖拽音视频文件到页面
2. 工具自动完成：提取音频 → 分段处理（突破单次 60 秒限制）→ 逐段发送讯飞 API 识别
3. 识别完成后可复制文本或下载 txt 文件
4. 支持自动分段，可一次性处理数小时的长音频

## 注意事项与风险

- **必须通过 HTTP 服务器访问**：直接双击 index.html 使用 `file://` 协议会遇到 CORS 错误，需要用 `python -m http.server` 等方式启动
- **讯飞免费额度限制**：每天 500 次，超出后需付费；注意"一次"指单段识别请求，长音频自动分段后会占用多次调用
- **网络依赖**：浏览器需能访问讯飞 WebSocket API（`ws://iat-api.xfyun.cn`），某些企业网络可能拦截 WebSocket
- **浏览器性能**：FFmpeg.wasm 处理大视频文件时可能消耗较多内存，建议音频/视频文件不超过 500MB
- **localStorage 清除风险**：清除浏览器数据会导致 API 凭据丢失，需重新配置

## 与你现有工具的关系

- 与 [[../05-开发技术栈/tools.video：不上传文件的在线视频压缩工具]] 同属纯浏览器端处理工具，可组成「提取音频→转换→转文字」的工作链
- 转写结果可直接用于 [[../01-AI-Agent生态/Claude Code Humanizer：用 Claude Code Humanizer 提升文章可读性]] 做去痕润色
- 与 videocut-skills 互补：本工具做内容转录，[[../01-AI-Agent生态/Claude Code 自动化剪辑：基于 Claude Code 的自动化剪辑工作流]] 做基于语义的智能剪辑
- 转写后的字幕/文稿可导入 [[Toonflow：开源 AI 短剧生成工具]] 作为剧本参考

## FAQ

### Q: 完全免费吗？
A: 代码开源免费（MIT），日活跃使用时讯飞 API 每天提供 500 次免费额度，个人日常使用通常足够。高频使用超出额度需付费。

### Q: 安全性如何？我的文件会上传到哪里？
A: 音频文件通过 WebAssembly（ffmpeg.wasm）在本地浏览器中处理，分段的音频数据通过 WebSocket 直连讯飞 API 服务器做语音识别。文件本身不会被上传到工具开发者或任何第三方服务器。API 凭据仅保存在你浏览器本地。

### Q: 一次能处理多长的音频？
A: 支持自动分段处理，理论上不限时长。单次识别限 60 秒，工具会自动切割后逐段发送。

### Q: 支持哪些语言和方言？
A: 主要支持中文普通话，也支持英文。具体以讯飞语音听写 API 的能力为准。

### Q: 支持部署到自己的服务器吗？
A: 可以。它是一个纯静态单 HTML 文件，Fork 仓库后部署到 GitHub Pages 或任意静态托管即可。注意：API 调用始终发生在用户浏览器端，你的服务器不会接触到任何文件或 API 请求。

## 相关链接

- GitHub：https://github.com/aiyoubucuoyou/voice-to-text-tools
- 在线演示：https://zhuan.dlidli.wang/
- 讯飞开放平台：https://www.xfyun.cn/
- 讯飞语音听写控制台：https://console.xfyun.cn/services/iat
