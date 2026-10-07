---
title: "Voice-Pro：免费 AI 配音神器，本地部署视频翻译与语音克隆"
slug: voice-pro
date: 2026-06-15
updated: 2026-06-15
tags: [配音, 语音克隆, ElevenLabs平替]
categories: [AI工具]
summary: "Voice-Pro：免费 AI 配音神器，本地部署视频翻译与语音克隆。平台：Win/Linux。"
focus_keyword: "Voice-Pro"
source: https://github.com/abus-aikorea/voice-pro
status: draft
---

# Voice-Pro：免费 AI 配音神器，本地部署视频翻译与语音克隆

> Win/Linux | [11k Stars](https://github.com/abus-aikorea/voice-pro/stargazers)

## 这是什么

Voice-Pro 是一站式 AI 视频翻译与语音克隆 WebUI，通过 Gradio 界面将 YouTube 视频下载、人声分离（Demucs）、语音识别（Whisper/Faster-Whisper/WhisperX）、100+语言翻译（Deep-Translator）和文字转语音/语音克隆（F5-TTS、E2-TTS、CosyVoice、Edge-TTS、kokoro）整合为完整工作流。

你可以上传一段视频或 YouTube 链接，Voice-Pro 自动提取音频、去除背景噪音、识别字幕、翻译为任意语言，最终用**克隆的音色或 TTS 引擎**生成多语种配音。这是目前最接近 **ElevenLabs 免费平替**的开源方案，且完全本地部署、无需订阅。

与同类的 RVC、GPT-SoVITS 等语音克隆工具不同，Voice-Pro 的优势在于"完整链路"——不是单一的 TTS 或语音克隆，而是覆盖从视频下载到多语言配音的全流程。内置零样本语音克隆支持（F5-TTS/CosyVoice），只需提供一段参考音频即可复刻目标音色。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 视频创作者/自媒体人，需要将视频翻译为多语言配音 | ✅ 推荐 | 全流程自动化：下载→去噪→识别→翻译→合成，一次搞定多语种版本 |
| 需要语音克隆但不愿付费 ElevenLabs 的个人开发者 | ✅ 推荐 | F5-TTS/CosyVoice 零样本克隆，免费本地运行，支持多语言音色复刻 |
| Mac 用户或没有 NVIDIA GPU 的用户 | ⚠️ 酌情 | 官方声明 Mac/Linux 未充分验证，无 GPU 时处理速度极慢，部分功能可能中断 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/abus-aikorea/voice-pro.git
cd voice-pro

# Windows 用户
configure.bat   # 安装 git/ffmpeg/CUDA 等依赖（首次约1小时）
start.bat       # 启动 WebUI，浏览器自动打开 http://127.0.0.1:7870

# Mac/Linux 用户（实验性支持）
chmod +x configure.sh start.sh
./configure.sh
./start.sh
```

推荐 NVIDIA GPU（CUDA 12.4），VRAM 建议 8GB+。首次启动会下载 CosyVoice2-0.5B 模型（约 9GB），网络不佳时可能需要数小时。若遇到问题，删除 `installer_files` 文件夹后重新运行 `configure.bat` + `start.bat`。

## 核心用法

1. **配音工作室**（Dubbing Studio）：输入 YouTube 链接或上传视频，选择 Demucs 去人声/去噪，然后用 Whisper 识别字幕，设置翻译目标语言，选择 TTS 引擎生成配音，可调节语速/音量/音调
2. **Whisper 字幕**：专注字幕生成，支持 90+ 语言，带视频内嵌字幕预览和词级高亮
3. **实时翻译**：麦克风实时语音识别 + 机器翻译，支持 SRT/ASS 等字幕文件翻译
4. **语音生成**：独立 TTS 页面，可选 Edge-TTS（400+音色）、F5-TTS（零样本克隆）、CosyVoice、kokoro，内置大量名人参考音色可直接试用
5. **语音克隆流程**：上传或录制 30 秒参考音频 → 选择克隆引擎（F5-TTS/CosyVoice）→ 输入目标文本 → 生成克隆音色朗读结果

## 注意事项与风险

- 官方明确表示因团队转向 WeConnect 开发，**该项目暂时不再更新维护**
- Windows + NVIDIA GPU 是已验证的稳定环境，Mac/Linux 使用可能遇到未解决问题
- 首次安装耗时较长（1 小时以上），需要稳定的网络连接
- CosyVoice2-0.5B 模型约 9GB，加上其他模型依赖，建议预留 20GB+ 硬盘空间
- 免费的 Edge-TTS 和 kokoro 是品质基线，付费版包含 Azure TTS 和 Azure Translator（通过 Shopify 购买）
- 语音克隆涉及伦理和法律风险，请勿用于冒充他人或欺诈用途

## 与你现有工具的关系

- **与 ElevenLabs**：Voice-Pro 是最接近的开源平替。ElevenLabs 品质更高但按字符收费，Voice-Pro 免费本地部署。可将 Voice-Pro 用于批量/实验场景，ElevenLabs 用于正式发音
- **与 Lovart/LibTV**：职责互补。Lovart/LibTV 生成视频画面，Voice-Pro 为视频生成多语言配音。搭配使用：用 Lovart 生成视频 → 用 Voice-Pro 做多语种配音 → 用 Auto-Subs 生成字幕
- **与 RVC/GPT-SoVITS**：Voice-Pro 内置 F5-TTS 和 CosyVoice，提供了替代方案。如果你已有 RVC 模型，Voice-Pro 也可作为前端 WebUI 使用

## 常见问题（FAQ）

**Q: Voice-Pro 的语音克隆和 ElevenLabs 差距有多大？**
A: F5-TTS 和 CosyVoice 在清晰度和自然度上已接近商用水平，但在情感表达和长句稳定性上仍有差距。对于短视频配音和个人项目足够使用，正式商业发行建议用 ElevenLabs。

**Q: 为什么启动后浏览器没有自动打开？**
A: 手动打开浏览器，输入命令窗口中显示的地址（默认 `http://127.0.0.1:7870`）即可。如果端口冲突，可在启动前修改配置。

**Q: 出现 CUDA Out-Of-Memory 错误怎么办？**
A: 将 Denoise 级别设为 0 或 1（级别 2 需 8GB+ VRAM），将 Compute Type 设为 int（float 质量更好但占用更多显存）。或使用 CPU 模式（速度会显著下降）。

## 相关链接

- GitHub：https://github.com/abus-aikorea/voice-pro
