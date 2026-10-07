---
title: "Privacy Filter：本地隐私脱敏，发给 AI 前清理敏感文本"
slug: privacy-filter
date: 2026-06-15
updated: 2026-06-15
tags: [隐私, 脱敏, 安全]
categories: [AI工具]
summary: "Privacy Filter：本地隐私脱敏，发给 AI 前清理敏感文本。平台：Mac/Win/Linux。"
focus_keyword: "Privacy Filter"
source: https://github.com/becoolme/privacyfilter
status: draft
---

# Privacy Filter：本地隐私脱敏，发给 AI 前清理敏感文本

> Web 工具 | 100% 本地运行 | OpenAI 开源模型

## 这是什么

[Privacy Filter](https://privacyfilter.app) 是一款**纯浏览器端运行的隐私脱敏工具**。你把文本粘贴进去，它自动识别并遮蔽姓名、邮箱、电话号码、地址、账号、日期、URL 和密钥等 8 类敏感信息，一键生成脱敏后的安全文本——全程数据不出设备。

核心方案基于 OpenAI 开源的 `privacy-filter` 模型权重，由 Transformers.js 在浏览器中本地执行推理。首运行从 Hugging Face 下载模型（约需几秒），之后利用浏览器缓存秒开。支持 WebGPU 硬件加速（Chrome/Edge），也提供 WASM 降级。

相比传统的正则脱敏方案，它的优势在于**上下文感知**：能识别多语言姓名、自由格式地址等正则难以覆盖的实体。但这是**辅助工具**，不能替代法律合规审查——建议关键场景用正则 + 此模型双重覆盖。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 日常送 Prompt 到 ChatGPT/Claude/Gemini 前清洗 | ✅ 推荐 | 一键遮蔽个人信息，避免无意泄露 |
| 处理客服工单、日志截图时脱敏 | ✅ 推荐 | 浏览器本地跑，不用把客户数据上传第三方 |
| 代码仓库审计（检测 README/文档中的密钥泄露） | ✅ 推荐 | 能识别 ghp_、api_key 等 secret 实体 |
| 需要完全合规的 GDPR/HIPAA 场景 | ❌ 不推荐 | 仅辅助工具，无法替代合规审计流程 |
| 需要批量 API 脱敏的生产流水线 | ⚠️ 酌情 | 无 API，纯浏览器端；批量场景建议直接调用 Hugging Face 模型 |

## 安装

无需安装。打开浏览器访问 [https://privacyfilter.app](https://privacyfilter.app) 即可使用。首次运行会自动从 Hugging Face 下载模型权重。

如果你希望本地部署：

```bash
git clone https://github.com/becoolme/privacyfilter.app
cd privacyfilter.app
# 用任意 HTTP 服务器托管静态文件即可
python3 -m http.server 8080
# 然后打开 http://localhost:8080
```

## 核心用法

1. 打开 [privacyfilter.app](https://privacyfilter.app)
2. 等模型加载完成后，在左侧输入框粘贴你要清洗的文本
3. 点击 **Detect**，右侧会显示高亮标注的实体和脱敏后的文本
4. 点击 **Copy result** 复制脱敏文本，直接粘贴到 ChatGPT 等对话窗口

**支持图片 OCR**：上传截图，浏览器本地 OCR 识别文字后再做 PII 脱敏——适用于分享报错截图、聊天记录等场景。

**8 类检测实体**：姓名（`private_person`）、邮箱、电话、地址、账号、日期、URL、密钥（`secret`）。你可以根据实际需求在结果中逐类确认。

## 注意事项与风险

- **非 100% 准确**：模型可能漏报或误报，脱敏后仍需人工复核，尤其是法律/医疗等敏感领域。
- **本地模型限制**：相比服务端大模型，`privacy-filter` 的覆盖范围有限，复杂场景建议正则 + 模型组合使用。
- **浏览器兼容**：WebGPU 加速仅 Chrome/Edge 支持最优；Safari/Firefox 回退 WASM，速度较慢。
- **首运行下载**：首次打开需下载约 30MB 模型文件，网络不佳时可能需要等待。

## 与你现有工具的关系

- 发送 Prompt 前与 [[OpenLess：开源语音输入，口述需求整理成 AI Prompt]]、[[SpokenType：支持自动润色的 AI 语音输入工具]] 配合：口述需求 → 自动润色 → Privacy Filter 脱敏 → 发送到 ChatGPT。
- 如果你在用 [[../01-AI-Agent生态/AiMaMi：OpenAI Codex 桌面管理工具]] 管理 Codex，可用 Privacy Filter 在粘贴敏感日志/配置前先行脱敏。
- 与 [[Image Provenance：纯浏览器端 AI 图片溯源，检测签名与 EXIF]] 互补：一个管文本隐私，一个管图片溯源。

## FAQ

### Q: 我的文本真的不会上传到服务器吗？
A: 不会。推理全部在浏览器内通过 Transformers.js 完成，首次加载模型来自 Hugging Face CDN，之后文本永不离开你的设备。可打开浏览器开发者工具 Network 面板验证——Detect 操作不会产生任何网络请求。

### Q: 能脱敏中文姓名和身份证号吗？
A: 模型能识别多语言姓名（含中文），但身份证号、车牌号等特定格式不在当前 8 类实体中。这些强格式实体建议用正则补充。Privacy Filter 更适合自然语言中的个人信息遮蔽。

### Q: 和 ChatGPT 的临时聊天模式有什么区别？
A: ChatGPT 临时聊天是服务端承诺不记录，但你仍需信任 OpenAI。Privacy Filter 在数据**离开你设备之前**就完成脱敏，两者互补——先脱敏，再发送，双重保险。

## 相关链接

- 官网：https://privacyfilter.app
- GitHub：https://github.com/becoolme/privacyfilter.app
- Hugging Face 模型：https://huggingface.co/openai/privacy-filter
