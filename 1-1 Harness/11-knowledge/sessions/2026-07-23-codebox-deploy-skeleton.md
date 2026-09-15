---
session_date: 2026-07-23
session_topic: "Lovart MFlow codebox 部署项目骨架"
session_slug: "codebox-deploy-skeleton"
profiles_used: [profile-lovart-management]
tools_used: [codebox API, Go, deploy-to-codebox.sh]
agents: [hermes]
duration_min: 20
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 需要把 Lovart MFlow 从本地 macOS 部署到 codebox 内网平台
- codebox 是 Go 后端 + MongoDB + exec 沙箱 + 飞书 auth 的 vibecoding 平台
- 需要: Pipeline API / Router API / Hooks API / Dashboard / Skills 迁移

# Solution
**Go 项目骨架 (416 行)**:
- `cmd/server/main.go`: HTTP 服务器 (Pipeline CRUD + Router + Hooks + Exec + Dashboard)
- `start.sh`: codebox 进程管理契约 (start/stop/status)
- `go.mod`: Go 模块定义
- `deploy-to-codebox.sh`: 一键部署脚本 (7 步: 创建项目 → 目录 → Go 源码 → Python 脚本 → Hooks → Skills → 启动)

**API 端点**:
- `GET /health` — 健康检查
- `GET /api/pipeline/summary` — 汇总统计
- `GET/POST /api/pipeline/items` — CRUD
- `GET /api/pipeline/items/{id}` — 详情
- `POST /api/pipeline/next` — 建议下一个
- `POST /api/router/decide` — 路由决策
- `GET /api/router/matrix` — 决策表
- `GET /api/router/profiles` — Profile 注册表
- `POST /api/hooks/{type}` — 质量检查 (4 种)
- `POST /api/exec` — 远程执行 Python/Shell
- `GET /` — Dashboard (Kanban 视图)

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/lovart-mflow-codebox/cmd/server/main.go` | add | 416 行 Go HTTP 服务器 |
| `1-4 Dev/lovart-mflow-codebox/go.mod` | add | Go 模块定义 |
| `1-4 Dev/lovart-mflow-codebox/start.sh` | add | codebox 进程管理契约 |
| `1-4 Dev/lovart-mflow-codebox/deploy-to-codebox.sh` | add | 一键部署脚本 |
| `1-1 Harness/01-project/PRD-codebox-deployment.md` | add | 部署 PRD |
| `1-1 Harness/01-project/迁移说明-codebox.md` | add | 迁移说明 |

# Tags
- relevant-tags: #codebox #deployment #go #api #dashboard #2026-07
