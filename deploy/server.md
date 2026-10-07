# 服务器部署

> 工作台三条部署路径（本地 / 服务器 / Docker）见 [deploy-guide.md](../docs/deploy-guide.md)。
> 本文件记录服务器形态的部署约定与**开源化迁移 runbook**。具体主机地址、密钥路径等
> 基础设施信息属于运维私有数据，不入公开仓库。

## 部署形态（服务器）

- **目录**：独立 checkout 目录（平铺布局，脚本全部项目根相对），与同机其他应用硬隔离（目录/端口/进程/日志）
- **URL**：独立 nginx/Apache server block 反向代理到工作台端口（默认 8088）
- **进程**：systemd 单元命名空间 `mflow-*`：
  - `mflow-daily.timer` → 每日 08:00（信号管线：搜索控制台拉数 + 舆情采集 + 规则同步）
  - `mflow-weekly.timer` → 每周一 07:00（每周管线）
  - `mflow-dream.timer` → 每日 02:30（记忆整理）
  - `mflow-status.timer` → 状态页刷新
  - `mflow-console.service` → 工作台常驻（console.py）
- **运行时**：Python 3.12 venv（google-auth / googleapiclient / pyyaml / requests + markdown）
- **环境契约**：`run/env.sh`（`MFLOW_PYTHON` / `MFLOW_LOCAL_DEV_ROOT` / `MFLOW_CONSOLE_PASSWORD`）。
  systemd 引用 env.sh 必须用 `bash -c source`（EnvironmentFile 不认 export 语法——踩过的坑）
- **变量命名**：环境变量统一 `MFLOW_*` 前缀；若存量 env.sh 用过旧前缀变量名，迁移时顺手改掉
  （见下文 runbook）；LLM profile 键若用过旧前缀，迁移时改成不带前缀的同名键
- **凭证**：环境变量 / root-only 文件注入，绝不入 git（`.gitignore` 已隔离 `secrets/`）

## 开源化迁移 runbook（服务器执行）

2026-09-27 起公开仓库不再追踪**内容与情报数据**（文章库、报告、关键词、知识库正文、
会话日志、项目记忆——含业务事实）。这些数据在服务器本地保留，按以下顺序迁移：

```bash
cd /www/wwwroot/mflow   # 按实际 checkout 目录

# 1) 备份本地数据（pull 会删除这些已追踪文件）
mkdir -p ~/mflow-data-backup
cp -a "insight-data" "genflow" "harness/11-knowledge" ~/mflow-data-backup/ 2>/dev/null || true

# 2) 拉取开源化后的代码
git pull

# 3) 把本地数据移回（这些目录已在 .gitignore，不会再被追踪/删除）
mv ~/mflow-data-backup/"insight-data" ~/mflow-data-backup/"genflow" .
mkdir -p "harness/11-knowledge"
cp -a ~/mflow-data-backup/"harness/11-knowledge/." "harness/11-knowledge/" 2>/dev/null || true

# 4) 默认项目目录对齐新命名（工作台默认项目 id 已改为 main）：
#    若 run/projects/ 下存在旧默认项目目录（不带 main 名），整体改名为 main

# 5) 重启工作台并验证
systemctl restart mflow-console.service
curl -fsS http://127.0.0.1:8088/ >/dev/null && echo console OK
```

**注意**：

- launchd/systemd 的**定时器标签**与 hermes profile 目录名属服务器本地配置，
  迁移时对齐仓库内的新命名即可（`com.mflow.*` / 不带前缀的 profile 键）；
- `run/env.sh` 变量名改为 `MFLOW_PYTHON` / `MFLOW_LOCAL_DEV_ROOT`；`run/llm.json`
  的 profiles 键去掉旧前缀（如 `xxx-creation` → `creation`）或保留 `default` 键兜底。

## 状态

- 服务器现状约定以运维私有文档为准（不入库）
- 迁移完成后在服务器本地跑一次 `bash "dev/scripts/session-init.sh"` 与
  `bash "dev/scripts/run-tests.sh"` 验证
