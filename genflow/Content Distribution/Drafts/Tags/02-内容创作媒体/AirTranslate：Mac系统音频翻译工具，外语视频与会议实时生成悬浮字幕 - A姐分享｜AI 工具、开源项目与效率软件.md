---

title: "AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕 - A姐分享｜AI 工具、开源项目与效率软件"
source: "https://www.ahhhhfs.com/80852/"
author:
  - "[[ahhhhfs]]"
published: 2026-05-19
created: 2026-08-04
description: "AirTranslate 是一款开源的 Mac 系统音频翻译与实时转写工具。它可以直接捕获 Mac 正在播放的系统音频并生成悬浮字幕，支持 Apple 模式与可选 GPT 模式，适合外语视频、会议和直播场景。"
tags:
  - "AI"
  - "视频"
  - "字幕"
  - "音频"
  - "翻译"

---
AirTranslate 是一款面向 macOS 的开源实时音频转写与翻译工具，它可以直接捕获 Mac 正在播放的系统音频，并把内容实时显示为转写文本、翻译结果或悬浮字幕。

[![AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕](https://www.ahhhhfs.com/wp-content/uploads/2026/05/AirTranslate%EF%BC%9AMac%E7%B3%BB%E7%BB%9F%E9%9F%B3%E9%A2%91%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7%EF%BC%8C%E5%A4%96%E8%AF%AD%E8%A7%86%E9%A2%91%E4%B8%8E%E4%BC%9A%E8%AE%AE%E5%AE%9E%E6%97%B6%E7%94%9F%E6%88%90%E6%82%AC%E6%B5%AE%E5%AD%97%E5%B9%95.webp "AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕")](https://www.ahhhhfs.com/wp-content/uploads/2026/05/AirTranslate%EF%BC%9AMac%E7%B3%BB%E7%BB%9F%E9%9F%B3%E9%A2%91%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7%EF%BC%8C%E5%A4%96%E8%AF%AD%E8%A7%86%E9%A2%91%E4%B8%8E%E4%BC%9A%E8%AE%AE%E5%AE%9E%E6%97%B6%E7%94%9F%E6%88%90%E6%82%AC%E6%B5%AE%E5%AD%97%E5%B9%95.jpg)

很多经常跨国开会，或者喜欢在 YouTube 上看外语视频的 Mac 用户，都会遇到一个挺烦的问题：普通翻译软件往往只能通过麦克风“听”声音，音质容易被扬声器、环境噪音和回音影响。想直接抓取 Mac 正在播放的系统音频，以前又常常要折腾 BlackHole 这类虚拟声卡和音频通道。AirTranslate 作为一款轻量级的 Mac系统音频翻译 工具，解决的正是这个麻烦。

[![AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕](https://www.ahhhhfs.com/wp-content/uploads/2026/05/AirTranslate%EF%BC%9AMac%E7%B3%BB%E7%BB%9F%E9%9F%B3%E9%A2%91%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7%EF%BC%8C%E5%A4%96%E8%AF%AD%E8%A7%86%E9%A2%91%E4%B8%8E%E4%BC%9A%E8%AE%AE%E5%AE%9E%E6%97%B6%E7%94%9F%E6%88%90%E6%82%AC%E6%B5%AE%E5%AD%97%E5%B9%95-02.webp "AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕")](https://www.ahhhhfs.com/wp-content/uploads/2026/05/AirTranslate%EF%BC%9AMac%E7%B3%BB%E7%BB%9F%E9%9F%B3%E9%A2%91%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7%EF%BC%8C%E5%A4%96%E8%AF%AD%E8%A7%86%E9%A2%91%E4%B8%8E%E4%BC%9A%E8%AE%AE%E5%AE%9E%E6%97%B6%E7%94%9F%E6%88%90%E6%82%AC%E6%B5%AE%E5%AD%97%E5%B9%95-02.jpg)

**AirTranslate是什么？** 它不是传统文本翻译工具，也不是离线字幕压制软件。它更像是一个运行在 Mac 桌面上的实时字幕层，直接调用底层 ScreenCaptureKit 框架抓取声音，非常适合处理正在播放的会议、视频、直播和课程音频。

## AirTranslate 和普通 Mac 翻译工具差别在哪？

它的核心差异在于“系统音频优先”。你不需要把声音从扬声器放出来再用麦克风收，它在系统内部就把音频流截流下来做识别。并且生成的字幕窗口是悬浮的，你可以边看视频或边开会，边看双语对照的字幕。

[![AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕](https://www.ahhhhfs.com/wp-content/uploads/2026/05/AirTranslate%EF%BC%9AMac%E7%B3%BB%E7%BB%9F%E9%9F%B3%E9%A2%91%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7%EF%BC%8C%E5%A4%96%E8%AF%AD%E8%A7%86%E9%A2%91%E4%B8%8E%E4%BC%9A%E8%AE%AE%E5%AE%9E%E6%97%B6%E7%94%9F%E6%88%90%E6%82%AC%E6%B5%AE%E5%AD%97%E5%B9%95-%E5%8E%9F%E7%90%86.webp "AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕")](https://www.ahhhhfs.com/wp-content/uploads/2026/05/AirTranslate%EF%BC%9AMac%E7%B3%BB%E7%BB%9F%E9%9F%B3%E9%A2%91%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7%EF%BC%8C%E5%A4%96%E8%AF%AD%E8%A7%86%E9%A2%91%E4%B8%8E%E4%BC%9A%E8%AE%AE%E5%AE%9E%E6%97%B6%E7%94%9F%E6%88%90%E6%82%AC%E6%B5%AE%E5%AD%97%E5%B9%95-%E5%8E%9F%E7%90%86.jpg)

## Apple 模式和 GPT 模式怎么选？

除了免装虚拟声卡，它把“翻译精度”和“成本”的选择权交给了用户，内置了两种工作模式：

- **Apple 模式（默认优先）：** 主要调用 macOS 自带的语音识别（Speech）与翻译（Translation）框架，成本更低，也偏向本地处理。具体语言是否可用、是否需要下载语言包，取决于你当前的 macOS 环境设置。
- **GPT 模式（更适合复杂语境）：** 如果你遇到专业外语会议、长句口语，或者对翻译流畅度要求更高，可以填入自己的 OpenAI API Key，让 OpenAI Realtime 模型参与实时转写和翻译。

[![AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕](https://www.ahhhhfs.com/wp-content/uploads/2026/05/AirTranslate%EF%BC%9AMac%E7%B3%BB%E7%BB%9F%E9%9F%B3%E9%A2%91%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7%EF%BC%8C%E5%A4%96%E8%AF%AD%E8%A7%86%E9%A2%91%E4%B8%8E%E4%BC%9A%E8%AE%AE%E5%AE%9E%E6%97%B6%E7%94%9F%E6%88%90%E6%82%AC%E6%B5%AE%E5%AD%97%E5%B9%95-%E6%A8%A1%E5%BC%8F%E6%AF%94%E8%BE%83.webp "AirTranslate：Mac系统音频翻译工具，外语视频与会议实时生成悬浮字幕")](https://www.ahhhhfs.com/wp-content/uploads/2026/05/AirTranslate%EF%BC%9AMac%E7%B3%BB%E7%BB%9F%E9%9F%B3%E9%A2%91%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7%EF%BC%8C%E5%A4%96%E8%AF%AD%E8%A7%86%E9%A2%91%E4%B8%8E%E4%BC%9A%E8%AE%AE%E5%AE%9E%E6%97%B6%E7%94%9F%E6%88%90%E6%82%AC%E6%B5%AE%E5%AD%97%E5%B9%95-%E6%A8%A1%E5%BC%8F%E6%AF%94%E8%BE%83.jpg)

**开 GPT 模式前，有几件事要知道：**  
默认 Apple 模式不需要 OpenAI API Key。只有开启 GPT 模式时才需要填入。你的 API Key 会存入 macOS 的 Keychain（钥匙串），不会被硬编码进应用或随发布包分发，但使用 GPT 模式时，仍然会产生 OpenAI API 调用成本和对应的数据流向。

## 真正门槛在哪？旧 Mac 用户要先看这里

AirTranslate 的体验看起来很省事，但它并不是“装上就万事大吉”的工具。旧版 macOS、权限设置和语言包支持，都会影响实际使用效果。

**避坑指南：**

1\. **系统限制严格：** AirTranslate运行要求是 macOS 26.0 或更高版本，依赖较新的底层抓取框架，旧版 macOS 用户不建议盲目折腾。

2\. **第一次的权限配置：** 初次运行需要在系统设置里授予“屏幕录制”“系统音频录制”和“语音识别”等权限。这里的“屏幕录制”主要是 ScreenCaptureKit 捕获系统音频所需，官方说明中也提到它不会把屏幕画面保存成录制文件。

3\. **翻译准度：** 实时转写的准确率依然受音频质量、语速影响；Apple 模式的翻译质量只能说“解决温饱”，不能指望它字字精准。

## 哪些 Mac 用户更适合把它留下来？

AirTranslate 更适合那些经常在 Mac 上接触外语音频的人。比如看海外开发教程、听英文播客、参加跨国会议，或者临时遇到一段没有字幕的视频。它不一定是每天都要打开的工具，但真遇到听不懂、没字幕、又不想折腾虚拟声卡的时候，放在工具箱里会比较省心。

偶尔用一下，先从 Apple 模式开始就够了，成本低，也不用先准备 OpenAI API Key。如果你经常处理外语会议、课程或长视频，再考虑接入 GPT 模式，用 API 成本换更好的转写和翻译体验。只是涉及公司会议、客户资料或敏感内容时，还是要先想清楚音频会经过哪里，别只看翻译效果。

## AirTranslate 常见问题

**Q：它能翻译哪些语言？**  
不固定。Apple 模式支持的语言取决于你 Mac 系统内下载的语言包；GPT 模式则取决于 OpenAI 模型本身支持的语言范围。

**Q：它能保存转写记录吗？**  
可以。它支持将转写记录以普通的.txt 文件格式保存在本机硬盘，方便会后整理纪要。

**Q：AirTranslate 是否必须使用 OpenAI？**  
不必须。默认 Apple 模式主要调用 macOS 自带的语音识别与翻译框架；只有开启 GPT 模式或 OpenAI 翻译模型时，才需要填写自己的 OpenAI API Key。

**Q：转写记录会保存在哪里？**  
AirTranslate 支持转写历史库，保存后的记录会以普通.txt 文件存放在 Mac 本机的 Application Support 目录中，并可在应用内查看、编辑或删除。涉及会议、客户资料等内容时，仍建议按自己的数据管理要求定期清理。

---

## AirTranslate 项目主页与源码入口

[🌐 官网直达](https://himomohi.github.io/AirTranslate/)

[项目介绍与编译发布版下载](https://himomohi.github.io/AirTranslate/)

  
[🐙 GitHub 项目主页

查看源码与部署文档 (Apache-2.0 开源协议)

](https://github.com/himomohi/AirTranslate)

**免责声明：** 本文基于项目公开页面与文档整理，偏向功能解读与选型判断。项目基于 Apache-2.0 协议开源，关于第三方 API 的使用成本、数据流向边界及 macOS 系统版本的具体兼容性（如要求 macOS 26.0+），请以项目仓库官方说明与你当前的设备环境为准。

本文由（ahhhhfs.com）根据项目官网、官方文档及公开资料整理。工具的功能、价格、授权与服务条款可能调整，请以官方最新说明为准。合理引用请注明来源并保留本文链接；如需全文转载，或发现内容错误、版权及授权问题，可通过 feedback#abskoop.com「联系我们」反馈（请将 # 替换为 @）。