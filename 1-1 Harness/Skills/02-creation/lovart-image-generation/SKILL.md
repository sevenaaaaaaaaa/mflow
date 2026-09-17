---
name: lovart-image-generation
description: 为 Blog 封面、Features/Tools 页面横幅、分发配图和产品截图生成图片。调用 Lovart API（`lovart-api` skill），上传到 CDN，回写到对应 MD/JSON 的 `cover_url` 或 image 字段。
---

# lovart-image-generation

## 路径契约

| 层 | 路径 |
|----|------|
| 文档 SSOT | `1-1 GEO Readme/` |
| Sanity 脚本 | `1-4 Dev/lovart.sanity.studio/scripts/` |
| SEO/Sentinel 脚本 | `1-4 Dev/scripts/` |
| 自动化 | `1-4 Dev/automation/` |
| 本 Skill | `1-1 Harness/Skills/lovart-image-generation/SKILL.md` |

为 Blog 封面、Features/Tools 页面横幅、分发配图和产品截图生成图片。调用 Lovart API（`lovart-api` skill），上传到 CDN，回写到对应 MD/JSON 的 `cover_url` 或 image 字段。

## Triggers

- "生成封面" / "generate cover"
- "生成配图" / "generate article images"
- Pipeline Step 3.5 自动触发
- `generate images for {slug}`

## Prerequisites

- Lovart API 认证已配置：`Skills/lovart-api-config.md`（Access Key + Secret Key）
- `lovart-api` skill 可用：`Skills/30-clawx/clawx-openclaw-skills-lovart-skill/SKILL.md`
- 环境变量：`export LOVART_ACCESS_KEY=...` `export LOVART_SECRET_KEY=...`
- 输出图片上传到 `assets-persist.lovart.ai` CDN

---

## 图片需求矩阵

| 内容类型 | 图片需求 | 比例 |
|---------|---------|------|
| Sanity Blog | 1 张封面 + 2-4 张正文配图 | 16:9 |
| Features 页 | 1 张横幅 Hero | 16:9 |
| Tools 页 | 1 张工具卡片 | 1:1 |
| Landing 页 | 1 张 Hero | 2.35:1 |
| 分发配图 (X/LinkedIn/小红书) | 1-4 张 | 平台要求 |
| 产品截图 | N 张实际界面 | 原生尺寸 |

---

## Workflow

### Phase 1: 检查存量

```bash
# Blog：检查 frontmatter cover_url 是否已有
grep "cover_url" "1-3 Content Gen/Content Calendar/{category}/{slug}.md"

# Features legacy：检查 heroSection.image
# Tools v2：检查 bodyJson 内 media.src（正式源 Page Gen/Pages/Tools/）
python3 -c "import json; d=json.load(open('1-3 Content Gen/Page Gen/Pages/Tools/en/{slug}-en.json')); import json as J; s=J.loads(d['bodyJson']); print(next((x.get('media',{}).get('src') for x in s if x.get('media')), 'MISSING'))"
```

**跳过**：cover_url 已存在且以 `assets-persist.lovart.ai` 开头、且非占位符。

**封面池兜底**：存量文章使用 `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/Cover Url 随机调取.md`（46 个 liblib CDN URL）。Stable hash 算法（`pick-cover.py`）确保同 slug → 同封面。

### Phase 2: 生成图片

**Prompt 策略**：

> ⚠️ 封面/插图 prompt 工作流待用户提供。当前占位——以下为调用 Lovart API 的通用框架，具体 prompt 模板待替换。

通过 `lovart-api` skill 调用生成：

```bash
# GPT Image 2 模式（封面/海报类）
lovart chat {prompt} --model image --style gpt-image-2

# Nano Banana Pro 模式（产品图/细节类）
lovart chat {prompt} --model image --style nano-banana-pro
```

**品牌上下文**（注入到 prompt 中）：
- 品牌名：Lovart（L 大写）
- 品牌色：渐变紫蓝色调
- 产品特征：ChatCanvas 对话式界面、MCoT 推理引擎可视化、Touch Edit 手势操作
- 需要 Logo 时使用 Brand Kit 中的官方 Logo

### Phase 3: CDN 上传 + 回写

上传到 `assets-persist.lovart.ai` CDN 后回写原文件：

**Blog MD**：
```bash
# 更新 frontmatter cover_url
sed -i '' 's/cover_url:.*/cover_url: {new_cdn_url}/' \
  "1-3 Content Gen/Content Calendar/{category}/{slug}.md"
```

**Features/Tools JSON**：
```python
import json
path = '1-4 Dev/Pages/Features/en/{slug}-en.json'
d = json.load(open(path))
d['heroSection']['image'] = '{cdn_url}'
json.dump(d, open(path, 'w'), indent=2)
```

### Phase 4: 正文配图同步

对于 Blog 正文中的图片占位（如果有），替换为空或跳过占位符，确保不泄露 `[IMAGE PLACEHOLDER]` / `[REAL SCREENSHOT REQUIRED]`。

---

## 图片规范

| 规范 | 要求 |
|------|------|
| 封面 CDN | `https://assets-persist.lovart.ai/` 开头 |
| 格式 | PNG（Blog）/ WebP（网页优化） |
| Blog 封面尺寸 | 1200×630（16:9） |
| Features 横幅 | 2400×1350 |
| Alt text | 含焦点关键词的英文描述 |
| 正文图 | 禁止 `[IMAGE PLACEHOLDER]` / `[REAL SCREENSHOT REQUIRED]` |

## 存量封面策略

已有封面池（`1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/Cover Url 随机调取.md`，46 个 URL）。不重新生成封面时使用 Stable hash 分配。

```bash
python3 scripts/pick-cover.py {slug}
```

---

## Output

```
Output/Images/
├── YYYY-MM-DD/
│   ├── {slug}-cover.png
│   └── manifest.json
```

## TODO — 待用户补全

- [ ] **封面 prompt 工作流**：Blog/Features/Tools 各类型的最佳 prompt 模板
- [ ] **正文插图策略**：哪些场景需要插图、每篇最少/最多几张
- [ ] **品牌视觉资产库**：Lovart 官方 Logo、色板、字体、品牌 Kit 的集中管理
- [ ] **Screenshot 自动化**：Playwright 自动截取产品界面

## Related

- Lovart API: `Skills/30-clawx/clawx-openclaw-skills-lovart-skill/SKILL.md`
- Prompt 库（仅供参考，非自动化模板）: `1-4 Dev/lovart.sanity.studio/Sanity Blog/Awsome Prompt/`
- 封面池: `1-3 Content Gen/Lovart-Blog-Pipeline/Lovart-Blogs/Cover Url 随机调取.md`
- 图片 CDN 规范: `lovart-sanity-publish/Sanity-Blog-发布统合指南.md` §4.7
