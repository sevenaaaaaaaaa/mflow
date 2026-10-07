---
title: 微信视频号下载助手（WX Channel Downloader）：简洁易用的微信视频号本地下载与管理工具 - A姐分享
source: https://www.ahhhhfs.com/77378/
author:
  - "[[ahhhhfs]]"
published: 2025-11-11
created: 2025-12-08
description: WX Channel Downloader 是一款基于 Go 与 SunnyNet 的本地 HTTP 代理工具，用于拦截微信视频号网页流量并注入操作面板，实现零配置启动、单个/批量下载、智能去重、分片上传与断点续传，多格式导出与CSV记录，支持合法场景下处理受保护内容。
tags:
  - clippings
profileName: NowX
postId: "3437"
postType: post
categories:
  - 69

tags: [视频, 下载, 工具]---

## 微信视频号下载助手（WX Channel Downloader）简介

WX Channel Downloader（微信视频号下载助手）通过在本地启动一个 HTTP 代理，拦截微信浏览器与视频号页面的流量并注入脚本，实现视频信息采集与本地保存。该工具主打“零配置、快速上手”，适合需要批量管理或备份自己或经授权视频内容的个人与团队。



### 核心功能

- **简单安装** ：下载即用，无需复杂配置，数分钟内完成部署。
- **自动注入** ：在视频号页面自动注入操作面板，无需手动脚本。
- **批量下载** ：支持单个、批量与全量选择下载。
- **智能去重** ：自动识别重复资源，节省带宽与存储。
- **分片上传** ：大文件分片并支持 **断点续传** ，提升稳定性。
- **受保护内容处理** ：在 **获得合法授权** 的前提下，可处理加密视频。
- **多格式导出** ：支持将视频链接导出为 **TXT / JSON / Markdown** 。
- **下载记录** ：自动将下载信息记录至 **CSV** ，便于检索与归档。
- **文件组织** ：按 **作者** 自动分类保存视频文件。
- **日志系统** ：支持文件大小滚动，定位问题更直接。

### 系统要求

- 操作系统： **Windows 10+**
- Go 环境： **1.23+** （仅在需从源码编译时）
- 浏览器： **微信浏览器**
- 网络：可正常访问微信视频号网站
- 权限：建议以 **管理员** 身份运行（便于证书自动安装）

### 安装与启动

**方式一：使用预编译版本（推荐）**

1. 前往 **GitHub Releases** 下载适配系统的最新版本（下载地址： [夸克](https://pan.quark.cn/s/4c3910066708 "微信视频号下载助手（WX Channel Downloader）：简洁易用的微信视频号本地下载与管理工具") ）
2. 解压至任意目录
3. 运行可执行文件

**方式二：从源码编译**

```bash
git clone https://github.com/nobiyou/wx_channel.git
cd wx_channel
# 基本编译
go build -o wx_channel.exe
# 优化体积（推荐）
go build -ldflags="-s -w" -o wx_channel_mini.exe
```

**快速开始**

```bash
# Windows 启动
wx_channel.exe
```
1. 在浏览器设置 **HTTP 代理：127.0.0.1:2025** （或你指定的端口），推荐使用 **SwitchyOmega** 配置。
2. 首次运行自动尝试安装根证书；若失败，手动安装 `downloads/SunnyRoot.cer` ，完成后重新打开视频号页面。
3. 进入微信视频号页面，使用已注入的前端面板进行 **单个/批量/选择** 下载。

### 命令行参数

```bash
wx_channel.exe --help                 # 帮助
wx_channel.exe -v, --version          # 版本信息
wx_channel.exe -p, --port <端口>      # 指定代理端口（默认 2025）
wx_channel.exe --uninstall            # 卸载根证书
```

### 环境变量示例

```bash
# 代理端口
WX_CHANNEL_PORT=2025
# 下载目录
WX_CHANNEL_DOWNLOADS_DIR=downloads
# 安全配置
WX_CHANNEL_TOKEN=your_secret_token
WX_CHANNEL_ALLOWED_ORIGINS=https://example.com
# 日志配置
WX_CHANNEL_LOG_FILE=logs/wx_channel.log
WX_CHANNEL_LOG_MAX_MB=5
# 并发配置
WX_CHANNEL_UPLOAD_CHUNK_CONCURRENCY=4
WX_CHANNEL_DOWNLOAD_CONCURRENCY=2
```

### 工作原理

- **代理拦截** ：启动本地 HTTP 代理服务器，拦截微信浏览器流量。
- **脚本注入** ：在视频号页面自动注入 JavaScript 操作面板。
- **信息采集** ：采集视频信息并通过 API 与本地服务交互。
- **文件保存** ：本地服务接收并保存至指定目录，按作者分类。
- **记录管理** ：下载记录自动写入 **CSV** ，便于检索与统计。

## 微信视频号下载助手（WX Channel Downloader）开源地址

下载地址： [夸克](https://pan.quark.cn/s/4c3910066708 "微信视频号下载助手（WX Channel Downloader）：简洁易用的微信视频号本地下载与管理工具")

GitHub地址： [https://github.com/nobiyou/wx\_channel](https://github.com/nobiyou/wx_channel "GitHub：nobiyou/wx_channel")
