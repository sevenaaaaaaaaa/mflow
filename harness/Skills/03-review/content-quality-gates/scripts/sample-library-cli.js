#!/usr/bin/env node
/**
 * List or print annotated content samples for Agent / editor use.
 *
 *   node sample-library-cli.js list
 *   node sample-library-cli.js show blog-en-good-001
 *   node sample-library-cli.js pair blog
 *   node sample-library-cli.js calibrate
 */

const path = require('path')
const { loadIndex, loadSample, findSamples, getPair, formatBrief } = require('./lib/sample-library')
const { checkBlogMarkdown } = require('./lib/anti-slop-rules')

const FIXTURE_GOOD = path.join(__dirname, '_fixtures/good-sample.md')
const FIXTURE_SLOP = path.join(__dirname, '_fixtures/slop-sample.md')

function cmdList() {
  const index = loadIndex()
  console.log(`Content Sample Library (${index.version})\n`)
  for (const s of index.samples) {
    console.log(
      `${s.id.padEnd(28)} ${s.verdict.padEnd(10)} ${s.content_type.padEnd(12)} ${s.rubric_score}  ${s.focus_query}`
    )
  }
}

function cmdShow(id) {
  const sample = loadSample(id)
  console.log(formatBrief(sample))
  console.log('\n---\n')
  console.log(sample.raw)
}

function cmdPair(type) {
  const good = getPair(type, 'gold')
  const bad = loadSample(loadIndex().bad_defaults[type])
  console.log('=== GOOD / GOLD ===')
  console.log(formatBrief(good))
  console.log('\n=== BAD ===')
  console.log(formatBrief(bad))
}

function cmdCalibrate() {
  const fs = require('fs')
  const index = loadIndex()
  const results = []

  if (fs.existsSync(FIXTURE_GOOD)) {
    const good = checkBlogMarkdown(fs.readFileSync(FIXTURE_GOOD, 'utf8'), { strict: true })
    const expect = index.samples.find((s) => s.id === 'blog-en-good-001')
    results.push({
      id: 'blog-en-good-001',
      expected_pass: expect?.preflight_pass,
      actual_fail: good.issues.some((i) => i.severity === 'BLOCK'),
      codes: good.issues.map((i) => i.code),
    })
  }

  if (fs.existsSync(FIXTURE_SLOP)) {
    const bad = checkBlogMarkdown(fs.readFileSync(FIXTURE_SLOP, 'utf8'), { strict: true })
    const expect = index.samples.find((s) => s.id === 'blog-en-bad-001')
    results.push({
      id: 'blog-en-bad-001',
      expected_pass: expect?.preflight_pass,
      actual_fail: bad.issues.some((i) => i.severity === 'BLOCK'),
      codes: bad.issues.map((i) => i.code),
    })
  }

  console.log('Calibration (fixtures vs sample preflight annotations):\n')
  for (const r of results) {
    const ok = r.expected_pass === !r.actual_fail
    console.log(`${ok ? 'OK' : 'MISMATCH'} ${r.id}: expected pass=${r.expected_pass}, blocked=${r.actual_fail}`)
    console.log(`  codes: ${r.codes.join(', ')}\n`)
  }
}

const [,, cmd, arg] = process.argv
switch (cmd) {
  case 'list':
    cmdList()
    break
  case 'show':
    if (!arg) {
      console.error('Usage: sample-library-cli.js show <id>')
      process.exit(2)
    }
    cmdShow(arg)
    break
  case 'pair':
    if (!arg) {
      console.error('Usage: sample-library-cli.js pair <content_type>')
      process.exit(2)
    }
    cmdPair(arg)
    break
  case 'calibrate':
    cmdCalibrate()
    break
  default:
    console.log(`Commands: list | show <id> | pair <type> | calibrate`)
    process.exit(cmd ? 2 : 0)
}
