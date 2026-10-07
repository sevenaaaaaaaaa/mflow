## How I evaluate a text-to-video model (the scoring rubric I actually use)

Most "best AI video" listicles rank by vibes: "looks cinematic," "impressive motion," "great for creators." That vocabulary is useless on a Tuesday at 11:40 a.m. with a campaign date two days out. I score every model on five axes that map to shipping, not demoing. I'm sharing the rubric because it's the only honest way to compare Hailuo against anything else — and because it explains why I pair it with Lovart instead of ranking it "number one" and moving on.

**Axis 1 — Time to first usable direction (weight 20%).** Not time to first pretty clip. Time to a clip where the object holds shape and the camera means something. Hailuo scores well here: on Brief A the perfume orbit was usable on attempt two. A model that needs eight attempts to hold a bottle shape fails this axis regardless of how the ninth looks.

**Axis 2 — Text edit cost (weight 25%).** The single most predictive axis for whether a brand can run a weekly campaign. If fixing "11am–2pm" requires regenerating the clip, the model is a demo toy. Hailuo scores poorly here because text is baked. Lovart's Touch Edit is what recovers the score for the paired workflow — but the model alone gets a low mark.

**Axis 3 — Brand consistency across a series (weight 20%).** Five clips of the same founder should look like five clips of the same founder. Hailuo has no memory; identity and color drift. Brand Kit in Lovart is what supplies the memory Hailuo lacks. Model-alone score: low. Paired score: high.

**Axis 4 — Channel crop survival (weight 15%).** Does the asset survive at 390px width on a phone? Hailuo's native 16:9 often crops the subject in half at 9:16. Building the frame in ChatCanvas at the target zones is the fix. Model-alone: medium. Paired: high.

**Axis 5 — Failure honesty (weight 20%).** Does the tool document where it breaks, or only show highlight reels? I weight this heavily because a team that doesn't know a model bakes text will lose a campaign discovering it at 6 p.m. on deadline day. Hailuo's marketing shows wins; this review documents the five failures above so your team learns them from me, not from a missed deadline.

Under this rubric, Hailuo is a strong Axis-1 model with weak Axis-2/3/4 alone, rescued on the paired desk. That's the real ranking. Not "best," not "worst" — best at the part it does, unfinished at the part you ship.

## A deeper walkthrough: Brief A, frame by frame

I want to show the perfume orbit in enough detail that you can predict your own result. The brief: "6-second perfume bottle rotating on a reflection floor, soft key light, no text, export 4:5 and 9:16."

Attempt 1 — Hailuo gave a bottle that started square and rounded its shoulders by frame 18. The reflection floor appeared only on the right side. Reject: shape instability.

Attempt 2 — I added "glass bottle, cylindrical, full reflection, centered" and "slow constant rotation." The bottle held. The reflection extended full width. This is the attempt I kept. Motion coherence: genuinely good. The rotation read as a product shot, not a simulation.

Attempt 3 — I tested "luxury feel, bokeh background." Hailuo blurred the background but also blurred the bottle's edge, softening the hero. Reject: edge crispness lost. Lesson: "luxury" as a motion adjective costs you the product's definition.

What I then did in Lovart: took attempt 2's still into ChatCanvas, locked Brand Kit (#C8642B accent on the label, not the bottle), exported 4:5 and 9:16 from the same composed frame. Hailuo animated the rotation; Lovart owned the brand and the crop. The two clips shipped to Instagram and Stories with the same label color and the bottle uncut.

The point of this walkthrough: Hailuo's win is real and specific (coherent rotation). The shipping work is Lovart's. Neither tool's marketing tells you this; only running the boring brief does.

## A deeper walkthrough: Brief B, the identity problem

Brief B was the founder walking through a studio, medium shot, shallow depth, 8 seconds. The brief mattered because founder-led content is where identity drift hurts most — if the founder looks like five cousins across five clips, the brand reads as inconsistent, and inconsistent reads as untrustworthy.

Attempt 1 — Hailuo held the face for five seconds, then the eye shape shifted at second six. Subtle, but a regular viewer notices "something's off" even if they can't name it.

Attempt 2 — I fed Hailuo a still of the founder (generated in Lovart with Brand Kit locked, consistent wardrobe) and asked for "slow walk, shallow depth." The animation respected the source face better because the starting frame was already correct. But across five separate clips generated on five days, the wardrobe lighting still drifted.

The fix was structural, not prompt-level: I generated all five source frames in one Lovart ChatCanvas session with Brand Kit locked, so the wardrobe, wall color, and logo placement were identical by construction. Then I animated each in Hailuo. The five founders became one founder. This is the part no text-to-video model solves — they have no session memory across generations. Lovart's Brand Kit is the memory.

If your use case is one hero founder clip, Hailuo alone is fine. If it's a founder series, you need the desk. Most brands posting weekly are in the second case.

## A deeper walkthrough: Brief C, the offer that didn't land

Brief C is the one that should worry every retail brand. "Two-for-one lunch, 11am–2pm, food close-up, 6-second loop." The offer is the entire point of the clip. If the offer doesn't land, the clip is decoration.

Hailuo rendered the food beautifully. It rendered "two-for-one lunch 11am-2pm" as baked texture with a hyphen that read as a minus, and the type was too small to read at 390px. I showed the clip to a coworker; ten seconds later they said "lunch something?" The hallway test failed.

The recovery path: I built the offer plate in Lovart ChatCanvas — "TWO-FOR-ONE LUNCH / 11AM–2PM" as editable type, large, high contrast — and used it as the hero frame. Hailuo animated the food close-up behind it; the type stayed sharp because it lived in Lovart, not in Hailuo's baked layer. The coworker test passed: "two-for-one lunch, 11 to 2." The offer landed.

This is the clearest demonstration of the central thesis: **type lives in the design layer, motion lives in the generation layer.** The moment you ask the model to render the offer, you've lost control of the one thing the clip exists to communicate.

## When to use Hailuo alone (and when not to)

Honest guidance, not a sales pitch.

**Use Hailuo alone when:** you need one hero clip, the subject is a physical object or a scene (not text), and you don't need brand consistency across a series. A single product orbit, a one-off cinematic city shot, a personal creative reel. In these cases Lovart is optional — generate in Hailuo, ship the clip.

**Use Hailuo + Lovart when:** the clip carries an offer, a brand, or a face that must repeat; you need more than one format; or the asset is part of a weekly campaign. Retail promos, founder series, product launches with typed CTAs, any work where a typo means regenerating. Here the desk isn't optional — it's the difference between shippable and stuck.

**Don't use Hailuo when:** you need editable text in the final video, long-form (it's sub-10s), or persistent character identity across many clips without a source-frame system. For those, generate the controlled frame in Lovart first, or use a tool built for series work.

The pattern across all three: Hailuo's value is bounded by "does the clip look good on first watch." Your job is bounded by "can a human correct this before Thursday." Know which boundary you're paying for.

## What I'd want from Hailuo next (a wishlist from the desk)

I'll close the evaluation half with what would actually change my workflow, stated plainly so the model's team hears the operator's side, not the demo's.

1. **An editable text layer post-generation.** Even a single locked text plate I can fix without regenerating would collapse the Axis-2 failure. Bake-free text is the single highest-impact fix.
2. **A session brand memory.** Let me set one hex and have it hold across a series. Brand Kit does this in Lovart; Hailuo has no equivalent and it shows in every multi-clip job.
3. **Source-frame locking for identity.** If I feed one correct founder still, hold that face across the series. Image-to-video is close; series consistency is the missing step.
4. **Native vertical composition, not cropped 16:9.** "Vertical" should recompose, not reframe. Until then, I build the frame in ChatCanvas at 9:16 and animate — which works, but it's a workaround.
5. **Honest failure docs.** Show the baked-text and drift cases in the marketing, not just the wins. Teams plan around known limits; they bleed around hidden ones.

None of these ask Hailuo to become a design tool. They ask it to stop losing the exit ramp — the editable, brandable, multi-format part that turns a clip into a shipped asset.
