---
type: knowledge-architecture
wing: lovart_mflow
version: 1.0
last_consolidated: 2026-07-05
covers: [Hermes, OpenCode, Cursor, Claude, Codex]
---

# 11 — Knowledge · Memory · Dream · Audit

> **这是 Lovart MFlow 的 SSOT**：单个项目内为 5 个 AI 工具（Hermes / OpenCode / Cursor / Claude / Codex）共享的"知识树 / 记忆 / 梦境 / 一致性审计"基础设施。
> 谁先找到这里（任意 agent / 任意 Profile / 任意 IDE），就从这里起步，再回到 `00-INDEX.md` 选工作线。

---

## 一、四件事是什么（人话版）

| 名字 | 一句话 | 形态 |
|------|--------|------|
| **知识树 Knowledge Tree** | "这个项目里所有重要东西 + 它们怎么连" | `KNOWLEDGE-TREE.md`（叙事） + `tree.yaml`（图） + 各文件 frontmatter（节点元数据） |
| **记忆 Memory** | "我们做过什么、踩过什么坑、当前事实是什么" | 用户层 `~/.hermes/memories/{MEMORY,USER}.md` + 项目层 `MEMORY-PROJECT.md` + 实体关系库 `entities.yaml` / `relationships.yaml` |
| **梦境 Dream** | "夜里没人看，让系统自己梳理：把今天的事实塞进记忆，把过期的标掉，把不一致的提 PR" | `dream/consolidate.sh`（记忆内化） + `dream/audit.sh`（一致性审计） + `dream/lovart.dream.plist`（launchd 调度）+ skill `lovart-dream-orchestrator`（手动触发） |
| **一致性审计 Audit** | "5 个工具会不会互相打架？CLAUDE.md 让 X 但 Hermes 不让 X？堵路" | `audit/audit-report-{YYYY-MM-DD}.md`（可读报告） + `audit/checks/`（结构化 JSON） |

---

## 二、目录契约

```
1-1 Harness/11-knowledge/
├── README.md                     ← 本文件：架构总览
├── KNOWLEDGE-TREE.md             ← 叙事 SSOT（人读，5 工具启动必读第一章）
├── tree.yaml                     ← 图 SSOT：节点 + 边
├── entities.yaml                 ← 实体库 SSOT（人编辑）
├── entities.jsonl                ← 实体库镜像（机读，1 行 1 实体）
├── relationships.yaml            ← 关系库 SSOT
├── relationships.jsonl           ← 关系库镜像
├── MEMORY-PROJECT.md             ← 项目记忆（项目专属事实，区别于 Hermes MEMORY.md 的全局偏好）
├── queries/                      ← 常用图查询（"X 用到哪些 skill"、"Y 被谁拥有"）
├── scripts/                      ← 工具调用的同步/查询助手
│   ├── kg-query.py               ← 实体 + 关系图查询 CLI
│   ├── sync-to-hermes-memory.sh  ← 反推 ~/.hermes/memories/MEMORY.md
│   └── emit-frontmatter.py       ← 校验所有受管文件带 frontmatter
├── dream/
│   ├── README.md                 ← 梦境使用说明（人调 / cron 调 / skill 调）
│   ├── consolidate.sh            ← 记忆内化（产物 → MEMORY-PROJECT.md + entities.yaml）
│   ├── audit.sh                  ← 5 工具一致性审计（产出 audit/reports/*）
│   └── lovart.dream.plist        ← macOS launchd 调度（每天 02:30 + 周报前）
└── audit/
    ├── checks/                   ← 结构化 JSON 审计结果
    ├── reports/                  ← 可读 Markdown 报告（含 patch 建议）
    └── README.md                 ← 审计维度清单
```

---

## 三、五工具各自怎么用它

| 工具 | 启动加载 | 写入位置 | 谁来维护一致性 |
|------|---------|---------|--------------|
| **Hermes** | Profile 启动时 hero prompt 引用 `MEMORY-PROJECT.md`；增量事实由 `dream/consolidate.sh` 反推到 `~/.hermes/memories/MEMORY.md` | `~/.hermes/memories/MEMORY.md` (user) + `11-knowledge/MEMORY-PROJECT.md` (project) | dream 同步脚本 |
| **OpenCode** | `opencode.jsonc` `instructions` 加 `1-1 Harness/11-knowledge/README.md` + `KNOWLEDGE-TREE.md` | 同上 | 同上 |
| **Cursor** | 加 rule `.cursor/rules/lovart-knowledge.mdc`，自动 attach 到所有 .md/.ts/.tsx/.json | 同上 | 同上 |
| **Claude** | `1-1 Harness/CLAUDE.md` 顶部加一句"启动先读 11-knowledge/README.md" | 同上 | 同上 |
| **Codex** | `AGENTS.md` 已指向 00-INDEX；扩展为追加 `1-1 Harness/11-knowledge/` 入口 | 同上 | 同上 |

**单一真相**：本目录 (`11-knowledge/`) 是所有工具的入口，工具各自不持有副本。Hermes 全局记忆作为下游缓存（便于跨项目偏好合并）。

---

## 四、运行顺序（新增/修改时如何保一致性）

1. 改文件 → frontmatter 自动校验（`scripts/emit-frontmatter.py`）
2. 改 skill/rule/profile → 手动更新 `tree.yaml` 对应节点 + `relationships.yaml` 边
3. 改"事实/习惯/纠正" → 写到 `MEMORY-PROJECT.md`（项目层）或 `~/.hermes/memories/USER.md`（用户层）
4. 改 5 工具入口配置 → 同步通过 `dream/audit.sh` 触发校验，输出 patch 建议 PR
5. 夜间 `dream/consolidate.sh` 自动：扫描变更 → 入库 → 反推 Hermes → 重生成 JSONL 镜像

---

## 五、什么时候不要这套

- 一次性提问（不写未来代码）：不读这套，直接答
- 用户没说过"会话间记得"：不写入任何记忆层
- 属于产物而不是事实：不进 MEMORY-PROJECT.md / entities.yaml，按 RULES-00 产出路由铁律走 `1-2 Insight/` 或 `Local Dev Output`

---

## 六、详细子文档

- 知识树全貌：`KNOWLEDGE-TREE.md`
- 实体/关系字典：`entities.yaml` / `relationships.yaml`
- 项目记忆细账：`MEMORY-PROJECT.md`
- 梦境使用：`dream/README.md`
- 审计维度：`audit/README.md`
- 跨 Profile 协调：父目录 `00-INDEX.md` + `02-rules/RULES-60-management.md`
