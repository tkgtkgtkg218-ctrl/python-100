from lib_web import mc, pred, fill, bugfix, write_page, t_page

STAGE = {
    "number": 8,
    "title": "DOM操作",
    "subtitle": "要素の取得・書き換え・class・要素の追加",
    "goals": [
        "DOM が、ブラウザが HTML から作る要素の木構造であることを説明できる",
        "querySelector・querySelectorAll で要素を取得できる",
        "textContent・value・classList・style で要素の内容や見た目を変更できる",
        "createElement と appendChild で要素を作って追加できる",
        "textContent と innerHTML の違い（安全性）を説明できる",
        "<script> を、操作したい要素より後ろに書く理由を説明できる",
    ],
    "prerequisites": ["変数・if・for・配列・オブジェクト・関数（ステージ1〜7）", "HTML の基本（要素・id・class。HTML/CSS コースのステージ1〜6程度）"],
    "topics": [
        "DOM とは（document）",
        "querySelector / querySelectorAll / getElementById",
        "textContent と innerHTML",
        "classList（add / remove / toggle / contains）",
        "style と属性（setAttribute / value）",
        "createElement / appendChild / remove",
        "<script> を書く位置",
    ],
    "pitfalls": [
        "querySelector が要素を見つけられないと null になり、その先を読むと TypeError になる",
        "querySelector は最初の1つ、querySelectorAll は全部（配列のような一覧）を返す",
        "id は # 、class は . をセレクタの先頭に付ける",
        "input の中身は textContent ではなく value",
        "style のプロパティ名は background-color ではなく backgroundColor",
        "ユーザーの入力を innerHTML に入れると危険（textContent を使う）",
    ],
    "next_links": ["ボタンを押したときに DOM を書き換える「イベント処理」へ進みます（ステージ9）"],
    "lesson": {
        "intro": "ここからが、JavaScript の本領です。ブラウザは、HTML を読み取ると、ページの内容を「要素の木」のようなデータ（DOM）に作り変えます。JavaScript は、この DOM を書き換えることで、ページの文字・見た目・構造を、あとから変えられます。この回では、「要素を取り出して、書き換える」基本の流れを学びます。",
        "sections": [
            {
                "id": "S08-L1",
                "title": "DOM と要素の取得・書き換え",
                "read_minutes": 3,
                "body": [
                    "DOM（Document Object Model）は、ブラウザが HTML をもとに作る、要素の木構造のデータです。JavaScript では document というオブジェクトを入り口にして、DOM の要素を読み書きします。DOM を書き換えても、HTML ファイルそのものは変わらず、いま表示しているページだけが変わります。",
                    "要素を取り出すには、CSS のセレクタを使います。document.querySelector(\"#title\") は id が title の要素、document.querySelector(\".note\") は class が note の最初の1つです。該当するものすべては document.querySelectorAll(\".note\") で、配列に似た一覧が返ります（添字や for...of で扱えます）。見つからないと null になります。",
                    "要素の文字を変えるには textContent を使います。入力欄（input）の中身は value です。textContent に入れた文字列は、HTML ではなく、ただの文字として表示されます。HTML として解釈させる innerHTML は、ユーザーの入力を入れると、悪意のあるコードを実行される危険があるため、文字を入れたいときは textContent を使います。",
                    "<script> は、操作したい要素より後ろ（body の最後など）に書きます。ブラウザは HTML を上から順に読むので、要素がまだ作られていない位置のスクリプトからは、その要素を取得できません。",
                ],
                "glossary": [
                    {"term": "DOM", "definition": "ブラウザが HTML から作る、要素の木構造のデータ。JavaScript から読み書きできる。"},
                    {"term": "querySelector", "definition": "CSS のセレクタで、最初に見つかった要素を取り出すメソッド。"},
                    {"term": "textContent", "definition": "要素の中の文字列。書き換えると画面の文字が変わる。"},
                ],
                "examples": [
                    {
                        "id": "S08-E1", "title": "要素を取り出して書き換える", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>DOM</title></head>
<body>
  <h1 id="title">変更前</h1>
  <p class="note">A</p>
  <p class="note">B</p>
  <script>
    document.querySelector("#title").textContent = "変更後";
    const notes = document.querySelectorAll(".note");
    notes[1].textContent = "Bを書き換えた";
  </script>
</body>
</html>''',
                        "line_notes": ["8行目: id が title の要素の文字を書き換えます。", "9〜10行目: class が note の要素を、すべて取り出し、2つ目（添字 1）の文字を書き換えます。", "<script> は、要素より後ろに書かれているので、要素を取り出せます。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "expr": "document.getElementById('title').textContent === '変更後' && document.querySelectorAll('.note')[1].textContent === 'Bを書き換えた' && document.querySelectorAll('.note')[0].textContent === 'A'"},
                    },
                    {
                        "id": "S08-E2", "title": "入力欄の value", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>value</title></head>
<body>
  <input id="name" type="text">
  <script>
    const input = document.querySelector("#name");
    input.value = "Hana";
    console.log(input.value);
  </script>
</body>
</html>''',
                        "line_notes": ["input の中身は、textContent ではなく value で読み書きします。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "expr": "document.getElementById('name').value === 'Hana'"},
                    },
                ],
            },
            {
                "id": "S08-L2",
                "title": "class・style・要素の追加",
                "read_minutes": 3,
                "body": [
                    "要素の class を操作するには classList を使います。classList.add(\"on\") で追加、remove(\"on\") で削除、toggle(\"on\") で「あれば削除、なければ追加」、contains(\"on\") で持っているかを調べます。見た目は CSS で class に書いておき、JavaScript では class を付け外しする方法が、保守しやすい基本の形です。",
                    "style プロパティで、直接スタイルを変えることもできます。CSS のプロパティ名のハイフンは取り除き、次の文字を大文字にします（background-color は el.style.backgroundColor）。属性は el.setAttribute(\"href\", \"b.html\") や el.getAttribute(\"href\") で扱います。",
                    "要素を新しく作って追加するには、document.createElement(\"li\") で要素を作り、textContent などで中身を設定し、親要素.appendChild(要素) で追加します。要素を削除するには el.remove() です。配列のデータからリストを作るときに、for と組み合わせてよく使います。",
                ],
                "glossary": [
                    {"term": "classList", "definition": "要素の class を操作するための機能。add / remove / toggle / contains。"},
                    {"term": "createElement", "definition": "新しい要素を作るメソッド。作っただけでは画面に出ない。"},
                    {"term": "appendChild", "definition": "親要素の末尾に、子要素を追加するメソッド。"},
                ],
                "examples": [
                    {
                        "id": "S08-E3", "title": "classList と style", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8"><title>class</title>
  <style>.on { color: red; }</style>
</head>
<body>
  <p id="msg">こんにちは</p>
  <script>
    const msg = document.querySelector("#msg");
    msg.classList.add("on");
    msg.style.fontSize = "24px";
  </script>
</body>
</html>''',
                        "line_notes": ["10行目: class を付けると、CSS の .on のルールが適用されて赤くなります。", "11行目: style で直接、文字の大きさを変えます（font-size → fontSize）。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "expr": "getComputedStyle(document.getElementById('msg')).color === 'rgb(255, 0, 0)' && getComputedStyle(document.getElementById('msg')).fontSize === '24px'"},
                    },
                    {
                        "id": "S08-E4", "title": "要素を作って追加する", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>追加</title></head>
<body>
  <ul id="list"></ul>
  <script>
    const fruits = ["りんご", "みかん", "ぶどう"];
    const list = document.querySelector("#list");
    for (const fruit of fruits) {
      const li = document.createElement("li");
      li.textContent = fruit;
      list.appendChild(li);
    }
  </script>
</body>
</html>''',
                        "line_notes": ["10行目: li 要素を作ります（まだ画面には出ません）。", "11行目: 中身の文字を設定します。", "12行目: ul の末尾に追加すると、画面に表示されます。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "expr": "document.querySelectorAll('#list > li').length === 3 && document.querySelector('#list > li:last-child').textContent === 'ぶどう'"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "セレクタの typo・# と . の取り違え", "wrong_code": "document.querySelector(\"#mgs\").textContent = \"OK\";", "why": "該当する要素がないと null が返り、null の textContent に代入しようとして TypeError になります。id は #、class は . です。", "fix": "document.querySelector(\"#msg\")"},
            {"title": "style にハイフン付きの名前", "wrong_code": "box.style.background-color = \"red\";", "why": "ハイフンは引き算として読まれ、SyntaxError になります。backgroundColor と書きます。", "fix": "box.style.backgroundColor = \"red\";"},
            {"title": "input の値に textContent", "wrong_code": "input.textContent = \"Hana\";", "why": "input は中身を持たない要素なので、文字は表示されません。value を使います。", "fix": "input.value = \"Hana\";"},
            {"title": "ユーザーの入力を innerHTML に入れる", "wrong_code": "el.innerHTML = userInput;", "why": "入力が HTML として解釈され、悪意のあるコードが実行される危険があります。", "fix": "el.textContent = userInput;"},
        ],
        "checkpoints": [
            "DOM は HTML から作られる要素の木。書き換えてもファイルは変わらない",
            "querySelector は最初の1つ、querySelectorAll は全部。見つからなければ null",
            "文字は textContent、入力欄は value",
            "classList の add / remove / toggle / contains",
            "style は backgroundColor のようにキャメルケース",
            "createElement → 中身を設定 → appendChild",
        ],
        "next_bridge": "ページを書き換える方法が分かりました。問題では、実際の HTML と組み合わせたコードを読み、書いてみましょう。ボタンで動かす方法は、次のステージで学びます。",
    },
}

CK = lambda html, **kw: dict({"format": "javascript_dom", "given_html": html}, **kw)

QUESTIONS = [
    mc(
        title="DOM とは何か", lang="javascript",
        prompt="DOM の説明として、正しいものはどれですか？",
        choices=[
            ("HTML ファイルそのもので、JavaScript で書き換えると、ファイルの内容も変わる", "DOM は、ブラウザが HTML を読み取って作る「いま表示しているページのデータ」です。DOM を書き換えても、HTML ファイルは変わりません。"),
            ("ブラウザが HTML から作る、要素を木構造で表したデータで、JavaScript から読み書きできる", ""),
            ("ページの見た目を指定する、CSS の一種である", "見た目を指定するのは CSS です。DOM は、ページの構造を JavaScript から操作するためのデータです。"),
        ],
        correct=1,
        why="DOM は、HTML をもとにブラウザが作る要素の木構造で、JavaScript の操作対象になるから。",
        expl="JavaScript でページを変えるとき、HTML ファイルを書き換えているのではなく、ブラウザの中にある DOM を書き換えています。ページを再読み込みすると、元の HTML から DOM が作り直されます。",
        concepts=["DOM", "document"], diff=1,
        hint="DOM は Document Object Model の略です。何の「モデル」でしょう？",
        ok="正解！DOM はブラウザが作る要素の木構造です。",
        ng="惜しい！DOM はファイルではなく、ブラウザの中のデータです。",
    ),
    pred(
        title="querySelector と querySelectorAll", lang="javascript",
        prompt="次の HTML と JavaScript を組み合わせたページを表示したあと、2つの p 要素の文字を順に並べるとどうなりますか？",
        code='''document.querySelector(".note").textContent = "X";
const notes = document.querySelectorAll(".note");
notes[1].textContent = "Y";''',
        check=CK('<p class="note">A</p>\n<p class="note">B</p>', probe="Array.from(document.querySelectorAll('.note')).map(function (e) { return e.textContent; }).join('')"),
        choices=[
            ("XB", "3行目で、2つ目の要素（添字 1）の文字も Y に書き換えているので、B のままではありません。", "XB"),
            ("XY", "", "XY"),
            ("XX", "querySelector は最初の1つだけを返します。2つ目は、3行目で notes[1] として別に書き換えています。", "XX"),
        ],
        correct=1,
        why="querySelector は最初の1つ（A）を X に、notes[1] は2つ目（B）を Y に変えるから。",
        expl="querySelector は条件に合う最初の1つ、querySelectorAll は条件に合うすべてを返します。notes[1] は添字 1、つまり2番目の要素です。",
        concepts=["querySelector", "querySelectorAll", "textContent"], diff=2,
        hint="1行目と3行目で、書き換わる要素はそれぞれどれでしょう？",
        ok="正解！querySelector は最初の1つ、All は全部です。",
        ng="惜しい！1行目は最初の1つ、3行目は2つ目を書き換えています。",
    ),
    mc(
        title="textContent と innerHTML", lang="javascript",
        prompt="ユーザーが入力した文字列 userInput を、画面の要素 el に表示します。安全な書き方はどれですか？",
        fmt="code",
        choices=[
            ("el.innerHTML = userInput;", "入力が HTML として解釈されるため、<img onerror=...> のような文字列を入れられると、悪意のあるコードが実行される危険があります。"),
            ("el.textContent = userInput;", ""),
            ("el.value = userInput;", "value は input などの入力欄の値を扱うプロパティです。一般の要素（p や div など）では、画面に表示されません。"),
        ],
        correct=1,
        why="textContent は、入れた文字列を HTML としてではなく、ただの文字として扱うから。",
        expl="innerHTML は HTML として解釈される文字列を入れられるので便利ですが、ユーザーの入力など信頼できない文字列を入れると、攻撃に使われる可能性があります。ただの文字を表示するなら textContent を使います。",
        concepts=["textContent", "innerHTML", "安全性"], diff=3,
        hint="入力された文字が、HTML として解釈されると何が起きるでしょう？",
        ok="正解！文字の表示は textContent が安全です。",
        ng="惜しい！HTML として解釈されない方法を選びましょう。",
    ),
    fill(
        title="class を付ける", lang="javascript",
        prompt="ボタンに class「active」を付けます。【空欄1】に入れるメソッド名を答えてください。",
        code='''const btn = document.querySelector("#btn");
btn.classList.__1__("active");''',
        check=CK('<button id="btn">送信</button>', expr="document.querySelector('#btn').classList.contains('active')"),
        blanks=[(["add", "toggle"], False)],
        wrong=[("b1", "remove", "remove は class を取り除くメソッドです。もともと active はないので、何も起きず、class は付きません。")],
        why="classList.add は、要素に class を追加するメソッドだから。",
        expl="classList には add（追加）、remove（削除）、toggle（なければ追加・あれば削除）、contains（持っているか調べる）があります。この場面では、add でも、まだ class がないので toggle でも同じ結果になります。",
        concepts=["classList", "add"], diff=2,
        hint="「追加する」を意味する英単語です。",
        ok="正解！classList.add で class を追加できます。",
        ng="惜しい！class を追加するメソッド名を思い出しましょう。",
    ),
    bugfix(
        title="セレクタの書き間違い", lang="javascript",
        prompt="id が msg の p 要素の文字を「OK」に書き換えたいのに、TypeError になります。1行目を直したものはどれですか？",
        code='''const el = document.querySelector("#mgs");
el.textContent = "OK";''',
        fixed='''const el = document.querySelector("#msg");
el.textContent = "OK";''',
        check=CK('<p id="msg">未設定</p>', expr="document.getElementById('msg').textContent === 'OK'"),
        target_line=1,
        choices=[
            ('const el = document.querySelector("msg");', "# も . も付けない msg は、<msg> という名前の要素を探します。そのような要素はないので null になり、同じ TypeError が起きます。"),
            ('const el = document.querySelector("#msg");', ""),
            ('const el = document.querySelector(".msg");', ". は class を探す書き方です。msg は id なので、見つからずに null になります。"),
        ],
        correct=1, fmt="code",
        why="id を探すセレクタは、# に続けて、HTML の id と同じ綴りで書く必要があるから。",
        expl="querySelector が要素を見つけられないと null を返します。null の textContent を書き換えようとして、TypeError になります。セレクタの綴りと、# （id）・.（class）の違いを確認します。",
        concepts=["querySelector", "セレクタ", "null"], diff=2,
        hint="HTML の id は何ですか？ セレクタの綴りと見比べましょう。",
        ok="正解！#id と綴りを合わせます。",
        ng="惜しい！id は # で始め、綴りも HTML と同じにします。",
    ),
    pred(
        title="要素を作って追加する", lang="javascript",
        prompt="次の HTML と JavaScript を組み合わせたページを表示したあと、ul 要素の中に表示される文字を、続けて書いたものを入力してください。",
        code='''const list = document.querySelector("#list");
for (let i = 1; i <= 3; i++) {
  const li = document.createElement("li");
  li.textContent = "項目" + i;
  list.appendChild(li);
}''',
        check=CK('<ul id="list"></ul>', probe="document.getElementById('list').textContent", expected="項目1項目2項目3"),
        out="項目1項目2項目3",
        wrong=[("項目1", "くり返しは3回行われ、そのたびに li が1つずつ追加されます。"), ("項目3項目2項目1", "appendChild は、親の末尾に追加します。先に追加した項目1が先頭に並びます。")],
        why="3回のくり返しで、「項目1」「項目2」「項目3」の li が順に末尾へ追加されるから。",
        expl="createElement で li を作り、textContent で中身を設定し、appendChild で ul の末尾へ追加します。くり返しの中でこれを行うと、データの数だけ要素を追加できます。",
        concepts=["createElement", "appendChild", "for"], diff=2,
        hint="appendChild は、子要素を末尾に追加します。",
        ok="正解！3つの li が順に追加されました。",
        ng="惜しい！くり返しの回数と、追加される順番を確認しましょう。",
    ),
    fill(
        title="入力欄に文字を入れる", lang="javascript",
        prompt="テキスト入力欄（input）に、Hana という文字を入れます。【空欄1】に入れるプロパティ名を答えてください。",
        code='''document.querySelector("#name").__1__ = "Hana";''',
        check=CK('<input id="name" type="text">', expr="document.querySelector('#name').value === 'Hana'"),
        blanks=[(["value"], False)],
        wrong=[("b1", "textContent", "input は中身を持たない要素なので、textContent に文字を入れても、入力欄には表示されません（value は変わらないまま）。")],
        why="入力欄の中身は、value プロパティで読み書きするから。",
        expl="p や div の文字は textContent ですが、input・textarea・select の値は value です。ユーザーが入力した文字を読み取るときも、value を使います。",
        concepts=["value", "input"], diff=2,
        hint="入力欄の「値」を意味する英単語です。",
        ok="正解！入力欄は value で読み書きします。",
        ng="惜しい！textContent ではなく、入力欄専用のプロパティを使います。",
    ),
    bugfix(
        title="style のプロパティ名", lang="javascript",
        prompt="id が box の要素の背景色を赤にしたいのに、コードが動きません。2行目を正しく書き直して入力してください（2行目の内容だけを入力）。",
        code='''const box = document.querySelector("#box");
box.style.background-color = "red";''',
        fixed='''const box = document.querySelector("#box");
box.style.backgroundColor = "red";''',
        check=CK('<div id="box">箱</div>', expr="getComputedStyle(document.querySelector('#box')).backgroundColor === 'rgb(255, 0, 0)'"),
        target_line=2, qi=True,
        accepted=['box.style.backgroundColor = "red";', 'box.style.backgroundColor = "red"', 'box.style.background = "red";', 'box.style.backgroundColor="red";'],
        wrong=[('box.style.background-color = "red";', "元のコードのままです。ハイフンは引き算として読まれ、SyntaxError になります。")],
        why="style のプロパティ名は、ハイフンを取り除いて次の文字を大文字にした形（backgroundColor）で書くから。",
        expl="CSS の background-color は、JavaScript では backgroundColor と書きます。ハイフンのままだと「background 引く color」と解釈され、構文エラーになります。",
        concepts=["style", "キャメルケース"], diff=3,
        hint="CSS の名前から、ハイフンを取り除いて、次の文字を大文字にします。",
        ok="正解！style はキャメルケースで書きます。",
        ng="惜しい！ハイフンを含む名前は、JavaScript ではそのまま使えません。",
    ),
    pred(
        title="classList の操作", lang="javascript",
        prompt="次の HTML と JavaScript を組み合わせたページを表示したあと、id が box の要素の class は、最終的にどうなりますか？",
        code='''const box = document.querySelector("#box");
box.classList.add("on");
box.classList.toggle("on");
box.classList.toggle("hidden");''',
        check=CK('<div id="box" class="card"></div>', probe="document.getElementById('box').className"),
        choices=[
            ("card on hidden", "3行目の toggle(\"on\") で、あった on が取り除かれます。toggle は「あれば削除、なければ追加」です。", "card on hidden"),
            ("card hidden", "", "card hidden"),
            ("card on", "4行目の toggle(\"hidden\") で、hidden が追加されます。また 3行目で on は取り除かれています。", "card on"),
        ],
        correct=1,
        why="on は add のあと toggle で削除され、hidden は toggle で追加されるから。",
        expl="2行目で card on、3行目の toggle(\"on\") で on が外れて card、4行目の toggle(\"hidden\") で hidden が加わり card hidden になります。",
        concepts=["classList", "toggle"], diff=3,
        hint="1行ずつ、class の一覧がどう変わるか書き出しましょう。",
        ok="正解！toggle は付け外しを切り替えます。",
        ng="惜しい！toggle は、あれば削除、なければ追加です。",
    ),
    write_page(
        title="配列からリストを作る", lang="javascript", fmt="javascript_dom",
        prompt="配列 fruits の要素を、1つずつ li 要素にして、id が list の ul 要素に追加する JavaScript を書いてください（li の中の文字は、配列の要素そのもの。順番もそのまま）。fruits と ul はあらかじめ用意されています。",
        given_html='<ul id="list"></ul>\n<script>const fruits = ["りんご", "みかん", "ぶどう"];</script>',
        starter="// fruits と #list はあらかじめ用意されています\n",
        ref='''const list = document.querySelector("#list");
for (const fruit of fruits) {
  const li = document.createElement("li");
  li.textContent = fruit;
  list.appendChild(li);
}''',
        alts=['''const list = document.getElementById("list");
fruits.forEach((fruit) => {
  const li = document.createElement("li");
  li.textContent = fruit;
  list.append(li);
});''', '''const list = document.querySelector("#list");
for (let i = 0; i < fruits.length; i++) {
  list.innerHTML += "<li>" + fruits[i] + "</li>";
}'''],
        bads=[
            ('''const list = document.querySelector("#list");
list.textContent = fruits.join(", ");''', "ul の中に li 要素が作られていません。要素ごとに createElement で li を作って追加します。"),
            ('''const list = document.querySelector("#list");
const li = document.createElement("li");
li.textContent = fruits[0];
list.appendChild(li);''', "最初の要素だけを追加しています。くり返しで、すべての要素を追加する必要があります。"),
        ],
        tests=[
            t_page("li が3つ追加されている", "document.querySelectorAll('#list > li').length === 3"),
            t_page("li の文字が配列の要素と同じ順番になっている", "Array.from(document.querySelectorAll('#list > li')).map(function (l) { return l.textContent; }).join('|') === 'りんご|みかん|ぶどう'"),
            t_page("要素が1つだけの配列でも動く", "Array.from(document.querySelectorAll('#list > li')).map(function (l) { return l.textContent; }).join('|') === 'ぱん'", visible=False, given_html='<ul id="list"></ul>\n<script>const fruits = ["ぱん"];</script>'),
            t_page("空の配列でも動く（li は0個）", "document.querySelectorAll('#list > li').length === 0 && !!document.getElementById('list')", visible=False, given_html='<ul id="list"></ul>\n<script>const fruits = [];</script>'),
            t_page("5つの要素でも動く", "Array.from(document.querySelectorAll('#list > li')).map(function (l) { return l.textContent; }).join('|') === 'a|b|c|d|e'", visible=False, given_html='<ul id="list"></ul>\n<script>const fruits = ["a","b","c","d","e"];</script>'),
        ],
        why="配列の要素ごとに、createElement で li を作り、textContent を設定し、appendChild で ul へ追加するから。",
        expl="くり返しの中で li を作って追加すれば、配列の要素数が変わっても同じコードで動きます。innerHTML に文字列を足していく別解も動きますが、入力が信頼できない場合は textContent を使う方が安全です。",
        concepts=["createElement", "appendChild", "for...of", "DOM操作"], diff=3,
        hint="for...of で fruits を順に取り出し、1つずつ li を作って list に追加します。",
        ok="正解！データから要素を作ってページに追加できました。",
        ng="惜しい！配列の要素が1つ・0個のときでも動くか確認しましょう。",
    ),
]
