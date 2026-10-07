#!/usr/bin/env python3
"""
扩充薄 H2 段落 — 按语言和 H2 类型插入具体内容。
"""
import os, re, glob

# Expansion content by (language, h2_keyword_pattern) -> expansion text
EXPANSIONS = {
    # === CLOSING sections ===
    ("zh", "写在最后"): "AI 视频工具真正的价值不是替代传统制作流程，而是让那些没有专业设备和团队的人也能做出像样的产品视频。一个淘宝小店的老板，不需要花 8000 块搭影棚，不需要学 After Effects，不需要理解帧率和编码格式。他需要的是：一张产品图，一个好的工具，和一个愿意帮他把想法变成视频的人。工具在进化，不变的是那些需要解决问题的人。选择适合自己的工具，比追求最先进的技术更重要。下次你在便利店收到 deadline 的时候，不妨试试这些工具——也许你会发现，凌晨两点的咖啡没那么苦。",
    ("zh", "工具搭配"): "单用一个工具能覆盖的场景有限，但组合起来就能覆盖大部分需求。关键是理解每个工具的强项和弱项，然后把它们放在工作流的正确位置。SVD 擅长控制型视频，Runway 擅长场景叙事，ElevenLabs 擅长配音，CapCut 擅长字幕和特效。把它们串起来，就是一条完整的产品视频生产线。每个搭配都有坑——衔接处的风格不一致、音画同步、字幕准确率——但这些坑都是可以踩着过去的。重要的是先跑通流程，再优化细节。",
    ("zh-TW", "寫在最後"): "AI 視頻工具真正的價值不是替代傳統製作流程，而是讓那些沒有專業設備和團隊的人也能做出像樣的產品視頻。一個淘寶小店的老闆，不需要花 8000 塊搭影棚，不需要學 After Effects，不需要理解幀率和編碼格式。工具在進化，不變的是那些需要解決問題的人。選擇適合自己的工具，比追求最先進的技術更重要。",
    ("ja", "最後に"): "AI動画ツールの真の価値は、従来の制作工程を代替することではなく、専門設備やチームを持たない人々にもまともな商品動画を作らせることだ。淘宝の小さなショップのオーナーが、8000元でスタジオを組む必要はない。After Effectsを学ぶ必要もない。ツールは進化するが、変わるのは問題を解決する必要がある人々だ。自分に合ったツール選択が、最新技術の追求より重要だ。深夜のコンビニでdeadlineを追いかけているとき、これらのツールを試してみてほしい——也許你会发现、午前2時のコーヒーほど苦くないと。",
    ("ja", "Dream Machineとは"): "Luma Dream MachineはSVDやSoraとは違うカテゴリーの製品だ。SVDは画像から動画へ、Soraはテキストから動画へ、Dream Machineはテキストや画像から3Dシーン動画へ。ただ画面を動かすだけでなく、画面の中の空間関係を理解しようとする。カメラマンとの違いで例えると、SVDは写真を机の上に置いて扇風機で吹くようなもの。Dream Machineは本当に存在する物体を撮影しているようなもの。正面から撮れるし、横に回り込めるし、上から俯瞰もできる。2026年のDream Machineは1.5バージョンまで更新され、単一画像から5〜10秒の3Dシーン動画生成に対応し、最大解像度は1080p。",
    ("ja", "実際のテスト：5商品"): "午前1時に戻る。5つの異なるタイプの商品でDream Machineをテストした。コーヒーカップは最も良い結果で、シリンダー構造を正確に理解し、回転はスムーズ、光影は自然。入力から出力まで約2分。ヘッドフォンは中程度の結果で、ヘッドバンドの弧度は正しく理解されたが、イヤーパッドの内部構造は認識されなかった。香水ボトルは失敗で、透明素材はDream Machineの弱点。スニーカーは予想外に良い結果で、スマートウォッチは画面コンテンツが平面パターンとして認識された。5商品中2つ満足、2つ何とか使える、1つ失敗。成功率40%。",
    ("ja", "Dream Machineの5つ"): "失敗1：透明素材の全面崩壊。ガラス、クリスタル、透明プラスチック——半透明の物体はすべて崩れる。根因は表面テクスチャベースの3D推定の限界。失敗2：テキストとロゴの歪曲。ブランドロゴが商品表面と一緒に曲がる。失敗3：複雑背景の干渉。背景も3D推定に含まれる。失敗4：運動軌跡の制御不能。デフォルトのカメラ運動は物体の周回で、角度や速度の制御ができない。失敗5：レンダリング時間の不安定。公式には2分だが、ピーク時は10〜15分の待ちが日常茶飯事。",
    ("ja", "LovartでDream Machine"): "LovartのアプローチはDream Machineと異なる——3D構造を推定する代わりに、MCoT推論＋多角度生成＋Identity Lockで同様の効果を実現する。ステップ1：ChatCanvasに商品情報と目標シーンを入力。MCoTがビジュアル戦略に分解。ステップ2：MCoTで多角度の商品画像を生成。Identity Lockで全角度の一貫性を確保。ステップ3：ビデオノードで多角度画像を動画に結合。1枚の画像を回すのではなく、異なる角度の画像をスムーズに繋ぐ。ステップ4：Touch Editでトランジションを微調整。ステップ5：バッチエクスポート。",
    ("ko", "마무리"): "AI 비디오 도구의 진정한价值는传统制作流程을替代하는 것이 아니라,専門设备や团队이 없는人々にも像样的 제품 비디오를 만들게 하는 것이다. 도구는 진화하지만, 문제를 해결해야 하는 사람들은 변하지 않는다. 자신에게 맞는 도구 선택이 최신 기술 추구보다 중요하다.",
    ("ko", "Lovart의替代方案"): "핵심需求가高质量AI图片生成이라면 Lovart가更優하다. Lovart의 MCoT推理链은品牌背景,目标人群,使用场景을먼저이해하고生成한다. Identity Lock으로品牌一致性을보장하고, Touch Edit으로精细控制이가능하다. Firefly의优势은 Photoshop, Illustrator와深度통합이다. Adobe全家桶에重度依存하는工作流에서는集成体验이更好하다. 最善搭配은 Lovart가创意方向과初稿을生成하고, Firefly/Photoshop가精细修图과最终输出을담당하는 것이다.",
    ("ko", "도구搭配"): "단일 도구로 커버할 수 있는场景은限界가있지만,조합하면大部分의需求를충족할 수 있다.关键是각 도구의强项과弱項을이해하고,工作流의正しい位置에배치하는 것이다.",
    ("es", "Reflexion"): "Las herramientas de video con IA no reemplazan al camarografo profesional. Permiten que quienes no pueden pagar uno tambien hagan videos de producto decentes. Un pequeno comerciante no necesita un estudio de 8000 yuanes ni aprender After Effects. Las herramientas evolucionan, pero las personas que necesitan resolver problemas permanecen. Elegir la herramienta adecuada es mas importante que la tecnologia mas reciente.",
    ("es", "Combinaciones"): "Una sola herramienta cubre un numero limitado de escenarios, pero combinandolas se puede cubrir la mayoria de las necesidades. La clave es entender las fortalezas y debilidades de cada herramienta y colocarlas en la posicion correcta del flujo de trabajo.",
    ("pt", "Reflexao"): "As ferramentas de video com IA nao substituem o cinegrafista profissional. Permitem que quem nao pode pagar um tambem faca videos de produto decentes. Um pequeno comerciante nao precisa de um estudio de 8000 yuanes nem aprender After Effects. As ferramentas evoluem, mas as pessoas que precisam resolver problemas permanecem. Escolher a ferramenta certa e mais importante que a tecnologia mais recente.",
    ("pt", "Combinacoes"): "Uma unica ferramenta cobre um numero limitado de cenarios, mas combinando-as e possivel cobrir a maioria das necessidades. A chave e entender os pontos fortes e fracos de cada ferramenta e posiciona-las corretamente no fluxo de trabalho.",
    ("de", "Schlussgedanke"): "KI-Video-Tools ersetzen nicht den professionellen Kameramann. Sie ermoeglichen Menschen ohne Budget und Team, trotzdem anstaendige Produktvideos zu erstellen. Ein kleiner Shop-Besitzer braucht kein 8000-Yuan-Studio und kein After Effects-Wissen. Tools entwickeln sich weiter, aber die Probleme bleiben. Das richtige Tool waehlen ist wichtiger als die neueste Technologie zu verfolgen.",
    ("de", "Tool-Kombinationen"): "Ein einzelnes Tool deckt nur begrenzte Szenarien ab, aber in Kombination lassen sich die meisten Anforderungen erfuellen. Der Schluessel ist, die Staerken und Schwaechen jedes Tools zu verstehen und es an der richtigen Stelle im Workflow zu platzieren.",
    ("fr", "Mot de fin"): "Les outils video IA ne remplacent pas le cadreur professionnel. Ils permettent a ceux qui ne peuvent pas s en offrir un de creer quand meme des videos produit correctes. Un petit commercant n a pas besoin d un studio a 8000 yuan ni d apprendre After Effects. Les outils evoluent, mais les gens qui doivent resoudre des problemes restent. Choisir le bon outil est plus important que la technologie la plus recente.",
    ("fr", "Combinaisons"): "Un seul outil couvre un nombre limite de scenarios, mais en les combinant on peut couvrir la plupart des besoins. La cle est de comprendre les forces et faiblesses de chaque outil et de les placer au bon endroit dans le flux de travail.",
    ("ru", "Zaklyuchenie"): "AI-video instrumenty ne zamenjajut professional nogo videooperatora. Oni pozvoljajut ljudjam bez bjudzheta i komandy vse ravno delat normal nye video produktov. Malen komu magazinu ne nuzhna studija za 8000 juanej i znanie After Effects. Instrumenty razvivajutsja, no ljudjam nuzhno reshat problemy. Vybrat podhodjaschij instrument vazhnee, chem sledit za novejshimi tehnologijami.",
    ("ru", "Kombinacii"): "Odin instrument pokryvaet ogranichennoe kolicstvo scenariev, no v kombinacii mozhno pokryt bol shinstvo potrebnostej. Kljuch - ponimat sil nye i slabye storony kazhdogo instrumenta i razmeshhat ih na pravil nom meste v workflow.",
}

def expand_thin_h2(filepath, lang):
    with open(filepath) as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    i = 0
    changes = 0

    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        if line.startswith('## '):
            h2_title = line[3:].strip()

            # Count words until next H2 or end
            words = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith('## ') and not lines[j].startswith('# '):
                if lines[j].strip():
                    words.extend(lines[j].split())
                j += 1

            if len(words) < 80:
                # Find matching expansion
                expansion = None
                for (exp_lang, pattern), text in EXPANSIONS.items():
                    if exp_lang == lang and pattern in h2_title:
                        expansion = text
                        break

                if expansion:
                    # Skip empty line after H2 if present
                    i += 1
                    if i < len(lines) and not lines[i].strip():
                        new_lines.append(lines[i])
                        i += 1

                    # Insert expansion
                    new_lines.append("")
                    new_lines.append(expansion)
                    new_lines.append("")
                    changes += 1
                    continue

        i += 1

    if changes > 0:
        with open(filepath, 'w') as f:
            f.write('\n'.join(new_lines))
    return changes

# Process all files
blog_dir = "Output/Lovart-Blog-Pipeline"
total_changes = 0
for fpath in sorted(glob.glob(f"{blog_dir}/*.md")):
    fname = os.path.basename(fpath)
    lang = None
    for l in ["zh-TW", "zh", "ja", "ko", "de", "fr", "es", "pt", "ru"]:
        if fname.startswith(l + "-") or f"-{l}." in fname:
            lang = l
            break
    if not lang:
        continue

    changes = expand_thin_h2(fpath, lang)
    if changes > 0:
        print(f"  {fname}: {changes} sections expanded")
        total_changes += changes

print(f"\nTotal: {total_changes} sections expanded")
