#!/usr/bin/env node
/**
 * Pre-publish checks for off-site distribution drafts.
 *
 *   node preflight-distribution.js --draft drafts/medium-x.md \
 *     --canonical https://lovart.ai/en/blog/x \
 *     --platform medium \
 *     --source-title "Original Title" \
 *     --source-word-count 2000
 *
 * Exit: 0 pass, 1 block
 */

const fs = require('fs')
const path = require('path')

function parseArgs(argv) {
  const out = {}
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i]
    if (a.startsWith('--')) {
      const key = a.slice(2).replace(/-/g, '_')
      const next = argv[i + 1]
      if (!next || next.startsWith('--')) out[key] = true
      else {
        out[key] = next
        i++
      }
    }
  }
  return out
}

function wordCount(text) {
  return text.split(/\s+/).filter(Boolean).length
}

function titleSimilarity(a, b) {
  if (!a || !b) return 0
  const na = a.toLowerCase().trim()
  const nb = b.toLowerCase().trim()
  if (na === nb) return 1
  const setA = new Set(na.split(/\s+/))
  const setB = new Set(nb.split(/\s+/))
  let inter = 0
  for (const w of setA) if (setB.has(w)) inter++
  return inter / Math.max(setA.size, setB.size)
}

function extractTitle(md) {
  const m = md.match(/^#\s+(.+)$/m) || md.match(/^title:\s*["']?(.+?)["']?\s*$/im)
  return m ? m[1].trim() : ''
}

function main() {
  const args = parseArgs(process.argv)
  const issues = []
  const warns = []

  if (!args.draft) {
    console.error('Usage: --draft PATH --canonical URL --platform NAME [--source-title T] [--source-word-count N]')
    process.exit(2)
  }

  const draftPath = path.resolve(args.draft)
  if (!fs.existsSync(draftPath)) {
    console.error(`Draft not found: ${draftPath}`)
    process.exit(2)
  }

  const body = fs.readFileSync(draftPath, 'utf8')
  const draftTitle = extractTitle(body)
  const wc = wordCount(body.replace(/```[\s\S]*?```/g, ''))
  const platform = (args.platform || 'unknown').toLowerCase()
  const canonical = args.canonical || ''
  const sourceTitle = args.source_title || ''
  const sourceWc = Number(args.source_word_count || 0)
  const maxRatio = Number(args.max_ratio || 0.4)

  if (!canonical.includes('lovart.ai')) {
    issues.push('BLOCK: canonical must point to lovart.ai')
  }

  if (sourceTitle && draftTitle && titleSimilarity(draftTitle, sourceTitle) > 0.85) {
    issues.push(`BLOCK: offsite title too similar to source (“${draftTitle}”)`)
  }

  if (sourceWc > 0 && wc > sourceWc * maxRatio) {
    issues.push(`BLOCK: draft ${wc} words > ${Math.round(maxRatio * 100)}% of source ${sourceWc}`)
  }

  const utmPattern = new RegExp(`utm_source=${platform}`, 'i')
  if (!utmPattern.test(body) && !body.includes('utm_source=')) {
    issues.push(`BLOCK: missing utm_source=${platform} in body`)
  }

  if (!body.includes(canonical.split('?')[0])) {
    warns.push('WARN: canonical URL path not found verbatim in draft')
  }

  const canonicalPlatforms = ['medium', 'devto', 'hashnode']
  if (canonicalPlatforms.includes(platform)) {
    if (!/canonical/i.test(body) && !args.canonical_declared) {
      warns.push(`WARN: ${platform} should declare canonical → main site (API field or front matter)`)
    }
  }

  if (wc < 80) {
    warns.push('WARN: draft very short (<80 words)')
  }

  console.log(`Preflight: ${draftPath}`)
  console.log(`  platform: ${platform}`)
  console.log(`  words: ${wc}`)
  console.log(`  title: ${draftTitle || '(none)'}`)

  for (const w of warns) console.log(`  ${w}`)
  for (const e of issues) console.log(`  ${e}`)

  if (issues.length) {
    console.log(`\nFAILED (${issues.length} blockers)`)
    process.exit(1)
  }
  console.log('\nPASSED')
  process.exit(0)
}

main()
