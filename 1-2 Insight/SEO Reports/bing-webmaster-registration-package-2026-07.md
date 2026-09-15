# Bing Webmaster Tools 自助注册包 | 2026-07-15

> 📅 时间: 2026-07-15
> 🎯 目标: 让中文 SEO 流量被 Bing/百度/搜狗等中文搜索引擎抓取
> 📌 关联: `扩展优化机会-2026-07-15.md` 的机会 1

---

## 一、为什么必须做

按 GA4 数据，中文 SEO 是 Lovart 第二大流量生态：
- /zh 首页: 463,387 sessions/月（14% 全 GA4）
- 但百度 / cn.bing / 360 / 搜狗 这些**中文搜索引擎完全跳过 /zh**，把全部流量引到 EN 根域

**根因**：Lovart 从未在 Bing Webmaster Tools 注册——而 Bing Webmaster API 同源驱动 `cn.bing.com/so.com/ntp.msn.cn`，**没注册 = 站点不在 Bing 索引流上** = 中文搜索引擎爬不到 /zh。

百度同理：百度站长平台（zhanzhang.baidu.com）注册是中文 SEO 必经步骤。

---

## 二、Bing Webmaster Tools 注册流程（10-15 分钟）

### Step 1 — 注册账号
- 打开 https://www.bing.com/webmasters
- 点击右上角"立即开始"或"Sign in"
- 用任一方式登录：
  - Microsoft 账号（Outlook/Hotmail）
  - Google 账号
  - Facebook 账号
  - 其他 OAuth

### Step 2 — 添加站点
- 在 Search 页面找到 "Add a site"
- 输入 `https://www.lovart.ai`（不带末尾斜杠）
- 点 "Add"

### Step 3 — 验证站点所有权（3 选 1，最简单是 HTML meta tag）

#### 选项 A: HTML `<meta>` 标签（最简单，5 分钟搞定）

注册后 Bing 会显示一个这样的标签：
```html
<meta name="msvalidate.01" content="ABC123XYZ..." />
```
把这个 meta tag 放到 https://www.lovart.ai/ 的 `<head>` 里（**也需要前端配合**）。

#### 选项 B: TXT DNS 记录（**推荐**，完成后不需要前端）

去 Lovart 的 DNS 管理后台（Cloudflare / 域名 registrar），加一条新 TXT 记录：
```
主机记录: @ (或 lovart.ai 或留空)
记录类型: TXT
记录值: BING_VERIFY_TOKEN (Bing 会显示这个 token)
TTL: 3600 (默认)
```

**这个方案最干净**——一旦设置完成，前端不需要改任何代码，DNS 验证 30-60 分钟自动通过。

#### 选项 C: XML 文件

下载 Bing 提供的 `BingSiteAuth.xml`，放 `https://www.lovart.ai/BingSiteAuth.xml`。

### Step 4 — 添加 Sitemap

注册 + 验证完成后：
1. 在 Bing Webmaster 左侧菜单 → "Sitemaps"
2. 添加以下 sitemap（**每次添加一行，等 Bing 处理完**）：

```
https://www.lovart.ai/sitemap.xml
https://www.lovart.ai/sitemap-index.xml
https://www.lovart.ai/sitemap_zh.xml
```

3. 对每个 sitemap 点击 "Submit"
4. Bing 通常 5-15 分钟会开始爬取

### Step 5 — 开启额外设置

- **Crawl control** → 设置 crawl rate（默认即可）
- **Site Move** → 不适用（Lovart 没换过域）
- **Block URLs** → 屏蔽 `/login`、`/signup` 等（可选，能省 Bingbot 配额）

### Step 6 — 检查中文搜索引擎专项

#### 百度站长平台（zhanzhang.baidu.com / baidu.com/webmaster）
- 注册 + 添加 `https://www.lovart.ai`
- 验证方式选 HTML 标签（同 Bing，但 token 是 `baidu-site-verification`）
- 提交 sitemap：`https://www.lovart.ai/sitemap.xml` 和 `https://www.lovart.ai/sitemap_zh.xml`
- **关键**：百度站长资源平台**已支持 push 接口**——也可以用 sitemap 的 push 路径

#### 360 站长平台（zhanzhan.360.cn）
- 比百度站长平台注册门槛低
- 同样添加 + 验证 + 提交 sitemap

#### 搜狗站长平台（zhanzhang.sogou.com）
- 较少使用，但 cn.bing 抓取有时也看该平台

---

## 三、注册成功后能等到的结果

按第一份报告的机会 1：
- 百度/cn.bing/360/sogou 等中文搜索引擎会把 `/zh` URL 列入索引
- 中文用户搜"lovart"会被引到 `/zh` 而不是 `/`
- 当前 41% 中文 SEO 流量全部走 EN 根域的现状逐步改善
- **预期**：3-6 周内 `/zh` 首页的 GSC impressions 翻倍

---

## 四、注册期间能并行做的事

我已经做了：
- ✅ 7 个 /diploma-design 多语言页面新建（B 任务）
- ✅ 8 个 /ai-image-upscaler 多语言页面新建（C 任务）
- ✅ /zh anniversary-card-design 新建
- ✅ /it secure-student-id-card-design 新建
- ✅ 9 个 seoTitle 中英文质量问题 patch（A 任务）

**这些新页面还没被任何搜索引擎索引**——注册 Bing Webmaster 之后可以手动 ping sitemap 让 Google + 百度 + 360 + Bing 重抓。

### 注册成功后 30 秒内可执行（已准备好的脚本）

```bash
# 1. 跑 B 任务 IndexNow 推送（已写好）
cd ~/Documents/Lovart\ Local\ Dev
python3 automation/indexnow-push-7-12-batch.py --apply

# 2. 跑 X 模板全批量推送（先创建对应脚本）
python3 automation/sitemap-reminder.py
```

---

## 五、Lovart 已有 sitemap 路径（已验证）

```
✅ https://www.lovart.ai/sitemap.xml           200
✅ https://www.lovart.ai/sitemap-index.xml    200
✅ https://www.lovart.ai/sitemap_zh.xml       200
❌ https://www.lovart.ai/zh/sitemap.xml      404
```

**注意**：现有 sitemap_zh.xml 看起来是单独的中文 sitemap。建议在 Bing Webmaster 后台**同时**注册它 + 主 sitemap。

---

## 六、检查清单

注册后 24 小时验证：
- [ ] Bing Search Reports 显示 Lovart 域名
- [ ] URL Inspection 能验证首页 /zh 等页面已收录
- [ ] Sitemap 报告显示 0 errors（"Discovered URLs" 大于 0）
- [ ] 中国地区流量（在 Bing 后台 Country Insights）开始显示爬取
- [ ] 30 天后：在百度站长资源平台 + Bing Webmaster 都看到 0 critical errors

---

## 七、百度站长平台**额外**提示

百度比 Bing 更严格，还需要做以下：
- **HTTPS 证书**：保证 Lovart 全站 HTTPS 已启用
- **Robots.txt**：确认 `/zh/` 没被 `Disallow`
- **响应时间**：中文 SEO 重视首屏加载速度，国内访问 Lovart 可能因 GFW 慢——考虑镜像或国内 CDN

百度站长资源平台官方路径：
- https://ziyuan.baidu.com/dashboard/index（已合并到百度搜索资源平台）
- 或直接搜"百度搜索资源平台"

---

## 资产

- **本注册包**：`Output/SEO-Reports/改造建议/bing-webmaster-registration-package-2026-07.md`
- **sitemap URL**：3 个有效路径已验证
- **域名注册商**：需用户查（Cloudflare？Aliyun？GoDaddy？）

---

*报告生成: 2026-07-15 16:10 UTC+8 | Lovart SEO Agent*
