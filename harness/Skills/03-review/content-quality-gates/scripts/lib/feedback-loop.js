/**
 * Content Feedback Loop — signal evaluation and action suggestions
 * SSOT: Content-Feedback-Loop.md
 */

const fs = require('fs')
const path = require('path')

const REGISTER_PATH = path.join(__dirname, '../../feedback/register.json')

const SIGNAL_ACTIONS = {
  SIG_CTR_LOW: ['ACT_REWRITE_HERO', 'ACT_DEMOTE_SAMPLE'],
  SIG_RANK_STUCK: ['ACT_SERp_REFRESH'],
  SIG_RANK_UP: ['ACT_PROMOTE_SAMPLE', 'ACT_LEDGER_DEFAULT'],
  SIG_BOUNCE_HIGH: ['ACT_REWRITE_FAQ_CTA'],
  SIG_CONV_LOW: ['ACT_REWRITE_FAQ_CTA'],
  SIG_ORM_NEGATIVE: ['ACT_ADD_BAD_SAMPLE', 'ACT_BLOCK_PHRASE'],
  SIG_BRAND_ONLY: ['ACT_SERp_REFRESH'],
  SIG_I18N_GAP: ['ACT_REWRITE_HERO'],
}

function loadRegister() {
  return JSON.parse(fs.readFileSync(REGISTER_PATH, 'utf8'))
}

function saveRegister(data) {
  fs.writeFileSync(REGISTER_PATH, JSON.stringify(data, null, 2) + '\n')
}

function slugFromUrl(url) {
  try {
    const u = new URL(url)
    const parts = u.pathname.split('/').filter(Boolean)
    return parts[parts.length - 1] || null
  } catch {
    return null
  }
}

function parseCsvLine(line) {
  const out = []
  let cur = ''
  let inQ = false
  for (const ch of line) {
    if (ch === '"') {
      inQ = !inQ
      continue
    }
    if (ch === ',' && !inQ) {
      out.push(cur.trim())
      cur = ''
    } else cur += ch
  }
  out.push(cur.trim())
  return out
}

function importCsv(csvPath) {
  const reg = loadRegister()
  const raw = fs.readFileSync(csvPath, 'utf8').trim()
  const lines = raw.split('\n')
  if (lines.length < 2) return { updated: 0, errors: ['empty csv'] }

  const headers = parseCsvLine(lines[0]).map((h) => h.toLowerCase())
  const idx = (name) => headers.indexOf(name)
  let updated = 0

  for (let i = 1; i < lines.length; i++) {
    const cols = parseCsvLine(lines[i])
    const url = cols[idx('url')]
    if (!url) continue
    const slug = slugFromUrl(url)
    let entry = reg.entries.find((e) => e.url === url || e.content_id === slug)
    if (!entry && slug) {
      entry = {
        content_id: slug,
        content_type: 'unknown',
        language: 'en',
        focus_query: '',
        published_at: null,
        url,
        status: 'watch',
        signals: [],
        actions: [],
      }
      reg.entries.push(entry)
    }
    if (!entry) continue

    if (idx('impressions') >= 0) entry.impressions_28d = Number(cols[idx('impressions')])
    if (idx('clicks') >= 0) entry.clicks_28d = Number(cols[idx('clicks')])
    if (idx('ctr') >= 0) entry.ctr_28d = Number(cols[idx('ctr')])
    if (idx('position') >= 0) entry.avg_position_28d = Number(cols[idx('position')])
    if (idx('period_end') >= 0) entry.metrics_period_end = cols[idx('period_end')]
    updated++
  }

  saveRegister(reg)
  return { updated, total: reg.entries.length }
}

function daysSince(isoDate) {
  if (!isoDate) return null
  const d = (Date.now() - new Date(isoDate).getTime()) / 86400000
  return Math.floor(d)
}

function evaluateEntry(entry, thresholds) {
  const signals = []
  const t = thresholds

  if (
    entry.impressions_28d != null &&
    entry.impressions_28d >= t.min_impressions_for_ctr &&
    entry.ctr_28d != null &&
    entry.ctr_28d < t.ctr_low_pct
  ) {
    signals.push('SIG_CTR_LOW')
  }

  const age = daysSince(entry.published_at)
  if (
    age != null &&
    age >= t.rank_stuck_days &&
    entry.avg_position_28d != null &&
    entry.avg_position_28d > t.rank_stuck_position
  ) {
    signals.push('SIG_RANK_STUCK')
  }

  if (entry.avg_position_28d != null && entry.avg_position_28d <= t.rank_up_top) {
    signals.push('SIG_RANK_UP')
  }

  if (entry.bounce_rate_28d != null && entry.bounce_rate_28d >= t.bounce_high_pct) {
    signals.push('SIG_BOUNCE_HIGH')
  }

  if (entry.signals_manual) {
    for (const s of entry.signals_manual) {
      if (!signals.includes(s)) signals.push(s)
    }
  }

  const actions = []
  for (const sig of signals) {
    for (const act of SIGNAL_ACTIONS[sig] || []) {
      if (!actions.includes(act)) actions.push(act)
    }
  }

  if (signals.length > 0 && entry.status === 'watch') entry.status = 'action_needed'
  if (signals.includes('SIG_RANK_UP') && (entry.rubric_score || 0) >= 80) {
    entry.status = 'promoted'
  }

  entry.signals = signals
  entry.actions = actions
  return entry
}

function evaluateAll() {
  const reg = loadRegister()
  for (const entry of reg.entries) {
    evaluateEntry(entry, reg.thresholds)
  }
  saveRegister(reg)
  return reg.entries.map((e) => ({
    content_id: e.content_id,
    signals: e.signals,
    actions: e.actions,
    status: e.status,
  }))
}

function buildReport(month) {
  const reg = loadRegister()
  const needs = reg.entries.filter((e) => e.status === 'action_needed' || (e.signals || []).length > 0)
  const promoted = reg.entries.filter((e) => e.status === 'promoted')

  let md = `# Feedback Review — ${month}\n\n`
  md += `> Auto-generated draft. Edit before archiving.\n\n`
  md += `## Summary\n\n`
  md += `- Pages in register: ${reg.entries.length}\n`
  md += `- Entries with signals: ${needs.length}\n`
  md += `- Promoted candidates: ${promoted.length}\n\n`
  md += `## Action queue\n\n`
  md += `| content_id | focus_query | signals | actions | status |\n`
  md += `|---|---|---|---|---|\n`
  for (const e of needs) {
    md += `| ${e.content_id} | ${e.focus_query || '—'} | ${(e.signals || []).join(', ')} | ${(e.actions || []).join(', ')} | ${e.status} |\n`
  }
  if (needs.length === 0) md += `| — | — | — | — | — |\n`

  md += `\n## Promoted candidates\n\n`
  for (const e of promoted) {
    md += `- **${e.content_id}** (${e.focus_query}) — consider \`ACT_PROMOTE_SAMPLE\`\n`
  }
  if (promoted.length === 0) md += `- None this period\n`

  md += `\n## Suggested mechanism updates\n\n`
  const allActions = new Set(needs.flatMap((e) => e.actions || []))
  if (allActions.has('ACT_TIGHTEN_PREFLIGHT') || allActions.has('ACT_BLOCK_PHRASE')) {
    md += `- Review \`anti-slop-rules.js\` and audit BLOCKED_PHRASES\n`
  }
  if (allActions.has('ACT_PROMOTE_SAMPLE') || allActions.has('ACT_DEMOTE_SAMPLE')) {
    md += `- Update \`samples/index.json\` verdicts\n`
  }
  if (allActions.has('ACT_LEDGER_DEFAULT')) {
    md += `- Update storyline Ledger defaults in Content-Production-Ledger.md\n`
  }

  return md
}

module.exports = {
  REGISTER_PATH,
  loadRegister,
  saveRegister,
  importCsv,
  evaluateAll,
  buildReport,
  evaluateEntry,
  SIGNAL_ACTIONS,
}
