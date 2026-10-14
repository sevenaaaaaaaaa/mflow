# CLAUDE.md — MFlow

## 项目简介

MFlow 是 GEO（生成式引擎优化）自动化内容生产系统：信号监测（舆情/SEO/SERP）→ 内容生产（Blog、各类落地页）→ 内容分发 → 质检（anti-bug / anti-slop / 排版 / CRO）。核心是单文件 Web 工作台 + Harness 技能库。

**先读 `AGENTS.md`**（会话门禁、知识/记忆读取顺序、Session 收尾日志均为强制约定）；Harness 细则见 `harness/00-INDEX.md` 与 `harness/CLAUDE.md`。

## 技术栈

- Python 3.10+（服务器 3.12 venv），以标准库为主，依赖 `markdown`、google-auth / googleapiclient、pyyaml、requests
- 工作台：`dev/console/console.py`（单文件 HTTP 服务，默认端口 8088）+ 静态 HTML
- 无数据库，状态落文件（`run/`）
- 调度：本地 launchd（`dev/automation/plists/`），服务器 systemd timer（`mflow-*`）
- 附带：`dev/mflow-codebox/`（Go）、`dev/wordpress/docker-compose.yml`（本地 WordPress 调试）

## 目录结构

```
dev/console/        工作台（console.py / console.html / mission.py）
dev/scripts/        管线与工具脚本（session-init.sh、run-tests.sh、hooks/、publish_adapters/、trident/、sentinel/…）
dev/automation/     每日/每周管线脚本与 launchd plist
dev/tests/          单元测试 test_*.py
harness/            Skills（技能唯一真相）、02-rules、03-workflows、10-config、11-knowledge（gitignored）
plugins/            质量门禁插件（geo/lang/quota/readability check、schema-generator…）
templates/          项目/行业模板
deploy/             发布脚本（sync.sh、push.sh）与 server.md
docs/               文档（deploy-guide.md、quickstart.md…）
run/                运行时数据（大部分 gitignored）
insight-data/ genflow/  内容/情报数据（gitignored）
```

`1-1 Harness` / `1-2 Insight` / `1-4 Dev` 为旧路径过渡垫片（gitignored），不要在其中开发。

## 常用命令

```bash
pip install markdown                                  # 安装（最小依赖）
bash "dev/scripts/session-init.sh"                    # 会话门禁（每次会话开始必跑）
export MFLOW_CONSOLE_PASSWORD=...                      # 不设则 API 全部拒绝
python3 "dev/console/console.py"                      # 启动工作台 → http://127.0.0.1:8088/
bash "dev/scripts/run-tests.sh"                       # 单元测试（自动隔离 MFLOW_RUN_DIR）
bash "dev/scripts/hooks/tests/smoketest_hooks.sh"     # hook 冒烟测试
python3 "harness/Skills/06-orchestrate/pipeline-state/pipeline_state.py" summary
bash "dev/automation/run-daily-pipeline.sh"           # 每日信号管线
```

build / lint：无独立命令（语法门禁含在 session-init.sh 中）。

## 部署方式

- 目标：服务器 `root@172.96.253.73`，SSH 端口 `28766`，目录 `/www/wwwroot/mflow`，systemd `mflow-console.service`（+ `mflow-daily/weekly/dream/status.timer`），对外 `https://nownexts.com/mflow/`（前置 Cloudflare）
- **双轨**：GitHub（公开仓库）只放代码；内容/情报数据、知识库、运行数据、凭据由 `.gitignore` 挡在仓库外，靠 rsync 从本地工作区送到服务器
- 唯一入口 `deploy/sync.sh`：本地测试 → gitleaks 扫描待提交改动（有泄漏即中止）→ `git add -A` + 提交 → push `main` → rsync 代码目录（原清单，`harness/Skills`、`harness/02-rules` 保持 `--delete`）→ rsync gitignored 内容（`insight-data/`、`genflow/`、`harness/11-knowledge/`、`dev/Output/`，`--update` 只增不删、不覆盖服务器上更新的文件）→ 重启 `mflow-console` → 服务端门禁 → 外部验证 → CF 缓存刷新

```bash
bash deploy/sync.sh                      # 全流程
bash deploy/sync.sh -m "feat: 说明"      # 指定提交说明（同 --msg，Conventional Commits）
bash deploy/sync.sh --server-only        # 跳过 git，只同步服务器 + 重启 + 验证
bash deploy/sync.sh --dry-run            # 测试 + gitleaks + 预览提交 + rsync -n；不提交/不推送/不重启
bash deploy/sync.sh --no-content         # 不同步 gitignored 内容数据
bash deploy/sync.sh --no-push | --no-commit | --skip-tests | --cf-purge-all
bash deploy/push.sh                      # 只推 GitHub
```

- 分支：`main`；无 GitHub Actions；默认提交信息 `chore(sync): auto-deploy <时间>`
- 本地 `.git/hooks/pre-commit` 跑 `gitleaks git --pre-commit --staged`，任何提交含密钥都会被拦下
- 密钥一律走环境变量或 gitignored 本地文件（变量名见 `.env.example`），如飞书 Base token：`FEISHU_BASE_TOKEN` 或 `harness/Skills/01-strategy/trident-data-engine/credentials/feishu_base_token`
- 服务器目录**不要再 `git pull`**：大量内容已出库，pull 会删掉服务器上的同名文件；更新一律走 `deploy/sync.sh`
- 其他路径（本地 / Docker）见 `docs/deploy-guide.md`，服务器约定见 `deploy/server.md`

## 开发工具 vs 使用工具（硬性规则）

MFlow 既是在开发的工具，也是每天在用的生产工具。两类产物必须分开：

| 类别 | 例子 | 放哪 | GitHub | 服务器 |
|---|---|---|---|---|
| 开发工具（产品代码） | `dev/`、`harness/Skills`、`plugins/`、`templates/` | 原目录 | ✅ | ✅（代码清单） |
| 使用工具的产物 | 运营/SEO 批处理脚本（如 `d2-setup.py`）、批次文件、一次性修复脚本、导出数据 | **`ops/`**（根目录随手脚本也算） | ❌ | ✅（内容同步，只增不删） |

- 用 MFlow 干活时新写的脚本一律放 `ops/`；`/ops/` 与根目录的 `*.py/*.sh/*.js/*.mjs/*.ts` 已 gitignore，`deploy/sync.sh` 只把它们送到服务器（`--update`，不覆盖服务器上更新的版本）。
- 公开仓库「零 Lovart」（2026-09-28 开源化 P2）：任何含 Lovart / 客户站点 / Sanity 项目信息的东西都属于第二类。
- 拿不准时按第二类处理（不进 GitHub），再问用户。

## 注意事项

- 环境变量：`MFLOW_CONSOLE_PASSWORD`、`MFLOW_API_TOKEN`、`MFLOW_CONSOLE_PORT`、`MFLOW_PYTHON`、`MFLOW_LOCAL_DEV_ROOT`、`MFLOW_RUN_DIR`、`MFLOW_ROOT`、`MFLOW_RESOURCE_ROOT`、`MFLOW_LOOP_TOKEN_CAP`、`MFLOW_REMOTE_HOST`、`MFLOW_REMOTE_PORT`、`MFLOW_SITE_URL`（服务器经 `run/env.sh` 注入）
- `deploy/cf.env`（`CF_API_TOKEN` / `CF_ZONE_ID` / `CF_DOMAIN`）与 `deploy/gh.env`（`GH_USER` / `GH_TOKEN`）为本地凭据文件，模板见 `*.env.example`，勿读勿入库
- `deploy/sync.sh` 会 `git add -A` 自动提交所有改动（已有 .gitignore + gitleaks 兜底），运行前仍应确认工作区
- 不存在独立的 `.claude/skills/`；技能以 `harness/Skills/` 为准，编辑器规则由 `dev/scripts/harness_sync.py` 生成
- 会话结束须按 `AGENTS.md` 写 Session Log 到 `harness/11-knowledge/sessions/`
- 脚本路径含空格，命令中务必加引号
