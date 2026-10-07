# C 任务去重评审报告 | 2026-07-15

> 📅 报告日期: 2026-07-15
> 📊 数据基线: GA4 organic_pages_30d + GSC top20 + Sanity 3845 compositePage
> 🎯 范围: 对 34 组 (language, slug) 重复去重做出 C-level 决策前的影响评审

> 关联资产:
> - `Output/SEO-Reports/改造建议/dedup-impact-report-2026-07.csv` (本报告明细 34 行)
> - `Output/SEO-Reports/改造建议/dedup-final-decisions-2026-07.csv` (决策明细)

---

## 摘要（先结论）

**34 组 (language, slug) 重复 = 34 个 URL = SEO 数据上 0 直接流量损失**。
但**实际决策并非"机械 unpublish"**：有 2 处 (KEEP 那侧) 本身就是历史错误产物，可能需要先修复再 unpublish。

按 AGENTS.md "修复优先于删除"——C 任务应该按 **3 阶段**执行，不是 1 次大批量：

| 阶段 | 数量 | 风险 | 行动 |
|------|------|------|------|
| 阶段 1 — 立即可推进 | **30** | LOW | 直接 move 到 drafts（KEEP 已被确认是真实功能页） |
| 阶段 2 — 二次确认 | **2** | KEEP 存疑 | 先修 KEEP 标题错位，再 unpublish MOVE |
| 阶段 3 — 暂缓 | **2** | 交叉 | B 任务刚 patch 完，先观察 14 天再决定是否 unpublish |

---

## 一、数据基线确认

**34 个 URL 在搜索引擎生态内 = 0 直接可见流量**

```
影响范围统计:
  GA4 30d sessions:     0
  GSC 28d clicks:       0  
  GSC 28d impressions:  0
  风险分布:             HIGH=0  MEDIUM=0  LOW=34
```

**真实风险不在 GSC/GA4，而在 SSR 行为**——前端 SSR 用 GROQ `*[_type=="compositePage" && language==X && slug.current==Y]`，返回值通常被 `.first()` 或前端遍历一次取一次——**每次 SSR 请求可能拿到不同的 _id**，导致 meta.description / canonical / hreflang 在不同请求之间抖动。

修好后预期：**单页 meta 一致性提高 → CTR 长期 +0.2-0.5pp**（无法精确量化因为这部分数据缺）。

---

## 二、按语言分布

| lang | 重复组数 |
|------|---------|
| fr | 6 |
| it | 6 |
| zh-TW | 4 |
| ja | 4 |
| ru | 4 |
| en | 3 |
| ko | 2 |
| pt | 2 |
| de | 2 |
| zh | 1 |

**法语 / 意大利语最严重**——这跟本周期 IT/FR 多语言翻译（7-1 那次）高度相关。翻译管线可能对**同 slug 重复写入**而不是 patch 既有 _id。

---

## 三、关键发现 1：34 组里 2 组 KEEP 是历史错位

### /ja/ai-picture-generator

```
KEEP:  features-ai-picture-generator-ja
       seoTitle: 「affiliate ads 生成器 | Lovart」  ⚠️ 关键词错位
MOVE:  tools-ai-picture-generator-ja  
       seoTitle: 「AI画像生成 | Lovart」         ← 这是 B 任务 v1 patch 后的状态
```

**问题**：KEEP 的 seoTitle 含 "affiliate ads"——但 slug 是 `ai-picture-generator`，**两者主题完全不匹配**。这个 _id 大概率是早期某个 Phase 1 试错时把 affiliate 工具的 _id 复用了 image generator 的 slug。

→ **不能直接 move 了之**，需要先修 KEEP 的 seoTitle，把 "affiliate ads" 改回 image generator 主题。

### /ja/ai-video-generator

```
KEEP:  features-ai-video-generator-ja
       seoTitle: 「Sora 2、Veo 3、Klingで動画生成｜Lovart」  ✅ 真日文长版
MOVE:  tools-ai-video-generator-ja  
       seoTitle: 「AI Video Generator |画像...」           ← 这是 B 任务 v1 patch 后的状态
```

**KEEP 是好的日文长版**（含 Sora/Veo/Kling 这三个模型）——这个可以放心保留。MOVE 移到 drafts 没问题。但用户已被 B 任务 patch 改成了「Video Generator | Lovartの無料ツール」——move 会浪费一次 patch 劳动。

---

## 四、关键发现 2：B 任务已 patch 的 2 个 MOVE

| (lang, slug) | MOVE _id | MOVE 当前 seoTitle | 处置建议 |
|------|------|------|------|
| /ja/ai-picture-generator | tools-ai-picture-generator-ja | AI画像生成 | Lovartの無料ツール |
| /ja/ai-video-generator | tools-ai-video-generator-ja | Video Generator | Lovartの無料ツール |

**这 2 个的 MOVE 是个尴尬态**：
- 我刚刚 B 任务 patch 了它们——让它们看起来很专业
- 但 MOVE 本来就该 unpublish——所以"刚 patch 就 move"是反方向动作
- 不会造成 SEO 损失（MOVE 上没流量），但是**逻辑上很别扭**

---

## 五、阶段化执行方案

按 AGENTS.md "修复优先于删除" + 不浪费 B 任务劳动，建议按下面 3 阶段推进：

### 阶段 1 — 立即可推进 (30 组)

**这 30 组的共同特征**：
- KEEP 是正确的本地化版本（lang match True）
- MOVE 是 EN 残本或简版（lang match False 或 desc < KEEP）
- 双方都没真实流量（GSC + GA4 都为 0）
- B 任务没 patch 过它们

**执行模式**：
```
对每个 MOVE_id:
  1. 读 _id 全部字段 → archive/duplicate-slugs-archived-2026-07.json
  2. 用 Sanity mutate draft.json 创建 drafts.<id> 副本
  3. delete 原 published _id
```

**30 个 _id 列表** (en/zh/de/部分 it/部分 fr/部分 ru 等) — 详见 `dedup-impact-report-2026-07.csv`。

**预期净效果**：30 个 URL 前端 SSR 收敛到唯一 _id，meta 抖动问题在该 30 URL 上消失。

### 阶段 2 — 二次确认 (1 组)

**/ja/ai-picture-generator**:

第一步先修 KEEP 的 seoTitle 错位（把 "affiliate ads" 改回 image generator 主题）：

```
_id: features-ai-picture-generator-ja
SET: seo.title = "AI画像生成 | Lovartで写真をプロ品質に"  
SET: seo.description = "Lovartの無料AI画像生成ツールで、プロ仕様の画像を数秒で生成..."
```

第二步再走阶段 1 的 3 步 move 操作。

### 阶段 3 — 暂缓 14 天 (2 组)

**/ja/ai-picture-generator /ja/ai-video-generator**（MOVE 被 B 任务 patch 过的）：

逻辑上：B 任务 patch 在 MOVE 上虽然不增 SEO 收益，但**patch 行为本身没造成任何伤害**。这两个 URL 上 GSC + GA4 全 0 流量。

建议：**等 7-21 周报**（7-21 当日）观察这两个 URL 是否被 Google 索引、真有 0 流量 → 届时再 move。如果发现 Google 已索引，给前端做 301 → KEEP；如果没索引，直接 move。

---

## 六、关键决策表

| # | 语言 | slug | KEEP _id | MOVE _id | 阶段 | 备注 |
|---|------|------|---------|---------|------|------|
| 1 | zh | ai-avatar-generator | 21dd4b6c-...-zh | tools-ai-avatar-generator-zh | 1 | 标准 |
| 2 | zh-TW | ai-avatar-generator | 21dd4b6c-... | tools-ai-avatar-generator-zh-TW | 1 | 标准 |
| 3 | fr | ai-design-agent | features-ai-design-agent-fr | 73328639-...-fr | 1 | KEEP 是法文长版 |
| 4 | it | ai-design-agent | 73328639-...-it | features-ai-design-agent-it | 1 | KEEP 意文长版 |
| 5 | ja | ai-design-agent | 73328639-...-ja | features-ai-design-agent-ja | 1 | KEEP 日文长版 |
| 6 | ko | ai-design-agent | 73328639-...-ko | features-ai-design-agent-ko | 1 | KEEP 韩文长版 |
| 7 | pt | ai-design-agent | 73328639-...-pt | features-ai-design-agent-pt | 1 | KEEP 葡文长版 |
| 8 | ru | ai-design-agent | 73328639-...-ru | features-ai-design-agent-ru | 1 | KEEP 俄文长版 |
| 9-18 | ... | ... | ... | ... | 1 | 详见 CSV |
| **33** | **ja** | **ai-picture-generator** | **features-ai-picture-generator-ja** | **tools-ai-picture-generator-ja** | **2** | **KEEP seoTitle 含 "affiliate ads" 错位！先修后 move** |
| **34** | **ja** | **ai-video-generator** | **features-ai-video-generator-ja** | **tools-ai-video-generator-ja (B patched)** | **3** | **MOVE 是 B 任务刚 patch 的；先等 7-21 周报** |

---

## 七、备份策略

按 AGENTS.md "修复优先于删除"——任何 unpublish 之前必须 100% 备份：

```
Output/QA-Memo/dedup-archived-2026-07-15.json
  - 含每个待 MOVE _id 的完整字段（除 _id 本身）
  - 含 reference 到原来 (lang, slug) + KEEP _id
  - 备份完成后才执行 unpublish
```

恢复方式（万一需要）：
```bash
# 取回 drafts 副本
python3 sanity-restore-dedup.py --lang ja --slug ai-video-generator
# 这从 drafts.* 取回, 重新 patch publishedAt
```

---

## 八、推荐下一步

请选一个：

- **A. 仅执行阶段 1（30 组 LOW 风险）**——立即可干，1-2 小时。先写 backup JSON，再 30 个 move to drafts。完成后前 30 个 URL SSR 收敛。
- **B. 执行阶段 1 + 阶段 2 同步修 KEEP 错位**——阶段 2 修 /ja/ai-picture-generator 的 "affiliate ads" 错位需要先 1 次 patch，然后才 move。整套约 3 小时。
- **C. 暂停，先做反向抽样—— 抽 1 组实际跑 move 验证流程 OK 后再批量**——稳妥但慢。
- **D. 完全暂缓，先看 7-21 周报 7-12 batch 索引情况再决定**——等 1 周。

---

*报告生成: 2026-07-15 14:30 UTC+8 | Lovart SEO Agent*
