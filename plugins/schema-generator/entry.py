"""schema-generator: transform(text, config) -> JSON-LD string"""
import json, re
from datetime import datetime

def transform(text, config=None):
    slug = (config or {}).get("slug", "untitled")
    lang = (config or {}).get("lang", "en")
    title_m = re.search(r"#\s+(.+)", text)
    title = title_m.group(1) if title_m else slug
    desc_m = re.search(r"description:\s*(.+)", text)
    desc = desc_m.group(1) if desc_m else ""
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    if lang != "en":
        url = f"https://www.lovart.ai/{lang}/blog/{slug}"
    else:
        url = f"https://www.lovart.ai/blog/{slug}"
    return json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": title[:110], "description": desc[:160], "url": url,
        "author": {"@type": "Organization", "name": (config or {}).get("author", "Lovart")},
        "publisher": {"@type": "Organization", "name": "Lovart"},
        "datePublished": now, "dateModified": now, "inLanguage": lang
    }, ensure_ascii=False, indent=2)
