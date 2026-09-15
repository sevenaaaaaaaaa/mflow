#!/usr/bin/env python3
"""
kg-query.py — read-only graph queries against entities+relationships JSONL.

Usage:
  python3 kg-query.py --id <entity_id>                           → 1 entity record (JSON)
  python3 kg-query.py --related-to <entity_id> [--direction both|in|out]
                                                            → neighbor edges
  python3 kg-query.py --ancestors <entity_id>                  → upstream chain (outgoing parent_of/owned_by)
  python3 kg-query.py --start <entity_id> --hop 2 --type uses  → all 'uses' within 2 hops
  python3 kg-query.py --list --kind skill                      → all skills (table)
  python3 kg-query.py --find <substring> [--kind profile]      → search by name
  python3 kg-query.py --audit-orphans                          → entities with no edges
  python3 kg-query.py --stats                                  → graph cardinality

Exit codes:
  0 OK, 1 not found, 2 bad args, 3 yaml/io
"""

import argparse
import json
import sys
from collections import defaultdict, Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent.parent
ENT_PATH = HERE / "entities.jsonl"
REL_PATH = HERE / "relationships.jsonl"


def die(msg, code=1):
    sys.stderr.write(f"kg-query: {msg}\n")
    sys.exit(code)


def load():
    if not ENT_PATH.exists() or not REL_PATH.exists():
        die("JSONL mirrors missing — run kg-emit-jsonl.py first", code=3)
    entities = {}
    kinds = defaultdict(int)
    for line in ENT_PATH.read_text("utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        entities[e["id"]] = e
        kinds[e.get("__kind", "?")] += 1
    rels = []
    for line in REL_PATH.read_text("utf-8").splitlines():
        if not line.strip():
            continue
        rels.append(json.loads(line))
    return entities, rels, kinds


def fmt_entity(e):
    return json.dumps(e, ensure_ascii=False, indent=2)


def fmt_rel(r):
    return f"[{r.get('type','?'):>10}] {r['from']} → {r['to']}  {'#'+r.get('notes','') if r.get('notes') else ''}".rstrip()


def cmd_id(args, ents, rels, _):
    e = ents.get(args.id)
    if not e:
        die(f"no entity with id={args.id}", 1)
    print(fmt_entity(e))


def cmd_related(args, ents, rels, _):
    eid = args.related_to
    if eid not in ents:
        die(f"no entity with id={eid}", 1)
    direction = args.direction
    out = []
    for r in rels:
        if r["from"] == eid and direction in ("both", "out"):
            out.append(r)
        elif r["to"] == eid and direction in ("both", "in"):
            out.append({**r, "from": r["to"], "to": r["from"], "_reversed": True})
    if not out:
        print("(no edges)")
        return
    for r in out:
        print(fmt_rel(r))


def cmd_ancestors(args, ents, rels, _):
    eid = args.ancestors
    if eid not in ents:
        die(f"no entity with id={eid}", 1)
    parent_edges = {"owns", "parent_of", "requires", "supersedes", "validates", "bootstraps"}
    visited = set()
    stack = [(eid, [])]
    out = []
    while stack:
        cur, path = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        for r in rels:
            if r["from"] == cur and r["type"] in parent_edges:
                out.append((r, path + [r["to"]]))
                stack.append((r["to"], path + [r["to"]]))
    for r, path in out:
        print(fmt_rel(r), "via path:", " → ".join(path))


def cmd_hop(args, ents, rels, _):
    eid = args.start
    if eid not in ents:
        die(f"no entity with id={eid}", 1)
    wanted = {args.type} if args.type else None
    seen = {eid}
    frontier = [(eid, 0)]
    out = []
    while frontier:
        cur, depth = frontier.pop(0)
        if depth >= args.hop:
            continue
        for r in rels:
            is_from = r["from"] == cur
            is_to = r["to"] == cur
            if not (is_from or is_to):
                continue
            # Always expand frontier (regardless of type filter)
            if is_from and r["to"] not in seen:
                seen.add(r["to"])
                frontier.append((r["to"], depth + 1))
            if is_to and r["from"] not in seen:
                seen.add(r["from"])
                frontier.append((r["from"], depth + 1))
            # Print only if matches filter
            if is_from and (not wanted or r["type"] in wanted):
                out.append((r, depth + 1))
            elif is_to and (not wanted or r["type"] in wanted):
                out.append((r, depth + 1))
    for r, d in out:
        print(f"hop={d}", fmt_rel(r))


def cmd_list(args, ents, rels, kinds):
    target_kind = args.kind
    if target_kind:
        for e in ents.values():
            if e.get("__kind") == target_kind:
                name = e.get("name", e["id"])
                status = e.get("status", "")
                print(f"  {e['id']:<60}  {status:<10}  {name}")
    else:
        for k, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
            print(f"  {k:<20} {n}")


def cmd_find(args, ents, rels, _):
    needle = args.find.lower()
    target_kind = args.kind
    hits = []
    for e in ents.values():
        if target_kind and e.get("__kind") != target_kind:
            continue
        hay = " ".join([e["id"], e.get("name", ""), *(e.get("aliases") or []), *(e.get("tags") or [])]).lower()
        if needle in hay:
            hits.append(e)
    for e in hits:
        print(e["id"], "—", e.get("name", ""), f"[{e.get('status','')}]")


def cmd_orphans(args, ents, rels, _):
    seen = set()
    for r in rels:
        seen.add(r["from"])
        seen.add(r["to"])
    orphans = [eid for eid in ents if eid not in seen]
    if not orphans:
        print("(no orphans)")
        return
    for eid in sorted(orphans):
        print(eid, "—", ents[eid].get("name", ""))


def cmd_stats(args, ents, rels, kinds):
    print("entities:", len(ents))
    for k, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<20} {n}")
    print("relationships:", len(rels))
    type_counter = Counter(r["type"] for r in rels)
    for k, n in sorted(type_counter.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<20} {n}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--id", help="lookup by id")
    p.add_argument("--related-to", help="neighbors of id")
    p.add_argument("--direction", choices=["both", "in", "out"], default="both")
    p.add_argument("--ancestors", help="upstream parent chain")
    p.add_argument("--start", help="BFS start")
    p.add_argument("--hop", type=int, default=2)
    p.add_argument("--type", help="filter by edge type")
    p.add_argument("--list", action="store_true")
    p.add_argument("--kind", help="filter by entity kind")
    p.add_argument("--find", help="substring search across id/name/aliases/tags")
    p.add_argument("--audit-orphans", action="store_true")
    p.add_argument("--stats", action="store_true")
    args = p.parse_args()

    ents, rels, kinds = load()

    if args.id:
        return cmd_id(args, ents, rels, kinds)
    if args.related_to:
        return cmd_related(args, ents, rels, kinds)
    if args.ancestors:
        return cmd_ancestors(args, ents, rels, kinds)
    if args.start:
        return cmd_hop(args, ents, rels, kinds)
    if args.list:
        return cmd_list(args, ents, rels, kinds)
    if args.find:
        return cmd_find(args, ents, rels, kinds)
    if args.audit_orphans:
        return cmd_orphans(args, ents, rels, kinds)
    if args.stats:
        return cmd_stats(args, ents, rels, kinds)
    p.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
