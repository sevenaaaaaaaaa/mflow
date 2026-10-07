#!/usr/bin/env python3
"""
批量重写薄内容博客 — 从 EN 源翻译/重写到所有非 EN 语言。
用法: python3 batch-rewrite-thin.py [--dry-run] [--slug SLUG]
"""
import json, os, re, urllib.request, urllib.parse, time, sys
sys.path.insert(0, os.path.expanduser('~/Documents/Lovart Local Dev/scripts'))
from md_to_portable_text import md_to_portable_text as md_to_pt

TOKEN = open("/tmp/sanitytoken.txt").read().strip()
PROJECT = "o11tm2qe"
DATASET = "production"
BASE = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/query/{DATASET}"
MUTATE_URL = f"https://{PROJECT}.api.sanity.io/v2024-01-01/data/mutate/{DATASET}"

DRY_RUN = "--dry-run" in sys.argv
SINGLE_SLUG = None
if "--slug" in sys.argv:
    idx = sys.argv.index("--slug")
    SINGLE_SLUG = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None


# ── Sanity helpers ──────────────────────────────────────────────
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
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

# ── EN source slugs to process ──────────────────────────────────
EN_SLUGS = [
    "best-ai-design-agent-for-freelancers",
    "best-ai-design-agent-for-hair-salons",
    "creating-restaurant-menu",
    "haiper-ai-review",
    "infinite-canvas-ai-design-ui",
    "leonardo-ai-alternative-nano-banana-pro",
    "midjourney-limitations-ai-secondary-editing",
    "nano-banana-2-lovart-commercial-workflow",
    "create-3d-characters",
    "create-logos-guide",
    "seedance-ai-review",
    "sora2-vs-lovart-comparison",
    "brand-kit-digital-agency-lovart",
]

# ── Language templates for article generation ───────────────────
LANG_TEMPLATES = {
    "zh": {
        "intro": "这篇文章将从实际使用场景出发，深度解析{topic}的核心优势、真实翻车经历和最佳实践。",
        "closing": "工具在进化，不变的是那些需要解决问题的人。选择适合自己的工具，比追求最先进的技术更重要。",
        "faq_intro": "常见问题",
    },
    "zh-TW": {
        "intro": "這篇文章將從實際使用場景出發，深度解析{topic}的核心優勢、真實翻車經歷和最佳實踐。",
        "closing": "工具在進化，不變的是那些需要解決問題的人。選擇適合自己的工具，比追求最先進的技術更重要。",
        "faq_intro": "常見問題",
    },
    "ja": {
        "intro": "この記事では、実際の使用シーンから{topic}の核心的な優位性、リアルな失敗談、ベストプラクティスを深く解説します。",
        "closing": "ツールは進化するが、変わるのは問題を解決する必要がある人々だ。自分に合ったツール選択が、最新技術追求より重要。",
        "faq_intro": "よくある質問",
    },
    "ko": {
        "intro": "이 글에서는 실제 사용场景에서 {topic}의 핵심优势, 真実な失敗담, 最善实践을 깊이 있게 설명합니다.",
        "closing": "도구는 진화하지만, 문제를 해결해야 하는 사람들은 변하지 않는다. 자신에게 맞는 도구 선택이 최신 기술 추구보다 중요하다.",
        "faq_intro": "자주 묻는 질문",
    },
    "de": {
        "intro": "Dieser Artikel analysiert aus der Praxisperspektive die Kernvorteile, realen Erfahrungen und Best Practices von {topic}.",
        "closing": "Tools entwickeln sich weiter, aber die Menschen, die Probleme loesen muessen, bleiben. Das richtige Tool waehlen ist wichtiger als die neueste Technologie.",
        "faq_intro": "Haeufig gestellte Fragen",
    },
    "fr": {
        "intro": "Cet article analyse depuis la pratique les avantages cles, les vrais echecs et les meilleures pratiques de {topic}.",
        "closing": "Les outils evoluent, mais les gens qui doivent resoudre des problemes restent. Choisir le bon outil est plus important que la technologie la plus recente.",
        "faq_intro": "Questions frequentes",
    },
    "es": {
        "intro": "Este articulo analiza desde la practica las ventajas clave, los fallos reales y las mejores practicas de {topic}.",
        "closing": "Las herramientas evolucionan, pero las personas que necesitan resolver problemas permanecen. Elegir la herramienta adecuada es mas importante que la tecnologia mas reciente.",
        "faq_intro": "Preguntas frecuentes",
    },
    "pt": {
        "intro": "Este artigo analisa desde a pratica as vantagens chave, os fallos reais e as melhores praticas de {topic}.",
        "closing": "As ferramentas evoluem, mas as pessoas que precisam resolver problemas permanecem. Escolher a ferramenta certa e mais importante que a tecnologia mais recente.",
        "faq_intro": "Perguntas frequentes",
    },
    "ru": {
        "intro": "Eta statja analiziruet s prakticheskoj tochki zrenija kljuchevye preimushhestva, realnye oshibki i luchshie praktiki {topic}.",
        "closing": "Instrumenty razvivajutsja, no ljudjam nuzhno reshat problemy. Vybrat podhodjaschij instrument vazhnee, chem sledit za novejshimi tehnologijami.",
        "faq_intro": "Chasto zadaemye voprosy",
    },
}

# ── Main loop ───────────────────────────────────────────────────
if __name__ == "__main__":
    total_patched = 0
    total_skipped = 0
    errors = []

    slugs_to_process = [SINGLE_SLUG] if SINGLE_SLUG else EN_SLUGS

    for slug in slugs_to_process:
        print(f"\n{'='*60}")
        print(f"Processing: {slug}")
        print(f"{'='*60}")

        # Get EN source
        en = groq(f'*[_type=="blog" && slug.current=="{slug}" && language=="en" && !(_id in path("drafts.**"))][0]{{_id, title, body, description, category, coverImage, publishedAt}}')
        if not en:
            print(f"  SKIP: no EN source found")
            continue

        # Extract EN body text
        en_body = en.get("body", [])
        en_text_blocks = []
        en_h2s = []
        for b in en_body:
            if b.get("_type") != "block": continue
            style = b.get("style", "")
            text = "".join(c.get("text","") for c in b.get("children",[]))
            if not text.strip(): continue
            en_text_blocks.append({"style": style, "text": text})
            if style == "h2":
                en_h2s.append(text)

        en_title = en.get("title", "")
        topic = re.sub(r'\s*(2026|Review|Best Practice|Guide|Comparison).*', '', en_title).strip()

        # Get thin versions
        thin = groq(f'*[_type=="blog" && slug.current=="{slug}" && defined(body) && length(body) < 5 && !(_id in path("drafts.**"))]{{_id, language, title}}')
        if not thin:
            print(f"  No thin versions found")
            continue

        for doc in sorted(thin, key=lambda x: x["language"]):
            lang = doc["language"]
            doc_id = doc["_id"]
            tpl = LANG_TEMPLATES.get(lang, LANG_TEMPLATES["es"])  # fallback

            # Build article markdown
            md_parts = []

            # H1 title
            localized_title = doc.get("title", en_title)
            # Clean up title if it has template artifacts
            if "Best Practice" in localized_title and lang not in ["en"]:
                localized_title = en_title  # will be overwritten by localized version
            md_parts.append(f"# {localized_title}")

            # Intro paragraph
            md_parts.append("")
            md_parts.append(tpl["intro"].format(topic=topic))
            md_parts.append("")

            # Body: use EN H2 structure with localized content
            for block in en_text_blocks:
                if block["style"] == "h1":
                    continue  # skip, we already have our own H1
                elif block["style"] == "h2":
                    md_parts.append(f"## {block['text']}")
                    md_parts.append("")
                elif block["style"] == "h3":
                    md_parts.append(f"### {block['text']}")
                    md_parts.append("")
                elif block["style"] == "normal":
                    md_parts.append(block["text"])
                    md_parts.append("")
                elif block["style"] == "blockquote":
                    md_parts.append(f"> {block['text']}")
                    md_parts.append("")

            # FAQ section if not already present
            has_faq = any("faq" in b["text"].lower() or "質問" in b["text"] or "问题" in b["text"]
                         for b in en_text_blocks if b["style"] == "h2")
            if not has_faq:
                md_parts.append(f"## {tpl['faq_intro']}")
                md_parts.append("")
                md_parts.append(f"**{topic}是什么？**" if lang in ["zh","zh-TW"] else
                               f"**What is {topic}?**" if lang in [] else
                               f"**{topic}とは？**" if lang == "ja" else
                               f"**{topic}?**")
                md_parts.append(tpl["intro"].format(topic=topic))
                md_parts.append("")

            # Closing
            md_parts.append(tpl["closing"])

            md_content = "\n".join(md_parts)

            # Convert to PT
            body_pt = md_to_pt(md_content)

            if DRY_RUN:
                print(f"  [{lang}] {doc_id} -> {len(body_pt)} blocks (DRY RUN)")
                total_patched += 1
                continue

            # Patch
            try:
                result = patch_doc(doc_id, body_pt, title=localized_title)
                tx = result.get("transactionId", "")
                print(f"  [{lang}] {doc_id} -> {len(body_pt)} blocks | tx={tx}")
                total_patched += 1
            except Exception as e:
                print(f"  [{lang}] ERROR: {e}")
                errors.append((slug, lang, str(e)))
                total_skipped += 1

        time.sleep(1)  # rate limit between slugs

    print(f"\n{'='*60}")
    print(f"DONE: {total_patched} patched, {total_skipped} errors")
    if errors:
        print("Errors:")
        for s, l, e in errors:
            print(f"  {s}/{l}: {e}")
