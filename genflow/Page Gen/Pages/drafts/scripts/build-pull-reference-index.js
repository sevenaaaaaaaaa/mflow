#!/usr/bin/env node
/**
 * Build a second-level index for Pages/drafts/_pull reference assets.
 *
 * Local-only: does not move, delete, import, publish, or rewrite source files.
 */

const fs = require('fs')
const path = require('path')

const DRAFTS_ROOT = path.resolve(__dirname, '..')
const ROOT = process.env.LOVART_PULL_DIR
  ? path.resolve(process.env.LOVART_PULL_DIR)
  : path.join(DRAFTS_ROOT, '_pull')  // fallback for backward compat
const OUT_MD = path.join(DRAFTS_ROOT, 'PULL_REFERENCE_INDEX.md')
const OUT_CSV = path.join(DRAFTS_ROOT, 'pull-reference-index-2026-06.csv')
const OUT_JSON = path.join(DRAFTS_ROOT, 'pull-reference-index-2026-06.json')

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, {withFileTypes: true})) {
    const p = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(p, files)
    else if (entry.isFile()) files.push(p)
  }
  return files
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'))
  } catch (error) {
    return {__parse_error: error.message}
  }
}

function inferLanguage(rel, data) {
  if (data.language) return normalizeLanguage(data.language)
  const parts = rel.split(path.sep)
  for (const part of parts) {
    const lang = normalizeLanguage(part)
    if (['en', 'de', 'fr', 'it', 'ja', 'ko', 'pt', 'ru', 'zh', 'zh-TW'].includes(lang)) return lang
  }
  const stem = path.basename(rel, path.extname(rel))
  const match = stem.match(/-(en|de|fr|it|ja|ko|pt|ru|zh|zhtw|zh-tw)$/i)
  return match ? normalizeLanguage(match[1]) : ''
}

function normalizeLanguage(lang) {
  const lower = String(lang || '').toLowerCase()
  if (lower === 'zhtw' || lower === 'zh-tw') return 'zh-TW'
  return lower
}

function inferTargetType(rel, data) {
  if (data.category) return data.category
  if (rel.includes(`${path.sep}Features${path.sep}`)) return 'feature'
  if (rel.includes(`${path.sep}Tools${path.sep}`)) return 'tool'
  if (rel.includes(`${path.sep}Solution${path.sep}`)) return 'solution'
  if (rel.includes(`${path.sep}blog${path.sep}`)) return 'blog'
  return ''
}

function managementStatus(bucket, data, ext) {
  if (bucket === 'blog') return 'pulled-blog-reference'
  if (bucket === 'outbound') return 'pulled-outbound-reference'
  if (bucket.includes('reflow')) return 'pulled-reflow-reference'
  if (bucket.endsWith('-new')) return 'pulled-new-language-reference'
  if (ext !== '.json') return 'pulled-support-reference'
  if (data.seo?.noIndex === true) return 'pulled-noindex-reference'
  return 'pulled-reference'
}

const rows = walk(ROOT).map((file) => {
  const rel = path.relative(DRAFTS_ROOT, file)
  const pullRel = path.relative(ROOT, file)
  const bucket = pullRel.split(path.sep)[0]
  const ext = path.extname(file)
  const data = ext === '.json' ? readJson(file) : {}
  return {
    management_status: managementStatus(bucket, data, ext),
    bucket,
    target_type: inferTargetType(rel, data),
    language: inferLanguage(rel, data),
    slug: data.slug || path.basename(file, ext),
    schemaVersion: data.schemaVersion || '',
    seo_noindex: data.seo?.noIndex === true ? 'true' : data.seo?.noIndex === false ? 'false' : '',
    parse_error: data.__parse_error || '',
    ext,
    path: rel,
  }
})

rows.sort((a, b) => a.management_status.localeCompare(b.management_status) || a.bucket.localeCompare(b.bucket) || a.path.localeCompare(b.path))

const fields = ['management_status', 'bucket', 'target_type', 'language', 'slug', 'schemaVersion', 'seo_noindex', 'ext', 'path', 'parse_error']
function escapeCsv(value) {
  const s = String(value ?? '')
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
}

fs.writeFileSync(OUT_CSV, [fields.join(','), ...rows.map((row) => fields.map((field) => escapeCsv(row[field])).join(','))].join('\n') + '\n')
fs.writeFileSync(OUT_JSON, JSON.stringify(rows, null, 2) + '\n')

let md = `# Pull Reference Index\n\n`
md += `> 日期：2026-06-09  \n`
md += `> 范围：Page Gen \`_pull/\` 参考池（已外置到运行层 \`~/Documents/Lovart Local Dev/Output/Page Gen/_pull/\`）。  \
`
md += `> 原则：二次分层索引；未移动、未删除、未提升发布状态。\n\n`
md += `## Summary\n\n`
md += `- Total files: ${rows.length}\n`
md += `- JSON parse errors: ${rows.filter((row) => row.parse_error).length}\n`
md += `- noIndex JSON rows: ${rows.filter((row) => row.seo_noindex === 'true').length}\n\n`
md += table('By Management Status', countBy('management_status'))
md += table('By Bucket', countBy('bucket'))
md += table('By Target Type', countBy('target_type'))
md += table('By Language', countBy('language'))
md += `## Notes\n\n`
md += `- \`_pull\` assets remain reference material. Promote only by copying through the normal draft/preflight path after human review.\n`
md += `- Reflow and new-language buckets are useful for localization comparison, not direct production import.\n`
fs.writeFileSync(OUT_MD, md)

console.log(JSON.stringify({rows: rows.length, outputs: [OUT_MD, OUT_CSV, OUT_JSON]}, null, 2))

function countBy(field) {
  const counts = new Map()
  for (const row of rows) counts.set(row[field] || '(blank)', (counts.get(row[field] || '(blank)') || 0) + 1)
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
}

function table(title, counts) {
  let out = `## ${title}\n\n| key | count |\n| --- | ---: |\n`
  for (const [key, count] of counts) out += `| ${key} | ${count} |\n`
  return `${out}\n`
}
