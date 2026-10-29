from lib_web import mc, pred, fill, bugfix, write_page, t_page

CLICK = lambda i: "document.getElementById('%s').click()" % i
SET_INPUT = lambda i, v: "(function(){var t=document.getElementById('%s'); t.value=%r; t.dispatchEvent(new Event('input'));})()" % (i, v)

STAGE = {
    "number": 9,
    "title": "イベント処理",
    "subtitle": "addEventListener・イベントオブジェクト・input・submit・バブリング",
    "goals": [
        "addEventListener で、クリックなどのイベントに関数を結びつけられる",
        "関数を「渡す」（fn）ことと「呼び出す」（fn()）ことの違いを説明できる",
        "イベントオブジェクト（e.target・e.target.value）を使える",
        "click・input・submit などのイベントを使い分けられる",
        "preventDefault と、イベントのバブリングの基本を説明できる",
        "ボタンを押すと表示が変わる、簡単な動きのあるページを書ける",
    ],
    "prerequisites": ["関数・アロー関数・コールバック（ステージ7）", "DOM 操作（ステージ8）"],
    "topics": [
        "イベントと addEventListener",
        "関数を渡す／呼び出すの違い",
        "イベントオブジェクト（e.target）",
        "input・change・submit・keydown",
        "preventDefault",
        "バブリングとイベント委譲の基本",
    ],
    "pitfalls": [
        "addEventListener(\"click\", fn()) と書くと、関数がその場で実行されてしまう",
        "イベント名は click であって、onclick ではない（on を付けない）",
        "querySelectorAll の結果にはまとめて addEventListener できない（1つずつ付ける）",
        "フォームの submit は、preventDefault しないとページが再読み込みされる",
        "入力欄の値は e.target.value（textContent ではない）",
    ],
    "next_links": ["DOM 操作とイベント処理を組み合わせて、ページで動く簡単なアプリを作ります（ステージ10）"],
    "lesson": {
        "intro": "ボタンを押したとき、文字を入力したとき、フォームを送ったとき。ユーザーが何かしたときに動く処理を書くのが「イベント処理」です。前の回で書いた DOM の書き換えを、ユーザーの操作に結びつけると、動きのあるページになります。",
        "sections": [
            {
                "id": "S09-L1",
                "title": "addEventListener と関数を渡すこと",
                "read_minutes": 3,
                "body": [
                    "要素.addEventListener(\"イベント名\", 関数) で、「そのイベントが起きたら、この関数を呼んでください」とブラウザに頼みます。クリックのイベント名は click です（onclick ではなく、on を付けません）。",
                    "関数には、関数名だけを書いて渡します。addEventListener(\"click\", inc) と書くと、クリックされたときにブラウザが inc を呼び出します。inc() と ( ) を付けると、登録する時点で inc が実行され、その戻り値（undefined）が渡されてしまうため、クリックしても何も起きません。",
                    "関数は、イベントオブジェクト（慣習で e と書く）を受け取ります。e.target は、イベントが起きた要素です。入力欄の値は e.target.value で読めます。",
                    "querySelectorAll の結果（要素の一覧）には、addEventListener を直接呼べません。for...of などで、1つずつ取り出して付けます。",
                ],
                "glossary": [
                    {"term": "イベント", "definition": "クリック、入力、送信など、ユーザーの操作やブラウザの出来事。"},
                    {"term": "イベントリスナー", "definition": "イベントが起きたときに呼び出される関数。addEventListener で登録する。"},
                    {"term": "e.target", "definition": "イベントが起きた要素。"},
                ],
                "examples": [
                    {
                        "id": "S09-E1", "title": "クリックしたら数を増やす", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>カウンター</title></head>
<body>
  <button id="plus">+1</button>
  <p id="count">0</p>
  <script>
    let count = 0;
    const out = document.querySelector("#count");
    document.querySelector("#plus").addEventListener("click", () => {
      count++;
      out.textContent = count;
    });
  </script>
</body>
</html>''',
                        "line_notes": ["10行目: \"click\" は、クリックのイベント名です。", "10〜13行目: クリックのたびに、この関数が呼ばれ、count が1ずつ増えます。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "actions": [CLICK("plus"), CLICK("plus"), CLICK("plus")], "expr": "document.getElementById('count').textContent === '3'"},
                    },
                    {
                        "id": "S09-E2", "title": "入力に反応する（input イベント）", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>input</title></head>
<body>
  <input id="name" type="text">
  <p id="out"></p>
  <script>
    document.querySelector("#name").addEventListener("input", (e) => {
      document.querySelector("#out").textContent = "こんにちは、" + e.target.value;
    });
  </script>
</body>
</html>''',
                        "line_notes": ["input イベントは、入力欄の中身が変わるたびに起きます。", "e.target は入力欄の要素で、e.target.value が現在の入力内容です。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "actions": [SET_INPUT("name", "Hana")], "expr": "document.getElementById('out').textContent === 'こんにちは、Hana'"},
                    },
                ],
            },
            {
                "id": "S09-L2",
                "title": "いろいろなイベント・preventDefault・バブリング",
                "read_minutes": 3,
                "body": [
                    "よく使うイベント: click（クリック）、input（入力のたび）、change（値が確定したとき）、submit（フォームの送信）、keydown（キーを押した）、DOMContentLoaded（HTML の読み込み完了）。",
                    "フォームの submit イベントは、そのままだとページを送信先へ移動（または再読み込み）します。それを止めて、JavaScript で処理したいときは、関数の中で e.preventDefault() を呼びます。",
                    "子要素で起きたイベントは、親要素へも伝わります（バブリング）。内側の要素のイベントリスナーが先、その外側の要素のものが後に呼ばれます。この性質を使って、親要素1つにリスナーを付け、e.target で「どの子がクリックされたか」を判断する方法をイベント委譲といいます。要素に data-名前=\"値\" という属性を付けておくと、JavaScript では el.dataset.名前 で読めます。",
                ],
                "glossary": [
                    {"term": "preventDefault", "definition": "イベントの標準の動作（フォーム送信によるページ移動など）を止めるメソッド。"},
                    {"term": "バブリング", "definition": "子要素で起きたイベントが、親要素へ順に伝わること。"},
                    {"term": "イベント委譲", "definition": "親要素にリスナーを付け、e.target で子要素を判断する書き方。"},
                ],
                "examples": [
                    {
                        "id": "S09-E3", "title": "フォームと preventDefault", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>submit</title></head>
<body>
  <form id="form">
    <input id="word" type="text" value="こんにちは">
    <button type="submit">送信</button>
  </form>
  <p id="msg"></p>
  <script>
    document.querySelector("#form").addEventListener("submit", (e) => {
      e.preventDefault();
      document.querySelector("#msg").textContent = "送信: " + document.querySelector("#word").value;
    });
  </script>
</body>
</html>''',
                        "line_notes": ["11行目: submit イベントで、ページ移動を止めて（preventDefault）、自分の処理を行います。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "actions": ["document.getElementById('form').dispatchEvent(new Event('submit', { cancelable: true }))"], "expr": "document.getElementById('msg').textContent === '送信: こんにちは'"},
                    },
                    {
                        "id": "S09-E4", "title": "イベント委譲", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>委譲</title></head>
<body>
  <ul id="menu">
    <li data-name="home">ホーム</li>
    <li data-name="about">概要</li>
    <li data-name="contact">連絡先</li>
  </ul>
  <p id="out"></p>
  <script>
    document.querySelector("#menu").addEventListener("click", (e) => {
      document.querySelector("#out").textContent = e.target.dataset.name;
    });
  </script>
</body>
</html>''',
                        "line_notes": ["ul に1つだけリスナーを付けています。li をクリックすると、バブリングで ul に伝わります。", "e.target は実際にクリックされた li で、data-name の値は dataset.name で読めます。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "actions": ["document.querySelectorAll('#menu li')[1].click()"], "expr": "document.getElementById('out').textContent === 'about'"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "関数を渡さず、呼び出してしまう", "wrong_code": "btn.addEventListener(\"click\", inc());", "why": "inc() は登録の時点で実行され、その戻り値（undefined）が渡されます。クリックしても何も起きません。", "fix": "btn.addEventListener(\"click\", inc);"},
            {"title": "イベント名に on を付ける", "wrong_code": "btn.addEventListener(\"onclick\", fn);", "why": "イベント名は click です。onclick というイベントはなく、何も起きません。", "fix": "btn.addEventListener(\"click\", fn);"},
            {"title": "一覧にまとめて addEventListener", "wrong_code": "document.querySelectorAll(\".btn\").addEventListener(\"click\", fn);", "why": "querySelectorAll の結果は要素の一覧で、addEventListener を持っていません（TypeError）。for...of で1つずつ付けます。", "fix": "for (const b of buttons) { b.addEventListener(\"click\", fn); }"},
            {"title": "preventDefault を忘れる", "wrong_code": "form.addEventListener(\"submit\", (e) => { ... });", "why": "標準の動作（ページ移動・再読み込み）が起き、画面の書き換えが消えてしまいます。", "fix": "関数の最初に e.preventDefault();"},
        ],
        "checkpoints": [
            "addEventListener(\"イベント名\", 関数) で結びつける",
            "関数は渡す（fn）。fn() は呼び出し",
            "イベント名は click・input・submit など（on を付けない）",
            "e.target は起きた要素、入力欄の値は e.target.value",
            "フォーム送信は preventDefault で止める",
            "イベントは子から親へ伝わる（バブリング）",
        ],
        "next_bridge": "「ユーザーの操作で動く」ページが書けるようになりました。問題で、イベント処理のコードを読み、書いてみましょう。",
    },
}

CK = lambda html, **kw: dict({"format": "javascript_dom", "given_html": html}, **kw)
COUNTER_HTML = '<button id="plus">+1</button>\n<p id="count">0</p>'

QUESTIONS = [
    mc(
        title="関数を渡す書き方", lang="javascript",
        prompt="ボタン btn がクリックされたときに、関数 handle を呼び出したい。正しい書き方はどれですか？",
        fmt="code",
        choices=[
            ('btn.addEventListener("click", handle());', "handle() と ( ) を付けると、登録した時点で handle が実行され、その戻り値が渡されます。クリックされても handle は呼ばれません。"),
            ('btn.addEventListener("click", handle);', ""),
            ("btn.addEventListener(click, handle);", "引用符がない click は、変数名と解釈されます。そのような変数はないので ReferenceError になります。イベント名は文字列で書きます。"),
        ],
        correct=1,
        why="イベントリスナーには、関数そのものを（呼び出さずに）渡すから。",
        expl="handle は関数そのもの、handle() は関数を呼び出した結果です。addEventListener に渡すのは、「あとで呼んでほしい関数」なので、( ) を付けません。",
        concepts=["addEventListener", "コールバック"], diff=2,
        hint="関数名のあとに ( ) を付けると、何が起こりますか？",
        ok="正解！関数は呼び出さずに渡します。",
        ng="惜しい！( ) の有無と、イベント名の引用符を確認しましょう。",
    ),
    pred(
        title="クリックするたびに増えるカウンター", lang="javascript",
        prompt="次の HTML と JavaScript を組み合わせたページで、ボタン（#plus）を3回クリックしたあと、#count に表示されている文字は何ですか？",
        code='''let count = 0;
const plus = document.querySelector("#plus");
const out = document.querySelector("#count");
plus.addEventListener("click", () => {
  count++;
  out.textContent = count;
});''',
        check=CK(COUNTER_HTML, actions=[CLICK("plus")] * 3, probe="document.getElementById('count').textContent"),
        choices=[
            ("0", "クリックのたびにリスナーが呼ばれ、textContent も書き換えられます。何度か押せば表示は変わります。", "0"),
            ("3", "", "3"),
            ("1", "リスナーは、クリックのたびに呼ばれます。1回目で終わりではなく、3回呼ばれるので count は 3 になります。", "1"),
        ],
        correct=1,
        why="クリックのたびにリスナーが呼ばれ、count が 1 ずつ増えて、3回で 3 になるから。",
        expl="addEventListener で登録した関数は、イベントが起きるたびに呼び出されます。count はリスナーの外側で宣言されているので、呼び出しをまたいで値が保たれます。",
        concepts=["addEventListener", "クリック", "変数の保持"], diff=2,
        hint="リスナーは、クリックのたびに何回呼ばれますか？",
        ok="正解！クリックのたびに関数が呼ばれます。",
        ng="惜しい！リスナーは、クリックのたびに呼ばれます。",
    ),
    fill(
        title="クリックのイベント名", lang="javascript",
        prompt="ボタンがクリックされたら、メッセージを表示します。【空欄1】に入れるイベント名を答えてください。",
        code='''const btn = document.querySelector("#btn");
btn.addEventListener("__1__", () => {
  document.querySelector("#msg").textContent = "押されました";
});''',
        check=CK('<button id="btn">押す</button>\n<p id="msg"></p>', actions=["document.getElementById('btn').click()"], expr="document.getElementById('msg').textContent === '押されました'"),
        blanks=[(["click"], False)],
        wrong=[("b1", "onclick", "イベント名には on を付けません。\"onclick\" というイベントはなく、クリックしても関数は呼ばれません。")],
        why="クリックのイベント名は click だから。",
        expl="イベント名は、click・input・submit のように、on を付けない名前です。HTML の属性 onclick と混同しやすいので注意しましょう。",
        concepts=["イベント名", "click"], diff=1,
        hint="on は付けません。",
        ok="正解！イベント名は click です。",
        ng="惜しい！on を付けない名前を入力しましょう。",
    ),
    bugfix(
        title="関数を呼び出してしまった", lang="javascript",
        prompt="ボタンを2回クリックしたら 2 と表示されるはずが、1 と表示されたまま変わりません。7行目を直したものはどれですか？",
        code='''let count = 0;
const out = document.querySelector("#count");
function inc() {
  count++;
  out.textContent = count;
}
document.querySelector("#plus").addEventListener("click", inc());''',
        fixed='''let count = 0;
const out = document.querySelector("#count");
function inc() {
  count++;
  out.textContent = count;
}
document.querySelector("#plus").addEventListener("click", inc);''',
        check=CK(COUNTER_HTML, actions=[CLICK("plus")] * 2, expr="document.getElementById('count').textContent === '2'"),
        target_line=7,
        choices=[
            ('document.querySelector("#plus").addEventListener("click", "inc");', "引用符で囲むと文字列になります。関数ではない値をリスナーに渡すと、TypeError になります。"),
            ('document.querySelector("#plus").addEventListener("click", inc);', ""),
            ('document.querySelector("#plus").addEventListener(click, inc);', "引用符のない click は変数名と解釈され、ReferenceError になります。"),
        ],
        correct=1, fmt="code",
        why="リスナーには、関数そのもの（inc）を渡す必要があり、inc() だと登録時に1回実行されるだけだから。",
        expl="inc() と書くと、ページを読み込んだ時点で inc が1回実行され、count が 1 になります。クリックしても呼ばれるリスナーが登録されないので、表示が 1 のまま変わりません。",
        concepts=["addEventListener", "関数を渡す"], diff=3,
        hint="読み込んだ直後に、すでに 1 と表示されていませんか？",
        ok="正解！関数は ( ) なしで渡します。",
        ng="惜しい！inc() と inc の違いを思い出しましょう。",
    ),
    pred(
        title="e.target は押された要素", lang="javascript",
        prompt="次の HTML と JavaScript を組み合わせたページで、2番目のボタン（B）をクリックしたあと、#out に表示されている文字を入力してください。",
        code='''const buttons = document.querySelectorAll("#btns button");
for (const b of buttons) {
  b.addEventListener("click", (e) => {
    document.querySelector("#out").textContent = e.target.textContent;
  });
}''',
        check=CK('<div id="btns"><button>A</button><button>B</button><button>C</button></div>\n<p id="out"></p>', actions=["document.querySelectorAll('#btns button')[1].click()"], probe="document.getElementById('out').textContent", expected="B"),
        out="B",
        wrong=[("A", "リスナーは3つのボタンすべてに付いていますが、呼ばれるのはクリックされたボタンのものです。e.target も、クリックされたボタンです。"), ("button", "e.target.textContent は、要素の名前ではなく、ボタンの中の文字を返します。")],
        why="e.target は、クリックされた要素（B のボタン）で、その textContent は B だから。",
        expl="同じ関数を複数の要素に付けても、e.target を見れば、どの要素で起きたイベントかが分かります。e.target.textContent は、そのボタンに書かれた文字です。",
        concepts=["イベントオブジェクト", "e.target", "for...of"], diff=3,
        hint="クリックしたのは、どのボタンですか？",
        ok="正解！e.target は、イベントが起きた要素です。",
        ng="惜しい！クリックしたボタンの中の文字を答えましょう。",
    ),
    mc(
        title="フォーム送信を止める", lang="javascript",
        prompt="フォームの submit イベントで、ページの移動や再読み込みを止めて、JavaScript だけで処理したい。リスナーの関数の中で呼ぶべきものはどれですか？",
        code='''form.addEventListener("submit", (e) => {
  // ここで何を呼ぶ？
});''',
        fmt="code",
        choices=[
            ("e.stopPropagation()", "stopPropagation は、イベントが親要素へ伝わるのを止めるものです。フォーム送信の標準動作（ページ移動）は止まりません。"),
            ("e.preventDefault()", ""),
            ("e.cancel()", "e.cancel() というメソッドはありません。呼ぶと TypeError になります。"),
        ],
        correct=1,
        why="preventDefault は、イベントの標準の動作（フォーム送信によるページ移動）を止めるから。",
        expl="preventDefault は「標準の動作を止める」、stopPropagation は「親への伝わりを止める」で、別のものです。送信を JavaScript で処理するときは、最初に preventDefault を呼びます。",
        concepts=["preventDefault", "submit"], diff=3,
        hint="「標準（デフォルト）の動作を止める」という名前のメソッドです。",
        ok="正解！preventDefault で標準動作を止めます。",
        ng="惜しい！標準の動作を止めるメソッド名を思い出しましょう。",
    ),
    fill(
        title="入力された文字を読み取る", lang="javascript",
        prompt="入力欄に文字を入れるたびに、その内容を #out に表示します。【空欄1】に入れるプロパティ名を答えてください。",
        code='''document.querySelector("#name").addEventListener("input", (e) => {
  document.querySelector("#out").textContent = e.target.__1__;
});''',
        check=CK('<input id="name" type="text">\n<p id="out"></p>', actions=[SET_INPUT("name", "Hana")], expr="document.getElementById('out').textContent === 'Hana'"),
        blanks=[(["value"], False)],
        wrong=[("b1", "textContent", "input は中身を持たない要素なので、textContent は空のままです。入力された文字は value で読みます。")],
        why="入力欄の中身は、value プロパティで読み取るから。",
        expl="input イベントのたびに e.target.value を読めば、入力途中の文字列をその場で表示できます。文字数のカウントなどにも使えます。",
        concepts=["input イベント", "value"], diff=2,
        hint="入力欄の中身を読み書きするプロパティ名です。",
        ok="正解！入力欄は value で読みます。",
        ng="惜しい！textContent ではなく、入力欄専用のプロパティです。",
    ),
    bugfix(
        title="一覧にまとめてリスナーを付けた", lang="javascript",
        prompt="2つのボタン（.btn）のどちらを押しても数が増えるはずが、TypeError になって動きません。正しい直し方はどれですか？",
        code='''let count = 0;
const buttons = document.querySelectorAll(".btn");
buttons.addEventListener("click", () => {
  count++;
  document.querySelector("#count").textContent = count;
});''',
        fixed='''let count = 0;
const buttons = document.querySelectorAll(".btn");
for (const b of buttons) {
  b.addEventListener("click", () => {
    count++;
    document.querySelector("#count").textContent = count;
  });
}''',
        check=CK('<button class="btn">A</button><button class="btn">B</button>\n<p id="count">0</p>', actions=["document.querySelectorAll('.btn')[0].click()", "document.querySelectorAll('.btn')[1].click()"], expr="document.getElementById('count').textContent === '2'"),
        choices=[
            ("addEventListener を addEventListeners に変える", "addEventListeners というメソッドはありません。呼ぶと、同じく TypeError になります。"),
            ("querySelectorAll の結果を for...of で1つずつ取り出し、それぞれに addEventListener を付ける", ""),
            ("querySelectorAll を querySelector に変える", "querySelector は最初の1つだけを返すので、エラーは消えますが、2つ目のボタンにはリスナーが付かず、押しても数が増えません。"),
        ],
        correct=1, fmt="text",
        why="querySelectorAll の結果は要素の一覧で、リスナーは1つずつの要素に付ける必要があるから。",
        expl="addEventListener は、1つの要素に対して呼び出すメソッドです。一覧には付いていないので TypeError になります。for...of で取り出した要素に、それぞれ付けます。",
        concepts=["querySelectorAll", "for...of", "TypeError"], diff=3,
        hint="addEventListener を持っているのは、要素1つひとつです。",
        ok="正解！一覧は、1つずつ取り出して処理します。",
        ng="惜しい！一覧そのものには addEventListener がありません。",
    ),
    pred(
        title="イベントのバブリング", lang="javascript",
        prompt="次の HTML と JavaScript を組み合わせたページで、内側のボタン（#inner）をクリックしたあと、#log に表示される文字はどうなりますか？",
        code='''const log = document.querySelector("#log");
document.querySelector("#outer").addEventListener("click", () => {
  log.textContent += "outer ";
});
document.querySelector("#inner").addEventListener("click", () => {
  log.textContent += "inner ";
});''',
        check=CK('<div id="outer"><button id="inner">押す</button></div>\n<p id="log"></p>', actions=[CLICK("inner")], probe="document.getElementById('log').textContent"),
        choices=[
            ("outer inner ", "イベントは、押された内側の要素から、外側（親）へ向かって順に伝わります。内側の inner が先です。", "outer inner "),
            ("inner outer ", "", "inner outer "),
            ("inner ", "子で起きたクリックは、親要素にも伝わります（バブリング）。そのため、親の outer のリスナーも呼ばれます。", "inner "),
        ],
        correct=1,
        why="クリックは、内側の要素で処理されたあと、親要素へ伝わるから。",
        expl="これをバブリングといいます。内側 → 外側の順にリスナーが呼ばれます。この性質を使うと、親要素にだけリスナーを付けて、子のクリックをまとめて処理できます（イベント委譲）。",
        concepts=["バブリング", "イベント委譲"], diff=4,
        hint="クリックされたのは内側のボタンです。そのイベントは、どちらへ伝わりますか？",
        ok="正解！内側から外側へ伝わります。",
        ng="惜しい！イベントは、子から親へ伝わります。",
    ),
    write_page(
        title="カウンターを作る", lang="javascript", fmt="javascript_dom",
        prompt="+1 ボタン（#plus）で数を 1 増やし、-1 ボタン（#minus）で 1 減らし、リセットボタン（#reset）で 0 に戻すカウンターを作ってください。数は #count の文字として表示します。ただし、0 より小さくならないようにすること（0 のときに -1 を押しても 0 のまま）。",
        given_html='<button id="minus">-1</button> <span id="count">0</span> <button id="plus">+1</button>\n<button id="reset">リセット</button>',
        starter="// #plus, #minus, #reset, #count はあらかじめ用意されています\n",
        ref='''let count = 0;
const out = document.querySelector("#count");
function render() {
  out.textContent = count;
}
document.querySelector("#plus").addEventListener("click", () => {
  count++;
  render();
});
document.querySelector("#minus").addEventListener("click", () => {
  if (count > 0) {
    count--;
  }
  render();
});
document.querySelector("#reset").addEventListener("click", () => {
  count = 0;
  render();
});''',
        alts=['''let count = 0;
const out = document.getElementById("count");
document.getElementById("plus").onclick = () => { count += 1; out.textContent = count; };
document.getElementById("minus").onclick = () => { count = Math.max(0, count - 1); out.textContent = count; };
document.getElementById("reset").onclick = () => { count = 0; out.textContent = count; };'''],
        bads=[
            ('''let count = 0;
const out = document.querySelector("#count");
document.querySelector("#plus").addEventListener("click", () => { count++; out.textContent = count; });
document.querySelector("#minus").addEventListener("click", () => { count--; out.textContent = count; });
document.querySelector("#reset").addEventListener("click", () => { count = 0; out.textContent = count; });''', "0 のときに -1 を押すと、-1 になってしまいます。0 より小さくならないよう、if で確認します。"),
            ('''let count = 0;
const out = document.querySelector("#count");
document.querySelector("#plus").addEventListener("click", () => { count++; out.textContent = count; });
document.querySelector("#minus").addEventListener("click", () => { if (count > 0) { count--; } out.textContent = count; });''', "リセットボタンの処理がありません。"),
        ],
        tests=[
            t_page("+1 を3回押すと 3 になる", "document.getElementById('count').textContent === '3'", actions=[CLICK("plus")] * 3),
            t_page("+1 を2回、-1 を1回押すと 1 になる", "document.getElementById('count').textContent === '1'", actions=[CLICK("plus"), CLICK("plus"), CLICK("minus")]),
            t_page("0 のときに -1 を押しても 0 のまま", "document.getElementById('count').textContent === '0'", actions=[CLICK("minus")], visible=False),
            t_page("+1 を5回押してリセットすると 0 になる", "document.getElementById('count').textContent === '0'", actions=[CLICK("plus")] * 5 + [CLICK("reset")], visible=False),
            t_page("リセットのあとにまた +1 すると 1 になる", "document.getElementById('count').textContent === '1'", actions=[CLICK("plus")] * 2 + [CLICK("reset"), CLICK("plus")], visible=False),
        ],
        why="3つのボタンにそれぞれイベントリスナーを付け、count を更新して #count に表示し、-1 は 0 より大きいときだけ行うから。",
        expl="データ（count）を更新し、そのあと表示（textContent）を書き換える、という流れです。表示を書き換える処理を render という関数にまとめると、どのボタンの処理からも同じように呼べます。",
        concepts=["addEventListener", "if", "DOM操作"], diff=4,
        hint="count を変数に持ち、各ボタンで更新してから #count の textContent に反映します。",
        ok="正解！動きのあるカウンターが作れました。",
        ng="惜しい！0 のときの -1 や、リセットのあとの動きを確認しましょう。",
    ),
]
