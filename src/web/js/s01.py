from lib_web import mc, pred, fill, bugfix, write_js, t_js_out

STAGE = {
    "number": 1,
    "title": "変数とデータ型",
    "subtitle": "console.log、let / const、データ型",
    "goals": [
        "JavaScript がブラウザの中で動くプログラミング言語であることを説明できる",
        "console.log で値をコンソールに表示できる",
        "let と const で変数を宣言し、値を入れたり変更したりできる",
        "数値・文字列・真偽値・undefined・null というデータ型を区別できる",
        "typeof で型を調べられる",
        "最初のエラー（ReferenceError / TypeError）の原因を推測できる",
    ],
    "prerequisites": ["特になし（HTML と CSS を少し知っていると、ステージ8以降が分かりやすくなります）"],
    "topics": [
        "JavaScript とは（HTML・CSS との役割の違い）",
        "動かす場所（<script> タグ、開発者ツールのコンソール）",
        "console.log とコメント",
        "let と const",
        "データ型（number / string / boolean / undefined / null）",
        "typeof",
    ],
    "pitfalls": [
        "console.log の出力はページの画面ではなく、開発者ツールのコンソールに出る",
        "const の変数に再代入するとエラー（TypeError）になる",
        "変数名の大文字・小文字は区別される（userName と username は別）",
        "引用符で囲まない文字は変数名として扱われ、ReferenceError になる",
        "\"42\"（文字列）と 42（数値）は別のデータ型",
    ],
    "next_links": ["変数の値を計算・比較する「演算子」（ステージ2）の土台になります"],
    "lesson": {
        "intro": "Webページの文章や構造は HTML、見た目は CSS で作ります。そこに「動き」を足すのが JavaScript です。ボタンを押したら表示が変わる、入力内容をチェックする、といったことができます。まずはコードを書いて結果を確かめる基本の道具、console.log と変数から始めましょう。",
        "sections": [
            {
                "id": "S01-L1",
                "title": "JavaScript と console.log",
                "read_minutes": 3,
                "body": [
                    "JavaScript は、Webブラウザの中で動くプログラミング言語です。HTML がページの構造、CSS が見た目を担当し、JavaScript が動きや計算を担当します（HTML と CSS はプログラミング言語ではなく、それぞれマークアップ言語・スタイルシート言語と呼びます）。",
                    "コードを動かす場所は2つあります。1つは HTML の中の <script> タグ、もう1つはブラウザの開発者ツール（多くのブラウザで F12 キー）にある「コンソール」です。このコースの問題では、書いたコードが自動で実行されます。",
                    "console.log(値) と書くと、値が開発者ツールのコンソールに表示されます。ページの画面には表示されません。結果を確かめるときの一番基本の道具です。複数の値を , で区切ると、間に空白を入れて1行に表示されます。",
                    "// から行末まではコメントで、実行されません。文の終わりには ; （セミコロン）を付けるのが一般的です。JavaScript は大文字と小文字を区別します（console.log は正しく、Console.log はエラーです）。",
                ],
                "glossary": [
                    {"term": "コンソール", "definition": "開発者ツールの中にある、メッセージやエラーを確認する画面。"},
                    {"term": "文", "definition": "実行の1つのまとまり。ふつう ; で終える。"},
                    {"term": "コメント", "definition": "// で始まる、人間向けのメモ。実行されない。"},
                ],
                "examples": [
                    {
                        "id": "S01-E1", "title": "いちばん短いコード", "language": "javascript",
                        "code": '''console.log("Hello");
console.log(10);
console.log("a", "b");''',
                        "expected_output": "Hello\n10\na b",
                        "line_notes": ["1行目: 文字列 Hello を表示します（引用符は表示されません）。", "2行目: 数値は引用符なしで書けます。", "3行目: カンマで区切ると、間に空白を入れて1行に表示されます。"],
                    },
                    {
                        "id": "S01-E2", "title": "HTMLの中に書く（script タグ）", "language": "html",
                        "code": '''<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>はじめて</title></head>
<body>
  <p>画面にはこの文章だけが表示されます</p>
  <script>
    console.log("コンソールに表示されます");
  </script>
</body>
</html>''',
                        "expected_output": "",
                        "line_notes": ["6〜8行目: <script> タグの中に JavaScript を書きます。", "console.log の結果は画面ではなく、開発者ツールのコンソールに出ます。"],
                        "preview": {"format": "html_document"},
                        "verify": {"format": "html_document", "expr": "document.scripts.length === 1 && document.querySelector('p').textContent.includes('画面')"},
                    },
                    {
                        "id": "S01-E3", "title": "コメント", "language": "javascript",
                        "code": '''// あいさつを表示する
console.log("Hi"); // 行の途中からでもOK
// console.log("Bye");''',
                        "expected_output": "Hi",
                        "line_notes": ["// 以降は実行されません。3行目のようにコードを一時的に無効にするのにも使えます。"],
                    },
                ],
            },
            {
                "id": "S01-L2",
                "title": "変数とデータ型",
                "read_minutes": 3,
                "body": [
                    "変数は、値に付ける名前です。let 名前 = 値; で宣言して値を入れます。あとから値を変えたいときは、let の変数に再び = で代入します。値を変えない変数は const で宣言します。const の変数に再代入するとエラー（TypeError）になります。",
                    "変数名には英字・数字・_ ・$ が使えますが、数字で始められません。大文字と小文字は区別されます。単語をつなぐときは userName のように、2語目の頭を大文字にする書き方（キャメルケース）が一般的です。",
                    "値には種類（データ型）があります。数値は number、文字列は string（\"\" か '' か `` で囲む）、真偽値は boolean（true / false）です。値がまだ入っていない変数は undefined、「意図的に空」を表す値は null です。",
                    "typeof 値 で型を調べられます。\"42\" のように引用符で囲むと数値ではなく文字列です。",
                ],
                "glossary": [
                    {"term": "変数", "definition": "値に付けた名前。"},
                    {"term": "宣言", "definition": "let や const で変数を作ること。"},
                    {"term": "データ型", "definition": "値の種類。number、string、boolean など。"},
                    {"term": "undefined", "definition": "値がまだ入っていないことを表す値。"},
                ],
                "examples": [
                    {
                        "id": "S01-E4", "title": "let と const", "language": "javascript",
                        "code": '''let score = 50;
score = 80;
const name = "Hana";
console.log(score);
console.log(name);''',
                        "expected_output": "80\nHana",
                        "line_notes": ["2行目: let の変数には、あとから値を入れ直せます（上書き）。", "3行目: const の変数は、あとから変更できません。"],
                    },
                    {
                        "id": "S01-E5", "title": "データ型を調べる", "language": "javascript",
                        "code": '''console.log(typeof 42);
console.log(typeof "42");
console.log(typeof true);
let x;
console.log(x);
console.log(typeof x);
console.log(typeof null);''',
                        "expected_output": "number\nstring\nboolean\nundefined\nundefined\nobject",
                        "line_notes": ["2行目: 引用符で囲んだ \"42\" は文字列です。", "4〜6行目: 値を入れていない変数は undefined です。", "7行目: typeof null が \"object\" になるのは、JavaScript の歴史的な仕様です。null の型は覚えなくても構いません。"],
                    },
                    {
                        "id": "S01-E6", "title": "const に再代入するとエラー", "language": "javascript",
                        "code": '''const price = 100;
price = 200;''',
                        "expected_output": "",
                        "expected_error": "TypeError",
                        "line_notes": ["const の変数に再代入すると TypeError（Assignment to constant variable）になります。"],
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "const の変数を書き換える", "wrong_code": "const count = 0;\ncount = 1;", "why": "const は再代入できず TypeError になります。書き換える変数は let で宣言します。", "fix": "let count = 0;"},
            {"title": "引用符を付け忘れる", "wrong_code": "let greeting = Hello;", "why": "引用符がない Hello は変数名と見なされ、ReferenceError になります。", "fix": "let greeting = \"Hello\";"},
            {"title": "大文字・小文字の違い", "wrong_code": "let userName = \"Hana\";\nconsole.log(username);", "why": "userName と username は別の名前です。宣言されていない名前を使うと ReferenceError になります。", "fix": "console.log(userName);"},
            {"title": "同じ名前を二重に宣言する", "wrong_code": "let a = 1;\nlet a = 2;", "why": "同じスコープで let の同名宣言はできず、SyntaxError になります。2回目は代入だけにします。", "fix": "let a = 1;\na = 2;"},
        ],
        "checkpoints": [
            "JavaScript はブラウザで動くプログラミング言語（HTML・CSS とは役割が違う）",
            "console.log の出力はコンソールに出る",
            "let は再代入できる、const は再代入できない",
            "number / string / boolean / undefined / null",
            "typeof で型を調べられる",
            "大文字と小文字は区別される",
        ],
        "next_bridge": "変数に値を入れられるようになりました。問題で、コードを読んで結果を予想したり、エラーの原因を探したりしてみましょう。",
    },
}

QUESTIONS = [
    mc(
        title="console.log の出力先", lang="javascript",
        prompt="JavaScript の console.log(\"こんにちは\") を実行すると、どこに表示されますか？",
        choices=[
            ("Webページの画面（本文）に文字が表示される", "ページの画面に表示するには、DOM（ステージ8）を使って要素の中身を書き換えます。console.log の出力は画面には出ません。"),
            ("ブラウザの開発者ツールのコンソールに表示される", ""),
            ("ポップアップのダイアログが開いて表示される", "ダイアログを出すのは alert という別の命令です。console.log は静かにコンソールへ出力します。"),
        ],
        correct=1,
        why="console.log は開発者ツールのコンソールに値を出力する命令だから。",
        expl="console.log は、プログラムの途中の値や結果を確かめるために、コンソールへメッセージを書き出します。ユーザーに見せる画面の表示とは別のものです。",
        concepts=["console.log", "コンソール"], diff=1,
        hint="ユーザー向けの画面ではなく、作る人が確認するための場所です。",
        ok="正解！console.log の出力先はコンソールです。",
        ng="惜しい！console.log はページの画面ではなく、コンソールに出力します。",
    ),
    pred(
        title="文字列と数値の表示", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''console.log("A");
console.log(10);
console.log("10");''',
        choices=[
            ("A 10 10", "console.log は呼ぶたびに改行して次の行へ出力します。3つの console.log は1行にならず、3行になります。"),
            ("\"A\"\n10\n\"10\"", "文字列を console.log に渡すと、引用符は表示されません。引用符は「これは文字列」と JavaScript に伝えるための目印です。"),
            ("A\n10\n10", ""),
        ],
        correct=2,
        why="console.log は1回ごとに改行し、文字列の引用符は表示しないから。",
        expl="数値の 10 と文字列の \"10\" は型が違いますが、console.log ではどちらも 10 と表示されます。型の違いは typeof で調べられます。",
        concepts=["console.log", "文字列", "数値"], diff=1,
        hint="console.log は1回ごとに1行ずつ出力します。引用符は表示されるでしょうか？",
        ok="正解！1回ごとに1行、引用符なしで表示されます。",
        ng="惜しい！console.log は1回ごとに改行し、引用符は表示しません。",
    ),
    mc(
        title="let と const の使い分け", lang="javascript",
        prompt="あとから値を変更しない（再代入しない）変数を宣言するとき、基本的に使うキーワードはどれですか？",
        fmt="code",
        choices=[
            ("let", "let は、あとから値を入れ直したい変数に使います。変更しない変数には、間違って書き換えるのを防げる const が向いています。"),
            ("var", "var は古い書き方で、スコープの扱いが分かりにくいため、現在は let と const を使うのが基本です。"),
            ("const", ""),
        ],
        correct=2,
        why="再代入しない値は const で宣言すると、誤って書き換えるとエラーで気づけるから。",
        expl="const は「定数」のように、あとから別の値を代入できない変数です。まず const で宣言し、値を変える必要があるときだけ let にする、という使い分けが一般的です。",
        concepts=["const", "let"], diff=1,
        hint="「変更しない」を表す英単語 constant の短縮形です。",
        ok="正解！変更しない値は const です。",
        ng="惜しい！再代入しない変数には const を使います。",
    ),
    pred(
        title="変数への再代入", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください。",
        code='''let score = 50;
score = 80;
console.log(score);''',
        out="80",
        wrong=[("50", "2行目で score に 80 が代入し直されています。let の変数は上書きできます。"), ("score", "console.log(score) は変数の名前ではなく、中に入っている値を表示します。")],
        why="let の変数に 80 が上書きされ、その値が表示されるから。",
        expl="let で宣言した変数は、あとから = で値を入れ直せます。2行目で 50 が 80 に置き換わるので、3行目では 80 が表示されます。",
        concepts=["let", "再代入"], diff=1,
        hint="2行目を実行すると、score の中身はどうなりますか？",
        ok="正解！let の変数は上書きできます。",
        ng="惜しい！2行目で score に何が入るか確認しましょう。",
    ),
    bugfix(
        title="const に再代入してしまう", lang="javascript",
        prompt="次のコードは TypeError になり、200 が表示されません。200 が表示されるようにする直し方はどれですか？",
        code='''const price = 100;
price = 200;
console.log(price);''',
        fixed='''let price = 100;
price = 200;
console.log(price);''', out="200", err="TypeError",
        choices=[
            ("price = 200 を price == 200 に変える", "== は等しいか調べる記号で、値は代入されません。エラーは消えますが、表示されるのは 100 のままです。"),
            ("const を let に変える", ""),
            ("console.log(price) の後ろの ; を消す", "セミコロンは関係ありません。エラーの原因は、const の変数への再代入です。"),
        ],
        correct=1, fmt="text",
        why="再代入したい変数は const ではなく let で宣言する必要があるから。",
        expl="const で宣言した変数は、あとから別の値を入れられません。値を変えたい price は let にします。エラーメッセージの Assignment to constant variable は「定数への代入」という意味です。",
        concepts=["const", "let", "TypeError"], diff=2,
        hint="エラーは2行目です。price は const で宣言されています。",
        ok="正解！変更する変数は let で宣言します。",
        ng="惜しい！エラーの原因は const への再代入です。",
    ),
    pred(
        title="typeof で型を調べる", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''console.log(typeof 42);
console.log(typeof "42");
console.log(typeof true);''',
        choices=[
            ("number\nnumber\nboolean", "\"42\" は引用符で囲まれているので、数値ではなく文字列（string）です。"),
            ("number\nstring\nstring", "true は引用符で囲まれていないので文字列ではなく、真偽値（boolean）です。"),
            ("number\nstring\nboolean", ""),
        ],
        correct=2,
        why="42 は number、\"42\" は string、true は boolean だから。",
        expl="見た目が数字でも、引用符で囲むと文字列になります。true と false は引用符なしで書く真偽値です。",
        concepts=["typeof", "データ型"], diff=2,
        hint="引用符で囲まれているかどうかに注目しましょう。",
        ok="正解！引用符の有無で型が変わります。",
        ng="惜しい！引用符で囲むと文字列、囲まなければ数値や真偽値です。",
    ),
    fill(
        title="文字列を変数に入れる", lang="javascript",
        prompt="変数 greeting に文字列 Hello を入れて、コンソールに Hello と表示したい。【空欄1】に入れるものを答えてください。",
        code='''let greeting = __1__;
console.log(greeting);''',
        blanks=[(['"Hello"', "'Hello'", "`Hello`"], True)],
        out="Hello",
        wrong=[("b1", "Hello", "引用符がない Hello は変数名と見なされます。そのような変数は宣言されていないので ReferenceError になります。")],
        why="文字列は引用符（\"\"・''・``）で囲んで書くから。",
        expl="引用符は「ここからここまでは文字列」という目印です。\"Hello\"、'Hello'、`Hello` のどれでも文字列になります。目印がない Hello は、変数の名前だと解釈されます。",
        concepts=["文字列", "引用符"], diff=1,
        hint="文字列を表すには、何で囲みますか？",
        ok="正解！文字列は引用符で囲みます。",
        ng="惜しい！引用符も含めて入力してみましょう。",
    ),
    pred(
        title="undefined と null", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''let a;
let b = null;
console.log(a);
console.log(b);''',
        out="undefined\nnull",
        wrong=[("null\nnull", "値を入れていない変数 a は undefined です。null は、自分で代入したときだけの値です。"), ("0\n0", "値が入っていない変数は 0 ではなく undefined、null も 0 ではありません。")],
        why="値を入れていない変数は undefined、null を代入した変数は null になるから。",
        expl="let a; のように値を決めずに宣言すると、a は undefined になります。b = null は「意図的に空にした」ことを表します。どちらも「値がない」状態ですが、別の値です。",
        concepts=["undefined", "null"], diff=2,
        hint="a には値を代入していません。",
        ok="正解！undefined と null は別の値です。",
        ng="惜しい！値を代入していない変数の中身を考えましょう。",
    ),
    bugfix(
        title="変数名の大文字・小文字", lang="javascript",
        prompt="変数 userName の値を表示するはずが ReferenceError になります。2行目を正しく書き直して入力してください（2行目の内容だけを入力）。",
        code='''let userName = "Hana";
console.log(username);''',
        fixed='''let userName = "Hana";
console.log(userName);''', out="Hana", err="ReferenceError",
        target_line=2, accepted=["console.log(userName);", "console.log(userName)"],
        wrong=[("console.log(username);", "元のコードのままです。username と userName は大文字・小文字が違うので別の名前です。")],
        why="変数名は大文字と小文字を区別するため、宣言した名前と同じ綴りで書く必要があるから。",
        expl="ReferenceError: username is not defined は「username という名前は定義されていない」という意味です。宣言したのは userName（N が大文字）なので、同じ綴りで書きます。",
        concepts=["変数名", "ReferenceError", "大文字小文字"], diff=2,
        hint="宣言した変数名と、使っている変数名を1文字ずつ比べましょう。",
        ok="正解！変数名は大文字・小文字まで同じにします。",
        ng="惜しい！宣言した名前と一文字ずつ見比べましょう。",
    ),
    write_js(
        title="変数を使って表示する", lang="javascript",
        prompt="変数 city に文字列 \"東京\"、変数 population に数値 14000000 を入れてください。そのあと console.log で city と population を、この順に別々の行に表示してください。変数は let または const で宣言すること。",
        starter="// ここに書きましょう\n",
        ref='''const city = "東京";
const population = 14000000;
console.log(city);
console.log(population);''',
        alts=['''let city = '東京';
let population = 14000000;
console.log(city);
console.log(population);'''],
        bads=[
            ('''console.log("東京");
console.log(14000000);''', "変数を使っていません。変数に入れてから、変数を表示するコードにしましょう。"),
            ('''let city = "東京";
let population = 14000000;
console.log(city, population);''', "カンマで区切ると同じ行に空白区切りで表示されます。別々の行にするには console.log を2回使います。"),
        ],
        req=[(r"\b(let|const)\s+city\b", "city を let か const で宣言してください"), (r"\b(let|const)\s+population\b", "population を let か const で宣言してください")],
        tests=[t_js_out("東京\n14000000\n")],
        why="変数に値を入れ、console.log を2回使えば、1行ずつ表示されるから。",
        expl="let（または const）で変数を2つ宣言して値を入れ、console.log(city); console.log(population); と書きます。console.log は呼び出すたびに改行するので、2行になります。",
        concepts=["let", "const", "変数", "console.log"], diff=2,
        hint="変数を2つ宣言してから、console.log を2回使います。",
        ok="正解！変数を使って表示できました。",
        ng="惜しい！変数を宣言しているか、別々の行になっているか確認しましょう。",
    ),
]
