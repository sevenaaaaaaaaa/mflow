# Round 31（2026-10-07）：Canvas 模板 + v5 交互与颜色修复（用户五问题全闭环）

用户五问题：红边框/滑块不能拖/莫名回顶/footer 多版权行/**应该用 Elementor Canvas 而非主题实现**。

**Canvas 模板**：7 页 REST 设 template=elementor_canvas——WP header/HFE footer/页面标题全部剥离（本机被 reset 看不到新状态是 CDN/浏览器缓存，加 cache-buster 验证 body=page-template-elementor_canvas、visibleHeaders=1）。
**v5 修复**：FAQ 粉边框（Hello 主题 button 全局样式）→ border none + color var(--text-default)；深色页面底色 → scope background var(--bg-base-default)；交互 JS 注入（FAQ 手风琴点击/before-after 滑块 pointer 拖动 clip-path/marquee keyframes/header 滚动收缩/href# 防跳顶）。验证：FAQ button border 0px、色 rgb(245,244,239) 深色白字 ✓；整页深色与主站一致 ✓。
**历史教训修正**：深色 overlay 灾难的真因是当时页面在浅色主题上——Canvas+dark scope 后深色渲染正常，无需 overlay hack。
git 最新。**效果**：blogs.lovart.ai/composite-replica-all 与主站 composite-page-all 同构（单 header/深色/33 组件）。
