# X (Twitter)

| 项 | 值 |
|----|-----|
| 自动化 | **爱贝壳**（槽 2）— 扩展同步草稿箱 |
| 补充 | Wechatsync `x`、fanout 浏览器自动 |
| 轨道 | A 短推 + 链主站 |

## 内容规格

- 单条或 3–5 条 thread
- 首条 hook ≤280 字符（留链接位）
- 含 UTM 主站链接
- 禁止主站全文粘贴

## 爱贝壳发布

1. 登录 x.com
2. 扩展侧栏粘贴 `drafts/x-{slug}.md`
3. 勾选 X → 同步草稿 → 后台确认

## 补充

```bash
# Wechatsync（Arc 登录 x.com 后）
bash scripts/publish-wechatsync.sh drafts/x-{slug}.md x
```
