## 会话汇总（2026-08-02/03）

### 一、换行污染 — 已清零
DE/FR/ES/PT/RU/IT/KO 七语 `span.text` 首尾 `\n` / `\n{3,}` 已用安全脚本清完；全量复扫 **dirty=0**。
脚本：`~/Documents/Lovart Local Dev/scripts/active/fix_blog_newlines.py`（完整 body、只改 text、完整性门禁）。

### 二、CTA 空壳 — 已回填
旧残缺投影整表覆写导致 CTA 丢 `link`。

| 批次 | 结果 |
|------|------|
| 兄弟语言/slug 回填 | **1306 篇 / 1311 CTA** |
| 残留 + 默认 CTA 兜底 | **+128 篇**（其中 101 用 `Try Lovart Free →` → lovart.ai） |
| 终态 | 7 语 **ctaBad≈0**（见当日复扫） |

脚本：`fix_blog_cta_from_siblings.py`（只改 `_type==cta` 且无 link 的节点；`--default-cta` 兜底）。

### 三、tableBlock 空壳 — 未动（有意）
约 **848** 篇 `tableBlock` 无 `rows`。
- Sanity history（Jul 28 前）已无 rows
- 抄 EN 会把英文表塞进非英语正文 → 违反 i18n
- 正确做法：从**同语言本地 MD** 重转 table 节点后 path-patch

### 四、防复发 / 根因
- `md_to_portable_text.py` 常规段落已 `strip()` + 空格合并，**不是**主污染源；直写/历史 patch 路径才会注入
- 已在 `validate_portable_text_body()` 加 **AB-NEWLINES** 门禁：非 code span 若含首尾 `\n` / `\n{3,}` / 内嵌 `\n\n` → BLOCK（`validate_pt_body.py` 自动吃到）

### 五、仍待做
1. **tableBlock 同源重建**（本地 MD → 只补 rows）
2. 约 25 篇中段有意 `\n\n` 人工判别（换行脚本刻意不压）
3. 恢复/重建缺失的 `preflight-content.js` Studio 入口（文档路径目前不存在；Python 校验已顶上）
