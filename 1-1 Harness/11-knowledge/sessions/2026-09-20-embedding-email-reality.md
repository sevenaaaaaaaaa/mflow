---
session_date: 2026-09-20
session_topic: "实测澄清: DeepSeek 无 embeddings；邮件改走本机 postfix；RAG 用 LLM 重排 + 语料补充规则/技能"
session_slug: "embedding-email-reality"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, console.py RAG, deploy/sync.sh]
agents: [opencode]
duration_min: 70
files_changed_count: 3
schema_bumps: 0
status: ready
---

# Context
- 用户问：之前给的 DeepSeek API 能否用于 embedding？服务器邮箱配置是否够用？

# Findings（实测，非推断）
1. **DeepSeek 无 embeddings**：`GET /v1/models` 仅 `deepseek-flash` / `deepseek-v4-pro`；`POST /v1/embeddings` 对任何模型名均 **404** → 该 key 无法做向量。
2. **服务器邮件**：postfix 运行中（:25），`mydestination` 空 = 纯外发；`/usr/sbin/sendmail` 可用。此前 MFlow 只实现了"远程 SMTP"模式，未接本机发送。全站无任何 SMTP 凭证（learnflow 的 SMTP 表单为空）。

# Solution（用已有资源）
1. **邮件走本机 sendmail**：`email_send` 在未配置 SMTP 时调用 `/usr/sbin/sendmail -t -i -f`；`email_cfg` 默认 `enabled=true, tls=sendmail`；离线通知不再因"未配置"跳过。实测 `已通过本机 sendmail 投递`。
2. **RAG 用现有 DeepSeek 做 LLM 重排**（无需 embedding）：`rag_rerank()` 对词法召回 Top-20 用对话模型重排到 Top-k；`rag_search_smart()` 串联；`semantic_search`/`/api/rag/search`/MCP 默认启用（可 `rerank=0` 关）。
3. **语料补充**：此前只索引 KB+记忆+实体 → 质量类问题召回不到规则。现把 **harness RULES-*.md 分块 + Skills** 纳入（1,430 → **1,538 块**）。
4. 实测：`发布前要检查什么` → **RULES-30 发布前检查清单** + `skill lovart-sanity-preflight`；`语言规范` → RULES-80 + i18n 词表；重排对同查询改变了排序顺序（生效）。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | _sendmail_send + email_send 本机回退 + email_cfg 默认 + rag_rerank/rag_search_smart + 语料补 rules/skills |

# Decisions Made
- D1: 不再等 embedding Key——用"词法召回 + LLM 重排"达到可用的语义效果，成本复用现有对话模型。
- D2: 邮件默认本机 sendmail（零凭证）；SMTP 作为可选增强。
- D3: RAG 语料必须含规则与技能，否则"质量类提问"永远召不回正确答案。

# Patterns Observed
- P1: "有没有能力"要实测（/models、/embeddings、:25 端口、sendmail），不要凭印象。
- P2: 检索质量的第一瓶颈常是**语料覆盖**，不是向量模型。
- P3: LLM 重排是小语料下的高性价比语义方案（无需新依赖/新厂商）。

# Open Questions
- Q1: 是否给重排加缓存（同查询复用）以降延迟/成本？
- Q2: 是否补全 RULES/技能后同步更新 rag-plan.md 的"能力边界"表？

# Cross-References
- decisions: docs/rag-plan.md
- related sessions: 2026-09-20-mcp-open-selfevolve-opc.md

# Tags
- relevant-tags: #embedding #deepseek #email #sendmail #rerank #rag
