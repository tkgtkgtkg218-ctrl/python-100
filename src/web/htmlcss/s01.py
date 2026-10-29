from lib_web import mc, pred, fill, bugfix, write_page, t_page

DOC_TITLE = '''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>ぼくのページ</title>
</head>
<body>
  <h1>ようこそ</h1>
</body>
</html>'''

STAGE = {
    "number": 1,
    "title": "HTMLの基本構造",
    "subtitle": "要素・タグ・属性と、HTML文書の骨組み",
    "goals": [
        "HTML がWebページの構造と意味を表すマークアップ言語であることを説明できる",
        "要素・開始タグ・終了タグ・内容・属性という用語を正しく使い分けられる",
        "<!doctype html>・html・head・body の役割を説明できる",
        "最小の HTML 文書を自分で書ける",
        "ブラウザが空白・改行・コメントをどう扱うかを説明できる",
    ],
    "prerequisites": ["特になし（テキストエディタでファイルを保存し、ブラウザで開ければ十分です）"],
    "topics": [
        "HTML とは（マークアップ言語。CSS・JavaScript との役割の違い）",
        "要素、開始タグ、終了タグ、内容",
        "属性と属性値",
        "文書型宣言 <!doctype html>",
        "html・head・body、meta charset、title",
        "コメント、空白と改行の扱い",
    ],
    "pitfalls": [
        "HTML は「実行」するものではなく、ブラウザが読み取って表示するもの",
        "終了タグの書き忘れ（ブラウザが推測して直すため、意図と違う構造になる）",
        "<!doctype html> を書かないと、ブラウザが古い互換モードで表示する",
        "ソースの改行や連続した空白は、そのままは表示されない",
        "属性値は引用符で囲む",
    ],
    "next_links": ["見出し・段落・強調など、文章の構造を表す要素を学びます（ステージ2）"],
    "lesson": {
        "intro": "Webページは、「何が見出しで、何が段落で、どこにリンクがあるか」という構造をもっています。その構造を、文章に目印（タグ）を付けて表すのが HTML です。まずは HTML の用語と、どのページにも共通する骨組みを覚えましょう。",
        "sections": [
            {
                "id": "S01-L1",
                "title": "HTML とは・要素と属性",
                "read_minutes": 3,
                "body": [
                    "HTML（HyperText Markup Language）は、文章の構造や意味をタグで示す「マークアップ言語」です。計算や条件分岐を書くプログラミング言語ではありません。見た目を整えるのは CSS（スタイルシート言語）、動きを付けるのは JavaScript（プログラミング言語）で、HTML・CSS・JavaScript がそれぞれ別の役割を担当します。",
                    "HTML は「実行」するのではなく、ブラウザが読み取って画面に表示します。.html という拡張子でファイルを UTF-8 で保存し、ブラウザで開けば確認できます。",
                    "HTML の基本単位は要素です。要素は、開始タグ（<p>）、内容（こんにちは）、終了タグ（</p>）でできています。終了タグには / が付きます。要素の中に別の要素を入れることを入れ子といい、閉じる順番は開いた順の逆にします。",
                    "開始タグの中に、追加の情報を属性（名前=\"値\"）で書けます。例: <p class=\"note\"> の class が属性名、note が属性値です。属性値は引用符で囲みます。<br> や <meta> のように内容を持たない要素（空要素）は、終了タグを書きません。",
                ],
                "glossary": [
                    {"term": "マークアップ言語", "definition": "文章にタグ（目印）を付けて、構造や意味を表す言語。HTML が代表例。"},
                    {"term": "要素", "definition": "開始タグ・内容・終了タグのまとまり。"},
                    {"term": "タグ", "definition": "< > で囲んだ目印。開始タグと終了タグがある。"},
                    {"term": "属性", "definition": "開始タグの中に書く、要素への追加情報。名前=\"値\" の形。"},
                    {"term": "空要素", "definition": "内容を持たず、終了タグを書かない要素（br, meta, img など）。"},
                ],
                "examples": [
                    {
                        "id": "S01-E1", "title": "要素の構成と属性", "language": "html",
                        "code": '''<p class="note">こんにちは、<strong>HTML</strong>です。</p>''',
                        "line_notes": ["<p class=\"note\"> が開始タグ、class が属性名、note が属性値です。", "「こんにちは、…です。」が内容で、</p> が終了タグです。", "<strong> は、p 要素の内容の中に入れ子になった要素です。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "document.querySelector('p.note').getAttribute('class') === 'note' && document.querySelector('p.note > strong').textContent === 'HTML'"},
                    },
                    {
                        "id": "S01-E2", "title": "入れ子と空要素", "language": "html",
                        "code": '''<p>1行目<br>2行目</p>''',
                        "line_notes": ["<br> は改行を表す空要素で、終了タグはありません。", "p 要素の内容の中に br 要素が入っています。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "document.querySelectorAll('p > br').length === 1"},
                    },
                ],
            },
            {
                "id": "S01-L2",
                "title": "HTML文書の骨組み",
                "read_minutes": 3,
                "body": [
                    "どのHTMLファイルも、次の骨組みから始めます。1行目の <!doctype html> は文書型宣言で、「これは現在の標準的な HTML です」とブラウザに伝えます。書き忘れると、ブラウザが古い表示ルール（互換モード）に切り替わり、レイアウトが意図とずれることがあります。",
                    "<html lang=\"ja\"> は文書全体を表す要素で、lang 属性で言語（日本語）を示します。その中は2つに分かれます。head には画面に直接は表示されない情報（文字コード <meta charset=\"utf-8\">、ページのタイトル <title> など）を、body には画面に表示する内容を書きます。",
                    "title はブラウザのタブや検索結果に表示されます。本文の見出し（h1 など）とは別のものです。",
                    "ソースコード中の改行や連続する空白は、表示するときには1つの空白としてまとめられます。改行したい場所には、<br> や段落（p 要素）を使います。<!-- と --> で囲んだ部分はコメントで、画面には表示されません。",
                ],
                "glossary": [
                    {"term": "文書型宣言", "definition": "<!doctype html>。文書の先頭に書き、標準モードで表示するようブラウザに伝える。"},
                    {"term": "head", "definition": "文書についての情報（文字コード・タイトルなど）を書く部分。"},
                    {"term": "body", "definition": "画面に表示する内容を書く部分。"},
                    {"term": "コメント", "definition": "<!-- ... --> で囲んだ、表示されないメモ。"},
                ],
                "examples": [
                    {
                        "id": "S01-E3", "title": "最小のHTML文書", "language": "html",
                        "code": DOC_TITLE,
                        "line_notes": ["1行目: 文書型宣言。必ず先頭に書きます。", "2行目: 文書全体を表す html 要素。lang=\"ja\" で日本語であることを示します。", "4行目: 文字コードを UTF-8 と指定します（空要素なので終了タグはありません）。", "5行目: ブラウザのタブに表示されるタイトルです。", "8行目: 画面に表示される見出しです。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "expr": "document.compatMode === 'CSS1Compat' && document.title === 'ぼくのページ' && document.documentElement.lang === 'ja' && document.querySelector('body > h1').textContent === 'ようこそ'"},
                    },
                    {
                        "id": "S01-E4", "title": "空白・改行・コメント", "language": "html",
                        "code": '''<p>こんにちは     世界
   です</p>
<!-- この行は表示されない -->
<p>おわり</p>''',
                        "line_notes": ["1〜2行目: 連続する空白や改行は、表示では1つの空白にまとめられます（「こんにちは 世界 です」）。", "3行目: コメントは画面に表示されません。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "document.querySelectorAll('p').length === 2 && document.querySelector('p').innerText === 'こんにちは 世界 です'"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "doctype の書き忘れ", "wrong_code": "<html lang=\"ja\">\n<body>…</body>\n</html>", "why": "<!doctype html> がないと、古い表示ルール（互換モード）で表示されます。", "fix": "文書の先頭に <!doctype html> を書く"},
            {"title": "終了タグの書き忘れ", "wrong_code": "<h1>見出し\n<p>本文</p>", "why": "h1 を閉じていないため、p 要素が h1 の中に入ってしまいます。ブラウザは推測で補うので、意図と違う構造になります。", "fix": "<h1>見出し</h1>"},
            {"title": "入れ子の順序が逆", "wrong_code": "<p><strong>強調</p></strong>", "why": "開いた順の逆に閉じる必要があります。順序が崩れると、ブラウザが推測で直し、構造が意図とずれることがあります。", "fix": "<p><strong>強調</strong></p>"},
            {"title": "属性値を引用符で囲まない", "wrong_code": "<p class=big note>", "why": "空白で値が切れ、note が別の属性として扱われます。属性値は引用符で囲みます。", "fix": "<p class=\"big note\">"},
        ],
        "checkpoints": [
            "HTML はマークアップ言語（プログラミング言語ではない）",
            "要素 ＝ 開始タグ ＋ 内容 ＋ 終了タグ",
            "属性は 名前=\"値\" の形で開始タグに書く",
            "空要素（br, meta など）に終了タグはない",
            "<!doctype html> を先頭に書く",
            "head は画面に表示されない情報、body は表示する内容",
            "ソースの連続した空白・改行は、表示では1つの空白になる",
        ],
        "next_bridge": "骨組みが書けるようになりました。問題で、タグや属性の用語、ブラウザの表示のされ方を確かめましょう。",
    },
}

QUESTIONS = [
    mc(
        title="HTMLの役割", lang="html",
        prompt="HTML の説明として、正しいものはどれですか？",
        choices=[
            ("文章の構造や意味を、タグで示すマークアップ言語である", ""),
            ("ページの色や余白など、見た目を指定するスタイルシート言語である", "それは CSS の説明です。HTML は見た目ではなく、「どこが見出しで、どこが段落か」といった構造と意味を表します。"),
            ("計算や条件分岐を書いて、ページに動きを付けるプログラミング言語である", "それは JavaScript の説明です。HTML には計算や条件分岐の仕組みはなく、プログラミング言語とは区別されます。"),
        ],
        correct=0,
        why="HTML は、タグで文章の構造と意味を表すマークアップ言語だから。",
        expl="Webページは、HTML（構造と意味）、CSS（見た目）、JavaScript（動き）の3つで作ります。それぞれの役割が違うので、「HTML でデザインを変える」「HTML で計算する」とは言いません。",
        concepts=["HTMLの役割", "マークアップ言語"], diff=1,
        hint="HTML の M は Markup（目印を付ける）の M です。",
        ok="正解！HTML は構造と意味を表すマークアップ言語です。",
        ng="惜しい！見た目は CSS、動きは JavaScript の担当です。",
    ),
    mc(
        title="終了タグ", lang="html",
        prompt="次の p 要素で、</p> の部分は何と呼びますか？",
        code='''<p>こんにちは</p>''',
        choices=[
            ("開始タグ", "開始タグは、内容の前にある <p> の部分です。</p> のように / が付くのは終了タグです。"),
            ("属性", "属性は、開始タグの中に 名前=\"値\" の形で書く追加情報です。ここには属性は書かれていません。"),
            ("終了タグ", ""),
        ],
        correct=2,
        why="内容のあとに書き、/ が付いたタグが終了タグだから。",
        expl="p 要素は、開始タグ <p>、内容「こんにちは」、終了タグ </p> でできています。「開始タグ」「内容」「終了タグ」をまとめたものが要素です。",
        concepts=["要素", "終了タグ"], diff=1,
        hint="/ が付いているのは、開始・終了のどちらでしょう？",
        ok="正解！</p> は終了タグです。",
        ng="惜しい！内容のあとの、/ が付いたタグを何と呼ぶか思い出しましょう。",
    ),
    pred(
        title="タブに表示される文字", lang="html",
        prompt="次の HTML をブラウザで開いたとき、ブラウザのタブ（ページのタイトル）に表示される文字列はどれですか？",
        code=DOC_TITLE,
        check={"format": "html_document", "probe": "document.title"},
        choices=[
            ("ようこそ", "「ようこそ」は body の中の h1 要素で、ページの本文の見出しです。タブに出るのは title 要素の内容です。", "ようこそ"),
            ("ぼくのページ", "", "ぼくのページ"),
            ("ja", "ja は html 要素の lang 属性の値で、文書の言語を示すだけです。画面にもタブにも表示されません。", "ja"),
        ],
        correct=1,
        why="タブに表示されるのは head の中の title 要素の内容だから。",
        expl="title 要素は、ブラウザのタブ、ブックマーク、検索結果に表示されます。body の中の h1 とは別物なので、両方を適切に書きます。",
        concepts=["title要素", "head"], diff=1,
        hint="タブに出る文字は、head と body のどちらに書かれていますか？",
        ok="正解！タブには title 要素の内容が表示されます。",
        ng="惜しい！title 要素の内容を探しましょう。",
    ),
    fill(
        title="文字コードの指定", lang="html",
        prompt="文字コードを UTF-8 と指定する meta 要素です。【空欄1】に入れるものを答えてください（半角で入力）。",
        code='''<!doctype html>
<html lang="ja">
<head>
  <meta charset="__1__">
  <title>テスト</title>
</head>
<body>
  <p>こんにちは</p>
</body>
</html>''',
        check={"format": "html_document", "expr": "document.querySelector('meta[charset]') !== null && document.querySelector('meta[charset]').getAttribute('charset').toLowerCase() === 'utf-8'"},
        blanks=[(["UTF-8", "utf-8"], False)],
        wrong=[("b1", "Shift_JIS", "文字コードは、現在のWebでは UTF-8 を指定するのが標準です。ファイル自体も UTF-8 で保存します。")],
        why="現在のWebの標準の文字コードは UTF-8 で、charset 属性にその名前を書くから。",
        expl="meta 要素の charset 属性で、HTML ファイルの文字コードをブラウザに伝えます。指定がファイルの実際の文字コードと違うと、文字化けの原因になります。UTF-8 は大文字・小文字どちらで書いても構いません。",
        concepts=["meta charset", "属性"], diff=2,
        hint="現在のWebで標準的に使われる文字コードの名前です。",
        ok="正解！charset=\"utf-8\" と指定します。",
        ng="惜しい！UTF-8 と入力してみましょう。",
    ),
    bugfix(
        title="doctype がない文書", lang="html",
        prompt="次の HTML は、ブラウザが古い互換モードで表示してしまいます。標準モードで表示されるようにする直し方はどれですか？",
        code='''<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>テスト</title>
</head>
<body>
  <p>こんにちは</p>
</body>
</html>''',
        fixed='''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>テスト</title>
</head>
<body>
  <p>こんにちは</p>
</body>
</html>''',
        check={"format": "html_document", "expr": "document.compatMode === 'CSS1Compat'"},
        choices=[
            ("head の中に <!doctype html> を書く", "文書型宣言は文書の一番最初に書くものです。head の中に書いても有効にならず、互換モードのままです。"),
            ("文書の1行目に <!doctype html> を書く", ""),
            ("html の後ろに <!-- html5 --> というコメントを書く", "コメントは表示されないメモで、文書型宣言の代わりにはなりません。"),
        ],
        correct=1, fmt="text",
        why="<!doctype html> を文書の先頭に書くと、ブラウザが標準モードで表示するから。",
        expl="doctype がないと、ブラウザは古いページとの互換のために「互換モード」で表示し、余白や大きさの計算が標準とずれることがあります。必ず1行目に <!doctype html> を書きます。",
        concepts=["文書型宣言", "標準モード"], diff=2,
        hint="文書型宣言は、文書のどこに書くものでしたか？",
        ok="正解！<!doctype html> を1行目に書きます。",
        ng="惜しい！文書型宣言は一番先頭に書きます。",
    ),
    bugfix(
        title="閉じ忘れた見出し", lang="html",
        prompt="p 要素が h1 要素の中に入ってしまっています。1行目を正しく書き直して入力してください（1行目の内容だけを入力）。",
        code='''<h1>見出し
<p>本文</p>''',
        fixed='''<h1>見出し</h1>
<p>本文</p>''',
        check={"format": "html_body", "expr": "document.querySelector('p').parentElement.tagName === 'BODY'"},
        target_line=1, accepted=["<h1>見出し</h1>"],
        wrong=[("<h1>見出し<h1>", "終了タグには / が必要です。/ がないと、もう1つ h1 を開始したことになってしまいます。")],
        why="h1 の終了タグ </h1> を書いて、見出しを閉じる必要があるから。",
        expl="終了タグを忘れると、ブラウザはどこで終わるか推測するため、p 要素が h1 の内側に入ってしまいます。本文が見出しの一部になってしまうので、要素は必ず閉じます。",
        concepts=["終了タグ", "入れ子"], diff=2,
        hint="見出しの内容のあとに、何を書けば要素が閉じますか？",
        ok="正解！終了タグで h1 を閉じました。",
        ng="惜しい！開始タグ <h1> に対応する終了タグを書きましょう。",
    ),
    mc(
        title="属性名と属性値", lang="html",
        prompt="次の html 要素の開始タグで、lang=\"ja\" の部分を何と呼びますか？",
        code='''<html lang="ja">''',
        choices=[
            ("要素", "要素は、開始タグ・内容・終了タグ全体のまとまりです。lang=\"ja\" はその開始タグの中の一部です。"),
            ("属性", ""),
            ("終了タグ", "終了タグは </html> のように / が付くタグです。lang=\"ja\" は開始タグの中に書く追加情報です。"),
        ],
        correct=1,
        why="開始タグの中に 名前=\"値\" の形で書く追加情報は、属性と呼ぶから。",
        expl="lang が属性名、\"ja\" が属性値です。この属性は、文書が日本語で書かれていることを示し、読み上げソフトや翻訳機能が利用します。",
        concepts=["属性", "lang"], diff=1,
        hint="名前=\"値\" の形で、開始タグの中に書かれています。",
        ok="正解！lang=\"ja\" は属性です。",
        ng="惜しい！開始タグの中の 名前=\"値\" は何と呼ぶでしょう？",
    ),
    pred(
        title="コメントの中の要素", lang="html",
        prompt="次の HTML をブラウザで表示したとき、画面に表示される p 要素（段落）はいくつですか？数字で入力してください。",
        code='''<p>A</p>
<!-- <p>B</p> -->
<p>C</p>''',
        check={"format": "html_body", "probe": "document.querySelectorAll('p').length", "expected": 2},
        out="2",
        wrong=[("3", "<!-- と --> で囲んだ部分はコメントです。コメントの中の <p>B</p> は、要素としても扱われず、表示されません。"), ("1", "コメントになっているのは B だけです。A と C の p 要素は表示されます。")],
        why="コメントの中の B は表示されず、A と C の2つだけが表示されるから。",
        expl="<!-- ... --> の内側は、ブラウザに無視されます。一時的にある部分を非表示にしたいとき、その部分をコメントにする使い方がよくあります。",
        concepts=["コメント"], diff=1,
        hint="<!-- と --> で囲まれた部分はどう扱われるでしょう。",
        ok="正解！コメントの中は表示されません。",
        ng="惜しい！コメントになっている部分を除いて数えましょう。",
    ),
    pred(
        title="空白と改行の表示", lang="html",
        prompt="次の HTML は、ソースの中で空白を多く入れ、途中で改行しています。ブラウザの表示では、この空白と改行はどう扱われますか？",
        code='''<p>こんにちは     世界
   です</p>''',
        check={"format": "html_body", "probe": "(function(){var t=document.querySelector('p').innerText; return /\\s{2,}|\\n/.test(t) ? 'preserved' : 'collapsed';})()"},
        choices=[
            ("ソースに書いたとおり、空白や改行がそのまま表示される", "HTML では、連続する空白や改行は、そのままは表示されません。改行したい場所には <br> や p 要素を使います。", "preserved"),
            ("連続する空白や改行は、1つの空白にまとめて表示される", "", "collapsed"),
            ("空白と改行がすべて取り除かれ、文字がつながって表示される", "取り除かれるのではなく、1つの空白に置き換わります。そのため、「世界」と「です」の間にも空白が1つ入ります。", "joined"),
        ],
        correct=1,
        why="HTML では、連続する空白や改行は1つの空白としてまとめて表示されるから。",
        expl="ソースの見やすさのために改行や字下げを使っても、表示には影響しません。逆に、表示で改行したいときは、ソースを改行するだけでは足りず、<br> や段落の要素を使います。",
        concepts=["空白の扱い", "br"], diff=2,
        hint="ソースを改行しても、画面で改行されるとは限りません。",
        ok="正解！連続する空白や改行は1つの空白になります。",
        ng="惜しい！HTML は連続した空白をまとめて表示します。",
    ),
    write_page(
        title="最小のHTML文書を書く", lang="html", fmt="html_document",
        prompt="次の条件を満たす HTML 文書を書いてください。\n・1行目に文書型宣言\n・html 要素に lang=\"ja\"\n・head の中に、文字コード UTF-8 の meta と、タイトル「マイページ」の title\n・body の中に、内容が「ようこそ」の見出し（h1）",
        starter="<!-- ここに書きましょう -->\n",
        ref='''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>マイページ</title>
</head>
<body>
  <h1>ようこそ</h1>
</body>
</html>''',
        alts=['''<!DOCTYPE html>
<html lang="ja">
<head>
<title>マイページ</title>
<meta charset="UTF-8">
</head>
<body><h1>ようこそ</h1></body>
</html>'''],
        bads=[
            ('''<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>マイページ</title>
</head>
<body>
  <h1>ようこそ</h1>
</body>
</html>''', "文書型宣言 <!doctype html> がありません。1行目に書きます。"),
            ('''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>ようこそ</title>
</head>
<body>
  <h1>マイページ</h1>
</body>
</html>''', "title と h1 の内容が入れ替わっています。title は「マイページ」、h1 は「ようこそ」です。"),
        ],
        tests=[
            t_page("文書型宣言があり、標準モードで表示される", "document.compatMode === 'CSS1Compat'"),
            t_page("html 要素の lang が ja", "document.documentElement.lang === 'ja'"),
            t_page("meta で文字コードが UTF-8", "(function(){var m=document.querySelector('head > meta[charset]'); return !!m && m.getAttribute('charset').toLowerCase()==='utf-8';})()"),
            t_page("title が「マイページ」", "document.title === 'マイページ'"),
            t_page("body に h1「ようこそ」がある", "(function(){var h=document.querySelector('body > h1'); return !!h && h.textContent.trim()==='ようこそ';})()"),
        ],
        why="doctype・lang・meta charset・title・h1 の5つがそろった骨組みを書くから。",
        expl="どのHTMLファイルも、この骨組みから始めます。head には画面に表示されない情報（文字コードとタイトル）、body には表示する内容（h1）を書きます。タグの大文字・小文字は区別されませんが、小文字で書くのが一般的です。",
        concepts=["HTML文書の骨組み", "doctype", "head", "body"], diff=2,
        hint="doctype → html（lang）→ head（meta, title）→ body（h1）の順に書きます。",
        ok="正解！HTML文書の骨組みが書けました。",
        ng="惜しい！5つの条件を1つずつ見直しましょう。",
    ),
]
