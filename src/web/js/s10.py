from lib_web import mc, pred, fill, bugfix, write_page, t_page

CLICK = lambda i: "document.getElementById('%s').click()" % i
SET = lambda i, v: "document.getElementById('%s').value=%r" % (i, v)
SET_EVT = lambda i, v: "(function(){var t=document.getElementById('%s'); t.value=%r; t.dispatchEvent(new Event('input'));})()" % (i, v)
ADD = lambda v: "document.getElementById('todoInput').value=%r; document.getElementById('addBtn').click()" % v
VIS = lambda i: "(getComputedStyle(document.getElementById('%s')).display !== 'none')" % i
CK = lambda html, **kw: dict({"format": "javascript_dom", "given_html": html}, **kw)

TODO_HTML = '<input id="todoInput" type="text">\n<button id="addBtn">追加</button>\n<ul id="todoList"></ul>'

TODO_APP = '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>ToDo</title></head>
<body>
  <input id="todoInput" type="text">
  <button id="addBtn">追加</button>
  <ul id="todoList"></ul>
  <script>
    const input = document.querySelector("#todoInput");
    const list = document.querySelector("#todoList");
    document.querySelector("#addBtn").addEventListener("click", () => {
      const text = input.value.trim();
      if (text === "") {
        return;
      }
      const li = document.createElement("li");
      li.textContent = text;
      list.appendChild(li);
      input.value = "";
    });
  </script>
</body>
</html>'''

STAGE = {
    "number": 10,
    "title": "簡単なWebアプリ制作",
    "subtitle": "データと表示を分けて、動くページを組み立てる",
    "goals": [
        "「データを更新する → 画面を書き換える」という流れでアプリを組み立てられる",
        "入力欄の値が文字列であることを意識し、Number() で数値にできる",
        "空の入力など、想定外の入力に対応できる",
        "カウンター・ToDo・タブ切替など、簡単なWebアプリを自分で書ける",
        "ここまでの JavaScript の知識（変数・配列・関数・DOM・イベント）を組み合わせられる",
    ],
    "prerequisites": ["ステージ1〜9のすべて（特に配列・関数・DOM 操作・イベント処理）"],
    "topics": [
        "データ（配列・数）と表示（DOM）を分けて考える",
        "入力値の取得（value）と数値への変換（Number）",
        "空の入力のチェック（trim）",
        "要素の追加と削除（createElement / appendChild / remove）",
        "class や hidden での表示の切り替え",
        "完成したアプリの全体像を読む",
    ],
    "pitfalls": [
        "input の value は、数字を入れても文字列（\"1\" + \"2\" は \"12\"）",
        "配列のデータを変えただけでは、画面は変わらない（render し直す）",
        "空の入力や、スペースだけの入力を忘れる",
        "追加・削除のあとに、件数などの表示を更新し忘れる",
        "一度に全部を作ろうとせず、1つの機能ずつ作って確かめる",
    ],
    "next_links": ["この先は、localStorage での保存、fetch での通信、ファイル分割・モジュール、フレームワークなどへ進めます（このコースでは扱いません）"],
    "lesson": {
        "intro": "最後のステージです。新しい文法はほとんどありません。変数・配列・関数・DOM・イベントを組み合わせて、ページの中で動く小さなアプリを作ります。コツは、いきなり全部を書かず、「何を覚えておくか（データ）」「画面にどう見せるか（表示）」「どの操作で何が起きるか（イベント）」を分けて考えることです。",
        "sections": [
            {
                "id": "S10-L1",
                "title": "アプリづくりの考え方",
                "read_minutes": 3,
                "body": [
                    "アプリは、「データを更新する → 画面を書き換える」の繰り返しです。例えば、ToDo アプリでは、「項目の一覧」がデータで、画面の li の並びが表示です。データだけを書き換えても、画面は自動では変わりません。データを変えたあと、表示を書き換える処理（render など）を呼ぶ必要があります。",
                    "入力欄の value は、数字を入れていても文字列です。そのまま + で足すと連結になるので、計算に使うときは Number(文字列) で数値にします。",
                    "ユーザーは、想定外の入力をします。空の入力や、スペースだけの入力は、追加しない、のようにチェックしましょう。文字列の前後の空白は trim() で取り除けます。",
                    "作る順番は、(1) 表示だけ作る、(2) 1つのボタンの動きだけ作る、(3) 想定外の入力に対応する、と、少しずつ確かめながら進めるのが安全です。",
                ],
                "glossary": [
                    {"term": "状態（データ）", "definition": "アプリが覚えておく値。数や配列など。"},
                    {"term": "render（描画）", "definition": "データをもとに、画面（DOM）を書き換える処理。"},
                    {"term": "trim", "definition": "文字列の前後の空白を取り除くメソッド。"},
                ],
                "examples": [
                    {
                        "id": "S10-E1", "title": "入力値は文字列", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>足し算</title></head>
<body>
  <input id="a" value="1">
  <input id="b" value="2">
  <button id="calc">足す</button>
  <p id="result"></p>
  <script>
    document.querySelector("#calc").addEventListener("click", () => {
      const a = Number(document.querySelector("#a").value);
      const b = Number(document.querySelector("#b").value);
      document.querySelector("#result").textContent = a + b;
    });
  </script>
</body>
</html>''',
                        "line_notes": ["11〜12行目: value は文字列なので、Number() で数値にしてから足します。", "Number() を付けないと、\"1\" + \"2\" が \"12\" になります。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "actions": [CLICK("calc")], "expr": "document.getElementById('result').textContent === '3'"},
                    },
                    {
                        "id": "S10-E2", "title": "ToDo の追加（空のチェックつき）", "language": "html",
                        "code": TODO_APP,
                        "line_notes": ["12行目: trim() で前後の空白を取り除きます。", "13〜15行目: 空なら何も追加せず、return でこの関数を終わります。", "20行目: 追加したあと、入力欄を空に戻します。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "actions": [ADD("牛乳を買う"), ADD("   "), ADD("宿題")], "expr": "document.querySelectorAll('#todoList > li').length === 2 && document.querySelectorAll('#todoList > li')[0].textContent === '牛乳を買う' && document.getElementById('todoInput').value === ''"},
                    },
                ],
            },
            {
                "id": "S10-L2",
                "title": "いろいろなアプリの作り方",
                "read_minutes": 3,
                "body": [
                    "タブの切り替えは、「どのパネルを見せるか」を切り替える処理です。各ボタンに data-target=\"p1\" のように、対応するパネルの id を持たせておくと、クリックされたボタンの dataset.target で、見せるパネルが分かります。パネルは hidden 属性（el.hidden = true / false）で、表示と非表示を切り替えられます。",
                    "一覧の項目を、クリックで「完了」にするには、classList.toggle(\"done\") を使います。残りの件数などは、クリックのたびに数え直して表示します。項目ごとにリスナーを付けるほか、親要素にまとめて付けて e.target で判断する（イベント委譲）書き方もあります。",
                    "削除ボタンつきのリストでは、li の中に button を作り、そのクリックで li.remove() を呼びます。追加と削除のたびに、件数の表示も更新します。",
                    "ここから先は、入力内容をブラウザに保存する localStorage、サーバーと通信する fetch、コードを複数ファイルに分けるモジュール、フレームワークなどへ進めます。このコースの範囲は、ここまでです。",
                ],
                "glossary": [
                    {"term": "dataset", "definition": "data-名前=\"値\" という属性を、JavaScript から el.dataset.名前 で読み書きする機能。"},
                    {"term": "remove", "definition": "要素を DOM から取り除くメソッド。"},
                ],
                "examples": [
                    {
                        "id": "S10-E3", "title": "タブの切り替え", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>タブ</title></head>
<body>
  <button class="tab" data-target="p1">タブ1</button>
  <button class="tab" data-target="p2">タブ2</button>
  <div id="p1" class="panel">内容1</div>
  <div id="p2" class="panel" hidden>内容2</div>
  <script>
    const tabs = document.querySelectorAll(".tab");
    const panels = document.querySelectorAll(".panel");
    for (const tab of tabs) {
      tab.addEventListener("click", () => {
        for (const p of panels) {
          p.hidden = p.id !== tab.dataset.target;
        }
      });
    }
  </script>
</body>
</html>''',
                        "line_notes": ["12行目: すべてのタブに、同じ処理のリスナーを付けています。", "14〜15行目: クリックされたタブの data-target と同じ id のパネルだけを、表示します。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "actions": ["document.querySelectorAll('.tab')[1].click()"], "expr": "document.getElementById('p1').hidden === true && document.getElementById('p2').hidden === false"},
                    },
                    {
                        "id": "S10-E4", "title": "クリックで完了にして、残りの件数を表示", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>完了</title></head>
<body>
  <ul id="list"><li>A</li><li>B</li><li>C</li></ul>
  <p>残り: <span id="remaining">3</span>件</p>
  <script>
    const items = document.querySelectorAll("#list li");
    const remaining = document.querySelector("#remaining");
    function update() {
      let n = 0;
      for (const li of items) {
        if (!li.classList.contains("done")) {
          n++;
        }
      }
      remaining.textContent = n;
    }
    for (const li of items) {
      li.addEventListener("click", () => {
        li.classList.toggle("done");
        update();
      });
    }
  </script>
</body>
</html>''',
                        "line_notes": ["10〜18行目: done の class がない li を数えて、残りの件数を表示します。", "21〜22行目: クリックで done を付け外しし、そのたびに件数を更新します。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "actions": ["document.querySelectorAll('#list li')[0].click()", "document.querySelectorAll('#list li')[2].click()"], "expr": "document.getElementById('remaining').textContent === '1'"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "入力値をそのまま足す", "wrong_code": "const a = document.querySelector(\"#a\").value;\nconst b = document.querySelector(\"#b\").value;\nresult.textContent = a + b;", "why": "value は文字列なので、\"1\" + \"2\" は \"12\" になります。Number() で数値にします。", "fix": "Number(a) + Number(b)"},
            {"title": "データだけ更新して画面を更新しない", "wrong_code": "todos.push(text);  // render() を呼ばない", "why": "配列を変えても、画面の DOM は自動では変わりません。", "fix": "データを変えたあとに render() を呼ぶ"},
            {"title": "空の入力を追加してしまう", "wrong_code": "const text = input.value;\nconst li = document.createElement(\"li\");", "why": "空やスペースだけの入力でも、空の項目が追加されます。trim() で取り除き、空なら return します。", "fix": "if (input.value.trim() === \"\") { return; }"},
            {"title": "削除のあとに件数を更新しない", "wrong_code": "del.addEventListener(\"click\", () => { li.remove(); });", "why": "項目は消えても、「N件」の表示は古いままです。", "fix": "li.remove(); updateTotal();"},
        ],
        "checkpoints": [
            "データを更新する → 画面を書き換える（render）",
            "input の value は文字列。計算には Number()",
            "空の入力は trim() で確認して無視する",
            "追加・削除のあとは、件数などの表示も更新する",
            "表示の切り替えは hidden や class の付け外し",
            "小さく作って、1つずつ確かめる",
        ],
        "next_bridge": "JavaScript の最後のステージです。読む問題と、自分でアプリを書く問題があります。1つの機能ずつ、確かめながら作っていきましょう。",
    },
}

QUESTIONS = [
    mc(
        title="アプリの作り方の基本", lang="javascript",
        prompt="ToDo アプリで「項目を追加したら、画面の一覧も変わる」ようにするとき、基本的な考え方として適切なものはどれですか？",
        choices=[
            ("配列（データ）に項目を追加したら、自動で画面も変わるので、画面側のコードは書かなくてよい", "配列を変えても、画面の DOM は自動では変わりません。データを変えたあとに、画面を書き換える処理を呼ぶ必要があります。"),
            ("データを更新したあとに、画面を書き換える処理（render）を呼んで、データと画面をそろえる", ""),
            ("画面の li の数を数えるだけで、データは持たずに作るのが基本である", "それでも動くアプリは作れますが、規模が大きくなると、画面を見ないとデータが分からず、管理が難しくなります。データを持つ方法が基本です。"),
        ],
        correct=1,
        why="DOM は自動では更新されないので、データを変えたあとに、表示を書き換える処理を呼ぶ必要があるから。",
        expl="データ（配列など）と表示（DOM）を分けて考えると、「何を覚えるか」と「どう見せるか」を別々に整理できます。更新は、データを変える → 表示を書き換える、の順です。",
        concepts=["アプリ設計", "データと表示"], diff=2,
        hint="DOM は、配列の中身を自動で追いかけてくれるでしょうか？",
        ok="正解！データを変えたら、表示を書き換えます。",
        ng="惜しい！データと画面は、自動ではそろいません。",
    ),
    pred(
        title="データを変えただけでは画面は変わらない", lang="javascript",
        prompt="次の HTML と JavaScript を組み合わせたページを表示したとき、ul の中の li は、いくつ表示されますか？",
        code='''const todos = [];
const list = document.querySelector("#list");
function render() {
  list.textContent = "";
  for (const t of todos) {
    const li = document.createElement("li");
    li.textContent = t;
    list.appendChild(li);
  }
}
todos.push("A");
todos.push("B");
render();
todos.push("C");''',
        check=CK('<ul id="list"></ul>', probe="document.querySelectorAll('#list > li').length"),
        choices=[
            ("3つ", "C を追加したのは render() を呼んだあとです。そのあと render を呼んでいないので、画面には反映されません。", 3),
            ("2つ", "", 2),
            ("0個", "render() は A と B を追加したあとに呼ばれているので、その時点の2つの li が作られています。", 0),
        ],
        correct=1,
        why="render() を呼んだ時点の配列（A と B）が画面になり、そのあとの C は、render を呼び直さない限り反映されないから。",
        expl="配列 todos には最終的に3つの要素がありますが、画面は、最後に render() を呼んだ時点の内容のままです。データを変えたら、もう一度 render() を呼ぶ必要があります。",
        concepts=["render", "データと表示"], diff=3,
        hint="最後の todos.push(\"C\") のあとに、render() は呼ばれていますか？",
        ok="正解！render し直さないと画面は変わりません。",
        ng="惜しい！画面が更新されるタイミングを追いましょう。",
    ),
    fill(
        title="入力値を数値にする", lang="javascript",
        prompt="2つの入力欄の値を足して、結果を表示します。ボタンを押すと 9 と表示されるように、【空欄1】と【空欄2】に入れる関数名を答えてください（どちらも同じ関数です）。",
        code='''document.querySelector("#calc").addEventListener("click", () => {
  const a = __1__(document.querySelector("#a").value);
  const b = __2__(document.querySelector("#b").value);
  document.querySelector("#result").textContent = a + b;
});''',
        check=CK('<input id="a" value="4">\n<input id="b" value="5">\n<button id="calc">足す</button>\n<p id="result"></p>', actions=[CLICK("calc")], expr="document.getElementById('result').textContent === '9'"),
        blanks=[(["Number", "parseFloat", "parseInt"], False), (["Number", "parseFloat", "parseInt"], False)],
        wrong=[("b1", "String", "String は、値を文字列にする関数です。a が文字列のままなので、a + b は連結になり、45 と表示されます。")],
        why="入力欄の value は文字列なので、Number() で数値にしてから足す必要があるから。",
        expl="Number(\"4\") は数値の 4 を返します。数値同士なら + は足し算になり、4 + 5 = 9 です。変換しないと、\"4\" + \"5\" で文字列の連結になり 45 になってしまいます。",
        concepts=["Number()", "value", "型変換"], diff=2,
        hint="文字列を数値に変える関数です。ステージ2で学びました。",
        ok="正解！入力値は Number() で数値にします。",
        ng="惜しい！入力値は文字列です。数値にする関数を使いましょう。",
    ),
    bugfix(
        title="入力欄の値が連結されてしまう", lang="javascript",
        prompt="2つの入力欄の値（1 と 2）を足して 3 を表示するつもりが、12 と表示されます。正しい直し方はどれですか？",
        code='''document.querySelector("#calc").addEventListener("click", () => {
  const a = document.querySelector("#a").value;
  const b = document.querySelector("#b").value;
  document.querySelector("#result").textContent = a + b;
});''',
        fixed='''document.querySelector("#calc").addEventListener("click", () => {
  const a = Number(document.querySelector("#a").value);
  const b = Number(document.querySelector("#b").value);
  document.querySelector("#result").textContent = a + b;
});''',
        check=CK('<input id="a" value="1">\n<input id="b" value="2">\n<button id="calc">計算</button>\n<p id="result"></p>', actions=[CLICK("calc")], expr="document.getElementById('result').textContent === '3'"),
        choices=[
            ("textContent を value に変える", "p 要素に value を代入しても、画面の文字は変わりません。原因は、a と b が文字列のままであることです。"),
            ("a と b を Number() で数値にしてから足す", ""),
            ("a + b を a - b に変える", "引き算なら、文字列が数値に変換されて計算されますが、結果は -1 で、足し算ではなくなってしまいます。"),
        ],
        correct=1, fmt="text",
        why="入力欄の value は文字列なので、+ が連結になっていたから。",
        expl="\"1\" + \"2\" は、足し算ではなく文字列の連結で \"12\" になります。Number() で数値に変換してから足すと、1 + 2 = 3 です。",
        concepts=["Number()", "文字列の連結", "value"], diff=3,
        hint="input の value は、数字を入れても、どんな型でしょう？",
        ok="正解！value は文字列なので、数値に変換します。",
        ng="惜しい！a と b の型を確認しましょう。",
    ),
    pred(
        title="toggle を2回", lang="javascript",
        prompt="次の HTML と JavaScript を組み合わせたページで、li をクリックを2回行ったあと、li は class「done」を持っていますか？ true か false で入力してください。",
        code='''const item = document.querySelector("#item");
item.addEventListener("click", () => {
  item.classList.toggle("done");
});''',
        check=CK('<ul><li id="item">買い物</li></ul>', actions=[CLICK("item")] * 2, probe="document.getElementById('item').classList.contains('done')", expected=False),
        out="false",
        wrong=[("true", "toggle は「あれば削除、なければ追加」です。1回目で追加、2回目で削除されるので、2回クリックすると元に戻ります。")],
        why="1回目のクリックで done が付き、2回目で外れるから。",
        expl="toggle は、クリックのたびに付け外しを切り替えます。奇数回のクリックでは付いていて、偶数回では付いていません。",
        concepts=["classList", "toggle", "click"], diff=2,
        hint="toggle は、あれば削除、なければ追加です。",
        ok="正解！toggle は付け外しを切り替えます。",
        ng="惜しい！1回目と2回目で、それぞれ何が起きるか考えましょう。",
    ),
    write_page(
        title="文字数カウンター", lang="javascript", fmt="javascript_dom",
        prompt="textarea（#memo）に文字を入力するたびに、入力された文字数を、#len の文字として表示してください。（最初は 0 と表示されています）",
        given_html='<textarea id="memo"></textarea>\n<p>文字数: <span id="len">0</span></p>',
        starter="// #memo と #len はあらかじめ用意されています\n",
        ref='''const memo = document.querySelector("#memo");
const len = document.querySelector("#len");
memo.addEventListener("input", () => {
  len.textContent = memo.value.length;
});''',
        alts=['''document.getElementById("memo").addEventListener("input", (e) => {
  document.getElementById("len").textContent = e.target.value.length;
});'''],
        bads=[
            ('''const memo = document.querySelector("#memo");
const len = document.querySelector("#len");
len.textContent = memo.value.length;''', "入力するたびに実行されるイベントリスナー（input）がありません。最初に1回だけ数えても、入力には反応しません。"),
            ('''const memo = document.querySelector("#memo");
const len = document.querySelector("#len");
memo.addEventListener("input", () => {
  len.textContent = memo.textContent.length;
});''', "textarea の入力内容は textContent ではなく value で読みます。textContent は空のままで、いつも 0 になります。"),
        ],
        tests=[
            t_page("「こんにちは」を入力すると 5 と表示される", "document.getElementById('len').textContent === '5'", actions=[SET_EVT("memo", "こんにちは")]),
            t_page("文字を消して空にすると 0 に戻る", "document.getElementById('len').textContent === '0'", actions=[SET_EVT("memo", "abc"), SET_EVT("memo", "")]),
            t_page("空白も1文字として数える", "document.getElementById('len').textContent === '5'", actions=[SET_EVT("memo", "a b c")], visible=False),
            t_page("入力のたびに更新される", "document.getElementById('len').textContent === '2'", actions=[SET_EVT("memo", "abcdef"), SET_EVT("memo", "ab")], visible=False),
        ],
        why="input イベントのたびに、入力欄の value の length を読んで、#len に表示するから。",
        expl="input イベントは、入力が変わるたびに起きます。textarea の中身は value で読み、length が文字数です。最初に1回だけ数えるのではなく、イベントのたびに数え直します。",
        concepts=["input イベント", "value", "length"], diff=3,
        hint="memo の input イベントで、memo.value.length を #len に入れます。",
        ok="正解！入力のたびに文字数を更新できました。",
        ng="惜しい！入力のたびに更新されるか、確認しましょう。",
    ),
    write_page(
        title="ToDo を追加する", lang="javascript", fmt="javascript_dom",
        prompt="入力欄（#todoInput）に文字を入れて「追加」ボタン（#addBtn）を押すと、その文字を内容とする li を、ul（#todoList）の末尾に追加してください。追加したら入力欄を空に戻します。空の入力、スペースだけの入力のときは、何も追加しないこと。",
        given_html=TODO_HTML,
        starter="// #todoInput, #addBtn, #todoList はあらかじめ用意されています\n",
        ref='''const input = document.querySelector("#todoInput");
const list = document.querySelector("#todoList");
document.querySelector("#addBtn").addEventListener("click", () => {
  const text = input.value.trim();
  if (text === "") {
    return;
  }
  const li = document.createElement("li");
  li.textContent = text;
  list.appendChild(li);
  input.value = "";
});''',
        alts=['''const input = document.getElementById("todoInput");
document.getElementById("addBtn").onclick = () => {
  const text = input.value.trim();
  if (text) {
    const li = document.createElement("li");
    li.textContent = text;
    document.getElementById("todoList").append(li);
    input.value = "";
  }
};'''],
        bads=[
            ('''const input = document.querySelector("#todoInput");
const list = document.querySelector("#todoList");
document.querySelector("#addBtn").addEventListener("click", () => {
  const li = document.createElement("li");
  li.textContent = input.value;
  list.appendChild(li);
  input.value = "";
});''', "空の入力や、スペースだけの入力でも、空の li が追加されてしまいます。trim() で空白を取り除いて、空なら何もしません。"),
            ('''const input = document.querySelector("#todoInput");
const list = document.querySelector("#todoList");
document.querySelector("#addBtn").addEventListener("click", () => {
  const text = input.value.trim();
  if (text === "") {
    return;
  }
  const li = document.createElement("li");
  li.textContent = text;
  list.appendChild(li);
});''', "追加したあとに、入力欄を空に戻していません。"),
        ],
        tests=[
            t_page("「牛乳」を追加すると li が1つできる", "document.querySelectorAll('#todoList > li').length === 1 && document.querySelector('#todoList > li').textContent === '牛乳'", actions=[ADD("牛乳")]),
            t_page("追加したあと、入力欄が空になる", "document.getElementById('todoInput').value === ''", actions=[ADD("牛乳")]),
            t_page("2つ追加すると、追加した順に並ぶ", "Array.from(document.querySelectorAll('#todoList > li')).map(function (l) { return l.textContent; }).join('|') === 'A|B'", actions=[ADD("A"), ADD("B")]),
            t_page("空の入力では追加されない", "document.querySelectorAll('#todoList > li').length === 0", actions=[ADD("")], visible=False),
            t_page("スペースだけの入力では追加されない", "document.querySelectorAll('#todoList > li').length === 0", actions=[ADD("   ")], visible=False),
        ],
        why="ボタンのクリックで、入力値を trim して空でなければ li を作って追加し、入力欄を空に戻すから。",
        expl="trim() で前後の空白を取り除いてから、空かどうかを確認します。空なら return で終わり、何も追加しません。追加のあとに value を空にしておくと、続けて入力できます。",
        concepts=["createElement", "appendChild", "trim", "addEventListener"], diff=4,
        hint="入力値を trim して、空なら return。空でなければ li を作って追加し、入力欄を空に戻します。",
        ok="正解！ToDo の追加ができました。",
        ng="惜しい！空の入力のとき、追加後の入力欄を確認しましょう。",
    ),
    write_page(
        title="タブの切り替え", lang="javascript", fmt="javascript_dom",
        prompt="タブ1・タブ2のボタン（class が tab）を押すと、data-target の値と同じ id のパネル（class が panel）だけが表示され、もう一方は非表示になるようにしてください。最初は p1 が表示され、p2 は非表示です。（表示・非表示は hidden 属性（el.hidden）で切り替えるのが簡単です）",
        given_html='<button class="tab" data-target="p1">タブ1</button>\n<button class="tab" data-target="p2">タブ2</button>\n<div id="p1" class="panel">内容1</div>\n<div id="p2" class="panel" hidden>内容2</div>',
        starter="// .tab と .panel はあらかじめ用意されています\n",
        ref='''const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".panel");
for (const tab of tabs) {
  tab.addEventListener("click", () => {
    for (const p of panels) {
      p.hidden = p.id !== tab.dataset.target;
    }
  });
}''',
        alts=['''document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".panel").forEach((p) => {
      p.style.display = p.id === tab.getAttribute("data-target") ? "block" : "none";
    });
  });
});'''],
        bads=[
            ('''const tabs = document.querySelectorAll(".tab");
tabs.addEventListener("click", () => {
  document.getElementById("p2").hidden = false;
  document.getElementById("p1").hidden = true;
});''', "querySelectorAll の結果には、addEventListener を直接付けられません。1つずつ取り出して付けます。また、どのタブでも p2 を見せてしまいます。"),
            ('''for (const tab of document.querySelectorAll(".tab")) {
  tab.addEventListener("click", () => {
    document.getElementById(tab.dataset.target).hidden = false;
  });
}''', "押されたタブのパネルを表示しているだけで、他のパネルを非表示にしていません。タブ2のあとにタブ1を押すと、p2 も表示されたままになります。"),
        ],
        tests=[
            t_page("最初は p1 が表示され、p2 は非表示（変更なし）", VIS("p1") + " && !" + VIS("p2")),
            t_page("タブ2を押すと p2 だけが表示される", VIS("p2") + " && !" + VIS("p1"), actions=["document.querySelectorAll('.tab')[1].click()"]),
            t_page("タブ2のあとにタブ1を押すと、p1 だけが表示される", VIS("p1") + " && !" + VIS("p2"), actions=["document.querySelectorAll('.tab')[1].click()", "document.querySelectorAll('.tab')[0].click()"], visible=False),
            t_page("同じタブを続けて押しても、表示は変わらない", VIS("p2") + " && !" + VIS("p1"), actions=["document.querySelectorAll('.tab')[1].click()", "document.querySelectorAll('.tab')[1].click()"], visible=False),
        ],
        why="クリックされたタブの data-target と同じ id のパネルだけを表示し、他のパネルは非表示にするから。",
        expl="すべてのタブにリスナーを付け、クリックされたら、すべてのパネルを見て「id が data-target と同じなら表示、違えば非表示」とします。1つだけを表示するのではなく、全パネルの状態を毎回決め直すのがポイントです。",
        concepts=["dataset", "hidden", "for...of", "イベント処理"], diff=4,
        hint="クリックのたびに、すべてのパネルについて、表示するか隠すかを決め直します。",
        ok="正解！タブの切り替えが作れました。",
        ng="惜しい！タブ2のあとにタブ1を押したときの表示を確認しましょう。",
    ),
    write_page(
        title="完了にして残りを数える", lang="javascript", fmt="javascript_dom",
        prompt="li をクリックするたびに、その li の class「done」を付けたり外したりしてください。そして、done が付いていない li の数を、#remaining の文字として表示してください（最初は 3 と表示されています）。",
        given_html='<ul id="list"><li>A</li><li>B</li><li>C</li></ul>\n<p>残り: <span id="remaining">3</span>件</p>',
        starter="// #list の li と #remaining はあらかじめ用意されています\n",
        ref='''const items = document.querySelectorAll("#list li");
const remaining = document.querySelector("#remaining");
function update() {
  let n = 0;
  for (const li of items) {
    if (!li.classList.contains("done")) {
      n++;
    }
  }
  remaining.textContent = n;
}
for (const li of items) {
  li.addEventListener("click", () => {
    li.classList.toggle("done");
    update();
  });
}''',
        alts=['''const remaining = document.getElementById("remaining");
document.getElementById("list").addEventListener("click", (e) => {
  if (e.target.tagName === "LI") {
    e.target.classList.toggle("done");
  }
  remaining.textContent = document.querySelectorAll("#list li:not(.done)").length;
});'''],
        bads=[
            ('''const items = document.querySelectorAll("#list li");
for (const li of items) {
  li.addEventListener("click", () => {
    li.classList.toggle("done");
  });
}''', "done の付け外しだけで、残りの件数の表示（#remaining）を更新していません。"),
            ('''const items = document.querySelectorAll("#list li");
const remaining = document.querySelector("#remaining");
for (const li of items) {
  li.addEventListener("click", () => {
    li.classList.add("done");
    remaining.textContent = document.querySelectorAll("#list li:not(.done)").length;
  });
}''', "classList.add だと、2回目のクリックで元に戻りません。付け外しを切り替えるには toggle を使います。"),
        ],
        tests=[
            t_page("1つ目をクリックすると done が付き、残りが 2 になる", "document.querySelectorAll('#list li')[0].classList.contains('done') && document.getElementById('remaining').textContent === '2'", actions=["document.querySelectorAll('#list li')[0].click()"]),
            t_page("もう1回クリックすると done が外れ、残りが 3 に戻る", "!document.querySelectorAll('#list li')[0].classList.contains('done') && document.getElementById('remaining').textContent === '3'", actions=["document.querySelectorAll('#list li')[0].click()", "document.querySelectorAll('#list li')[0].click()"]),
            t_page("3つすべてをクリックすると、残りが 0 になる", "document.getElementById('remaining').textContent === '0'", actions=["document.querySelectorAll('#list li')[0].click()", "document.querySelectorAll('#list li')[1].click()", "document.querySelectorAll('#list li')[2].click()"], visible=False),
            t_page("2つ目だけクリックしても、他の li には done が付かない", "!document.querySelectorAll('#list li')[0].classList.contains('done') && document.querySelectorAll('#list li')[1].classList.contains('done') && document.getElementById('remaining').textContent === '2'", actions=["document.querySelectorAll('#list li')[1].click()"], visible=False),
        ],
        why="クリックで toggle し、そのたびに done が付いていない li を数え直して表示するから。",
        expl="done の付け外し（toggle）と、残りの件数の表示（update）を、1回のクリックの中でセットで行います。件数は、付け外しのたびに数え直す方法が、間違いが起きにくい基本の形です。",
        concepts=["classList.toggle", "イベント処理", "DOM操作"], diff=4,
        hint="クリックのたびに、toggle したあと、done がない li の数を表示します。",
        ok="正解！状態の更新と表示の更新をセットで書けました。",
        ng="惜しい！2回クリックしたときの動きを確認しましょう。",
    ),
    write_page(
        title="削除ボタンつきの ToDo アプリ", lang="javascript", fmt="javascript_dom",
        prompt="次の仕様の、簡単な ToDo アプリを作ってください。\n・「追加」ボタン（#addBtn）で、入力欄（#todoInput）の文字を内容とする li を #todoList に追加する。空やスペースだけの入力は追加しない。追加後は入力欄を空に戻す。\n・各 li の中に「削除」ボタン（button 要素。class は del）を付け、押すとその li を削除する。\n・#total には、li の数を「N件」の形で常に表示する（最初は「0件」）。",
        given_html='<input id="todoInput" type="text">\n<button id="addBtn">追加</button>\n<ul id="todoList"></ul>\n<p id="total">0件</p>',
        starter="// #todoInput, #addBtn, #todoList, #total はあらかじめ用意されています\n",
        ref='''const input = document.querySelector("#todoInput");
const list = document.querySelector("#todoList");
const total = document.querySelector("#total");

function updateTotal() {
  total.textContent = list.children.length + "件";
}

document.querySelector("#addBtn").addEventListener("click", () => {
  const text = input.value.trim();
  if (text === "") {
    return;
  }
  const li = document.createElement("li");
  const span = document.createElement("span");
  span.textContent = text;
  const del = document.createElement("button");
  del.textContent = "削除";
  del.className = "del";
  del.addEventListener("click", () => {
    li.remove();
    updateTotal();
  });
  li.appendChild(span);
  li.appendChild(del);
  list.appendChild(li);
  input.value = "";
  updateTotal();
});''',
        alts=['''const input = document.getElementById("todoInput");
const list = document.getElementById("todoList");
const total = document.getElementById("total");
const refresh = () => { total.textContent = `${list.querySelectorAll("li").length}件`; };
document.getElementById("addBtn").addEventListener("click", () => {
  const text = input.value.trim();
  if (!text) return;
  const li = document.createElement("li");
  li.append(text);
  const del = document.createElement("button");
  del.className = "del";
  del.textContent = "削除";
  del.addEventListener("click", () => { li.remove(); refresh(); });
  li.append(del);
  list.append(li);
  input.value = "";
  refresh();
});'''],
        bads=[
            ('''const input = document.querySelector("#todoInput");
const list = document.querySelector("#todoList");
const total = document.querySelector("#total");
document.querySelector("#addBtn").addEventListener("click", () => {
  const text = input.value.trim();
  if (text === "") return;
  const li = document.createElement("li");
  li.textContent = text;
  const del = document.createElement("button");
  del.className = "del";
  del.textContent = "削除";
  del.addEventListener("click", () => { li.remove(); });
  li.appendChild(del);
  list.appendChild(li);
  input.value = "";
  total.textContent = list.children.length + "件";
});''', "削除したときに、#total の件数を更新していません。追加と削除のどちらでも、件数の表示を更新します。"),
            ('''const input = document.querySelector("#todoInput");
const list = document.querySelector("#todoList");
const total = document.querySelector("#total");
document.querySelector("#addBtn").addEventListener("click", () => {
  const text = input.value.trim();
  if (text === "") return;
  const li = document.createElement("li");
  li.textContent = text;
  list.appendChild(li);
  input.value = "";
  total.textContent = list.children.length + "件";
});''', "各 li に、削除ボタン（class が del の button）がありません。"),
        ],
        tests=[
            t_page("1つ追加すると、li が1つと「1件」になる", "document.querySelectorAll('#todoList > li').length === 1 && document.getElementById('total').textContent === '1件'", actions=[ADD("A")]),
            t_page("2つ追加すると「2件」で、1つ目に A が含まれる", "document.getElementById('total').textContent === '2件' && document.querySelectorAll('#todoList > li')[0].textContent.indexOf('A') >= 0", actions=[ADD("A"), ADD("B")]),
            t_page("削除ボタンで、その li が消えて「1件」になる", "document.querySelectorAll('#todoList > li').length === 1 && document.querySelector('#todoList > li').textContent.indexOf('B') >= 0 && document.getElementById('total').textContent === '1件'", actions=[ADD("A"), ADD("B"), "document.querySelectorAll('#todoList .del')[0].click()"]),
            t_page("空やスペースだけの入力では追加されず、「0件」のまま", "document.querySelectorAll('#todoList > li').length === 0 && document.getElementById('total').textContent === '0件'", actions=[ADD(""), ADD("  ")], visible=False),
            t_page("3つ追加して真ん中を削除すると、A と C が残り「2件」", "Array.from(document.querySelectorAll('#todoList > li')).map(function (l) { return l.textContent.indexOf('A') >= 0 ? 'A' : (l.textContent.indexOf('C') >= 0 ? 'C' : '?'); }).join('') === 'AC' && document.getElementById('total').textContent === '2件'", actions=[ADD("A"), ADD("B"), ADD("C"), "document.querySelectorAll('#todoList .del')[1].click()"], visible=False),
            t_page("追加後に入力欄が空になる", "document.getElementById('todoInput').value === ''", actions=[ADD("A")], visible=False),
        ],
        why="追加・削除のどちらでも件数を更新し、各 li に削除ボタンを持たせて、そのクリックで li を消すから。",
        expl="追加の処理と削除の処理の両方から、updateTotal() のような「表示を更新する関数」を呼ぶのがポイントです。関数に分けておくと、同じ処理を何度も書かずに済みます。ここまでの知識を組み合わせて、一通りのアプリが書けました。",
        concepts=["DOM操作", "イベント処理", "関数", "createElement", "remove"], diff=5,
        hint="追加と削除の両方のあとに、件数の表示を更新する関数を呼びます。",
        ok="正解！JavaScript の学習はここまでです。おめでとうございます！",
        ng="惜しい！削除したときの件数の表示を確認しましょう。",
    ),
]
