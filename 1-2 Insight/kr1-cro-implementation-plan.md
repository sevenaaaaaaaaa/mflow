# KR1 CRO 实施方案 — Meta Description + 首页 CTA

> **日期**：2026-06-14
> **目标**：Top 5 非品牌词 CTR 从 <0.3% → 2-3%；首页注册转化率提升

---

## 一、Top 5 非品牌词 Meta 重写

### 当前问题

首页 Title: `Lovart – World's First AI Design Agent | Create Pro Designs in Minutes`
→ 完全不包含任何非品牌关键词，用户搜竞品词看到这个标题不会点击

### 优化方案

#### 方案 A：首页 Title/Description 动态适配（推荐）

在首页 `<head>` 中加入条件逻辑，根据 referrer 或 URL 参数动态切换 Meta：

```html
<!-- 默认 Meta -->
<title>Lovart – World's First AI Design Agent | Create Pro Designs in Minutes</title>
<meta name="description" content="Lovart is the world's first AI design agent. Create logos, posters, brand kits & marketing assets from one brief. Free 500 daily credits. No credit card needed.">
```

#### 方案 B：为每个关键词创建独立落地页（长期方案）

| 关键词 | 目标页面 | Title | Description |
|--------|---------|-------|-------------|
| **freepik ai** | `/tools/ai-image-generator/` | `Freepik AI Alternative — Free AI Image Generator \| Lovart` | `Create stunning images for free with Lovart's AI Design Agent. No design skills needed. Generate logos, posters & brand assets in seconds. Try free — no credit card required.` |
| **freepik ai image generator** | `/tools/ai-image-generator/` | `Free AI Image Generator — Better Than Freepik AI \| Lovart` | `Generate professional images instantly with Lovart's AI agent. Supports logos, posters, social media graphics & more. Free 500 daily credits. No credit card needed.` |
| **artlist ai** | `/` (首页) | `Artlist AI Alternative — Free AI Design Agent \| Lovart` | `Lovart is a free AI design agent that creates brand visuals, marketing assets & video content. One brief → full campaign. Trusted by 10M+ creators worldwide.` |
| **luma dream machine** | `/tools/ai-video-generator/` | `Luma Dream Machine Alternative — AI Video + Design Agent \| Lovart` | `Lovart goes beyond video generation. Create complete brand campaigns — logos, posters, social media & video — with one AI design agent. Free to start.` |
| **flora ai** | `/` (首页) | `Flora AI Alternative — Free AI Design Agent for Creators \| Lovart` | `Create professional designs with Lovart's AI agent. Generate logos, brand kits, marketing assets & more — all from one brief. Free 500 daily credits. Try now.` |

### 预期效果

| 指标 | 当前 | 优化后 | 增量 |
|------|------|--------|------|
| 月点击（5 词合计） | 134 | ~1,995 | +1,861 |
| 月新增注册（按 14.4%） | 19 | ~287 | +268 |
| 月新增付费（按 1.11%） | 0.2 | ~3.2 | +3 |

---

## 二、首页 CTA 优化

### 当前问题

1. 首屏 Hero 区 CTA 是 "Design now"，不够直接
2. 主要注册 CTA "Get started for free" 在页面中下部
3. 首屏无 Social Proof

### 优化方案

#### 2.1 首屏加 Social Proof 横幅

在 Hero 区下方、Agentic Intelligence 上方插入：

```html
<section class="social-proof-banner">
  <div class="trust-metrics">
    <span>🌍 Trusted by 10M+ creators in 70+ countries</span>
    <span>⭐ 4.2/5 on ReviewNexa</span>
    <span>🎨 500M+ designs created</span>
  </div>
</section>
```

**样式建议**：
- 背景：半透明深色/品牌色
- 字体：14-16px，白色
- 布局：横向滚动或 flex 居中
- 位置：Hero 区正下方，用户滚动前就能看到

#### 2.2 首屏 Hero CTA 强化

将 Hero 区的 CTA 从 "Design now" 改为更直接的注册引导：

```html
<!-- 当前 -->
<button>Design now</button>

<!-- 优化后 -->
<div class="hero-cta-group">
  <button class="primary">Start Free — No Credit Card</button>
  <button class="secondary">See How It Works</button>
</div>
```

**关键改动**：
- 主按钮文案：强调 "Free" + "No Credit Card"（降低心理门槛）
- 次按钮：给犹豫用户一个缓冲选项
- 按钮颜色：主按钮用高对比色（品牌强调色）

#### 2.3 底部 CTA 增加 Urgency 元素

```html
<!-- 当前 -->
<h2>Design with Lovart</h2>
<p>Create with momentum. Bring your vision to life.</p>
<button>Get started for free</button>

<!-- 优化后 -->
<h2>Start Creating for Free</h2>
<p>Join 10M+ creators. 500 daily credits. No credit card needed.</p>
<button>Get Started Free →</button>
<p class="urgency">🔥 2,847 creators signed up today</p>
```

---

## 三、执行清单

### 本周（W1）

| # | 动作 | 方式 | 优先级 |
|---|------|------|--------|
| 1 | 首页默认 Meta Description 更新 | 修改 Sanity CMS 首页 SEO 字段 | P0 |
| 2 | 首屏 Social Proof 横幅 | 前端代码 + Sanity 组件 | P0 |
| 3 | 首屏 Hero CTA 文案修改 | 前端代码 | P0 |
| 4 | 底部 CTA 增加 Urgency | 前端代码 | P1 |

### 下周（W2）

| # | 动作 | 方式 | 优先级 |
|---|------|------|--------|
| 5 | `/tools/ai-image-generator/` 页面 Meta 优化 | Sanity CMS | P0 |
| 6 | `/tools/ai-video-generator/` 页面 Meta 优化 | Sanity CMS | P0 |
| 7 | artlist ai / flora ai 首页 Meta A/B 测试 | GSC 数据验证 | P1 |

### W3-W4

| # | 动作 | 方式 | 优先级 |
|---|------|------|--------|
| 8 | 注册流程审计（Hotjar/Clarity） | 安装热力图工具 | P0 |
| 9 | Google 一键登录置顶 | 前端代码 | P1 |
| 10 | Paywall 策略调整 | Product 决策 | P1 |

---

## 四、验证方式

1. **Meta 修改后**：GSC → 搜索效果 → 筛选这 5 个关键词 → 观察 CTR 变化（2-4 周见效）
2. **首页 CTA 修改后**：GA4 → 首页注册按钮点击事件 → 对比修改前后
3. **Social Proof 横幅**：Hotjar 热力图 → 观察首屏停留时间和滚动率

---

*KR1 CRO Action #3 完成。下一步：确认落地页 URL → 执行 Meta 修改。*
