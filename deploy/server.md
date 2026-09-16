# 服务器部署接线（2026-09-15 已部署 ✅）

## 目标服务器

- 主机：`172.96.253.73`，SSH 端口 `28766`，用户 `root`
- 私钥：`~/OpenFlowDev/.ssh/172.96.253.73_id_ed25519`（本机，未入本仓库；known_hosts 见同目录）
- 连通验证：`ssh -i ~/OpenFlowDev/.ssh/172.96.253.73_id_ed25519 -p 28766 root@172.96.253.73 'uname -a'`

## 与 XMP/OpenFlow 的隔离（用户硬性要求，2026-09-15）

MFlow 部署**必须与既有 XMP（OpenFlow，`/var/www/openflow`）完全隔离**：

- **独立目录**：`/var/www/mflow`（仓库 checkout 即此目录，平铺布局，脚本已全部项目根相对）
- **独立 URL**：独立 nginx server block（独立 conf 文件，如 `/etc/nginx/conf.d/mflow.conf` 或宝塔对应 vhost），
  server_name 用独立子域（如 `mflow.<主域名>`，具体域名部署时由用户确认）；**禁止**挂在 openflow 站点的子路径下
- **独立进程**：systemd 单元命名空间 `mflow-*`（mflow-daily.timer / mflow-weekly.timer / mflow-dream.timer），与 openflow 的 php-fpm/进程互不引用
- **独立日志**：`/var/www/mflow/run/logs/`，不写 openflow 目录
- 两侧唯一共享：同一台机器、同一个 root SSH；磁盘/端口层面如需再分（不同 listen 端口），部署时按 nginx 现场配置定

## 关联 GitHub

- 本仓库远端：`https://github.com/sevenaaaaaaaaa/mflow`（私有，原名 mflow-dev 已改名）
- gh CLI 已登录 `sevenaaaaaaaaa`（repo scope）
- 同账号参考项目：`openflow`（PHP，同服务器 /var/www/openflow，nginx.site.conf / baota-rewrites.conf 可参考 nginx 写法）

## 部署形态（v1 约定，未执行）

- 形态：内核 CLI + systemd timer（对应本机 launchd：daily 08:00 / weekly Mon 07:00 / dream 02:30）
- 运行时：uv 建 venv（google-auth + googleapiclient + pyyaml + requests），即本机 trident-venv 的复刻
- 凭证：环境变量 / root-only env 文件注入，绝不入 git（.gitignore 已隔离 secrets/）
- 国内分发轨（Wechatsync 浏览器扩展）不上服务器，保留在 Mac
- ~~部署动作必须用户明示授权后执行~~ **用户已于 2026-09-15 授权，部署完成**

## 已部署实况（2026-09-15，2026-09-16 迁移路径）

- 代码：`/www/wwwroot/mflow/`（2026-09-16 从 /var/www/mflow 迁移，rsync，排除 From Datawork / Content Calendar / Page Gen / 分发 Drafts / .git——创作大数据池留在 Mac）
- 运行时：uv + Python 3.12.14 → `/var/www/mflow/.venv`（google-auth/googleapiclient/pyyaml/requests）；系统 Python 3.6 未动
- 环境契约：`/var/www/mflow/run/env.sh`（LOVART_LOCAL_DEV_ROOT=/var/www/mflow/run/local-dev、LOVART_PYTHON=.venv）——输出/日志全部落在 mflow 自己目录内
- systemd（全部 CST 时区，与 Mac launchd 语义一致）：
  - `mflow-daily.timer` → 每日 08:00（mflow-pipeline@daily.service）
  - `mflow-weekly.timer` → 周一 07:00（mflow-pipeline@weekly.service）
  - `mflow-dream.timer` → 每日 02:30（mflow-dream.service）
  - `mflow-status.timer` → 每 30 分钟刷新状态页（mflow-status.service）
- 独立 URL：**https://nownexts.com/mflow/**（宝塔 Apache vhost 反向代理 /mflow/ → localhost:8088，零影响 XMP/OpenFlow 主站；2026-09-16 路径迁移至 /www/wwwroot/mflow/ 后验证通过）
- 工作台（2026-09-15 增）：`mflow-console.service`，console.py 直绑 0.0.0.0:8088（取代 Apache 静态页，mflow.conf 已 disabled-by-console）。密码 `MFLOW_CONSOLE_PASSWORD` 在 run/env.sh。功能：管线看板+状态机推进 / 路由决策 / 质量钩子执行 / 每日管线触发与日志 / 调度与健康 / 分发只读。发布类操作只读（铁律）。systemd 引用 env.sh 必须用 `bash -c source`（EnvironmentFile 不认 export 语法——踩过的坑）
- 验证记录：session-init 4 门禁 PASS · pipeline smoke 39/39 · 每日管线全链路 exit 0（gsc/sentinel/harness 全 OK，feishu SKIP 同 Mac）
- 隔离确认：80/443 仍为 XMP/OpenFlow；MFlow 仅占 8088；无共享目录/进程/日志
