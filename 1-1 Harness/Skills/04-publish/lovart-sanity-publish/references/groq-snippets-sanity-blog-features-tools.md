# Sanity GROQ 速查 — Blog / Features / Tools（production）

> **用途**：import 前查线上是否已有、import 后验收。在 https://lovart.sanity.studio Vision 或 `npx sanity documents query` 执行。  
> **项目**：`o11tm2qe` · **dataset**：`production`

---

## 1. 单篇是否已存在（import 前）

```groq
// Blog — en
*[_type == "blog" && slug.current == "my-article-slug" && language == "en"][0]{
  _id, title, language, "slug": slug.current
}

// Feature 功能页
*[_type == "compositePage" && category == "feature" && slug.current == "graphic-design" && language == "en"][0]{
  _id, title, language, sourceType, "slug": slug.current
}

// Tool 工具页
*[_type == "compositePage" && category == "tool" && slug.current == "ai-logo-generator" && language == "en"][0]{
  _id, title, language, "slug": slug.current
}
```

**解读**：有结果 → 线上已有该 `_id` 范围文档；`import --missing` 会**跳过**同 `_id`，不会覆盖。

---

## 2. 某 slug 多语言是否齐全

```groq
*[_type == "compositePage" && category == "feature" && slug.current == "graphic-design"]{
  _id, language, title
} | order(language asc)
```

```groq
*[_type == "blog" && slug.current == "my-article-slug"]{
  _id, language, title
} | order(language asc)
```

---

## 3. 导入后抽查（最近更新）

```groq
*[_type == "blog" && language == "zh" && _updatedAt > "2026-05-29T00:00:00Z"]{
  _id, title, "slug": slug.current, _updatedAt
}[0...10]
```

```groq
*[_type == "compositePage" && category == "feature" && language == "en" && _updatedAt > "2026-05-29T00:00:00Z"]{
  _id, title, sourceType, "slug": slug.current
}[0...10]
```

---

## 4. CLI 示例

```bash
cd "…/1-4 Dev/lovart.sanity.studio"

npx sanity documents query '*[_type=="blog" && slug.current=="my-slug" && language=="en"][0]._id' \
  --dataset production

npx sanity documents query '*[_type=="compositePage" && category=="feature" && slug.current=="graphic-design"]{_id,language}' \
  --dataset production
```

需已 `npx sanity login` 或配置 token。

---

## 5. 与脚本验收的关系

| 场景 | GROQ | 脚本 |
|------|------|------|
| import 前「要不要转这篇」 | §1 查 `_id` | — |
| Blog import 后 | §3 | `verify-blog-publish.js --with-user-token` |
| Features/Tools import 后 | §3 | `verify-composite.js --with-user-token -- --type features --sample 20` |

---

## 6. 相关文档

- [first-run-and-incremental-policy.md](./first-run-and-incremental-policy.md) — `--missing` 语义
- [SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md](./SOP-Lovart-Sanity-Blog-Features-Tools-换设备交接与首次运行.md)
