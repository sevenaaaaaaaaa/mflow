# 多 Agent 自动化迁移指南

> **目标**：以 **项目级 shell 脚本** 为 SSOT，把 launchd 定时任务迁到 Cursor / Codex / Claude Code / OpenCode / Hermes / DeepSeek GUI。  
> **工作区根**：`LifeOS Pro PARA Vault`（git 根），日常 cwd 为子目录 `1-Project/`。
> **运行看板**：[../定期任务/自动化运行看板.md](../定期任务/自动化运行看板.md)

---

## 一、迁移原则

| 层 | 职责 |
|----|------|
| **Shell / Python 脚本** | 真正改文件、调 API（`dev/automation/`、`scripts/`） |
| **Agent 调度** | 按 cron 触发、读 log/报告、摘要、legacy>0 时拦编辑 |
| **launchd** | 可全部卸载；保留仅作离线兜底 |

```bash
# 卸载本机全部 com.mflow.* launchd（迁到 Cursor 后）
bash "dev/automation/unload-all-launchd.sh"
```

---

## 二、任务清单 → 脚本 → Cursor 草稿

| 任务 | 频率 | 项目入口 | Cursor 草稿 JSON | 原 launchd |
|------|------|----------|------------------|------------|
| Tools Pull | 周一 08:00 | `automation/tools-pull/pull-tools-from-production.sh` | `mflow-tools-pull.workflow.json` | ✅ 已保存 |
| 内容健康检查 | 周一 08:30 | `automation/content-health/weekly-health-check.sh` | `mflow-content-health-weekly.workflow.json` | `com.mflow.content-health-weekly` |
| Trident 三引擎 | 周一 06:00 | `dev/scripts/trident/run_all.sh` | `mflow-trident-weekly.workflow.json` | PRD `com.mflow.trident.weekly` |
| SEO 周报 | 周一 09:00 | `dev/scripts/weekly_review_v3.py` | `mflow-seo-weekly.workflow.json` | PRD `com.mflow.seo.weekly` |
| Sentinel 采集+日报 | 每日 08:00 | `scripts/sentinel/collect.py` + `report.py --daily` | `mflow-sentinel-daily.workflow.json` | PRD / 旧 plist |
| SEO 月报 | 每月 3 日 06:00 | `scripts/seo_monthly_v2.py` | 待建 | PRD |
| Sitemap 周更 | 周一 02:00 | Skill `sitemap-update` | 待建 | 归档 v2 plist |

**Cursor 导入**：Automations → New → 用 `open_automation` 预填各 JSON，或复制 `workflow.prompts[0].prompt` + cron。工作区选 **vault 根**。

---

## 三、各平台怎么接同一套脚本

详细配置见 [agent-platforms/](./agent-platforms/README.md)。

| 平台 | 配置文件 | 定时能力 | 推荐用途 |
|------|----------|----------|----------|
| **Cursor** | `.cursor/automations/*.workflow.json` | Automations cron | **主调度** + 摘要 |
| **Codex** | `AGENTS.md` + `~/.codex/` | 外部 cron / CI 调 `codex exec` | 无 UI 批处理 |
| **Claude Code** | `CLAUDE.md` + `.claude/settings.json` | 无内置 cron → Cursor/cron 触发 | 交互式 deep work |
| **OpenCode** | `~/.config/opencode/opencode.jsonc` | 无内置 cron | Skills 同步、Sanity 管道 |
| **Hermes** | `~/.config/opencode/skills/20-hermes/` | 依赖宿主 | Lark/飞书侧 automation |
| **DeepSeek GUI** | 应用内「系统提示」+ 手动 | 无 | 轻量问答，**不适合**无人值守 pull |

---

## 四、共享 Agent 提示词块（复制到任意平台）

### Tools Pull

```
bash "dev/automation/tools-pull/pull-tools-from-production.sh"
Read `~/Documents/MFlow Local Dev/Output/composite-v2-audit/pull-tools-latest.json` — legacy must be 0.
Do NOT sanity import/deploy/--replace.
```

### 内容健康检查

```
bash "dev/automation/content-health/weekly-health-check.sh"
Future release dates = 0; brokenUrls = 0 in `~/Documents/MFlow Local Dev/Temp/品牌/pull` reports.
```

### Trident Weekly

```
cd "dev/scripts/trident" && bash run_all.sh
Summarize updated JSON under `~/Documents/MFlow Local Dev/Output/Data Ingestion/` and reports under `insight-data/Trident Insights/`.
Do NOT sanity import/deploy/--replace.
```

### 周一早晨推荐顺序（若全迁 Cursor）

06:00 Trident → 08:00 Tools Pull → 08:30 Content Health → 09:00 SEO Weekly

---

## 五、凭证与环境（全平台共用）

| 项 | 位置 |
|----|------|
| Sanity | `dev/品牌.sanity.studio/.env` 或 `SANITY_API_TOKEN` |
| GSC/GA4/Bing | 项目内共享：`harness/Skills/trident-data-engine/credentials/`；脚本入口：`dev/scripts/trident/` |
| LLM | `~/.zshrc`：`OPENAI_API_KEY`、`ANTHROPIC_API_KEY` |
| 日志 | `~/Library/Logs/品牌方/`（launchd 遗留）、`pull-tools-latest.json` |

Cloud Agent **无法**直接读本机 `~/.zshrc` 与 iCloud 路径 — Cursor Automation 需选 **本机 Cloud Agent / local cwd** 且 vault 可访问；纯云端 VM 需改方案（git remote + secrets）。

---

## 六、launchd → Cursor 迁移步骤

1. 在 Cursor 按上表 **Save** 各 Automation（Tools Pull 已完成）
2. 各跑 **Run once** 验收
3. `bash dev/automation/unload-all-launchd.sh`
4. 更新 [06-自动化状态.md](./06-自动化状态.md)

---

## 七、限制说明

- **DeepSeek GUI / Hermes**：无等价 Cursor Automations cron；用「复制提示词 + 手动 Run」或继续 shell cron 只跑脚本、Agent 只看 log。
- **Obsidian + iCloud**：Cloud Agent 克隆仓库时确保含 `1-Project`；敏感 token 勿提交 git。
- **费用**：Cursor 定时 = Cloud Agent Max Mode；纯 shell 的 launchd 零 Agent 费。
