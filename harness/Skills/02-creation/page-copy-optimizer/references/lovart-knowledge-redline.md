# Lovart 知识库红线

> 本文件定义页面文案优化中的事实边界。它不是“尽量参考”的建议，而是 replacement copy 的发布前条件。

## 1. 必须核验的事实类型

以下任何一类一旦出现在 Hero、proof、CTA、FAQ、SEO title/description 或 comparison 中，均要有 Lovart 知识库来源：

- 产品能力、操作路径、输入、输出、可编辑性；
- 模型、分辨率、导出格式、兼容性、集成；
- 价格、免费额度、试用、套餐、折扣；
- 商用权利、版权、隐私、数据处理；
- 速度、质量、准确率、用户数、客户、评分、转化数据；
- 竞品能力、缺陷、价格或比较结论；
- 官方产品名、功能名、术语与大小写。

## 2. 检索优先级

按下列顺序检索，记录具体文件路径与章节：

1. `insight-data/Knowledge Base/Lovart New Help Center/`：当前操作、产品能力、账户/套餐说明；
2. `insight-data/Knowledge Base/Lovart Docs Archive/`：补充工具能力；注意更新时间，不能以旧文档覆盖更新资料；
3. `insight-data/Knowledge Base/Lovart Introduction/` 和 `Changelog/`：产品定位、版本变化与发布日期；
4. 已验证的线上产品页面或内部产品事实；若与知识库冲突，以更新、更官方的材料为准并升级确认。

SERP、竞品页面、用户评论、模型常识和生成模型“通常能做什么”都**不是** Lovart 产品事实来源。

## 3. 四种判定

| 状态 | 可以怎么写 | 不能怎么写 |
|---|---|---|
| `verified` | 用知识库原意准确改写，并在 Fact Ledger 标文件/章节 | 扩大为未提及的效果保证 |
| `qualified` | 保留原有限定，如“支持…时”“取决于模型/套餐” | 删掉条件后写绝对承诺 |
| `unknown` | 删除、降级为用户需确认的问题，或保留 `[待考证]` | 用“可能”“通常”“AI 可以”伪装为事实 |
| `conflict` | 停止改写并升级产品/内容负责人确认 | 选择更营销的一方继续写 |

## 4. Fact Ledger 格式

每个优化包必须包含：

```markdown
## Fact Ledger
| Claim | Status | Lovart knowledge source | Copy decision |
|---|---|---|---|
| Upload an image and remove its background | verified | <KB path + section> | 可写入 Hero / proof |
| Export SVG and PDF | unknown | 未找到当前 KB 证据 | 删除，不可暗示 |
| Generate hundreds of templates | unknown | 仅见竞品 SERP 描述 | 删除，不可比较 |
```

只写“题目提供”或“用户说过”时，必须标为临时输入，并在发布前补知识库核验；不能把临时输入伪装成产品证据。

## 5. 术语与品牌

- 使用知识库中实际出现的产品名和功能名，不自行翻译、缩写或改大小写。
- 面向非英文市场时，产品名通常保持官方写法；解释性文案按 locale Skill 本地化。
- 不把竞品名称放进普通工具页 Hero；comparison 页面也只能写可核实、可解释的差异。

## 6. 最终红线检查

在交付 replacement copy 前逐句检查：

1. 这句话是否含一个可验证的外部事实？
2. 若有，Fact Ledger 是否指向 Lovart 知识库？
3. 来源是否支持该句的强度、范围与条件？
4. 若用户因转化理由要求写得更强，是否仍然真实？

任一答案为否：该句不能进入页面。
