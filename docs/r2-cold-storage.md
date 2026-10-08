# R2 冷存储与异地备份（A 方案）

把服务器上**冷数据**镜像到 Cloudflare R2，并做 `run/` 的增量异地备份。
**非破坏**：服务器上的副本原样保留，R2 只做冷存储与灾备。

## 存什么

| 内容 | R2 路径 | 方式 |
|---|---|---|
| `run/library`（内容库镜像） | `mflow/library/` | `rclone sync`（R2 与本地一致） |
| `run/_archive` | `mflow/_archive/` | 同上 |
| `run/qa` | `mflow/qa/` | 同上 |
| `run/styles`（素材） | `mflow/styles/` | 同上 |
| 其余 `run/`（projects/auth/logs/rag…） | `mflow/backup/run/` | `rclone sync` + `--backup-dir` |

被覆盖/删除的文件进 `mflow/backup/run-trash/<时间戳>/`，可回滚。日志落 `run/logs/r2-backup-*.log`。

## 为什么不能“整个项目搬 R2”

R2 是对象存储，**不跑代码**。MFlow 的工作台（`dev/console/console.py`，107 个 API）与
systemd 定时器必须有计算。且 console 重度依赖本地文件系统（原子 `os.replace`、目录扫描、
文件锁）——用 FUSE 把 R2 挂成本地盘会显著伤稳定性。故：**计算留服务器，冷数据上 R2**。

## 一次性配置（服务器，root）

1. 装 rclone 静态二进制到 `/usr/local/bin/rclone`。
2. 写 root-only remote `~/.config/rclone/rclone.conf`：

```ini
[r2]
type = s3
provider = Cloudflare
access_key_id = <R2 Access Key>
secret_access_key = <R2 Secret Key>
endpoint = https://<account_id>.r2.cloudflarestorage.com
acl = private
```

3. 安装定时任务：`bash deploy/install-r2-backup.sh`（每日 03:30，systemd timer）。
4. 首次全量：`bash dev/scripts/r2_backup.sh`（约几分钟）。

## 常用命令

```bash
bash dev/scripts/r2_backup.sh --dry-run     # 预演，不传输
bash dev/scripts/r2_backup.sh               # 立即跑一次
rclone size r2:mflow                        # R2 侧体积/对象数
rclone ls   r2:mflow/library | head         # 抽查
systemctl list-timers mflow-r2-backup.timer # 看下次运行
```

## 恢复演练

```bash
rclone copy r2:mflow/library/<path> /tmp/restore/   # 取回单个文件
rclone sync r2:mflow/backup/run /www/wwwroot/mflow/run   # 全量回灌（谨慎）
```

## 进一步降低服务器占用（B 方案，未做）

若要让冷数据**只留在 R2**、本地按需拉取，需要改 `console.py`：`/api/library/*`、
多语言覆盖、物料扫描、内链体检都直接读 `run/library`，须改成“本地缓存 + R2 按需取”。
属重构，风险高于本方案，需要单独评估。
