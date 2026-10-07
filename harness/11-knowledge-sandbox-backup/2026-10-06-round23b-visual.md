# Round 23b（2026-10-06）：视觉修复 + 浏览器截图验收通过

用户反馈"完全看不到任何前端样式"——根因：**block theme 不自动加载 style.css**（传统主题行为，block theme 必须显式 enqueue）。修复链：
1. functions.php 加 wp_enqueue_scripts（style.css + Google Fonts：Instrument Serif/Noto Serif SC/Inter/Barlow Condensed）
2. 字体栈修正：主站标题字体实际 token 是 --font-serif-deck（Feature-Deck 字体），非猜的 serif-display；子站用 Instrument Serif fallback
3. 按钮样式作用域全局化（原选择器只命中 cta-default 区块，hero 内不生效）
4. hero 内主按钮亮色（深底可见性）
5. 样式写足：设计 tokens :root 桥接/hero 深底全屏+serif clamp 大标题+黄绿斜体高亮/CTA 浅灰卡片/博客排版（mono 日期/serif 标题）

**浏览器截图验收**（browser-use，不再让用户试）：
- hero：深底圆角容器 + AI DESIGN PARTNER badge（mono 大写）+ serif 大标题 + 黄绿斜体高亮 + 白色主按钮/ghost 次按钮 ✓
- CTA：浅灰卡片 + serif 标题 + 深色胶囊按钮 ✓
- 页脚品牌口号 + Try Free ✓

git 3730151。视觉基线确立——P1 组件按此密度开发。
