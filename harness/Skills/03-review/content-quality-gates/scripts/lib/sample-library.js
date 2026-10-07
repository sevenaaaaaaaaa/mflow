/**
 * Content Sample Library loader
 * SSOT index: ../samples/index.json
 * Doc: 1-1 GEO Readme/文档/04-质量治理/Content-Sample-Library.md
 */

const fs = require('fs')
const path = require('path')

const SAMPLES_DIR = path.join(__dirname, '../../samples')
const INDEX_PATH = path.join(SAMPLES_DIR, 'index.json')

function loadIndex() {
  return JSON.parse(fs.readFileSync(INDEX_PATH, 'utf8'))
}

function loadSample(id) {
  const index = loadIndex()
  const entry = index.samples.find((s) => s.id === id)
  if (!entry) throw new Error(`Unknown sample: ${id}`)
  const filePath = path.join(SAMPLES_DIR, entry.file)
  const raw = fs.readFileSync(filePath, 'utf8')
  const fm = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  if (!fm) return { meta: {}, body: raw, entry }
  const meta = {}
  for (const line of fm[1].split('\n')) {
    const m = line.match(/^(\w+):\s*(.*)$/)
    if (m) meta[m[1]] = m[2].replace(/^["']|["']$/g, '')
  }
  return { meta, body: fm[2], entry, raw }
}

function findSamples({ content_type, verdict, language, tag } = {}) {
  const index = loadIndex()
  return index.samples.filter((s) => {
    if (content_type && s.content_type !== content_type) return false
    if (verdict && s.verdict !== verdict) return false
    if (language && s.language !== language) return false
    if (tag && !(s.tags || []).includes(tag)) return false
    return true
  })
}

function getPair(content_type, prefer = 'gold') {
  const index = loadIndex()
  const goodId = index.gold_defaults?.[content_type] || index.samples.find((s) => s.content_type === content_type && s.verdict === 'good')?.id
  const badId = index.bad_defaults?.[content_type]
  if (prefer === 'bad' && badId) return loadSample(badId)
  if (goodId) return loadSample(goodId)
  throw new Error(`No default sample for type: ${content_type}`)
}

function formatBrief(sample) {
  const e = sample.entry
  return [
    `Sample: ${e.id} (${e.verdict}, score ${e.rubric_score})`,
    `Pattern: ${sample.meta.reusable_pattern || sample.entry.focus_query || '—'}`,
    `Pair with: ${e.pair_with || '—'}`,
    `Preflight: ${e.preflight_pass ? 'pass' : 'fail ' + (e.preflight_codes || []).join(', ')}`,
  ].join('\n')
}

module.exports = {
  SAMPLES_DIR,
  loadIndex,
  loadSample,
  findSamples,
  getPair,
  formatBrief,
}
