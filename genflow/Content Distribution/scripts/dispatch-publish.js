#!/usr/bin/env node
/**
 * Agent 写稿后的统一分发入口
 *   国内 → Wechatsync
 *   海外 API → publish-devto.js / publish-github-discussions.js / publish-blogger.js
 *   海外爱贝壳 → Medium / X（扩展草稿箱，人工确认）
 *
 *   node scripts/dispatch-publish.js --manifest queue/dispatch-xxx.json
 *   node scripts/dispatch-publish.js --manifest queue/dispatch-xxx.json --dry-run
 *   node scripts/dispatch-publish.js --manifest queue/dispatch-xxx.json --cn-only
 *   node scripts/dispatch-publish.js --manifest queue/dispatch-xxx.json --global-only
 */

const fs = require('fs')
const path = require('path')
const { spawnSync } = require('child_process')

const ROOT = path.resolve(__dirname, '..')
const CONFIG = path.join(ROOT, 'config', 'platforms.json')
const QUEUE = path.join(ROOT, 'queue')

function parseArgs(argv) {
  const out = { dry_run: false }
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--dry-run') out.dry_run = true
    else if (a === '--approved') out.approved = true
    else if (a === '--skip-preflight') out.skip_preflight = true
    else if (a === '--skip-wechatsync-wait') out.skip_wechatsync_wait = true
    else if (a === '--cn-only') out.cn_only = true
    else if (a === '--global-only') out.global_only = true
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
    content_id: meta.content_id || path.basename(file, '.md'),
  }
}

function run(cmd, args) {
  const r = spawnSync(cmd, args, { cwd: ROOT, stdio: 'inherit', shell: false })
  return r.status === 0
}

function preflight(draft, platform, manifest, meta) {
  const args = [
    path.join('scripts', 'preflight-distribution.js'),
    '--draft', draft,
    '--platform', platform,
    '--canonical', manifest.canonical_url || meta.canonical,
  ]
  if (manifest.source_title || meta.source_title) {
    args.push('--source-title', manifest.source_title || meta.source_title)
  }
  if (manifest.source_word_count) {
    args.push('--source-word-count', String(manifest.source_word_count))
  }
  return run('node', args)
}

function normalizeManifest(manifest) {
  const cn = manifest.cn || []
  const global = manifest.global || []
  if (manifest.items?.length) {
    const platforms = loadJson(CONFIG)
    for (const it of manifest.items) {
      const spec = platforms[it.platform]
      if (!spec) continue
      if (spec.region === 'cn') cn.push(it)
      else global.push(it)
    }
  }
  if (manifest.cursor_items?.length) {
    for (const it of manifest.cursor_items) global.push(it)
  }
  return { cn, global }
}

function ensureWechatsyncBridge(skipWait, dryRun) {
  if (dryRun || skipWait) return true
  console.log('\n>>> 国内轨：等待 Wechatsync 扩展连接')
  return run('bash', [path.join('scripts', 'wechatsync-wait-connect.sh'), '45'])
}

function dispatchCn(items, manifest, platforms, opts) {
  const results = { ok: [], fail: [] }
  const cnItems = items.filter((it) => {
    const spec = platforms[it.platform]
    return spec && spec.primary_publisher === 'wechatsync'
  })

  if (!cnItems.length) {
    console.log('\n>>> 国内轨：无待发布项')
    return results
  }

  if (!opts.dry_run && !opts.skip_wechatsync_wait) {
    if (!ensureWechatsyncBridge(opts.skip_wechatsync_wait, opts.dry_run)) {
      console.error('Wechatsync 未连接，国内发布中止')
      for (const it of cnItems) results.fail.push({ platform: it.platform, reason: 'wechatsync_offline' })
      return results
    }
  }

  console.log('\n>>> 国内轨：Wechatsync')
  for (const item of cnItems) {
    const spec = platforms[item.platform]
    const draft = path.isAbsolute(item.draft) ? item.draft : path.join(ROOT, item.draft)
    console.log(`\n--- ${item.platform} ← ${item.draft} ---`)

    if (!fs.existsSync(draft)) {
      results.fail.push({ platform: item.platform, reason: 'missing_draft' })
      continue
    }

    const meta = parseDraftMeta(draft)
    if (!opts.skip_preflight && spec.preflight) {
      if (!preflight(draft, item.platform, manifest, meta)) {
        results.fail.push({ platform: item.platform, reason: 'preflight' })
        continue
      }
    }

    const wsId = spec.wechatsync_id || item.platform
    if (opts.dry_run) {
      console.log(`[dry-run] wechatsync sync ${item.draft} -p ${wsId}`)
      results.ok.push(item.platform)
      continue
    }

    const ok = run('bash', [
      path.join('scripts', 'publish-wechatsync.sh'),
      draft,
      wsId,
    ])
    if (ok) results.ok.push(item.platform)
    else results.fail.push({ platform: item.platform, reason: 'publish_error' })
  }
  return results
}

function dispatchGlobalApi(items, manifest, platforms, opts) {
  const results = { ok: [], fail: [] }
  const apiItems = items.filter((it) => {
    const spec = platforms[it.platform]
    return spec && spec.primary_publisher === 'api'
  })

  if (!apiItems.length) {
    console.log('\n>>> 海外 API 轨：无待发布项')
    return results
  }

  console.log('\n>>> 海外 API 轨')
  for (const item of apiItems) {
    const spec = platforms[item.platform]
    const draft = path.isAbsolute(item.draft) ? item.draft : path.join(ROOT, item.draft)
    console.log(`\n--- ${item.platform} ← ${item.draft} ---`)

    if (!fs.existsSync(draft)) {
      results.fail.push({ platform: item.platform, reason: 'missing_draft' })
      continue
    }

    const meta = parseDraftMeta(draft)
    if (!opts.skip_preflight && spec.preflight) {
      if (!preflight(draft, item.platform, manifest, meta)) {
        results.fail.push({ platform: item.platform, reason: 'preflight' })
        continue
      }
    }

    const scriptArgs = [path.join(ROOT, spec.script), '--draft', draft]
    if (opts.dry_run) scriptArgs.push('--dry-run')

    if (opts.dry_run) {
      console.log(`[dry-run] node ${path.relative(ROOT, spec.script)} --draft ${item.draft}`)
      results.ok.push(item.platform)
      continue
    }

    const ok = run('node', scriptArgs)
    if (ok) results.ok.push(item.platform)
    else results.fail.push({ platform: item.platform, reason: 'publish_error' })
  }
  return results
}

function dispatchAibeike(items, manifest, platforms, opts) {
  const results = { pending: [] }
  const abItems = items.filter((it) => {
    const spec = platforms[it.platform]
    return spec && spec.primary_publisher === 'aibeike'
  })

  if (!abItems.length) {
    console.log('\n>>> 爱贝壳轨：无待发布项')
    return results
  }

  console.log('\n>>> 爱贝壳轨（扩展 → 草稿箱 → 人工确认）')
  for (const item of abItems) {
    const spec = platforms[item.platform]
    const draft = path.isAbsolute(item.draft) ? item.draft : path.join(ROOT, item.draft)
    console.log(`\n--- ${item.platform} (slot ${spec.aibeike_slot || '?'}) ← ${item.draft} ---`)

    if (!fs.existsSync(draft)) {
      console.log('  ✗ 草稿缺失')
      continue
    }

    const meta = parseDraftMeta(draft)
    if (!opts.skip_preflight && spec.preflight) {
      if (!preflight(draft, item.platform, manifest, meta)) {
        console.log('  ✗ preflight 未通过')
        continue
      }
    }

    console.log('  1. Arc/Chrome 打开爱贝壳扩展侧栏')
    console.log(`  2. 粘贴 ${item.draft} 内容，勾选 ${spec.label}`)
    console.log('  3. 同步到平台草稿箱 → 各平台后台确认发布')
    console.log('  4. 发布后更新 queue/published.json')
    results.pending.push(item.platform)
  }
  return results
}

function dispatchManualGlobal(items, manifest, platforms, opts) {
  const manual = manifest.manual_global || []
  const list = manual.length ? manual : items.filter((it) => {
    const spec = platforms[it.platform]
    return spec && spec.primary_publisher === 'manual'
  })

  if (!list.length) return []

  console.log('\n>>> 海外人工轨')
  for (const item of list) {
    const draft = path.isAbsolute(item.draft) ? item.draft : path.join(ROOT, item.draft)
    const spec = platforms[item.platform]
    console.log(`  ${item.platform}: ${item.draft}`)
    if (fs.existsSync(draft) && spec?.preflight && !opts.skip_preflight) {
      const meta = parseDraftMeta(draft)
      preflight(draft, item.platform, manifest, meta)
    }
    if (item.note) console.log(`    → ${item.note}`)
    else if (spec?.label) console.log(`    → 见 channels/${item.platform.replace(/_/g, '-')}.md`)
  }
  return list.map((i) => i.platform)
}

function main() {
  const opts = parseArgs(process.argv)
  if (!opts.manifest) {
    console.error('用法: node scripts/dispatch-publish.js --manifest queue/dispatch-xxx.json')
    process.exit(1)
  }

  const manifestPath = path.isAbsolute(opts.manifest)
    ? opts.manifest
    : path.join(ROOT, opts.manifest)
  if (!fs.existsSync(manifestPath)) {
    console.error(`清单不存在: ${manifestPath}`)
    process.exit(1)
  }

  const manifest = loadJson(manifestPath)
  const platforms = loadJson(CONFIG)
  const { cn, global } = normalizeManifest(manifest)

  const needsReview = !opts.approved && manifest.approved !== true
  if (needsReview) {
    opts.dry_run = true
    console.log('\n>>> 待人工审核：清单 approved≠true 且未传 --approved，仅预检不真发')
    console.log('>>> 请阅读 drafts/ 全文后设 "approved": true 并加 --approved\n')
    console.log('>>> 规范见 EDITORIAL.md\n')
  }

  const cnRes = opts.global_only ? { ok: [], fail: [] } : dispatchCn(cn, manifest, platforms, opts)
  const apiRes = opts.cn_only ? { ok: [], fail: [] } : dispatchGlobalApi(global, manifest, platforms, opts)
  const aibeikeRes = opts.cn_only ? { pending: [] } : dispatchAibeike(global, manifest, platforms, opts)
  const manualGlobal = opts.cn_only ? [] : dispatchManualGlobal(global, manifest, platforms, opts)

  console.log('\n========== 分发汇总 ==========')
  console.log('国内 Wechatsync 成功:', cnRes.ok.join(', ') || '(无)')
  console.log('国内失败:', cnRes.fail.map((f) => `${f.platform}(${f.reason})`).join(', ') || '(无)')
  console.log('海外 API 成功:', apiRes.ok.join(', ') || '(无)')
  console.log('海外 API 失败:', apiRes.fail.map((f) => `${f.platform}(${f.reason})`).join(', ') || '(无)')
  console.log('爱贝壳待操作:', aibeikeRes.pending?.join(', ') || '(无)')
  console.log('其他人工待发布:', manualGlobal.join(', ') || '(无)')
  console.log('\n栈定义: config/stack.json | 补充: channels/supplementary.md')

  const failed = cnRes.fail.length + apiRes.fail.length
  process.exit(failed ? 1 : 0)
}

main()
