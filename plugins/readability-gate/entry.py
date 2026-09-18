"""readability-gate: Flesch Reading Ease scoring gate (EN only)"""
import re

def check(file_path, lang="en", config=None):
    max_score = (config or {}).get("max_score", 12)
    if lang != "en":
        return {"rc": 0, "out": f"[readability] skip (lang={lang}, only EN scored)"}
    text = open(file_path, encoding="utf-8").read()
    if text.startswith("---"):
        text = text.split("---", 2)[-1] if text.count("---") >= 2 else text
    text = re.sub(r"^#+ .*", "", text, flags=re.M)
    text = re.sub(r"```[\s\S]*?```", "", text)
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if len(s.strip()) > 5]
    words = re.findall(r"[A-Za-z]+", text)
    if not sentences or not words:
        return {"rc": 0, "out": "[readability] insufficient content"}
    syllables = sum(max(1, len(re.findall(r"[aeiouAEIOU]", w))) for w in words)
    flesch = 206.835 - 1.015 * (len(words) / len(sentences)) - 1.455 * (syllables / len(words))
    if flesch > max_score:
        return {"rc": 1, "out": f"Flesch {flesch:.1f} > {max_score} — too complex"}
    return {"rc": 0, "out": f"Flesch={flesch:.1f} <= {max_score}"}
