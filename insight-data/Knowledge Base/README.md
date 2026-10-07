# Lovart Knowledge Base

> KB = source-of-truth for all Lovart content. **All blog/landing-page writers must query KB before writing.**

## 4-layer architecture

```
Layer 0  sources/       raw .md / .docx / .html / json
Layer 1  kb-doc files   ≈35 units, all frontmatter'd by kb-frontmatter.py
Layer 2  atomic claims  (planned v0.3)
Layer 3  KB-Index/      by-topic.md / citations.md / capability-glossary.md (auto-gen)
```

## Quick navigation

| 你想 | 看 |
|------|------|
| 理解 schema | `KB-SCHEMA.md` |
| 看 topic × 各 KB unit 表 | `KB-Index/by-topic.md` |
| 看每个 capability = 哪些 URL | `KB-Index/capability-glossary.md` |
| 看每个 URL = 哪些 KB units | `KB-Index/citations.md` |
| 加新 URL 进 KB | `Changelog/URL-LIST.md` 或 `Reference/URL-LIST.md` |
| 重 build 索引 | `scripts/build-index.py --write` |

## 当 writer profile 启动时，硬性顺序

```
1. 解析 topic
2. bash scripts/kb-mine.py --root <vault> --topic "<topic>"     ← KB context
3. 拼 brief = topic description + KB context (capability hits + URLs)
4. dispatch hermes/opencode writer with brief + KB context
5. writer 输出 → quality cascade MUST-CITE-KB BLOCK check
6. cascade 中 critic 阻 BLOCK → rewrite + 再 mine → 再 write
```

如果 KB 没命中 → escalate 或 warn；**不**让 writer 编。

## Slot 等用户填

```
insight-data/Knowledge Base/Changelog/URL-LIST.md       ← 用户给 changelog / news / release notes URL
insight-data/Knowledge Base/Reference/URL-LIST.md       ← 用户给 Lovart 内部 doc 交叉引用 URL
```

填完运行：

```bash
python3 scripts/kb-ingest.py --root <vault> --allow-fetch
python3 scripts/kb-frontmatter.py --root <vault>
python3 scripts/build-index.py --root <vault> --write
```

## 待清

✅ 已清理（2026-07-05）：`insight-data/Knowledge Base/.venv/` 22 MB docx→md 工具链已删。KB 根从 22 MB → 636 KB。
任何 .docx 重装指引：`~/Documents/Lovart Local Dev/lovart-kb-venv` 跑 `uv venv` + `pip install mammoth python-docx`。完整说明看 `scripts/kb-ingest.py` `html_to_md()` 注释。
