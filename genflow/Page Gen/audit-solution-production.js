#!/usr/bin/env node
/**
 * Audit Solution pages: local JSON + optional Sanity production bodyJson section order.
 * Run from sanity studio cwd:
 *   node ../../1-3 Content Gen/Page Gen/Pages/Solution/audit-solution-production.js
 *   node .../audit-solution-production.js --sanity
 */
const fs = require('fs')
const path = require('path')
const {execSync} = require('child_process')

const SSOT = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'solution-storylines-v2.json'), 'utf8')
)
const SLUG_TO_STORYLINE = SSOT.contentStrategyMapping

const enDir = path.join(__dirname, 'en')
const files = fs.readdirSync(enDir).filter((f) => f.endsWith('-en.json'))

function sectionTypes(data) {
  if (Array.isArray(data.section) && data.section.length) {
    return data.section.map((s) => s.type)
  }
  if (typeof data.bodyJson === 'string') {
    return JSON.parse(data.bodyJson).map((s) => s.type)
  }
  return []
}

function checkDoc(label, slug, types) {
  const storyline = SLUG_TO_STORYLINE[slug]
  if (!storyline) {
    console.log(`⚠️  ${label}: no contentStrategyMapping for slug "${slug}"`)
    return false
  }
  const expected = SSOT.storylines[storyline]?.sections
  if (!expected) {
    console.log(`❌ ${label}: unknown storyline ${storyline}`)
    return false
  }
  const ok =
    types.length === 12 &&
    JSON.stringify(types) === JSON.stringify(expected)
  const status = ok ? '✅' : '❌'
  console.log(
    `${status} ${label} [${storyline}] ${types.length} sections` +
      (ok ? '' : `\n   expected: ${expected.join(' → ')}\n   actual:   ${types.join(' → ')}`)
  )
  return ok
}

let allOk = true
console.log('=== Local JSON audit ===')
for (const file of files.sort()) {
  const data = JSON.parse(fs.readFileSync(path.join(enDir, file), 'utf8'))
  const localStoryline = data.storyline
  const mapped = SLUG_TO_STORYLINE[data.slug]
  if (mapped && localStoryline !== mapped) {
    console.log(
      `⚠️  ${file}: storyline "${localStoryline}" should be "${mapped}"`
    )
    allOk = false
  }
  if (!checkDoc(file, data.slug, sectionTypes(data))) allOk = false
}

if (process.argv.includes('--sanity')) {
  console.log('\n=== Sanity production audit ===')
  const studioDir = path.resolve(__dirname, '../../../../1-4 Geo Dev/lovart.sanity.studio')
  const query =
    '*[_type=="compositePage" && category=="solution" && language=="en"]{_id, "slug": slug.current, bodyJson}'
  const raw = execSync(
    `npx sanity documents query '${query}' --dataset production`,
    {cwd: studioDir, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe']}
  )
  const docs = JSON.parse(raw.replace(/^[^\[]*/, '').trim())
  for (const doc of docs.sort((a, b) => a._id.localeCompare(b._id))) {
    let types = []
    try {
      types = JSON.parse(doc.bodyJson).map((s) => s.type)
    } catch (e) {
      console.log(`❌ ${doc._id}: bodyJson parse error`)
      allOk = false
      continue
    }
    if (!checkDoc(doc._id, doc.slug, types)) allOk = false
  }
}

console.log(allOk ? '\n✅ All checks passed' : '\n❌ Issues found')
process.exit(allOk ? 0 : 1)
