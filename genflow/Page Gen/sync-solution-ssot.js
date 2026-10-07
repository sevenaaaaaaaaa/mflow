#!/usr/bin/env node
/**
 * Copy solution-storylines-v2.json → Refresh-Page/solution-storylines.json
 * Run when iCloud has released file locks on Refresh-Page.
 */
const fs = require('fs')
const path = require('path')

const src = path.join(__dirname, 'solution-storylines-v2.json')
const dest = path.join(__dirname, '../../Refresh-Page/solution-storylines.json')

try {
  fs.copyFileSync(src, dest)
  console.log(`Synced SSOT → ${dest}`)
} catch (err) {
  console.error(`Sync failed: ${err.message}`)
  console.error('Copy manually when Refresh-Page is writable, or run from Finder after unlocking iCloud files.')
  process.exit(1)
}
