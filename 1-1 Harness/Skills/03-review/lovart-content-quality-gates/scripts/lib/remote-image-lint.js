const http = require('http')
const https = require('https')

const MAX_BYTES = 65536
const MAX_REDIRECTS = 4

function looksLikeImageUrl(url, pathHint = '') {
  return (
    /^https?:\/\//i.test(String(url || '')) &&
    (/\.(png|jpe?g|webp|gif|svg)(\?|$)/i.test(url) ||
      /(assets-persist|cdn\.sanity|liblib|image|images|cover)/i.test(`${url} ${pathHint}`))
  )
}

function requestBuffer(url, opts = {}, redirects = 0) {
  return new Promise((resolve, reject) => {
    const target = new URL(url)
    const lib = target.protocol === 'http:' ? http : https
    const req = lib.request(
      target,
      {
        method: opts.method || 'GET',
        headers: opts.headers || {},
        timeout: opts.timeout || 12000,
      },
      (res) => {
        const status = res.statusCode || 0
        const location = res.headers.location
        if ([301, 302, 303, 307, 308].includes(status) && location && redirects < MAX_REDIRECTS) {
          const next = new URL(location, target).toString()
          res.resume()
          resolve(requestBuffer(next, opts, redirects + 1))
          return
        }

        const chunks = []
        let total = 0
        res.on('data', (chunk) => {
          total += chunk.length
          if (total <= MAX_BYTES) chunks.push(chunk)
          if (total > MAX_BYTES) res.destroy()
        })
        res.on('close', () =>
          resolve({
            statusCode: status,
            headers: res.headers,
            body: Buffer.concat(chunks),
            finalUrl: target.toString(),
          }),
        )
        res.on('end', () =>
          resolve({
            statusCode: status,
            headers: res.headers,
            body: Buffer.concat(chunks),
            finalUrl: target.toString(),
          }),
        )
      },
    )
    req.on('timeout', () => req.destroy(new Error('timeout')))
    req.on('error', reject)
    req.end()
  })
}

function parsePng(buffer) {
  if (buffer.length < 24) return null
  if (buffer.toString('hex', 0, 8) !== '89504e470d0a1a0a') return null
  return {
    width: buffer.readUInt32BE(16),
    height: buffer.readUInt32BE(20),
    format: 'png',
  }
}

function parseGif(buffer) {
  if (buffer.length < 10) return null
  const sig = buffer.toString('ascii', 0, 6)
  if (sig !== 'GIF87a' && sig !== 'GIF89a') return null
  return {
    width: buffer.readUInt16LE(6),
    height: buffer.readUInt16LE(8),
    format: 'gif',
  }
}

function parseJpeg(buffer) {
  if (buffer.length < 4 || buffer[0] !== 0xff || buffer[1] !== 0xd8) return null
  let offset = 2
  while (offset + 9 < buffer.length) {
    if (buffer[offset] !== 0xff) {
      offset += 1
      continue
    }
    const marker = buffer[offset + 1]
    const size = buffer.readUInt16BE(offset + 2)
    if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(marker)) {
      return {
        width: buffer.readUInt16BE(offset + 7),
        height: buffer.readUInt16BE(offset + 5),
        format: 'jpeg',
      }
    }
    if (size < 2) break
    offset += 2 + size
  }
  return null
}

function parseWebp(buffer) {
  if (buffer.length < 30) return null
  if (buffer.toString('ascii', 0, 4) !== 'RIFF' || buffer.toString('ascii', 8, 12) !== 'WEBP') return null
  const chunk = buffer.toString('ascii', 12, 16)
  if (chunk === 'VP8X') {
    return {
      width: 1 + buffer.readUIntLE(24, 3),
      height: 1 + buffer.readUIntLE(27, 3),
      format: 'webp',
    }
  }
  return null
}

function parseImageSize(buffer) {
  return parsePng(buffer) || parseGif(buffer) || parseJpeg(buffer) || parseWebp(buffer)
}

async function inspectImage(url) {
  const res = await requestBuffer(
    url,
    {
      method: 'GET',
      headers: {
        Range: `bytes=0-${MAX_BYTES - 1}`,
        'User-Agent': 'Lovart-Quality-Gates/1.0',
      },
    },
    0,
  )

  const contentType = String(res.headers['content-type'] || '')
  const contentLength = Number(res.headers['content-length'] || 0)
  const size = parseImageSize(res.body)
  return {
    statusCode: res.statusCode,
    finalUrl: res.finalUrl,
    contentType,
    contentLength,
    width: size?.width || null,
    height: size?.height || null,
    format: size?.format || null,
  }
}

function collectMarkdownImageRefs(raw, frontmatter = {}) {
  const refs = []
  if (frontmatter.cover_url && looksLikeImageUrl(frontmatter.cover_url, 'cover_url')) {
    refs.push({ url: frontmatter.cover_url, role: 'cover', alt: frontmatter.title || '' })
  }
  for (const m of String(raw || '').matchAll(/!\[([^\]]*)\]\((https?:\/\/[^)]+)\)/g)) {
    refs.push({ url: m[2], role: 'body-image', alt: m[1].trim() })
  }
  for (const m of String(raw || '').matchAll(/<img[^>]+src=["'](https?:\/\/[^"']+)["'][^>]*alt=["']([^"']*)["'][^>]*>/gi)) {
    refs.push({ url: m[1], role: 'body-image', alt: m[2].trim() })
  }
  return dedupeRefs(refs)
}

function collectCompositeImageRefs(page) {
  const refs = []
  function walk(node, path = []) {
    if (Array.isArray(node)) {
      node.forEach((item, idx) => walk(item, path.concat(String(idx))))
      return
    }
    if (!node || typeof node !== 'object') return
    for (const [key, value] of Object.entries(node)) {
      const nextPath = path.concat(key)
      if (typeof value === 'string') {
        const pathHint = nextPath.join('.')
        if ((key === 'src' || key === 'url') && looksLikeImageUrl(value, pathHint)) {
          refs.push({
            url: value,
            role: classifyRole(pathHint),
            alt: typeof node.alt === 'string' ? node.alt.trim() : '',
            pathHint,
          })
        }
      } else {
        walk(value, nextPath)
      }
    }
  }
  walk(page)
  return dedupeRefs(refs)
}

function dedupeRefs(refs) {
  const seen = new Map()
  for (const ref of refs) {
    if (!seen.has(ref.url)) seen.set(ref.url, ref)
  }
  return [...seen.values()]
}

function classifyRole(pathHint) {
  const lower = String(pathHint || '').toLowerCase()
  if (/(ogimage|seo\.ogimage)/.test(lower)) return 'og'
  if (/(cover|cover_url)/.test(lower)) return 'cover'
  if (/hero/.test(lower)) return 'hero'
  if (/avatar/.test(lower)) return 'avatar'
  return 'image'
}

function evaluateImageRef(ref, info) {
  const issues = []
  const add = (code, severity, message, detail) => issues.push({ code, severity, message, detail })

  if (info.statusCode < 200 || info.statusCode >= 400) {
    add('IMG_HTTP', 'BLOCK', `Image URL returned HTTP ${info.statusCode}`, ref.url)
    return issues
  }
  if (!/^image\//i.test(info.contentType) && !info.format) {
    add('IMG_CONTENT_TYPE', 'WARN', `Remote asset may not be an image (${info.contentType || 'unknown'})`, ref.url)
  }

  if (!ref.alt && ref.role !== 'avatar') {
    add('IMG_ALT', 'WARN', `Missing alt text for ${ref.role} image`, ref.url)
  }

  if (!info.width || !info.height) {
    add('IMG_DIMENSIONS', 'WARN', 'Could not detect image dimensions', ref.url)
    return issues
  }

  const aspect = info.width / info.height
  if (info.width < 300 || info.height < 200) {
    add('IMG_TINY', 'BLOCK', `Image too small: ${info.width}x${info.height}`, ref.url)
  }
  if (ref.role !== 'avatar' && info.width <= 192 && info.height <= 192) {
    add('IMG_ICONISH', 'BLOCK', `Image looks icon-sized: ${info.width}x${info.height}`, ref.url)
  }
  if (ref.role === 'og' && (info.width < 1200 || info.height < 630)) {
    add('IMG_OG_SIZE', 'WARN', `OG image smaller than 1200x630: ${info.width}x${info.height}`, ref.url)
  }
  if ((ref.role === 'hero' || ref.role === 'cover') && (info.width < 800 || info.height < 450)) {
    add('IMG_HERO_SIZE', 'WARN', `${ref.role} image smaller than 800x450: ${info.width}x${info.height}`, ref.url)
  }
  if (aspect > 4 || aspect < 0.25) {
    add('IMG_ASPECT', 'WARN', `Extreme aspect ratio ${aspect.toFixed(2)} (${info.width}x${info.height})`, ref.url)
  }

  return issues
}

async function lintMarkdownImages(raw, frontmatter = {}) {
  const refs = collectMarkdownImageRefs(raw, frontmatter)
  return lintRefs(refs)
}

async function lintCompositeImages(page) {
  const refs = collectCompositeImageRefs(page)
  return lintRefs(refs)
}

async function lintRefs(refs) {
  const issues = []
  for (const ref of refs) {
    try {
      const info = await inspectImage(ref.url)
      issues.push(...evaluateImageRef(ref, info))
    } catch (error) {
      issues.push({
        code: 'IMG_HTTP',
        severity: 'BLOCK',
        message: `Image check failed: ${error.message}`,
        detail: ref.url,
      })
    }
  }
  return issues
}

module.exports = {
  lintMarkdownImages,
  lintCompositeImages,
}
