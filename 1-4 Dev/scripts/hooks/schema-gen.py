#!/usr/bin/env python3
"""schema-gen.py — 从 composite/blog doc 自动生成 Schema.org JSON-LD。
Usage: python3 schema-gen.py --file draft.md --type blog|composite --slug s --lang en --title T
Output: JSON-LD string to stdout"""
import json, re, sys, argparse
from pathlib import Path
from datetime import datetime

def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m: return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" not in line: continue
        k, v = line.split(":", 1); fm[k.strip()] = v.strip().strip("\"'")
    return fm

def generate(doc_type, title, description, slug, lang, author="Lovart", image_url=""):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    if doc_type == "blog":
        ld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title[:110],
            "description": description[:160],
            "url": f"https://www.lovart.ai/{lang}/blog/{slug}" if lang != "en" else f"https://www.lovart.ai/blog/{slug}",
            "author": {"@type": "Organization", "name": author},
            "publisher": {"@type": "Organization", "name": "Lovart", "logo": {"@type": "ImageObject", "url": "https://www.lovart.ai/logo.png"}},
            "datePublished": now,
            "dateModified": now,
            "inLanguage": lang,
        }
        if lang in ("zh", "zh-TW", "ja", "ko"):
            kb_type = "HowTo"
        else:
            kb_type = "Article"
        ld["@type"] = "Article"
    elif doc_type in ("composite", "compositePage"):
        ld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title[:110],
            "description": description[:160],
            "url": f"https://www.lovart.ai/{'/' + lang if lang != 'en' else ''}/{doc_type}/{slug}",
            "inLanguage": lang,
        }
    else:
        ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": f"https://www.lovart.ai/{slug}"}
    return ld

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--type", default="blog")
    ap.add_argument("--slug", default="")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--title", default="")
    ap.add_argument("--description", default="")
    a = ap.parse_args()
    text = open(a.file, encoding="utf-8").read()
    fm = parse_fm(text)
    slug = a.slug or fm.get("slug", "untitled")
    title = a.title or fm.get("title", slug)
    desc = a.description or fm.get("description", "")
    ld = generate(a.type, title, desc, slug, a.lang)
    print(json.dumps(ld, ensure_ascii=False, indent=2))
