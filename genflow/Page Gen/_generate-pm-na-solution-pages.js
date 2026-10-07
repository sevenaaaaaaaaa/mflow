#!/usr/bin/env node
/**
 * Generate NA PM Solution pages from Product Marketing copy.
 * Marketers → solution-p-marketing (P1)
 * Business owners → solution-i-ecommerce (I1)
 */
const fs = require('fs')
const path = require('path')

const STORYLINES = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'solution-storylines-v2.json'), 'utf8')
)

const IMG = {
  heroMkt:
    'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/437351775c82f2d4aa7628eccd1ffa393a8d8010d3b448678901622628cc95cf.png',
  heroBiz:
    'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/55b94439550ff0fefec6a09ca160df2fe8d0f24f.png',
  b1: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/76f6f16db402baffa46024261bf5603e63fe763833b01f497731603a2495a346.png',
  b2: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/23baa922486b6ebd84c24d0f0af8b451e1792f3565221b27ceff84b20b125669.png',
  b3: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/a5b053a156c28e87940cd226a93c311a07f437b5c0c48635f6b3240fe57b6de8.png',
  b4: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/181f2cd3e3b8744401ef85904d63f0c07c492887604dcacd369ea3e807183bc6.png',
  tab1: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/b8e9479301c56b3946bbce10cadc78b70e0d6365.png',
  tab2: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/1f66f7b0726f0b3f59645d6b3a471691818a07f2.png',
  tab3: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/8efdfd8318084a8c88bb72c706bb33c7f2564b8b.png',
  s1: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/181ed5a5733bccb4594c29e1c15bd1ce93f8ea52.png',
  s2: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/98dde485f8c6789596006f5ee601a445d6606b78.png',
  s3: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/805d2e070d4404ed0cd6ae865930375919374b97.png',
}

const SHARED_TOOLS = [
  {
    icon: 'brand',
    title: 'Brand kit',
    description: 'Save your colors, fonts & logos to stay on-brand across every design',
  },
  {
    icon: 'sparkle',
    title: 'Custom skills',
    description: 'Teach Lovart your workflow once, then reuse it anytime',
  },
  {
    icon: 'video',
    title: 'Animate logos',
    description: 'Bring your logo to life with motion in a few clicks',
  },
  {
    icon: 'brand',
    title: 'Font generator',
    description: "Create custom fonts that match your brand's look",
  },
  {
    icon: 'image',
    title: 'Upscale images',
    description: 'Sharpen and enlarge images without losing quality',
  },
  {
    icon: 'pointer',
    title: 'Remove background',
    description: 'Cut out backgrounds cleanly in 1 click',
  },
  {
    icon: 'refresh',
    title: 'Multi-angles',
    description: 'Generate the same subject from multiple angles instantly',
  },
  {
    icon: 'globe',
    title: 'Access to all image&video models',
    description: 'Switch between top AI models like GPT image 2 and Seedance 2, all in one place',
  },
]

const FAQ_WHAT_IS_LOVART = {
  question: 'What is Lovart?',
  answer:
    'Lovart is an AI design agent that turns your ideas into polished creative design (product shots, social posts, marketing campaign kits, brand videos, and more) in minutes. Most design products give you tools. Lovart gives you finished outcomes. You describe what you need, and Lovart handles the end-to-end creative process: picking models, generating assets, and editing assets with AI, so you get production-ready files fast and easy. To learn how to use Lovart, please visit https://www.lovart.ai/docs/getting-started/how-lovart-works.',
}

const FAQ_MODELS = {
  question: 'Is Lovart integrated with top AI models?',
  answer:
    'Switch between top AI models like GPT image 2 and Seedance 2, all in one place.',
}

const FAQ_COMMERCIAL = {
  question: 'Can I use Lovart output commercially, and do I own the rights to it?',
  answer:
    'Paid plans include commercial usage rights for assets you create. Check your plan for export limits and licensing details.',
}

const FAQ_EXPORT = {
  question: 'What sizes and formats can I export?',
  answer:
    'Export channel-ready sizes for Instagram, X, YouTube, LinkedIn, Facebook, Meta, TikTok Shop, Amazon, Shopify, and more.',
}

const FAQ_FREE = {
  question: 'Is Lovart free to use?',
  answer: 'You can start free on Lovart. Upgrade when you need more credits, premium models, and team features.',
}

const FAQ_MORE = {
  question: 'I have more questions!',
  answer: 'Visit https://www.lovart.ai/docs or contact our support team — we are happy to help.',
}

function orderSections(storylineId, sectionsByType) {
  const order = STORYLINES.storylines[storylineId].sections
  return order.map((type) => {
    const s = sectionsByType[type]
    if (!s) throw new Error(`Missing ${type} for ${storylineId}`)
    return { ...s, type }
  })
}

function buildPage(meta) {
  const ordered = orderSections(meta.storyline, meta.sectionsByType)
  return {
    _type: 'compositePage',
    category: 'solution',
    slug: meta.slug,
    title: meta.title,
    description: meta.description,
    sourceType: 'solution',
    storyline: meta.storyline,
    bodyJson: JSON.stringify(ordered),
    seo: {
      title: meta.seoTitle || `${meta.title} | Lovart`,
      description: meta.description,
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
    url_path: `/solution/${meta.slug}`,
    section: ordered,
  }
}

const marketers = {
  'hero-cinematic': {
    tag: 'Marketers',
    title: 'Good design is good marketing',
    highlightedText: 'Design agent that makes marketers prolific',
    description: '500K+ marketers use Lovart to scale content marketing',
    buttons: [
      { text: 'Try Lovart today', action: 'openLogin', variant: 'primary' },
      { text: 'See campaign examples', href: '', variant: 'secondary' },
    ],
    media: { src: IMG.heroMkt, alt: 'Lovart for marketers — campaign kit and social creative' },
  },
  'bento-4': {
    title: 'Why marketers choose Lovart',
    description: 'From one brief to channel-ready campaigns — on brand, editable, fast.',
    columns: 4,
    features: [
      {
        title: 'One brief in, a whole campaign out',
        description:
          'Upload a campaign brief, and get a complete campaign kit with dozens of images, social posts, ads, videos, and everything you need to launch in minutes.',
        media: { src: IMG.b1, alt: 'Campaign kit from one brief' },
      },
      {
        title: 'On-brand assets across every channel',
        description:
          'Upload your logo and brand kit, Lovart keeps every campaign asset on-brand, and auto-sizes it for Instagram, X, YouTube, LinkedIn, Facebook, and more',
        media: { src: IMG.b4, alt: 'On-brand multi-channel assets' },
      },
      {
        title: 'Easily change anything with AI editing',
        description:
          'Swap backgrounds, update products, change models, rewrite copy, or resize designs in seconds without starting over.',
        media: { src: IMG.b2, alt: 'AI editing in Lovart' },
      },
      {
        title: 'Start with a template / skill',
        description: '500K+ marketers use Lovart to scale content marketing',
        media: { src: IMG.b3, alt: 'Templates and custom skills' },
      },
    ],
  },
  'capability-tabs': {
    title: 'More design tools to help you create on-brand assets',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      {
        label: 'Brand kit',
        icon: 'brand',
        content: {
          title: 'Brand kit',
          description: 'Save your colors, fonts & logos to stay on-brand across every design',
          media: { src: IMG.b4, alt: 'Brand kit' },
          points: ['Colors, fonts & logos', 'On-brand across every design', 'Channel-ready exports'],
        },
      },
      {
        label: 'Custom skills',
        icon: 'sparkle',
        content: {
          title: 'Custom skills',
          description: 'Teach Lovart your workflow once, then reuse it anytime',
          media: { src: IMG.b1, alt: 'Custom skills' },
          points: ['Teach your workflow once', 'Reuse anytime', 'Campaign kit', 'Social poster'],
        },
      },
      {
        label: 'Animate logos',
        icon: 'video',
        content: {
          title: 'Animate logos',
          description: 'Bring your logo to life with motion in a few clicks',
          media: { src: IMG.tab2, alt: 'Animate logos' },
          points: ['Motion graphics', 'Branded assets', 'Few clicks'],
        },
      },
      {
        label: 'All models',
        icon: 'globe',
        content: {
          title: 'Access to all image&video models',
          description:
            'Switch between top AI models like GPT image 2 and Seedance 2, all in one place',
          media: { src: IMG.tab3, alt: 'Image and video models' },
          points: ['GPT image 2', 'Seedance 2', 'Image & video in one place'],
        },
      },
    ],
  },
  'bento-2': {
    title: 'Built for how marketers work',
    columns: 2,
    features: [
      {
        title: 'One brief in, a whole campaign out',
        description:
          'Upload a campaign brief, and get a complete campaign kit with dozens of images, social posts, ads, videos, and everything you need to launch in minutes.',
        media: { src: IMG.b1, alt: 'Campaign out' },
      },
      {
        title: 'On-brand assets across every channel',
        description:
          'Upload your logo and brand kit, Lovart keeps every campaign asset on-brand, and auto-sizes it for Instagram, X, YouTube, LinkedIn, Facebook, and more',
        media: { src: IMG.b4, alt: 'On-brand channels' },
      },
    ],
  },
  'workflow-vertical': {
    title: 'From brief to launch in minutes',
    description: 'Upload a campaign brief — Lovart handles the rest.',
    layout: 'vertical',
    steps: [
      {
        step: 1,
        title: 'Upload a campaign brief',
        description:
          'Upload a campaign brief, and get a complete campaign kit with dozens of images, social posts, ads, videos, and everything you need to launch in minutes.',
        media: { src: IMG.b1, alt: 'Upload brief' },
      },
      {
        step: 2,
        title: 'Get on-brand assets for every channel',
        description:
          'Upload your logo and brand kit, Lovart keeps every campaign asset on-brand, and auto-sizes it for Instagram, X, YouTube, LinkedIn, Facebook, and more',
        media: { src: IMG.b4, alt: 'On-brand assets' },
      },
      {
        step: 3,
        title: 'Easily change anything with AI editing',
        description:
          'Swap backgrounds, update products, change models, rewrite copy, or resize designs in seconds without starting over.',
        media: { src: IMG.b2, alt: 'AI editing' },
      },
    ],
  },
  'comparison-table': {
    title: 'Tools vs finished outcomes',
    description: 'Most design products give you tools. Lovart gives you finished outcomes.',
    headers: ['Need', 'Design tools', 'Lovart for marketers'],
    highlightColumn: 2,
    rows: [
      {
        feature: 'Campaign production',
        values: [
          'Piece together across tools',
          'One brief in, a whole campaign out',
        ],
      },
      {
        feature: 'Brand consistency',
        values: [
          'Manual resizing per channel',
          'On-brand assets across every channel',
        ],
      },
      {
        feature: 'Editing',
        values: [
          'Start over for every change',
          'Easily change anything with AI editing',
        ],
      },
      {
        feature: 'Outcome',
        values: ['Tools', 'Finished outcomes — production-ready files fast and easy'],
      },
    ],
  },
  'cluster-block-dense': {
    title: 'More design tools to help you create on-brand assets',
    description: 'Built for various professionals',
    cards: [
      ...SHARED_TOOLS,
      {
        icon: 'pointer',
        title: 'Business owners',
        description:
          'Get professional marketing visuals out the door faster — ads, social posts, and e-commerce product shots, all in Lovart.',
      },
      {
        icon: 'brand',
        title: 'Designers',
        description:
          'Spend less time on repetitive work and more on ideas, while keeping full control of the look in Lovart.',
      },
    ],
  },
  'showcase-stacked': {
    title: 'Start with a template / skill',
    items: [
      {
        media: { src: IMG.s1, alt: 'Campaign kit' },
        title: 'Campaign kit',
        description:
          'Upload a campaign brief, and get a complete campaign kit with dozens of images, social posts, ads, videos, and everything you need to launch in minutes.',
        cta: { text: 'Try Lovart today', href: '' },
      },
      {
        media: { src: IMG.s2, alt: 'Social poster' },
        title: 'Social poster',
        description:
          'On-brand assets auto-sized for Instagram, X, YouTube, LinkedIn, Facebook, and more',
        cta: { text: 'Create social posts', href: '' },
      },
      {
        media: { src: IMG.s3, alt: 'Motion graphics' },
        title: 'Branded assets & motion graphics',
        description: 'Bring your logo to life with motion in a few clicks',
        cta: { text: 'Animate your brand', href: '' },
      },
    ],
  },
  testimonial: {
    title: 'What marketers say about Lovart',
    testimonials: [
      {
        quote:
          'Lovart saves me about one full afternoon every week on social media posts. Better images in my essays act as stronger advertising, driving more engagement and traffic. One essay saw a 191% increase in views after a few weeks of Lovart-assisted images. I also booked an award-winning author for developmental editing, and that single package paid for my Lovart yearly subscription many times over.',
        author: 'Boaz',
        role: 'The Orthodox Snake Writing Agency',
      },
      {
        quote:
          'My typical day consists of research, studying marketing strategies, managing social media, and customer service. Lovart helps me maintain a high-quality brand by producing high-quality images. It saves me about 10–15 hours a week compared to creating content in Canva, giving me more time for product and marketing work. This has enabled me to launch 7 more products and reach about 300 more customers.',
        author: 'Abokar Hassan',
        role: 'Co-founder & Head of Marketing at Amana Home',
      },
    ],
  },
  'pricing-block': {
    title: 'Try Lovart today',
    description: '500K+ marketers use Lovart to scale content marketing',
  },
  faq: {
    title: 'FAQ',
    items: [
      FAQ_WHAT_IS_LOVART,
      {
        question: 'What can I make with Lovart as a marketer?',
        answer:
          "Most of what you'd normally brief out to a designer or piece together across separate tools. Ad and paid social creative, organic posts, banners, product images, and email visuals — generated from a prompt or a reference, then refined by just telling Lovart what to change. You stay on-brand with your saved colors, fonts, and logos, and export everything in the sizes each channel needs.",
      },
      FAQ_MODELS,
      FAQ_COMMERCIAL,
      FAQ_EXPORT,
      FAQ_FREE,
      FAQ_MORE,
    ],
  },
  'cta-default': {
    title: 'Try Lovart today',
    description: 'Good design is good marketing — design agent that makes marketers prolific.',
    buttons: [
      { text: 'Try Lovart today', action: 'openLogin', variant: 'primary' },
      { text: 'See pricing', href: '', variant: 'secondary' },
    ],
  },
}

const businessOwners = {
  'hero-journey': {
    badge: 'Business owners',
    title: 'Good design is good business',
    highlightedText: 'Ship product photos, ads, and packaging in minutes',
    description: '1M+ business owners use Lovart to scale content marketing',
    buttons: [
      { text: 'Try Lovart today', action: 'openLogin', variant: 'primary' },
      { text: 'See product examples', href: '', variant: 'secondary' },
    ],
    journeyCards: [
      {
        step: '01',
        title: 'Animated logos',
        subtitle: 'Bring your logo to life with motion in a few clicks.',
        icon: 'brand',
      },
      {
        step: '02',
        title: 'Amazon product listing kit',
        subtitle: 'Main shots, lifestyle scenes, infographics, and A+ modules, sized to spec.',
        icon: 'image',
      },
      {
        step: '03',
        title: 'Ad creatives for A/B testing',
        subtitle: 'Dozens of 9:16, 1:1, and 16:9 ad variants for Meta and other ad platforms.',
        icon: 'flask',
      },
      {
        step: '04',
        title: 'On-model photography',
        subtitle:
          'Realistic on-model shots with diverse poses, body types, and styling contexts.',
        icon: 'pointer',
      },
      {
        step: '05',
        title: 'Packaging & campaigns',
        subtitle: '3D mockups, BFCM kits, and email visuals — all from one brief.',
        icon: 'sparkle',
      },
    ],
  },
  'bento-4': {
    title: 'Why business owners choose Lovart',
    description: '1M+ business owners use Lovart to scale content marketing',
    columns: 4,
    features: [
      {
        title: 'One brief in, a whole campaign out',
        description:
          'Upload a product, share a brief, and get 40+ product images, ads, videos, social posts, and everything you need to launch in minutes.',
        media: { src: IMG.b1, alt: 'One brief campaign out' },
      },
      {
        title: 'On-brand product assets tailored for every channel',
        description:
          'Upload your logo and brand kit, Lovart keeps every asset on-brand, and auto-sizes it for Meta, TikTok Shop, Amazon, Shopify, and more.',
        media: { src: IMG.b4, alt: 'On-brand product assets' },
      },
      {
        title: 'Easily change anything with AI editing',
        description:
          'Swap backgrounds, update products, change models, rewrite copy, or resize designs in seconds without starting over.',
        media: { src: IMG.b2, alt: 'AI editing' },
      },
      {
        title: 'Sell more without hiring more',
        description:
          'Launch more products, run more promotions, and test more campaigns while spending less time and money on creative production.',
        media: { src: IMG.b3, alt: 'Sell more without hiring more' },
      },
    ],
  },
  'capability-tabs': {
    title: 'What business owners make with Lovart',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      {
        label: 'Listings',
        icon: 'image',
        content: {
          title: 'Build Amazon/Shopify product listing kits',
          description:
            'Produce main shots, lifestyle scenes, infographics, and A+ modules, sized to spec for Seller Central and Shopify PDPs.',
          media: { src: IMG.s1, alt: 'Product listing kits' },
          points: ['Amazon Seller Central', 'Shopify PDPs', 'Main shots & lifestyle scenes'],
        },
      },
      {
        label: 'Ads & video',
        icon: 'video',
        content: {
          title: 'Ad creatives & cinematic product videos',
          description:
            'Generate dozens of ad variants for Meta. Turn one product image into product demos, UGC videos, unboxing reels, slow motion shots and more.',
          media: { src: IMG.tab2, alt: 'Ads and video' },
          points: ['9:16, 1:1, 16:9 ad variants', 'UGC & unboxing reels', 'A/B testing at scale'],
        },
      },
      {
        label: 'Brand & packaging',
        icon: 'brand',
        content: {
          title: 'Design logo and brand identity',
          description:
            'Generate a full brand identity with logo, color palette, typography, and more in one sitting. Visualize labels, colors, and SKU options in photorealistic 3D before you commit to a print run.',
          media: { src: IMG.b4, alt: 'Brand and packaging' },
          points: ['Logo & brand identity', 'Packaging variations', '3D mockups'],
        },
      },
      {
        label: 'Campaigns',
        icon: 'sparkle',
        content: {
          title: 'BFCM, email & localization',
          description:
            'Generate hero banners, ads, emails, and social posts that match across Shopify, Klaviyo, and Meta, all from one brief. Translate copy, swap models, and adapt scenes for any region.',
          media: { src: IMG.tab3, alt: 'Campaigns' },
          points: ['BFCM & holiday campaigns', 'Email and SMS visuals', 'Localize for any market'],
        },
      },
    ],
  },
  'bento-2': {
    title: 'Outcomes business owners measure',
    columns: 2,
    features: [
      {
        title: 'One brief in, a whole campaign out',
        description:
          'Upload a product, share a brief, and get 40+ product images, ads, videos, social posts, and everything you need to launch in minutes.',
        media: { src: IMG.b1, alt: 'Campaign out' },
      },
      {
        title: 'Sell more without hiring more',
        description:
          'Launch more products, run more promotions, and test more campaigns while spending less time and money on creative production.',
        media: { src: IMG.b3, alt: 'Sell more' },
      },
    ],
  },
  'workflow-vertical': {
    title: 'From product brief to launch',
    description: 'Upload a product, share a brief — ship in minutes.',
    layout: 'vertical',
    steps: [
      {
        step: 1,
        title: 'Upload a product, share a brief',
        description:
          'Upload a product, share a brief, and get 40+ product images, ads, videos, social posts, and everything you need to launch in minutes.',
        media: { src: IMG.b1, alt: 'Upload product brief' },
      },
      {
        step: 2,
        title: 'On-brand assets for every channel',
        description:
          'Upload your logo and brand kit, Lovart keeps every asset on-brand, and auto-sizes it for Meta, TikTok Shop, Amazon, Shopify, and more.',
        media: { src: IMG.b4, alt: 'Channel assets' },
      },
      {
        step: 3,
        title: 'Easily change anything with AI editing',
        description:
          'Swap backgrounds, update products, change models, rewrite copy, or resize designs in seconds without starting over.',
        media: { src: IMG.b2, alt: 'Edit with AI' },
      },
    ],
  },
  'comparison-table': {
    title: 'Tools vs finished outcomes',
    description: 'Most design products give you tools. Lovart gives you finished outcomes.',
    headers: ['Need', 'Manual creative production', 'Lovart for business owners'],
    highlightColumn: 2,
    rows: [
      {
        feature: 'Product launch assets',
        values: ['Weeks of production', '40+ images, ads, videos, social posts in minutes'],
      },
      {
        feature: 'Channel sizing',
        values: ['Resize every asset manually', 'Auto-sized for Meta, TikTok Shop, Amazon, Shopify'],
      },
      {
        feature: 'Editing',
        values: ['Reshoots and redesigns', 'Easily change anything with AI editing'],
      },
      {
        feature: 'Scale',
        values: ['Hire more for more output', 'Sell more without hiring more'],
      },
    ],
  },
  'cluster-block-dense': {
    title: 'More design tools to help you create on-brand assets',
    description: 'Built for various professionals',
    cards: [
      ...SHARED_TOOLS,
      {
        icon: 'sparkle',
        title: 'Marketers',
        description:
          'Ship full campaigns without waiting on the design queue — ad variants, landing pages, emails, and social posts, all in Lovart.',
      },
      {
        icon: 'brand',
        title: 'Designers',
        description:
          'Spend less time on repetitive work and more on ideas, while keeping full control of the look in Lovart.',
      },
    ],
  },
  'showcase-stacked': {
    title: 'Use cases business owners run today',
    items: [
      {
        media: { src: IMG.s1, alt: 'Amazon Shopify listing kit' },
        title: 'Build Amazon/Shopify product listing kits',
        description:
          'Produce main shots, lifestyle scenes, infographics, and A+ modules, sized to spec for Seller Central and Shopify PDPs.',
        cta: { text: 'Build listing kits', href: '' },
      },
      {
        media: { src: IMG.s2, alt: 'Product videos' },
        title: 'Cinematic product videos from one shot',
        description:
          'Turn one product image into product demos, UGC videos, unboxing reels, slow motion shots and more for every platform.',
        cta: { text: 'Create product video', href: '' },
      },
      {
        media: { src: IMG.s3, alt: 'BFCM campaign' },
        title: 'Build a BFCM or holiday campaign',
        description:
          'Generate hero banners, ads, emails, and social posts that match across Shopify, Klaviyo, and Meta, all from one brief.',
        cta: { text: 'Plan a campaign', href: '' },
      },
    ],
  },
  'review-grid-3col': {
    title: 'What business owners say about Lovart',
    columns: 3,
    reviews: [
      {
        title: '10–15 hours saved per week vs. Canva',
        body: 'Lovart saves me about 10–15 hours a week compared to creating content in Canva, giving me more time for product and marketing work. This has enabled me to launch 7 more products and reach about 300 more customers.',
        author: 'Abokar Hassan',
        role: 'Co-founder of Amana Home',
      },
      {
        title: 'Campaign production: 28–35 hrs → 7–9 hrs',
        body: "A full campaign went from 28–35 hours over 2–3 weeks to 7–9 hours total. I now save 22–27 hours per week… Capacity increased from 3–4 major clients per month to 7–8 major projects. Revenue is up almost 2x because I can take on more work. It's the difference between surviving and scaling.",
        author: 'Alchemists Cask',
        role: 'Founder of Alchemists Cask',
      },
    ],
  },
  'pricing-block': {
    title: 'Try Lovart today',
    description: '1M+ business owners use Lovart to scale content marketing',
  },
  faq: {
    title: 'FAQ',
    items: [
      FAQ_WHAT_IS_LOVART,
      {
        question: 'What can I make with Lovart as a business owner?',
        answer:
          'Design logo and brand identity. Build Amazon/Shopify product listing kits. Create packaging variations & 3D mockups. Get ad creatives for A/B testing. Cinematic product videos from one shot. Build a BFCM or holiday campaign. Design Email and SMS visuals. Create on-model photography in every angle. Localize creative assets for any market. Swap models and products in any image.',
      },
      FAQ_MODELS,
      FAQ_COMMERCIAL,
      FAQ_EXPORT,
      FAQ_FREE,
      FAQ_MORE,
    ],
  },
  'cta-default': {
    title: 'Try Lovart today',
    description:
      'Good design is good business — ship product photos, ads, and packaging in minutes.',
    buttons: [
      { text: 'Try Lovart today', action: 'openLogin', variant: 'primary' },
      { text: 'See pricing', href: '', variant: 'secondary' },
    ],
  },
}

const pages = [
  {
    file: 'good-design-for-marketers-en.json',
    slug: 'good-design-for-marketers',
    title: 'Good Design for Marketers',
    seoTitle: 'Good Design for Marketers | Lovart',
    description:
      'Good design is good marketing. Design agent that makes marketers prolific — 500K+ marketers use Lovart to scale content marketing.',
    keywords: [
      'lovart for marketers',
      'marketing campaign kit',
      'ai design for marketers',
      'good design good marketing',
    ],
    ogImage: IMG.heroMkt,
    storyline: 'solution-p-marketing',
    sectionsByType: marketers,
  },
  {
    file: 'good-design-for-business-owners-en.json',
    slug: 'good-design-for-business-owners',
    title: 'Good Design for Business Owners',
    seoTitle: 'Good Design for Business Owners | Lovart',
    description:
      'Good design is good business. Ship product photos, ads, and packaging in minutes — 1M+ business owners use Lovart to scale content marketing.',
    keywords: [
      'lovart for business owners',
      'product listing kit',
      'amazon shopify creative',
      'good design good business',
    ],
    ogImage: IMG.heroBiz,
    storyline: 'solution-i-ecommerce',
    sectionsByType: businessOwners,
  },
]

const outDir = path.join(__dirname, 'en')
for (const p of pages) {
  const doc = buildPage(p)
  const expected = STORYLINES.storylines[p.storyline].sections
  const actual = doc.section.map((s) => s.type)
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`Section mismatch for ${p.slug}`)
  }
  const outPath = path.join(outDir, p.file)
  fs.writeFileSync(outPath, JSON.stringify(doc, null, 2) + '\n')
  console.log(`Wrote ${outPath} [${p.storyline}]`)
}

// Update SSOT mapping
const ssotPath = path.join(__dirname, 'solution-storylines-v2.json')
const ssot = JSON.parse(fs.readFileSync(ssotPath, 'utf8'))
ssot.contentStrategyMapping['good-design-for-marketers'] = 'solution-p-marketing'
ssot.contentStrategyMapping['good-design-for-business-owners'] = 'solution-i-ecommerce'
fs.writeFileSync(ssotPath, JSON.stringify(ssot, null, 2) + '\n')
console.log('Updated solution-storylines-v2.json contentStrategyMapping')
