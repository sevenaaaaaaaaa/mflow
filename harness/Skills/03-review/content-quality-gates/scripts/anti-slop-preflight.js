#!/usr/bin/env node
/**
 * Anti-Slop preflight — standalone runner (Blog MD + composite JSON).
 *
 * Usage:
 *   node anti-slop-preflight.js --file path/to/article.md
 *   node anti-slop-preflight.js --file path/to/tool-en.json
 *   node anti-slop-preflight.js --dir path/to/blog/folder --glob "*.md"
 *   node anti-slop-preflight.js --file article.md --strict
 *   node anti-slop-preflight.js --file article.md --report out.json
 *
 * Integrate into studio preflight:
 *   const { checkBlogMarkdown, checkCompositePage, summarize } = require('./lib/anti-slop-rules.js')
 */

const fs = require('fs')
const path = require('path')
const {
  checkBlogMarkdown,
  checkCompositePage,
  summarize,
  proQualityCheck,
  parseFrontmatter,
} = require('./lib/anti-slop-rules')
const { lintMarkdownImages, lintCompositeImages } = require('./lib/remote-image-lint')

function parseArgs(argv) {
  const opts = { strict: false, glob: '*.md', pro: false, skipRemote: false }
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--strict') opts.strict = true
    else if (a === '--pro') opts.pro = true
    else if (a === '--skip-remote') opts.skipRemote = true
    else if (a === '--file') opts.file = argv[++i]
    else if (a === '--dir') opts.dir = argv[++i]
    else if (a === '--glob') opts.glob = argv[++i]
    else if (a === '--report') opts.report = argv[++i]
    else if (a === '--help' || a === '-h') opts.help = true
  }
  return opts
}

function usage() {
  console.log(`Anti-Slop Preflight (v2.1 — L1 + L1b + L2 + L2b pro-quality)

  node anti-slop-preflight.js --file <path> [--strict] [--pro] [--skip-remote] [--report out.json]
  node anti-slop-preflight.js --dir <folder> [--glob "*.md"] [--strict] [--pro] [--skip-remote]

  --strict       Treat WARNs as BLOCK for CI
  --pro          Run L2 pro-quality checks (regression + first-person + table + lang mix + bullets)
  --skip-remote  Skip remote image HTTP/dimension checks

Exit codes: 0 pass, 1 BLOCK/fail, 2 usage error
`)
}

function isJsonFile(p) {
  return /\.json$/i.test(p)
}

async function checkFile(filePath, strict, pro, skipRemote) {
  const rel = path.basename(filePath)
  const raw = fs.readFileSync(filePath, 'utf8')
  if (isJsonFile(filePath)) {
    let page
    try {
      page = JSON.parse(raw)
    } catch (e) {
      return { file: rel, failed: true, issues: [{ code: 'JSON_PARSE', severity: 'BLOCK', message: e.message }] }
    }
    const result = checkCompositePage(page, { strict })
    // L2 pro-quality for composite pages (bodyJson text)
    if (pro) {
      let bodyText = ''
      try {
        const sections = typeof page.bodyJson === 'string' ? JSON.parse(page.bodyJson) : page.bodyJson
        if (Array.isArray(sections)) {
          bodyText = sections.map(s => JSON.stringify(s)).join('\n')
        }
      } catch {}
      const lang = page.language || 'en'
      const pqIssues = proQualityCheck(bodyText, { strict, language: lang })
      result.issues = result.issues.concat(pqIssues)
    }
    if (!skipRemote) {
      const remoteIssues = await lintCompositeImages(page)
      result.issues = result.issues.concat(remoteIssues)
    }
    const sum = summarize(result.issues, strict)
    return {
      file: rel,
      ...sum,
      issues: result.issues,
      meta: {
        lang: result.lang,
        sections: result.sectionCount,
        archetype: result.archetype || 'page',
        pq: pro ? 'enabled' : 'off',
        remote: skipRemote ? 'skipped' : 'enabled',
      },
    }
  }
  // Markdown blog
  const result = checkBlogMarkdown(raw, { strict })
  // L2 pro-quality for markdown
  if (pro) {
    // Strip frontmatter for body text
    const bodyText = raw.replace(/^---[\s\S]*?---\n/, '').trim()
    // Extract H2 and FAQ titles for PQ_FAQ_IS_H2_COPY check
    const h2Matches = [...bodyText.matchAll(/^##\s+(.+)$/gm)]
    const h2Titles = h2Matches.map(m => m[1].trim())
    const faqTitles = []
    const faqHeadings = ['FAQ', '常见问题', 'よくある質問', 'Domande frequenti', 'Preguntas frecuentes',
      'Questions fréquentes', 'Häufig gestellte Fragen', 'Perguntas frequentes',
      '자주 묻는 질문', 'Часто задаваемые вопросы']
    for (const fh of faqHeadings) {
      const faqIdx = bodyText.indexOf(`## ${fh}`)
      if (faqIdx > 0) {
        const faqSection = bodyText.slice(faqIdx)
        const qMatches = faqSection.matchAll(/^###\s+(.+)$/gm)
        for (const m of qMatches) faqTitles.push(m[1].trim())
        break
      }
    }
    const lang = result.lang
    const pqIssues = proQualityCheck(bodyText, { strict, language: lang, h2Titles, faqTitles })
    result.issues = result.issues.concat(pqIssues)
  }
  if (!skipRemote) {
    const frontmatter = result.frontmatter || parseFrontmatter(raw)
    const remoteIssues = await lintMarkdownImages(raw, frontmatter)
    result.issues = result.issues.concat(remoteIssues)
  }
  const sum = summarize(result.issues, strict)
  return {
    file: rel,
    ...sum,
    issues: result.issues,
    meta: {
      lang: result.lang,
      h2: result.h2Count,
      faq: result.faqCount,
      archetype: result.archetype || 'generic',
      pq: pro ? 'enabled' : 'off',
      remote: skipRemote ? 'skipped' : 'enabled',
    },
  }
}

function listFiles(dir, glob) {
  const ext = glob.replace('*', '')
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(ext.replace(/^\./, '')) || (ext === '.md' && f.endsWith('.md')))
    .map((f) => path.join(dir, f))
}

function printIssues(result) {
  const icon = result.failed ? 'FAIL' : 'OK'
  console.log(`\n[${icon}] ${result.file}`)
  if (result.meta) console.log(`  meta: ${JSON.stringify(result.meta)}`)
  for (const i of result.issues || []) {
    console.log(`  ${i.severity} ${i.code}: ${i.message}${i.detail ? ` — ${i.detail}` : ''}`)
  }
}

async function main() {
  const opts = parseArgs(process.argv)
  if (opts.help || (!opts.file && !opts.dir)) {
    usage()
    process.exit(2)
  }

  const files = opts.file ? [path.resolve(opts.file)] : listFiles(path.resolve(opts.dir), opts.glob)
  const results = []
  for (const f of files) {
    results.push(await checkFile(f, opts.strict, opts.pro, opts.skipRemote))
  }
  let anyFail = false

  for (const r of results) {
    printIssues(r)
    if (r.failed) anyFail = true
  }

  const report = {
    at: new Date().toISOString(),
    strict: opts.strict,
    total: results.length,
    failed: results.filter((r) => r.failed).length,
    results,
  }

  if (opts.report) {
    fs.mkdirSync(path.dirname(path.resolve(opts.report)), { recursive: true })
    fs.writeFileSync(path.resolve(opts.report), JSON.stringify(report, null, 2))
    console.log(`\nReport: ${opts.report}`)
  }

  console.log(`\n--- ${report.failed}/${report.total} failed ---`)
  process.exit(anyFail ? 1 : 0)
}

main().catch((error) => {
  console.error(error.stack || error.message)
  process.exit(1)
})
