#!/usr/bin/env node
/**
 * Blogger OAuth helper (Desktop app, redirect http://localhost).
 *
 *   node scripts/blogger-oauth.js              # print + open auth URL
 *   node scripts/blogger-oauth.js --code CODE  # exchange code → refresh_token in .env
 */

const fs = require('fs')
const path = require('path')
const https = require('https')
const { execSync } = require('child_process')

const ROOT = path.resolve(__dirname, '..')
const ENV_PATH = path.join(ROOT, '.env')
const REDIRECT_URI = 'http://localhost'
const SCOPE = 'https://www.googleapis.com/auth/blogger'

function loadEnv() {
  if (!fs.existsSync(ENV_PATH)) return {}
  const out = {}
  for (const line of fs.readFileSync(ENV_PATH, 'utf8').split('\n')) {
    const t = line.trim()
    if (!t || t.startsWith('#')) continue
    const i = t.indexOf('=')
    if (i > 0) out[t.slice(0, i).trim()] = t.slice(i + 1).trim()
  }
  return out
}

function upsertEnv(key, value) {
  let lines = fs.existsSync(ENV_PATH) ? fs.readFileSync(ENV_PATH, 'utf8').split('\n') : []
  let found = false
  lines = lines.map((line) => {
    if (line.startsWith(`${key}=`)) {
      found = true
      return `${key}=${value}`
    }
    return line
  })
  if (!found) lines.push(`${key}=${value}`)
  fs.writeFileSync(ENV_PATH, lines.filter((l, i, a) => i < a.length - 1 || l !== '').join('\n') + '\n')
}

function authUrl(clientId) {
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: REDIRECT_URI,
    response_type: 'code',
    scope: SCOPE,
    access_type: 'offline',
    prompt: 'consent',
  })
  return `https://accounts.google.com/o/oauth2/v2/auth?${params}`
}

function exchangeCode(clientId, clientSecret, code) {
  const body = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    code,
    grant_type: 'authorization_code',
    redirect_uri: REDIRECT_URI,
  }).toString()

  return new Promise((resolve, reject) => {
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

async function main() {
  const env = loadEnv()
  const clientId = env.GOOGLE_CLIENT_ID
  const clientSecret = env.GOOGLE_CLIENT_SECRET
  if (!clientId || !clientSecret) {
    console.error('Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env first')
    process.exit(2)
  }

  const codeIdx = process.argv.indexOf('--code')
  if (codeIdx < 0) {
    const url = authUrl(clientId)
    console.log('1. 浏览器打开以下链接，用 Blogger 所在 Google 账号登录并授权：\n')
    console.log(url)
    console.log('\n2. 授权后会跳转到 http://localhost/?code=...（页面可能打不开，正常）')
    console.log('3. 从地址栏复制 code= 后面整段，运行：')
    console.log('   node scripts/blogger-oauth.js --code PASTE_CODE_HERE')
    try {
      execSync(`open "${url}"`, { stdio: 'ignore' })
      console.log('\n（已在浏览器打开授权页）')
    } catch {
      // ignore
    }
    return
  }

  const code = process.argv[codeIdx + 1]
  if (!code) {
    console.error('Missing code after --code')
    process.exit(2)
  }

  const res = await exchangeCode(clientId, clientSecret, code.trim())
  if (res.status < 200 || res.status >= 300 || res.body?.error) {
    console.error('Token exchange failed:', res.status, res.body)
    process.exit(1)
  }

  const refresh = res.body.refresh_token
  if (!refresh) {
    console.error('No refresh_token in response. Revoke app access at https://myaccount.google.com/permissions and retry with prompt=consent.')
    console.error('Response:', res.body)
    process.exit(1)
  }

  upsertEnv('GOOGLE_REFRESH_TOKEN', refresh)
  console.log('✓ GOOGLE_REFRESH_TOKEN 已写入 .env')
  console.log('\n下一步：')
  console.log('  node scripts/publish-blogger.js --list-blogs')
  console.log('  # 把 blog id 填入 BLOGGER_BLOG_ID')
}

main().catch((e) => {
  console.error(e.message || e)
  process.exit(1)
})
