from lib_web import mc, pred, fill, bugfix, write_page, t_page

ITEMS3 = '<div class="container">\n  <div class="item">1</div>\n  <div class="item">2</div>\n  <div class="item">3</div>\n</div>'
ITEM_CSS = '''.item {
  width: 50px;
  height: 50px;
}'''
LAYOUT_PROBE = "(function () { var t = Array.from(document.querySelectorAll('.item')).map(function (e) { return Math.round(e.getBoundingClientRect().top); }); var l = Array.from(document.querySelectorAll('.item')).map(function (e) { return Math.round(e.getBoundingClientRect().left); }); return t.every(function (v) { return v === t[0]; }) ? 'row' : (l.every(function (v) { return v === l[0]; }) ? 'column' : 'other'); })()"

STAGE = {
    "number": 9,
    "title": "Flexbox",
    "subtitle": "display: flex、主軸と交差軸、並べ方・揃え方・伸び縮み",
    "goals": [
        "display: flex で、子要素を横一列に並べられる",
        "Flex コンテナ（親）と Flex アイテム（子）、主軸と交差軸という用語を使える",
        "flex-direction・justify-content・align-items・gap・flex-wrap を使える",
        "flex（flex: 1 など）で、アイテムの幅を割り振れる",
        "ナビゲーションバー・カードの横並び・中央寄せを Flexbox で作れる",
    ],
    "prerequisites": ["ボックスモデル・display（ステージ8）", "CSS の基本・セレクタ（ステージ6〜7）"],
    "topics": [
        "display: flex と Flex コンテナ・Flex アイテム",
        "主軸と交差軸、flex-direction",
        "justify-content（主軸方向の並べ方）",
        "align-items（交差軸方向の揃え方）",
        "gap と flex-wrap",
        "flex（flex-grow）によるアイテムの伸び縮み",
    ],
    "pitfalls": [
        "display: flex は、並べたい要素の「親」に書く（子ではない）",
        "justify-content や align-items は、display: flex を指定した親でないと効かない",
        "flex-direction: column にすると、主軸が縦になり、justify-content と align-items の向きが入れ替わる",
        "align-items が縦方向の中央揃えに効くのは、親に height（高さ）がある場合",
        "display の値は flex（flexbox や inline-flexbox などは存在しない）",
    ],
    "next_links": ["画面の幅に合わせてレイアウトを変える「レスポンシブデザイン」を学びます（ステージ10）"],
    "lesson": {
        "intro": "ボタンを横に並べる、メニューを左右に振り分ける、カードを均等に並べる、要素を中央に置く。昔は、このような配置に工夫が必要でした。現在の CSS では、Flexbox（フレキシブルボックス）を使うと、少ない記述で実現できます。",
        "sections": [
            {
                "id": "S09-L1",
                "title": "Flexbox の基本",
                "read_minutes": 3,
                "body": [
                    "親要素に display: flex; を指定すると、親は Flex コンテナ、その直接の子は Flex アイテムになります。アイテムは、標準では、横一列（行方向）に並びます。block 要素の子は、通常は縦に並ぶので、display: flex の効果が分かりやすい変化です。",
                    "アイテムが並ぶ方向を主軸、それに垂直な方向を交差軸といいます。flex-direction で主軸の向きを決めます（row = 横、column = 縦。標準は row）。",
                    "justify-content は、主軸方向の並べ方です。flex-start（始点に寄せる。標準）・center（中央）・flex-end（終点に寄せる）・space-between（両端に寄せて間を均等に）・space-around・space-evenly などがあります。align-items は、交差軸方向の揃え方で、stretch（標準）・flex-start・center・flex-end があります。縦方向の中央揃えには、親に高さが必要です。",
                    "gap は、アイテムの間隔を一括で決めます。アイテムが親の幅に収まらないときは、標準では縮みますが、flex-wrap: wrap を指定すると、折り返して、次の行に並びます。",
                ],
                "glossary": [
                    {"term": "Flex コンテナ", "definition": "display: flex を指定した親要素。"},
                    {"term": "Flex アイテム", "definition": "Flex コンテナの直接の子要素。"},
                    {"term": "主軸 / 交差軸", "definition": "アイテムが並ぶ方向 / それに垂直な方向。"},
                ],
                "examples": [
                    {
                        "id": "S09-E1", "title": "横に並べる", "language": "css",
                        "context_html": ITEMS3,
                        "code": '''.container {
  display: flex;
}
.item {
  width: 50px;
  height: 50px;
  background-color: lightblue;
}''',
                        "line_notes": ["親（.container）に display: flex を指定すると、子（.item）が横一列に並びます。", "display: flex がなければ、div は、ブロック要素なので、縦に並びます。"],
                        "preview": {"format": "css", "given_html": ITEMS3},
                        "verify": {"format": "css", "given_html": ITEMS3, "expr": LAYOUT_PROBE + " === 'row'"},
                    },
                    {
                        "id": "S09-E2", "title": "並べ方と揃え方", "language": "css",
                        "context_html": ITEMS3,
                        "code": '''.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 300px;
  height: 120px;
}
.item {
  width: 50px;
  height: 50px;
  background-color: lightblue;
}''',
                        "line_notes": ["space-between で、最初のアイテムを左端、最後のアイテムを右端に寄せ、間を均等にします。", "align-items: center で、縦方向（交差軸）の中央に揃えます。親に height があるので、効果が出ます。"],
                        "preview": {"format": "css", "given_html": ITEMS3},
                        "verify": {"format": "css", "given_html": ITEMS3, "expr": "(function () { var c = document.querySelector('.container').getBoundingClientRect(); var it = document.querySelectorAll('.item'); var f = it[0].getBoundingClientRect(), l = it[2].getBoundingClientRect(); return Math.round(f.left) === Math.round(c.left) && Math.round(l.right) === Math.round(c.right) && Math.abs((f.top + f.height / 2) - (c.top + c.height / 2)) < 1; })()"},
                    },
                    {
                        "id": "S09-E3", "title": "gap と折り返し", "language": "css",
                        "context_html": ITEMS3,
                        "code": '''.container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  width: 200px;
}
.item {
  width: 80px;
  height: 50px;
  background-color: lightblue;
}''',
                        "line_notes": ["80px + 10px + 80px = 170px は 200px に収まるので、2つ並びます。", "3つ目は、収まらないので、flex-wrap: wrap により次の行に折り返します。"],
                        "preview": {"format": "css", "given_html": ITEMS3},
                        "verify": {"format": "css", "given_html": ITEMS3, "expr": "(function () { var it = Array.from(document.querySelectorAll('.item')).map(function (e) { return e.getBoundingClientRect(); }); return Math.round(it[0].top) === Math.round(it[1].top) && it[2].top > it[0].top && Math.round(it[1].left - it[0].right) === 10; })()"},
                    },
                ],
            },
            {
                "id": "S09-L2",
                "title": "アイテムの伸び縮み",
                "read_minutes": 2,
                "body": [
                    "flex プロパティで、アイテムが、余った幅をどう分け合うかを決められます。flex: 1 を、すべてのアイテムに指定すると、親の幅を等分します。flex: 1 と flex: 2 のアイテムを並べると、余った幅が、1 : 2 の割合で分けられます（幅は、1 : 2 の比になります）。",
                    "flex: 1 は、flex-grow（余った幅を分け合う割合）が 1 であることを表す書き方（flex: 1 1 0 の省略）です。カードを横に均等に並べるときや、検索ボックスを、残りの幅いっぱいに伸ばしたいときに使います。",
                    "親に display: flex、justify-content: center、align-items: center を指定すると、子要素を、親の中央に置けます。以前は難しかった「縦横の中央寄せ」が、簡単に書けます。",
                ],
                "glossary": [
                    {"term": "flex: 1", "definition": "余った幅を、他のアイテムと等しい割合で分け合って、伸びる指定。"},
                    {"term": "flex-grow", "definition": "余った幅を、どれだけの割合で分けてもらうかを決める値。"},
                ],
                "examples": [
                    {
                        "id": "S09-E4", "title": "flex で幅を分ける", "language": "css",
                        "context_html": '<div class="container">\n  <div class="a">A</div>\n  <div class="b">B</div>\n</div>',
                        "code": '''.container {
  display: flex;
  width: 300px;
}
.a {
  flex: 1;
}
.b {
  flex: 2;
}''',
                        "line_notes": ["300px を 1 : 2 で分けるので、A は 100px、B は 200px になります。"],
                        "preview": {"format": "css", "given_html": '<div class="container">\n  <div class="a">A</div>\n  <div class="b">B</div>\n</div>'},
                        "verify": {"format": "css", "given_html": '<div class="container">\n  <div class="a">A</div>\n  <div class="b">B</div>\n</div>', "expr": "Math.round(document.querySelector('.a').getBoundingClientRect().width) === 100 && Math.round(document.querySelector('.b').getBoundingClientRect().width) === 200"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "子に display: flex を書く", "wrong_code": ".item { display: flex; }", "why": "並べたい要素（子）ではなく、それを囲む親に指定します。", "fix": ".container { display: flex; }"},
            {"title": "flex の指定なしに justify-content を使う", "wrong_code": ".container { justify-content: center; }", "why": "display: flex を指定した親にだけ効きます。ほかの親には効果がありません。", "fix": ".container { display: flex; justify-content: center; }"},
            {"title": "display の値の書き間違い", "wrong_code": "display: flexbox;", "why": "flexbox という値はなく、無効になります。正しくは flex です。", "fix": "display: flex;"},
            {"title": "縦の中央揃えに高さがない", "wrong_code": ".container { display: flex; align-items: center; }", "why": "親の高さが、中身の高さしかないと、縦方向に余白がなく、中央揃えの効果が見えません。", "fix": ".container { height: 200px; }"},
        ],
        "checkpoints": [
            "display: flex は、並べたい子の親に指定する",
            "主軸は並ぶ方向、交差軸はそれに垂直な方向",
            "justify-content は主軸方向、align-items は交差軸方向",
            "gap でアイテムの間隔、flex-wrap: wrap で折り返し",
            "flex: 1 で余った幅を等分する",
            "中央寄せは、display: flex + justify-content + align-items",
        ],
        "next_bridge": "Flexbox で、横並びや中央寄せが書けるようになりました。問題で、主軸と交差軸の考え方を確かめましょう。",
    },
}

QUESTIONS = [
    mc(
        title="display: flex を書く場所", lang="css",
        prompt="3つの div を横一列に並べたい。display: flex は、どの要素に指定しますか？",
        code='''<div class="container">
  <div class="item">1</div>
  <div class="item">2</div>
  <div class="item">3</div>
</div>''',
        choices=[
            ("3つの .item それぞれに指定する", "子（.item）に指定すると、子の中身の並べ方が変わるだけで、3つの子が横に並ぶことにはなりません。並べたい要素の「親」に指定します。"),
            ("3つを囲んでいる、親の .container に指定する", ""),
            ("body 要素に指定する", "body に指定すると、body の直接の子（ここでは .container）が、横に並ぶだけです。3つの .item を並べたいなら、それらの直接の親に指定します。"),
        ],
        correct=1,
        why="Flexbox は、親（Flex コンテナ）に指定して、その直接の子（Flex アイテム）を並べる仕組みだから。",
        expl="display: flex を指定した要素が Flex コンテナとなり、その直接の子が Flex アイテムになります。孫以降の要素は、Flex アイテムではありません。",
        concepts=["display: flex", "Flexコンテナ"], diff=1,
        hint="並べたいのは3つの子です。それらを囲んでいるのは？",
        ok="正解！Flexbox は、親に指定します。",
        ng="惜しい！並べたい要素の「親」に指定します。",
    ),
    pred(
        title="display: flex の並び方", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、3つのアイテムは、どう並びますか？",
        code='''.container {
  display: flex;
}
''' + ITEM_CSS,
        check={"format": "css", "given_html": ITEMS3, "probe": LAYOUT_PROBE},
        choices=[
            ("縦に並ぶ（1つずつ改行される）", "display: flex を指定すると、直接の子は、標準で、横一列（行方向）に並びます。縦に並ぶのは、flex を指定しない div の場合です。", "column"),
            ("横一列に並ぶ", "", "row"),
            ("1つの場所に重なって表示される", "アイテムは、重なりません。主軸方向（標準は横）に、順番に並びます。", "other"),
        ],
        correct=1,
        why="Flex コンテナの標準の flex-direction は row（横方向）だから。",
        expl="display: flex がない div は、ブロック要素なので縦に並びます。flex を指定すると、flex-direction の標準（row）の向きに、横一列で並びます。",
        concepts=["display: flex", "flex-direction"], diff=1,
        hint="flex-direction の標準の値は row です。",
        ok="正解！標準は横一列です。",
        ng="惜しい！flex-direction の標準の向きを確認しましょう。",
    ),
    pred(
        title="space-between の並び方", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、3つのアイテムは、どのように並びますか？（コンテナの幅は 300px、アイテムの幅は 50px です）",
        code='''.container {
  display: flex;
  justify-content: space-between;
  width: 300px;
}
''' + ITEM_CSS,
        check={"format": "css", "given_html": ITEMS3, "probe": "(function () { var c = document.querySelector('.container').getBoundingClientRect(); var it = Array.from(document.querySelectorAll('.item')).map(function (e) { return e.getBoundingClientRect(); }); var gap1 = it[1].left - it[0].right, gap2 = it[2].left - it[1].right; if (Math.round(it[0].left) === Math.round(c.left) && Math.round(it[2].right) === Math.round(c.right) && Math.round(gap1) === Math.round(gap2) && gap1 > 1) return 'between'; if (Math.round(it[0].left) === Math.round(c.left)) return 'start'; return 'other'; })()"},
        choices=[
            ("左端に詰めて並ぶ", "左端に詰めて並ぶのは、justify-content の標準の値（flex-start）です。space-between は、両端に寄せて、間を均等にします。", "start"),
            ("両端に寄せて並び、アイテムの間が均等に空く", "", "between"),
            ("中央に寄って並ぶ", "中央に寄せるのは、justify-content: center です。", "other"),
        ],
        correct=1,
        why="space-between は、最初と最後のアイテムを両端に寄せ、間の余白を等しくするから。",
        expl="ここでは、300 − 50×3 = 150px の余りが、アイテムの間の2か所に、75px ずつ分けられます。ナビゲーションバーで、ロゴを左、メニューを右に振り分けるときにもよく使います。",
        concepts=["justify-content", "space-between"], diff=2,
        hint="space-between は、「間（between）に余白を入れる」という意味です。",
        ok="正解！両端に寄せて、間を均等にします。",
        ng="惜しい！space-between の名前の意味を考えましょう。",
    ),
    fill(
        title="縦に並べる", lang="css",
        prompt="3つのアイテムを、Flexbox のまま、縦一列に並べます。【空欄1】に入れる値を答えてください。",
        code='''.container {
  display: flex;
  flex-direction: __1__;
}
''' + ITEM_CSS,
        check={"format": "css", "given_html": ITEMS3, "expr": LAYOUT_PROBE + " === 'column'"},
        blanks=[(["column"], False)],
        wrong=[("b1", "vertical", "flex-direction の値は、row・column・row-reverse・column-reverse です。vertical という値はなく、無効になり、横一列のままです。")],
        why="flex-direction: column にすると、主軸が縦方向になるから。",
        expl="column にすると、主軸が縦になり、justify-content は縦方向の並べ方、align-items は横方向の揃え方になります。向きが入れ替わる点に注意しましょう。",
        concepts=["flex-direction", "主軸"], diff=2,
        hint="「列（縦）」を意味する英単語です。",
        ok="正解！column で縦に並びます。",
        ng="惜しい！flex-direction の値を確認しましょう。",
    ),
    fill(
        title="縦方向の中央に揃える", lang="css",
        prompt="高さ 200px のコンテナの中で、アイテムを縦方向（交差軸）の中央に揃えます。【空欄1】に入れる値を答えてください。",
        code='''.container {
  display: flex;
  height: 200px;
  align-items: __1__;
}
.item {
  width: 50px;
  height: 50px;
}''',
        check={"format": "css", "given_html": '<div class="container">\n  <div class="item">1</div>\n</div>', "expr": "(function () { var c = document.querySelector('.container').getBoundingClientRect(); var i = document.querySelector('.item').getBoundingClientRect(); return Math.abs((i.top + i.height / 2) - (c.top + c.height / 2)) < 1; })()"},
        blanks=[(["center"], False)],
        wrong=[("b1", "middle", "middle という値はありません。中央揃えは center です。無効な値は無視され、アイテムは上に寄ったままです。")],
        why="align-items: center で、交差軸（ここでは縦）の中央に揃うから。",
        expl="標準の flex-direction（row）では、主軸は横、交差軸は縦です。align-items は交差軸方向の揃え方なので、縦の中央揃えに使います。",
        concepts=["align-items", "交差軸"], diff=2,
        hint="「中心」を意味する英単語です。",
        ok="正解！align-items: center です。",
        ng="惜しい！「真ん中」を表す、CSS の値を入力しましょう。",
    ),
    bugfix(
        title="効かない justify-content", lang="css",
        prompt="アイテムを水平方向の中央に置くつもりが、左に寄ったままです。正しい直し方はどれですか？",
        code='''.container {
  justify-content: center;
  width: 300px;
}''',
        fixed='''.container {
  display: flex;
  justify-content: center;
  width: 300px;
}''',
        check={"format": "css", "given_html": '<div class="container">\n  <div class="item" style="width:50px;height:50px">1</div>\n</div>', "expr": "(function () { var c = document.querySelector('.container').getBoundingClientRect(); var i = document.querySelector('.item').getBoundingClientRect(); return Math.abs((i.left + i.width / 2) - (c.left + c.width / 2)) < 1; })()"},
        choices=[
            ("justify-content を、align-items に変える", "align-items は、交差軸（縦）方向の揃え方です。水平方向の中央寄せには、justify-content を使います（その前に、display: flex が必要です）。"),
            ("コンテナに display: flex を追加する", ""),
            ("center を middle に変える", "middle という値はありません。無効になり、中央に寄りません。"),
        ],
        correct=1, fmt="text",
        why="justify-content は、display: flex を指定した親でないと効かないから。",
        expl="justify-content や align-items は、Flexbox（や Grid）のためのプロパティです。display: flex がない親に書いても、エラーにならず、無視されます。",
        concepts=["justify-content", "display: flex"], diff=2,
        hint="justify-content が働くには、親がどんな状態である必要があるでしょう？",
        ok="正解！display: flex が必要です。",
        ng="惜しい！親の display を確認しましょう。",
    ),
    pred(
        title="gap を含めた位置", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、3つ目のアイテムの左端は、コンテナの左端から何 px の位置にありますか？数字だけを入力してください。",
        code='''.container {
  display: flex;
  gap: 10px;
}
''' + ITEM_CSS,
        check={"format": "css", "given_html": ITEMS3, "probe": "Math.round(document.querySelectorAll('.item')[2].getBoundingClientRect().left - document.querySelector('.container').getBoundingClientRect().left)", "expected": 120},
        out="120",
        wrong=[("100", "アイテムの間に、gap の 10px が入ります。50 + 50 = 100px に、さらに gap が 2 か所分（20px）加わります。"), ("110", "gap は、アイテムとアイテムの間の2か所にあります。1か所だけではありません。")],
        why="(50px + 10px) × 2 = 120px になるから。",
        expl="gap は、アイテムの間（ここでは、1つ目と2つ目の間、2つ目と3つ目の間の2か所）に入ります。3つ目の左端は、1つ目（50px）+ gap（10px）+ 2つ目（50px）+ gap（10px）= 120px の位置です。",
        concepts=["gap"], diff=3,
        hint="3つ目の左側には、アイテムが2つと、gap が2か所あります。",
        ok="正解！gap は、間の数だけ入ります。",
        ng="惜しい！gap が何か所に入るか数えましょう。",
    ),
    bugfix(
        title="display の値の書き間違い", lang="css",
        prompt="アイテムを横に並べるつもりが、縦のままです。2行目を正しく書き直して入力してください（2行目の内容だけを入力）。",
        code='''.container {
  display: flexbox;
}
''' + ITEM_CSS,
        fixed='''.container {
  display: flex;
}
''' + ITEM_CSS,
        check={"format": "css", "given_html": ITEMS3, "expr": LAYOUT_PROBE + " === 'row'"},
        target_line=2, accepted=["display: flex;", "display:flex;", "display: flex"],
        wrong=[("display: flexbox;", "元のコードのままです。flexbox という値はなく、無効になります。正しい値は flex です。")],
        why="display の値は、flex であり、flexbox ではないから。",
        expl="CSS のプロパティの値の綴りを間違えても、エラーは出ず、宣言が無視されるだけです。見た目が変わらないときは、値の綴りを確認します。",
        concepts=["display: flex", "綴りミス"], diff=2,
        hint="Flexbox の機能を指定する display の値は、短い語です。",
        ok="正解！display: flex です。",
        ng="惜しい！値の綴りを確認しましょう。",
    ),
    pred(
        title="flex: 1 と flex: 2", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、コンテナの幅は 300px です。A と B の幅は、それぞれ何 px になりますか？",
        code='''.container {
  display: flex;
  width: 300px;
}
.a { flex: 1; }
.b { flex: 2; }''',
        check={"format": "css", "given_html": '<div class="container">\n  <div class="a">A</div>\n  <div class="b">B</div>\n</div>', "probe": "['.a', '.b'].map(function (s) { return Math.round(document.querySelector(s).getBoundingClientRect().width); }).join(',')"},
        choices=[
            ("A: 150px、B: 150px", "flex の値が違うので、等分にはなりません。1 : 2 の割合で分けられます。", "150,150"),
            ("A: 100px、B: 200px", "", "100,200"),
            ("A: 200px、B: 100px", "flex の値が大きい B のほうが、広くなります。", "200,100"),
        ],
        correct=1,
        why="余った幅 300px が、1 : 2 の割合で分けられ、A が 100px、B が 200px になるから。",
        expl="flex: 1 を全部に指定すれば、等分です。値を変えると、その割合で幅が決まります。カードの横並びや、残りの幅いっぱいに伸ばしたい部品に便利です。",
        concepts=["flex", "flex-grow"], diff=3,
        hint="300px を、1 : 2 に分けます。",
        ok="正解！1 : 2 の割合で分けられます。",
        ng="惜しい！flex の値の比で、幅を分けます。",
    ),
    write_page(
        title="3つのカードを横に並べる", lang="css", fmt="css",
        prompt="次の HTML の .cards に、CSS だけで、次の見た目を指定してください。\n・.cards の幅を 600px にし、3つの .card を横一列に並べる\n・.card どうしの間隔を 16px にする\n・3つの .card の幅を、すべて等しくして、.cards の幅いっぱいに広げる（flex を使う）\n・.card の中の文字を、水平・垂直とも中央に揃える（.card 自身も、Flexbox にする）\n・.card の高さを 100px にする",
        given_html='<div class="cards">\n  <div class="card">A</div>\n  <div class="card">B</div>\n  <div class="card">C</div>\n</div>',
        starter="/* ここに CSS を書きましょう */\n",
        ref='''.cards {
  display: flex;
  gap: 16px;
  width: 600px;
}
.card {
  flex: 1;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: lightblue;
}''',
        alts=['''.cards { width: 600px; display: flex; column-gap: 16px; }
.card { flex: 1 1 0; height: 100px; display: flex; align-items: center; justify-content: center; }'''],
        bads=[
            ('''.cards {
  display: flex;
  width: 600px;
}
.card {
  flex: 1;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}''', "カードの間隔（gap）が 16px になっていません。"),
            ('''.cards {
  display: flex;
  gap: 16px;
  width: 600px;
}
.card {
  width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}''', "カードの幅が 100px に固定されていて、.cards の幅いっぱいに広がっていません。flex: 1 で、余った幅を等分します。"),
        ],
        tests=[
            t_page("3つのカードが、横一列に並んでいる", "(function () { var t = Array.from(document.querySelectorAll('.card')).map(function (e) { return Math.round(e.getBoundingClientRect().top); }); return t.length === 3 && t.every(function (v) { return v === t[0]; }); })()"),
            t_page("カードどうしの間隔が 16px", "(function () { var c = Array.from(document.querySelectorAll('.card')).map(function (e) { return e.getBoundingClientRect(); }); return Math.round(c[1].left - c[0].right) === 16 && Math.round(c[2].left - c[1].right) === 16; })()"),
            t_page("3つのカードの幅が等しく、.cards の幅いっぱいに広がっている", "(function () { var c = Array.from(document.querySelectorAll('.card')).map(function (e) { return e.getBoundingClientRect(); }); var p = document.querySelector('.cards').getBoundingClientRect(); return Math.abs(c[0].width - c[1].width) < 1 && Math.abs(c[1].width - c[2].width) < 1 && Math.abs(c[0].left - p.left) < 1 && Math.abs(c[2].right - p.right) < 1 && Math.round(p.width) === 600; })()"),
            t_page("カードの高さが 100px", "Math.round(document.querySelector('.card').getBoundingClientRect().height) === 100"),
            t_page("カードの中の文字が、水平・垂直とも中央にある", "(function () { var el = document.querySelector('.card'); var s = getComputedStyle(el); return s.display === 'flex' && s.justifyContent === 'center' && s.alignItems === 'center'; })()", visible=False),
        ],
        why="親に display: flex と gap、子に flex: 1 を指定して等分に並べ、子自身も flex にして、中身を中央に揃えるから。",
        expl="flex: 1 を全部のカードに指定すると、間隔（gap）を除いた幅を等分します。カードの中の文字を中央に置くには、カード自身を Flexbox にして、justify-content と align-items を center にします。Flexbox は、入れ子にして使えます。",
        concepts=["display: flex", "gap", "flex", "justify-content", "align-items"], diff=3,
        hint="親に display: flex と gap。子に flex: 1。子の中身は、子自身を flex にして中央に。",
        ok="正解！Flexbox でカードを並べられました。",
        ng="惜しい！間隔・幅・中身の揃えを、1つずつ確認しましょう。",
    ),
]
