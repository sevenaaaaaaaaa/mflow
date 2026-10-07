#!/usr/bin/env node
/**
 * Generate industry-axis Solution examples (I1–I6, all 6 storylines).
 * Run: node _generate-industry-examples.js
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
  wellnessHero: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/181f2cd3e3b8744401ef85904d63f0c07c492887604dcacd369ea3e807183bc6.png',
  before: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/eb6f103da589f07f425f2c736237e33f4d1719fa.png',
  after: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/7eb9d35ed6aaf819fbe425badb3310b77bdc38a7.png',
  localHero: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/b6ac2200d8f883894a7f18ee1da19d7d7aab2a7f.png',
  missionHero: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/d11411bc15e95312819272bf39a65a3cbdf230b2.png',
  saasHero: 'https://assets-persist.lovart.ai/web/model/28e251feadfb49ba8a81eb86bd81f2e2/437351775c82f2d4aa7628eccd1ffa393a8d8010d3b448678901622628cc95cf.png',
  creatorHero: 'https://assets-persist.lovart.ai/img/0ec3ec8352e24750bddb7764c24e81e1/181ed5a5733bccb4594c29e1c15bd1ce93f8ea52.png',
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
      title: `${meta.title} | Lovart`,
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

const wellness = {
  'hero-cinematic': {
    tag: 'Fitness & Wellness Solution',
    title: 'Turn your studio brand into',
    highlightedText: 'membership-driving creative',
    description:
      'Lovart helps gyms, yoga studios, coaches, and beauty brands produce class promos, transformation graphics, social reels, and member campaigns — on-brand, without a full design team.',
    buttons: [
      { text: 'Build wellness creative', href: '', variant: 'primary' },
      { text: 'See class promo examples', href: '', variant: 'secondary' },
    ],
    media: { src: IMG.wellnessHero, alt: 'Fitness and wellness creative workflow in Lovart' },
  },
  'bento-4': {
    title: 'Four creative outputs every wellness business needs',
    description: 'From class schedules to member retention — one agent workflow.',
    columns: 4,
    features: [
      { title: 'Class & program promos', description: 'Seasonal challenges, new class launches, trainer spotlights.', media: { src: IMG.bento2, alt: 'Class promos' } },
      { title: 'Member transformation', description: 'Before/after, progress stories, and testimonial visuals.', media: { src: IMG.showcase2, alt: 'Transformations' } },
      { title: 'Social & community', description: 'Reels covers, story frames, and community challenge graphics.', media: { src: IMG.bento3, alt: 'Social content' } },
      { title: 'Brand Kit consistency', description: 'Studio colors, typography, and logo across every touchpoint.', media: { src: IMG.bento1, alt: 'Brand Kit' } },
    ],
  },
  'capability-tabs': {
    title: 'Four modules for fitness and wellness growth',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      { label: 'Acquire', icon: 'social', content: { title: 'Fill classes and trials', description: 'Generate intro offers, trial week graphics, and local ad variants.', media: { src: IMG.tab2, alt: 'Acquire' }, points: ['Trial promos', 'Local Meta ads', 'Influencer collab assets'] } },
      { label: 'Convert', icon: 'sparkle', content: { title: 'Turn interest into memberships', description: 'Pricing sheets, package comparisons, and signup landing visuals.', media: { src: IMG.wellnessHero, alt: 'Convert' }, points: ['Membership tiers', 'Limited-time offers', 'Consultation booking graphics'] } },
      { label: 'Retain', icon: 'refresh', content: { title: 'Keep members engaged', description: 'Challenge calendars, milestone badges, and renewal reminder creative.', media: { src: IMG.bento1, alt: 'Retain' }, points: ['30-day challenges', 'Milestone celebrations', 'Win-back campaigns'] } },
      { label: 'Brand', icon: 'brand', content: { title: 'Look premium across channels', description: 'Brand Kit keeps franchise, boutique, and solo coach visuals aligned.', media: { src: IMG.bento4, alt: 'Brand' }, points: ['Multi-location rules', 'Trainer personal brands', 'On-brand exports'] } },
    ],
  },
  'bento-2': {
    title: 'Two outcomes wellness operators track',
    columns: 2,
    features: [
      { title: 'More trial-to-member conversion', description: 'Professional promos without agency retainers.', media: { src: IMG.bento2, alt: 'Conversion' } },
      { title: 'Consistent studio identity', description: 'Every instructor post still looks like your brand.', media: { src: IMG.bento1, alt: 'Identity' } },
    ],
  },
  'workflow-vertical': {
    title: 'Wellness creative workflow in three steps',
    description: 'From studio brief to published member campaign.',
    layout: 'vertical',
    steps: [
      { step: 1, title: 'Set up studio Brand Kit', description: 'Upload logo, brand colors, class photography, and offer details.', media: { src: IMG.bento1, alt: 'Brand Kit' } },
      { step: 2, title: 'Generate class and member campaigns', description: 'Batch promos, challenges, social frames, and email headers from one brief.', media: { src: IMG.wellnessHero, alt: 'Generate' } },
      { step: 3, title: 'Refine and publish', description: 'Touch Edit offer copy and imagery; export for Instagram, email, and print.', media: { src: IMG.showcase2, alt: 'Publish' } },
    ],
  },
  'comparison-before-after': {
    title: 'Before & after — studio marketing with Lovart',
    description: 'Same offer, same class. Lovart turns generic gym graphics into branded membership creative that converts.',
    aspect: '16:9',
    before: {
      media: { src: IMG.before, alt: 'Generic fitness promo with mismatched fonts and stock photo' },
      label: 'Before',
    },
    after: {
      media: { src: IMG.after, alt: 'Branded class promo with consistent colors and offer layout' },
      label: 'After Lovart',
    },
  },
  'cluster-block-dense': {
    title: 'Wellness scenarios this solution covers',
    description: 'Vertical use cases studios and coaches run today.',
    cards: [
      { icon: 'image', title: 'Boutique fitness studios', description: 'Class packs, intro offers, and member milestone graphics.' },
      { icon: 'brand', title: 'Yoga & pilates brands', description: 'Calm, consistent visual language across locations.' },
      { icon: 'sparkle', title: 'Personal trainers', description: 'Program promos, client progress posts, and lead magnets.' },
      { icon: 'social', title: 'Beauty & aesthetics', description: 'Treatment menus, seasonal offers, and before/after cards.' },
      { icon: 'refresh', title: 'Health coaching', description: 'Webinar graphics, challenge calendars, and nurture emails.' },
      { icon: 'globe', title: 'Franchise rollouts', description: 'Localize offers while keeping national brand locked.' },
    ],
  },
  'showcase-stacked': {
    title: 'What wellness brands ship with Lovart',
    items: [
      { media: { src: IMG.showcase1, alt: 'Class launch kit' }, title: 'Class launch kits — one brief, full promo suite', description: 'Posters, stories, email headers, and paid ads from a single program brief.', cta: { text: 'Plan a class launch', href: '' } },
      { media: { src: IMG.showcase2, alt: 'Transformation campaign' }, title: 'Transformation campaigns — credible before/after', description: 'Member stories and challenge graphics that build trust without stock clichés.', cta: { text: 'Build a challenge', href: '' } },
      { media: { src: IMG.showcase3, alt: 'Retention creative' }, title: 'Retention loops — renewals and win-backs', description: 'Milestone badges, renewal reminders, and seasonal re-engagement offers.', cta: { text: 'Design retention creative', href: '' } },
    ],
  },
  testimonial: {
    title: 'Wellness operators scaling creative with Lovart',
    testimonials: [
      { quote: 'We launched a 6-week challenge with 24 branded assets in one afternoon — our old agency quote was two weeks.', author: 'Tina R.', role: 'Owner, boutique Pilates studio' },
      { quote: 'Trainers finally post on-brand content without me reviewing every pixel.', author: 'Marcus D.', role: 'Franchise fitness operator' },
      { quote: 'Before/after cards look professional enough for paid social — membership trials up 22%.', author: 'Elena V.', role: 'Aesthetics clinic marketing lead' },
    ],
  },
  'pricing-block': {
    title: 'Plans for solo coaches and multi-location studios',
    description: 'Start free. Upgrade when campaigns go paid or multi-seat.',
  },
  faq: {
    title: 'AI Design Solution for Fitness & Wellness FAQ',
    items: [
      { question: 'Is this for gyms, studios, or solo coaches?', answer: 'All three. Lovart scales from personal trainers to multi-location franchises with Brand Kit governance.' },
      { question: 'Can we create before/after and transformation graphics?', answer: 'Yes. Wellness storylines emphasize transformation visuals and credible member-story layouts.' },
      { question: 'Do we need a designer on staff?', answer: 'No. Front-desk staff, trainers, and marketers can generate on-brand creative in plain language.' },
      { question: 'Which channels are supported?', answer: 'Instagram, TikTok, email, local paid social, print posters, and landing page heroes — with correct aspect ratios.' },
      { question: 'Multi-location brand control?', answer: 'Brand Kit locks core identity; locations can customize offers and schedules within rules.' },
      { question: 'Commercial usage for member marketing?', answer: 'Paid plans include commercial rights for assets you create. Check your plan for team seats and exports.' },
    ],
  },
  'cta-default': {
    title: 'Ready to fill classes with on-brand creative?',
    description: 'Start free — describe your next program promo on ChatCanvas.',
    buttons: [
      { text: 'Start wellness trial', action: 'openLogin', variant: 'primary' },
      { text: 'See pricing', href: '', variant: 'secondary' },
    ],
  },
}

const local = {
  'hero-journey': {
    badge: 'Local Business Solution',
    title: 'Design for every step',
    highlightedText: 'from discovery to repeat visit',
    description:
      'A local business lives on foot traffic, reviews, and referrals. Lovart keeps your menus, offers, social posts, and signage aligned from first search to loyal regular.',
    buttons: [
      { text: 'Map local customer journey', href: '', variant: 'primary' },
      { text: 'See storefront examples', href: '', variant: 'secondary' },
    ],
    journeyCards: [
      { step: '01', title: 'Get discovered', subtitle: 'Google, Maps, Instagram, and local ad creative that matches your offer.', icon: 'search' },
      { step: '02', title: 'Drive the visit', subtitle: 'Promotions, hours, menus, and event posters that convert browsers.', icon: 'pointer' },
      { step: '03', title: 'In-store experience', subtitle: 'Signage, table tents, QR menus, and staff announcement graphics.', icon: 'brand' },
      { step: '04', title: 'Collect reviews', subtitle: 'Review-request cards, thank-you inserts, and follow-up email headers.', icon: 'chat' },
      { step: '05', title: 'Bring them back', subtitle: 'Loyalty offers, seasonal campaigns, and referral reward visuals.', icon: 'refresh' },
    ],
  },
  'bento-4': {
    title: 'Four assets every local business needs weekly',
    description: 'Restaurant, salon, retail, and service shops — same workflow.',
    columns: 4,
    features: [
      { title: 'Menus & offer sheets', description: 'Daily specials, seasonal menus, and package pricing.', media: { src: IMG.bento4, alt: 'Menus' } },
      { title: 'Social & local ads', description: 'Instagram posts, story promos, and neighborhood ad variants.', media: { src: IMG.bento2, alt: 'Social ads' } },
      { title: 'In-store signage', description: 'Posters, window clings, table tents, and event boards.', media: { src: IMG.localHero, alt: 'Signage' } },
      { title: 'On-brand everything', description: 'Brand Kit so weekend staff posts still look like you.', media: { src: IMG.bento1, alt: 'Brand Kit' } },
    ],
  },
  'capability-tabs': {
    title: 'Four ways local businesses use Lovart',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      { label: 'Promote', icon: 'sparkle', content: { title: 'Run weekly offers', description: 'Happy hour, flash sales, holiday menus, and appointment specials.', media: { src: IMG.bento2, alt: 'Promote' }, points: ['Limited-time offers', 'Event posters', 'Local ad crops'] } },
      { label: 'Showcase', icon: 'image', content: { title: 'Show what you sell', description: 'Food photography style scenes, service menus, and portfolio grids.', media: { src: IMG.localHero, alt: 'Showcase' }, points: ['Product hero shots', 'Service menus', 'Before/after for salons'] } },
      { label: 'Retain', icon: 'refresh', content: { title: 'Reward repeat customers', description: 'Loyalty cards, birthday offers, and referral bonus graphics.', media: { src: IMG.bento3, alt: 'Retain' }, points: ['Stamp card designs', 'SMS promo images', 'Email headers'] } },
      { label: 'Operate', icon: 'brand', content: { title: 'Keep ops staff on-brand', description: 'Managers and owners generate updates without waiting on designers.', media: { src: IMG.bento1, alt: 'Operate' }, points: ['Hours change graphics', 'Hiring posters', 'Policy signage'] } },
    ],
  },
  'bento-2': {
    title: 'Two wins local owners care about',
    columns: 2,
    features: [
      { title: 'Same-day promo turnaround', description: 'Rainy Tuesday special live before the lunch rush.', media: { src: IMG.bento2, alt: 'Turnaround' } },
      { title: 'Professional look on a small budget', description: 'Agency-quality menus and ads without agency retainers.', media: { src: IMG.localHero, alt: 'Professional look' } },
    ],
  },
  'workflow-horizontal': {
    title: 'Local business creative in three steps',
    description: 'Fast enough for owners who also run the floor.',
    layout: 'horizontal',
    steps: [
      { step: 1, title: 'Upload your brand basics', description: 'Logo, colors, photos of your space, menu, and current offers.' },
      { step: 2, title: 'Generate this week’s assets', description: 'Social posts, flyers, signage, and email graphics in one session.' },
      { step: 3, title: 'Print, post, and iterate', description: 'Export print-ready sizes; Touch Edit when the special changes.' },
    ],
  },
  'comparison-table': {
    title: 'Lovart vs typical local business marketing',
    headers: ['Need', 'DIY Canva templates', 'Local print shop', 'Lovart Local Solution'],
    highlightColumn: 3,
    rows: [
      { feature: 'Speed for weekly specials', values: ['Hours of template hunting', '2–5 day turnaround', 'Minutes with brand memory'] },
      { feature: 'Brand consistency', values: ['Drifts per employee', 'Depends on brief quality', 'Brand Kit on every output'] },
      { feature: 'Multi-channel sizes', values: ['Manual resizing', 'Print-only focus', 'Social, print, email from one brief'] },
      { feature: 'Edit after generation', values: ['Restart layout', 'New proof cycle', 'Touch Edit and Text Edit'] },
      { feature: 'Cost vs agency', values: ['Low but inconsistent', 'Per-job fees add up', 'Flat subscription, unlimited variants'] },
    ],
  },
  'cluster-block-dense': {
    title: 'Local industries this solution fits',
    description: 'Same workflow, different vertical copy and examples.',
    cards: [
      { icon: 'image', title: 'Restaurants & cafes', description: 'Menus, daily specials, delivery promos, and event nights.' },
      { icon: 'brand', title: 'Salons & spas', description: 'Service menus, stylist spotlights, and booking promos.' },
      { icon: 'pointer', title: 'Retail storefronts', description: 'Window posters, sale signage, and product feature cards.' },
      { icon: 'globe', title: 'Real estate local', description: 'Open house flyers, listing graphics, and agent personal brand.' },
      { icon: 'chat', title: 'Home & local services', description: 'Before/after, quote graphics, and seasonal service promos.' },
      { icon: 'refresh', title: 'Community events', description: 'Farmers market booths, pop-ups, and partnership co-marketing.' },
    ],
  },
  'showcase-stacked': {
    title: 'From slow season to packed weekend',
    items: [
      { media: { src: IMG.showcase1, alt: 'Weekly promo kit' }, title: 'Weekly promo kits — specials without stress', description: 'Social, print flyer, and in-store signage from one Tuesday special brief.', cta: { text: 'Create a weekly promo', href: '' } },
      { media: { src: IMG.localHero, alt: 'Storefront campaign' }, title: 'Storefront campaigns — look open and inviting', description: 'Window posters, hours updates, and hiring signs that match your vibe.', cta: { text: 'Design storefront creative', href: '' } },
      { media: { src: IMG.showcase3, alt: 'Loyalty creative' }, title: 'Loyalty & referrals — keep regulars coming back', description: 'Stamp cards, birthday offers, and thank-you graphics that feel personal.', cta: { text: 'Build loyalty assets', href: '' } },
    ],
  },
  testimonial: {
    title: 'Local businesses marketing with Lovart',
    testimonials: [
      { quote: 'Our weekend special goes live on Instagram and the printed table tents in under an hour.', author: 'Kenji M.', role: 'Owner, neighborhood ramen bar' },
      { quote: 'I stopped paying $400 per menu redesign every season.', author: 'Sofia L.', role: 'Cafe operator' },
      { quote: 'Listing flyers and open-house posts finally match our brokerage brand.', author: 'Andre W.', role: 'Local real estate team lead' },
    ],
  },
  'pricing-block': {
    title: 'Affordable plans for owner-operators',
    description: 'Free to try. Pro when you publish weekly promos across channels.',
  },
  faq: {
    title: 'AI Design Solution for Local Business FAQ',
    items: [
      { question: 'Is this only for restaurants?', answer: 'No. Restaurants, salons, retail, services, and local real estate use the same local-business storyline.' },
      { question: 'Can I get print-ready files?', answer: 'Yes. Export sizes suitable for flyers, posters, menus, and signage — plus social crops.' },
      { question: 'Do I need design skills?', answer: 'No. Describe your special, hours, or service in plain language; Brand Kit handles visual consistency.' },
      { question: 'How fast can I update a daily special?', answer: 'Most owners generate and post within minutes using Touch Edit for price or item changes.' },
      { question: 'Multiple locations?', answer: 'Brand Kit supports shared identity with per-location offer and hours customization.' },
      { question: 'Commercial usage?', answer: 'Paid plans include commercial rights for marketing assets you create for your business.' },
    ],
  },
  'cta-default': {
    title: 'Ready to market your local business like a brand?',
    description: 'Start free — create this week’s promo on ChatCanvas.',
    buttons: [
      { text: 'Start free', action: 'openLogin', variant: 'primary' },
      { text: 'See local examples', href: '', variant: 'secondary' },
    ],
  },
}

const mission = {
  'hero-journey': {
    badge: 'Nonprofit & Mission Solution',
    title: 'Design for every step',
    highlightedText: 'from awareness to sustained impact',
    description:
      'Mission-driven organizations need trust, clarity, and urgency — on limited budgets. Lovart helps you produce campaign creative, donor materials, volunteer drives, and program stories that stay on-brand.',
    buttons: [
      { text: 'Plan a campaign', href: '', variant: 'primary' },
      { text: 'See nonprofit examples', href: '', variant: 'secondary' },
    ],
    journeyCards: [
      { step: '01', title: 'Raise awareness', subtitle: 'Social, email, and partner graphics that explain your cause clearly.', icon: 'globe' },
      { step: '02', title: 'Build trust', subtitle: 'Impact reports, transparency visuals, and program explainers.', icon: 'brand' },
      { step: '03', title: 'Drive action', subtitle: 'Donation appeals, event registrations, and volunteer signup creative.', icon: 'pointer' },
      { step: '04', title: 'Thank & retain', subtitle: 'Donor thank-you graphics, updates, and milestone celebrations.', icon: 'chat' },
      { step: '05', title: 'Scale programs', subtitle: 'Grant decks, partner kits, and localized campaign variants.', icon: 'refresh' },
    ],
  },
  'bento-4': {
    title: 'Four creative needs every mission org faces',
    description: 'Fundraising, programs, volunteers, and trust — one workflow.',
    columns: 4,
    features: [
      { title: 'Fundraising campaigns', description: 'Appeals, giving days, matched gifts, and year-end drives.', media: { src: IMG.missionHero, alt: 'Fundraising' } },
      { title: 'Program storytelling', description: 'Impact stats, beneficiary stories, and field update graphics.', media: { src: IMG.showcase1, alt: 'Storytelling' } },
      { title: 'Volunteer & event', description: 'Recruitment posters, event banners, and registration pages.', media: { src: IMG.bento2, alt: 'Volunteer' } },
      { title: 'Brand trust system', description: 'Consistent, dignified visuals across chapters and partners.', media: { src: IMG.bento1, alt: 'Brand trust' } },
    ],
  },
  'capability-tabs': {
    title: 'Four modules for mission-driven teams',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      { label: 'Fundraise', icon: 'sparkle', content: { title: 'Launch giving campaigns fast', description: 'Appeal graphics, email headers, social carousels, and landing heroes.', media: { src: IMG.missionHero, alt: 'Fundraise' }, points: ['Giving day kits', 'Matched gift banners', 'Year-end appeals'] } },
      { label: 'Educate', icon: 'search', content: { title: 'Explain complex issues clearly', description: 'Infographic-style visuals, program explainers, and FAQ graphics.', media: { src: IMG.tab1, alt: 'Educate' }, points: ['Issue explainers', 'Policy summaries', 'School program one-pagers'] } },
      { label: 'Mobilize', icon: 'globe', content: { title: 'Recruit volunteers and attendees', description: 'Event posters, signup stories, and partner co-branded assets.', media: { src: IMG.tab2, alt: 'Mobilize' }, points: ['Volunteer drives', 'Community events', 'Chapter toolkits'] } },
      { label: 'Report', icon: 'brand', content: { title: 'Show impact with dignity', description: 'Annual report visuals, donor updates, and grant presentation graphics.', media: { src: IMG.bento3, alt: 'Report' }, points: ['Impact snapshots', 'Board decks', 'Partner reports'] } },
    ],
  },
  'bento-2': {
    title: 'Two outcomes nonprofit leaders need',
    columns: 2,
    features: [
      { title: 'Campaign-ready in days, not weeks', description: 'Small teams ship full appeal kits without agency quotes.', media: { src: IMG.bento2, alt: 'Speed' } },
      { title: 'Trustworthy, consistent brand', description: 'Every chapter and volunteer post reflects your mission standards.', media: { src: IMG.bento1, alt: 'Trust' } },
    ],
  },
  'workflow-vertical': {
    title: 'Mission campaign workflow in three steps',
    description: 'Built for lean comms teams and development staff.',
    layout: 'vertical',
    steps: [
      { step: 1, title: 'Define campaign narrative', description: 'Upload brand guide, impact stats, beneficiary stories, and partner logos.', media: { src: IMG.tab1, alt: 'Narrative' } },
      { step: 2, title: 'Generate the appeal kit', description: 'Email, social, web, print, and partner assets from one campaign brief.', media: { src: IMG.missionHero, alt: 'Appeal kit' } },
      { step: 3, title: 'Localize and report impact', description: 'Chapter variants, donor thank-yous, and post-campaign impact graphics.', media: { src: IMG.showcase3, alt: 'Report' } },
    ],
  },
  'comparison-table': {
    title: 'Lovart vs typical nonprofit marketing approaches',
    headers: ['Need', 'Volunteer-made Canva', 'Agency pro bono (limited)', 'Lovart Mission Solution'],
    highlightColumn: 3,
    rows: [
      { feature: 'Campaign turnaround', values: ['Inconsistent quality', 'Weeks when available', 'Days with repeatable kits'] },
      { feature: 'Brand dignity & consistency', values: ['High variance', 'Strong but one-off', 'Brand Kit across chapters'] },
      { feature: 'Multi-channel appeal assets', values: ['Manual resizing', 'Partial coverage', 'Email, social, print, web together'] },
      { feature: 'Cost on tight budgets', values: ['Staff time hidden cost', 'Unreliable availability', 'Predictable subscription'] },
      { feature: 'Impact storytelling', values: ['Template fatigue', 'Custom but slow', 'Story + stat visuals at scale'] },
    ],
  },
  'cluster-block-dense': {
    title: 'Mission-driven scenarios this solution covers',
    description: 'Nonprofits, NGOs, schools, and community orgs.',
    cards: [
      { icon: 'sparkle', title: 'Annual & giving day campaigns', description: 'Year-end, #GivingTuesday, and emergency appeals.' },
      { icon: 'globe', title: 'NGO field programs', description: 'Localized storytelling with global brand guardrails.' },
      { icon: 'brand', title: 'Education & youth nonprofits', description: 'Enrollment drives, program flyers, and parent comms.' },
      { icon: 'chat', title: 'Community health & aid', description: 'Awareness campaigns with sensitive, dignified visuals.' },
      { icon: 'pointer', title: 'Volunteer recruitment', description: 'Posters, stories, and onboarding welcome kits.' },
      { icon: 'refresh', title: 'Donor stewardship', description: 'Thank-you graphics, impact updates, and renewal appeals.' },
    ],
  },
  'showcase-stacked': {
    title: 'Impact creative that builds trust',
    items: [
      { media: { src: IMG.missionHero, alt: 'Giving campaign' }, title: 'Giving campaigns — full appeal kits', description: 'Email hero, social carousel, donation page banner, and print insert from one brief.', cta: { text: 'Build an appeal kit', href: '' } },
      { media: { src: IMG.showcase1, alt: 'Impact story' }, title: 'Impact stories — dignity and clarity', description: 'Beneficiary stories and outcome stats without sensational stock imagery.', cta: { text: 'Tell your impact story', href: '' } },
      { media: { src: IMG.showcase3, alt: 'Volunteer drive' }, title: 'Volunteer drives — mobilize your community', description: 'Recruitment posters, event graphics, and partner co-marketing assets.', cta: { text: 'Launch a volunteer campaign', href: '' } },
    ],
  },
  testimonial: {
    title: 'Mission organizations creating with Lovart',
    testimonials: [
      { quote: 'We shipped our giving day kit in three days — last year the agency timeline was three weeks.', author: 'Hannah C.', role: 'Comms director, regional NGO' },
      { quote: 'Chapters finally share graphics that look like one organization, not twelve different brands.', author: 'David O.', role: 'Brand lead, education nonprofit' },
      { quote: 'Our volunteer recruitment posts look professional enough to compete with larger orgs.', author: 'Priya N.', role: 'Program manager, community health org' },
    ],
  },
  'pricing-block': {
    title: 'Plans for lean teams and growing chapters',
    description: 'Start free. Team plans when campaigns run year-round across staff and volunteers.',
  },
  faq: {
    title: 'AI Design Solution for Nonprofits FAQ',
    items: [
      { question: 'Is Lovart appropriate for sensitive causes?', answer: 'Yes. Mission storylines emphasize dignified storytelling and consistent brand trust — not sensational templates.' },
      { question: 'Can small comms teams use this?', answer: 'Built for lean teams. One development or comms staffer can produce full appeal kits without design training.' },
      { question: 'Multi-chapter or affiliate brands?', answer: 'Brand Kit locks core identity; chapters localize copy and offers within guidelines.' },
      { question: 'Grant and board presentation graphics?', answer: 'Generate impact snapshots, program explainers, and deck visuals from the same campaign context.' },
      { question: 'Volunteer-created content?', answer: 'Role-based access lets volunteers generate within brand guardrails — reducing off-brand posts.' },
      { question: 'Discounts for nonprofits?', answer: 'Check current pricing page for nonprofit or education programs; commercial usage included on paid plans.' },
    ],
  },
  'cta-default': {
    title: 'Ready to launch your next impact campaign?',
    description: 'Start free — build your appeal kit on ChatCanvas.',
    buttons: [
      { text: 'Start mission trial', action: 'openLogin', variant: 'primary' },
      { text: 'See campaign examples', href: '', variant: 'secondary' },
    ],
  },
}

const saas = {
  'hero-cinematic': {
    tag: 'B2B SaaS Solution',
    title: 'Ship product marketing creative at',
    highlightedText: 'release velocity',
    description:
      'Lovart helps SaaS teams produce launch kits, PLG onboarding visuals, sales decks, and in-app marketing — one agent workflow from feature brief to multi-channel rollout.',
    buttons: [
      { text: 'Build a launch kit', href: '', variant: 'primary' },
      { text: 'See SaaS examples', href: '', variant: 'secondary' },
    ],
    media: { src: IMG.saasHero, alt: 'B2B SaaS product marketing workflow in Lovart' },
  },
  'bento-4': {
    title: 'Four creative outputs every SaaS GTM team needs',
    description: 'Product launches, PLG, sales enablement, and lifecycle — one workflow.',
    columns: 4,
    features: [
      { title: 'Launch kits', description: 'Release heroes, changelog graphics, and announcement carousels.', media: { src: IMG.bento2, alt: 'Launch kits' } },
      { title: 'PLG onboarding', description: 'Empty states, upgrade prompts, and activation email headers.', media: { src: IMG.tab2, alt: 'PLG onboarding' } },
      { title: 'Sales enablement', description: 'One-pagers, deck visuals, and competitive battlecards.', media: { src: IMG.bento1, alt: 'Sales enablement' } },
      { title: 'Brand Kit governance', description: 'Product, marketing, and CS stay on-brand across exports.', media: { src: IMG.bento4, alt: 'Brand Kit' } },
    ],
  },
  'capability-tabs': {
    title: 'Four modules in the SaaS creative solution',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      { label: 'Launch', icon: 'sparkle', content: { title: 'Ship release creative fast', description: 'Feature brief → launch page heroes, social, email, and in-app banners.', media: { src: IMG.saasHero, alt: 'Launch' }, points: ['Release notes visuals', 'Product Hunt kits', 'Webinar promo suites'] } },
      { label: 'PLG', icon: 'pointer', content: { title: 'Drive activation and upgrade', description: 'Onboarding illustrations, upgrade modals, and lifecycle email headers.', media: { src: IMG.tab2, alt: 'PLG' }, points: ['Activation flows', 'Trial expiry creative', 'Feature adoption nudges'] } },
      { label: 'Sales', icon: 'brand', content: { title: 'Equip reps with on-brand assets', description: 'Battlecards, one-pagers, and demo deck visuals from product context.', media: { src: IMG.tab1, alt: 'Sales' }, points: ['Competitive visuals', 'ROI one-pagers', 'Partner co-marketing'] } },
      { label: 'Scale', icon: 'globe', content: { title: 'Localize without rebuilding', description: 'Market-specific offers and compliance-friendly variants from one brief.', media: { src: IMG.tab3, alt: 'Scale' }, points: ['Regional landing pages', 'Localized ads', 'Enterprise procurement decks'] } },
    ],
  },
  'bento-2': {
    title: 'Two outcomes SaaS leaders measure',
    columns: 2,
    features: [
      { title: 'Faster release cycles', description: 'Marketing no longer blocks product launches on design queue time.', media: { src: IMG.bento2, alt: 'Release velocity' } },
      { title: 'Consistent product story', description: 'Launch, sales, and lifecycle assets tell the same value prop.', media: { src: IMG.bento1, alt: 'Consistent story' } },
    ],
  },
  'workflow-vertical': {
    title: 'SaaS GTM creative workflow in three steps',
    description: 'From feature brief to multi-channel launch kit.',
    layout: 'vertical',
    steps: [
      { step: 1, title: 'Upload product and GTM context', description: 'Feature specs, brand guide, competitor pages, ICP, and channel sizes.', media: { src: IMG.tab1, alt: 'Upload context' } },
      { step: 2, title: 'Generate the launch asset set', description: 'Web heroes, ads, email, in-app, and sales one-pagers from one brief.', media: { src: IMG.saasHero, alt: 'Generate assets' } },
      { step: 3, title: 'Iterate and localize', description: 'Touch Edit offer copy; roll out regional and segment variants.', media: { src: IMG.showcase2, alt: 'Iterate' } },
    ],
  },
  'comparison-table': {
    title: 'Lovart vs typical SaaS marketing workflows',
    headers: ['Need', 'Generic AI image tool', 'Agency + in-house hybrid', 'Lovart SaaS Solution'],
    highlightColumn: 3,
    rows: [
      { feature: 'Start from product context', values: ['One-off prompts', 'Brief cycles + handoffs', 'Feature, ICP, and URLs in one agent brief'] },
      { feature: 'Full launch kit coverage', values: ['Single assets', 'Partial channel coverage', 'Web, ads, email, in-app, sales together'] },
      { feature: 'Edit after generation', values: ['Regenerate', 'Manual Figma edits', 'Touch Edit, Text Edit, Edit Elements'] },
      { feature: 'Cross-team brand control', values: ['Inconsistent', 'Guidelines + QA backlog', 'Brand Kit across PMM, design, sales'] },
      { feature: 'PLG + sales alignment', values: ['Siloed tools', 'Separate vendors', 'One workflow for activation and enablement'] },
    ],
  },
  'cluster-block-dense': {
    title: 'SaaS scenarios this solution covers',
    description: 'B2B product marketing, PLG, and sales-led GTM.',
    cards: [
      { icon: 'sparkle', title: 'Feature launches', description: 'Release heroes, changelog graphics, and launch email suites.' },
      { icon: 'pointer', title: 'PLG growth', description: 'Onboarding, activation, and upgrade creative at experiment speed.' },
      { icon: 'brand', title: 'Sales enablement', description: 'Battlecards, one-pagers, and demo deck visuals.' },
      { icon: 'globe', title: 'Market expansion', description: 'Localized landing pages and regional ad variants.' },
      { icon: 'flask', title: 'A/B at GTM speed', description: 'Headline and hero variants without design tickets.' },
      { icon: 'refresh', title: 'Lifecycle marketing', description: 'Renewal, expansion, and win-back campaign kits.' },
    ],
  },
  'showcase-stacked': {
    title: 'From feature brief to full GTM rollout',
    items: [
      { media: { src: IMG.showcase1, alt: 'Launch kit' }, title: 'Launch kits — one brief, every channel', description: 'Web hero, social carousel, email header, and in-app banner from a single release brief.', cta: { text: 'Plan a launch', href: '' } },
      { media: { src: IMG.showcase2, alt: 'PLG creative' }, title: 'PLG creative — activation without design queue', description: 'Onboarding illustrations and upgrade prompts that match your product UI story.', cta: { text: 'Build PLG assets', href: '' } },
      { media: { src: IMG.showcase3, alt: 'Sales enablement' }, title: 'Sales enablement — reps ship on-brand', description: 'One-pagers and battlecard visuals grounded in live product positioning.', cta: { text: 'Create sales assets', href: '' } },
    ],
  },
  'review-grid-3col': {
    title: 'What changes when SaaS teams work with an agent',
    columns: 3,
    reviews: [
      { title: 'Launches stopped waiting on design', body: 'We shipped a full release kit the same week the feature froze — not three sprints later.', author: 'Jordan Lee', role: 'PMM Lead, devtools SaaS' },
      { title: 'PLG and sales finally matched', body: 'Activation emails and sales one-pagers pulled from the same product brief.', author: 'Priya Shah', role: 'Head of Growth' },
      { title: 'Localization scaled', body: 'Three regional landing variants in one session — copy and visuals stayed aligned.', author: 'Marco Alvarez', role: 'Global Marketing Manager' },
      { title: 'Experiment velocity up', body: 'Hero and headline tests weekly without filing design tickets.', author: 'Emily Tran', role: 'Demand Gen' },
      { title: 'Brand Kit saved us from drift', body: 'CS, PMM, and agency contractors all export within guardrails.', author: 'Chris Park', role: 'Brand Design Lead' },
      { title: 'Sales decks look product-native', body: 'Battlecard visuals updated the day positioning changed.', author: 'Nina Okonkwo', role: 'Sales Enablement' },
    ],
  },
  'pricing-block': {
    title: 'Plans for startup GTM and enterprise marketing orgs',
    description: 'Start free. Team plans when launches run multi-seat across PMM, design, and sales.',
  },
  faq: {
    title: 'AI Design Solution for B2B SaaS FAQ',
    items: [
      { question: 'Is this for PLG, sales-led, or both?', answer: 'Both. The SaaS storyline covers launch, PLG activation, sales enablement, and lifecycle from one agent workflow.' },
      { question: 'What should we upload first?', answer: 'Feature brief, brand guide, product screenshots, ICP notes, competitor URLs, and target channel sizes.' },
      { question: 'Can we generate in-app and email assets together?', answer: 'Yes — one brief can produce web heroes, email headers, in-app banners, and social variants.' },
      { question: 'How does Brand Kit help cross-functional teams?', answer: 'PMM, design, CS, and agencies generate within the same color, type, and logo rules.' },
      { question: 'Enterprise governance?', answer: 'For SSO, multi-region, and procurement-led teams, pair with solution-p-enterprise storyline and enterprise plan features.' },
      { question: 'Commercial usage?', answer: 'Paid plans include commercial rights for marketing assets you create. Check your plan for team seats.' },
    ],
  },
  'cta-default': {
    title: 'Ready to ship your next release with full GTM creative?',
    description: 'Start free — paste your feature brief on ChatCanvas.',
    buttons: [
      { text: 'Start SaaS trial', action: 'openLogin', variant: 'primary' },
      { text: 'See launch examples', href: '', variant: 'secondary' },
    ],
  },
}

const creator = {
  'hero-gallery': {
    badge: 'Creator Economy Solution',
    title: 'Start anywhere in your content stack,',
    highlightedText: 'keep one agent context',
    description:
      'YouTubers, podcasters, newsletter writers, and personal brands need thumbnails, episode art, carousels, and sponsor kits — Lovart keeps every format on-brand in one workflow.',
    buttons: [
      { text: 'Build your creator kit', href: '', variant: 'primary' },
      { text: 'See format examples', href: '', variant: 'secondary' },
    ],
    toolTiles: [
      { label: 'Video thumbnails', sublabel: 'YouTube, Shorts, course promos', media: { src: IMG.showcase1, alt: 'Video thumbnails' } },
      { label: 'Podcast & audio', sublabel: 'Cover art, audiograms, guests', media: { src: IMG.showcase2, alt: 'Podcast art' } },
      { label: 'Newsletter & blog', sublabel: 'Headers, hero images, lead magnets', media: { src: IMG.bento2, alt: 'Newsletter headers' } },
      { label: 'Social carousels', sublabel: 'Instagram, LinkedIn, Threads', media: { src: IMG.bento3, alt: 'Social carousels' } },
      { label: 'Sponsor & media kits', sublabel: 'Rate cards, one-pagers, decks', media: { src: IMG.bento1, alt: 'Media kits' } },
      { label: 'Merch & community', sublabel: 'Drop graphics, event banners', media: { src: IMG.creatorHero, alt: 'Community assets' } },
    ],
  },
  'bento-4': {
    title: 'Four creative jobs every creator business runs',
    description: 'Publish, grow, monetize, and stay on-brand — without a design retainer.',
    columns: 4,
    features: [
      { title: 'Publish faster', description: 'Thumbnails, episode art, and newsletter headers per release.', media: { src: IMG.showcase1, alt: 'Publish' } },
      { title: 'Grow across platforms', description: 'Resize and reframe for YouTube, TikTok, LinkedIn, and email.', media: { src: IMG.bento3, alt: 'Grow' } },
      { title: 'Monetize professionally', description: 'Sponsor kits, media decks, and course launch creative.', media: { src: IMG.bento2, alt: 'Monetize' } },
      { title: 'Brand Kit for your IP', description: 'Lock colors, type, and avatar style across every format.', media: { src: IMG.bento4, alt: 'Brand Kit' } },
    ],
  },
  'capability-tabs': {
    title: 'Four modules for creator-led businesses',
    description: '',
    autoplayIntervalMs: 0,
    tabs: [
      { label: 'Publish', icon: 'image', content: { title: 'Ship every release on time', description: 'Thumbnails, episode covers, newsletter heroes, and community posts.', media: { src: IMG.creatorHero, alt: 'Publish' }, points: ['YouTube thumbnails', 'Podcast cover art', 'Newsletter headers'] } },
      { label: 'Grow', icon: 'social', content: { title: 'Repurpose without starting over', description: 'Turn one brief into carousels, shorts covers, and quote cards.', media: { src: IMG.tab2, alt: 'Grow' }, points: ['Carousel suites', 'Clip covers', 'Quote graphics'] } },
      { label: 'Monetize', icon: 'sparkle', content: { title: 'Look credible to sponsors', description: 'Media kits, sponsor one-pagers, and course launch suites.', media: { src: IMG.tab1, alt: 'Monetize' }, points: ['Rate card visuals', 'Sponsor mockups', 'Launch landing heroes'] } },
      { label: 'Brand', icon: 'brand', content: { title: 'Personal IP that scales', description: 'Brand Kit keeps editors and VAs inside your visual identity.', media: { src: IMG.bento1, alt: 'Brand' }, points: ['Avatar + color rules', 'Series templates', 'Editor handoff'] } },
    ],
  },
  'bento-2': {
    title: 'Two outcomes creators optimize for',
    columns: 2,
    features: [
      { title: 'More output per release', description: 'One recording session → full promo suite same day.', media: { src: IMG.showcase2, alt: 'Output' } },
      { title: 'Sponsor-ready presentation', description: 'Media kits that look agency-made, not template-made.', media: { src: IMG.bento2, alt: 'Sponsor ready' } },
    ],
  },
  'workflow-horizontal': {
    title: 'Creator production workflow in three steps',
    description: 'From episode brief to multi-platform promo kit.',
    layout: 'horizontal',
    steps: [
      { step: 1, title: 'Set up creator Brand Kit', description: 'Upload logo, colors, avatar style, and series naming rules.', media: { src: IMG.bento1, alt: 'Brand Kit' } },
      { step: 2, title: 'Generate the release kit', description: 'Thumbnail, episode art, carousels, and email header from one brief.', media: { src: IMG.creatorHero, alt: 'Generate' } },
      { step: 3, title: 'Repurpose and publish', description: 'Touch Edit titles; export platform-specific sizes and sponsor variants.', media: { src: IMG.showcase3, alt: 'Publish' } },
    ],
  },
  'comparison-table': {
    title: 'Lovart vs typical creator design workflows',
    headers: ['Need', 'Canva templates', 'Freelance designer', 'Lovart Creator Solution'],
    highlightColumn: 3,
    rows: [
      { feature: 'Per-release turnaround', values: ['DIY time cost', 'Days to weeks', 'Same-day multi-format kits'] },
      { feature: 'Cross-platform consistency', values: ['Template drift', 'Strong but expensive', 'Brand Kit across formats'] },
      { feature: 'Repurpose from one brief', values: ['Manual resize', 'Extra scope fees', 'Agent keeps episode context'] },
      { feature: 'Sponsor-ready quality', values: ['Generic', 'High but slow', 'Media kits at publish speed'] },
      { feature: 'Edit after generation', values: ['Layer hunting', 'Revision rounds', 'Touch Edit and Text Edit in place'] },
    ],
  },
  'cluster-block-dense': {
    title: 'Creator scenarios this solution covers',
    description: 'YouTube, podcast, newsletter, and personal brand businesses.',
    cards: [
      { icon: 'image', title: 'YouTube & video creators', description: 'Thumbnails, banners, end screens, and course promos.' },
      { icon: 'chat', title: 'Podcasters & audio shows', description: 'Cover art, guest promo kits, and audiogram frames.' },
      { icon: 'globe', title: 'Newsletter writers', description: 'Headers, lead magnets, and sponsorship graphics.' },
      { icon: 'social', title: 'Social-first creators', description: 'Carousels, quote cards, and launch countdown suites.' },
      { icon: 'sparkle', title: 'Course & cohort launches', description: 'Enrollment pages, webinar promos, and student onboarding.' },
      { icon: 'brand', title: 'Personal brand consultants', description: 'LinkedIn authority content and speaking one-pagers.' },
    ],
  },
  'showcase-horizontal': {
    title: 'Creator formats you can ship from one brief',
    items: [
      { media: { src: IMG.showcase1, alt: 'YouTube kit' }, title: 'YouTube release kits', description: 'Thumbnail, banner, community post, and shorts cover tied to one episode brief.', cta: { text: 'Build a video kit', href: '' } },
      { media: { src: IMG.showcase2, alt: 'Podcast kit' }, title: 'Podcast episode suites', description: 'Cover art, guest promo cards, and newsletter header for every drop.', cta: { text: 'Design episode art', href: '' } },
      { media: { src: IMG.showcase3, alt: 'Sponsor kit' }, title: 'Sponsor & media kits', description: 'Rate cards and one-pagers that look credible to brand partners.', cta: { text: 'Create a media kit', href: '' } },
    ],
  },
  testimonial: {
    title: 'Creators scaling output with Lovart',
    testimonials: [
      { quote: 'I publish twice a week now — thumbnail, carousel, and newsletter header ship before I finish editing.', author: 'Alex Kim', role: 'Tech YouTuber, 180K subs' },
      { quote: 'My podcast cover and guest promo kit used to take a freelancer three days. Now it is same afternoon.', author: 'Rachel M.', role: 'Interview podcast host' },
      { quote: 'Sponsors stopped asking if I had a real media kit — the deck looks agency-grade.', author: 'Devon S.', role: 'Newsletter creator' },
    ],
  },
  'pricing-block': {
    title: 'Plans for solo creators and small media teams',
    description: 'Start free. Upgrade when you run paid promos, courses, or multi-editor workflows.',
  },
  faq: {
    title: 'AI Design Solution for Creators FAQ',
    items: [
      { question: 'Is this only for YouTubers?', answer: 'No. The creator storyline covers video, podcast, newsletter, social, courses, and personal brand IP.' },
      { question: 'Can my editor or VA use Brand Kit?', answer: 'Yes. Role-based access lets collaborators generate inside your visual rules.' },
      { question: 'Platform-specific sizes?', answer: 'Export YouTube thumbnails, podcast square art, LinkedIn carousels, Instagram stories, and email headers from one brief.' },
      { question: 'Sponsor and media kits?', answer: 'Generate rate card visuals, one-pagers, and deck graphics that match your channel brand.' },
      { question: 'Edit thumbnails without regenerating?', answer: 'Touch Edit and Text Edit let you fix titles, faces, and backgrounds in place.' },
      { question: 'Commercial usage for sponsored content?', answer: 'Paid plans include commercial rights for assets you create. Check your plan for export limits.' },
    ],
  },
  'cta-default': {
    title: 'Ready to ship your next release with a full promo kit?',
    description: 'Start free — describe your next episode or launch on ChatCanvas.',
    buttons: [
      { text: 'Start creator trial', action: 'openLogin', variant: 'primary' },
      { text: 'See format gallery', href: '', variant: 'secondary' },
    ],
  },
}

const pages = [
  {
    file: 'ai-design-for-fitness-wellness-hub-en.json',
    slug: 'ai-design-for-fitness-wellness-hub',
    title: 'AI Design Solution for Fitness & Wellness',
    description:
      'Produce class promos, member campaigns, transformation graphics, and social content for gyms, studios, coaches, and beauty brands — on-brand without a design team.',
    keywords: ['ai design fitness', 'wellness marketing creative', 'gym promo design', 'lovart wellness'],
    ogImage: IMG.wellnessHero,
    storyline: 'solution-i-wellness',
    sectionsByType: wellness,
  },
  {
    file: 'ai-design-for-small-business-hub-en.json',
    slug: 'ai-design-for-small-business-hub',
    title: 'AI Design Solution for Local Business',
    description:
      'Menus, weekly specials, social posts, signage, and loyalty creative for restaurants, salons, retail, and local services — same-day turnaround on a small budget.',
    keywords: ['ai design local business', 'restaurant menu design ai', 'small business marketing', 'lovart local'],
    ogImage: IMG.localHero,
    storyline: 'solution-i-local',
    sectionsByType: local,
  },
  {
    file: 'ai-design-solution-for-nonprofits-en.json',
    slug: 'ai-design-solution-for-nonprofits',
    title: 'AI Design Solution for Nonprofits',
    description:
      'Fundraising appeals, impact stories, volunteer drives, and donor materials for NGOs and mission-driven orgs — trustworthy creative on a lean budget.',
    keywords: ['ai design nonprofit', 'fundraising creative ai', 'ngo marketing design', 'lovart nonprofit'],
    ogImage: IMG.missionHero,
    storyline: 'solution-i-mission',
    sectionsByType: mission,
  },
  {
    file: 'ai-design-solution-for-saas-en.json',
    slug: 'ai-design-solution-for-saas',
    title: 'AI Design Solution for B2B SaaS',
    description:
      'Ship launch kits, PLG onboarding visuals, sales enablement, and lifecycle campaigns — one agent workflow for product marketing and growth teams.',
    keywords: ['ai design saas', 'b2b product marketing creative', 'plg design workflow', 'lovart saas'],
    ogImage: IMG.saasHero,
    storyline: 'solution-i-saas',
    sectionsByType: saas,
  },
  {
    file: 'ai-design-solution-for-creators-en.json',
    slug: 'ai-design-solution-for-creators',
    title: 'AI Design Solution for Creators',
    description:
      'Thumbnails, podcast art, newsletter headers, carousels, and sponsor kits for YouTubers, podcasters, and personal brands — on-brand without a design retainer.',
    keywords: ['ai design creators', 'youtube thumbnail ai', 'podcast cover design', 'lovart creators'],
    ogImage: IMG.creatorHero,
    storyline: 'solution-i-creator',
    sectionsByType: creator,
  },
]

const outDir = path.join(__dirname, 'en')
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true })

for (const p of pages) {
  const doc = buildPage(p)
  const expected = STORYLINES.storylines[p.storyline].sections
  const actual = doc.section.map((s) => s.type)
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`Section mismatch for ${p.slug}\nexpected: ${expected.join(' → ')}\nactual:   ${actual.join(' → ')}`)
  }
  const outPath = path.join(outDir, p.file)
  fs.writeFileSync(outPath, JSON.stringify(doc, null, 2) + '\n')
  console.log(`Wrote ${outPath} [${p.storyline}]`)
}

// Update coverage matrix in solution-storylines-v2.json
const ssotPath = path.join(__dirname, 'solution-storylines-v2.json')
const ssot = JSON.parse(fs.readFileSync(ssotPath, 'utf8'))
for (const [id, slug] of [
  ['solution-i-ecommerce', 'ai-design-solution-for-shopify'],
  ['solution-i-wellness', 'ai-design-for-fitness-wellness-hub'],
  ['solution-i-local', 'ai-design-for-small-business-hub'],
  ['solution-i-mission', 'ai-design-solution-for-nonprofits'],
  ['solution-i-saas', 'ai-design-solution-for-saas'],
  ['solution-i-creator', 'ai-design-solution-for-creators'],
]) {
  ssot.coverageMatrix.industry[id] = { status: 'example', slug }
}
ssot.gapBacklog.industry = []
ssot.contentStrategyMapping['ai-design-solution-for-saas'] = 'solution-i-saas'
ssot.contentStrategyMapping['ai-design-solution-for-creators'] = 'solution-i-creator'
fs.writeFileSync(ssotPath, JSON.stringify(ssot, null, 2) + '\n')
console.log('Updated solution-storylines-v2.json coverage (industry 6/6)')
