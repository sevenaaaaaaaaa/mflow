#!/usr/bin/env node
/**
 * Generate Solution page reference cases (composite-v2, 12 sections × 6 storylines).
 * Run: node _generate-examples.js
 */
const fs = require('fs')
const path = require('path')

const STORYLINES = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'solution-storylines-v2.json'), 'utf8')
)

const IMG = {
  hero: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/55b94439550ff0fefec6a09ca160df2fe8d0f24f.png',
  bento1: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/7eb9d35ed6aaf819fbe425badb3310b77bdc38a7.png',
  bento2: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/5d48ca781dea8ab12d0c93fc32e3ad8afa815631.png',
  bento3: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/eb6f103da589f07f425f2c736237e33f4d1719fa.png',
  bento4: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/4c90f673629d0bbd5fce85ad374352d4e40deb3e.png',
  tab1: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/b8e9479301c56b3946bbce10cadc78b70e0d6365.png',
  tab2: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/1f66f7b0726f0b3f59645d6b3a471691818a07f2.png',
  tab3: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/8efdfd8318084a8c88bb72c706bb33c7f2564b8b.png',
  showcase1: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/181ed5a5733bccb4594c29e1c15bd1ce93f8ea52.png',
  showcase2: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/98dde485f8c6789596006f5ee601a445d6606b78.png',
  showcase3: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/805d2e070d4404ed0cd6ae865930375919374b97.png',
  mosaic1: 'https://assets-persist.lovart.ai/img/d92cfdbbb4c243d8a269dc6d1301540c/5049909fb1610fbc90ed8b25cfecc77ffc14fcee.png',
  mosaic2: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/7eb9d35ed6aaf819fbe425badb3310b77bdc38a7.png',
  mosaic3: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/4c90f673629d0bbd5fce85ad374352d4e40deb3e.png',
  mosaic4: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/5d48ca781dea8ab12d0c93fc32e3ad8afa815631.png',
  mktHero: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/437351775c82f2d4aa7628eccd1ffa393a8d8010d3b448678901622628cc95cf.png',
  mktB1: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/76f6f16db402baffa46024261bf5603e63fe763833b01f497731603a2495a346.png',
  mktB2: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/23baa922486b6ebd84c24d0f0af8b451e1792f3565221b27ceff84b20b125669.png',
  mktB3: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/a5b053a156c28e87940cd226a93c311a07f437b5c0c48635f6b3240fe57b6de8.png',
  mktB4: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/181f2cd3e3b8744401ef85904d63f0c07c492887604dcacd369ea3e807183bc6.png',
  agencyHero: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/b6ac2200d8f883894a7f18ee1da19d7d7aab2a7f.png',
  agencyDetail: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/d11411bc15e95312819272bf39a65a3cbdf230b2.png',
}

function orderSections(storylineId, sectionsByType) {
  const order = STORYLINES.storylines[storylineId].sections
  return order.map((type) => {
    const s = sectionsByType[type]
    if (!s) throw new Error(`Missing ${type} for ${storylineId}`)
    return { ...s, type }
  })
}

function buildPage({ slug, title, description, keywords, ogImage, storyline, sectionsByType }) {
  const ordered = orderSections(storyline, sectionsByType)
  return {
    _type: 'compositePage',
    category: 'solution',
    slug,
    title,
    description,
    sourceType: 'solution',
    storyline,
    bodyJson: JSON.stringify(ordered),
    seo: {
      title: `${title} | Lovart`,
      description,
      keywords,
      noIndex: true,
      ogImage: {
        _type: 'imageSource',
        url: ogImage,
        alt: title,
        sourceType: 'external',
      },
    },
    language: 'en',
    schemaVersion: 'composite-v2',
    url_path: `/solution/${slug}`,
    section: ordered,
  }
}

// --- solution-ecommerce (Shopify) ---
const shopifyByType = {
  'hero-journey': {
    badge: 'Shopify Growth Solution',
    title: 'Design for every step',
    highlightedText: 'from click to repeat purchase',
    description:
      'A Shopify funnel is not one asset. Lovart keeps context alive from paid creative to product page, checkout reassurance, post-purchase email, and retargeting content.',
    buttons: [
      { text: 'Map the journey', href: '', variant: 'primary' },
      { text: 'See product visuals', href: '', variant: 'secondary' },
    ],
    journeyCards: [
      { step: '01', title: 'Traffic hook', subtitle: 'Meta, TikTok, Google creative that matches the offer.', icon: 'social' },
      { step: '02', title: 'Landing page', subtitle: 'Hero, proof, comparison, and CTA from one campaign brief.', icon: 'pointer' },
      { step: '03', title: 'PDP proof', subtitle: 'Product photos, mockups, reviews, and use-case scenes.', icon: 'image' },
      { step: '04', title: 'Checkout confidence', subtitle: 'Trust badges, bundle visuals, and guarantee graphics.', icon: 'brand' },
      { step: '05', title: 'Retention loop', subtitle: 'Email, SMS, and retargeting variants from one brand system.', icon: 'refresh' },
    ],
  },
  'bento-4': {
    title: 'Four pillars of the Shopify creative solution',
    description: 'What every DTC team gets when production, brand, and channel specs stay in one agent workflow.',
    columns: 4,
    features: [
      { title: 'Brand Kit', description: 'Lock colors, type, and logo rules across every asset.', media: { src: IMG.bento1, alt: 'Brand Kit' } },
      { title: 'Product visuals', description: 'PDP hero shots, lifestyle scenes, and marketplace crops.', media: { src: IMG.bento4, alt: 'Product visuals' } },
      { title: 'Paid social variants', description: 'Meta, TikTok, and Google hooks from one brief.', media: { src: IMG.bento2, alt: 'Paid social' } },
      { title: 'Editable exports', description: 'Touch Edit and Text Edit without regenerating winners.', media: { src: IMG.bento3, alt: 'Editable exports' } },
    ],
  },
  'capability-tabs': {
    title: 'Four modules in one Shopify solution',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      { label: 'Research', icon: 'search', content: { title: 'Start from SKU and market context', description: 'Upload product photos, brand guides, competitor URLs, and offer details.', media: { src: IMG.tab1, alt: 'Research' }, points: ['Competitor analysis', 'Product spec intake', 'Audience framing'] } },
      { label: 'Product visuals', icon: 'image', content: { title: 'Generate PDP and catalog imagery', description: 'Hero shots, lifestyle scenes, bundles, and marketplace crops from one SKU brief.', media: { src: IMG.hero, alt: 'Product visuals' }, points: ['1:1, 4:5, 9:16 crops', 'Mockups', 'SKU labeling'] } },
      { label: 'Acquisition', icon: 'sparkle', content: { title: 'Scale paid and organic creative', description: 'Turn PDP directions into ad hooks, landing modules, and email headers.', media: { src: IMG.tab2, alt: 'Acquisition' }, points: ['Fast Mode tests', 'Offer badges', 'Channel sizing'] } },
      { label: 'Retention', icon: 'refresh', content: { title: 'Extend winners post-launch', description: 'Refresh retargeting, post-purchase email, and seasonal campaigns.', media: { src: IMG.tab3, alt: 'Retention' }, points: ['Localized offers', 'CRM headers', 'Remarketing frames'] } },
    ],
  },
  'bento-2': {
    title: 'Two outcomes Shopify teams measure',
    columns: 2,
    features: [
      { title: 'More creative tests', description: 'Weekly hook and offer variants without a production queue.', media: { src: IMG.bento2, alt: 'Creative tests' } },
      { title: 'One visual system', description: 'PDP, ads, email, and social look like the same brand.', media: { src: IMG.bento1, alt: 'Visual system' } },
    ],
  },
  'workflow-vertical': {
    title: 'How the Shopify solution ships',
    description: 'From product brief to full-funnel rollout.',
    layout: 'vertical',
    steps: [
      { step: 1, title: 'Upload SKU and brand context', description: 'Product photos, brand PDFs, PDP screenshots, competitor URLs.', media: { src: IMG.hero, alt: 'Upload context' } },
      { step: 2, title: 'Generate the conversion asset set', description: 'PDP visuals, ads, social crops, and email headers from one brief.', media: { src: IMG.bento3, alt: 'Generate assets' } },
      { step: 3, title: 'Refine, test, and export', description: 'Touch Edit, Text Edit, and Brand Kit — then export channel-ready sizes.', media: { src: IMG.tab2, alt: 'Refine and export' } },
    ],
  },
  'comparison-table': {
    title: 'Lovart vs common Shopify creative workflows',
    description: 'Agent workflow vs fragmented production.',
    headers: ['Need', 'Single-purpose AI generator', 'Manual design workflow', 'Lovart Shopify Solution'],
    highlightColumn: 3,
    rows: [
      { feature: 'Start from business context', values: ['One prompt at a time', 'Strategist + designer handoffs', 'SKU, offer, brand, and URLs in one brief'] },
      { feature: 'Create full-funnel assets', values: ['One image at a time', 'Multiple tools', 'PDP, ads, email, landing, social, video'] },
      { feature: 'Edit after generation', values: ['Regenerate whole output', 'Manual edits', 'Touch Edit, Text Edit, Edit Elements'] },
      { feature: 'Preserve brand consistency', values: ['Prompt repetition', 'Guidelines + QA', 'Brand Kit across exports'] },
      { feature: 'Scale variants', values: ['Prompt duplication', 'Slow queue', 'Fast Mode for hooks and markets'] },
    ],
  },
  'cluster-block-dense': {
    title: 'Where Shopify funnels leak creative performance',
    description: 'Operational problems this solution fixes.',
    cards: [
      { icon: 'chat', title: 'Ad-to-page mismatch', description: 'Paid social and PDP visuals tell different stories.' },
      { icon: 'image', title: 'Weak product imagery', description: 'SKU photos do not create desire or trust.' },
      { icon: 'flask', title: 'Slow A/B tests', description: 'Every hook change becomes a design ticket.' },
      { icon: 'brand', title: 'Brand drift', description: 'Channels slowly stop looking like one brand.' },
      { icon: 'globe', title: 'Localization bottleneck', description: 'New markets rebuilt manually.' },
      { icon: 'refresh', title: 'No post-launch loop', description: 'Cannot refresh winners for remarketing.' },
    ],
  },
  'showcase-stacked': {
    title: 'From flat SKU photo to conversion-ready creative',
    items: [
      { media: { src: IMG.showcase1, alt: 'Product visuals' }, title: 'Product visuals — generate desire', description: 'Lifestyle scenes and marketplace crops from SKU photos.', cta: { text: 'Create product visuals', href: '' } },
      { media: { src: IMG.showcase2, alt: 'Touch Edit' }, title: 'Touch Edit — fix the exact leak', description: 'Change a label or background without destroying the composition.', cta: { text: 'Try precise editing', href: '' } },
      { media: { src: IMG.showcase3, alt: 'Text Edit' }, title: 'Text Edit — sale copy stays editable', description: 'Swap discount and urgency claims inside finished images.', cta: { text: 'Edit offer copy', href: '' } },
    ],
  },
  'review-grid-3col': {
    title: 'What changes when ecommerce teams work with an agent',
    columns: 3,
    reviews: [
      { title: 'From SKU photo to campaign system', body: 'PDP images, ad variants, and email headers in one session — edits stayed connected.', author: 'Lena Brooks', role: 'Founder, Glow Pantry' },
      { title: 'Creative tests stopped feeling expensive', body: 'Fast Mode for hooks, Thinking Mode for winners — we test weekly now.', author: 'Noah Kim', role: 'Performance Marketer' },
      { title: 'Brand consistency finally scaled', body: 'Brand Kit gave us a guardrail across every export.', author: 'Amara Cole', role: 'Brand Lead, Ritual Home' },
      { title: 'Text Edit saved promotion updates', body: 'Changing sale copy without remaking the whole asset.', author: 'Miguel Santos', role: 'Lifecycle Manager' },
      { title: 'Mockups sold the product story', body: 'Scenes looked real enough for ads before the final shoot.', author: 'Grace Huang', role: 'Merchandising Lead' },
      { title: 'Workflow stayed alive after launch', body: 'Launch direction became retargeting and localized assets.', author: 'Ethan Reed', role: 'Shopify Operator' },
    ],
  },
  'pricing-block': { title: 'Choose the Shopify creative workflow depth you need', description: 'Start free. Upgrade when campaigns go paid.' },
  faq: {
    title: 'AI Design Solution for Shopify FAQ',
    items: [
      { question: 'Is Lovart a Shopify app?', answer: 'Lovart is an AI design agent workflow for Shopify teams — not a Shopify admin plugin.' },
      { question: 'What should we upload first?', answer: 'SKU photos, brand guidelines, ads, PDP screenshots, specs, competitor URLs, and channel sizes.' },
      { question: 'Full-funnel from one brief?', answer: 'Yes — PDP, paid social, landing modules, email headers, and video keyframes.' },
      { question: 'Brand consistency?', answer: 'Brand Kit locks colors, typography, and logo rules on every generation.' },
      { question: 'Edit after generation?', answer: 'Touch Edit, Text Edit, and Edit Elements fix details without full regeneration.' },
      { question: 'Commercial usage?', answer: 'Paid plans include commercial rights. Check your plan for export limits.' },
    ],
  },
  'cta-default': {
    title: 'Ready to turn one SKU into a full Shopify launch system?',
    description: 'Start free — upload your first product brief on ChatCanvas.',
    buttons: [
      { text: 'Design a Shopify launch', action: 'openLogin', variant: 'primary' },
      { text: 'See the workflow', href: '', variant: 'secondary' },
    ],
  },
}

// --- solution-team (Marketing Teams) ---
const teamByType = {
  'hero-cinematic': {
    tag: 'Marketing Team Solution',
    title: 'Scale marketing creative without',
    highlightedText: 'scaling design headcount',
    description:
      'Lovart lets marketing teams produce 5× more visual content — social ads, email campaigns, landing pages, event materials — with brand consistency and zero design bottlenecks.',
    buttons: [
      { text: 'Start scaling creative', href: '', variant: 'primary' },
      { text: 'See team workflows', href: '', variant: 'secondary' },
    ],
    media: { src: IMG.mktHero, alt: 'Marketing team creative workflow in Lovart' },
  },
  'bento-4': {
    title: 'Four capabilities in the marketing team solution',
    description: 'Distributed production with centralized brand control.',
    columns: 4,
    features: [
      { title: 'Batch generation', description: 'One campaign brief → full visual suite.', media: { src: IMG.mktB1, alt: 'Batch generation' } },
      { title: 'Brand governance', description: 'Brand Kit with role-based permissions.', media: { src: IMG.mktB4, alt: 'Brand governance' } },
      { title: 'Same-day reactive', description: 'Trending moments in under 10 minutes.', media: { src: IMG.mktB3, alt: 'Reactive content' } },
      { title: 'A/B at scale', description: '10–20 ad variants per campaign.', media: { src: IMG.mktB2, alt: 'A/B testing' } },
    ],
  },
  'capability-tabs': {
    title: 'How marketing teams run on Lovart',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      { label: 'Distribute', icon: 'globe', content: { title: 'Marketers produce their own assets', description: 'Channel owners create in ChatCanvas — constrained by Brand Kit.', media: { src: IMG.mktB1, alt: 'Distributed' }, points: ['Role-based access', 'Self-serve social/email', 'No design queue'] } },
      { label: 'Batch', icon: 'sparkle', content: { title: 'Launch campaigns in one session', description: 'Theme, audience, messaging → ads, headers, landing heroes.', media: { src: IMG.mktHero, alt: 'Batch' }, points: ['Multi-channel sizes', 'Offer variants', 'Event graphics'] } },
      { label: 'Test', icon: 'flask', content: { title: 'Statistically meaningful creative tests', description: 'Headline, imagery, CTA, and color variants at scale.', media: { src: IMG.mktB2, alt: 'Test' }, points: ['Paid social matrices', 'Email visual pairs', 'Landing hero variants'] } },
      { label: 'Reallocate', icon: 'brand', content: { title: 'Free designers for strategic work', description: '50–70% capacity back to brand and motion projects.', media: { src: IMG.mktB4, alt: 'Reallocate' }, points: ['Creative direction', 'Custom illustration', 'High-impact concepts'] } },
    ],
  },
  'bento-2': {
    title: 'Two shifts marketing leaders expect',
    columns: 2,
    features: [
      { title: '4× creative output', description: 'Same headcount, more channels, faster publish.', media: { src: IMG.mktB3, alt: 'Output' } },
      { title: 'Same-day turnaround', description: 'Reactive content while the moment trends.', media: { src: IMG.mktB2, alt: 'Turnaround' } },
    ],
  },
  'workflow-vertical': {
    title: 'Marketing team rollout in three steps',
    description: 'From brand setup to distributed production.',
    layout: 'vertical',
    steps: [
      { step: 1, title: 'Set up Brand Kit and permissions', description: 'Lock colors and typography; assign marketer vs reviewer roles.', media: { src: IMG.mktB4, alt: 'Brand setup' } },
      { step: 2, title: 'Distribute production to channel owners', description: 'Social, email, and demand gen generate within brand boundaries.', media: { src: IMG.mktB1, alt: 'Distribute' } },
      { step: 3, title: 'Test, approve, and scale winners', description: 'Design reviews quality; growth scales variants across channels.', media: { src: IMG.mktHero, alt: 'Scale' } },
    ],
  },
  'comparison-table': {
    title: 'Lovart vs traditional marketing creative workflows',
    headers: ['Need', 'Design team queue', 'Fragmented AI tools', 'Lovart Marketing Solution'],
    highlightColumn: 3,
    rows: [
      { feature: 'Production volume', values: ['40–60 assets/month', 'One-off generations', '300–1000+ on Team/Business'] },
      { feature: 'Reactive speed', values: ['3–7 days', 'Minutes, no brand memory', 'Same-day with Brand Kit'] },
      { feature: 'Brand consistency', values: ['Manual QA', 'Prompt luck', 'Locked Brand Kit'] },
      { feature: 'Creative testing', values: ['2–3 variants', 'No shared matrix', '10–20 from one brief'] },
      { feature: 'Designer focus', values: ['60% production', 'Tool switching', '50–70% back to strategy'] },
    ],
  },
  'cluster-block-dense': {
    title: 'Marketing scenarios this solution covers',
    description: 'Named use cases teams deploy today.',
    cards: [
      { icon: 'brand', title: 'B2B SaaS content engine', description: 'Blog, LinkedIn, webinar, and sales one-pagers.' },
      { icon: 'sparkle', title: 'E-commerce holiday ramp', description: '40–60 assets per event without freelance bottlenecks.' },
      { icon: 'globe', title: 'Global regional campaigns', description: 'Local adaptations with locked global identity.' },
      { icon: 'social', title: 'Paid social refresh', description: 'Weekly Meta, TikTok, LinkedIn creative.' },
      { icon: 'pointer', title: 'Product launch suites', description: 'Ads, email, landing, partner assets in one batch.' },
      { icon: 'refresh', title: 'Lifecycle and retention', description: 'Post-purchase and nurture on one canvas.' },
    ],
  },
  'showcase-stacked': {
    title: 'What changes when marketing owns production',
    items: [
      { media: { src: IMG.mktB1, alt: 'Batch' }, title: 'Batch generation — one brief, full suite', description: 'Launch themes become ads, headers, and event graphics.', cta: { text: 'Try a campaign brief', href: '' } },
      { media: { src: IMG.mktB2, alt: 'A/B' }, title: 'A/B testing at statistical scale', description: 'Variants at the volume performance marketing requires.', cta: { text: 'Generate ad variants', href: '' } },
      { media: { src: IMG.mktB4, alt: 'Brand' }, title: 'Brand governance at scale', description: 'Creative freedom within boundaries — no visual chaos.', cta: { text: 'Set up Brand Kit', href: '' } },
    ],
  },
  testimonial: {
    title: 'Marketing teams scaling creative with Lovart',
    testimonials: [
      { quote: 'Creative output went up 4×. Design headcount stayed flat. Publish dropped from five days to same-day.', author: 'Rachel M.', role: 'CMO, B2B SaaS' },
      { quote: 'More holiday variants than ever — Q4 design spend was $297 vs $12,000 budgeted for freelancers.', author: 'David K.', role: 'Marketing Director, E-commerce' },
      { quote: 'Regional campaigns look globally on-brand. Consistency score went from 6.2 to 9.1.', author: 'Anika P.', role: 'Global Brand Lead' },
    ],
  },
  'pricing-block': { title: 'Plans for marketing teams of every size', description: 'Team ($49) · Business ($99) · Enterprise ($149).' },
  faq: {
    title: 'AI Design Solution for Marketing Teams FAQ',
    items: [
      { question: 'Can non-designers use Lovart?', answer: 'Yes. Plain-language prompts with Brand Kit guardrails.' },
      { question: 'Impact on design team?', answer: 'Routine production moves to marketers; designers focus on strategy.' },
      { question: 'A/B tests at scale?', answer: 'Generate 10–20 variants from one brief.' },
      { question: 'Multi-user teams?', answer: 'Team, Business, and Enterprise include role-based access.' },
      { question: 'Reactive content speed?', answer: 'Under 10 minutes for trending campaigns.' },
      { question: 'Global brand consistency?', answer: 'Master profile with locked core elements and regional flexibility.' },
    ],
  },
  'cta-default': {
    title: 'Ready to scale your marketing creative output?',
    description: 'Start free — generate your first campaign visual suite in minutes.',
    buttons: [
      { text: 'Start free trial', action: 'openLogin', variant: 'primary' },
      { text: 'See pricing', href: '', variant: 'secondary' },
    ],
  },
}

// --- solution-agency ---
const agencyByType = {
  'hero-mosaic': {
    badge: 'Agency Solution',
    title: 'Deliver for every client',
    highlightedText: 'without context-switch chaos',
    description:
      'Lovart lets agencies manage multi-client brand profiles, slash pitch spec work, and turn production hours into margin — while senior talent stays on strategy.',
    buttons: [
      { text: 'See multi-client workflow', href: '', variant: 'primary' },
      { text: 'View deliverables', href: '', variant: 'secondary' },
    ],
    mosaicTiles: [
      { title: 'Client Brand Kits', subtitle: 'Switch client context in one workspace — colors, type, and logo rules per retainer.', media: { src: IMG.mosaic2, alt: 'Client Brand Kits' } },
      { title: 'Pitch concepts', subtitle: 'Generate spec creative for new business without unpaid weeks of production.', media: { src: IMG.mosaic1, alt: 'Pitch concepts' } },
      { title: 'Production scaling', subtitle: 'Resize, variant, and localize deliverables without rebuilding from scratch.', media: { src: IMG.mosaic3, alt: 'Production scaling' } },
      { title: 'Client-ready exports', subtitle: 'PSD, SVG, PDF, and channel crops — polished enough to ship same day.', media: { src: IMG.mosaic4, alt: 'Client exports' } },
    ],
  },
  'bento-4': {
    title: 'Four agency outcomes with Lovart',
    description: 'What creative and marketing agencies buy when they adopt an AI design solution.',
    columns: 4,
    features: [
      { title: 'Multi-client brands', description: '15+ brand systems without mental recalibration errors.', media: { src: IMG.mosaic2, alt: 'Multi-client' } },
      { title: '3× faster delivery', description: 'Production hours reclaimed for strategy and pitches.', media: { src: IMG.agencyHero, alt: 'Faster delivery' } },
      { title: 'Higher pitch win rate', description: 'Spec work in hours, not unpaid weeks.', media: { src: IMG.mosaic1, alt: 'Pitch win rate' } },
      { title: 'Margin protection', description: 'Same output with fewer billable production hours.', media: { src: IMG.agencyDetail, alt: 'Margin' } },
    ],
  },
  'capability-tabs': {
    title: 'How agencies run client work on Lovart',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      { label: 'Onboard', icon: 'brand', content: { title: 'Per-client Brand Kit setup', description: 'Import guidelines, lock palettes, assign team permissions per retainer.', media: { src: IMG.mosaic2, alt: 'Onboard' }, points: ['Client folders', 'Logo rules', 'Reviewer roles'] } },
      { label: 'Pitch', icon: 'sparkle', content: { title: 'New business spec creative', description: 'Concept boards, mockups, and sample deliverables before the retainer starts.', media: { src: IMG.mosaic1, alt: 'Pitch' }, points: ['Concept exploration', 'Presentation decks', 'Sample social grids'] } },
      { label: 'Produce', icon: 'image', content: { title: 'Retainer production at scale', description: 'Campaign suites, resizing, and localization without designer bottlenecks.', media: { src: IMG.agencyHero, alt: 'Produce' }, points: ['Batch variants', 'Channel crops', 'Touch Edit revisions'] } },
      { label: 'Deliver', icon: 'pointer', content: { title: 'Client approval on ChatCanvas', description: 'Share directions, collect feedback, export final assets in professional formats.', media: { src: IMG.agencyDetail, alt: 'Deliver' }, points: ['Review links', 'Version history', 'Export-ready files'] } },
    ],
  },
  'feature-detail': {
    title: 'Core agency deliverables from one agent',
    description: 'What changes when production and strategy share one workspace.',
    items: [
      {
        title: 'Pitch decks that win without burning margin',
        description: 'Generate concept visuals, mockups, and sample campaigns for new business — in hours instead of unpaid weeks.',
        points: ['Concept boards', 'Sample social grids', 'Presentation-ready exports'],
        media: { src: IMG.mosaic1, alt: 'Pitch decks' },
        cta: { text: 'Build a pitch concept', href: '', variant: 'primary' },
      },
      {
        title: 'Retainer production without the resize treadmill',
        description: 'One approved direction becomes platform variants, localized cuts, and refresh cycles — same client brand context throughout.',
        reverse: true,
        points: ['Multi-channel resizing', 'Offer and seasonal refreshes', 'Brand-locked variants'],
        media: { src: IMG.agencyHero, alt: 'Retainer production' },
        cta: { text: 'Scale a client campaign', href: '', variant: 'primary' },
      },
    ],
  },
  'workflow-horizontal': {
    title: 'Agency workflow in three steps',
    description: 'From client brief to billable deliverable.',
    layout: 'horizontal',
    steps: [
      { step: 1, title: 'Load client brand', description: 'Select Brand Kit, upload brief, attach references and competitor context.' },
      { step: 2, title: 'Generate and refine', description: 'Batch campaign assets; Touch Edit client feedback without restarting.' },
      { step: 3, title: 'Export and invoice', description: 'Ship channel-ready files — production hours become margin.' },
    ],
  },
  'comparison-table': {
    title: 'Lovart vs traditional agency production',
    headers: ['Need', 'Manual studio', 'Freelance bench', 'Lovart Agency Solution'],
    highlightColumn: 3,
    rows: [
      { feature: 'Multi-client brand switching', values: ['Manual guideline lookup', 'Per-vendor rebrief', 'Per-client Brand Kit in one workspace'] },
      { feature: 'Pitch spec investment', values: ['$5k–$25k unpaid per pitch', 'Inconsistent quality', 'Concept suites in hours'] },
      { feature: 'Production throughput', values: ['Linear with headcount', 'Availability risk', '3× output, same seniors on strategy'] },
      { feature: 'Revision cycles', values: ['Full redesign rounds', 'Email chain chaos', 'Touch Edit targeted fixes'] },
      { feature: 'Margin on retainers', values: ['Production eats billable hours', 'Mark-up on pass-through', 'AI absorbs production layer'] },
    ],
  },
  'cluster-block-dense': {
    title: 'Agency scenarios Lovart is built for',
    description: 'Where studios deploy the solution today.',
    cards: [
      { icon: 'brand', title: 'Creative agency retainers', description: 'Social, display, and email variants across 10+ clients.' },
      { icon: 'sparkle', title: 'New business pitches', description: 'Spec creative without sinking margin before the win.' },
      { icon: 'globe', title: 'Marketing agency localization', description: 'Regional campaign adaptations per client brand.' },
      { icon: 'image', title: 'Design shop overflow', description: 'Absorb production spikes without freelance scramble.' },
      { icon: 'pointer', title: 'Brand identity rollouts', description: 'System applications across touchpoints from one guide.' },
      { icon: 'refresh', title: 'Always-on content retainers', description: 'Weekly social and ad refresh without new headcount.' },
    ],
  },
  'canvas-wall': {
    title: 'Client work wall — one studio, many brands',
    description: 'A sample of deliverable types agencies ship from Lovart across retainers and pitches.',
    cta: { text: 'Open agency workspace', href: '', variant: 'secondary' },
    columns: 4,
    items: [
      { media: { src: IMG.agencyHero, alt: 'Social campaign grid' }, author: 'client.retainer', caption: 'Social campaign grid' },
      { media: { src: IMG.mosaic1, alt: 'Pitch concept board' }, author: 'new.business', caption: 'Pitch concept board' },
      { media: { src: IMG.mosaic3, alt: 'Product launch kit' }, author: 'launch.kit', caption: 'Product launch kit' },
      { media: { src: IMG.agencyDetail, alt: 'Email and display set' }, author: 'lifecycle.set', caption: 'Email and display set' },
      { media: { src: IMG.mosaic2, alt: 'Brand refresh applications' }, author: 'brand.refresh', caption: 'Brand refresh applications' },
      { media: { src: IMG.mosaic4, alt: 'Localized ad variants' }, author: 'localize.ads', caption: 'Localized ad variants' },
    ],
  },
  'review-grid-4col': {
    title: 'High-impact agency workflows',
    columns: 4,
    reviews: [
      { title: 'Pitch spec in a day', body: 'We present three concept directions with mockups — pitch cost dropped 60%.', author: 'Studio Ops', role: 'New business' },
      { title: 'Retainer margin up', body: 'Production used to eat senior hours. Now strategists stay on strategy.', author: 'Creative Director', role: 'Brand retainer' },
      { title: 'Client switching solved', body: 'Brand Kits per client ended the wrong-logo-on-wrong-brand nightmare.', author: 'Account Lead', role: 'Multi-client shop' },
      { title: 'Revision rounds shortened', body: 'Touch Edit means we fix the CTA badge, not rebuild the ad.', author: 'Art Director', role: 'Performance clients' },
    ],
  },
  'pricing-block': { title: 'Agency plans — from boutique to networked studios', description: 'Team for small shops · Business for multi-retainer · Enterprise for holding-company governance.' },
  faq: {
    title: 'AI Design Solution for Agencies FAQ',
    items: [
      { question: 'Can we manage multiple client brands?', answer: 'Yes. Separate Brand Kit profiles per client with role-based team access.' },
      { question: 'Does this replace our designers?', answer: 'No. It absorbs production work so seniors focus on strategy, pitches, and creative direction.' },
      { question: 'Pitch spec work?', answer: 'Generate concept boards and sample deliverables in hours — reducing unpaid pitch investment.' },
      { question: 'Client approval workflow?', answer: 'Review on ChatCanvas, iterate with Touch Edit, export professional formats.' },
      { question: 'White-label or client-facing?', answer: 'Export client-ready assets. Enterprise adds custom governance and SSO.' },
      { question: 'Commercial rights for client work?', answer: 'Paid plans include commercial usage for assets you create for clients.' },
    ],
  },
  'cta-default': {
    title: 'Ready to deliver more client work with better margins?',
    description: 'Start free — set up your first client Brand Kit on ChatCanvas.',
    buttons: [
      { text: 'Start agency trial', action: 'openLogin', variant: 'primary' },
      { text: 'See agency workflows', href: '', variant: 'secondary' },
    ],
  },
}

const pages = [
  {
    file: 'ai-design-solution-for-shopify-en.json',
    slug: 'ai-design-solution-for-shopify',
    title: 'AI Design Solution for Shopify',
    description:
      'Turn one product brief into PDP visuals, ad creatives, landing pages, email headers, and video concepts — one agent workflow for Shopify and DTC teams.',
    keywords: ['ai design shopify', 'shopify creative solution', 'dtc design workflow', 'lovart shopify'],
    ogImage: IMG.hero,
    storyline: 'solution-i-ecommerce',
    sectionsByType: shopifyByType,
  },
  {
    file: 'ai-design-solution-for-marketing-teams-en.json',
    slug: 'ai-design-solution-for-marketing-teams',
    title: 'AI Design Solution for Marketing Teams',
    description:
      'Scale marketing creative output without scaling headcount. Produce 5× more on-brand visuals across every channel with distributed production and Brand Kit governance.',
    keywords: ['ai design marketing team', 'marketing creative solution', 'team design scaling', 'lovart marketing'],
    ogImage: IMG.mktHero,
    storyline: 'solution-p-marketing',
    sectionsByType: teamByType,
  },
  {
    file: 'ai-design-solution-for-agencies-en.json',
    slug: 'ai-design-solution-for-agencies',
    title: 'AI Design Solution for Agencies',
    description:
      'Manage multi-client brand profiles, deliver campaigns 3× faster, protect margins, and pitch with AI-generated concept work. Lovart for creative and marketing agencies.',
    keywords: ['ai design for agencies', 'agency design solution', 'multi-client design', 'lovart agency'],
    ogImage: IMG.agencyHero,
    storyline: 'solution-p-agency',
    sectionsByType: agencyByType,
  },
]

const outDir = path.join(__dirname, 'en')
for (const p of pages) {
  const doc = buildPage(p)
  const expected = STORYLINES.storylines[p.storyline].sections
  const actual = doc.section.map((s) => s.type)
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`Section order mismatch for ${p.slug}`)
  }
  const outPath = path.join(outDir, p.file)
  fs.writeFileSync(outPath, JSON.stringify(doc, null, 2) + '\n')
  console.log(`Wrote ${outPath} [${p.storyline}] (${doc.section.length} sections)`)
}
