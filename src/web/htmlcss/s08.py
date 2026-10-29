from lib_web import mc, pred, fill, bugfix, write_page, t_page

BOX_HTML = '<div class="box">箱</div>'
BOX_CSS = '''.box {
  width: 200px;
  padding: 20px;
  border: 5px solid black;
  margin: 10px;
}'''

STAGE = {
    "number": 8,
    "title": "ボックスモデル",
    "subtitle": "content・padding・border・margin と、box-sizing・display",
    "goals": [
        "すべての要素が「箱（ボックス）」で、内容・padding・border・margin の4層でできていることを説明できる",
        "width・height が、box-sizing によって、どこまでの大きさを指すかを説明できる",
        "padding・margin の1〜4つの値の書き方（上右下左）を使える",
        "margin: 0 auto で、ブロック要素を水平方向に中央へ置ける",
        "border・border-radius・background-color で、箱の見た目を整えられる",
        "display の block・inline・inline-block・none の違いを説明できる",
    ],
    "prerequisites": ["CSS の基本（ステージ6）", "文字と色の装飾・単位（ステージ7）", "ブロックとインライン（ステージ2）"],
    "topics": [
        "ボックスモデル（content / padding / border / margin）",
        "width と height、box-sizing（content-box / border-box）",
        "padding・margin の書き方と省略記法",
        "border と border-radius",
        "margin: 0 auto による中央寄せ",
        "上下の margin の相殺（重なり）",
        "display（block / inline / inline-block / none）",
    ],
    "pitfalls": [
        "width は、標準では内容（content）の幅だけ。padding と border を足した分だけ、実際の幅は大きくなる",
        "インライン要素（span など）には、width・height・上下の margin が効かない",
        "margin: 0 auto の中央寄せには、width の指定が必要",
        "上下に隣り合う margin は、足し算ではなく、大きいほうの値に重なる（相殺）",
        "border は、太さ・線の種類・色の3つを書く（線の種類を忘れると表示されない）",
    ],
    "next_links": ["箱を横に並べたり、中央に寄せたりする「Flexbox」を学びます（ステージ9）"],
    "lesson": {
        "intro": "ブラウザは、HTML のすべての要素を、四角い箱として配置します。余白・枠線・大きさを自由に決められるのは、この「ボックスモデル」の仕組みがあるからです。レイアウトの基本中の基本なので、箱の4層の構造を、しっかり押さえましょう。",
        "sections": [
            {
                "id": "S08-L1",
                "title": "ボックスモデルと大きさ",
                "read_minutes": 3,
                "body": [
                    "1つの要素の箱は、内側から順に、内容（content）、内側の余白（padding）、枠線（border）、外側の余白（margin）の4層でできています。padding は背景色が広がる範囲の内側、margin は背景色が付かない、他の要素との間の距離です。",
                    "width と height は、標準（box-sizing: content-box）では、内容（content）の大きさです。width: 200px、padding: 20px、border: 5px のとき、箱の見た目の幅は、200 + 20×2 + 5×2 = 250px になります。box-sizing: border-box を指定すると、width が、padding と border を含めた幅になり、見た目の幅が、width のとおり 200px になります。レイアウトの計算が楽になるため、実際の制作では、全体に border-box を指定することが多くあります。",
                    "padding と margin は、値の数で意味が変わります。1つ（10px）は4辺すべて、2つ（10px 20px）は上下と左右、3つは上・左右・下、4つ（10px 20px 30px 40px）は上・右・下・左の順（時計回り）です。border は、太さ・線の種類・色を、border: 2px solid red; のようにまとめて書きます。線の種類（solid など）を忘れると、枠線は表示されません。",
                ],
                "glossary": [
                    {"term": "padding", "definition": "枠線の内側の余白。背景色が付く。"},
                    {"term": "border", "definition": "要素を囲む枠線。"},
                    {"term": "margin", "definition": "枠線の外側の余白。他の要素との距離。背景色は付かない。"},
                    {"term": "box-sizing", "definition": "width・height が、どの範囲の大きさを指すかを決めるプロパティ。"},
                ],
                "examples": [
                    {
                        "id": "S08-E1", "title": "content-box と border-box", "language": "css",
                        "context_html": '<div class="a">A</div>\n<div class="b">B</div>',
                        "code": '''.a, .b {
  width: 200px;
  padding: 20px;
  border: 5px solid black;
}
.b {
  box-sizing: border-box;
}''',
                        "line_notes": ["A は標準（content-box）なので、見た目の幅は 200 + 40 + 10 = 250px になります。", "B は border-box なので、padding と border を含めて、見た目の幅が 200px になります。"],
                        "preview": {"format": "css", "given_html": '<div class="a">A</div>\n<div class="b">B</div>'},
                        "verify": {"format": "css", "given_html": '<div class="a">A</div>\n<div class="b">B</div>', "expr": "document.querySelector('.a').offsetWidth === 250 && document.querySelector('.b').offsetWidth === 200"},
                    },
                    {
                        "id": "S08-E2", "title": "余白の省略記法", "language": "css",
                        "context_html": '<div class="box">箱</div>',
                        "code": '''.box {
  padding: 10px 20px 30px 40px;
  margin: 5px 15px;
}''',
                        "line_notes": ["padding の4つの値は、上・右・下・左の順です。", "margin の2つの値は、上下（5px）と、左右（15px）です。"],
                        "preview": {"format": "css", "given_html": '<div class="box">箱</div>'},
                        "verify": {"format": "css", "given_html": '<div class="box">箱</div>', "expr": "(function () { var s = getComputedStyle(document.querySelector('.box')); return s.paddingTop === '10px' && s.paddingRight === '20px' && s.paddingBottom === '30px' && s.paddingLeft === '40px' && s.marginTop === '5px' && s.marginLeft === '15px'; })()"},
                    },
                ],
            },
            {
                "id": "S08-L2",
                "title": "中央寄せ・margin の重なり・display",
                "read_minutes": 3,
                "body": [
                    "ブロック要素を水平方向の中央に置くには、width を指定して、margin: 0 auto; と書きます。左右の margin が auto だと、余った幅が左右に等しく分けられます。width を指定しないと、ブロック要素は親の幅いっぱいに広がるため、中央に寄っているように見えません。",
                    "上下に隣り合う要素の margin は、足されず、大きいほうの値に重なります（相殺）。例えば、上の要素の下の margin が 20px、下の要素の上の margin が 20px なら、間隔は 40px ではなく 20px です。",
                    "display は、要素の表示の仕方を決めます。block は前後で改行され、width・height が効きます。inline は文章の流れに並び、width・height・上下の margin が効きません。inline-block は、文章の流れに並びつつ、width・height が効きます。none は、要素を表示せず、場所も取りません。",
                    "border-radius で角を丸くできます（例: border-radius: 8px;）。background-color は、padding の範囲まで広がります。",
                ],
                "glossary": [
                    {"term": "margin の相殺", "definition": "上下に隣り合う margin が足されず、大きいほうの値に重なること。"},
                    {"term": "display", "definition": "要素の表示の仕方（block・inline・inline-block・none など）。"},
                ],
                "examples": [
                    {
                        "id": "S08-E3", "title": "中央寄せと角丸", "language": "css",
                        "context_html": '<div class="card">カード</div>',
                        "code": '''.card {
  width: 300px;
  margin: 0 auto;
  padding: 16px;
  border: 1px solid gray;
  border-radius: 8px;
  background-color: lightyellow;
}''',
                        "line_notes": ["width を指定して、margin: 0 auto で中央に寄せています。", "background-color は、padding の範囲まで広がります。"],
                        "preview": {"format": "css", "given_html": '<div class="card">カード</div>'},
                        "verify": {"format": "css", "given_html": '<div class="card">カード</div>', "expr": "(function () { var e = document.querySelector('.card'); var r = e.getBoundingClientRect(); return Math.abs(r.left + r.width / 2 - document.documentElement.clientWidth / 2) < 1 && getComputedStyle(e).borderTopLeftRadius === '8px'; })()"},
                    },
                    {
                        "id": "S08-E4", "title": "display の違い", "language": "css",
                        "context_html": '<span class="a">A</span><span class="b">B</span><span class="c">C</span>',
                        "code": '''span {
  width: 100px;
  height: 30px;
}
.b {
  display: inline-block;
}
.c {
  display: none;
}''',
                        "line_notes": ["A は、インラインなので、width と height が効きません。", "B は、inline-block なので、幅 100px が効きます。", "C は、display: none なので、表示されず、場所も取りません。"],
                        "preview": {"format": "css", "given_html": '<span class="a">A</span><span class="b">B</span><span class="c">C</span>'},
                        "verify": {"format": "css", "given_html": '<span class="a">A</span><span class="b">B</span><span class="c">C</span>', "expr": "document.querySelector('.a').offsetWidth < 100 && document.querySelector('.b').offsetWidth === 100 && document.querySelector('.c').offsetWidth === 0"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "width だけで見た目の幅が決まると思う", "wrong_code": "width: 200px; padding: 20px; border: 5px solid;  /* 見た目は 200px のつもり */", "why": "標準では、padding と border が width の外側に足されます。見た目は 250px になります。", "fix": "box-sizing: border-box; を指定する"},
            {"title": "width なしで margin: 0 auto", "wrong_code": ".box { margin: 0 auto; }", "why": "ブロック要素は、width がないと、親の幅いっぱいに広がるので、中央に寄りません。", "fix": ".box { width: 300px; margin: 0 auto; }"},
            {"title": "border の線の種類を書かない", "wrong_code": "border: 2px red;", "why": "線の種類（solid など）がないと、無効になり、枠線が表示されません。", "fix": "border: 2px solid red;"},
            {"title": "span に width を指定する", "wrong_code": "span { width: 100px; }", "why": "インライン要素には、width が効きません。display: inline-block や block にします。", "fix": "span { display: inline-block; width: 100px; }"},
        ],
        "checkpoints": [
            "箱は、内容・padding・border・margin の4層",
            "width は標準では内容の幅。border-box なら padding・border を含む",
            "値が4つなら上右下左、2つなら上下と左右",
            "border は 太さ 線の種類 色",
            "中央寄せは width と margin: 0 auto",
            "上下の margin は重なる（相殺）。インラインには width が効かない",
        ],
        "next_bridge": "箱の大きさと余白を、計算して決められるようになりました。問題で、ボックスモデルの理解を確かめましょう。",
    },
}

QUESTIONS = [
    mc(
        title="ボックスモデルの4層", lang="css",
        prompt="ボックスモデルで、箱の内側から外側へ、正しい順に並んでいるものはどれですか？",
        choices=[
            ("内容（content）→ padding → border → margin", ""),
            ("内容（content）→ margin → border → padding", "margin は、一番外側の余白です。内側の余白（padding）が、内容のすぐ外側にあります。"),
            ("border → 内容（content）→ padding → margin", "枠線（border）は、内容と padding の外側を囲んでいます。内容が、一番内側です。"),
        ],
        correct=0,
        why="内容の外側に padding、その外に border、さらにその外に margin があるから。",
        expl="覚え方: 「中身 → 内側の余白 → 枠線 → 外側の余白」。背景色が広がるのは、padding の範囲までで、margin には背景色は付きません。",
        concepts=["ボックスモデル"], diff=1,
        hint="箱の中身から、外へ向かって、4つの層を順に考えましょう。",
        ok="正解！内容 → padding → border → margin です。",
        ng="惜しい！箱の層の順序を確認しましょう。",
    ),
    pred(
        title="箱の見た目の幅", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、.box の見た目の幅（枠線の外側まで。margin は含まない）は、何 px になりますか？",
        code=BOX_CSS,
        check={"format": "css", "given_html": BOX_HTML, "probe": "document.querySelector('.box').offsetWidth"},
        choices=[
            ("200px", "標準（content-box）では、width は内容だけの幅です。padding と border が、その外側に足されます。", 200),
            ("250px", "", 250),
            ("270px", "margin は、箱の外側の余白で、見た目の幅（枠線の外側まで）には含まれません。", 270),
        ],
        correct=1,
        why="200（内容）+ 20×2（padding）+ 5×2（border）= 250px だから。",
        expl="見た目の幅は、content + 左右の padding + 左右の border です。margin は、まわりとの距離なので、幅には含みません。",
        concepts=["ボックスモデル", "width", "content-box"], diff=2,
        hint="左右に、padding と border が付くので、2倍して足します。",
        ok="正解！padding と border が足されます。",
        ng="惜しい！width が指す範囲を確認しましょう。",
    ),
    pred(
        title="box-sizing: border-box", lang="css",
        prompt="前の問題の CSS に、box-sizing: border-box; を足しました。見た目の幅（枠線の外側まで）は、何 px になりますか？",
        code='''.box {
  box-sizing: border-box;
  width: 200px;
  padding: 20px;
  border: 5px solid black;
  margin: 10px;
}''',
        check={"format": "css", "given_html": BOX_HTML, "probe": "document.querySelector('.box').offsetWidth"},
        choices=[
            ("250px", "border-box では、width が padding と border を含む幅になります。250 にはなりません。", 250),
            ("200px", "", 200),
            ("160px", "padding と border は、width の中に含まれますが、幅そのものから引かれて見た目が小さくなるわけではありません。見た目の幅は、width のとおりの 200px です（内容の幅が小さくなります）。", 160),
        ],
        correct=1,
        why="border-box では、width が、padding と border を含めた見た目の幅になるから。",
        expl="このとき、内容（content）の幅は、200 − 40 − 10 = 150px に、自動で小さくなります。レイアウトの計算がしやすいので、多くのサイトで、全要素に border-box が指定されています。",
        concepts=["box-sizing", "border-box"], diff=3,
        hint="border-box は、枠線までを含めた幅になります。",
        ok="正解！border-box では width のとおりの幅です。",
        ng="惜しい！border-box の働きを確認しましょう。",
    ),
    fill(
        title="余白の省略記法", lang="css",
        prompt="上下の padding を 10px、左右の padding を 20px にします。【空欄1】に入れる値を答えてください（半角で、空白で区切って入力）。",
        code='''.box {
  padding: __1__;
}''',
        check={"format": "css", "given_html": BOX_HTML, "expr": "(function () { var s = getComputedStyle(document.querySelector('.box')); return s.paddingTop === '10px' && s.paddingBottom === '10px' && s.paddingLeft === '20px' && s.paddingRight === '20px'; })()"},
        blanks=[(["10px 20px"], False)],
        wrong=[("b1", "20px 10px", "2つの値は、上下 → 左右の順です。「20px 10px」だと、上下が 20px、左右が 10px になります。")],
        why="2つの値の省略記法は、上下 → 左右の順に書くから。",
        expl="1つなら4辺すべて、2つなら上下・左右、3つなら上・左右・下、4つなら上・右・下・左（時計回り）です。margin も同じ書き方です。",
        concepts=["padding", "省略記法"], diff=2,
        hint="2つの値は、「上下」「左右」の順です。",
        ok="正解！2つの値は上下 → 左右です。",
        ng="惜しい！値の順番を確認しましょう。",
    ),
    pred(
        title="上下の margin の相殺", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、段落 A の下端と、段落 B の上端の間隔は、何 px になりますか？数字だけを入力してください。",
        code='''p {
  margin: 20px 0;
  padding: 0;
}''',
        check={"format": "css", "given_html": '<p class="a">A</p>\n<p class="b">B</p>', "probe": "Math.round(document.querySelector('.b').getBoundingClientRect().top - document.querySelector('.a').getBoundingClientRect().bottom)", "expected": 20},
        out="20",
        wrong=[("40", "上下に隣り合う margin は、足されません。大きいほうの値（ここでは同じ 20px）に重なり、間隔は 20px になります。"), ("0", "A の下に 20px、B の上に 20px の margin があり、重なって 20px の間隔が空きます。")],
        why="上下に隣り合う margin は、足し算ではなく、大きいほうの値に重なる（相殺される）から。",
        expl="margin の相殺は、ブロック要素の上下の margin で起こります。左右の margin や、padding では起こりません。段落の間隔が、思ったより狭いときの理由の1つです。",
        concepts=["margin", "相殺"], diff=3,
        hint="20 + 20 ではありません。上下の margin は、重なります。",
        ok="正解！上下の margin は、大きいほうに重なります。",
        ng="惜しい！margin の相殺を思い出しましょう。",
    ),
    bugfix(
        title="中央に寄らない箱", lang="css",
        prompt="箱を、画面の中央に置くつもりで margin: 0 auto を指定したのに、幅が広がるだけで、中央に寄った小さな箱になりません。正しい直し方はどれですか？",
        code='''.box {
  margin: 0 auto;
}''',
        fixed='''.box {
  width: 300px;
  margin: 0 auto;
}''',
        check={"format": "css", "given_html": '<div class="box">中央</div>', "expr": "(function () { var r = document.querySelector('.box').getBoundingClientRect(); return r.width === 300 && Math.abs(r.left + r.width / 2 - document.documentElement.clientWidth / 2) < 1; })()"},
        choices=[
            ("margin を 0 auto から auto 0 に変える", "auto 0 は、上下が auto、左右が 0 です。左右の余白がないので、水平方向の中央寄せにはなりません。"),
            ("box に width を指定する（例: width: 300px;）", ""),
            ("margin を padding に変える", "padding: 0 auto は、padding に auto は使えないので無効です。また、padding は内側の余白で、箱の位置は変わりません。"),
        ],
        correct=1, fmt="text",
        why="ブロック要素は、width がないと親の幅いっぱいに広がるため、auto の余白が分けられず、中央寄せにならないから。",
        expl="margin: 0 auto は、左右の余白を自動で、同じ大きさにする指定です。余る幅がないと、効果がありません。width（または max-width）で、親より小さい幅を指定します。",
        concepts=["margin: auto", "width", "中央寄せ"], diff=3,
        hint="余りの幅がないと、左右に分けることができません。",
        ok="正解！width を指定して中央寄せにします。",
        ng="惜しい！箱の幅はどうなっているでしょう？",
    ),
    mc(
        title="padding と margin の違い", lang="css",
        prompt="padding と margin の違いとして、正しい説明はどれですか？",
        choices=[
            ("padding は枠線の内側の余白で、背景色が付く。margin は枠線の外側の余白で、背景色は付かない", ""),
            ("padding は枠線の外側、margin は枠線の内側の余白である", "反対です。padding が内側、margin が外側です。"),
            ("どちらも枠線の内側の余白で、書き方が違うだけである", "padding は内側、margin は外側で、役割が違います。"),
        ],
        correct=0,
        why="padding は枠線の内側（背景色が付く）、margin は枠線の外側（透明で、他の要素との距離）だから。",
        expl="ボタンの文字の周りの余白は padding、ボタン同士の間隔は margin、のように使い分けます。覚え方は、padding = 詰め物（箱の中）、margin = 余白（箱の外）。",
        concepts=["padding", "margin"], diff=1,
        hint="背景色が付くのは、どちらの余白でしょう？",
        ok="正解！padding は内側、margin は外側です。",
        ng="惜しい！内側と外側を取り違えていませんか？",
    ),
    bugfix(
        title="表示されない枠線", lang="css",
        prompt="赤い枠線を付けたつもりが、枠線が表示されません。2行目を正しく書き直して入力してください（2行目の内容だけを入力）。",
        code='''.box {
  border: 2px red;
}''',
        fixed='''.box {
  border: 2px solid red;
}''',
        check={"format": "css", "given_html": BOX_HTML, "expr": "getComputedStyle(document.querySelector('.box')).borderTopWidth === '2px' && getComputedStyle(document.querySelector('.box')).borderTopColor === 'rgb(255, 0, 0)'"},
        target_line=2, accepted=["border: 2px solid red;", "border:2px solid red;", "border: solid 2px red;", "border: 2px red solid;", "border: 2px solid red", "border: red solid 2px;"],
        wrong=[("border: 2px red;", "元のコードのままです。線の種類（solid など）がないと、宣言が無効になり、枠線が表示されません。")],
        why="border には、線の種類（solid など）の指定が必要だから。",
        expl="border は、太さ・線の種類・色を、まとめて書く省略記法です。線の種類は、実線（solid）、破線（dashed）、点線（dotted）などです。省略すると、標準が none（なし）になるため、枠線は表示されません。",
        concepts=["border", "省略記法"], diff=2,
        hint="線の「種類」を表す語が抜けています。",
        ok="正解！線の種類（solid）が必要です。",
        ng="惜しい！border の3つの値を確認しましょう。",
    ),
    pred(
        title="インライン要素の width", lang="css",
        prompt="次の HTML と CSS を組み合わせたページで、span 要素に指定した width: 100px; は、どうなりますか？",
        code='''span {
  width: 100px;
}''',
        check={"format": "css", "given_html": '<span class="s">A</span>', "probe": "document.querySelector('.s').offsetWidth >= 100 ? 'applied' : 'ignored'"},
        choices=[
            ("効いて、幅が 100px になる", "span はインライン要素で、width が効きません。幅は、中の文字の幅になります。", "applied"),
            ("インライン要素なので、width は無視される", "", "ignored"),
            ("エラーになって、span が表示されない", "CSS には、エラーで表示が止まる仕組みはありません。効かない指定は、無視されるだけです。", "error"),
        ],
        correct=1,
        why="インライン要素には、width と height が効かないから。",
        expl="width を効かせたいときは、display: inline-block（文章の流れに並べたいとき）や、display: block を指定します。a 要素をボタンのように大きくしたいときにも、この指定が必要です。",
        concepts=["display", "インライン要素", "width"], diff=3,
        hint="span は、ブロックとインラインのどちらでしたか？",
        ok="正解！インライン要素には width が効きません。",
        ng="惜しい！span のデフォルトの display を思い出しましょう。",
    ),
    write_page(
        title="カードを作る", lang="css", fmt="css",
        prompt="次の HTML の .card に、CSS だけで、次の見た目を指定してください。\n・枠線を含めた見た目の幅を、ちょうど 300px にする（box-sizing: border-box を使う）\n・padding を 16px、枠線を 1px の実線（色は gray）、角の丸みを 8px にする\n・背景色を lightyellow にする\n・水平方向の中央に寄せる\n・.card の下に、24px の余白を取る",
        given_html='<div class="card">\n  <h2>タイトル</h2>\n  <p>本文です。</p>\n</div>',
        starter="/* ここに CSS を書きましょう */\n",
        ref='''.card {
  box-sizing: border-box;
  width: 300px;
  margin: 0 auto 24px;
  padding: 16px;
  border: 1px solid gray;
  border-radius: 8px;
  background-color: lightyellow;
}''',
        alts=['''.card {
  box-sizing: border-box;
  width: 300px;
  padding: 16px;
  border: 1px solid gray;
  border-radius: 8px;
  background: lightyellow;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 24px;
}'''],
        bads=[
            ('''.card {
  width: 300px;
  margin: 0 auto 24px;
  padding: 16px;
  border: 1px solid gray;
  border-radius: 8px;
  background-color: lightyellow;
}''', "box-sizing: border-box がないので、見た目の幅が 300 + 32 + 2 = 334px になります。"),
            ('''.card {
  box-sizing: border-box;
  width: 300px;
  padding: 16px;
  border: 1px solid gray;
  border-radius: 8px;
  background-color: lightyellow;
  margin-bottom: 24px;
}''', "水平方向の中央寄せ（margin の左右を auto にする）がありません。"),
        ],
        tests=[
            t_page("見た目の幅がちょうど 300px", "document.querySelector('.card').offsetWidth === 300"),
            t_page("padding が 16px、枠線が 1px の実線で gray", "(function () { var s = getComputedStyle(document.querySelector('.card')); return s.paddingTop === '16px' && s.paddingLeft === '16px' && s.borderTopWidth === '1px' && s.borderTopStyle === 'solid' && s.borderTopColor === 'rgb(128, 128, 128)'; })()"),
            t_page("角の丸みが 8px、背景色が lightyellow", "(function () { var s = getComputedStyle(document.querySelector('.card')); return s.borderTopLeftRadius === '8px' && s.backgroundColor === 'rgb(255, 255, 224)'; })()"),
            t_page("水平方向の中央に寄っている", "(function () { var r = document.querySelector('.card').getBoundingClientRect(); return Math.abs(r.left + r.width / 2 - document.documentElement.clientWidth / 2) < 1; })()"),
            t_page("下の margin が 24px", "getComputedStyle(document.querySelector('.card')).marginBottom === '24px'", visible=False),
            t_page("内容の幅は 300 − 32 − 2 = 266px", "document.querySelector('.card').clientWidth - 32 === 266", visible=False),
        ],
        why="box-sizing: border-box と width: 300px で見た目の幅を決め、padding・border・border-radius・background-color・margin で箱を整えるから。",
        expl="border-box にすると、width: 300px が、padding と border を含めた幅になるので、見た目が300pxになります。中央寄せの margin: 0 auto 24px は、上 0・左右 auto・下 24px の省略記法です。",
        concepts=["box-sizing", "padding", "border", "margin", "border-radius"], diff=3,
        hint="margin: 0 auto 24px は、上 0・左右 auto・下 24px です。",
        ok="正解！ボックスモデルを使いこなせました。",
        ng="惜しい！見た目の幅（border-box）と、中央寄せを確認しましょう。",
    ),
]
