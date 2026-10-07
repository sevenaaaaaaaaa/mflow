# Lovart Blog Review Expansion Task — Self-Contained Agent Prompt

> Share this prompt with any agent (Cursor, Codex, OpenCode, Claude Code, or new Hermes session).
> All paths, credentials, and workflow instructions are included.

---

## TASK

Expand **8 AI tool review blog posts** for Lovart's blog from their current word counts to **7,500+ words** each. These are "Review skeleton" pages that were originally 200-300 word placeholders. First drafts have been written and published to Sanity, but they need expansion to meet the 7,500-word quality threshold.

## RULES (BLOCK-level — do not violate)

1. **7,500+ words per article.** No excuses. Count words before submitting.
2. **First-person voice throughout.** "I tested..." "I generated..." "My client said..." At least 50+ "I"/"my" per article.
3. **Real翻车 (failure story) in every article.** A specific moment where the tool failed, with specific details (frame numbers, dollar amounts, client quotes). No abstract "many users struggle."
4. **搭档 stack in every article.** Every tool mentioned needs a pairing: "Dream Machine + Premiere" "Haiper + Lovart" etc. At least 5 "+" pairings per article.
5. **Gold-line closing.** Every article ends with a single bold sentence — ≤20 words, quotable, not slogan-y. Example: "The tool that makes the prettiest clip isn't the one that ships the video."
6. **Honest competitor praise.** If a competitor is better at something, say so explicitly with evidence. Then pivot: "But for production work..." / "However, if you need to actually ship..."
7. **No banned AI-slop words.** Never use: unlock, revolutionize, seamless, empower, game-changer, cutting-edge, leverage, "in today's fast-paced", "the future of"
8. **Keep existing CTA blocks.** The text CTA and button CTA at the end of each article must remain intact.
9. **Expand existing content — do not replace.** Add sections, case studies, FAQ depth, week-in-the-life comparisons. Don't delete what's already there.

## SANITY CONNECTION

```python
import json, urllib.request

with open('/Users/seveno/.config/sanity/config.json') as f:
    cfg = json.load(f)
token = cfg['authToken']

HEADERS = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
QUERY_URL = 'https://o11tm2qe.api.sanity.io/v2026-01-01/data/query/production'
MUTATE_URL = 'https://o11tm2qe.api.sanity.io/v2026-01-01/data/mutate/production'

def q(query_str):
    payload = json.dumps({'query': query_str}).encode()
    req = urllib.request.Request(QUERY_URL, data=payload, headers=HEADERS)
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())['result']

def mutate(mutations):
    payload = json.dumps({'mutations': mutations}).encode()
    req = urllib.request.Request(MUTATE_URL, data=payload, headers=HEADERS)
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())
```

## WORKFLOW

For each article:

### Step 1: Fetch current body from Sanity
```python
slug = 'hedra-ai-review'  # change per article
doc = q(f'*[_type=="blog" && language=="en" && slug.current=="{slug}"][0]{{_id, "body":body[]{{..., children[]{{..., marks[]}}}}}}')
body = doc['body']
doc_id = doc['_id']
```

### Step 2: Inspect current structure
Check what's already there — H2 sections, CTA blocks, FAQ. Find the weak spots that need expansion.

### Step 3: Write expansion content
Add or expand sections. Recommended additions for articles under 5,000 words:
- **Real project case study**: Walk through a specific client project scene-by-scene (~1,500 words)
- **Week-in-the-life**: Day-by-day comparison of using this tool vs Lovart (~1,200 words)
- **Deeper competitor analysis**: Specific feature-by-feature comparison with 1-2 named competitors (~800 words)
- **When NOT to use**: Explicit anti-recommendations (~600 words)
- **Expanded FAQ**: 2-4 sentence answers with specific data, not generic (~1,000 words)
- **Physics/technical deep-dive**: Frame-by-frame analysis with specific failure counts (~800 words)

### Step 4: Convert markdown to Portable Text
```bash
cd "/Users/seveno/Documents/Lovart Local Dev"
python3 scripts/md_to_portable_text.py /tmp/ARTICLE.md /tmp/ARTICLE-pt.json
```

### Step 5: Patch to Sanity
```python
with open('/tmp/ARTICLE-pt.json') as f:
    new_body = json.load(f)
# Preserve existing CTA blocks — find them in the original body and append to new_body
for block in body:
    if block.get('_type') == 'cta':
        new_body.append(block)
mutate([{"patch": {"id": doc_id, "set": {"body": new_body}}}])
```

### Step 6: Verify
```bash
curl -s -o /dev/null -w "%{http_code}" "https://www.lovart.ai/blog/SLUG"
```

## ARTICLES TO EXPAND (in priority order)

### TIER 1 — Almost there (need ~1,000-1,700 more words)
1. **hedra-ai-review** — 6,200 words. Need: ~1,300. Add: deeper Synthesia comparison, one more real project scene, "When Hedra is wrong" section.
2. **haiper-ai-review** — 6,487 words. Need: ~1,013. Add: "When Haiper is wrong" section, market positioning map, expanded FAQ answers.
3. **pika-ai-review** — 5,791 words. Need: ~1,709. Add: more lip-sync test data, creative workflow day-in-the-life, CapCut detailed comparison.

### TIER 2 — Need substantial work (~4,000-5,000 more words)
4. **vidu-ai-review** — 2,660 words. Need: ~4,840. Add: project case study, week comparison, expanded FAQ, detailed physics benchmark data.
5. **adobe-firefly-review** — 2,746 words. Need: ~4,754. Add: real project with Photoshop workflow, Midjourney/FLUX detailed comparison, "when Firefly wins/loses" decision framework.
6. **hailuo-ai-review** — 2,449 words. Need: ~5,051. Add: project case study, frame-by-frame analysis data, week comparison, Chinese market context.

### TIER 3 — Basically rewrites needed (~6,000+ more words)
7. **pictory-ai-review** — 1,058 words. Need: ~6,442. Add: everything — this is a skeleton that needs full expansion with case study, week comparison, competitor analysis, FAQ.
8. **capcut-ai-review** — 889 words. Need: ~6,611. Add: everything — same as pictory.

## EXPANSION CONTENT TEMPLATE

When adding new sections, use this structure:

```markdown
### Section Title That Makes a Judgment

[2-3 paragraphs with specific data, first-person narrative, honest assessment]

**Specific claim with number**: "Hedra's lip sync handled 'Irish wristwatch' correctly on 3 out of 5 attempts..."

**Bold comparison point**: "Synthesia's avatar read it like a press release. Hedra's avatar performed it."

[Transition to Lovart relevance]: "Lovart handles this differently: [specific capability] means [specific benefit]."
```

## ANTI-PATTERNS TO AVOID

- "In this section, we will explore..." — never use
- "AI video tools are changing the landscape..." — banned opening
- Generic claims without numbers: "significantly faster" → "28 seconds vs 75 seconds"
- Lovart-is-always-better: be honest when competitors win on specific dimensions
- Template repetition: each article needs unique翻车 stories, unique搭档stacks, unique金句 closings

## GOLD-LINE CLOSING EXAMPLES (from completed articles)

From Luma: "**The tool that makes the prettiest 5-second clip isn't the one that ships the video. The one that lets you fix frame 47 without starting over is.**"

From Hedra: "**The best avatar tool isn't the one that generates the most expressive performance. It's the one that lets you fix the wink without starting over.**"

From Haiper: "**Beautiful physics don't ship videos. Editable timelines do.**"

From Pika: "**The best effect in the world doesn't matter if you can't adjust the timing by two frames.**"

Each remaining article needs its own unique gold-line that captures the specific tension between that tool's strength and its production limitation.

---

## DISTRIBUTION SUGGESTION

Split the 8 articles across multiple agents:
- Agent A (Cursor/Codex): Tier 1 articles (Hedra, Haiper, Pika) — fastest wins
- Agent B (OpenCode): Tier 2 articles (Vidu, Firefly, Hailuo) — moderate work
- Agent C (Claude Code/Hermes): Tier 3 articles (Pictory, CapCut) — longest work

Or any other split. The Sanity token, file paths, and workflow are self-contained.
