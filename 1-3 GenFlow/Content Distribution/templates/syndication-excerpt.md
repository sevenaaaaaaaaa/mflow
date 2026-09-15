# 轨道 A — 摘要再分发母模板

> 替换 `{{...}}` 占位符。站外词数目标：主站 {{source_word_count}} 的 20–40%。

---

## 元数据（YAML front matter）

```yaml
track: syndication
platform: {{platform}}
source_url: {{canonical_url}}
source_title: "{{source_title}}"
offsite_title: "{{offsite_title}}"
utm: "?utm_source={{platform}}&utm_medium=syndication&utm_campaign=offsite_{{slug}}"
canonical: {{canonical_url}}
main_site_published_days_ago: {{days_since_publish}}
tier: {{tier}}
```

---

## 正文结构

### 标题

{{offsite_title}}

（不得与 `{{source_title}}` 相同）

### 钩子（全新首段，≤120 字）

{{hook_paragraph}}

### 核心要点（3–5 条，改写非复制）

- {{bullet_1}}
- {{bullet_2}}
- {{bullet_3}}

### 可选：一小段代码/示例（仅 DEV.to / Hashnode）

```
{{code_snippet_if_any}}
```

### 引流 CTA（必须）

Read the full guide on lovart.ai (canonical source):

{{canonical_url}}{{utm}}

---

## Agent 自检

- [ ] 未粘贴主站全文
- [ ] 标题与主站不同
- [ ] 含 UTM 链接
- [ ] Medium/Hashnode 设 canonical
- [ ] 主站已发布 ≥7 天
