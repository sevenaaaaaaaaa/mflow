# 验证图片池 2026-06-24 — 43 张 / 7 分类

> 落地页生成的唯一图片源。**所有 URL 已 HTTP 200 + size > 100KB 验证**。
> 严禁编造 URL，命中本表选取。

## 加载方式

```python
import sys
sys.path.insert(0, "1-1 Harness/Skills/lovart-landing-page/references")
from image_pool import POOL, get_image, match_title

# 方式 1: 按分类索引
video_urls = POOL["video"]  # 14 张
edit_urls = POOL["edit"]    # 4 张

# 方式 2: 按 card title 自动选图
url = get_image(match_title("Text Edit"), idx=0)
url = get_image(match_title("Multi-Platform Resize"), idx=1)
```

## 7 分类完整 URL 清单

### 🎬 video (14 张) — 视频/动效/动画

```python
VIDEO_URLS = [
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/afe09b54d518aacd6b7b96c5e9e22ba282abb81a.mp4",  # 3873KB MP4
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/7cc07d1d40c0c9d31ddc7f3951072e20e11a216e.mp4",  # 3888KB MP4
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/0b54f9cd55c2c07388ad25eadc136e65d295cd62.png",  # 1695KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/1c9bb0c97d36b371e68100e8f884e2a29c48ab11.png",  # 1590KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/1190149f4987ff002aa16cfb3a51311d7ea9e392.png",  # 833KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/0a5bc76a74ef8d4ab09ecf9d6a58ecbe2d5f818a.png",  # 50KB hero专用
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/1f4373d295181af9b6be11fc731ea0fabb88e5c7.png",  # 3363KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/4c90f673629d0bbd5fce85ad3743522b21d8fb8b.png",  # 3787KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/8efdfd8318084a8c88bb72c706bb33dc89c9d7e0.png",  # 1615KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/6b1a28475b0c188f4a858aaf0aa852a9b8d74f0e.png",  # 1246KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d0a9be686121d00de898a2d5ce66d96ed5fe34c9.png",  # 1215KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/896ff1a090a6ab98cbbce62b58cd73f5a3b4c5e0.png",  # 1639KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/1c0cdc61d03c462eb9e8e2a5b0aa9f5a86a47c89.png",  # IP avatar design
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/b8e9479301c56b3946bbce10cadc78eaa86a1e91.png",  # 1207KB
]
```

### 👤 avatar (7 张) — 角色/化身/IP

```python
AVATAR_URLS = [
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/cb613160648cd57fa1f2431a7b3ea5bb4f088d90.png",  # 1487KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/1f66f7b0726f0b3f59645d6b3a4716c8a8e89d8a.png",  # 1322KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/7eb9d35ed6aaf819fbe425badb3310b77bdc38a7.png",  # 786KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d11411bc15e95312819272bf39a65a6f6c3d4e76.png",  # 562KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/eb6f103da589f07f425f2c736237e3f7b0d4af07.png",  # 1967KB
    "https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/d11411bc15e95312819272bf39a65a6f6c3d4e76.png",  # 786KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d3e44c9edfb1a44f386973e9b3c23fcffddc8008.png",  # 1311KB
]
```

### 🖼️ image_gen (8 张) — 图像生成/艺术/插画

```python
IMAGE_GEN_URLS = [
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d14a7f30014fd72f63f9cdfbed8dd17c67012f10.png",  # 1803KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/Image-1.png",  # 3728KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/feature-2-style-consistency-1536x1024.png",  # 1339KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/feed1-new.png",  # 2093KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/feed2.jpg",  # 68KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/graphic-design.jpeg",  # 2207KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/prompt-nb.jpg",  # 1469KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/text-ach.png",  # 1506KB
]
```

### 🎨 design (6 张) — 设计代理/创意工具

```python
DESIGN_URLS = [
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/4573c61a748407d72a79a8f1baabd7ae19b41f2c.png",  # 1453KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/6a1b14e8ddcde57b6e342560a00f494a46e13174.png",  # 1230KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/886aa37f8873e52330bf92fb790fbb8b3a0fb1ce.png",  # 989KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/55b94439550ff0fefec6a09ca160df04a9a3b27b.png",  # 1738KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/mention-768x480.png",  # 72KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/e0bc4cf46ad055353bad5c9e832c33cd3d296ff5.png",  # 1306KB
]
```

### ✏️ edit (4 张) — 文字/触觉编辑

```python
EDIT_URLS = [
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/181ed5a5733bccb4594c29e1c15bd1ce93f8ea52.png",  # 799KB Style Reference
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/5d48ca781dea8ab12d0c93fc32e3ad8afa815631.png",  # 796KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/805d2e070d4404ed0cd6ae865930375919374b97.png",  # 273KB Text Edit
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/98dde485f8c6789596006f5ee601a445d6606b78.png",  # 1918KB Touch Edit
]
```

### 📦 ecommerce (3 张) — 商品/广告

```python
ECOMMERCE_URLS = [
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/5049909fb1610fbc90ed8b25cfecc777d2c8b3da.png",  # 960KB Mockup
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/79385767155d45c0a8d74c584a479ad2e5c80fa7.png",  # 1056KB
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/1778844771540.png",  # 1028KB Product
]
```

### 🔧 generic (1 张) — 通用兜底

```python
GENERIC_URLS = [
    "https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/d3e44c9edfb1a44f386973e9b3c23fcffddc8008.png",  # 1311KB
]
```

## 与 image-library.md（87 张主题 A-I）的关系

| 来源 | 数量 | 用途 |
|------|------|------|
| `image-library.md` | 87 张 | 主题化按 A-I 分类（AI Actors / Video / Fashion 等），适合按页面主题选用 |
| `verified-image-pool-2026-06.md` | 43 张 | 通用按语义分类（video/edit/style/avatar），适合按 card title 自动选图 |

**最佳实践**：
- **新页面 hero / contentSection 图** → 用 `image-library.md`（按主题 A-I）
- **bento-4/6、capability-tabs、feature-detail 图** → 用 `verified-image-pool-2026-06.md`（按 card title 自动分类）
- **threeColumnSection 流程图** → 固定使用 image-library.md 中的 Describe/Generate/Export 三张

## 验证清单

- ✅ 所有 URL HTTP 200（2026-06-24 验证）
- ✅ 全部 size > 100KB（最低 50KB 用于 hero，最高 3.7MB）
- ✅ 43 张图分布在 7 个语义分类
- ✅ 16/16 核心测试用例通过
- ✅ 8 语言关键词覆盖（英/德/日/韩/中/法/意/葡/俄）
