---
profileName: NowX
postId: "3451"
postType: post
categories:
  - 69

tags: [视频]---
## YouTube 到 B站的全自动搬运神器：YTB2BILI 视频处理系统

2025-11-23 [AI工具](https://www.ahhhhfs.com/funny_site/ai-tool/) [趣站](https://www.ahhhhfs.com/funny_site/) 4 0 [0](https://www.ahhhhfs.com/77743/#comments)

- [详情介绍](https://www.ahhhhfs.com/77743/#pills-details)
- [常见问题](https://www.ahhhhfs.com/77743/#pills-faq)
- [评论建议](https://www.ahhhhfs.com/77743/#pills-comments)

## YTB2BILI：一站式YouTube到B站自动搬运系统

YTB2BILI 是一款开源且功能完整的视频自动处理工具，专为内容创作者、运营团队和二次剪辑搬运者打造。它支持从 YouTube 等平台自动下载视频，生成字幕、翻译内容、提取封面和元数据，并通过智能调度定时上传到 Bilibili，全流程无需人工干预，大幅节省操作成本。


### 🎬 视频处理全链路自动化

系统基于 Whisper AI、DeepSeek AI、百度翻译等先进技术，实现高精度视频解析与语言处理。核心处理环节包括：

- **字幕生成** ：Whisper AI 自动识别并生成精准字幕
- **封面提取** ：自动获取高清封面并上传至云端
- **多语翻译** ：支持百度和 DeepSeek AI，实现中英互译及多语种覆盖
- **元数据构建** ：通过AI分析自动生成符合B站规范的标题、描述与标签

### ⏱️ 智能调度与定时上传

YTB2BILI 内置定时策略，自动按照频率发布内容：

- 每小时上传一条已完成处理的视频
- 自动延时上传字幕，保持节奏与内容同步
- 可视化控制面板，支持任务追踪与失败重试

### 🖥️ 后台管理系统

内置可视化管理面板，帮助用户轻松掌控每一个处理节点：

- 实时监控视频处理进度与状态
- 失败步骤可手动重试
- 所有文件（视频、封面、字幕）可一键查看与下载

### 🔐 Bilibili 登录集成

系统支持 B站扫码登录与自动状态检测，无需频繁手动验证：

- 快速扫码登录
- 自动生成二维码并检测登录状态
- 登录信息自动持久化，减少反复登录

### 🧠 技术架构

后端采用 Go + Gin 框架，结合 GORM 多数据库支持，配合腾讯云COS实现大文件存储与上传。前端基于 Next.js 与 React 18，结合 Tailwind CSS 打造响应式界面。

核心依赖包括 yt-dlp、Whisper、DeepSeek AI 与 B站官方 SDK，确保下载、识别、翻译与上传全过程稳定高效。

---

下载地址： [网盘](https://pan.quark.cn/s/d2558e35cf09)

访问 GitHub 项目： [https://github.com/difyz9/ytb2bili](https://github.com/difyz9/ytb2bili "YTB2BILI 地址")