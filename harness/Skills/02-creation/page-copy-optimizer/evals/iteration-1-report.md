# Iteration 1 Eval Report

## 方法

对同一组三项真实存量优化任务进行只读 A/B：

- **Baseline**：只读取现有 `landing-writer`；
- **Candidate**：读取 `page-copy-optimizer`；
- 任务：英文去背景工具页、英文 logo maker 的竞品承诺越界、日语 `hero-split` 图文 CTA 冲突。

本轮评估不测“文案是否更优美”，而测批量优化时最容易失控的可观察行为。

## 断言与结果

| 断言 | Baseline | Candidate | 证据 |
|---|---:|---:|---|
| 不添加题目未验证的事实 | 3/3 | 3/3 | 两组均未虚构速度、格式、商用权或模板数量 |
| 移除并解释无依据的 SVG/PDF 承诺 | 1/1 | 1/1 | 两组均删除该承诺；Candidate 额外产出 do-not-claim 和事实台账 |
| 把图片/CTA/模块问题从文案问题中分离 | 3/3 | 3/3 | 两组均指出 before/after 图、CTA 落点和 hero-split 4:3 属于非文案升级项 |
| 模块级诊断与改写理由可审计 | 0/3 | 3/3 | Candidate 每题输出 existing issue、replacement、why、fact source、dependency |
| 可复用的 page promise / proof / CTA 契约 | 0/3 | 3/3 | Candidate 每题输出 Copy Contract，包含 input→output、proof、risk reducer、CTA、禁止承诺 |
| CRO 假设与测量边界 | 0/3 | 3/3 | Candidate 说明指标、流量分层和“不保证提升”；Baseline 只给方案 |
| 日语页面的本地化边界 | 1/1 | 1/1 | 两组都使用可执行日语 CTA；Candidate Skill 已补规则：ja 必读 ja-copywriter |

## 结论

Baseline 的事实安全与基础改写能力足够强，因此新 Skill **不应替代** `landing-writer` 的新页面创作能力。

Candidate 的增量价值已验证为：

1. 固定诊断 → 契约 → 模块 diff → 事实台账 → 非文案升级 → CRO 测量的交付顺序；
2. 将“写一句更好文案”转为可被审核、patch、复跑和实验验证的优化包；
3. 在图文、CTA、产品事实、页面结构交界处明确停下并升级，而不是强行靠 copy 掩盖问题。

结论：保留 `page-copy-optimizer` 作为既有页面的专用入口；保留 `landing-writer` 负责新页面、故事线和结构性重建。

## 工具限制

Skill Creator 的 `eval-viewer/generate_review.py` 需要 Python ≥3.10（使用 `dict | None` 类型语法）；本机 Python 3.9.6，查看器启动失败。因此本轮以本报告保留 A/B 证据。升级运行时后，应把三项任务的完整 baseline/candidate 输出落入标准 workspace，并生成可交互人工评审页。
