"""Assemble Lovart 101 markdown bodies from structured sections."""

from __future__ import annotations

from ..lovart_101_common import closing_blocks


def join_paragraphs(paragraphs: list[str]) -> str:
    return "\n\n".join(p.strip() for p in paragraphs if p.strip())


def render_subsections(subsections: list[tuple[str, list[str]]]) -> str:
    parts: list[str] = []
    for h3, paras in subsections:
        parts.append(f"### {h3}\n\n{join_paragraphs(paras)}")
    return "\n\n".join(parts)


def render_steps(steps: list[tuple[str, list[str]]]) -> str:
    lines: list[str] = []
    for i, (title, paras) in enumerate(steps, 1):
        lines.append(f"### Step {i}: {title}\n\n{join_paragraphs(paras)}")
    return "\n\n".join(lines)


def build_body(
    h1: str,
    hook: str,
    image1: str,
    part1_title: str,
    part1_subs: list[tuple[str, list[str]]],
    part2_title: str,
    part2_subs: list[tuple[str, list[str]]],
    part3_title: str,
    steps: list[tuple[str, list[str]]],
    cluster: str,
    derivative: list[str],
    faq: list[tuple[str, str]],
    extra_links: list[tuple[str, str]] | None = None,
    images: list[tuple[str, str]] | None = None,
) -> str:
    return f"""# {h1}

{hook}

{image1}

---

## {part1_title}

{render_subsections(part1_subs)}

---

## {part2_title}

{render_subsections(part2_subs)}

---

## {part3_title}

{render_steps(steps)}

{closing_blocks(cluster, derivative, faq, extra_links, images)}
"""
