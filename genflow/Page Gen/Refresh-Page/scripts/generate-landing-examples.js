#!/usr/bin/env node
/**
 * Generate Landing Page reference JSON (7 storylines).
 * Run from repo: node "1-3 Content Gen/Page Gen/Refresh-Page/scripts/generate-landing-examples.js"
 */

const fs = require('fs');
const path = require('path');
const {
  buildCtaSection,
  buildPromptLauncherBlock,
  mergeFaqItems,
  strengthenHeroDescription,
  validateLandingCopyPreflight,
} = require('./lib/landing-copy-rules');

const REFRESH = path.resolve(__dirname, '..');
const JSON_SSOT = path.join(REFRESH, 'landing-storylines.json');
const OUT_DIR = path.join(REFRESH, 'landing-examples/en');

const IMG = {
  hero: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/55b94439550ff0fefec6a09ca160df2fe8d0f24f.png',
  research: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/1f66f7b0726f0b3f59645d6b3a471691818a07f2.png',
  product: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/4c90f673629d0bbd5fce85ad374352d4e40deb3e.png',
  ads: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/5d48ca781dea8ab12d0c93fc32e3ad8afa815631.png',
  edit: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/eb6f103da589f07f425f2c736237e33f4d1719fa.png',
  video: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/8efdfd8318084a8c88bb72c706bb33c7f2564b8b.png',
  brand: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/7eb9d35ed6aaf819fbe425badb3310b77bdc38a7.png',
  funnel: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/b8e9479301c56b3946bbce10cadc78b70e0d6365.png',
  variant: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/1f4373d295181af9b6be11fc731ea026cb883957.png',
  mockup: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/d11411bc15e95312819272bf39a65a3cbdf230b2.png',
  og: 'https://assets-persist.lovart.ai/img/079352d520c34315b54e3e3eb87c2674/36a638ec-768a-43d6-adc6-3f5e34f77ac9.png',
};

const CASES = [
  {
    theme: 'shopify-growth',
    storyline: 'landing-gallery-detail',
    slugBase: 'draft-lovart-shopify-growth',
    title: 'Lovart for Shopify Growth — Landing (gallery-detail) | Lovart',
    description: 'Paid media reference: multi-tool gallery hero + feature-detail deep dive for ecommerce campaigns.',
    keywords: ['lovart shopify', 'ai ecommerce creative', 'shopify landing page'],
    persona: 'shopify',
  },
  {
    theme: 'creative-studio',
    storyline: 'landing-gallery-funnel',
    slugBase: 'draft-lovart-creative-studio',
    title: 'Lovart Creative Studio — Landing (gallery-funnel) | Lovart',
    description: 'Paid media reference: gallery hero + horizontal showcase funnel for agency retargeting.',
    keywords: ['lovart creative studio', 'agency landing page', 'full funnel creative'],
    persona: 'agency',
  },
  {
    theme: 'brand-campaign',
    storyline: 'landing-brand-trust',
    slugBase: 'draft-lovart-brand-campaign',
    title: 'Lovart Brand Campaign — Landing (brand-trust) | Lovart',
    description: 'Upper-funnel reference: cinematic hero, logo loop and testimonials for brand awareness ads.',
    keywords: ['lovart brand', 'ai design partner', 'brand awareness landing'],
    persona: 'brand',
  },
  {
    theme: 'tool-trial',
    storyline: 'landing-trial-now',
    slugBase: 'draft-lovart-tool-trial',
    title: 'Try Lovart AI Design Agent — Landing (trial-now) | Lovart',
    description: 'Search/trial reference: split hero + prompt launcher for tool-keyword conversion.',
    keywords: ['try lovart', 'ai design agent free', 'lovart trial'],
    persona: 'trial',
  },
  {
    theme: 'competitor-alt',
    storyline: 'landing-vs-competitor',
    slugBase: 'draft-lovart-competitor-alt',
    title: 'Lovart vs Template Tools — Landing (vs-competitor) | Lovart',
    description: 'Conquest reference: before/after comparison for competitor and alternative keywords.',
    keywords: ['lovart alternative', 'lovart vs', 'ai design agent comparison'],
    persona: 'vs',
  },
  {
    theme: 'promo-retarget',
    storyline: 'landing-offer-close',
    slugBase: 'draft-lovart-promo-retarget',
    title: 'Lovart Pro Offer — Landing (offer-close) | Lovart',
    description: 'Bottom-funnel reference: journey hero, pricing and review grid for retargeting promos.',
    keywords: ['lovart pricing', 'lovart pro offer', 'lovart retargeting'],
    persona: 'offer',
  },
  {
    theme: 'platform-demo',
    storyline: 'landing-full',
    slugBase: 'draft-lovart-platform',
    title: 'Lovart Platform — Landing (full demo, 15 sections) | Lovart',
    description: 'Internal QA only: widest module coverage including trial, logo, testimonial and pricing.',
    keywords: ['lovart platform', 'lovart demo', 'composite page demo'],
    persona: 'full',
  },
];

function loadSequences() {
  const raw = JSON.parse(fs.readFileSync(JSON_SSOT, 'utf8'));
  const map = {};
  for (const [id, meta] of Object.entries(raw.storylines)) map[id] = meta.sections;
  return map;
}

function sectionBuilders(ctx) {
  const p = ctx.persona;
  const storyline = ctx.storyline;
  const m = IMG;
  return {
    'hero-gallery': () => ({
      type: 'hero-gallery',
      badge: p === 'shopify' ? 'Shopify growth' : 'Creative studio',
      title: p === 'shopify' ? 'One agent for your' : 'Start anywhere,',
      highlightedText: p === 'shopify' ? 'full Shopify creative funnel' : 'keep one agent context',
      description: strengthenHeroDescription(
        p === 'shopify'
          ? 'PDP visuals, paid social, email and retargeting from one brief — without resetting brand context.'
          : 'Image, video, decks and campaigns stay connected after the first asset is generated.',
        {
          output: 'Generate ads, PDP visuals, email assets and video cuts from the same campaign brief.',
        },
      ),
      buttons: [
        { text: 'Start free', href: '', variant: 'primary' },
        { text: 'See examples', href: '', variant: 'secondary' },
      ],
      toolTiles: [
        { label: 'Product Images', sublabel: 'PDP + catalog', media: { src: m.product, alt: 'Product' } },
        { label: 'Video Ads', sublabel: 'TikTok + Reels', media: { src: m.video, alt: 'Video' } },
        { label: 'Ad Creative', sublabel: 'Meta + Google', media: { src: m.ads, alt: 'Ads' } },
        { label: 'Brand Kit', sublabel: 'Logo + type', media: { src: m.brand, alt: 'Brand Kit' } },
        { label: 'Social Posts', sublabel: 'Stories + feed', media: { src: m.variant, alt: 'Social' } },
        { label: 'Email Headers', sublabel: 'Campaign flows', media: { src: m.mockup, alt: 'Email' } },
      ],
    }),
    'hero-cinematic': () => ({
      type: 'hero-cinematic',
      badge: 'AI Design Partner',
      title: 'Creative that feels',
      highlightedText: 'agency-grade from day one',
      description: strengthenHeroDescription(
        'Lovart researches, generates and refines brand-ready assets — built for teams running always-on paid campaigns.',
        {
          input: 'Start from a campaign brief, references, product URLs or brand rules.',
          output: 'Generate brand-ready assets, campaign visuals and motion cuts.',
        },
      ),
      buttons: [
        { text: 'Start creating', href: '', variant: 'primary' },
        { text: 'Watch overview', href: '', variant: 'secondary' },
      ],
      media: { src: m.hero, alt: 'Lovart cinematic hero' },
    }),
    'hero-split': () => ({
      type: 'hero-split',
      badge: p === 'vs' ? 'Switch to Lovart' : 'AI Design Agent',
      title: p === 'vs' ? 'Stop rebuilding context' : 'Try autonomous',
      highlightedText: p === 'vs' ? 'in every creative tool' : 'creative workflow',
      description: strengthenHeroDescription(
        p === 'vs'
          ? 'Lovart keeps brief, brand and edits on one ChatCanvas — unlike template tools that reset every export.'
          : 'Describe your project once. Lovart researches, designs and delivers coordinated assets in minutes.',
        {
          output: 'Generate coordinated assets you can refine and export without switching apps.',
        },
      ),
      buttons: [
        { text: p === 'vs' ? 'Compare workflows' : 'Start free trial', href: '', variant: 'primary' },
        { text: 'See how it works', href: '', variant: 'secondary' },
      ],
      media: { src: m.hero, alt: 'Hero' },
    }),
    'hero-journey': () => ({
      type: 'hero-journey',
      badge: 'Limited-time offer',
      title: 'Ship more campaigns',
      highlightedText: 'without adding headcount',
      description: strengthenHeroDescription(
        'Upgrade to Lovart Pro for commercial exports, Brand Kit and unlimited agent projects.',
        {
          input: 'Start from the briefs and assets your team already uses.',
          output: 'Generate deliverables your team can launch, localize and reuse across channels.',
          risk: 'Start free, then upgrade when campaign delivery needs more scale.',
        },
      ),
      buttons: [{ text: 'Claim offer', href: '', variant: 'primary' }],
      media: { src: m.brand, alt: 'Offer hero' },
      steps: [
        { label: 'Brief', description: 'Upload brand + campaign context' },
        { label: 'Generate', description: 'Agent delivers coordinated assets' },
        { label: 'Scale', description: 'Extend winners across channels' },
      ],
    }),
    'bento-6': () => ({
      type: 'bento-6',
      title: 'Six capabilities paid teams rely on',
      description: 'One agent context from research through variant loops.',
      columns: 3,
      features: [
        { title: 'Research', description: 'Web Search + uploads before pixels.', media: { src: m.funnel, alt: 'Research' } },
        { title: 'Generate', description: 'Image and video from one brief.', media: { src: m.product, alt: 'Generate' } },
        { title: 'Edit', description: 'Touch Edit and Text Edit in place.', media: { src: m.edit, alt: 'Edit' } },
        { title: 'Brand Kit', description: 'Consistent rules across channels.', media: { src: m.brand, alt: 'Brand Kit' } },
        { title: 'Variants', description: 'Fast Mode for creative testing.', media: { src: m.variant, alt: 'Variants' } },
        { title: 'Extend', description: 'Scale winners across the funnel.', media: { src: m.ads, alt: 'Extend' } },
      ],
    }),
    'bento-4': () => ({
      type: 'bento-4',
      title: 'Four controls every performance team needs',
      description: 'Brand, edit, mockup and variant loops.',
      columns: 4,
      features: [
        { title: 'Brand Kit', description: 'Lock visual rules.', media: { src: m.brand, alt: 'Brand Kit' } },
        { title: 'Touch Edit', description: 'Surgical changes.', media: { src: m.edit, alt: 'Touch Edit' } },
        { title: 'Text Edit', description: 'Offer copy in place.', media: { src: m.ads, alt: 'Text Edit' } },
        { title: 'Mockup', description: 'Realistic scenes.', media: { src: m.mockup, alt: 'Mockup' } },
      ],
    }),
    'bento-2': () => ({
      type: 'bento-2',
      title: 'Two modes to start fast',
      description: 'Autonomous agent or guided collaboration.',
      columns: 2,
      features: [
        { title: 'Autonomous mode', description: 'Brief to delivery end-to-end.', media: { src: m.hero, alt: 'Autonomous' } },
        { title: 'Guided mode', description: 'You steer; agent executes.', media: { src: m.research, alt: 'Guided' } },
      ],
    }),
    'capability-tabs': () => ({
      type: 'capability-tabs',
      title: 'Four workflows on one canvas',
      description: '',
      tabs: [
        {
          label: 'Research',
          icon: 'search',
          content: {
            title: 'Context before generation',
            description: 'Competitor URLs, brand PDFs and product specs inform every asset.',
            media: { src: m.research, alt: 'Research' },
            points: ['Web Search', 'File upload', 'Market context'],
            cta: { text: 'Build brief', href: '' },
          },
        },
        {
          label: 'Generate',
          icon: 'sparkle',
          content: {
            title: 'Multi-model output',
            description: 'Image, video and copy from one session.',
            media: { src: m.product, alt: 'Generate' },
            points: ['Multiple ratios', 'Mockups', 'Ad variants'],
            cta: { text: 'Generate', href: '' },
          },
        },
        {
          label: 'Edit',
          icon: 'pointer',
          content: {
            title: 'Fix what is wrong',
            description: 'Touch Edit and Text Edit preserve layout.',
            media: { src: m.edit, alt: 'Edit' },
            points: ['Point-and-edit', 'Copy in place', 'Layers'],
            cta: { text: 'Refine', href: '' },
          },
        },
        {
          label: 'Extend',
          icon: 'brand',
          content: {
            title: 'Scale the winner',
            description: 'Same direction across PDP, ads, email and social.',
            media: { src: m.brand, alt: 'Extend' },
            points: ['Brand Kit', 'Fast Mode', 'Localization'],
            cta: { text: 'Scale', href: '' },
          },
        },
      ],
    }),
    'tool-grid': () => ({
      type: 'tool-grid',
      title: 'Entry points into the same agent',
      description: 'Start from the asset you need today.',
      tools: [
        { icon: 'image', name: 'AI Product Image Generator', category: 'Catalog', description: 'PDP and lifestyle visuals.', tags: ['PDP'], href: '', rating: 4.9 },
        { icon: 'video', name: 'AI Video Generator', category: 'Paid social', description: 'Hooks and vertical frames.', tags: ['Video'], href: '', rating: 4.8 },
        { icon: 'sparkle', name: 'AI Design Agent', category: 'Workflow', description: 'End-to-end projects.', tags: ['Agent'], href: '', rating: 4.9 },
        { icon: 'brand', name: 'Brand Kit', category: 'Governance', description: 'Rules across assets.', tags: ['Brand'], href: '', rating: 4.8 },
        { icon: 'remove-bg', name: 'Remove BG + Mockup', category: 'Production', description: 'Isolated product scenes.', tags: ['Mockup'], href: '', rating: 4.8 },
        { icon: 'social', name: 'Social Post Designer', category: 'Retention', description: 'On-brand posts and stories.', tags: ['Social'], href: '', rating: 4.7 },
      ],
    }),
    'logo-loop': () => ({
      type: 'logo-loop',
      text: 'Trusted by millions of creators, agencies and brands worldwide.',
    }),
    'testimonial': () => ({
      type: 'testimonial',
      title: 'Teams running always-on campaigns on Lovart',
      testimonials: [
        { quote: 'We cut creative production time by 70% without sacrificing brand consistency.', author: 'Sarah M.', role: 'Growth lead' },
        { quote: 'Brand Kit kept every Meta variant on-model through a full launch week.', author: 'Carlos R.', role: 'Ecommerce director' },
        { quote: 'Our agency ships client variants in hours, not revision rounds.', author: 'Jennifer P.', role: 'Creative director' },
      ],
    }),
    'prompt-launcher': () => ({
      type: 'prompt-launcher',
      ...buildPromptLauncherBlock('campaign asset', [
        { label: 'PDP refresh', prompt: 'Create a PDP image system for a premium skincare SKU: hero, lifestyle, comparison and 4:5 ad crop.' },
        { label: 'Meta ad variants', prompt: 'Generate 8 Meta ad concepts for a DTC coffee brand with bundle offer and 1:1 crops.' },
        { label: 'Brand launch', prompt: 'Build a launch kit: logo directions, social headers, email hero and story frames.' },
      ]),
      prompts: [
        { label: 'PDP refresh', prompt: 'Create a PDP image system for a premium skincare SKU: hero, lifestyle, comparison and 4:5 ad crop.' },
        { label: 'Meta ad variants', prompt: 'Generate 8 Meta ad concepts for a DTC coffee brand with bundle offer and 1:1 crops.' },
        { label: 'Brand launch', prompt: 'Build a launch kit: logo directions, social headers, email hero and story frames.' },
      ],
    }),
    'canvas-wall': () => ({
      type: 'canvas-wall',
      title: 'One workspace, every surface',
      description: 'PDP, ads, email, social and video from the same brief.',
      cta: { text: 'Open gallery', href: '', variant: 'secondary' },
      columns: 4,
      items: [
        { media: { src: m.product, alt: 'PDP' }, author: 'pdp', likes: 248, caption: 'PDP hero' },
        { media: { src: m.ads, alt: 'Ad' }, author: 'ads', likes: 412, caption: 'Paid social' },
        { media: { src: m.brand, alt: 'Email' }, author: 'email', likes: 189, caption: 'Email header' },
        { media: { src: m.video, alt: 'Video' }, author: 'video', likes: 326, caption: 'Video hook' },
      ],
    }),
    'workflow-horizontal': () => ({
      type: 'workflow-horizontal',
      title: 'Three steps to shippable creative',
      description: 'From brief to export.',
      layout: 'horizontal',
      steps: [
        { step: 1, title: 'Brief', description: 'Share goals, audience and references.' },
        { step: 2, title: 'Generate', description: 'Explore directions; refine with edits.' },
        { step: 3, title: 'Export', description: 'Scale winners across channels.' },
      ],
    }),
    'workflow-vertical': () => ({
      type: 'workflow-vertical',
      title: 'How teams close campaigns on Lovart',
      layout: 'vertical',
      steps: [
        { step: 1, title: 'Align offer', description: 'Lock promo, audience and brand rules.' },
        { step: 2, title: 'Produce variants', description: 'Spin channel-ready assets fast.' },
        { step: 3, title: 'Launch + retarget', description: 'Extend winners with Brand Kit.' },
      ],
    }),
    'comparison-table': () => ({
      type: 'comparison-table',
      title: 'Lovart vs fragmented creative stacks',
      description: 'Why paid teams consolidate on one agent.',
      headers: ['Need', 'Templates / DIY', 'Agency', 'Lovart AI Design Agent'],
      highlightColumn: 3,
      rows: [
        { feature: 'Brand memory', values: ['Manual', 'PDF guide', 'Brand Kit + context'] },
        { feature: 'Time to first asset', values: ['Minutes', 'Weeks', 'Minutes'] },
        { feature: 'Post-gen edits', values: ['Limited', 'Rounds', 'Touch / Text / Elements'] },
        { feature: 'Cross-channel', values: ['Manual', 'Siloed teams', 'One canvas'] },
      ],
    }),
    'comparison-before-after': () => ({
      type: 'comparison-before-after',
      title: 'Before and after switching to Lovart',
      description: 'What performance teams fix first.',
      before: {
        label: 'Before',
        title: 'Context resets every export',
        description: 'Brief lives in Slack; assets drift channel by channel.',
        media: { src: m.mockup, alt: 'Before' },
      },
      after: {
        label: 'After',
        title: 'One agent, one brand system',
        description: 'Edits, variants and exports stay on ChatCanvas.',
        media: { src: m.brand, alt: 'After' },
      },
    }),
    'cluster-block-dense': () => ({
      type: 'cluster-block-dense',
      title: 'Where paid creative workflows break',
      description: 'Friction points media buyers recognize.',
      cards: [
        { icon: 'chat', title: 'Ad-to-page mismatch', description: 'Creative promise ≠ landing visuals.' },
        { icon: 'image', title: 'Slow variant tests', description: 'Every hook becomes a design ticket.' },
        { icon: 'brand', title: 'Brand drift', description: 'Channels stop looking like one brand.' },
        { icon: 'flask', title: 'Tool sprawl', description: 'Research, gen and edit in different apps.' },
        { icon: 'globe', title: 'Localization lag', description: 'New markets rebuild manually.' },
        { icon: 'refresh', title: 'Weak retarget loop', description: 'Winners cannot refresh fast enough.' },
      ],
    }),
    'feature-detail': () => ({
      type: 'feature-detail',
      title: 'From brief to coordinated delivery',
      description: 'Each row maps to a shippable outcome.',
      items: [
        {
          title: 'Brief with market context',
          description: 'Upload references and competitor URLs before generation.',
          points: ['Web Search', 'Brand PDFs', 'SKU context'],
          cta: { text: 'Build brief', href: '', variant: 'primary' },
          media: { src: m.research, alt: 'Brief' },
        },
        {
          title: 'Generate channel-ready assets',
          description: 'PDP, ads, email and social from one direction.',
          reverse: true,
          points: ['Multi ratio', 'Mockups', 'Variants'],
          cta: { text: 'Generate', href: '', variant: 'primary' },
          media: { src: m.product, alt: 'Generate' },
        },
      ],
    }),
    'showcase-horizontal': () => ({
      type: 'showcase-horizontal',
      title: 'Full-funnel rollout on one canvas',
      items: [
        { media: { src: m.research, alt: 'Acquire' }, title: 'Acquire', description: 'Hooks, thumbnails and ad variants.', cta: { text: 'Plan acquisition', href: '' } },
        { media: { src: m.product, alt: 'Convert' }, title: 'Convert', description: 'PDP and landing visuals with proof.', cta: { text: 'Improve conversion', href: '' } },
        { media: { src: m.video, alt: 'Retarget' }, title: 'Retarget', description: 'Short cuts and reminder creatives.', cta: { text: 'Retarget', href: '' } },
        { media: { src: m.brand, alt: 'Localize' }, title: 'Localize', description: 'Regional variants, same brand system.', cta: { text: 'Localize', href: '' } },
      ],
    }),
    'review-grid-3col': () => ({
      type: 'review-grid-3col',
      title: 'What teams say after switching',
      reviews: [
        { quote: 'Paid ROAS improved when PDP and ads finally matched.', author: 'Alex T.', role: 'Performance marketer', rating: 5 },
        { quote: 'We launch promo weeks with half the design backlog.', author: 'Mia L.', role: 'Ecommerce lead', rating: 5 },
        { quote: 'Client throughput up without hiring another designer.', author: 'Jordan K.', role: 'Agency owner', rating: 5 },
      ],
    }),
    'pricing-block': () => ({
      type: 'pricing-block',
      title: 'Choose the plan for your campaign scale',
      description: 'Start free. Upgrade when assets go client-facing.',
    }),
    'faq': () => ({
      type: 'faq',
      title: 'Landing page FAQ',
      items: mergeFaqItems(
        [
          { question: 'Can I edit after generation?', answer: 'Yes. Touch Edit, Text Edit and Edit Elements refine output without restarting.' },
          { question: 'Which Landing storyline should I use for ads?', answer: 'Match intent: trial for Search, brand-trust for awareness, vs-competitor for conquest, offer-close for retargeting. See landing-storylines.json.' },
          { question: 'Is landing-full for paid traffic?', answer: 'No. landing-full is a 15-section internal demo only.' },
        ],
        { question: 'Is Lovart a generator or a design agent?', answer: 'Lovart is an AI Design Agent — it researches, generates, edits and extends coordinated assets from one brief.' },
      ),
    }),
    'cta-default': () => ({
      type: 'cta-default',
      ...buildCtaSection('campaign workflow', { storyline }),
      buttons: [
        { text: p === 'offer' ? 'Get Pro offer' : 'Get started', action: 'openLogin', variant: 'primary' },
        { text: 'See examples', href: '', variant: 'secondary' },
      ],
    }),
  };
}

function buildDoc(c, sequences) {
  const slug = `${c.slugBase}-${c.storyline}`;
  const types = sequences[c.storyline];
  if (!types) throw new Error(`Unknown storyline: ${c.storyline}`);
  const ctx = { persona: c.persona, storyline: c.storyline };
  const builders = sectionBuilders(ctx);
  const sections = types.map((t) => {
    const fn = builders[t];
    if (!fn) throw new Error(`No builder for ${t} in ${c.storyline}`);
    return fn();
  });
  return {
    slug,
    language: 'en',
    category: 'topic',
    schemaVersion: 'composite-v2',
    storylineId: c.storyline,
    storylineTemplate: c.storyline,
    draftStatus: 'local-only',
    draftTheme: c.theme,
    draftNotes: `Landing Page reference (${c.storyline}, ${types.length} sections)`,
    url_path: `https://www.lovart.ai/topics/${slug}`,
    title: c.title,
    description: c.description,
    bodyJson: JSON.stringify(sections),
    copyPrimaryPromise: c.title,
    copyIntent: c.storyline,
    seo: {
      _type: 'seo',
      title: c.title,
      description: c.description,
      keywords: c.keywords,
      ogImage: { _type: 'imageSource', sourceType: 'external', url: IMG.og, alt: c.title },
      noIndex: true,
    },
  };
}

function main() {
  const dryRun = process.argv.includes('--dry-run');
  const sequences = loadSequences();
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const manifest = [];

  for (const c of CASES) {
    const doc = buildDoc(c, sequences);
    const preflight = validateLandingCopyPreflight({
      title: doc.title,
      description: doc.description,
      bodyJson: doc.bodyJson,
      storyline: c.storyline,
    });
    if (preflight.errors.length) throw new Error(`[copy-preflight] ${c.storyline}: ${preflight.errors.join(' | ')}`);
    const file = `${doc.slug}-en.json`;
    const expected = sequences[c.storyline].join(',');
    const actual = JSON.parse(doc.bodyJson).map((s) => s.type).join(',');
    if (expected !== actual) throw new Error(`Order mismatch ${file}`);
    manifest.push({
      theme: c.theme,
      storyline: c.storyline,
      slug: doc.slug,
      file,
      sections: sequences[c.storyline].length,
      copyPreflightWarnings: preflight.warnings,
    });
    if (dryRun) {
      console.log('[dry-run]', file, sequences[c.storyline].length);
      continue;
    }
    fs.writeFileSync(path.join(OUT_DIR, file), `${JSON.stringify(doc, null, 2)}\n`);
    console.log('Wrote', file);
  }

  if (!dryRun) {
    fs.writeFileSync(path.join(REFRESH, 'landing-examples/manifest.json'), `${JSON.stringify({ generatedAt: new Date().toISOString(), cases: manifest }, null, 2)}\n`);
  }
}

main();
