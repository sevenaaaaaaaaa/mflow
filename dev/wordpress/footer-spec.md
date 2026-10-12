# 站点页脚内容规格（给 Elementor Theme Builder 用）

> 由 `split-footer.py` 从 5 个页面共用的 cta-default 块里抽出。
> 这 5 页的页脚 HTML **完全一致**（md5 相同），所以一份全站模板即可。

## 栏目与链接

### Company

| 文案 | 链接 |
|---|---|
| Pricing | `https://www.lovart.ai/pricing` |
| Changelog | `https://www.lovart.ai/changelog` |
| Docs | `https://www.lovart.ai/docs` |
| News | `https://www.lovart.ai/news` |
| Terms of Use | `https://www.lovart.ai/statement/terms-of-use` |
| Privacy Policy | `https://www.lovart.ai/statement/privacy-policy` |

### Resources

| 文案 | 链接 |
|---|---|
| Explore | `https://www.lovart.ai/explore` |
| Blog | `https://www.lovart.ai/blog` |
| Tools | `https://www.lovart.ai/tools` |
| Features | `https://www.lovart.ai/features` |
| Solutions | `https://www.lovart.ai/solutions` |
| Topics | `https://www.lovart.ai/topics` |

### Social

| 文案 | 链接 |
|---|---|
| X | `https://twitter.com/lovart_ai` |
| YouTube | `https://www.youtube.com/@lovart_ai` |
| LinkedIn | `https://www.linkedin.com/company/lovart-ai` |
| Instagram | `https://www.instagram.com/lovart.ai` |
| TikTok | `https://www.tiktok.com/@lovart_ai` |

## 版权

`© 2026 All Rights Reserved, Lovart`

## 主题 / 语言切换器

页脚里还有两个切换器按钮：Auto · English · Auto · English。
它们的行为在 `replica.js` 的 `initTheme` / `initLang` 里。
**Theme Builder 版页脚要不要保留它们，需要你定** —— 若不保留，
迁移后记得把 `initTheme` / `initLang` 一并删掉。

## 搭建建议

用 Elementor **核心免费微件**即可，不要依赖插件包（页脚是全站件，依赖越少越好）：

- 容器（flex 横向，3 列）
- 每列：Heading（栏标题）+ Icon List（链接，关掉图标）
- 底部：Text Editor（版权）

搭好后在 Theme Builder 里把显示条件设为「整站」，
然后跑 `split-footer.py --write` 把这 5 页块里的页脚摘掉。

原始 HTML 见 `footer-raw.html`（作视觉比对基准）。
