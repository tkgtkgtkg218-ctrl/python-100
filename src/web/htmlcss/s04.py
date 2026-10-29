from lib_web import mc, pred, fill, bugfix, write_page, t_page

STAGE = {
    "number": 4,
    "title": "リストとページ構造",
    "subtitle": "ul / ol / li、header・nav・main・footer などの構造を表す要素",
    "goals": [
        "ul・ol・li で、順序のないリスト・順序のあるリストを書き分けられる",
        "リストを入れ子にする正しい書き方を説明できる",
        "header・nav・main・section・article・footer などで、ページの構造を表せる",
        "div と、意味を持つ構造の要素を使い分けられる",
        "ナビゲーションを「リンクのリスト」として書ける",
    ],
    "prerequisites": ["HTML の基本構造（ステージ1）", "文章の要素（ステージ2）", "リンク（ステージ3）"],
    "topics": [
        "ul（順序なし）と ol（順序あり）、li",
        "リストの入れ子",
        "ol の start 属性",
        "header / nav / main / footer",
        "section / article / aside",
        "div との使い分け",
    ],
    "pitfalls": [
        "li は、必ず ul・ol の直接の子にする（li だけを body に置かない）",
        "リストの入れ子は、ul の中に直接 ul ではなく、li の中に ul を入れる",
        "li の終了タグ </li> の書き忘れ（次の li で自動的に閉じられるが、意図しない構造になりやすい）",
        "main はページに1つ。何でも div で書かず、意味のある要素を選ぶ",
        "リストは「見た目の点」のためではなく、「項目が並んでいる」という構造のために使う",
    ],
    "next_links": ["ユーザーが入力するための「フォーム」を学びます（ステージ5）"],
    "lesson": {
        "intro": "項目を並べるときに使うのがリスト、ページの「頭・メニュー・本文・足」を表すときに使うのが、header・nav・main・footer などの構造の要素です。要素の意味を正しく選ぶと、人にも、検索エンジンや読み上げソフトにも、ページの構造が伝わります。",
        "sections": [
            {
                "id": "S04-L1",
                "title": "リスト（ul / ol / li）",
                "read_minutes": 3,
                "body": [
                    "順序に意味のない項目の並び（買い物リスト、メニューなど）は ul（unordered list）、順序に意味のある並び（手順、ランキングなど）は ol（ordered list）で表します。どちらも、項目1つずつを li（list item）要素で書き、li は ul・ol の直接の子にします。",
                    "標準の表示では、ul の項目には黒い丸（●）、ol には 1. 2. 3. の番号が付きます。この見た目は CSS で変えられます。ol には start=\"3\" のように、始まりの番号を指定する属性もあります。",
                    "リストを入れ子にするときは、li の中に、別の ul（または ol）を入れます。ul の中に、直接 ul を書くのは誤りです。",
                ],
                "glossary": [
                    {"term": "ul", "definition": "順序のないリスト（unordered list）。"},
                    {"term": "ol", "definition": "順序のあるリスト（ordered list）。"},
                    {"term": "li", "definition": "リストの項目（list item）。ul・ol の直接の子にする。"},
                ],
                "examples": [
                    {
                        "id": "S04-E1", "title": "ul と ol", "language": "html",
                        "code": '''<ul>
  <li>りんご</li>
  <li>みかん</li>
</ul>
<ol start="3">
  <li>卵を割る</li>
  <li>かき混ぜる</li>
</ol>''',
                        "line_notes": ["ul の項目には、標準では黒い丸が付きます。", "ol の項目には、標準では番号が付きます。start=\"3\" で、3から始まります。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "getComputedStyle(document.querySelector('ul > li')).listStyleType === 'disc' && getComputedStyle(document.querySelector('ol > li')).listStyleType === 'decimal' && document.querySelector('ol').start === 3"},
                    },
                    {
                        "id": "S04-E2", "title": "リストの入れ子", "language": "html",
                        "code": '''<ul>
  <li>果物
    <ul>
      <li>りんご</li>
      <li>みかん</li>
    </ul>
  </li>
  <li>野菜</li>
</ul>''',
                        "line_notes": ["「果物」の li の中に、さらに ul を入れています。", "入れ子の ul は、li の直接の子ではなく、li の内容の一部です。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "document.querySelectorAll('li').length === 4 && document.querySelectorAll('body > ul > li').length === 2 && document.querySelector('ul > li > ul > li').textContent === 'りんご'"},
                    },
                ],
            },
            {
                "id": "S04-L2",
                "title": "ページの構造を表す要素",
                "read_minutes": 3,
                "body": [
                    "ページの大まかな構造は、意味を持つ要素で表せます。header はページ（や記事）の頭の部分（ロゴや題名）、nav はメニューなどのナビゲーション、main はそのページの主要な内容（1ページに1つ）、footer は足の部分（著作権表示など）です。",
                    "section は内容のひとまとまり（章や節）、article は単独で成り立つ記事・投稿、aside は補足的な内容（関連リンクなど）です。どれにも当てはまらず、デザインのためだけに囲みたいとき、意味を持たない div を使います。",
                    "nav の中のメニューは、リンク（a）の並びなので、ul と li で書くのが一般的です。header や footer は、ページ全体にも、section や article の中にも使えます。",
                ],
                "glossary": [
                    {"term": "header / footer", "definition": "ページ（や節）の頭・足の部分を表す要素。"},
                    {"term": "nav", "definition": "ナビゲーション（メニュー）を表す要素。"},
                    {"term": "main", "definition": "そのページの主要な内容を表す要素。1ページに1つ。"},
                ],
                "examples": [
                    {
                        "id": "S04-E3", "title": "ページの骨組み", "language": "html",
                        "code": '''<header>
  <h1>ぼくのサイト</h1>
  <nav>
    <ul>
      <li><a href="index.html">ホーム</a></li>
      <li><a href="about.html">概要</a></li>
    </ul>
  </nav>
</header>
<main>
  <article>
    <h2>はじめまして</h2>
    <p>ようこそ。</p>
  </article>
</main>
<footer>
  <p>© 2026 ぼくのサイト</p>
</footer>''',
                        "line_notes": ["header の中に、題名とメニュー（nav）を入れています。", "main の中に、主要な内容の記事（article）を入れています。", "footer に、著作権表示を入れています。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "Array.from(document.body.children).map(function (e) { return e.tagName; }).join(',') === 'HEADER,MAIN,FOOTER' && document.querySelectorAll('nav li > a').length === 2 && document.querySelectorAll('main > article > h2').length === 1"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "li を直接 body に置く", "wrong_code": "<li>りんご</li>\n<li>みかん</li>", "why": "li は ul か ol の直接の子にします。そうでない li は、リストとして扱われません。", "fix": "<ul>\n  <li>りんご</li>\n  <li>みかん</li>\n</ul>"},
            {"title": "ul の中に直接 ul を入れる", "wrong_code": "<ul>\n  <li>果物</li>\n  <ul><li>りんご</li></ul>\n</ul>", "why": "入れ子のリストは、li の中に入れます。ul の直接の子は li だけです。", "fix": "<li>果物\n  <ul><li>りんご</li></ul>\n</li>"},
            {"title": "終了タグ </li> の書き間違い", "wrong_code": "<li>りんご<li>", "why": "</li> のつもりで <li> と書くと、新しい項目が始まり、空の li ができます。", "fix": "<li>りんご</li>"},
            {"title": "何でも div で書く", "wrong_code": "<div class=\"header\">…</div>", "why": "意味のある要素（header・nav・main・footer）があるなら、そちらを使うと、構造が伝わります。", "fix": "<header>…</header>"},
        ],
        "checkpoints": [
            "順序なしは ul、順序ありは ol。項目は li",
            "li は ul・ol の直接の子",
            "リストの入れ子は、li の中に ul・ol を入れる",
            "header・nav・main・footer でページの構造を表す",
            "section・article・aside は内容のまとまり",
            "意味のある要素がないときだけ div",
        ],
        "next_bridge": "ページの骨組みが、意味のある要素で書けるようになりました。問題で、リストと構造の書き方を確かめましょう。",
    },
}

UL_OL = '''<ul>
  <li>りんご</li>
</ul>
<ol>
  <li>卵を割る</li>
</ol>'''

QUESTIONS = [
    mc(
        title="ul と ol の使い分け", lang="html",
        prompt="料理の「手順（1. 卵を割る、2. かき混ぜる、…）」を HTML で表すとき、最も適切な要素はどれですか？",
        choices=[
            ("ul と li", "ul は、順序に意味のないリストです。手順のように、順序に意味がある場合は ol を使います。"),
            ("ol と li", ""),
            ("p を並べて、手で番号を書く", "番号を手で書くと、項目を足したときに番号を付け直す必要があります。順序のあるリストなら、ol がその番号を自動で付けます。"),
        ],
        correct=1,
        why="順序に意味のある項目の並びは、ol で表すから。",
        expl="買い物リストのように順序に意味がないなら ul、手順やランキングのように順序に意味があるなら ol を選びます。見た目（丸か番号か）は CSS でも変えられるので、意味で選びます。",
        concepts=["ol", "ul", "li"], diff=1,
        hint="手順は、順番が大事です。",
        ok="正解！順序があるなら ol です。",
        ng="惜しい！順序に意味があるかで選びます。",
    ),
    pred(
        title="リストの標準の記号", lang="html",
        prompt="次の HTML をブラウザの標準の表示で見たとき、項目の先頭にどんな記号が付きますか？（list-style-type の値）",
        code=UL_OL,
        check={"format": "html_body", "probe": "getComputedStyle(document.querySelector('ul > li')).listStyleType + ',' + getComputedStyle(document.querySelector('ol > li')).listStyleType"},
        choices=[
            ("ul は番号（1.）、ol は黒い丸（●）", "反対です。順序のない ul に黒い丸、順序のある ol に番号が付きます。", "decimal,disc"),
            ("ul は黒い丸（●）、ol は番号（1.）", "", "disc,decimal"),
            ("どちらにも記号は付かない", "li の先頭に付く記号は、ブラウザの標準のスタイルで決まります。標準では、ul に丸、ol に番号が付きます。", "none,none"),
        ],
        correct=1,
        why="標準のスタイルでは、ul の項目には黒い丸、ol の項目には番号が付くから。",
        expl="この記号は、CSS の list-style-type で変えられます（例: none で記号なし）。意味（順序の有無）は変わらないので、見た目だけ変えたいときも、ul と ol を意味で選びます。",
        concepts=["ul", "ol", "標準スタイル"], diff=1,
        hint="順序のない ul と、順序のある ol で、記号が違います。",
        ok="正解！ul は丸、ol は番号です。",
        ng="惜しい！ul と ol の標準の記号を確認しましょう。",
    ),
    fill(
        title="番号の開始位置", lang="html",
        prompt="ol の番号を 3 から始めます。【空欄1】に入れる属性名を答えてください。",
        code='''<ol __1__="3">
  <li>卵を割る</li>
  <li>かき混ぜる</li>
</ol>''',
        check={"format": "html_body", "expr": "document.querySelector('ol').start === 3"},
        blanks=[(["start"], False)],
        wrong=[("b1", "begin", "begin という属性はありません。ol の番号の開始位置は、start 属性で指定します。")],
        why="ol の番号の開始位置は、start 属性で指定するから。",
        expl="start=\"3\" とすると、最初の項目が 3. になります。リストが前のページから続いているときなどに使います。",
        concepts=["ol", "start属性"], diff=2,
        hint="「開始」を意味する英単語です。",
        ok="正解！start 属性で開始番号を指定します。",
        ng="惜しい！「始める」を意味する属性名です。",
    ),
    bugfix(
        title="リストの外に出た li", lang="html",
        prompt="2つの項目を、リストとして書いたつもりが、li がリストの中に入っていません。正しい直し方はどれですか？",
        code='''<li>りんご</li>
<li>みかん</li>''',
        fixed='''<ul>
  <li>りんご</li>
  <li>みかん</li>
</ul>''',
        check={"format": "html_body", "expr": "document.querySelectorAll('li').length === 2 && Array.from(document.querySelectorAll('li')).every(function (l) { return l.parentElement.tagName === 'UL'; })"},
        choices=[
            ("li を p に変える", "p に変えると、リストの項目ではなく、段落になります。項目が並んでいるという構造が失われます。"),
            ("2つの li を、ul で囲む", ""),
            ("li を div で囲む", "li の親は、ul か ol でなければなりません。div で囲んでも、リストにはなりません。"),
        ],
        correct=1, fmt="text",
        why="li は、ul（または ol）の直接の子でなければならないから。",
        expl="li は、リストの項目を表す要素で、単独では使えません。順序のないリストなら ul、順序のあるリストなら ol で囲みます。",
        concepts=["li", "ul"], diff=2,
        hint="li の親になれる要素は何でしょう？",
        ok="正解！li は ul か ol の中に入れます。",
        ng="惜しい！li を囲む要素を考えましょう。",
    ),
    mc(
        title="入れ子のリストの書き方", lang="html",
        prompt="「果物」の項目の中に、「りんご」を入れ子にしたリストを書くとき、正しい書き方はどれですか？",
        fmt="code",
        choices=[
            ('<ul>\n  <li>果物</li>\n  <ul><li>りんご</li></ul>\n</ul>', "ul の直接の子には、ul を置けません。ul の直接の子は li だけです。入れ子のリストは、li の中に入れます。"),
            ('<ul>\n  <li>果物\n    <ul><li>りんご</li></ul>\n  </li>\n</ul>', ""),
            ('<ul>\n  <li>果物</li>\n  <li><li>りんご</li></li>\n</ul>', "li の中に li を直接入れることはできません。li の項目は、ul や ol の直接の子にします。"),
        ],
        correct=1,
        why="入れ子のリストは、親の li の内容の一部として、li の中に書くから。",
        expl="「果物」という項目の下位に「りんご」がある、という構造なので、「果物」の li の中に ul を入れます。ul の直下に ul を置く書き方は、HTML の規則に反します。",
        concepts=["リストの入れ子"], diff=3,
        hint="入れ子の ul は、どの要素の中に入りますか？",
        ok="正解！入れ子のリストは li の中に書きます。",
        ng="惜しい！ul の直接の子になれるのは li だけです。",
    ),
    pred(
        title="入れ子のリストの li の数", lang="html",
        prompt="次の HTML には、li 要素が全部でいくつありますか？数字で入力してください。",
        code='''<ul>
  <li>A
    <ul>
      <li>B</li>
      <li>C</li>
    </ul>
  </li>
  <li>D</li>
</ul>''',
        check={"format": "html_body", "probe": "document.querySelectorAll('li').length", "expected": 4},
        out="4",
        wrong=[("2", "外側の ul の li は2つ（A と D）ですが、入れ子の ul の中にも li（B と C）があります。すべて数えます。"), ("3", "入れ子のリストの中にも、li が2つあります。A・B・C・D の4つです。")],
        why="外側の li が A と D の2つ、入れ子の中の li が B と C の2つで、合わせて4つだから。",
        expl="入れ子のリストの中の li も、それぞれが1つの項目です。ul の外側と内側で、合計の数は変わりません。",
        concepts=["リストの入れ子", "li"], diff=2,
        hint="A・B・C・D と、4つの項目があります。",
        ok="正解！入れ子の中の li も数えます。",
        ng="惜しい！入れ子の中にある li も数えましょう。",
    ),
    fill(
        title="ナビゲーションを表す要素", lang="html",
        prompt="サイトのメニュー（リンクの並び）を、ナビゲーションを表す要素で囲みます。【空欄1】【空欄2】に入れる要素名を答えてください（開始タグと終了タグで同じ名前です）。",
        code='''<__1__>
  <a href="index.html">ホーム</a>
  <a href="about.html">概要</a>
</__2__>''',
        check={"format": "html_body", "expr": "document.querySelectorAll('nav > a').length === 2"},
        blanks=[(["nav"], False), (["nav"], False)],
        wrong=[("b1", "menu", "menu という要素は、ナビゲーションを表すものとしては使えません。ナビゲーションには nav を使います。")],
        why="ナビゲーションを表す要素は nav だから。",
        expl="nav は navigation の略です。メニューのように、他のページや同じページ内の主要な場所へ移動するためのリンクのまとまりに使います。",
        concepts=["nav"], diff=1,
        hint="navigation の略です。",
        ok="正解！nav はナビゲーションです。",
        ng="惜しい！navigation の略を考えましょう。",
    ),
    bugfix(
        title="閉じ忘れた li", lang="html",
        prompt="2つの項目のリストのはずが、空の項目が増えてしまい、li が3つになっています。2行目を正しく書き直して入力してください（2行目の内容をすべて入力）。",
        code='''<ul>
  <li>りんご<li>
  <li>みかん</li>
</ul>''',
        fixed='''<ul>
  <li>りんご</li>
  <li>みかん</li>
</ul>''',
        check={"format": "html_body", "expr": "document.querySelectorAll('li').length === 2"},
        target_line=2, accepted=["<li>りんご</li>"],
        wrong=[("<li>りんご<li>", "元のコードのままです。終了タグには / が必要です。/ がないと、新しい li の開始になり、空の項目ができます。")],
        why="終了タグには / が必要で、/ を忘れると新しい li が始まってしまうから。",
        expl="<li> を2つ続けて書くと、2つ目の <li> は新しい項目の開始になります。そのため、空の li が1つ増えます。終了タグ </li> を書きます。",
        concepts=["li", "終了タグ"], diff=2,
        hint="終了タグと開始タグの違いは、何でしたか？",
        ok="正解！終了タグには / を付けます。",
        ng="惜しい！終了タグの書き方を確認しましょう。",
    ),
    mc(
        title="main 要素の役割", lang="html",
        prompt="main 要素の説明として、正しいものはどれですか？",
        choices=[
            ("そのページの主要な内容を表す要素で、1ページに1つだけ使う", ""),
            ("ページの先頭に必ず置く、ロゴやメニューを表す要素である", "ページの頭の部分は header、メニューは nav です。main は、ロゴやメニューを除いた、ページの主要な内容を囲みます。"),
            ("内容を持たない、デザイン用の区切りの要素である", "意味を持たない、デザイン用の区切りは div です。main は、「ここが主要な内容」という意味を持つ要素です。"),
        ],
        correct=0,
        why="main は、そのページの中心となる内容を表し、1ページに1つだけ使うから。",
        expl="ヘッダーやフッター、サイドバーなどの共通部分は、main の外に置きます。読み上げソフトの利用者が、「本文へ移動」という操作で、main に直接移れる利点もあります。",
        concepts=["main", "セマンティクス"], diff=2,
        hint="「主要な」を意味する英単語です。",
        ok="正解！main は主要な内容を表します。",
        ng="惜しい！header・nav・div との違いを確認しましょう。",
    ),
    write_page(
        title="構造の要素でページを組み立てる", lang="html", fmt="html_body",
        prompt="次の構造のページを、適切な要素で書いてください（body の中身だけを書きます）。\n・header の中に、見出し1「ぼくのサイト」と、nav（その中に ul・li・a で、「ホーム」→ index.html、「概要」→ about.html、「連絡先」→ contact.html のメニュー）\n・main の中に、article（その中に見出し2「はじめまして」と、段落「ようこそ。」）\n・footer の中に、段落「© 2026 ぼくのサイト」",
        starter="<!-- ここに書きましょう -->\n",
        ref='''<header>
  <h1>ぼくのサイト</h1>
  <nav>
    <ul>
      <li><a href="index.html">ホーム</a></li>
      <li><a href="about.html">概要</a></li>
      <li><a href="contact.html">連絡先</a></li>
    </ul>
  </nav>
</header>
<main>
  <article>
    <h2>はじめまして</h2>
    <p>ようこそ。</p>
  </article>
</main>
<footer>
  <p>© 2026 ぼくのサイト</p>
</footer>''',
        alts=['''<header><h1>ぼくのサイト</h1><nav><ul><li><a href="index.html">ホーム</a></li><li><a href="about.html">概要</a></li><li><a href="contact.html">連絡先</a></li></ul></nav></header>
<main><article><h2>はじめまして</h2><p>ようこそ。</p></article></main>
<footer><p>© 2026 ぼくのサイト</p></footer>'''],
        bads=[
            ('''<div class="header">
  <h1>ぼくのサイト</h1>
  <div class="nav">
    <a href="index.html">ホーム</a>
    <a href="about.html">概要</a>
    <a href="contact.html">連絡先</a>
  </div>
</div>
<div class="main">
  <h2>はじめまして</h2>
  <p>ようこそ。</p>
</div>
<div class="footer"><p>© 2026 ぼくのサイト</p></div>''', "div だけで書かれていて、header・nav・main・footer などの意味を持つ要素を使っていません。"),
            ('''<header>
  <h1>ぼくのサイト</h1>
  <nav>
    <li><a href="index.html">ホーム</a></li>
    <li><a href="about.html">概要</a></li>
    <li><a href="contact.html">連絡先</a></li>
  </nav>
</header>
<main>
  <article><h2>はじめまして</h2><p>ようこそ。</p></article>
</main>
<footer><p>© 2026 ぼくのサイト</p></footer>''', "li が ul で囲まれていません。メニューは、ul と li の中にリンクを入れて書きます。"),
        ],
        tests=[
            t_page("body の直下が、header・main・footer の順になっている", "Array.from(document.body.children).map(function (e) { return e.tagName; }).join(',') === 'HEADER,MAIN,FOOTER'"),
            t_page("header の中に、見出し1「ぼくのサイト」と nav がある", "(function () { var h = document.querySelector('header > h1'); return !!h && h.textContent.trim() === 'ぼくのサイト' && !!document.querySelector('header > nav'); })()"),
            t_page("nav の中に ul があり、3つの li に、正しいリンクが入っている", "(function () { var a = document.querySelectorAll('nav > ul > li > a'); return a.length === 3 && a[0].getAttribute('href') === 'index.html' && a[1].getAttribute('href') === 'about.html' && a[2].getAttribute('href') === 'contact.html' && a[0].textContent.trim() === 'ホーム' && a[1].textContent.trim() === '概要' && a[2].textContent.trim() === '連絡先'; })()"),
            t_page("main の中に article があり、見出し2と段落がある", "(function () { var a = document.querySelector('main > article'); return !!a && a.querySelector('h2').textContent.trim() === 'はじめまして' && a.querySelector('p').textContent.trim() === 'ようこそ。'; })()"),
            t_page("footer の中に段落がある", "(function () { var p = document.querySelector('footer > p'); return !!p && p.textContent.trim() === '© 2026 ぼくのサイト'; })()"),
            t_page("main はページに1つだけ", "document.querySelectorAll('main').length === 1", visible=False),
        ],
        why="header・nav・main・article・footer と、リスト（ul・li）を意味に合わせて使って、ページの構造を表すから。",
        expl="ページの頭を header、メニューを nav、主要な内容を main、足を footer で表します。メニューは、リンクが並んでいるので ul と li で書くのが一般的です。ここで作った骨組みに、CSS で見た目を付けていきます。",
        concepts=["header", "nav", "main", "footer", "ul", "li", "article"], diff=3,
        hint="header → main → footer の順。メニューは ul・li・a の入れ子です。",
        ok="正解！意味のある要素でページの骨組みが書けました。",
        ng="惜しい！要素の入れ子と、リンクの内容を確認しましょう。",
    ),
]
