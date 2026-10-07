## Prompt patterns that actually work (copy these)

After two weeks I have a short list of prompt shapes that reliably produce shippable motion in Hailuo. These are the ones I reuse; the ones that fail are in the failure log above.

**Object orbit.** "〔object〕rotating 360° on 〔surface〕, 〔light〕key light, constant slow rotation, no text, 6s." The constants that matter: name the rotation speed ("constant slow"), name the surface ("reflection floor"), and ban text. Without "no text" Hailuo adds decorative type you'll have to remove in Lovart.

**Founder b-roll.** Start from a Lovart-generated still of the founder with Brand Kit locked. Prompt Hailuo: "slow dolly-in, shallow depth, 8s, keep subject identical to source frame." Feeding the correct still is what holds identity — don't ask Hailuo to invent the face.

**Food close-up loop.** " Extreme close-up of 〔dish〕, steam rising slow, 6s loop, no text." Then build the offer plate in Lovart ChatCanvas and composite it over the loop. The food is Hailuo; the offer is Lovart. Never merge them in the prompt.

**City establishing shot.** " Wide establishing shot of 〔city〕at blue hour, slow crane up, 10s, cinematic, no text." Hailuo's camera intent shines here. Keep it text-free and add any title in Lovart after.

**Product hero for social.** State the crop in the brief before generating: " composed for 4:5 Instagram, product centered, negative space top for headline, no text." Build the negative space in ChatCanvas so Lovart's headline drops in clean. Hailuo animates the product; Lovart owns the zone.

The pattern across all five: describe the physical motion precisely, ban text explicitly, and let Lovart own everything that must be edited later. Prompts that mix "make it pretty" with "put the offer on screen" produce pretty clips with broken offers.

## What I'd tell May next time

May shipped the Thursday asset. The perfume orbit went live on Instagram and Stories with the same label color and the bottle uncut. The voice note I got back was "the lunch promo is the one I'm worried about" — so the next week we ran Brief C the Lovart-first way: offer plate built in ChatCanvas, food still at 8K, Hailuo animating only the steam. The coworker hallway test passed. The offer landed.

If I could give every small team one sentence before they touch a text-to-video model, it's this: the clip is a rough cut, not the job. The job is the corrected, on-brand, multi-format asset that actually goes live — and that job lives in a design desk, not in the model that made the motion. Hailuo makes the motion well. Lovart makes it shippable. Use each for the half it's best at, and Thursday stops owning you.
