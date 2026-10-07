#!/usr/bin/env node
/** One-shot: update storyline field in en/*.json to v2 IDs */
const fs = require('fs')
const path = require('path')
const map = {
  'ai-design-solution-for-shopify-en.json': 'solution-i-ecommerce',
  'ai-design-solution-for-marketing-teams-en.json': 'solution-p-marketing',
  'ai-design-solution-for-agencies-en.json': 'solution-p-agency',
}
const dir = path.join(__dirname, 'en')
for (const [file, storyline] of Object.entries(map)) {
  const p = path.join(dir, file)
  const doc = JSON.parse(fs.readFileSync(p, 'utf8'))
  doc.storyline = storyline
  fs.writeFileSync(p, JSON.stringify(doc, null, 2) + '\n')
  console.log(file, '→', storyline)
}
