# Tools Pull — production → 本地正式源

**原则**：Sanity production 是真相源；本地 `Page Gen/Pages/Tools/` 是编辑区。定期 pull 避免线下迁移与线上漂移。

## 一键命令（推荐）

```bash
# 从任意目录
bash "1-4 Dev/automation/tools-pull/pull-tools-from-production.sh"

# 或进入 studio
cd "1-4 Dev/lovart.sanity.studio"
node scripts/pull-tools-from-production.js
```

等价于顺序执行：

1. `export-composite-production.js` → `~/Documents/Lovart Local Dev/Output/composite-v2-audit/production-export.json`
2. `sync-tools-from-production.js` → `Page Gen/Pages/Tools/`
3. 审计摘要 + `pull-tools-latest.json`

### 选项

|  flag | 作用 |
|-------|------|
| `--dry-run` | 不写本地 JSON |
| `--skip-export` | 复用已有 export（离线 / 省 API） |
| `--from-chunks` | export 从 `production-chunks/` 读（无 token 时） |

## 何时跑

| 场景 | 建议 |
|------|------|
| Tools `import --missing` 成功后 | 同会话 pull 一次 |
| 每周一 / Sprint 初 | launchd 或 Cursor Automation |
| Studio 手改、他人 import 后 | 改本地前先 pull |
| 换设备 | 必跑 |

**注意**：pull 会覆盖同路径 JSON；有未提交本地编辑时先备份或提交。

## macOS 定时（launchd）

```bash
cd "1-4 Dev/automation/tools-pull"
bash install.sh
```

- 默认：**每周一 07:00**
- 日志：`~/Library/Logs/Lovart/tools-pull-weekly.log`
- 手动：`launchctl start com.lovart.tools-pull-weekly`

## Cursor Automation（第二层）

见 [`cursor-tools-pull-automation.md`](../../1-5%20Harness/automation/cursor-tools-pull-automation.md)。

项目级 shell 脚本优先 — Cursor Automation 仅调用同一入口，保证与 launchd / 手工命令一致。

## 凭证

需 Sanity read token（与 export 相同）：

- `SANITY_API_TOKEN` 环境变量，或
- studio `.env`，或
- `~/.config/sanity/config.json` 的 `authToken`

## 产出

| 路径 | 说明 |
|------|------|
| `~/Documents/Lovart Local Dev/Output/composite-v2-audit/production-export.json` | 线上快照 |
| `~/Documents/Lovart Local Dev/Output/composite-v2-audit/pull-tools-latest.json` | 最近一次 pull 摘要 |
| `1-3 Content Gen/Page Gen/Pages/Tools/` | 本地正式源（含 `_syncedFromProduction`） |
