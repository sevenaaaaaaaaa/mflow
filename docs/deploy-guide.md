# MFlow 部署指南（本地 / 线上服务器 / Docker）

> MFlow 是"文件 + 状态机 + 定时任务"架构：无常驻数据库、无消息队列，任何能跑 Python 的机器都能部署。

---

## 一、本地运行（macOS / Linux，5 分钟）

```bash
git clone https://github.com/sevenaaaaaaaaa/mflow.git && cd mflow
uv venv .venv
uv pip install --python .venv/bin/python markdown pyyaml requests google-auth google-auth-httplib2 google-api-python-client
mkdir -p run/logs
printf 'export MFLOW_CONSOLE_PASSWORD=change-me\nexport LOVART_PYTHON=%s/.venv/bin/python\nexport LOVART_LOCAL_DEV_ROOT=%s/run/local-dev\n' "$PWD" "$PWD" > run/env.sh
source run/env.sh && .venv/bin/python "1-4 Dev/console/console.py"
# http://127.0.0.1:8088
```

`LOVART_LOCAL_DEV_ROOT` 是输出/日志/数据的运行时根目录，全部收在项目内，删目录即完全重置。

## 二、线上服务器（systemd，生产推荐）

以 Ubuntu/Debian 为例（CentOS 7 已验证可行）：

```bash
# 1) 代码与运行时
git clone https://github.com/sevenaaaaaaaaa/mflow.git /var/www/mflow && cd /var/www/mflow
curl -LsSf https://astral.sh/uv/install.sh | sh
~/.local/bin/uv venv .venv --python 3.12
~/.local/bin/uv pip install --python .venv/bin/python markdown pyyaml requests google-auth google-auth-httplib2 google-api-python-client

# 2) 环境契约（shell 语法；systemd 用 bash -c source 消费）
mkdir -p run/logs run/local-dev
cat > run/env.sh <<EOF
export MFLOW_CONSOLE_PASSWORD=你的强密码
export LOVART_LOCAL_DEV_ROOT=/var/www/mflow/run/local-dev
export LOVART_PYTHON=/var/www/mflow/.venv/bin/python
export PATH=/var/www/mflow/.venv/bin:/usr/local/bin:/usr/bin:/bin
EOF
chmod 600 run/env.sh

# 3) 工作台服务
cat > /etc/systemd/system/mflow-console.service <<'EOF'
[Unit]
Description=MFlow Console
After=network-online.target
[Service]
Type=simple
WorkingDirectory=/var/www/mflow
ExecStart=/bin/bash -c "source /var/www/mflow/run/env.sh && exec /var/www/mflow/.venv/bin/python \"/var/www/mflow/1-4 Dev/console/console.py\""
Restart=always
RestartSec=3
[Install]
WantedBy=multi-user.target
EOF

# 4) 定时器（每日管线 08:00 / 周报周一 07:00 / 夜间整理 02:30）
for j in daily weekly; do
cat > /etc/systemd/system/mflow-pipeline@$j.service <<EOF
[Unit]
Description=MFlow $j pipeline
After=network-online.target
[Service]
Type=oneshot
WorkingDirectory=/var/www/mflow
ExecStart=/bin/bash -c "source /var/www/mflow/run/env.sh && exec bash '/var/www/mflow/1-4 Dev/automation/run-$j-pipeline.sh'"
EOF
cat > /etc/systemd/system/mflow-$j.timer <<EOF
[Unit]
Description=MFlow $j timer
[Timer]
OnCalendar=$([ $j = daily ] && echo '*-*-* 08:00:00' || echo 'Mon *-*-* 07:00:00')
Persistent=true
Unit=mflow-pipeline@$j.service
[Install]
WantedBy=timers.target
EOF
done
systemctl enable --now mflow-console mflow-daily.timer mflow-weekly.timer
```

细节（独立 nginx/Apache vhost、与既有站点隔离、时区）参考 `deploy/server.md` 的实战记录。

## 三、Docker（可选）

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir markdown pyyaml requests google-auth google-auth-httplib2 google-api-python-client
ENV MFLOW_CONSOLE_PORT=8088
EXPOSE 8088
CMD ["python", "1-4 Dev/console/console.py"]
```

```bash
docker build -t mflow . && docker run -d -p 8088:8088 \
  -e MFLOW_CONSOLE_PASSWORD=change-me -v mflow_run:/app/run mflow
```

## 四、凭证与安全

- 全部凭证不入 git：`.gitignore` 覆盖 `secrets/`、各 credentials 目录、`run/llm.json`
- 控制台密码：`MFLOW_CONSOLE_PASSWORD`；**未设置时 fail-closed 全拒绝**
- 外网暴露建议：加反向代理 TLS（Caddy 一行即可）或限公司 IP
- 备份：状态即文件——备份 `run/`、`secrets/`、`1-1 Harness/`、`1-3 GenFlow/.pipeline/` 四处即可整机恢复

## 五、路径契约

- 所有脚本按自身位置推导路径，clone 到任意平铺目录即可
- 环境变量（可选覆盖）：`MFLOW_CONSOLE_PASSWORD` / `MFLOW_CONSOLE_PORT` / `LOVART_LOCAL_DEV_ROOT` / `LOVART_PYTHON` / `LOVART_RESOURCE_ROOT`
- 注意：systemd 的 `EnvironmentFile` 不认 `export` 语法；env 文件含 export 时统一用 `bash -c source` 启动（实战教训，见 deploy/server.md）
