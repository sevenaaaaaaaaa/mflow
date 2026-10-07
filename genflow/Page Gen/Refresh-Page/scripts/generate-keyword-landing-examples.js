#!/usr/bin/env node
/**
 * Generate Landing Page reference JSON from non-brand core keywords.
 * Batch 1: Lovart-SEO-2026-05 §8.5 — 13 Google zero-rank core keywords.
 * Batch 3: §4.5 高曝光低 CTR + §8.3/8.4 模型流量（Sora/Seedance 等）
 *
 * Run: node scripts/generate-keyword-landing-examples.js [--batch=google|bing|model|all]
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
const EXAMPLES = path.join(REFRESH, 'landing-examples/en');
const OUT_DIR = path.join(EXAMPLES, 'keywords');

const STORYLINE_TEMPLATES = {
  'landing-trial-now': 'draft-lovart-tool-trial-landing-trial-now-en.json',
  'landing-gallery-detail': 'draft-lovart-shopify-growth-landing-gallery-detail-en.json',
  'landing-gallery-funnel': 'draft-lovart-creative-studio-landing-gallery-funnel-en.json',
  'landing-brand-trust': 'draft-lovart-brand-campaign-landing-brand-trust-en.json',
};

/** §8.5：GSC 5,000 词中完全无排名的 13 个核心非品牌词 */
const KEYWORD_CASES_BATCH1 = [
  {
    batchId: 'google-13',
    seoReportRef: 'Lovart-SEO-2026-05 §8.5',
    theme: 'kw-ai-ad-generator',
    keyword: 'AI Ad Generator',
    slugBase: 'draft-ai-ad-generator',
    storyline: 'landing-gallery-funnel',
    priority: 'P0',
    category: '营销/商业场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'AI Ad Generator — Meta, Google and Social Variants from One Brief | Lovart',
    description:
      'Generate ad images and video hooks for paid social and display. Lovart AI Design Agent delivers variant loops, Touch Edit and Brand Kit — beyond single ad exports.',
    keywords: ['ai ad generator', 'ai ads creator', 'ad creative generator'],
    hero: {
      badge: 'AI Ad Generator',
      title: 'Spin ad variants',
      highlightedText: 'without resetting brand context',
      description:
        'May SEO report flags ai ad generator as a zero-rank core gap. Lovart connects generation, edits and fast variant loops on one ChatCanvas.',
      primaryCta: 'Generate ad variants',
    },
    faqLead: {
      question: 'What ad formats can Lovart generate?',
      answer:
        'Lovart supports multi-ratio ad images and video hooks for paid social, display and ecommerce — with Fast Mode for variant testing and Brand Kit for consistency.',
    },
  },
  {
    theme: 'kw-ai-commercial',
    keyword: 'AI Commercial',
    slugBase: 'draft-ai-commercial',
    storyline: 'landing-gallery-funnel',
    priority: 'P0',
    category: '营销/商业场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'AI Commercial Generator — Product Ads and Promo Videos | Lovart',
    description:
      'Create AI commercial videos and ad creatives for launches and promos. Brief once; Lovart generates hooks, product demos and retarget cuts with Brand Kit.',
    keywords: ['ai commercial', 'ai commercial generator', 'ai ad video'],
    hero: {
      badge: 'AI Commercial',
      title: 'Commercial creatives',
      highlightedText: 'from brief to broadcast-ready cuts',
      description:
        'Low-competition commercial intent in the core keyword matrix — Lovart extends one promo brief into hooks, demos and retarget variants on one agent canvas.',
      primaryCta: 'Create AI commercial',
    },
    faqLead: {
      question: 'Can Lovart generate AI commercial videos?',
      answer:
        'Yes. Lovart produces commercial-style product ads, promo hooks and vertical cuts — with image-to-video, Touch Edit and campaign extension in the same workflow.',
    },
  },
  {
    theme: 'kw-ai-design-generator',
    keyword: 'AI Design Generator',
    slugBase: 'draft-ai-design-generator',
    storyline: 'landing-brand-trust',
    priority: 'P0',
    category: '核心产品类',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'AI Design Generator — Agent-Led Brand and Campaign Systems | Lovart',
    description:
      'Beyond single-shot generation: Lovart AI Design Agent researches, generates, edits and extends coordinated brand and campaign assets — built for always-on marketing teams.',
    keywords: ['ai design generator', 'ai graphic design', 'ai design tool'],
    hero: {
      badge: 'AI Design Generator',
      title: 'Design generation that',
      highlightedText: 'behaves like a creative partner',
      description:
        'One of 13 zero-rank core keywords in the May SEO report — Lovart positions as an AI Design Agent, not a template picker or single-output generator.',
      primaryCta: 'Start designing with Lovart',
    },
    faqLead: {
      question: 'Is Lovart an AI design generator or a design agent?',
      answer:
        'Lovart is an AI Design Agent — it orchestrates research, multi-model generation, Touch/Text Edit and cross-channel extension, not isolated one-off outputs.',
    },
  },
  {
    theme: 'kw-ai-logo-generator',
    keyword: 'AI Logo Generator',
    slugBase: 'draft-ai-logo-generator',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: 'Logo/设计类',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'AI Logo Generator — Brand Marks and Launch Kits | Lovart',
    description:
      'Generate logo directions, social headers and launch assets from one brief. Lovart extends logo work into Brand Kit, ads and social — not a standalone SVG export.',
    keywords: ['ai logo generator', 'logo design ai', 'ai logo maker'],
    hero: {
      badge: 'AI Logo Generator',
      title: 'Logo directions that',
      highlightedText: 'extend into a full Brand Kit',
      description:
        'High-volume logo intent with zero Google core coverage in May — try Lovart free: generate marks, refine with edits, then scale across channels with Brand Kit.',
      primaryCta: 'Try logo generator free',
    },
    faqLead: {
      question: 'Does Lovart stop at logo generation?',
      answer:
        'No. Lovart treats logos as the start of a brand system — extend into social headers, ads, email and video with consistent Brand Kit rules on ChatCanvas.',
    },
    prompts: [
      { label: 'Startup mark', prompt: 'Generate 4 logo directions for a fintech app: minimal wordmark, icon+wordmark, dark and light variants.' },
      { label: 'Rebrand kit', prompt: 'Refresh a DTC skincare logo and produce social avatar, email header and 1:1 ad lockup in the new system.' },
      { label: 'Launch pack', prompt: 'Create logo, story frames and launch ad crops for a consumer hardware preorder campaign.' },
    ],
  },
  {
    theme: 'kw-brand-video',
    keyword: 'Brand Video',
    slugBase: 'draft-brand-video',
    storyline: 'landing-brand-trust',
    priority: 'P0',
    category: '营销/商业场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'Brand Video — Awareness Cuts and Always-On Campaign Film | Lovart',
    description:
      'Produce brand video for upper-funnel awareness and always-on campaigns. Cinematic hero directions, social cuts and retarget refreshes — governed by Brand Kit.',
    keywords: ['brand video', 'brand video ai', 'ai brand film'],
    hero: {
      badge: 'Brand Video',
      title: 'Brand video that',
      highlightedText: 'stays on-model across every cut',
      description:
        'Brand video sits in the May report zero-rank list — Lovart pairs cinematic generation with logo-loop trust signals and testimonial-ready campaign extension.',
      primaryCta: 'Start brand video',
    },
    faqLead: {
      question: 'Is Lovart suited for brand awareness video?',
      answer:
        'Yes. landing-brand-trust fits upper-funnel brand video: cinematic hero, social proof modules and coordinated still + motion assets from one brand brief.',
    },
  },
  {
    theme: 'kw-character-consistency',
    keyword: 'Character Consistency',
    slugBase: 'draft-character-consistency',
    storyline: 'landing-gallery-detail',
    priority: 'P0',
    category: '核心功能/场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'Character Consistency — Same Face Across Ads, Social and Video | Lovart',
    description:
      'Keep characters and mascots consistent across image and video outputs. Lovart Style Consistency and Brand Kit reduce prompt lottery on multi-asset campaigns.',
    keywords: ['character consistency', 'consistent character ai', 'same character ai'],
    hero: {
      badge: 'Character Consistency',
      title: 'Consistent characters',
      highlightedText: 'across every campaign surface',
      description:
        'Differentiation keyword with low competition in the core matrix — Lovart deep-dives capability tabs and feature-detail for teams scaling character-led creatives.',
      primaryCta: 'Explore consistency tools',
    },
    faqLead: {
      question: 'How does Lovart maintain character consistency?',
      answer:
        'Lovart combines Style Consistency, Brand Kit and agent context so the same character direction carries through ads, social carousels and video hooks without re-prompting from scratch.',
    },
  },
  {
    theme: 'kw-dall-e',
    keyword: 'DALL-E',
    slugBase: 'draft-dall-e-image-generation',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: 'AI模型类',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'DALL-E Style Image Generation — Multi-Model Agent on Lovart',
    description:
      'Need DALL-E class image output plus edits and campaign extension? Lovart runs multi-model image generation inside an AI Design Agent — brief, refine and scale on ChatCanvas.',
    keywords: ['dall-e', 'dall e image generator', 'dall-e ai'],
    hero: {
      badge: 'DALL-E class generation',
      title: 'Multi-model images',
      highlightedText: 'with edits and campaign extension',
      description:
        'Model-name search volume in May report with zero core ranking — Lovart offers prompt-to-image trial plus Touch Edit and cross-channel scale, not a single-image export.',
      primaryCta: 'Try image generation free',
    },
    faqLead: {
      question: 'Does Lovart include DALL-E?',
      answer:
        'Lovart integrates multiple image models in one agent workflow. You get DALL-E class output plus Touch/Text Edit, Brand Kit and extension to ads, social and video — beyond a standalone generator.',
    },
    prompts: [
      { label: 'Concept frame', prompt: 'Generate a cinematic product hero in DALL-E style: premium skincare bottle, soft studio light, 4:5 crop.' },
      { label: 'Ad variant', prompt: 'Create 4 ad frames from one product direction — consistent palette, space for offer copy overlay.' },
      { label: 'Extend to social', prompt: 'Turn the winning frame into a 5-slide carousel with matching typography and character.' },
    ],
  },
  {
    theme: 'kw-marketing-video-ai',
    keyword: 'Marketing Video AI',
    slugBase: 'draft-marketing-video-ai',
    storyline: 'landing-gallery-funnel',
    priority: 'P0',
    category: '营销/商业场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'Marketing Video AI — Acquire, Convert and Retarget on One Canvas | Lovart',
    description:
      'Marketing video AI for performance teams: hook variants, product demos, social cuts and retarget refreshes — orchestrated by an AI Design Agent with Brand Kit.',
    keywords: ['marketing video ai', 'ai marketing video', 'video ads ai'],
    hero: {
      badge: 'Marketing Video AI',
      title: 'Marketing video AI that',
      highlightedText: 'covers the full funnel',
      description:
        'P1 enterprise intent in the keyword matrix, zero Google rank in May — showcase-horizontal funnel narrative for acquire → convert → retarget video workflows.',
      primaryCta: 'Plan marketing video',
    },
    faqLead: {
      question: 'Is Lovart built for marketing video workflows?',
      answer:
        'Yes. Lovart targets marketing video AI use cases: paid social hooks, product demos, UGC-style variants and retarget refreshes — with Brand Kit keeping campaigns consistent.',
    },
  },
  {
    theme: 'kw-product-video',
    keyword: 'Product Video',
    slugBase: 'draft-product-video',
    storyline: 'landing-gallery-detail',
    priority: 'P0',
    category: '营销/商业场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'Product Video — PDP Clips, Demos and Ad Hooks | Lovart',
    description:
      'Product video for ecommerce: hero loops, feature demos and paid social hooks from one SKU brief. Generate, edit and scale with Lovart AI Design Agent.',
    keywords: ['product video', 'product video ai', 'ecommerce product video'],
    hero: {
      badge: 'Product Video',
      title: 'Product video for',
      highlightedText: 'PDP, ads and retarget — one brief',
      description:
        'Opportunity keyword in core matrix, listed in May zero-rank batch — gallery-detail deep dive for SKU demos, loops and catalog-scale variants.',
      primaryCta: 'Create product video',
    },
    faqLead: {
      question: 'Can Lovart generate product videos for ecommerce?',
      answer:
        'Yes. Lovart produces PDP loops, feature demos and paid social hooks from product briefs — with image-to-video, edits and catalog-scale variants on one canvas.',
    },
  },
  {
    theme: 'kw-social-media-video',
    keyword: 'Social Media Video',
    slugBase: 'draft-social-media-video',
    storyline: 'landing-gallery-funnel',
    priority: 'P0',
    category: '营销/商业场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'Social Media Video AI — Reels, Stories and Feed Cuts | Lovart',
    description:
      'Generate social media video for Reels, Stories, TikTok and feed posts. One brief → vertical hooks, carousel companions and retarget refreshes with Brand Kit.',
    keywords: ['social media video', 'ai social video', 'instagram video ai'],
    hero: {
      badge: 'Social Media Video',
      title: 'Social video at',
      highlightedText: 'platform-native ratios — one agent',
      description:
        'Mid-priority in competitor matrix, zero rank in May GSC core set — funnel storyline for teams publishing always-on social video at scale.',
      primaryCta: 'Create social video',
    },
    faqLead: {
      question: 'Which social formats does Lovart support?',
      answer:
        'Lovart generates 9:16, 1:1 and 4:5 video hooks plus matching stills from one brief — ideal for Reels, Stories, TikTok and paid social variants.',
    },
  },
  {
    theme: 'kw-talking-avatar',
    keyword: 'Talking Avatar',
    slugBase: 'draft-talking-avatar',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: '核心功能/场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'Talking Avatar — AI Presenters and UGC-Style Video | Lovart',
    description:
      'Create talking avatar and presenter-style video for ads and explainers. Try prompts for lip-sync ready cuts, then extend with Brand Kit across channels.',
    keywords: ['talking avatar', 'ai talking avatar', 'talking head ai'],
    hero: {
      badge: 'Talking Avatar',
      title: 'Talking avatars',
      highlightedText: 'inside your campaign workflow',
      description:
        'Low-competition avatar keyword in core matrix, zero Google coverage in May — instant trial via prompt-launcher for presenter and UGC-style cuts.',
      primaryCta: 'Try talking avatar free',
    },
    faqLead: {
      question: 'Can Lovart generate talking avatar video?',
      answer:
        'Lovart supports presenter-style and UGC-style video generation as part of the agent canvas — brief, generate, edit and extend to ads and social without a separate avatar app.',
    },
    prompts: [
      { label: 'Product explainer', prompt: 'Generate a 30s talking presenter explaining a SaaS feature — clean backdrop, 9:16 and 16:9 crops.' },
      { label: 'UGC ad hook', prompt: 'Create a UGC-style talking head opener for a skincare offer — authentic tone, space for captions.' },
      { label: 'Localized variant', prompt: 'Produce 3 language variants of the same presenter script with consistent wardrobe and framing.' },
    ],
  },
  {
    theme: 'kw-ugc-generator',
    keyword: 'UGC Generator',
    slugBase: 'draft-ugc-generator',
    storyline: 'landing-gallery-funnel',
    priority: 'P0',
    category: '营销/商业场景',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'UGC Generator — Authentic Ad Hooks and Social Proof Creatives | Lovart',
    description:
      'Generate UGC-style ad hooks, testimonials and social proof creatives at scale. Lovart Fast Mode variant loops keep performance testing fast without losing brand rules.',
    keywords: ['ugc generator', 'ai ugc ads', 'ugc video generator'],
    hero: {
      badge: 'UGC Generator',
      title: 'UGC-style creatives',
      highlightedText: 'at performance-team velocity',
      description:
        'Opportunity keyword flagged in May zero-rank list — funnel narrative for teams spinning authentic hooks, demos and retarget UGC variants from one brief.',
      primaryCta: 'Generate UGC variants',
    },
    faqLead: {
      question: 'How is Lovart different from a standalone UGC generator?',
      answer:
        'Lovart embeds UGC-style generation in a full agent workflow — research, generate, Touch Edit, Brand Kit and cross-channel extension on one canvas.',
    },
  },
  {
    theme: 'kw-workflow-automation',
    keyword: 'Workflow Automation',
    slugBase: 'draft-workflow-automation',
    storyline: 'landing-brand-trust',
    priority: 'P0',
    category: 'AI Agent类',
    keywordSource: 'Lovart-SEO-2026-05 §8.5 · Google 零排名',
    title: 'Workflow Automation — AI Design Agent for Creative Ops | Lovart',
    description:
      'Automate creative workflow from brief to multi-channel delivery. Lovart AI Design Agent replaces tool sprawl with research, generation, edits and Brand Kit governance.',
    keywords: ['workflow automation', 'ai workflow automation', 'creative workflow ai'],
    hero: {
      badge: 'Workflow Automation',
      title: 'Creative workflow automation',
      highlightedText: 'with an AI Design Agent',
      description:
        'Enterprise-leaning keyword in core matrix, zero rank in May — brand-trust storyline for teams replacing fragmented stacks with agent-led creative ops.',
      primaryCta: 'See agent workflow',
    },
    faqLead: {
      question: 'Does Lovart automate design workflows?',
      answer:
        'Yes. Lovart automates research → generate → edit → extend in one agent session — reducing handoffs between image, video, copy and brand governance tools.',
    },
  },
];

/** §8.11 Bing 未覆盖核心词（相对 Batch1 的增量）+ §9 Tools 高流量页配对 */
const KEYWORD_CASES_BATCH2 = [
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11 + §9',
    relatedToolsPath: '/tools/text-to-image-generator',
    theme: 'kw-ai-image-generator',
    keyword: 'AI Image Generator',
    slugBase: 'draft-ai-image-generator',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: '核心产品类',
    keywordSource: 'Bing Core 零排名 · 配对 tools/text-to-image-generator',
    title: 'AI Image Generator — On-Brand Images from One Agent Brief | Lovart',
    description:
      'P0 core keyword with Bing zero rank in May. Generate PDP, ad and social images — extend from /tools/text-to-image-generator into full campaign workflows on ChatCanvas.',
    keywords: ['ai image generator', 'text to image', 'ai photo generator'],
    hero: {
      badge: 'AI Image Generator',
      title: 'Generate images that',
      highlightedText: 'scale beyond a single tool page',
      description:
        'May report: Bing Core 5.6% vs Google 63.9%. Pair this landing with text-to-image-generator traffic — agent-led edits, Brand Kit and cross-channel extension.',
      primaryCta: 'Try image generator free',
    },
    faqLead: {
      question: 'How does this differ from the text-to-image tool page?',
      answer:
        'The tool page starts generation fast; this landing sells the agent workflow — research, Touch/Text Edit, Brand Kit and extension to ads, email and video on one canvas.',
    },
    prompts: [
      { label: 'PDP hero', prompt: 'Generate a PDP hero and 3 lifestyle crops for wireless earbuds — studio light, 1:1 and 4:5.' },
      { label: 'Meta ads', prompt: 'Create 6 Meta ad concepts for skincare launch with offer overlay space.' },
      { label: 'Catalog scale', prompt: 'Refresh 12 SKU packshots with consistent brand palette and shadows.' },
    ],
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11 + §9',
    relatedToolsPath: '/tools/video-generator',
    theme: 'kw-ai-video-generator',
    keyword: 'AI Video Generator',
    slugBase: 'draft-ai-video-generator',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: '核心产品类',
    keywordSource: 'Bing §8.11 零排名 · 配对 tools/video-generator',
    title: 'AI Video Generator — Hooks and Ad Cuts on ChatCanvas | Lovart',
    description:
      'Bing lists ai video generator among 34 uncovered core keywords. Bridge /tools/video-generator traffic into agent-led variant loops and Brand Kit governance.',
    keywords: ['ai video generator', 'ai video maker', 'video generator ai'],
    hero: {
      badge: 'AI Video Generator',
      title: 'Video generation',
      highlightedText: 'connected to your static campaign assets',
      description:
        'Dual-engine gap keyword — try vertical hooks and product clips, then extend winning directions to ads and social without leaving the agent.',
      primaryCta: 'Try video generator free',
    },
    faqLead: {
      question: 'Does Lovart replace a standalone AI video generator?',
      answer:
        'Lovart includes multi-model video generation but positions as an AI Design Agent — same brief powers video hooks, PDP stills and retarget refreshes.',
    },
    prompts: [
      { label: 'TikTok hook', prompt: '9:16 product hook for DTC snack: bold opener, hero at 2s, CTA end card.' },
      { label: 'Image to video', prompt: 'Animate PDP hero into a 6s ecommerce loop with subtle parallax.' },
      { label: 'Ad pack', prompt: 'Four video ad variants: UGC, studio, lifestyle, offer-led — 1:1 and 9:16.' },
    ],
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-ai-photo-generator',
    keyword: 'AI Photo Generator',
    slugBase: 'draft-ai-photo-generator',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: '核心产品类',
    keywordSource: 'Bing §8.11 零排名',
    title: 'AI Photo Generator — Product, Lifestyle and Ad Photography | Lovart',
    description:
      'Generate studio, lifestyle and ad-ready photos from one brief. Lovart pairs photo generation with mockups, Touch Edit and catalog-scale variants.',
    keywords: ['ai photo generator', 'ai photography generator', 'product photo ai'],
    hero: {
      badge: 'AI Photo Generator',
      title: 'Photo generation',
      highlightedText: 'with mockups and catalog scale',
      description:
        'High-volume photo intent missing on Bing Core in May — isolate SKUs, place in scenes, then spin ad and social crops from the same agent context.',
      primaryCta: 'Try photo generator free',
    },
    faqLead: {
      question: 'Is AI photo generation different from image generation in Lovart?',
      answer:
        'Photo workflows emphasize product realism, lighting and mockup placement — Lovart extends those outputs to PDP, ads and email with Brand Kit.',
    },
    prompts: [
      { label: 'Studio packshot', prompt: 'Premium studio packshot for handbag SKU — white plus lifestyle variant, consistent shadow.' },
      { label: 'Lifestyle set', prompt: 'Three lifestyle scenes for home fragrance line — morning, evening, gift context.' },
      { label: 'Ad crop', prompt: '4:5 ad-safe product photo with gradient backdrop and copy margin.' },
    ],
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-background-remover',
    keyword: 'Background Remover',
    slugBase: 'draft-background-remover',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: '核心产品类',
    keywordSource: 'Bing §8.11 零排名',
    title: 'Background Remover — Product Cutouts to Full Campaign Scenes | Lovart',
    description:
      'Remove backgrounds and build mockups, PDP visuals and ad crops in one agent — not a one-click PNG export.',
    keywords: ['background remover', 'remove background ai', 'ai background removal'],
    hero: {
      badge: 'Background Remover',
      title: 'Remove backgrounds,',
      highlightedText: 'then ship the full product story',
      description:
        'Utility keyword in Bing uncovered core set — Lovart chains cutouts into mockups, Touch Edit and multi-format campaign extension.',
      primaryCta: 'Try background remover',
    },
    faqLead: {
      question: 'Is background removal standalone in Lovart?',
      answer:
        'It is an entry point: isolate SKUs, drop into mockups, then extend to ads, email and social without switching apps.',
    },
    prompts: [
      { label: 'Catalog batch', prompt: 'Remove BG from 12 SKUs; white plus lifestyle mockup for each.' },
      { label: 'PDP scene', prompt: 'Handbag cutout into premium studio and outdoor mockups.' },
      { label: 'Ad-ready', prompt: 'Product cutout with gradient backdrop and Meta 4:5 safe margins.' },
    ],
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-image-to-video',
    keyword: 'Image to Video',
    slugBase: 'draft-image-to-video',
    storyline: 'landing-gallery-detail',
    priority: 'P0',
    category: '核心功能/场景',
    keywordSource: 'Bing §8.11 零排名 · GSC image to image 有少量点击',
    title: 'Image to Video — Animate Product Heroes and Ad Stills | Lovart',
    description:
      'Turn PDP heroes and ad stills into loops and hooks. Gallery-detail landing for image-to-video inside a full campaign agent workflow.',
    keywords: ['image to video', 'photo to video ai', 'animate product image'],
    hero: {
      badge: 'Image to Video',
      title: 'Animate winning stills',
      highlightedText: 'without rebuilding the campaign brief',
      description:
        'P0 feature keyword with Bing zero core rank — deep-dive modules show how stills become vertical hooks, PDP loops and retarget cuts on one canvas.',
      primaryCta: 'Start image to video',
    },
    faqLead: {
      question: 'Can I animate existing product images in Lovart?',
      answer:
        'Yes. Upload or generate stills, animate with image-to-video models, refine with edits, then extend matching ads and social from the same session.',
    },
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11 + §9',
    relatedToolsPath: '/tools/text-to-image-generator',
    theme: 'kw-text-to-video',
    keyword: 'Text to Video',
    slugBase: 'draft-text-to-video',
    storyline: 'landing-gallery-detail',
    priority: 'P0',
    category: '核心功能/场景',
    keywordSource: '核心词矩阵 P0 · 配对 video-generator 漏斗',
    title: 'Text to Video — Script to Channel-Ready Clips | Lovart',
    description:
      'Prompt-to-video as part of an agent canvas — not a standalone clip exporter. Connect text-to-video with image gen, edits and multi-format scale.',
    keywords: ['text to video', 'ai text to video', 'prompt to video'],
    hero: {
      badge: 'Text to Video',
      title: 'Prompt to video,',
      highlightedText: 'then extend across the campaign',
      description:
        'Core P0 keyword complementing Bing batch — gallery-detail narrative for teams outgrowing single-purpose video tools.',
      primaryCta: 'Start with text to video',
    },
    faqLead: {
      question: 'Can text-to-video live alongside image and ad workflows?',
      answer:
        'Yes. Lovart keeps script, visuals, edits and format variants in one agent workflow instead of isolated clip tools.',
    },
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-ai-avatar',
    keyword: 'AI Avatar',
    slugBase: 'draft-ai-avatar',
    storyline: 'landing-trial-now',
    priority: 'P1',
    category: '核心功能/场景',
    keywordSource: 'Bing §8.11 零排名',
    title: 'AI Avatar — Presenters, Spokespersons and Brand Mascots | Lovart',
    description:
      'Create AI avatar visuals and presenter-style cuts for ads and explainers — with Brand Kit consistency across stills and video.',
    keywords: ['ai avatar', 'ai avatar generator', 'virtual spokesperson ai'],
    hero: {
      badge: 'AI Avatar',
      title: 'AI avatars',
      highlightedText: 'governed by Brand Kit rules',
      description:
        'Differentiation keyword in Bing uncovered set — generate avatar directions, refine with edits, extend to talking-head and UGC-style video.',
      primaryCta: 'Try AI avatar free',
    },
    faqLead: {
      question: 'Does Lovart support AI avatar video?',
      answer:
        'Lovart supports avatar and presenter-style generation as part of the agent canvas — brief once, output stills and video hooks with consistent brand rules.',
    },
    prompts: [
      { label: 'Brand mascot', prompt: 'Friendly mascot avatar for fintech app — still poses plus 9:16 presenter intro.' },
      { label: 'Explainer host', prompt: 'Professional presenter for SaaS feature walkthrough — 30s script, clean backdrop.' },
      { label: 'Localized set', prompt: 'Three locale variants of same avatar wardrobe and framing.' },
    ],
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-ai-poster',
    keyword: 'AI Poster',
    slugBase: 'draft-ai-poster',
    storyline: 'landing-gallery-detail',
    priority: 'P1',
    category: 'Logo/设计类',
    keywordSource: 'Bing §8.11 零排名 · GSC ai poster 有少量命中',
    title: 'AI Poster — Event, Promo and Retail Posters at Scale | Lovart',
    description:
      'Generate poster directions for events, promos and retail — refine with Touch Edit and scale variants with Brand Kit.',
    keywords: ['ai poster', 'ai poster maker', 'poster generator ai'],
    hero: {
      badge: 'AI Poster',
      title: 'Posters that',
      highlightedText: 'match your wider campaign system',
      description:
        'May GSC shows ai poster prompt traffic — gallery-detail landing connects poster output to ads, social and email from one brief.',
      primaryCta: 'Create AI poster',
    },
    faqLead: {
      question: 'Can Lovart generate print-ready posters?',
      answer:
        'Lovart generates poster layouts with editable layers — extend the same direction to digital ads, social and email headers on ChatCanvas.',
    },
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-ai-banner',
    keyword: 'AI Banner',
    slugBase: 'draft-ai-banner',
    storyline: 'landing-gallery-funnel',
    priority: 'P1',
    category: 'Logo/设计类',
    keywordSource: 'Bing §8.11 零排名',
    title: 'AI Banner — Display, Web and Social Banner Variants | Lovart',
    description:
      'Spin display, web hero and social banner variants from one promo brief — Fast Mode loops for performance teams.',
    keywords: ['ai banner', 'ai banner maker', 'banner generator ai'],
    hero: {
      badge: 'AI Banner',
      title: 'Banner variants',
      highlightedText: 'for every placement — one agent',
      description:
        'Mid-low competition banner intent missing on Bing Core — funnel storyline for acquire → convert banner systems across channels.',
      primaryCta: 'Generate banners',
    },
    faqLead: {
      question: 'Which banner sizes does Lovart support?',
      answer:
        'Lovart outputs common display, web hero, social and email widths from one brief — with Brand Kit and Fast Mode variant testing.',
    },
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-ai-shorts',
    keyword: 'AI Shorts',
    slugBase: 'draft-ai-shorts',
    storyline: 'landing-gallery-funnel',
    priority: 'P1',
    category: '营销/商业场景',
    keywordSource: 'Bing §8.11 零排名',
    title: 'AI Shorts — Vertical Hooks for TikTok, Reels and Shorts | Lovart',
    description:
      'Generate AI shorts and vertical hooks at performance-team velocity — variant loops with Brand Kit for always-on social.',
    keywords: ['ai shorts', 'ai short video', 'youtube shorts ai'],
    hero: {
      badge: 'AI Shorts',
      title: 'Short-form video',
      highlightedText: 'at the speed of paid social testing',
      description:
        'Opportunity keyword in competitor matrix, Bing zero rank — funnel modules for hook → product demo → retarget short cuts.',
      primaryCta: 'Create AI shorts',
    },
    faqLead: {
      question: 'Is Lovart built for short-form social video?',
      answer:
        'Yes. Lovart targets 9:16 hooks and short cuts with Fast Mode variant loops — same brief extends to static ad companions.',
    },
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    relatedToolsPath: '/tools/ai-lip-sync-generator',
    theme: 'kw-lip-sync',
    keyword: 'Lip Sync',
    slugBase: 'draft-lip-sync',
    storyline: 'landing-trial-now',
    priority: 'P1',
    category: '核心功能/场景',
    keywordSource: 'Bing §8.11 零排名 · 低竞争 P1',
    title: 'Lip Sync — Talking Head and UGC-Style Video | Lovart',
    description:
      'Low-competition lip sync keyword — generate presenter and UGC-style synced video inside the agent workflow, not a standalone app.',
    keywords: ['lip sync', 'ai lip sync', 'lip sync video ai'],
    hero: {
      badge: 'Lip Sync',
      title: 'Lip-sync video',
      highlightedText: 'inside your campaign agent',
      description:
        'P1 burst keyword per core matrix, Bing uncovered — pair with lip-sync tool traffic; extend synced cuts to ads and social variants.',
      primaryCta: 'Try lip sync free',
    },
    faqLead: {
      question: 'Does Lovart include lip sync generation?',
      answer:
        'Lovart supports lip-sync style video as part of presenter and UGC workflows — generate, edit and extend with Brand Kit on one canvas.',
    },
    prompts: [
      { label: 'UGC opener', prompt: 'UGC-style talking head opener for skincare offer — authentic tone, caption-safe framing.' },
      { label: 'Product demo', prompt: '30s synced presenter explaining SaaS feature — 9:16 and 16:9 exports.' },
      { label: 'Locale pack', prompt: 'Three language lip-sync variants with consistent wardrobe.' },
    ],
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-cinematic-video',
    keyword: 'Cinematic Video',
    slugBase: 'draft-cinematic-video',
    storyline: 'landing-brand-trust',
    priority: 'P1',
    category: '核心功能/场景',
    keywordSource: 'Bing §8.11 零排名',
    title: 'Cinematic Video — Film-Grade Brand and Product Films | Lovart',
    description:
      'Cinematic video for brand launches and hero campaigns — upper-funnel trust modules plus coordinated still and motion assets.',
    keywords: ['cinematic video', 'cinematic ai video', 'film grade ai video'],
    hero: {
      badge: 'Cinematic Video',
      title: 'Cinematic cuts',
      highlightedText: 'with brand-trust storytelling',
      description:
        'Mid-low competition cinematic intent on Bing Core gap list — brand-trust storyline with logo loop and testimonial-ready modules.',
      primaryCta: 'Start cinematic video',
    },
    faqLead: {
      question: 'Can Lovart produce cinematic brand video?',
      answer:
        'Yes. Lovart generates cinematic hero directions and social cuts — governed by Brand Kit for always-on campaign consistency.',
    },
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-graphic-design',
    keyword: 'Graphic Design',
    slugBase: 'draft-graphic-design',
    storyline: 'landing-brand-trust',
    priority: 'P0',
    category: 'Logo/设计类',
    keywordSource: 'Bing §8.11 零排名 · 核心矩阵高优先级',
    title: 'Graphic Design — Agent-Led Layouts, Ads and Brand Systems | Lovart',
    description:
      'High-volume graphic design intent with Bing zero core rank — agent-led generation, edits and Brand Kit vs manual layout tools.',
    keywords: ['graphic design', 'graphic design ai', 'ai graphic design tool'],
    hero: {
      badge: 'Graphic Design',
      title: 'Graphic design',
      highlightedText: 'orchestrated by an AI Design Agent',
      description:
        'Red-high competition keyword in core matrix — brand-trust landing for teams replacing fragmented layout stacks with agent workflows.',
      primaryCta: 'Explore graphic design agent',
    },
    faqLead: {
      question: 'Is Lovart a graphic design tool or an agent?',
      answer:
        'Lovart is an AI Design Agent — it researches, generates layouts and visuals, edits in place and extends winners across channels.',
    },
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11',
    theme: 'kw-flux',
    keyword: 'FLUX',
    slugBase: 'draft-flux-image-generation',
    storyline: 'landing-trial-now',
    priority: 'P1',
    category: 'AI模型类',
    keywordSource: 'Bing §8.11 零排名 · 模型蹭流量',
    title: 'FLUX Image Generation — Multi-Model Agent on Lovart',
    description:
      'FLUX-class image output plus Touch Edit, Brand Kit and campaign extension — model-name search intent without a single-shot export.',
    keywords: ['flux', 'flux ai', 'flux image generator'],
    hero: {
      badge: 'FLUX generation',
      title: 'FLUX-quality images',
      highlightedText: 'with agent edits and scale',
      description:
        'Model keyword on Bing uncovered list — trial landing for teams searching FLUX who need edits and cross-channel extension.',
      primaryCta: 'Try FLUX generation free',
    },
    faqLead: {
      question: 'Does Lovart include FLUX models?',
      answer:
        'Lovart integrates multiple image models including FLUX-class output — plus Touch/Text Edit, Brand Kit and campaign extension in one agent.',
    },
    prompts: [
      { label: 'Product hero', prompt: 'FLUX-style product hero for premium skincare — soft studio, 4:5 crop.' },
      { label: 'Ad frames', prompt: 'Four ad frames from one product direction with offer copy space.' },
      { label: 'Social set', prompt: 'Matching 1:1 and 9:16 social crops from winning hero.' },
    ],
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §8.11 + §9',
    relatedToolsPath: '/tools/veo3.1',
    theme: 'kw-kling',
    keyword: 'Kling',
    slugBase: 'draft-kling-video-generation',
    storyline: 'landing-trial-now',
    priority: 'P1',
    category: 'AI模型类',
    keywordSource: 'Bing §8.11 零排名 · 配对 tools/veo3.1 模型流量',
    title: 'Kling Video Generation — Model Output Inside a Design Agent | Lovart',
    description:
      'Kling-class video generation within Lovart agent workflow — brief, generate hooks, edit and extend to ads alongside other models like Veo.',
    keywords: ['kling', 'kling ai', 'kling video generator'],
    hero: {
      badge: 'Kling video',
      title: 'Kling-class video',
      highlightedText: 'inside a multi-model agent canvas',
      description:
        'Video model search volume on Bing gap list — pair with existing model tool pages; extend clips to full campaign delivery on ChatCanvas.',
      primaryCta: 'Try Kling video free',
    },
    faqLead: {
      question: 'Why use Lovart for Kling video instead of a standalone app?',
      answer:
        'Lovart embeds Kling-class generation in research → generate → edit → extend — same brief powers hooks, PDP stills and retarget variants.',
    },
    prompts: [
      { label: 'Product hook', prompt: 'Kling-style 9:16 hook for hardware launch — cinematic motion, product hero at 3s.' },
      { label: 'Image animate', prompt: 'Animate lifestyle still into 6s loop for PDP and Meta.' },
      { label: 'Variant pack', prompt: 'Three hook variants same script — UGC, studio, lifestyle tones.' },
    ],
  },
  {
    batchId: 'bing-delta',
    seoReportRef: 'Lovart-SEO-2026-05 §9',
    relatedToolsPath: '/tools/veo3.1',
    theme: 'kw-veo-3',
    keyword: 'Veo 3',
    slugBase: 'draft-veo-3-video-generation',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: 'AI模型类',
    keywordSource: '§8.9 Bing 命中 veo 3 · 配对 tools/veo3.1',
    title: 'Veo 3 Video Generation — From Model Search to Campaign Delivery | Lovart',
    description:
      'May report shows veo 3 as top Bing core hit — bridge /tools/veo3.1 into agent-led campaign extension with Brand Kit.',
    keywords: ['veo 3', 'veo 3 ai', 'google veo 3 video'],
    hero: {
      badge: 'Veo 3 video',
      title: 'Veo 3 generation',
      highlightedText: 'extended across your full funnel',
      description:
        'Highest Bing core competitor hit in May — this landing converts model traffic into agent workflows beyond a single tool export.',
      primaryCta: 'Try Veo 3 video free',
    },
    faqLead: {
      question: 'How is this landing different from the Veo 3.1 tool page?',
      answer:
        'The tool page starts generation; this landing sells campaign extension — edits, Brand Kit, ad companions and retarget refreshes on one canvas.',
    },
    prompts: [
      { label: 'Launch hook', prompt: 'Veo 3 style 9:16 launch hook for consumer electronics — cinematic, product reveal at 4s.' },
      { label: 'Demo clip', prompt: '30s product demo with clean typography overlays and end CTA frame.' },
      { label: 'Retarget cut', prompt: 'Short reminder cut reusing launch visual language — 1:1 and 9:16.' },
    ],
  },
];

/** §4.5 高曝光低 CTR 词 + §8.3/8.4 模型/GSC 命中词（非 alternative 对比页） */
const KEYWORD_CASES_BATCH3 = [
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8.3',
    relatedToolsPath: '/features/ai-video-prompt-generator-veo-sora',
    theme: 'kw-sora',
    keyword: 'Sora',
    slugBase: 'draft-sora-video-generation',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: 'AI模型类',
    keywordSource: 'GSC sora2 66点击 · 配对 veo-sora feature',
    title: 'Sora Video Generation — Model Output Inside a Design Agent | Lovart',
    description:
      'May GSC: sora2 matched 66 clicks. Generate Sora-class video inside Lovart — edit, Brand Kit and campaign extension beyond a single clip export.',
    keywords: ['sora', 'sora ai', 'sora video generator', 'sora2'],
    hero: {
      badge: 'Sora video',
      title: 'Sora-class video',
      highlightedText: 'with agent edits and funnel extension',
      description:
        'Model-name traffic from May report — pair with ai-video-prompt-generator feature; extend hooks to ads, PDP stills and retarget on ChatCanvas.',
      primaryCta: 'Try Sora video free',
    },
    faqLead: {
      question: 'Does Lovart include Sora video generation?',
      answer:
        'Lovart integrates multi-model video including Sora-class output — plus Touch Edit, Brand Kit and cross-channel extension in one AI Design Agent.',
    },
    prompts: [
      { label: 'Concept hook', prompt: 'Sora-style 9:16 launch hook — cinematic product reveal, 6s, CTA end frame.' },
      { label: 'Storyboard', prompt: 'Three-scene product story: problem, demo, offer — consistent palette.' },
      { label: 'Retarget', prompt: 'Short reminder cut reusing hero visual language — 1:1 and 9:16.' },
    ],
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8.4',
    relatedToolsPath: '/features/seedance-2-0-ai-video-generator',
    theme: 'kw-seedance',
    keyword: 'Seedance',
    slugBase: 'draft-seedance-video-generation',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: 'AI模型类',
    keywordSource: 'GSC seedance 2.0 free 113点击 · Seedance feature',
    title: 'Seedance Video Generation — 2.0 Model Inside Lovart Agent | Lovart',
    description:
      'May top GSC model hits: seedance 2.0 free (113 clicks). Bridge Seedance tool traffic into full campaign agent workflows.',
    keywords: ['seedance', 'seedance 2.0', 'seedance 2.0 free', 'seedance ai video'],
    hero: {
      badge: 'Seedance video',
      title: 'Seedance 2.0 output',
      highlightedText: 'scaled across paid social variants',
      description:
        'Strong May CTR on seedance 2.0 free — this landing converts model seekers into agent-led variant loops with Brand Kit.',
      primaryCta: 'Try Seedance free',
    },
    faqLead: {
      question: 'How is this different from the Seedance 2.0 tool page?',
      answer:
        'The feature page starts generation fast; this landing sells extension — edits, multi-format ads and retarget refreshes from one brief.',
    },
    prompts: [
      { label: 'Product loop', prompt: 'Seedance 6s PDP loop — subtle motion, ecommerce-ready, 1:1 and 9:16.' },
      { label: 'Ad hook', prompt: 'Vertical hook for hardware preorder — cinematic motion, logo safe zone.' },
      { label: 'Variant pack', prompt: 'Three hooks same offer — studio, lifestyle, UGC tone.' },
    ],
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8.4',
    theme: 'kw-seedream',
    keyword: 'Seedream',
    slugBase: 'draft-seedream-image-generation',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: 'AI模型类',
    keywordSource: 'GSC seedream 4.5 free 34点击',
    title: 'Seedream Image Generation — Multi-Model Agent on Lovart',
    description:
      'Seedream 4.5 free drove 34 GSC clicks in May. Generate Seedream-class images with Touch Edit, Brand Kit and campaign extension.',
    keywords: ['seedream', 'seedream 4.5', 'seedream ai', 'seedream free'],
    hero: {
      badge: 'Seedream',
      title: 'Seedream-quality images',
      highlightedText: 'plus edits and channel scale',
      description:
        'Image model traffic with solid May CTR — trial landing for teams who need more than a single PNG export.',
      primaryCta: 'Try Seedream free',
    },
    faqLead: {
      question: 'Does Lovart support Seedream generation?',
      answer:
        'Lovart integrates Seedream-class models alongside other image generators — with agent edits and cross-channel extension on one canvas.',
    },
    prompts: [
      { label: 'PDP hero', prompt: 'Seedream-style PDP hero for premium skincare — studio light, 4:5 crop.' },
      { label: 'Ad set', prompt: 'Four Meta ad frames from one product direction with copy space.' },
      { label: 'Social', prompt: 'Matching 1:1 feed and 9:16 story crops from winning hero.' },
    ],
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8 + 核心词矩阵',
    theme: 'kw-midjourney',
    keyword: 'Midjourney',
    slugBase: 'draft-midjourney-image-generation',
    storyline: 'landing-trial-now',
    priority: 'P1',
    category: 'AI模型类',
    keywordSource: '模型名搜索词 · 非 alternative 页',
    title: 'Midjourney Style Image Generation — Agent Workflow on Lovart',
    description:
      'Midjourney-class image output plus Touch Edit, Brand Kit and full campaign extension — not Discord-style single-image exports.',
    keywords: ['midjourney', 'midjourney ai', 'midjourney style generator'],
    hero: {
      badge: 'Midjourney-class images',
      title: 'Strong concept frames',
      highlightedText: 'that extend into full campaigns',
      description:
        'Model search intent capture — generate stylized images, refine in place, scale to ads, social and video on ChatCanvas.',
      primaryCta: 'Try generation free',
    },
    faqLead: {
      question: 'Is this a Midjourney replacement page?',
      answer:
        'No — this is a capability landing for Midjourney-style generation inside Lovart AI Design Agent, with edits and multi-channel extension built in.',
    },
    prompts: [
      { label: 'Concept board', prompt: 'Four Midjourney-style directions for a fashion lookbook — cohesive palette.' },
      { label: 'Hero frame', prompt: 'Cinematic product hero for headphones — bold lighting, 4:5 ad crop.' },
      { label: 'Extend', prompt: 'Turn winning frame into 6 Meta ad variants with Brand Kit.' },
    ],
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8 + 核心词 P2',
    theme: 'kw-motion-control',
    keyword: 'Motion Control',
    slugBase: 'draft-motion-control',
    storyline: 'landing-gallery-detail',
    priority: 'P2',
    category: '核心功能/场景',
    keywordSource: '核心词矩阵 P2 · 技术差异化',
    title: 'Motion Control — Directed Camera and Subject Motion in AI Video | Lovart',
    description:
      'Low-competition motion control keyword — gallery-detail deep dive for teams needing directed movement in product and ad video.',
    keywords: ['motion control', 'ai motion control', 'camera motion ai video'],
    hero: {
      badge: 'Motion Control',
      title: 'Control motion',
      highlightedText: 'in product and ad video workflows',
      description:
        'P2 differentiation keyword — capability tabs and feature-detail explain motion control inside a full campaign agent, not a demo clip tool.',
      primaryCta: 'Explore motion control',
    },
    faqLead: {
      question: 'Does Lovart support motion control in video?',
      answer:
        'Lovart integrates motion control capabilities within multi-model video generation — brief once, refine motion, extend cuts across channels.',
    },
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §9',
    relatedToolsPath: '/tools/text-to-image-generator',
    theme: 'kw-text-to-image',
    keyword: 'Text to Image',
    slugBase: 'draft-text-to-image',
    storyline: 'landing-trial-now',
    priority: 'P0',
    category: '核心功能/场景',
    keywordSource: '核心词 P0 · 配对 text-to-image-generator',
    title: 'Text to Image — Prompt to On-Brand Visuals | Lovart',
    description:
      'Core text-to-image intent — start from /tools/text-to-image-generator, extend into agent-led edits, Brand Kit and multi-format campaigns.',
    keywords: ['text to image', 'ai text to image', 'prompt to image'],
    hero: {
      badge: 'Text to Image',
      title: 'Prompt to image,',
      highlightedText: 'then edit and scale the winner',
      description:
        'Foundational non-brand keyword — trial landing with prompt-launcher examples for PDP, ads and social from one brief.',
      primaryCta: 'Try text to image free',
    },
    faqLead: {
      question: 'How does text-to-image work in Lovart?',
      answer:
        'Describe your visual in natural language; Lovart generates with multi-model output, then Touch/Text Edit and Brand Kit extend winners across channels.',
    },
    prompts: [
      { label: 'PDP', prompt: 'Text-to-image PDP hero for coffee subscription box — warm lifestyle, 1:1.' },
      { label: 'Ad concept', prompt: 'Six ad concepts for fitness app trial — bold hooks, 4:5 crops.' },
      { label: 'Brand mood', prompt: 'Mood board direction for sustainable fashion — 4 cohesive frames.' },
    ],
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8.4',
    theme: 'kw-image-to-image',
    keyword: 'Image to Image',
    slugBase: 'draft-image-to-image',
    storyline: 'landing-gallery-detail',
    priority: 'P1',
    category: '核心功能/场景',
    keywordSource: 'GSC image to image 45点击 · CTR 8.6%',
    title: 'Image to Image — Restyle, Adapt and Scale Product Visuals | Lovart',
    description:
      'May GSC: image to image at 8.6% CTR — gallery-detail for restyle, ratio adaptation and campaign extension from reference frames.',
    keywords: ['image to image', 'image to image ai', 'ai image variation'],
    hero: {
      badge: 'Image to Image',
      title: 'Transform reference frames',
      highlightedText: 'into full channel-ready sets',
      description:
        'Positive CTR signal in May — deep-dive landing for teams restyling heroes, adapting ratios and scaling variants with Brand Kit.',
      primaryCta: 'Start image to image',
    },
    faqLead: {
      question: 'What is image-to-image used for in Lovart?',
      answer:
        'Upload a reference; Lovart restyles, adapts ratios and generates variants — then extends matching ads, social and video from the same agent session.',
    },
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §4.5',
    theme: 'kw-freepik-ai-image-generator',
    keyword: 'Freepik AI Image Generator',
    slugBase: 'draft-freepik-ai-image-generator',
    storyline: 'landing-gallery-detail',
    priority: 'P0',
    category: '高曝光低CTR',
    keywordSource: '§4.5 · 65,392曝光 / 0.1% CTR · 非品牌对比页',
    title: 'AI Image Generator — Custom Visuals, Not Stock Downloads | Lovart',
    description:
      'May report: freepik ai image generator = 65K exposure, 0.1% CTR. CTR-optimized landing — agent-led generation with edits and Brand Kit vs generic stock flows.',
    keywords: ['freepik ai image generator', 'ai image generator free', 'custom ai images'],
    hero: {
      badge: 'AI Image Generator',
      title: 'Custom AI images',
      highlightedText: 'built for campaigns — not stock downloads',
      description:
        'High-exposure May query with near-zero CTR — this landing matches search intent with clearer value: agent workflow, edits and unique on-brand output.',
      primaryCta: 'Generate custom images',
    },
    faqLead: {
      question: 'Why use Lovart for AI image generation?',
      answer:
        'Teams searching this query often want fast AI images — Lovart adds agent context, Touch/Text Edit, Brand Kit and extension to ads and video beyond stock-style outputs.',
    },
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §4.5 / §8.10',
    theme: 'kw-canva-ai-image-generator',
    keyword: 'Canva AI Image Generator',
    slugBase: 'draft-canva-ai-image-generator',
    storyline: 'landing-trial-now',
    priority: 'P1',
    category: '高曝光低CTR',
    keywordSource: '§8.10 Bing canva ai image generator · 非 alternative 页',
    title: 'AI Image Generator for Campaign Teams — Agent-Led, Not Template-Only | Lovart',
    description:
      'Capture canva ai image generator search intent with a trial landing — agent-led images, edits and cross-channel scale (not a Canva vs Lovart comparison page).',
    keywords: ['canva ai image generator', 'canva ai generator', 'ai image generator for marketing'],
    hero: {
      badge: 'AI Image Generator',
      title: 'AI images for campaigns',
      highlightedText: 'with agent edits and Brand Kit',
      description:
        'May Bing partial match on canva ai image generator — trial landing emphasizing agent workflow beyond template-bound image exports.',
      primaryCta: 'Try AI images free',
    },
    faqLead: {
      question: 'Is this a Canva comparison page?',
      answer:
        'No. This landing targets AI image generator intent for marketing teams — Lovart positions as an AI Design Agent with edits, Brand Kit and multi-channel extension.',
    },
    prompts: [
      { label: 'Campaign set', prompt: 'Generate email hero, social post and Meta ad from one promo brief.' },
      { label: 'PDP refresh', prompt: 'PDP hero plus 3 lifestyle crops for home goods SKU.' },
      { label: 'Variant loop', prompt: 'Eight 1:1 ad hooks for bundle offer — consistent brand colors.' },
    ],
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8.3',
    theme: 'kw-hailuo-ai-video-generator',
    keyword: 'Hailuo AI Video Generator',
    slugBase: 'draft-hailuo-ai-video-generator',
    storyline: 'landing-trial-now',
    priority: 'P1',
    category: '高曝光低CTR',
    keywordSource: 'GSC hailuo ai video generator 15点击',
    title: 'AI Video Generator — Hooks and Product Clips on ChatCanvas | Lovart',
    description:
      'May GSC compound query hailuo ai video generator — trial landing bridging model search into Lovart multi-model video agent workflow.',
    keywords: ['hailuo ai video generator', 'ai video generator', 'hailuo video ai'],
    hero: {
      badge: 'AI Video Generator',
      title: 'Multi-model video',
      highlightedText: 'including Hailuo-class output',
      description:
        'Compound model + category query from May data — generate hooks and clips, then extend with Brand Kit across channels.',
      primaryCta: 'Try video generator free',
    },
    faqLead: {
      question: 'Does Lovart include Hailuo video models?',
      answer:
        'Lovart integrates multiple video models in one agent — generate, edit and extend hooks and product clips without switching apps.',
    },
    prompts: [
      { label: 'Vertical hook', prompt: '9:16 product hook for snack brand — bold opener, CTA end card.' },
      { label: 'Demo clip', prompt: '15s feature demo with clean typography overlays.' },
      { label: 'Retarget', prompt: 'Short reminder cut — 1:1 and 9:16 from same brief.' },
    ],
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8.10 + Agent类',
    theme: 'kw-ai-design-agent',
    keyword: 'AI Design Agent',
    slugBase: 'draft-ai-design-agent',
    storyline: 'landing-brand-trust',
    priority: 'P0',
    category: 'AI Agent类',
    keywordSource: '竞品词 §三 AI Agent · Bing design agent 命中',
    title: 'AI Design Agent — Research, Generate, Edit and Scale Campaigns | Lovart',
    description:
      'Category landing for AI Design Agent intent — cinematic trust modules plus coordinated image, video and brand asset delivery.',
    keywords: ['ai design agent', 'design agent', 'ai design agent free'],
    hero: {
      badge: 'AI Design Agent',
      title: 'An AI Design Agent',
      highlightedText: 'not a single-purpose generator',
      description:
        'May Bing surfaced design agent queries — brand-trust storyline for teams replacing tool sprawl with agent-led creative ops.',
      primaryCta: 'Meet the design agent',
    },
    faqLead: {
      question: 'What is an AI Design Agent?',
      answer:
        'Lovart orchestrates research, multi-model generation, Touch/Text Edit and cross-channel extension from one brief — beyond isolated image or video tools.',
    },
  },
  {
    batchId: 'model-ctr',
    seoReportRef: 'Lovart-SEO-2026-05 §8.4',
    theme: 'kw-ai-illustration-generator',
    keyword: 'AI Illustration Generator',
    slugBase: 'draft-ai-illustration-generator',
    storyline: 'landing-trial-now',
    priority: 'P1',
    category: '核心产品类',
    keywordSource: 'GSC ai illustration generator free 28点击 · tools/free-ai-illustration-generator',
    relatedToolsPath: '/tools/free-ai-illustration-generator',
    title: 'AI Illustration Generator — Editorial and Campaign Illustrations | Lovart',
    description:
      'Pair /tools/free-ai-illustration-generator traffic with agent extension — illustrations that scale to ads, social and email with Brand Kit.',
    keywords: ['ai illustration generator', 'ai illustration generator free', 'free ai illustration'],
    hero: {
      badge: 'AI Illustration Generator',
      title: 'Illustrations that',
      highlightedText: 'extend into full campaign systems',
      description:
        'May GSC free illustration queries plus existing tool page traffic — trial landing with prompt examples for editorial and ad use cases.',
      primaryCta: 'Try illustration generator free',
    },
    faqLead: {
      question: 'Can illustrations scale to ads and social?',
      answer:
        'Yes. Lovart generates illustrations then extends the winning style to ad frames, social carousels and email headers with Brand Kit consistency.',
    },
    prompts: [
      { label: 'Editorial', prompt: 'Editorial illustration for fintech blog — flat vector, brand palette.' },
      { label: 'Ad hero', prompt: 'Bold illustration hero for sustainability campaign — 4:5 ad crop.' },
      { label: 'Carousel', prompt: 'Five-slide illustrated carousel for app onboarding — consistent character.' },
    ],
  },
];

const BATCHES = {
  google: KEYWORD_CASES_BATCH1,
  bing: KEYWORD_CASES_BATCH2,
  model: KEYWORD_CASES_BATCH3,
  all: [...KEYWORD_CASES_BATCH1, ...KEYWORD_CASES_BATCH2, ...KEYWORD_CASES_BATCH3],
};

function patchSections(sections, c) {
  return sections.map((s) => {
    if (s.type === 'hero-split' || s.type === 'hero-gallery' || s.type === 'hero-cinematic') {
      return {
        ...s,
        badge: c.hero.badge,
        title: c.hero.title,
        highlightedText: c.hero.highlightedText,
        description: strengthenHeroDescription(c.hero.description, {
          output: `Generate ${c.keyword.toLowerCase()} outputs and campaign-ready assets.`,
          risk: 'Start free, keep brand context, and refine winners on ChatCanvas.',
        }),
        buttons: s.buttons?.map((btn, i) =>
          i === 0 && c.hero.primaryCta ? { ...btn, text: c.hero.primaryCta } : btn,
        ),
        media: s.media ? { ...s.media, alt: c.keyword } : s.media,
      };
    }
    if (s.type === 'prompt-launcher' && c.prompts) {
      const promptLauncher = buildPromptLauncherBlock(c.keyword, c.prompts);
      return {
        ...s,
        ...promptLauncher,
      };
    }
    if (s.type === 'faq') {
      return {
        ...s,
        title: `${c.keyword} FAQ`,
        items: mergeFaqItems(s.items, { question: c.faqLead.question, answer: c.faqLead.answer }),
      };
    }
    if (s.type === 'cta-default') {
      const ctaCopy = buildCtaSection(c.keyword, { storyline: c.storyline });
      return {
        ...s,
        ...ctaCopy,
      };
    }
    return s;
  });
}

function buildDoc(template, c) {
  const slug = `${c.slugBase}-${c.storyline}`;
  const sections = patchSections(JSON.parse(template.bodyJson), c);
  return {
    slug,
    language: 'en',
    category: 'topic',
    schemaVersion: 'composite-v2',
    storylineId: c.storyline,
    storylineTemplate: c.storyline,
    draftStatus: 'local-only',
    draftTheme: c.theme,
    draftNotes: [
      c.keywordSource,
      c.storyline,
      `(${sections.length} sections)`,
      c.relatedToolsPath ? `tools→${c.relatedToolsPath}` : null,
    ]
      .filter(Boolean)
      .join(' · '),
    targetKeyword: c.keyword,
    keywordPriority: c.priority,
    keywordCategory: c.category,
    batchId: c.batchId || 'google-13',
    seoReportRef: c.seoReportRef || 'Lovart-SEO-2026-05 §8.5',
    relatedToolsPath: c.relatedToolsPath || undefined,
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
      ogImage: template.seo.ogImage,
      noIndex: true,
    },
  };
}

function main() {
  const dryRun = process.argv.includes('--dry-run');
  const batchArg = process.argv.find((a) => a.startsWith('--batch='));
  const batchKey = batchArg ? batchArg.split('=')[1] : 'all';
  const cases = BATCHES[batchKey];
  if (!cases) {
    throw new Error(`Unknown --batch=${batchKey}. Use google | bing | model | all`);
  }

  fs.mkdirSync(OUT_DIR, { recursive: true });

  const manifest = [];
  for (const c of cases) {
    const templateFile = STORYLINE_TEMPLATES[c.storyline];
    if (!templateFile) throw new Error(`No template for ${c.storyline}`);
    const template = JSON.parse(fs.readFileSync(path.join(EXAMPLES, templateFile), 'utf8'));
    const doc = buildDoc(template, c);
    const preflight = validateLandingCopyPreflight({
      title: doc.title,
      description: doc.description,
      bodyJson: doc.bodyJson,
      storyline: c.storyline,
    });
    if (preflight.errors.length) {
      throw new Error(`[copy-preflight] ${c.keyword}: ${preflight.errors.join(' | ')}`);
    }
    const file = `${doc.slug}-en.json`;
    const rel = `en/keywords/${file}`;

    manifest.push({
      batchId: doc.batchId,
      keyword: c.keyword,
      priority: c.priority,
      category: c.category,
      storyline: c.storyline,
      theme: c.theme,
      slug: doc.slug,
      file: rel,
      sections: JSON.parse(doc.bodyJson).length,
      copyPreflightWarnings: preflight.warnings,
      seoReportRef: doc.seoReportRef,
      relatedToolsPath: doc.relatedToolsPath || null,
    });

    if (dryRun) {
      console.log('[dry-run]', doc.batchId, c.keyword, '→', c.storyline, rel);
      continue;
    }
    fs.writeFileSync(path.join(OUT_DIR, file), `${JSON.stringify(doc, null, 2)}\n`);
    console.log('Wrote', rel);
  }

  if (!dryRun) {
    fs.writeFileSync(
      path.join(REFRESH, 'landing-examples/keyword-manifest.json'),
      `${JSON.stringify(
        {
          generatedAt: new Date().toISOString(),
          seoReport: 'insight-data/Trident Insights/reports/monthly/Lovart-SEO-2026-05.md',
          batches: {
            'google-13': { ref: '§8.5', count: KEYWORD_CASES_BATCH1.length },
            'bing-delta': { ref: '§8.11 + §9', count: KEYWORD_CASES_BATCH2.length },
            'model-ctr': { ref: '§4.5 + §8.3/8.4', count: KEYWORD_CASES_BATCH3.length },
          },
          cases: manifest,
        },
        null,
        2,
      )}\n`,
    );
  }
}

main();
