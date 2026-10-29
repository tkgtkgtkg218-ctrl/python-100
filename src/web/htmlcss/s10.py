from lib_web import mc, pred, fill, bugfix, write_page, t_page

CARDS3 = '<div class="cards">\n  <div class="card">A</div>\n  <div class="card">B</div>\n  <div class="card">C</div>\n</div>'
MQ_RED = '''p {
  color: black;
}
@media (min-width: 600px) {
  p {
    color: red;
  }
}'''
HORIZ = "(function () { var t = Array.from(document.querySelectorAll('.card')).map(function (e) { return Math.round(e.getBoundingClientRect().top); }); return t.length === 3 && t.every(function (v) { return v === t[0]; }); })()"
STACK = "(function () { var r = Array.from(document.querySelectorAll('.card')).map(function (e) { return e.getBoundingClientRect(); }); return r.length === 3 && r[0].top < r[1].top && r[1].top < r[2].top && Math.round(r[0].left) === Math.round(r[1].left) && Math.round(r[1].left) === Math.round(r[2].left); })()"

STAGE = {
    "number": 10,
    "title": "レスポンシブデザインと簡単なページ制作",
    "subtitle": "viewport・メディアクエリ・柔軟なレイアウト・ページを組み立てる",
    "goals": [
        "レスポンシブウェブデザインとは何か、なぜ必要かを説明できる",
        "viewport の meta 要素の役割を説明できる",
        "max-width・% などの柔軟な指定で、画面幅に合わせて伸び縮みする箱を作れる",
        "メディアクエリ（@media）で、画面幅に応じて、スタイルを切り替えられる",
        "モバイルファーストの考え方で、スマホから PC まで対応するページを作れる",
        "ここまでの HTML・CSS の知識を組み合わせて、簡単なページを自分で作れる",
    ],
    "prerequisites": ["ステージ1〜9のすべて（特に、ボックスモデルと Flexbox）"],
    "topics": [
        "レスポンシブウェブデザインとは",
        "viewport の meta 要素",
        "max-width と相対的な幅（%）",
        "画像の幅の調整（max-width: 100%）",
        "メディアクエリ（@media (min-width / max-width)）",
        "モバイルファーストと flex-wrap",
        "簡単なページの制作",
    ],
    "pitfalls": [
        "viewport の meta 要素がないと、スマホでは、PC 向けの幅で表示されて小さくなる",
        "固定の幅（width: 800px など）は、画面が狭いと、はみ出して横スクロールになる",
        "メディアクエリの条件には、かっこ（( )）が必要（@media (min-width: 600px)）",
        "min-width は「その幅以上」、max-width は「その幅以下」",
        "画像は、max-width: 100%; height: auto; を付けないと、親の幅を超えることがある",
    ],
    "next_links": ["HTML と CSS の基本は、ここまでです。次は、JavaScript で動きを付けたり、CSS の Grid・アニメーションなどを学べます"],
    "lesson": {
        "intro": "Webページは、大きな PC の画面でも、小さなスマートフォンの画面でも見られます。画面の幅に合わせて、レイアウトを変えられるように作る考え方を「レスポンシブウェブデザイン」といいます。これまで学んだ HTML と CSS の知識を総動員して、どんな幅でも読みやすいページを作りましょう。",
        "sections": [
            {
                "id": "S10-L1",
                "title": "viewport と柔軟な幅",
                "read_minutes": 3,
                "body": [
                    "スマートフォンのブラウザは、PC 向けに作られたページを見られるように、標準では、広い幅（約 980px）で表示を作り、それを縮小して画面に収めます。そのため、スマホ向けに作ったページでも、小さく表示されてしまいます。これを防ぐのが、head に書く viewport の meta 要素です: <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">。「画面の幅を、そのまま表示の幅にする」という意味です。",
                    "画面幅に合わせて伸び縮みする箱は、固定の幅（width: 800px）ではなく、柔軟な指定で作ります。max-width: 600px; margin: 0 auto; と書くと、画面が広いときは 600px で中央に寄り、狭いときは画面の幅いっぱいに縮みます。幅を % で指定するのも、親の幅に合わせる方法です。",
                    "画像は、max-width: 100%; height: auto; を指定すると、親の幅を超えず、縦横の比率を保ったまま縮みます。",
                ],
                "glossary": [
                    {"term": "レスポンシブウェブデザイン", "definition": "画面の幅に合わせて、レイアウトを変える、Web ページの作り方。"},
                    {"term": "viewport", "definition": "ブラウザの表示領域。meta 要素で、その幅の扱いを指定する。"},
                    {"term": "max-width", "definition": "要素の幅の上限。これより広くならない。"},
                ],
                "examples": [
                    {
                        "id": "S10-E1", "title": "viewport の meta 要素", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>レスポンシブ</title>
</head>
<body>
  <p>スマホでも読みやすいページ</p>
</body>
</html>''',
                        "line_notes": ["5行目が、viewport の指定です。width=device-width で、表示の幅を、画面の幅に合わせます。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "expr": "document.querySelector('meta[name=viewport]').content.indexOf('width=device-width') >= 0"},
                    },
                    {
                        "id": "S10-E2", "title": "max-width で伸び縮み", "language": "css",
                        "context_html": '<div class="wrap">中身</div>',
                        "code": '''body { margin: 0; }
.wrap {
  max-width: 600px;
  margin: 0 auto;
  background-color: lightyellow;
}''',
                        "line_notes": ["画面が 600px より広ければ、幅 600px で中央に寄ります。", "画面が 600px より狭ければ、画面の幅いっぱいになります。"],
                        "preview": {"format": "css", "given_html": '<div class="wrap">中身</div>', "viewport": 800},
                        "verify": {"format": "css", "given_html": '<div class="wrap">中身</div>', "viewport": 800, "expr": "document.querySelector('.wrap').getBoundingClientRect().width === 600"},
                    },
                ],
            },
            {
                "id": "S10-L2",
                "title": "メディアクエリとページの組み立て",
                "read_minutes": 3,
                "body": [
                    "メディアクエリは、画面の幅などの条件に合うときだけ、スタイルを適用する仕組みです。@media (min-width: 600px) { ... } は「画面の幅が 600px 以上のとき」、@media (max-width: 600px) { ... } は「600px 以下のとき」です。条件には、かっこが必要です。",
                    "モバイルファーストは、まず、狭い画面（スマホ）向けのスタイルを基本として書き、広い画面で変えたいところだけ、min-width のメディアクエリで上書きする考え方です。スマホ向けは、シンプルな縦並びが基本なので、記述が少なくなります。",
                    "Flexbox は、レスポンシブと相性の良い仕組みです。flex-wrap: wrap で、幅が足りないときに折り返したり、メディアクエリで flex-direction を column と row に切り替えたりして、横並びと縦並びを切り替えられます。",
                    "ページを作るときは、(1) HTML で、header・main・footer などの構造を書く、(2) 基本のスタイル（文字・色・余白）を整える、(3) 画面幅ごとのレイアウトを、メディアクエリで調整する、の順で進めると、整理しやすくなります。",
                ],
                "glossary": [
                    {"term": "メディアクエリ", "definition": "@media で、画面の幅などの条件に応じて、スタイルを切り替える仕組み。"},
                    {"term": "モバイルファースト", "definition": "スマホ向けのスタイルを基本にして、広い画面向けを、あとから追加する設計の考え方。"},
                ],
                "examples": [
                    {
                        "id": "S10-E3", "title": "メディアクエリ", "language": "css",
                        "context_html": '<p>画面の幅で色が変わります</p>',
                        "code": MQ_RED,
                        "line_notes": ["標準では黒です。", "画面の幅が 600px 以上のときだけ、赤になります。この例では、画面幅 800px で表示しています。"],
                        "preview": {"format": "css", "given_html": '<p>画面の幅で色が変わります</p>', "viewport": 800},
                        "verify": {"format": "css", "given_html": '<p>画面の幅で色が変わります</p>', "viewport": 800, "expr": "getComputedStyle(document.querySelector('p')).color === 'rgb(255, 0, 0)'"},
                    },
                    {
                        "id": "S10-E4", "title": "モバイルファーストの横並び", "language": "css",
                        "context_html": CARDS3,
                        "code": '''.cards {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.card {
  padding: 16px;
  background-color: lightblue;
}
@media (min-width: 600px) {
  .cards {
    flex-direction: row;
  }
  .card {
    flex: 1;
  }
}''',
                        "line_notes": ["基本は、縦並び（column）です。スマホ向けのスタイルです。", "画面の幅が 600px 以上のときだけ、横並び（row）に切り替わります。"],
                        "preview": {"format": "css", "given_html": CARDS3, "viewport": 800},
                        "verify": {"format": "css", "given_html": CARDS3, "viewport": 800, "expr": HORIZ},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "viewport の meta 要素を書かない", "wrong_code": "<head>\n  <meta charset=\"utf-8\">\n  <title>…</title>\n</head>", "why": "スマホでは、PC 向けの広い幅で表示を作って縮小されるため、文字が小さくなります。", "fix": "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"},
            {"title": "固定の幅で、横にはみ出す", "wrong_code": ".photo { width: 800px; }", "why": "画面が 800px より狭いと、はみ出して、横スクロールになります。", "fix": ".photo { width: 800px; max-width: 100%; }"},
            {"title": "メディアクエリのかっこを忘れる", "wrong_code": "@media min-width: 600px { … }", "why": "条件は、かっこで囲む必要があります。かっこがないと、無効になって無視されます。", "fix": "@media (min-width: 600px) { … }"},
            {"title": "min-width と max-width の取り違え", "wrong_code": "@media (min-width: 600px) { …スマホ向け… }", "why": "min-width は「その幅以上」です。狭い画面向けに使うなら、max-width（以下）です。", "fix": "@media (max-width: 600px) { … }"},
        ],
        "checkpoints": [
            "viewport の meta 要素で、画面の幅に合わせる",
            "固定の幅ではなく、max-width や % で柔軟に",
            "メディアクエリは @media (min-width: 〇〇px) のようにかっこ付き",
            "min-width は以上、max-width は以下",
            "モバイルファースト: 基本は狭い画面向け、広い画面は min-width で追加",
            "Flexbox（flex-direction・flex-wrap）と組み合わせる",
        ],
        "next_bridge": "最後のステージです。メディアクエリや max-width を読み解く問題と、ページを1から作る問題があります。ここまで学んだことを、総動員しましょう。",
    },
}

QUESTIONS = [
    mc(
        title="viewport の meta 要素", lang="html",
        prompt="head の中の、次の meta 要素は、何のために書きますか？",
        code='''<meta name="viewport" content="width=device-width, initial-scale=1">''',
        choices=[
            ("スマホなどで、画面の幅に合わせた大きさでページを表示するため", ""),
            ("ページを、スマホでしか表示できないようにするため", "PC を含む、どの端末でも見られます。この指定は、スマホでも、画面の幅に合わせて表示させるためのものです。"),
            ("文字コードを UTF-8 にするため", "文字コードを指定するのは、<meta charset=\"utf-8\"> です。この meta 要素は、表示領域の幅の扱いを指定します。"),
        ],
        correct=0,
        why="viewport の指定がないと、スマホは、PC 向けの広い幅で表示を作って縮小してしまうから。",
        expl="width=device-width は「表示の幅を、端末の画面の幅にする」、initial-scale=1 は「最初の拡大率は等倍」という意味です。レスポンシブデザインには、欠かせない指定です。",
        concepts=["viewport", "meta"], diff=2,
        hint="name=\"viewport\" は、「表示領域」の指定です。",
        ok="正解！画面の幅に合わせて表示します。",
        ng="惜しい！charset とは役割が違います。",
    ),
    pred(
        title="狭い画面でのメディアクエリ", lang="css",
        prompt="次の HTML と CSS を組み合わせたページを、画面の幅 500px で表示したとき、段落の文字は何色になりますか？",
        code=MQ_RED,
        check={"format": "css", "given_html": "<p>テスト</p>", "viewport": 500, "probe": "getComputedStyle(document.querySelector('p')).color"},
        choices=[
            ("赤", "(min-width: 600px) は、画面の幅が 600px 以上のときの条件です。500px は、600px より狭いので、赤にはなりません。", "rgb(255, 0, 0)"),
            ("黒", "", "rgb(0, 0, 0)"),
            ("文字が表示されない", "メディアクエリの条件に合わなくても、基本のルールは適用され、文字は黒で表示されます。", "none"),
        ],
        correct=1,
        why="500px は、min-width: 600px の条件を満たさないので、基本の黒のままだから。",
        expl="min-width は「その幅以上」です。画面が 600px 以上のときだけ、メディアクエリの中のルールが適用され、赤になります。それ以外は、基本のルール（黒）です。",
        concepts=["メディアクエリ", "min-width"], diff=2,
        hint="500 は 600 以上ですか？",
        ok="正解！条件を満たさないので黒のままです。",
        ng="惜しい！min-width の意味を確認しましょう。",
    ),
    pred(
        title="画面幅 800px のとき", lang="css",
        prompt="次の HTML と CSS を組み合わせたページを、画面の幅 800px で表示したとき、メニュー（.menu）は表示されますか？",
        code='''.menu {
  display: block;
}
@media (max-width: 600px) {
  .menu {
    display: none;
  }
}''',
        check={"format": "css", "given_html": '<nav class="menu">メニュー</nav>', "viewport": 800, "probe": "getComputedStyle(document.querySelector('.menu')).display"},
        choices=[
            ("表示される（display: block のまま）", "", "block"),
            ("表示されない（display: none になる）", "(max-width: 600px) は、画面の幅が 600px 以下のときの条件です。800px は 600px より広いので、条件を満たしません。", "none"),
            ("画面の幅に関係なく、いつも表示されない", "メディアクエリは、条件に合うときだけ適用されます。800px では、基本のルールの display: block が使われます。", "x"),
        ],
        correct=0,
        why="800px は、max-width: 600px の条件を満たさないので、基本のルールが適用されるから。",
        expl="max-width は「その幅以下」です。スマホのように狭い画面では、メニューを隠して、ボタンで開く、といった作りによく使います。",
        concepts=["メディアクエリ", "max-width"], diff=2,
        hint="800 は 600 以下ですか？",
        ok="正解！max-width は「以下」です。",
        ng="惜しい！max-width の意味を確認しましょう。",
    ),
    fill(
        title="狭い画面向けの条件", lang="css",
        prompt="画面の幅が 600px 以下のとき、段落の文字を赤にします。【空欄1】に入れる条件の名前を答えてください。",
        code='''@media (__1__: 600px) {
  p {
    color: red;
  }
}''',
        check={"format": "css", "given_html": "<p>テスト</p>", "viewport": 500, "expr": "getComputedStyle(document.querySelector('p')).color === 'rgb(255, 0, 0)'"},
        blanks=[(["max-width"], False)],
        wrong=[("b1", "min-width", "min-width は「その幅以上」です。500px は 600px 未満なので条件に当てはまらず、赤になりません。「以下」は max-width です。")],
        why="「その幅以下」のときの条件は、max-width だから。",
        expl="min-width（以上）と max-width（以下）は、混同しやすい組み合わせです。「スマホ向けに max-width、広い画面向けに min-width」と整理して覚えましょう。",
        concepts=["max-width", "メディアクエリ"], diff=2,
        hint="「以下」を表す条件です。",
        ok="正解！max-width は「以下」です。",
        ng="惜しい！min と max の意味を確認しましょう。",
    ),
    bugfix(
        title="画面からはみ出す箱", lang="css",
        prompt="幅 800px の箱が、スマホ（画面幅 400px）で、画面からはみ出してしまいます。画面の幅に収まるようにするには、どうすればよいですか？",
        code='''.photo {
  width: 800px;
  height: 100px;
  background-color: gray;
}''',
        fixed='''.photo {
  width: 800px;
  max-width: 100%;
  height: 100px;
  background-color: gray;
}''',
        check={"format": "css", "given_html": '<div class="photo"></div>', "viewport": 400, "expr": "document.querySelector('.photo').getBoundingClientRect().width <= document.documentElement.clientWidth"},
        choices=[
            ("width を、もっと大きい値（1200px など）にする", "幅を大きくすると、もっとはみ出します。画面より広くならないように、上限を決めます。"),
            ("max-width: 100% を追加する", ""),
            ("body に overflow: hidden を指定する", "はみ出した部分を隠すだけで、箱は小さくなりません。見える範囲が切れてしまう（内容が見えなくなる）ので、適切な対処ではありません。"),
        ],
        correct=1, fmt="text",
        why="max-width: 100% は、親の幅を超えないように、上限を決める指定だから。",
        expl="width: 800px だけだと、画面の幅が 800px より狭くても、800px のままです。max-width: 100% を足すと、親の幅（画面の幅）を超えず、狭い画面では、親の幅に縮みます。画像にも、同じ指定を使います。",
        concepts=["max-width", "%", "レスポンシブ"], diff=3,
        hint="親の幅を超えないようにする、上限の指定です。",
        ok="正解！max-width: 100% で上限を決めます。",
        ng="惜しい！幅の「上限」を決める指定を使います。",
    ),
    bugfix(
        title="かっこのないメディアクエリ", lang="css",
        prompt="画面の幅が 600px 以下のときに、段落を赤くするつもりが、画面幅 500px でも赤くなりません。1行目を正しく書き直して入力してください（1行目の内容をすべて入力）。",
        code='''@media max-width: 600px {
  p {
    color: red;
  }
}''',
        fixed='''@media (max-width: 600px) {
  p {
    color: red;
  }
}''',
        check={"format": "css", "given_html": "<p>テスト</p>", "viewport": 500, "expr": "getComputedStyle(document.querySelector('p')).color === 'rgb(255, 0, 0)'"},
        target_line=1, accepted=["@media (max-width: 600px) {", "@media (max-width:600px) {", "@media (max-width: 600px){", "@media (max-width:600px){"],
        wrong=[("@media max-width: 600px {", "元のコードのままです。メディアクエリの条件は、かっこ（( )）で囲む必要があります。かっこがないと、無効になって無視されます。")],
        why="メディアクエリの条件は、( ) で囲んで書く必要があるから。",
        expl="@media の条件には、(max-width: 600px) のように、かっこが必要です。かっこがないと、メディアクエリ全体が無効になり、中のルールは、どの画面幅でも適用されません。",
        concepts=["メディアクエリ", "構文"], diff=2,
        hint="条件の部分を、何かの記号で囲みます。",
        ok="正解！条件はかっこで囲みます。",
        ng="惜しい！@media の条件の書き方を確認しましょう。",
    ),
    pred(
        title="折り返したときの行数", lang="css",
        prompt="次の HTML と CSS を組み合わせたページを、画面の幅 500px で表示したとき、アイテムは何行に並びますか？数字だけを入力してください。（body の標準の余白は 8px なので、コンテナの幅は 484px です）",
        code='''.container {
  display: flex;
  flex-wrap: wrap;
}
.item {
  width: 200px;
  height: 50px;
}''',
        check={"format": "css", "given_html": '<div class="container">\n  <div class="item">1</div>\n  <div class="item">2</div>\n  <div class="item">3</div>\n</div>', "viewport": 500, "probe": "new Set(Array.from(document.querySelectorAll('.item')).map(function (e) { return Math.round(e.getBoundingClientRect().top); })).size", "expected": 2},
        out="2",
        wrong=[("1", "200px × 3 = 600px は、コンテナの幅 484px に収まりません。flex-wrap: wrap があるので、収まらない分は折り返します。"), ("3", "200px × 2 = 400px は 484px に収まるので、2つは同じ行に並びます。")],
        why="1行に収まるのは2つ（400px）までで、3つ目は次の行に折り返すから。",
        expl="flex-wrap: wrap を指定すると、アイテムが親の幅に収まらないとき、次の行に折り返します。指定がないと、標準では、アイテムが縮んで1行に収まろうとします。画面の幅によって、行数が変わるので、レスポンシブな並べ方に便利です。",
        concepts=["flex-wrap", "レスポンシブ"], diff=3,
        hint="484px の中に、200px のアイテムが、何個収まりますか？",
        ok="正解！収まらないアイテムは折り返します。",
        ng="惜しい！1行に収まる個数を計算しましょう。",
    ),
    mc(
        title="モバイルファースト", lang="css",
        prompt="「モバイルファースト」の考え方として、正しいものはどれですか？",
        choices=[
            ("まず PC 向けのスタイルを書き、スマホ向けは、max-width のメディアクエリですべて作り直す", "それは、デスクトップファーストの考え方です。モバイルファーストは、スマホ向けを基本にします。"),
            ("まずスマホ向けのスタイルを基本として書き、広い画面向けを、min-width のメディアクエリで追加する", ""),
            ("スマホ向けのページと PC 向けのページを、別々の HTML ファイルとして、2つ作る", "レスポンシブデザインは、1つの HTML を、CSS で、画面の幅に合わせて切り替えます。ファイルを分ける必要はありません。"),
        ],
        correct=1,
        why="スマホ向けを基本にして、広い画面で必要な変更だけを、min-width で足す設計だから。",
        expl="スマホ向けは、縦並びの、シンプルなレイアウトが基本なので、基本のスタイルが少なくなります。広い画面で横並びにしたいところだけを、@media (min-width: …) で追加します。",
        concepts=["モバイルファースト", "min-width"], diff=2,
        hint="Mobile First は、「スマホを最初に」という意味です。",
        ok="正解！スマホ向けを基本にします。",
        ng="惜しい！何を最初に書くか、考えましょう。",
    ),
    pred(
        title="max-width で伸び縮みする箱", lang="css",
        prompt="次の HTML と CSS を組み合わせたページを、画面の幅 400px で表示したとき、.wrap の幅は何 px になりますか？（body の余白は 0 にしています）",
        code='''body { margin: 0; }
.wrap {
  max-width: 600px;
  margin: 0 auto;
}''',
        check={"format": "css", "given_html": '<div class="wrap">中身</div>', "viewport": 400, "probe": "Math.round(document.querySelector('.wrap').getBoundingClientRect().width)"},
        choices=[
            ("600px", "max-width は、幅の上限です。画面が 600px より狭いときは、600px にはならず、画面の幅に合わせて縮みます。", 600),
            ("400px", "", 400),
            ("800px", "max-width は上限で、画面より広くなることはありません。", 800),
        ],
        correct=1,
        why="ブロック要素は、親の幅いっぱいに広がり、max-width（600px）より狭ければ、その幅になるから。",
        expl="画面が広いときは 600px で止まり、中央に寄ります。狭いときは、画面の幅いっぱいに縮みます。「ちょうどよく伸び縮みする」ため、レスポンシブな本文の幅によく使います。",
        concepts=["max-width", "柔軟な幅"], diff=2,
        hint="画面の幅が 400px のとき、600px まで広がれるでしょうか？",
        ok="正解！max-width は上限です。",
        ng="惜しい！max-width が何の上限か確認しましょう。",
    ),
    write_page(
        title="レスポンシブなページを作る", lang="html", fmt="html_document",
        prompt="次の仕様のページを、HTML と CSS（style 要素）で書いてください。\n【HTML】文書型宣言・lang=\"ja\"・UTF-8 の meta・viewport の meta（content に width=device-width を含める）・title（空でない）。body の中に、header（見出し1を含む）、main（その中に .cards。.cards の中に、見出し2と段落を持つ .card を3つ）、footer。\n【CSS】画面の幅が 600px 以上のときは、3つの .card を横一列（幅は等分）に並べる。599px 以下のときは、縦に並べる（左端はそろえる）。どの幅でも、横スクロールは出さない。",
        starter="<!doctype html>\n<html lang=\"ja\">\n<head>\n  <!-- ここに書きましょう -->\n</head>\n<body>\n</body>\n</html>\n",
        ref='''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>レスポンシブなページ</title>
  <style>
    body { margin: 0; font-family: sans-serif; }
    header, footer { padding: 16px; background-color: #333; color: white; }
    main { padding: 16px; }
    .cards { display: flex; flex-direction: column; gap: 16px; }
    .card { padding: 16px; border: 1px solid #ccc; }
    @media (min-width: 600px) {
      .cards { flex-direction: row; }
      .card { flex: 1; }
    }
  </style>
</head>
<body>
  <header>
    <h1>ぼくのサイト</h1>
  </header>
  <main>
    <div class="cards">
      <div class="card"><h2>カードA</h2><p>説明A</p></div>
      <div class="card"><h2>カードB</h2><p>説明B</p></div>
      <div class="card"><h2>カードC</h2><p>説明C</p></div>
    </div>
  </main>
  <footer>
    <p>© 2026</p>
  </footer>
</body>
</html>''',
        alts=['''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ページ</title>
<style>
body { margin: 0; }
.cards { display: flex; flex-wrap: wrap; }
.card { box-sizing: border-box; width: 100%; padding: 8px; }
@media (min-width: 600px) { .card { width: 33.3333%; } }
</style>
</head>
<body>
<header><h1>タイトル</h1></header>
<main><div class="cards">
<div class="card"><h2>A</h2><p>a</p></div>
<div class="card"><h2>B</h2><p>b</p></div>
<div class="card"><h2>C</h2><p>c</p></div>
</div></main>
<footer><p>footer</p></footer>
</body>
</html>'''],
        bads=[
            ('''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>ページ</title>
  <style>
    body { margin: 0; }
    .cards { display: flex; flex-direction: column; }
    @media (min-width: 600px) { .cards { flex-direction: row; } .card { flex: 1; } }
  </style>
</head>
<body>
  <header><h1>タイトル</h1></header>
  <main><div class="cards">
    <div class="card"><h2>A</h2><p>a</p></div>
    <div class="card"><h2>B</h2><p>b</p></div>
    <div class="card"><h2>C</h2><p>c</p></div>
  </div></main>
  <footer><p>footer</p></footer>
</body>
</html>''', "viewport の meta 要素がありません。スマホで、画面の幅に合わせて表示するために必要です。"),
            ('''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ページ</title>
  <style>
    body { margin: 0; }
    .cards { display: flex; }
    .card { width: 200px; }
  </style>
</head>
<body>
  <header><h1>タイトル</h1></header>
  <main><div class="cards">
    <div class="card"><h2>A</h2><p>a</p></div>
    <div class="card"><h2>B</h2><p>b</p></div>
    <div class="card"><h2>C</h2><p>c</p></div>
  </div></main>
  <footer><p>footer</p></footer>
</body>
</html>''', "画面の幅によらず、いつも横並びです。599px 以下では、縦に並べる必要があります（メディアクエリが必要です）。"),
        ],
        tests=[
            t_page("標準モードで、lang が ja、UTF-8・viewport・title がある", "document.compatMode === 'CSS1Compat' && document.documentElement.lang === 'ja' && !!document.querySelector('meta[charset]') && !!document.querySelector('meta[name=viewport]') && document.querySelector('meta[name=viewport]').content.indexOf('width=device-width') >= 0 && document.title.trim().length > 0"),
            t_page("header の中に見出し1、main の中に .cards と 3つの .card（それぞれ見出し2と段落）、footer がある", "(function () { var cs = document.querySelectorAll('main .cards > .card'); return !!document.querySelector('header h1') && cs.length === 3 && Array.from(cs).every(function (c) { return !!c.querySelector('h2') && !!c.querySelector('p'); }) && !!document.querySelector('footer'); })()"),
            t_page("画面幅 800px のとき、3つのカードが横一列に並ぶ", HORIZ, viewport=800),
            t_page("画面幅 400px のとき、3つのカードが縦に並び、左端がそろう", STACK, viewport=400),
            t_page("画面幅 600px ちょうどのとき、横一列に並ぶ（600px 以上）", HORIZ, viewport=600, visible=False),
            t_page("画面幅 599px のとき、縦に並ぶ（599px 以下）", STACK, viewport=599, visible=False),
            t_page("画面幅 400px のとき、横スクロールが出ない", "document.documentElement.scrollWidth <= document.documentElement.clientWidth", viewport=400, visible=False),
            t_page("画面幅 800px のとき、横スクロールが出ない", "document.documentElement.scrollWidth <= document.documentElement.clientWidth", viewport=800, visible=False),
            t_page("画面幅 800px のとき、3つのカードの幅が、ほぼ等しい", "(function () { var w = Array.from(document.querySelectorAll('.card')).map(function (e) { return e.getBoundingClientRect().width; }); return Math.abs(w[0] - w[1]) < 2 && Math.abs(w[1] - w[2]) < 2; })()", viewport=800, visible=False),
        ],
        why="HTML の構造と viewport を書き、スマホ向けの縦並びを基本にして、min-width: 600px のメディアクエリで横並びに切り替えるから。",
        expl="モバイルファーストで、基本は flex-direction: column（縦並び）、@media (min-width: 600px) で row（横並び）にします。境界の 600px と 599px で、切り替わるか確認することも大切です。HTML と CSS の知識を総動員して、1つのページが作れました。",
        concepts=["viewport", "メディアクエリ", "Flexbox", "ページ制作", "セマンティクス"], diff=5,
        hint="基本は column、@media (min-width: 600px) で row。viewport の meta も忘れずに。",
        ok="正解！HTML/CSS の学習はここまでです。おめでとうございます！",
        ng="惜しい！境界（600px と 599px）と、横スクロールを確認しましょう。",
    ),
]
