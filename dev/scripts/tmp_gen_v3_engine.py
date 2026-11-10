#!/usr/bin/env python3
"""tmp_gen_v3_engine.py — V3 全量重写引擎

结构：三层锚定（材质真实 / 单一焦点 / 克制配色）+ 四层变量（材质 / 布光 / 场景 / 叙事瞬间）+ agent 隐喻
- 33 条 Hero（A/B/C）+ 18 条 gallery media：手工撰写（视觉权重最高）
- 216 条行业瓦片 + 28 工具瓦片 + 90 模块 + 7 journey + 5 视频：规则引擎（含机位/材质/布光/场景轮转）

输出：v3/*.jsonl（不改动 v2 文件，便于对照）
"""
import json, re
from pathlib import Path

D = Path("/Users/seveno/MFlow Dev/mflow/harness/Docs/S3-内容创作/Hero封面批次-2026-11")
V3 = D / "v3"
V3.mkdir(exist_ok=True)

ANCHOR = ("material truth with visible surface texture, one focal point only, "
          "muted base with at most one accent")
TEXT = "no text, no letters, no watermark, no screens, no UI windows"

# ══════════════ 材质 / 布光 / 场景 / 瞬间 词库 ══════════════
MAT_L4 = [
    "cold-pressed watercolour paper with visible fibre",
    "translucent vellum that glows slightly at the edges",
    "newsprint with a fibrous open surface",
    "cotton stock with a soft deckled edge",
    "kraft board with visible fibre and a raw cut edge",
    "cotton stock silkscreened with a visible halftone dot",
    "coated stock with a matte laminate and one blind-embossed area",
    "wood-free paper with a faint laid line",
]
MAT_PHOTO = [
    "cold-pressed paper with visible fibre",
    "raw unbleached linen with visible weave and thickness",
    "nubuck leather with a soft nap that catches the light",
    "brushed bronze with directional micro-scratches",
    "unglazed terracotta with a chalky uneven surface",
    "marble plaster with a faint granular tooth",
    "solid oak with open grain and hand-sanded edges",
    "bead-blasted anodised aluminium with a fine matte grain",
    "translucent vellum laid over a darker ground",
    "cotton stock with a blind letterpress impression",
]
MAT_3D = [
    "unglazed terracotta with a chalky surface",
    "matte stoneware with a fine throwing line",
    "bead-blasted aluminium with a soft matte grain",
    "waxed concrete with a faint pour mark",
    "brushed bronze with directional micro-scratches",
    "soapstone with a dry powdery touch",
    "moulded paper pulp with visible fibre",
    "cast plaster with a matte porous surface",
]
LIGHT_PHOTO = [
    "north-facing window light, soft and directional",
    "single-source chiaroscuro with deep falloff from the upper left",
    "softbox rim light defining the silhouette against a darker ground",
    "raking sidelight that reveals every surface texture",
    "golden-hour backlight with a faint lens bloom",
    "museum vitrine light, tight and clinical",
    "overcast daylight, even and almost shadowless",
    "one practical task lamp pooling light on the subject",
]
LIGHT_3D = [
    "a single large soft HDRI from the upper left with a long gentle shadow",
    "a tight rim light from behind leaving the front in soft half-shadow",
    "a low grazing light that skims the surface and reveals tooling",
    "clinical vitrine lighting with a narrow falloff",
    "an overcast dome light producing almost no shadow",
    "one warm practical light pooling on the object from the right",
]
LIGHT_L4 = [
    "flat even daylight with no specular highlight",
    "raking sidelight across the paper that reveals its tooth",
    "diffuse north window light falling evenly with one soft edge shadow",
    "proofing-room light, neutral and shadowless",
]
SCENE_PHOTO = [
    "set on a designer's atelier bench with tools pushed to the edges of frame",
    "set on a print workshop bench with ink-stained felt",
    "against an open archive drawer of filed material samples",
    "in a museum vitrine with a glass edge catching a sliver of light",
    "on a material library bench with labelled swatch boards receding out of focus",
    "on a gallery wall with one piece hung and the rest bare",
    "in a proofing room with colour charts pinned to the wall behind",
    "on a quiet studio plinth in a corner with a raw plaster wall behind",
]
SCENE_3D = [
    "on a designer's atelier bench with the clutter pushed to the frame edges",
    "on a studio plinth in an empty room with a raw plaster wall",
    "beside an open archive shelf of filed forms",
    "on a material library bench with labelled sample boards behind",
    "in a bare vitrine room with one hard shadow line across the floor",
    "on a long workbench receding into soft depth",
]
SCENE_L4 = [
    "pinned to a gallery wall with the rest of the wall left bare",
    "laid on a proofing bench with colour charts just out of focus",
    "resting on an archive drawer of filed sheets",
    "mounted on a material library board beside labelled swatches",
    "taped to a pinboard still showing earlier versions beneath",
    "set on a bare desk with a single steel ruler at the edge",
]
MOMENT = [
    "resting as a finished piece",
    "caught mid-way as it forms",
    "left half-finished with one edge unresolved",
    "just delivered, still unsettled on the surface",
    "being handled in use",
    "filed away as part of a set",
]
# agent 隐喻（物理化，绝不画 UI）
AGENT = [
    ("one brief card feeding three finished deliverables in three different media",
     "one brief, three deliverables"),
    ("the same subject shown in three progressive states along one line, raw then resolved then delivered",
     "raw to delivered"),
    ("the piece caught completing itself, an edge still turning over",
     "finishing on its own"),
    ("one visual language repeated across four material grounds of identical size",
     "one language, four grounds"),
    ("the final piece laid precisely over three earlier drafts at even intervals",
     "iteration stack"),
]
PRINT_L4 = ["letterpress", "silkscreen", "risograph", "offset halftone",
            "blind emboss with one foil accent", "screen print on kraft",
            "duotone offset", "foil stamp over a matte ground"]

CAM6 = [
    "viewed straight on and perfectly centred",
    "seen from a slight three-quarter angle with a short throw shadow",
    "cropped tight into the main shape so it nearly fills the frame",
    "shown as a flat overhead top-down layout",
    "seen from a low angle looking slightly upward",
    "shown as a clean side profile against the ground",
    "placed off-centre with generous negative space on one side",
    "overlapping a plain secondary sheet tucked behind",
    "bled edge to edge so the composition runs off frame",
    "isolated small within a large calm field",
    "arranged on a bold diagonal axis",
    "layered with a soft foreground edge cutting the lower corner",
]


def lane_kind(lane):
    if lane.startswith("L1") or lane.startswith("L5"):
        return "photo"
    if lane.startswith("L2"):
        return "cinema"
    if lane.startswith("L3"):
        return "3d"
    if lane.startswith("L4"):
        return "flat"
    return "paper"


def pools(kind):
    return {
        "photo": (MAT_PHOTO, LIGHT_PHOTO, SCENE_PHOTO),
        "cinema": (MAT_PHOTO, LIGHT_PHOTO, SCENE_PHOTO),
        "3d": (MAT_3D, LIGHT_3D, SCENE_3D),
        "flat": (MAT_L4, LIGHT_L4, SCENE_L4),
        "paper": (MAT_L4, LIGHT_L4, SCENE_L4),
    }[kind]


def v3_tile(rec, i, total_tiles, set_offset=0):
    """规则引擎：行业瓦片 / 工具瓦片 / 模块。set_offset 用于不同套装错开词库。"""
    kind = lane_kind(rec.get("lane", "L1-photo-editorial"))
    mats, lights, scenes = pools(kind)
    k = i + set_offset
    mat = mats[k % len(mats)]
    light = lights[k % len(lights)]
    scene = scenes[(k * 3) % len(scenes)]
    moment = MOMENT[(k * 2) % len(MOMENT)]
    cam = CAM6[(i - 1) % min(6, max(total_tiles, 1))] if total_tiles <= 6 else CAM6[(i - 1) % 12]

    # 主题色（沿用 v2 的 palette，已足够克制）
    pal = rec.get("_palette") or "a muted warm-grey base with at most one coral accent"

    # 排版类：印刷方法轮转
    print_note = ""
    if kind == "flat":
        print_note = f", printed in {PRINT_L4[i % len(PRINT_L4)]}"

    subj = rec.get("_subject") or "the central form"
    # agent 隐喻：每 3 条用 1 条
    agent = ""
    if i % 3 == 0:
        a, _ = AGENT[(i // 3) % len(AGENT)]
        agent = f", {a}"

    ratio = rec.get("ratio", "1:1")
    tail = ("bottom 25% kept clean for label overlay" if rec.get("field") == "gallery"
            else "lower 30% kept visually simple for caption overlay" if rec.get("variant") == "hero-mosaic"
            else "")
    seed_note = ""
    if rec.get("field") == "gallery":
        seed_note = f", locked seed and style reference shared across all {total_tiles} tiles"

    parts = [f"Editorial still life in {mat}{print_note}", light, scene,
             f"one subject only: {subj}, {moment}{agent}", cam,
             ANCHOR, pal, ratio]
    if tail:
        parts.append(tail)
    parts.append(seed_note.lstrip(", ") if seed_note else None)
    parts.append(TEXT)
    return ", ".join(p for p in parts if p)


def subject_of(prompt):
    """从 v2 prompt 提取主体"""
    m = re.search(r"one subject only: (.*?)(?:, (?:viewed|seen|cropped|shown|placed|"
                  r"overlapping|bled|isolated|arranged|layered|the subject))", prompt)
    if m:
        return m.group(1).strip()
    m = re.search(r"one subject only: (.*?),", prompt)
    if m:
        return m.group(1).strip()
    return None


def palette_of(prompt):
    m = re.search(r"((?:a |)[a-z][^,]{6,60}? palette)", prompt)
    if m:
        return m.group(1).strip()
    m = re.search(r"(muted [^,]{4,40} with at most one [^,]{3,20} accent)", prompt)
    return m.group(1) if m else None


def load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def dump(p, rows):
    Path(p).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


# ══════════════ 手工 V3：20 条 split ══════════════
SPLIT_V3 = {
"S-PLA": ("Soft-body 3D render in bead-blasted anodised aluminium and unglazed terracotta, "
  "single-source chiaroscuro with deep falloff from the upper left, set on a designer's atelier "
  "bench with tools pushed to the edges of frame, one folded-corner brief card entering a machined "
  "slot while three finished pieces stand beside it in three different media — a cotton-paper "
  "print, a linen swatch panel, a bronze-edged plaque — one brief, three deliverables, rendered at "
  "an equivalent 50mm perspective", "Lovart design agent turning one brief into deliverables across three media"),
"S-VID": ("Cinematic still shot on 35mm film with subtle grain, strictly a two-colour teal-and-amber "
  "palette, golden-hour backlight with a faint lens bloom, laid on a print workshop bench with "
  "ink-stained felt, a single film strip held by hand-sanded oak pegs showing three progressive "
  "states of the same scene — raw frame, graded frame, finished frame — shallow depth of field at 50mm",
  "Lovart video agent grading one scene from raw frame to finished frame"),
"S-IMG": ("High-end editorial photograph, raking sidelight that reveals every surface texture, in a "
  "proofing room with colour charts pinned to the wall behind, one large painted canvas standing on "
  "a hand-sanded oak easel with three earlier studies leaning behind it at even intervals, the "
  "painting still wet at one edge, 85mm with shallow depth of field",
  "Lovart image agent iterating from studies to a finished painting"),
"S-SOC": ("High-end commercial photograph, north-facing window light, soft and directional, on a "
  "material library bench with labelled swatch boards receding out of focus, one vertical story "
  "print on cold-pressed paper laid down with three blank paper cutouts in different aspect ratios "
  "aligned beside it, visible crop marks ruled in pencil, 50mm overhead",
  "Lovart social agent adapting one story print across platform ratios"),
"S-ECO": ("High-end commercial product photograph, softbox rim light defining the silhouette against "
  "a darker ground, on a material library bench, one matte ceramic bottle on a nubuck leather pad "
  "with a single linen swatch folded beside it and a plain white cutout of the same bottle leaning "
  "behind — studio shot and listing cutout in one frame, 100mm macro",
  "Lovart ecommerce agent producing studio and listing versions of one product"),
"S-LOG": ("Macro still-life photograph, museum vitrine light, tight and clinical, one abstract mark "
  "repeated across four material grounds of identical size — cold-pressed paper, raw linen, brushed "
  "bronze, translucent vellum — each catching the light differently, arranged in a precise row",
  "Lovart brand agent applying one mark across four material grounds"),
"S-PRT": ("Macro still-life photograph, raking sidelight that reveals every surface texture, on a "
  "print workshop bench with ink-stained felt, three printed pieces — a letterpressed poster, a "
  "tri-fold brochure, a menu — overlapping in a tidy arrangement, visible crop marks and bleed "
  "guides, cotton stock with a blind emboss impression, 100mm",
  "Lovart print agent producing a coordinated print set"),
"S-DOC": ("Macro still-life photograph, north-facing window light, soft and directional, in a "
  "proofing room with colour charts pinned up, a short stack of presentation sheets fanned slightly, "
  "the top sheet carrying one blind-embossed rising bar form in deep ink, a steel pen resting beside "
  "the stack, 100mm",
  "Lovart deck agent assembling a presentation set"),
"S-AVA": ("High-end editorial photograph, overcast daylight, even and almost shadowless, on a bare "
  "desk with a single steel ruler at the edge, five portrait prints fanned in a small brass stand, "
  "each showing the same person rendered in a different medium — photographic, painted, clay, flat "
  "poster, ink sketch — 85mm shallow depth of field",
  "Lovart avatar agent rendering one person across five mediums"),
"S-PED": ("High-end editorial photograph, raking sidelight that reveals every surface texture, on a "
  "print workshop bench, one landscape print split exactly down the centre by a clean vertical tear: "
  "the left half soft and unresolved under dull wash, the right half resolving into crisp detail "
  "with true colour, a loupe resting at the edge of frame, 85mm",
  "Lovart photo agent resolving an image from unresolved to crisp"),
"S-IND": ("High-end editorial photograph, north-facing window light, soft and directional, one matte "
  "standing board on a workbench holding three printed proofs pinned side by side, behind it a "
  "softly blurred commercial interior — half office, half retail — built as a swappable backdrop, "
  "the board's linen hinge visible, 85mm",
  "Lovart industry agent tailoring one design system to a sector"),
"S-ADS": ("Editorial flat graphic printed in silkscreen on cotton stock with a visible halftone dot, "
  "raking sidelight across the paper that reveals its tooth, pinned to a gallery wall with the rest "
  "of the wall bare, one bold product silhouette in tangerine against a cream field with a strong "
  "diagonal shadow shape and a deep charcoal accent block, flat layout with no photographic perspective",
  "Lovart ads agent producing a bold campaign key visual"),
"S-CRE": ("High-end commercial photograph, one practical task lamp pooling light on the subject, on "
  "a proofing bench, two thumbnail prints standing upright in a hand-sanded oak stand, one printed "
  "slightly brighter and one cooler for comparison, a small triangular play motif cut from paper "
  "resting in front, 85mm shallow depth of field",
  "Lovart creator agent testing thumbnail variants side by side"),
"S-CMP": ("Editorial flat graphic printed in duotone offset, flat even daylight with no specular "
  "highlight, laid on a proofing bench with colour charts just out of focus, the frame split by one "
  "clean vertical rule: left a messy pile of dull grey paper scraps, right a single crisp cream card "
  "carrying one coral geometric mark, flat layout with no photographic perspective",
  "Lovart compared with traditional tools — clutter versus one clean deliverable"),
"S-WEB": ("Layered paper-craft diorama cut from cold-pressed paper, diffuse north window light "
  "falling evenly with one soft edge shadow, set on a bare desk, a hand-cut page layout standing in "
  "shallow depth — one hero banner layer, two card layers and a rounded chip layer — each layer's "
  "raw cut edge visible on the shadow line",
  "Lovart web agent building a page as layered paper planes"),
"S-AUD": ("Macro still-life photograph, raking sidelight that reveals every surface texture, on a "
  "print workshop bench, a vinyl record half slid from a matte sleeve with its groove catching the "
  "light, two small cover cards leaning behind it on brushed bronze stands, 100mm",
  "Lovart audio agent producing cover art and audio visuals"),
"S-INT": ("High-end editorial photograph, north-facing window light, soft and directional, on a "
  "material library bench, a miniature living-room model with one wall panel lifted to reveal "
  "layered material swatches inside — linen, plaster, oak — the cut edges of each layer visible, 85mm",
  "Lovart interior agent revealing material layers inside a room model"),
"S-EDU": ("Layered paper-craft diorama cut from cold-pressed paper and construction stock, an "
  "overcast dome light producing almost no shadow, on a classroom shelf, a hand-cut worksheet sheet, "
  "three flashcards and one small book standing in layered depth with visible deckled edges",
  "Lovart education agent assembling a classroom material set"),
"S-3D": ("Soft-body 3D render in matte stoneware and bead-blasted aluminium, a single large soft "
  "HDRI from the upper left with a long gentle shadow, on a studio plinth in an empty room with a "
  "raw plaster wall, a pencil sketch card on the left and the same object resolved as a stoneware "
  "model on the right, three material chips of terracotta, bronze and plaster along the base",
  "Lovart 3D agent resolving a sketch into a material model"),
"S-FAS": ("High-end editorial photograph, softbox rim light defining the silhouette against a darker "
  "ground, on a designer's atelier bench, a small dress form wearing a miniature tailored garment in "
  "raw unbleached linen with two fabric swatches draped over its arm — one nubuck, one silk — the "
  "fabric edges left raw and visible, 85mm",
  "Lovart fashion agent tailoring a garment from fabric swatches"),
}

# ══════════════ 手工 V3：5 条 cinematic ══════════════
CINE_V3 = {
"C-PLA": ("Soft-body 3D render in bead-blasted aluminium and unglazed terracotta, wide establishing "
  "shot in three layers — foreground a folded-corner brief card on a shallow tray, midground a row of "
  "finished pieces in three different media standing on a long workbench, background an empty warm-grey "
  "studio volume with one soft coral source — single-source chiaroscuro from the upper left, the "
  "bench receding, at most one hero element per layer, one brief card feeding three finished deliverables in three different media",
  "Lovart design agent studio — one brief becoming a row of deliverables"),
"C-IMG": ("High-end editorial photograph, wide shot in three layers — foreground a blurred jar of "
  "brushes catching north window light, midground one large vivid landscape painting on a hand-sanded "
  "oak easel in full focus with three earlier studies leaning behind it, background a tall window with "
  "soft out-of-focus daylight — the painting still wet at one edge, warm neutral base with one "
  "saturated accent living only inside the painting",
  "Lovart image agent — studies resolving into one finished painting"),
"C-ECO": ("High-end commercial product photograph, wide shot in three layers — foreground the blurred "
  "edge of a matte ceramic bottle on nubuck leather, midground the same bottle centred on a sand "
  "podium in full focus, background a plain white listing card leaning against raw linen — softbox rim "
  "light defining each silhouette, sand and cream base with one deep-green accent",
  "Lovart ecommerce agent — studio shot and listing cutout in one frame"),
"C-LOG": ("Macro still-life photograph, wide shot in three layers — foreground the blurred embossed "
  "corner of a cotton-paper card, midground a precise row of upright brand cards on a stone ledge each "
  "carrying the same abstract blind-embossed mark with one brass foil accent, background a deep "
  "warm-grey studio void — raking sidelight travelling across the row, ivory and charcoal base",
  "Lovart brand agent — one mark across a row of material grounds"),
"C-IND": ("High-end editorial photograph, wide shot in three layers — foreground the blurred edge of a "
  "designer's worktable, midground one matte standing board with three printed proofs pinned side by "
  "side, background a softly blurred commercial interior half office half retail, built as a "
  "swappable backdrop — north window light with a warm accent from the right, neutral base",
  "Lovart industry agent — one design system adapted to a sector"),
}

# ══════════════ 手工 V3：8 条 mosaic（4 瓦 × 2 套）══════════════
MOSAIC_V3 = {
"M-PLA": [
  ("Soft-body 3D render in unglazed terracotta and bead-blasted aluminium, raking sidelight that "
   "reveals every surface texture, on a designer's atelier bench, state 1 of a 4-step sequence on the "
   "same machined console: a folded-corner brief card resting on a shallow tray beside an empty slot",
   "Lovart workflow 1 — brief waiting"),
  ("Soft-body 3D render in unglazed terracotta and bead-blasted aluminium, raking sidelight, on the "
   "same atelier bench, state 2 of a 4-step sequence on the same console: the brief card caught "
   "mid-insertion, its leading edge already inside the slot, bending very slightly as it goes in on "
   "its own",
   "Lovart workflow 2 — brief entering the machine"),
  ("Soft-body 3D render in unglazed terracotta and bead-blasted aluminium, raking sidelight, on the "
   "same atelier bench, state 3 of a 4-step sequence on the same console: the card gone, one small "
   "framed print standing fresh on the bench beside the slot",
   "Lovart workflow 3 — first deliverable"),
  ("Soft-body 3D render in unglazed terracotta and bead-blasted aluminium, raking sidelight, on the "
   "same atelier bench, state 4 of a 4-step sequence on the same console: three finished pieces in "
   "three different media standing in a neat row, the slot at rest",
   "Lovart workflow 4 — full set delivered"),
],
"M-IND": [
  ("High-end commercial photograph, raking sidelight across a raw surface, on a print workshop bench, "
   "state 1 of a 4-step sequence on the same package: a plain kraft box beside a folded-corner brief "
   "card, both untouched, kraft fibre visible at the cut edge",
   "Lovart industry workflow 1 — blank package and brief"),
  ("High-end commercial photograph, raking sidelight, on the same bench, state 2 of a 4-step sequence "
   "on the same package: the kraft box now wrapped in a freshly printed sleeve, one corner of the "
   "sleeve still lifting as it settles",
   "Lovart industry workflow 2 — sleeve applying"),
  ("High-end commercial photograph, raking sidelight, on the same bench, state 3 of a 4-step sequence "
   "on the same package: five identical sleeved boxes aligned in a batch row, one being set down, the "
   "registration marks lining up",
   "Lovart industry workflow 3 — batch run"),
  ("High-end commercial photograph, raking sidelight, on the same bench, state 4 of a 4-step sequence "
   "on the same package: the sleeved box standing on a retail shelf between two bare shelf slots",
   "Lovart industry workflow 4 — on shelf"),
],
}

# ══════════════ 手工 V3：18 条 gallery media ══════════════
MEDIA_V3 = {
"logo": ("Editorial still life in cold-pressed paper with a blind letterpress impression, north-facing "
  "window light, on a material library bench with labelled swatch boards receding out of focus, one "
  "abstract mark shown as a primary lockup with one compact arrangement beside it, the impression "
  "still holding the paper's memory of pressure", "logo design"),
"poster": ("Editorial still life printed in risograph on cold-pressed paper with a visible grain, raking "
  "sidelight across the sheet, pinned to a gallery wall with the rest of the wall bare, one poster "
  "with a strong abstract focal shape and a bold typographic hierarchy suggested only by abstract grey "
  "bars", "poster design"),
"banner": ("Editorial still life in cotton stock silkscreened with a visible halftone dot, flat even "
  "daylight with no specular highlight, resting on an archive drawer of filed sheets, one wide banner "
  "with a single focal shape and a confident typographic rhythm suggested only by abstract bars",
  "banner design"),
"menu": ("Macro still-life photograph, north-facing window light, on a print workshop bench, an open "
  "printed menu page on uncoated stock with a small dish illustration and a clean list structure "
  "suggested only by abstract grey bars, the fold line softened from use", "menu design"),
"brochure": ("Macro still-life photograph, raking sidelight that reveals every surface texture, on a "
  "print workshop bench, a tri-fold brochure open to one spread showing an image panel and a text "
  "panel, the fold creases catching light, cotton stock with a soft deckled edge", "brochure design"),
"business-card": ("Macro still-life photograph, single-source chiaroscuro with deep falloff, on a "
  "designer's atelier bench, a pair of business cards — one face up, one angled behind — carrying an "
  "blind-embossed abstract mark on thick cotton stock, the paper's cut edge visible", "business card design"),
"packaging": ("High-end commercial product photograph, softbox rim light defining the silhouette, on a "
  "material library bench, a product packaging box at a flattering angle with a label panel and one "
  "brass foil detail catching the light, kraft fibre visible at the folded edge", "packaging design"),
"cover": ("Macro still-life photograph, museum vitrine light, tight and clinical, a printed cover in a "
  "vitrine with an embossed abstract artwork field and one brass foil edge, the emboss depth readable "
  "in the raking light", "cover design"),
"video-thumbnail": ("Editorial still life printed in offset halftone on coated stock with a matte "
  "laminate, raking sidelight across the sheet, taped to a pinboard still showing earlier versions "
  "beneath, one thumbnail composition with a dominant focal subject and a strong corner-to-corner "
  "diagonal", "video thumbnail design"),
"social-media": ("Editorial still life in cotton stock with one silkscreen layer, flat even daylight, "
  "laid on a proofing bench, a set of social post cards in a tidy overlapping stack with one hero card "
  "fully visible on top, the stack edge showing the thickness of the stock", "social media design"),
"ecommerce-main": ("High-end commercial product photograph, softbox rim light defining the silhouette "
  "against a darker ground, on a studio plinth with raw plaster behind, a single product on a nubuck "
  "leather pad with a soft contact shadow, one linen swatch folded beside it for scale",
  "ecommerce main image"),
"product-detail": ("Editorial still life printed in duotone offset, flat even daylight, resting on an "
  "archive drawer, a product detail module as two stacked content panels — an image block and a "
  "feature block — with the registration marks still visible at the trim", "product detail page design"),
"ppt": ("Editorial still life in cold-pressed paper with one blind-embossed data shape, north window "
  "light, on a proofing bench, one presentation sheet with a dominant layout block and a clean "
  "supporting arrangement of abstract data shapes, the sheet lifted slightly at one corner",
  "presentation slide design"),
"resume": ("Editorial still life in uncoated wood-free paper with a faint laid line, flat even daylight, "
  "on a bare desk with a steel ruler at the edge, a resume layout with a clear column structure, an "
  "abstract avatar block and ruled content lines, the paper showing its grain", "resume design"),
"font": ("Macro still-life photograph, raking sidelight revealing the impression depth, a type specimen "
  "sheet in letterpress on cotton stock showing large abstract glyph forms with fine rule lines, one "
  "glyph blind-embossed rather than inked, generous margins", "type specimen design"),
"illustration": ("Editorial still life printed in risograph with a visible overlapping grain, raking "
  "sidelight, pinned to a gallery wall with the rest bare, an illustration set of three related flat "
  "panels sharing one motif, the ink misregistration left as intent", "illustration design"),
"data-story": ("Editorial still life in cotton stock with silkscreen layers, flat even daylight, on a "
  "proofing bench with colour charts out of focus, a data-story layout with abstract shapes, connected "
  "flow blocks and a clear hierarchy, one blind-embossed area catching the light", "infographic design"),
"brand-identity": ("Macro still-life photograph, museum vitrine light, one brand identity board on "
  "cotton stock carrying the mark, a colour chip row of material samples and three fabric squares — "
  "linen, nubuck, silk — each cut edge visible, the board resting at a slight angle", "brand identity system"),
}


def main():
    # ── A: split ──
    A = load(D / "module-A-split.jsonl")
    A.sort(key=lambda r: (0 if r["priority"] == "P0" else 1, -r.get("pages", 0)))
    outA = []
    for r in A:
        body, alt = SPLIT_V3[r["id"]] if r["id"] in SPLIT_V3 else (None, None)
        if body is None:
            continue
        outA.append({**r,
                     "prompt": f"{body}, {ANCHOR}, 4:3, edges safe for rounded-corner crop, {TEXT}",
                     "alt": alt, "prompt_version": "v3"})
    dump(V3 / "A-split.jsonl", outA)
    print(f"A-split: {len(outA)}")

    # ── B: cinematic ──
    B = load(D / "module-B-cinematic.jsonl")
    outB = []
    for r in B:
        body, alt = CINE_V3[r["id"]]
        outB.append({**r,
                     "prompt": f"{body}, {ANCHOR}, 16:10, top and bottom 8% fading to a neutral ground, {TEXT}",
                     "alt": alt, "prompt_version": "v3"})
    dump(V3 / "B-cinematic.jsonl", outB)
    print(f"B-cinematic: {len(outB)}")

    # ── C: mosaic ──
    C = load(D / "module-C-mosaic.jsonl")
    outC = []
    for r in C:
        setid = r["id"].rsplit("-", 1)[0]
        tile = r["tile"]
        body, alt = MOSAIC_V3[setid][tile - 1]
        pal = "muted warm-grey base with at most one coral accent"
        outC.append({**r,
                     "prompt": (f"{body}, {ANCHOR}, {pal}, 4:3, lower 30% kept visually simple for "
                                f"caption overlay, locked seed and style reference shared across all "
                                f"four tiles, {TEXT}"),
                     "alt": alt, "prompt_version": "v3"})
    dump(V3 / "C-mosaic.jsonl", outC)
    print(f"C-mosaic: {len(outC)}")

    # ── D: gallery media（18）──
    dm = [r for r in load(D / "module-D-gallery.jsonl") if r["field"] == "media"]
    outM = []
    for r in dm:
        cat = r["theme"]
        if cat in MEDIA_V3:
            body, label = MEDIA_V3[cat]
            outM.append({**r,
                         "prompt": f"{body}, {ANCHOR}, 16:10, top and bottom 8% fading to a neutral ground, {TEXT}",
                         "alt": f"Lovart {label} — 品类总览", "prompt_version": "v3"})
    dump(V3 / "D-media.jsonl", outM)
    print(f"D-media: {len(outM)}")

    # ── D: 行业瓦片（main6 108 + b2b4 72 + rest2 36 = 216）──
    tiles = []
    for f in ["module-D-gallery.jsonl", "module-D-gallery-b2b4.jsonl", "module-D-gallery-rest2.jsonl"]:
        for r in load(D / f):
            if r["field"] != "gallery":
                continue
            r = dict(r)
            r["_subject"] = subject_of(r["prompt"]) or "the central form"
            r["_palette"] = palette_of(r["prompt"]) or "a muted warm-grey base with at most one coral accent"
            tiles.append(r)
    # 每个品类 12 条 → total_tiles 用该品类实际条数
    by_cat = {}
    for r in tiles:
        by_cat.setdefault(r["theme"], []).append(r)
    outT = []
    for ci, (cat, group) in enumerate(by_cat.items()):
        group.sort(key=lambda x: (x.get("industry_id", ""), x.get("tile", 0)))
        for i, r in enumerate(group, 1):
            outT.append({**{k: v for k, v in r.items() if not k.startswith("_")},
                         "prompt": v3_tile(r, i, len(group), set_offset=ci * 2),
                         "prompt_version": "v3"})
    dump(V3 / "D-tiles.jsonl", outT)
    print(f"D-tiles: {len(outT)}")

    # ── D: 工具瓦片（28，只取 main6 一份）──
    tools = [dict(r, _subject=r.get("label") or subject_of(r["prompt"]) or "the tool output",
                  _palette="a muted warm-grey base with at most one accent")
             for r in load(D / "module-D-gallery.jsonl") if r["field"] == "toolTiles"]
    outTl = []
    by_set = {}
    for r in tools:
        by_set.setdefault(r["theme"], []).append(r)
    for si, (setid, group) in enumerate(by_set.items()):
        for i, r in enumerate(group, 1):
            outTl.append({**{k: v for k, v in r.items() if not k.startswith("_")},
                          "prompt": v3_tile(r, i, len(group), set_offset=si * 3),
                          "prompt_version": "v3"})
    dump(V3 / "D-tools.jsonl", outTl)
    print(f"D-tools: {len(outTl)}")

    # ── journey media（7）──
    jm = load(D / "batches" / "E4-journey-media.jsonl")
    outJ = []
    for i, r in enumerate(jm, 1):
        mats, lights, scenes = pools("photo")
        subj = r["prompt"].split("wide establishing shot: ")[-1].split(", the scene fills")[0]
        outJ.append({**r,
                     "prompt": (f"High-end editorial photograph in {mats[i % len(mats)]}, "
                                f"{lights[i % len(lights)]}, {scenes[(i*3) % len(scenes)]}, "
                                f"wide establishing shot three layers deep: {subj}, "
                                f"{ANCHOR}, muted neutral base with at most one accent, 16:10, "
                                f"top and bottom 8% fading to a neutral ground, {TEXT}"),
                     "prompt_version": "v3"})
    dump(V3 / "E4-journey.jsonl", outJ)
    print(f"E4-journey: {len(outJ)}")

    # ── 视频（5）──
    vid = load(D / "E5-cinematic-video.jsonl")
    outV = []
    for i, r in enumerate(vid, 1):
        mats, lights, scenes = pools("cinema")
        motion = r["prompt"].split("— ")[-1].split(", composed in three")[0]
        outV.append({**r,
                     "prompt": (f"Cinematic still shot on 35mm film, strictly a two-colour teal-and-amber "
                                f"palette, {lights[i % len(lights)]}, on {scenes[i % len(scenes)]}, "
                                f"{motion}, composed three layers deep with at most one hero element per "
                                f"layer, {ANCHOR}, 16:10, 8 seconds, top and bottom 8% fading to a "
                                f"neutral ground, {TEXT}"),
                     "prompt_version": "v3"})
    dump(V3 / "E5-video.jsonl", outV)
    print(f"E5-video: {len(outV)}")

    # ── 模块（90）──
    mods = load(D / "modules" / "module-prompts.jsonl")
    outMo = []
    for i, r in enumerate(mods, 1):
        kind = "3d" if "matte ceramic" in r["prompt"] or "Soft-body" in r["prompt"] else (
            "flat" if "flat-graphic" in r["prompt"] or "Swiss grid" in r["prompt"] else "photo")
        mats, lights, scenes = pools(kind)
        # 提取主体（模块 prompt 结构：..., the subject fills about X% of frame, ...）
        m = re.search(r"(?:shot of |composition of |diorama of |still life of |, )([^,]{25,120}?), the subject fills", r["prompt"])
        subj = m.group(1) if m else r["label"]
        ratio = "16:10" if "16:10" in r["prompt"] else ("4:3" if "4:3" in r["prompt"] else "1:1")
        # agent 隐喻：按模块语义分配（comparison / portrait 不适用）
        AGENT_BY_MODULE = {
            "bento-2": [AGENT[0], AGENT[4]],
            "bento-4": [AGENT[0], AGENT[1]],
            "bento-6": [AGENT[0], AGENT[3], AGENT[4]],
            "feature-detail": [AGENT[4], AGENT[1]],
            "capability-tabs": [AGENT[3], AGENT[1]],
            "canvas-wall": [AGENT[3], AGENT[0]],
            "workflow-horizontal": [AGENT[1], AGENT[2]],
            "showcase-stacked": [AGENT[1], AGENT[3]],
            "media-marquee": [AGENT[3]],
            "tool-grid": [AGENT[0], AGENT[3]],
        }
        stype = r.get("stype", "")
        agent_phrase = ""
        pool_ag = AGENT_BY_MODULE.get(stype)
        if pool_ag:
            agent_phrase = pool_ag[(i - 1) % len(pool_ag)][0]

        ag_part = f", {agent_phrase}" if agent_phrase else ""
        body = (f"Editorial still life in {mats[i % len(mats)]}, {lights[i % len(lights)]}, "
                f"{scenes[(i*3) % len(scenes)]}, one subject only: {subj}, "
                f"{MOMENT[(i*2) % len(MOMENT)]}{ag_part}, {ANCHOR}, "
                f"muted neutral base with at most one accent, {ratio}")
        outMo.append({**r, "prompt": f"{body}, {TEXT}", "prompt_version": "v3"})
    dump(V3 / "modules.jsonl", outMo)
    print(f"modules: {len(outMo)}")

    total = (len(outA) + len(outB) + len(outC) + len(outM) + len(outT)
             + len(outTl) + len(outJ) + len(outV) + len(outMo))
    print(f"\n== V3 总计 {total} 条 ==")


if __name__ == "__main__":
    main()
