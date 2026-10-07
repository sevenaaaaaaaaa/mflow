/**
 * language ↔ bodyJson alignment gate
 *
 * BLOCK when page.language and body copy script disagree.
 * Lane A: language=en but body is JA/KO/RU/ZH (or FR-dominant)
 * Lane B: non-EN page with EN shell / wrong script
 *
 * Codes:
 *   BODY_I18N_EN_WRONG  — EN page hung with non-English body
 *   BODY_I18N_EN_SHELL  — non-EN page body still English / missing target script
 *   BODY_I18N_WRONG     — non-EN page hung with another wrong script
 */

const HAN = /[\u4e00-\u9fff]/g
const HIRA = /[\u3040-\u309f]/g
const KATA = /[\u30a0-\u30ff]/g
const KO = /[\uac00-\ud7af]/g
const RU = /[\u0400-\u04ff]/g
const LATIN = /[A-Za-zÀ-ÿ]/g
const EN_W =
  /\b(the|and|with|for|your|you|from|this|that|create|generate|design|tool|professional|using)\b/gi
const FR_W =
  /\b(le|la|les|des|une|du|de|et|pour|avec|vous|nous|est|sont|dans|sur|par|plus|votre|créez|générer|outil)\b/gi
const DE_W =
  /\b(der|die|das|und|mit|für|von|den|dem|ein|eine|ist|sind|nicht|auch|auf|zu|oder|erstellen|gestaltung)\b/gi
const IT_W =
  /\b(il|lo|la|le|gli|di|del|della|che|per|con|una|sono|non|più|come|creare|genera|strumento)\b/gi
const PT_W =
  /\b(de|da|do|das|dos|para|com|uma|você|seu|sua|não|mais|como|criar|gerar|ferramenta)\b/gi

function count(re, text) {
  const m = text.match(re)
  return m ? m.length : 0
}

function extractBodyText(page) {
  let bj = page.bodyJson
  if (bj == null) return ''
  if (typeof bj === 'string') {
    try {
      bj = JSON.parse(bj)
    } catch {
      return bj
    }
  }
  const acc = []
  const walk = (obj) => {
    if (obj == null) return
    if (typeof obj === 'string') {
      if (obj.startsWith('http') || obj.length < 2) return
      acc.push(obj)
      return
    }
    if (Array.isArray(obj)) {
      obj.forEach(walk)
      return
    }
    if (typeof obj === 'object') {
      for (const [k, v] of Object.entries(obj)) {
        if (['_key', '_type', '_id', 'url', 'src', 'href', 'asset', 'image', 'icon', 'logo', 'id'].includes(k)) {
          continue
        }
        walk(v)
      }
    }
  }
  walk(bj)
  return acc.join(' ')
}

function scores(text) {
  return {
    han: count(HAN, text),
    hira: count(HIRA, text),
    kata: count(KATA, text),
    hang: count(KO, text),
    cyr: count(RU, text),
    lat: count(LATIN, text),
    en: count(EN_W, text),
    fr: count(FR_W, text),
    de: count(DE_W, text),
    it: count(IT_W, text),
    pt: count(PT_W, text),
    chars: text.length,
    kana: count(HIRA, text) + count(KATA, text),
  }
}

/**
 * @returns {{ok:boolean, code?:string, reason?:string}}
 */
function classifyBodyLang(lang, sc) {
  if (sc.chars < 80) return {ok: true, reason: 'short_skip'}

  if (lang === 'en') {
    if (sc.hang >= 30 && sc.hang >= sc.lat * 0.15) {
      return {ok: false, code: 'BODY_I18N_EN_WRONG', reason: 'en_body_is_ko'}
    }
    if (sc.kana >= 20) return {ok: false, code: 'BODY_I18N_EN_WRONG', reason: 'en_body_is_ja'}
    if (sc.cyr >= 30 && sc.cyr > sc.lat * 0.2) {
      return {ok: false, code: 'BODY_I18N_EN_WRONG', reason: 'en_body_is_ru'}
    }
    if (sc.han >= 40 && sc.kana < 10 && sc.han > sc.lat * 0.4) {
      return {ok: false, code: 'BODY_I18N_EN_WRONG', reason: 'en_body_is_zh'}
    }
    if (sc.fr >= 8 && sc.fr > sc.en * 1.2) {
      return {ok: false, code: 'BODY_I18N_EN_WRONG', reason: 'en_body_is_fr'}
    }
    return {ok: true}
  }

  if (lang === 'zh' || lang === 'zh-TW') {
    if (sc.kana >= 30 && sc.kana > sc.han * 0.4) {
      return {ok: false, code: 'BODY_I18N_WRONG', reason: 'zh_body_is_ja'}
    }
    if (sc.hang >= 40) return {ok: false, code: 'BODY_I18N_WRONG', reason: 'zh_body_is_ko'}
    if (sc.han < 40 && sc.lat > 200 && sc.en >= 8) {
      return {ok: false, code: 'BODY_I18N_EN_SHELL', reason: 'zh_en_shell'}
    }
    if (sc.han < 20 && sc.lat > 100) {
      return {ok: false, code: 'BODY_I18N_EN_SHELL', reason: 'zh_missing_han'}
    }
    return {ok: true}
  }

  if (lang === 'ja') {
    if (sc.hang >= 40) return {ok: false, code: 'BODY_I18N_WRONG', reason: 'ja_body_is_ko'}
    if (sc.kana < 10 && sc.lat > 200 && sc.en >= 8) {
      return {ok: false, code: 'BODY_I18N_EN_SHELL', reason: 'ja_en_shell'}
    }
    return {ok: true}
  }

  if (lang === 'ko') {
    if (sc.hang < 20 && sc.lat > 200 && sc.en >= 8) {
      return {ok: false, code: 'BODY_I18N_EN_SHELL', reason: 'ko_en_shell'}
    }
    return {ok: true}
  }

  if (lang === 'ru') {
    if (sc.cyr < 30 && sc.lat > 200 && sc.en >= 8) {
      return {ok: false, code: 'BODY_I18N_EN_SHELL', reason: 'ru_en_shell'}
    }
    return {ok: true}
  }

  if (['de', 'fr', 'it', 'pt'].includes(lang)) {
    const target = sc[lang] || 0
    const en = sc.en
    if (sc.kana >= 30 || sc.hang >= 40 || (sc.cyr >= 30 && sc.lat < 150)) {
      return {ok: false, code: 'BODY_I18N_WRONG', reason: `${lang}_wrong_script`}
    }
    if (en >= 10 && target <= 3 && en >= Math.max(target, 1) * 3) {
      return {ok: false, code: 'BODY_I18N_EN_SHELL', reason: `${lang}_en_shell`}
    }
    if (en >= 12 && target < 8 && sc.lat > 200 && target < en * 0.5) {
      return {ok: false, code: 'BODY_I18N_EN_SHELL', reason: `${lang}_en_shell`}
    }
    return {ok: true}
  }

  return {ok: true}
}

/**
 * @param {object} page compositePage-like JSON
 * @returns {{issues: Array, lang: string, scores?: object}}
 */
function checkBodyI18n(page) {
  const lang = page.language || 'en'
  const text = extractBodyText(page)
  const sc = scores(text)
  const result = classifyBodyLang(lang, sc)
  const issues = []
  if (!result.ok) {
    issues.push({
      code: result.code || 'BODY_I18N_WRONG',
      severity: 'BLOCK',
      message: `language=${lang} body mismatch reason=${result.reason} chars=${sc.chars}`,
      detail: result.reason,
    })
  }
  return {issues, lang, scores: sc, reason: result.reason || 'ok'}
}

module.exports = {
  checkBodyI18n,
  extractBodyText,
  scores,
  classifyBodyLang,
}
