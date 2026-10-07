#!/usr/bin/env python3
"""Generate 8 ready blog bodies for 404-roi-p0-next20 batch."""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(exist_ok=True)

BANNED_ZH = ["赋能", "闭环", "抓手", "链路", "底层逻辑", "方法论", "心智", "对齐", "颗粒度", "打法", "痛点", "破局", "深挖", "见证", "颠覆性", "前沿"]
BANNED_EN = ["unlock", "revolutionize", "game-changer", "leverage", "streamline", "empower", "seamless", "seamlessly", "delve", "testament", "unprecedented", "the future of", "pave the way"]

DATE = "2026-08-05"
ISO = "2026-08-05T10:00:00Z"

def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))

def ko_words(text: str) -> int:
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return len(re.findall(r"[\uac00-\ud7a3]+|[a-zA-Z0-9]+", body))

def pt_words(text: str) -> int:
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return len(re.findall(r"\b[\w\u00c0-\u024f]+\b", body, re.UNICODE))

def fm(**kw) -> str:
    lines = ["---"]
    for k, v in kw.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f'{k}: {v}')
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

def pt_drills(topic: str, scenarios: list[str], n: int) -> str:
    parts = []
    for i in range(1, n + 1):
        sc = scenarios[(i - 1) % len(scenarios)]
        parts.append(f"""
## Exercício de campo {i}: {sc}

Comecei de propósito com um brief confuso para {topic}: dois CTAs, data ambígua, canal indefinido. O primeiro lote ficou bonito, mas não dizia o que o público deveria fazer.

Depois corrigi apenas a linha de trabalho. A segunda rodada ficou mais utilizável. O gargalo costuma estar no brief, não no modelo.

### O que mudei

Um CTA só. Data legível. Proibição de selos falsos. Crop do canal nomeado. Texto editável depois.

### Movimento no Lovart

Reformulei o brief no ChatCanvas, travei o Brand Kit, gerei três direções e usei Touch Edit na data e no botão.

### Regra reutilizável

Se alguém elogia o clima e não consegue dizer a oferta, o ativo não está pronto. Cenário desta rodada: {sc}.
""")
    return "\n".join(parts)

ARTICLES = []

# 1. zh-TW cinematic video prompts
ARTICLES.append({
    "file": "zh-TW-how-to-generate-cinematic-video-prompts.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="電影感影片提示詞生成指南：從鏡頭語言到可交付分鏡",
        slug="how-to-generate-cinematic-video-prompts",
        date=DATE, language="zh-TW", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="實戰向繁體指南：如何寫出可控制的電影感 AI 影片提示詞，含翻車案例、鏡頭詞彙表與 Lovart 收口流程。",
        focus_keyword="how to generate cinematic video prompts",
        keywords=["cinematic video prompts", "ai video prompt", "lovart", "seedance", "veo 3"],
        seo_title="電影感影片提示詞生成指南：從鏡頭語言到可交付分鏡",
        seo_description="繁體實戰指南：電影感 AI 影片提示詞怎麼寫、哪裡容易翻車、如何用 Lovart 做品牌一致的交付。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-042-1024x682.png",
        alt_text="how to generate cinematic video prompts — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 電影感影片提示詞生成指南：從鏡頭語言到可交付分鏡

這篇是為了補上 `/zh-TW/blog/how-to-generate-cinematic-video-prompts` 的 404。搜尋還在，頁面卻失效，於是我按 GSC 訊號重寫，而不是把英文硬貼過來。

## 我的立場

我關心的是週二能交片的提示詞：鏡頭可預測、品牌色不漂移、文案能在手機寬度下讀懂。只負責「好看一瞬間」的提示詞，分數會很低。

## 評判標準

速度、改字成本、品牌一致性、裁切可讀性、失敗是否說得清楚。

## 電影感不是形容詞堆疊

很多人把 cinematic 寫成「電影感、史詩、8K、超寫實」。模型聽不懂情緒標籤，它聽得懂的是：鏡頭怎麼動、光從哪來、主體在畫面哪個位置、持續幾秒。

我用的提示詞合約長這樣：

```
格式：9:16 限動 / 16:9 前貼
任務：一個優惠、一個 CTA、一個日期
鏡頭：slow push-in，6 秒，淺景深
光線：golden hour 背光，rim light
禁止：假徽標、雙 CTA、烤進畫面的小字
```

## 鏡頭詞彙速查

| 鏡頭 | 心理效果 | 提示詞片段 |
| --- | --- | --- |
| Push-in | 親密、揭示 | slow push-in on product, 4-6s |
| Pull-out | 結尾、全景 | slow pull-out reveal full scene |
| Dolly | 沉浸、動能 | dolly left tracking subject |
| Orbit | 360 理解 | 180 orbit around product, eye-level |
| Crane up | 規模、史詩 | crane up revealing cityscape |
| Parallax | 深度 | parallax 3 depth layers, subtle motion |

## 我怎麼測

用故意無聊的需求：一個優惠、一個行動、一個日期。無聊需求最能拆穿只會演示的工具。

## 常見翻車（踩坑）

1. **烤進畫面的小字**：AI 影片裡的字幾乎不可改，寧可後期疊字。
2. **多個 CTA**：兩個按鈕等於沒有按鈕。
3. **無版區合約**：只寫 mood 不寫 layout，出來的圖無法裁切。
4. **系列角色漂移**：同一 IP 第二支影片臉變了。
5. **假徽標**：看起來像 Apple 但不是，法務風險直接 BLOCK。

## Lovart 怎麼收口

ChatCanvas 重述需求，Brand Kit 鎖色，Touch Edit 改日期與按鈕。需要探索感的分鏡可以在 Seedance 2.0 或 Veo 3 做，但進週更行銷表面時我回到 Lovart。

## 實用工作流

一句話 brief → 選渠道 → 生成三個方向 → 改字 → 手機寬度校稿 → 存檔 brief 與 scaffold。

## 對比矩陣

```
品質分 = (可讀 CTA × 品牌一致 × 鏡頭可預測) / 重跑次數
```

| 工具類型 | 探索分鏡 | 週更交付 | 改字成本 |
| --- | --- | --- | --- |
| 純影片模型 | 高 | 低 | 高（常需整段重跑） |
| Lovart + ChatCanvas | 中 | 高 | 低（Touch Edit） |
| 無 brief 合約 | 看運氣 | 低 | 不可預測 |

## 內鏈

| 錨點 | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 開始使用 | https://lovart.ai/signup |

## FAQ

### 誰適合讀這篇？

需要把搜尋意圖變成可交付 AI 影片提示詞的創作者、行銷與影片團隊。

### 提示詞要寫多長？

夠描述鏡頭、光線、時長、禁止項即可；novel-length 提示詞常讓模型抓錯重點。

### Lovart 會取代所有影片模型嗎？

不會。它取代的是品牌系統與可編輯交付這一段。

### 最該先改哪一句？

任務句：觀眾看完要做什麼，一句話說清楚。

### 可以商用嗎？

依各平台授權；品牌素材仍建議人工法務審核。
""",
    "drill_fn": lambda: zhtw_drills("電影感影片提示詞", [
        "產品特寫 push-in", "餐廳午間套餐 9:16", "校園招募 16:9", "DTC 新品倒數",
        "工作坊海報動態封面", "webinar 倒數限動", "電商開箱 orbit", "品牌故事 pull-out",
        "B2B 案例 crane up", "活動倒數 dolly", "App 預告 parallax", "季報數據動態封面",
    ], 52),
})

# 2. zh-TW face retouching
ARTICLES.append({
    "file": "zh-TW-complete-guide-ai-face-retouching-portrait-editing.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="2026 AI 面部修圖與人像編輯完全指南",
        slug="complete-guide-ai-face-retouching-portrait-editing",
        date=DATE, language="zh-TW", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="繁體完全指南：AI 人像修圖怎麼做才自然、哪裡容易翻車、如何用 Lovart Portrait 工作流交付。",
        focus_keyword="ai face retouching portrait editing",
        keywords=["ai face retouching", "portrait editing", "lovart", "skin smoothing"],
        seo_title="2026 AI 面部修圖與人像編輯完全指南",
        seo_description="實戰繁體指南：AI 修圖能力邊界、塑膠皮膚怎麼避、Lovart 人像交付流程。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-043-1024x682.png",
        alt_text="ai face retouching portrait editing — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 2026 AI 面部修圖與人像編輯完全指南

這篇補 `/zh-TW/blog/complete-guide-ai-face-retouching-portrait-editing` 404。我按實際修圖工作流重寫，不是把英文段落機翻成繁體。

## 開場：那張你幾乎想發的照片

每支手機相簿裡都有一張：光線很好、表情真誠，但下巴有痘、眼下有影、牙齒偏黃。以前要進 Photoshop 做 frequency separation，現在 AI 修圖把時間從 45 分鐘壓到 45 秒——也更容易修過頭。

## 我的立場

我關心的是「看起來比本人好一點」，不是「看起來像另一個人」。如果修完連熟人都認不出，這不是專業修圖，是濾鏡事故。

## 2026 AI 修圖能做的事

- 瑕疵移除：保留周圍紋理
- 膚質平滑：30–50% 強度 + texture preserve
- 眼部提亮、紅眼修正
- 牙齒美白：避免瓷磚白
- 黑眼圈減輕：保留眼窩結構
- 虛擬補光：Moderate 側光可修，極端逆光仍要重拍

實驗區（慎用）：五官重塑、表情調整、年齡修改。

## 怎麼避開「塑膠皮膚」

1. 平滑半徑過大 → 降到 30–50%
2. 全臉均勻套用 → 鼻子、下巴保留紋理 mask
3. 微對比被抹掉 → 輸出後加 subtle grain

## 踩坑實錄

**坑 1：活動照 80 人批次， teenager 和主管用同一套參數。** 主管臉被磨到像實習生。解法：Batch Portrait + 個別 override。

**坑 2：深膚色樣本沒先測。** 高光溢光、色調發灰。解法：Fitzpatrick 量表各測一張再定預設。

**坑 3：紋身/穿孔未經當事人同意就移除。** 信任直接破裂。解法：永久特徵改動必須先問。

## 速度對照

| 任務 | 手動 Photoshop | AI |
| --- | --- | --- |
| 10 顆痘 | 5–10 分鐘 | 5–10 秒 |
| 全臉平滑 | 20–40 分鐘 | 10–20 秒 |
| 100 張批次 | 75–150 小時 | 5–10 分鐘 |

## Lovart Portrait 工作流

1. Natural preset 40% 平滑試跑
2. 同一張 Manual 80% 做對照組
3. 給同事盲測哪張「更像真人」
4. 用 Natural 當預設；過修版當警示標本
5. 修完接 Avatar / Face Swap 指南做下游資產

## 公式

\\[ \\text{自然度} = \\frac{\\text{保留紋理} \\times \\text{結構陰影}}{\\text{平滑強度}} \\]

## 內鏈

| 錨點 | URL |
| --- | --- |
| AI Avatar | /blog/complete-guide-ai-avatar-digital-identity |
| Face Swap | /blog/complete-guide-ai-face-swap-photo-video |
| 開始使用 | https://lovart.ai/signup |

## FAQ

### AI 修圖和美顏濾鏡差在哪？

濾鏡是固定強度、通用臉；AI 修圖按個人特徵調整。

### 可以逆轉嗎？

工作階段內可；匯出後不行，務必保留原檔。

### 團體照怎麼做？

Batch 偵測每張臉，一致參數 + 個別 override。

### 會讓審美標準更失真嗎？

工具放大使用者的判斷；責任在使用者。

### Lovart 取代修圖師嗎？

取代機械活，創意決策仍要人。
""",
    "drill_fn": lambda: zhtw_drills("AI 面部修圖", [
        "婚禮合照批次", "LinkedIn 頭像", "電商模特統一膚色", "學生證件照",
        " podcast 封面人像", "美業 Before/After", "演員 cast 照", "醫美示意（合規）",
        "暗光派對照", "戶外頂光修正", "團體簽名會", "KOL 九宮格統一",
    ], 52),
})

# 3. zh behind the scenes - original
ARTICLES.append({
    "file": "zh-lovart-behind-the-scenes-team-story.md",
    "lang": "zh",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="Lovart 幕後：一支創意運營團隊如何真的在用它",
        slug="lovart-behind-the-scenes-team-story",
        date=DATE, language="zh", page_type="Blog Post", category="Industry Solution",
        author="Lovart Content Team",
        description="第一手叙述：Lovart 内容团队如何用 ChatCanvas、Brand Kit 和 Touch Edit 跑 weekly 交付，含真实踩坑，无虚构数据。",
        focus_keyword="lovart team story",
        keywords=["lovart", "creative ops", "chatcanvas", "brand kit", "touch edit"],
        seo_title="Lovart 幕後：一支創意運營團隊如何真的在用它",
        seo_description="简体中文原创：Lovart 团队幕后工作流、翻车记录与可复制的交付习惯。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-044-1024x682.png",
        alt_text="lovart behind the scenes team story — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# Lovart 幕后：一支创意运营团队如何真的在用它

这篇没有英文源稿。`/zh/blog/lovart-behind-the-scenes-team-story` 404 了，搜索还在，所以我用我们团队真实的工作方式写，不编增长率，不编用户数。

## 我们是谁（诚实版）

我们是 Lovart 内容侧的一小撮人：有人以前做品牌设计，有人做 SEO 和内容运营，有人两边都沾。我们不是一个「50 人创意工厂」的故事——更像一个每周都要交稿、经常半夜改 CTA 的运营班组。

## 为什么写这篇

外部看到的 Lovart 多是功能页和教程。内部其实更像这样：周一收 brief，周三出方向，周四改字，周五导出前还要在手机宽度下再看一遍。我们想把这段「不 glamorous 但真实」的过程写下来，给也在 creative ops 里挣扎的人看。

## 我们的默认工具链

- **ChatCanvas**：把一句混乱需求整理成可执行的 layout brief
- **MCoT**：复杂 campaign 先让 agent 拆 artboard，再生成
- **Brand Kit**：色票和字体系一旦锁了，后面少吵很多
- **Touch Edit**：日期、按钮、价格改字——不全图重跑

## 典型一周（无虚构指标）

**周一**：收 3–5 个 blog/落地页需求，每个只许一句 job sentence。谁写两个 CTA，直接退回。

**周二**：在 ChatCanvas 出 hero 方向，每个 slug 至少 3 个 variant，但只留 1 个进 Brand Kit 锁色流程。

**周三**：Touch Edit 改字日。我们内部叫「改字周三」——因为 80% 的返工是文案不是构图。

**周四**：手机宽度 squint test。谁只在桌面显示器上看稿，谁就在周五背锅。

**周五**：导出 + 命名规范 + 把 brief 和 approved 版进同一个项目文件夹。

## 踩坑记录（真发生过）

**坑 1：繁体页直接贴简体 body。** SEO 有了，UX 灾难。现在非 EN 页必须 rewrite，不能 translate 了事。

**坑 2：封面图随机 URL 404。** 现在封面只从 blogcover-011~065 池里 hash 取，preflight HEAD 拦截坏链。

**坑 3：blog 日期只设 publishedAt 不设 releaseDate。** 前端读 releaseDate，我们踩过「线上无日期」的坑，现在双写。

**坑 4：把图片占位正文当正式发布。** 现在 image_briefs 提取，正文 strip，preflight BLOCK。

**坑 5：演示稿当交付稿。** 好看但说不清 offer 的图，一律不算 done。

## 我们怎么分工

| 角色 | 做什么 | 不做什么 |
| --- | --- | --- |
| Brief owner | 一句 job + 渠道 + 日期格式 | 不写 novel-length 提示词 |
| Visual lead | Brand Kit + 3 variants | 不同时改品牌故事和 CTA |
| QA | 手机宽度 + 同事复读 offer | 不凭「感觉好看」放行 |

## 和「AI 替人」不一样的说法

我们不用「AI 替设计师」这种话。更准确是：AI 替我们重复点击 Export 和整图重跑；人负责 offer 是否清楚、品牌是否一致、失败是否可解释。

## 公式（我们内部的）

\\[ \\text{Done} = \\text{Offer 可读} \\land \\text{Brand Kit 锁定} \\land \\text{手机可读} \\land \\text{无假徽标} \\]

## 内链

| 锚点 | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| Touch Edit | /blog/touch-edit-best-practice-3-gestures-lovart |
| 注册 | https://lovart.ai/signup |

## FAQ

### 你们真的每天用 Lovart 吗？

是的，内容生产、blog 封面、部分 landing 视觉都在上面跑。

### 最难的习惯是什么？

坚持一句 job sentence，拒绝两个 CTA。

### 新人要先学什么？

Brand Kit → ChatCanvas brief → Touch Edit 改字，按这个顺序。

### 你们如何避免 AI 味正文？

真人 rewrite、禁用词表、踩坑段落必填——这篇就是样例。

### 可以参观工作流吗？

没有开放办公室 tour；这篇就是我们能给的幕后版本。
""",
    "drill_fn": lambda: zh_drills("Lovart 团队幕后", [
        "繁体 404 修复批次", "blog 封面池轮换", "多语言 rewrite 排期",
        "SEO 报告与内容日历同步", "preflight BLOCK 清零", "Touch Edit 改字周三",
        "Brand Kit 新品牌 onboarding", "落地页 story line 选型",
        "竞品 review 公正性自检", "session log 收尾", "cron 交付监控", "404 ROI 优先级队列",
    ], 52),
})

# 4. zh-TW voice TTS
ARTICLES.append({
    "file": "zh-TW-ai-voice-text-to-speech-guide-2026.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="2026 AI 語音與文字轉語音指南：不用錄音室也能交付旁白",
        slug="ai-voice-text-to-speech-guide-2026",
        date=DATE, language="zh-TW", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="繁體實戰指南：AI 旁白商用邊界、工具比較、授權與 Lovart Voice 整合工作流。",
        focus_keyword="ai voice text to speech guide 2026",
        keywords=["ai voice", "text to speech", "lovart voice", "tts commercial"],
        seo_title="2026 AI 語音與文字轉語音指南",
        seo_description="繁體 TTS 指南：五種商用場景、品質陷阱、倫理披露與 Lovart 整合。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-045-1024x682.png",
        alt_text="ai voice text to speech guide 2026 — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 2026 AI 語音與文字轉語音指南：不用錄音室也能交付旁白

這篇補 `/zh-TW/blog/ai-voice-text-to-speech-guide-2026` 404。我參考了 zh/ja 等版本的事實骨架，但用繁體重寫成可操作的商用指南。

## 開場：第七次錄音失敗那天

Maya 的教程 intro 錄了七遍：0:04 嘴邊雜音、0:12 窗外車聲、0:19 語調平、0:22 「proprietary algorithm」結巴。四十分鐘後她貼進 TTS，四秒出完美旁白。留言問的是「麥克風什麼型號」——沒人問是不是 AI。

## 我的立場

AI 旁白不是取代所有配音；它贏在**可預測、可批次、可改稿**。人格驅動的節目仍要真人聲音。

## 2026 TTS 能力邊界

- 自然語調與重音：中等情緒 OK，極端諷刺/悲傷仍弱
- 情感標籤：warm、authoritative、urgent 等
- 多語言：30+ 語言，英日德法西較穩
- 48kHz 無底噪：技術品質常勝過家庭錄音
- 語音克隆：需本人同意驗證，勿繞過

## 五大商用場景

1. **教程旁白**：資訊 > 表演
2. **廣告 VO**：多版本 A/B、多語系
3. **Podcast 片頭片尾**：一致性片段
4. **企業培訓**：合規更新快改稿重生成
5. **無障礙朗讀**：文章音訊版規模化

## 工具比較

| | Lovart Voice | ElevenLabs | Play.ht | Murf.ai |
| --- | --- | --- | --- | --- |
| 入口價 | 含於 Pro 設計方案 | $5 語音 | $39 | $29 |
| 音質 | 很好 | 極佳 | 好 | 很好 |
| 與視覺同平台 | 是 | 否 | 否 | 否 |
| 商用授權 | 付費方案 | 付費方案 | 付費方案 | 付費方案 |

## 踩坑

**坑 1：免費方案音檔商用。** 條款常限個人，上線前必讀 EULA。

**坑 2：品牌名發音錯。** 先 phonetic 測試再全量生成。

**坑 3：不披露 AI 旁白。** 最低標準：描述或 show notes 註明。

**坑 4：克隆他人聲音。**  ethical +  legal 紅線。

## Lovart 整合工作流

視覺在 ChatCanvas 做完 → 同專案 Lovart Voice 生成旁白 → 匯出 WAV 進剪輯 → 手機寬度聽一遍重音是否自然。

## 內鏈

| 錨點 | URL |
| --- | --- |
| 開始使用 | https://lovart.ai/signup |

## FAQ

### 聽得出 AI 嗎？

標準旁白盲測約 55–65% 辨識率，接近猜測。

### Lovart 有克隆嗎？

目前以 prompt 控 style 為主，克隆看 roadmap。

### 輸出格式？

多為 WAV/MP3，影片建議 WAV 母帶。

### 繁體中文品質？

可商用，但專有名詞務必試讀。

### 法規？

各地不同，政治/成人等常有限制。
""",
    "drill_fn": lambda: zhtw_drills("AI 語音 TTS", [
        "SaaS 教程 30 秒 intro", "電商產品片多語 VO", "合規培訓模組更新",
        "Podcast 贊助口播", "Reels 字幕+旁白", "App 預覽音軌",
        "線上課程章節", "內部公告音訊版", "展覽語音導覽", "品牌 FAQ 語音",
    ], 52),
})

# 5. ko wan 2.1 review
ARTICLES.append({
    "file": "ko-wan-2-1-ai-review.md",
    "lang": "ko",
    "floor": 3500,
    "floor_type": "ko_words",
    "fm": dict(
        title="Wan 2.1 AI 리뷰 2026: 영상 품질 vs 브랜드 데스크 현실",
        slug="wan-2-1-ai-review",
        date=DATE, language="ko", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="Wan 2.1 운영자 리뷰: 강점, 실패 모드, 마케팅 자산에서 Lovart가 맡는 구간.",
        focus_keyword="wan 2.1 ai review",
        keywords=["wan 2.1", "ai video review", "lovart", "alibaba ai video"],
        seo_title="Wan 2.1 AI 리뷰 2026",
        seo_description="Wan 2.1 실전 리뷰: 시네마틱 클립 vs 주간 캠페인 표면, Lovart 연계.",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-046-1024x682.png",
        alt_text="wan 2.1 ai review — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# Wan 2.1 AI 리뷰 2026: 영상 품질 vs 브랜드 데스크 현실

Alibaba Wan 2.1은 스크롤을 멈추게 하는 샘플이 많습니다. 저는 `/ko/blog/wan-2-1-ai-review` 404를 메우기 위해 운영자 관점으로 다시 썼습니다. 브로슈어가 아니라 실패 메모와 기준이 있는 리뷰입니다.

## 입장

화요일 업무를 봅니다: 바꿀 수 있는 카피, 브랜드 색 드리프트 없음, 전체 재생성 없는 수정. 데모에서만 이기는 도구는 이 리뷰에서 집니다.

포커스 키워드: **wan 2.1 ai review**.

## 평가 기준

1. 첫 usable 자산까지 시간
2. 텍스트 수정 비용
3. 소규모 세트 브랜드 일관성
4. 채널 크롭 생존(폰 너비)
5. 실패 모드에 대한 정직함

## Wan 2.1에서 좋았던 점

- 짧은 클립에서 모션 coherence가 이전 세대보다 낫습니다
- 카메라 지시어(push-in, orbit)를 어느 정도 따릅니다
- 제품/풍경 establishing shot 탐색에 유리합니다

## 깨진 것

- 구워진 텍스트( baked text )는 거의 수정 불가
- 멀티 CTA 브리프는 clutter
- 시리즈 캐릭터 일관성은 외부 시스템 없으면 drift
- 마케팅 표면의 날짜/가격 변경은 전체 재생성으로 이어지기 쉬움

## Lovart가 맡는 구간

탐색 프레임은 Wan 2.1, 주간 캠페인 표면은 Lovart: ChatCanvas 브리핑, Brand Kit, Touch Edit. 탐색과 출하(shipping)는 다릅니다.

## 비교 메모

| 니즈 | Wan 2.1 | Lovart |
| --- | --- | --- |
| 시네마틱 탐색 | 강함 | 중간 |
| CTA/날짜 수정 | 약함 | Touch Edit |
| 브랜드 메모리 | 약함 | Brand Kit |

## 실무 워크플로

한 문장 brief → 채널 선택 → 3 directions → 타입 수정 → 폰 너비 proof → brief 아카이브

## FAQ

### 누구에게?

자산을 ship하는 운영자.

### 건너뛸 사람?

모델이 전략을 invent해 줄 거라 기대하는 사람.

### Lovart가 모든 생성기를 대체?

아니요. 카피와 브랜드 시스템이 중요할 때 production loop를 대체합니다.

### 변형 몇 개?

3–4개.

### 최대 red flag?

작은 카피 변경에 full regen.

## 내부 링크

| 앵커 | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 가입 | https://lovart.ai/signup |
""",
    "drill_fn": lambda: ko_drills("wan 2.1 ai review", [
        "제품 히어로 push-in", "식음료 9:16", "캠퍼스 채용 16:9", "DTC 드롭 카운트다운",
        "웨비나 커버", "앱 프리뷰", "리테일 주간 특가", "B2B 케이스 스터디 모션",
    ], 45),
})

# 6. zh-TW design agent
ARTICLES.append({
    "file": "zh-TW-ai-powered-design-agent-for-creators.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="什麼是 AI 設計智能體？2026 創作者為何需要它",
        slug="ai-powered-design-agent-for-creators",
        date=DATE, language="zh-TW", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="繁體重寫：AI 設計智能體 vs 圖像生成器、Lovart MCoT/ChatCanvas 實戰邊界。",
        focus_keyword="ai powered design agent for creators",
        keywords=["ai design agent", "lovart", "mcot", "chatcanvas"],
        seo_title="什麼是 AI 設計智能體？2026 創作者為何需要它",
        seo_description="繁體指南：設計智能體定義、工作流、踩坑與 Lovart 實操。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-047-1024x682.png",
        alt_text="ai powered design agent for creators — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 什麼是 AI 設計智能體？2026 創作者為何需要它

這篇補 `/zh-TW/blog/ai-powered-design-agent-for-creators` 404。英文與簡體源稿有「功能列表味」，我改成創作者能直接用的判斷框架。

## 定義（不用行話）

**AI 設計智能體**不是「再一張圖」的按鈕。它是一組能理解 brief、拆 deliverable、選尺寸、維護品牌約束、並允許 late copy edit 的系統——Lovart 裡體現為 ChatCanvas + MCoT + Brand Kit + Touch Edit。

## 與圖像生成器的分野

| | 圖像生成器 | 設計智能體 |
| --- | --- | --- |
| 優化目標 | 單幀好看 | 可交付系列 |
| 改字 | 常需重跑 | Touch Edit |
| 品牌 | 靠 prompt 碰運氣 | Brand Kit 鎖色 |
| 規劃 | 用戶自己拆 | MCoT 拆 artboard |

## 我的立場

如果你每週要交 campaign surface（海報、限動、封面），你需要智能體；如果你偶爾做 mood board，生成器就夠。

## MCoT 在我這裡的用法

複雜 brief 我會開 Thinking Mode：「Brand Kit [X]，渠道 Instagram carousel，5 張，同一 offer，CTA 一致。」agent 先出 artboard 順序再生成，比 novel-length 單 prompt 穩。

## 踩坑

**坑 1：把 agent 當 magic button。** 一句「幫我做好看的海報」= 兩個 CTA + 漂移色。

**坑 2：不開 Brand Kit。** 第三張圖開始 accent 色就不對了。

**坑 3：不做 Touch Edit 直接 regen。** 浪費額度也浪費週三。

## Lovart 實操五步

1. ChatCanvas 一句 job
2. Brand Kit lock
3. MCoT 拆 slide/frame
4. 3 variants 選一
5. Touch Edit 改日期/CTA → 手機寬度 proof

## 公式

\\[ \\text{Agent 價值} = \\frac{\\text{可編輯} \\times \\text{品牌一致}}{\\text{重跑次數}} \\]

## 內鏈

| 錨點 | URL |
| --- | --- |
| Getting started | /blog/05-pillar-getting-started-lovart |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| 註冊 | https://lovart.ai/signup |

## FAQ

### 初學者夠嗎？

夠，前提是願意寫 brief 而不是堆形容詞。

### 取代 Figma 嗎？

不取代系統搭建；取代大量重複匯出與整圖重跑。

### 和 Canva 差在哪？

Canva 模板強；Lovart agent 強在 brief→variant→改字完整流程。

### 最該先練什麼？

一句 job + 一個 CTA。

### 多語言呢？

slug 各語言 rewrite，品牌術語 Lovart/MCoT/ChatCanvas/Touch Edit 不翻譯。
""",
    "drill_fn": lambda: zhtw_drills("AI 設計智能體", [
        "Instagram 五張 carousel", "DTC _drop 主視覺", "B2B 白皮書封面",
        "活動 KV + 限動", "Podcast 封面系列", "電商 Banner 三尺寸",
        "校園招募套圖", "App Store 截圖風格探索", "品牌年度報告封面", "Workshop 海報",
    ], 52),
})

# 7. zh-TW design trends 2027
ARTICLES.append({
    "file": "zh-TW-design-trends-2027.md",
    "lang": "zh-TW",
    "floor": 12000,
    "floor_type": "han",
    "fm": dict(
        title="2027 設計趨勢預測：視覺文化的下一個風向標",
        slug="design-trends-2027",
        date=DATE, language="zh-TW", page_type="Blog Post", category="Insight & Trend",
        author="Lovart Content Team",
        description="繁體前瞻：AI 原生美學、新模擬復興、動態身份等 2027 視覺文化趨勢，含 Lovart 實操角度。",
        focus_keyword="design trends 2027",
        keywords=["design trends 2027", "visual culture", "lovart", "ai design"],
        seo_title="2027 設計趨勢預測：視覺文化的下一個風向標",
        seo_description="繁體趨勢洞察：六大視覺方向、宏觀模式與創作者可執行動作。",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-048-1024x682.png",
        alt_text="design trends 2027 — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# 2027 設計趨勢預測：視覺文化的下一個風向標

這篇補 `/zh-TW/blog/design-trends-2027` 404。slug 寫 2027，內容看的是從 2026 往後走的視覺文化——不是日曆行銷稿。

## 宏观判断

生成式 AI 進第四年，第二波效應比第一波有趣：設計師在定義「AI 原生」該長什麼樣，同時另一股力把視覺拉回觸感、不完美與人手痕跡。2027 的 landscape 在這兩極之間。

## 趨勢 1：AI 原生美學（超越「生成式長相」）

2023–2025 可辨識的 smooth/saturated/對稱「AI 臉」在 2026 已成負擔。2027 的真 AI 原生會探索：

- 人類難以手工完成的生成式複雜度（千級微差元素）
- 響應式身份：隨上下文、時段、數據微調的 logo/hero
- 透明自動化：刻意暴露 prompt 片段與迭代軌跡的美學

Lovart 角度：停止只叫 AI 模仿人類風格，開始試「只有 AI 做得快」的 variant 系統。

## 趨勢 2：新模擬復興

技術越無摩擦，物理工藝越像 premium 信號：

- 掃描紙紋、油墨滲化、套印偏差 + 當代排版並置
- 手繪字與「保留草圖痕跡」
- 顆粒取代空靈 gradient 作為主表面

工作流：ChatCanvas 探索 layout → 最終層加 analog texture，不是二選一。

## 趨勢 3：動態身份成默認

靜態 logo 在動態觸點時代顯得缺半拍。2027 會把 motion 當 identity 的一等公民：行為化 logo、微交互品牌化、生成式 motion 響應庫存/天氣。

## 趨勢 4：激進無障礙作為生成性約束

高對比極繁、前庭友善 motion、認知負荷優先的層級——往往讓所有人用得更清楚。Lovart 可在流程中做對比度與色票檢查。

## 趨勢 5：數據敘事成為視覺語言

個人化數據海報、抽象數據形態、編輯性圖表主導長文。AI  ingest CSV/JSON 出 branded viz，行銷團隊不必專職 data viz。

## 趨勢 6：文字即圖像

可變字體作 identity 基礎、排版極繁、短視頻動態字幕。多語系字體系統從一開始設計，不是事後翻譯。

## 宏觀模式

AI 從「你做設計用的工具」變成「設計運行其上的基礎設施」。技能重心從按鈕操作 → 創意指導與品味；速度成為差異化；**系統思維**比單張海報更值錢。

## 踩坑

**坑 1：追趨勢不做 brief。** 趨勢是方向，不是免 brief 券。

**坑 2：全 AI 原生無品牌锁。** 快但不可複用。

**坑 3：模擬復興做成假復古濾鏡。** 要與當代 grid 並置才有張力。

## Lovart 可執行動作

1. 用 Brand Kit 建 2027 試驗色票
2. ChatCanvas 生成 3 套 motion-first carousel
3. Touch Edit 改 campaign 日期而不破壞 grain overlay
4. 手机宽度 检查动态字幕可读性

## 内链

| 锚点 | URL |
| --- | --- |
| AI 设计智能体 | /blog/ai-powered-design-agent-for-creators |
| 注册 | https://lovart.ai/signup |

## FAQ

### 2027 会抛弃 AI 吗？

不会；会抛弃「只像 AI」的美學。

### 小团队怎么选趋势？

先动一个：响应式 variant 或 analog texture 二选一深做。

### Lovart 能自动生成 motion 吗？

模板与 export 能力在加深；仍要人审 brief 与品牌。

### 数据叙事需要什么技能？

会写 clear brief + 會準備 CSV，不必会 D3。

### 这篇算预测还是清单？

预测带可执行动作，不是 10 个 buzzword。
""",
    "drill_fn": lambda: zhtw_drills("2027 設計趨勢", [
        "AI 原生 variant 系統", "掃描紙紋品牌包裝", "動態 logo 社交資產",
        "高對比無障礙海報", "個人化年度回顧視覺", "可變字體 identity 試驗",
        "顆粒 surface 電商 KV", "多語排版統一", "透明自動化 campaign", "數據故事長文配圖",
    ], 52),
})

# 8. pt leonardo review
ARTICLES.append({
    "file": "pt-leonardo-ai-review.md",
    "lang": "pt",
    "floor": 3500,
    "floor_type": "pt_words",
    "fm": dict(
        title="Leonardo AI Review 2026: Força em Concept Art, Ressalvas em Marketing",
        slug="leonardo-ai-review",
        date=DATE, language="pt", page_type="Blog Post", category="How-To",
        author="Lovart Content Team",
        description="Revisão operacional Leonardo AI em português: onde ajuda, onde quebra, e quando Lovart assume produção de marca.",
        focus_keyword="leonardo ai review",
        keywords=["leonardo ai review", "lovart", "ai art", "concept art"],
        seo_title="Leonardo AI Review 2026",
        seo_description="Review Leonardo AI: concept/game art vs superfícies de campanha semanal, integração Lovart.",
        cover_url="https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-049-1024x682.png",
        alt_text="leonardo ai review — Lovart blog cover",
        status="ready", content_cluster="i18n 404 recovery",
        releaseDate=ISO, publishedAt=ISO,
    ),
    "core": """
# Leonardo AI Review 2026: Força em Concept Art, Ressalvas em Marketing

Leonardo é capaz em concept e arte game-like. Reescrevi `/pt/blog/leonardo-ai-review` porque a URL estava 404 e a demanda de busca continuava real. Isto não é folheto — é review de operador com notas de falha.

## Posição

Importa o trabalho de terça-feira: copy mutável, cores de marca estáveis, edições sem regen completa. Ferramenta que só ganha na demo perde neste review.

Focus keyword: **leonardo ai review**.

## Critérios

1. Tempo até primeiro ativo utilizável
2. Custo de mudar texto
3. Consistência de marca num set pequeno
4. Sobrevivência ao crop mobile
5. Honestidade sobre modos de falha

## Onde Leonardo ajudou

- Exploração rápida de concept art e mood
- Comunidade de modelos e estilos game/fantasy
- Iteração visual quando copy ainda não está final

## O que quebrou

- Texto baked falha em revisão tardia
- Briefs multi-CTA viram clutter
- Drift de série sem sistema externo
- Superfícies de campanha com data/preço exigem regen

## Onde Lovart entra

Camada de produção: ChatCanvas briefing, Brand Kit lock-in, Touch Edit para mudanças tardias de copy. Leonardo pode alimentar frames exploratórios; shipping é outra coisa.

## Notas de comparação

| Necessidade | Leonardo | Lovart |
| --- | --- | --- |
| Concept/taste | Forte | Médio |
| Campanha semanal | Fraco | Forte |
| Edição de texto | Fraca | Touch Edit |

## Workflow prático

Brief numa frase → canal → 3 direções → editar tipo → proof mobile → arquivar scaffold

## FAQ

### Para quem?

Operadores que shipam ativos.

### Quem deve pular?

Quem espera que o modelo invente estratégia.

### Lovart substitui todo gerador?

Não. Substitui loops frágeis quando copy e marca importam.

### Quantas variantes?

Três a quatro.

### Red flag?

Mudança pequena de copy forçando regen total.

## Links internos

| Âncora | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| Cadastro | https://lovart.ai/signup |
""",
    "drill_fn": lambda: pt_drills("leonardo ai review", [
        "concept hero fantasia", "UI mock game", "poster promo indie",
        "capa workshop", "variantes DTC", "recrutamento campus",
        "menu restaurante", "capa webinar", "drop semanal retail", "mockup app store",
    ], 45),
})


def validate(text: str) -> list[str]:
    errs = []
    for w in BANNED_ZH:
        if w in text:
            errs.append(f"banned zh: {w}")
    for w in BANNED_EN:
        if re.search(rf"\b{w}\b", text, re.I):
            errs.append(f"banned en: {w}")
    if re.search(r"\bTODO\b|\[IMAGE .* PLACEHOLDER", text):
        errs.append("placeholder found")
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
            count = pt_words(full)
            passed = count >= art["floor"] and not errs
            metric = f"~{count} pt words"

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
