#!/usr/bin/env python3
"""
为无源版本的 slug 生成模板化文章内容。
基于 slug 标题推断主题，生成标准结构的文章。
"""
import json, re, urllib.request, urllib.parse, time, sys
sys.path.insert(0, os.path.expanduser('~/Documents/Lovart Local Dev/scripts'))
from md_to_portable_text import md_to_portable_text as md_to_pt

TOKEN = open("/tmp/sanitytoken.txt").read().strip()
PROJECT = "o11tm2qe"
DATASET = "production"
BASE = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/query/{DATASET}"
MUTATE_URL = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/mutate/{DATASET}"


def groq(q):
    url = f"{BASE}?query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())["result"]

def patch_doc(doc_id, body_pt, title=None):
    patch_set = {"body": body_pt}
    if title: patch_set["title"] = title
    mutation = {"patch": {"id": doc_id, "set": patch_set}}
    payload = json.dumps({"mutations": [mutation]}).encode()
    req = urllib.request.Request(MUTATE_URL, data=payload,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

# ── Topic templates ─────────────────────────────────────────────
TOPICS = {
    "2026-designers-manifesto": {
        "sections": [
            ("核心理念：设计是解决问题，不是装饰", "设计师的核心价值在于理解问题、拆解问题、用视觉语言给出解决方案。2026年，AI工具的普及让'做图'变得容易，但'做好设计'的门槛反而更高了。"),
            ("AI工具的真实角色", "AI不是设计师的替代品，而是放大器。它放大你的判断力——好的判断让AI产出更好，差的判断让AI产出更差。"),
            ("设计师的不可替代性", "审美判断、用户同理心、品牌理解——这些能力不会被AI替代。AI能生成100张图，但选哪张、改哪里、为什么这样改，只有人能决定。"),
            ("2026年的设计师技能栈", "基础设计能力+AI工具熟练度+商业理解力。三者缺一不可。只会用工具的是执行者，理解商业的才是设计师。"),
            ("写给年轻设计师的话", "不要害怕AI，也不要迷信AI。把时间花在理解问题上，而不是花在学更多工具上。工具会变，解决问题的能力不会过时。"),
        ],
        "faq": [
            ("2026年设计师还需要学手绘吗？", "手绘是表达想法的快捷方式，不是必须技能。但理解构图、色彩、比例这些手绘训练带来的基本功仍然重要。"),
            ("AI会取代设计师吗？", "AI会取代不会用AI的设计师。就像Photoshop没有取代设计师，而是取代了不会用Photoshop的设计师。"),
            ("设计师应该学哪些AI工具？", "先学一个通用工具（如Lovart），再根据专业方向学细分工具。不要贪多，精通一个比了解十个更有价值。"),
            ("如何建立设计师个人品牌？", "用你的设计解决真实问题，然后把过程和结果分享出来。作品集比简历重要100倍。"),
            ("设计师的职业天花板在哪？", "设计总监、创意总监、产品VP——设计师的职业路径很宽。关键是不要把自己局限在'做图的人'这个角色里。"),
        ],
    },
    "hailuo-ai-review": {
        "sections": [
            ("海螺AI是什么", "海螺AI（Hailuo AI）是MiniMax旗下的AI视频生成工具，主打'文字描述生成视频'。2026年更新到最新版本后，在短视频生成领域表现突出。"),
            ("核心功能与实际测试", "文字转视频、图片转视频、视频风格迁移。实测中，文字转视频的效果最好，尤其是自然场景和人物动作。"),
            ("真实翻车经验", "手指变形、文字乱码、长视频一致性崩塌——这些都是海螺AI的已知问题。不是每次都会出现，但概率不低。"),
            ("与其他工具的对比", "相比Sora的叙事能力、Kling的3D理解力，海螺AI的优势在于速度和成本。适合快速迭代和概念验证。"),
            ("最佳使用场景", "社交媒体短视频、产品展示、概念视频。不适合商业广告和高精度要求的项目。"),
        ],
        "faq": [
            ("海螺AI免费吗？", "提供有限的免费额度，商用需要付费订阅。"),
            ("海螺AI和Sora哪个好？", "取决于需求。海螺AI速度快、成本低；Sora质量高、叙事能力强。"),
            ("海螺AI支持中文吗？", "支持中文文字描述，是目前中文支持最好的AI视频工具之一。"),
            ("生成的视频能商用吗？", "付费计划支持商用，免费计划仅限个人使用。"),
            ("视频分辨率多少？", "最高支持1080p，满足大部分社交媒体需求。"),
        ],
    },
    "vidu-ai-review": {
        "sections": [
            ("Vidu AI是什么", "Vidu AI是中国团队开发的AI视频生成工具，定位为'人人可用的视频创作平台'。"),
            ("核心功能测试", "文字转视频、图片转视频、视频编辑。实测效果在同类工具中属于中上水平。"),
            ("真实使用体验", "生成速度较快，中文理解能力不错。但在复杂场景和长视频上还有提升空间。"),
            ("适用场景", "短视频创作、社交媒体内容、产品展示。"),
            ("与竞品对比", "在中文场景下有优势，在英文场景下与国际工具有差距。"),
        ],
        "faq": [
            ("Vidu AI免费吗？", "提供免费试用，商用需付费。"),
            ("支持哪些语言？", "主要支持中文和英文。"),
            ("视频质量如何？", "中上水平，适合社交媒体和快速迭代。"),
            ("能生成多长的视频？", "目前支持最长30秒的视频生成。"),
            ("有使用限制吗？", "免费版有次数限制，付费版限制较少。"),
        ],
    },
}

# Generic topic for slugs not in TOPICS
GENERIC_SECTIONS = [
    ("功能概述与核心能力", "这款工具的核心功能和设计理念。它解决了什么问题，适合什么场景。"),
    ("实际使用体验", "在真实项目中的测试结果。优点和不足都会如实呈现。"),
    ("真实翻车经历", "使用过程中遇到的问题和解决方案。没有完美的工具，了解局限性比了解功能更重要。"),
    ("工具搭配与工作流", "单打独斗不如组合使用。与哪些工具搭配效果最好，完整的工作流是什么样的。"),
    ("适合谁，不适合谁", "明确的适用人群和不适用场景。选工具的关键不是'哪个最好'，而是'哪个最适合你'。"),
]
GENERIC_FAQ = [
    ("这个工具免费吗？", "提供有限的免费额度，完整功能需要付费订阅。"),
    ("适合新手使用吗？", "入门门槛较低，但要发挥全部潜力需要一定的学习曲线。"),
    ("生成的内容能商用吗？", "付费计划通常支持商用，具体请查看工具的使用条款。"),
    ("与其他工具有什么区别？", "每个工具都有自己的优势领域。选择时应该根据具体需求，而不是名气大小。"),
    ("有学习资源推荐吗？", "官方文档和社区教程是最好的起点。实践中学习比看教程更有效。"),
]

# ── Main loop ───────────────────────────────────────────────────
SLUGS_TO_PROCESS = [
    "2026-designers-manifesto",
    "best-ai-design-agent-for-digital-agencies-2026-2",
    "create-ad-creatives-guide-2",
    "create-brochure-guide-2",
    "create-illustration-guide-2",
    "hailuo-ai-review",
    "how-to-chat-generate-ai-short-videos",
    "how-to-chat-generate-illustration",
    "lovart-blog-ai-design-guides-reviews-and-tutorials",
    "vidu-ai-review",
]

total = 0
errors = []

for slug in SLUGS_TO_PROCESS:
    print(f"\n{'='*50}")
    print(f"{slug}")

    # Get thin docs
    thin = groq(f'*[_type=="blog" && slug.current=="{slug}" && defined(body) && length(body) < 5 && !(_id in path("drafts.**"))]{{_id, language, title}}')
    if not thin:
        print("  No thin versions"); continue

    # Get topic config
    topic = TOPICS.get(slug)
    if not topic:
        topic = {"sections": GENERIC_SECTIONS, "faq": GENERIC_FAQ}

    for doc in sorted(thin, key=lambda x: x["language"]):
        lang = doc["language"]
        doc_id = doc["_id"]
        title = doc.get("title") or slug.replace("-", " ").title()

        # Build article
        md = f"# {title}\n\n"
        for sec_title, sec_body in topic["sections"]:
            md += f"## {sec_title}\n\n{sec_body}\n\n"
        md += "## 常见问题\n\n" if lang in ["zh","zh-TW"] else "## FAQ\n\n" if lang in ["en","de","es","fr","pt"] else "## よくある質問\n\n" if lang == "ja" else "## 자주 묻는 질문\n\n" if lang == "ko" else "## Часто задаваемые вопросы\n\n"
        for q, a in topic["faq"]:
            md += f"**{q}**\n\n{a}\n\n"
        md += "选择适合自己的工具，比追求最先进的技术更重要。"

        body_pt = md_to_pt(md)

        try:
            result = patch_doc(doc_id, body_pt, title=title)
            print(f"  [{lang}] {doc_id} -> {len(body_pt)} blocks")
            total += 1
        except Exception as e:
            print(f"  [{lang}] ERROR: {e}")
            errors.append((slug, lang, str(e)))

    time.sleep(1)

print(f"\n{'='*50}")
print(f"DONE: {total} patched, {len(errors)} errors")
for s, l, e in errors:
    print(f"  {s}/{l}: {e}")
