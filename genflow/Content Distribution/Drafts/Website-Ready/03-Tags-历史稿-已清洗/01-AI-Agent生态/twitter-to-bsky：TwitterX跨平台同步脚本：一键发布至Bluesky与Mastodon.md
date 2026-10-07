---
title: "twitter-to-bsky：TwitterX跨平台同步脚本：一键发布至Bluesky与Mastodon"
slug: twitter-to-bskytwitterx跨平台同步脚本一键发布至bluesky与mastodon
date: 2026-08-04
updated: 2026-08-04
tags: [AI, 开源, 免费, 浏览器, 视频]
categories: [软件应用]
summary: "2025-12-24 油猴脚本 软件 0 0 [0]("
focus_keyword: "twitter-to-bsky"
source: ""
status: draft
---

## twitter-to-bsky：Twitter/X跨平台同步脚本：一键发布至Bluesky与Mastodon

2025-12-24 油猴脚本 软件 0 0 0

- 详情介绍
- 常见问题
- 评论建议

## Twitter一键同步Bluesky与Mastodon的实用工具

**twitter-to-bsky** 是一款基于浏览器的跨平台内容同步脚本，帮助用户在 Twitter/X 网页端发布内容的同时，自动同步至去中心化社交平台 **Bluesky** 和 **Mastodon** 。该工具采用 userscript 编写，可在桌面浏览器（如 Chrome、Firefox、Edge）中通过 **Tampermonkey** 或 **Violentmonkey** 插件运行。


### 为什么值得使用跨平台同步脚本？

虽然社交内容跨发通常并不被推荐，但在平台迁移初期，这种方式可以有效保持内容同步，避免用户在迁移至Bluesky或Mastodon后失联。该脚本非常适合转发新闻、博客等通用内容，而不适用于私信、回复、@提及等特定于Twitter的互动。

## 支持的内容类型

- 纯文本推文
- 附带一张或多张图片的推文
- 包含链接预览卡的推文

*注意：Bluesky 目前尚不支持视频与GIF格式。*

## 安装与设置说明

### 第一步：安装浏览器插件

可选择以下任意一个插件：

- [Tampermonkey](https://www.tampermonkey.net/)
- [Violentmonkey](https://violentmonkey.github.io/)

### 第二步：安装 userscript

访问 [twitter-to-bsky](https://github.com/59de44955ebd/twitter-to-bsky/raw/main/twitter-to-bsky.user.js) 并加载脚本。

加载后，在Twitter网页界面将新增以下组件：

- 导航栏新增“交叉发布”按钮，可填写你的 Mastodon 与 Bluesky 登录信息
- 推文编辑器中新增“Mastodon”和“Bluesky”勾选框，勾选后将同步发布至对应平台

### Mastodon设置

- **实例地址** ：如 `https://mastodon.social`
- **Access Token** ：前往 Mastodon 设置 → Development → 创建新应用，获取Token填写

### Bluesky设置

- **账号 Handle** ：完整账号格式，如 `@example.bsky.social`
- **App 密码** ：非登录密码。请前往 Bluesky 设置 → 高级 → App Passwords，生成并填写


## 兼容性与已知限制

该脚本在 **Chrome + Violentmonkey** 组合下表现良好。
在 **Firefox + Violentmonkey** 环境中可能会因内容安全策略（CSP）限制而间歇失效，建议Firefox用户优先使用Tampermonkey插件。

GitHub地址： [https://github.com/59de44955ebd/twitter-to-bsky](https://github.com/59de44955ebd/twitter-to-bsky)

脚本地址： [https://github.com/59de44955ebd/twitter-to-bsky/raw/main/twitter-to-bsky.user.js](https://github.com/59de44955ebd/twitter-to-bsky/raw/main/twitter-to-bsky.user.js)

本文链接：

### 相关

MultiPost开源多平台发布工具：一键同步知乎/微博/小红书等全平台（免费浏览器扩展）

自媒体运营神器：AutoX 实现视频一键搬家与多平台同步发布

COSE：一键多平台同步发布工具，一次编辑，多平台同步发布

1. 转载请保留原文链接谢谢！
- 本站所有资源文章出自互联网收集整理，本站不参与制作，如果侵犯了您的合法权益，请联系本站我们会及时删除。
- 本站发布资源来源于互联网，可能存在水印或者引流等信息，请用户擦亮眼睛自行鉴别，做一个有主见和判断力的用户。
- 本站资源仅供研究、学习交流之用，若使用商业用途，请购买正版授权，否则产生的一切后果将由下载用户自行承担。
- 联系方式（#替换成@）：feedback#abskoop.com[上一篇

Galaxy Downloader：B站/抖音/小红书通用媒体下载器（视频+音频+图文笔记）

]( "Galaxy Downloader：B站/抖音/小红书通用媒体下载器（视频+音频+图文笔记）")[下一篇

短视频直播8天线下系统课，零基础入门，内容涵盖全面，账号运营，拍摄剪辑，直播电商

]( "短视频直播8天线下系统课，零基础入门，内容涵盖全面，账号运营，拍摄剪辑，直播电商")
