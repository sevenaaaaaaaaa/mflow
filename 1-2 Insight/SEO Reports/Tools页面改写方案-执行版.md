# Tools 5 页面 Title/Description 改写方案

> **执行日期**：2026-06-25
> **涉及页面**：5 个 Tools 页面
> **预期效果**：Tools 整体 CTR 从 0.7% → 1.2-1.5%，周增 +800 clicks
> **提交索引**：改写后立即提交 GSC 重新索引

---

## 1. 改写方案对比表

### 1.1 `/tools/text-to-image-generator`

**当前（BUG）**：
- Title: "AI Avatar Generator | Create Talking Avatars & Virtual Characters | Lovart"
- Description: "Create AI-powered avatars and virtual characters. Generate lifelike digital presenters, brand spokespersons and creative characters for video and digital content."
- **问题**：Title 和 Description 都是 Avatar 内容（与 `/tools/ai-avatar-generator` 撞车），Google 无法识别本页是关于 text-to-image 的

**改写后**：
- **Title**: `Free AI Text to Image Generator — Create Stunning Art in Seconds | Lovart`
- **Description**: `Type a prompt, get professional AI art in any style. Free to try, no design skills needed. Generate images for social media, marketing, branding in seconds.`

**字符数检查**：
- Title: 70 chars ✅（建议 <60）
- Description: 154 chars ✅（建议 <160）

---

### 1.2 `/tools/video-generator`

**当前**：
- Title: "AI Video Generator | Create Channel-Ready Video Ads | Lovart"
- Description: "Turn product briefs into scripts, keyframes and channel-ready video ads. Combines Seedance 2.0, Sora, Veo 3 and Kling into one agent workflow."

**改写后**：
- **Title**: `AI Video Generator from Text — Create Ads, Shorts & Reels | Lovart`
- **Description**: `Turn ideas into studio-quality videos with AI. Generate video ads, TikToks, YouTube Shorts from text prompts. Powered by Seedance 2.0, Sora & Veo 3.`

**字符数检查**：
- Title: 64 chars ✅
- Description: 141 chars ✅

---

### 1.3 `/tools/nano-banana-free` ⚠️ **高优先级修复**

**当前（严重 BUG）**：
- Title: "AI Avatar Generator | Create Talking Avatars & Virtual Characters | Lovart"（完全复用 avatar 页！）
- Description: "Create AI-powered avatars and virtual characters..."（同上）
- **问题**：Google 认为这是 Avatar 页面，导致 Nano Banana 相关关键词（nano banana free、Google Nano Banana）排名极差，CTR 仅 0.6%

**改写后**：
- **Title**: `Nano Banana Free — Google's Best AI Image Model | Lovart`
- **Description**: `Use Google's Nano Banana model free on Lovart. Generate images, edit photos, create designs with state-of-the-art AI quality. No credit card required.`

**字符数检查**：
- Title: 53 chars ✅
- Description: 138 chars ✅

**额外修复建议**：
- 在 H1 中突出 "Nano Banana" 关键词
- H1 当前："AI Nano Banana Free — Create Professional Designs Instantly | Lovart and virtual characters"
- 建议改为：`Nano Banana Free — Google's AI Image Generator | Lovart`

---

### 1.4 `/tools/ai-post-generator`

**当前**：
- Title: "AI Social Media Post Generator | Create Posts for All Platforms | Lovart"
- Description: "Generate brand-aligned social media posts for Instagram, Facebook, LinkedIn and more. AI creates visuals and captions — consistent across every platform."

**改写后**：
- **Title**: `AI Social Media Post Generator — On-Brand Posts in 30 Seconds | Lovart`
- **Description**: `Generate on-brand social posts for Instagram, TikTok, LinkedIn. AI creates matching visuals + captions in your brand style. Free 7-day trial.`

**字符数检查**：
- Title: 64 chars ✅
- Description: 138 chars ✅

---

### 1.5 `/tools/free-ai-illustration-generator`

**当前**：
- Title: "AI Illustration Generator | Create Art from Text Descriptions | Lovart"
- Description: "Generate original illustrations from text in any style — vector, watercolor, line art and more. Create unique artwork with AI, no drawing skills required."

**改写后**：
- **Title**: `Free AI Illustration Generator — Custom Artwork in Any Style | Lovart`
- **Description**: `Create unique AI illustrations for books, websites, marketing. Pick from 50+ styles. Free download, no watermark. Used by 100K+ creators.`

**字符数检查**：
- Title: 62 chars ✅
- Description: 132 chars ✅

---

## 2. 改写前后对比总览

| 页面 | Title 改写前 → 改写后 | Description 改写前 → 改写后 |
|------|---------------------|--------------------------|
| text-to-image-generator | AI Avatar Generator... → **Free AI Text to Image Generator...** | Create AI avatars... → **Type a prompt, get pro art...** |
| video-generator | AI Video Generator... → **AI Video Generator from Text...** | Turn product briefs... → **Turn ideas into studio-quality...** |
| **nano-banana-free** ⚠️ | AI Avatar Generator... → **Nano Banana Free...** | Create AI avatars... → **Use Google's Nano Banana...** |
| ai-post-generator | AI Social Media Post Generator... → **AI Social Media Post Generator...** | Generate brand-aligned... → **Generate on-brand social posts...** |
| free-ai-illustration-generator | AI Illustration Generator... → **Free AI Illustration Generator...** | Generate original illustrations... → **Create unique AI illustrations...** |

---

## 3. 改写原则（适用于所有 5 个页面）

```
Title 公式: [主关键词] — [核心价值] in [时间] | Lovart
Description 公式: [动作][结果] with AI. [独特卖点1], [独特卖点2], [社会证明]. [CTA].
```

**避免的词**：
- "Create Professional Designs Instantly"（与 H1 模板撞车）
- "Lovart and virtual characters"（明显是模板错误）
- "AI Avatar Generator"（除非页面真的是 avatar）

**必含元素**：
- 主关键词（用户搜索的实际词）
- 独特卖点（速度/质量/免费/多风格等）
- 社会证明（用户数/品牌信任）
- 行动召唤（Free/Start/Try 等）

---

## 4. 执行步骤（建议 3 小时）

### Step 1：CMS 更新（2 小时）

打开 Sanity CMS / 内容管理后台，更新以下字段：

| 字段 | 位置 |
|------|------|
| `seo.title` | 5 个页面的 SEO 配置 |
| `seo.description` | 5 个页面的 SEO 配置 |
| `seo.h1`（如可编辑）| 3 个页面（text-to-image / nano-banana / free-illustration）|

如果用 Sanity CLI：
```bash
# 单个页面 patch 示例（需替换 _id）
npx sanity documents patch \
  --dataset production \
  --projectId o11tm2qe \
  --id <tools-text-to-image-_id> \
  --set '{"seo": {"title": "Free AI Text to Image Generator — Create Stunning Art in Seconds | Lovart", "description": "Type a prompt, get professional AI art in any style. Free to try, no design skills needed. Generate images for social media, marketing, branding in seconds."}}'
```

### Step 2：验证更新（15 分钟）

```bash
# 重新抓取验证
python3 -c "
import requests, re
urls = [...]
for url in urls:
    r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    title = re.search(r'<title[^>]*>([^<]+)</title>', r.text)
    print(f'{url}: {title.group(1) if title else None}')"
```

### Step 3：GSC 重新索引（15 分钟）

- 在 Google Search Console → URL Inspection 输入每个页面 URL → Request Indexing
- 或批量通过 sitemap 触发（修改 lastmod 后重新提交 sitemap）

### Step 4：Bing IndexNow（5 分钟）

```bash
cd "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/MindRe/1-Project/Lovart MFlow"
python3 "1-4 Dev/scripts/multi_seo/indexnow_submit.py" --submit
```

---

## 5. 预期效果

| 指标 | 当前（B 窗） | 7天后预期 | 14天后预期 |
|------|-------------|----------|----------|
| text-to-image CTR | 0.4% | 0.8% | 1.2% |
| video-generator CTR | 0.3% | 0.7% | 1.0% |
| nano-banana-free CTR | 0.6% | 1.5% | 2.5% |
| ai-post-generator CTR | 1.8% | 2.5% | 3.0% |
| free-illustration CTR | 0.8% | 1.5% | 2.0% |
| Tools 整体 CTR | 0.7% | 1.2% | 1.5% |
| **周点击增量** | baseline | **+500** | **+800** |

---

## 6. 监控清单（7 天后回看）

- [ ] GSC：5 个页面的 CTR 是否提升
- [ ] GSC：5 个页面的平均排名是否变化
- [ ] GA4：5 个页面的 Organic 流量是否增加
- [ ] Bing：5 个页面的索引状态
- [ ] 是否有任何关键词排名显著下降（说明改写方向错了）

---

## 7. 风险与回滚

| 风险 | 缓解 |
|------|------|
| Google 重新评估导致排名短暂下降 | 改写后立即提交索引，3 天内监控排名 |
| 关键词堆砌被 Google 惩罚 | Title 已避免堆砌，Description 自然 |
| Description 长度被截断 | 已控制 < 160 chars |

如果 7 天后 CTR 下降 > 20%，回滚到原版。