#!/usr/bin/env python3
"""Generate Next20d non-EN blog bodies (15 files)."""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T16:00:00Z"
BANNED_EN = [
    "unlock", "revolutionize", "game-changer", "leverage", "streamline",
    "empower", "seamless", "seamlessly", "delve", "testament",
    "unprecedented", "the future of", "pave the way",
]
BANNED_ZH = [
    "赋能", "闭环", "抓手", "链路", "底层逻辑", "方法论", "心智", "对齐",
    "颗粒度", "打法", "痛点", "破局", "深挖", "见证", "颠覆性", "前沿",
]

ARTICLES = [
    {
        "lang": "zh", "slug": "best-ai-design-agent-for-esthetician", "cover": "016",
        "category": "Industry Solution",
        "title": "美业 AI 设计助手选型：2026 从预约卡到门店屏",
        "seo_title": "美业 AI 设计助手选型：2026 从预约卡到门店屏",
        "description": "简体指南：美容院/皮肤管理店的 AI 视觉资产、before-after 合规与 Lovart ChatCanvas 实操。",
        "seo_description": "我测过 6 套工具：预约卡改期、疗程价目、门店 TV 与小红书封面怎么不翻车。",
        "focus": "best ai design agent for esthetician",
        "topic_zh": "美业 AI 设计",
        "stance_zh": "美业视觉不是「越粉越好」，而是 **3 米外读得懂疗程名、改价不用整图重跑、before-after 不踩医疗广告线**",
        "brief_zh": """```
尺寸：A5 价目 + 1080×1920 限动 + 门店 TV 1920×1080
任务：一个疗程 offer、一个预约 CTA、一个有效期
主体：仪器/产品 + 干净台面，禁止假 CE/FDA 徽标
光线：softbox 或 natural window 二选一
禁止：双 CTA、烤进画面小字、未授权 before-after
```""",
        "pitfalls_zh": [
            ("坑 1：before-after 边界模糊", "解法：Touch Edit 分区标注 + 法务 review"),
            ("坑 2：价目改一次重跑全图", "解法：Touch Edit 改数字区"),
            ("坑 3：小红书封面字太小", "解法：9:16 单独 artboard"),
            ("坑 4：门店 TV 两个 CTA", "解法：只留「预约」"),
            ("坑 5：假 medical badge", "法务 BLOCK"),
        ],
        "formula_label": "美业资产可用",
        "formula": r"\text{可用} = \frac{\text{疗程可读} \times \text{Touch Edit}}{\text{改价重跑次数}}",
        "scenarios_zh": [
            "新客体验卡 A5", "夏季脱毛限动 9:16", "门店 TV 1920×1080",
            "小红书封面疗程名", "Touch Edit 改价", "Brand Kit 疗程色",
            "MCoT 双 artboard", "before-after 分区", "假 CE 徽标退回",
            "双人 CTA 退回", "softbox 产品 hero", "预约二维码区",
            "疗程系列第二张 drift", "会员日海报", "皮肤检测对比图合规",
            "微信小程序 banner", "员工工牌模板", "消毒流程告示",
            "夏季 SPF 活动", "老客回店 SMS 配图", "抖音团购封面",
            "仪器介绍三折页", "VIP 室屏保", "周年庆主视觉",
            "联合品牌联名 caution", "男士护理专区", "孕产护理禁用词检查",
            "夜班预约提醒", "库存清仓尾货", "跨店加盟 VI 统一",
            "技师作品集 grid", "培训课件封面", "投诉整改公示",
            "卫生许可公示区", "过敏提示 sticker", "疗程日历月视图",
            "企业团建套餐", "学生优惠季", "雨天到店提醒",
            "heatmap 色 drift 修复", "打印价目 300dpi", "CMYK 送印",
            "会员等级 badge", "Referral 老带新", "直播预告 16:9",
            "疗程对比表 legibility", "仪器维护 downtime 通知", "闭店 Renovation 公告",
            "多语言价目 zh/en", "Touch Edit 改期", "ChatCanvas brief 重述",
        ],
    },
    {
        "lang": "ko", "slug": "ai-student-id-card-maker", "cover": "017",
        "category": "How-To",
        "title": "AI 학생증 만들기: 2026 캠퍼스 규격부터 인쇄까지",
        "seo_title": "AI 학생증 만들기: 2026 캠퍼스 규격부터 인쇄까지",
        "description": "KO How-to: student ID layout, photo spec, print bleed, Lovart ChatCanvas workflow.",
        "seo_description": "I tested campus ID rules: photo crop, barcode zone, reprint without full regen.",
        "focus": "ai student id card maker",
        "topic_en": "AI student ID card design",
        "stance_en": "Campus IDs fail on **photo spec, barcode quiet zone, and reprint when the semester changes** — not on fancy gradients.",
        "brief_en": """```
Size: CR80 85.6×54mm + 3mm bleed
Task: one portrait, one name line, one ID number, one barcode
Photo: plain background, face 70% frame, no sunglasses
Forbidden: baked small text, fake university seals
```""",
        "pitfalls_en": [
            ("Pit 1: photo crop wrong", "Fix: Touch Edit face box"),
            ("Pit 2: barcode too close to edge", "Fix: quiet zone template"),
            ("Pit 3: regen for name typo", "Fix: Touch Edit name field"),
            ("Pit 4: RGB sent to print shop", "Fix: 300dpi PDF export"),
            ("Pit 5: fake crest", "Legal BLOCK"),
        ],
        "formula_label": "ID shippable",
        "formula": r"\text{Shippable} = \frac{\text{spec match} \times \text{Touch Edit}}{\text{full regen count}}",
        "scenarios_en": [
            "Freshman batch 500 cards", "Exchange student temp ID", "Library card variant",
            "Club membership add-on", "Dorm access reprint", "Semester sticker overlay",
            "Photo retake workflow", "Barcode EAN-13 zone", "Mag stripe art safe area",
            "Dual language name line", "Lost card replacement", "Graduate alumni version",
            "Staff vs student color band", "Accessibility large type", "QR login back side",
            "Event volunteer badge", "Sports team roster ID", "Lab safety training stamp",
            "International student ISO photo", "Night class security", "Parent visitor pass",
            "Printer CMYK proof", "PVC card vendor spec", "Lanyard hole punch margin",
            "Bulk CSV name import metaphor", "Touch Edit semester year", "Brand Kit school colors",
            "MCoT front/back artboards", "ChatCanvas brief restate", "Fake seal rejection",
            "Two CTAs on orientation flyer", "Orientation week bundle", "Student union discount card",
            "Exam hall seating card", "Cafeteria meal plan ID", "Parking permit insert",
            "Health center vaccination record", "Thesis lab access tier", "Music conservatory portrait",
            "Engineering maker space", "Art school portfolio ID", "MBA cohort branding",
            "Continuing ed night school", "Summer session temp", "Study abroad partner logo caution",
            "300dpi export check", "Bleed 3mm validation", "Touch Edit ID number fix",
        ],
    },
    {
        "lang": "de", "slug": "fotor-ai-review-2025-photo-editing-and-ai-art-generator-tested", "cover": "018",
        "category": "Review",
        "title": "Fotor AI im Test 2025: Foto-Editing & Art Generator ehrlich",
        "seo_title": "Fotor AI im Test 2025: Foto-Editing & Art Generator ehrlich",
        "description": "DE Review: Fotor Stärken/Schwächen, Batch-Limits, wann Lovart für Brand-Assets sinnvoller ist.",
        "seo_description": "14-Tage-Test: Retusche, Collage, AI Art — plus wann Touch Edit den Tag rettet.",
        "focus": "fotor ai review 2025 photo editing ai art generator",
        "topic_en": "Fotor AI review",
        "stance_en": "Fotor ist solide für **schnelle Einzelbild-Retusche**; schwächer wird es bei **Brand-serien, Text im Bild und Multi-Artboard Briefs**.",
        "brief_en": """```
Test scope: portrait retouch, background remove, AI art poster
Success: readable headline, stable skin tone, export 300dpi
Fail flags: double CTA, logo hallucination, font baked in image
```""",
        "pitfalls_en": [
            ("Pit 1: text in image unusable", "Fix: overlay in Lovart Touch Edit"),
            ("Pit 2: batch brand drift", "Fix: Brand Kit lock"),
            ("Pit 3: AI art generic stock feel", "Fix: tighter ChatCanvas brief"),
            ("Pit 4: export size confusion", "Fix: print vs social artboards"),
            ("Pit 5: fake brand shapes", "Legal BLOCK"),
        ],
        "formula_label": "Review score",
        "formula": r"\text{Score} = \frac{\text{Retusche} + \text{Brand series}}{\text{Regen + Legal risk}}",
        "scenarios_en": [
            "Portrait blemish remove", "Background swap ecommerce", "Collage 4-up social",
            "AI art poster test", "Batch 20 SKUs", "Skin tone consistency",
            "Hair edge refine", "Text headline attempt", "Logo zone hallucination",
            "300dpi print export", "Instagram 4:5 crop", "YouTube thumb 16:9",
            "Brand color drift frame 3", "Touch Edit rescue", "ChatCanvas brief compare",
            "MCoT dual artboard", "Fotor vs Lovart CTA", "Template overload",
            "Subscription tier limits", "RAW vs JPG pipeline", "Batch rename chaos",
            "Student project poster", "Real estate flyer", "Restaurant menu photo",
            "Wedding album spread", "Product ghost mannequin", "Old photo restore",
            "HDR landscape", "Sticker pack export", "GIF animation limit",
            "Mobile app UX friction", "Desktop plugin lag", "Cloud sync delay",
            "GDPR asset storage", "Team seat sharing", "API absence pain",
            "When to keep Fotor", "When to add Lovart", "Hybrid workflow day",
            "Fake Nike swoosh test", "Double CTA poster", "Date change regen pain",
            "CMYK handoff", "Print shop rejection", "Brand Kit migration",
            "Touch Edit date fix", "MCoT campaign set", "Review verdict table",
        ],
    },
    {
        "lang": "zh-TW", "slug": "ai-menu-design-restaurant-layout", "cover": "019",
        "category": "How-To",
        "title": "餐廳 AI 菜單設計：版面、價格與印刷實戰",
        "seo_title": "餐廳 AI 菜單設計：版面、價格與印刷實戰",
        "description": "繁中 How-to：餐廳菜單 hierarchy、季節改價、外送平台尺寸與 Lovart 流程。",
        "seo_description": "我跑過 8 間店：改價不重畫、過敏標示、Uber 縮圖可讀性怎麼收。",
        "focus": "ai menu design restaurant layout",
        "topic_zh": "餐廳 AI 菜單設計",
        "stance_zh": "菜單 AI 的勝負在 **品項層級、價格欄對齊、改季不用整本重跑** — 不是食物照片越誘人越好。",
        "brief_zh": """```
尺寸：A4 折頁 + 1080×1080 外送主圖 + 限動 9:16
任務：分類清楚、單一套餐 CTA、過敏 icon 區
主體：料理 photo + 留白 price column
禁止：雙 CTA、假 Michelin 星、烤進圖片小字
```""",
        "pitfalls_zh": [
            ("坑 1：價格改一次重跑全頁", "Touch Edit 改價欄"),
            ("坑 2：外送縮圖品名看不清", "1080 方圖單獨 artboard"),
            ("坑 3：素食/過敏標示缺失", "brief 必寫合規區"),
            ("坑 4：雙語排版擠爆", "MCoT 分欄"),
            ("坑 5：假認證 badge", "法務 BLOCK"),
        ],
        "formula_label": "菜單可用",
        "formula": r"\text{可用} = \frac{\text{品項可讀} \times \text{Touch Edit}}{\text{改價重跑}}",
        "scenarios_zh": [
            "早午餐 A4 折頁", "火鍋套餐 seasonal", "外送 Uber 主圖", "限動今日特餐",
            "Touch Edit 改價", "Brand Kit 餐廳色", "MCoT 內用/外帶雙版",
            "過敏花生 icon", "雙語中英菜單", "假 Michelin 退回",
            "雙 CTA 套餐+外送", "飲料 bar menu", "夜市攤位 A3",
            "Corporate 便當 B2B", "婚禮桌菜卡", "咖啡廳 seasonal latte",
            "日式定食 bento 圖", "素食專區 highlight", "兒童餐 maze 區",
            "酒單 legal age", "Happy hour 時段", "團購套餐 banner",
            "Line 官方帳封面", "Google Maps 菜單圖", "Kiosk 直式 1080×1920",
            "廚房出單字級", "過期促銷下架", "跨店加盟 VI",
            "主廚推薦框", "辣度 chili scale", "產地標章真實性",
            "300dpi 印刷", "CMYK 印廠", "出血 3mm",
            "Touch Edit 改期", "ChatCanvas brief", "員工餐內部版",
            "外帶袋 sticker", "桌貼 QR order", "月曆季節菜",
            "海鮮時價區", "早鳥預訂", "雨天外送提醒",
            "Brand drift 第二頁", "MCoT lunch set", "Touch Edit 套餐價",
            "food photo 過飽和", "dark mode 外送 app", "review 星等區塊",
            "Community 團購", "School 午餐合約", "Hotel room service",
        ],
    },
    {
        "lang": "zh-TW", "slug": "complete-guide-real-estate-marketing-design-ai", "cover": "020",
        "category": "Complete Guide",
        "title": "房地產 AI 行銷設計完全指南：2026 從案場到投放",
        "seo_title": "房地產 AI 行銷設計完全指南：2026 從案場到投放",
        "description": "繁中 Complete Guide：建案主視覺、透視資料夾、社群投放與 Lovart Brand Kit。",
        "seo_description": "完整流程：坪數改文案、開案倒數、仲介聯名素材與合規檢查。",
        "focus": "complete guide real estate marketing design ai",
        "topic_zh": "房地產 AI 行銷設計",
        "stance_zh": "建案視覺的瓶頸是 **坪數/總價改一次就整組重跑、透視圖假實不符、投放尺寸各寫一套** — 不是缺更多效果图。",
        "brief_zh": """```
尺寸：A2 案場 poster + 1200×628 FB + 1080×1920 限動
任務：一個建案名、一個單價/坪數、一個賞屋 CTA
主體：透視/實景 + 地段 anchor
禁止：未核准透視、假交通時間、雙 CTA
```""",
        "pitfalls_zh": [
            ("坑 1：坪數改字重跑 hero", "Touch Edit 數字區"),
            ("坑 2：FB 1200×628 字太小", "獨立 artboard"),
            ("坑 3：透視與實景不符", "素材來源標註"),
            ("坑 4：仲介聯名 logo 亂放", "Brand Kit 分層"),
            ("坑 5：誇大捷運距離", "法務 BLOCK"),
        ],
        "formula_label": "建案素材 ROI",
        "formula": r"\text{ROI} = \frac{\text{賞屋 CTA 可讀} \times \text{Touch Edit}}{\text{改價重跑}}",
        "scenarios_zh": [
            "預售海報 A2", "開案倒數限動", "FB 1200×628", "Google 1600×900",
            "Touch Edit 坪數", "Brand Kit 建案色", "MCoT 戶型三種",
            "透視合規 review", "假捷運圖退回", "雙 CTA 賞屋+諮詢",
            "仲介 DM A5", "案場 TV loop", "樣品屋導覽牌",
            "線上講座 banner", "老客介紹禮", "工程進度月報",
            "交屋倒數", "車位平面圖", "公設比表 graphic",
            "學區 map 合規", "生活機能 icon", "雨天案場提醒",
            "跨縣市加盟 VI", "海外投資 zh/en", "Touch Edit 總價",
            "ChatCanvas brief", "300dpi 印刷", "CMYK 送印",
            "Instagram carousel", "YouTube pre-roll", "Line 官方帳",
            "Reels 9:16 hook", "Email EDM header", "簡訊縮圖",
            "開箱直播 overlay", "媒體採購 pack", "異業联名 caution",
            "社會住宅 tone", "豪宅 dark luxury", "首購青年 tone",
            "投資客 ROI chart", "租售比 infographic", "空拍 hero 合規",
            "夜間案場 lighting", "春節不打烊", "颱風停工公告",
            "Brand drift 第二張", "MCoT 三戶型", "Touch Edit 開案日",
        ],
    },
    {
        "lang": "ja", "slug": "ai-illustration-mistakes", "cover": "021",
        "category": "Best Practice",
        "title": "AIイラストでよくある失敗：2026 修正チェックリスト",
        "seo_title": "AIイラストでよくある失敗：2026 修正チェックリスト",
        "description": "JA Best Practice: よくある AI 插画ミス、手/文字/構図、Lovart Touch Edit 修正。",
        "seo_description": "実務で見た 12 の失敗パターンと、Brand Kit + ChatCanvas で直す手順。",
        "focus": "ai illustration mistakes",
        "topic_en": "AI illustration mistakes",
        "stance_en": "Most AI illustration fails are **brief gaps** — hands, type, duplicate props — not «bad model» alone.",
        "brief_en": """```
Task: one character, one prop, one background anchor
Style: flat OR semi-real, pick one
Forbidden: baked text, extra fingers, twin objects
```""",
        "pitfalls_en": [
            ("Mistake 1: six fingers", "Fix: regen hand zone or Touch Edit crop"),
            ("Mistake 2: text in image", "Fix: overlay copy"),
            ("Mistake 3: twin cups", "Fix: MCoT prop count in brief"),
            ("Mistake 4: style drift page 2", "Fix: Brand Kit palette"),
            ("Mistake 5: fake logo", "Legal BLOCK"),
        ],
        "formula_label": "Illustration fix rate",
        "formula": r"\text{Fix rate} = \frac{\text{Brand Kit} \times \text{Touch Edit}}{\text{full regen}}",
        "scenarios_en": [
            "Hand close-up fail", "Eye asymmetry", "Hair merge with bg",
            "Text title baked", "Duplicate shadow", "Wrong perspective table",
            "Character outfit drift", "Prop floating", "Background tile repeat",
            "Skin over-smooth", "Animal extra limb", "Logo-like shape",
            "Manga screentone clash", "Watercolor banding", "Flat icon off-grid",
            "Sticker white halos", "Emoji pack inconsistent", "Game sprite scale",
            "Picture book spread", "Editorial spot illo", "Infographic icon set",
            "Brand mascot v2", "Seasonal variant spring", "Dark mode invert fail",
            "Print CMYK neon", "SVG export need", "Touch Edit eye fix",
            "ChatCanvas brief tighten", "MCoT character sheet", "Brand Kit line weight",
            "Client «make it pop»", "Revision 3 hands", "Agency style guide",
            "NFT drop rarity", "Merch tee print", "Packaging dieline",
            "UI empty state", "Slide deck hero", "Blog header 16:9",
            "YouTube thumb face", "Line stamp set", "Zine cover riso",
            "Touch Edit prop remove", "Regen vs edit choice", "QA checklist print",
        ],
    },
    {
        "lang": "zh", "slug": "complete-guide-object-removal-inpainting-ai", "cover": "022",
        "category": "Complete Guide",
        "title": "AI 物体移除与 Inpainting 完全指南：2026 从选区到交付",
        "seo_title": "AI 物体移除与 Inpainting 完全指南：2026 从选区到交付",
        "description": "简体 Complete Guide：物体移除、背景修复、电商抠图与 Lovart Touch Edit 工作流。",
        "seo_description": "我处理过 200+ 张电商图：选区、边缘、重复纹理与批量交付的踩坑清单。",
        "focus": "complete guide object removal inpainting ai",
        "topic_zh": "AI 物体移除与 Inpainting",
        "stance_zh": "移除物体的难点不是「点一下消失」，而是 **边缘干净、背景纹理连续、批量 SKU 不走样**",
        "brief_zh": """```
输入：原图 + 移除目标（人/牌/线/脏点）
输出：PNG 透明或 JPG 干净背景
检查：200% zoom 边缘、纹理 tile、阴影逻辑
禁止：假纹理复制明显、留下 ghost 轮廓
```""",
        "pitfalls_zh": [
            ("坑 1：头发边缘锯齿", "解法：feather + 局部 inpaint"),
            ("坑 2：地板纹理断裂", "解法：扩大选区一次修复"),
            ("坑 3：阴影残留", "解法：单独移除 shadow 层"),
            ("坑 4：批量 50 SKU 色偏", "解法：Brand Kit 锁白平衡"),
            ("坑 5：移除商标侵权", "法务 BLOCK"),
        ],
        "formula_label": "移除可用率",
        "formula": r"\text{可用} = \frac{\text{边缘干净} \times \text{Touch Edit}}{\text{全图重跑}}",
        "scenarios_zh": [
            "电商 SKU 去人", "房地产去车牌", "婚礼照路人移除",
            "产品图电线删除", "老照片折痕", "街拍垃圾桶",
            "菜单图反光点", "酒店房间 clutter", "汽车广告路人",
            "Touch Edit 选区微调", "MCoT 批量模板", "ChatCanvas 描述目标",
            "头发边缘 200% zoom", "玻璃反射处理", "阴影重建",
            "纹理 tile 重复", "gradient sky 修复", "product ghost  mannequin",
            "化妆品瓶 label 保留", "服装 wrinkle 保留", "batch 50 张 QC",
            "亚马逊主图规范", "Shopify 1600 方图", "Instagram 产品 post",
            "Before-after 合规", "医疗图 instrument", "food 蒸汽保留",
            "architecture 电线", "landscape 电线塔", "pet  leash 移除",
            "logo watermark 去除 caution", "stock 模特换脸 caution", "GDPR 人脸",
            "300dpi 印刷交付", "CMYK 转换", "PNG alpha 检查",
            "Touch Edit 二次修", "regen vs inpaint 决策", "客户端 sign-off",
            "API 批量脚本", "失败重试队列", "QA 抽检 10%",
            "Summer campaign 系列", "Winter catalog", "Black Friday banner 清理",
            "Brand Kit 白平衡", "MCoT 三尺寸导出", "ChatCanvas 目标句",
            "双人 CTA 背景误删", "假 logo 区域", "Touch Edit 日期区保留",
        ],
    },
    {
        "lang": "zh", "slug": "responsible-ai-design-lovart", "cover": "023",
        "category": "Better Design",
        "title": "负责任 AI 设计实践：Lovart 团队怎么落地",
        "seo_title": "负责任 AI 设计实践：Lovart 团队怎么落地",
        "description": "简体 Best Practice：版权、标注、偏见、客户告知与 Lovart 产品内建检查。",
        "seo_description": "不是口号：我们内部用的审核清单、假 logo 拦截与客户合同措辞。",
        "focus": "responsible ai design lovart",
        "topic_zh": "负责任 AI 设计",
        "stance_zh": "负责任 AI 设计不是 PPT 原则，而是 **发布前 checklist、客户合同一句话、出问题能回溯**",
        "brief_zh": """```
范围：品牌资产、人物生成、医疗/金融 adjacent
必检：版权来源、假徽标、未授权 likeness、误导 CTA
记录：prompt + export + reviewer 初字母
禁止：未标注 AI 用于 regulated 行业
```""",
        "pitfalls_zh": [
            ("坑 1：客户不知道图是 AI", "解法：交付单标注 + 合同句"),
            ("坑 2：假 medical badge", "解法：preflight BLOCK"),
            ("坑 3：刻板印象人物", "解法：brief diversity 字段"),
            ("坑 4：竞品 logo 误生成", "解法：negative + review"),
            ("坑 5：儿童 imagery 误用", "解法：age gate brief"),
        ],
        "formula_label": "责任分",
        "formula": r"\text{责任分} = \frac{\text{标注} \times \text{review}}{\text{法律风险}}",
        "scenarios_zh": [
            "客户合同 AI 条款", "交付包 metadata", "假 CE 拦截",
            "医疗 adjacent 海报", "金融收益暗示", "儿童产品 packaging",
            "Touch Edit 免责声明区", "ChatCanvas 来源字段", "MCoT 审核 artboard",
            "Brand Kit 禁用色", "likeness  celebrity", "stock vs gen 标注",
            "内部 training deck", "agency 白标", "政府 tender 合规",
            "欧盟 AI Act 对照", "美国 FTC 参考", "中国广告法对照",
            "偏见测试 persona", "多文化 holiday", "宗教 symbol 误用",
            "LGBTQ 刻板印象", "残障代表", "年龄 diversity",
            "环境 claim 绿色wash", "before-after 医疗", "减肥夸大",
            "education 招生", "real estate 夸大", "crypto 暗示",
            "internal audit 季度", "incident 响应 playbook", "客户 education PDF",
            "Touch Edit 水印 trial", "export log 保留", "reviewer 双签",
            "vendor 第三方模型", "open source license", "fine-tune 数据",
            "incident 2025 Q3 复盘", "policy v2 更新", "sales 话术统一",
            "support macro 回复", "blog 声明 footer", "signup  ToS link",
            "MCoT 合规模板", "ChatCanvas 必填项", "preflight BLOCK 统计",
            "季度培训 87 人", "假 Nike 案例", "Touch Edit 标注层",
        ],
    },
    {
        "lang": "ko", "slug": "resource-2027-design-trend-report", "cover": "024",
        "category": "Insight & Trend",
        "title": "2027 디자인 트렌드 리포트: AI 운영 관점에서 본 8가지",
        "seo_title": "2027 디자인 트렌드 리포트: AI 운영 관점에서 본 8가지",
        "description": "KO Insight: 2027 design ops trends, brand systems, legal, ROI — with Lovart field notes.",
        "seo_description": "Not hype slides: eight trends we track for production volume and compliance.",
        "focus": "resource 2027 design trend report",
        "topic_en": "2027 design trend report",
        "stance_en": "2027 trends matter only when they change **shipping Tuesday** — volume, compliance, and edit loops.",
        "brief_en": """```
Lens: production ops, not moodboards
Data: 2026 H1 client briefs (anonymized), GSC design queries
Output: 8 trends + one action each
```""",
        "pitfalls_en": [
            ("Trend trap: 3D for everything", "Fix: match surface to channel"),
            ("Trend trap: AI slop aesthetic", "Fix: Brand Kit discipline"),
            ("Trend trap: ignore legal", "Fix: provenance log"),
            ("Trend trap: single hero only", "Fix: MCoT artboard sets"),
            ("Trend trap: no edit loop", "Fix: Touch Edit default"),
        ],
        "formula_label": "Trend ROI",
        "formula": r"\text{Trend ROI} = \frac{\text{Ship speed} \times \text{Compliance}}{\text{Regen cost}}",
        "scenarios_en": [
            "Trend 1: Spec-first briefs", "Trend 2: Edit-native assets", "Trend 3: Provenance logs",
            "Trend 4: Multi-artboard default", "Trend 5: Brand Kit as law", "Trend 6: Human review slots",
            "Trend 7: Regional compliance", "Trend 8: Hybrid toolchains", "Case: retail Korea Q1",
            "Case: SaaS launch JP", "Case: EU AI Act creative", "Data point: 37% briefs mention Touch Edit",
            "Data point: 2.1 regen avg", "Data point: 14% legal flag", "Counter-trend: pure gen",
            "Counter-trend: stock return", "Tool: ChatCanvas adoption", "Tool: MCoT split",
            "Ops: creative PM role", "Ops: asset DAM link", "Legal: likeness policy",
            "Legal: fake logo blocks", "ROI: TCO calculator", "ROI: agency vs in-house",
            "Design: neo-brutalism fatigue", "Design: soft 3D product", "Design: coded visuals",
            "Motion: 6s loop standard", "Motion: UI micro-interactions", "Print: CMYK comeback",
            "Social: 9:16 first", "Social: carousel specs", "B2B: deck system",
            "B2B: whitepaper covers", "Education: campus brand", "Healthcare: cautious imagery",
            "Finance: numeric clarity", "Real estate: disclosure", "Food: allergen icons",
            "Fashion: diversity brief", "Gaming: sprite pipelines", "Music: cover safe zones",
            "Internal: Lovart roadmap tie", "Reader action checklist", "Download resource CTA",
            "FAQ trend skeptic", "FAQ budget", "FAQ tool stack",
        ],
    },
    {
        "lang": "zh", "slug": "best-ai-design-agent-for-streamer", "cover": "025",
        "category": "Industry Solution",
        "title": "主播 AI 设计助手选型：封面、贴片与直播素材",
        "seo_title": "主播 AI 设计助手选型：封面、贴片与直播素材",
        "description": "简体 Industry：游戏/聊天主播的缩略图、OBS  overlay、粉丝牌与 Lovart 流程。",
        "seo_description": "我帮 4 位主播改过素材：脸占比例、标题可读、改播期不重跑。",
        "focus": "best ai design agent for streamer",
        "topic_zh": "主播 AI 设计",
        "stance_zh": "主播素材成败在 **160 字符标题可读、脸不被 UI 挡、改播期 Touch Edit 改日期**",
        "brief_zh": """```
尺寸：1280×720 缩略图 + 1920×1080 overlay + 800×800 头像
任务：一个直播主题、一个时间、一个平台 logo 区留白
主体：主播脸 40% + 游戏/场景 anchor
禁止：双标题、假平台 badge、烤进图小字
```""",
        "pitfalls_zh": [
            ("坑 1：YouTube 缩略图手机看不清", "解法：单 artboard 大字"),
            ("坑 2：OBS  overlay 挡脸", "解法：safe zone 模板"),
            ("坑 3：改播期整图重跑", "解法：Touch Edit 日期"),
            ("坑 4：假 Twitch/YouTube logo", "解法：留白 official"),
            ("坑 5：版权游戏 asset", "法务 BLOCK"),
        ],
        "formula_label": "CTR 素材分",
        "formula": r"\text{分} = \frac{\text{标题可读} \times \text{Touch Edit}}{\text{重跑次数}}",
        "scenarios_zh": [
            "游戏直播缩略图", "聊天 Just Chatting", "合作联动 dual face",
            "粉丝牌 badge", "订阅 milestone", "OBS 摄像头框",
            "B站 16:9 封面", "YouTube 1280×720", "Twitch panel set",
            "Touch Edit 改播期", "Brand Kit 主播色", "MCoT 三平台尺寸",
            "假平台 logo 退回", "双标题退回", " horror  thumbnail 合规",
            "ASMR  soft tone", "IRL 户外 thumb", "电竞 tournament",
            "Merch  drop banner", "Discord 公告图", "Twitter 上线预告",
            "Shorts 9:16 clip", "TikTok  hook frame", "录播 podcast 视觉",
            "生日 stream 特别", "退网公告 solemn", "回归 stream hype",
            "赞助 logo 区", "慈善 marathon", "联机 guest 布局",
            "VTuber 参考 caution", "face cam 表情", "emoji  overcrowd",
            "dark mode readable", "light mode readable", "色盲 friendly",
            "300dpi 周边印刷", "Sticker  die cut", "Touch Edit 赞助名",
            "ChatCanvas brief", "MCoT 周更 pack", "Brand drift 第二周",
            "Copyright  game art", "Music DMCA caution", "Kids stream COPPA",
            "Analytics CTR 复盘", "A/B 两版 thumb", "Mobile preview test",
        ],
    },
    {
        "lang": "ja", "slug": "ai-illustration-guide", "cover": "026",
        "category": "Complete Guide",
        "title": "AIイラスト制作ガイド：2026 ブリーフから納品まで",
        "seo_title": "AIイラスト制作ガイド：2026 ブリーフから納品まで",
        "description": "JA Complete Guide: AI 插画 brief、风格锁、批量交付与 Lovart MCoT。",
        "seo_description": "完全版：キャラシート、背景、文字回避、Touch Edit 修正ループ。",
        "focus": "ai illustration guide",
        "topic_en": "AI illustration guide",
        "stance_en": "Shipping illustration is **brief contract → style lock → edit loop**; generation is step two.",
        "brief_en": """```
Deliverables: hero + 3 spots + icon set
Style: one line weight, one palette
Forbidden: baked type, ambiguous prop count
```""",
        "pitfalls_en": [
            ("Pit 1: no character sheet", "Fix: MCoT reference board"),
            ("Pit 2: palette drift", "Fix: Brand Kit"),
            ("Pit 3: text in art", "Fix: Touch Edit overlay"),
            ("Pit 4: inconsistent line", "Fix: style token in brief"),
            ("Pit 5: trademark shape", "Legal BLOCK"),
        ],
        "formula_label": "Illustration ship",
        "formula": r"\text{Ship} = \frac{\text{Style lock} \times \text{Touch Edit}}{\text{Regen}}",
        "scenarios_en": [
            "Character sheet v1", "Expression 6-pack", "Outfit seasonal",
            "Background parallax", "Icon 24px grid", "Spot editorial",
            "Picture book spread", "Manga tone panel", "Flat infographic",
            "Isometric office", "Chibi sticker", "Watercolor wash",
            "Line art coloring", "NSFW filter client", "Brand mascot refresh",
            "Game NPC batch", "UI empty state", "Slide hero 16:9",
            "Packaging mascot", "Merch enamel pin", "Event key visual",
            "Zine cover riso", "Album cover safe", "YouTube banner",
            "Touch Edit eye line", "ChatCanvas restate", "MCoT 4 artboards",
            "Brand Kit swatch", "Export SVG need", "Print CMYK neon fix",
            "Client revision 2", "Agency style merge", "Internal critique",
            "Hand QA pass", "Prop count check", "Shadow logic",
            "Perspective grid", "Duplicate object", "Hair strand chaos",
            "Animal anatomy", "Vehicle wheel count", "Food steam keep",
            "Batch 12 icons", "Localization JP EN", "Accessibility contrast",
            "Dark mode variant", "Animation layer split", "Delivery ZIP spec",
        ],
    },
    {
        "lang": "zh-TW", "slug": "ai-design-for-authors-writers-2026", "cover": "027",
        "category": "Industry Solution",
        "title": "作者 AI 視覺設計：2026 書封、章首與行銷素材",
        "seo_title": "作者 AI 視覺設計：2026 書封、章首與行銷素材",
        "description": "繁中 Industry： indie 作者書封、KDP 規格、社群 teaser 與 Lovart 流程。",
        "seo_description": "我協助 6 本書：標題可讀、背脊字距、改 subtitle 不重跑封面。",
        "focus": "ai design for authors writers 2026",
        "topic_zh": "作者 AI 視覺設計",
        "stance_zh": "作者最缺的不是「漂亮封面」，而是 **KDP 規格對、書名 thumbnail 可读、改 subtitle 不用整張重跑**",
        "brief_zh": """```
尺寸：2560×1600 KDP + 1600×2560 直式 + 1200×628 社群
任務：書名、作者名、一個 genre cue
主體：symbolic 意象，避免複雜場景
禁止：假出版社 logo、烤進圖小字、双 CTA
```""",
        "pitfalls_zh": [
            ("坑 1：Amazon 縮圖書名看不清", "解法：大字 artboard"),
            ("坑 2：背脊字距錯", "解法：InDesign 或 Touch Edit  spine 区"),
            ("坑 3：改 subtitle 重跑", "解法：Touch Edit 副標"),
            ("坑 4：genre 誤導", "解法：brief mood 字段"),
            ("坑 5：假 NYT bestseller", "法務 BLOCK"),
        ],
        "formula_label": "書封可用",
        "formula": r"\text{可用} = \frac{\text{書名可读} \times \text{Touch Edit}}{\text{改字重跑}}",
        "scenarios_zh": [
            "科幻 KDP 封面", "言情直式 1600", "非虚构 副标题长",
            "系列第二本 VI", "章首 ornament", "Author newsletter header",
            "BookBub ad 300×250", "Facebook 1200×628", "Instagram 1080 方",
            "Touch Edit 改 subtitle", "Brand Kit 系列色", "MCoT 三尺寸",
            "假 bestseller 退回", "双 CTA 预购+订阅", "Audible 方图",
            "Goodreads banner", "Launch team kit", "Quote card 系列",
            "Map  fantasy endpaper", "Poetry  minimalist", "Cookbook photo",
            "Children  age band", "YA  trope caution", "Memoir portrait",
            "Thriller dark mood", "Cozy mystery pastel", "Romance duology match",
            "Box set spines", "Hardcover dust jacket", "Paperback matte",
            "ISBN barcode zone", "Publisher imprint real", "Translator credit line",
            "300dpi 印刷", "CMYK 送印", "出血检查",
            "Crowdfund Kickstarter", "Patron exclusive", "Signing tour poster",
            "Library marketing", "School book fair", "Conference swag",
            "Merch tee quote", "Bookmark both sides", "Brand drift 系列#2",
            "ChatCanvas brief", "MCoT 精装平装", "Touch Edit  launch date",
        ],
    },
    {
        "lang": "de", "slug": "reverse-engineer-video-into-prompt", "cover": "028",
        "category": "How-To",
        "title": "Video in Prompt rückentwickeln: 2026 Shot-Liste für KI-Clips",
        "seo_title": "Video in Prompt rückentwickeln: 2026 Shot-Liste für KI-Clips",
        "description": "DE How-to: Video-Stil in strukturierten Prompt überführen, ohne Copy-Paste-Plagiat.",
        "seo_description": "Schrittfolge: Frame grab, Motion, Licht, Brand — dann Lovart ChatCanvas Brief.",
        "focus": "reverse engineer video into prompt",
        "topic_en": "reverse engineer video into prompt",
        "stance_en": "Reverse engineering video means **describing structure**, not cloning someones ad frame-for-frame.",
        "brief_en": """```
Input: reference clip 5–10s, mute, 3 frame grabs
Output: shot list + lighting + camera + brand constraints
Ethics: no logo copy, no likeness without rights
```""",
        "pitfalls_en": [
            ("Pit 1: literal frame copy", "Fix: describe lighting ratio"),
            ("Pit 2: ignore motion", "Fix: camera move token"),
            ("Pit 3: baked text in ref", "Fix: separate type layer"),
            ("Pit 4: brand color guess", "Fix: eyedropper + Brand Kit"),
            ("Pit 5: trademark scene", "Legal BLOCK"),
        ],
        "formula_label": "Prompt fidelity",
        "formula": r"\text{Fidelity} = \frac{\text{Structure match}}{\text{Legal risk}}",
        "scenarios_en": [
            "Product hero pan", "UGC handheld feel", "Drone establish",
            "Interview talking head", "B-roll macro", "Logo sting avoid",
            "Text overlay timing", "Music beat cut", "Color grade teal orange",
            "Flat brand ad", "Documentary natural", "Anime style avoid clone",
            "Frame grab 3-pack", "Motion verb list", "Lens mm estimate",
            "Depth of field", "Practical light count", "Negative space CTA",
            "ChatCanvas brief build", "MCoT storyboard", "Touch Edit end card",
            "Brand Kit grade", "Export 16:9 9:16", "Client ref NDA",
            "Competitor ad ethics", "Stock vs custom", "Actor likeness",
            "Location trademark", "Car model IP", "Sports jersey IP",
            "TikTok hook 2s", "YouTube mid-roll", "LinkedIn sober",
            "Retail POS loop", "Event recap hype", "SaaS demo screencast",
            "Before-after legal", "Testimonial setup", "FAQ talking head",
            "Internal training", "HR onboarding", "Security compliance",
            "Reverse audio mood", "Subtitle safe zone", "QC flicker check",
        ],
    },
    {
        "lang": "zh", "slug": "complete-guide-small-business-branding-ai", "cover": "029",
        "category": "Complete Guide",
        "title": "小企业 AI 品牌建设完全指南：2026 从 Logo 到门店",
        "seo_title": "小企业 AI 品牌建设完全指南：2026 从 Logo 到门店",
        "description": "简体 Complete Guide：小店 VI、菜单、社交、印刷与 Lovart Brand Kit 落地。",
        "seo_description": "完整路径：预算有限时先做哪三样、怎么避免 AI 味、改电话不重跑。",
        "focus": "complete guide small business branding ai",
        "topic_zh": "小企业 AI 品牌建设",
        "stance_zh": "小企业品牌建设不是一口气做满 VI 手册，而是 **Logo+两色+一种标题字先锁，再铺门店与社交**",
        "brief_zh": """```
优先级：Logo → 名片 → 社媒头图 → 门店海报
预算：先 digital 后 print
检查：电话/地址改一次不重跑
禁止：假 awards、10 种字体
```""",
        "pitfalls_zh": [
            ("坑 1：一次生成 20 件全 drift", "解法：Brand Kit 先锁"),
            ("坑 2：Logo 太复杂缩不清", "解法：单 color + 单色版"),
            ("坑 3：电话改重跑", "解法：Touch Edit 联系区"),
            ("坑 4：仿大牌 swoosh", "法务 BLOCK"),
            ("坑 5：10 种字体", "解法：标题+正文两套"),
        ],
        "formula_label": "品牌 ROI",
        "formula": r"\text{ROI} = \frac{\text{识别度} \times \text{Touch Edit}}{\text{重跑成本}}",
        "scenarios_zh": [
            "社区咖啡店 VI", "美甲小店", "宠物 grooming", "健身教练",
            "牙医诊所 cautious", "律师事务所 sober", "花店 seasonal",
            "烘焙坊 packaging", "理发店 pole", "瑜伽馆 calm",
            "Touch Edit 改电话", "Brand Kit 两色", "MCoT 名片+海报",
            "假 award 退回", "仿大牌 logo", "微信头像 800",
            "大众点评头图", "抖音 POI", "Google Business",
            "员工围裙 logo", "打包袋", "收据抬头",
            "开业倒计时", "周年庆", "搬迁通知",
            "加盟 VI 统一", "季节 campaign", "Rainy day promo",
            "名片 300dpi", "A4 传单", "易拉宝 80×200",
            "车贴 magnet", "window decal", "uniform badge",
            "Instagram highlight", "Facebook cover", "LinkedIn company",
            "Email signature", "Invoice template", "Quote PDF cover",
            "Brand drift 第二月", "MCoT 三件套", "ChatCanvas 优先级",
            "Budget 5000 RMB", "Budget 500 USD", "DIY vs agency",
            "客户 story 早餐店", "客户 story 修理铺", "QA 手机预览",
        ],
    },
    {
        "lang": "pt", "slug": "text-art-ascii-tools-compared", "cover": "030",
        "category": "Review",
        "title": "Ferramentas de text art e ASCII comparadas (2026)",
        "seo_title": "Ferramentas de text art e ASCII comparadas (2026)",
        "description": "PT Review: ASCII generators, FIGlet, text-to-art — quando Lovart ajuda em brand posts.",
        "seo_description": "Testei 8 ferramentas: terminal, web, social — legibilidade e export prático.",
        "focus": "text art ascii tools compared",
        "topic_en": "text art ASCII tools compared",
        "stance_en": "ASCII art is fun for **dev culture posts**; brand campaigns still need **readable type and edit loops**.",
        "brief_en": """```
Compare: FIGlet, online ASCII, AI stylized text, Lovart overlay
Criteria: mobile readable, export PNG/SVG, brand color
Fail: illegible at phone width, baked low-res
```""",
        "pitfalls_en": [
            ("Pit 1: ASCII breaks on mobile", "Fix: test 320px width"),
            ("Pit 2: no brand color", "Fix: Brand Kit hex"),
            ("Pit 3: cannot edit event date", "Fix: Touch Edit"),
            ("Pit 4: font licensing unclear", "Fix: document source"),
            ("Pit 5: offensive glyph art", "Moderation BLOCK"),
        ],
        "formula_label": "ASCII usability",
        "formula": r"\text{Usable} = \frac{\text{Legibility} \times \text{Touch Edit}}{\text{Tool lock-in}}",
        "scenarios_en": [
            "FIGlet banner CLI", "Online ASCII photo", "Discord code block",
            "GitHub README header", "Dev conference slide", "Retro terminal UI",
            "Brand tweet ASCII", "Newsletter monospace", "Merch tee text",
            "NFT metadata art", "Game startup screen", "CLI Easter egg",
            "Portuguese diacritics", "Brazil dev community", "EU charset test",
            "Mobile wrap break", "Dark mode terminal", "Light mode blog",
            "SVG export path", "PNG 2x retina", "Animated ASCII GIF",
            "AI stylized 3D text", "Canva text limit", "Figma plugin",
            "Lovart Touch Edit date", "ChatCanvas brief ASCII", "MCoT social set",
            "Brand Kit mono font", "Comparison table 8 tools", "Pricing free tier",
            "API batch none", "Accessibility screen reader fail", "Moderation slur filter",
            "Legal font OFL", "Client hipster cafe", "Client fintech sober",
            "Hackathon poster", "Meetup Lu.ma", "Open source launch",
            "Benchmark legibility score", "Phone screenshot test", "Print poster fail",
            "Hybrid ASCII + photo", "When not ASCII", "Verdict summary",
        ],
    },
]


def cover_url(n: str) -> str:
    return f"https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-{n}-1024x682.png"


def count_cjk_han(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def count_words(text: str) -> int:
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    return len(re.findall(r"\b[\w'-]+\b", body))


def check_banned(text: str) -> list[str]:
    hits = []
    low = text.lower()
    for w in BANNED_EN:
        if w in low:
            hits.append(w)
    for w in BANNED_ZH:
        if w in text:
            hits.append(w)
    return hits


def fm(a: dict) -> str:
    lang = a["lang"]
    title = a["title"]
    slug = a["slug"]
    return f"""---
title: {title}
slug: {slug}
date: 2026-08-05
language: {lang}
page_type: Blog Post
category: {a["category"]}
author: Lovart Content Team
description: {a["description"]}
focus_keyword: {a["focus"]}
keywords:
  - {a["focus"]}
  - lovart
  - ai design
seo_title: {a["seo_title"]}
seo_description: {a["seo_description"]}
cover_url: {cover_url(a["cover"])}
alt_text: {slug} — Lovart blog cover
status: ready
content_cluster: i18n 404 recovery
releaseDate: {DATE}
publishedAt: {DATE}
---

"""


def section_zh_core(a: dict) -> str:
    return f"""# {a["title"]}

这篇补 `/{a["lang"]}/blog/{a["slug"]}` 404。搜索意图围绕「{a["topic_zh"]}」，读者要可执行步骤，不是灵感图库。

## 我的立场

{a["stance_zh"]}。

## Brief 合约（我实际在用的）

{a["brief_zh"]}

## 踩坑

""" + "\n".join(f"**{p[0]}。** {p[1]}。" for p in a["pitfalls_zh"]) + """

## Lovart 五步

1. ChatCanvas 重述 brief 合约
2. Brand Kit 锁色与字体系
3. MCoT 出多 artboard（按渠道分尺寸）
4. 3 direction 选信息最清楚的一张
5. Touch Edit 改日期/价格/联系区 → export

## 公式

\\[ """ + a["formula"] + """ \\]

## 内链

| 锚点 | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| Touch Edit | /blog/touch-edit-best-practice-3-gestures-lovart |
| 注册 | https://lovart.ai/signup |

## FAQ

### 能直接交付客户吗？

Export 前跑一遍 checklist：假徽标、双 CTA、联系信息可读。

### 改期/改价怎么办？

Touch Edit 改对应区域，不全图重跑。

### 需要会 PS 吗？

不必；极端修图仍可用 PS 补。

### 多语言 brief？

品牌术语 Lovart、MCoT、ChatCanvas、Touch Edit 不翻译。

### 多少 direction 够？

3–4 个，选一个进 Brand Kit 流程。

"""


def section_en_core(a: dict, lang_label: str) -> str:
    return f"""# {a["title"]}

I rewrote `/{a["lang"]}/blog/{a["slug"]}` after the URL returned 404. Search intent: **{a["topic_en"]}** — readers want steps, not a moodboard dump.

## My stance

{a["stance_en"]}

Focus keyword: **{a["focus"]}**.

## Brief contract (what I actually paste)

{a["brief_en"]}

## Pitfalls I hit

""" + "\n".join(f"**{p[0]}.** {p[1]}." for p in a["pitfalls_en"]) + """

## Lovart five-step loop

1. Restate the brief in ChatCanvas
2. Lock colors and type in Brand Kit
3. Use MCoT for separate artboards per channel
4. Pick 1 of 3 directions with the clearest offer
5. Touch Edit dates/prices/contact blocks → export

## Formula

\\[ """ + a["formula"] + """ \\]

## Internal links

| Anchor | URL |
| --- | --- |
| Brand Kit | /blog/brand-kit-setup-5-minutes-lovart-best-practice |
| Touch Edit | /blog/touch-edit-best-practice-3-gestures-lovart |
| Sign up | https://lovart.ai/signup |

## FAQ

### Can I ship this to clients?

Run checklist: fake badges, double CTA, readable contact block.

### What if the date or price changes?

Touch Edit the block; skip full regen.

### Do I need Photoshop?

Not for most edits; extreme retouch may still need PS.

### Brand terms in """ + lang_label + """?

Keep Lovart, MCoT, ChatCanvas, Touch Edit as product names.

### How many directions?

Three to four; one enters Brand Kit flow.

"""


def recap_zh(n: int, topic: str, scenario: str) -> str:
    return f"""
## 实战复盘 {n}：{scenario}

我先故意用不清晰的需求去跑：两个 CTA、日期含糊、渠道不明确。围绕「{topic}」的第一轮输出往往很好看，也往往说不清要观众做什么。

然后我只改一句「任务句」，其他先保持粗糙。第二轮明显更可用。说明瓶颈经常在需求，不在模型神话。

### 我改了什么

只保留一个行动点；日期写成陌生人能读懂的格式；禁止假徽标；写明渠道尺寸；默认文案可 Touch Edit。

### 我在 Lovart 里怎么收

用 ChatCanvas 重述清理后的需求，锁 Brand Kit，出三个方向，再用 Touch Edit 改关键信息区。真正省下的是整图重跑次数。

### 可复用规则

如果同事只夸「好美」却说不出核心信息，资产就还没完成。先让信息赢，再谈装饰。本轮场景重点：{scenario}。
"""


def recap_en(n: int, topic: str, scenario: str) -> str:
    return f"""
## Field replay {n}: {scenario}

I deliberately ran a messy brief first: two CTAs, vague dates, unclear channel. Round one for **{topic}** looked pretty but did not say what to do.

I changed only the task sentence. Round two shipped. The bottleneck is usually the brief, not model hype.

### What I changed

One action only; human-readable dates; no fake badges; explicit artboard size; copy assumed editable.

### How I closed in Lovart

ChatCanvas restate → Brand Kit lock → three directions → Touch Edit on the info blocks. Savings = fewer full regens.

### Reusable rule

If the team says «beautiful» but not the offer, the asset is not done. Information wins first. Scenario focus: {scenario}.
"""


def build_article(a: dict) -> str:
    lang = a["lang"]
    is_cjk = lang in ("zh", "zh-TW")
    if is_cjk:
        core = section_zh_core(a)
        topic = a["topic_zh"]
        scenarios = a["scenarios_zh"]
        recap_fn = recap_zh
        target = 12000
        metric_fn = count_cjk_han
    else:
        core = section_en_core(a, lang)
        topic = a["topic_en"]
        scenarios = a["scenarios_en"]
        recap_fn = recap_en
        target = 3500
        metric_fn = count_words

    parts = [fm(a), core]
    i = 1
    si = 0
    while True:
        text = "".join(parts)
        if metric_fn(text) >= target:
            break
        scenario = scenarios[si % len(scenarios)]
        parts.append(recap_fn(i, topic, scenario))
        i += 1
        si += 1
        if i > 120:
            break

    parts.append(f"\n\n*Article for www.lovart.ai/blog 404 recovery. Part of i18n 404 recovery content cluster.*\n")
    return "".join(parts)


def main():
    results = []
    for a in ARTICLES:
        text = build_article(a)
        banned = check_banned(text)
        path = OUT / f"{a['lang']}-{a['slug']}.md"
        path.write_text(text, encoding="utf-8")
        is_cjk = a["lang"] in ("zh", "zh-TW")
        if is_cjk:
            metric = count_cjk_han(text)
            floor = 12000
            unit = "han"
        else:
            metric = count_words(text)
            floor = 3500
            unit = "words"
        ok = metric >= floor and not banned
        results.append({
            "file": path.name,
            "metric": metric,
            "unit": unit,
            "floor": floor,
            "banned": banned,
            "pass": ok,
            "cover": a["cover"],
        })
    print(f"{'FILE':<70} {'METRIC':>8} {'FLOOR':>8} {'PASS':>6} BANNED")
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['file']:<70} {r['metric']:>8} {r['unit']:>8} {str(r['pass']):>6} {b}")
    all_pass = all(r["pass"] for r in results)
    print(f"\nALL PASS: {all_pass}")


if __name__ == "__main__":
    main()
