# OPC/自由职业者全栈开源工具矩阵（2026 年 6 月）

> 数据来源：GitHub 实时星数，2026-06-14 采集。按工作流阶段排列。

## 创意生产

| 环节 | 开源工具 | Stars | 许可证 | 替代谁 | GitHub |
|------|----------|-------|--------|--------|--------|
| 平面设计 | Penpot | 49.6k | MPL-2.0 | Figma | penpot/penpot |
| 白板/图表 | Excalidraw | 125k | MIT | Miro | excalidraw/excalidraw |
| 视频剪辑 | OpenCut | 55.4k | MIT | CapCut/Descript | OpenCut-app/OpenCut |
| 屏幕录制 | OBS Studio | 73.1k | GPLv2 | — | obsproject/obs-studio |
| 录屏+标注 | Screenity | 18.2k | GPLv3 | Loom | alyssaxuu/screenity |
| AI 配音 | VoxCPM | 26.1k | Apache-2.0 | ElevenLabs | OpenBMB/VoxCPM |
| 演示文稿 | Presenton | 8.2k | Apache-2.0 | Gamma | presenton/presenton |
| 演示文稿(轻量) | ALLWEONE | 2.9k | MIT | Gamma | allweonedev/presentation-ai |

## 业务管理

| 环节 | 开源工具 | Stars | 许可证 | 替代谁 | GitHub |
|------|----------|-------|--------|--------|--------|
| 工作空间 | AppFlowy | 72.3k | AGPL-3.0 | Notion | AppFlowy-IO/AppFlowy |
| 项目管理 | Plane | 50.8k | AGPL-3.0 | Linear/Jira | makeplane/plane |
| 项目管理(非技术) | Leantime | 10k | AGPL-3.0 | Basecamp | leantime/leantime |
| 数据库 | NocoDB | 63.4k | AGPL-3.0 | Airtable | nocodb/nocodb |
| CRM | Twenty | 49.8k | AGPL-3.0 | HubSpot/Salesforce | twentyhq/twenty |
| CRM(个人) | Monica | 24.8k | AGPL-3.0 | — | monicahq/monica |
| 发票+收款 | Invoice Ninja | 9.8k | Elastic-2.0 | HoneyBook/Bonsai | invoiceninja/invoiceninja |
| 合同+签名 | Oreko | 19 | AGPL-3.0 | Bonsai | orekoapp/oreko |
| 时间追踪 | solidtime | 8.7k | AGPL-3.0 | Toggl | solidtime-io/solidtime |
| 时间追踪(成熟) | Kimai | 4.7k | AGPL-3.0 | Toggl | kimai/kimai |

## 沟通+自动化

| 环节 | 开源工具 | Stars | 许可证 | 替代谁 | GitHub |
|------|----------|-------|--------|--------|--------|
| 会议预约 | Cal.com | 45.5k | MIT | Calendly | calcom/cal.com |
| 会议记录 | Meetily | 12.7k | Open Source | Fathom | Zackriya-Solutions/meetily |
| 会议转录API | Vexa | 2.2k | — | Otter.ai | Vexa-ai/vexa |
| 社媒调度 | Postiz | 27k | AGPL-3.0 | Buffer/Hootsuite | gitroomhq/postiz-app |
| 工作流自动化 | n8n | 192k | Sustainable Use | Zapier/Make | n8n-io/n8n |

## 建站+作品集

| 环节 | 开源工具 | Stars | 许可证 | 替代谁 | GitHub |
|------|----------|-------|--------|--------|--------|
| 作品集模板 | Astrofy | 1.4k | MIT | — | manuelernestog/astrofy |
| 可视化建站 | Webstudio | 8.6k | AGPL-3.0 | Framer/Webflow | webstudio-is/webstudio |

## 前 10 名按 Stars 排序

1. n8n — 192k ⭐（自动化）
2. Excalidraw — 125k ⭐（白板）
3. OBS Studio — 73.1k ⭐（录屏）
4. AppFlowy — 72.3k ⭐（工作空间）
5. NocoDB — 63.4k ⭐（数据库）
6. OpenCut — 55.4k ⭐（视频剪辑）
7. Plane — 50.8k ⭐（项目管理）
8. Penpot — 49.6k ⭐（设计）
9. Twenty CRM — 49.8k ⭐（CRM）
10. Cal.com — 45.5k ⭐（会议预约）

## 注意事项

- **OpenCut** 目前正在重写（v0.3.0），生产环境用 `opencut-classic` 分支
- **Oreko** 很新（19 stars）但功能完整：可视化报价、电子签名（E-SIGN/UETA）、Stripe Connect
- **Invoice Ninja** 的 Elastic-2.0 许可证不是 OSI 标准开源，但源可用且自托管免费
- **n8n** 的 Sustainable Use License 是 fair-code，自托管免费，商业转售需授权
- **Meetily** 用本地 Whisper 模型做转录，隐私安全但需要 GPU
- **VoxCPM** 需要 ~8GB 显存（CUDA 12+），Linux 主要目标平台
