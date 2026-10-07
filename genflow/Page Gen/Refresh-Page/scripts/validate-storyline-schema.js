#!/usr/bin/env node
/**
 * Validate storyline governance schema.
 *
 * This is intentionally dependency-free. It checks that the storyline SSOTs and
 * copy bindings stay aligned before page generation expands further.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

const FILES = {
  landing: path.join(ROOT, 'landing-storylines.json'),
  solution: path.join(ROOT, 'solution-storylines.json'),
  scenario: path.join(ROOT, 'scenarios-storylines.json'),
  pageBindings: path.join(ROOT, 'page-copy-bindings.json'),
};

const COPY_BINDING_REQUIRED = [
  'intent',
  'copyIntentAliases',
  'heroMust',
  'requiredSections',
  'proofTypes',
  'ctaStyle',
  'faqFocus',
  'benchmarkPool',
];

const CTA_STYLES = new Set([
  'trial',
  'compare',
  'offer',
  'brand',
  'educate',
  'solution',
  'default',
]);

const DIMENSIONS = new Set([
  'copy',
  'modules',
  'personalization',
  'imagery',
  'cro',
  'qa',
]);

const BENCHMARK_POOLS = new Set([
  'landing',
  'solution',
  'scenario',
  'feature',
  'tool',
  'product',
  'topic',
]);

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    throw new Error(`Invalid JSON: ${path.relative(ROOT, file)} — ${error.message}`);
  }
}

function validateArray(ctx, value, errors, { allowEmpty = false } = {}) {
  if (!Array.isArray(value)) {
    errors.push(`${ctx} must be an array.`);
    return;
  }
  if (!allowEmpty && value.length === 0) {
    errors.push(`${ctx} must not be empty.`);
  }
}

function validateCopyBinding(ctx, binding, { masterIntents, errors }) {
  if (!binding || typeof binding !== 'object' || Array.isArray(binding)) {
    errors.push(`${ctx} must be an object.`);
    return;
  }

  for (const key of COPY_BINDING_REQUIRED) {
    if (!(key in binding)) errors.push(`${ctx}.${key} is required.`);
  }

  if (binding.intent && !masterIntents.has(binding.intent)) {
    errors.push(`${ctx}.intent "${binding.intent}" is not in masterIntents.`);
  }
  validateArray(`${ctx}.copyIntentAliases`, binding.copyIntentAliases, errors);
  validateArray(`${ctx}.heroMust`, binding.heroMust, errors);
  validateArray(`${ctx}.requiredSections`, binding.requiredSections, errors, { allowEmpty: true });
  validateArray(`${ctx}.proofTypes`, binding.proofTypes, errors);
  validateArray(`${ctx}.faqFocus`, binding.faqFocus, errors);

  if (binding.ctaStyle && !CTA_STYLES.has(binding.ctaStyle)) {
    errors.push(`${ctx}.ctaStyle "${binding.ctaStyle}" is not allowed.`);
  }
  if (binding.benchmarkPool && !BENCHMARK_POOLS.has(binding.benchmarkPool)) {
    errors.push(`${ctx}.benchmarkPool "${binding.benchmarkPool}" is not allowed.`);
  }
}

function validateSections(ctx, sections, errors) {
  validateArray(`${ctx}.sections`, sections, errors);
  if (!Array.isArray(sections)) return;
  for (const [index, section] of sections.entries()) {
    if (typeof section !== 'string' || !section) {
      errors.push(`${ctx}.sections[${index}] must be a non-empty string.`);
    }
  }
  const duplicates = sections.filter((item, index) => sections.indexOf(item) !== index);
  // Duplicates are valid for sections like cta-default/cluster-block-dense in some storylines.
  return new Set(duplicates);
}

function validateBindingAgainstSections(ctx, binding, sections, errors) {
  if (!binding || !Array.isArray(sections)) return;
  const sectionSet = new Set(sections);
  if (binding.heroType && sections[0] !== binding.heroType) {
    errors.push(`${ctx}.copy.heroType "${binding.heroType}" does not match first section "${sections[0]}".`);
  }
  for (const required of binding.requiredSections || []) {
    if (!sectionSet.has(required)) {
      errors.push(`${ctx}.copy.requiredSections contains "${required}" but sections do not include it.`);
    }
  }
  const proofHit = (binding.proofTypes || []).some((type) => sectionSet.has(type));
  if (!proofHit) {
    errors.push(`${ctx}.copy.proofTypes has no overlap with sections.`);
  }
}

function main() {
  const errors = [];
  const warnings = [];

  const landing = readJson(FILES.landing);
  const solution = readJson(FILES.solution);
  const scenario = readJson(FILES.scenario);
  const pageBindings = readJson(FILES.pageBindings);

  const masterIntents = new Set(pageBindings.masterIntents || []);
  const croStageByIntent = pageBindings.governedDimensions?.croStageByIntent || {};

  validateArray('page-copy-bindings.masterIntents', pageBindings.masterIntents, errors);

  for (const intent of masterIntents) {
    if (!(intent in croStageByIntent)) {
      errors.push(`governedDimensions.croStageByIntent missing "${intent}".`);
    }
  }
  for (const intent of Object.keys(croStageByIntent)) {
    if (!masterIntents.has(intent)) {
      errors.push(`governedDimensions.croStageByIntent has unknown intent "${intent}".`);
    }
  }

  const dimensions = pageBindings.governedDimensions?.dimensions || {};
  for (const dim of DIMENSIONS) {
    if (!dimensions[dim]) errors.push(`governedDimensions.dimensions.${dim} is required.`);
  }

  const crosswalk = pageBindings.intentCrosswalk || {};
  for (const [alias, intents] of Object.entries(crosswalk)) {
    validateArray(`intentCrosswalk.${alias}`, intents, errors);
    for (const intent of intents || []) {
      if (!masterIntents.has(intent)) {
        errors.push(`intentCrosswalk.${alias} references unknown intent "${intent}".`);
      }
    }
  }

  // landing: per-storyline copy blocks.
  for (const [id, storyline] of Object.entries(landing.storylines || {})) {
    const ctx = `landing.storylines.${id}`;
    validateSections(ctx, storyline.sections, errors);
    if (storyline.intent && !masterIntents.has(storyline.intent)) {
      errors.push(`${ctx}.intent "${storyline.intent}" is not in masterIntents.`);
    }
    validateCopyBinding(`${ctx}.copy`, { intent: storyline.intent, ...(storyline.copy || {}) }, { masterIntents, errors });
    validateBindingAgainstSections(ctx, storyline.copy, storyline.sections, errors);
    if (storyline.sectionCount && Array.isArray(storyline.sections) && storyline.sectionCount !== storyline.sections.length) {
      errors.push(`${ctx}.sectionCount ${storyline.sectionCount} does not match sections.length ${storyline.sections.length}.`);
    }
  }

  for (const [alias, target] of Object.entries(landing.legacyAliases || {})) {
    if (!landing.storylines?.[target]) {
      errors.push(`landing.legacyAliases.${alias} targets missing storyline "${target}".`);
    }
  }

  // solution / scenario: copyDefault applies to all storylines.
  for (const [name, doc] of [
    ['solution', solution],
    ['scenario', scenario],
  ]) {
    validateCopyBinding(`${name}.copyDefault`, doc.copyDefault, { masterIntents, errors });
    for (const [id, storyline] of Object.entries(doc.storylines || {})) {
      const ctx = `${name}.storylines.${id}`;
      validateSections(ctx, storyline.sections, errors);
      validateBindingAgainstSections(ctx, doc.copyDefault, storyline.sections, errors);
      if (doc.sectionCount && Array.isArray(storyline.sections) && doc.sectionCount !== storyline.sections.length) {
        errors.push(`${ctx} sections.length ${storyline.sections.length} does not match ${name}.sectionCount ${doc.sectionCount}.`);
      }
    }
    for (const [alias, target] of Object.entries(doc.aliases || {})) {
      if (!doc.storylines?.[target]) {
        errors.push(`${name}.aliases.${alias} targets missing storyline "${target}".`);
      }
    }
  }

  // Feature / tool / product / topic bindings do not own section order yet.
  const allPageBindingStorylines = new Set();
  for (const [pageType, block] of Object.entries(pageBindings.pageTypes || {})) {
    const ctx = `pageTypes.${pageType}`;
    validateCopyBinding(`${ctx}.copyDefault`, block.copyDefault, { masterIntents, errors });
    validateArray(`${ctx}.storylines`, block.storylines, errors);
    for (const id of block.storylines || []) {
      if (allPageBindingStorylines.has(id)) {
        errors.push(`pageTypes.${pageType}.storylines duplicates storyline "${id}" across page types.`);
      }
      allPageBindingStorylines.add(id);
    }
  }

  if (warnings.length) {
    for (const warning of warnings) console.warn(`[WARN] ${warning}`);
  }

  if (errors.length) {
    console.error(`Storyline schema validation failed: ${errors.length} error(s)`);
    for (const error of errors) console.error(`- ${error}`);
    process.exit(1);
  }

  const counts = {
    landing: Object.keys(landing.storylines || {}).length,
    solution: Object.keys(solution.storylines || {}).length,
    scenario: Object.keys(scenario.storylines || {}).length,
    pageBindingOnly: allPageBindingStorylines.size,
  };
  console.log('Storyline schema validation passed.');
  console.log(JSON.stringify(counts, null, 2));
}

main();
