# Lovart Skill Entrypoint Governance

> 目的：防止 skill 层重新出现“父入口已存在，但中间层/子 skill 继续抢路由”的问题。

## Canonical Entrypoints

| 场景 | 唯一父入口 | 内部支撑 skill |
|------|------------|----------------|
| Blog 创作 | `lovart-blog` / `lovart-blog-signal-writer` 父链 | `lovart-complete-guide`、`lovart-insight-trend`、`lovart-best-practice` 等分类子 skill |
| 落地页生成/刷新 | `lovart-landing-page` | `lovart-page-serp-writer`、`refresh-page-page-generator` |
| 质量门禁 | `lovart-content-quality-gates` | `lovart-content-audit`；`lovart-sanity-preflight` 仅兼容别名 |
| Sanity 发布 | `lovart-sanity-publish` | `lovart-sanity-content-publish`、`lovart-tools-sanity-publish`、`lovart-features-sanity-publish`、`lovart-product-sanity-publish`、`lovart-scenarios-sanity-publish` |
| 分发 | `lovart-multi-platform-push` | `lovart-content-distribution` |

## Support-Only Rule

支撑 skill 必须满足：

- frontmatter 加 `disable-model-invocation: true`（平台支持时生效）。
- 文件开头写明 `Support-only`，说明只能由哪个父 skill 调用。
- README / agent / profile 不把它列为用户触发入口。
- 子 skill 不复制父层治理职责，只保留专门 SOP、模板、脚本细节。

## Agent Preload Rule

Claude/Hermes/OpenCode profile 只预加载父入口 skill：

- `lovart-page` 只预加载 `lovart-landing-page`。
- `lovart-qa` 只预加载 `lovart-content-quality-gates`。
- `lovart-publisher` 只预加载 `lovart-sanity-publish`。
- 分类 blog 子 skill 不预加载到非 blog agent。

## 新增 Skill Checklist

新增或迁移 skill 前先判断：

1. 它是否是用户会直接说出的完整任务入口？
2. 如果不是，是否已有父入口能路由到它？
3. 是否需要 `disable-model-invocation: true`？
4. 是否已同步到 `1-1 Harness/Skills` 与 `1-1 Harness/.claude/skills`？
5. 是否更新 `1-1 Harness/05-skills/skills-usage.md`、`.cursor/skills/README.md`、agent preloads？

任一答案不明确，默认作为 support-only，不新增用户入口。
