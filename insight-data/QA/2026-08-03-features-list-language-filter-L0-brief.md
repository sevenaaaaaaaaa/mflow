# Features 列表页 L0：按 language 过滤 — 前端修复 Brief

> 日期：2026-08-03  
> 受众：主站前端（apps/lovart）  
> 优先级：P0  
> 内容侧状态：Sanity 各语言 title/description 跨语言污染已清零；用户仍可能看到混语言卡片，根因在列表查询未过滤 `language`。

## 问题
`/features`（及各语言前缀列表）拉取 `compositePage` 时未按当前路由语言过滤，导致 EN 列表混入 DE/ZH/JA 等文档卡片（此前观测约 27 张跨 10 语言）。

## 期望行为
- 访问 `/features` 或 `/en/features` → 仅 `language == "en"`（或站点默认语言约定）
- 访问 `/de/features` → 仅 `language == "de"`
- 其余 `fr/it/ja/ko/pt/ru/zh/zh-TW` 同理
- 同一 `slug` 多语言文档不得出现在错误语言列表中

## 建议 GROQ 形态（示意）
```groq
*[_type == "compositePage"
  && category == "feature"   // 或你们现用的 features 判定
  && language == $lang
  && !(_id in path("drafts.**"))
] | order(coalesce(releaseDate, _updatedAt) desc) {
  _id, title, language, "slug": slug.current, cover, description, seo
}
```

## 实现检查清单
1. 列表页 query 增加 `language == $lang`，`$lang` 来自路由/locale
2. 确认不要用「只按 slug 去重、忽略 language」的合并逻辑
3. 若存在 `features-` / 无前缀 / UUID 多 `_id`，列表应只取前端约定的那一类（内容侧经验：无前缀 `-{lang}` 为常用可读版）
4. ISR/CDN：发布后对 `/[lang]/features` 做 revalidate 或 purge，避免旧卡片标题残留
5. 回归：打开 en/de/ja/zh-TW 四个列表，目视卡片标题文字脚本是否与语言一致

## 非本 brief 范围
- 列表页 H1/面包屑/CTA 硬编码英文（L1 i18n）— 可另开任务
- bodyJson 详情页语言残留（L3）— 内容侧后续批次
- Sanity schema 变更 — 不需要

## 验收标准
- 每个语言列表页卡片语言纯净（无中文出现在 DE/EN/FR 等列表）
- 同 slug 不会在错误语言列表重复出现
- 清缓存后抽查与 Sanity 当前 title 一致
