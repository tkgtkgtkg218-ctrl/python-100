from lib_web import mc, pred, fill, bugfix, write_page, t_page

STAGE = {
    "number": 7,
    "title": "文字と色の装飾",
    "subtitle": "色の指定方法・文字の大きさ・単位・セレクタの組み合わせ",
    "goals": [
        "色を、名前・#rrggbb・rgb() の書き方で指定できる",
        "font-size・font-weight・line-height・text-align・text-decoration を指定できる",
        "px・em・rem・% という単位の違いを説明できる",
        "子孫セレクタ（空白）・子セレクタ（>）・グループ化（,）を使い分けられる",
        "疑似クラス :hover の意味を説明できる",
    ],
    "prerequisites": ["CSS の基本（ステージ6）"],
    "topics": [
        "色の指定（名前・#rrggbb・#rgb・rgb()）",
        "font-size と単位（px / em / rem / %）",
        "font-weight・font-family・line-height",
        "text-align・text-decoration",
        "子孫セレクタ・子セレクタ・グループ化",
        "疑似クラス :hover",
    ],
    "pitfalls": [
        "数値だけで単位を付けない指定（font-size: 20;）は無効になる（0 だけは単位不要）",
        "em は親の文字の大きさが基準、rem は html 要素の文字の大きさが基準",
        "line-height は、単位なしの数値（1.5）にすると、文字の大きさに合わせて決まる",
        "h1 h2 {…}（空白）は、h1 の中の h2 を選ぶ。h1, h2 {…}（カンマ）が、両方を選ぶ",
        "px 固定の文字の大きさは、ブラウザの文字サイズ設定が効きにくい",
    ],
    "next_links": ["要素の内側・外側の余白を決める「ボックスモデル」を学びます（ステージ8）"],
    "lesson": {
        "intro": "文字の大きさ・太さ・色・行の間隔を整えるだけで、ページはぐっと読みやすくなります。この回では、CSS で文字を整えるための基本のプロパティと、「単位」の考え方、そして、スタイルを適用する対象を細かく選ぶセレクタを学びます。",
        "sections": [
            {
                "id": "S07-L1",
                "title": "色・文字・単位",
                "read_minutes": 3,
                "body": [
                    "色の指定方法は、いくつかあります。名前（red）、16進数（#ff0000 や、短い #f00）、rgb(255, 0, 0)（赤・緑・青の強さを 0〜255 で指定）です。これらは、書き方が違うだけで、同じ色（この例ではすべて赤）を表せます。",
                    "文字の大きさは font-size、太さは font-weight（normal / bold / 100〜900 の数値）、書体は font-family（sans-serif など）、行の高さは line-height です。line-height は、単位なしの数値（1.5 など）にすると、文字の大きさの1.5倍になり、文字を大きくしても、読みやすい行間が保たれます。text-align は文字の水平方向の揃え（left / center / right）、text-decoration は下線などの装飾（underline / none）です。",
                    "長さの単位には、px（画面の点の数。固定）、em（親要素の文字の大きさに対する倍率）、rem（html 要素の文字の大きさに対する倍率。標準は 16px）、%（親に対する割合）があります。文字の大きさには、ユーザーがブラウザで文字サイズを変更したときに追従できる、rem や em を使うのが推奨されます。数値のあとの単位は省略できず、20 だけだと無効です（0 だけは単位なしで書けます）。",
                ],
                "glossary": [
                    {"term": "rem", "definition": "html 要素（ルート）の文字の大きさを 1 とする単位。標準では 1rem = 16px。"},
                    {"term": "em", "definition": "その要素の親の文字の大きさを 1 とする単位。"},
                    {"term": "line-height", "definition": "1行の高さ（行間）。"},
                ],
                "examples": [
                    {
                        "id": "S07-E1", "title": "同じ色の書き方", "language": "css",
                        "context_html": '<p class="a">A</p>\n<p class="b">B</p>\n<p class="c">C</p>\n<p class="d">D</p>',
                        "code": '''.a { color: red; }
.b { color: #ff0000; }
.c { color: #f00; }
.d { color: rgb(255, 0, 0); }''',
                        "line_notes": ["4つの書き方は、すべて同じ赤を表します。", "#f00 は、#ff0000 の短縮形です（各桁を2回ずつ繰り返したもの）。"],
                        "preview": {"format": "css", "given_html": '<p class="a">A</p>\n<p class="b">B</p>\n<p class="c">C</p>\n<p class="d">D</p>'},
                        "verify": {"format": "css", "given_html": '<p class="a">A</p>\n<p class="b">B</p>\n<p class="c">C</p>\n<p class="d">D</p>', "expr": "Array.from(document.querySelectorAll('p')).every(function (p) { return getComputedStyle(p).color === 'rgb(255, 0, 0)'; })"},
                    },
                    {
                        "id": "S07-E2", "title": "単位の違い", "language": "css",
                        "context_html": '<div class="outer">\n  <p class="e">A</p>\n  <p class="r">B</p>\n  <p class="p">C</p>\n</div>',
                        "code": '''.outer { font-size: 20px; }
.e { font-size: 2em; }
.r { font-size: 2rem; }
.p { font-size: 150%; }''',
                        "line_notes": ["2em は、親（.outer）の 20px の2倍で 40px。", "2rem は、html 要素（標準 16px）の2倍で 32px。", "150% は、親の 20px の 1.5倍で 30px。"],
                        "preview": {"format": "css", "given_html": '<div class="outer">\n  <p class="e">A</p>\n  <p class="r">B</p>\n  <p class="p">C</p>\n</div>'},
                        "verify": {"format": "css", "given_html": '<div class="outer">\n  <p class="e">A</p>\n  <p class="r">B</p>\n  <p class="p">C</p>\n</div>', "expr": "['e', 'r', 'p'].map(function (c) { return getComputedStyle(document.querySelector('.' + c)).fontSize; }).join(',') === '40px,32px,30px'"},
                    },
                    {
                        "id": "S07-E3", "title": "文字の整え方", "language": "css",
                        "context_html": '<p class="t">こんにちは。文字を整えます。</p>',
                        "code": '''.t {
  font-size: 20px;
  font-weight: bold;
  line-height: 1.5;
  text-align: center;
  text-decoration: underline;
}''',
                        "line_notes": ["line-height: 1.5 は、文字の大きさ（20px）の1.5倍で、30px になります。", "font-weight: bold は、数値の 700 と同じです。"],
                        "preview": {"format": "css", "given_html": '<p class="t">こんにちは。文字を整えます。</p>'},
                        "verify": {"format": "css", "given_html": '<p class="t">こんにちは。文字を整えます。</p>', "expr": "(function () { var s = getComputedStyle(document.querySelector('.t')); return s.fontSize === '20px' && s.fontWeight === '700' && s.lineHeight === '30px' && s.textAlign === 'center' && s.textDecorationLine === 'underline'; })()"},
                    },
                ],
            },
            {
                "id": "S07-L2",
                "title": "セレクタの組み合わせ",
                "read_minutes": 3,
                "body": [
                    "セレクタは、組み合わせて、適用する対象を細かく選べます。div p のように空白で区切ると、子孫セレクタです。div の中にある（何段階下でもよい）p をすべて選びます。div > p のように > でつなぐと、子セレクタです。div の直接の子の p だけを選びます。h1, h2 のようにカンマで区切ると、グループ化で、h1 と h2 の両方に、同じスタイルを適用します。",
                    "疑似クラスは、要素の状態を表します。a:hover は、マウスポインターが乗っているときのリンク、:first-child は、最初の子要素です。マウスを乗せたときに色を変えるなど、動きのある見た目を CSS だけで作れます。",
                    "セレクタが複雑になると、詳細度が高くなり、あとから上書きしにくくなります。基本は、class を付けて、クラスセレクタで指定するのが、管理しやすい方法です。",
                ],
                "glossary": [
                    {"term": "子孫セレクタ", "definition": "空白で区切る。内側にある要素を、深さを問わず選ぶ。"},
                    {"term": "子セレクタ", "definition": "> でつなぐ。直接の子だけを選ぶ。"},
                    {"term": "疑似クラス", "definition": ":hover のように、要素の状態に応じて適用するセレクタ。"},
                ],
                "examples": [
                    {
                        "id": "S07-E4", "title": "子セレクタとグループ化", "language": "css",
                        "context_html": '<div>\n  <p>A</p>\n  <section>\n    <p>B</p>\n  </section>\n</div>\n<h1>見出し1</h1>\n<h2>見出し2</h2>',
                        "code": '''div > p {
  color: red;
}
h1, h2 {
  color: blue;
}''',
                        "line_notes": ["div > p は、div の直接の子の p（A）だけを選びます。section の中の p（B）は選ばれません。", "h1, h2 は、h1 と h2 の両方を選びます。"],
                        "preview": {"format": "css", "given_html": '<div>\n  <p>A</p>\n  <section>\n    <p>B</p>\n  </section>\n</div>\n<h1>見出し1</h1>\n<h2>見出し2</h2>'},
                        "verify": {"format": "css", "given_html": '<div>\n  <p>A</p>\n  <section>\n    <p>B</p>\n  </section>\n</div>\n<h1>見出し1</h1>\n<h2>見出し2</h2>', "expr": "(function () { var c = function (s) { return getComputedStyle(document.querySelector(s)).color; }; return c('div > p') === 'rgb(255, 0, 0)' && c('section p') !== 'rgb(255, 0, 0)' && c('h1') === 'rgb(0, 0, 255)' && c('h2') === 'rgb(0, 0, 255)'; })()"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "単位を付けない", "wrong_code": "font-size: 20;", "why": "0 以外の数値には、単位が必要です。単位がないと、宣言全体が無効になります。", "fix": "font-size: 20px;"},
            {"title": "グループ化にカンマを付けない", "wrong_code": "h1 h2 { color: red; }", "why": "空白は子孫セレクタです。「h1 の中の h2」という意味になり、並んだ h1・h2 には当たりません。", "fix": "h1, h2 { color: red; }"},
            {"title": "text-align: middle", "wrong_code": "text-align: middle;", "why": "middle という値はありません。中央揃えは center です。", "fix": "text-align: center;"},
            {"title": "px 固定ばかりにする", "wrong_code": "html { font-size: 14px; }  /* すべて px */", "why": "ブラウザの文字サイズの設定が効きにくくなります。文字の大きさには rem や em を使うと、利用者の設定に追従できます。", "fix": "font-size: 1rem;"},
        ],
        "checkpoints": [
            "色は、名前・#rrggbb・rgb() で指定できる",
            "文字の大きさ・太さ・行間・揃え・装飾のプロパティ",
            "em は親、rem は html、% は親が基準",
            "line-height は単位なしの数値が扱いやすい",
            "空白は子孫、> は子、カンマはグループ化",
            ":hover は、マウスが乗っているときの状態",
        ],
        "next_bridge": "文字と色を整えられるようになりました。問題で、単位とセレクタの理解を確かめましょう。",
    },
}

QUESTIONS = [
    pred(
        title="em・rem・% の計算", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、3つの p（A・B・C）の文字の大きさは、それぞれ何 px になりますか？（html 要素の文字の大きさは、標準の 16px とします）",
        code='''.outer { font-size: 20px; }
.e { font-size: 2em; }
.r { font-size: 2rem; }
.p { font-size: 150%; }''',
        check={"format": "css", "given_html": '<div class="outer">\n  <p class="e">A</p>\n  <p class="r">B</p>\n  <p class="p">C</p>\n</div>', "probe": "['e', 'r', 'p'].map(function (c) { return getComputedStyle(document.querySelector('.' + c)).fontSize; }).join(',')"},
        choices=[
            ("A: 40px、B: 40px、C: 30px", "rem は、親（.outer）ではなく、html 要素の文字の大きさ（標準の 16px）が基準です。2rem は 32px です。", "40px,40px,30px"),
            ("A: 40px、B: 32px、C: 30px", "", "40px,32px,30px"),
            ("A: 20px、B: 32px、C: 20px", "em と % は、親（.outer）の 20px に対する倍率なので、2em は 40px、150% は 30px になります。", "20px,32px,20px"),
        ],
        correct=1,
        why="em と % は親の 20px が基準、rem は html の 16px が基準だから。",
        expl="2em = 20px × 2 = 40px、2rem = 16px × 2 = 32px、150% = 20px × 1.5 = 30px です。rem は、親の大きさに関係なく、いつも同じ大きさになるので、扱いやすい単位です。",
        concepts=["em", "rem", "%", "font-size"], diff=3,
        hint="em と % は親、rem は html 要素が基準です。",
        ok="正解！基準になる要素が、単位ごとに違います。",
        ng="惜しい！em・rem・% の基準を確認しましょう。",
    ),
    fill(
        title="太字にする", lang="css",
        prompt="段落の文字を太字にします。【空欄1】に入れる値を答えてください。",
        code='''p {
  font-weight: __1__;
}''',
        check={"format": "css", "given_html": "<p>こんにちは</p>", "expr": "getComputedStyle(document.querySelector('p')).fontWeight === '700'"},
        blanks=[(["bold", "700"], False)],
        wrong=[("b1", "heavy", "heavy という値はありません。無効な値は無視されるので、太字にならず、標準の太さのままです。")],
        why="太字は、font-weight の値を bold（または 700）にするから。",
        expl="font-weight は、normal（400）・bold（700）のほか、100〜900 の数値でも指定できます。見出しは、標準で太字になっているので、普通の太さにしたいときは、normal を指定します。",
        concepts=["font-weight"], diff=1,
        hint="太字を意味する英単語です。",
        ok="正解！font-weight: bold で太字です。",
        ng="惜しい！太字を表す値を入力しましょう。",
    ),
    pred(
        title="line-height の計算", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、段落の1行の高さ（line-height の実際の値）は、何 px になりますか？「30px」のように、単位を付けて入力してください。",
        code='''p {
  font-size: 20px;
  line-height: 1.5;
}''',
        check={"format": "css", "given_html": "<p>こんにちは</p>", "probe": "getComputedStyle(document.querySelector('p')).lineHeight", "expected": "30px"},
        out="30px",
        wrong=[("1.5px", "単位のない 1.5 は、px ではなく、文字の大きさに対する倍率です。20px の 1.5倍で、30px になります。"), ("20px", "文字の大きさ（font-size）と、行の高さ（line-height）は別です。line-height が 1.5 なので、20px の 1.5倍になります。")],
        why="単位のない line-height は、文字の大きさ（20px）に対する倍率なので、20 × 1.5 = 30px になるから。",
        expl="単位のない数値は、倍率として子要素にも引き継がれるので、子要素の文字の大きさが違っても、それに合った行間になります。本文の行間は、1.5〜1.8 程度が読みやすいとされます。",
        concepts=["line-height"], diff=2,
        hint="単位のない line-height は、何に対する倍率でしょうか？",
        ok="正解！line-height の単位なしは、倍率です。",
        ng="惜しい！20px の 1.5倍を計算しましょう。",
    ),
    mc(
        title="文字の大きさに rem を使う理由", lang="css",
        prompt="文字の大きさ（font-size）を、px ではなく、rem や em で指定することが推奨される理由として、最も適切なものはどれですか？",
        choices=[
            ("px で指定すると、ブラウザの表示が崩れてエラーになるから", "px で指定しても、エラーにはなりません。問題は、利用者が文字サイズを変えたときに、追従しにくいことです。"),
            ("ブラウザの文字サイズの設定を変えた利用者に、追従して大きさが変わるから", ""),
            ("rem や em のほうが、常に px より、文字が大きくなるから", "rem や em は、基準の大きさに対する倍率で、px より大きくなるとは限りません。基準によって変わるので、設定に追従します。"),
        ],
        correct=1,
        why="rem・em は、基準の文字の大きさに対する倍率なので、利用者の設定した文字サイズに追従できるから。",
        expl="視力などの事情で、ブラウザの標準の文字サイズを大きくしている人がいます。px で固定すると、その設定が効かず、読みにくいままになることがあります。",
        concepts=["rem", "アクセシビリティ"], diff=3,
        hint="px は「固定」、rem は「基準に対する倍率」です。",
        ok="正解！利用者の設定に追従できます。",
        ng="惜しい！px が「固定」であることを考えましょう。",
    ),
    bugfix(
        title="単位のない font-size", lang="css",
        prompt="段落の文字を 20px にしたいのに、大きさが変わりません。2行目を直したものはどれですか？",
        code='''p {
  font-size: 20;
}''',
        fixed='''p {
  font-size: 20px;
}''',
        check={"format": "css", "given_html": "<p>こんにちは</p>", "expr": "getComputedStyle(document.querySelector('p')).fontSize === '20px'"},
        target_line=2,
        choices=[
            ("font-size: 20 px;", "数値と単位の間に空白があると、1つの値として読めず、無効になります。単位は、数値にくっつけて書きます。"),
            ("font-size: 20px;", ""),
            ('font-size: "20px";', "値を引用符で囲むと、文字列になります。font-size には、長さの値（20px など）を、そのまま書きます。"),
        ],
        correct=1, fmt="code",
        why="0 以外の数値には、単位（px など）を、数値にくっつけて書く必要があるから。",
        expl="単位がない数値は、無効な値として、宣言ごと無視されます。そのため、エラーにならず、大きさが標準のままになります。",
        concepts=["font-size", "単位"], diff=2,
        hint="数値のあとに、続けて何を書くのでしょう？",
        ok="正解！数値には単位を付けます。",
        ng="惜しい！数値と単位の書き方を確認しましょう。",
    ),
    fill(
        title="中央揃え", lang="css",
        prompt="見出しの文字を、水平方向の中央に揃えます。【空欄1】に入れる値を答えてください。",
        code='''h1 {
  text-align: __1__;
}''',
        check={"format": "css", "given_html": "<h1>ようこそ</h1>", "expr": "getComputedStyle(document.querySelector('h1')).textAlign === 'center'"},
        blanks=[(["center"], False)],
        wrong=[("b1", "middle", "middle という値はありません。無効な値は無視されるので、標準の左揃えのままです。中央揃えは center です。")],
        why="中央揃えの値は center だから。",
        expl="text-align の主な値は、left（左揃え）・center（中央揃え）・right（右揃え）です。日本語では「中央」ですが、CSS の値は center と書きます。",
        concepts=["text-align"], diff=1,
        hint="中心を意味する英単語（英国式の綴りではなく）です。",
        ok="正解！text-align: center です。",
        ng="惜しい！「真ん中」を表す、CSS の値を入力しましょう。",
    ),
    pred(
        title="子セレクタの対象", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、文字が赤くなる段落は、どれですか？（R が赤、- が赤でないことを表します。上から順に A・B です）",
        code='''div > p {
  color: red;
}''',
        check={"format": "css", "given_html": '<div>\n  <p>A</p>\n  <section>\n    <p>B</p>\n  </section>\n</div>', "probe": "Array.from(document.querySelectorAll('p')).map(function (p) { return getComputedStyle(p).color === 'rgb(255, 0, 0)' ? 'R' : '-'; }).join('')"},
        choices=[
            ("A と B の両方（RR）", "div > p の > は、直接の子だけを選びます。B は、section の中にあり、div の直接の子ではありません。", "RR"),
            ("A だけ（R-）", "", "R-"),
            ("どちらも赤くならない（--）", "A は div の直接の子の p なので、赤くなります。", "--"),
        ],
        correct=1,
        why="div > p は、div の直接の子の p だけを選び、section の中の p には当たらないから。",
        expl="空白で区切る子孫セレクタ（div p）なら、B も選ばれて RR になります。> で区切る子セレクタは、直接の子に限定します。",
        concepts=["子セレクタ", "子孫セレクタ"], diff=3,
        hint="B は、div の直接の子ですか？ それとも、section の中ですか？",
        ok="正解！> は、直接の子だけを選びます。",
        ng="惜しい！> と空白の違いを確認しましょう。",
    ),
    bugfix(
        title="見出しをまとめて指定する", lang="css",
        prompt="h1 と h2 の両方を青くしたいのに、どちらも青くなりません。1行目を正しく書き直して入力してください（1行目の内容をすべて入力）。",
        code='''h1 h2 {
  color: blue;
}''',
        fixed='''h1, h2 {
  color: blue;
}''',
        check={"format": "css", "given_html": "<h1>見出し1</h1>\n<h2>見出し2</h2>", "expr": "getComputedStyle(document.querySelector('h1')).color === 'rgb(0, 0, 255)' && getComputedStyle(document.querySelector('h2')).color === 'rgb(0, 0, 255)'"},
        target_line=1, accepted=["h1, h2 {", "h1,h2 {", "h1, h2{", "h1,h2{"],
        wrong=[("h1 h2 {", "元のコードのままです。空白は子孫セレクタで、「h1 の中にある h2」という意味になります。並んだ h1 と h2 の両方に当てるには、カンマで区切ります。")],
        why="複数のセレクタに同じスタイルを当てるときは、カンマで区切るから。",
        expl="h1 h2 は、h1 要素の中にある h2 だけを選ぶセレクタです。h1 と h2 を並べて書いただけでは、そのような構造のものがないので、何にも当たりません。",
        concepts=["グループ化", "子孫セレクタ"], diff=2,
        hint="複数のセレクタを並べるときの区切りの記号は何でしょう？",
        ok="正解！カンマでグループ化します。",
        ng="惜しい！空白とカンマの意味の違いを確認しましょう。",
    ),
    mc(
        title="疑似クラス :hover", lang="css",
        prompt="次の CSS は、どんなときに、リンクの文字を赤くしますか？",
        code='''a:hover {
  color: red;
}''',
        choices=[
            ("マウスポインターが、リンクの上に乗っているとき", ""),
            ("リンクを、すでに1回クリックしたことがあるとき", "クリック済みのリンクを選ぶのは、:visited という別の疑似クラスです。:hover は、マウスが乗っている状態です。"),
            ("ページを読み込んだ直後の、すべてのリンク", "常に適用するなら、疑似クラスなしの a { color: red; } と書きます。:hover は、マウスが乗っている間だけの指定です。"),
        ],
        correct=0,
        why=":hover は、マウスポインターが乗っている状態を表す疑似クラスだから。",
        expl="疑似クラスは、要素の「状態」に応じてスタイルを当てるための仕組みです。:hover（マウスが乗っている）のほかに、:focus（入力欄などが選ばれている）、:first-child（最初の子）などがあります。",
        concepts=["疑似クラス", ":hover"], diff=2,
        hint="hover は、「浮かぶ」「乗る」という意味の英単語です。",
        ok="正解！:hover は、マウスが乗っている状態です。",
        ng="惜しい！hover の意味を考えましょう。",
    ),
    write_page(
        title="文字を整えたページ", lang="css", fmt="css",
        prompt="次の HTML に、CSS だけで、次の見た目を指定してください。\n・h1: 文字を中央揃え、文字色を #0044cc、大きさを 2rem\n・class が lead の段落: 大きさを 1.25rem、太字\n・すべての p: 行の高さを、文字の大きさの 1.8 倍（単位なしの数値）\n・a: 下線を消す\n・strong: 文字色を red",
        given_html='<h1>旅の記録</h1>\n<p class="lead">京都に行きました。</p>\n<p>清水寺で<strong>夕日</strong>を見ました。</p>\n<a href="#">ページの先頭へ</a>',
        starter="/* ここに CSS を書きましょう */\n",
        ref='''h1 {
  text-align: center;
  color: #0044cc;
  font-size: 2rem;
}
.lead {
  font-size: 1.25rem;
  font-weight: bold;
}
p {
  line-height: 1.8;
}
a {
  text-decoration: none;
}
strong {
  color: red;
}''',
        alts=['''h1 { text-align: center; color: rgb(0, 68, 204); font-size: 32px; }
p { line-height: 1.8; }
p.lead { font-size: 20px; font-weight: 700; }
a { text-decoration: none; }
p strong { color: #f00; }'''],
        bads=[
            ('''h1 {
  text-align: center;
  color: #0044cc;
  font-size: 2rem;
}
.lead {
  font-size: 1.25rem;
  font-weight: bold;
}
a {
  text-decoration: none;
}
strong {
  color: red;
}''', "すべての p の行の高さ（line-height）を指定していません。p セレクタで 1.8 を指定します。"),
            ('''h1 { text-align: center; color: #0044cc; font-size: 2rem; }
.lead { font-size: 1.25rem; }
p { line-height: 1.8; }
a { text-decoration: none; }
strong { color: red; }''', ".lead が太字になっていません。font-weight: bold（または 700）も指定します。"),
        ],
        tests=[
            t_page("h1: 中央揃え・色 #0044cc・大きさ 2rem（32px）", "(function () { var s = getComputedStyle(document.querySelector('h1')); return s.textAlign === 'center' && s.color === 'rgb(0, 68, 204)' && s.fontSize === '32px'; })()"),
            t_page(".lead: 大きさ 1.25rem（20px）で太字", "(function () { var s = getComputedStyle(document.querySelector('p.lead')); return s.fontSize === '20px' && s.fontWeight === '700'; })()"),
            t_page("p の行の高さが、文字の大きさの 1.8 倍（16px なら 28.8px）", "getComputedStyle(document.querySelectorAll('p')[1]).lineHeight === '28.8px'"),
            t_page("a の下線がない", "getComputedStyle(document.querySelector('a')).textDecorationLine === 'none'"),
            t_page("strong の文字色が赤", "getComputedStyle(document.querySelector('strong')).color === 'rgb(255, 0, 0)'"),
            t_page(".lead の行の高さも、文字の大きさの 1.8 倍（20px なら 36px）", "getComputedStyle(document.querySelector('p.lead')).lineHeight === '36px'", visible=False),
        ],
        why="色・大きさ・太さ・行間・揃え・装飾のプロパティを、それぞれのセレクタに指定するから。",
        expl="line-height は、単位のない数値（1.8）にすると、文字の大きさが違っても、それぞれに合わせた行間になります。.lead は文字が大きいので、行の高さも 36px になります。a の下線は、text-decoration: none で消せます。",
        concepts=["font-size", "line-height", "text-align", "text-decoration", "rem"], diff=3,
        hint="5つのルールを書きます。line-height は、単位なしの数値です。",
        ok="正解！文字の装飾ができました。",
        ng="惜しい！.lead や strong の指定、line-height の値を確認しましょう。",
    ),
]
