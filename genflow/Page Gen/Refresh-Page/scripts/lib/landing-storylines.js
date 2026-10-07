/**
 * Landing Page storylines — loads Refresh-Page/landing-storylines.json
 * Copy to: dev/lovart.sanity.studio/scripts/lib/landing-storylines.js
 */

const fs = require('fs');
const path = require('path');

const JSON_PATH = path.resolve(__dirname, '../../landing-storylines.json');

function loadStorylinesFromJson() {
  const raw = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
  const map = {};
  for (const [id, meta] of Object.entries(raw.storylines || {})) {
    map[id] = meta.sections;
  }
  if (raw.legacyAliases) {
    for (const [alias, target] of Object.entries(raw.legacyAliases)) {
      if (map[target]) map[alias] = map[target];
    }
  }
  return map;
}

const LANDING_STORYLINES = loadStorylinesFromJson();

function typeSequenceForStoryline(storylineId) {
  const seq = LANDING_STORYLINES[storylineId];
  if (!seq) throw new Error(`Unknown landing storyline: ${storylineId}`);
  return seq;
}

function sectionCountForStoryline(storylineId) {
  return typeSequenceForStoryline(storylineId).length;
}

module.exports = {
  LANDING_STORYLINES,
  typeSequenceForStoryline,
  sectionCountForStoryline,
};
