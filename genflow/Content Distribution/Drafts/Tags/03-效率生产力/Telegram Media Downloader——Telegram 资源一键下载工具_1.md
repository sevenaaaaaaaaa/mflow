---
profileName: NowX
postId: "3457"
postType: post
categories:
  - 69

tags: [下载, 工具]---
## Telegram Media Downloader简介

**Telegram 资源一键下载工具（Telegram Media Downloader** ）是一个基于 Dineshkarthik 项目的电报资源下载工具，用于从 Telegram 会话/私聊/频道下载媒体文件。支持跨平台部署，提供网页端查看下载进度，可通过 Bot 指令触发下载；支持下载你已加入但受下载限制的私有群资源。单文件最大支持 **2GiB** 。无论是公开频道还是已加入的私有群，都可以轻松下载被限制访问的资源。

## 核心功能

- **下载范围** ：会话 / 私聊 / 频道中的媒体。
- **媒体类型** ：音频、文档、照片、视频、video\_note、语音。
- **进度可视化** ：内置 Web 界面展示任务状态与进度。
- **Bot 交互** ：从机器人下发命令或转发消息即可下载。
- **文件上限** ：单文件最高 **2GiB** 。
- **跨平台** ：适合多种运行环境。

## 运行方式

### 方式一：机器人模式

通过 Bot 指令触发下载或转发消息到 Bot，实现自动拉取与保存。

![Code style: black](https://www.ahhhhfs.com/76407/www.w3.org/2000/svg'%20viewBox='0%200%200%200'%3E%3C/svg%3E "Telegram 资源一键下载工具：支持网页进度与Bot指令、单文件至2GiB 2")

### 方式二：一次性下载工具

作为本地/服务器上的临时工具，执行完单次下载任务即止。

![Code style: black](https://www.ahhhhfs.com/76407/www.w3.org/2000/svg'%20viewBox='0%200%200%200'%3E%3C/svg%3E "Telegram 资源一键下载工具：支持网页进度与Bot指令、单文件至2GiB 3")

## Web 界面与访问

- 默认地址：启动后在浏览器访问 `localhost:5000` 。
- 远程访问：将配置项 `web_host` 设为 `0.0.0.0` 以供外网访问。

## 环境与兼容

- **语言环境** ：Python **3.7+** 。
- **适配对象** ：音频/文档/照片/视频/video\_note/语音等常见媒体类型。

## 使用提示

- 仅在遵守 Telegram 条款与当地法律的前提下使用，确保对目标资源拥有合法访问与下载权限。

## Telegram Media Downloader如何使用

GitHub地址： [https://github.com/tangyoha/telegram\_media\_downloader](https://github.com/tangyoha/telegram_media_downloader "https://github.com/tangyoha/telegram_media_downloader")