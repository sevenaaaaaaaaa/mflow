#!/usr/bin/env node
/**
 * Content Feedback Loop CLI
 *
 *   node feedback-loop-cli.js list
 *   node feedback-loop-cli.js add --id slug --type tool --lang en --query "..." --url "..."
 *   node feedback-loop-cli.js import --csv gsc-export.csv
 *   node feedback-loop-cli.js evaluate
 *   node feedback-loop-cli.js report --month 2026-06 [--out ../feedback/reviews/2026-06.md]
 */

const fs = require('fs')
const path = require('path')
const {
  loadRegister,
  saveRegister,
  importCsv,
  evaluateAll,
  buildReport,
} = require('./lib/feedback-loop')

function parseArgs(argv) {
  const opts = { _: [] }
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--csv') opts.csv = argv[++i]
    else if (a === '--month') opts.month = argv[++i]
    else if (a === '--out') opts.out = argv[++i]
    else if (a === '--id') opts.id = argv[++i]
    else if (a === '--type') opts.type = argv[++i]
    else if (a === '--lang') opts.lang = argv[++i]
    else if (a === '--query') opts.query = argv[++i]
    else if (a === '--url') opts.url = argv[++i]
    else if (a === '--score') opts.score = Number(argv[++i])
    else if (a === '--sample') opts.sample = argv[++i]
    else if (a === '--help' || a === '-h') opts.help = true
    else if (a.startsWith('--')) opts[a.slice(2)] = argv[++i]
    else opts._.push(a)
  }
  return opts
}

function usage() {
  console.log(`Content Feedback Loop CLI

  list
  add --id <slug> --type <type> --lang <lang> --query "..." --url "..." [--score N] [--sample id]
  import --csv <file>
  evaluate
  report --month YYYY-MM [--out path.md]
`)
}

function cmdList() {
  const reg = loadRegister()
  console.log(`Register (${reg.entries.length} entries)\n`)
  for (const e of reg.entries) {
    console.log(
      `${(e.content_id || '').padEnd(28)} ${(e.status || '').padEnd(14)} ${e.focus_query || ''}  sig:${(e.signals || []).join(',')}`
    )
  }
}

function cmdAdd(opts) {
  if (!opts.id || !opts.url) {
    console.error('add requires --id and --url')
    process.exit(2)
  }
  const reg = loadRegister()
  if (reg.entries.some((e) => e.content_id === opts.id)) {
    console.error(`Entry exists: ${opts.id}`)
    process.exit(1)
  }
  reg.entries.push({
    content_id: opts.id,
    content_type: opts.type || 'unknown',
    language: opts.lang || 'en',
    focus_query: opts.query || '',
    published_at: new Date().toISOString().slice(0, 10),
    sample_ref: opts.sample || null,
    rubric_score: opts.score || null,
    url: opts.url,
    impressions_28d: null,
    clicks_28d: null,
    ctr_28d: null,
    avg_position_28d: null,
    signals: [],
    actions: [],
    status: 'watch',
  })
  saveRegister(reg)
  console.log(`Added: ${opts.id}`)
}

function main() {
  const opts = parseArgs(process.argv)
  const cmd = opts._[0]

  if (opts.help || !cmd) {
    usage()
    process.exit(cmd ? 0 : 2)
  }

  switch (cmd) {
    case 'list':
      cmdList()
      break
    case 'add':
      cmdAdd(opts)
      break
    case 'import': {
      if (!opts.csv) {
        console.error('import requires --csv')
        process.exit(2)
      }
      const r = importCsv(path.resolve(opts.csv))
      console.log(`Updated ${r.updated} rows (${r.total} entries total)`)
      break
    }
    case 'evaluate': {
      const results = evaluateAll()
      console.log('Evaluated:\n')
      for (const r of results) {
        console.log(`  ${r.content_id}: ${r.signals.join(', ') || '—'} → ${r.actions.join(', ') || '—'} [${r.status}]`)
      }
      break
    }
    case 'report': {
      const month = opts.month || new Date().toISOString().slice(0, 7)
      const md = buildReport(month)
      if (opts.out) {
        const outPath = path.resolve(opts.out)
        fs.mkdirSync(path.dirname(outPath), { recursive: true })
        fs.writeFileSync(outPath, md)
        console.log(`Wrote: ${outPath}`)
      } else {
        console.log(md)
      }
      break
    }
    default:
      console.error(`Unknown command: ${cmd}`)
      usage()
      process.exit(2)
  }
}

main()
