# 竞品词落地页图片 Prompt 清单（13 页 × 14 槽位）
# 用于 Lovart/ComfyUI 批量生图
# 生成日期: 2026-06-18

## 跨页共享图片（仅需生成 1 套）

### [SHARED] feature-detail — MCoT Engine（所有页共用）
> Prompt: A split-screen infographic showing the difference between single-prompt AI generation (left: a simple text-to-image flow) vs Lovart's MCoT multi-step reasoning engine (right: a flowchart showing market research → concept planning → generation → refinement → export). Dark theme, Lovart brand purple accents. Clean tech illustration style.

### [SHARED] feature-detail — ChatCanvas（所有页共用）
> Prompt: An infinite canvas workspace with multiple design iterations visible — sketches, refined versions, color explorations. A chat panel on the side showing a conversation between user and AI agent. Modern UI design, dark mode, Lovart brand style. Example: www.lovart.ai/canvas

### [SHARED] feature-detail — Brand Kit（所有页共用）
> Prompt: A brand identity system dashboard showing color palettes, typography scale, logo variants, and usage examples. "Brand Kit" prominent. Multiple projects shown inheriting the same brand rules. Clean SaaS UI, dark theme with Lovart purple.

### [SHARED] canvas-wall — 10 张示例图（所有页共用）
> 以下 10 张为通用展示图，覆盖多品类：startup / e-commerce / agency / creator / enterprise / education / healthcare / real estate / restaurant / fashion
> Prompt (×10 variations): {category} design output on laptop and phone screens, professional lighting, clean modern workspace, branded materials visible. 
> 品类: "tech startup branding", "e-commerce product", "agency creative", "content creator", "enterprise presentation", "education materials", "healthcare brand", "real estate marketing", "restaurant menu design", "fashion lookbook"

---

## 每页独立图片

### 1. ai-logo-generator

#### hero-split
> Prompt: A user typing "modern tech startup logo" into the Lovart canvas, and the canvas responding with 4 distinct logo variations — wordmark, lettermark, abstract, combination mark — all with the same brand aesthetic. Clean dark UI, purple glow accents. Professional design tool interface.

#### bento-4 (4 张)
1. **Brand Context Engine**: Interface showing brand values input fields (mission, audience, industry) feeding into a logo generation pipeline. Like a brand strategy tool merged with a design tool.
2. **Multi-Style Exploration**: Grid of 6 logo variants — wordmark, lettermark, pictorial, abstract, combination, emblem — all for the same brand. Clean comparison layout.
3. **Surface-Aware Output**: One logo automatically displayed across favicon, app icon, Instagram profile, website header, business card, and t-shirt. Consistent scaling and adaptation.
4. **Touch Edit Refinement**: Close-up of a logo on canvas with a user clicking a color element, a popup showing "make this navy blue", and the logo updating in real time.

#### capability-tabs (4 张)
1. **From Brief**: Text input describing a company → flowing into logo generation. Business context emphasized.
2. **From Reference**: Upload panel with reference logos dropped in → moodboard extraction → original logo variations.
3. **From Sketch**: Phone photo of a paper sketch → digitized vector logo with polished finish. Before/after style.
4. **Brand Kit Export**: Export dialog showing SVG/PNG/PDF options plus color palette swatches and font pairings.

#### bento-2 (2 张)
1. **Autonomous Agent**: Canvas showing the agent auto-generating logo options, research notes visible in sidebar, user sipping coffee — hands-off workflow.
2. **Guided Collaboration**: Split view — user clicking elements + typing natural language instructions on one side, logo updating on the other.

---

### 2. ai-design-generator

#### hero-split
> Prompt: Lovart canvas with a creative brief panel on the left and multiple design outputs — social post, banner ad, presentation slide — all on-brand on the right. "AI Design Generator" header. Professional agency-style interface, dark mode, purple accents.

#### bento-4 (4 张)
1. **Context-Aware**: Brand palette + typography flowing into 3 different design outputs that all share the same visual identity.
2. **Multi-Format Output**: One concept shown as Instagram post, LinkedIn banner, email header, and print flyer — auto-adapted proportions.
3. **Touch Edit**: User pointer clicking a headline in a design → typing "make this bolder and larger" → instant update.
4. **Brand Kit Memory**: Timeline showing project 1 → 2 → 3 → 4, each inheriting the same brand rules automatically.

#### capability-tabs (4 张)
1. **From Brief**: Design spec input form → generated social media graphic, presentation, and ad creative.
2. **From Reference**: Moodboard upload → AI extracting color/typography/style patterns → original designs.
3. **Batch Generate**: Single brief → 10 design variants for A/B testing, all consistently branded.
4. **Export Ready**: Multi-format export panel — Instagram (1080×1080), LinkedIn (1200×627), Story (1080×1920).

#### bento-2 (2 张)
1. **Autonomous**: Agent autonomously creating designs while showing its reasoning in a sidebar.
2. **Guided**: User manually adjusting layout with Touch Edit while AI suggests improvements.

---

### 3. ai-avatar

#### hero-split
> Prompt: One reference photo on the left → 9 different avatar styles on the right (professional headshot, cartoon, anime, 3D, pixel art, watercolor, vector flat, cyberpunk, vintage). Lovart canvas interface. Avatar maker theme.

#### bento-4 (4 张)
1. **Context-Aware**: Same face rendered in 4 different contexts — LinkedIn professional, gaming avatar, brand mascot, social profile — maintaining identity.
2. **Multi-Format**: Same avatar output as profile circle, full-body illustration, emoji set, and banner header.
3. **Touch Edit**: Click on avatar's hair → "make it shorter and blonde" → instant update keeping face identity.
4. **Brand Kit Memory**: Character style guide panel — reference face, style presets, color palette — all locked for consistency.

#### capability-tabs (4 张)
1. **From Brief**: Text description "young professional woman, friendly, approachable" → generated avatars.
2. **From Reference**: Upload 3 photos of same person → AI learns face → generates consistent avatars in any style.
3. **Batch Generate**: 20 avatars generated from one reference — different expressions, poses, outfits.
4. **Export Ready**: Avatar export panel — PNG with transparency, multiple sizes, style variants organized.

#### bento-2 (2 张)
1. **Autonomous**: Agent auto-generating avatar variations while user reviews.
2. **Guided**: User fine-tuning eye shape, nose, mouth via Touch Edit sliders/descriptions.

---

### 4. ai-ad-generator

#### hero-split
> Prompt: Product photo on the left → 4 ad variants on the right (Facebook carousel, Instagram Story, Google Display, TikTok video frame). All share same campaign messaging. "AI Ad Generator" header. Marketing dashboard aesthetic, dark mode.

#### bento-4 (4 张)
1. **Context-Aware**: Campaign brief input (product, audience, budget, goals) → ad creative that reflects the strategy.
2. **Multi-Format**: One ad concept auto-resized to Meta Feed, Story, Display Banner, and Vertical Video — native to each.
3. **Touch Edit**: Click headline → "make it more urgent" → copy updates across all formats.
4. **Brand Kit**: Brand logo + colors + fonts automatically applied to every ad variant without manual setup.

#### capability-tabs (4 张)
1. **From Brief**: Product info + target audience → multiple ad directions with different hooks and visuals.
2. **From Reference**: Upload winning ads from competitors → AI extracts successful patterns → creates original variants.
3. **Batch Generate**: 50 ad variants for multivariate testing, organized by hook/visual/CTA combination.
4. **Export Ready**: Platform-specific exports — Meta ad specs, Google Display sizes, TikTok video format.

#### bento-2 (2 张)
1. **Autonomous**: Agent autonomously generating and A/B testing ad variants.
2. **Guided**: Marketer tweaking ad copy and visuals with Touch Edit, previewing on device mockups.

---

### 5. ai-commercial

#### hero-split
> Prompt: A product brief on the left flowing into a finished commercial video on the right, with storyboard frames, script excerpts, and variant versions visible mid-process. Video production studio aesthetic with Lovart interface elements. Dark theme.

#### bento-4 (4 张)
1. **Context-Aware**: Brand values + product specs + target audience → storyboard and script auto-generated.
2. **Multi-Format**: Same commercial output as 16:9 YouTube, 9:16 TikTok, 1:1 Instagram — with auto-cropping.
3. **Touch Edit**: Click a scene → "change background to sunset" → entire scene updates with consistent lighting.
4. **Brand Kit**: Brand colors + logo watermark automatically applied to every frame.

#### capability-tabs (4 张)
1. **From Brief**: Product description → full commercial script + storyboard + generated video.
2. **From Reference**: Upload reference commercial → AI extracts pacing, transitions, color grade → applies to new product.
3. **Batch Generate**: Multiple commercial variants — different hooks, different music, different CTAs.
4. **Export Ready**: Export panel — 4K/1080p, horizontal/vertical/square, with/without subtitles.

#### bento-2 (2 张)
1. **Autonomous**: Agent generating full commercial from brief, showing progress: script ✓ → storyboard ✓ → video ✓.
2. **Guided**: Director refining scenes frame-by-frame with Touch Edit and natural language.

---

### 6. ai-banner

#### hero-split
> Prompt: Multiple banner ads displayed on mockup screens — Google Display Network, website leaderboard, email header, social cover photo. All from one design brief. "AI Banner Generator" header. Ad-tech dashboard aesthetic. Dark theme Lovart UI.

#### bento-4 (4 张)
1. **Context-Aware**: Campaign brief → banner creative that matches the campaign message and CTA.
2. **Multi-Format**: One banner concept auto-generated as leaderboard (728×90), medium rectangle (300×250), skyscraper (160×600), mobile banner (320×50).
3. **Touch Edit**: Click CTA button → "test 'Shop Now' vs 'Get 50% Off'" → both variants generated.
4. **Brand Kit**: Brand assets automatically applied — no manual color picking or logo placement.

#### capability-tabs (4 张)
1. **From Brief**: Campaign goal + product → banner creatives with strategic messaging.
2. **From Reference**: Upload top-performing banners → AI learns layout patterns → creates fresh originals.
3. **Batch Generate**: 30 banner sizes from one concept, all IAB standard dimensions.
4. **Export Ready**: Export as HTML5, static JPG/PNG, or GIF — all optimized for ad platforms.

#### bento-2 (2 张)
1. **Autonomous**: Agent generating banner sets while optimizing for CTR based on historical data.
2. **Guided**: Designer refining layout and copy with Touch Edit, previewing on device mockups.

---

### 7. brand-video

#### hero-split
> Prompt: Brand story timeline on the left → polished brand video on the right, with brand identity elements (logo, colors, typography) woven throughout. Corporate video production aesthetic. "Brand Video Generator" on Lovart interface.

#### bento-4 (4 张)
1. **Context-Aware**: Brand book upload → video storyboard that reflects brand personality and values.
2. **Multi-Format**: Brand video output as YouTube hero, website header, social teaser, and TV commercial format.
3. **Touch Edit**: Click a transition → "make it smoother, add brand color overlay" → instant update.
4. **Brand Kit**: Brand identity automatically applied to motion graphics, lower thirds, and outro card.

#### capability-tabs (4 张)
1. **From Brief**: Company story → script → storyboard → finished brand video.
2. **From Reference**: Upload brand film references → AI extracts cinematic language → applies.
3. **Batch Generate**: Multiple brand video variants — different tones (inspirational, educational, product-focused).
4. **Export Ready**: Export in broadcast, web, and social specs.

#### bento-2 (2 张)
1. **Autonomous**: Agent producing full brand video from company brief.
2. **Guided**: Creative director fine-tuning pacing and visuals with Touch Edit.

---

### 8. character-consistency

#### hero-split
> Prompt: Same character (young woman with red hair, glasses) appearing in 6 completely different scenes — office, beach, coffee shop, library, park, concert — with identical face, outfit, and proportions. Before/after comparison with other AI tools showing inconsistency. "Character Consistency" header. Dark UI.

#### bento-4 (4 张)
1. **Context-Aware**: Character reference sheet → every generated image maintains the exact character appearance.
2. **Multi-Format**: Same character as comic panel, animation frame, game sprite, and illustration — all consistent.
3. **Touch Edit**: Click character's outfit → "change to winter coat" → updates across all scenes.
4. **Brand Kit**: Character locked in Brand Kit — face, body type, outfit, style — immutable across projects.

#### capability-tabs (4 张)
1. **From Reference**: Upload 3 photos of character → AI creates reference model → generates infinite consistent scenes.
2. **Style Transfer**: Same character rendered in anime, realistic, 3D, watercolor, and pixel art styles.
3. **Batch Scenes**: 20 scenes with same character — different locations, lighting, emotions — all consistent.
4. **Export Ready**: Character sheet export + individual scene renders.

#### bento-2 (2 张)
1. **Autonomous**: Agent generating storyboard with consistent character across all frames.
2. **Guided**: Artist fine-tuning character details while AI maintains consistency.

---

### 9. lip-sync

#### hero-split
> Prompt: Audio waveform on the left → talking avatar on the right with perfect lip sync. Mouth shapes matching phonemes visible in a reference panel. "AI Lip Sync" header. Video production UI. Dark theme.

#### bento-4 (4 张)
1. **Context-Aware**: Script text → voiceover → avatar with natural lip movements matching the speech.
2. **Multi-Format**: Same talking video as horizontal presentation, vertical social clip, and square ad.
3. **Touch Edit**: Click mouth at timestamp → "make smile wider here" → precise adjustment.
4. **Brand Kit**: Branded lower third, intro/outro, and watermark auto-applied.

#### capability-tabs (4 张)
1. **From Audio**: Upload audio file → AI generates lip-synced avatar automatically.
2. **From Text**: Type script → AI generates voiceover + synced avatar in one step.
3. **Batch Generate**: Multiple language versions — same avatar, different languages, perfect sync.
4. **Export Ready**: Export as MP4 with embedded subtitles, multiple resolutions.

#### bento-2 (2 张)
1. **Autonomous**: Agent handling full pipeline: script → voice → avatar → video.
2. **Guided**: Editor fine-tuning lip sync timing and expressions frame-by-frame.

---

### 10. marketing-video-ai

#### hero-split
> Prompt: Marketing brief on the left → finished product explainer video on the right, with structure (hook → problem → solution → CTA) visible mid-process. "AI Marketing Video" header. Marketing dashboard aesthetic on Lovart canvas.

#### bento-4 (4 张)
1. **Context-Aware**: Product page URL → AI extracts features → generates video script and visuals.
2. **Multi-Format**: Marketing video output as YouTube ad, Instagram Reel, TikTok, and website hero.
3. **Touch Edit**: Click product shot → "zoom in on the feature being described" → scene adjusts.
4. **Brand Kit**: Brand identity auto-applied — intro animation, color grade, end card.

#### capability-tabs (4 张)
1. **From Product**: Product details → AI researches market → generates compelling marketing narrative.
2. **From Reference**: Upload competitor videos → AI extracts effective patterns → original marketing video.
3. **Batch Generate**: Multiple versions — different hooks, different CTAs — for A/B testing.
4. **Export Ready**: Platform-optimized exports with aspect ratios and durations per platform best practices.

#### bento-2 (2 张)
1. **Autonomous**: Agent producing complete marketing video from product brief.
2. **Guided**: Marketing manager refining messaging and visuals with Touch Edit.

---

### 11. product-video

#### hero-split
> Prompt: Product photo on white background on the left → same product in a realistic lifestyle scene on the right — proper lighting, shadows, context. "AI Product Video" header. E-commerce studio aesthetic with Lovart UI elements.

#### bento-4 (4 张)
1. **Context-Aware**: Product specs + target customer → AI places product in contextually relevant scenes.
2. **Multi-Format**: Product video as e-commerce listing, social ad, website showcase, and email GIF.
3. **Touch Edit**: Click background → "change to marble countertop with natural light" → realistic update.
4. **Brand Kit**: Brand styling applied to scene — consistent lighting temperature, color grade.

#### capability-tabs (4 张)
1. **From Photo**: Upload product photo on white → 360° rotation video generated automatically.
2. **From Reference**: Upload lifestyle reference → AI matches lighting, composition, and mood.
3. **Batch Scenes**: One product → 10 different lifestyle scenes (kitchen, office, outdoor, studio).
4. **Export Ready**: Export as looping video, still frames, and platform-specific formats.

#### bento-2 (2 张)
1. **Autonomous**: Agent generating full product showcase from photos.
2. **Guided**: Art director positioning product and adjusting scene details.

---

### 12. social-media-video

#### hero-split
> Prompt: Social content calendar on the left → auto-generated videos for TikTok, Reels, Shorts on the right — all with consistent branding but platform-native formats. "AI Social Video" header. Creator dashboard aesthetic on Lovart canvas.

#### bento-4 (4 张)
1. **Context-Aware**: Brand voice + content pillars → video concepts that match brand personality.
2. **Multi-Format**: Same content auto-formatted for TikTok (9:16, 60s), Reels (9:16, 90s), Shorts (9:16, 60s), and Pinterest (2:3).
3. **Touch Edit**: Click caption text → "make it more casual and Gen-Z" → tone updates across video.
4. **Brand Kit**: Brand colors, logo bug, and end card auto-applied to every video.

#### capability-tabs (4 张)
1. **From Trend**: Trending audio/sound → AI generates matching video content with brand overlay.
2. **From Script**: Write a hook → AI generates full short-form video with captions and transitions.
3. **Batch Schedule**: One brief → 7 videos for the week, each with different hooks and formats.
4. **Export Ready**: Platform-native exports with auto-generated captions and hashtag suggestions.

#### bento-2 (2 张)
1. **Autonomous**: Agent auto-generating daily social content from content calendar.
2. **Guided**: Creator fine-tuning hook, pacing, and captions with Touch Edit.

---

### 13. talking-avatar

#### hero-split
> Prompt: A single portrait photo on the left → the same person as a lifelike talking avatar on the right, mid-speech with natural facial expressions and gestures. "AI Talking Avatar" header. Video presentation aesthetic. Dark Lovart UI.

#### bento-4 (4 张)
1. **Context-Aware**: Photo upload → AI creates 3D head model → generates natural speech animations.
2. **Multi-Format**: Same avatar as corporate presenter, tutorial host, virtual assistant, and personalized message.
3. **Touch Edit**: Click expression → "more enthusiastic and energetic" → face adjusts naturally.
4. **Brand Kit**: Branded background, lower third, and intro animation auto-applied.

#### capability-tabs (4 张)
1. **From Photo**: One photo → fully animated avatar ready to speak any script.
2. **From Script**: Type presentation text → avatar delivers it with natural pacing and gestures.
3. **Batch Languages**: Same avatar delivering same message in English, Spanish, Mandarin, Japanese.
4. **Export Ready**: Export as video with transparent background, with/without subtitles.

#### bento-2 (2 张)
1. **Autonomous**: Agent generating complete training video with avatar presenter.
2. **Guided**: Director fine-tuning avatar expressions, gestures, and timing.

---

## 生成参数建议

- **分辨率**: hero-split → 1200×900, bento/capability-tabs/canvas-wall → 800×800, feature-detail → 1000×600
- **风格**: Clean SaaS/tech aesthetic, Lovart brand purple (#7C3AED) accents, dark mode UI with subtle gradients
- **人物**: Diverse models, professional but approachable, natural expressions
- **文案覆盖**: 图片中不嵌入具体文案（避免多语言版本需要重新生成），用占位线条或 Lorem ipsum
- **格式**: PNG with transparency for UI elements, JPG for scene images
- **总量**: ~182 张（含共享图 13 张），实际独立图 ~156 张
