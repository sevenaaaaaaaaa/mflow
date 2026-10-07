#!/usr/bin/env node
/**
 * Build two Product page reference examples (en).
 *
 * Case A — ChatCanvas: SEO canonical, 产品能力, product-标准
 * Case B — Brand Kit:  SEO + social proof, 产品特色, product-含社会证明
 *
 * See Refresh-Page/PRODUCT-PRODUCTION.md for 官网 vs 投放、能力/特色/功能、与 Scenario/Solution 边界.
 * Run: node _build-examples.js
 */
const fs = require('fs');
const path = require('path');

const IMG = {
  canvas: 'https://assets-persist.lovart.ai/img/d92cfdbbb4c243d8a269dc6d1301540c/5049909fb1610fbc90ed8b25cfecc77ffc14fcee.png',
  brand: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/7eb9d35ed6aaf819fbe425badb3310b77bdc38a7.png',
  touch: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/98dde485f8c6789596006f5ee601a445d6606b78.png',
  text: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/805d2e070d4404ed0cd6ae865930375919374b97.png',
  product: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/55b94439550ff0fefec6a09ca160df2fe8d0f24f.png',
  workflow: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/1f66f7b0726f0b3f59645d6b3a471691818a07f2.png',
  video: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/437351775c82f2d4aa7628eccd1ffa393a8d8010d3b448678901622628cc95cf.png',
  mockup: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/4c90f673629d0bbd5fce85ad374352d4e40deb3e.png',
  palette: 'https://assets-persist.lovart.ai/img/d92cfdbbb4c243d8a269dc6d1301540c/6b1a28475b0c188f4a858aaf0aa852793de580c3.png',
  guidelines: 'https://assets-persist.lovart.ai/img/d92cfdbbb4c243d8a269dc6d1301540c/d0a9be686121d00de898a2d5ce66d9db1b057e97.png',
};

function writePage(filename, meta, sections) {
  const doc = {
    _type: 'compositePage',
    category: 'product',
    slug: meta.slug,
    title: meta.title,
    description: meta.description,
    storyline: meta.storyline,
    bodyJson: JSON.stringify(sections),
    seo: {
      title: meta.seoTitle,
      description: meta.seoDescription,
      keywords: meta.keywords,
      noIndex: true,
      ogImage: {
        _type: 'imageSource',
        url: meta.ogImage,
        alt: meta.title,
        sourceType: 'external',
      },
    },
    language: 'en',
    schemaVersion: 'composite-v2',
    url_path: `/product/${meta.slug}`,
    section: sections,
  };
  fs.writeFileSync(path.join(__dirname, filename), JSON.stringify(doc, null, 2) + '\n');
}

// ── Case 1: product-标准 — ChatCanvas ──────────────────────────────────────

const chatCanvasSections = [
  {
    type: 'hero-cinematic',
    tag: 'Lovart Product',
    title: 'Meet ChatCanvas —',
    highlightedText: 'where every design conversation lives',
    description:
      'ChatCanvas is Lovart\'s infinite spatial workspace. Brief, generate, compare, and refine every asset in one persistent canvas — not scattered across tabs, folders, or export folders.',
    buttons: [
      { text: 'Open ChatCanvas', href: '', variant: 'primary' },
      { text: 'See the workflow', href: '', variant: 'secondary' },
    ],
    media: { src: IMG.canvas, alt: 'Lovart ChatCanvas workspace' },
  },
  {
    type: 'bento-4',
    title: 'Four reasons teams work inside ChatCanvas',
    description: 'The core product behaviors that separate an agent workspace from a single-output generator.',
    columns: 4,
    features: [
      {
        title: 'Infinite spatial memory',
        description: 'Zoom out, pan, and keep every generation visible for side-by-side comparison.',
        media: { src: IMG.canvas, alt: 'Infinite canvas' },
      },
      {
        title: 'Persistent sessions',
        description: 'Close the browser — your canvases, history, and context stay ready.',
        media: { src: IMG.product, alt: 'Persistent workspace' },
      },
      {
        title: 'Multi-canvas projects',
        description: 'Separate boards for exploration, client review, and final export without losing links.',
        media: { src: IMG.workflow, alt: 'Multi-canvas projects' },
      },
      {
        title: 'Agent + canvas edits',
        description: 'Chat to generate; Touch Edit to refine — same surface, no handoffs.',
        media: { src: IMG.touch, alt: 'Agent and canvas edits' },
      },
    ],
  },
  {
    type: 'capability-tabs',
    title: 'What you do inside ChatCanvas',
    description: 'Four modes teams use daily — each tab maps to a real production job.',
    autoplayIntervalMs: 0,
    tabs: [
      {
        label: 'Brief & plan',
        icon: 'search',
        content: {
          title: 'Start from business context',
          description: 'Drop references, brand PDFs, SKU sheets, or competitor URLs. Lovart reasons before pixels move.',
          media: { src: IMG.workflow, alt: 'Brief and plan in ChatCanvas' },
          points: ['Channel specs and offer context', 'Reference boards on canvas', 'Thinking Mode for strategy'],
        },
      },
      {
        label: 'Generate',
        icon: 'sparkle',
        content: {
          title: 'Generate beside the conversation',
          description: 'Images, layouts, mockups, and video keyframes appear on canvas as the agent works — not in a download queue.',
          media: { src: IMG.product, alt: 'Generate on canvas' },
          points: ['Image and layout generation', 'Video keyframes and motion', 'Fast Mode for variant loops'],
        },
      },
      {
        label: 'Compare',
        icon: 'image',
        content: {
          title: 'Compare directions spatially',
          description: 'Arrange hooks, hero options, and campaign territories side by side. Pick winners without re-briefing.',
          media: { src: IMG.canvas, alt: 'Compare on canvas' },
          points: ['Side-by-side variant boards', 'Branch explorations', 'Client-ready review layouts'],
        },
      },
      {
        label: 'Ship',
        icon: 'brand',
        content: {
          title: 'Refine and export from canvas',
          description: 'Touch Edit, Text Edit, and Edit Elements polish the last mile — then export channel-ready files.',
          media: { src: IMG.touch, alt: 'Refine and export' },
          points: ['Touch Edit precision', 'Multi-format export', 'Brand Kit alignment'],
        },
      },
    ],
  },
  {
    type: 'tool-grid',
    title: 'Tools that connect inside ChatCanvas',
    description: 'Every Lovart tool opens into the same workspace — start from the asset you need today.',
    tools: [
      {
        icon: 'sparkle',
        name: 'Image Generator',
        category: 'Visuals',
        description: 'Hero shots, social crops, and campaign graphics from one brief.',
        tags: ['Image', 'Campaign', 'Social'],
        href: '',
        rating: 4.9,
      },
      {
        icon: 'video',
        name: 'Video Generator',
        category: 'Motion',
        description: 'Keyframes, hooks, and vertical cuts without leaving canvas.',
        tags: ['Video', '9:16', 'Ads'],
        href: '',
        rating: 4.8,
      },
      {
        icon: 'brand',
        name: 'Brand Kit',
        category: 'Governance',
        description: 'Logo, color, and type rules travel with every canvas session.',
        tags: ['Brand', 'Consistency'],
        href: '',
        rating: 4.9,
      },
      {
        icon: 'pointer',
        name: 'Touch Edit',
        category: 'Editing',
        description: 'Click any element — regenerate, recolor, or reposition in place.',
        tags: ['Edit', 'Precision'],
        href: '',
        rating: 4.8,
      },
      {
        icon: 'image',
        name: 'Mockup',
        category: 'Product',
        description: 'Place flat art into photorealistic scenes from canvas.',
        tags: ['Mockup', 'PDP'],
        href: '',
        rating: 4.8,
      },
      {
        icon: 'social',
        name: 'Social Post Designer',
        category: 'Channels',
        description: 'Posts, stories, and covers that inherit canvas context.',
        tags: ['Social', 'Stories'],
        href: '',
        rating: 4.7,
      },
    ],
  },
  {
    type: 'workflow-vertical',
    title: 'How ChatCanvas fits your week',
    description: 'A vertical walkthrough for teams adopting the workspace for the first time.',
    layout: 'vertical',
    steps: [
      {
        step: 1,
        title: 'Create a canvas for the job',
        description: 'Name it for the campaign, client, or SKU. Upload references and set Brand Kit once.',
        media: { src: IMG.workflow, alt: 'Create a canvas' },
      },
      {
        step: 2,
        title: 'Brief the agent in chat',
        description: 'Describe outcomes — channel, audience, formats. Generations land on canvas as the agent works.',
        media: { src: IMG.product, alt: 'Brief the agent' },
      },
      {
        step: 3,
        title: 'Compare, refine, export',
        description: 'Arrange winners, Touch Edit details, export every format from one session.',
        media: { src: IMG.touch, alt: 'Refine and export' },
      },
    ],
  },
  {
    type: 'comparison-table',
    title: 'ChatCanvas vs fragmented creative stacks',
    description: 'Why teams move from chat-only generators and folder sprawl to a spatial agent workspace.',
    headers: ['Need', 'Chat-only AI tool', 'Figma + exports folder', 'Lovart ChatCanvas'],
    highlightColumn: 3,
    rows: [
      {
        feature: 'Variant comparison',
        values: ['Scroll chat history', 'Manual boards and duplicates', 'Spatial side-by-side on canvas'],
      },
      {
        feature: 'Session persistence',
        values: ['Often lost between sessions', 'Files scattered by tool', 'Canvases persist with full history'],
      },
      {
        feature: 'Edit after generation',
        values: ['Regenerate whole output', 'Re-import and rework', 'Touch Edit on canvas in place'],
      },
      {
        feature: 'Cross-tool context',
        values: ['One modality per thread', 'Manual handoffs', 'Image, video, mockup in one workspace'],
      },
      {
        feature: 'Client review',
        values: ['Screenshot exports', 'Shared Figma links + exports', 'Review layouts on canvas'],
      },
    ],
  },
  {
    type: 'cluster-block-dense',
    title: 'Teams that live in ChatCanvas',
    description: 'Common production loops the workspace is built for.',
    cards: [
      { icon: 'sparkle', title: 'Campaign exploration', desc: 'Hook boards, hero options, and ad territories in one session.' },
      { icon: 'brand', title: 'Brand system rollout', desc: 'Apply Brand Kit while exploring new visual directions.' },
      { icon: 'video', title: 'Video storyboards', desc: 'Keyframes, thumbnails, and cut variants beside the brief.' },
      { icon: 'image', title: 'Product launch walls', desc: 'PDP, ads, email, and social from one SKU context.' },
      { icon: 'pointer', title: 'Agency client boards', desc: 'Separate canvases per client with shared agent skills.' },
      { icon: 'refresh', title: 'Weekly test loops', desc: 'Fast Mode variants without losing last week\'s winners.' },
    ],
  },
  {
    type: 'showcase-stacked',
    title: 'See ChatCanvas in action',
    items: [
      {
        media: { src: IMG.canvas, alt: 'Spatial variant board' },
        title: 'Variant boards — Compare hooks without re-briefing',
        description: 'Arrange twelve ad directions on one canvas. Stakeholders pick winners in a single review.',
        cta: { text: 'Try variant boards', href: '' },
      },
      {
        media: { src: IMG.touch, alt: 'Touch Edit on canvas' },
        title: 'Touch Edit — Fix one element, keep the composition',
        description: 'Select a label, shadow, or product detail. Regenerate just that layer while the rest stays locked.',
        cta: { text: 'See Touch Edit', href: '' },
      },
      {
        media: { src: IMG.video, alt: 'Video keyframes on canvas' },
        title: 'Motion on canvas — Keyframes beside stills',
        description: 'Storyboard vertical hooks next to hero stills. Motion and static share one campaign context.',
        cta: { text: 'Explore video on canvas', href: '' },
      },
    ],
  },
  {
    type: 'testimonial',
    title: 'What teams say about working in ChatCanvas',
    testimonials: [
      {
        quote: 'We stopped exporting to Slack threads. Everything — brief, variants, approvals — lives on one canvas now.',
        author: 'Maya Lin',
        role: 'Creative Director, DTC brand',
      },
      {
        quote: 'The spatial layout changed how we run creative reviews. Clients pick from a board, not a zip file.',
        author: 'Jordan Ellis',
        role: 'Agency founder',
      },
      {
        quote: 'Persistent canvases mean Monday picks up where Friday left off. That alone saved us hours.',
        author: 'Priya Shah',
        role: 'Growth lead',
      },
    ],
  },
  {
    type: 'pricing-block',
    title: 'Plans for solo creators and teams',
    description: 'Start free on ChatCanvas. Upgrade when you need more credits, premium models, and team seats.',
  },
  {
    type: 'faq',
    title: 'ChatCanvas FAQ',
    items: [
      {
        question: 'What is ChatCanvas?',
        answer: 'ChatCanvas is Lovart\'s infinite spatial workspace where you brief an AI design agent, generate assets, compare variants, and refine output — all in one persistent canvas.',
      },
      {
        question: 'How is ChatCanvas different from Lovart chat?',
        answer: 'Chat is the conversation layer. ChatCanvas is where generations land spatially — arranged, compared, edited, and exported as a production surface.',
      },
      {
        question: 'Do my canvases persist?',
        answer: 'Yes. Canvases, generation history, and context persist across sessions. You can maintain multiple canvases per project or client.',
      },
      {
        question: 'Can I use Touch Edit on canvas?',
        answer: 'Yes. Touch Edit, Text Edit, and Edit Elements work directly on canvas elements — no re-export to another tool.',
      },
      {
        question: 'Does Brand Kit apply inside ChatCanvas?',
        answer: 'Yes. Active Brand Kit rules apply to new generations and edits within any canvas session.',
      },
      {
        question: 'Can teams share canvases?',
        answer: 'Team plans support shared workspaces so stakeholders can review variant boards and approved directions together.',
      },
    ],
  },
  {
    type: 'cta-default',
    title: 'Ready to work in one canvas?',
    description: 'Start free — create your first ChatCanvas and brief the agent in minutes.',
    buttons: [
      { text: 'Open ChatCanvas', href: '', variant: 'primary', action: 'openLogin' },
      { text: 'See product lineup', href: '', variant: 'secondary' },
    ],
  },
];

writePage('chatcanvas-en.json', {
  slug: 'chatcanvas',
  title: 'ChatCanvas',
  description:
    'Lovart ChatCanvas is the infinite spatial workspace where teams brief an AI design agent, compare variants, and ship channel-ready assets in one persistent session.',
  storyline: 'product-标准',
  seoTitle: 'ChatCanvas | Lovart AI Design Workspace',
  seoDescription:
    'Brief, generate, compare, and refine every creative asset in Lovart ChatCanvas — the infinite agent workspace for design teams.',
  keywords: ['chatcanvas', 'lovart workspace', 'ai design canvas', 'agent workspace', 'creative collaboration'],
  ogImage: IMG.canvas,
}, chatCanvasSections);

// ── Case 2: product-含社会证明 — Brand Kit ───────────────────────────────────

const brandKitBase = [
  {
    type: 'hero-cinematic',
    tag: 'Lovart Product',
    title: 'Brand Kit keeps',
    highlightedText: 'every output on-brand automatically',
    description:
      'Upload logo, colors, typography, and visual rules once. Brand Kit applies them across ChatCanvas sessions, generators, and exports — so teams stop policing every pixel manually.',
    buttons: [
      { text: 'Set up Brand Kit', href: '', variant: 'primary' },
      { text: 'See examples', href: '', variant: 'secondary' },
    ],
    media: { src: IMG.palette, alt: 'Lovart Brand Kit' },
  },
  {
    type: 'bento-4',
    title: 'Four Brand Kit capabilities teams rely on',
    description: 'Governance without slowing production — the product behaviors that scale brand consistency.',
    columns: 4,
    features: [
      {
        title: 'One-time setup',
        description: 'Logo, palette, fonts, and guidelines in about three minutes.',
        media: { src: IMG.palette, alt: 'Brand Kit setup' },
      },
      {
        title: 'Auto-apply rules',
        description: 'Every new generation inherits active brand elements.',
        media: { src: IMG.brand, alt: 'Auto-apply brand rules' },
      },
      {
        title: 'Multiple kits',
        description: 'Agencies switch client brands with one click.',
        media: { src: IMG.guidelines, alt: 'Multiple brand kits' },
      },
      {
        title: 'Style Consistency',
        description: 'Visual guardrails across image, layout, and motion.',
        media: { src: IMG.product, alt: 'Style consistency' },
      },
    ],
  },
  {
    type: 'capability-tabs',
    title: 'How Brand Kit works across Lovart',
    description: 'Four layers of brand governance — from setup to export.',
    autoplayIntervalMs: 0,
    tabs: [
      {
        label: 'Define',
        icon: 'brand',
        content: {
          title: 'Upload once, reuse everywhere',
          description: 'Add logo files, primary and accent colors, headline and body fonts, and optional brand PDFs.',
          media: { src: IMG.palette, alt: 'Define brand kit' },
          points: ['Logo and color extraction', 'Typography pairing', 'Guideline PDF import'],
        },
      },
      {
        label: 'Apply',
        icon: 'sparkle',
        content: {
          title: 'Automatic on every generation',
          description: 'Image Generator, layouts, mockups, and video keyframes inherit Brand Kit without repeated prompts.',
          media: { src: IMG.brand, alt: 'Apply brand kit' },
          points: ['No manual color picking', 'Consistent type treatment', 'Logo placement rules'],
        },
      },
      {
        label: 'Guard',
        icon: 'pointer',
        content: {
          title: 'Style Consistency guardrails',
          description: 'Off-brand colors and treatments get corrected before export — especially across large variant batches.',
          media: { src: IMG.guidelines, alt: 'Brand guardrails' },
          points: ['Contrast and accessibility checks', 'Cross-channel consistency', 'Variant batch QA'],
        },
      },
      {
        label: 'Scale',
        icon: 'refresh',
        content: {
          title: 'Multiple kits for agencies and portfolios',
          description: 'Maintain dozens of client or sub-brand kits. Switch active kit per canvas or project.',
          media: { src: IMG.mockup, alt: 'Scale brand kits' },
          points: ['Per-client kits', 'Sub-brand variants', 'Team-wide defaults'],
        },
      },
    ],
  },
  {
    type: 'tool-grid',
    title: 'Where Brand Kit connects in the stack',
    description: 'Brand Kit is not a standalone export — it powers every Lovart surface below.',
    tools: [
      {
        icon: 'sparkle',
        name: 'ChatCanvas',
        category: 'Workspace',
        description: 'Active kit travels with every canvas session and edit.',
        tags: ['Canvas', 'Session'],
        href: '',
        rating: 4.9,
      },
      {
        icon: 'image',
        name: 'Image Generator',
        category: 'Visuals',
        description: 'Campaign and PDP imagery with locked palette and type.',
        tags: ['Image', 'Campaign'],
        href: '',
        rating: 4.9,
      },
      {
        icon: 'video',
        name: 'Video Generator',
        category: 'Motion',
        description: 'Lower-thirds, end cards, and motion with brand colors.',
        tags: ['Video', 'Motion'],
        href: '',
        rating: 4.8,
      },
      {
        icon: 'social',
        name: 'Social Post Designer',
        category: 'Channels',
        description: 'Posts and stories that match PDP and ad creative.',
        tags: ['Social', 'Stories'],
        href: '',
        rating: 4.8,
      },
      {
        icon: 'pointer',
        name: 'Text Edit',
        category: 'Editing',
        description: 'Swap copy while preserving brand typography on canvas.',
        tags: ['Copy', 'Typography'],
        href: '',
        rating: 4.7,
      },
      {
        icon: 'brand',
        name: 'Style Consistency',
        category: 'Governance',
        description: 'Batch QA for hooks, markets, and seasonal variants.',
        tags: ['QA', 'Variants'],
        href: '',
        rating: 4.8,
      },
    ],
  },
  {
    type: 'workflow-vertical',
    title: 'Set up Brand Kit in three steps',
    description: 'Most teams are production-ready in one short session.',
    layout: 'vertical',
    steps: [
      {
        step: 1,
        title: 'Upload brand assets',
        description: 'Logo, colors, fonts, and optional guidelines PDF. Lovart can extract palette from references.',
        media: { src: IMG.palette, alt: 'Upload brand assets' },
      },
      {
        step: 2,
        title: 'Activate on canvas',
        description: 'Select the kit for your project. New generations and edits inherit rules automatically.',
        media: { src: IMG.brand, alt: 'Activate brand kit' },
      },
      {
        step: 3,
        title: 'Ship consistent exports',
        description: 'PDP, ads, email, and social exports share one visual system — no manual QA pass.',
        media: { src: IMG.mockup, alt: 'Consistent exports' },
      },
    ],
  },
  {
    type: 'comparison-table',
    title: 'Brand Kit vs manual brand enforcement',
    headers: ['Need', 'Prompt repetition', 'Design-system docs + QA', 'Lovart Brand Kit'],
    highlightColumn: 3,
    rows: [
      {
        feature: 'Setup time',
        values: ['None — but inconsistent', 'Days of documentation', 'Minutes — upload and go'],
      },
      {
        feature: 'Per-asset enforcement',
        values: ['Luck and reviewer eye', 'Manual checklist', 'Automatic on generation'],
      },
      {
        feature: 'Multi-client agencies',
        values: ['Error-prone switching', 'Separate Figma libraries', 'One-click kit switch'],
      },
      {
        feature: 'Variant batches',
        values: ['Drift across prompts', 'Slow QA queue', 'Style Consistency guardrails'],
      },
      {
        feature: 'Cross-channel alignment',
        values: ['Ads ≠ PDP ≠ email', 'Multiple handoffs', 'One kit across all surfaces'],
      },
    ],
  },
  {
    type: 'cluster-block-dense',
    title: 'Brand problems Brand Kit solves',
    cards: [
      { icon: 'brand', title: 'Off-color exports', desc: 'Stop #1a73e8 vs #1a73e9 debates — palette is locked.' },
      { icon: 'refresh', title: 'Seasonal drift', desc: 'Holiday variants stay on-brand without new guideline docs.' },
      { icon: 'globe', title: 'Localization', desc: 'Swap copy and markets; visual system stays intact.' },
      { icon: 'sparkle', title: 'AI variant sprawl', desc: 'Fast Mode hooks inherit rules — drift gets caught early.' },
      { icon: 'image', title: 'Agency portfolios', desc: 'Dozens of client kits without cross-contamination.' },
      { icon: 'pointer', title: 'Last-mile edits', desc: 'Text Edit preserves typography while offers change daily.' },
    ],
  },
  {
    type: 'showcase-stacked',
    title: 'Brand Kit across real deliverables',
    items: [
      {
        media: { src: IMG.mockup, alt: 'On-brand product scenes' },
        title: 'Product visuals — Same palette on PDP and ads',
        description: 'Hero shots, lifestyle scenes, and paid social crops share one color and type system.',
        cta: { text: 'See product visuals', href: '' },
      },
      {
        media: { src: IMG.text, alt: 'Text Edit with brand typography' },
        title: 'Text Edit — Offers change, typography stays',
        description: 'Swap sale copy inside finished creative without breaking font rules.',
        cta: { text: 'Try Text Edit', href: '' },
      },
      {
        media: { src: IMG.video, alt: 'On-brand video end cards' },
        title: 'Motion — End cards and lower-thirds on-brand',
        description: 'Video hooks and end slates inherit logo and color rules automatically.',
        cta: { text: 'Explore video + Brand Kit', href: '' },
      },
    ],
  },
  {
    type: 'logo-loop',
    text: 'Lovart Brand Kit is trusted by agencies, DTC brands, and in-house creative teams worldwide.',
  },
  {
    type: 'testimonial',
    title: 'Teams scaling brand without slowing down',
    testimonials: [
      {
        quote: 'Brand Kit made our paid social, PDP, and email creative finally look like one system instead of three teams.',
        author: 'Priya Shah',
        role: 'Creative Director, Home goods ecommerce',
      },
      {
        quote: 'We manage twelve client kits. Switching is one click — we stopped shipping off-brand variants.',
        author: 'Ethan Reed',
        role: 'Agency operator',
      },
      {
        quote: 'Style Consistency caught drift in a Fast Mode batch before it hit Meta. That paid for itself.',
        author: 'Lena Brooks',
        role: 'Founder, Glow Pantry',
      },
    ],
  },
  {
    type: 'pricing-block',
    title: 'Brand Kit on every plan — more governance on teams',
    description: 'Core Brand Kit is included from free tier. Team plans add shared kits, seats, and batch QA workflows.',
  },
  {
    type: 'faq',
    title: 'Brand Kit FAQ',
    items: [
      {
        question: 'What goes into a Brand Kit?',
        answer: 'Logo files, primary and accent colors, headline and body fonts, and optional brand guideline PDFs. Lovart can extract colors from reference images.',
      },
      {
        question: 'Does Brand Kit work with ChatCanvas?',
        answer: 'Yes. Activate a kit per canvas or project. Generations and Touch Edit sessions inherit the active kit automatically.',
      },
      {
        question: 'Can agencies manage multiple client brands?',
        answer: 'Yes. Create separate kits per client or sub-brand and switch the active kit with one click.',
      },
      {
        question: 'What is Style Consistency?',
        answer: 'Style Consistency is Lovart\'s guardrail layer that checks variant batches for off-brand colors, treatments, and typography before export.',
      },
      {
        question: 'Does Brand Kit support accessibility?',
        answer: 'Brand Kit can flag contrast issues against common accessibility thresholds when palette combinations are applied.',
      },
      {
        question: 'Is Brand Kit included on free plans?',
        answer: 'Yes. Core Brand Kit setup and auto-apply are available on free tier. Team governance features expand on paid plans.',
      },
    ],
  },
  {
    type: 'cta-default',
    title: 'Ready to stop policing every export?',
    description: 'Set up Brand Kit once — every Lovart surface stays on-brand from the first generation.',
    buttons: [
      { text: 'Set up Brand Kit', href: '', variant: 'primary', action: 'openLogin' },
      { text: 'Compare plans', href: '', variant: 'secondary' },
    ],
  },
];

writePage('brand-kit-en.json', {
  slug: 'brand-kit',
  title: 'Brand Kit',
  description:
    'Lovart Brand Kit uploads logo, colors, typography, and visual rules once — then applies them across ChatCanvas, generators, and exports automatically.',
  storyline: 'product-含社会证明',
  seoTitle: 'Brand Kit | Lovart Brand Governance',
  seoDescription:
    'Upload brand assets once. Lovart Brand Kit keeps every generation, edit, and export on-brand across ChatCanvas and all generators.',
  keywords: ['brand kit', 'lovart brand', 'style consistency', 'brand governance', 'ai brand design'],
  ogImage: IMG.palette,
}, brandKitBase);

console.log('Wrote chatcanvas-en.json (product-标准, 12 sections)');
console.log('Wrote brand-kit-en.json (product-含社会证明, 13 sections)');
