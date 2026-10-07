#!/usr/bin/env node
/**
 * Publish draft to Google Blogger (API v3).
 *
 *   node publish-blogger.js --draft drafts/blogger-slug.md --dry-run
 *   node publish-blogger.js --list-blogs
 *
 * Requires in .env:
 *   GOOGLE_CLIENT_ID
 *   GOOGLE_CLIENT_SECRET
 *   GOOGLE_REFRESH_TOKEN
 *   BLOGGER_BLOG_ID
 *
 * Setup: scripts/setup-blogger.md
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
  const md = raw.replace(/^---[\s\S]*?---\n?/, '').trim()
  return { title, canonical, md }
}

function escapeHtml(s) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function inlineMd(text) {
  return escapeHtml(text)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>')
}

function markdownToHtml(md) {
  const lines = md.split('\n')
  const out = []
  let inList = false

  const closeList = () => {
    if (inList) {
      out.push('</ul>')
      inList = false
    }
  }

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) {
      closeList()
      continue
    }
    const h = trimmed.match(/^(#{1,3})\s+(.+)$/)
    if (h) {
      closeList()
      const level = h[1].length
      out.push(`<h${level}>${inlineMd(h[2])}</h${level}>`)
      continue
    }
    const li = trimmed.match(/^[-*]\s+(.+)$/)
    if (li) {
      if (!inList) {
        out.push('<ul>')
        inList = true
      }
      out.push(`<li>${inlineMd(li[1])}</li>`)
      continue
    }
    closeList()
    out.push(`<p>${inlineMd(trimmed)}</p>`)
  }
  closeList()
  return out.join('\n')
}

function httpsJson(method, url, headers, bodyObj) {
  return new Promise((resolve, reject) => {
    const u = new URL(url)
    const body = bodyObj ? JSON.stringify(bodyObj) : null
    const req = https.request(
      {
        hostname: u.hostname,
        path: u.pathname + u.search,
        method,
        headers: {
          ...headers,
          ...(body ? { 'Content-Length': Buffer.byteLength(body) } : {}),
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
    if (body) req.write(body)
    req.end()
  })
}

async function getAccessToken(env) {
  const params = new URLSearchParams({
    client_id: env.GOOGLE_CLIENT_ID,
    client_secret: env.GOOGLE_CLIENT_SECRET,
    refresh_token: env.GOOGLE_REFRESH_TOKEN,
    grant_type: 'refresh_token',
  })
  return new Promise((resolve, reject) => {
    const body = params.toString()
    const req = https.request(
      {
        hostname: 'oauth2.googleapis.com',
        path: '/token',
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Content-Length': Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = ''
        res.on('data', (c) => (data += c))
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data)
            if (parsed.error) reject(new Error(parsed.error_description || parsed.error))
            else resolve(parsed.access_token)
          } catch (e) {
            reject(e)
          }
        })
      }
    )
    req.on('error', reject)
    req.write(body)
    req.end()
  })
}

async function fetchUserBlogs(accessToken) {
  const res = await httpsJson(
    'GET',
    'https://www.googleapis.com/blogger/v3/users/self/blogs',
    { Authorization: `Bearer ${accessToken}` },
    null
  )
  if (res.status < 200 || res.status >= 300) {
    throw new Error(`Blogger list error ${res.status}: ${JSON.stringify(res.body)}`)
  }
  return res.body?.items || []
}

async function insertPost(accessToken, blogId, title, content, canonical) {
  let html = markdownToHtml(content)
  if (canonical) {
    html += `\n<p><em>Canonical source: <a href="${escapeHtml(canonical)}">${escapeHtml(canonical)}</a></em></p>`
  }
  const res = await httpsJson(
    'POST',
    `https://www.googleapis.com/blogger/v3/blogs/${blogId}/posts/`,
    {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    { title, content: html }
  )
  if (res.status < 200 || res.status >= 300) {
    throw new Error(`Blogger insert error ${res.status}: ${JSON.stringify(res.body)}`)
  }
  return res.body
}

function appendLog(entry) {
  if (!fs.existsSync(LOGS)) fs.mkdirSync(LOGS, { recursive: true })
  const logFile = path.join(ROOT, 'logs', `${entry.date}-blogger-${entry.slug}.json`)
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
  const wantListBlogs = args.includes('--list-blogs')
  const env = loadEnv()

  const required = ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'GOOGLE_REFRESH_TOKEN']
  for (const k of required) {
    if (!env[k]) {
      console.error(`Missing ${k} in .env — see scripts/setup-blogger.md`)
      process.exit(2)
    }
  }

  const accessToken = await getAccessToken(env)

  if (wantListBlogs) {
    const blogs = await fetchUserBlogs(accessToken)
    console.log('Your Blogger blogs:')
    for (const b of blogs) {
      console.log(`  - ${b.name} id=${b.id} url=${b.url}`)
    }
    process.exit(0)
  }

  if (!env.BLOGGER_BLOG_ID) {
    console.error('Set BLOGGER_BLOG_ID in .env (run with --list-blogs to find it)')
    process.exit(2)
  }

  const draftIdx = args.indexOf('--draft')
  if (draftIdx < 0 || !args[draftIdx + 1]) {
    console.error('Usage: node publish-blogger.js --draft PATH [--dry-run]')
    console.error('       node publish-blogger.js --list-blogs')
    process.exit(2)
  }

  const draftPath = path.resolve(args[draftIdx + 1])
  const { title, canonical, md } = parseDraft(draftPath)
  const slug = path.basename(draftPath, '.md').replace(/^blogger-/, '')

  console.log('Blogger publish:')
  console.log(JSON.stringify({
    blog_id: env.BLOGGER_BLOG_ID,
    title,
    canonical,
    content: `[${md.length} chars markdown]`,
  }, null, 2))

  if (dryRun) {
    console.log('\nDRY RUN — not posted')
    process.exit(0)
  }

  const post = await insertPost(accessToken, env.BLOGGER_BLOG_ID, title, md, canonical)
  appendLog({
    date: new Date().toISOString().slice(0, 10),
    platform: 'blogger',
    slug,
    canonical,
    offsite_url: post.url,
    status: 'published',
  })
  console.log('Published:', post.url)
}

main().catch((e) => {
  console.error(e.message || e)
  process.exit(1)
})
