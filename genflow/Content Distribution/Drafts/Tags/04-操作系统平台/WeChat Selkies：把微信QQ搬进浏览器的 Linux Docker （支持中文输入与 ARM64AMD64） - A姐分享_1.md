---
title: "WeChat Selkies：把微信/QQ搬进浏览器的 Linux Docker （支持中文输入与 ARM64/AMD64） - A姐分享"
source: "https://www.ahhhhfs.com/76835/"
author:
  - "[[ahhhhfs]]"
published: 2025-10-26
created: 2025-11-07
description: "WeChat Selkies 将官方微信/QQ 的 Linux 客户端封装进 Docker 容器，通过 Selkies 的 WebRTC 技术把界面投送到浏览器。用户无需在本机安装微信/QQ，即可在 Chrome、Firefox、Safari 等现代浏览器中直接使用，适合服务器端部署与远程办公场景。 开源地址：https://github.com/nickrunning/wechat-selkies"
tags:
  - "浏览器"
  - "Docker"
---
## WeChat Selkies：把微信/QQ搬进浏览器的 Linux Docker （支持中文输入与 ARM64/AMD64）

2025-10-26 [GitHub项目](https://www.ahhhhfs.com/funny_site/github%e9%a1%b9%e7%9b%ae/) [趣站](https://www.ahhhhfs.com/funny_site/) 1 0 [0](https://www.ahhhhfs.com/76835/#comments)

- [详情介绍](https://www.ahhhhfs.com/76835/#pills-details)
- [常见问题](https://www.ahhhhfs.com/76835/#pills-faq)
- [评论建议](https://www.ahhhhfs.com/76835/#pills-comments)

## WeChat Selkies概览

**WeChat Selkies** 将官方微信/QQ 的 Linux 客户端封装进 Docker 容器，通过 **Selkies 的 WebRTC** 技术把界面投送到浏览器。用户无需在本机安装微信/QQ，即可在 Chrome、Firefox、Safari 等现代浏览器中直接使用，适合服务器端部署与远程办公场景。  
开源地址：https://github.com/nickrunning/wechat-selkies

[![WeChat Selkies：把微信/QQ搬进浏览器的 Linux Docker （支持中文输入与 ARM64/AMD64）](https://www.ahhhhfs.com/wp-content/uploads/2025/10/WeChat-Selkies%EF%BC%9A%E6%8A%8A%E5%BE%AE%E4%BF%A1-QQ%E6%90%AC%E8%BF%9B%E6%B5%8F%E8%A7%88%E5%99%A8%E7%9A%84-Linux-Docker-%EF%BC%88%E6%94%AF%E6%8C%81%E4%B8%AD%E6%96%87%E8%BE%93%E5%85%A5%E4%B8%8E-ARM64-AMD64%EF%BC%89.jpg "WeChat Selkies：把微信/QQ搬进浏览器的 Linux Docker （支持中文输入与 ARM64/AMD64） 1")](https://www.ahhhhfs.com/wp-content/uploads/2025/10/WeChat-Selkies%EF%BC%9A%E6%8A%8A%E5%BE%AE%E4%BF%A1-QQ%E6%90%AC%E8%BF%9B%E6%B5%8F%E8%A7%88%E5%99%A8%E7%9A%84-Linux-Docker-%EF%BC%88%E6%94%AF%E6%8C%81%E4%B8%AD%E6%96%87%E8%BE%93%E5%85%A5%E4%B8%8E-ARM64-AMD64%EF%BC%89.jpg)

## 核心特性

- **浏览器直达** ：打开网页即可用微信/QQ，无需本地安装。
- **容器化部署** ：Docker 一键拉起，环境隔离更可控。
- **数据持久化** ：配置与聊天记录可落盘保存。
- **中文体验完善** ：内置中文字体，本地中文输入法可用。
- **图片复制与文件传输** ：侧边栏面板开启后即可完成粘贴与传输。
- **多架构兼容** ：原生支持 **AMD64** 与 **ARM64** 。
- **可选硬件加速** ：按需启用 **GPU 加速** 。
- **窗口切换器** ：左上角新增悬浮窗，便于切换后台窗口。
- **自动启动** ：可配置开机自启微信与 QQ（可选）。

## 环境与访问

### 环境要求

- Docker
- Docker Compose
- 支持 WebRTC 的现代浏览器（如 Chrome、Firefox、Safari）

### 典型使用场景

- 轻量化企业或个人的 **远程办公与服务器常驻登录**
- 多终端随时接入的 **无客户端运维环境**
- 需要 **ARM 服务器/树莓派** 等场景的跨架构使用

## 升级与故障排查

升级后若出现功能缺失，可先清空本地挂载目录中的 `openbox` 目录（示例：`./config/.config/openbox` ），再重启容器以恢复组件加载。

## WeChat Selkies项目链接

GitHub地址： [https://github.com/nickrunning/wechat-selkies](https://github.com/nickrunning/wechat-selkies "WeChat Selkies GitHub地址")

本文链接： [https://www.ahhhhfs.com/76835/](https://www.ahhhhfs.com/76835/ "WeChat Selkies：把微信/QQ搬进浏览器的 Linux Docker （支持中文输入与 ARM64/AMD64）")

### 相关

[Wechat Article Exporter：微信公众号文章批量下载工具 支持阅读量/评论抓取与HTML样式100%还原](https://www.ahhhhfs.com/74911/ "Wechat Article Exporter：微信公众号文章批量下载工具 支持阅读量/评论抓取与HTML样式100%还原")

[PairDrop：跨平台 P2P 文件秒传工具，无需注册、一键上手](https://www.ahhhhfs.com/72805/ "PairDrop：跨平台 P2P 文件秒传工具，无需注册、一键上手")

[FileSync：开源·端到端加密的实时文件传输（WebRTC/P2P｜免注册｜一对多分发）](https://www.ahhhhfs.com/75460/ "FileSync：开源·端到端加密的实时文件传输（WebRTC/P2P｜免注册｜一对多分发）")

1. 转载请保留原文链接谢谢！
- 本站所有资源文章出自互联网收集整理，本站不参与制作，如果侵犯了您的合法权益，请联系本站我们会及时删除。
- 本站发布资源来源于互联网，可能存在水印或者引流等信息，请用户擦亮眼睛自行鉴别，做一个有主见和判断力的用户。
- 本站资源仅供研究、学习交流之用，若使用商业用途，请购买正版授权，否则产生的一切后果将由下载用户自行承担。
- 联系方式（#替换成@）：feedback#abskoop.com[上一篇

Type Words：开源英语单词与文章练习工具（智能记忆曲线、跟打+默写、免费无广告）

](https://www.ahhhhfs.com/76829/ "Type Words：开源英语单词与文章练习工具（智能记忆曲线、跟打+默写、免费无广告）")[下一篇

电商财税合规线下课，适合老板+财务，教你规避涉税风险，实现低成本合规经营

](https://www.ahhhhfs.com/76840/ "电商财税合规线下课，适合老板+财务，教你规避涉税风险，实现低成本合规经营")