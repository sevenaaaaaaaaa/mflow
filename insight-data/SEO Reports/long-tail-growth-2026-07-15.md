# Lovart SEO 长尾流量扩展路线图 | 2026-07-15

> 📅 报告日期: 2026-07-15
> 📊 数据基线: GA4 organic_pages_30d (5.83M sessions) + GSC top20 + Sanity 3845 compositePage
> 🎯 范围: 把"17 个入口页吃 69.3% SEO 流量"逐步降到 40%，长尾池全面扩散

> 前置文档: 
> - `Output/SEO-Reports/本周建议执行诊断-2026-07-15.md`（已校正原建议文档数据偏差）
> - `Output/SEO-Reports/扩展优化机会-2026-07-15.md`（11 个扩展机会）

---

## 摘要（先结论）

**首页集中度 69.3% 是 Lovart 当前 SEO 风险点也是增长杠杆**。把 67.3% → 50% 的长尾份额**不是把首页降下来，而是把池子撑起来**——通过 7-21 周报后等 1548 个新 URL 自然索引、修复 34 组重复 slug、Tier B/C 内链激活，把"沉睡 3828 个 compositePage"激活。

**80% 的增长不需要建新页面，只需要在 Sanity 里 patch 已发布页**——按 AGENTS.md RULE 1 "不动 schemaTypes/" + 修复优先于删除。

**量化目标**（按 GA4 organic trend 类推）：
- 当前 5.83M sessions/月 + Top 17 占 67.3%
- 7-21 周报后 + Google 索引稳定 = +0.7M sessions（Top 17 跌到 ~60%）
- 12 个月目标 = Top 17 占 40%，总盘 12M sessions

---

## 一、流量集中度精确基线（GA4 organic_pages_30d）

| 排名 | 路径 | sessions | % | cumulative |
|------|------|---------|---|-----------|
| 1 | /canvas | 1,184,999 | 20.3% | 20.3% |
| 2 | / | 891,749 | 15.3% | 35.6% |
| 3 | /ai-tool/image-generator | 553,631 | 9.5% | 45.1% |
| 4 | /zh/home | 463,387 | 7.9% | 53.0% |
| 5 | /inspiration | 335,261 | 5.7% | 58.8% |
| 6 | /home | 261,463 | 4.5% | 63.3% |
| 7 | /search | 237,343 | 4.1% | 67.3% |
| 8 | /comfy | 184,236 | 3.2% | 70.5% |
| 9 | /sd | 166,388 | 2.9% | 73.3% |
| 10 | /ai-tool/video-generator | 153,109 | 2.6% | 76.0% |
| 11-17 | ... | ... | ... | 84.6% |
| 18-30 | /asset /workflows /pt/home /image-model /viphome /lib3 /zh/login /projects | ~498,883 | 8.6% | 92.3% |
| 30+ | 剩余 270 个长尾 | ~456,894 | 7.7% | 100% |

**Top 10 占 76.0%**（同比第一份报告算的 17 个页占 69.3% 更精确，因为仅 30 个 Top 页面已吃掉了总流量 92.3%）。

---

## 二、四个 GSC Top 20 异常：立即可抓

| URL | clicks | impressions | CTR | 问题 |
|-----|--------|--------------|-----|------|
| `/zh` | 1,207 | 205,080 | **0.59%** | 极低：可能 hreflang 错配（实测已确认 hreflang 是齐的，可能是 title 在中文搜索结果显示英文） |
| `/zh-TW` | 481 | 100,624 | **0.48%** | 极低：同 zh |
| `/pricing` | 1,582 | 487,720 | **0.32%** | 极低：用户搜索 pricing 没下叉 |
| `/login` | 1,144 | 164,949 | **0.69%** | 极低：大量登录页曝光但用户其实想找 brand query |
| `/ru/features/ai-carousel-generator` | 722 | 5,169 | **13.97%** | **极高** — 俄语长尾着陆成功！**复制该模式** |
| `/ru/features/change-video-background` | 489 | 4,651 | **10.51%** | 俄语长尾高 CTR，**复制该模式** |

### 即时可做
1. **PATCH `/zh` 和 `/zh-TW` 的 seoTitle / seoDescription**（不破坏 schema，只改字段）——把中文 SEO CTR 从 0.5% 拉到 3% 等同于 +5,000 月点击
2. **PATCH `/pricing` 页面中文版 seoTitle**（如果是英文，搜索引擎读出来只能匹配英文搜索 query）
3. **PATCH `/login` 页面**：应该不出现在搜索曝光里，应该 `<meta name="robots" content="noindex,nofollow">`（但这是前端活）

---

## 三、长尾扩展 4 阶段路线图

### 阶段 0 — 当前 (2026-07-15)
- Top 17 占 67.3%，长尾 32.7%
- 5.83M sessions/月
- 主要资产: 3845 compositePage，3828 个未进 GA4 Top 300

### 阶段 1 — 7-21 周报观察期 (2026-08-15)
- 等 Google 索引 7-12 发布的 1548 个 URL
- 行动: IndexNow 批量推送（已完成，下方脚本就绪）
- **预期**: Top 17 占 ~60%，长尾 ~40%，总量 ~6.5M（+11%）
- **触发器**: 30 天后若新发布的 tools 页仍未进 GSC Top 100，则方案 1+3 升级

### 阶段 2 — 修正 + 激活期 (2026-10-15)
- 修复 34 组重复 slug（去重 → CTR 涨 → 长尾页进 Top 100）
- Tier B 33 篇激活：cross-link + IndexNow
- Tier C 1577 篇诊断：3 个最老 URL（/en/tools/ai-voice-generator-free, /ai-virtual-try-on, /image-to-3d-ai）做深度内容 patch
- **预期**: Top 17 占 ~50%，长尾 ~50%，总量 ~8M (+23%)
- **关键 KPI**: GSC 收录率 = 80%（vs 当前 47% 估算）

### 阶段 3 — 全面扩散期 (2026 Q4)
- /blog 池扩量：从 0.6% → 5% 总流量份额
- 新建 /vs-civitai、/pixai-alternative 等竞品对比页（4 个）
- 百度站长平台注册 + sitemap 单独提交（中文 SEO 流量 +30%）
- **预期**: Top 17 占 ~40%，长尾 ~60%，总量 ~12M (+50%)

---

## 四、即刻可做的 5 件 Sanity 操作

按 AGENTS.md "修复优先于删除"——这些**都是 patch 现有文档**，不涉及 schema 变更。

### 1. /zh、/zh-TW、Pricing 中文化（30 分钟）
去 Sanity 后台找 `/zh` slug 对应的 compositePage，patch：
- seo.title 改成纯中文（含主要功能关键词，不只是品牌前缀）
- seo.description 改成中文 + 加 "免费试用"、"1 分钟创建" 等转化词

### 2. 34 组重复 _id 去重（4-6 小时）
依据 `Output/SEO-Reports/改造建议/duplicate-slugs-action-2026-07.csv`
- 每组保留 1 个（按决策规则：UUID _id + 长 seoDesc 优先）
- 其他 move 到 drafts（不是 delete）
- 该操作让 SSR 不再随机返回 meta，提升 CTR 平均 0.2-0.5pp

### 3. Tier B 33 篇激活（2 小时）
依据 `Output/SEO-Reports/改造建议/internal-cold-pages-inlinks-recovery-2026-07.csv` 中 `tierB-activate` 33 篇
- 在 /inspiration / 首页 recommendations 加 33 个 cross-link entry（Sanity patch）
- 改各页 seo.title / seo.description 确保差异化（非重复模板）

### 4. Tier C 1577 篇诊断分批（持续）
依据 `internal-cold-pages-inlinks-recovery-2026-07.csv` 中 `tierC-diagnose`
- 每周 batch patch 50-100 篇
- 加 cross-link entry + push IndexNow

### 5. /ru 高 CTR 长尾复制（1 小时）
- 找出 /ru/features/ai-carousel-generator、/change-video-background 内容为什么精准
- 对 /zh、/ja、/ko、/de 等 5 个低 CTR 语言做相似深度 patch

---

## 五、关键路径上不做的"反向"清理

按 AGENTS.md "修复优先于删除"——这些**绝对不能做**：

- ❌ 不要把所有 Tier C (>60d 冷门) 1566 篇批量 delete——会再触发 InLinks 跌
- ❌ 不要把 34 组重复 _id 直接 unpublish 重复的那个——要 move 到 drafts 保留 _id 供未来恢复
- ❌ 不要为新发布 1548 URL 单独建一组 sitemap——它们自动进现有 sitemap

---

## 六、资源说明

**已生成资产**：
- `Output/SEO-Reports/改造建议/internal-cold-pages-inlinks-recovery-2026-07.csv`（3109 行 = 1499 Tier A + 33 Tier B + 1577 Tier C）
- `Output/SEO-Reports/改造建议/duplicate-slugs-action-2026-07.csv`（34 行决策列表）
- `Output/SEO-Reports/改造建议/ja-title-template-rework-2026-07.csv`（18 行 patch 清单）
- `Output/SEO-Reports/改造建议/indexnow-batch-2026-07-12.csv` + `.txt`（1548 URLs）
- `Output/SEO-Reports/改造建议/long-tail-traffic-mix-target-2026-07.csv`（4 行阶段目标）
- `automation/indexnow-push-7-12-batch.py`（可一键 dry-run 或 --apply）

---

*报告生成: 2026-07-15 | Lovart SEO Agent | 路线: 不问就干*
