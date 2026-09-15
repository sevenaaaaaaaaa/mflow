# DeepSeek GUI（桌面 / Web）

> DeepSeek 客户端 **无** 项目级 cron、无 vault 文件系统访问；仅适合 **问答 + 粘贴日志**，不适合替代 Tools pull 自动化。

## 推荐使用方式

| 用途 | 做法 |
|------|------|
| 读 pull 结果 | 粘贴 `pull-tools-latest.json` 内容，问「有无风险」 |
| 写文案 / SEO | 粘贴 SOP 片段 + 主题 |
| **无人值守 pull** | ❌ 改用 Cursor Automations 或 bash |

## 系统提示（复制到 DeepSeek「自定义助手」）

```
你是 Lovart GEO 运维助手。用户会粘贴 JSON 日志或 shell 输出。

规则：
- production 是 Sanity 真相源；本地 Page Gen/Pages/Tools 可被 pull 覆盖
- legacy Tools count 必须为 0；future release dates 必须为 0
- 不要建议 sanity deploy、--replace import、删除 production 文档

常用验收字段：
- pull-tools-latest.json: written, audit.legacy, audit.draft
- health check: brokenUrls, future release dates count

回答用简体中文，先结论后细节。
```

## 与自动化栈关系

```
[Cursor Automations / bash]  → 执行脚本、写 JSON
         ↓
[DeepSeek GUI]               → 人工粘贴、二次解读（可选）
```

## 凭证

DeepSeek API Key 在 DeepSeek 应用内配置；**不要**把 Sanity / GSC 密钥粘贴进 DeepSeek 对话。

## 若需「DeepSeek 模型」跑代码

用 **OpenCode / Cursor** 选 DeepSeek 模型提供商（若已接入），仍走 [opencode.md](./opencode.md) / [cursor.md](./cursor.md)，而非 GUI  alone。
