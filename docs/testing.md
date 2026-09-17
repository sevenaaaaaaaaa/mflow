# 自动化测试（T4）

> 目标：核心机制（护栏/执行器/配额/熔断/预设）有**离线可跑的单元测试**，并进会话门禁，防止"改坏不知道"。

## 运行

```bash
bash "1-4 Dev/scripts/run-tests.sh"       # 本地
# 或服务器：cd /www/wwwroot/mflow && bash "1-4 Dev/scripts/run-tests.sh"
```

- 纯标准库 `unittest`（21 用例，~3 秒，无网络/无外部依赖）
- 本地若缺 `markdown` 依赖会自动注入 stub（被测逻辑不需要它）

## 覆盖范围（21 用例）

| 套件 | 用例 | 关键断言 |
|------|------|---------|
| `TestSpecGuard` | 5 | 类型白名单拒绝 · 额外字段拒绝 · 规模上限(≤200) · dry-run 默认 true · budget_profile 放行 |
| `TestBreaker` | 4 | 致命错误模式识别（401/403/key/余额/quota）· trip 后阻断 · 冷却后半开 · 手动复位 |
| `TestQuota` | 5 | admin 不限 · 条目超额拦截 · 用量累加 · 80% 预警去重 · 写入配额判定 |
| `TestHousekeeping` | 1 | 幂等（无旧数据全 0） |
| `TestAgentContext` | 3 | CJK bigram 分词 · 规则注入 ≤1200 字符 · skills 检索命中且 ≤5 |
| `TestPresets` | 3 | 预设清单与类型合法 · 未知预设报错 · 多语言展开（3 语言正确） |

## 门禁集成

`session-init.sh` **GATE 6**：跑 `run-tests.sh`，失败即门禁不过（`sync.sh` 发布前也会跑 session-init，所以测试失败会挡住发布）。

```
[GATE 6] unit tests
  ✓ GATE 6: 单元测试通过（21 用例）
```

## 后续扩充建议

- 执行器端到端（起临时目录 + 假 Sanity 端点）→ 覆盖 `asset_replace/field_patch` 的 patch 构造
- `preset_expand` 其余分支（依赖真实 Sanity/GEO 数据 → 需 fixture 化）
- 前端 JS 语法检查已由 GATE 5 覆盖（node --check），可补关键函数的行为测试
