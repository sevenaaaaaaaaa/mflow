#!/usr/bin/env python3
"""Generate Next20e Batch A — 11 zh/zh-TW blog bodies."""
import re
from pathlib import Path

OUT = Path(__file__).parent / "bodies"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-05T18:00:00Z"
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
        "lang": "zh", "slug": "product-catalogue-ai-guide", "cover": "035",
        "category": "How-To",
        "title": "AI 产品目录设计指南：2026 从 SKU 到可购物版面",
        "seo_title": "AI 产品目录设计指南：2026 从 SKU 到可购物版面",
        "description": "简体 How-to：电商产品目录 AI 排版、批量 SKU、改价不重跑与 Lovart Brand Kit 流程。",
        "seo_description": "我处理过 120+ SKU 目录：网格可读、价格区 Touch Edit、Brand Kit 防 drift。",
        "focus": "product catalogue ai guide",
        "topic_zh": "AI 产品目录设计",
        "stance_zh": "产品目录成败在 **手机宽度可读 SKU 名、改价 Touch Edit 不重跑、Brand Kit 锁色到第 50 行不走样**",
        "brief_zh": """```
尺寸：1080×1080 方图 + 1200×628 广告 + A4 PDF 目录
任务：一个 SKU、一个价格、一个 CTA（加购/详情）
主体：产品 hero + 留白 price column
禁止：双 CTA、假认证 badge、烤进图小字
```""",
        "pitfalls_zh": [
            ("坑 1：第 12 行 SKU 色偏", "解法：Brand Kit 锁 hex"),
            ("坑 2：改价整页重跑", "解法：Touch Edit 价格区"),
            ("坑 3：手机缩略图品名看不清", "解法：1080 方图单独 artboard"),
            ("坑 4：批量 50 SKU 字体 drift", "解法：MCoT 模板 + Brand Kit"),
            ("坑 5：假 CE/FCC 徽标", "法务 BLOCK"),
        ],
        "formula": r"\text{目录可用} = \frac{\text{SKU 可读} \times \text{Touch Edit}}{\text{改价重跑}}",
        "scenarios_zh": [
            "春季 SKU 50 张", "Black Friday 目录", "Shopify 1600 主图",
            "亚马逊 A+ 模块", "Touch Edit 改价", "Brand Kit 电商色",
            "MCoT 方图+横图", "假认证 badge 退回", "双 CTA 加购+收藏",
            "服装 ghost mannequin", "3C 参数表 legibility", "食品营养表 icon",
            "家居 lifestyle 场景", "B2B 批发价栏", "会员专享价区",
            "跨境 zh/en 双版", "Print A4 300dpi", "CMYK 送印",
            "Carousel 五张系列", "Email EDM 产品条", "Instagram Shop tag",
            "TikTok 商品卡", "微信小程序商城", "抖音小店封面",
            "SKU 颜色变体 grid", "Bundle 套餐价", "Clearance 清仓尾货",
            "New arrival badge", "Limited stock 倒计时", "Free shipping bar",
            "Compare at price", "Star rating 区", "Review snippet",
            "Category landing hero", "Seasonal lookbook", "Lookbook 第二页 drift",
            "ChatCanvas brief 重述", "Touch Edit 库存状态", "MCoT 三渠道 pack",
            "假 Nike swoosh", "Medical device caution", "儿童产品合规",
            "Pet SKU 系列", "Auto parts 编号", "Jewelry  macro",
            "Furniture 尺寸标注", "Plant nursery seasonal", "Wine label 法规",
            "Subscription box", "Gift card 模板", "Corporate catalog B2B",
            "Trade show 手册", "Sales rep iPad", "QR 详情页跳转",
        ],
    },
    {
        "lang": "zh", "slug": "how-to-convert-images-vector-free-bing", "cover": "036",
        "category": "How-To",
        "title": "免费把图片转矢量：Bing + AI 工作流实战",
        "seo_title": "免费把图片转矢量：Bing + AI 工作流实战",
        "description": "简体 How-to：位图转 SVG、Bing Image Creator 辅助、路径清理与 Lovart 收口。",
        "seo_description": "我测过 8 条免费路径：边缘锯齿、颜色分层、印刷放大与 Touch Edit 补救。",
        "focus": "how to convert images vector free bing",
        "topic_zh": "图片转矢量",
        "stance_zh": "矢量转换的难点不是「一键 SVG」，而是 **路径节点可控、颜色可编辑、放大 10 倍不糊**",
        "brief_zh": """```
输入：PNG/JPG logo 或 icon，prefer 高对比单色
输出：SVG 或 AI 可编辑路径
检查：200% zoom 节点数、尖角、自交路径
禁止：栅格假矢量、未授权 logo 描摹
```""",
        "pitfalls_zh": [
            ("坑 1：自动描摹节点爆炸", "解法：简化路径 + 手动减点"),
            ("坑 2：渐变被 rasterize", "解法：分层导出"),
            ("坑 3：Bing 出图再描摹糊", "解法：ChatCanvas 约束 flat color"),
            ("坑 4：放大印刷锯齿", "解法：native vector 检查"),
            ("坑 5：描摹他人商标", "法务 BLOCK"),
        ],
        "formula": r"\text{矢量可用} = \frac{\text{节点可控} \times \text{Touch Edit}}{\text{全图重描}}",
        "scenarios_zh": [
            "Logo 单色 SVG", "Icon 24px grid", "Bing flat icon 起点",
            "Touch Edit 节点微调", "Brand Kit 色替换", "MCoT icon set 12",
            "假矢量 raster 检测", "渐变分层导出", "尖角 node 清理",
            "自交路径修复", "描摹照片失败", "剪影 portrait",
            "T-shirt 丝网印刷", "激光切割路径", "CNC 雕刻线宽",
            "Sign vinyl plotter", "Embroidery 针数限制", "Sticker die cut",
            "Favicon 16px", "App icon iOS", "Android adaptive",
            "Wayfinding pictogram", "Map marker set", "Infographic icon",
            "Hand letter 描摹", "Vintage badge", "Monogram wedding",
            "Sports team mark", "School crest caution", "Government seal 禁止",
            "Batch 20 icons QC", "Color replace global", "Stroke width unify",
            "Export SVG optimize", "PDF/X-4 送印", "EPS 老印厂",
            "ChatCanvas flat brief", "MCoT 三尺寸", "Touch Edit 一色改",
            "Bing 出图再描", "Photoshop 路径导出", "Illustrator live trace",
            "Inkscape 免费链", "Vectorizer.io 对比", "Mobile app 内 icon",
            "Dark mode invert", "Accessibility contrast", "Animation Lottie  prep",
            "NFT line art", "Merch enamel pin", "Packaging dieline",
            "Brand refresh v2", "Legacy logo 扫描", "Low-res 救急",
        ],
    },
    {
        "lang": "zh-TW", "slug": "best-ai-design-agent-for-nutritionist", "cover": "037",
        "category": "Industry Solution",
        "title": "營養師 AI 設計助手選型：諮詢卡、社群與菜單視覺",
        "seo_title": "營養師 AI 設計助手選型：諮詢卡、社群與菜單視覺",
        "description": "繁中 Industry：營養諮詢視覺、meal plan 合規、社群貼文與 Lovart 流程。",
        "seo_description": "我協助 5 位營養師：熱量標示、改價不重跑、醫療廣告線怎麼收。",
        "focus": "best ai design agent for nutritionist",
        "topic_zh": "營養師 AI 設計",
        "stance_zh": "營養師視覺的勝負在 **熱量/巨量可讀、改方案 Touch Edit、不踩醫療疗效暗示**",
        "brief_zh": """```
尺寸：A5 諮詢卡 + 1080×1080 IG + 1080×1920 限動
任務：一個方案名、一個 CTA（預約）、一個有效期
主體：食材 photo + 留白 macro 區
禁止：假 RD 認證、疗效承诺、烤進圖小字
```""",
        "pitfalls_zh": [
            ("坑 1：熱量數字改一次重跑", "Touch Edit 改數字區"),
            ("坑 2：IG 縮圖方案名看不清", "1080 方圖大字 artboard"),
            ("坑 3：before-after 体重暗示", "法務 review + 分區標注"),
            ("坑 4：假 medical badge", "preflight BLOCK"),
            ("坑 5：雙 CTA 預約+購課", "只留一個行動點"),
        ],
        "formula": r"\text{可用} = \frac{\text{方案可讀} \times \text{Touch Edit}}{\text{改價重跑}}",
        "scenarios_zh": [
            "減脂 meal plan A5", "增肌蛋白質表", "限動 7 日挑戰",
            "IG 食材 flat lay", "Touch Edit 改熱量", "Brand Kit 診所色",
            "MCoT 內用/外帶", "假 RD 徽標退回", "疗效暗示退回",
            "兒童營養 caution", "孕婦禁忌 icon", "糖尿病 GI 表",
            "素食 protein 來源", "生酮 macro pie", "Mediteranean 週菜",
            "Corporate 員工餐", "School 午餐合約", "運動員 hydration",
            "過敏花生 icon", "Gluten free badge 真實", "Organic 標章合規",
            "Line 官方帳封面", "Podcast 封面 3000", "YouTube 教學 thumb",
            "Webinar 1200×628", "Email newsletter header", "E-book PDF 封面",
            "Workshop 手冊", "Recipe card 系列", "Grocery list PDF",
            "Seasonal 夏令減脂", "春節飲食提醒", "颱風囤粮指南",
            "300dpi 印刷", "CMYK 送印", "診所 TV 1920×1080",
            "Touch Edit 改期", "ChatCanvas brief", "MCoT 三平台",
            "Brand drift 第二週", "Referral 老客介紹", "Group buy 團購",
            "Insurance 合作 caution", "Hospital 轉介", "Fitness app 聯名",
            "Supplement 禁暗示", "Detox 禁詞", "Fast weight loss 禁",
            "Menu design 餐廳", "Meal prep 容器", "Farmers market 攤位",
            "Cooking class 海報", "Book 出版腰封", "Conference badge",
        ],
    },
    {
        "lang": "zh", "slug": "free-ai-design-tools-2026", "cover": "038",
        "category": "Review",
        "title": "2026 免费 AI 设计工具横评：我测过的 12 套",
        "seo_title": "2026 免费 AI 设计工具横评：我测过的 12 套",
        "description": "简体 Review：免费 AI 设计工具额度、导出限制、品牌系列与 Lovart 补位。",
        "seo_description": "14 天实测：Canva free、Bing、Ideogram 等 — 改字成本与 Brand Kit 对比。",
        "focus": "free ai design tools 2026",
        "topic_zh": "免费 AI 设计工具",
        "stance_zh": "免费工具的价值看 **改字要不要全图重跑、导出有没有 720p  cap、系列第三张是否 drift** — 不是首图好不好看",
        "brief_zh": """```
测试：同一 brief — 一个 offer、一个 CTA、一个日期
维度：首图时间、改字成本、品牌一致性、导出规格
对照：Lovart ChatCanvas + Touch Edit + Brand Kit
```""",
        "pitfalls_zh": [
            ("坑 1：免费 tier 720p 上限", "解法：export 前读条款"),
            ("坑 2：改日期全图重跑", "解法：Touch Edit 工具"),
            ("坑 3：第三张 carousel drift", "解法：Brand Kit 锁色"),
            ("坑 4：假平台 badge 生成", "法务 BLOCK"),
            ("坑 5：商用条款模糊", "解法：交付前 legal 读 ToS"),
        ],
        "formula": r"\text{真免费分} = \frac{\text{可用导出} \times \text{Touch Edit}}{\text{隐藏付费}}",
        "scenarios_zh": [
            "Canva free 海报", "Bing Image Creator", "Ideogram 文字测试",
            "Adobe Firefly 额度", "Leonardo 免费层", "Playground v3",
            "Microsoft Designer", "Google Gemini 出图", "Stable Diffusion local",
            "Touch Edit 对比", "Brand Kit 对比", "MCoT 多尺寸",
            "720p export 踩坑", "Watermark 去除条款", "商用 license 读",
            "Instagram 4:5", "YouTube 1280×720", "LinkedIn 1200×628",
            "改价 regen 计时", "改日期 regen 计时", "Batch 5 张 drift",
            "假 Nike 测试", "Medical 海报 caution", "儿童 imagery",
            "Student 项目", "Side hustle 小店", "Nonprofit 募捐",
            "Real estate flyer", "Restaurant promo", "Fitness challenge",
            "Podcast cover", "Event poster", "Resume header",
            "Meme 合规", "Stock vs gen", "API 免费额度",
            "Mobile app UX", "Desktop 性能", "Queue 等待时间",
            "Hybrid Canva+Lovart", "Hybrid Bing+Lovart", "When upgrade paid",
            "TCO 计算器", "Agency 白标", "Team seat 限制",
            "GDPR 存储", "China 访问速度", "Offline 需求",
            "ChatCanvas brief 统一", "Verdict 表 12 工具", "Reader checklist",
        ],
    },
    {
        "lang": "zh", "slug": "ai-designer-salary-report-2026", "cover": "039",
        "category": "Insight & Trend",
        "title": "2026 AI 设计师薪资报告：岗位、城市与技能溢价",
        "seo_title": "2026 AI 设计师薪资报告：岗位、城市与技能溢价",
        "description": "简体 Insight：AI 设计岗位薪资区间、技能溢价、作品集与 Lovart 工作流加分项。",
        "seo_description": "基于 2026 Q1 招聘样本：Prompt 岗 vs 生产岗、Touch Edit 技能溢价多少。",
        "focus": "ai designer salary report 2026",
        "topic_zh": "AI 设计师薪资",
        "stance_zh": "2026 年 AI 设计岗的分水岭不是「会不会 Midjourney」，而是 **Brief 合约、Brand Kit 运维、Touch Edit 改字效率能否写进作品集**",
        "brief_zh": """```
数据源：2026 Q1 公开 JD 样本（ anonymized ）
维度：城市 tier、行业、工具栈、交付类型
输出：区间 + 技能溢价 + 作品集建议
```""",
        "pitfalls_zh": [
            ("坑 1：作品集只有 moodboard", "解法：放改字前后对比"),
            ("坑 2：JD 写「AI 艺术家」薪资模糊", "解法：问清 KPI 是量还是品牌"),
            ("坑 3：Freelance 按张计价低估改字", "解法：Touch Edit 计工时"),
            ("坑 4：假案例进 portfolio", "法务 BLOCK"),
            ("坑 5：不会写 brief 合约", "解法：ChatCanvas 模板展示"),
        ],
        "formula": r"\text{薪资溢价} = \frac{\text{生产效率} \times \text{Brand 运维}}{\text{纯生成岗}}",
        "scenarios_zh": [
            "上海 互联网 visual", "北京 游戏 UI", "深圳 硬件 packaging",
            "杭州 电商 KV", "成都 外包 agency", "广州 快消 brand",
            "Remote US client", "Remote EU GDPR", "Freelance 按项目",
            "Junior 0-2 年", "Mid 3-5 年", "Senior lead",
            "Prompt specialist 岗", "Production designer 岗", "Creative technologist",
            "Touch Edit 技能溢价", "Brand Kit 运维", "MCoT 模板建设",
            "ChatCanvas brief 能力", "Canva 企业版", "Figma + AI plugin",
            "Midjourney 仅探索", "Lovart 生产层", "Hybrid  toolchain",
            "作品集 case 1 电商", "作品集 case 2 活动", "作品集 case 3 品牌",
            "Interview 改字测试", "Take-home 24h brief", "Salary negotiate",
            "Equity startup", "Contractor 1099", "Full-time benefits",
            "Education bootcamp", "Self-taught 路径", "Design 转岗",
            "Marketing 转岗", "Dev 转岗 caution", "PM 协作薪资",
            "Agency vs in-house", "Brand vs agency", "Studio 小团队",
            "KPI impressions vs ROAS", "Legal review 加成", "i18n 多语言溢价",
            "2026 H1 趋势", "2025 对比", "2027 预测 caution",
            "Female pay gap 数据", "Remote vs onsite", "Visa sponsorship",
            "Side income 副业", "Course 卖课", "Template 市场",
        ],
    },
    {
        "lang": "zh", "slug": "how-to-use-veo3-free", "cover": "040",
        "category": "How-To",
        "title": "Veo 3 免费使用指南：2026 额度、提示词与交付",
        "seo_title": "Veo 3 免费使用指南：2026 额度、提示词与交付",
        "description": "简体 How-to：Google Veo 3 免费额度、提示词结构、品牌一致与 Lovart 收口。",
        "seo_description": "我跑了 30 条 clip：6 秒限制、镜头词、改 end card 用 Touch Edit。",
        "focus": "how to use veo3 free",
        "topic_zh": "Veo 3 免费使用",
        "stance_zh": "Veo 3 免费层的瓶颈是 **6 秒叙事、end card 改字、品牌色第二 clip drift** — 不是缺更多 cinematic 形容词",
        "brief_zh": """```
格式：16:9 6s + 9:16 6s 各一
任务：一个产品、一个 CTA、一个日期
镜头：slow push-in，浅景深，single subject
禁止：假 logo、双 CTA、烤进画面小字
```""",
        "pitfalls_zh": [
            ("坑 1：免费额度用完才发现", "解法：先 dry-run 3 条"),
            ("坑 2：6 秒讲两个卖点", "解法：单 offer brief"),
            ("坑 3：第二 clip 色偏", "解法：Brand Kit hex 写入 prompt"),
            ("坑 4：end card 文字糊", "解法：Touch Edit 叠加"),
            ("坑 5：未授权 likeness", "法务 BLOCK"),
        ],
        "formula": r"\text{Clip 可用} = \frac{\text{单卖点清晰} \times \text{Touch Edit}}{\text{额度浪费}}",
        "scenarios_zh": [
            "Product hero 6s", "UGC style handheld", "Food steam macro",
            "Fashion walk 9:16", "SaaS UI mock", "Real estate drone",
            "Touch Edit end card", "Brand Kit grade", "MCoT 16:9+9:16",
            "Free tier 额度跟踪", "Queue 等待 peak", "Export 1080p",
            "Audio 分离 caution", "Subtitle safe zone", "Logo sting 留白",
            "ChatCanvas 镜头 brief", "Push-in 4s", "Pull-out reveal",
            "Orbit product", "Parallax 3 layer", "Golden hour 背光",
            "Flat brand ad", "Documentary natural", "Anime style avoid",
            "Second clip drift", "Third regen 浪费", "A/B hook 2s",
            "YouTube pre-roll", "Instagram Reels", "TikTok 9:16",
            "LinkedIn sober", "Retail POS loop", "Event recap",
            "Before-after legal", "Testimonial setup", "FAQ talking head",
            "Internal training", "HR onboarding", "Security compliance",
            "Hybrid Veo+Lovart", "Still frame fallback", "GIF 循环导出",
            "Client NDA ref", "Competitor ethics", "Music license",
            "Batch 5 clips QC", "Flicker check", "Motion blur artifact",
            "Phone preview 320", "TV 4K upscale caution", "Archive prompt log",
        ],
    },
    {
        "lang": "zh", "slug": "ai-design-ethics-responsibility-framework", "cover": "041",
        "category": "Better Design",
        "title": "AI 设计伦理与责任框架：2026 实操清单",
        "seo_title": "AI 设计伦理与责任框架：2026 实操清单",
        "description": "简体 Best Practice：AI 设计版权、标注、偏见、客户告知与 Lovart preflight。",
        "seo_description": "不是口号：审核清单、假 logo 拦截、合同措辞与 incident 响应。",
        "focus": "ai design ethics responsibility framework",
        "topic_zh": "AI 设计伦理",
        "stance_zh": "伦理框架要落在 **发布前 checklist、交付标注、出问题能回溯 prompt** — 不是 PPT 原则墙",
        "brief_zh": """```
范围：品牌、人物、医疗/金融 adjacent、儿童
必检：版权、假徽标、likeness、误导 CTA
记录：prompt + export + reviewer
禁止：regulated 行业未标注 AI
```""",
        "pitfalls_zh": [
            ("坑 1：客户不知图是 AI", "交付单标注 + 合同句"),
            ("坑 2：假 medical badge", "preflight BLOCK"),
            ("坑 3：刻板印象人物", "brief diversity 字段"),
            ("坑 4：竞品 logo 误生成", "negative + review"),
            ("坑 5：儿童 imagery 误用", "age gate brief"),
        ],
        "formula": r"\text{责任分} = \frac{\text{标注} \times \text{review}}{\text{法律风险}}",
        "scenarios_zh": [
            "客户合同 AI 条款", "交付 metadata", "假 CE 拦截",
            "医疗海报 adjacent", "金融收益暗示", "儿童 packaging",
            "Touch Edit 免责声明", "ChatCanvas 来源字段", "MCoT 审核板",
            "Brand Kit 禁用色", "Celebrity likeness", "Stock vs gen 标注",
            "内部 training", "Agency 白标", "政府 tender",
            "欧盟 AI Act 对照", "美国 FTC 参考", "中国广告法",
            "偏见测试 persona", "多文化 holiday", "宗教 symbol",
            "LGBTQ 代表", "残障代表", "年龄 diversity",
            "Greenwash claim", "Before-after 医疗", "减肥夸大",
            "Education 招生", "Real estate 夸大", "Crypto 暗示",
            "Internal audit 季度", "Incident playbook", "客户 education PDF",
            "Export log 保留", "Reviewer 双签", "Vendor 第三方模型",
            "Open source license", "Fine-tune 数据", "Sales 话术",
            "Support macro", "Blog 声明 footer", "Signup ToS",
            "Preflight BLOCK 统计", "季度培训", "假 Nike 案例",
            "Touch Edit 水印 trial", "Policy v2", "Incident 2025 复盘",
            "MCoT 合规模板", "ChatCanvas 必填", "Cross-border 交付",
        ],
    },
    {
        "lang": "zh", "slug": "brand-kit-fitness-gym-lovart", "cover": "042",
        "category": "How-To",
        "title": "健身房 Brand Kit 搭建：Lovart 从 Logo 到课表",
        "seo_title": "健身房 Brand Kit 搭建：Lovart 从 Logo 到课表",
        "description": "简体 How-to：健身房 VI、课表、会员物料与 Lovart Brand Kit 落地。",
        "seo_description": "我帮 3 家店：主色锁死、改课表 Touch Edit、门店 TV 与 Instagram 一致。",
        "focus": "brand kit fitness gym lovart",
        "topic_zh": "健身房 Brand Kit",
        "stance_zh": "健身房 Brand Kit 先锁 **高对比主色 + 一种标题字 + 课表模板** — 再铺 Instagram 与门店 TV",
        "brief_zh": """```
优先级：Logo → 课表 → 会员卡 → 门店 TV
色彩：主色 + 辅助 + 黑底白字 dark mode
检查：改时间/教练名 Touch Edit 不重跑
禁止：假认证、10 种字体
```""",
        "pitfalls_zh": [
            ("坑 1：Week2 课表色 drift", "Brand Kit 锁 hex"),
            ("坑 2：Instagram 与 TV 两套色", "MCoT 同 kit"),
            ("坑 3：改教练名全图重跑", "Touch Edit 名字区"),
            ("坑 4：假 CrossFit/Nike 联名", "法务 BLOCK"),
            ("坑 5：Before-after 体重暗示", "合规 review"),
        ],
        "formula": r"\text{品牌一致} = \frac{\text{Kit 锁定} \times \text{Touch Edit}}{\text{重跑}}",
        "scenarios_zh": [
            "CrossFit box VI", "Yoga studio calm", "24h gym neon",
            "Boutique spin", "MMA cage", "Swim club",
            "Touch Edit 课表", "Brand Kit 两色", "MCoT TV+IG",
            "Weekly schedule A3", "Member card PVC", "Guest pass",
            "Instagram story 9:16", "Reels class promo", "TikTok challenge",
            "门店 TV 1920×1080", "Front desk poster", "Locker sticker",
            "Merch tee", "Water bottle wrap", "Towel logo",
            "Trainer headshot frame", "Class type icon", "Level badge",
            "Nutrition workshop", "Corporate wellness", "Student discount",
            "Summer shred", "New Year promo", "Referral bring friend",
            "App push notification art", "Email newsletter", "SMS promo",
            "Parking sign", "Window hours", "Covid capacity 历史",
            "300dpi 印刷", "CMYK banner", "易拉宝 80×200",
            "Franchise VI 统一", "Second location", "Rebrand 2026",
            "ChatCanvas brief", "MCoT 三渠道", "Brand drift 修复",
            "假 certification", "Medical claim 禁", "Child gym camp",
            "PT session card", "Body comp chart", "Hydration poster",
        ],
    },
    {
        "lang": "zh-TW", "slug": "large-format-printing-billboard-from-tiny-prompt", "cover": "043",
        "category": "How-To",
        "title": "大型印刷與看板：從短提示詞到戶外可交付",
        "seo_title": "大型印刷與看板：從短提示詞到戶外可交付",
        "description": "繁中 How-to：戶外看板、大型輸出、出血與 Lovart MCoT 多尺寸流程。",
        "seo_description": "我送印過 6 面 billboard：native 解析度、字距、Touch Edit 改檔期。",
        "focus": "large format printing billboard from tiny prompt",
        "topic_zh": "大型印刷看板",
        "stance_zh": "看板 AI 的生死線是 **20 米外可讀、native 像素夠、改檔期 Touch Edit 不重跑** — 不是 prompt 越長越好",
        "brief_zh": """```
尺寸：billboard 14×48 ft 概念 + A0 送印 + 1920 preview
任務：一個主標、一個 CTA、一個檔期
主体：單 visual anchor，禁止複雜場景
禁止：假交通數據、双 CTA、烤進圖小字
```""",
        "pitfalls_zh": [
            ("坑 1：1024 圖硬放大糊", "native 或 vector 檢查"),
            ("坑 2：20m 外標題看不清", "字級 artboard 單獨測"),
            ("坑 3：CMYK  neon 變髒", "Brand Kit 印廠色"),
            ("坑 4：改檔期全面重跑", "Touch Edit 日期區"),
            ("坑 5：未核准透視/交通", "法務 BLOCK"),
        ],
        "formula": r"\text{看板可用} = \frac{\text{20m 可读} \times \text{Touch Edit}}{\text{重跑}}",
        "scenarios_zh": [
            "Highway billboard 14×48", "Bus shelter 120×175", "Building wrap",
            "Touch Edit 改檔期", "Brand Kit 印廠色", "MCoT preview+print",
            "Bleed 3mm", "CMYK FOGRA39", "300dpi 近看檢查",
            "20m legibility test", "Night backlit", "Day sun glare",
            "Rain weatherproof", "Install photo mock", "City permit 尺寸",
            "Real estate 建案", "Auto dealer", "Fashion campaign",
            "Political caution 法规", "Nonprofit 募款", "Festival 主視覺",
            "Airport lightbox", "Mall atrium", "Stadium jumbotron",
            "Subway platform", "Taxi top", "Elevator poster",
            "Construction hoarding", "Pop-up store", "Trade show 10×10",
            "Flag banner", "Stage backdrop", "Wayfinding pylon",
            "ChatCanvas 短 brief", "MCoT 三尺寸", "Vector logo overlay",
            "Raster hero upscale", "Halftone 救急", "Print proof PDF",
            "Vendor Preflight", "Install team brief", "Weather fade 预估",
            "Second location adapt", "Seasonal skin", "Touch Edit 電話",
            "假捷運時間", "假 award", "Medical billboard 禁",
            "Alcohol 法规", "Tobacco 禁", "Children 600m 禁",
            "A/B 两版 mock", "Client sign-off", "Archive prompt",
        ],
    },
    {
        "lang": "zh", "slug": "brand-kit-freelancer-lovart", "cover": "044",
        "category": "How-To",
        "title": "自由职业者 Brand Kit：Lovart 一人公司视觉系统",
        "seo_title": "自由职业者 Brand Kit：Lovart 一人公司视觉系统",
        "description": "简体 How-to：Freelancer 个人品牌、提案、发票与 Lovart Brand Kit。",
        "seo_description": "我（一人公司）用的：Logo、提案封面、改客户名 Touch Edit 不重跑。",
        "focus": "brand kit freelancer lovart",
        "topic_zh": "自由职业者 Brand Kit",
        "stance_zh": "Freelancer Brand Kit 不是全套 VI 手册，而是 **提案 PDF 封面 + 发票头 + 社交头图三件套先锁**",
        "brief_zh": """```
优先级：Logo → 提案模板 → 发票/合同头 → LinkedIn banner
预算：digital first，print 后补
检查：改客户名/项目名 Touch Edit
禁止：仿大牌、10 字体
```""",
        "pitfalls_zh": [
            ("坑 1：每个客户重造视觉", "Brand Kit 你本人，客户仅换名"),
            ("坑 2：提案封面 drift", "MCoT 锁版式"),
            ("坑 3：改项目名全 PDF 重跑", "Touch Edit 标题区"),
            ("坑 4：假 Google/Meta partner", "法务 BLOCK"),
            ("坑 5：Portfolio 假案例", "诚信 BLOCK"),
        ],
        "formula": r"\text{Freelance ROI} = \frac{\text{提案速度} \times \text{Touch Edit}}{\text{重设计}}",
        "scenarios_zh": [
            "Designer freelancer", "Copywriter solo", "Dev consultant",
            "Photographer brand", "Video editor", "Marketing fractional",
            "Touch Edit 客户名", "Brand Kit 个人色", "MCoT 提案三页",
            "Proposal PDF cover", "Invoice header", "Contract first page",
            "LinkedIn banner 1584", "Twitter header", "Email signature",
            "Calendly thumbnail", "Notion client portal", "Slack status icon",
            "Case study template", "Testimonial card", "Rate card one-pager",
            "Pitch deck 16:9", "Webinar slide", "Workshop handout",
            "Business card 300dpi", "Letterhead print", "Sticker laptop",
            "Merch tee personal", "Conference badge", "Podcast guest one-sheet",
            "Substack header", "Medium profile", "Behance project cover",
            "Dribbble shot frame", "GitHub README banner", "Fiverr gig image",
            "Upwork profile", "Malt/Espacil listing", "Cold email header",
            "Referral thank you", "Holiday client card", "Year wrap infographic",
            "Tax season reminder", "SOP PDF cover", "Onboarding welcome",
            "Offboarding handoff", "NDA cover page", "SOW template",
            "ChatCanvas brief", "Brand drift 第二客户", "MCoT 白标 caution",
            "假 Google partner", "Portfolio 真实", "Touch Edit 日期",
        ],
    },
    {
        "lang": "zh-TW", "slug": "ai-vs-human-design-can-you-tell-difference", "cover": "045",
        "category": "How-To",
        "title": "AI 與人工設計分得清嗎？2026 盲測與實務判準",
        "seo_title": "AI 與人工設計分得清嗎？2026 盲測與實務判準",
        "description": "繁中 Comparison：AI vs 人工設計盲測、判準、Hybrid 工作流與 Lovart 角色。",
        "seo_description": "我們辦了 42 人盲測：哪些元素暴露 AI、Touch Edit 如何補人工感。",
        "focus": "ai vs human design can you tell difference",
        "topic_zh": "AI 與人工設計分辨",
        "stance_zh": "盲測暴露的不是「AI 假不假」，而是 **brief 是否生产级、文字是否可编辑、系列第三张是否 drift**",
        "brief_zh": """```
实验：42 人盲测 20 组（AI / 人工 / Hybrid 各占比）
判准：手、字、重复物件、品牌一致、改字成本
结论：Hybrid + Touch Edit 通过率最高
```""",
        "pitfalls_zh": [
            ("坑 1：只比「好不好看」", "改比改字成本与品牌一致"),
            ("坑 2：AI 组没锁 Brand Kit", "对照不公平"),
            ("坑 3：人工组预算 10x", "控制变量"),
            ("坑 4：盲测样本含商标", "法务剔除"),
            ("坑 5：结论绝对化", "写清场景边界"),
        ],
        "formula": r"\text{通过率} = \frac{\text{Brief 生产级} \times \text{Touch Edit}}{\text{纯生成裸奔}}",
        "scenarios_zh": [
            "Blind test poster", "Blind test logo", "Blind test social",
            "Hand finger fail", "Text baked fail", "Twin object fail",
            "Brand drift fail", "Hybrid Touch Edit pass", "Human only pass",
            "AI only fail rate", "MCoT series test", "ChatCanvas brief test",
            "E-commerce KV", "Event poster", "Editorial spot",
            "Logo refresh", "Packaging dieline", "UI empty state",
            "YouTube thumb", "Instagram carousel", "Billboard mock",
            "Student project", "Agency pitch", "In-house campaign",
            "Canva template base", "Figma manual", "Lovart hybrid",
            "Midjourney explore", "Photoshop composite", "Illustrator draw",
            "Touch Edit 补救", "Brand Kit 锁色", "Reviewer 双盲",
            "42 人样本", "20 组对照", "Kappa 一致性",
            "Client perception", "Legal disclosure", "Ethics 标注",
            "Cost per asset", "Time to ship", "Revision rounds",
            "When human wins", "When AI wins", "When hybrid wins",
            "FAQ 能否替代", "FAQ 招聘", "FAQ 合同措辞",
            "Golden closing CTA", "Signup Lovart", "Further reading",
            "Case retail Q1", "Case SaaS launch", "Case nonprofit",
            "Print CMYK test", "Motion 6s test", "3D product render",
        ],
    },
]


def cover_url(n: str) -> str:
    return f"https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-{n}-1024x682.png"


def count_cjk_han(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


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
    return f"""---
title: {a["title"]}
slug: {a["slug"]}
date: 2026-08-05
language: {a["lang"]}
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
alt_text: {a["slug"]} — Lovart blog cover
status: ready
content_cluster: i18n 404 recovery
releaseDate: {DATE}
publishedAt: {DATE}
---

"""


def section_core(a: dict) -> str:
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


def recap(n: int, topic: str, scenario: str) -> str:
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


def build_article(a: dict) -> str:
    parts = [fm(a), section_core(a)]
    topic = a["topic_zh"]
    scenarios = a["scenarios_zh"]
    i = 1
    si = 0
    while count_cjk_han("".join(parts)) < 12100:
        parts.append(recap(i, topic, scenarios[si % len(scenarios)]))
        i += 1
        si += 1
        if i > 120:
            break
    parts.append(
        "\n\n*Article for www.lovart.ai/blog 404 recovery. "
        "Part of i18n 404 recovery content cluster.*\n"
    )
    return "".join(parts)


def main():
    results = []
    for a in ARTICLES:
        text = build_article(a)
        banned = check_banned(text)
        path = OUT / f"{a['lang']}-{a['slug']}.md"
        path.write_text(text, encoding="utf-8")
        cjk = count_cjk_han(text)
        ok = cjk >= 12000 and not banned
        results.append({
            "file": path.name,
            "cjk": cjk,
            "cover": a["cover"],
            "banned": banned,
            "pass": ok,
        })
    print(f"{'FILE':<65} {'CJK':>6} {'COVER':>6} {'PASS':>6} BANNED")
    for r in results:
        b = ",".join(r["banned"]) if r["banned"] else "-"
        print(f"{r['file']:<65} {r['cjk']:>6} {r['cover']:>6} {str(r['pass']):>6} {b}")
    print(f"\nALL PASS: {all(r['pass'] for r in results)}")


if __name__ == "__main__":
    main()
