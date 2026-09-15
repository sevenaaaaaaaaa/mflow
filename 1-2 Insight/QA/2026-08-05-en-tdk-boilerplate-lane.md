# 英文落地页 TDK boilerplate 车道 — 2026-08-05

> 谁会读：内容 / SEO / 发布  
> 为什么现在读：非英文合成壳 P0 已清零；全库 preflight 剩余红灯几乎全在 EN  
> 读完改变什么：英文问题拆成「真套话重写」与「门禁误伤」两条线，按 GSC 开干  
> 下一步：先修门禁 EN 误伤 → 按流量重写 Create professional 队列

## 结论

英文侧 **不是**「drafts 空字段大爆炸」。`--sanity --lang en` 实扫：

| 指标 | 值 |
|------|-----|
| EN compositePage | 1438 |
| BLOCK 页 | **944** |
| 原因 | `en_boilerplate` **944**；`wrong_script` **1**（内部预览页）；`empty` **0** |
| 字段 | 几乎全是 `description` / `seo.description`（title 基本干净） |

其中 **~900 篇** 是真问题：`Create professional {slug 词} with Lovart's AI Design Agent` 一类 slug 填空。  
另有 **~40 篇** 是门禁误伤：正文正常，但命中 `from Text` / `in seconds with` 等过宽子串（例如 `nano-banana-free` 的 “Generate images from text”）。

## GSC 优先级（2026-05-01～07-22）

数据：`~/Documents/Lovart Local Dev/Output/QA-Memo/tdk-en-boilerplate-gsc-priority-2026-08-05.json`

| 队列 | 页数 | 备注 |
|------|------|------|
| clicks>0 或 impr≥100 | **651** | 合计约 5.2 万 clicks / 561 万 impressions（按页累加，同 slug 多文档会重复计流量） |
| clicks≥10 | **~200** | 建议 P0 真重写 |
| 长尾 | **293** | 产品化去套话即可 |

TOP 真脏样例：`text-to-image-generator`、`video-generator`、`edit-ai-generated-images`、`veo3.1`、`free-ai-illustration-generator` —— description 仍是 Create professional 填空。

## 修复车道

### A. 门禁（防误伤，当天做）

- **非英文**：维持完整 `EN_BOILER`（抓 EN 壳）
- **英文**：只 BLOCK 真套话：`Create professional` / `Professional Design Tool` / `Design Tool | Lovart`  
  不再用 `from Text`、`in seconds with`、`Free to Try` 误伤正常英文营销句  
- `with Lovart's AI Design Agent`：非英文仍 BLOCK；英文降为仅当整句是短模板时再拦（首批可先不拦，靠内容车道清 Create professional）

### B. 内容 P0（真重写）

1. 队列 = description/seo.description 以 `Create professional` 开头（或等价填空）的 EN 页  
2. 先写 **clicks≥10**（~200）→ 再写其余 traffic → 最后长尾批量  
3. 写法：卖点句 + 能力 + Lovart 动作；**禁止** Create professional / AI Design Agent 尾缀套话  
4. `description` 与 `seo.description` 同步（771 页双字段同脏）  
5. Sanity：`--missing` 不适用已有文档 → **patch**；先 backup JSON，dry-run 再 apply

### C. 明确不做（本轮）

- bodyJson 正文重写（另有 body 错配线，P0 高流量已修过）  
- 删 production 文档  
- 用放宽门禁代替重写 900 篇 Create professional

## 验收

1. `preflight_tdk_i18n.py --sanity --lang en`：`Create professional` 类 BLOCK = 0  
2. 高流量抽样 20 篇：描述可读、含具体能力、无 slug 填空感  
3. 非英文 `en_boilerplate` 复扫仍为 0（门禁改动不得回潮）

## 执行进度（同日）

| 步骤 | 结果 |
|------|------|
| 摸底 | 944 页 BLOCK → 几乎全是 description 套话 |
| 门禁收窄 | EN 页不再用 `from Text` / `in seconds with` 误伤；真套话仍 BLOCK |
| P0 clicks≥10 | **183** 篇 patch（vault 154 + productized 29），fails 0 |
| 剩余全量 | **720** 篇 patch（vault 349 + productized 371），fails 0 |
| 终扫 | EN `en_boilerplate` = **0**；仅剩 1 页 `wrong_script`（`internal-section-gallery-preview` 内部中文预览，非正式流量） |
| **高流量精修** | clicks≥50 共 **93** 文档：wave1 **53** + wave2 **40** + short-video **2** 补丁；手写级 description 覆盖完毕 |
| **Title 精修** | 弱 title 787 → 清零严重项；见下方 Title 车道 |

备份 / 结果：

- `~/Documents/Lovart Local Dev/Output/QA-Memo/tdk-en-boilerplate-gsc-priority-2026-08-05.json`
- `tdk-en-boilerplate-p0-backup-2026-08-05.json` / `…-p0-patch-result-…`
- `tdk-en-boilerplate-remaining-backup-2026-08-05.json` / `…-remaining-patch-result-…`
- `tdk-en-preflight-final-2026-08-05.json`
- `tdk-en-desc-craft-workset-2026-08-05.json` / `tdk-en-desc-craft-backup-…` / `tdk-en-desc-craft-wave2-…`
- `tdk-en-title-weak-audit-2026-08-05.json` / `tdk-en-title-craft-*` / `tdk-en-title-wave2-*` / `tdk-en-title-cleanup3-*`

### 质量分层（诚实口径）

- **vault 优先**：有母稿且过门禁的 description 直接回填（质量高于填空）
- **productized**：按品类 hook 生成去套话描述（过门禁、可索引，但不是专栏级终稿）
- **craft（clicks≥50）**：按 slug 手写能力句（模型名 / Touch Edit / 无绿幕等具体差异）+ 禁用词自检；`description` 与 `seo.description` 同步
- **title craft**：关键词前置 + 差异点 + `| Lovart`；同步 `title`/`seo.title`；禁 Agent 尾缀 / Ai Title Case / Create professional / 禁用词
- **未做**：bodyJson / 故事线真重写；**其他语言 title** 待 EN 稳定后再开

## Title 车道（同日续）

### 摸底

| 口径 | 值 |
|------|-----|
| EN 页 | 1438 |
| 弱 title | **787**（bare 464 / too_long 255 / agent_tail 132 / slug_titlecase 99 …） |
| P0 clicks≥50 | **64**（另补漏网高流量如 `text-to-image-generator`） |
| P1 clicks 10–49 | **88** |

### 执行

| 波次 | 篇数 | 做法 |
|------|------|------|
| P0+P1 | **182** | 高流量手写 craft + 其余 auto 去尾缀 |
| wave2 严重项+光秃 | **634** | 清 agent_tail / generic_tail / bare（含长尾） |
| cleanup | **138+6** | Create professional 残渣、超长截断、**3 个 EN 挂法文 title** |

### 验收（终态）

- 严重项（agent_tail / Create professional / Ai Title Case / banned / generic Design Tool 尾缀）≈ **0**
- too_long ≈ **0**
- 高流量样例：`Text Image Generator` → `AI Text to Image Generator — Free, Editable | Lovart`；`Veo3.1` → `Veo 3.1 AI Video Generator — Realistic Motion | Lovart`
- 顺带修了 EN 文档误挂法文 title（store graphics / restaurant email / worksheet）

### 进步空间（已看到）

- feature/tool 同 slug 双文档 title 已对齐，但 URL 去重/合并是另一条线
- **非英文 title** 下一轮再开（用户确认 EN 完成后再做）

## Title 个性化方案（纠正品类卖点库）

### 问题

品类卖点库轮换（`Export Campaign Sets`×103 等）= **AI 模板痕迹 + 近似页标题撞车**，对 SERP/列表都有害。

### 原则（现行）

1. **禁止共享卖点库** — 同一 benefit 句不得批量复用  
2. **个性化信号优先级**  
   - 高流量：手写 craft（保留）  
   - slug 自带差异：`for TikTok` / `No Watermark` / `Free` → 写进主标题，不另挂万能半句  
   - 否则：从**该页自己的 description** 压 3–5 词完整角度（不截半句）  
   - 再否则：干净 `AI {具体关键词} | Lovart`，宁可不挂卖点也不撞车  
3. **验收**：benefit 一次性占比高；`Free to Try` 类伪个性化 = 0；半截句 ≈ 0  

### 执行

| 波次 | 结果 |
|------|------|
| personalized v1 | 1158 篇去银行库；撞车从 646 页骤降 |
| personalized v2 | 678 篇：修半截句、收回高流量手写、`for-X` 折叠进主标题 |

备份：`tdk-en-title-personalized-*` / `tdk-en-title-personalized-v2-*`

## 关联

- 前序非英文合成壳收尾：`2026-08-04-tdk-gsc-rewrite-and-preflight-gate.md`  
- 门禁脚本：`1-4 Dev/scripts/preflight_tdk_i18n.py` + `tdk-i18n-gate.js`
