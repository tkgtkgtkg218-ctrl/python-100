from lib_web import mc, pred, fill, bugfix, write_page, t_page

QS_HTML = '<p class="warn">A</p>\n<p>B</p>\n<p class="warn">C</p>'
RED = "rgb(255, 0, 0)"

STAGE = {
    "number": 6,
    "title": "CSSの基本",
    "subtitle": "ルールの書き方・セレクタ・文字色と背景色・優先順位",
    "goals": [
        "CSS が、見た目を指定するスタイルシート言語であることを説明できる",
        "セレクタ・プロパティ・値・宣言ブロックという用語を使って、CSS のルールを読める",
        "style 要素・外部ファイル（link）・style 属性の3つの適用方法を説明できる",
        "要素・クラス・id のセレクタで、スタイルを適用する対象を選べる",
        "color と background-color で、文字色と背景色を指定できる",
        "スタイルの優先順位（詳細度・後勝ち）と、継承の基本を理解する",
    ],
    "prerequisites": ["HTML の基本（ステージ1〜5）。特に、要素・属性（class・id）"],
    "topics": [
        "CSS とは（スタイルシート言語）",
        "ルールの書き方（セレクタ { プロパティ: 値; }）",
        "適用方法（style 要素・link・style 属性）",
        "要素・クラス・id セレクタ",
        "color と background-color（色の名前）",
        "優先順位と継承",
        "コメント /* */",
    ],
    "pitfalls": [
        "宣言の終わりの ; を忘れると、次の宣言までまとめて無効になる",
        "プロパティ名の綴り間違い（color を colour と書くなど）は、エラーにならず無視される",
        "class は .、id は # をセレクタの先頭に付ける",
        "同じ要素に複数のルールが当たるときは、詳細度（id > class > 要素）と、後に書いたものが優先される",
        "文字色などは、子要素にも引き継がれる（継承）。背景色などは、引き継がれない",
    ],
    "next_links": ["文字の大きさ・太さ・色の指定方法を、さらに詳しく学びます（ステージ7）"],
    "lesson": {
        "intro": "HTML で文章の構造を書いたら、次は見た目を整えます。見た目を指定するのが CSS（Cascading Style Sheets）です。CSS は、HTML と同じく、プログラミング言語ではなく、「スタイルシート言語」です。「この要素は、こういう見た目にしてね」という指定のルールを書きます。",
        "sections": [
            {
                "id": "S06-L1",
                "title": "CSS のルールと適用方法",
                "read_minutes": 3,
                "body": [
                    "CSS は、ルールセット（ルール）の集まりです。1つのルールは、セレクタ { 宣言; 宣言; } の形です。セレクタは「どの要素に」、宣言は「どう変えるか」を表します。宣言は、プロパティ: 値; の形で、例えば color: red; は、プロパティ color（文字色）の値を red にする、という意味です。",
                    "CSS を HTML に適用する方法は3つあります。(1) head の中の style 要素に書く。(2) 別ファイルに書いて、head の中に <link rel=\"stylesheet\" href=\"style.css\"> で読み込む。(3) 要素の style 属性に直接書く。ページ全体で共通のスタイルを管理しやすい (2) が、実際のサイト作りの基本です。(3) は、特定の1か所だけに使います。",
                    "/* ... */ で囲んだ部分はコメントで、ブラウザに無視されます。HTML のコメント（<!-- -->）とは書き方が違います。",
                    "CSS は、書き間違いがあっても、エラーメッセージは出ません。間違った宣言は無視されるだけなので、見た目が変わらないときは、綴りや ; を確認します。",
                ],
                "glossary": [
                    {"term": "セレクタ", "definition": "スタイルを適用する対象を選ぶ部分（h1、.warn、#main など）。"},
                    {"term": "宣言", "definition": "プロパティ: 値; の1組。"},
                    {"term": "プロパティ", "definition": "変えたい見た目の項目（color、background-color など）。"},
                    {"term": "値", "definition": "プロパティに指定する内容（red など）。"},
                ],
                "examples": [
                    {
                        "id": "S06-E1", "title": "style 要素に書く", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>CSS</title>
  <style>
    /* 見出しの文字を赤にする */
    h1 {
      color: red;
    }
  </style>
</head>
<body>
  <h1>ようこそ</h1>
</body>
</html>''',
                        "line_notes": ["7〜9行目が1つのルールです。h1 がセレクタ、{ } の中が宣言ブロックです。", "color が プロパティ、red が値です。宣言の終わりには ; を付けます。", "6行目の /* */ はコメントです。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "expr": "getComputedStyle(document.querySelector('h1')).color === 'rgb(255, 0, 0)'"},
                    },
                    {
                        "id": "S06-E2", "title": "外部ファイルを読み込む", "language": "html",
                        "code": '''<head>
  <meta charset="utf-8">
  <title>CSS</title>
  <link rel="stylesheet" href="style.css">
</head>''',
                        "line_notes": ["style.css というファイルに、CSS を書いておき、link 要素で読み込みます。", "rel=\"stylesheet\" は、「このファイルはスタイルシートです」という意味です。"],
                        "preview": None,
                        "verify": {"format": "html_document", "expr": "document.querySelector('link').rel === 'stylesheet' && document.querySelector('link').getAttribute('href') === 'style.css'", "allow_errors": True},
                    },
                ],
            },
            {
                "id": "S06-L2",
                "title": "セレクタ・色・優先順位",
                "read_minutes": 3,
                "body": [
                    "セレクタには、主に3つの種類があります。要素セレクタ（p など、その名前の要素すべて）、クラスセレクタ（.warn など、class=\"warn\" の要素すべて）、id セレクタ（#main など、id=\"main\" の要素1つ）です。class はいくつの要素にも付けられ、id はページの中で1つだけに付けます。",
                    "文字の色は color、背景の色は background-color で指定します。色は、red・blue・yellow・green などの名前で指定できます（ほかの指定方法は、ステージ7で学びます）。",
                    "同じ要素に、複数のルールが当たるときは、詳細度の高いものが優先されます。詳細度は、id セレクタ > クラスセレクタ > 要素セレクタの順です。詳細度が同じときは、あとに書いたものが優先されます（後勝ち）。",
                    "color などの一部のプロパティは、子要素に引き継がれます（継承）。親に color を指定すると、子の p も同じ色になります。background-color や border など、継承されないプロパティもあります。",
                ],
                "glossary": [
                    {"term": "クラスセレクタ", "definition": ".名前 の形で、class が一致する要素すべてを選ぶセレクタ。"},
                    {"term": "id セレクタ", "definition": "#名前 の形で、id が一致する要素を選ぶセレクタ。"},
                    {"term": "詳細度", "definition": "複数のルールが競合したとき、どれが優先されるかを決める強さ。"},
                    {"term": "継承", "definition": "親要素の指定が、子要素に引き継がれること。"},
                ],
                "examples": [
                    {
                        "id": "S06-E3", "title": "クラスとid", "language": "css",
                        "context_html": '<p class="warn">A</p>\n<p>B</p>\n<p id="main" class="warn">C</p>',
                        "code": '''.warn {
  color: red;
}
#main {
  background-color: yellow;
}''',
                        "line_notes": [".warn は、class=\"warn\" の p（A と C）を選びます。", "#main は、id=\"main\" の p（C）だけを選びます。"],
                        "preview": {"format": "css", "given_html": '<p class="warn">A</p>\n<p>B</p>\n<p id="main" class="warn">C</p>'},
                        "verify": {"format": "css", "given_html": '<p class="warn">A</p>\n<p>B</p>\n<p id="main" class="warn">C</p>', "expr": "(function () { var p = document.querySelectorAll('p'); var c = function (e) { return getComputedStyle(e).color; }; return c(p[0]) === 'rgb(255, 0, 0)' && c(p[1]) !== 'rgb(255, 0, 0)' && c(p[2]) === 'rgb(255, 0, 0)' && getComputedStyle(p[2]).backgroundColor === 'rgb(255, 255, 0)' && getComputedStyle(p[0]).backgroundColor !== 'rgb(255, 255, 0)'; })()"},
                    },
                    {
                        "id": "S06-E4", "title": "優先順位", "language": "css",
                        "context_html": '<div class="box">\n  <p id="x" class="c">文章</p>\n</div>',
                        "code": '''.box { color: green; }
p { color: blue; }
.c { color: orange; }
#x { color: red; }''',
                        "line_notes": ["p には、4つのルールが当たりそうですが、id セレクタ（#x）が最も強いので、赤になります。", ".box の green は、p 自身を選ぶルールがあるので、継承の指定より、そのルールが優先されます。"],
                        "preview": {"format": "css", "given_html": '<div class="box">\n  <p id="x" class="c">文章</p>\n</div>'},
                        "verify": {"format": "css", "given_html": '<div class="box">\n  <p id="x" class="c">文章</p>\n</div>', "expr": "getComputedStyle(document.getElementById('x')).color === 'rgb(255, 0, 0)'"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "; の書き忘れ", "wrong_code": "p { color: red background-color: yellow; }", "why": "color の値が「red background-color: yellow」という、不正な値になり、color と背景色の両方が無視されます。", "fix": "p { color: red; background-color: yellow; }"},
            {"title": "プロパティ名の綴りミス", "wrong_code": "p { colour: red; }", "why": "colour というプロパティはありません。エラーにならず、無視されるだけなので気づきにくいミスです。", "fix": "p { color: red; }"},
            {"title": "class に . を付け忘れる", "wrong_code": "warn { color: red; }", "why": "warn という名前の要素（<warn>）を選ぶことになり、class=\"warn\" の要素には当たりません。", "fix": ".warn { color: red; }"},
            {"title": "HTML のコメントを CSS に書く", "wrong_code": "<!-- 見出し -->\nh1 { color: red; }", "why": "CSS のコメントは /* */ です。<!-- --> は、CSS では正しいコメントではありません。", "fix": "/* 見出し */"},
        ],
        "checkpoints": [
            "ルールは セレクタ { プロパティ: 値; }",
            "適用方法は style 要素・link・style 属性",
            "要素・.クラス・#id のセレクタ",
            "文字色は color、背景色は background-color",
            "詳細度は id > class > 要素、同じなら後勝ち",
            "color は子に継承される。書き間違いはエラーにならず無視される",
        ],
        "next_bridge": "CSS のルールの読み書きができるようになりました。問題で、セレクタと優先順位を確かめましょう。",
    },
}

QUESTIONS = [
    mc(
        title="CSS とは", lang="css",
        prompt="CSS の説明として、正しいものはどれですか？",
        choices=[
            ("ページの色・余白・配置など、見た目を指定するスタイルシート言語である", ""),
            ("文章の構造をタグで表すマークアップ言語である", "それは HTML の説明です。CSS は、構造に対して見た目を指定します。"),
            ("計算や条件分岐でページを動かすプログラミング言語である", "それは JavaScript の説明です。CSS には、計算や条件分岐でページを動かす仕組みはありません。"),
        ],
        correct=0,
        why="CSS は、HTML で書いた構造に、見た目を与えるスタイルシート言語だから。",
        expl="HTML（構造）・CSS（見た目）・JavaScript（動き）は、それぞれ別の役割です。同じ HTML でも、CSS を変えれば、まったく違う見た目にできます。",
        concepts=["CSSの役割", "スタイルシート言語"], diff=1,
        hint="CSS は Cascading Style Sheets の略です。Style（様式・見た目）に注目しましょう。",
        ok="正解！CSS は見た目を指定します。",
        ng="惜しい！HTML・CSS・JavaScript の役割を整理しましょう。",
    ),
    mc(
        title="CSS の用語", lang="css",
        prompt="次の CSS のルールで、color の部分は、何と呼びますか？",
        code='''h1 {
  color: red;
}''',
        choices=[
            ("セレクタ", "セレクタは、スタイルを適用する対象を選ぶ部分で、ここでは h1 です。"),
            ("プロパティ", ""),
            ("値", "値は、プロパティに指定する内容で、ここでは red です。"),
        ],
        correct=1,
        why="color は、変えたい見た目の項目で、プロパティと呼ぶから。",
        expl="h1 がセレクタ、{ } の中が宣言ブロック、color がプロパティ、red が値です。「color: red;」の1組を、宣言と呼びます。",
        concepts=["セレクタ", "プロパティ", "値"], diff=1,
        hint="「color: red;」の左側と右側に、それぞれ名前があります。",
        ok="正解！color はプロパティです。",
        ng="惜しい！セレクタ・プロパティ・値を区別しましょう。",
    ),
    fill(
        title="文字色を指定するプロパティ", lang="css",
        prompt="見出し（h1）の文字を赤にします。【空欄1】に入れるプロパティ名を答えてください。",
        code='''h1 {
  __1__: red;
}''',
        check={"format": "css", "given_html": "<h1>見出し</h1>", "expr": "getComputedStyle(document.querySelector('h1')).color === 'rgb(255, 0, 0)'"},
        blanks=[(["color"], False)],
        wrong=[("b1", "background-color", "background-color は背景の色を指定するプロパティです。文字の色は color です。")],
        why="文字の色を指定するプロパティは color だから。",
        expl="color は文字色、background-color は背景色です。「background-color」は、ハイフンでつないだ名前で、color とは別のプロパティです。",
        concepts=["color", "プロパティ"], diff=1,
        hint="「色」を意味する英単語です。",
        ok="正解！文字色は color です。",
        ng="惜しい！背景色とは別のプロパティです。",
    ),
    pred(
        title="クラスセレクタの対象", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、文字が赤くなる段落はどれですか？（R が赤、- が赤でないことを表します）",
        code='''.warn {
  color: red;
}''',
        check={"format": "css", "given_html": QS_HTML, "probe": "Array.from(document.querySelectorAll('p')).map(function (p) { return getComputedStyle(p).color === 'rgb(255, 0, 0)' ? 'R' : '-'; }).join('')"},
        choices=[
            ("A だけ（R--）", ".warn は、class=\"warn\" が付いたすべての要素に当たります。A の他に、C にも当たります。", "R--"),
            ("A と C（R-R）", "", "R-R"),
            ("A・B・C のすべて（RRR）", "B には class=\"warn\" が付いていません。.warn は、その class を持つ要素だけに当たります。", "RRR"),
        ],
        correct=1,
        why=".warn は class=\"warn\" を持つすべての要素に当たり、A と C がそれに該当するから。",
        expl="クラスセレクタは、同じ class が付いた要素を、まとめて選びます。1か所だけを選びたいときは、id セレクタ（#名前）を使います。",
        concepts=["クラスセレクタ"], diff=2,
        hint="class=\"warn\" が付いているのはどれでしょう？ HTML は、A・B・C の3つの p です。",
        ok="正解！クラスセレクタは、同じ class の要素すべてを選びます。",
        ng="惜しい！HTML の class 属性を確認しましょう。",
        # 表示用: 下の HTML は問題文に context_html として表示される
    ),
    pred(
        title="スタイルの優先順位", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、段落の文字は、何色で表示されますか？",
        code='''p { color: blue; }
.c { color: green; }
#x { color: red; }''',
        check={"format": "css", "given_html": '<p id="x" class="c">文章</p>', "probe": "getComputedStyle(document.getElementById('x')).color"},
        choices=[
            ("blue（青。一番上に書いたルール）", "書く順番より、詳細度の強さが優先されます。要素セレクタ（p）は、最も弱いセレクタです。", "rgb(0, 0, 255)"),
            ("red（赤。id セレクタのルール）", "", "rgb(255, 0, 0)"),
            ("green（緑。クラスセレクタのルール）", "クラスセレクタは、要素セレクタより強いですが、id セレクタには負けます。", "rgb(0, 128, 0)"),
        ],
        correct=1,
        why="id セレクタ > クラスセレクタ > 要素セレクタの順に、詳細度が高いから。",
        expl="詳細度が違うときは、書く順番に関係なく、詳細度の高いルールが優先されます。同じ詳細度のときだけ、あとに書いたものが優先されます。",
        concepts=["詳細度", "優先順位"], diff=3,
        hint="この3つのセレクタの強さの順番を思い出しましょう。",
        ok="正解！id セレクタが最も強いです。",
        ng="惜しい！セレクタの詳細度を比べましょう。",
    ),
    bugfix(
        title="宣言の区切り", lang="css",
        prompt="文字を赤、背景を黄色にしたいのに、どちらも効きません。正しい直し方はどれですか？",
        code='''p { color: red background-color: yellow; }''',
        fixed='''p { color: red; background-color: yellow; }''',
        check={"format": "css", "given_html": "<p>テスト</p>", "expr": "getComputedStyle(document.querySelector('p')).color === 'rgb(255, 0, 0)' && getComputedStyle(document.querySelector('p')).backgroundColor === 'rgb(255, 255, 0)'"},
        target_line=1,
        choices=[
            ("p { color: red, background-color: yellow; }", "宣言どうしの区切りは、カンマではなく、セミコロン（;）です。カンマでは、値が不正になり、どちらも無視されます。"),
            ("p { color: red; background-color: yellow; }", ""),
            ("p { color: red: background-color: yellow; }", "コロン（:）は、プロパティと値の間に使う記号です。宣言どうしを区切るのは、セミコロン（;）です。"),
        ],
        correct=1, fmt="code",
        why="宣言どうしは、セミコロン（;）で区切る必要があるから。",
        expl="; を忘れると、color の値が「red background-color: yellow」という不正な値になり、color の宣言全体が無視されます。background-color の宣言もなくなるため、どちらも効きません。",
        concepts=["宣言", "セミコロン"], diff=2,
        hint="宣言の終わりに付ける記号は何でしたか？",
        ok="正解！宣言は ; で区切ります。",
        ng="惜しい！宣言どうしの区切りの記号を確認しましょう。",
    ),
    bugfix(
        title="プロパティ名の綴りミス", lang="css",
        prompt="文字を赤にしたいのに、色が変わりません。2行目を正しく書き直して入力してください（2行目の内容だけを入力）。",
        code='''p {
  colour: red;
}''',
        fixed='''p {
  color: red;
}''',
        check={"format": "css", "given_html": "<p>テスト</p>", "expr": "getComputedStyle(document.querySelector('p')).color === 'rgb(255, 0, 0)'"},
        target_line=2, accepted=["color: red;", "color:red;"],
        wrong=[("colour: red;", "元のコードのままです。colour というプロパティはありません。CSS は、間違った宣言を、エラーを出さずに無視します。")],
        why="プロパティ名は color と綴る必要があり、違う綴りはエラーなく無視されるから。",
        expl="CSS には、エラーメッセージがありません。見た目が変わらないときは、プロパティ名の綴りや、値の書き方を確認します。開発者ツールでは、無視された宣言に打ち消し線が付いて分かります。",
        concepts=["color", "綴りミス"], diff=2,
        hint="CSS のプロパティ名は、英語（アメリカ式）の綴りです。",
        ok="正解！プロパティ名の綴りを直しました。",
        ng="惜しい！プロパティ名を確認しましょう。",
    ),
    fill(
        title="外部の CSS ファイルを読み込む", lang="html",
        prompt="style.css を読み込みます。【空欄1】に入れる、rel 属性の値を答えてください。",
        code='''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>CSS</title>
  <link rel="__1__" href="style.css">
</head>
<body>
  <p>こんにちは</p>
</body>
</html>''',
        check={"format": "html_document", "expr": "document.querySelector('link').rel === 'stylesheet'"},
        blanks=[(["stylesheet"], False)],
        wrong=[("b1", "css", "rel の値は、リンク先と、このページの関係を表す決まった語です。スタイルシートは stylesheet と書きます。")],
        why="外部の CSS ファイルを読み込む link の rel は、stylesheet と書くから。",
        expl="rel（relationship = 関係）には、link 先がこのページとどういう関係かを書きます。CSS ファイルの場合は stylesheet です。href には、ファイルの場所を、相対パスで書きます。",
        concepts=["link", "rel", "外部CSS"], diff=2,
        hint="スタイルシートを意味する英単語を、続けて書きます。",
        ok="正解！rel=\"stylesheet\" と書きます。",
        ng="惜しい！スタイルシートを表す語を入力しましょう。",
    ),
    pred(
        title="文字色の継承", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、div の中の段落の文字は、何色で表示されますか？",
        code='''.box {
  color: green;
}''',
        check={"format": "css", "given_html": '<div class="box">\n  <p>文章</p>\n</div>', "probe": "getComputedStyle(document.querySelector('p')).color"},
        choices=[
            ("黒のまま。p には直接指定していないので、変わらない", "color は、親要素の指定が、子要素に引き継がれる（継承される）プロパティです。", "rgb(0, 0, 0)"),
            ("緑。親の .box の color が、p に引き継がれる", "", "rgb(0, 128, 0)"),
            ("エラーになって、何も表示されない", "CSS は、エラーにならず、継承も自然に行われます。", "error"),
        ],
        correct=1,
        why="color は継承されるプロパティなので、親の指定が子の p に引き継がれるから。",
        expl="文字に関する多くのプロパティ（color・font-size など）は継承されます。一方、背景色や枠線のように、継承されないプロパティもあります。親に指定すれば、子に1つずつ指定しなくて済みます。",
        concepts=["継承", "color"], diff=2,
        hint="color は、子要素にも引き継がれるプロパティです。",
        ok="正解！color は継承されます。",
        ng="惜しい！継承の働きを確認しましょう。",
    ),
    write_page(
        title="色を付けて見た目を整える", lang="css", fmt="css",
        prompt="次の HTML に、CSS だけで、次の見た目を指定してください（色は名前か #rrggbb で指定します）。\n・h1 の文字色を blue（青）\n・class が lead の段落の背景色を yellow（黄色）\n・すべての p の文字色を #333333",
        given_html='<h1>ようこそ</h1>\n<p class="lead">はじめまして。</p>\n<p>ここは練習ページです。</p>',
        starter="/* ここに CSS を書きましょう */\n",
        ref='''h1 {
  color: blue;
}
.lead {
  background-color: yellow;
}
p {
  color: #333333;
}''',
        alts=['''h1 { color: #0000ff; }
p { color: #333; }
p.lead { background-color: #ffff00; }'''],
        bads=[
            ('''h1 {
  color: blue;
}
.lead {
  background-color: yellow;
}''', "すべての p の文字色（#333333）を指定していません。p セレクタで指定します。"),
            ('''h1 {
  background-color: blue;
}
.lead {
  color: yellow;
}
p {
  color: #333333;
}''', "color（文字色）と background-color（背景色）が逆になっています。"),
        ],
        tests=[
            t_page("h1 の文字色が青", "getComputedStyle(document.querySelector('h1')).color === 'rgb(0, 0, 255)'"),
            t_page("class が lead の段落の背景色が黄色", "getComputedStyle(document.querySelector('p.lead')).backgroundColor === 'rgb(255, 255, 0)'"),
            t_page("すべての p の文字色が #333333", "Array.from(document.querySelectorAll('p')).every(function (p) { return getComputedStyle(p).color === 'rgb(51, 51, 51)'; })"),
            t_page("lead でない段落の背景色は変わっていない", "getComputedStyle(document.querySelectorAll('p')[1]).backgroundColor === 'rgba(0, 0, 0, 0)'", visible=False),
            t_page("h1 の背景色は変わっていない", "getComputedStyle(document.querySelector('h1')).backgroundColor === 'rgba(0, 0, 0, 0)'", visible=False),
        ],
        why="要素セレクタ（h1・p）とクラスセレクタ（.lead）で対象を選び、color と background-color で色を指定するから。",
        expl="h1 { color: blue; } で見出しの文字色、.lead { background-color: yellow; } でクラスの背景色、p { color: #333333; } で全段落の文字色を指定します。#333333 は、少し黒に近い灰色です。",
        concepts=["セレクタ", "color", "background-color"], diff=2,
        hint="3つのルールを書きます。lead は、クラスセレクタ（.lead）です。",
        ok="正解！色を指定できました。",
        ng="惜しい！文字色と背景色を取り違えていないか確認しましょう。",
    ),
]
