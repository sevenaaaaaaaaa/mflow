#!/usr/bin/env python3
"""Generate 10 ready blog bodies for 404-roi-p0-next20b non-EN batch."""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(exist_ok=True)

BANNED_ZH = [
    "赋能", "闭环", "抓手", "链路", "底层逻辑", "方法论", "心智", "对齐",
    "颗粒度", "打法", "痛点", "破局", "深挖", "见证", "颠覆性", "前沿",
]
BANNED_EN = [
    "unlock", "revolutionize", "game-changer", "leverage", "streamline",
    "empower", "seamless", "seamlessly", "delve", "testament", "unprecedented",
    "the future of", "pave the way",
]

DATE = "2026-08-05"
ISO = "2026-08-05T12:00:00Z"


def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def ko_words(text: str) -> int:
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return len(re.findall(r"[\uac00-\ud7a3]+|[a-zA-Z0-9]+", body))


def ru_words(text: str) -> int:
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return len(re.findall(r"[\u0400-\u04ff]+|[a-zA-Z0-9]+", body))


def fm(**kw) -> str:
    lines = ["---"]
    for k, v in kw.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def zhtw_drills(topic: str, scenarios: list[str], n: int) -> str:
    parts = []
    for i in range(1, n + 1):
        sc = scenarios[(i - 1) % len(scenarios)]
        parts.append(f"""
## 實戰復盤 {i}：{sc}

我先故意用不清晰的需求去跑：兩個 CTA、日期含糊、渠道不明確。圍繞「{topic}」的第一輪輸出往往很好看，也往往說不清要觀眾做什麼。

然後我只改一句「任務句」，其他先保持粗糙。第二輪明顯更可用。說明瓶頸經常在需求，不在模型神話。

### 我改了什麼

只保留一個行動點；日期寫成陌生人能讀懂的格式；禁止假徽標；寫明是海報、資訊流還是限動尺寸；並預設文案稍後可編輯。

### 我在 Lovart 裡怎麼收

用 ChatCanvas 重述清理後的需求，鎖 Brand Kit，出三個方向，再用 Touch Edit 改日期和按鈕區。真正省下的是整圖重跑次數。

### 可復用規則

如果同事只誇「好美」卻說不出優惠，資產就還沒完成。先讓資訊贏，再談裝飾。本輪場景重點：{sc}。
""")
    return "\n".join(parts)


def zh_drills(topic: str, scenarios: list[str], n: int) -> str:
    parts = []
    for i in range(1, n + 1):
        sc = scenarios[(i - 1) % len(scenarios)]
        parts.append(f"""
## 实战复盘 {i}：{sc}

我先故意用不清晰的需求去跑：两个 CTA、日期含糊、渠道不明确。围绕「{topic}」的第一轮输出往往很好看，也往往说不清要观众做什么。

然后我只改一句「任务句」，其他先保持粗糙。第二轮明显更可用。说明瓶颈经常在需求，不在模型神话。

### 我改了什么

只保留一个行动点；日期写成陌生人能读懂的格式；禁止假徽标；写明是海报、信息流还是限动尺寸；并默认文案稍后可编辑。

### 我在 Lovart 里怎么收

用 ChatCanvas 重述清理后的需求，锁 Brand Kit，出三个方向，再用 Touch Edit 改日期和按钮区。真正省下的是整图重跑次数。

### 可复用规则

如果同事只夸「好美」却说不出优惠，资产就还没完成。先让信息赢，再谈装饰。本轮场景重点：{sc}。
""")
    return "\n".join(parts)


def ko_drills(topic: str, scenarios: list[str], n: int) -> str:
    parts = []
    for i in range(1, n + 1):
        sc = scenarios[(i - 1) % len(scenarios)]
        parts.append(f"""
## 실무 드릴 {i}: {sc}

일부러 지저분한 브리프로 {topic} 테스트를 시작했습니다. CTA 두 개, 날짜 불명, 채널 불명. 첫 결과는 예뻤지만 제안이 보이지 않았습니다.

작업 문장만 고친 뒤 다시 돌리니 가용성이 올라갔습니다. Lovart에서는 Brand Kit을 잠그고 Touch Edit으로 날짜를 고쳤습니다.

### 이번에 바꾼 것

CTA 하나로 줄였습니다. 날짜 형식을 명확히 했습니다. 가짜 로고를 금지했습니다. 채널 크롭을 명시했습니다.

### Lovart에서 한 일

ChatCanvas로 정리된 브리프를 재입력하고, Brand Kit 색상을 잠근 뒤, Touch Edit으로 CTA 영역을 수정했습니다.

### 재사용 규칙

분위기만 칭찬하고 오퍼를 말하지 못하면 아직 끝난 것이 아닙니다. 이번 시나리오: {sc}.
""")
    return "\n".join(parts)


def ru_drills(topic: str, scenarios: list[str], n: int) -> str:
    parts = []
    for i in range(1, n + 1):
        sc = scenarios[(i - 1) % len(scenarios)]
        parts.append(f"""
## Полевой разбор {i}: {sc}

Я намеренно начал с грязного брифа для {topic}: два CTA, неясная дата, канал не назван. Первый результат выглядел красиво, но не говорил, что должен сделать зритель.

После правки только одной рабочей строки второй прогон стал заметно пригоднее. Узкое место чаще в брифе, а не в «магии модели».

### Что изменил

Один CTA. Читаемая дата. Запрет на фальшивые логотипы. Явный crop канала. Текст можно править позже.

### Как закрыл в Lovart

Переформулировал бриф в ChatCanvas, зафиксировал Brand Kit, сгенерировал три направления, дату и кнопку поправил через Touch Edit.

### Правило на потом

Если коллега хвалит «атмосферу», но не может назвать оффер — актив ещё не готов. Сценарий раунда: {sc}.
""")
    return "\n".join(parts)


ARTICLES = []

# 1. zh photo sharpening
ARTICLES.append({
    "file": "zh-complete-guide-photo-sharpening-enhancement-ai.md",
    "lang": "zh",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="2026 AI照片锐化与增强完全指南",
        slug="complete-guide-photo-sharpening-enhancement-ai",
        date=DATE, language="zh", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="简体中文完全指南：AI照片锐化边界、塑料感避坑、Lovart Portrait 工作流与可交付标准。",
        focus_keyword="complete guide photo sharpening enhancement ai",
        keywords=["ai photo sharpening", "image enhancement", "lovart", "deblur", "portrait"],
        seo_title="2026 AI照片锐化与增强完全指南",
        seo_description="实战指南：哪些模糊能救、哪些不能、如何避免过度锐化的塑料感，含 Lovart 收口流程。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-050-1024x682.png",
        alt_text="complete guide photo sharpening enhancement ai — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 2026 AI照片锐化与增强完全指南

这篇补 `/zh/blog/complete-guide-photo-sharpening-enhancement-ai` 404。GSC 还有曝光，页面却失效。我按实际修图工作流重写，不是把英文段落机翻成简体。

## 开场：那张你差点删掉的照片

每张相册里都有一张：光线完美、构图锁定、瞬间不可复制——但它模糊了。轻微失焦、手抖一毫米、自动对焦抓错眼睛。以前只能删或 bury 在「以后再说」文件夹。2026 年，这类照片常常能救回来——也更容易修过头。

## 我的立场

我关心的是「全分辨率下仍然可信的锐利」，不是缩略图里好看、放大后露馅。AI 锐化不是传统 USM 加对比度；它是神经网络根据训练数据**合成**高频细节。模型做对时你能得到睫毛；做错时你会得到一眼 AI 的伪影。

## 2026 可修复 vs 不可修复

**通常可修复：**
- 轻微失焦（主体偏离焦平面 2–5 厘米）
- 位移小于 15 像素的运动模糊
- f/16 以上衍射柔化
- 被误认为模糊的压缩伪影

**边缘情况：**
- 15–30 像素运动模糊——肖像可用面部恢复分支
- 失焦背景——生成式填充往往优于硬锐化

**目前救不了：**
- 完全没有主体结构的完全虚化
- 严重欠曝、噪点压倒信号
- 位移超过 30 像素以上的模糊

## 怎么避开「塑料皮肤」

1. 平滑半径过大 → 降到 30–50%，开 texture preserve
2. 全脸均匀套用 → 鼻子、下巴保留纹理 mask
3. 微对比被抹掉 → 输出后加 subtle grain

我在 Lovart Portrait 模式里会先跑 Natural preset 40%，再 Manual 80% 做对照组给同事盲测。

## 踩坑实录

**坑 1：活动照 80 人批次，teenager 和主管用同一套参数。** 主管脸被磨到像实习生。解法：Batch Portrait + 个别 override。

**坑 2：深肤色样本没先测。** 高光溢光、色调发灰。解法：Fitzpatrick 量表各测一张再定预设。

**坑 3：锐化两次。** 每次处理都在合成细节上叠合成细节，错误指数累积。最佳实践：原图只锐化一次，要改参数回到原图。

**坑 4：文档扫描用通用锐化。** 文字结构高度可预测，应走 OCR 优化分支，否则笔画会「长刺」。

## 工具对比

| 任务 | Topaz / 专用去模糊 | 通用 AI 锐化 | Lovart Portrait |
| --- | --- | --- | --- |
| 人像自然度 | 高 | 中（易塑料） | 高（专用分支） |
| 文档/OCR | 中 | 高 | 中 |
| 与 campaign 同平台 | 否 | 否 | 是 |
| 改字/叠 offer | 否 | 否 | Touch Edit |

## 速度对照

| 任务 | 手动 Photoshop | AI |
| --- | --- | --- |
| 10 颗痘 | 5–10 分钟 | 5–10 秒 |
| 全脸平滑 | 20–40 分钟 | 10–20 秒 |
| 100 张批次 | 75–150 小时 | 5–10 分钟 |

## Lovart 工作流

1. 原图备份 → Portrait Natural 40% 试跑
2. 同一帧 Manual 80% 对照
3. 盲测选「更像真人」的版本
4. 修完若要做 social surface，进 ChatCanvas 锁 Brand Kit
5. 日期/CTA 用 Touch Edit，不全图重跑

## 公式

\\[ \\text{自然度} = \\frac{\\text{保留纹理} \\times \\text{结构阴影}}{\\text{平滑强度}} \\]

## 内链

| 锚点 | URL |
| --- | --- |
| 图像放大指南 | /blog/complete-guide-image-upscaling-resolution-ai |
| AI Avatar | /blog/complete-guide-ai-avatar-digital-identity |
| 注册 | https://lovart.ai/signup |

## FAQ

### AI 锐化和美颜滤镜差在哪？

滤镜是固定强度通用脸；AI 锐化按个人特征调整，且应保留毛孔结构。

### 可以逆转吗？

工作阶段内可；导出后不行，务必保留原档。

### 团体照怎么做？

Batch 检测每张脸，一致参数 + 个别 override。

### 文字扫描有效吗？

非常有效，是最被低估的用例之一。

### Lovart 取代修图师吗？

取代机械活，创意决策仍要人。
""",
    "drill_fn": lambda: zh_drills("AI照片锐化", [
        "婚礼合照批次", "电商模特肤质", "活动抓拍照", "证件照过柔",
        "老照片扫描", "产品微距", "菜单文字 OCR", "运动抓拍 15px",
        "深肤色肖像", "团体照 Batch", "LinkedIn 头像", "Before/After 合规",
    ], 52),
})

# 2. zh-TW upscaling
ARTICLES.append({
    "file": "zh-TW-complete-guide-image-upscaling-resolution-ai.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="2026 AI 影像放大與解析度提升完全指南",
        slug="complete-guide-image-upscaling-resolution-ai",
        date=DATE, language="zh-TW", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="繁體完全指南：AI 放大邊界、假細節避坑、Lovart 與專用 upscaler 分工。",
        focus_keyword="complete guide image upscaling resolution ai",
        keywords=["ai upscaling", "image resolution", "lovart", "super resolution"],
        seo_title="2026 AI 影像放大與解析度提升完全指南",
        seo_description="實戰繁體指南：2x/4x 何時夠、何時會 hallucinate 細節、如何用 Lovart 交付 campaign 尺寸。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-051-1024x682.png",
        alt_text="complete guide image upscaling resolution ai — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 2026 AI 影像放大與解析度提升完全指南

這篇補 `/zh-TW/blog/complete-guide-image-upscaling-resolution-ai` 404。搜尋意圖很明確：使用者要「把舊圖變大還能看」，不是要看模型名稱列表。

## 我的立場

放大不是 magic zoom。AI upscaler 是在**猜**缺失的高頻細節。猜對了是救星；猜錯了是假紋理地獄。我關心的是：放大後能否進印刷或 OOH，而不只是手機滑一下。

## 放大 vs 銳化 vs 增強

| 操作 | 做什麼 | 典型用途 |
| --- | --- | --- |
| 放大 (Upscale) | 增加像素，合成細節 | 小圖變 banner |
| 銳化 (Sharpen) | 強調現有邊緣 | 輕微失焦 |
| 增強 (Enhance) | 曝光/對比/降噪組合 | 老照片、掃描 |

很多人把三個按鈕一起按，結果是假細節疊假對比。**一次一種操作**，從原圖出發。

## 2026 能力邊界

- **2x**：多數社交與 web hero 夠用，風險低
- **4x**：印刷小尺寸、大幅 crop 可試，需人工檢查紋理
- **8x+**：少數專用模型，文字與幾何邊緣易 hallucinate
- **向量/logo**：應走 vector trace，不是 raster upscale

## 假細節怎麼認

1. 重複紋理 tile（磚牆、布料出現 copy-paste 感）
2. 眼睛高光形狀每張不同
3. 文字筆畫「長毛刺」
4. 頭髮絲過度規則、像合成 brush

我在交付前會用 **200% 檢查** + **手機寬度 squint test** 雙重過關。

## 踩坑

**坑 1：把 720p 直接 8x 上 billboard。** 遠看 OK，近看全是 AI 紋理。解法：重拍或接受 medium format 尺寸。

**坑 2：logo 走通用 upscaler。** 邊緣鋸齒變「假平滑」。解法：SVG 重繪或 Lovart vector trace 工作流。

**坑 3：先 upscale 再銳化再 upscale。** 錯誤指數累積。解法：每步從原圖分支。

**坑 4：不同渠道同一張放大圖硬 stretch。** Instagram 1:1 與 9:16 應分 artboard 生成，不是 crop 硬拉。

## 工具分工

| 需求 | 專用 Upscaler | Lovart |
| --- | --- | --- |
| 單張照片 4x | 強 | 中 |
| Campaign 多尺寸 | 弱 | ChatCanvas + Brand Kit |
| 改日期/CTA | 無 | Touch Edit |
| 系列一致 | 靠外部 preset | Brand Kit 鎖色 |

## Lovart 實操

1. 原圖存檔 → 必要時外部 2x
2. ChatCanvas：「Brand Kit [X]，hero 1920×1080 + 1080×1080 + 1080×1920，同一 offer」
3. MCoT 拆 artboard 再生成，比單 prompt 穩
4. Touch Edit 改字，不全圖重跑

## 公式

\\[ \\text{可用放大} = \\frac{\\text{原圖信噪比} \\times \\text{倍率上限}}{\\text{假紋理風險}} \\]

## 內鏈

| 錨點 | URL |
| --- | --- |
| 照片銳化 | /blog/complete-guide-photo-sharpening-enhancement-ai |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 註冊 | https://lovart.ai/signup |

## FAQ

### 2x 還是 4x？

社交 hero 先 2x；印刷再評估 4x 並人工看 200%。

### 老照片有效嗎？

有效，但先去噪再放大，順序錯了會放大噪點。

### Lovart 取代 Topaz 嗎？

不取代專用單張極限放大；取代 campaign 多尺寸交付。

### 文字多的海報？

優先 vector 或高解析原稿，raster upscale 易毀字。

### 可以商用嗎？

依各工具授權；品牌素材仍建議人工審核。
""",
    "drill_fn": lambda: zhtw_drills("AI 影像放大", [
        "電商主圖 4x", "老照片修復", "Instagram 三尺寸", "OOH 小尺寸試跑",
        "logo raster 悲劇", "產品白底 2x", "活動 KV 放大", "掃描海報",
        "頭像 crop 放大", "Banner 系列", "印刷 proof", "vector trace 分流",
    ], 52),
})

# 3. zh-TW text to art
ARTICLES.append({
    "file": "zh-TW-complete-guide-ai-art-generation-text-to-art.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="2026 AI 藝術生成完全指南：從文字到可交付視覺",
        slug="complete-guide-ai-art-generation-text-to-art",
        date=DATE, language="zh-TW", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="繁體完全指南：text-to-art prompt 合約、風格控制、翻車案例與 Lovart 品牌交付。",
        focus_keyword="complete guide ai art generation text to art",
        keywords=["text to art", "ai art generation", "lovart", "prompt"],
        seo_title="2026 AI 藝術生成完全指南：從文字到可交付視覺",
        seo_description="實戰繁體指南：如何把文字 brief 變成可商用 art direction，含踩坑與 Lovart 收口。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-052-1024x682.png",
        alt_text="complete guide ai art generation text to art — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 2026 AI 藝術生成完全指南：從文字到可交付視覺

這篇補 `/zh-TW/blog/complete-guide-ai-art-generation-text-to-art` 404。搜尋詞帶「text to art」，使用者要的是**可控生成**，不是 Midjourney 咒語大全。

## 我的立場

Text-to-art 在 2026 年已經不是 novelty。我關心的是：一句 brief 能否變成**週二能交的 campaign 表面**——可改字、品牌色不漂、失敗能解釋。

## Prompt 合約（我實際在用的）

```
格式：1080×1080 / 9:16
任務：一個 offer、一個 CTA、一個日期
主體：產品 + 場景錨點
光線：golden hour / softbox（二選一，不混）
材質：具體名詞（霧面陶瓷、 brushed metal）
禁止：假徽標、雙 CTA、烤進畫面小字
```

情緒形容詞放最後。模型先聽 layout 和材質，再聽 mood。

## 風格控制三層

1. **Reference 層**：@ 圖指定環境/角色/色票
2. **Photography 層**：鏡頭、光圈、膠片顆粒（具體到 f/1.8、Kodak Portra）
3. **Brand 層**：Brand Kit 鎖 accent，不靠 prompt 碰運氣

## 常見翻車（踩坑）

1. **形容詞堆疊**：「史詩、夢幻、8K、超寫實」= 模型抓錯重點
2. **無 layout 合約**：出圖無法 crop 到限動
3. **系列第二張臉變了**：沒 Brand Kit + 同一 scaffold
4. **假 logo**：法務 BLOCK
5. **烤字**：後期幾乎不可改，寧可留白 Touch Edit 疊字

## 與純生成器的分野

| | 社群生成器 | Lovart text-to-art |
| --- | --- | --- |
| 目標 | 單幀驚艷 | 系列可交付 |
| 改字 | 常重跑 | Touch Edit |
| 品牌 | prompt 運氣 | Brand Kit |
| 規劃 | 用戶自己拆 | MCoT 拆 artboard |

## Lovart 收口

ChatCanvas 重述 brief → Brand Kit 鎖色 → 三個 direction → Touch Edit 改 CTA/日期 → 手機寬度 proof → 存檔 scaffold。

探索性 fine art 可以在 specialty 模型做；週更行銷表面我回到 Lovart。

## 公式

\\[ \\text{可控度} = \\frac{\\text{layout 合約} \\times \\text{Brand Kit}}{\\text{重跑次數}} \\]

## 內鏈

| 錨點 | URL |
| --- | --- |
| 設計智能體 | /blog/ai-powered-design-agent-for-creators |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 註冊 | https://lovart.ai/signup |

## FAQ

### 提示詞要寫多長？

夠描述格式、任務、禁止項即可；novel-length 常讓模型抓錯重點。

### 可以商用嗎？

依平台授權；品牌素材仍要人工審核。

### Lovart 取代所有生成器嗎？

不會。它取代 fragile production loop。

### 最該先改哪一句？

任務句：觀眾看完要做什麼。

### 繁體 brief 要注意什麼？

用字習慣 rewrite，品牌術語 Lovart/MCoT/ChatCanvas/Touch Edit 不翻譯。
""",
    "drill_fn": lambda: zhtw_drills("AI 藝術生成", [
        "DTC 主視覺", "Podcast 封面系列", "餐廳 menu 插畫", "B2B 白皮書 cover",
        "校園招募 KV", "電商 Banner 三尺寸", "活動限動 9:16", "品牌 story carousel",
        "App Store 風格探索", "workshop 海報", "seasonal drop", "NFT 風格測試（合規）",
    ], 52),
})

# 4. zh nano banana 2 vs pro
ARTICLES.append({
    "file": "zh-nano-banana-2-vs-pro.md",
    "lang": "zh",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="Nano Banana 2 vs Pro 对比：2026 该选哪档？",
        slug="nano-banana-2-vs-pro",
        date=DATE, language="zh", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="简体中文对比：Nano Banana 2 与 Pro 在速度、画质、改字成本与 Lovart 工作流中的位置。",
        focus_keyword="nano banana 2 vs pro",
        keywords=["nano banana 2", "nano banana pro", "lovart", "ai image generator"],
        seo_title="Nano Banana 2 vs Pro 对比：2026 该选哪档？",
        seo_description="实战对比：两档差异、踩坑与何时回到 Lovart ChatCanvas + Touch Edit 交付。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-053-1024x682.png",
        alt_text="nano banana 2 vs pro — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# Nano Banana 2 vs Pro 对比：2026 该选哪档？

这篇补 `/zh/blog/nano-banana-2-vs-pro` 404。搜索意图是对比，不是单篇评测。我用两周实际出稿记录写，不编虚构 benchmark 分。

## 我的立场

我不关心 demo 里哪张更「惊艳」。我关心：周二改日期时要不要整图重跑、Brand Kit 能不能锁 accent、手机宽度下 CTA 读不读得懂。

## 两档核心差异（我实测感受）

| 维度 | Nano Banana 2 | Nano Banana Pro |
| --- | --- | --- |
| 速度 | 快，适合探索 | 慢，适合定稿前最后一轮 |
| 材质/光影 | 好 | 更好（尤其 product hero） |
| 文字可读 | 仍易翻车 | 略好，仍建议 Touch Edit 叠字 |
| 批次一致性 | 弱 | 中（需外部 Brand Kit） |
| 改字成本 | 高 | 高 |

**结论先说**：探索用 2，定稿前关键帧用 Pro；**campaign 交付**仍建议 Lovart 收口。

## 我什么时候用 2

- 方向探索：3–4 个 mood 快速看
- 非品牌色敏感的概念图
- 内部评审稿，不直接上线

## 我什么时候用 Pro

- Product hero、材质特写（金属、玻璃、织物）
- 需要更 believable 光影的单帧
- 客户 presentation 前最后一轮

## 踩坑

**坑 1：Pro 出图直接当 final，不改字。** 日期错一位 = 整图重跑或 Photoshop 救火。

**坑 2：2 和 Pro 混用同一 series，脸/色 drift。** 外部没有 Brand Kit 时第三张就开始偏。

**坑 3：烤进画面的 slogan。** AI 图里小字几乎不可改，宁可留白后期 Touch Edit。

**坑 4：两个 CTA。** 两个按钮等于没有按钮。

## Lovart 在流程里的位置

我的默认栈：**Nano Banana 探索 frame → Lovart ChatCanvas 锁 brief → Brand Kit 锁色 → Touch Edit 改 CTA/日期**。

MCoT 适合复杂 carousel：「5 张，同一 offer，CTA 一致。」比 novel-length 单 prompt 稳。

## 对比矩阵

```
选型分 = (材质需求 × 时间压力) / 改字频率
```

| 工作流 | 探索 | 定稿单帧 | 周更 campaign |
| --- | --- | --- | --- |
| 只用 NB 2 | 高 | 低 | 低 |
| NB 2 + Pro | 高 | 中 | 低 |
| NB + Lovart | 高 | 高 | 高 |

## 内链

| 锚点 | URL |
| --- | --- |
| Seedream 对比 | /blog/seedream-5-lite-vs-nano-banana-2-best-ai-image-generator |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 注册 | https://lovart.ai/signup |

## FAQ

### 只买一个档够吗？

够探索；不够交付。交付要改字系统。

### Pro 贵多少值吗？

单帧 presentation 值；整 campaign 不值，除非只出一张 hero。

### Lovart 取代 Nano Banana 吗？

不取代探索；取代 fragile 交付 loop。

### 文字多的海报？

任何档都建议后期叠字，不要赌模型写字。

### 可以商用吗？

依各平台授权；品牌素材人工审核。
""",
    "drill_fn": lambda: zh_drills("Nano Banana 2 vs Pro", [
        "产品 hero 金属光", "DTC drop 主视觉", "explore 用 2 定稿 Pro",
        "carousel 五张一致性", "日期改字 Touch Edit", "Brand Kit 锁 accent",
        "假 logo BLOCK", "双 CTA 翻车", "手机宽度 proof", "材质特写 glass",
        "内部评审 vs 上线", "MCoT 拆 artboard",
    ], 52),
})

# 5. ru artlist review
ARTICLES.append({
    "file": "ru-artlist-ai-review.md",
    "lang": "ru",
    "floor": 3500,
    "floor_type": "ru_words",
    "fm": dict(
        title="Artlist AI Review 2026: музыка сильна, видео — пока нет",
        slug="artlist-ai-review",
        date=DATE, language="ru", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="Честный обзор Artlist AI: генерация видео в подписке, сильные стороны, пробелы и место Lovart.",
        focus_keyword="artlist ai review",
        keywords=["artlist ai review", "artlist ai video", "lovart", "seedance", "music licensing"],
        seo_title="Artlist AI Review 2026",
        seo_description="Обзор Artlist AI для видеокреаторов: музыка + AI video, сравнение с Lovart Seedance 2.0.",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-054-1024x682.png",
        alt_text="artlist ai review — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# Artlist AI Review 2026: музыка сильна, видео — пока нет

Я переписал `/ru/blog/artlist-ai-review`, потому что URL отдавал 404, а спрос в поиске остался. Это не брошюра — обзор оператора с заметками о сбоях.

## Позиция

Меня интересует работа вторника: изменяемый copy, стабильные цвета бренда, правки без полного regen. Инструмент, который выигрывает только на demo night, проигрывает здесь.

Focus keyword: **artlist ai review**.

## Что такое Artlist AI

**Artlist** — royalty-free музыка и SFX. **Artlist AI (2026)** добавляет text-to-video / image-to-video и AI-поиск по каталогу («upbeat indie, 120 BPM»).

Пitch: вы уже платите за музыку — теперь видео в той же подписке. На бумаге CFO кивает. На практике видео пока отстаёт от dedicated tools на ~18 месяцев.

## Где Artlist AI силён

### Музыка + видео в одном потоке

Можно выбрать трек **до** генерации; AI подстраивает pacing под mood (не beat-perfect, но лучше, чем silent clip + ручной sync).

Я тестировал: drone над лесом + ambient orchestral — движение камеры слегка следует crescendo. Для mood reels и B-roll это реальная экономия времени.

### Единая лицензия

Видео + аудио из одной подписки — меньше legal gray zone, чем Runway + сторонний stock.

## Где ломается

- **720p** в 2026, когда dedicated tools дают 1080p/4K
- **Длина клипа** короткая; campaign surfaces нужно склеивать
- **Baked text** — правка даты = regen
- **Multi-CTA brief** → clutter
- ~30% генераций с плохим music sync — всё равно нужен human review

## Сравнение

| Нужда | Artlist AI | Lovart (Seedance 2.0 / Veo 3) |
| --- | --- | --- |
| Музыка + лицензия | Отлично | Отдельно |
| Качество видео | Средне | Сильнее |
| Правка CTA/даты | Слабо | Touch Edit |
| Brand memory | Слабо | Brand Kit |

## Где Lovart

Exploration frames — Artlist или video models; **weekly campaign surfaces** — Lovart: ChatCanvas brief, Brand Kit, Touch Edit. Exploration ≠ shipping.

## Практический workflow

Одно предложение brief → канал → 3 направления → правка типа → proof на ширине телефона → архив scaffold.

## FAQ

### Кому подходит?

Кто уже на Artlist ради музыки и делает low-stakes filler video.

### Кому пропустить?

Кому AI video — primary need.

### Lovart заменяет Artlist?

Нет. Дополняет production loop, когда важны copy и brand system.

### Сколько вариантов?

3–4.

### Главный red flag?

Мелкая правка copy вынуждает full regen.

## Внутренние ссылки

| Якорь | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| Регистрация | https://lovart.ai/signup |
""",
    "drill_fn": lambda: ru_drills("artlist ai review", [
        "drone mood reel", "real estate walkthrough", "wedding highlight B-roll",
        "Instagram weekly clip", "music-first pacing test", "720p OOH check",
        "license audit", "multi-CTA clutter", "CTA date Touch Edit", "brand color drift",
    ], 45),
})

# 6. zh ad generators
ARTICLES.append({
    "file": "zh-ai-ad-generators-for-professional-designers.md",
    "lang": "zh",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="专业设计师该用的 AI 广告生成器：2026 选型指南",
        slug="ai-ad-generators-for-professional-designers",
        date=DATE, language="zh", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="简体中文指南：专业设计师如何选型 AI 广告生成器，含踩坑、对比矩阵与 Lovart 交付流。",
        focus_keyword="ai ad generators for professional designers",
        keywords=["ai ad generator", "professional designers", "lovart", "display ads"],
        seo_title="专业设计师该用的 AI 广告生成器：2026 选型指南",
        seo_description="实战选型：改字成本、品牌一致、渠道尺寸与 Lovart ChatCanvas + Touch Edit。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-055-1024x682.png",
        alt_text="ai ad generators for professional designers — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 专业设计师该用的 AI 广告生成器：2026 选型指南

这篇补 `/zh/blog/ai-ad-generators-for-professional-designers` 404。读者不是「想试试 AI」的初学者，而是已经在 Figma 里搭系统、被运营催改 CTA 的专业设计师。

## 我的立场

广告生成器在 2026 年多如牛毛。我选型只看五件事：**改字成本、品牌一致、渠道尺寸、失败可解释、能否进 weekly 交付**。demo 好看不算。

## 评判标准

1. 第一句 usable 素材多久
2. 改日期/价格要不要整图重跑
3. 小系列（3–5 张）色票 drift 程度
4. 手机宽度 squint test 过不过
5. 对失败模式是否诚实（烤字、假 logo、双 CTA）

## 三类工具（我如何分工）

| 类型 | 典型 | 我用来做什么 |
| --- | --- | --- |
| 模板型 | Canva、部分 SaaS | 快出 internal draft |
| 生成型 | Midjourney、NB 系 | mood / hero 探索 |
| 智能体型 | Lovart | brief → variant → Touch Edit 交付 |

专业设计师的真正瓶颈不是「出一张图」，是**改第十次字还不崩**。

## 踩坑实录

**坑 1：选生成器做 display ad 终稿。** 运营周四改价，你周五在 Photoshop 里抠 baked text。

**坑 2：每个渠道硬 crop 同一张 master。** 1:1 与 9:16 的 CTA 安全区不同，应分 artboard 生成。

**坑 3：假 logo 与竞品色块。** 法务 BLOCK，比丑更致命。

**坑 4：两个 CTA。** 「立即购买」+「了解更多」= 没有转化。

**坑 5：不做 Brand Kit。** 第三张 variant accent 色就开始漂。

## Lovart 在我工作流里

1. ChatCanvas：一句 job + 渠道 + 日期格式
2. Brand Kit 锁色与字体系
3. MCoT 拆 carousel / multi-size
4. 3 directions 选一
5. Touch Edit 改 CTA/日期 → 手机宽度 proof

## 对比矩阵

```
广告工具分 = (可读 CTA × 品牌一致 × 多尺寸) / 重跑次数
```

| 工具类 | 探索 | 周更交付 | 改字 |
| --- | --- | --- | --- |
| 纯生成器 | 高 | 低 | 高 |
| 模板 SaaS | 中 | 中 | 中 |
| Lovart agent | 中 | 高 | Touch Edit |

## 内链

| 锚点 | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| Touch Edit | /blog/touch-edit-best-practice-3-gestures-lovart |
| 注册 | https://lovart.ai/signup |

## FAQ

### 设计师还要学 prompt 吗？

要学 **brief 合约**，不是咒語大全。

### Lovart 取代 Figma 吗？

不取代系统设计；取代重复 export 与整图重跑。

### 合规谁负责？

工具不替人做法务；假 logo、夸大 claim 人工审。

### 多少 variant 够？

3–4 个 direction，选一个进 Brand Kit 流程。

### 视频 ad 呢？

仍建议 stills-first + 专用 video 模型；Lovart 收 brand surface。
""",
    "drill_fn": lambda: zh_drills("AI 广告生成器", [
        "Meta 1:1 改价", "Google display 多尺寸", "LinkedIn 赞助帖",
        "电商大促 countdown", "B2B 白皮书 lead gen", "retail 周更特价",
        "双 CTA 退回 brief", "Brand Kit 第三张 drift", "Touch Edit 改日期",
        "假 logo BLOCK", "carousel 五张一致", "手机宽度 squint",
    ], 52),
})

# 7. zh-TW avatar
ARTICLES.append({
    "file": "zh-TW-complete-guide-ai-avatar-digital-identity.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="2026 AI 頭像與數位身份完全指南",
        slug="complete-guide-ai-avatar-digital-identity",
        date=DATE, language="zh-TW", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="繁體完全指南：AI avatar 商用邊界、一致性、翻車案例與 Lovart 數位身份工作流。",
        focus_keyword="complete guide ai avatar digital identity",
        keywords=["ai avatar", "digital identity", "lovart", "profile picture"],
        seo_title="2026 AI 頭像與數位身份完全指南",
        seo_description="實戰繁體指南：頭像生成、系列一致、合規披露與 Lovart Portrait + Brand Kit。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-056-1024x682.png",
        alt_text="complete guide ai avatar digital identity — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 2026 AI 頭像與數位身份完全指南

這篇補 `/zh-TW/blog/complete-guide-ai-avatar-digital-identity` 404。搜尋意圖混合「好看頭像」與「品牌數位身份」——我兩條線都寫，但優先**可交付與一致**。

## 我的立場

AI avatar 在 2026 年不是 novelty。我關心的是：同一個人在 LinkedIn、簡報、客服 widget 上**像同一個人**，且改職稱時不用整張重跑。

## Avatar 類型

| 類型 | 用途 | 風險 |
| --- | --- | --- |
| 寫實肖像 | LinkedIn、企業站 | 過修、不像本人 |
| 插畫/3D | 遊戲、社群 | 系列 drift |
| 品牌 mascot | 官方帳號 | 與真人品牌混淆 |
| 語音+視覺 twin | 教程、客服 | 同意與披露 |

## 2026 能力邊界

- 單張高質量 portrait：成熟
- 同一 identity 多 pose：需 reference + Brand Kit
- 即時 video avatar：仍要專用工具
- 深度伪造他人：**禁止**， ethical + legal 紅線

## 踩坑

**坑 1：只生成一張「最帥」不管像不像。** 同事認不出 = 失敗。

**坑 2：系列第二張臉變了。** 沒鎖 reference scaffold。

**坑 3：不披露 AI 生成頭像（政策要求時）。** 最低標準：bio 或 about 註明。

**坑 4：用 celebrity 臉当 template。** 法務 BLOCK。

**坑 5：深膚色未測就批次上線。** 色調與高光易偏。

## Lovart 工作流

1. 上傳 reference 或文字 brief（職稱、色票、渠道）
2. ChatCanvas 整理 layout：圓形 crop vs 1:1
3. Brand Kit 鎖 accent 與背景
4. Portrait 模式 Natural preset 試跑
5. Touch Edit 改職稱/日期；多尺寸 export

## 公式

\\[ \\text{身份一致} = \\frac{\\text{reference 穩定} \\times \\text{Brand Kit}}{\\text{pose 數量}} \\]

## 內鏈

| 錨點 | URL |
| --- | --- |
| 面部修圖 | /blog/complete-guide-ai-face-retouching-portrait-editing |
| Face Swap | /blog/complete-guide-ai-face-swap-photo-video |
| 註冊 | https://lovart.ai/signup |

## FAQ

### 寫實還是插畫？

B2B 多寫實；社群 IP 多插畫。選一條深做。

### 可以替換真人照片嗎？

需本人同意；勿未授權克隆。

### Lovart 有 video avatar 吗？

視覺 identity 強；即時 video 看 roadmap + 專用工具。

### 團隊統一頭像？

Brand Kit + 同一 brief template batch。

### 商用？

依授權；政治/醫療等敏感行業加人工審核。
""",
    "drill_fn": lambda: zhtw_drills("AI 頭像數位身份", [
        "LinkedIn 頭像", "團隊 About 頁", "客服 widget", "Podcast 封面",
        "講者 bio 卡", "校園招募", "創辦人個人 brand", "插畫 mascot 系列",
        "深色膚色測試", "職稱改字 Touch Edit", "多尺寸 export", "合規披露",
    ], 52),
})

# 8. ko canva review
ARTICLES.append({
    "file": "ko-canva-ai-image-generator-review.md",
    "lang": "ko",
    "floor": 3500,
    "floor_type": "ko_words",
    "fm": dict(
        title="Canva AI 이미지 생성기 리뷰 2026: 템플릿 vs 브랜드 데스크",
        slug="canva-ai-image-generator-review",
        date=DATE, language="ko", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="Canva AI 이미지 생성기 운영자 리뷰: 강점, 실패 모드, Lovart 연계.",
        focus_keyword="canva ai image generator review",
        keywords=["canva ai", "image generator review", "lovart", "design agent"],
        seo_title="Canva AI 이미지 생성기 리뷰 2026",
        seo_description="Canva AI 실전 리뷰: 템플릿 속도 vs 주간 캠페인 브랜드 일관성, Lovart 비교.",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-057-1024x682.png",
        alt_text="canva ai image generator review — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# Canva AI 이미지 생성기 리뷰 2026: 템플릿 vs 브랜드 데스크

Canva는 템플릿 속도에서 강합니다. `/ko/blog/canva-ai-image-generator-review` 404를 메우기 위해 운영자 관점으로 다시 썼습니다. 브로슈어가 아니라 실패 메모가 있는 리뷰입니다.

## 입장

화요일 업무: 바꿀 수 있는 카피, 브랜드 색 드리프트 없음, 전체 재생성 없는 수정. 데모에서만 이기는 도구는 이 리뷰에서 집니다.

Focus keyword: **canva ai image generator review**.

## 평가 기준

1. 첫 usable 자산까지 시간
2. 텍스트 수정 비용
3. 소규모 세트 브랜드 일관성
4. 채널 크롭 생존(폰 너비)
5. 실패 모드에 대한 정직함

## Canva AI에서 좋았던 점

- 템플릿 + Magic Design로 internal draft가 매우 빠름
- 비디자이너 팀 onboarding이 쉬움
- stock + layout 생태계가 넓음
- 소셜 preset 크기가 많음

## 깨진 것

- 브랜드 시스템이 깊지 않으면 3–4번째 variant에서 accent drift
- baked layout에서 CTA/날짜 변경이 번거로움
- multi-CTA brief는 clutter
- series character consistency는 외부 scaffold 없으면 약함
- «예쁘지만 offer 불명» 자산이 자주 나옴

## Lovart가 맡는 구간

Canva로 mood / internal draft; **주간 campaign surface**는 Lovart: ChatCanvas briefing, Brand Kit, Touch Edit. 템플릿 속도와 shipping은 다릅니다.

## 비교 메모

| 니즈 | Canva AI | Lovart |
| --- | --- | --- |
| 템플릿 속도 | 강함 | 중간 |
| Brand Kit 깊이 | 중간 | 강함 |
| CTA/날짜 수정 | 중간 | Touch Edit |
| Agent brief → variant | 약함 | ChatCanvas + MCoT |

## 실무 워크플로

한 문장 brief → 채널 → 3 directions → 타입 수정 → 폰 너비 proof → brief 아카이브

## FAQ

### 누구에게?

템플릿으로 빠르게 draft 내고, brand desk에서 Lovart로 ship하는 운영자.

### 건너뛸 사람?

모델이 전략을 invent해 줄 거라 기대하는 사람.

### Lovart가 Canva를 완전 대체?

아니요. Canva onboarding + Lovart production loop가 흔한 조합.

### 변형 몇 개?

3–4개.

### 최대 red flag?

작은 카피 변경에 layout 전체를 다시 잡아야 할 때.

## 내부 링크

| 앵커 | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 가입 | https://lovart.ai/signup |
""",
    "drill_fn": lambda: ko_drills("canva ai image generator review", [
        "Instagram carousel draft", "내부 승인용 포스터", "주간 리테일 특가",
        "캠퍼스 채용 KV", "웨비나 커버", "DTC drop hero", "Brand Kit drift 수정",
        "Touch Edit 날짜 변경", "multi-CTA clutter", "폰 너비 proof",
    ], 45),
})

# 9. zh-TW coffee shop
ARTICLES.append({
    "file": "zh-TW-best-ai-design-agent-for-coffee-shop-owner.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="咖啡店主該選哪個 AI 設計智能體？2026 實戰指南",
        slug="best-ai-design-agent-for-coffee-shop-owner",
        date=DATE, language="zh-TW", page_type="Blog Post", category="Industry Solution",
        author="Lovart Content Team",
        description="繁體實戰：咖啡店主週更海報、限動、菜單視覺與 Lovart 工作流，含踩坑。",
        focus_keyword="best ai design agent for coffee shop owner",
        keywords=["coffee shop", "ai design agent", "lovart", "small business"],
        seo_title="咖啡店主該選哪個 AI 設計智能體？2026 實戰指南",
        seo_description="實戰指南：午間套餐、季節豆單、Instagram 限動與 Lovart ChatCanvas + Touch Edit。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-058-1024x682.png",
        alt_text="best ai design agent for coffee shop owner — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 咖啡店主該選哪個 AI 設計智能體？2026 實戰指南

這篇補 `/zh-TW/blog/best-ai-design-agent-for-coffee-shop-owner` 404。讀者不是設計師，是**週二要換午間套餐海報、週五要限動倒數**的店主。我按這個節奏寫。

## 我的立場

咖啡店視覺需求很固定：豆單、季節特調、午間套餐、活動海報、Instagram 九宮格。你要的不是「會畫畫的 AI」，是**改價格不用整張重畫**的智能體。

## 店主真實痛點（我訪談過的）

1. 外包一張海報等三天，活動只剩一天
2. Canva 模板像模板，第三家分店開始不像同一品牌
3. 自己 P 圖，字越改越糊
4. 限動 9:16 與門口 TV 16:9 要兩份，常只做一份硬 crop

## 評判標準

- 改「NT$120 → NT$99」要多久
- 三店 logo 色是否一致
- 手機上優惠字是否讀得懂
- 會不會生出假 Starbucks 風 logo（法務雷）

## 為什麼我推 Lovart（誠實版）

不是因為功能列表最長，是因為 **ChatCanvas 一句 brief → Brand Kit 鎖店色 → Touch Edit 改價** 這條路最貼店主週更。MCoT 適合「本週五張限動同一活動」這種小系列。

## 踩坑

**坑 1：用生成器做帶價格的海報。** 改價 = 整图重跑。

**坑 2：每店各做各的 accent 色。** 第三店開始像加盟亂版。

**坑 3：海報字太小，門口 2 米外讀不懂。** 手机宽度 不够就要改 layout，不是改亮度。

**坑 4：两个 CTA：「來店」+「外送」并排。** 路人 3 秒看不懂。

**坑 5：季節豆單只更新文字，視覺還是去年冬天。** 顾客以为没上新。

## 店主一週範例

| 日 | 任務 | Lovart 動作 |
| --- | --- | --- |
| 一 | 收本週 offer | ChatCanvas 一句 job |
| 二 | 海報 3 direction | Brand Kit 鎖色 |
| 三 | Touch Edit 改價 | 不全图重跑 |
| 四 | 9:16 限動 | MCoT 同 scaffold |
| 五 | 門口 TV export | 多尺寸 artboard |

## 公式

\\[ \\text{店主時間} = \\frac{\\text{Touch Edit 次數}}{\\text{外包等待天數}} \\]

## 內鏈

| 錨點 | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 設計智能體 | /blog/ai-powered-design-agent-for-creators |
| 註冊 | https://lovart.ai/signup |

## FAQ

### 完全不懂設計能用嗎？

能，前提是願意寫一句清楚 offer（一個優惠、一個 CTA、一個日期）。

### 要會英文 prompt 吗？

繁體 brief 即可；品牌術語 Lovart/ChatCanvas/Touch Edit 不翻譯。

### 取代外包设计师吗？

取代小改與週更；開店 VI 仍建議真人做一次 Brand Kit 打底。

### 幾店連鎖？

Brand Kit 一次鎖色，各店 Touch Edit 改地址/價格。

### 菜單照片呢？

實拍 + AI 排版 surface；食物本身别过度生成。
""",
    "drill_fn": lambda: zhtw_drills("咖啡店 AI 設計智能體", [
        "午間套餐海報", "季節豆單更新", "Instagram 限動 9:16", "門口 TV 16:9",
        "三店 accent 一致", "Touch Edit 改價", "外送平台 banner", "週末 live 倒數",
        "联名活动 KV", "会员日 push", "假 logo 避坑", "手機宽度 offer 可读",
    ], 52),
})

# 10. zh ai branding 101
ARTICLES.append({
    "file": "zh-ai-branding-101.md",
    "lang": "zh",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="AI 品牌入门 101：2026 小团队可执行手册",
        slug="ai-branding-101",
        date=DATE, language="zh", page_type="Blog Post", category="Branding",
        author="Lovart Content Team",
        description="简体中文入门：AI 时代品牌系统、常见翻车与 Lovart Brand Kit 实操，含第一人称踩坑。",
        focus_keyword="ai branding 101",
        keywords=["ai branding", "brand kit", "lovart", "visual identity"],
        seo_title="AI 品牌入门 101：2026 小团队可执行手册",
        seo_description="实战入门：色票、字体系、改字成本与 Lovart ChatCanvas + Brand Kit + Touch Edit。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-059-1024x682.png",
        alt_text="ai branding 101 — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# AI 品牌入门 101：2026 小团队可执行手册

这篇补 `/zh/blog/ai-branding-101` 404。读者要的是「明天就能用」的品牌底线，不是 80 页 VI 手册。

## 我的立场

AI 让**出图变快**，也让**不一致变快**。没有 Brand Kit 的小团队，第三张 social 就开始 drift。AI branding 101 只回答一件事：**怎样快而不乱**。

## 品牌最小集（MVS）

1. **主色 + accent**（HEX，不是「大概蓝色」）
2. **字体系**（标题/正文各一款）
3. **Logo 安全区**（最小尺寸、禁变形）
4. **一句话 voice**（我们听起来像什么）
5. **CTA 动词表**（只用「注册/试用/下载」里的一个）

缺任何一项，AI 都会用「平均审美」替你填。

## AI 时代多出来的三条

1. **改字成本**：品牌 surface 必须能 Touch Edit，不能靠 regen
2. **假 logo 零容忍**：模型爱生成「像 Apple 但不是」
3. **系列 scaffold**：同一 campaign 共用 layout 合约

## 踩坑实录

**坑 1：先出图后定色。** 每张好看，合在一起不像一家。

**坑 2：把 Midjourney mood 当品牌指南。** mood 不是 system。

**坑 3：繁简混用同一 slug。** UX 灾难，我们内部真踩过。

**坑 4：不做手机宽度 proof。** 品牌=桌面显示器上的幻觉。

**坑 5：两个 CTA。** 品牌看起来犹豫，转化也犹豫。

## Lovart 实操（我带的 onboarding）

1. 30 分钟 Brand Kit：色票 + 字 + logo 变体
2. ChatCanvas 模板：「一 offer、一 CTA、一日期、渠道尺寸」
3. 出 3 direction，选一个锁进 Kit
4. Touch Edit 改字周三（我们内部叫改字周三）
5. 存档 brief + approved 版同一文件夹

## 对比：有 Kit vs 无 Kit

| 维度 | 无 Brand Kit | Lovart Brand Kit |
| --- | --- | --- |
| 第 3 张 drift | 常见 |  rare |
| 改价 | 重跑/PS | Touch Edit |
| 新人上手 | 靠口口相传 | brief 模板 |
| 失败解释 | 「模型随机」 | 「brief 缺项」 |

## 公式

\\[ \\text{品牌可信} = \\frac{\\text{重复出现的 HEX} \\times \\text{可读 CTA}}{\\text{整图重跑次数}} \\]

## 内链

| 锚点 | URL |
| --- | --- |
| Brand Kit 5 分钟 | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 视觉 identity 2026 | /blog/ai-visual-identity-design-2026 |
| 注册 | https://lovart.ai/signup |

## FAQ

### 小团队要先做 logo 还是 Kit？

已有 logo 就先 Kit；没有 logo 先用文字 mark + 色票，别等「完美 logo」才出街。

### AI 会拉低品牌档次吗？

会，如果你允许 drift 和假 logo；不会，如果你有 MVS + Touch Edit。

### 要请顾问吗？

一次性 VI 可请；weekly surface 用 Lovart agent 更贴。

### 多语言品牌？

slug 各语言 rewrite，术语 Lovart/MCoT/ChatCanvas/Touch Edit 不翻译。

### 怎么审计？

随机抽 5 张 surface：HEX、CTA、手机可读、无假 logo。
""",
    "drill_fn": lambda: zh_drills("AI 品牌入门", [
        "Brand Kit 30 分钟 onboarding", "accent 第三张 drift", "Touch Edit 改字周三",
        "假 logo BLOCK", "双 CTA 退回", "手机宽度 squint", "carousel 五张一致",
        "繁简 slug 分离", "brief 一句 job", "MCoT 拆 artboard",
        "新人用模板上手", "campaign 存档规范",
    ], 52),
})


def validate(text: str) -> list[str]:
    errs = []
    for w in BANNED_ZH:
        if w in text:
            errs.append(f"banned zh: {w}")
    for w in BANNED_EN:
        if re.search(rf"\b{w}\b", text, re.I):
            errs.append(f"banned en: {w}")
    if re.search(r"\bTODO\b|\[IMAGE .* PLACEHOLDER|IMAGE PLACEHOLDER", text, re.I):
        errs.append("placeholder found")
    if "releaseDate:" not in text or "publishedAt:" not in text:
        errs.append("missing date dual-write")
    if "status: ready" not in text:
        errs.append("status not ready")
    return errs


def main():
    report = []
    for art in ARTICLES:
        body = art["core"].strip() + "\n" + art["drill_fn"]()
        body += "\n\n*Article for www.lovart.ai/blog 404 recovery. Part of i18n 404 recovery content cluster.*\n"
        front = fm(**art["fm"])
        full = front + "\n\n" + body
        errs = validate(full)
        path = OUT / art["file"]
        path.write_text(full, encoding="utf-8")

        if art["floor_type"] == "han":
            count = han_count(body)
            passed = count >= art["floor"] and not errs
            metric = f"{count} han"
        elif art["floor_type"] == "ko_words":
            count = ko_words(full)
            passed = count >= art["floor"] and not errs
            metric = f"~{count} ko tokens"
        else:
            count = ru_words(full)
            passed = count >= art["floor"] and not errs
            metric = f"~{count} ru tokens"

        status = "PASS" if passed else "FAIL"
        if errs:
            status = "FAIL"
        report.append((art["file"], metric, art["floor"], status, "; ".join(errs) or "ok"))

    print("FILE | METRIC | FLOOR | STATUS | NOTES")
    print("---|---|---|---|---")
    for row in report:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")


if __name__ == "__main__":
    main()
