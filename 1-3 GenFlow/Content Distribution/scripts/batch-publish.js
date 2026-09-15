#!/usr/bin/env node
/**
 * @deprecated 请用 dispatch-publish.js（国内 Wechatsync + 海外 MCP）
 * 批量发布：预检 → 按 config/platforms.json 路由到各发布器
 *
 *   node scripts/batch-publish.js --manifest queue/batch-manifest.json
 *   node scripts/batch-publish.js --manifest queue/batch-manifest.json --dry-run
 *   node scripts/batch-publish.js --manifest queue/batch-manifest.json --only medium,devto,zhihu
 *   node scripts/batch-publish.js --manifest queue/batch-manifest.json --skip-wechatsync-wait
 */

const fs = require('fs')
const path = require('path')
const { spawnSync } = require('child_process')

const ROOT = path.resolve(__dirname, '..')
const CONFIG = path.join(ROOT, 'config', 'platforms.json')

function parseArgs(argv) {
  const out = { dry_run: false, skip_wechatsync_wait: false }
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--dry-run') out.dry_run = true
    else if (a === '--skip-preflight') out.skip_preflight = true
    else if (a === '--skip-wechatsync-wait') out.skip_wechatsync_wait = true
    else if (a.startsWith('--')) {
      const key = a.slice(2).replace(/-/g, '_')
      const next = argv[i + 1]
      if (next && !next.startsWith('--')) {
        out[key] = next
        i++
      }
    }
  }
  return out
}

function loadJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'))
}

function parseDraftMeta(file) {
  const raw = fs.readFileSync(file, 'utf8')
  const fm = raw.match(/^---\n([\s\S]*?)\n---/)
  const meta = {}
  if (fm) {
    for (const line of fm[1].split('\n')) {
      const m = line.match(/^(\w+):\s*(.+)$/)
      if (m) meta[m[1]] = m[2].replace(/^["']|["']$/g, '').trim()
    }
  }
  const titleM = raw.match(/^#\s+(.+)$/m)
  return {
    platform: meta.platform || '',
    canonical: meta.canonical || meta.source_url || '',
    source_title: meta.source_title || '',
    title: titleM ? titleM[1].trim() : path.basename(file, '.md'),
  }
}

function run(cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, {
    cwd: ROOT,
    stdio: 'inherit',
    shell: false,
    ...opts,
  })
  return r.status === 0
}

function preflight(draft, platform, manifest, meta) {
  const args = [
    path.join('scripts', 'preflight-distribution.js'),
    '--draft',
    draft,
    '--platform',
    platform,
    '--canonical',
    manifest.canonical_url || meta.canonical,
  ]
  if (manifest.source_title || meta.source_title) {
    args.push('--source-title', manifest.source_title || meta.source_title)
  }
  if (manifest.source_word_count) {
    args.push('--source-word-count', String(manifest.source_word_count))
  }
  return run('node', args)
}

function publishNode(script, draft, dryRun) {
  const args = [path.join(ROOT, script), '--draft', draft]
  if (dryRun) args.push('--dry-run')
  return run('node', args)
}

function publishWechatsync(draft, platformId, dryRun) {
  if (dryRun) {
    console.log(`[dry-run] wechatsync sync ${draft} -p ${platformId}`)
    return true
  }
  return run('bash', [
    path.join('scripts', 'publish-wechatsync.sh'),
    draft,
    platformId,
  ])
}

function ensureWechatsyncBridge(skipWait) {
  if (skipWait) {
    console.log('跳过 wechatsync-wait-connect（请确认 Arc 扩展已连接）')
    return true
  }
  console.log('等待 Wechatsync 扩展连接…')
  return run('bash', [path.join('scripts', 'wechatsync-wait-connect.sh'), '45'])
}

function main() {
  const args = parseArgs(process.argv)
  if (!args.manifest) {
    console.error('用法: node scripts/batch-publish.js --manifest queue/batch-manifest.json [--dry-run]')
    process.exit(1)
  }

  const manifestPath = path.isAbsolute(args.manifest)
    ? args.manifest
    : path.join(ROOT, args.manifest)
  if (!fs.existsSync(manifestPath)) {
    console.error(`清单不存在: ${manifestPath}`)
    process.exit(1)
  }

  const manifest = loadJson(manifestPath)
  const platforms = loadJson(CONFIG)
  const dryRun = args.dry_run || manifest.dry_run === true
  const only = args.only ? args.only.split(',').map((s) => s.trim()) : null

  let items = manifest.items || []
  if (only) items = items.filter((it) => only.includes(it.platform))

  const cnItems = items.filter((it) => {
    const p = platforms[it.platform]
    return p && p.publisher === 'wechatsync'
  })

  if (cnItems.length && !dryRun) {
    if (!ensureWechatsyncBridge(args.skip_wechatsync_wait)) {
      console.error('Wechatsync 未连接，国内平台跳过。可先: open -a Arc chrome-extension://hchobocdmclopcbnibdnoafilagadion/src/popup/index.html')
      process.exit(1)
    }
  }

  const results = { ok: [], fail: [], skip: [] }

  for (const item of items) {
    const platform = item.platform
    const spec = platforms[platform]
    const draftRel = item.draft
    const draft = path.isAbsolute(draftRel) ? draftRel : path.join(ROOT, draftRel)

    console.log(`\n=== ${platform} ← ${draftRel} ===`)

    if (!spec) {
      console.error(`未知平台: ${platform}`)
      results.fail.push({ platform, reason: 'unknown_platform' })
      continue
    }

    if (spec.workflow === 'cursor' || spec.workflow === 'manual') {
      console.log(`跳过 (${spec.workflow}): 请用 Cursor MCP 或人工 — 见 manifest.cursor_items`)
      results.skip.push({ platform, reason: spec.workflow })
      continue
    }

    if (!fs.existsSync(draft)) {
      console.error(`草稿不存在: ${draft}`)
      results.fail.push({ platform, reason: 'missing_draft' })
      continue
    }

    const meta = parseDraftMeta(draft)
    if (!args.skip_preflight && spec.preflight) {
      if (!preflight(draft, platform, manifest, meta)) {
        console.error(`预检未通过: ${platform}`)
        results.fail.push({ platform, reason: 'preflight' })
        continue
      }
    }

    let ok = false
    if (spec.publisher === 'node' && spec.script) {
      ok = publishNode(spec.script, draft, dryRun)
    } else if (spec.publisher === 'wechatsync') {
      ok = publishWechatsync(draft, spec.wechatsync_id || platform, dryRun)
    } else {
      console.error(`未配置发布器: ${platform}`)
      results.fail.push({ platform, reason: 'no_publisher' })
      continue
    }

    if (ok) results.ok.push(platform)
    else results.fail.push({ platform, reason: 'publish_error' })
  }

  console.log('\n=== 批量发布汇总 ===')
  console.log('成功:', results.ok.join(', ') || '(无)')
  console.log('失败:', results.fail.map((f) => `${f.platform}(${f.reason})`).join(', ') || '(无)')
  console.log('跳过:', results.skip.map((s) => `${s.platform}(${s.reason})`).join(', ') || '(无)')

  if (manifest.cursor_items?.length) {
    console.log('\n--- Cursor MCP 待处理 ---')
    for (const c of manifest.cursor_items) {
      console.log(`  ${c.platform}: ${c.draft}${c.note ? ` — ${c.note}` : ''}`)
    }
  }

  process.exit(results.fail.length ? 1 : 0)
}

main()
