"""
V4: sitemap (with TDK tags) + robots.txt + llms.txt + CSV
  - sitemap: <video:title> uses SEO title, <video:description> includes keywords, <video:tag> per keyword
  - robots.txt: standard crawl policy
  - llms.txt: categorized by 内容分类, per llmstxt.org spec
"""
import csv, json, re, html
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

CSV_PATH = Path(__file__).resolve().parent.parent / ".hermes/desktop-attachments/liblib_597_works.csv"
OUT_DIR = Path(__file__).resolve().parent.parent / "Output/liblib-seo"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SITE_BASE = "https://www.liblib.tv"
SITE_NAME = "LibTV (哩布哩布AI创作平台)"
BRAND = "LibTV"
VIDEO_NS = "http://www.google.com/schemas/sitemap-video/1.1"

CATEGORY_PRIORITY_CN = [
    "动画短片", "短片剧集", "MV", "创意TVC", "产品展示",
    "教学教程", "概念设计", "游戏美宣", "人文科普", "3D",
    "仿真人", "风格美学", "儿童教育", "公益广告", "企业宣传",
    "文旅政媒", "经典衍生", "精品漫剧", "才艺颜值", "2D",
    "meme", "vlog", "PPT演绎", "简历模卡", "营销促销", "其他",
]
TV_TOOLBOX_CATEGORY = "教学教程"

PLATFORM_TAGS = {
    "精选画布", "先锋", "专业", "荣誉", "TV工具箱",
    "AI影像狂飙季", "广告导演请就位", "AI漫剧精卫计划",
    "大乱斗｜vol.1 显形记", "大乱斗｜vol.2《AI，想象和尖叫》",
    "1-原创 IP 漫剧赛道", "2-国风非遗专项", "1-创意TVC",
    "2-故事短片", "3-非遗创生", "1-纪实与观察",
    "2-剧情与讽刺", "3-创意与超现实", "StarVideo2.0",
    "短片单元", "创意单元", "广告单元",
}

CATEGORY_DISPLAY_ORDER = [
    "动画短片", "短片剧集", "MV", "创意TVC", "产品展示",
    "教学教程", "概念设计", "仿真人", "3D", "游戏美宣",
    "人文科普", "风格美学", "公益广告", "儿童教育",
    "企业宣传", "文旅政媒", "经典衍生", "精品漫剧",
    "2D", "才艺颜值", "meme", "vlog", "PPT演绎",
    "简历模卡", "营销促销", "其他",
]

def extract_primary_cn_category(tags_str):
    if not tags_str: return "AI视频"
    tags = [t.strip() for t in tags_str.split("|")]
    tag_set = set(tags)
    if "TV工具箱" in tag_set: return TV_TOOLBOX_CATEGORY
    if "功能卖点" in tag_set: return "产品展示"
    if "规则演示" in tag_set: return "公益广告"
    if "商业广告" in tag_set: return "创意TVC"
    for cat in CATEGORY_PRIORITY_CN:
        if cat in tag_set: return cat
    return "AI视频"

def get_all_content_tags(tags_str):
    if not tags_str: return []
    return [t for t in [t.strip() for t in tags_str.split("|")] if t not in PLATFORM_TAGS and len(t) >= 2]

def build_title(name, cn_category):
    clean = name.strip().replace('"', '').replace('"', '')
    title = f"{clean} - {cn_category} - {BRAND}"
    if len(title) > 60 and len(clean) > 35:
        clean = clean[:35] + "…"
        title = f"{clean} - {cn_category} - {BRAND}"
    return title

def build_description(name, desc, tags_str, author, cn_category):
    clean_desc = ""
    if desc and len(desc) >= 10:
        d = desc.strip()
        core = d[:100]
        for sep in ["。", "！", "？"]:
            idx = core.rfind(sep)
            if idx > 30: core = core[:idx+1]; break
        clean_desc = core
    content_tags = get_all_content_tags(tags_str)
    if clean_desc and len(clean_desc) >= 10:
        suffix = f"——{author}用{BRAND} AI工具创作的{cn_category}作品"
        non_dup = [t for t in content_tags[:3] if t != cn_category]
        if non_dup: suffix += f"，涵盖{'、'.join(non_dup[:2])}"
        result = clean_desc + suffix
        if len(result) > 158: result = clean_desc[:120] + suffix[-35:]
        return result[:158]
    else:
        result = f"{author}使用{BRAND} AI工具创作的{cn_category}作品《{name}》"
        non_dup = [t for t in content_tags[:3] if t != cn_category]
        if non_dup: result += f"，涵盖{'、'.join(non_dup[:2])}等元素"
        return (result + "，探索AI影像的无限可能。")[:158]

def build_keywords(name, tags_str, desc, author, cn_category):
    kws, seen = [], set()
    if cn_category and cn_category != "AI视频": kws.append(cn_category); seen.add(cn_category)
    for t in get_all_content_tags(tags_str):
        if t not in seen and len(t) >= 3 and len(kws) < 5: kws.append(t); seen.add(t)
    if author and len(author) >= 2 and not re.match(r'^\d', author) and author not in seen and len(kws) < 6:
        kws.append(author); seen.add(author)
    for bk in ["LibTV", "AI视频", "AIGC", "AI创作"]:
        if len(kws) < 8 and bk not in seen: kws.append(bk); seen.add(bk)
    return ", ".join(kws[:8])

def build_social_tags(detail_url, title, description, cover_url, video_url):
    og = {"og:title": title, "og:description": description, "og:url": detail_url,
          "og:site_name": SITE_NAME, "og:type": "video.other", "og:locale": "zh_CN"}
    if cover_url: og.update({"og:image": cover_url, "og:image:width": "1200", "og:image:height": "630", "og:image:alt": title})
    if video_url: og.update({"og:video": video_url, "og:video:type": "video/mp4", "og:video:width": "1920", "og:video:height": "1080"})
    tw = {"twitter:card": "summary_large_image", "twitter:title": title, "twitter:description": description, "twitter:site": "@LibTV_Official"}
    if cover_url: tw["twitter:image"] = cover_url; tw["twitter:image:alt"] = title
    return {"openGraph": og, "twitterCard": tw}

def build_jsonld_creative_work(row, description, cn_category, cover_url, video_url):
    tuuid = row.get("templateUuid", "")
    detail_url = row.get("作品详情页", "") or f"{SITE_BASE}/detail/{tuuid}"
    name = row.get("名称", "").strip()
    pub_date = row.get("发布时间", "")
    iso_date = ""
    if pub_date:
        try: iso_date = datetime.strptime(pub_date.strip(), "%Y年%m月%d日 %H:%M").isoformat()
        except: pass
    ld = {"@context": "https://schema.org", "@type": "VideoObject", "@id": detail_url,
          "name": name, "description": description, "thumbnailUrl": cover_url or "",
          "uploadDate": iso_date, "url": detail_url}
    if video_url: ld["contentUrl"] = video_url; ld["embedUrl"] = detail_url
    if row.get("作者昵称"): ld["author"] = {"@type": "Person", "name": row["作者昵称"]}
    if row.get("标签"): ld["keywords"] = ", ".join([t.strip() for t in row["标签"].split("|") if t.strip()][:8])
    try:
        if int(row.get("点赞数", 0)):
            ld["interactionStatistic"] = {"@type": "InteractionCounter",
                "interactionType": "https://schema.org/LikeAction", "userInteractionCount": int(row["点赞数"])}
    except: pass
    ld["publisher"] = {"@type": "Organization", "name": "LibTV (哩布哩布)", "url": SITE_BASE}
    if cn_category: ld["genre"] = cn_category
    return ld

def build_jsonld_breadcrumb(detail_url, name, cn_category):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "LibTV 首页", "item": SITE_BASE},
            {"@type": "ListItem", "position": 2, "name": cn_category or "全部作品", "item": f"{SITE_BASE}/explore"},
            {"@type": "ListItem", "position": 3, "name": name}]}

def build_tdk_html(title, description, keywords):
    return (f'<title>{html.escape(title)}</title>\n'
            f'<meta name="description" content="{html.escape(description)}">\n'
            f'<meta name="keywords" content="{html.escape(keywords)}">')

def build_structured_data_html(ld_video, ld_breadcrumb, og, twitter, detail_url):
    parts = [
        f'<script type="application/ld+json">\n{json.dumps(ld_video, ensure_ascii=False, indent=2)}\n</script>',
        f'<script type="application/ld+json">\n{json.dumps(ld_breadcrumb, ensure_ascii=False, indent=2)}\n</script>',
        "\n".join(f'<meta property="{html.escape(p)}" content="{html.escape(str(v))}">' for p, v in og.items()),
        "\n".join(f'<meta name="{html.escape(n)}" content="{html.escape(str(v))}">' for n, v in twitter.items()),
        f'<link rel="canonical" href="{html.escape(detail_url)}">',
    ]
    return "\n\n".join(parts)

def vid_tag(el, tag_name, text):
    sub = SubElement(el, f"{{{VIDEO_NS}}}{tag_name}")
    sub.text = html.escape(str(text)[:2048])

def main():
    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f): rows.append(row)
    print(f"Processing {len(rows)} works (V4)…")

    urlset = Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
                                 "xmlns:video": VIDEO_NS,
                                 "xmlns:image": "http://www.google.com/schemas/sitemap-image/1.1"})

    # homepage
    home = SubElement(urlset, "url")
    SubElement(home, "loc").text = f"{SITE_BASE}/"
    SubElement(home, "changefreq").text = "daily"
    SubElement(home, "priority").text = "1.0"
    SubElement(home, "lastmod").text = datetime.now().strftime("%Y-%m-%d")

    for path, prio, freq in [("/explore","0.9","daily"),("/canvas","0.8","weekly"),
        ("/community","0.7","weekly"),("/events/ai-video-festival","0.7","weekly"),
        ("/events/director-challenge","0.7","weekly"),("/events/anime-contest","0.7","weekly")]:
        el = SubElement(urlset, "url")
        SubElement(el, "loc").text = f"{SITE_BASE}{path}"

    seo_rows = []
    cat_counter = Counter()
    cat_items = defaultdict(list)

    for row in rows:
        tuuid = row.get("templateUuid","")
        detail_url = row.get("作品详情页","") or f"{SITE_BASE}/detail/{tuuid}"
        name = row.get("名称","").strip()
        author = row.get("作者昵称","").strip()
        desc = row.get("描述","").strip()
        tags_str = row.get("标签","").strip()
        pub_date = row.get("发布时间","").strip()
        cover_url = row.get("封面URL","").strip()
        video_url = row.get("视频URL","").strip()
        likes = row.get("点赞数","0").strip()

        cn_category = extract_primary_cn_category(tags_str)
        cat_counter[cn_category] += 1

        title = build_title(name, cn_category)
        meta_desc = build_description(name, desc, tags_str, author, cn_category)
        keywords = build_keywords(name, tags_str, desc, author, cn_category)
        kw_list = [k.strip() for k in keywords.split(", ")]

        social = build_social_tags(detail_url, title, meta_desc, cover_url, video_url)
        ld_video = build_jsonld_creative_work(row, meta_desc, cn_category, cover_url, video_url)
        ld_breadcrumb = build_jsonld_breadcrumb(detail_url, name, cn_category)

        # sitemap: URL with video extension carrying full TDK
        url_el = SubElement(urlset, "url")
        SubElement(url_el, "loc").text = detail_url
        SubElement(url_el, "priority").text = "0.8"
        if pub_date:
            try:
                dt = datetime.strptime(pub_date, "%Y年%m月%d日 %H:%M")
                SubElement(url_el, "lastmod").text = dt.strftime("%Y-%m-%d")
            except: pass

        ve = SubElement(url_el, f"{{{VIDEO_NS}}}video")
        vid_tag(ve, "title", title)
        vid_tag(ve, "description", meta_desc)
        if cover_url: vid_tag(ve, "thumbnail_loc", cover_url)
        if video_url: vid_tag(ve, "content_loc", video_url)
        try:
            vid_tag(ve, "publication_date",
                    datetime.strptime(pub_date, "%Y年%m月%d日 %H:%M").isoformat() if pub_date
                    else datetime.now().isoformat())
        except: pass
        vid_tag(ve, "family_friendly", "yes")
        for kw in kw_list[:8]: vid_tag(ve, "tag", kw)
        if author: vid_tag(ve, "uploader", author)

        seo_rows.append({
            "序号": row.get("序号",""), "templateUuid": tuuid,
            "作品名称": name, "作者": author, "详情页URL": detail_url,
            "内容分类": cn_category, "原始标签": tags_str, "描述原文": desc,
            "TDK_Meta_HTML": build_tdk_html(title, meta_desc, keywords),
            "结构化数据_HTML": build_structured_data_html(ld_video, ld_breadcrumb, social["openGraph"], social["twitterCard"], detail_url),
            "封面URL": cover_url, "视频URL": video_url, "点赞数": likes, "发布时间": pub_date,
        })
        cat_items[cn_category].append((name, detail_url, meta_desc[:120], author, likes))

    # Write sitemap
    rough = tostring(urlset, encoding="unicode")
    xml_str = minidom.parseString(rough).toprettyxml(indent="  ", encoding="UTF-8")
    with open(OUT_DIR / "sitemap.xml", "wb") as f: f.write(xml_str)
    print(f"✅ sitemap.xml ({len(rows)+7} URLs, <video:title> = SEO title, <video:tag> = keywords)")

    # Write CSV
    fieldnames = ["序号","templateUuid","作品名称","作者","详情页URL",
                  "内容分类","原始标签","描述原文","TDK_Meta_HTML",
                  "结构化数据_HTML","封面URL","视频URL","点赞数","发布时间"]
    with open(OUT_DIR / "liblib_597_seo_metadata.csv", 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(seo_rows)
    print(f"✅ liblib_597_seo_metadata.csv ({len(seo_rows)} rows)")

    # robots.txt
    robots = f"""User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /login
Disallow: /register

Sitemap: {SITE_BASE}/sitemap.xml
"""
    with open(OUT_DIR / "robots.txt", "w") as f: f.write(robots)
    print("✅ robots.txt")

    # llms.txt
    llms = [f"# {BRAND} — 哩布哩布 AI 影像创作平台",
            f"> {len(rows)} 部 AI 生成视频作品，涵盖 {len(cat_counter)} 个内容分类。所有作品均由创作者使用 LibTV AI 工具制作。",
            "", f"- 首页: {SITE_BASE}", f"- 发现页: {SITE_BASE}/explore",
            f"- 画布创作: {SITE_BASE}/canvas", f"- Sitemap: {SITE_BASE}/sitemap.xml", ""]
    total = 0
    for cat in CATEGORY_DISPLAY_ORDER:
        items = cat_items.get(cat, [])
        if not items: continue
        llms.append(f"## {cat}（{len(items)} 部）\n")
        for name, url, desc_short, author, likes in items:
            llms.append(f"- [{name}]({url}) by {author}（👍{likes}）: {desc_short}")
        llms.append(""); total += len(items)
    with open(OUT_DIR / "llms.txt", "w", encoding="utf-8") as f: f.write("\n".join(llms))
    print(f"✅ llms.txt ({total} 作品, {len([c for c in CATEGORY_DISPLAY_ORDER if cat_items.get(c)])} 分类章节)")

    print(f"\n📊 分类: {dict(cat_counter.most_common(5))}")

if __name__ == "__main__":
    main()
