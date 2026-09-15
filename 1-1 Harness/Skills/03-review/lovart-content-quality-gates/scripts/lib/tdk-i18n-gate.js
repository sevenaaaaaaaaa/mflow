/**
 * language ↔ TDK alignment gate (title / seo.title / seo.description / description)
 *
 * BLOCK when page language and TDK script/boilerplate disagree.
 * Used by anti-slop-preflight and studio preflight-content.js.
 *
 * Codes:
 *   TDK_I18N_TITLE   — title / seo.title wrong language or EN shell
 *   TDK_I18N_DESC    — description / seo.description wrong language or EN shell
 *   TDK_I18N_EMPTY   — required TDK empty (strict mode)
 */

const HAN = /[\u4e00-\u9fff]/
const JA = /[\u3040-\u30ff]/
const KO = /[\uac00-\ud7af]/
const RU = /[\u0400-\u04FF]/
const LATIN = /[A-Za-z]/
const LANG_TAG = /^\[(IT|PT|FR|DE|JA|KO|RU|ZH|EN)\]\s*/i
const EN_BOILER =
  /\b(Create professional|with Lovart'?s AI Design Agent|Professional Design Tool|Design Tool \| Lovart|in seconds with|Free to Try|from Text)\b/i
/** EN pages only — slug-dump / product shell; do not flag legitimate "from text" copy. */
const EN_PAGE_BOILER =
  /\b(Create professional|Professional Design Tool|Design Tool \| Lovart)\b/i
const SLUG_TITLE_CASE = /^Ai [A-Z][a-z]+( [A-Za-z0-9/-]+){1,10}\s*\|\s*Lovart\s*$/
const SYNTH_ZH_SHELL = /｜Lovart AI 设计工具\s*$|｜Lovart AI 設計工具\s*$/
const SYNTH_JA_SHELL = /^Lovartの.+｜AIでプロ品質/
const SYNTH_KO_SHELL = /\|\s*Lovart AI로 전문 디자인\s*$/
const SYNTH_RU_SHELL = /\sс ИИ \| Lovart\s*$/
const SYNTH_DESC_WRAP =
  /用 Lovart AI 设计代理，为「|用 Lovart AI 設計代理，為「|LovartのAIデザインエージェントで「|Lovart AI 디자인 에이전트로 “|Создавайте профессиональные материалы для «|Créez des résultats professionnels pour|Crea risultati professionali per|Crie resultados profissionais para|Erstellen Sie mit Lovarts KI-Design-Agenten professionelle Ergebnisse/

function asStr(v) {
  if (typeof v === 'string') return v
  if (Array.isArray(v)) return v.filter(Boolean).join(' ')
  return ''
}

function flags(text) {
  const t = asStr(text)
  return {
    t,
    han: HAN.test(t),
    ja: JA.test(t),
    ko: KO.test(t),
    ru: RU.test(t),
    latin: LATIN.test(t),
    enBoiler: EN_BOILER.test(t) || /^Create professional\b/i.test(t),
    langTag: LANG_TAG.test(t),
    slugTc: SLUG_TITLE_CASE.test(t),
    synthShell:
      SYNTH_ZH_SHELL.test(t) ||
      SYNTH_JA_SHELL.test(t) ||
      SYNTH_KO_SHELL.test(t) ||
      SYNTH_RU_SHELL.test(t) ||
      SYNTH_DESC_WRAP.test(t),
  }
}

function titleReasons(lang, text) {
  const f = flags(text)
  const reasons = []
  if (!f.t.trim()) {
    reasons.push('empty')
    return reasons
  }
  if (f.langTag) reasons.push('lang_tag_prefix')
  if (f.synthShell) reasons.push('synth_shell')
  if (lang === 'en') {
    if (f.han || f.ja || f.ko || f.ru) reasons.push('wrong_script')
    return reasons
  }
  if (['de', 'fr', 'it', 'pt'].includes(lang)) {
    if (f.han || f.ja || f.ko || f.ru) reasons.push('wrong_script')
    if (f.enBoiler) reasons.push('en_boilerplate')
    if (f.slugTc) reasons.push('slug_title_case_en')
  } else if (lang === 'ja') {
    // Kanji-only Japanese titles are valid; require CJK or kana, reject pure Latin shells.
    if (f.ko || f.ru) reasons.push('wrong_script')
    if (!f.ja && !f.han && f.latin) reasons.push('latin_only')
    if (f.enBoiler && !f.ja && !f.han) reasons.push('en_boilerplate')
  } else if (lang === 'ko') {
    if (f.han || f.ja || f.ru) reasons.push('wrong_script')
    if (!f.ko && f.latin) reasons.push('latin_only')
    if (f.enBoiler && !f.ko) reasons.push('en_boilerplate')
  } else if (lang === 'ru') {
    if (f.han || f.ja || f.ko) reasons.push('wrong_script')
    if (!f.ru && f.latin) reasons.push('no_cyrillic')
    if (f.enBoiler && !f.ru) reasons.push('en_boilerplate')
  } else if (lang === 'zh' || lang === 'zh-TW') {
    if (f.ja || f.ko || f.ru) reasons.push('wrong_script')
    if (!f.han && f.latin) reasons.push('latin_only')
    if (f.enBoiler && !f.han) reasons.push('en_boilerplate')
  }
  return reasons
}

function descReasons(lang, text, {allowEmpty = false} = {}) {
  const f = flags(text)
  const reasons = []
  if (!f.t.trim()) {
    if (!allowEmpty) reasons.push('empty')
    return reasons
  }
  // Script alignment alone does not make a useful meta description. Enforce
  // a lower information floor by writing system; this is not a padding target.
  const minLength = {
    en: 120,
    de: 120,
    fr: 120,
    it: 120,
    pt: 120,
    ru: 120,
    ja: 90,
    ko: 90,
    zh: 80,
    'zh-TW': 80,
  }[lang] || 120
  if (f.t.length < minLength) reasons.push('too_short')
  if (f.synthShell) reasons.push('synth_shell')
  if (lang === 'en') {
    const enPageBoiler = EN_PAGE_BOILER.test(f.t) || /^Create professional\b/i.test(f.t)
    if (enPageBoiler) reasons.push('en_boilerplate')
    if (f.han || f.ja || f.ko || f.ru) reasons.push('wrong_script')
    return reasons
  }
  if (f.enBoiler) reasons.push('en_boilerplate')
  if (['de', 'fr', 'it', 'pt'].includes(lang)) {
    if (f.han || f.ja || f.ko || f.ru) reasons.push('wrong_script')
  } else if (lang === 'ja') {
    if (f.ko || f.ru) reasons.push('wrong_script')
    if (!f.ja && !f.han && f.latin && f.t.length > 40) reasons.push('latin_only')
  } else if (lang === 'ko') {
    if (f.han || f.ja || f.ru) reasons.push('wrong_script')
    if (!f.ko && f.latin && f.t.length > 40) reasons.push('latin_only')
  } else if (lang === 'ru') {
    if (f.han || f.ja || f.ko) reasons.push('wrong_script')
    if (!f.ru && f.latin && f.t.length > 40) reasons.push('no_cyrillic')
  } else if (lang === 'zh' || lang === 'zh-TW') {
    if (f.ja || f.ko || f.ru) reasons.push('wrong_script')
    if (!f.han && f.latin && f.t.length > 40) reasons.push('latin_only')
  }
  return reasons
}

/**
 * @param {object} page compositePage-like JSON
 * @param {{strict?: boolean}} opts
 * @returns {{issues: Array<{code:string,severity:string,message:string,field?:string}>}}
 */
function checkTdkI18n(page, opts = {}) {
  const strict = !!opts.strict
  const lang = page.language || 'en'
  const seo = page.seo || {}
  const issues = []

  const pairs = [
    ['title', page.title, 'title'],
    ['seo.title', seo.title, 'title'],
    ['description', page.description, 'desc'],
    ['seo.description', seo.description, 'desc'],
  ]

  for (const [field, value, kind] of pairs) {
    const reasons =
      kind === 'title'
        ? titleReasons(lang, value)
        : descReasons(lang, value, {allowEmpty: !strict})
    if (!reasons.length) continue
    const code = kind === 'title' ? 'TDK_I18N_TITLE' : reasons.includes('empty') ? 'TDK_I18N_EMPTY' : 'TDK_I18N_DESC'
    const severity =
      reasons.includes('empty') && !strict
        ? 'WARN'
        : 'BLOCK'
    issues.push({
      code,
      severity,
      field,
      message: `language=${lang} field=${field} reasons=${reasons.join(',')}: ${asStr(value).slice(0, 80)}`,
    })
  }
  return {issues, lang}
}

module.exports = {
  checkTdkI18n,
  titleReasons,
  descReasons,
  flags,
}
