# STATE 1 OUTLINE — complete-guide-ai-face-swap-photo-video (EN)

Lane: Deep (GSC impr 3,789; EN URL currently 404; ZH is strong source)
Floor: ≥7,500 EN words | Sanity category: Complete Guide
Cover: https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-036-1024x682.png
Publish plan: clone hijacked `-en` body → create `-ja` → PATCH `-en` with real EN

## Column spine
Face swap is not a one-click trick. The hard part is making the face look like it was always there — and that is a low-tolerance production workflow, not a magic button.

## Three claims to attack
1. "One-click face swap is good enough for client delivery."
2. "If the model is strong enough, bad source photos still work."
3. "Video face swap is just photo face swap run on every frame."

## Evidence anchors (≥5)
- Client case: 12 product plates, talent schedule collapse, one afternoon delivery
- 15-second talking-head swap with side-turn drift + glasses glare
- Neck/shadow "mask" failure as the #1 tell
- Long video (>2 min) identity drift → split into 20–30s segments
- Lighting direction / color temperature / intensity as three independent failure axes
- Paste-swap vs rebuild-from-face tradeoff

## H2 budget
1. Hook + stance — 700
2. What Lovart face swap actually is — 650
3. Source materials (three iron rules + selection flow) — 900
4. Photo four-step workflow — 900
5. Video temporal workflow — 850
6. Lighting consistency deep dive — 700
7. Paste-swap vs rebuild-from-face — 650
8. Three failure recoveries + three postmortems — 800
9. Five-inspection QA — 550
10. Comparison matrix (Lovart vs dedicated apps) — 550
11. Ethics / consent / commercial paperwork — 550
12. Prompt templates + secondary creation — 650
13. Derivative scenarios + beginner drills — 500
14. FAQ (8+) — 700
15. E-E-A-T / Internal Links / Image Appendix / close — 400

ASCII matrix: tool comparison + failure-mode matrix
Formula: DeliveryQuality = f(SourceMatch, LightingAlign, LocalEditPasses, TemporalLock)

## Lovart role map
- ChatCanvas: place source + target, brief constraints
- Nano Banana Pro: generation / upscale / relight assist
- Touch Edit: neck seam, hairline, glare frames
- Edit Elements: lock background / product logo layers
