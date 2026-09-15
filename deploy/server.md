# 服务器部署接线（2026-09-15，未部署——仅登记）

## 目标服务器

- 主机：`172.96.253.73`，SSH 端口 `28766`，用户 `root`
- 私钥：`~/OpenFlowDev/.ssh/172.96.253.73_id_ed25519`（本机，未入本仓库；known_hosts 见同目录）
- 连通验证：`ssh -i ~/OpenFlowDev/.ssh/172.96.253.73_id_ed25519 -p 28766 root@172.96.253.73 'uname -a'`

## 关联 GitHub

- 本沙箱远端：`https://github.com/sevenaaaaaaaaa/mflow-dev`（私有）
- gh CLI 已登录 `sevenaaaaaaaaa`（repo scope）
- 同账号参考项目：`openflow`（PHP，同服务器部署过，deploy/baota-rewrites.conf 是宝塔环境）

## 部署形态（v1 约定，未执行）

- 形态：内核 CLI + systemd timer（launchd plist 逐字段翻译：daily 08:00 / weekly Mon 07:00 / dream 02:30）
- 运行时：uv 建 venv（google-auth + googleapiclient + pyyaml + requests），即本机 trident-venv 的复刻
- 凭证：环境变量 / root-only env 文件注入，绝不入 git（.gitignore 已隔离 secrets/）
- 路径：本仓库 checkout 即项目根（平铺布局，所有脚本已改为项目根相对——2026-09-15 修复，兼容 vault/沙箱/服务器三种布局）
- 国内分发轨（Wechatsync 浏览器扩展）不上服务器，保留在 Mac
- 部署动作必须用户明示授权后执行
