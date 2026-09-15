# Sanity 发布参考实现（Lovart 生产在用）

参考 skill：`1-1 Harness/Skills/04-publish/lovart-sanity-publish/SKILL.md`

要点（即铁律）：
1. preflight BLOCK=0 前置（lovart-content-quality-gates）
2. 正文转 Portable Text：`~/Documents/Lovart Local Dev/scripts/md_to_portable_text.py`（表格 string-cell schema）
3. NDJSON 磁盘流式写入，正文不进 LLM 上下文
4. `npx sanity dataset import --missing` 增量导入（禁 --replace / 禁 deploy）
5. Blog 日期双写：releaseDate + publishedAt 必须一致
6. 导入后 verify（L2）：GROQ 抽查文档存在性与字段完整性
