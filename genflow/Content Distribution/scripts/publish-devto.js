#!/usr/bin/env node
/**
 * Publish draft to DEV.to (semi-auto).
 * Requires DEVTO_API_KEY in .env
 *
 *   node publish-devto.js --draft drafts/devto-slug.md --dry-run
 */

const fs = require('fs')
const path = require('path')
const https = require('https')

const ROOT = path.resolve(__dirname, '..')
const LOGS = path.join(ROOT, 'logs')

function loadEnv() {
  const envPath = path.join(ROOT, '.env')
  if (!fs.existsSync(envPath)) return {}
  const out = {}
  for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
    const t = line.trim()
    if (!t || t.startsWith('#')) continue
    const i = t.indexOf('=')
    if (i > 0) out[t.slice(0, i).trim()] = t.slice(i + 1).trim()
  }
  return out
}

function parseDraft(file) {
  const raw = fs.readFileSync(file, 'utf8')
  const titleM = raw.match(/^#\s+(.+)$/m) || raw.match(/offsite_title:\s*["']?(.+?)["']?\s*$/im)
  const canonicalM = raw.match(/source_url:\s*(\S+)/) || raw.match(/canonical:\s*(\S+)/)
  const title = titleM ? titleM[1].trim() : path.basename(file, '.md')
  const canonical = canonicalM ? canonicalM[1].trim() : ''
  const tagM = raw.match(/tags:\s*\[([^\]]+)\]/i)
  const tags = tagM
    ? tagM[1].split(',').map((t) => t.trim().replace(/['"]/g, '')).filter(Boolean).slice(0, 4)
    : ['ai', 'tutorial']
  const content = raw.replace(/^---[\s\S]*?---\n?/, '').trim()
  return { title, canonical, content, tags }
}

function postDevto(apiKey, payload, method = 'POST', articleId) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ article: payload })
    const path = articleId ? `/api/articles/${articleId}` : '/api/articles'
    const req = https.request(
      {
        hostname: 'dev.to',
        path,
        method,
        headers: {
          'api-key': apiKey,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = ''
        res.on('data', (c) => (data += c))
        res.on('end', () => {
          try {
            resolve({ status: res.statusCode, body: JSON.parse(data) })
          } catch {
            resolve({ status: res.statusCode, body: data })
          }
        })
      }
    )
    req.on('error', reject)
    req.write(body)
    req.end()
  })
}

function appendLog(entry) {
  if (!fs.existsSync(LOGS)) fs.mkdirSync(LOGS, { recursive: true })
  const logFile = path.join(LOGS, `${entry.date}-${entry.platform}-${entry.slug}.json`)
  fs.writeFileSync(logFile, JSON.stringify(entry, null, 2) + '\n')

  const pubPath = path.join(ROOT, 'queue', 'published.json')
  const pub = fs.existsSync(pubPath) ? JSON.parse(fs.readFileSync(pubPath, 'utf8')) : { items: [] }
  pub.updated = entry.date
  pub.items.push(entry)
  fs.writeFileSync(pubPath, JSON.stringify(pub, null, 2) + '\n')
}

async function main() {
  const args = process.argv.slice(2)
  const dryRun = args.includes('--dry-run')
  const draftIdx = args.indexOf('--draft')
  if (draftIdx < 0 || !args[draftIdx + 1]) {
    console.error('Usage: node publish-devto.js --draft PATH [--dry-run]')
    process.exit(2)
  }

  const draftPath = path.resolve(args[draftIdx + 1])
  const { title, canonical, content, tags } = parseDraft(draftPath)
  const slug = path.basename(draftPath, '.md').replace(/^devto-/, '')
  const env = loadEnv()
  const apiKey = env.DEVTO_API_KEY

  const payload = {
    title,
    body_markdown: content,
    published: false,
    canonical_url: canonical || undefined,
    tags,
  }

  console.log('DEV.to publish payload:')
  console.log(JSON.stringify({ ...payload, body_markdown: `[${content.length} chars]` }, null, 2))

  if (dryRun) {
    console.log('\nDRY RUN — not posted')
    process.exit(0)
  }

  if (!apiKey) {
    console.error('Set DEVTO_API_KEY in .env')
    process.exit(2)
  }

  let res = await postDevto(apiKey, payload)
  if (res.status < 200 || res.status >= 300) {
    console.error('DEV.to API error (create draft):', res.status, res.body)
    process.exit(1)
  }

  const id = res.body?.id
  if (!id) {
    console.error('DEV.to draft created but no id returned:', res.body)
    process.exit(1)
  }

  res = await postDevto(apiKey, { ...payload, published: true }, 'PUT', id)
  if (res.status < 200 || res.status >= 300) {
    console.error('DEV.to API error (publish):', res.status, res.body)
    process.exit(1)
  }

  const url = res.body?.url
  appendLog({
    date: new Date().toISOString().slice(0, 10),
    platform: 'devto',
    slug,
    canonical,
    offsite_url: url,
    status: 'published',
  })
  console.log('Published:', url)
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
