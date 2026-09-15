# 2026-08-07 Tools 路由与壳队列 SSOT

## 路由统一结论（勿再混用）

| 层 | 正确值 | 错误/历史 |
|----|--------|-----------|
| **URL 路径** | `/tools/{slug}`（复数） | 无 `/tool/` |
| **Sanity `pageType`** | `tool`（单数） | `tools` 计数=0，禁止新写 |
| **JSON `category`** | `tool` | — |
| **`sourceType`** | 建议补 `tools`（与 Features=`features` 对称）；现状 Tools 全为 null | 勿写成 `tool` |
| **`_id` 规范** | `tools-{slug}-{lang}` | `tool-*` / UUID 为历史债，新写禁止 |

前端查询 `/tools/*` 必须：`_type=="compositePage" && pageType=="tool" && slug.current==$slug && language==$lang`。禁止只 match `_id match "tools*"`（会漏 UUID/`tool-*`），禁止 Features 同 slug 抢答。

## 壳队列核实（纠正「475」）

| 口径 | 数量 | 说明 |
|------|------|------|
| 宽匹配 `Professional Creative Tool` OR `Generate professional` | 723 | 含大量误报 |
| **严格 CLASSIC_SHELL**（hero 含 `Professional Creative Tool`，或 `Generate professional … in seconds with AI`，或 Four ways+该短语） | **148** | 全是 **en** |
| 今日已改（TDK/其他会话） | 排除 | 队列用 `_updatedAt < 2026-08-07` |
| 线上抽查 | 20/20 LIVE_SHELL | Sanity=线上=真壳，可重写 |

清单：`~/Documents/Lovart Local Dev/Output/QA-Memo/tools-classic-shell-verified-2026-08-07.json`

## 与「Tools TDK」会话的隔离

- 对方今日主要动 **ko/zh-TW/ru** 等 + 少量 EN pilot（与本 148 slug **零重叠**）。
- 本队列只 patch **上述 148 个 `tools-*-en`** 的 **bodyJson + 整页 TDK**（门禁要求整页重写，不能只改壳留烂 TDK）。
- 不同时改 Features 差异化文案（另会话 diversify Features）；Tools 修好后若 Features 仍是壳，再 Tools→Features 同步防 SSR 闪回。

## 重写规范

父入口：`lovart-landing-page` → composite-v2 **T-long**（对齐 golden `ai-logo-generator-en` 12 段）。门禁：`preflight_tools_page_rewrite.py --strict` BLOCK=0 才 patch。

## 执行记录（本会话）

- 生成器：`~/Documents/Lovart Local Dev/Output/QA-Memo/tools-classic-shell-rewrite-2026-08-07.py`
- 产物 JSON：`.../tools-shell-rewrite-batch-2026-08-07/` + `1-3 GenFlow/Page Gen/Pages/Tools/en/`
- **148/148** EN CLASSIC_SHELL 已 patch（`pageType=tool`，补 `sourceType=tools`，整页 bodyJson+TDK）
- 队列复核：`still_emdash=0 / cleared=148`
- 另同步 **56** 篇仍含壳短语的 Features EN 双胞胎（防 `/tools/` SSR 闪回）；样例页 Tools+Features Sanity hero 均已非壳
- 库内宽匹配 `— Professional Creative Tool` 仍可能 >0（其他非本队列页/弱匹配）；本队列已清零
- 线上抽查仍可能见旧 H1：**CDN/ISR**。Sanity 已新、curl 仍旧壳 → purge `/tools/*` 或等 TTL
