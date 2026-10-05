# WordPress 设计复刻 · 开发区

- `lovart-theme/` — Lovart 主题（Gutenberg 原生区块路线，R1 定稿 2026-10-06）
  - theme.json：381 设计 tokens → WP 语义映射（palette 9 / 字体栈 / 流式字号 / custom 全量桥接）
  - blocks/：`lovart/{type}` 区块（block.json + render.php），functions.php 自动注册
  - 首批 2 个范式区块：hero-cinematic / cta-default
- `wp-blocks-poc/` — 三路线映射 POC 产物（定稿依据）
- `docker-compose.yml` — 本地测试环境（:8090，主题热挂载）

## 路线定稿记录（2026-10-06）
R1 原生区块胜出——数据层 POC（真实 landing-full JSON：15 sections/311 字段/30 列表/34 媒体/29 嵌套）：
Gutenberg 属性直塞无损；ACF 深嵌套 repeater 爆炸；Elementor 拍平语义全丢。
渲染层与主站一致性由 theme.json（同一 tokens）+ 区块 render.php 保证；视觉对照主站逐组件校准。
设计 tokens：381 项（主站 CSS 反推，design-tokens.json）——语义色 #100f09 文本/#f9f8f6 底/#147dff 品牌/serif-display 标题。
