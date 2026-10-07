/**
 * Unified page copy rules.
 *
 * Single source of truth for landing / page copy preflight. Copy requirements are
 * DERIVED from the storyline SSOTs, not hardcoded here:
 *   - landing-storylines.json      (per-storyline `copy` block)
 *   - solution-storylines.json     (file-level `copyDefault`)
 *   - scenarios-storylines.json    (file-level `copyDefault`)
 *   - page-copy-bindings.json      (feature/tool/product/topic `copyDefault`)
 *
 * The exported function names are kept backward-compatible with the previous
 * landing-only implementation so existing generators keep working.
 */

const fs = require('fs');
const path = require('path');

const REFRESH = path.resolve(__dirname, '..', '..');

const SSOT_FILES = {
  landing: path.join(REFRESH, 'landing-storylines.json'),
  solution: path.join(REFRESH, 'solution-storylines.json'),
  scenario: path.join(REFRESH, 'scenarios-storylines.json'),
  page: path.join(REFRESH, 'page-copy-bindings.json'),
};

const INPUT_CUES = [
  'prompt', 'brief', 'product url', 'url', 'image', 'script', 'reference', 'brand kit', 'upload',
];

const OUTPUT_CUES = [
  'logo', 'visual', 'video', 'commercial', 'brand kit', 'campaign', 'mockup', 'carousel',
  'assets', 'exports', 'cuts', 'layout', 'poster', 'design',
];

const EDIT_CUES = [
  'chatcanvas', 'touch edit', 'text edit', 'edit', 'refine', 'review', 'variant',
];

const RISK_CUES = [
  'start free', 'free', 'no credit card', 'commercial-ready', 'commercial', 'without resetting',
  'without switching', 'brand-safe', 'export-ready', 'editable',
];

const BANNED_PHRASES = [
  'revolutionize', 'game-changer', 'streamline', 'empower', 'seamless', 'unlock',
];

const HERO_CUE_MAP = {
  input: INPUT_CUES,
  output: OUTPUT_CUES,
  editPath: EDIT_CUES,
  riskReducer: RISK_CUES,
};

let REGISTRY = null;

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function buildRegistry() {
  if (REGISTRY) return REGISTRY;
  const byStoryline = {};
  let intentCrosswalk = {};
  let masterIntents = [];

  // landing: per-storyline copy blocks
  const landing = readJson(SSOT_FILES.landing);
  intentCrosswalk = { ...landing.intentCrosswalk };
  for (const [id, meta] of Object.entries(landing.storylines || {})) {
    byStoryline[id] = {
      pageType: 'landing',
      intent: meta.intent,
      heroType: meta.copy?.heroType || (meta.sections && meta.sections[0]) || null,
      ...(meta.copy || {}),
    };
  }
  for (const [alias, target] of Object.entries(landing.legacyAliases || {})) {
    if (byStoryline[target]) byStoryline[alias] = byStoryline[target];
  }

  // solution + scenario: file-level copyDefault applies to all storylines in file
  for (const key of ['solution', 'scenario']) {
    const doc = readJson(SSOT_FILES[key]);
    const def = doc.copyDefault || {};
    for (const [id, meta] of Object.entries(doc.storylines || {})) {
      byStoryline[id] = {
        pageType: key,
        intent: def.intent,
        heroType: (meta.sections && meta.sections[0]) || null,
        ...def,
      };
    }
    for (const [alias, target] of Object.entries(doc.aliases || {})) {
      if (byStoryline[target]) byStoryline[alias] = byStoryline[target];
    }
  }

  // feature / tool / product / topic: page-copy-bindings.json
  const page = readJson(SSOT_FILES.page);
  masterIntents = page.masterIntents || [];
  intentCrosswalk = { ...intentCrosswalk, ...(page.intentCrosswalk || {}) };
  for (const [pageType, block] of Object.entries(page.pageTypes || {})) {
    const def = block.copyDefault || {};
    for (const id of block.storylines || []) {
      byStoryline[id] = { pageType, intent: def.intent, ...def };
    }
  }

  REGISTRY = { byStoryline, intentCrosswalk, masterIntents };
  return REGISTRY;
}

function getCopyBinding(storyline) {
  if (!storyline) return null;
  return buildRegistry().byStoryline[storyline] || null;
}

function includesAny(text, cues) {
  const haystack = String(text || '').toLowerCase();
  return cues.some((cue) => haystack.includes(cue));
}

function dedupeFaq(items) {
  const seen = new Set();
  return items.filter((item) => {
    const key = `${item.question}::${item.answer}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function strengthenHeroDescription(description, options = {}) {
  const {
    input = 'Start from a prompt, brief, product URL or reference image.',
    output = 'Generate campaign-ready visuals, videos and brand assets.',
    edit = 'Refine winners with ChatCanvas, Touch Edit and Text Edit.',
    risk = 'Start free and keep brand context across every output.',
  } = options;

  let text = String(description || '').trim();
  if (!text) text = `${input} ${output}`;
  if (!includesAny(text, INPUT_CUES)) text = `${text} ${input}`.trim();
  if (!includesAny(text, OUTPUT_CUES)) text = `${text} ${output}`.trim();
  if (!includesAny(text, EDIT_CUES)) text = `${text} ${edit}`.trim();
  if (!includesAny(text, RISK_CUES)) text = `${text} ${risk}`.trim();
  return text.replace(/\s+/g, ' ').trim();
}

function buildPromptLauncherBlock(keyword, prompts = []) {
  return {
    title: `Try ${String(keyword || 'the workflow').toLowerCase()} from a real brief`,
    description:
      `Start with a prompt, brief, product URL or reference image. Generate ${String(keyword || 'campaign')} outputs, refine them on ChatCanvas, and export the winning variants.`,
    prompts,
    cta: { text: keyword ? `Try ${keyword} now` : 'Try the workflow now' },
    tip: 'Start free — no credit card required.',
  };
}

/**
 * Resolve the CTA copy variant. Accepts an explicit variant, or a storyline id
 * (preferred) so the CTA style is derived from the storyline's copy binding.
 */
function resolveCtaStyle({ variant, storyline } = {}) {
  if (variant) return variant;
  const binding = getCopyBinding(storyline);
  return binding?.ctaStyle || 'default';
}

function buildCtaSection(keyword, variantOrOpts = 'default') {
  const style =
    typeof variantOrOpts === 'string'
      ? variantOrOpts
      : resolveCtaStyle(variantOrOpts);
  const kw = String(keyword || 'the workflow').toLowerCase();

  if (style === 'offer') {
    return {
      title: 'Claim the plan that fits your next campaign push',
      description: `Start free, then upgrade when ${kw} moves into live production and commercial delivery.`,
    };
  }
  if (style === 'compare') {
    return {
      title: `Ready to compare ${kw} side by side?`,
      description: 'See how Lovart keeps brief, edits and brand context together before you switch.',
    };
  }
  if (style === 'brand') {
    return {
      title: `Bring ${kw} into a brand system your team can trust`,
      description: 'See real examples and workflow before you commit — Lovart keeps every campaign on-model.',
    };
  }
  if (style === 'solution') {
    return {
      title: `See how ${kw} replaces your fragmented creative stack`,
      description: 'Walk through the team workflow, governance and delivery — then start a pilot.',
    };
  }
  if (style === 'educate') {
    return {
      title: `Put ${kw} to work in a real project`,
      description: 'Start from a brief, generate the first output, then refine and export without switching tools.',
    };
  }
  return {
    title: `Ready to use ${kw} in a real workflow?`,
    description: 'Start from a real brief, generate the first output, then refine and export without leaving ChatCanvas.',
  };
}

function mergeFaqItems(existingItems, leadItem) {
  const defaults = [
    {
      question: 'Can I edit the output after generation?',
      answer:
        'Yes. Lovart keeps generation and editing in the same workflow with ChatCanvas, Touch Edit and Text Edit, so teams can refine without restarting from scratch.',
    },
    {
      question: 'Is this suitable for commercial work?',
      answer:
        'Use the page-specific proof, export and rights guidance on the page. If a commercial detail is not verified, mark it `[待考证]` instead of guessing.',
    },
    {
      question: 'What inputs should I prepare first?',
      answer:
        'The strongest starts are a clear brief plus one or more of these: product URL, reference image, script, brand kit or existing campaign assets.',
    },
  ];

  return dedupeFaq([leadItem, ...(existingItems || []), ...defaults]).slice(0, 6);
}

function collectText(node) {
  if (!node) return '';
  if (typeof node === 'string') return node;
  if (Array.isArray(node)) return node.map(collectText).join(' ');
  if (typeof node === 'object') return Object.values(node).map(collectText).join(' ');
  return '';
}

/**
 * Storyline-driven copy preflight.
 *
 * Requirements are derived from the storyline's resolved copy binding when a
 * storyline id is known. `requirePromptLauncher` is still accepted for backward
 * compatibility, but the binding's `requiredSections` is the primary source.
 */
function validateLandingCopyPreflight({
  title,
  description,
  bodyJson,
  storyline,
  requirePromptLauncher = false,
}) {
  const sections = typeof bodyJson === 'string' ? JSON.parse(bodyJson) : bodyJson;
  const errors = [];
  const warnings = [];
  const binding = getCopyBinding(storyline);

  const types = sections.map((s) => String(s.type || ''));
  const hero = sections.find((section) => String(section.type || '').startsWith('hero-'));
  const faq = sections.find((section) => section.type === 'faq');
  const cta = sections.find((section) => section.type === 'cta-default');

  const proofTypeSet = new Set(
    binding?.proofTypes && binding.proofTypes.length
      ? binding.proofTypes
      : [
          'comparison-table',
          'comparison-before-after',
          'testimonial',
          'review-grid-3col',
          'review-grid-4col',
          'pricing-block',
          'feature-detail',
        ],
  );
  const hasProof = types.some((t) => proofTypeSet.has(t));

  // Hero copy dimensions: default to input+output; storyline binding can widen/narrow.
  const heroMust = binding?.heroMust && binding.heroMust.length
    ? binding.heroMust
    : ['input', 'output'];

  if (!hero) {
    errors.push('Missing hero section.');
  } else {
    const heroText = collectText([hero.badge, hero.title, hero.highlightedText, hero.description]);
    for (const dim of heroMust) {
      const cues = HERO_CUE_MAP[dim];
      if (!cues) continue; // subject/buyer/proof are editorial, not keyword-checkable
      const missing = !includesAny(heroText, cues);
      if (!missing) continue;
      // input/output are blocking; editPath/riskReducer are warnings
      if (dim === 'input' || dim === 'output') {
        errors.push(`Hero copy missing clear ${dim} cue.`);
      } else {
        warnings.push(`Hero copy missing ${dim} cue.`);
      }
    }
  }

  if (!hasProof) errors.push('Body lacks strong proof section.');
  if (!faq || !Array.isArray(faq.items) || faq.items.length < 3) {
    errors.push('FAQ must contain at least 3 items.');
  }
  if (!cta) errors.push('Missing bottom CTA section.');

  // Storyline-required structural anchors (drives copy that depends on them).
  const requiredSections = new Set(binding?.requiredSections || []);
  if (requirePromptLauncher) requiredSections.add('prompt-launcher');
  for (const required of requiredSections) {
    if (!types.includes(required)) {
      errors.push(`Storyline ${storyline || '(unknown)'} requires section: ${required}.`);
    }
  }

  const pageText = collectText([title, description, sections]);
  BANNED_PHRASES.forEach((phrase) => {
    if (pageText.toLowerCase().includes(phrase)) {
      warnings.push(`Contains banned phrase candidate: ${phrase}`);
    }
  });

  return {
    errors,
    warnings,
    binding: binding
      ? {
          pageType: binding.pageType,
          intent: binding.intent,
          ctaStyle: binding.ctaStyle,
          benchmarkPool: binding.benchmarkPool,
        }
      : null,
    summary: {
      storyline: storyline || null,
      hero: hero?.type || null,
      proofPresent: hasProof,
      faqCount: faq?.items?.length || 0,
      ctaPresent: Boolean(cta),
      requiredSections: [...requiredSections],
    },
  };
}

module.exports = {
  buildCtaSection,
  buildPromptLauncherBlock,
  mergeFaqItems,
  strengthenHeroDescription,
  validateLandingCopyPreflight,
  // unified additions
  getCopyBinding,
  resolveCtaStyle,
  buildRegistry,
};
