# DEV.to

| 项 | 值 |
|----|-----|
| 自动化 | **MCP auto**（主轨）· fallback `publish-devto.js` |
| 轨道 | A 技术摘要；B 教程全文 |
| canonical | `canonical_url` 字段 |
| API | DEV Community API Key |

## 内容规格

- 标题：技术向，可含 how-to
- 长度：800–1500 词
- Tags：最多 4 个（如 `ai`, `design`, `tutorial`）
- 封面：换图；`cover_image` 可选

## 适配要点

1. 代码块用新示例，勿整段复制主站
2. 适合 `/blog/` 教程类 S 级页
3. `published: false` 草稿审后再发

## 发布

```bash
node scripts/publish-devto.js --draft drafts/devto-{slug}.md
```
