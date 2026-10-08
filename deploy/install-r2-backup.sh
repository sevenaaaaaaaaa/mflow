#!/usr/bin/env bash
# install-r2-backup.sh — 在服务器安装/更新 MFlow R2 冷备 systemd 单元
#
# 前置（一次性，root）：
#   1) 安装 rclone 静态二进制到 /usr/local/bin/rclone
#   2) 写 rclone remote（root-only）~/.config/rclone/rclone.conf：
#        [r2]
#        type = s3
#        provider = Cloudflare
#        access_key_id = <R2 Access Key>
#        secret_access_key = <R2 Secret Key>
#        endpoint = https://<account_id>.r2.cloudflarestorage.com
#        acl = private
#      （凭据来源见运维私有文档；绝不入库）
#
# 用法（服务器上，root）：bash deploy/install-r2-backup.sh
# 覆盖目录：MFLOW_ROOT=/www/wwwroot/mflow bash deploy/install-r2-backup.sh
set -euo pipefail

ROOT="${MFLOW_ROOT:-/www/wwwroot/mflow}"
SVC="/etc/systemd/system/mflow-r2-backup.service"
TMR="/etc/systemd/system/mflow-r2-backup.timer"
RCLONE_BIN="${RCLONE_BIN:-/usr/local/bin/rclone}"

if [[ ! -x "$RCLONE_BIN" ]]; then
    echo "✗ 未找到 rclone：$RCLONE_BIN（先装 rclone，见本脚本顶部）" >&2
    exit 2
fi
if ! "$RCLONE_BIN" listremotes 2>/dev/null | grep -q '^r2:'; then
    echo "✗ rclone 未配置 remote [r2]（见本脚本顶部）" >&2
    exit 2
fi
if [[ ! -f "$ROOT/dev/scripts/r2_backup.sh" ]]; then
    echo "✗ 缺少 $ROOT/dev/scripts/r2_backup.sh（先同步代码）" >&2
    exit 2
fi

cat > "$SVC" <<EOF
[Unit]
Description=MFlow R2 冷备（library/_archive/qa 镜像 + run 增量备份）
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory=$ROOT
ExecStart=/bin/bash "$ROOT/dev/scripts/r2_backup.sh"
Nice=10
IOSchedulingClass=idle
EOF

cat > "$TMR" <<EOF
[Unit]
Description=每日 03:30 运行 MFlow R2 冷备

[Timer]
OnCalendar=*-*-* 03:30:00
Persistent=true
RandomizedDelaySec=600

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now mflow-r2-backup.timer
systemctl list-timers mflow-r2-backup.timer --no-pager || true
echo "✓ 已安装并启用 mflow-r2-backup.timer（每日 03:30）"
