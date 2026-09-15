#!/usr/bin/env node
/**
 * Publish draft to Medium (semi-auto).
 * Requires MEDIUM_INTEGRATION_TOKEN and MEDIUM_USER_ID in .env
 *
 *   node publish-medium.js --draft drafts/medium-slug.md
 *   node publish-medium.js --draft drafts/medium-slug.md --dry-run
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
  const content = raw.replace(/^---[\s\S]*?---\n?/, '').trim()
  return { title, canonical, content }
}

function postMedium(token, userId, payload) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(payload)
    const req = https.request(
      {
        hostname: 'api.medium.com',
        path: `/v1/users/${userId}/posts`,
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
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
    console.error('Usage: node publish-medium.js --draft PATH [--dry-run]')
    process.exit(2)
  }

  const draftPath = path.resolve(args[draftIdx + 1])
  const { title, canonical, content } = parseDraft(draftPath)
  const slug = path.basename(draftPath, '.md').replace(/^medium-/, '')
  const env = loadEnv()
  const token = env.MEDIUM_INTEGRATION_TOKEN
  const userId = env.MEDIUM_USER_ID

  const payload = {
    title,
    contentFormat: 'markdown',
    content,
    publishStatus: 'public',
    canonicalUrl: canonical || undefined,
    tags: ['ai', 'design', 'lovart'],
  }

  console.log('Medium publish payload:')
  console.log(JSON.stringify({ ...payload, content: `[${content.length} chars]` }, null, 2))

  if (dryRun) {
    console.log('\nDRY RUN — not posted')
    process.exit(0)
  }

  if (!token || !userId) {
    console.error('Set MEDIUM_INTEGRATION_TOKEN and MEDIUM_USER_ID in .env')
    process.exit(2)
  }

  const res = await postMedium(token, userId, payload)
  if (res.status < 200 || res.status >= 300) {
    console.error('Medium API error:', res.status, res.body)
    process.exit(1)
  }

  const url = res.body?.data?.url || res.body?.data?.publishUrl
  appendLog({
    date: new Date().toISOString().slice(0, 10),
    platform: 'medium',
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
