---
title: "PlainApp：开源 AirDroid 替代，浏览器管理安卓手机"
slug: plainapp
date: 2026-06-15
updated: 2026-06-15
tags: [手机管理, AirDroid替代, 开源]
categories: [软件应用]
summary: "PlainApp：开源 AirDroid 替代，浏览器管理安卓手机。平台：Android/Web。"
focus_keyword: "PlainApp"
source: https://github.com/plainhub/plain-app
author: ""
status: draft
---

# PlainApp：开源 AirDroid 替代，浏览器管理安卓手机

> 5.6k+ stars | Kotlin | AGPL-3.0 | 100% 本地，数据不离开你的网络

## 这是什么

## 这是什么

PlainApp 是一个开源 Android 应用，安装后将你的手机变成一个可通过局域网内任意浏览器访问的自托管管理中枢。无需注册账号、无需云端中转、无需付费订阅——你可以在电脑浏览器上直接管理手机文件、查看短信和通话记录、浏览相册、镜像屏幕，甚至从桌面发送短信。

PlainApp 的核心定位是 AirDroid 的开源替代方案。大多数手机管理工具要么将数据经过自己的服务器中转，要么将高级功能锁在付费订阅后面，甚至塞满广告。PlainApp 坚持 100% 本地运行，所有流量通过 TLS + XChaCha20-Poly1305 端到端加密，代码完全开源（AGPL-3.0）。

除了远程管理，PlainApp 本身也是一个功能丰富的独立应用，内置 Markdown 笔记、RSS 阅读器、音视频播放器、DLNA/Chromecast 投屏、P2P 聊天与文件分享、番茄钟甚至环境噪音检测。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 经常需要在电脑上操作手机的用户 | ✅ 推荐 | 浏览器访问文件、短信、相册、通知，无需安装任何电脑端软件，支持 PWA 固定到桌面 |
| 注重隐私、不愿数据上云的用户 | ✅ 推荐 | 所有数据留在局域网，端到端加密，代码可审计，无任何第三方服务器中转 |
| AirDroid 免费版用户感到受限 | ✅ 推荐 | 完全免费无广告，不限制设备数量，提供 AirDroid 付费版才有的屏幕镜像和通知同步 |
| 仅需简单文件传输的用户 | ⚠️ 酌情 | 功能过于全面，如果只传文件，[[../04-操作系统平台/Blip：免费跨平台文件传输工具]] 或 KDE Connect 更轻量 |
| iOS 用户 | ❌ 不推荐 | 仅支持 Android 9.0+，iOS 版功能有限 |

## 安装

从 Google Play 或 F-Droid 安装 PlainApp（要求 Android 9.0+）：

- [Google Play](https://play.google.com/store/apps/details?id=com.ismartcoding.plain)
- [F-Droid](https://f-droid.org/packages/com.ismartcoding.plain/)
- [GitHub Releases](https://github.com/plainhub/plain-app/releases/latest)

安装后，确保手机和电脑在同一 Wi-Fi 网络下：

1. 打开 PlainApp，首页会显示一个局域网地址（如 `https://192.168.1.100:8080`）。
2. 在电脑浏览器中输入该地址，完成设备配对。
3. 首次访问时浏览器会提示证书警告（因为用的是自签名证书），点击"继续访问"即可。

如需从源码构建：

```bash
git clone https://github.com/plainhub/plain-app
# 使用 Android Studio 打开项目
# 生成 release.jks 并创建 keystore.properties
# 然后 ./gradlew assembleRelease
```

## 核心用法

1. **文件管理**：在浏览器中浏览手机内部存储、SD 卡和 USB OTG 设备，支持上传、下载、重命名、删除操作。
2. **短信与通话**：在桌面浏览器中阅读短信和通话记录，直接用电脑键盘编写和发送短信。
3. **屏幕镜像**：实时将手机屏幕投射到浏览器，支持音频传输和远程控制。
4. **通知同步**：手机通知实时镜像到浏览器，不遗漏任何消息。
5. **内置应用**：Markdown 笔记、RSS 阅读器、音视频播放器（支持播放列表）、DLNA/Chromecast 投屏、P2P 聊天与文件分享、番茄钟、噪音检测。
6. **PWA 支持**：在 Chrome/Edge 中可将 PlainApp 网页"安装"到桌面，像原生应用一样使用。

## 注意事项与风险

- **必须在同一局域网**：手机和电脑需连接同一 Wi-Fi。不支持远程/蜂窝网络访问（这是隐私设计，而非功能缺失）。
- **自签名证书**：首次通过浏览器访问时会提示安全警告，需手动信任。这在局域网内是安全的，但不要在公共 Wi-Fi 上使用。
- **后台保活**：部分 Android 厂商（如华为/小米）会激进杀后台，可能导致服务中断。建议将 PlainApp 加入电池白名单。
- **代理/VPN 冲突**：如果手机开启了 VPN，局域网地址可能无法访问，需要关闭 VPN 或配置分流规则。
- **Android 9.0+ 要求**：较老设备无法运行。

## 与你现有工具的关系

- 与 [[../03-效率生产力/UniClipboard：免账号开源跨设备剪贴板同步]] 互补：PlainApp 负责文件/短信/通知管理，UniClipboard 专注跨设备剪贴板同步。
- 与 [[../04-操作系统平台/Blip：免费跨平台文件传输工具]] 的场景差异：Blip 适合单次快速传文件，PlainApp 适合持续的手机管理需求。
- 与 [[../04-操作系统平台/Shizuku 通话录音：免 Root Android 录音工具]] 配合：两者可同时在 Android 上运行，PlainApp 提供远程管理，Shizuku 提供通话录音能力。
- 与 [[../01-AI-Agent生态/Lobe Chat：开源高颜值ChatGPT客户端]] 的思路一致：都是追求"数据留在本地、能力不输商业版"的开源替代方案。

## FAQ

### Q: PlainApp 和 AirDroid 的核心区别是什么？
A: PlainApp 完全开源、100% 本地、永久免费无广告。AirDroid 有免费版但限制设备数量和数据传输额度，且部分功能需要付费订阅，数据可能经过其服务器中转。

### Q: 离开家还能用吗？
A: 默认不支持远程访问，这是刻意为之的隐私设计。如果确实需要，可以自行配置 VPN（如 WireGuard）连接到家庭网络后再访问。

### Q: 手机上需要一直开着 PlainApp 吗？
A: 是的，需要在手机后台运行。建议开启通知栏常驻服务和电池优化白名单来保持连接。

## 相关链接

- 官方网站：https://plainapp.app
- 文档：https://plainapp.app/docs
- GitHub：https://github.com/plainhub/plain-app
- Discord：https://discord.gg/RQWcS6DEEe
- 来源：https://www.ahhhhfs.com/81216/
