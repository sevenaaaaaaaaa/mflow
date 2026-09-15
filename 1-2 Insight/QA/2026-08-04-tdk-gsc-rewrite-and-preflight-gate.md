# GSC 优先 TDK 真重写 + preflight 门禁 — 2026-08-04

## 结论

1. 按 GSC（2026-05-01～07-22）给合成 TDK 排序后，**96** 篇有点击或曝光≥100 的非英文页已完成真重写并写入 Sanity。
2. language↔TDK 门禁已落地：Python 可运行入口 + Node `tdk-i18n-gate.js`（挂入 anti-slop composite 检查）。fixture 验证可 BLOCK 合成壳。

## GSC 队列

- 合成池 1050 → 有流量 625 → 重写队列 96（clicks>0 或 impr≥100）
- 队列合计约 **600 clicks / 17.3k impressions**（同期非英文落地切片）
- Top：`zh/infinite-chatcanvas-ai-collaboration`（299c）已换成 ChatCanvas 母语标题

## 重写质量分层

| 来源 | 数量 | 说明 |
|------|------|------|
| concept bank 真写 | 49 | 按品类母语标题+描述 |
| vault | 5 | 本地成稿 |
| generic 产品化 | 42 | 有目标语言脚本与卖点句，弱于 bank，但已去合成壳 |

备份：`~/Documents/Lovart Local Dev/Output/QA-Memo/tdk-gsc-rewrite-backup-2026-08-04.json`

## Preflight 门禁

```bash
python3 "1-4 Dev/scripts/preflight_tdk_i18n.py" --file page.json
python3 "1-4 Dev/scripts/preflight_tdk_i18n.py" --ndjson import.ndjson --strict
python3 "1-4 Dev/scripts/preflight_tdk_i18n.py" --sanity --lang zh,ja --limit 200
```

Node SSOT：`1-1 Harness/Skills/03-review/lovart-content-quality-gates/scripts/lib/tdk-i18n-gate.js`  
已接入：`anti-slop-rules.js` → `checkCompositePage`。

BLOCK 码：`TDK_I18N_TITLE` / `TDK_I18N_DESC` / `TDK_I18N_EMPTY`。

## P0 收尾（同日续跑）

- 实扫剩余合成壳清单 **807** → 全量 patch（bank 806 + vault 1，fails 0）
- 备份：`~/Documents/Lovart Local Dev/Output/QA-Memo/tdk-p0-remaining-backup-2026-08-04.json`
- 复扫：`synth_shell_remaining = 0`（非英文 compositePage 3983 篇）
- 非英文页上 `en_boilerplate` 同步为 **0**
- **未做**：bodyJson / 正确 skills 生成流程（P1，另开）

## 仍未覆盖（非本轮 P0）

- 全库 `preflight_tdk_i18n.py --sanity` 仍有 BLOCK（多为英文页 boilerplate、drafts 空字段/脚本错配等），与「合成壳」队列无关
- `lovart.sanity.studio/scripts/preflight-content.js` 主路径仍缺失；以 Python 门禁 + anti-slop 为当前可运行入口
- 正文/结构真重写走落地页 skills，不在本会话
