# WordPress 设计复刻 · 开发区

- `lovart-theme/` — Lovart 主题（Gutenberg 原生区块路线，R1 定稿 2026-10-06）
  - theme.json：381 设计 tokens → WP 语义映射（palette 9 / 字体栈 / 流式字号 / custom 全量桥接）
  - blocks/：`lovart/{type}` 区块（block.json + render.php），functions.php 自动注册
  - 首批 2 个范式区块：hero-cinematic / cta-default
- `wp-blocks-poc/` — 三路线映射 POC 产物（定稿依据）
- `docker-compose.yml` — 本地测试环境（:8090，主题热挂载）

## 路线定稿记录（2026-10-06）——✅ 全链路验证完成

**R1 原生区块胜出**，依据：
- 数据层 POC（真实 landing-full JSON：15 sections/311 字段/30 列表/34 媒体/29 嵌套）：Gutenberg 属性直塞无损；ACF 深嵌套 repeater 爆炸；Elementor 拍平语义全丢
- **渲染层实测（本地 Docker WP 6.7 + wp-cli）**：lovart 主题激活 → hero-cinematic + cta-default 区块注册 → 测试页渲染 8 项断言全 PASS（badge/serif 标题/黄绿高亮/description/按钮含 ghost/CTA）
- **tokens 生效实测**：theme.json palette 9 色 + custom 96 组在前端输出 `--wp--preset--color--base/brand/text/base-secondary` ✓
- 排查记录：缺 page.html 会回退 index 导致 page content 不渲染（已补）；theme.json 探查误判（wp eval 转义问题），最终以前端 CSS 变量输出为准

设计 tokens：381 项（主站 CSS 反推，design-tokens.json）——语义色 #100f09 文本 / #f9f8f6 底 / #147dff 品牌 / #c4ff8c 黄绿高亮 / serif-display 标题字体。

## 下一步（P1 组件开发前的注意）
- docker compose up -d → http://localhost:8090（wp / Lovart2026!x）
- 新组件范式：blocks/{type}/block.json + render.php，functions.php 自动注册
- 每组件渲染断言脚本化（curl grep 类名+内容）
