# For 北美市场

> **文档定位**：面向北美市场团队的操作指南  
> **更新日期**：2026-06-04  
> **适用范围**：Lovart 项目北美市场 SEO 优化和内容策略相关人员

---

## 一、概述

本文档为北美市场团队提供完整的操作指南，涵盖北美市场定义、地区报告生成方法、品牌词和非品牌词分析、竞品词覆盖分析、市场特定的 SEO 策略等核心内容。

### 1.1 北美市场定义

**北美地区包含国家：**

| 国家 | 代码 | 语言 | 市场特点 |
|------|------|------|----------|
| 美国 | US | 英语 | 最大市场，竞争激烈 |
| 加拿大 | CA | 英语/法语 | 双语市场，需注意法语内容 |
| 英国 | GB | 英语 | 英式英语，需注意拼写差异 |
| 澳大利亚 | AU | 英语 | 英式英语，市场相对较小 |
| 新西兰 | NZ | 英语 | 英式英语，市场最小 |

### 1.2 市场特点

- **语言**：主要为英语，加拿大含法语
- **竞争**：高度竞争，需精细化 SEO 策略
- **用户行为**：注重隐私、品牌信任、用户体验
- **搜索习惯**：长尾关键词、问题式搜索、本地化搜索

---

## 二、地区报告生成方法

### 2.1 地区报告类型

| 报告类型 | 数据源 | 主要内容 |
|----------|--------|----------|
| **GSC 地区报告** | Google Search Console | 关键词排名、点击、曝光、CTR |
| **GA4 地区报告** | Google Analytics 4 | 用户行为、会话、转化 |
| **品牌/非品牌报告** | GSC + 竞品词库 | 品牌词和非品牌词表现 |
| **地区 mini 月报** | 综合 | 完整的地区月度报告 |

### 2.2 地区报告生成命令

```bash
# 生成北美地区月报
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month 2026-05 --region north_america

# 生成北美地区周报
python3 "1-4 Dev/scripts/weekly_review_v3.py" --region north_america

# 生成北美地区日报
python3 "1-4 Dev/scripts/sentinel/collect.py" --source gsc --region north_america
```

### 2.3 地区报告结构

**月报 §11.2–11.8 分区月报（双月）：**

| 表 | 双月列 | 环比列 |
|----|--------|--------|
| GSC 汇总 | 点击、曝光、CTR、点击占比、曝光占比 | 五项均有 |
| 品牌/非品牌 | 点击、曝光、CTR（双月） | 点击、曝光环比 |
| Top15 词 | {上月}/{报告月} 点击+曝光 | 点击环比 |
| Top10 页面 | 双月点击 | 点击环比 |

---

## 三、品牌词和非品牌词分析

### 3.1 品牌词分类规则

> **🚨 SSOT 铁律**：品牌词分类的唯一代码来源是 `1-4 Dev/scripts/lovart_brand_match.py`。禁止硬编码品牌词列表。所有品牌词判定必须通过 `is_brand()` 函数。

```python
from lovart_brand_match import is_brand, partition_keywords
```

**北美市场常见品牌词变体（已由 `lovart_brand_match` 覆盖）：**
- lovart ai（最常见）
- loveart（常见拼写错误）
- lo art（分词搜索）
- lovart.ia（AI 变体）

### 3.2 非品牌词分析

**竞品词库规模：** 265 全量词 / 36 核心词

**北美市场常见非品牌词类别：**
- AI 设计工具相关
- 图片生成相关
- Logo 制作相关
- 海报设计相关
- 社交媒体内容相关

### 3.3 品牌词和非品牌词报告生成

```bash
# 生成品牌词和非品牌词报告
python3 "1-4 Dev/scripts/seo_monthly_v2.py" --month 2026-05 --brand-analysis

# 生成竞品词覆盖分析
python3 "1-4 Dev/scripts/competitor_deep_match.py" --region north_america
```

---

## 四、竞品词覆盖分析

### 4.1 竞品词匹配引擎

```
GSC N 关键词 × 竞品 265 全量词（子串匹配）
  ├── Full Match: 宽口径，所有竞品词变体
  ├── Core Match: 严口径，36 个高优先级核心词
  ├── SEO 报告: 覆盖率+分层表现+缺失分析
  └── Sentinel: 行业词变化检测+竞品种子词对比
```

### 4.2 北美市场竞品词分析

**主要竞品：**
- Canva
- Adobe Firefly
- Midjourney
- DALL-E
- Stable Diffusion

**竞品词覆盖分析指标：**
- 覆盖率：命中竞品词数量 / 总竞品词数量
- 分层表现：Top 10/50/100 的竞品词表现
- 缺失分析：完全无排名的核心词

### 4.3 竞品词覆盖分析报告生成

```bash
# 生成竞品词覆盖分析报告
python3 "1-4 Dev/scripts/competitor_deep_match.py" --region north_america --output north_america_competitor.json

# 查看竞品词覆盖分析结果
cat "1-2 Insight/Trident Insights/reports/competitor_match_result.json" | python3 -m json.tool | head -50
```

---

## 五、市场特定的 SEO 策略

### 5.1 关键词策略

**关键词类型：**
- **品牌词**：保护品牌词排名，优化品牌词变体
- **非品牌词**：覆盖竞品词，优化长尾关键词
- **问题式关键词**：回答用户问题，优化 Featured Snippet
- **本地化关键词**：针对特定国家/地区的关键词

**关键词优化建议：**
1. **品牌词**：确保品牌词排名第一，优化品牌词变体
2. **竞品词**：覆盖核心竞品词，优化竞品词页面
3. **长尾词**：优化长尾关键词，提高转化率
4. **问题式词**：优化问题式关键词，争取 Featured Snippet

### 5.2 内容策略

**内容类型：**
- **功能页面**：优化 Features 页面，提高转化率
- **工具页面**：优化 Tools 页面，提高试用率
- **博客内容**：优化博客内容，提高流量
- **案例内容**：优化案例内容，提高信任度

**内容优化建议：**
1. **本地化**：针对北美市场本地化内容
2. **用户体验**：优化用户体验，提高转化率
3. **移动优先**：优化移动端体验
4. **页面速度**：优化页面加载速度

### 5.3 技术 SEO 策略

**技术 SEO 要点：**
- **网站结构**：优化网站结构，提高爬虫效率
- **URL 结构**：优化 URL 结构，提高可读性
- **Schema 标记**：添加 Schema 标记，提高搜索结果展示
- **页面速度**：优化页面加载速度，提高用户体验

**技术 SEO 优化建议：**
1. **网站结构**：优化网站结构，提高爬虫效率
2. **URL 结构**：优化 URL 结构，提高可读性
3. **Schema 标记**：添加 Schema 标记，提高搜索结果展示
4. **页面速度**：优化页面加载速度，提高用户体验

---

## 六、地区报告数据源

### 6.1 GSC 数据源

**GSC 数据字段：**
- `clicks`：点击次数
- `impressions`：曝光次数
- `ctr`：点击率
- `position`：平均排名

**GSC 数据查询：**
```bash
# 查询北美地区 GSC 数据
python3 "1-1 Harness/Skills/lovart-trident-data-engine/scripts/gsc_fetch.py" --region north_america
```

### 6.2 GA4 数据源

**GA4 数据字段：**
- `sessions`：会话数
- `users`：用户数
- `newUsers`：新用户数
- `conversions`：转化数

**GA4 数据查询：**
```bash
# 查询北美地区 GA4 数据
python3 "1-1 Harness/Skills/lovart-trident-data-engine/scripts/ga4_fetch.py" --region north_america
```

### 6.3 竞品词库数据源

**竞品词库数据：**
- `1-2 Insight/Trident Insights/竞品核心非品牌词/lovart_competitors_keywords.md`
- 265 全量词 / 36 核心词

**竞品词匹配：**
```bash
# 查询北美地区竞品词匹配
python3 "1-4 Dev/scripts/competitor_deep_match.py" --region north_america
```

---

## 七、地区报告产出路径

### 7.1 月报产出路径

```
1-2 Insight/Trident Insights/reports/monthly/
├── Lovart-SEO-2026-05.md                    # 全站月报
├── Lovart-SEO-2026-05-north-america.md      # 北美地区月报
├── .metrics/
│   ├── 2026-05.json                         # 年均 metrics
│   └── 2026-05-north-america.json           # 北美地区 metrics
```

### 7.2 周报产出路径

```
1-2 Insight/Trident Insights/reports/weekly/
├── Lovart-SEO-review-2026-05-25-2026-05-31.md                    # 全站周报
├── Lovart-SEO-review-2026-05-25-2026-05-31-north-america.md      # 北美地区周报
```

### 7.3 日报产出路径

```
1-2 Insight/Trident Insights/reports/daily/
├── Lovart-SEO-2026-05-31.md                    # 全站日报
├── Lovart-SEO-2026-05-31-north-america.md      # 北美地区日报
```

---

## 八、地区报告检查清单

### 8.1 月报检查清单

- [ ] 北美地区定义正确（美国、加拿大、英国、澳大利亚、新西兰）
- [ ] GSC 汇总表包含点击、曝光、CTR、点击占比、曝光占比
- [ ] 品牌/非品牌表包含点击、曝光、CTR（双月）
- [ ] Top15 词表包含双月点击+曝光
- [ ] Top10 页面表包含双月点击
- [ ] 所有表格包含环比列
- [ ] 包含 💡 洞察段落
- [ ] 包含 📊 年均对比

### 8.2 周报检查清单

- [ ] 北美地区定义正确
- [ ] Top5 品牌/非品牌表包含点击、曝光、CTR
- [ ] Top5 页面表包含点击、曝光、CTR
- [ ] 所有表格包含环比列
- [ ] 包含 💡 洞察段落

### 8.3 日报检查清单

- [ ] 北美地区定义正确
- [ ] GSC 数据包含点击、曝光、CTR
- [ ] 包含环比列
- [ ] 包含 💡 洞察段落

---

## 九、常见问题

### 9.1 如何生成北美地区报告？

1. **确定报告类型**：月报、周报或日报
2. **运行生成命令**：使用对应的生成命令
3. **检查报告内容**：使用检查清单验证报告内容
4. **优化报告内容**：根据检查结果优化报告内容

### 9.2 如何优化北美市场 SEO？

1. **关键词优化**：优化品牌词和非品牌词
2. **内容优化**：优化本地化内容
3. **技术 SEO**：优化网站技术 SEO
4. **用户体验**：优化用户体验

### 9.3 如何分析北美市场竞品？

1. **竞品词分析**：分析竞品词覆盖情况
2. **竞品内容分析**：分析竞品内容策略
3. **竞品技术分析**：分析竞品技术 SEO
4. **竞品用户分析**：分析竞品用户行为

---

## 十、相关文档

- [AGENTS.md](./AGENTS.md) - 项目规则和标准
- [WORKFLOWS.md](./WORKFLOWS.md) - 运维手册
- [For-SEO-负责人.md](./For-SEO-负责人.md) - SEO 负责人操作指南
- [For-日本市场.md](./For-日本市场.md) - 日本市场操作指南
- [For-数据对接分析师.md](./For-数据对接分析师.md) - 数据对接操作指南

---

> **维护者**：Lovart 团队  
> **最后更新**：2026-06-04  
> **版本**：V1.0
