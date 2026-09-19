---
session_date: 2026-09-19
session_topic: "RAG 向量化底座（可插拔 embedding + 本地 TF-IDF 兜底 + 混合检索）+ 知识库可视化重构"
session_slug: "rag-foundation-kb-ux"
profiles_used: [profile-lovart-management]
tools_used: [console.py, console.html, docs/rag-plan.md, ego-browser, deploy/sync.sh]
agents: [opencode]
duration_min: 120
files_changed_count: 4
schema_bumps: 0
status: ready
---

# Context
- 用户提出：知识库可视化体验一般；知识库没有 RAG 向量化，"打算怎么办"。
- 服务器约束：仅 DeepSeek Key（无 embeddings 接口）、2GB 内存/3 核（本地模型风险高）。

# Solution
1. **RAG 底座（可插拔 + 兜底）**：
   - `rag_build()`：知识库按标题分块 + 记忆事实 + 实体 → 1,432 块（~2s）；`scheme` 版本控制，方案变更全量重建，否则按内容哈希增量。
   - `embed_texts()`：配了 `llm.json.embedding` → 远程 `/embeddings`；否则 **本地稀疏 TF-IDF 余弦**（字符 bigram/trigram + 词 + 语料 IDF + L2 归一），取代最初的哈希向量（哈希碰撞伤语义）。
   - `rag_search()`：稀疏/稠密点积检索。
   - **混合检索**：`kb_search_for_ai` 用 RRF 融合关键词与向量召回；索引缺失退化为纯关键词（无回归）。
   - 接口 `GET /api/rag/status|search`、`POST /api/rag/build`；Agent 工具 `semantic_search`。
2. **知识库可视化重构**：页面改为「左筛选（知识源+项目专属源）+ 右结果（宽栏）」；顶部「检索底座」卡显示 后端/分块/时间/配置提示 + 重建；搜索加「语义」开关；结果展示 来源·栏目·片段·相关度。
3. **文档** `docs/rag-plan.md`：能力边界表、开启真实向量的一步配置、为何不建向量库、后续 rerank/摘要索引/引用回写。

# Files Changed
| 路径 | 操作 | 备注 |
|------|------|------|
| `1-4 Dev/console/console.py` | modify | rag_cfg/rag_build/_corpus_idf/local_embed(稀疏TFIDF)/remote_embed/rag_search/rag_status/hybrid in kb_search_for_ai/端点/semantic_search 工具 |
| `1-4 Dev/console/console.html` | modify | KB 页布局重构 + RAG 状态卡 + 语义搜索 |
| `docs/rag-plan.md` | add | RAG 方案与边界 |

# Decisions Made
- D1: 不假装做 RAG——未配 embedding 时用**诚实且有用**的 TF-IDF，而非哈希伪向量。
- D2: 混合检索（RRF）而非替换关键词，保证无回归。
- D3: 不引入向量库：当前 1.4k 块内存余弦足够；>10 万块再上 sqlite-vec。
- D4: `scheme` 版本控制索引，避免方案变更后向量与检索算法不匹配。

# Patterns Observed
- P1: 哈希向量（hashing trick）在缺少训练时语义能力反而差于 TF-IDF；兜底应选可解释的词法方案。
- P2: JSON 往返会把 dict 的 int 键变字符串，向量点积必须统一键类型。
- P3: 增量复用必须以"向量方案版本"为条件，否则换方案后仍复用旧向量。
- P4: 布局是"可用性"的一部分——结果列表被挤进 240px 窄栏即等同不可用。

# Open Questions
- Q1: 真实 embedding 选型（硅基流动 BGE-M3 / DashScope / 智谱）与预算？
- Q2: 是否加 rerank（LLM 或交叉编码器）？
- Q3: 内容库 17.5k 是否做摘要索引？

# Cross-References
- entities: ds-knowledge-base
- decisions: docs/rag-plan.md
- related sessions: 2026-09-19-p1-1b-memory-review-ui.md

# Tags
- relevant-tags: #rag #embedding #hybrid-retrieval #tfidf #kb #ux
