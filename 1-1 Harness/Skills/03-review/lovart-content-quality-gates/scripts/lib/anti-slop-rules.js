/**
 * Anti-Slop preflight rules — SSOT for banned phrases, placeholders, shrinkage heuristics.
 * Pair with: 1-1 GEO Readme/文档/04-质量治理/Preflight-Anti-Slop-Gates.md
 *
 * Integrate into lovart.sanity.studio/scripts/preflight-content.js via:
 *   const antiSlop = require('.../anti-slop-rules.js')
 */

const BANNED_PHRASES_EN = [
  /\bin today'?s fast[- ]paced\b/i,
  /\bunlock\b/i,
  /\brevolutioniz(e|ing|es|ed)\b/i,
  /\bseamless(ly)?\b/i,
  /\bempower(s|ing|ed)?\b/i,
  /\bgame[- ]changer\b/i,
  /\bcutting[- ]edge\b/i,
  /\bleverage(s|d|ing)?\b/i,
  /\bAI[- ]powered platform\b/i,
  /\bthe future of\b/i,
  /\btransform(s|ing|ed)? your (workflow|business)\b/i,
]

const BANNED_PHRASES_ZH = [
  /赋能/,
  /闭环/,
  /颠覆性/,
  /革命性/,
  /一站式解决方案/,
  /在当今快节奏/,
  /解锁.*潜力/,
  /无缝衔接/,
  /未来可期/,
  /综上所述/,
]

const BANNED_PHRASES_JA = [
  /革新的な/,
  /シームレス/,
  /ワンストップ/,
  /今後に期待/,
]

const PLACEHOLDER_PATTERNS = [
  /IMAGE PLACEHOLDER/i,
  /\[IMAGE\s*\d*\s*PLACEHOLDER\]/i,
  /\[TODO\]/i,
  /\[TBD\]/i,
  /\[待补充\]/,
  /\[待考证\]/, // WARN only — allowed when explicitly marked
  /lorem ipsum/i,
  /xxx+/i,
  /\(section_[a-z]{2}(-[a-z]{2})?\)/i,
]

const BAD_LINK_PATTERNS = [
  /\/博客文章\//,
  /\/cluster\//,
  /\.md\)/,
  /\]\(#\)/,
  /\]\(\/\)/,
]

const GENERIC_H2_PATTERNS = [
  /^#+\s*(benefits?|features?|conclusion|summary|introduction|overview)\s*$/im,
  /^#+\s*(优势|特点|总结|结论|概述|简介)\s*$/im,
  /^#+\s*(まとめ|概要|結論)\s*$/im,
  /^#+\s*part\s+\d+/im,
]

const CTA_PATTERNS = [
  /lovart\.ai\/signup/i,
  /lovart\.ai\/pricing/i,
  /\/signup\b/i,
  /\/pricing\b/i,
  /get started/i,
  /try (lovart|free)/i,
  /免费试用/,
  /立即体验/,
  /今すぐ/,
]

function placeholderSeverity(re) {
  return re.source.includes('待考证') ? 'WARN' : 'BLOCK'
}

function detectLanguage(text, fallback = 'en') {
  if (/[\u3040-\u30ff]/.test(text)) return 'ja'
  if (/[\u4e00-\u9fff]/.test(text)) return 'zh'
  return fallback
}

function countMatches(text, patterns) {
  const hits = []
  for (const re of patterns) {
    const m = text.match(new RegExp(re.source, re.flags.includes('g') ? re.flags : re.flags + 'g'))
    if (m) hits.push(...m)
  }
  return hits
}

function extractH2Sections(markdown) {
  const lines = markdown.split('\n')
  const sections = []
  let current = null
  for (const line of lines) {
    const m = line.match(/^##\s+(.+)$/)
    if (m) {
      if (current) sections.push(current)
      current = { title: m[1].trim(), body: '' }
    } else if (current) {
      current.body += line + '\n'
    }
  }
  if (current) sections.push(current)
  return sections
}

function wordCount(text) {
  const cjk = (text.match(/[\u4e00-\u9fff\u3040-\u30ff]/g) || []).length
  const words = text.trim().split(/\s+/).filter(Boolean).length
  return cjk > words ? cjk : words
}

function sectionDensityScore(text) {
  let score = 0
  if (/\d/.test(text)) score++
  if (/(例如|比如|for example|e\.g\.|case study|案例)/i.test(text)) score++
  if (/(因为|因此|however|but|机制|workflow|步骤|step)/i.test(text)) score++
  if (wordCount(text) >= 120) score++
  return Math.min(3, score)
}

function stripFaqTail(text) {
  const m = text.search(/^##\s*(FAQ|常见问题|よくある質問)\s*$/im)
  return m > 0 ? text.slice(0, m) : text
}

function stripFrontmatter(content) {
  return content.replace(/^---\n[\s\S]*?\n---\n?/, '')
}

function unquote(value) {
  return String(value || '').trim().replace(/^['"]|['"]$/g, '')
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/)
  if (!match) return {}
  const out = {}
  const lines = match[1].split('\n')
  let activeArrayKey = null

  for (const rawLine of lines) {
    const line = rawLine.replace(/\t/g, '    ')
    if (!line.trim()) continue

    if (activeArrayKey && /^\s*-\s+/.test(line)) {
      out[activeArrayKey].push(unquote(line.replace(/^\s*-\s+/, '')))
      continue
    }
    activeArrayKey = null

    const m = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/)
    if (!m) continue
    const [, key, rawValue] = m
    const value = rawValue.trim()
    if (!value) {
      out[key] = []
      activeArrayKey = key
      continue
    }
    out[key] = unquote(value)
  }

  return out
}

function countEnglishWords(text) {
  const normalized = String(text || '')
    .replace(/[`*_>#-]/g, ' ')
    .replace(/[^\p{L}\p{N}\s'-]+/gu, ' ')
  return normalized.split(/\s+/).filter(Boolean).length
}

function countCjkChars(text) {
  return (String(text || '').match(/[\u4e00-\u9fff]/g) || []).length
}

function getLengthStats(text) {
  return {
    englishWords: countEnglishWords(text),
    cjkChars: countCjkChars(text),
    measured: wordCount(text),
  }
}

function inferArticleArchetype(frontmatter = {}, body = '') {
  const category = String(frontmatter.category || '').toLowerCase()
  const pageType = String(frontmatter.page_type || frontmatter.pageType || '').toLowerCase()
  const template = String(frontmatter.template || '').toLowerCase()
  const title = String(frontmatter.title || '').toLowerCase()
  const slug = String(frontmatter.slug || '').toLowerCase()
  const haystack = `${category}\n${pageType}\n${template}\n${title}\n${slug}\n${body.slice(0, 1200).toLowerCase()}`

  if (pageType || /^t\d-/.test(template)) return null
  if (/complete guide|ultimate guide|完整指南|终极指南/.test(haystack)) return 'complete-guide'
  if (category === 'insight & trend' || /insight\s*&\s*trend|行业洞察/.test(haystack)) return 'insight-trend'
  if (category === 'lovart 101' || /\blovart 101\b/.test(haystack)) return 'lovart-101'
  return null
}

function getLengthTarget(archetype, lang) {
  const isZh = String(lang || '').startsWith('zh')
  if (archetype === 'complete-guide') {
    return isZh
      ? { metric: 'cjkChars', min: 12000, label: '12,000 Chinese characters' }
      : { metric: 'englishWords', min: 7500, label: '7,500 English words' }
  }
  if (archetype === 'insight-trend') {
    return isZh
      ? { metric: 'cjkChars', min: 8000, label: '8,000 Chinese characters' }
      : { metric: 'englishWords', min: 4500, label: '4,500 English words' }
  }
  if (archetype === 'lovart-101' && !isZh) {
    return { metric: 'englishWords', min: 4500, label: '4,500 English words' }
  }
  return null
}

function countMarkdownImageSignals(body, frontmatter = {}) {
  const mdImages = [...String(body || '').matchAll(/!\[([^\]]*)\]\((https?:\/\/[^)]+)\)/g)]
  const htmlImages = [...String(body || '').matchAll(/<img[^>]+src=["'](https?:\/\/[^"']+)["'][^>]*>/gi)]
  const imageBriefCount = Array.isArray(frontmatter.image_briefs) ? frontmatter.image_briefs.length : 0
  const emptyAltCount = mdImages.filter((m) => !m[1].trim()).length
  return {
    imageCount: mdImages.length + htmlImages.length + imageBriefCount,
    emptyAltCount,
  }
}

function countInternalLinks(text) {
  const matches = String(text || '').match(/\]\((\/(?:blog|tools|features|feature|product|products|solution|scenario|topic|pseo)\/[^)#\s]+)\)/g)
  return matches ? matches.length : 0
}

function seoDepthCheckMarkdown(content, frontmatter = {}, opts = {}) {
  const issues = []
  const add = (code, severity, message, detail) => issues.push({ code, severity, message, detail })
  const body = stripFrontmatter(content)
  const h1Count = (body.match(/^#\s+.+$/gm) || []).length
  const archetype = opts.archetype || inferArticleArchetype(frontmatter, body)
  const length = getLengthStats(body)

  if (h1Count !== 1) add('SEO_H1', 'BLOCK', `Expected exactly 1 H1, found ${h1Count}`)

  const targetKeywords = Array.isArray(frontmatter.target_keywords)
    ? frontmatter.target_keywords.filter(Boolean)
    : []
  if (targetKeywords.length) {
    const primary = targetKeywords[0].toLowerCase()
    const h1 = ((body.match(/^#\s+(.+)$/m) || [])[1] || '').toLowerCase()
    const earlyBody = body.slice(0, Math.max(1200, Math.floor(body.length * 0.25))).toLowerCase()
    if (!h1.includes(primary)) {
      add('SEO_PRIMARY_KEYWORD', 'WARN', `Primary keyword missing from H1: ${targetKeywords[0]}`)
    }
    if (!earlyBody.includes(primary)) {
      add('SEO_PRIMARY_KEYWORD', 'WARN', `Primary keyword not used in early body: ${targetKeywords[0]}`)
    }
  }

  if ((frontmatter.page_type || frontmatter.template) && !/<script[^>]+application\/ld\+json/i.test(content)) {
    add('SEO_STRUCTURED_DATA', 'WARN', 'Missing JSON-LD block in markdown source')
  } else if (/<script[^>]+application\/ld\+json/i.test(content) && !/"@type"\s*:\s*"/.test(content)) {
    add('SEO_STRUCTURED_DATA', 'WARN', 'JSON-LD block exists but "@type" is missing')
  }

  const internalLinks = countInternalLinks(body)
  if (length.measured >= 1800 && internalLinks < 2) {
    add('SEO_INTERNAL_LINKS', 'WARN', `Only ${internalLinks} internal links in long article`)
  }

  const imageSignals = countMarkdownImageSignals(body, frontmatter)
  if (imageSignals.emptyAltCount > 0) {
    add('IMG_ALT', 'WARN', `${imageSignals.emptyAltCount} markdown image(s) have empty alt text`)
  }
  if ((archetype === 'complete-guide' || archetype === 'insight-trend') && imageSignals.imageCount < 2) {
    add('IMG_ALLOCATION', 'WARN', `Only ${imageSignals.imageCount} image signals for long-form article`)
  }

  return issues
}

function countCompositeImageSignals(sections) {
  let count = 0
  function walk(node) {
    if (Array.isArray(node)) {
      node.forEach(walk)
      return
    }
    if (!node || typeof node !== 'object') return
    for (const [key, value] of Object.entries(node)) {
      if (typeof value === 'string') {
        if ((key === 'src' || key === 'url') && /^https?:\/\//i.test(value)) count++
      } else {
        walk(value)
      }
    }
  }
  walk(sections)
  return count
}

function seoDepthCheckComposite(page, sections = []) {
  const issues = []
  const add = (code, severity, message, detail) => issues.push({ code, severity, message, detail })
  const seo = page.seo || {}
  const imageSignals = countCompositeImageSignals(sections)

  if (!page.seo || typeof page.seo !== 'object') {
    add('SEO_META', 'BLOCK', 'Missing seo object on composite page')
    return issues
  }
  if (!String(seo.title || '').trim()) add('SEO_META_TITLE', 'BLOCK', 'Missing seo.title')
  if (!String(seo.description || '').trim()) add('SEO_META_DESC', 'BLOCK', 'Missing seo.description')
  if (!Array.isArray(seo.keywords) || seo.keywords.length < 3) {
    add('SEO_META_KEYWORDS', 'WARN', 'seo.keywords should contain at least 3 keywords')
  }
  if (!String(seo.ogImage?.url || '').trim()) add('SEO_OG_IMAGE', 'BLOCK', 'Missing seo.ogImage.url')
  if (seo.ogImage?.url && !String(seo.ogImage?.alt || '').trim()) {
    add('IMG_ALT', 'WARN', 'seo.ogImage.alt is empty')
  }
  const structuredData = seo.structuredData?.json || seo.structuredData || page.structuredData?.json || page.structuredData
  if (!structuredData) add('SEO_STRUCTURED_DATA', 'WARN', 'Missing structured data payload on composite page')

  if (sections.length >= 10 && imageSignals < 4) {
    add('IMG_ALLOCATION', 'WARN', `Only ${imageSignals} image signals for a ${sections.length}-section page`)
  }

  return issues
}

function analyzeShrinkage(text) {
  const body = stripFaqTail(text)
  const len = body.length
  if (len < 2000) return { skip: true, reason: 'too_short' }
  const firstEnd = Math.floor(len * 0.3)
  const midEnd = Math.floor(len * 0.7)
  const first = body.slice(0, firstEnd)
  const middle = body.slice(firstEnd, midEnd)
  const last = body.slice(midEnd)
  const scores = {
    first: sectionDensityScore(first),
    middle: sectionDensityScore(middle),
    last: sectionDensityScore(last),
  }
  const fail =
    scores.last === 0 ||
    (scores.last === 1 && scores.first >= 2 && scores.middle >= 2)
  return { skip: false, scores, fail }
}

function countFaqItems(markdown) {
  const faqHeading = markdown.match(/^##\s*(FAQ|常见问题|常見問題|よくある質問|자주 묻는 질문|Perguntas frequentes|Questions fréquentes|Domande frequenti|Häufig gestellte Fragen|Preguntas frecuentes)/im)
  if (!faqHeading) return 0
  const idx = markdown.search(/^##\s*(FAQ|常见问题|常見問題|よくある質問|자주 묻는 질문|Perguntas frequentes|Questions fréquentes|Domande frequenti|Häufig gestellte Fragen|Preguntas frecuentes)/im)
  const faqBlock = markdown.slice(idx)
  const qCount = (faqBlock.match(/^###\s+/gm) || []).length
  const liCount = (faqBlock.match(/^\s*[-*]\s+\*\*/gm) || []).length
  return Math.max(qCount, liCount)
}

function checkBlogMarkdown(content, opts = {}) {
  const issues = []
  const frontmatter = parseFrontmatter(content)
  const bodyText = stripFrontmatter(content)
  const lang = opts.language || frontmatter.language || detectLanguage(content)
  const strict = !!opts.strict
  const archetype = inferArticleArchetype(frontmatter, bodyText)
  const lengthStats = getLengthStats(bodyText)

  const add = (code, severity, message, detail) => {
    issues.push({ code, severity, message, detail })
  }

  if (!/^---\n[\s\S]+?\n---/.test(content)) {
    add('MD_FRONTMATTER', 'BLOCK', 'Missing YAML frontmatter')
  }

  for (const re of BAD_LINK_PATTERNS) {
    if (re.test(content)) add('MD_LINK', 'BLOCK', `Bad internal link pattern: ${re}`)
  }

  for (const re of PLACEHOLDER_PATTERNS) {
    if (re.test(content)) {
      const sev = placeholderSeverity(re)
      add('UX_PLACEHOLDER', sev, `Placeholder or marker found: ${re}`)
    }
  }

  const banned =
    lang === 'zh' || lang === 'zh-TW'
      ? [...BANNED_PHRASES_ZH, ...BANNED_PHRASES_EN.slice(0, 4)]
      : lang === 'ja'
        ? [...BANNED_PHRASES_JA, ...BANNED_PHRASES_EN.slice(0, 4)]
        : BANNED_PHRASES_EN

  const bannedHits = countMatches(content, banned)
  if (bannedHits.length >= 3) {
    add('AS_BANNED_DENSITY', strict ? 'BLOCK' : 'WARN', `High banned-phrase density (${bannedHits.length})`, bannedHits.slice(0, 5).join(', '))
  } else if (bannedHits.length > 0) {
    add('AS_BANNED_PHRASE', 'WARN', `Banned phrase(s): ${bannedHits.slice(0, 3).join(', ')}`)
  }

  for (const re of GENERIC_H2_PATTERNS) {
    if (re.test(content)) add('AS_GENERIC_H2', 'WARN', `Generic H2 heading: ${re}`)
  }

  const h2s = extractH2Sections(content)
  if (h2s.length > 0 && h2s.length < 3 && wordCount(content) > 1500) {
    add('AS_H2_COUNT', 'WARN', `Long article with only ${h2s.length} H2 sections`)
  }

  for (const h2 of h2s) {
    if (/^(FAQ|常见问题|よくある質問)$/i.test(h2.title)) continue
    const wc = wordCount(h2.body)
    const density = sectionDensityScore(h2.body)
    const listItems = (h2.body.match(/^\s*(\d+\.|[-*])\s+/gm) || []).length
    if (wc > 0 && wc < 40 && listItems < 2) {
      add('AS_THIN_H2', 'WARN', `Thin H2 section: "${h2.title}" (${wc} words)`)
    }
    if (density < 2 && wc > 200) {
      add('AS_LOW_DENSITY_H2', 'WARN', `Low information density in H2: "${h2.title}"`)
    }
  }

  const faqCount = countFaqItems(content)
  if (faqCount < 3) add('UX_FAQ', 'BLOCK', `FAQ count ${faqCount} < 3`)

  if (!CTA_PATTERNS.some((re) => re.test(content))) {
    add('UX_CTA', 'BLOCK', 'No CTA pattern found (signup/pricing/get started)')
  }

  const lengthTarget = getLengthTarget(archetype, lang)
  if (lengthTarget) {
    const actual = lengthStats[lengthTarget.metric] || 0
    if (actual < lengthTarget.min) {
      add(
        'LENGTH_TARGET',
        'BLOCK',
        `${archetype} requires at least ${lengthTarget.label}`,
        `${actual}/${lengthTarget.min}`,
      )
    }
  }

  const shrink = analyzeShrinkage(bodyText)
  if (!shrink.skip && shrink.fail) {
    add('AS_SHRINKAGE', strict ? 'BLOCK' : 'WARN', 'Last 30% appears thinner than opening', JSON.stringify(shrink.scores))
  }

  issues.push(...seoDepthCheckMarkdown(content, frontmatter, { archetype, language: lang }))

  return { lang, issues, h2Count: h2s.length, faqCount, archetype, lengthStats, frontmatter }
}

function collectCompositeText(page) {
  const parts = [page.title, page.description, JSON.stringify(page.seo || {})]
  let sections = []
  try {
    const raw = page.bodyJson
    sections = typeof raw === 'string' ? JSON.parse(raw) : raw
  } catch {
    return { parts: parts.join('\n'), sections: [], parseError: true }
  }
  if (!Array.isArray(sections)) return { parts: parts.join('\n'), sections: [], parseError: true }
  for (const s of sections) {
    parts.push(JSON.stringify(s))
  }
  return { parts: parts.join('\n'), sections, parseError: false }
}

function checkCompositePage(page, opts = {}) {
  const issues = []
  const strict = !!opts.strict
  const lang = page.language || 'en'
  const add = (code, severity, message, detail) => issues.push({ code, severity, message, detail })

  const { parts, sections, parseError } = collectCompositeText(page)
  if (parseError) {
    add('JSON_BODY', 'BLOCK', 'bodyJson parse failed')
    return { lang, issues }
  }

  for (const re of PLACEHOLDER_PATTERNS) {
    if (re.test(parts)) {
      const sev = placeholderSeverity(re)
      add('UX_PLACEHOLDER', sev, `Placeholder in page copy: ${re}`)
    }
  }

  if (/\(section_[a-z]{2}/i.test(parts)) {
    add('I18N_MARKER', 'BLOCK', 'Translation section marker found')
  }

  const hasFaq = sections.some((s) => s.type === 'faq' && (s.items?.length >= 3 || s.faq?.length >= 3))
  if (!hasFaq) add('UX_FAQ', 'BLOCK', 'FAQ section missing or < 3 items')

  const hasCta = sections.some((s) =>
    /signup|pricing|get started|try free|免费|体験/i.test(JSON.stringify(s))
  )
  if (!hasCta) add('UX_CTA', 'BLOCK', 'No CTA in composite sections')

  const hero = sections.find((s) => /hero|prompt-launcher/i.test(s.type || ''))
  if (hero) {
    const heroText = JSON.stringify(hero)
    const hasIO = /(input|prompt|upload|输出|export|生成)/i.test(heroText)
    if (!hasIO && page.category === 'tool') {
      add('AS_HERO_IO', 'WARN', 'Tool page hero may not state input/output')
    }
  }

  const banned =
    lang.startsWith('zh') ? BANNED_PHRASES_ZH : lang === 'ja' ? BANNED_PHRASES_JA : BANNED_PHRASES_EN
  const hits = countMatches(parts, banned)
  if (hits.length >= 4) {
    add('AS_BANNED_DENSITY', strict ? 'BLOCK' : 'WARN', `High banned-phrase density (${hits.length})`)
  }

  const shrink = analyzeShrinkage(parts)
  if (!shrink.skip && shrink.fail) {
    add('AS_SHRINKAGE', strict ? 'BLOCK' : 'WARN', 'Page copy back third appears thin', JSON.stringify(shrink.scores))
  }

  issues.push(...seoDepthCheckComposite(page, sections))

  // language ↔ TDK alignment (title / seo.title / description / seo.description)
  try {
    const { checkTdkI18n } = require('./tdk-i18n-gate')
    const tdk = checkTdkI18n(page, { strict })
    for (const issue of tdk.issues || []) {
      issues.push(issue)
    }
  } catch (e) {
    add('TDK_I18N_GATE', 'WARN', `tdk-i18n-gate unavailable: ${e.message}`)
  }

  // language ↔ bodyJson alignment (EN wrong-lang / EN shell)
  try {
    const { checkBodyI18n } = require('./body-i18n-gate')
    const bodyGate = checkBodyI18n(page)
    for (const issue of bodyGate.issues || []) {
      issues.push(issue)
    }
  } catch (e) {
    add('BODY_I18N_GATE', 'WARN', `body-i18n-gate unavailable: ${e.message}`)
  }

  return { lang, issues, sectionCount: sections.length }
}

function summarize(issues, strict = false) {
  const blocks = issues.filter((i) => i.severity === 'BLOCK')
  const warns = issues.filter((i) => i.severity === 'WARN')
  const failed = blocks.length > 0 || (strict && warns.length > 0)
  return { failed, blockCount: blocks.length, warnCount: warns.length, blocks, warns }
}

/**
 * ======================================================
 * L2 Pro-Quality 检测 (v2)
 * ======================================================
 */

const CONTRADICTION_PATTERNS_EN = [
  /\b(but|however|though|yet|although|nevertheless|instead|despite|while|whereas|on the other hand|that said)\b/i,
]

const CONTRADICTION_PATTERNS_ZH = [
  /但是/,
  /不过/,
  /尽管/,
  /然而/,
  /虽然/,
  /但(?!\.)/,
  /却(?!\.)/,
  /反之/,
  /与此(同时|相反)/,
]

const FIRST_PERSON_PATTERNS_EN = [
  /\bI\b/i,
  /\bI['\u2019](ve|d|ll|m)\b/i,
  /\bmy\b/i,
  /\bmine\b/i,
]

const FIRST_PERSON_PATTERNS_ZH = [
  /我(?!们)/,
  /我自己/,
]

const REJECTION_PATTERNS = [
  /don't/i,
  /shouldn't/i,
  /not recommended/i,
  /avoid/i,
  /never/i,
  /别/,
  /不要/,
  /避免/,
  /不推荐/,
  /不适合/,
  /不适用/,
  /non adatto/i,
  /non consigliato/i,
  /evitare/i,
  /non utilizzare/i,
]

const SPECIFIC_NUMBER_PATTERN = /\b\d{2,}\b/

/**
 * L2 Pro-Quality check —反对不普通/反纯SEO/反内容农场
 *
 * @param {string} text — plain text body (frontmatter stripped)
 * @param {object} opts
 * @param {boolean} opts.strict — strict mode
 * @param {string} opts.language — 'en', 'zh', 'ja', etc.
 * @returns {Array<{code:string, severity:string, message:string, detail?:string}>}
 */
function proQualityCheck(text, opts = {}) {
  const issues = []
  const strict = !!opts.strict
  const lang = opts.language || detectLanguage(text)
  const add = (code, severity, message, detail) => issues.push({ code, severity, message, detail })

  // 1. PQ_GENERIC_VOICE — 无第一人称 => 不普通
  const firstPersonPatterns = lang === 'zh' || lang === 'zh-TW' ? FIRST_PERSON_PATTERNS_ZH : FIRST_PERSON_PATTERNS_EN
  const fpCount = countMatches(text, firstPersonPatterns).length
  if (fpCount === 0) {
    add('PQ_GENERIC_VOICE', 'BLOCK', 'Zero first-person markers — content reads like generic AI copy, no作者 voice')
  } else if (fpCount < 3) {
    add('PQ_GENERIC_VOICE', 'WARN', `Only ${fpCount} first-person markers — too few for genuine voice`)
  }

  // 2. PQ_NO_CONTRADICTION — 零矛盾标记 => 纯 SEO / 无判断
  const contraPatterns = lang === 'zh' || lang === 'zh-TW' ? CONTRADICTION_PATTERNS_ZH : CONTRADICTION_PATTERNS_EN
  const contraCount = countMatches(text, contraPatterns).length
  if (contraCount === 0) {
    add('PQ_NO_CONTRADICTION', 'WARN', 'Zero contradiction markers (but/however/though) — content has no trade-offs')
  }

  // 3. PQ_NONSPECIFIC_FAILURE — 无具体数字 => 翻车不具体
  const numberCount = countMatches(text, [SPECIFIC_NUMBER_PATTERN]).length
  if (numberCount < 3) {
    add('PQ_NONSPECIFIC_FAILURE', 'WARN', `Only ${numberCount} specific numbers — failures/ results lack concrete detail`)
  }

  // 4. PQ_NO_JUDGEMENT — 无不推荐 => 内容农场（只说好不说坏）
  const rejectionCount = countMatches(text, REJECTION_PATTERNS).length
  if (rejectionCount === 0) {
    add('PQ_NO_JUDGEMENT', 'WARN', 'Zero negative recommendations — no judgement, reads like content farm')
  }

  // 5. PQ_FAQ_IS_H2_COPY — FAQ 与 H2 重复（需传 h2Titles 和 faqTitles）
  if (opts.h2Titles && opts.faqTitles && opts.h2Titles.length > 1 && opts.faqTitles.length > 1) {
    let overlap = 0
    for (const faqQ of opts.faqTitles) {
      const faqLower = faqQ.toLowerCase().replace(/^(what|how|why|can|do|does|is|are|when|where|which) /, '')
      for (const h2 of opts.h2Titles) {
        const h2Lower = h2.toLowerCase()
        // Jaccard-like similarity: if FAQ title is substring of H2 or vice versa
        if (faqLower.length > 3 && (h2Lower.includes(faqLower) || faqLower.includes(h2Lower))) {
          overlap++
          break
        }
      }
    }
    if (overlap >= Math.ceil(opts.faqTitles.length * 0.7)) {
      add('PQ_FAQ_IS_H2_COPY', 'WARN', `${overlap}/${opts.faqTitles.length} FAQ questions overlap with H2 headings — not real user objections`)
    }
  }

  // 6. PQ_PATCHWORK_STRUCTURE — 探测拼凑（H2 间无逻辑依赖）
  // 通过检查 H2 是否包含唯一数字/判断词来近似判断
  if (opts.h2Titles && opts.h2Titles.length >= 2) {
    const judgementSignals = [/\d/, /\b(why|how|when|what if|but|however|instead)\b/i, /原因|如何|为什么|什么时候|但/]
    const h2sWithoutJudgement = opts.h2Titles.filter(h2 => {
      return !judgementSignals.some(re => re.test(h2))
    })
    if (h2sWithoutJudgement.length >= Math.ceil(opts.h2Titles.length * 0.5)) {
      add('PQ_PATCHWORK_STRUCTURE', 'WARN',
        `${h2sWithoutJudgement.length}/${opts.h2Titles.length} H2s lack judgement signals — may be patchwork structure`)
    }
  }

  // ---- L2b-2: TABLE_IN_BODY — markdown table in body (Sanity incompatible) ----
  if (/^\s*\|.+\|.+\|/m.test(text)) {
    add('TABLE_IN_BODY', 'BLOCK', 'Markdown table found in body text — Sanity Portable Text does not render markdown tables')
  }

  // ---- L2b-3: LANG_MIX_ZH — Chinese chars in non-CJK articles ----
  const zhCount = (text.match(/[\u4e00-\u9fff]/g) || []).length
  if (lang !== 'ja' && lang !== 'ko' && lang !== 'zh' && lang !== 'zh-TW' && zhCount > 0) {
    add('LANG_MIX_ZH', 'BLOCK', `${zhCount} Chinese character(s) in ${lang} article — language pollution bug`)
  }

  // ---- L2b-4: BULLET_ONLY_TEXT / BULLET_SHRINKAGE ----
  const allLines = text.split('\n').filter(l => l.trim().length > 0)
  if (allLines.length > 0) {
    let bulletLines = 0
    for (const l of allLines) {
      const s = l.trim()
      if (/^[-*]\s/.test(s)) bulletLines++
      else if (/^\d+[.)]\s/.test(s)) bulletLines++
    }
    const bulletRatio = bulletLines / allLines.length
    const wc = wordCount(text)
    if (bulletRatio > 0.5) {
      add('BULLET_ONLY_TEXT', strict && wc < 3000 ? 'BLOCK' : 'WARN',
        `${Math.round(bulletRatio * 100)}% of lines are bullet-points — no paragraph prose`)
      if (wc < 3000) {
        add('BULLET_SHRINKAGE', 'WARN',
          `Short article (${wc} words) with ${Math.round(bulletRatio * 100)}% bullets — classic shrinkage`)
      }
    } else if (bulletRatio > 0.3 && wc < 2000) {
      add('BULLET_SHRINKAGE', 'WARN',
        `${wc}-word article with ${Math.round(bulletRatio * 100)}% bullet density — possible shrinkage`)
    }
  }

  return issues
}

module.exports = {
  BANNED_PHRASES_EN,
  BANNED_PHRASES_ZH,
  BANNED_PHRASES_JA,
  PLACEHOLDER_PATTERNS,
  BAD_LINK_PATTERNS,
  checkBlogMarkdown,
  checkCompositePage,
  analyzeShrinkage,
  sectionDensityScore,
  summarize,
  proQualityCheck,
  // Pro-Quality patterns
  REJECTION_PATTERNS,
  CONTRADICTION_PATTERNS_EN,
  CONTRADICTION_PATTERNS_ZH,
  FIRST_PERSON_PATTERNS_EN,
  FIRST_PERSON_PATTERNS_ZH,
  SPECIFIC_NUMBER_PATTERN,
  stripFrontmatter,
  parseFrontmatter,
  getLengthStats,
  inferArticleArchetype,
  getLengthTarget,
  seoDepthCheckMarkdown,
  seoDepthCheckComposite,
}
