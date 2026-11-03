# Page Copy Optimizer Scorecard

> 用于诊断和改写后的自检。决策顺序固定为：**页面主题 → 模块 CRO → SERP 参考 → Lovart 知识库红线**。它评估“页面是否把用户任务说清并给出可信下一步”，不预测或保证转化率。

## 100 分评分卡

| 维度 | 分值 | 0 分信号 | 满分信号 |
|---|---:|---|---|
| Page theme / routing | 18 | 页面只堆关键词，没回答查询任务 | 首屏、页面类型和故事线都服务同一搜索意图 |
| Module CRO | 22 | Hero、proof、CTA、FAQ 各说各话 | 每个模块清楚推进理解、降低风险或行动 |
| SERP reference | 15 | 不看 SERP，或照抄竞品承诺 | 从意图、异议、饱和模式中提炼可验证差异 |
| Hero clarity | 8 | 抽象 slogan；看不出用户/输入/输出 | 在 3 秒内能说出对象、任务、输入/输出和风险降低点 |
| Proof and CTA fit | 8 | 只有“更强/更快”的自称或泛 CTA | CTA 前有可验证 proof，CTA 与页面任务一致 |
| Listing title and description | 10 | 裸关键词标题、描述复述标题、卡片相邻时不可区分或截断失义 | 标题说明具体任务；描述补足结果/适配性；前 30 卡中可扫描且完整显示 |
| Image-copy compatibility | 4 | 图片只是背景或与 CTA 争注意力 | 图片证明机制/结果，文本讲价值，CTA 指向下一步 |
| Lovart knowledge redline / locale safety | 15 | 编造能力、格式、价格、竞品结论，或直译腔 | 每个关键事实可追溯到 Lovart 知识库；未知项显式标记 |

## 判定

- `<60`：先重做 page promise / intent；不要只润色句子。
- `60–74`：先改 Hero、proof、CTA，再改 FAQ。
- `75–84`：局部模块优化；需要图文或证据层检查。
- `≥85`：可进入实验或发布前流程，但仍不等于“高转化”。

任一以下项为 0，页面不得以“已优化”交付：

- Page theme / routing；
- Module CRO；
- Listing title and description（当页面在列表中展示时）；
- Lovart knowledge redline / locale safety。

## Copy Diagnosis 模板

```markdown
## Copy Diagnosis
| Dimension | Score | Evidence | Impact | Recommended action |
|---|---:|---|---|---|
| Intent / routing | | | | |
| Hero clarity | | | | |
| Proof and editability | | | | |
| CTA fit | | | | |
| Objection handling | | | | |
| Distinctive value | | | | |
| Image-copy compatibility | | | | |
| Fact / locale safety | | | | |
```

## 最小验证

### 3 秒测试

展示首屏后，观察者能否回答：

1. 这是谁的页面？
2. 他/她要完成什么工作？
3. 输入什么，得到什么？
4. 下一步应该做什么？

### 5 秒测试

- 遮住图片，CTA 与承诺仍清晰；
- 遮住文字，图片仍是任务相关的机制/结果；
- 不依赖不可验证数字或模糊形容词。

### 列表卡测试

在真实或等宽度的列表卡中，不读详情页正文即可回答：

1. 这张卡解决的具体任务是什么？
2. 它与前后相邻卡片有什么不同？
3. 标题被截断后，核心任务是否仍存在？
4. 描述是否带来标题没有说的新信息（结果、对象、适配性或风险降低），而非重复关键词？

### 实验记录

```text
Hypothesis:
Changed sections:
Unchanged controls:
Audience / locale / traffic source:
Baseline metric and date range:
Observed metric and date range:
Confounders:
Decision:
```
