---
type: dream-readme
version: 1.0
updated: 2026-07-05
scope: "profile-lovart-management"
tools: [hermes, opencode, cursor, claude, codex]
status: active
path: 1-1 Harness/11-knowledge/dream/README.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Dream — 梦境的使用说明

梦境 = 没人看着的时候，让系统自己收拾：把今天的事实塞进记忆、把过期的标掉、把工具之间的不一致提 PR。

## 三种触发方式

| 入口 | 谁用 | 何时 |
|------|------|------|
| **launchd 自动** | 全 5 工具 | 每日 02:30 |
| **manual cron / launchctl kickstart** | 运维 | 月初盘点、季度切换、紧急一致性修复 |
| **skill `lovart-dream-orchestrator`** | 任意 Profile | "今晚先把这些理一理再开工" |

## 一次梦境做的事（顺序）

1. **emit JSONL**：从 `entities.yaml` + `relationships.yaml` 重新生成 `entities.jsonl` + `relationships.jsonl`。这是机器读取的 SSOT 镜像。
2. **frontmatter check**：跑 `fm-check.py`，记录缺失比例（informational）。
3. **MEMORY-PROJECT.md 反推**：若 `entities.yaml` mtime 更新，则更新 `MEMORY-PROJECT.md` 的 `last_consolidated` 字段。
4. **同步 Hermes MEMORY**：把 `MEMORY-PROJECT.md` 的"重要新事实"段反推到 `~/.hermes/memories/MEMORY.md`（"project slice"）。
5. **audit**：跑 6 项 audit（A1-A6），写 `audit/reports/audit-report-{YYYY-MM-DD}.md` + `audit/checks/audit-{YYYY-MM-DD}.json`。
6. **exit code**：若 audit 发现 ERROR，cron 侧应发邮件/通知；若仅 WARN，写入报告即可。

## 安装 launchd（macOS）

```bash
# 1. 处理 plist 中的 /REPLACE_WITH_VAULT_ROOT/ 占位
VAULT="/path/to/1-Project/Lovart MFlow"
sed "s|/REPLACE_WITH_VAULT_ROOT|$VAULT|g" dream/lovart.dream.plist \
  > ~/Library/LaunchAgents/com.lovart.dream.plist

# 2. 加载
launchctl unload ~/Library/LaunchAgents/com.lovart.dream.plist 2>/dev/null || true
launchctl load ~/Library/LaunchAgents/com.lovart.dream.plist

# 3. 立即试跑
launchctl kickstart -k gui/$(id -u)/com.lovart.dream
tail -f /tmp/com.lovart.dream.out.log
```

> Hermes 也可注册 cron（`hermes cron add ...`），二者择一即可。launchd 路径已配，`hermes cron` 暂未启用。

## 手动命令行

```bash
# 跑一次完整梦境
bash 1-1\ Harness/11-knowledge/dream/consolidate.sh

# 只 refresh JSONL
bash 1-1\ Harness/11-knowledge/dream/consolidate.sh --emit-only

# 只跑 audit（不写报告）
bash 1-1\ Harness/11-knowledge/dream/audit.sh --no-write-today

# 只跑 A3 (entry-point refs)
bash 1-1\ Harness/11-knowledge/dream/audit.sh --no-write-today A3

# 看当次报告
ls -t 1-1\ Harness/11-knowledge/audit/reports/ | head
```

## 通过 skill 触发

任意 agent / Profile 触发 `lovart-dream-orchestrator`：
- "今晚准备发 blog，先把梦境跑一遍" → 跑 audit only, write report
- "新人入项 / 工具换了 / 配置改了" → 跑 consolidate.sh 全套一步完成

skill 通过 Bash 调用 `consolidate.sh` / `audit.sh`。

## 安全 / 边界

梦境**只做**：
- 重新生成机器可读镜像（JSONL）
- bump 时间戳
- 写日志与报告
- 反推 Hermes MEMORY.md（仅当 entities.yaml 有新条目）

梦境**不做**：
- 自动改 entry-point 文件（HIGH 风险，留 audit 标记 + 用户手动改）
- 自动修补 frontmatter（LOW 风险，但会有"AI 见 AI 改"的循环）
- 删除任何文件
- 触发外部发布（Sanity / Sitemap / IndexNow 等）
