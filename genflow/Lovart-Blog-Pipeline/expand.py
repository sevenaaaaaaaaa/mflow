"""Expand outline bullets into full paragraphs for 101 articles."""

from __future__ import annotations

SHORT_BRIDGE = (
    "On **ChatCanvas**, Lovart's **Design Agent** applies **MCoT** planning, "
    "**Brand Kit** rules when configured, and semantic edits (**Touch Edit**, "
    "**Text Edit**, **Edit Elements**) before you pay for a full reroll."
)


def expand_bullet(bullet: str, context: str, *, include_bridge: bool) -> str:
    b = bullet.strip()
    if not b.endswith("."):
        b += "."
    ctx = context.strip()
    if ctx and not ctx.endswith("."):
        ctx += "."
    tail = f" {SHORT_BRIDGE}" if include_bridge else ""
    return (
        f"{b} {ctx} "
        "Treat references as contracts, document approvals in the chat thread, "
        "and export with channel-specific filenames so media buyers do not guess crop or color at the last mile. "
        "When results drift, inspect the MCoT plan in Thinking Mode, adjust Brand Kit or references, "
        "then prefer Touch Edit or Text Edit over a full reroll."
        f"{tail}"
    )


def bullets_to_paragraphs(bullets: list[str], contexts: list[str]) -> list[str]:
    if not contexts:
        contexts = ["This step maps directly to Lovart production workflows on ChatCanvas."]
    if len(contexts) < len(bullets):
        contexts = contexts + [contexts[-1]] * (len(bullets) - len(contexts))
    return [
        expand_bullet(b, c, include_bridge=(i == len(bullets) - 1))
        for i, (b, c) in enumerate(zip(bullets, contexts))
    ]
