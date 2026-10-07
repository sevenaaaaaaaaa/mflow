#!/usr/bin/env python3
"""Build a non-destructive, categorized website-upload staging area from Drafts."""

from __future__ import annotations

import csv
import hashlib
import re
import shutil
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Website-Ready"
PLATFORM_MARKERS = (
    "知乎", "百家", "zhihu", "baijia", "什么值得买", "全链接",
    "英文版", "51cto", "quora", "专栏版", "csdn版", "掘金版",
)
CONTENT_HOSTS = {
    "ahhhhfs.com", "www.ahhhhfs.com", "nownexts.com", "www.nownexts.com",
    "mp.weixin.qq.com", "appinn.com", "www.appinn.com", "waerfa.com",
    "www.waerfa.com", "appmiu.com", "www.appmiu.com", "utgd.net",
    "www.utgd.net", "macwf.com", "www.macwf.com",
}
BRAND_PATTERNS = (
    r"\s*[-–—｜|]\s*A姐分享(?:｜AI\s*工具、开源项目与效率软件)?",
    r"\s*[-–—｜|]\s*Mac玩儿法(?:\s*[|｜].*)?",
)
SITE_JUNK = re.compile(
    r"^(?:上一篇|下一篇|相关推荐|相关文章|猜你喜欢|评论建议|详情介绍|"
    r"返回首页|网站地图|热门文章|最新文章|扫码关注|关注公众号)\s*[:：]?",
    re.I,
)


def is_platform_variant(path: Path) -> bool:
    stem = path.stem.lower()
    return any(marker in stem for marker in PLATFORM_MARKERS)


def article_dirs(section: Path) -> list[Path]:
    result = []
    for directory in section.rglob("*"):
        if not directory.is_dir() or not directory.name[:1].isdigit():
            continue
        if any(p.is_file() for p in directory.glob("*.md")):
            result.append(directory)
    return sorted(result)


def canonical_candidates(directory: Path) -> list[Path]:
    return [
        p for p in directory.glob("*.md")
        if p.is_file() and p.name != "00-选品.md" and not is_platform_variant(p)
    ]


def choose_master(directory: Path) -> tuple[Path | None, str]:
    candidates = canonical_candidates(directory)
    if not candidates:
        return None, "no-platform-neutral-file"
    typed = [p for p in candidates if p.stem.startswith(("T1-", "T2-", "T3-"))]
    pool = typed or candidates
    if len(pool) == 1:
        return pool[0], "unique-typed-master" if typed else "unique-neutral-file"

    # Prefer the neutral base that has the most platform-specific siblings.
    all_md = [p for p in directory.glob("*.md") if p.is_file()]
    def score(path: Path) -> tuple[int, int, int, str]:
        base = path.stem
        sibling_variants = sum(
            1 for other in all_md
            if other != path and other.stem.startswith(base) and is_platform_variant(other)
        )
        return (sibling_variants, int(path.stem.startswith(("T1-", "T2-", "T3-"))), len(path.stem), path.name)

    return max(pool, key=score), f"heuristic-from-{len(pool)}-neutral-files"


def strip_brand(text: str) -> str:
    for pattern in BRAND_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.I)
    return text.strip()


def url_host(url: str) -> str:
    return urlparse(url).netloc.lower()


def clean_legacy(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    lines = text.splitlines()
    cleaned: list[str] = []
    in_frontmatter = bool(lines and lines[0].strip() == "---")
    fm_end_seen = False

    for line in lines:
        if in_frontmatter and not fm_end_seen and line.strip() == "---" and cleaned:
            fm_end_seen = True
            cleaned.append(line)
            continue

        if in_frontmatter and not fm_end_seen:
            field = re.match(r"^(source|author|original_url|site)\s*:\s*(.*)$", line, re.I)
            if field:
                value = field.group(2).strip().strip('"\'')
                urls = re.findall(r"https?://[^\s\]\)>\"']+", value)
                if field.group(1).lower() != "source" or any(url_host(u) in CONTENT_HOSTS for u in urls):
                    changes.append("removed-source-site-frontmatter")
                    continue

        if SITE_JUNK.match(line.strip()):
            changes.append("removed-site-navigation")
            continue

        urls = re.findall(r"https?://[^\s\]\)>\"']+", line)
        if urls and any(url_host(u) in CONTENT_HOSTS for u in urls):
            if re.match(r"^\s*(?:[-*]\s*)?(?:来源|原文|转载|文章链接|本文地址)\s*[:：]", line, re.I):
                changes.append("removed-source-site-line")
                continue
            if re.search(r"!\[[^]]*]\([^)]*\)", line):
                changes.append("removed-source-site-image")
                continue

            # Keep the anchor wording but remove links to the old publisher.
            old = line
            line = re.sub(
                r"\[([^]]+)]\((https?://[^)]+)\)",
                lambda m: m.group(1) if url_host(m.group(2).split()[0].strip('"\'')) in CONTENT_HOSTS else m.group(0),
                line,
            )
            line = re.sub(
                r"https?://[^\s\]\)>\"']+",
                lambda m: "" if url_host(m.group(0)) in CONTENT_HOSTS else m.group(0),
                line,
            )
            if line != old:
                changes.append("removed-source-site-link")

        old = line
        line = strip_brand(line)
        if line != old.strip():
            changes.append("removed-source-brand")
        cleaned.append(line.rstrip())

    result = "\n".join(cleaned).strip() + "\n"
    result = re.sub(r"\n{4,}", "\n\n\n", result)
    return result, sorted(set(changes))


def normalized_hash(text: str) -> str:
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    body = re.sub(r"\s+", "", body).lower()
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def safe_name(name: str) -> str:
    name = strip_brand(name)
    name = re.sub(r"_1(?:_1)?(?=\.md$)", "", name)
    return name


def residual_flags(text: str) -> list[str]:
    flags = []
    lowered = text.lower()
    for host in CONTENT_HOSTS:
        if host in lowered:
            flags.append(f"publisher-domain:{host}")
    for brand in ("a姐分享", "mac玩儿法", "来源：nownexts.com", "来源: nownexts.com"):
        if brand in lowered:
            flags.append(f"publisher-brand:{brand}")
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S).strip()
    if len(body) < 500:
        flags.append("short-body")
    return sorted(set(flags))


def copy_assets(source_dir: Path, target_dir: Path) -> int:
    count = 0
    for item in source_dir.iterdir():
        if item.suffix.lower() == ".md" or item.name.startswith("00-"):
            continue
        target = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
            count += sum(1 for x in item.rglob("*") if x.is_file())
        elif item.is_file():
            shutil.copy2(item, target)
            count += 1
    return count


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    rows: list[dict[str, str]] = []
    seen: dict[str, str] = {}
    counts = Counter()

    for section, label in (("Daily", "01-Daily-新稿"), ("Cluster", "02-Cluster-专题")):
        base = ROOT / section
        for directory in article_dirs(base):
            master, rule = choose_master(directory)
            if not master:
                rows.append({"status": "excluded", "source": str(directory.relative_to(ROOT)), "output": "", "reason": rule})
                counts["excluded"] += 1
                continue
            text = master.read_text(encoding="utf-8", errors="replace")
            digest = normalized_hash(text)
            rel_dir = directory.relative_to(base)
            category = rel_dir.parts[0] if section == "Cluster" and len(rel_dir.parts) > 1 else "未分类"
            article_folder = rel_dir.name
            target_dir = OUT / label / category / article_folder
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / "article.md"
            if digest in seen:
                rows.append({"status": "duplicate", "source": str(master.relative_to(ROOT)), "output": seen[digest], "reason": "same-body"})
                counts["duplicate"] += 1
                shutil.rmtree(target_dir)
                continue
            target.write_text(text, encoding="utf-8")
            assets = copy_assets(directory, target_dir)
            seen[digest] = str(target.relative_to(ROOT))
            rows.append({"status": "ready", "source": str(master.relative_to(ROOT)), "output": str(target.relative_to(ROOT)), "reason": f"{rule};assets={assets}"})
            counts[f"{section.lower()}_ready"] += 1

    tags = ROOT / "Tags"
    for source in sorted(p for p in tags.rglob("*.md") if p.is_file()):
        text = source.read_text(encoding="utf-8", errors="replace")
        cleaned, changes = clean_legacy(text)
        flags = residual_flags(cleaned)
        digest = normalized_hash(cleaned)
        relative = source.relative_to(tags)
        target_rel = relative.with_name(safe_name(relative.name))
        status = "review" if flags else "ready"
        lane = "04-Tags-需人工复核" if flags else "03-Tags-历史稿-已清洗"
        target = OUT / lane / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if digest in seen:
            rows.append({"status": "duplicate", "source": str(source.relative_to(ROOT)), "output": seen[digest], "reason": "same-body-after-cleaning"})
            counts["duplicate"] += 1
            continue
        target.write_text(cleaned, encoding="utf-8")
        seen[digest] = str(target.relative_to(ROOT))
        reason = ";".join(changes + flags) or "no-publisher-trace-detected"
        rows.append({"status": status, "source": str(source.relative_to(ROOT)), "output": str(target.relative_to(ROOT)), "reason": reason})
        counts[f"tags_{status}"] += 1

    manifest = OUT / "manifest.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("status", "source", "output", "reason"))
        writer.writeheader()
        writer.writerows(rows)

    report = f"""# 网站稿件盘点与整理结果

本目录由 `organize_website_ready.py` 非破坏性生成；原始 `Daily`、`Cluster`、`Tags` 均未改动。

## 结论

- Daily 新稿可上传：{counts['daily_ready']} 篇。
- Cluster 专题可上传：{counts['cluster_ready']} 篇。
- Tags 历史稿清洗后可上传：{counts['tags_ready']} 篇。
- Tags 仍需人工复核：{counts['tags_review']} 篇。
- 跨来源重复稿：{counts['duplicate']} 篇，未重复复制。
- 因缺少平台中性正文而排除：{counts['excluded']} 个目录。

## 目录说明

- `01-Daily-新稿/`：每个序号目录仅保留一个平台中性正文，标准 T1/T2/T3 母版优先。
- `02-Cluster-专题/`：按原 Cluster 主题分类保留，每个序号目录只取一个母版。
- `03-Tags-历史稿-已清洗/`：已移除可识别的旧发布站品牌、导航、评论、来源站链接和图片热链。
- `04-Tags-需人工复核/`：仍有旧发布站域名/品牌，或正文少于 500 字符。
- `manifest.csv`：逐篇记录来源、输出、状态、选择或清洗原因。

## 上传边界

`ready` 表示已完成本轮结构和旧站痕迹筛查，不代表事实准确性、版权、链接有效性或网站 CMS 字段已经通过最终发布质检。实际上传前仍需跑网站侧 schema、标题、slug、摘要、图片和版权检查。
"""
    (OUT / "README.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
