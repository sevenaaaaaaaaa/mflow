#!/usr/bin/env node
/**
 * Build a local map for Page Gen PublishedMirror / EditableSource JSON files.
 *
 * This does not call Sanity, import, publish, or modify source page JSON.
 * Sanity production remains the online source of truth.
 */

const fs = require('fs')
const path = require('path')

const ROOT = path.resolve(__dirname, '..')
const SOURCE_DIRS = ['Tools', 'Features', 'Solution', 'Products']
const OUT_CSV = path.join(ROOT, 'PUBLISHED_MIRROR_LOCAL_MAP.csv')
const OUT_JSON = path.join(ROOT, 'PUBLISHED_MIRROR_LOCAL_MAP.json')
const OUT_MD = path.join(ROOT, 'PUBLISHED_MIRROR_LOCAL_MAP.md')

function walk(dir, files = []) {
  if (!fs.existsSync(dir)) return files
  for (const entry of fs.readdirSync(dir, {withFileTypes: true})) {
    const p = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(p, files)
    else if (entry.isFile() && entry.name.endsWith('.json')) files.push(p)
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

function asBool(value) {
  return value === true ? 'true' : value === false ? 'false' : ''
}

function categoryFromDir(dir) {
  const map = {Tools: 'tool', Features: 'feature', Solution: 'solution', Products: 'product'}
  return map[dir] || ''
}

const rows = []
for (const sourceDir of SOURCE_DIRS) {
  for (const file of walk(path.join(ROOT, sourceDir))) {
    const data = readJson(file)
    if (!data.slug || !data.bodyJson) continue
    const rel = path.relative(ROOT, file)
    const lang = data.language || path.basename(path.dirname(file))
    const slug = data.slug || path.basename(file, '.json').replace(new RegExp(`-${lang}$`), '')
    const category = data.category || data.type || categoryFromDir(sourceDir)
    const seo = data.seo || {}
    const key = `${category}:${lang}:${slug}`
    rows.push({
      key,
      source_dir: sourceDir,
      category,
      language: lang,
      slug,
      schemaVersion: data.schemaVersion || '',
      storylineTemplate: data.storylineTemplate || '',
      title: seo.title || data.title || '',
      url_path: data.url_path || '',
      seo_noindex: asBool(seo.noIndex),
      parse_error: data.__parse_error || '',
      path: rel,
    })
  }
}

const keyCounts = new Map()
for (const row of rows) keyCounts.set(row.key, (keyCounts.get(row.key) || 0) + 1)
for (const row of rows) row.local_duplicate_key = keyCounts.get(row.key) > 1 ? 'true' : 'false'

rows.sort((a, b) => a.key.localeCompare(b.key) || a.path.localeCompare(b.path))

const fields = [
  'key',
  'source_dir',
  'category',
  'language',
  'slug',
  'schemaVersion',
  'storylineTemplate',
  'seo_noindex',
  'local_duplicate_key',
  'title',
  'url_path',
  'path',
  'parse_error',
]

function escapeCsv(value) {
  const s = String(value ?? '')
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
}

fs.writeFileSync(
  OUT_CSV,
  [fields.join(','), ...rows.map((row) => fields.map((field) => escapeCsv(row[field])).join(','))].join('\n') + '\n',
)
fs.writeFileSync(OUT_JSON, JSON.stringify(rows, null, 2) + '\n')

function countBy(field) {
  const counts = new Map()
  for (const row of rows) counts.set(row[field] || '(blank)', (counts.get(row[field] || '(blank)') || 0) + 1)
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
}

let md = `# PublishedMirror Local Map\n\n`
md += `> 日期：2026-06-09  \n`
md += `> 范围：Page Gen 本地 PublishedMirror / EditableSource JSON。  \n`
md += `> 原则：只读本地映射；未访问 Sanity production、未 import、未发布。线上真相源仍为 Sanity production。\n\n`
md += `## Summary\n\n`
md += `- Total local JSON rows: ${rows.length}\n`
md += `- Parse errors: ${rows.filter((row) => row.parse_error).length}\n`
md += `- Local duplicate keys: ${rows.filter((row) => row.local_duplicate_key === 'true').length}\n`
md += `- noIndex rows: ${rows.filter((row) => row.seo_noindex === 'true').length}\n\n`
md += table('By Source Dir', countBy('source_dir'))
md += table('By Category', countBy('category'))
md += table('By Language', countBy('language'))
md += `## Local Duplicate Keys\n\n`
md += `| key | files |\n| --- | --- |\n`
for (const [key, count] of [...keyCounts.entries()].filter(([, count]) => count > 1).sort((a, b) => b[1] - a[1])) {
  const files = rows.filter((row) => row.key === key).map((row) => `\`${row.path}\``).join('<br>')
  md += `| ${key} | ${files} |\n`
}
if (![...keyCounts.values()].some((count) => count > 1)) md += `| none |  |\n`
md += `\n## Production Sync Note\n\n`
md += `This map is for local governance only. Before changing published content, pull or verify Sanity production and keep the existing dry-run/import authorization rule.\n`
fs.writeFileSync(OUT_MD, md)

console.log(JSON.stringify({rows: rows.length, duplicateRows: rows.filter((row) => row.local_duplicate_key === 'true').length, outputs: [OUT_MD, OUT_CSV, OUT_JSON]}, null, 2))

function table(title, counts) {
  let out = `## ${title}\n\n| key | count |\n| --- | ---: |\n`
  for (const [key, count] of counts) out += `| ${key} | ${count} |\n`
  return `${out}\n`
}
