#!/usr/bin/env node
/*
 * Build a lightweight internal-link index for Lovart content planning.
 *
 * Outputs:
 *   1-3 Content Gen/CONTENT_LINK_INDEX.md
 *   1-3 Content Gen/content-link-index.csv
 */
const fs = require('fs')
const path = require('path')

const PROJECT_ROOT = path.resolve(__dirname, '../..')
const CONTENT_ROOT = fs.existsSync(path.join(PROJECT_ROOT, '1-3 GenFlow'))
  ? path.join(PROJECT_ROOT, '1-3 GenFlow')
  : path.join(PROJECT_ROOT, '1-3 Content Gen')
const BLOG_ROOT = path.join(CONTENT_ROOT, 'Lovart-Blog-Pipeline/Lovart-Blogs/03-Published')
const PAGE_ROOT = path.join(CONTENT_ROOT, 'Page Gen/Pages')
const REFRESH_ROOT = path.join(CONTENT_ROOT, 'Page Gen/Refresh-Page/landing-examples')
const OUT_MD = path.join(CONTENT_ROOT, 'CONTENT_LINK_INDEX.md')
const OUT_CSV = path.join(CONTENT_ROOT, 'content-link-index.csv')

const BLOG_BASE_URL = process.env.LOVART_BLOG_BASE_URL || 'https://blogs.lovart.ai'
const SITE_BASE_URL = process.env.LOVART_SITE_BASE_URL || 'https://www.lovart.ai'

function walk(dir, predicate, out = []) {
  if (!fs.existsSync(dir)) return out
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name)
    const st = fs.statSync(p)
    if (st.isDirectory()) walk(p, predicate, out)
    else if (!predicate || predicate(p)) out.push(p)
  }
  return out
}

function csvEscape(value) {
  const s = String(value || '')
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
}

function slugifyFromFile(file) {
  return path.basename(file).replace(/\.(md|json)$/i, '').replace(/-(en|zh|ja|pt|ru|de|fr|it|ko|zh-TW)$/i, '')
}

function parseFrontmatter(text) {
  if (!text.startsWith('---\n')) return {meta: {}, body: text}
  const end = text.indexOf('\n---', 4)
  if (end < 0) return {meta: {}, body: text}
  const raw = text.slice(4, end).split('\n')
  const body = text.slice(end + 4).trim()
  const meta = {}
  let currentKey = null
  for (const line of raw) {
    const kv = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/)
    if (kv) {
      currentKey = kv[1]
      let v = kv[2].trim()
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1)
      meta[currentKey] = v || []
      continue
    }
    const item = line.match(/^\s*-\s*(.*)$/)
    if (item && currentKey) {
      if (!Array.isArray(meta[currentKey])) meta[currentKey] = meta[currentKey] ? [meta[currentKey]] : []
      meta[currentKey].push(item[1].replace(/^["']|["']$/g, ''))
    }
  }
  return {meta, body}
}

function firstParagraph(body) {
  const para = body
    .split(/\n\s*\n/)
    .map((p) => p.replace(/^#+\s+/gm, '').replace(/[*_`]/g, '').trim())
    .find((p) => p && !p.startsWith('---') && !p.startsWith('|'))
  return (para || '').replace(/\s+/g, ' ').slice(0, 220)
}

function tokenize(text) {
  return new Set(
    String(text || '')
      .toLowerCase()
      .replace(/https?:\/\/\S+/g, ' ')
      .split(/[^a-z0-9]+/)
      .filter((w) => w.length >= 4 && !['with', 'from', 'that', 'this', 'your', 'into', 'guide', 'best'].includes(w)),
  )
}

function overlapScore(a, b) {
  let score = 0
  for (const x of a) if (b.has(x)) score += 1
  return score
}

function pageUrl(category, slug, lang) {
  const prefix = {
    tool: 'tools',
    feature: 'features',
    product: 'products',
    solution: 'solutions',
    scenario: 'scenarios',
    topic: 'topics',
  }[String(category || '').toLowerCase()] || String(category || 'pages').toLowerCase()
  const langPrefix = lang && lang !== 'en' ? `/${lang}` : ''
  return `${SITE_BASE_URL}${langPrefix}/${prefix}/${slug}`
}

function readBlogs() {
  return walk(BLOG_ROOT, (p) => p.endsWith('.md')).map((file) => {
    const text = fs.readFileSync(file, 'utf8')
    const {meta, body} = parseFrontmatter(text)
    const slug = meta.slug || slugifyFromFile(file)
    const tags = Array.isArray(meta.tags) ? meta.tags : String(meta.tags || '').split(',').map((x) => x.trim()).filter(Boolean)
    const description = meta.meta_description || firstParagraph(body)
    const title = meta.title || slug
    const category = meta.category || path.basename(path.dirname(file))
    const tokens = tokenize([title, description, category, tags.join(' '), meta.focus_keyword].join(' '))
    return {
      type: 'blog',
      title,
      slug,
      language: 'en',
      category,
      url: `${BLOG_BASE_URL}/${slug}/`,
      description,
      scenario: [category, meta.difficulty, meta.tool].filter(Boolean).join(' / '),
      tags: tags.join('; '),
      source: path.relative(PROJECT_ROOT, file),
      tokens,
    }
  })
}

function extractBodyHints(raw) {
  let arr = []
  try {
    const body = typeof raw === 'string' ? JSON.parse(raw) : raw
    if (Array.isArray(body)) arr = body
  } catch {
    arr = []
  }
  const titles = []
  for (const s of arr.slice(0, 8)) {
    if (s.title) titles.push(s.title)
    if (Array.isArray(s.features)) for (const f of s.features.slice(0, 3)) if (f.title) titles.push(f.title)
    if (Array.isArray(s.items)) for (const f of s.items.slice(0, 3)) if (f.title) titles.push(f.title)
  }
  return titles.slice(0, 8)
}

function readPages() {
  const roots = ['Tools', 'Features', 'Products', 'Solution']
  const files = roots.flatMap((r) => walk(path.join(PAGE_ROOT, r), (p) => p.endsWith('.json')))
  const pages = files.map((file) => {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'))
    const slug = data.slug || slugifyFromFile(file)
    const lang = data.language || path.basename(path.dirname(file))
    const category = data.category || path.basename(path.dirname(path.dirname(file))).toLowerCase()
    const description = data.description || data.seo?.description || ''
    const keywords = Array.isArray(data.seo?.keywords) ? data.seo.keywords.join('; ') : ''
    const hints = extractBodyHints(data.bodyJson)
    const title = data.title || data.seo?.title || slug
    const tokens = tokenize([title, description, category, keywords, hints.join(' ')].join(' '))
    return {
      type: category,
      title,
      slug,
      language: lang,
      category,
      url: pageUrl(category, slug, lang),
      description,
      scenario: hints.join(' / '),
      tags: keywords,
      source: path.relative(PROJECT_ROOT, file),
      tokens,
    }
  })
  const topicFiles = [...new Set([
    ...walk(path.join(REFRESH_ROOT, 'en'), (p) => p.endsWith('.json') && !path.basename(p).startsWith('draft-')),
    ...walk(path.join(REFRESH_ROOT, 'en/keywords'), (p) => p.endsWith('.json') && !path.basename(p).startsWith('draft-')),
  ])]
  const topics = topicFiles.map((file) => {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'))
    const slug = data.slug || slugifyFromFile(file)
    const lang = data.language || 'en'
    const category = data.category || 'topic'
    const description = data.description || data.seo?.description || ''
    const keywords = Array.isArray(data.seo?.keywords) ? data.seo.keywords.join('; ') : ''
    const hints = extractBodyHints(data.bodyJson)
    const title = data.title || data.seo?.title || slug
    const tokens = tokenize([title, description, category, keywords, hints.join(' ')].join(' '))
    return {
      type: category,
      title,
      slug,
      language: lang,
      category,
      url: pageUrl(category, slug, lang),
      description,
      scenario: hints.join(' / '),
      tags: keywords,
      source: path.relative(PROJECT_ROOT, file),
      tokens,
    }
  })
  return [...pages, ...topics]
}

function attachMatches(blogs, pages) {
  for (const page of pages) {
    page.suitedArticles = blogs
      .map((b) => ({b, score: overlapScore(page.tokens, b.tokens)}))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5)
      .map((x) => x.b.slug)
      .join('; ')
  }
  for (const blog of blogs) {
    blog.suggestedLinks = pages
      .filter((p) => p.language === 'en')
      .map((p) => ({p, score: overlapScore(blog.tokens, p.tokens)}))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 8)
      .map((x) => `${x.p.slug} (${x.p.category})`)
      .join('; ')
  }
}

function writeCsv(rows) {
  const headers = ['type', 'language', 'category', 'title', 'slug', 'url', 'description', 'scenario', 'tags_or_keywords', 'suited_articles', 'suggested_links', 'source']
  const lines = [headers.join(',')]
  for (const r of rows) {
    lines.push([
      r.type,
      r.language,
      r.category,
      r.title,
      r.slug,
      r.url,
      r.description,
      r.scenario,
      r.tags,
      r.suitedArticles || '',
      r.suggestedLinks || '',
      r.source,
    ].map(csvEscape).join(','))
  }
  fs.writeFileSync(OUT_CSV, lines.join('\n') + '\n')
}

function writeMarkdown(blogs, pages) {
  const canonicalPages = pages.filter((p) => p.language === 'en')
  const lines = []
  lines.push('# Content Link Index')
  lines.push('')
  lines.push(`Generated: ${new Date().toISOString()}`)
  lines.push('')
  lines.push('Purpose: lightweight internal-link and distribution reference for Blog writing, page updates, and content republishing.')
  lines.push('')
  lines.push(`- Blog entries: ${blogs.length}`)
  lines.push(`- Page entries: ${pages.length}`)
  lines.push(`- Canonical EN pages: ${canonicalPages.length}`)
  lines.push(`- Full CSV: \`content-link-index.csv\``)
  lines.push('')
  lines.push('## Canonical Pages')
  lines.push('')
  lines.push('| Type | Title | URL | Scenario | Best-fit Articles |')
  lines.push('|------|-------|-----|----------|-------------------|')
  for (const p of canonicalPages.sort((a, b) => `${a.category}:${a.slug}`.localeCompare(`${b.category}:${b.slug}`))) {
    lines.push(`| ${p.category} | ${p.title.replace(/\|/g, '/')} | ${p.url} | ${(p.scenario || '').replace(/\|/g, '/').slice(0, 160)} | ${(p.suitedArticles || '').replace(/\|/g, '/')} |`)
  }
  lines.push('')
  lines.push('## Published Blogs')
  lines.push('')
  lines.push('| Category | Title | URL | Suggested Page Links |')
  lines.push('|----------|-------|-----|----------------------|')
  for (const b of blogs.sort((a, b) => a.slug.localeCompare(b.slug))) {
    lines.push(`| ${b.category} | ${b.title.replace(/\|/g, '/')} | ${b.url} | ${(b.suggestedLinks || '').replace(/\|/g, '/')} |`)
  }
  fs.writeFileSync(OUT_MD, lines.join('\n') + '\n')
}

function main() {
  const blogs = readBlogs()
  const pages = readPages()
  attachMatches(blogs, pages)
  writeCsv([...pages, ...blogs])
  writeMarkdown(blogs, pages)
  console.log(`Wrote ${path.relative(PROJECT_ROOT, OUT_MD)}`)
  console.log(`Wrote ${path.relative(PROJECT_ROOT, OUT_CSV)}`)
  console.log(`Indexed ${blogs.length} blogs and ${pages.length} pages`)
}

main()
