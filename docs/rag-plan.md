# RAG / 知识库向量化 方案

> 状态：**底座已落地（2026-09-19）**；真实 embedding 待配置 Key。
> 原则：不假装做 RAG——先说清能力边界，再给可插拔方案。

## 一、现状（已实现）

- **语料**：知识库（按标题分块）+ 项目记忆（288 条事实）+ 实体图谱（98 个）= **1,432 块**，构建耗时 ~2s。
- **可插拔 embedding**：
  - 已配置 → 走远程 `/embeddings`（OpenAI 兼容）。
  - 未配置 → **本地稀疏 TF-IDF 余弦**（字符 bigram/trigram + 词，带语料 IDF，零依赖）。
- **混合检索**：关键词（现有意图路由打分）+ 向量（RRF 融合）→ 透明接入 `kb_search_for_ai` / `ai_context` / Agent；索引缺失时退化为纯关键词，**无回归**。
- **接口**：`GET /api/rag/status`、`GET /api/rag/search`、`POST /api/rag/build`；Agent 工具 `semantic_search`。
- **UI**：知识中台顶部「检索底座」卡（后端/分块/时间/配置提示 + 重建）；搜索框旁「语义」开关；结果展示 来源·栏目·片段·相关度。
- **存储**：`run/rag/index.json`（含 `scheme` 版本，方案变更即全量重建；增量按内容哈希）。

## 二、诚实的边界

| 能力 | 本地 TF-IDF（当前兜底） | 真实 embedding（待配） |
|---|---|---|
| 关键词/近邻词命中 | 好 | 好 |
| 同义/改述（"怎么避免AI味" → anti-slop） | **弱** | 好 |
| 跨语言（中文问 → 英文文档） | 弱 | 好（多语言模型） |
| 成本 | 0 | 按量计费 |
| 依赖 | 无 | 一个 API Key |

**重要判断**：对 Agent 检索质量提升最大的往往不是 embedding 本身，而是 **分块 + 元数据 + 重排**（已做分块与来源元数据；重排可后续加）。

## 三、如何开启真实向量（一步）

在服务器 `run/llm.json` 增加：
```json
"embedding": {"provider":"siliconflow","base":"https://api.siliconflow.cn/v1","key":"sk-...","model":"BAAI/bge-m3","dim":1024}
```
可选后端（任一 OpenAI 兼容 `/embeddings`）：
- 硅基流动 BGE-M3（中文强、便宜）
- 阿里 DashScope text-embedding-v3
- 智谱 embedding-3
- OpenAI text-embedding-3-small
- 本地 Ollama（`http://127.0.0.1:11434/v1`, `nomic-embed-text`）——注意服务器仅 2GB 内存

配置后：知识中台 → 「重建索引」→ 状态显示「远程向量 · <模型>」，语义质量显著提升。

## 四、为什么不建向量库 / 不做全量 17.5k 向量

- 规模：1.4k 块（KB+记忆+实体）→ 内存余弦足够；内容库 17.5k 只索引标题/摘要。
- 引入 FAISS/Milvus/pgvector 会带来运维负担，而当前瓶颈不在此。
- 触发升级的信号：语料 > 10 万块 或 需要多租户隔离时，再上 **sqlite-vec**（单文件、零运维）。

## 五、后续（按性价比）

1. **重排（rerank）**：向量召回 Top-20 → 用 LLM 或交叉编码器重排 Top-5（配置真实 embedding 后收益最大）。
2. **内容库摘要索引**：为 17.5k 页面生成一句话摘要并嵌入，供"找参考页"。
3. **引用回写**：把 Agent 实际引用过的知识块记入 `run/rag/usage.jsonl`，形成"知识被使用度"，反哺 KB 清理与补充。
4. **自动增量**：KB/记忆变更后自动重建（当前手动/定时可调）。
