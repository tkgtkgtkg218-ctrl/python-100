from lib_web import mc, pred, fill, bugfix, write_page, t_page

STAGE = {
    "number": 3,
    "title": "リンクと画像",
    "subtitle": "a 要素と img 要素、パスの書き方、alt 属性",
    "goals": [
        "a 要素と href 属性でリンクを作れる",
        "絶対URL・相対パス・ページ内リンク・メールリンクを書き分けられる",
        "target=\"_blank\" と rel=\"noopener noreferrer\" の意味を説明できる",
        "img 要素で画像を表示し、alt・width・height を正しく指定できる",
        "figure と figcaption で、画像に説明を付けられる",
    ],
    "prerequisites": ["HTML の基本構造（ステージ1）", "見出し・段落・ブロックとインライン（ステージ2）"],
    "topics": [
        "a 要素と href",
        "URL とパス（絶対URL / 相対パス / ../ / ページ内リンク / mailto:）",
        "target と rel",
        "img 要素（src / alt / width / height）",
        "alt の書き方",
        "figure と figcaption",
    ],
    "pitfalls": [
        "リンク先は href（src ではない）、画像のファイルは src（href ではない）",
        "相対パスは、いま書いている HTML ファイルの場所が基準",
        "リンクの文字を「こちら」にしない（リンク先が分かる文字にする）",
        "alt を書かない・「画像」などの無意味な文字にしない",
        "target=\"_blank\" を使うときは rel=\"noopener noreferrer\" も付ける",
    ],
    "next_links": ["項目を並べる「リスト」と、ページ全体の構造を表す要素を学びます（ステージ4）"],
    "lesson": {
        "intro": "Web（ウェブ）の「ウェブ（蜘蛛の巣）」は、ページとページがリンクでつながっていることに由来します。HTML では、a 要素でリンクを、img 要素で画像を表します。どちらも、「ファイルの場所（パス）」を正しく書くことが大切です。",
        "sections": [
            {
                "id": "S03-L1",
                "title": "リンク（a 要素）",
                "read_minutes": 3,
                "body": [
                    "リンクは a 要素で作り、リンク先を href 属性で指定します。<a href=\"https://example.com/\">外部サイト</a> のように、a 要素の内容が、画面に表示されるリンクの文字です。「こちら」ではなく「ねこの解説サイト」のように、リンク先が分かる文字にします。",
                    "href には、いくつかの書き方があります。(1) 絶対URL: https://example.com/ のように、ページのアドレス全体。(2) 相対パス: about.html（同じフォルダ）、pages/info.html（下のフォルダ）、../index.html（1つ上のフォルダ）のように、いま書いているファイルの場所を基準にした書き方。(3) ページ内リンク: #section のように、同じページの id が section の場所へ移動。(4) メールリンク: mailto:info@example.com。",
                    "リンク先を新しいタブで開くには target=\"_blank\" を付けます。このとき、リンク先のページから元のページを操作されるのを防ぐため、rel=\"noopener noreferrer\" も併せて付けるのが安全です。",
                ],
                "glossary": [
                    {"term": "href", "definition": "a 要素のリンク先を指定する属性（Hypertext REFerence）。"},
                    {"term": "絶対URL", "definition": "https:// から始まる、ページのアドレス全体。"},
                    {"term": "相対パス", "definition": "いま書いているファイルの場所を基準にした、ファイルの場所の書き方。"},
                ],
                "examples": [
                    {
                        "id": "S03-E1", "title": "いろいろなリンク", "language": "html",
                        "code": '''<p><a href="https://example.com/">外部サイト</a></p>
<p><a href="about.html">概要ページ</a></p>
<p><a href="#bottom">ページの下へ</a></p>
<p><a href="mailto:info@example.com">メールを送る</a></p>
<p id="bottom">ここがページの下</p>''',
                        "line_notes": ["1行目: 絶対URL。", "2行目: 相対パス（同じフォルダの about.html）。", "3行目: ページ内リンク。id が bottom の要素へ移動します。", "4行目: メールソフトを開くリンク。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "(function () { var a = document.querySelectorAll('a'); return a.length === 4 && a[0].getAttribute('href') === 'https://example.com/' && a[2].hash === '#bottom' && a[3].protocol === 'mailto:' && !!document.getElementById('bottom'); })()"},
                    },
                    {
                        "id": "S03-E2", "title": "新しいタブで開く", "language": "html",
                        "code": '''<a href="https://example.com/" target="_blank" rel="noopener noreferrer">新しいタブで開く</a>''',
                        "line_notes": ["target=\"_blank\" で新しいタブに開きます。", "rel=\"noopener noreferrer\" は、セキュリティとプライバシーのために付けます。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "(function () { var a = document.querySelector('a'); return a.target === '_blank' && a.relList.contains('noopener') && a.relList.contains('noreferrer'); })()"},
                    },
                ],
            },
            {
                "id": "S03-L2",
                "title": "画像（img 要素）",
                "read_minutes": 3,
                "body": [
                    "画像は img 要素で表します。img は内容を持たない空要素で、終了タグは書きません。src 属性に画像ファイルの場所を、alt 属性にその画像を言葉で説明した代替テキストを書きます。alt は、画像が表示できないときや、目の見えない人が読み上げソフトで読むときに使われる、大切な属性です。",
                    "alt には、画像の内容や、その画像が伝えたいことを書きます。「画像」「写真」のような言葉だけにはしません。飾りだけの画像（意味を持たないもの）には、alt=\"\"（空）と書き、読み上げでは読み飛ばされるようにします。",
                    "width と height 属性で、画像の表示の大きさ（px）を指定できます。あらかじめ指定しておくと、画像が読み込まれる前から場所が確保され、読み込み後に表示が動く（ガタつく）のを防げます。",
                    "画像に説明文（キャプション）を付けたいときは、figure 要素の中に img と figcaption 要素を入れます。",
                ],
                "glossary": [
                    {"term": "alt", "definition": "画像の代替テキスト。画像が表示できないときや、読み上げで使われる。"},
                    {"term": "src", "definition": "画像ファイルの場所を指定する属性（SouRCe）。"},
                    {"term": "figure / figcaption", "definition": "図とその説明（キャプション）をまとめる要素。"},
                ],
                "examples": [
                    {
                        "id": "S03-E3", "title": "画像の表示", "language": "html",
                        "code": '''<img src="images/cat.jpg" alt="窓辺で寝ている黒いねこ" width="300" height="200">''',
                        "line_notes": ["src は画像の場所（このファイルから見た相対パス）です。", "alt は画像の内容を言葉で説明します。", "width と height は、表示する大きさ（px）です。画像ファイルがあれば、その画像が 300×200 で表示されます（この例のファイルは用意していないので、プレビューには alt の文字が出ます）。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "(function () { var i = document.querySelector('img'); return i.getAttribute('src') === 'images/cat.jpg' && i.alt === '窓辺で寝ている黒いねこ' && i.getAttribute('width') === '300' && i.getAttribute('height') === '200'; })()"},
                    },
                    {
                        "id": "S03-E4", "title": "図とキャプション", "language": "html",
                        "code": '''<figure>
  <img src="images/cat.jpg" alt="窓辺で寝ている黒いねこ" width="300" height="200">
  <figcaption>図1: 窓辺のねこ</figcaption>
</figure>''',
                        "line_notes": ["figure の中に、img と figcaption をまとめます。", "figcaption は、画像の下に表示される説明文です。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "document.querySelector('figure > img') !== null && document.querySelector('figure > figcaption').textContent === '図1: 窓辺のねこ'"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "href と src の取り違え", "wrong_code": "<a src=\"about.html\">概要</a>", "why": "リンク先を指定するのは href です。src では、リンクとして働きません。", "fix": "<a href=\"about.html\">概要</a>"},
            {"title": "alt を書かない", "wrong_code": "<img src=\"cat.jpg\">", "why": "代替テキストがないと、画像が見られない人に内容が伝わりません。", "fix": "<img src=\"cat.jpg\" alt=\"窓辺で寝ているねこ\">"},
            {"title": "ページ内リンクの id が合っていない", "wrong_code": "<a href=\"#section2\">…</a>\n<h2 id=\"sec2\">…</h2>", "why": "# のあとの文字が、移動先の id と完全に同じでないと、移動できません。", "fix": "<a href=\"#sec2\">"},
            {"title": "新しいタブで開くのに rel がない", "wrong_code": "<a href=\"…\" target=\"_blank\">", "why": "target=\"_blank\" を使うときは、rel=\"noopener noreferrer\" も付けると安全です。", "fix": "<a href=\"…\" target=\"_blank\" rel=\"noopener noreferrer\">"},
        ],
        "checkpoints": [
            "リンク先は href、画像の場所は src",
            "相対パスは、いま書いているファイルが基準（../ は1つ上）",
            "ページ内リンクは #id",
            "target=\"_blank\" には rel=\"noopener noreferrer\"",
            "img は空要素。alt を必ず書く（飾りなら alt=\"\"）",
            "figure と figcaption で、画像に説明を付けられる",
        ],
        "next_bridge": "リンクと画像で、ページ同士や、画像と文章をつなげられるようになりました。問題で、パスや alt の書き方を確かめましょう。",
    },
}

QUESTIONS = [
    mc(
        title="href の役割", lang="html",
        prompt="a 要素の href 属性は、何を指定するものですか？",
        code='''<a href="https://example.com/">サンプル</a>''',
        choices=[
            ("リンクをクリックしたときに移動する先（リンク先）", ""),
            ("画面に表示されるリンクの文字", "画面に表示される文字は、a 要素の内容（開始タグと終了タグの間）です。href は、移動先を指定する属性です。"),
            ("リンクの文字の色", "文字の色は CSS で指定します。href は、リンク先の指定です。"),
        ],
        correct=0,
        why="href は、リンク先のアドレスを指定する属性だから。",
        expl="a 要素は、内容（表示される文字）と、href 属性（リンク先）でできています。href がない a 要素は、リンクとして働きません。",
        concepts=["a要素", "href"], diff=1,
        hint="Hypertext REFerence（参照先）の略です。",
        ok="正解！href はリンク先を指定します。",
        ng="惜しい！href が何を指定するか確認しましょう。",
    ),
    mc(
        title="相対パスの書き方", lang="html",
        prompt="次のフォルダ構成で、index.html から images フォルダの cat.png を表示する img 要素の src は、どれが正しいですか？\n\nsite/\n├ index.html\n└ images/\n   └ cat.png",
        fmt="code",
        choices=[
            ('<img src="../images/cat.png" alt="ねこ">', "../ は「1つ上のフォルダ」を指します。index.html は site フォルダにあり、そこから見て images は同じ階層にあるので、../ は不要です。"),
            ('<img src="/images/cat.png" alt="ねこ">', "先頭の / は、サイトの一番上（ルート）を基準にした書き方です。site フォルダがサイトの最上位でない場合は、別の場所を指してしまいます。相対パスで書くのが確実です。"),
            ('<img src="images/cat.png" alt="ねこ">', ""),
        ],
        correct=2,
        why="index.html と同じ階層にある images フォルダの中を、そのまま images/cat.png と書けるから。",
        expl="相対パスは、いま書いている HTML ファイルの場所が基準です。同じフォルダなら cat.png、1つ下なら images/cat.png、1つ上なら ../cat.png のように書きます。",
        concepts=["相対パス", "img"], diff=2,
        hint="index.html から見て、images フォルダはどこにありますか？",
        ok="正解！同じ階層なら、フォルダ名から書き始めます。",
        ng="惜しい！index.html から見た位置を確認しましょう。",
    ),
    pred(
        title="../ で指すリンク先", lang="html",
        prompt="次の HTML で、base 要素は、このページのアドレスが https://example.com/blog/post1.html であることを表しています（相対パスの基準を示す要素です）。リンク「概要」をクリックすると、どのアドレスへ移動しますか？",
        code='''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <base href="https://example.com/blog/post1.html">
  <title>記事</title>
</head>
<body>
  <a href="../about.html">概要</a>
</body>
</html>''',
        check={"format": "html_document", "probe": "document.querySelector('a').href"},
        choices=[
            ("https://example.com/blog/about.html", "../ は、1つ上のフォルダを指します。blog フォルダの1つ上は example.com の最上位なので、blog の中の about.html ではありません。", "https://example.com/blog/about.html"),
            ("https://example.com/about.html", "", "https://example.com/about.html"),
            ("https://example.com/blog/post1.html/about.html", "post1.html はファイルで、フォルダではありません。相対パスは、ファイルがあるフォルダ（blog）が基準です。", "https://example.com/blog/post1.html/about.html"),
        ],
        correct=1,
        why="基準は blog フォルダで、../ はその1つ上（example.com の最上位）なので、そこの about.html を指すから。",
        expl="ファイルの場所（フォルダ）から、../ で1つ上へ戻り、about.html を探します。ページの URL が https://example.com/blog/post1.html なら、基準になるのは blog フォルダです。",
        concepts=["相対パス", "../"], diff=3,
        hint="相対パスの基準は、ファイル名の前の「フォルダ」です。",
        ok="正解！../ は1つ上のフォルダです。",
        ng="惜しい！基準のフォルダから、1つ上へ戻って考えましょう。",
    ),
    fill(
        title="画像の代替テキスト", lang="html",
        prompt="画像に「窓辺で寝ているねこ」という代替テキストを付けます。【空欄1】に入れる属性名を答えてください。",
        code='''<img src="cat.jpg" __1__="窓辺で寝ているねこ">''',
        check={"format": "html_body", "expr": "document.querySelector('img').getAttribute('alt') === '窓辺で寝ているねこ'"},
        blanks=[(["alt"], False)],
        wrong=[("b1", "title", "title は、マウスを乗せたときに出る補足ですが、画像の代替テキストではありません。画像が表示できないときや、読み上げでは alt が使われます。")],
        why="img の代替テキストを指定する属性は alt だから。",
        expl="alt は alternative（代わりの）の略です。画像が読み込めなかったときに表示される文字や、読み上げソフトが読む文字として使われます。",
        concepts=["alt"], diff=1,
        hint="alternative（代わりの）の略です。",
        ok="正解！alt は代替テキストです。",
        ng="惜しい！画像の代わりになる文字を指定する属性です。",
    ),
    mc(
        title="alt の役割", lang="html",
        prompt="img 要素の alt 属性の説明として、最も適切なものはどれですか？",
        choices=[
            ("画像の上にマウスを置いたときに出る、吹き出しの文字", "マウスを置いたときに出る文字は、title 属性で指定するものです。alt は、画像の代わりとなる文字です。"),
            ("画像が表示できないときや、読み上げソフトで読み上げられる、代替テキスト", ""),
            ("画像のファイル名を、画面に表示するための文字", "alt は、ファイル名ではなく、画像の内容を言葉で説明するための文字です。"),
        ],
        correct=1,
        why="alt は、画像を見られない場合に、画像の代わりに内容を伝える文字だから。",
        expl="画像が読み込めない、画像が見えない、読み上げを使っている、などの場合に、alt が画像の代わりになります。検索エンジンも、画像の内容を知る手がかりにします。",
        concepts=["alt", "アクセシビリティ"], diff=1,
        hint="alternative は「代わりの」という意味です。",
        ok="正解！alt は代替テキストです。",
        ng="惜しい！alt は、画像の代わりに内容を伝える文字です。",
    ),
    bugfix(
        title="新しいタブで開くリンクの安全性", lang="html",
        prompt="外部サイトを新しいタブで開くリンクです。安全のために、rel 属性を付けたいとき、正しく書いたものはどれですか？",
        code='''<a href="https://example.com/" target="_blank">外部サイト</a>''',
        fixed='''<a href="https://example.com/" target="_blank" rel="noopener noreferrer">外部サイト</a>''',
        check={"format": "html_body", "expr": "document.querySelector('a').relList.contains('noopener')"},
        target_line=1,
        choices=[
            ('<a href="https://example.com/" target="_blank" rel="external">外部サイト</a>', "rel=\"external\" は、外部サイトへのリンクであることを表すだけで、元のページを守る働きはありません。noopener が必要です。"),
            ('<a href="https://example.com/" target="_blank" rel="noopener noreferrer">外部サイト</a>', ""),
            ('<a href="https://example.com/" target="_blank" nofollow>外部サイト</a>', "nofollow は、rel 属性の値として書くもので、単独の属性としては存在しません。また、noopener の代わりにもなりません。"),
        ],
        correct=1, fmt="code",
        why="target=\"_blank\" のリンクには、rel=\"noopener noreferrer\" を付けると、元のページを守れるから。",
        expl="新しいタブで開いたページから、元のページを操作されてしまう危険を防ぐのが noopener です。noreferrer は、リンク元のアドレスを相手に伝えないための指定です。",
        concepts=["target", "rel", "セキュリティ"], diff=3,
        hint="rel の値として、2つの語をスペースで区切って書きます。",
        ok="正解！rel=\"noopener noreferrer\" を付けます。",
        ng="惜しい！元のページを守る値を選びましょう。",
    ),
    pred(
        title="画像の表示サイズ", lang="html",
        prompt="次の img 要素の画像ファイル（src の中身）は、本来の大きさが 1×1 ピクセルの、とても小さな画像です（画像のデータを src に直接書いています）。ブラウザは、この画像を、どの大きさで表示しますか？",
        code='''<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt="点" width="120" height="80">''',
        check={"format": "html_body", "probe": "(function () { var r = document.querySelector('img').getBoundingClientRect(); return Math.round(r.width) + 'x' + Math.round(r.height); })()"},
        choices=[
            ("本来の大きさの 1×1 ピクセルのまま表示される", "width と height を指定すると、画像は、その大きさに拡大（または縮小）されて表示されます。本来の大きさのままにはなりません。", "1x1"),
            ("幅120px × 高さ80px の大きさで表示される", "", "120x80"),
            ("width と height が大きすぎるので、表示されない", "width と height は、大きくても指定したとおりの大きさで表示されます。画像の本来の大きさと違うと、引き伸ばされてぼやけるので、画像に合わせた大きさにするのが基本です。", "0x0"),
        ],
        correct=1,
        why="width と height 属性を指定すると、画像は、その大きさで表示されるから。",
        expl="あらかじめ大きさを指定しておくと、画像の読み込み前から場所が確保され、読み込み後に周りの文章が動いてしまう（レイアウトのずれ）のを防げます。ただし、本来の大きさと違う値を指定すると、画像は拡大・縮小されます。",
        concepts=["img", "width", "height"], diff=2,
        hint="width と height は、「表示する大きさ」を指定する属性でした。",
        ok="正解！指定した大きさで表示されます。",
        ng="惜しい！width と height 属性の働きを思い出しましょう。",
    ),
    fill(
        title="リンク先を指定する属性", lang="html",
        prompt="a 要素のリンク先を指定します。【空欄1】に入れる属性名を答えてください。",
        code='''<a __1__="https://example.com/">サンプル</a>''',
        check={"format": "html_body", "expr": "document.querySelector('a').getAttribute('href') === 'https://example.com/'"},
        blanks=[(["href"], False)],
        wrong=[("b1", "src", "src は、img などで、画像ファイルの場所を指定する属性です。リンク先は href で指定します。")],
        why="リンク先は href 属性で指定するから。",
        expl="href（リンク先）と src（画像などの読み込み元）は、似ているので間違えやすい属性です。「リンクは href、画像は src」と覚えましょう。",
        concepts=["href", "src"], diff=1,
        hint="a 要素のリンク先の属性です。",
        ok="正解！リンク先は href です。",
        ng="惜しい！img の src と混同していませんか？",
    ),
    bugfix(
        title="ページ内リンクが動かない", lang="html",
        prompt="「第2章へ」をクリックしても、第2章の見出しへ移動しません。1行目を正しく書き直して入力してください（1行目の内容をすべて入力）。",
        code='''<a href="#section2">第2章へ</a>
<h2 id="sec2">第2章</h2>''',
        fixed='''<a href="#sec2">第2章へ</a>
<h2 id="sec2">第2章</h2>''',
        check={"format": "html_body", "expr": "document.getElementById(document.querySelector('a').getAttribute('href').slice(1)) !== null"},
        target_line=1, accepted=['<a href="#sec2">第2章へ</a>', "<a href='#sec2'>第2章へ</a>"], qi=True,
        wrong=[('<a href="#section2">第2章へ</a>', "元のコードのままです。# のあとの文字が、移動先の id（sec2）と一致していません。")],
        why="ページ内リンクの # のあとは、移動先の要素の id と、まったく同じ文字にする必要があるから。",
        expl="href=\"#section2\" は、id が section2 の要素を探します。h2 の id は sec2 なので、見つからず、移動しません。id の綴りを、リンク側と移動先で合わせます。",
        concepts=["ページ内リンク", "id"], diff=2,
        hint="# のあとの文字と、h2 の id を見比べましょう。",
        ok="正解！id と # のあとの文字を合わせます。",
        ng="惜しい！移動先の id を確認しましょう。",
    ),
    write_page(
        title="リンクと画像を使ったページ", lang="html", fmt="html_body",
        prompt="次の内容を HTML で書いてください（body の中身だけ）。\n・見出し1「ねこ図鑑」（id は top）\n・段落「詳しくは」のあとに、「ねこの解説サイト」というリンク（リンク先は https://example.com/cats、新しいタブで開き、安全のための rel も付ける）\n・画像（ファイルは images/cat.jpg、代替テキストは「窓辺で寝ているねこ」、幅300、高さ200）\n・段落の中に、ページの先頭（見出し1）へ戻る「ページの先頭へ」というページ内リンク",
        starter="<!-- ここに書きましょう -->\n",
        ref='''<h1 id="top">ねこ図鑑</h1>
<p>詳しくは<a href="https://example.com/cats" target="_blank" rel="noopener noreferrer">ねこの解説サイト</a></p>
<img src="images/cat.jpg" alt="窓辺で寝ているねこ" width="300" height="200">
<p><a href="#top">ページの先頭へ</a></p>''',
        alts=['''<h1 id="top">ねこ図鑑</h1>
<p>詳しくは<a target="_blank" rel="noreferrer noopener" href="https://example.com/cats">ねこの解説サイト</a></p>
<p><img alt="窓辺で寝ているねこ" src="images/cat.jpg" height="200" width="300"></p>
<p><a href="#top">ページの先頭へ</a></p>'''],
        bads=[
            ('''<h1 id="top">ねこ図鑑</h1>
<p>詳しくは<a href="https://example.com/cats" target="_blank">ねこの解説サイト</a></p>
<img src="images/cat.jpg" alt="窓辺で寝ているねこ" width="300" height="200">
<p><a href="#top">ページの先頭へ</a></p>''', "新しいタブで開くリンクに、rel=\"noopener noreferrer\" がありません。"),
            ('''<h1 id="top">ねこ図鑑</h1>
<p>詳しくは<a href="https://example.com/cats" target="_blank" rel="noopener noreferrer">ねこの解説サイト</a></p>
<img src="images/cat.jpg" width="300" height="200">
<p><a href="#top">ページの先頭へ</a></p>''', "img に alt 属性がありません。画像の内容を言葉で説明する代替テキストを書きます。"),
        ],
        tests=[
            t_page("見出し1「ねこ図鑑」の id が top", "(function () { var h = document.querySelector('h1'); return !!h && h.id === 'top' && h.textContent.trim() === 'ねこ図鑑'; })()"),
            t_page("外部リンクのリンク先と文字が正しい", "(function () { var a = document.querySelector('a[href=\"https://example.com/cats\"]'); return !!a && a.textContent.trim() === 'ねこの解説サイト'; })()"),
            t_page("外部リンクが新しいタブで開き、rel に noopener と noreferrer がある", "(function () { var a = document.querySelector('a[href=\"https://example.com/cats\"]'); return !!a && a.target === '_blank' && a.relList.contains('noopener') && a.relList.contains('noreferrer'); })()"),
            t_page("画像の src・alt・大きさが正しい", "(function () { var i = document.querySelector('img'); return !!i && i.getAttribute('src') === 'images/cat.jpg' && i.alt === '窓辺で寝ているねこ' && i.getAttribute('width') === '300' && i.getAttribute('height') === '200'; })()"),
            t_page("ページ内リンクが #top を指し、移動先が存在する", "(function () { var a = document.querySelector('a[href=\"#top\"]'); return !!a && a.textContent.trim() === 'ページの先頭へ' && !!document.getElementById('top'); })()", visible=False),
        ],
        why="a 要素の href・target・rel と、img 要素の src・alt・width・height を、それぞれ正しく書くから。",
        expl="リンクは href、画像は src。新しいタブで開くリンクには rel=\"noopener noreferrer\"、画像には必ず alt を付けます。ページ内リンクは、移動先の id と、# のあとの文字を合わせます。",
        concepts=["a要素", "img", "alt", "target", "rel", "ページ内リンク"], diff=3,
        hint="リンクは href、画像は src。ページ内リンクの移動先は id で決まります。",
        ok="正解！リンクと画像を使ったページが書けました。",
        ng="惜しい！条件を1つずつ見直しましょう。",
    ),
]
