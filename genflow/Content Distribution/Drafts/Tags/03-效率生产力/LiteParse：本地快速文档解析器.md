---
title: "LiteParse：本地快速文档解析器"
slug: liteparse-local-document-parser
date: 2026-06-02
updated: 2026-05-29
tags: [LiteParse, PDF解析, OCR, RAG, LlamaIndex, Rust, AI工具]
categories: [AI工具]
summary: LiteParse 是 run-llama 开源的本地文档解析器，Rust 核心约 8.9k star，专注 PDF/Office/图片快速抽取带边界框文本，内置 Tesseract OCR，提供 lit CLI 与 Python/Node/WASM 绑定；适合 RAG 与 Agent 流水线，复杂版式可升级云 LlamaParse。
focus_keyword: LiteParse
source: https://github.com/run-llama/liteparse
author: run-llama（LlamaIndex）
status: draft
---

# LiteParse：本地快速文档解析器

> 约 8.9k GitHub stars | Apache 2.0 | Rust 核心 | 全本地、无云依赖 | 官方文档：https://developers.llamaindex.ai/liteparse/

## 这是什么

[LiteParse](https://github.com/run-llama/liteparse) 是 LlamaIndex 团队（`run-llama`）维护的**独立开源文档解析工具**，定位是「又快又轻」：用 PDFium 做空间文本解析，输出带 **bounding box** 的 JSON 或纯文本，不捆绑专有 LLM、也不要求云端 API，一切在本地机器完成。

与同类「重云、重模型」方案相比，LiteParse 明确只做**高质量空间文本 + 可选 OCR + 页面截图**，把复杂表格、多栏、手写、扫描件等难例留给商业云产品 [LlamaParse](https://developers.llamaindex.ai/python/cloud/llamaparse/)（README 中直说本地解析到顶后应上云）。

输入除 PDF 外，还支持通过 LibreOffice / ImageMagick **自动转 PDF** 再解析：Word、PPT、Excel、常见图片等。OCR 默认内置 **Tesseract**（零配置），也可挂 HTTP OCR 服务（EasyOCR、PaddleOCR 或自研，遵循 `OCR_API_SPEC.md`）。另提供 `lit screenshot` 为高 DPI 页面截图，方便 LLM Agent 读取版式与图表。

> **版本说明**：当前仓库主分支为 V2；旧版 V1 代码在 `logan/liteparse-v1` 分支。

## 适合谁 / 不适合谁

| 人群 | 是否推荐 | 原因 |
|------|----------|------|
| 搭建本地 RAG / 知识库流水线 | ✅ 推荐 | 本地 JSON/文本 + bbox，易切块入库 |
| 需要 Agent 读 PDF 且要页面截图 | ✅ 推荐 | `lit screenshot` 专为视觉信息设计 |
| 隐私 / 离线 / 不想文档上云 | ✅ 推荐 | 无云依赖；可用 `TESSDATA_PREFIX` 离线 OCR |
| Python / Node / Rust / 浏览器 WASM 多栈团队 | ✅ 推荐 | 官方多语言绑定与统一 `lit` CLI |
| 批量处理目录内 Office/PDF | ✅ 推荐 | `lit batch-parse` + 可选 `--recursive` |
| 密集表格、多栏、扫描手写、复杂图表 | ⚠️ 酌情 | README 建议改用 LlamaParse 云解析 |
| 不愿安装 LibreOffice / ImageMagick | ⚠️ 酌情 | 非 PDF 格式需额外系统依赖 |
| 只要 Markdown 美化排版、不做抽取 | ❌ 不推荐 | 见 [[../01-AI-Agent生态/html-anything：AI 时代的 HTML 编辑器]] 等 |

## 安装与前置条件

- **核心**：各语言包均附带同名 CLI `lit`（WASM 包除外）
- **OCR 默认**：Tesseract 已捆绑，一般无需单独安装
- **可选（多格式输入）**：
  - Office → PDF：`LibreOffice`（macOS `brew install --cask libreoffice` 等）
  - 图片 → PDF：`ImageMagick`（`brew install imagemagick` 等）
- **可选（高精度 OCR）**：自建或示例 HTTP OCR 服务（EasyOCR / PaddleOCR）

### 按语言安装

| 语言 | 安装命令 |
|------|----------|
| Node.js / TypeScript | `npm i @llamaindex/liteparse` |
| Python | `pip install liteparse` |
| Rust（CLI） | `cargo install liteparse` |
| Rust（库） | `cargo add liteparse` |
| 浏览器 WASM | `npm i @llamaindex/liteparse-wasm` |

### Agent Skill（可选）

```bash
npx skills add run-llama/llamaparse-agent-skills --skill liteparse
```

或手动复制 [SKILL.md](https://github.com/run-llama/llamaparse-agent-skills/blob/main/skills/liteparse/SKILL.md) 到你的 Skills 目录（可与 [[../01-AI-Agent生态/skills-manage：20+ 平台 Agent Skills 中央统一管理]] 联用）。

## 核心用法

### 单文件解析

```bash
# 默认文本输出
lit parse document.pdf

# JSON 输出到文件
lit parse document.pdf --format json -o output.json

# 指定页码
lit parse document.pdf --target-pages "1-5,10,15-20"

# 关闭 OCR（纯文本 PDF）
lit parse document.pdf --no-ocr

# 远程 PDF（stdin）
curl -sL https://example.com/report.pdf | lit parse -
```

常用参数：`--ocr-language`（Tesseract 语言，默认 `eng`）、`--ocr-server-url`（HTTP OCR）、`--dpi`（默认 150）、`--max-pages`（默认 1000）、`--password`（加密文档）。

### 批量解析

```bash
lit batch-parse ./input-directory ./output-directory
# 可选：--recursive、--extension .pdf、--format json
```

### 为 Agent 生成页面截图

```bash
lit screenshot document.pdf -o ./screenshots
lit screenshot document.pdf --target-pages "1,3,5" --dpi 300 -o ./screenshots
```

文本抽取无法覆盖的图表、版式信息，可配合截图喂给多模态模型（与 [[x-cli：AI Agent 一句话操控网页的 CLI 工具集]]、[[../01-AI-Agent生态/GBrain：AI Agent 的个人大脑层]] 等 Agent 栈思路一致）。

### 库调用

各语言详见仓库内 `packages/node`、`packages/python`、`crates/liteparse` 的 README；浏览器场景用 `@llamaindex/liteparse-wasm`。

### 与 LlamaParse 的分工

| 场景 | 建议 |
|------|------|
| 可提取文本的 PDF、轻量流水线、本地隐私 | LiteParse |
| 复杂版式、扫描件、生产级结构化 Markdown | LlamaParse（云，README 含免费注册链接） |

## 注意事项与风险

- **抓取说明**：本篇基于 GitHub API + `main` 分支 README（2026-06-02）；**未抓取** Twitter/X 原帖正文（t.co 仅重定向到仓库）。Star 数、Issue 数以 GitHub 实时为准。
- **解析上限**：本地 PDFium + Tesseract 对复杂文档质量有限；误判或漏检时需 `--ocr-server-url` 或上云 LlamaParse。
- **系统依赖**：处理 `.docx` / `.pptx` / 图片等需本机 LibreOffice / ImageMagick；Windows 可能需把 LibreOffice 的 `program` 目录加入 PATH。
- **离线 OCR**：设置 `TESSDATA_PREFIX` 或 `--tessdata-path` 指向 `.traineddata` 目录。
- **许可**：Apache 2.0；基于 PDFium、Tesseract 等，商用前请自行核对供应链合规。
- **V1/V2**：链接到旧版 V1 分支的文档或教程可能已过时。

## 与你现有工具的关系

- **知识库 / RAG**：解析 PDF 切块后可导入向量库，与 [[../01-AI-Agent生态/LLM Wiki：让 AI 替你维护个人知识库]] 的「文档进库」环节互补；Obsidian 侧写作仍用本地 Markdown，PDF 源文件用 LiteParse 预处理。
- **Skills 生态**：官方提供 `liteparse` Agent Skill，可与 [[../01-AI-Agent生态/skills-manage：20+ 平台 Agent Skills 中央统一管理]]、[[../01-AI-Agent生态/codex-plusplus：给你的 Codex 装上插件系统]] 一并纳入多 IDE 工作流。
- **内容形态**：[[../01-AI-Agent生态/html-anything：AI 时代的 HTML 编辑器]] / [[../01-AI-Agent生态/html-anything：4.6k 星从 Markdown 到精美 HTML]] 解决「稿 → 发布 HTML」；LiteParse 解决「PDF/Office → 机器可读文本/JSON」，二者不重叠。
- **音视频**：[[../02-内容创作媒体/Buzz：离线 Whisper 音视频转录与翻译]] 处理音轨；LiteParse 处理版式文档，可组成多媒体资料入库管线。
- **编码规范**：仓库提供 `AGENTS.md` / `CLAUDE.md`，与 [[../01-AI-Agent生态/Karpathy 编码行为准则：AI Agent 的 4 条铁律]] 同属「约束 Agent 写代码」类资源，但 LiteParse 侧是**解析工具**而非行为准则。

## FAQ

### Q: LiteParse 和 LlamaParse 必须二选一吗？
A: 不必。README 推荐本地先用 LiteParse 做快速、隐私友好的抽取；遇到复杂文档再切 LlamaParse 云解析，二者同属 LlamaIndex 生态。

### Q: 没有 GPU 能用吗？
A: 可以。默认 Tesseract 在 CPU 上运行；`--num-workers` 可调并发。若接 EasyOCR/PaddleOCR HTTP 服务，性能取决于该服务部署方式。

### Q: 为什么 t.co 链接打不开原文？
A: `https://t.co/EyYpq5Qrh3` 经重定向指向本仓库，**无独立推文正文**被纳入本篇；若需传播语境，请在 X/Twitter 客户端查看原帖（本次未抓取，可能受登录/地区限制）。

## 相关链接

- 官方仓库：https://github.com/run-llama/liteparse
- 文档：https://developers.llamaindex.ai/liteparse/
- 短链来源：https://t.co/EyYpq5Qrh3（→ 上述仓库）
- LlamaParse 云解析：https://developers.llamaindex.ai/python/cloud/llamaparse/
- Agent Skill：https://github.com/run-llama/llamaparse-agent-skills/tree/main/skills/liteparse
- 本库相关笔记：[[../01-AI-Agent生态/LLM Wiki：让 AI 替你维护个人知识库]]、[[../01-AI-Agent生态/skills-manage：20+ 平台 Agent Skills 中央统一管理]]、[[../02-内容创作媒体/Buzz：离线 Whisper 音视频转录与翻译]]
