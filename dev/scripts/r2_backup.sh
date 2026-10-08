#!/usr/bin/env bash
# r2_backup.sh — run/ 冷数据镜像到 Cloudflare R2 + run/ 增量异地备份（A 方案）
#
# 原则：非破坏。服务器上的副本原样保留，R2 只做冷存储与灾备。
#   · 冷镜像（rclone sync，R2 侧与本地保持一致）：
#       run/library · run/_archive · run/qa · run/styles
#   · 整 run/ 增量备份（排除上面已单独镜像的冷目录，避免重复占用）：
#       变更/删除的文件进 backup/run-trash/<时间戳>，可回滚
#
# 依赖：服务器已装 rclone 并配置 remote（默认 r2）——见 deploy/install-r2-backup.sh
# 配置：MFLOW_R2_REMOTE（默认 r2）· MFLOW_R2_BUCKET（默认 mflow）
# 用法：bash dev/scripts/r2_backup.sh [--dry-run]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUN="$ROOT/run"
RCLONE="${RCLONE_BIN:-rclone}"
REMOTE="${MFLOW_R2_REMOTE:-r2}"
BUCKET="${MFLOW_R2_BUCKET:-mflow}"
STAMP="$(date +%Y%m%d-%H%M)"
DRY=()
DRY_LABEL="no"
if [[ "${1:-}" == "--dry-run" ]]; then DRY=(--dry-run); DRY_LABEL="yes"; fi

command -v "$RCLONE" >/dev/null 2>&1 || { echo "✗ 未找到 rclone（见 deploy/install-r2-backup.sh）" >&2; exit 2; }

LOG_DIR="$RUN/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/r2-backup-$STAMP.log"

# 同一时刻只跑一个（避免手动触发与定时任务重叠）
exec 9>"$RUN/.r2-backup.lock"
flock -n 9 || { echo "已有 r2 备份在跑，跳过本次"; exit 0; }

COMMON=(--transfers 8 --checkers 16 --fast-list --s3-no-check-bucket --stats 0 --log-level NOTICE)

{
  echo "=== MFlow R2 备份 · $(date '+%F %T') ==="
  echo "remote=$REMOTE bucket=$BUCKET run=$RUN dry=$DRY_LABEL"

  # 1) 冷镜像（R2 侧与本地一致；源目录不存在则跳过）
  for d in library _archive qa styles; do
    if [[ ! -d "$RUN/$d" ]]; then echo "[skip] run/$d 不存在"; continue; fi
    echo "--- 冷镜像 run/$d → $REMOTE:$BUCKET/$d"
    "$RCLONE" sync "$RUN/$d" "$REMOTE:$BUCKET/$d" "${COMMON[@]}" ${DRY[@]+"${DRY[@]}"}
  done

  # 2) run/ 增量备份（排除已镜像的冷目录；改动/删除进 run-trash）
  echo "--- run/ 增量备份 → $REMOTE:$BUCKET/backup/run"
  "$RCLONE" sync "$RUN" "$REMOTE:$BUCKET/backup/run" "${COMMON[@]}" ${DRY[@]+"${DRY[@]}"} \
    --exclude 'library/**' --exclude '_archive/**' --exclude 'qa/**' --exclude 'styles/**' \
    --exclude '.r2-backup.lock' --exclude 'logs/r2-backup-*.log' \
    --backup-dir "$REMOTE:$BUCKET/backup/run-trash/$STAMP" --suffix ""

  echo "=== 完成 · $(date '+%F %T') ==="
} 2>&1 | tee -a "$LOG"

echo "R2 备份完成，日志：$LOG"
"$RCLONE" size "$REMOTE:$BUCKET" 2>/dev/null | tail -1 || true
