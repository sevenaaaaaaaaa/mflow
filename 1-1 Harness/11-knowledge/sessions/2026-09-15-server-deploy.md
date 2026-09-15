---
type: session-log
session_date: 2026-09-15
session_slug: server-deploy
status: ready
---

# Session Log — MFlow 服务器私有实例部署

## 目标
用户授权部署。硬性要求：独立目录 + 独立 URL，不与 XMP/OpenFlow 混部。

## 服务器实况
- CentOS 7 / 宝塔 Apache（80/443 = XMP）/ Docker / 2G 内存 / 上海时区 / 系统 Python 3.6（不动）
- 方案：uv 独立 Python 3.12.14 venv；rsync 代码（排除创作大数据池，~300M）；systemd timers；Apache 独立 8088 vhost

## 完成
1. /var/www/mflow 独立目录；run/env.sh 环境契约（输出/日志自包含于 mflow 目录）
2. systemd 4 timers：daily 08:00 / weekly 周一 07:00 / dream 02:30 / status 每 30min（全部 CST，与 Mac 语义一致，Persistent=true 补跑）
3. 独立 URL http://172.96.253.73:8088/：Apache Listen 8088 + panel/vhost/apache/mflow.conf（IncludeOptional 挂载，零改动既有配置）；render-status.py 渲染 pipeline/Sentinel/fm-check 三源状态页
4. 验证：session-init 4 门禁 PASS、pipeline smoke 39/39、每日管线全链路 exit 0（服务器真实拉 GSC + Sentinel 22 源 + harness 同步）、外部 8088 可达
5. 凭证随 rsync 就位（trident/sentinel credentials、secrets/），权限继承

## 差异与说明
- 服务器副本无 .git（运行副本，版本真相在 GitHub）；无创作内容池（Calendar/Page Gen/Drafts 留 Mac）
- 飞书 SKIP 与 Mac 一致（凭据未配）；weekly timer 下周一首跑待观察
- Mac 与服务器现各有一份 Sentinel 日报输出（各自本地路径），互不干扰；将来若需合并口径，在报告层做

## Lessons
- scp 远程路径含空格用 sftp 转义会翻车——经 /tmp 中转最稳
- 宝塔 IncludeOptional 目录是加 vhost 的零侵入通道，比改 httpd.conf/vhosts 安全
