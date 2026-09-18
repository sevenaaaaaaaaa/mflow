"""link-suggester: analyze(data) -> {suggestions: [...]}"""
import json, math, re
from pathlib import Path

def analyze(data, config=None):
    text = data.get("text", "")[:3000]
    library_path = data.get("library_path", "/www/wwwroot/mflow/run/library/lovart-global")
    top = (config or {}).get("top", 5)
    t = text.lower()
    words = set(re.findall(r"[a-z0-9]{3,}", t))
    cjk = re.findall(r"[\u4e00-\u9fff]", t)
    bigrams = {"".join(cjk[i:i + 2]) for i in range(len(cjk) - 1)}
    dt = words | bigrams
    if not dt:
        return {"suggestions": [], "note": "no tokens"}
    base = Path(library_path)
    if not base.exists():
        return {"suggestions": [], "note": "library not found"}
    hits = []
    for f in base.rglob("*.md"):
        if f.name.startswith("_"):
            continue
        name_t = set(re.findall(r"[a-z0-9]{3,}", f.stem.lower()))
        overlap = len(dt & name_t)
        if overlap < 2:
            continue
        hits.append((overlap * math.log(1 + overlap), f))
    hits.sort(key=lambda x: -x[0])
    return {"suggestions": [{"slug": f.stem, "path": str(f), "relevance": round(s, 1)}
                            for s, f in hits[:top]]}
