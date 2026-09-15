# 每周内容分发调度

## 节奏

| 时间 | 动作 | 命令 / 触发 |
|------|------|-------------|
| 周一 09:00 | GA 页面评分 | `python3 scripts/score-pages-for-distribution.py --days 28` |
| 周一 09:30 | 更新待办队列 | 输出 `queue/pending.json`（脚本自动） |
| 周一 10:00 | Agent 生成草稿 | Cursor：为 pending 写 `cn`+`global` 稿 → `queue/dispatch-*.json` |
| 周三 14:00 | 预检 + 人工审核 | `dispatch-publish.js --dry-run`（内置 preflight） |
| 周三 15:00 | 国内发布 | `dispatch-publish.js --cn-only`（Wechatsync） |
| 周三 15:30 | 海外发布 | `mcp-flush-prompt.sh` → Cursor MCP publish |
| 周五 17:00 | 周报复盘 | 填写 `logs/weekly-YYYY-MM-DD.md` |

## 方式 A — macOS launchd（推荐本地）

创建 `~/Library/LaunchAgents/com.lovart.content-distribution.score.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.lovart.content-distribution.score</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/seveno/Projects/content-distribution/scripts/score-pages-for-distribution.py</string>
    <string>--days</string>
    <string>28</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key>
    <integer>1</integer>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>/Users/seveno/Projects/content-distribution/logs/cron-score.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/seveno/Projects/content-distribution/logs/cron-score.err</string>
</dict>
</plist>
```

加载：

```bash
launchctl load ~/Library/LaunchAgents/com.lovart.content-distribution.score.plist
```

## 方式 B — Cursor Automation

在 Cursor Automations 新建定时任务（每周一 09:00）：

**Prompt 摘要：**

1. `cd ~/Projects/content-distribution`
2. 运行 `python3 scripts/score-pages-for-distribution.py --days 28`（失败则 `--sample` 并告警）
3. 读取 `queue/pending.json` Top 5
4. 对每篇 S/A 级 blog，按 `channels/medium.md` 与 `channels/devto.md` 生成 `drafts/` 摘要
5. 对每篇草稿运行 `preflight-distribution.js`
6. 将结果摘要写入 `logs/weekly-{date}.md`（不自动发布，等待周三人工）

**Tools：** Shell、Read、Write

## 方式 C — 手动 cron

```cron
0 9 * * 1 cd /Users/seveno/Projects/content-distribution && /usr/bin/python3 scripts/score-pages-for-distribution.py --days 28 >> logs/cron-score.log 2>&1
```

## 告警

- 评分脚本 exit 2 → Trident 快照缺失，检查 `TRIDENT_ROOT`
- preflight exit 1 → 不得发布，修稿后重跑
- 同一 `canonical_url` 本月在 `published.json` 已 ≥2 条 → 跳过该平台

## 周报模板

`logs/weekly-YYYY-MM-DD.md`：

```markdown
# 分发周报 YYYY-MM-DD

## 本周发布
| 平台 | 主站 URL | 站外 URL | UTM 会话 |

## 候选池
- S/A 级新增：N 篇

## 轨道 B
- 新 brief：...

## 下周
- ...
```
