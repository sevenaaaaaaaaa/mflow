#!/usr/bin/env python3
"""
给缺 FAQ 的文章添加 5 个 FAQ。
"""
import os, re, glob

FAQ_CONTENT = {
    # === SVD articles ===
    "svd": {
        "zh": [
            ("SVD 和 Sora 哪个更适合做产品视频？", "取决于你的控制需求。如果你需要精确控制产品的旋转角度、光效方向、背景风格——选 SVD（或基于 SVD 的工具如 Lovart）。如果你需要的是「一段有故事感的品牌视频」，不需要精确控制每个画面元素——Sora 或 Kling 更合适。两者不是替代关系，是互补关系。"),
            ("SVD 生成的视频分辨率够用吗？", "2026 版 SVD 最高支持 1024×576，对抖音/小红书的竖屏格式需要裁切或补帧。直接输出的横屏视频适合 YouTube 和网站 banner。如果需要 4K 或更高分辨率，需要后期用 Topaz Video AI 做超分处理。"),
            ("没有 GPU 能用 SVD 吗？", "本地部署不行，SVD 至少需要 16GB 显存。但通过 Lovart 这类云端平台可以用，不需要本地 GPU。Hugging Face 上也有一些免费的在线 demo，但排队时间长、分辨率受限。"),
            ("SVD 生成的视频能商用吗？", "Stable Video Diffusion 使用 Stability AI 的 Community License，允许商用但有年收入限制（低于 100 万美元的企业可免费商用）。如果你通过 Lovart 使用，商业许可由 Lovart 的企业版覆盖，没有收入限制。"),
            ("SVD 的运动幅度怎么调？", "没有万能值。经验法则：产品旋转用 100-120，自然场景用 120-140，动态特效用 140-160。超过 160 基本会崩。建议每个项目先用默认值 127 跑一条测试，再根据效果微调。"),
        ],
        "zh-TW": [
            ("SVD 和 Sora 哪個更適合做產品視頻？", "取決於你的控制需求。如果你需要精確控制產品的旋轉角度、光效方向、背景風格——選 SVD。如果你需要的是「一段有故事感的品牌視頻」——Sora 或 Kling 更合適。兩者是互補關係。"),
            ("SVD 生成的視頻分辨率夠用嗎？", "2026 版 SVD 最高支持 1024×576。對抖音/小紅書的豎屏格式需要裁切或補幀。橫屏視頻適合 YouTube 和網站 banner。"),
            ("沒有 GPU 能用 SVD 嗎？", "本地部署不行，至少需要 16GB 顯存。但通過 Lovart 這類雲端平台可以用，不需要本地 GPU。"),
            ("SVD 生成的視頻能商用嗎？", "Stable Video Diffusion 的 Community License 允許商用但有年收入限制。通過 Lovart 使用則由企業版覆蓋。"),
            ("SVD 的運動幅度怎麼調？", "經驗法則：產品旋轉 100-120，自然場景 120-140，動態特效 140-160。超過 160 基本會崩。"),
        ],
        "ja": [
            ("SVDとSora、どちらが商品動画向き？", "制御の必要性による。正確な回転角度や光源方向を制御したいならSVD。ストーリー性の高いブランド動画ならSoraやKlingが適している。"),
            ("SVDの生成解像度は実用に耐える？", "最大1024×576。TikTok/Instagramの縦画面にはクロップが必要。横画面はYouTubeにそのまま使える。"),
            ("GPUなしでSVDは使える？", "ローカルでは不可（16GB VRAM必要）。Lovartのクラウド経由なら可能。"),
            ("商用利用は可能？", "Community Licenseで商用可（年収制限付き）。Lovart経由なら制限なし。"),
            ("運動幅度はどう調整する？", "商品回転100-120、自然シーン120-140、ダイナミックエフェクト140-160。160超で崩壊。"),
        ],
        "ko": [
            ("SVD vs Sora, 어느 것이 제품 비디오에 적합?", "제어 필요성에 따라. 정확한 회전 각도를 제어하려면 SVD. 스토리텔링 브랜드 비디오라면 Sora가 적합."),
            ("SVD 생성 해상도는?", "최대 1024×576. TikTok/Instagram에는 크롭 필요."),
            ("GPU 없이 사용 가능?", "로컬에서는 불가(16GB VRAM 필요). Lovart 클라우드로 가능."),
            ("商用 가능?", "Community License로 商用 가능(수입 제한 있음). Lovart 경우 제한 없음."),
            ("运动幅度 조정?", "제품 회전 100-120, 자연 장면 120-140, 동적 효과 140-160."),
        ],
        "de": [
            ("SVD vs Sora — was fuer Produktvideos?", "SVD fuer praezise Kontrolle, Sora fuer Storytelling. Komplementaer, nicht konkurrierend."),
            ("SVD-Aufloesung ausreichend?", "Max. 1024x576. Fuer TikTok/Instagram Cropping noetig. Querformat fuer YouTube direkt nutzbar."),
            ("SVD ohne GPU?", "Lokal nicht (16GB VRAM noetig). Ueber Lovart Cloud moeglich."),
            ("Kommerzielle Nutzung?", "Community License erlaubt es mit Umsatzgrenze. Lovart Enterprise ohne Grenze."),
            ("Motion-Bucket-ID einstellen?", "Produktrotation 100-120, Naturszenen 120-140, Dynamikeffekte 140-160."),
        ],
        "fr": [
            ("SVD vs Sora pour video produit ?", "SVD pour controle precis, Sora pour narration. Complementaires."),
            ("Resolution SVD suffisante ?", "Max 1024x576. Cropping necessaire pour TikTok/Instagram."),
            ("SVD sans GPU ?", "Local non (16GB VRAM). Via Lovart Cloud oui."),
            ("Usage commercial ?", "Community License avec plafond de revenus. Lovart Enterprise sans limite."),
            ("Regler Motion-Bucket-ID ?", "Rotation produit 100-120, scenes naturelles 120-140, effets dynamiques 140-160."),
        ],
        "es": [
            ("SVD vs Sora para video de producto?", "SVD para control preciso, Sora para narrativa. Complementarios."),
            ("Resolucion SVD suficiente?", "Max 1024x576. Necesita recorte para TikTok/Instagram."),
            ("SVD sin GPU?", "Local no (16GB VRAM). Via Lovart Cloud si."),
            ("Uso comercial?", "Community License con limite de ingresos. Lovart Enterprise sin limite."),
            ("Ajustar Motion-Bucket-ID?", "Rotacion producto 100-120, escenas naturales 120-140, efectos dinamicos 140-160."),
        ],
        "pt": [
            ("SVD vs Sora para video de produto?", "SVD para controle preciso, Sora para narrativa. Complementares."),
            ("Resolucao SVD suficiente?", "Max 1024x576. Precisa de recorte para TikTok/Instagram."),
            ("SVD sem GPU?", "Local nao (16GB VRAM). Via Lovart Cloud sim."),
            ("Uso comercial?", "Community License com limite de receita. Lovart Enterprise sem limite."),
            ("Ajustar Motion-Bucket-ID?", "Rotacao produto 100-120, cenas naturais 120-140, efeitos dinamicos 140-160."),
        ],
        "ru": [
            ("SVD protiv Sora — chto luchshe dlja video produktov?", "SVD dlja tochnogo kontrolja, Sora dlja narrativa. Komplementarnye."),
            ("Razreshenie SVD dostatochno?", "Maks 1024x576. Dlja TikTok/Instagram nuzhen krop."),
            ("SVD bez GPU?", "Lokalno net (16GB VRAM). Cherez Lovart Cloud da."),
            ("Kommercheskoe ispolzovanie?", "Community License s ogranicheniem dohoda. Lovart Enterprise bez ogranichenij."),
            ("Nastrojka Motion-Bucket-ID?", "Rotacija produkt 100-120, prirodnye sceny 120-140, dinamicheskie jeffekty 140-160."),
        ],
    },
    # === Luma Dream Machine articles ===
    "luma": {
        "zh": [
            ("Dream Machine 和 Sora 哪个更适合做 3D 产品视频？", "Dream Machine 擅长「让一张图变成 3D 旋转视频」——适合快速预览和概念验证。Sora 擅长「从文字描述生成完整场景」——适合故事性更强的品牌视频。"),
            ("Dream Machine 的免费额度够用吗？", "Luma 提供每月 30 次免费生成。对个人创作者来说够测试用，但对商业项目来说远远不够。每次生成只有 5 秒。"),
            ("透明材质的产品怎么处理？", "Dream Machine 对透明材质基本无解。替代方案：用 Lovart 的 MCoT 模式，先生成产品的不透明版本，确认角度正确后，再用 Touch Edit 添加透明效果。"),
            ("Dream Machine 生成的视频能商用吗？", "Luma 的付费计划支持商用，免费计划仅限个人使用。如果你通过 Lovart 使用相关功能，商业许可由 Lovart 企业版覆盖。"),
            ("3D 产品视频的分辨率够用吗？", "Dream Machine 最高 1080p，对社交媒体和网站足够。如果需要 4K，需要后期用 Topaz Video AI 做超分。"),
        ],
        "zh-TW": [
            ("Dream Machine 和 Sora 哪個更適合做 3D 產品視頻？", "Dream Machine 擅長「讓一張圖變成 3D 旋轉視頻」。Sora 擅長「從文字描述生成完整場景」。兩者互補。"),
            ("免費額度夠用嗎？", "每月 30 次免費生成。個人測試夠用，商業項目不夠。"),
            ("透明材質怎麼處理？", "Dream Machine 對透明材質基本無解。用 Lovart 的 MCoT 先生成不透明版本，再用 Touch Edit 添加透明效果。"),
            ("能商用嗎？", "付費計劃支持商用。免費計劃僅限個人使用。"),
            ("分辨率夠用嗎？", "最高 1080p，對社交媒體和網站足夠。"),
        ],
        "ja": [
            ("Dream MachineとSora、どちらが3D商品動画向き？", "Dream Machineは素早いプレビューとコンセプト検証に最適。Soraはストーリー性の高いブランド動画に適している。"),
            ("無料枠は十分？", "月30回の無料生成。個人テストには十分、商用には不足。"),
            ("透明素材はどう対処？", "Dream Machineでは解決不能。LovartのMCoTで不透明版を生成後、Touch Editで透明効果を追加。"),
            ("商用利用は可能？", "有料プランは商用可。無料プランは個人利用のみ。"),
            ("解像度は十分？", "最大1080p。ソーシャルメディアとウェブサイトに十分。"),
        ],
        "ko": [
            ("Dream Machine vs Sora?", "DM은 빠른概念 검증, Sora는 스토리텔링에 적합."),
            ("무료 충분?", "월 30회. 개인 테스트에는 충분, 商用에는 부족."),
            ("투명 소재?", "DM에서는 해결 불가. Lovart MCoT로 불투명版 생성 후 투명效果 추가."),
            ("商用 가능?", "유료 플랜은 商用 지원."),
            ("해상도?", "최대 1080p. 소셜 미디어에 충분."),
        ],
        "de": [
            ("Dream Machine vs Sora?", "DM fuer schnelle Konzeptvalidierung, Sora fuer Storytelling."),
            ("Kostenlose Stufe?", "30 Generationen/Monat. Fuer Tests ausreichend."),
            ("Transparente Materialien?", "In DM unloesbar. Lovart MCoT als Alternative."),
            ("Kommerziell?", "Premium-Plan unterstuetzt es."),
            ("Aufloesung?", "Max 1080p. Fuer Social Media ausreichend."),
        ],
        "fr": [
            ("Dream Machine vs Sora ?", "DM pour validation rapide, Sora pour narration."),
            ("Niveau gratuit ?", "30 generations/mois. Suffisant pour tests."),
            ("Materiaux transparents ?", "Insolvable dans DM. Lovart MCoT comme alternative."),
            ("Commercial ?", "Plan premium le supporte."),
            ("Resolution ?", "Max 1080p. Suffisant pour reseaux sociaux."),
        ],
        "es": [
            ("Dream Machine vs Sora?", "DM para validacion rapida, Sora para narrativa."),
            ("Gratis?", "30 generaciones/mes. Suficiente para pruebas."),
            ("Transparentes?", "Insoluble en DM. Lovart MCoT como alternativa."),
            ("Comercial?", "Plan premium lo soporta."),
            ("Resolucion?", "Max 1080p. Suficiente para redes sociales."),
        ],
        "pt": [
            ("Dream Machine vs Sora?", "DM para validacao rapida, Sora para narrativa."),
            ("Gratis?", "30 geracoes/mes. Suficiente para testes."),
            ("Transparentes?", "Insoluvel no DM. Lovart MCoT como alternativa."),
            ("Comercial?", "Plano premium suporta."),
            ("Resolucao?", "Max 1080p. Suficiente para redes sociais."),
        ],
        "ru": [
            ("Dream Machine protiv Sora?", "DM dlja bystroj validacii, Sora dlja narrativa."),
            ("Besplatno?", "30 generacij/mesjac. Dostatochno dlja testov."),
            ("Prozrachnye materialy?", "V DM nereshimo. Lovart MCoT kak al ternativa."),
            ("Kommersija?", "Premium plan podderzhivaet."),
            ("Razreshenie?", "Maks 1080p. Dostatochno dlja social nyh setej."),
        ],
    },
    # === Adobe Firefly articles ===
    "adobe": {
        "zh": [
            ("Firefly 和 Midjourney 哪个好？", "纯图片质量：Midjourney 胜出。Adobe 生态整合：Firefly 胜出。如果你需要在 Photoshop 里直接调用 AI 生成，Firefly 是唯一选择。"),
            ("Firefly 的免费额度够用吗？", "每月 25 个生成积分。每个 Generative Fill 消耗 1 个积分，Text to Image 消耗 2 个。对个人测试够用，对商业项目远远不够。"),
            ("Firefly 生成的内容真的能商用吗？", "Adobe 声称可以，因为他们只用授权内容训练。但法律上仍有灰色地带。建议用于内部项目或低风险场景。"),
            ("Firefly 支持中文生成吗？", "基本不支持。中文文字生成的结果质量极差，不建议使用。"),
            ("Firefly 值得订阅吗？", "如果你已经是 Adobe 全家桶用户，Firefly 是附带的增值功能。单独为 Firefly 订阅不值得——Midjourney 或 Lovart 的性价比更高。"),
        ],
        "zh-TW": [
            ("Firefly 和 Midjourney 哪個好？", "純圖片質量：Midjourney 勝出。Adobe 生態整合：Firefly 勝出。"),
            ("免費額度夠用嗎？", "每月 25 個生成積分。個人測試夠用，商業項目不夠。"),
            ("能商用嗎？", "Adobe 聲稱可以，但法律上仍有灰色地帶。"),
            ("支持中文嗎？", "基本不支持。中文生成質量極差。"),
            ("值得訂閱嗎？", "已是 Adobe 用戶則有附加價值。單獨訂閱不值得。"),
        ],
        "ja": [
            ("Firefly vs Midjourney?", "画像品質はMidjourney勝ち。Adobe統合はFirefly勝ち。"),
            ("無料枠?", "月25クレジット。個人テストには十分。"),
            ("商用可能?", "Adobeは可能と主張。法的には灰色地帯。"),
            ("日本語対応?", "ほぼ未対応。"),
            ("订阅する価値?", "Adobeユーザーなら付加価値あり。単独購入は不值得。"),
        ],
        "ko": [
            ("Firefly vs Midjourney?", "이미지 품질은 Midjourney. Adobe 통합은 Firefly."),
            ("무료?", "월 25 크레딧. 개인 테스트에는 충분."),
            ("商用?", "Adobe는 가능 주장. 법적으로 회색 지대."),
            ("한국어?", "基本上不可用."),
            ("구독 가치?", "Adobe 사용자면 부가 가치. 단독 구독은 不值得."),
        ],
        "de": [
            ("Firefly vs Midjourney?", "Bildqualitaet: Midjourney. Adobe-Integration: Firefly."),
            ("Kostenlos?", "25 Credits/Monat. Fuer Tests ausreichend."),
            ("Kommerziell?", "Adobe sagt ja, rechtlich grau."),
            ("Deutsch?", "Basis, nicht sehr nuetzlich."),
            ("Abo lohnt sich?", "Fuer Adobe-Nutzer ja. Allein nicht."),
        ],
        "fr": [
            ("Firefly vs Midjourney ?", "Qualite image : Midjourney. Integration Adobe : Firefly."),
            ("Gratuit ?", "25 credits/mois. Suffisant pour tests."),
            ("Commercial ?", "Adobe dit oui, juridiquement gris."),
            ("Francais ?", "Basique, pas tres utile."),
            ("Abonnement ?", "Pour utilisateurs Adobe oui. Seul non."),
        ],
        "es": [
            ("Firefly vs Midjourney?", "Calidad imagen: Midjourney. Integracion Adobe: Firefly."),
            ("Gratis?", "25 creditos/mes. Suficiente para pruebas."),
            ("Comercial?", "Adobe dice si, legalmente gris."),
            ("Espanol?", "Basico, no muy util."),
            ("Suscripcion?", "Para usuarios Adobe si. Solo no."),
        ],
        "pt": [
            ("Firefly vs Midjourney?", "Qualidade imagem: Midjourney. Integracao Adobe: Firefly."),
            ("Gratis?", "25 creditos/mes. Suficiente para testes."),
            ("Comercial?", "Adobe diz sim, legalmente cinza."),
            ("Portugues?", "Basico, nao muito util."),
            ("Assinatura?", "Para usuarios Adobe sim. Sozinho nao."),
        ],
        "ru": [
            ("Firefly protiv Midjourney?", "Kachestvo: Midjourney. Integracija Adobe: Firefly."),
            ("Besplatno?", "25 kreditov/mesjac. Dlja testov dostatochno."),
            ("Kommersija?", "Adobe govorit da, juridicheski seraja zona."),
            ("Russkij?", "Bazovyj, ne ochen polezno."),
            ("Podpiska?", "Dlja polzovatelej Adobe da. Otdelno net."),
        ],
    },
}

TOPIC_MAP = {
    "stable-video-diffusion": "svd",
    "luma-dream-machine": "luma",
    "adobe-firefly": "adobe",
}

def detect_lang(fname):
    for l in ["zh-TW", "zh", "ja", "ko", "de", "fr", "es", "pt", "ru"]:
        if fname.startswith(l + "-") or f"-{l}." in fname:
            return l
    return None

def detect_topic(fname):
    for pattern, topic in TOPIC_MAP.items():
        if pattern in fname:
            return topic
    return None

def add_faq(filepath, lang, topic):
    with open(filepath) as f:
        content = f.read()

    # Skip if already has FAQ
    faq_count = len(re.findall(r'\*\*.*?\?\*\*', content))
    if faq_count >= 5:
        return 0

    faqs = FAQ_CONTENT.get(topic, {}).get(lang, [])
    if not faqs:
        return 0

    # Find CTA section (before ---)
    cta_pos = content.find("\n---\n")
    if cta_pos == -1:
        cta_pos = len(content)

    # Build FAQ section
    faq_header = {
        "zh": "## 常见问题\n\n",
        "zh-TW": "## 常見問題\n\n",
        "ja": "## よくある質問\n\n",
        "ko": "## 자주 묻는 질문\n\n",
        "de": "## Haeufig gestellte Fragen\n\n",
        "fr": "## Questions frequentes\n\n",
        "es": "## Preguntas frecuentes\n\n",
        "pt": "## Perguntas frequentes\n\n",
        "ru": "## Chasto zadaemye voprosy\n\n",
    }.get(lang, "## FAQ\n\n")

    faq_text = faq_header
    for q, a in faqs:
        faq_text += f"**{q}**\n\n{a}\n\n"

    # Insert before CTA
    new_content = content[:cta_pos].rstrip() + "\n\n" + faq_text + "\n" + content[cta_pos:]

    with open(filepath, 'w') as f:
        f.write(new_content)
    return len(faqs)

blog_dir = "Output/Lovart-Blog-Pipeline"
total = 0
for fpath in sorted(glob.glob(f"{blog_dir}/*.md")):
    fname = os.path.basename(fpath)
    lang = detect_lang(fname)
    topic = detect_topic(fname)
    if not lang or not topic:
        continue
    added = add_faq(fpath, lang, topic)
    if added > 0:
        print(f"  {fname}: +{added} FAQ")
        total += added

print(f"\nTotal: {total} FAQ added")
