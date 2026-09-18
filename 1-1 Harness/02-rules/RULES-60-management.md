---
type: rule
version: 2.0
updated: 2026-07-05
scope: "profile-management-active"
tools: [hermes, opencode, claude]
status: active
path: 1-1 Harness/02-rules/RULES-60-management.md
generator: 1-1 Harness/11-knowledge/scripts/fm-fix.py
---
# Lovart RULES — 60 管理类（Management）

> 适用路线：项目管理、工程管理、知识管理、Hermes 优化
> 加载 Profile：`lovart-management`

---


## 一、硬条款（违反即 BLOCK）

1. **必须**每个会话结束时写 session log（1-1 Harness/11-knowledge/sessions/）
2. **必须**每个会话结束后跑 harness_sync（skills → 运行时同步）
3. **禁止**在 session 中跳过 session-init 门禁
4. **必须**定期归档 60 天以上的会话日志（降噪）
5. **必须**保持 00-INDEX.md 与磁盘实存一致
6. **禁止**在 11-knowledge/sessions/ 之外的目录写会话日志
7. **必须**用 MEMORY-PROJECT.md 做项目记忆的 SSOT
8. **禁止**绕过 Knowledge Graph 直接改 entities.yaml

## 二、参数表

### 会话管理

| 文件 | 用途 |
|------|------|
| 00-INDEX.md | Harness 主索引 v3.1 |
| 11-knowledge/sessions/*.md | 会话日志（每天归档） |
| 11-knowledge/MEMORY-PROJECT.md | 项目记忆 SSOT |
| 11-knowledge/KNOWLEDGE-TREE.md | 知识树 |
| 11-knowledge/audit/reports/ | 梦境审计报告 |

### 知识库治理

| 项 | 频率 | 负责人 |
|---|------|--------|
| 降噪治理 | 每日 03:20 自动 | MFlow housekeeping |
| session 归档 | >60 天自动 | housekeeping |
| 规则更新 | 按需 | 人工确认 |
| 模板更新 | 按需 | 人工确认 |
