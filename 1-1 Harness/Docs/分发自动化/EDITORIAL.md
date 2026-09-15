# 编辑与发布规范

## 语言

| 区域 | 语言 | 平台 |
|------|------|------|
| 国内 `cn` | **简体中文** | 知乎、CSDN、思否、掘金等全部 Wechatsync 平台 |
| 海外 `global` | **英文** | DEV.to、Blogger、Medium、X |

禁止：国内发英文稿、海外发中文稿（除非该平台明确例外）。

## 内容结构（每篇必须包含 4 款工具）

每篇站外稿必须完整覆盖以下 GitHub 项目（不可只写其中一两个）：

1. **screenshot-to-code** — https://github.com/abi/screenshot-to-code
2. **Open Design** — https://github.com/nexu-io/open-design
3. **Open CoDesign** — https://github.com/OpenCoworkAI/open-codesign
4. **libtv-skills** — https://github.com/libtv-labs/libtv-skills

### 文风参考

`content/github-ai-design-tools-kb.md` 及用户提供的 Liblib 宣发合集：

- **开篇**：痛点 / 身份代入（「很多程序员第一反应是…」）
- **每款工具独立小节**：机制解释（2–3 段）+ **具体场景** + 仓库/体验链接
- **篇幅**：中文稿目标 **1800–2800 字**；英文稿目标 **900–1400 words**
- **结尾**：选型表或总结 + 可选 Lovart 软引流（非硬广）

## 发布前人工审核（强制）

1. Agent 写稿 → `drafts/` + 更新 `queue/dispatch-*.json`
2. `approved: false`（默认）→ 仅预检，**不真发**
3. **用户阅读并修改** `drafts/` 内全文
4. 用户确认后：清单设 `"approved": true`
5. 再执行：

```bash
node scripts/dispatch-publish.js --manifest queue/xxx.json --approved
```

未带 `--approved` 且清单 `approved !== true` 时，dispatch 只做 dry-run 级预检与打印待审列表。
