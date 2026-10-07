#!/usr/bin/env node
/**
 * Publish draft to GitHub Discussions (GraphQL API).
 *
 *   node publish-github-discussions.js --draft drafts/github-discussions-slug.md
 *   node publish-github-discussions.js --draft drafts/github-discussions-slug.md --dry-run
 *   node publish-github-discussions.js --list-categories
 *
 * Requires in .env:
 *   GITHUB_TOKEN
 *   GITHUB_DISCUSSIONS_REPO=owner/repo
 *   GITHUB_DISCUSSION_CATEGORY=General   (optional, default General)
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
  const title = titleM ? titleM[1].trim() : path.basename(file, '.md')
  const body = raw.replace(/^---[\s\S]*?---\n?/, '').trim()
  return { title, body }
}

function graphql(token, query, variables = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ query, variables })
    const req = https.request(
      {
        hostname: 'api.github.com',
        path: '/graphql',
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
          'User-Agent': 'content-distribution',
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

async function resolveRepoAndCategory(token, owner, name, categoryName) {
  const query = `
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
        hasDiscussionsEnabled
        discussionCategories(first: 25) {
          nodes { id name slug }
        }
      }
    }
  `
  const res = await graphql(token, query, { owner, name })
  if (res.body?.errors?.length) {
    throw new Error(res.body.errors.map((e) => e.message).join('; '))
  }
  const repo = res.body?.data?.repository
  if (!repo) throw new Error(`Repository not found: ${owner}/${name}`)
  if (repo.hasDiscussionsEnabled === false) {
    throw new Error(`Discussions not enabled on ${owner}/${name}. Enable in repo Settings → General.`)
  }
  const categories = repo.discussionCategories?.nodes || []
  const category =
    categories.find((c) => c.name.toLowerCase() === categoryName.toLowerCase()) ||
    categories.find((c) => c.slug === categoryName.toLowerCase()) ||
    categories[0]
  if (!category) throw new Error('No discussion categories found')
  return { repositoryId: repo.id, categoryId: category.id, categoryName: category.name, categories }
}

async function createDiscussion(token, repositoryId, categoryId, title, body) {
  const mutation = `
    mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: {
        repositoryId: $repositoryId
        categoryId: $categoryId
        title: $title
        body: $body
      }) {
        discussion { id url title number }
      }
    }
  `
  const res = await graphql(token, mutation, { repositoryId, categoryId, title, body })
  if (res.body?.errors?.length) {
    throw new Error(res.body.errors.map((e) => e.message).join('; '))
  }
  return res.body?.data?.createDiscussion?.discussion
}

function appendLog(entry) {
  if (!fs.existsSync(LOGS)) fs.mkdirSync(LOGS, { recursive: true })
  const logFile = path.join(LOGS, `${entry.date}-github_discussions-${entry.slug}.json`)
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
  const listCategories = args.includes('--list-categories')
  const env = loadEnv()
  const token = env.GITHUB_TOKEN
  const repoSpec = env.GITHUB_DISCUSSIONS_REPO || ''
  const categoryName = env.GITHUB_DISCUSSION_CATEGORY || 'General'

  if (!token || !repoSpec) {
    console.error('Set GITHUB_TOKEN and GITHUB_DISCUSSIONS_REPO in .env')
    console.error('See scripts/setup-github-discussions.md')
    process.exit(2)
  }

  const [owner, name] = repoSpec.split('/')
  if (!owner || !name) {
    console.error('GITHUB_DISCUSSIONS_REPO must be owner/repo')
    process.exit(2)
  }

  const { repositoryId, categoryId, categoryName: resolvedCategory, categories } =
    await resolveRepoAndCategory(token, owner, name, categoryName)

  if (listCategories) {
    console.log(`Categories for ${owner}/${name}:`)
    for (const c of categories) console.log(`  - ${c.name} (${c.slug}) id=${c.id}`)
    process.exit(0)
  }

  const draftIdx = args.indexOf('--draft')
  if (draftIdx < 0 || !args[draftIdx + 1]) {
    console.error('Usage: node publish-github-discussions.js --draft PATH [--dry-run]')
    console.error('       node publish-github-discussions.js --list-categories')
    process.exit(2)
  }

  const draftPath = path.resolve(args[draftIdx + 1])
  const { title, body } = parseDraft(draftPath)
  const slug = path.basename(draftPath, '.md').replace(/^github-discussions-/, '')

  console.log('GitHub Discussions publish:')
  console.log(JSON.stringify({
    repo: `${owner}/${name}`,
    category: resolvedCategory,
    title,
    body: `[${body.length} chars]`,
  }, null, 2))

  if (dryRun) {
    console.log('\nDRY RUN — not posted')
    process.exit(0)
  }

  const discussion = await createDiscussion(token, repositoryId, categoryId, title, body)
  const url = discussion?.url
  appendLog({
    date: new Date().toISOString().slice(0, 10),
    platform: 'github_discussions',
    slug,
    offsite_url: url,
    status: 'published',
  })
  console.log('Published:', url)
}

main().catch((e) => {
  console.error(e.message || e)
  process.exit(1)
})
