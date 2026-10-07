# 落地页正文语种全站扫描 — 2026-08-05

> 谁会读：内容 / SEO / 发布  
> 为什么现在读：落地页语种门禁已清零；机翻稿需后续人工/编辑重写  
> 读完改变什么：语种 BLOCK 已过；质量仍是 `gt_machine` 门禁级  
> 下一步：按栏目把机翻稿升级为编辑稿；Blog 另走 signal-writer

## 结论

全站 production `compositePage` **4992** 篇扫描后：

- **Lane A（EN 错挂）**：**115 → 0**（已修，复核 FAIL=0）
- **Lane B（EN 壳/错脚本）**：**653 → 0**（有源 119 + 机翻 534，终核 FAIL=0）
- 正常：**4217**；正文过短跳过：**7**

不分流量优先级；P0（GSC≥100）28 篇已于 2026-08-04 修完。

## Lane A 分因（修复前）

- en_body_is_ja：51 · en_body_is_ko：39 · en_body_is_fr：15 · en_body_is_ru：9 · en_body_is_zh：1

## Lane B 主因（修复前 Top）

- pt_en_shell 158 · zh_en_shell 118 · de_en_shell 99 · it_en_shell 97 · fr_en_shell 94
- ru_en_shell 27 · ko_en_shell 14 · zh_body_is_ja 11

## GT 说明

GT = Google Translate 机翻。用户 2026-08-05 授权对 Lane B 无源队列用机翻**先过语种门禁**。写入标记：`method=gt_machine` / `quality=gate_pass_machine`。不是栏目终稿。

## 数据

`~/Documents/Lovart Local Dev/Output/QA-Memo/landing-body-lang-fullscan-2026-08-05.json`

## 修复进度

### Lane A EN 错挂 — 115/115 已修，复核 FAIL=0

- 方法：vault EN / 干净 EN twin / `structural_en_minimal`（非 GT）
- 产物：`laneA-en-fix-results-2026-08-05.json`、`laneA-en-verify-2026-08-05.json`

### Lane B — 有源 119 + 机翻 534 = 653 清零

- 有源覆盖：`laneB-fix-results-2026-08-05.json`
- 机翻批次（授权）：**534/534 FIXED**，终核 **FAIL=0**
  - 首轮 532 FIXED + 2 ERROR（网络）；补跑修完
  - 8 篇 zh/zh-TW 首轮混入日文（`ja_contam`），改从干净 EN twin 重翻后 PASS
  - 语言分布：pt 145 · it 94 · fr 91 · de 84 · zh 53 · zh-TW 44 · ru 15 · ko 7 · ja 1
- 产物：`laneB-gt-results-2026-08-05.json`、`laneB-gt-verify-final-2026-08-06.json`、`laneB-gt-retry-2026-08-06.json`

### 门禁

- `body-i18n-gate.js` 已接入 `checkCompositePage`（`BODY_I18N_EN_WRONG` / `BODY_I18N_EN_SHELL` → BLOCK）
