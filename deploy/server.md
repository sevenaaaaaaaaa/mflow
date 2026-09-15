# 服务器部署接线（2026-09-15，未部署——仅登记）

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
- 部署动作必须用户明示授权后执行
