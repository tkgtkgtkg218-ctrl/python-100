from lib_web import mc, pred, fill, bugfix, write_page, t_page

STAGE = {
    "number": 2,
    "title": "見出し・段落・テキスト",
    "subtitle": "文章の構造を表す要素と、ブロック・インライン",
    "goals": [
        "見出し（h1〜h6）と段落（p）で、文章の構造を表せる",
        "強調（strong / em）、改行（br）、区切り（hr）、まとまり（div / span）を使い分けられる",
        "要素の意味（セマンティクス）と見た目を区別して考えられる",
        "ブロックレベルの要素とインラインの要素の、表示の違いを説明できる",
        "< や & を文字として表示する文字参照（&lt; &amp; など）を使える",
    ],
    "prerequisites": ["HTML の基本構造・要素と属性（ステージ1）"],
    "topics": [
        "見出し h1〜h6 と、見出しの階層",
        "段落 p と、改行 br・区切り線 hr",
        "強調 strong / em（意味）と、b / i（見た目だけ）",
        "div と span（意味を持たないまとまり）",
        "ブロックとインライン",
        "文字参照（&lt; &gt; &amp;）",
    ],
    "pitfalls": [
        "文字を大きくしたいから h1 を使う（見出しは構造のために使う。大きさは CSS で変える）",
        "段落の間を空けるために <br> を並べる（段落は p 要素で分ける）",
        "p の中に見出しなどのブロック要素を入れる（p は途中で自動的に閉じられてしまう）",
        "br は空要素。</br> と書くと、改行が2つになってしまう",
        "< をそのまま書くと、タグの始まりと誤解される（&lt; と書く）",
    ],
    "next_links": ["他のページや画像へつなぐ「リンク」と「画像」を学びます（ステージ3）"],
    "lesson": {
        "intro": "文章を読みやすくするには、見出しで内容を区切り、段落で文をまとめ、大事な部分を強調します。HTML では、これらを要素で表します。大切なのは、要素を「見た目」ではなく「意味・構造」で選ぶことです。見た目は、あとで CSS で整えられます。",
        "sections": [
            {
                "id": "S02-L1",
                "title": "見出し・段落・強調",
                "read_minutes": 3,
                "body": [
                    "見出しは h1（最も大きな見出し）から h6 までの6段階です。数字は文章の階層を表します。h1 はページ全体の題名、h2 はその中の大きな節、h3 は h2 の中の小節、というように使い、h1 → h3 のように階層を飛ばすのは避けます。「文字を大きくしたいから」ではなく、「この部分が見出しだから」使います。",
                    "段落は p 要素で表します。文章のまとまりごとに p を分けます。段落の間を空けたいからといって、br を並べるのは誤りです。br は、住所や詩のように、1つの段落の中で改行したいときだけに使う空要素で、終了タグはありません。hr は、内容の区切り（話題の転換）を表す水平線です。",
                    "strong は「重要」、em は「強調（話し言葉で強く読む）」という意味を持ちます。単に太字・斜体にしたいだけの見た目の指定は CSS で行います。ブラウザの標準では、strong は太字、em は斜体で表示されます。",
                    "div と span は、意味を持たない、まとまりのための要素です。ほかに適切な意味のある要素がないときに、CSS や JavaScript の目印として使います。",
                ],
                "glossary": [
                    {"term": "セマンティクス", "definition": "要素が持つ意味。見た目ではなく、役割で要素を選ぶ考え方。"},
                    {"term": "見出し（h1〜h6）", "definition": "文章の構造を表す6段階の見出し。数字が小さいほど上の階層。"},
                    {"term": "段落（p）", "definition": "文のまとまり。"},
                ],
                "examples": [
                    {
                        "id": "S02-E1", "title": "見出しと段落と強調", "language": "html",
                        "code": '''<h1>旅の記録</h1>
<p>京都に行きました。</p>
<h2>1日目</h2>
<p>清水寺で<strong>夕日</strong>を見ました。</p>
<p>住所:<br>京都市東山区<br>清水1丁目</p>
<hr>
<p>おわり</p>''',
                        "line_notes": ["h1 がページの題名、h2 がその中の節です。", "<strong> は、内容が重要であることを表します。", "<br> は、段落の中で改行するための空要素です。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "Array.from(document.body.children).map(function (e) { return e.tagName; }).join(',') === 'H1,P,H2,P,P,HR,P' && document.querySelectorAll('p > strong').length === 1 && document.querySelectorAll('br').length === 2"},
                    },
                    {
                        "id": "S02-E2", "title": "文字参照", "language": "html",
                        "code": '''<p>&lt;p&gt; は段落を表すタグです。</p>
<p>AT&amp;T</p>''',
                        "line_notes": ["&lt; は <、&gt; は >、&amp; は & を表す文字参照です。", "そのまま < や & を書くと、タグの始まりなどと誤解されることがあります。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "document.querySelectorAll('p')[0].textContent === '<p> は段落を表すタグです。' && document.querySelectorAll('p')[1].textContent === 'AT&T'"},
                    },
                ],
            },
            {
                "id": "S02-L2",
                "title": "ブロックとインライン",
                "read_minutes": 2,
                "body": [
                    "要素は、画面での並び方によって、大きく2種類に分けられます。ブロックレベルの要素（p、h1〜h6、div など）は、前後で改行され、1つが1行（以上）を占めます。インラインの要素（span、strong、em、a など）は、文章の流れの中に並び、改行されません。",
                    "この違いは、ブラウザの標準の表示（display プロパティの初期値）です。のちに学ぶ CSS の display で、変更できます。インライン要素の中にブロック要素を入れるのは避け、ブロック要素の中にインライン要素を入れる構造を基本にします。",
                    "p 要素の中に見出し（h2 など）を入れることはできません。p の途中で見出しの開始タグがあると、ブラウザが p を自動で閉じてしまい、意図と違う構造になります。",
                ],
                "glossary": [
                    {"term": "ブロックレベル要素", "definition": "前後で改行され、1つ以上の行を占める要素（p、div、h1 など）。"},
                    {"term": "インライン要素", "definition": "文章の流れの中に並び、改行されない要素（span、strong、a など）。"},
                ],
                "examples": [
                    {
                        "id": "S02-E3", "title": "インラインとブロックの表示", "language": "html",
                        "code": '''<span>りんご</span><span>みかん</span>
<div>ぶどう</div><div>もも</div>''',
                        "line_notes": ["span は横に並びます（インライン）。", "div は1つずつ改行されて縦に並びます（ブロック）。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "(function () { var s = document.querySelectorAll('span'), d = document.querySelectorAll('div'); return s[0].getBoundingClientRect().top === s[1].getBoundingClientRect().top && d[0].getBoundingClientRect().top < d[1].getBoundingClientRect().top; })()"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "文字を大きくするために見出しを使う", "wrong_code": "<h1>お知らせ（大きい文字にしたいだけ）</h1>", "why": "見出しは構造を表すものです。大きさだけが目的なら、p に CSS（font-size）を指定します。", "fix": "<p>お知らせ</p> に CSS で大きさを指定"},
            {"title": "br で段落の間を空ける", "wrong_code": "文章1<br><br>文章2", "why": "段落の構造を表せません。段落ごとに p 要素で分け、間隔は CSS で調整します。", "fix": "<p>文章1</p><p>文章2</p>"},
            {"title": "br の終了タグを書く", "wrong_code": "<br>1行目</br>", "why": "br は空要素で終了タグはありません。</br> は、ブラウザには <br> として扱われ、改行が2つになります。", "fix": "1行目<br>2行目"},
            {"title": "p の中に見出しを入れる", "wrong_code": "<p>はじめに<h2>見出し</h2></p>", "why": "h2 の開始タグの時点で p が自動的に閉じられ、あとの </p> は余分な空の p になります。", "fix": "<p>はじめに</p>\n<h2>見出し</h2>"},
        ],
        "checkpoints": [
            "見出し h1〜h6 は構造のために使い、階層を飛ばさない",
            "段落は p。段落の間を空けるために br は使わない",
            "strong は重要、em は強調。見た目だけなら CSS",
            "div と span は意味を持たないまとまり",
            "ブロックは改行される、インラインは文章の流れに並ぶ",
            "< は &lt;、& は &amp; と書く",
        ],
        "next_bridge": "文章の構造を、要素で表せるようになりました。問題で、要素の意味や、ブラウザでの表示を確かめましょう。",
    },
}

SPAN_DIV = '''<span>りんご</span><span>みかん</span>
<div>ぶどう</div><div>もも</div>'''

QUESTIONS = [
    mc(
        title="見出しを使う理由", lang="html",
        prompt="Webページで h1〜h6 の見出し要素を使う理由として、最も適切なものはどれですか？",
        choices=[
            ("文字を大きく、太く表示するため", "見出しの文字がブラウザで大きく表示されるのは標準の見た目にすぎません。文字の大きさは CSS で自由に変えられます。見出しは構造を表すために使います。"),
            ("文章の構造（どこが題名で、どこが節か）を表すため", ""),
            ("ページのタイトルをブラウザのタブに表示するため", "タブに表示されるのは head の中の title 要素です。見出しは、本文の中の構造を表す要素です。"),
        ],
        correct=1,
        why="見出しは、文章の階層構造を表すための要素で、見た目はCSSで決めるから。",
        expl="見出しの階層は、検索エンジンや読み上げソフトが、ページの構造をつかむ手がかりにもなります。見た目のために選ぶのではなく、意味で選びます。",
        concepts=["見出し", "セマンティクス"], diff=1,
        hint="見た目は CSS が担当でした。HTML は何を表すのでしょう？",
        ok="正解！見出しは構造を表す要素です。",
        ng="惜しい！見た目ではなく、意味・構造のために使います。",
    ),
    pred(
        title="ブロックとインラインの並び", lang="html",
        prompt="次の HTML をブラウザで表示したとき、同じ行に横に並ぶのはどれですか？",
        code=SPAN_DIV,
        check={"format": "html_body", "probe": "(function () { var s = document.querySelectorAll('span'), d = document.querySelectorAll('div'); var sp = s[0].getBoundingClientRect().top === s[1].getBoundingClientRect().top; var dv = d[0].getBoundingClientRect().top === d[1].getBoundingClientRect().top; return sp && !dv ? 'span' : (dv && !sp ? 'div' : 'other'); })()"},
        choices=[
            ("div 要素の2つ（ぶどうともも）", "div はブロックレベル要素なので、前後で改行され、1つずつ別の行に並びます。", "div"),
            ("span 要素の2つ（りんごとみかん）", "", "span"),
            ("どの要素も、別々の行になる", "span はインライン要素なので、改行されず、文章の流れの中で横に並びます。", "other"),
        ],
        correct=1,
        why="span はインライン要素なので横に並び、div はブロックレベル要素なので縦に並ぶから。",
        expl="p や div などのブロックレベル要素は、前後で改行されます。span や strong などのインライン要素は、文章の流れの中に並びます。この区別は、あとで CSS でレイアウトを組むときの土台になります。",
        concepts=["ブロック要素", "インライン要素"], diff=2,
        hint="span と div は、それぞれブロックとインラインのどちらでしょう？",
        ok="正解！span はインライン、div はブロックです。",
        ng="惜しい！ブロックとインラインの表示の違いを思い出しましょう。",
    ),
    pred(
        title="< を文字として表示する", lang="html",
        prompt="次の HTML をブラウザで表示したとき、p 要素の中に表示される文字を、そのまま入力してください。",
        code='''<p>&lt;p&gt;は段落を表します</p>''',
        check={"format": "html_body", "probe": "document.querySelector('p').textContent", "expected": "<p>は段落を表します"},
        out="<p>は段落を表します",
        wrong=[("&lt;p&gt;は段落を表します", "&lt; と &gt; は文字参照です。ブラウザが < と > に置き換えて表示するので、& や ; は表示されません。"), ("は段落を表します", "&lt;p&gt; は、タグではなく、「<p>」という文字として表示されます。")],
        why="&lt; は < を、&gt; は > を表す文字参照で、ブラウザが記号に置き換えて表示するから。",
        expl="HTML の中で < や > をそのまま書くと、タグの始まり・終わりと誤解されます。文字として表示したいときは、&lt; &gt; と書きます。& 自体は &amp; です。",
        concepts=["文字参照"], diff=2,
        hint="&lt; が何を表しているか思い出しましょう。",
        ok="正解！文字参照は記号に置き換えて表示されます。",
        ng="惜しい！&lt; と &gt; が何に置き換わるか確認しましょう。",
    ),
    fill(
        title="重要な部分を表す要素", lang="html",
        prompt="文章の中の「重要」という語を、「重要である」という意味を持つ要素で囲みます。【空欄1】【空欄2】に入れる要素名を答えてください（開始タグと終了タグで同じ名前です）。",
        code='''<p>これは<__1__>重要</__2__>なお知らせです。</p>''',
        check={"format": "html_body", "expr": "document.querySelector('p > strong') !== null && document.querySelector('p > strong').textContent === '重要'"},
        blanks=[(["strong"], False), (["strong"], False)],
        wrong=[("b1", "b", "b は見た目だけ太字にする要素で、「重要」という意味は持ちません。重要性を表したいときは strong を使います。")],
        why="「重要である」という意味を表す要素は strong だから。",
        expl="strong は重要性、em は強調を表します。b と i は意味を持たず、見た目だけの指定ですが、見た目は CSS で指定するのが基本なので、まず strong と em を選びます。",
        concepts=["strong", "セマンティクス"], diff=2,
        hint="「強い」「重要な」を意味する英単語です。",
        ok="正解！strong は重要性を表します。",
        ng="惜しい！重要性を表す要素名を思い出しましょう。",
    ),
    bugfix(
        title="p の中に見出しを入れた", lang="html",
        prompt="見出し（h2）を段落の中に入れたつもりが、意図と違う構造になっています。どう直すのが適切ですか？",
        code='''<p>はじめに<h2>見出し</h2></p>''',
        fixed='''<p>はじめに</p>
<h2>見出し</h2>''',
        check={"format": "html_body", "expr": "document.querySelector('h2').parentElement.tagName === 'BODY' && document.querySelectorAll('p').length === 1"},
        choices=[
            ("h2 を strong に変える", "strong はインライン要素なので p の中に入れられますが、見出しではなくなってしまいます。構造が変わるので、直し方としては不適切です。"),
            ("p を先に閉じて、p と h2 を並べて書く", ""),
            ("</p> を </h2> に書き換える", "h2 はすでに閉じています。閉じ忘れはなく、p が自動で閉じられることが問題なので、並べて書くことが必要です。"),
        ],
        correct=1, fmt="text",
        why="p の中にはブロック要素の h2 を入れられないので、p を閉じてから h2 を並べる必要があるから。",
        expl="h2 の開始タグが現れた時点で、ブラウザは p を自動的に閉じます。その結果、あとの </p> は対応する開始タグのない余計なタグとなり、空の p 要素が作られてしまいます。",
        concepts=["ブロック要素", "p", "入れ子"], diff=3,
        hint="p の中に入れられるのは、インライン要素の方でした。",
        ok="正解！p と見出しを並べて書きます。",
        ng="惜しい！p の中には見出しを入れられません。",
    ),
    mc(
        title="段落を分ける正しい方法", lang="html",
        prompt="2つの段落の間を空けて、文章を読みやすく表示したい。HTML の書き方として最も適切なものはどれですか？",
        choices=[
            ("段落ごとに p 要素で分け、間隔は CSS で調整する", ""),
            ("段落の間に br を何個も並べる", "br は、段落の中での改行のための要素です。段落の構造を表せず、読み上げソフトなどにも正しく伝わりません。間隔は CSS で調整します。"),
            ("全角の空白を何個も並べて空ける", "空白の数で見た目を調整する方法は、画面幅や文字の大きさで崩れやすく、構造も表せません。"),
        ],
        correct=0,
        why="文章のまとまりは p 要素で表し、見た目の間隔は CSS が担当するから。",
        expl="HTML は構造、CSS は見た目、と役割を分けます。段落の間隔は、CSS の margin などで調整します（ステージ8で学びます）。",
        concepts=["p", "br", "役割の分担"], diff=2,
        hint="HTML が担当するのは構造、CSS が担当するのは見た目でした。",
        ok="正解！構造は p、間隔は CSS です。",
        ng="惜しい！段落は p 要素で表します。",
    ),
    bugfix(
        title="br の終了タグ", lang="html",
        prompt="2行に分けて表示するつもりが、改行が余分に入ってしまいます。正しく書き直して入力してください（1行目の内容をすべて入力）。",
        code='''<p>1行目<br>2行目</br></p>''',
        fixed='''<p>1行目<br>2行目</p>''',
        check={"format": "html_body", "expr": "document.querySelectorAll('br').length === 1"},
        target_line=1, accepted=["<p>1行目<br>2行目</p>", "<p>1行目<br/>2行目</p>", "<p>1行目<br />2行目</p>"],
        wrong=[("<p>1行目<br>2行目</br></p>", "元のコードのままです。br は空要素なので終了タグがありません。</br> は、ブラウザには <br> として扱われ、余分な改行が入ります。")],
        why="br は空要素で終了タグを書かないため、</br> を取り除く必要があるから。",
        expl="</br> という終了タグは存在しません。ブラウザは、これを開始タグ <br> とみなして、改行をもう1つ追加します。空要素は、<br> または <br /> のように書きます。",
        concepts=["br", "空要素"], diff=2,
        hint="br は、内容を持たない要素です。終了タグは必要でしょうか？",
        ok="正解！br に終了タグは書きません。",
        ng="惜しい！空要素の書き方を確認しましょう。",
    ),
    mc(
        title="見出しの階層", lang="html",
        prompt="ページの見出しを、h1 の次にいきなり h3 を使って書いた。この書き方について、適切なものはどれですか？",
        code='''<h1>旅の記録</h1>
<h3>1日目</h3>''',
        choices=[
            ("問題ない。h3 のほうが小さい文字で見やすいから", "文字の大きさは CSS で決められます。見出しの数字は、階層（構造）を表すものなので、見た目で選ぶのは適切ではありません。"),
            ("階層が飛んでおり、構造が分かりにくくなる。h2 を使うのが適切", ""),
            ("エラーになり、ページが表示されなくなる", "HTML は、書き方が不適切でも、ブラウザが表示しようとします。エラーにはなりませんが、構造として好ましくありません。"),
        ],
        correct=1,
        why="h1 の下の階層は h2 なので、階層を飛ばすと、文章の構造が正しく伝わらなくなるから。",
        expl="見出しは、章 → 節 → 小節のように入れ子になった構造を表します。h1 → h2 → h3 の順に使い、見た目を変えたいときは CSS を使います。",
        concepts=["見出しの階層"], diff=2,
        hint="見出しの数字は、何を表しているでしょう？",
        ok="正解！見出しの階層を飛ばしません。",
        ng="惜しい！見出しの数字は階層を表します。",
    ),
    pred(
        title="最も大きい見出しはどれか", lang="html",
        prompt="次の HTML をブラウザの標準の表示で見たとき、文字が最も大きく表示される見出しはどれですか？",
        code='''<h3>C</h3>
<h1>A</h1>
<h2>B</h2>''',
        check={"format": "html_body", "probe": "(function () { var hs = ['h1', 'h2', 'h3'].map(function (t) { return parseFloat(getComputedStyle(document.querySelector(t)).fontSize); }); return ['h1', 'h2', 'h3'][hs.indexOf(Math.max.apply(null, hs))]; })()"},
        choices=[
            ("h3（C）", "書かれた順ではなく、番号で大きさが決まります。標準の表示では、数字が小さいほど大きく表示されます。", "h3"),
            ("h1（A）", "", "h1"),
            ("h2（B）", "h2 は h1 の次に大きく、最も大きいのは h1 です。", "h2"),
        ],
        correct=1,
        why="標準の表示では、h1 が最も大きく、h6 に向かって小さくなるから。",
        expl="ブラウザの標準のスタイルでは、h1 が最も大きく、h6 が最も小さく表示されます。ただし、これは見た目の標準にすぎず、CSS で変更できます。",
        concepts=["見出し", "ブラウザの標準スタイル"], diff=1,
        hint="書かれている順番ではなく、見出しの数字に注目しましょう。",
        ok="正解！標準では h1 が最も大きく表示されます。",
        ng="惜しい！見出しの数字と大きさの関係を確認しましょう。",
    ),
    write_page(
        title="見出しと段落でページを書く", lang="html", fmt="html_body",
        prompt="次の内容を、適切な要素で書いてください（body の中身だけを書きます）。\n・見出し1「旅の記録」\n・段落「京都に行きました。」\n・見出し2「1日目」\n・段落「清水寺で夕日を見ました。」（「夕日」だけを strong で囲む）\n・見出し2「2日目」\n・段落「奈良で鹿に会いました。」",
        starter="<!-- ここに書きましょう -->\n",
        ref='''<h1>旅の記録</h1>
<p>京都に行きました。</p>
<h2>1日目</h2>
<p>清水寺で<strong>夕日</strong>を見ました。</p>
<h2>2日目</h2>
<p>奈良で鹿に会いました。</p>''',
        alts=['''<h1>旅の記録</h1><p>京都に行きました。</p><h2>1日目</h2><p>清水寺で<strong>夕日</strong>を見ました。</p><h2>2日目</h2><p>奈良で鹿に会いました。</p>'''],
        bads=[
            ('''<h1>旅の記録</h1>
<p>京都に行きました。</p>
<h2>1日目</h2>
<p>清水寺で夕日を見ました。</p>
<h2>2日目</h2>
<p>奈良で鹿に会いました。</p>''', "「夕日」が strong で囲まれていません。重要な語を strong で囲みます。"),
            ('''<h1>旅の記録</h1>
京都に行きました。<br><br>
<h2>1日目</h2>
清水寺で<strong>夕日</strong>を見ました。<br><br>
<h2>2日目</h2>
奈良で鹿に会いました。''', "段落を p 要素で書いていません。文章のまとまりは p で表し、br で間を空けないようにします。"),
        ],
        tests=[
            t_page("body の直下の要素の並びが、h1・p・h2・p・h2・p になっている", "Array.from(document.body.children).map(function (e) { return e.tagName; }).join(',') === 'H1,P,H2,P,H2,P'"),
            t_page("見出しの文字が正しい（h1「旅の記録」、h2「1日目」「2日目」）", "document.querySelector('h1').textContent.trim() === '旅の記録' && Array.from(document.querySelectorAll('h2')).map(function (h) { return h.textContent.trim(); }).join('|') === '1日目|2日目'"),
            t_page("2つ目の段落に、strong で囲んだ「夕日」がある", "(function () { var s = document.querySelectorAll('p > strong'); return s.length === 1 && s[0].textContent === '夕日' && s[0].parentElement.textContent.indexOf('清水寺') >= 0; })()"),
            t_page("段落の文章が正しい", "Array.from(document.querySelectorAll('p')).map(function (p) { return p.textContent.trim(); }).join('|') === '京都に行きました。|清水寺で夕日を見ました。|奈良で鹿に会いました。'", visible=False),
            t_page("br を使わずに段落を分けている", "document.querySelectorAll('br').length === 0", visible=False),
        ],
        why="見出しと段落を意味に合わせて使い分け、重要な語を strong で囲むから。",
        expl="h1 → h2 → h2 の階層で見出しを書き、文章のまとまりを p で書きます。strong は、強調したい語だけを囲みます（p の中のインライン要素）。段落の間を br で空けないことも大切です。",
        concepts=["見出し", "p", "strong", "文書の構造"], diff=2,
        hint="h1、p、h2、p、h2、p の順に並べます。strong は p の中に入れます。",
        ok="正解！文章の構造を要素で表せました。",
        ng="惜しい！要素の並びと、strong の位置を確認しましょう。",
    ),
]
