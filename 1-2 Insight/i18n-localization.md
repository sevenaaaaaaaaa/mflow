# Lovart i18n 约束文件

> 创建日期：2026-06-14
> 用途：落地页 CRO 多语言本地化改写约束

---

## 一、目标语言

| 语言 | 代码 | 优先级 | 备注 |
|------|------|--------|------|
| English | en | P0 | 默认语言，所有页面先有 EN 版本 |
| Deutsch | de | P0 | 德国市场，高付费转化 |
| Français | fr | P0 | 法国市场 |
| Italiano | it | P0 | 意大利市场 |
| 日本語 | ja | P0 | 日本市场，高设计需求 |
| 한국어 | ko | P0 | 韩国市场，高社媒需求 |
| Português | pt | P0 | 巴西市场 |
| Русский | ru | P1 | 俄罗斯市场 |
| 简体中文 | zh | P1 | 中国市场 |
| 繁體中文 | zh-TW | P1 | 台湾/香港市场 |

---

## 二、翻译原则

### 2.1 本地化改写（非直译）

**禁止**：逐字翻译英文文案
**要求**：根据目标市场的表达习惯重新撰写

示例：
- EN: "Start Creating Free" → JA: "今すぐ無料で始める"（直译OK，日语简洁）
- EN: "No design skills needed" → DE: "Keine Vorkenntnisse nötig"（德语习惯用"Vorkenntnisse"而非直译"Design-Fähigkeiten"）
- EN: "10x faster" → ZH: "速度快10倍"（中文数字前置）

### 2.2 品牌术语不翻译

以下术语保持英文原文，不翻译：
- Lovart
- ChatCanvas
- Nano Banana
- Seedream
- Seedance
- GPT Image
- Flux
- Veo
- Kling

### 2.3 格式要求

| 元素 | 约束 |
|------|------|
| **hero.title** | ≤60 字符，含主关键词 + `| Lovart` |
| **hero.description** | 120-160 字符，含 1-2 个长尾词 |
| **hero.badge** | 用目标语言的品类名 |
| **highlightedText** | 5-8 词，核心差异点 |
| **faq.question** | 含目标语言的搜索意图关键词 |
| **faq.answer** | 80-150 字符，包含品牌术语 |
| **cta.title** | 行动导向，含"免费"类词汇 |
| **cta.description** | 强调低门槛（无信用卡、免费额度等） |

### 2.4 SEO 关键词本地化

每个语言需要根据当地搜索习惯调整关键词：

| 语言 | 主关键词模式 | 示例 |
|------|-------------|------|
| EN | "AI [Category] Maker" | "AI Poster Maker" |
| DE | "KI [Kategorie] Ersteller" | "KI-Poster-Ersteller" |
| FR | "Créateur [Catégorie] IA" | "Créateur d'Affiche IA" |
| IT | "Creatore [Categoria] IA" | "Creatore Poster IA" |
| JA | "AI [カテゴリ] メーカー" | "AI ポスターメーカー" |
| KO | "AI [카테고리] 메이커" | "AI 포스터 메이커" |
| PT | "Criador de [Categoria] IA" | "Criador de Pôster IA" |
| RU | "ИИ [Категория] Создатель" | "ИИ Создатель Постеров" |
| ZH | "AI [类别] 生成器" | "AI 海报生成器" |
| ZH-TW | "AI [類別] 生成器" | "AI 海報生成器" |

---

## 三、CRO 文案本地化规则

### 3.1 Hero Section

```
标题结构：[主关键词] — [价值主张] | Lovart
描述结构：[120-160字符，含主关键词+长尾词+CTA暗示]
高亮文本：[5-8词核心差异]
```

各语言价值主张参考：
- EN: "Create Professional Designs Instantly"
- DE: "Professionelle Designs sofort erstellen"
- FR: "Créez des designs professionnels instantanément"
- IT: "Crea design professionale istantaneamente"
- JA: "プロのデザインを瞬時に作成"
- KO: "전문적인 디자인을 즉시 생성"
- PT: "Crie designs profissionais instantaneamente"
- RU: "Создавайте профессиональный дизайн мгновенно"
- ZH: "即时创建专业设计"
- ZH-TW: "即時創建專業設計"

### 3.2 CTA 按钮

| 语言 | 主 CTA | 次 CTA |
|------|--------|--------|
| EN | "Start Free — No Credit Card" | "See Examples" |
| DE | "Kostenlos starten" | "Beispiele ansehen" |
| FR | "Commencer gratuitement" | "Voir les exemples" |
| IT | "Inizia gratis" | "Vedi esempi" |
| JA | "無料で始める" | "サンプルを見る" |
| KO | "무료로 시작하기" | "예시 보기" |
| PT | "Comece grátis" | "Ver exemplos" |
| RU | "Начать бесплатно" | "Смотреть примеры" |
| ZH | "免费开始" | "查看示例" |
| ZH-TW | "免費開始" | "查看範例" |

### 3.3 FAQ

FAQ 需覆盖目标语言的搜索意图：
1. 价格/免费相关（"Is [品类] free?" → 目标语言等价表达）
2. 新手相关（"Do I need experience?" → 目标语言等价表达）
3. 版权相关（"Can I use commercially?" → 目标语言等价表达）
4. 格式相关（"What formats?" → 目标语言等价表达）
5. 对比相关（"How is it different from [竞品]?" → 目标语言等价表达）

---

## 四、质量门禁

### 4.1 上线前检查

- [ ] 所有 10 种语言版本已创建
- [ ] hero.title ≤ 60 字符
- [ ] hero.description 120-160 字符
- [ ] hero.buttons 链接指向 `/home`
- [ ] 所有 CTA 按钮有 href
- [ ] FAQ ≥ 5 条
- [ ] 品牌术语未被翻译
- [ ] SEO 关键词已本地化（非直译）

### 4.2 CRO 指标

| 指标 | 目标 |
|------|------|
| 多语言覆盖率 | 100% 页面 × 10 语言 |
| CTA 点击率 | > 2% |
| FAQ 展开率 | > 15% |
| 首屏跳出率 | < 40% |

---

## 五、翻译工作流

```
1. EN 版本 → 确保 14-section 结构完整 + CRO 文案优化
2. 批量翻译 → 9 种语言 × 每页 14 个 section
3. 本地化审核 → 品牌术语、SEO 关键词、CTA 按钮
4. 上线 → 验证 canonical 指向 EN 版本
```

---

## 六、备注

- **canonical**：所有非 EN 版本的 `seo.canonical` 指向 EN 版本 URL
- **hreflang**：由前端代码根据 `language` 字段自动生成
- **图片**：多语言版本共用同一套图片（图片不含文字）
- **brand**：brand 字段由 Sanity 全局控制，无需每页设置
