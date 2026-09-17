#!/usr/bin/env python3
"""Markdown to Sanity Portable Text converter with full inline formatting support.

Handles:
- ##/###/#### headings
- **bold**, *italic*, ***bold+italic***
- `inline code`
- [link text](url)
- ![alt](image_url)
- Numbered lists (1. ...)
- Bullet lists (- ... or * ...)
- Blockquotes (> ...)
- Horizontal rules (---, ***, ___)
- Code blocks (```)
- Tables (| col1 | col2 |)
- Paragraphs (auto-merged consecutive non-empty lines)

Portable Text block structure:
{
  "_type": "block",
  "_key": "<random>",
  "style": "normal|h1|h2|h3|h4|blockquote",
  "children": [
    {"_type": "span", "_key": "<random>", "text": "...", "marks": ["strong"]},
    {"_type": "span", "_key": "<random>", "text": "...", "marks": ["em"]},
    {"_type": "a", "_key": "<random>", "href": "https://...", "_type": "link"},
  ],
  "markDefs": [{"_key": "link-<n>", "_type": "link", "href": "..."}]
}

Table structure (Lovart production schema SSOT — @sanity/table):
{
  "_type": "table",
  "_key": "<random>",
  "rows": [
    {
      "_type": "tableRow",
      "_key": "<random>",
      "cells": ["col1 text", "col2 text"]   # plain strings, NOT objects
    }
  ]
}

HARD RULES (2026-08-03 corrected against deployed schema):
- cells MUST be string[]; never tableCell / block / span trees
- table + tableRow MUST have _key; string cells have no _key
- Do NOT invent tableCell — it is not in o11tm2qe schema
"""

import re
import uuid


def _key():
    """Generate a short random key for Portable Text."""
    return uuid.uuid4().hex[:12]


def _parse_inline(text):
    """Parse inline markdown into Portable Text spans and markDefs.
    
    Uses a simple state machine (no regex) to avoid catastrophic backtracking.
    Returns (spans, markDefs).
    """
    spans = []
    markDefs = []
    link_counter = [0]
    i = 0
    n = len(text)
    
    def add_text(t):
        if t:
            spans.append({"_type": "span", "_key": _key(), "text": t})
    
    while i < n:
        # Inline code `...`
        if text[i] == '`':
            end = text.find('`', i + 1)
            if end > 0:
                spans.append({"_type": "span", "_key": _key(), "text": text[i+1:end], "marks": ["code"]})
                i = end + 1
                continue
        
        # Bold+italic ***...***
        if text[i:i+3] == '***':
            end = text.find('***', i + 3)
            if end > 0:
                spans.append({"_type": "span", "_key": _key(), "text": text[i+3:end], "marks": ["strong", "em"]})
                i = end + 3
                continue
        
        # Bold **...**
        if text[i:i+2] == '**':
            end = text.find('**', i + 2)
            if end > 0:
                spans.append({"_type": "span", "_key": _key(), "text": text[i+2:end], "marks": ["strong"]})
                i = end + 2
                continue
        
        # Italic *...* (but not ** or ***)
        if text[i] == '*' and (i + 1 < n and text[i+1] != '*'):
            end = text.find('*', i + 1)
            if end > 0 and end > i + 1:
                spans.append({"_type": "span", "_key": _key(), "text": text[i+1:end], "marks": ["em"]})
                i = end + 1
                continue
        
        # Link [text](url)
        if text[i] == '[':
            bracket_end = text.find(']', i + 1)
            if bracket_end > 0 and bracket_end + 1 < n and text[bracket_end + 1] == '(':
                paren_end = text.find(')', bracket_end + 2)
                if paren_end > 0:
                    link_text = text[i+1:bracket_end]
                    link_url = text[bracket_end+2:paren_end]
                    link_key = f"link-{link_counter[0]}"
                    link_counter[0] += 1
                    markDefs.append({"_key": link_key, "_type": "link", "href": link_url})
                    spans.append({"_type": "span", "_key": _key(), "text": link_text, "marks": [link_key]})
                    i = paren_end + 1
                    continue
        
        # Image ![alt](url) - treat as text placeholder
        if text[i:i+2] == '![':
            bracket_end = text.find(']', i + 2)
            if bracket_end > 0 and bracket_end + 1 < n and text[bracket_end + 1] == '(':
                paren_end = text.find(')', bracket_end + 2)
                if paren_end > 0:
                    alt = text[i+2:bracket_end] or "image"
                    spans.append({"_type": "span", "_key": _key(), "text": f"[{alt}]"})
                    i = paren_end + 1
                    continue
        
        # Plain text - collect until next special char
        j = i + 1
        while j < n and text[j] not in ('`', '*', '[', '!'):
            j += 1
        add_text(text[i:j])
        i = j
    
    if not spans and text:
        add_text(text)
    
    return spans, markDefs


def _strip_frontmatter(md_text):
    """Strip YAML frontmatter (--- delimited) from the beginning of markdown."""
    if md_text.startswith('---'):
        # Find the closing ---
        end = md_text.find('---', 3)
        if end > 0:
            return md_text[end + 3:].lstrip('\n')
    return md_text


def _is_table_row(line):
    """Check if a line is a Markdown table row (| col | col |)."""
    stripped = line.strip()
    if not stripped.startswith('|') or not stripped.endswith('|'):
        return False
    # Must have non-empty content between pipes
    inner = stripped[1:-1].strip()
    return len(inner) > 0


def _is_table_separator(line):
    """Check if a line is a table separator (| --- | --- |)."""
    stripped = line.strip()
    if not _is_table_row(stripped):
        return False
    # Remove pipes and check if remaining is all dashes/spaces/colons
    inner = stripped[1:-1]
    cells = inner.split('|')
    for cell in cells:
        cell_stripped = cell.strip()
        if cell_stripped and not re.match(r'^[-:]+$', cell_stripped):
            return False
    return True


def _parse_table_row(line):
    """Parse a table row into cell texts."""
    stripped = line.strip()
    # Remove leading and trailing pipes
    inner = stripped[1:-1]
    # Split by pipe
    cells = inner.split('|')
    return [cell.strip() for cell in cells]


def _plain_cell_text(text):
    """Collapse markdown inline markup to plain string for schema string cells."""
    if text is None:
        return ""
    t = str(text)
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", t)
    t = re.sub(r"___(.+?)___", r"\1", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"__(.+?)__", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"_(.+?)_", r"\1", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    t = re.sub(r"\[(.+?)\]\([^)]+\)", r"\1", t)
    return t.strip()


def _make_table_block(rows_data):
    """Create a Lovart-schema table block: cells are plain strings."""
    rows = []
    for row_cells in rows_data:
        cells = [_plain_cell_text(cell_text) for cell_text in row_cells]
        rows.append({
            "_type": "tableRow",
            "_key": _key(),
            "cells": cells,
        })
    return {
        "_type": "table",
        "_key": _key(),
        "rows": rows,
    }


def count_key_issues(nodes, path="body"):
    """Recursively find typed Portable Text nodes missing _key.

    String table cells are schema-valid and are not checked for _key.
    Returns list of path strings.
    """
    issues = []

    def walk(obj, cur):
        if isinstance(obj, dict):
            typ = obj.get("_type")
            if typ and not obj.get("_key"):
                issues.append(f"{cur}._type={typ} MISSING _key")
            for k, v in obj.items():
                if k in ("children", "rows", "cells", "markDefs"):
                    walk(v, f"{cur}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                # schema: tableRow.cells is string[] — skip primitives
                if isinstance(v, (str, int, float, bool)) or v is None:
                    continue
                walk(v, f"{cur}[{i}]")

    walk(nodes, path)
    return issues


def validate_portable_text_body(blocks):
    """Validate Lovart blog body PT structure. Returns {ok, issues}.

    Checks:
    1. every typed node has _key (except string cells)
    2. table cells are plain strings (BLOCK if object / tableCell / block)
    3. table/tableRow have _type + _key
    4. non-code span.text must not carry layout newlines
       (leading/trailing \\n, \\n{3,}, or embedded \\n\\n) — AB-NEWLINES
    """
    if not isinstance(blocks, list):
        return {"ok": False, "issues": ["body is not a list"]}

    issues = []
    issues.extend(count_key_issues(blocks))

    for bi, blk in enumerate(blocks):
        if not isinstance(blk, dict):
            issues.append(f"body[{bi}] is not an object")
            continue

        # Span newline pollution (skip fenced-code spans that legitimately keep \n)
        if blk.get("_type") == "block":
            for ci, child in enumerate(blk.get("children") or []):
                if not isinstance(child, dict):
                    continue
                text = child.get("text")
                if not isinstance(text, str) or not text:
                    continue
                marks = child.get("marks") or []
                if "code" in marks:
                    continue
                if text != text.strip("\n"):
                    issues.append(
                        f"body[{bi}].children[{ci}].text has leading/trailing newlines (AB-NEWLINES)"
                    )
                elif re.search(r"\n{3,}", text):
                    issues.append(
                        f"body[{bi}].children[{ci}].text has \\n{{3,}} runs (AB-NEWLINES)"
                    )
                elif "\n\n" in text:
                    issues.append(
                        f"body[{bi}].children[{ci}].text embeds \\n\\n blank line (AB-NEWLINES)"
                    )

        if blk.get("_type") != "table":
            continue
        if not blk.get("_key"):
            issues.append(f"body[{bi}].table MISSING _key")
        rows = blk.get("rows") or []
        if not isinstance(rows, list) or not rows:
            issues.append(f"body[{bi}].table has empty/invalid rows")
            continue
        for ri, row in enumerate(rows):
            if not isinstance(row, dict):
                issues.append(f"body[{bi}].rows[{ri}] is not an object")
                continue
            if row.get("_type") != "tableRow":
                issues.append(f"body[{bi}].rows[{ri}] _type!={row.get('_type')!r} (want tableRow)")
            if not row.get("_key"):
                issues.append(f"body[{bi}].rows[{ri}] MISSING _key")
            cells = row.get("cells")
            if not isinstance(cells, list):
                issues.append(f"body[{bi}].rows[{ri}].cells is not a list")
                continue
            for ci, cell in enumerate(cells):
                if isinstance(cell, str):
                    continue
                if isinstance(cell, dict):
                    ctype = cell.get("_type")
                    issues.append(
                        f"body[{bi}].rows[{ri}].cells[{ci}] is object _type={ctype!r} "
                        f"(schema requires string)"
                    )
                else:
                    issues.append(
                        f"body[{bi}].rows[{ri}].cells[{ci}] type={type(cell).__name__} "
                        f"(schema requires string)"
                    )

    return {"ok": len(issues) == 0, "issues": issues}


def md_to_portable_text(md_text):
    """Convert Markdown string to Sanity Portable Text blocks.
    
    Full support for:
    - Headings (##/###/####)
    - Bold (**text**), italic (*text*), bold+italic (***text***)
    - Inline code (`code`)
    - Links [text](url)
    - Images ![alt](url) (as standalone blocks)
    - Numbered lists
    - Bullet lists
    - Blockquotes (> ...)
    - Code blocks (```)
    - Tables (| col1 | col2 |)
    - Horizontal rules
    - Paragraphs
    """
    if not md_text or not md_text.strip():
        return []
    
    # Strip YAML frontmatter if present
    md_text = _strip_frontmatter(md_text)
    
    blocks = []
    lines = md_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
        
        # Horizontal rule
        if line.strip() in ('---', '***', '___') and len(line.strip()) >= 3:
            i += 1
            continue
        
        # Code block (```)
        if line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # skip closing ```
            code_text = '\n'.join(code_lines)
            if code_text:
                blocks.append({
                    "_type": "block",
                    "_key": _key(),
                    "style": "normal",
                    "children": [{
                        "_type": "span",
                        "_key": _key(),
                        "text": code_text,
                        "marks": ["code"],
                    }],
                    "markDefs": [],
                })
            continue
        
        # H1 heading
        if line.startswith('# ') and not line.startswith('## '):
            heading_text = line[2:].strip()
            spans, markDefs = _parse_inline(heading_text)
            blocks.append({
                "_type": "block",
                "_key": _key(),
                "style": "h1",
                "children": spans,
                "markDefs": markDefs,
            })
            i += 1
            continue
        
        # H2 heading
        if line.startswith('## '):
            heading_text = line[3:].strip()
            spans, markDefs = _parse_inline(heading_text)
            blocks.append({
                "_type": "block",
                "_key": _key(),
                "style": "h2",
                "children": spans,
                "markDefs": markDefs,
            })
            i += 1
            continue
        
        # H3 heading
        if line.startswith('### '):
            heading_text = line[4:].strip()
            spans, markDefs = _parse_inline(heading_text)
            blocks.append({
                "_type": "block",
                "_key": _key(),
                "style": "h3",
                "children": spans,
                "markDefs": markDefs,
            })
            i += 1
            continue
        
        # H4 heading
        if line.startswith('#### '):
            heading_text = line[5:].strip()
            spans, markDefs = _parse_inline(heading_text)
            blocks.append({
                "_type": "block",
                "_key": _key(),
                "style": "h4",
                "children": spans,
                "markDefs": markDefs,
            })
            i += 1
            continue
        
        # Blockquote (> ...)
        if line.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:].strip())
                i += 1
            quote_text = ' '.join(quote_lines)
            spans, markDefs = _parse_inline(quote_text)
            blocks.append({
                "_type": "block",
                "_key": _key(),
                "style": "blockquote",
                "children": spans,
                "markDefs": markDefs,
            })
            continue
        
        # Table (| col1 | col2 |)
        if _is_table_row(line):
            rows_data = []
            while i < len(lines) and _is_table_row(lines[i]):
                if not _is_table_separator(lines[i]):
                    rows_data.append(_parse_table_row(lines[i]))
                i += 1
            if rows_data:
                blocks.append(_make_table_block(rows_data))
            continue
        
        # Numbered list (1. ...)
        if re.match(r'^\d+\.\s', line):
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                item_text = re.sub(r'^\d+\.\s+', '', lines[i]).strip()
                i += 1
                # Collect continuation lines (non-empty, non-heading, non-list)
                while (i < len(lines) and lines[i].strip()
                       and not lines[i].startswith('#')
                       and not re.match(r'^\d+\.\s', lines[i])
                       and not lines[i].startswith('- ')
                       and not lines[i].startswith('* ')
                       and not lines[i].startswith('> ')
                       and not _is_table_row(lines[i])):
                    item_text += ' ' + lines[i].strip()
                    i += 1
                spans, markDefs = _parse_inline(item_text)
                blocks.append({
                    "_type": "block",
                    "_key": _key(),
                    "style": "normal",
                    "children": spans,
                    "markDefs": markDefs,
                    "listItem": "number",
                })
            continue
        
        # Bullet list (- ... or * ...)
        if line.startswith('- ') or line.startswith('* '):
            bullet_char = line[0]
            while i < len(lines) and lines[i].startswith(bullet_char + ' '):
                item_text = lines[i][2:].strip()
                i += 1
                while (i < len(lines) and lines[i].strip()
                       and not lines[i].startswith('#')
                       and not re.match(r'^\d+\.\s', lines[i])
                       and not lines[i].startswith('- ')
                       and not lines[i].startswith('* ')
                       and not lines[i].startswith('> ')
                       and not _is_table_row(lines[i])):
                    item_text += ' ' + lines[i].strip()
                    i += 1
                spans, markDefs = _parse_inline(item_text)
                blocks.append({
                    "_type": "block",
                    "_key": _key(),
                    "style": "normal",
                    "children": spans,
                    "markDefs": markDefs,
                    "listItem": "bullet",
                })
            continue
        
        # Image on its own line (![alt](url))
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', line)
        if img_match:
            alt_text = img_match.group(1) or "image"
            img_url = img_match.group(2)
            blocks.append({
                "_type": "block",
                "_key": _key(),
                "style": "normal",
                "children": [{
                    "_type": "span",
                    "_key": _key(),
                    "text": f"[Image: {alt_text}]",
                }],
                "markDefs": [],
            })
            i += 1
            continue
        
        # Regular paragraph — collect until blank line or next heading/list/table
        para_lines = [line.strip()]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if (not next_line.strip()
                or next_line.startswith('#')
                or re.match(r'^\d+\.\s', next_line)
                or next_line.startswith('- ')
                or next_line.startswith('* ')
                or next_line.startswith('> ')
                or next_line.strip().startswith('```')
                or next_line.strip() in ('---', '***', '___')
                or _is_table_row(next_line)):
                break
            para_lines.append(next_line.strip())
            i += 1
        
        para_text = ' '.join(para_lines)
        if para_text:
            spans, markDefs = _parse_inline(para_text)
            blocks.append({
                "_type": "block",
                "_key": _key(),
                "style": "normal",
                "children": spans,
                "markDefs": markDefs,
            })
    
    return blocks


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            md = f.read()
    else:
        md = sys.stdin.read()
    
    blocks = md_to_portable_text(md)
    print(json.dumps(blocks, indent=2, ensure_ascii=False))
