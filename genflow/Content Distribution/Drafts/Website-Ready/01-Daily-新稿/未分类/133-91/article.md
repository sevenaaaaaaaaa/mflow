---
title: "91：个人私有视频站与多网盘302播放"
slug: 91-personal-private-video-site
date: 2026-06-02
updated: 2026-05-29
tags: [91, 私有部署, 网盘, Go, Docker, 自托管]
categories: [AI工具]
summary: nianzhibai/91 是 Go 写的个人私有视频站：对接 115、PikPak、123云盘、OneDrive、Google Drive 与本地存储，多数后端支持 302 直链省带宽，自动生成封面与预览片段，内置爬虫与短视频模式，2C2G 可跑，MIT 开源。
focus_keyword: 91 私有视频站
source: https://t.co/CeIuDkJEtB · https://github.com/nianzhibai/91
author: nianzhibai
status: draft
---

# 91：个人私有视频站与多网盘302播放

> 768+ stars | MIT | Go | 端口 9191 | 短链来源：https://t.co/CeIuDkJEtB

## 这是什么

[nianzhibai/91](https://github.com/nianzhibai/91)（README 亦称 **nine one**）面向**个人私有部署**的 Web 视频站：把分散在多家网盘或本地的影片集中成可浏览、可在线播放的私有库，而不是公网流媒体平台。

核心方案：

- **多存储后端**：115 云盘、PikPak、123云盘、OneDrive、Google Drive、本地上传目录。
- **低带宽播放**：115 / PikPak / 123 / OneDrive 支持 **302 重定向**，播放流量走网盘 CDN，不占自建机出口带宽；Google Drive 需服务器中转，体验受机房带宽限制。
- **选片体验**：自动为视频生成**封面图**与**预览片段**；支持黑黄 / 粉白双主题、**抖音式短视频**沉浸模式。
- **内置 91 爬虫**：可抓取站点「本月最热」入库（见 README `data/spider91/` 目录）。
- **资源占用**：官方称 **2C2G** 可稳定运行，主要开销在封面与预览转码生成。

与 [[AIMedia：全自动 AI 媒体创作与多平台发布]] 等「AI 写稿 + 多平台发布」不同，91 是**自建播放与网盘聚合**，不强调内容生成。

**抓取说明（本次建档）：** `t.co/CeIuDkJEtB` 经 `curl -L` 解析为上述 GitHub 仓库；**未获取原始推文正文**（短链未经过 x.com）。正文来自 `main/README.md` 与 GitHub API；仓库页 `description` 仅「nine one」，细节以 README 为准。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 已有 115 / PikPak / 123 等网盘、想自建家庭片库 | ✅ 推荐 | 302 模式省服务器带宽 |
| 有 Linux VPS / 家用 NAS，接受 Docker 或一键脚本 | ✅ 推荐 | 提供 `install.sh` 与 Compose |
| 需要公网 UGC 平台、多用户社交 | ❌ 不推荐 | 产品设计为个人私有 |
| 无法合规使用网盘与爬虫来源内容 | ❌ 不推荐 | README 要求有权访问的内容并遵守法律 |
| 仅要本地转录 / 翻译字幕 | ⚠️ 用别的工具 | 见 [[../02-内容创作媒体/Buzz：离线 Whisper 音视频转录与翻译]] 等 |

## 安装与前置条件

- **环境**：Linux 服务器或 NAS；`curl`、`ca-certificates`；Docker（若走 Compose）。
- **网盘**：各后端 API / 凭证需在后台 `/admin` 配置（详见仓库 `backend/README.md`）。
- **合规**：仅接入你有权管理的内容；README 明确「不对外传播，仅限个人使用」。

### 方式一：一键脚本（推荐）

```bash
sudo apt update && sudo apt install -y curl ca-certificates
curl -fsSL https://raw.githubusercontent.com/nianzhibai/91/main/install.sh -o install.sh
sudo bash install.sh
```

| 地址 | 说明 |
|------|------|
| `http://<服务器IP>:9191/` | 前台 |
| `http://<服务器IP>:9191/admin` | 后台 |

安装后可用 `91` 命令（`video-site-91` 为别名）：`91 status`、`91 logs`、`91 update`、`91 restart`、`91 stop`。自定义端口：`FRONTEND_PORT=8080 sudo -E bash install.sh`。

### 方式二：Docker Compose

```yaml
services:
  video-site-91:
    image: ghcr.io/nianzhibai/91:stable
    container_name: video-site-91
    ports:
      - "9191:9191"
    volumes:
      - ./data:/opt/video-site-91/data
    restart: unless-stopped
```

```bash
docker compose pull && docker compose up -d
```

数据目录含 `config.yaml`、`video-site.db`、`previews/`、`uploads/`、`spider91/` 等（脚本部署默认在 `/opt/video-site-91/`）。

## 核心用法

### 存储与播放

1. 后台绑定网盘或配置本地目录。
2. 前台浏览带封面 / 预览的片库；按需切换主题或短视频模式。
3. 播放时确认当前后端是否走 302（Google Drive 除外，会占用服务器带宽）。

### 爬虫与本地文件

- 爬虫数据写入 `./data/spider91/`（Compose）或安装路径下对应目录。
- 本地上传保存在 `uploads/`；SQLite 元数据在 `video-site.db`。

### 运维

- 首次 502 可执行 `91 restart`。
- v0.0.2 之前旧版升级失败时，按 README 先拉新 `install.sh` 再 `sudo bash /tmp/install-91.sh update`。

## 注意事项与风险

- **法律与平台条款**：爬虫、网盘内容与所在地法律、各云盘 ToS 冲突风险由部署者自负；勿用于未授权传播。
- **敏感内容**：项目名与爬虫能力与成人向站点相关，建档与分享笔记时注意受众与平台政策。
- **凭证安全**：`config.yaml` 含管理员与网盘密钥，需限制文件权限并勿提交到公开仓库。
- **带宽**：Google Drive 播放走中转；高并发观看需评估服务器出口。
- **抓取局限**：本次未验证 `install.sh` 与镜像拉取；星标数来自 GitHub API（约 768），会随时间变化；预览图仅 README 外链，未本地化。

## 与你现有工具的关系

| 工具 | 关系 |
|------|------|
| [[../02-内容创作媒体/Buzz：离线 Whisper 音视频转录与翻译]] | 本地**转录 / 字幕导出**；91 负责**片库播放与网盘聚合**，可互补 |
| [[../02-内容创作媒体/Violin：开源视频翻译与配音 Skill]] | 视频**翻译配音**流水线；91 不提供 AI 配音 |
| [[../02-内容创作媒体/MioSub：一站式 AI 字幕生成与压制]] | 字幕压制工作流；与 91 播放层无直接集成 |
| [[../01-AI-Agent生态/ClipSketch AI：视频瞬间转手绘故事板]] | 创意分镜；与私有片库场景不同 |
| [[CyberVerse：自托管实时数字人 Agent 平台]] | 同属**自托管**基础设施思路，业务域不同（数字人 vs 视频站） |
| [[AIMedia：全自动 AI 媒体创作与多平台发布]] | 面向**公域自媒体发布**；91 面向**私有观看** |

项目致谢 [OpenList](https://github.com/OpenListTeam/OpenList)，若你使用 OpenList 做网盘挂载，可与 91 的后端选型一并评估。

## FAQ

### Q: 短链 https://t.co/CeIuDkJEtB 指向哪里？
A: 解析后为 https://github.com/nianzhibai/91；推广可能来自 X/Twitter，但本次未抓取推文原文。

### Q: 最低服务器配置？
A: README 称 2 核 2G 可稳定运行；封面与预览生成会占用 CPU/磁盘 I/O。

### Q: 和 Jellyfin / Emby 有何不同？
A: 91 强调国内网盘（115、PikPak、123 等）302 直链与内置爬虫工作流，而非通用家庭媒体服务器协议生态。

### Q: 如何更新？
A: 脚本安装用 `91 update`；Docker 用 `docker compose pull && docker compose up -d`，镜像 tag 可用 `ghcr.io/nianzhibai/91:stable` 或固定版本如 `v0.0.6`。

## 相关链接

- 官方仓库：https://github.com/nianzhibai/91
- 短链来源：https://t.co/CeIuDkJEtB
- 安装脚本：https://raw.githubusercontent.com/nianzhibai/91/main/install.sh
- 容器镜像：`ghcr.io/nianzhibai/91:stable`
- 后端文档：[backend/README.md](https://github.com/nianzhibai/91/blob/main/backend/README.md)
- 本库相关笔记：[[../02-内容创作媒体/Buzz：离线 Whisper 音视频转录与翻译]]、[[../02-内容创作媒体/Violin：开源视频翻译与配音 Skill]]、[[CyberVerse：自托管实时数字人 Agent 平台]]
