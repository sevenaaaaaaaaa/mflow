---
title: "ClashMac：基于 mihomo 内核的轻量级 macOS 菜单栏客户端（SwiftUI 原生） - A姐分享"
source: "https://www.ahhhhfs.com/78012/"
author:
  - "[[ahhhhfs]]"
published: 2025-12-03
created: 2025-12-08
description: "ClashMac 是一款基于 mihomo 内核的轻量级 macOS 菜单栏客户端，SwiftUI 原生开发。支持一键接管系统代理与增强模式、免密特权助手、毫秒级 SSE 流量监控、可视化面板与 Web Dashboard，适配 Apple Silicon 与 Intel 架构。"
tags:
  - "Mac"
  - "macOS"
  - "UI"
---
## ClashMac：基于 mihomo 内核的轻量级 macOS 菜单栏客户端（SwiftUI 原生）

2025-12-03 [Mac](https://www.ahhhhfs.com/software/mac/) [软件](https://www.ahhhhfs.com/software/) 1 0 [0](https://www.ahhhhfs.com/78012/#comments)

- [详情介绍](https://www.ahhhhfs.com/78012/#pills-details)
- [常见问题](https://www.ahhhhfs.com/78012/#pills-faq)
- [评论建议](https://www.ahhhhfs.com/78012/#pills-comments)

## ClashMac概览

ClashMac 是基于 **mihomo** 内核打造的 macOS 菜单栏客户端，采用 **SwiftUI** 原生技术，界面与交互风格与系统一致。聚焦“轻量与高效”，提供系统代理一键接管、增强模式、实时流量与资源占用可视化，并集成 Web Dashboard 便于快速调试与查看状态。

[![ClashMac：基于 mihomo 内核的轻量级 macOS 菜单栏客户端（SwiftUI 原生）](https://www.ahhhhfs.com/wp-content/uploads/2025/12/ClashMac%EF%BC%9A%E5%9F%BA%E4%BA%8E-mihomo-%E5%86%85%E6%A0%B8%E7%9A%84%E8%BD%BB%E9%87%8F%E7%BA%A7-macOS-%E8%8F%9C%E5%8D%95%E6%A0%8F%E5%AE%A2%E6%88%B7%E7%AB%AF%EF%BC%88SwiftUI-%E5%8E%9F%E7%94%9F%EF%BC%89.jpg "ClashMac：基于 mihomo 内核的轻量级 macOS 菜单栏客户端（SwiftUI 原生） 1")](https://www.ahhhhfs.com/wp-content/uploads/2025/12/ClashMac%EF%BC%9A%E5%9F%BA%E4%BA%8E-mihomo-%E5%86%85%E6%A0%B8%E7%9A%84%E8%BD%BB%E9%87%8F%E7%BA%A7-macOS-%E8%8F%9C%E5%8D%95%E6%A0%8F%E5%AE%A2%E6%88%B7%E7%AB%AF%EF%BC%88SwiftUI-%E5%8E%9F%E7%94%9F%EF%BC%89.jpg)

### 核心特性

- **原生体验** ：SwiftUI 开发，视觉与交互贴合 macOS。
- **轻量高效** ：常驻菜单栏，资源占用低。
- **网络接管** ：一键开启/关闭系统代理与增强模式。
- **特权助手** ：免密管理系统代理与内核，减少重复授权。
- **实时监控** ：基于 **SSE 推送** 的毫秒级上/下行速率刷新。
- **可视化面板** ：查看流量统计、连接数、内存占用等关键指标。
- **Web Dashboard** ：集成在线控制面板入口，便于规则与连接状态管理。

### 下载与安装

**获取安装包** （ [前往 GitHub Releases](https://github.com/666OS/ClashMac/releases) / [国内网盘](https://pan.quark.cn/s/89962644134c "ClashMac：基于 mihomo 内核的轻量级 macOS 菜单栏客户端") ）：

- Apple Silicon（M1/M2/M3/M4）： `ClashMac-v*-macos-arm64.zip`
- Intel Mac： `ClashMac-v*-macos-x86_64.zip`

**安装步骤**

1. 解压下载的 zip。
2. 将 `ClashMac.app` 拖入「应用程序」文件夹。
3. 首次打开如遇安全提示，右键 App 图标选择「打开」。

**如何确认芯片类型**  
点击屏幕左上角苹果标志 →「关于本机」查看“芯片”信息。

### Gatekeeper 拦截与处理

应用未经过 Apple 公证时，macOS 可能阻止直接打开。可按需选择以下方式：

**方式一：在系统设置中允许**

1. 尝试打开 ClashMac，出现安全警告时点击「完成」。
2. 前往「系统设置 → 隐私与安全性」。
3. 在提示“ClashMac 已被阻止打开”处点击「仍要打开」，在弹窗中再次选择「仍要打开」。

**方式二：终端解除限制（清除扩展属性）**

```
xattr -cr /Applications/ClashMac.app
```

**方式三：移除隔离属性**

```
xattr -d com.apple.quarantine /Applications/ClashMac.app
```

### 可视化与监控

- **流量/连接/内存** ：在菜单栏面板内即时查看关键信息。
- **Web Dashboard** ：从应用内直达控制面板，查看规则、节点状态与连接详情。

### 配置兼容

如需快速验证，参阅项目提供的 **测试专用配置** 。实际使用时请根据自身场景与合规需求加载相应配置文件。

### 使用范围与合规说明

ClashMac 为通用网络调试与流量管理工具，不内置节点与规则。请在合法合规场景下使用，遵守当地法律法规与平台政策；涉及第三方服务的内容与费用由用户自行承担。

### 适配人群

- 需要在 macOS 上进行网络调试与流量观察的开发者与进阶用户。
- 偏好菜单栏常驻、轻量占用与原生交互的 macOS 用户。
- 需要可视化面板与 Dashboard 协作的团队成员。

## ClashMac开源地址

下载地址： [网盘](https://pan.quark.cn/s/89962644134c "ClashMac：基于 mihomo 内核的轻量级 macOS 菜单栏客户端")

GitHub地址： [`https://github.com/666OS/ClashMac`](https://github.com/666OS/ClashMac "ClashMac 开源地址")

本文链接： [https://www.ahhhhfs.com/78012/](https://www.ahhhhfs.com/78012/ "ClashMac：基于 mihomo 内核的轻量级 macOS 菜单栏客户端（SwiftUI 原生）")

### 相关

[光晕带：让 Mac 菜单栏流光溢彩的轻量级美化神器](https://www.ahhhhfs.com/73772/ "光晕带：让 Mac 菜单栏流光溢彩的轻量级美化神器")

[Platypus：将命令行脚本一键打包为原生 macOS 应用的开发者神器](https://www.ahhhhfs.com/76228/ "Platypus：将命令行脚本一键打包为原生 macOS 应用的开发者神器")

[Seelen UI：用可自定义 Dock 与平铺管理重塑 Windows 桌面（WebView 安全叠加、开源、支持 70+ 语言）](https://www.ahhhhfs.com/76380/ "Seelen UI：用可自定义 Dock 与平铺管理重塑 Windows 桌面（WebView 安全叠加、开源、支持 70+ 语言）")

1. 转载请保留原文链接谢谢！
- 本站所有资源文章出自互联网收集整理，本站不参与制作，如果侵犯了您的合法权益，请联系本站我们会及时删除。
- 本站发布资源来源于互联网，可能存在水印或者引流等信息，请用户擦亮眼睛自行鉴别，做一个有主见和判断力的用户。
- 本站资源仅供研究、学习交流之用，若使用商业用途，请购买正版授权，否则产生的一切后果将由下载用户自行承担。
- 联系方式（#替换成@）：feedback#abskoop.com[上一篇

Python分布式爬虫与逆向进阶实战

](https://www.ahhhhfs.com/78005/ "Python分布式爬虫与逆向进阶实战")[下一篇

SubsTracker：开源订阅管理与多渠道到期提醒系统（Cloudflare Workers 部署）

](https://www.ahhhhfs.com/78019/ "SubsTracker：开源订阅管理与多渠道到期提醒系统（Cloudflare Workers 部署）")