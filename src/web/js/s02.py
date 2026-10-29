from lib_web import mc, pred, fill, bugfix, write_js, t_js_out

STAGE = {
    "number": 2,
    "title": "演算子",
    "subtitle": "計算・文字列の連結・比較・論理演算",
    "goals": [
        "算術演算子（+ - * / % **）で計算できる",
        "+= などの代入演算子と、文字列の連結・テンプレートリテラルを使える",
        "=（代入）と ===（比較）の違いを説明できる",
        "&&（かつ）・||（または）・!（否定）を使える",
        "文字列と数値が混ざったときの動き（型変換）と NaN を理解する",
    ],
    "prerequisites": ["console.log（ステージ1）", "let / const とデータ型（ステージ1）"],
    "topics": [
        "算術演算子（+ - * / % **）と計算の優先順位",
        "代入演算子（= += -= など）と ++ / --",
        "文字列の連結（+）とテンプレートリテラル",
        "比較演算子（=== !== < > <= >=）と ==",
        "論理演算子（&& || !）",
        "型変換（Number()）と NaN",
    ],
    "pitfalls": [
        "/ は整数除算ではない（7 / 2 は 3.5）",
        "\"5\" + 3 は 8 ではなく文字列の \"53\" になる",
        "等しいかの比較は ===（= は代入）",
        "== は型を自動で変換して比べるため、=== を使うのが基本",
        "テンプレートリテラルはバッククォート（`）で囲む。\"...\" では ${ } が使えない",
    ],
    "next_links": ["比較や論理演算の結果（true / false）を使って、処理を分岐させます（ステージ3）"],
    "lesson": {
        "intro": "変数に入れた値を、計算したり、つなげたり、比べたりするのが演算子です。次のステージの「条件分岐」は、ここで学ぶ比較演算子と論理演算子の結果を使って動きます。",
        "sections": [
            {
                "id": "S02-L1",
                "title": "計算・代入・文字列の連結",
                "read_minutes": 3,
                "body": [
                    "算術演算子は + - * / % ** です。% は割った余り、** は累乗（べき乗）です。JavaScript の / は小数まで計算する割り算で、7 / 2 は 3.5 になります（整数の商を返す演算子はありません）。掛け算・割り算は足し算・引き算より先に計算され、( ) で順序を変えられます。",
                    "x += 5 は x = x + 5 の短い書き方です。-= *= /= も同様で、x++ は x に 1 を足す書き方です。",
                    "文字列同士を + でつなぐと、文字列の連結になります。文字列と数値を + でつなぐと、数値が文字列になって連結されます（\"5\" + 3 は \"53\"）。変数を文字列に埋め込むには、バッククォート ` で囲んだテンプレートリテラルの中に ${式} と書くのが読みやすい方法です。",
                ],
                "glossary": [
                    {"term": "演算子", "definition": "+ や * など、計算や比較を表す記号。"},
                    {"term": "代入演算子", "definition": "= や += のように、変数に値を入れる演算子。"},
                    {"term": "テンプレートリテラル", "definition": "バッククォート（`）で囲み、${ } で値を埋め込める文字列。"},
                ],
                "examples": [
                    {
                        "id": "S02-E1", "title": "いろいろな計算", "language": "javascript",
                        "code": '''console.log(7 + 2);
console.log(7 / 2);
console.log(7 % 2);
console.log(2 ** 3);
console.log(2 + 3 * 4);
console.log((2 + 3) * 4);''',
                        "expected_output": "9\n3.5\n1\n8\n14\n20",
                        "line_notes": ["2行目: / は小数も含めた割り算です。", "3行目: % は余りです。", "5〜6行目: 掛け算が先。( ) で順序を変えられます。"],
                    },
                    {
                        "id": "S02-E2", "title": "代入演算子と文字列", "language": "javascript",
                        "code": '''let total = 10;
total += 5;
total++;
console.log(total);
const name = "Hana";
const age = 12;
console.log("名前: " + name);
console.log(`${name}さんは${age}歳です`);
console.log("5" + 3);''',
                        "expected_output": "16\n名前: Hana\nHanaさんは12歳です\n53",
                        "line_notes": ["2行目: total = total + 5 と同じ。3行目: ++ は 1 増やします。", "8行目: テンプレートリテラルの ${ } の部分が変数の値に置き換わります。", "9行目: 文字列と数値の + は連結になるので、結果は 8 ではなく \"53\" です。"],
                    },
                ],
            },
            {
                "id": "S02-L2",
                "title": "比較・論理演算子と型変換",
                "read_minutes": 3,
                "body": [
                    "比較演算子は結果が true か false になります。等しいかは === 、等しくないかは !== 、大小は < > <= >= です。= は代入なので、比較には使えません。",
                    "== も等しいかを調べますが、型が違うと自動で変換して比べるため、5 == \"5\" が true になるなど分かりにくい結果になります。=== は型も含めて比べるので、基本は === を使います。",
                    "論理演算子は && （かつ）、|| （または）、! （否定）です。a && b は両方 true のときだけ true、a || b はどちらか一方でも true なら true です。",
                    "- * / を使うと、文字列は数値に自動変換されます（\"10\" / 2 は 5）。数値にできない文字列だと NaN（Not a Number）になります。自分で変換するときは Number(\"10\") を使います。",
                ],
                "glossary": [
                    {"term": "===", "definition": "型も含めて等しいかを調べる比較演算子（厳密等価）。"},
                    {"term": "型変換", "definition": "値のデータ型が、自動または Number() などで別の型に変わること。"},
                    {"term": "NaN", "definition": "数値として計算できなかったときの値（Not a Number）。typeof は number。"},
                ],
                "examples": [
                    {
                        "id": "S02-E3", "title": "比較と論理演算", "language": "javascript",
                        "code": '''console.log(5 === 5);
console.log(5 === "5");
console.log(5 == "5");
console.log(5 !== 3);
console.log(3 > 2 && 2 > 5);
console.log(3 > 2 || 2 > 5);
console.log(!true);''',
                        "expected_output": "true\nfalse\ntrue\ntrue\nfalse\ntrue\nfalse",
                        "line_notes": ["2行目: 数値の 5 と文字列の \"5\" は、=== では等しくありません。", "3行目: == は型を変換して比べるので true になります（分かりにくいため使わないのが基本です）。"],
                    },
                    {
                        "id": "S02-E4", "title": "型変換と NaN", "language": "javascript",
                        "code": '''console.log("10" / 2);
console.log("abc" * 2);
console.log(Number("10") + 5);
console.log("10" + 5);
console.log(typeof NaN);''',
                        "expected_output": "5\nNaN\n15\n105\nnumber",
                        "line_notes": ["1行目: / は文字列を数値に変換して計算します。", "2行目: 数値にできない文字列との計算は NaN になります。", "3〜4行目: Number() で数値にすると足し算になり、しないと連結になります。"],
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "= と === の取り違え", "wrong_code": "console.log(n = 5);", "why": "= は代入です。n に 5 を入れた結果（5）が表示されます。等しいかを調べるには ===。", "fix": "console.log(n === 5);"},
            {"title": "文字列と数値の足し算", "wrong_code": "console.log(\"3\" + 4);", "why": "文字列と数値を + でつなぐと、連結になり \"34\" になります。計算したいときは Number() で数値にします。", "fix": "console.log(Number(\"3\") + 4);"},
            {"title": "テンプレートリテラルで引用符を使う", "wrong_code": "console.log(\"${name}さん\");", "why": "\" \" の中では ${ } は展開されず、そのまま表示されます。バッククォート（`）で囲みます。", "fix": "console.log(`${name}さん`);"},
            {"title": "整数の割り算を期待する", "wrong_code": "console.log(7 / 2);  // 3 と思い込む", "why": "JavaScript の / は小数も計算し、3.5 になります。切り捨てたいときは Math.floor(7 / 2) を使います。", "fix": "console.log(Math.floor(7 / 2));"},
        ],
        "checkpoints": [
            "/ は小数も計算する、% は余り、** は累乗",
            "+= や ++ で変数を更新できる",
            "文字列 + 数値 は連結になる",
            "等しいかは ===（= は代入）",
            "&& は かつ、|| は または、! は否定",
            "数値にできない計算は NaN になる",
        ],
        "next_bridge": "比較や論理演算の結果は true / false になります。問題で、式の結果を正確に読み取る練習をしましょう。",
    },
}

QUESTIONS = [
    pred(
        title="割り算・余り・累乗", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''console.log(7 / 2);
console.log(7 % 2);
console.log(2 ** 3);''',
        choices=[
            ("3\n1\n8", "JavaScript の / は小数まで計算する割り算なので、7 / 2 は 3 ではなく 3.5 です。"),
            ("3.5\n1\n6", "** は累乗です。2 ** 3 は 2 を3回かける 8 で、2 × 3 の 6 ではありません。"),
            ("3.5\n1\n8", ""),
        ],
        correct=2,
        why="7 / 2 は 3.5、7 % 2 は余り 1、2 ** 3 は 8 だから。",
        expl="JavaScript の割り算は小数も含めて計算します。余りは %、累乗は ** で求めます。整数の商だけが欲しいときは Math.floor(7 / 2) のように別の方法を使います。",
        concepts=["算術演算子", "%", "**"], diff=1,
        hint="7 を 2 で割ると、商は 3、余りは 1 ですが、/ は小数まで出します。",
        ok="正解！/ は小数まで計算します。",
        ng="惜しい！/ と % と ** の意味をもう一度確認しましょう。",
    ),
    pred(
        title="文字列と数値の計算", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''console.log("5" + 3);
console.log("5" - 3);
console.log(5 + 3);''',
        out="53\n2\n8",
        wrong=[("8\n2\n8", "\"5\" + 3 は、文字列と数値の + なので、足し算ではなく連結になり \"53\" です。"), ("53\n53\n8", "- は連結には使えず、文字列を数値に変換して引き算します。\"5\" - 3 は 2 です。")],
        why="+ は文字列があると連結、- は数値に変換して引き算になるから。",
        expl="+ は「足し算」と「文字列の連結」の両方に使われるため、片方が文字列だと連結になります。- には連結の意味がないので、文字列は数値に変換されて計算されます。",
        concepts=["文字列の連結", "型変換"], diff=2,
        hint="+ は、片方が文字列のときどう働くでしょう？ - は？",
        ok="正解！+ は文字列があると連結になります。",
        ng="惜しい！+ と - で動きが違う点に注目しましょう。",
    ),
    mc(
        title="テンプレートリテラルの書き方", lang="javascript",
        prompt="変数 age に 20 が入っています。「私は20歳です」と表示するために、変数を文字列に埋め込む正しい書き方はどれですか？",
        code='''const age = 20;''',
        fmt="code",
        choices=[
            ('console.log("私は${age}歳です");', "ダブルクォート \" \" の中では ${ } は展開されず、「私は${age}歳です」とそのまま表示されます。"),
            ("console.log(`私は{age}歳です`);", "バッククォートは正しいですが、${ } の $ が抜けています。「私は{age}歳です」とそのまま表示されます。"),
            ("console.log(`私は${age}歳です`);", ""),
        ],
        correct=2,
        why="変数を埋め込めるのは、バッククォートで囲んだ中の ${ } だけだから。",
        expl="テンプレートリテラルは、バッククォート ` で文字列を囲み、${式} の部分に値を埋め込みます。日本語キーボードでは Shift + @ キーで入力できます。",
        concepts=["テンプレートリテラル"], diff=2,
        hint="埋め込みには、バッククォートと ${ } の両方が必要です。",
        ok="正解！バッククォートと ${ } の組み合わせです。",
        ng="惜しい！囲む記号と、埋め込みの書き方の両方を確認しましょう。",
    ),
    pred(
        title="比較演算子の結果", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''console.log(5 === "5");
console.log(5 == "5");
console.log(5 !== 3);''',
        choices=[
            ("true\ntrue\ntrue", "=== は型も比べます。数値の 5 と文字列の \"5\" は型が違うので false です。"),
            ("false\ntrue\ntrue", ""),
            ("false\nfalse\ntrue", "== は型を自動で変換して比べるので、5 == \"5\" は true になります。だから === を使うのが基本です。"),
        ],
        correct=1,
        why="=== は型も比べて false、== は型を変換して true、!== は等しくないので true だから。",
        expl="== と === の違いは「型を変換して比べるか」です。== は予想しにくい結果になることがあるため、比較には基本的に === と !== を使います。",
        concepts=["===", "==", "!=="], diff=2,
        hint="=== は型まで同じかを確認します。",
        ok="正解！=== は型も含めて比べます。",
        ng="惜しい！== と === の違いを思い出しましょう。",
    ),
    fill(
        title="変数に足し込む", lang="javascript",
        prompt="変数 total に 5 を足して、15 と表示したい。【空欄1】に入れる演算子を答えてください。",
        code='''let total = 10;
total __1__ 5;
console.log(total);''',
        blanks=[(["+="], False)],
        out="15",
        wrong=[("b1", "=", "= は代入なので、total が 5 に上書きされ、5 と表示されます。足し込むには += を使います。")],
        why="+= は、左の変数に右の値を足して代入し直す演算子だから。",
        expl="total += 5 は total = total + 5 と同じです。-= *= /= も同じ考え方です。",
        concepts=["代入演算子", "+="], diff=1,
        hint="「足して代入」の記号です。",
        ok="正解！+= で足し込めます。",
        ng="惜しい！= だけだと上書きになります。",
    ),
    pred(
        title="論理演算子", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''console.log(true && false);
console.log(true || false);
console.log(!true);''',
        out="false\ntrue\nfalse",
        wrong=[("true\ntrue\ntrue", "&& は両方が true のときだけ true、! は true と false を反転します。"), ("false\ntrue\ntrue", "! は反転するので、!true は false です。")],
        why="&& は両方 true で true、|| は片方が true で true、! は反転するから。",
        expl="&&（かつ）は両方が true のときだけ true です。||（または）は一方でも true なら true です。!（否定）は true と false を入れ替えます。",
        concepts=["&&", "||", "!"], diff=2,
        hint="&& は「かつ」、|| は「または」です。",
        ok="正解！論理演算子を正しく読めています。",
        ng="惜しい！&&・||・! の意味を確認しましょう。",
    ),
    bugfix(
        title="比較したつもりが代入", lang="javascript",
        prompt="変数 n が 5 かどうかを調べて true と表示したいのに、5 と表示されます。2行目を直したものはどれですか？",
        code='''let n = 5;
console.log(n = 5);''',
        fixed='''let n = 5;
console.log(n === 5);''', out="true", buggy_out="5", target_line=2,
        choices=[
            ("console.log(n === 5);", ""),
            ("console.log(n == = 5);", "== と = の間に空白があると、1つの演算子として読めず SyntaxError になります。"),
            ("console.log(n =< 5);", "=< という演算子はありません。「以下」は <= と書きますが、等しいかを調べたいなら ===です。"),
        ],
        correct=0, fmt="code",
        why="等しいかどうかの比較には、代入の = ではなく === を使うから。",
        expl="n = 5 は「n に 5 を代入する」式で、その結果の 5 が表示されていました。n === 5 なら、n が 5 と等しいかを調べ、結果の true が表示されます。",
        concepts=["=", "===", "代入と比較"], diff=2,
        hint="代入と比較の記号は違います。比較は = を3つです。",
        ok="正解！比較には === を使います。",
        ng="惜しい！= は代入、=== が比較です。",
    ),
    pred(
        title="数値にできない計算", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''console.log("10" / 2);
console.log("abc" * 2);''',
        out="5\nNaN",
        wrong=[("5\n0", "数値にできない文字列 \"abc\" との計算は 0 ではなく NaN（Not a Number）になります。"), ("\"10\" / 2\nNaN", "計算式がそのまま表示されることはありません。\"10\" は数値の 10 に変換され、10 / 2 の結果 5 が表示されます。")],
        why="\"10\" は数値に変換されて 5、\"abc\" は数値にできず NaN になるから。",
        expl="/ や * は、文字列を数値に変換して計算します。\"10\" は 10 になりますが、\"abc\" は数値にできないので、計算結果は NaN（数値ではない）です。NaN は何と計算しても NaN になります。",
        concepts=["型変換", "NaN"], diff=3,
        hint="\"abc\" は数値に変換できるでしょうか？",
        ok="正解！数値にできない計算は NaN です。",
        ng="惜しい！文字列が数値に変換できるかを考えましょう。",
    ),
    bugfix(
        title="足し算が連結になる", lang="javascript",
        prompt="a と b を足した 7 を表示するつもりが 34 と表示されます。3行目を正しく書き直して入力してください（3行目の内容だけを入力）。",
        code='''let a = "3";
let b = 4;
console.log(a + b);''',
        fixed='''let a = "3";
let b = 4;
console.log(Number(a) + b);''', out="7", buggy_out="34",
        target_line=3, accepted=["console.log(Number(a) + b);", "console.log(Number(a)+b);", "console.log(Number(a) + b)", "console.log(+a + b);", "console.log(b + Number(a));"],
        wrong=[("console.log(a + b);", "元のコードのままです。a は文字列なので、+ は足し算ではなく連結になります。")],
        why="a は文字列なので、Number() で数値に変換してから足す必要があるから。",
        expl="\"3\" + 4 は連結で \"34\" になります。Number(a) で数値の 3 にすれば、3 + 4 の足し算で 7 になります。",
        concepts=["Number()", "型変換", "文字列の連結"], diff=3,
        hint="a の型は文字列です。足し算にするには、どうすればよいでしょう？",
        ok="正解！数値に変換してから足しました。",
        ng="惜しい！文字列と数値の + は連結になります。",
    ),
    write_js(
        title="税込み価格を求める", lang="javascript",
        prompt="変数 price に商品の価格、変数 taxPercent に消費税の割合（パーセント、整数）が入っています。税込み価格（price + 税額。税額は price × taxPercent ÷ 100）を console.log で表示するコードを書いてください。",
        starter="// price と taxPercent はあらかじめ用意されています\n",
        ref="console.log(price + price * taxPercent / 100);",
        alts=["const tax = price * taxPercent / 100;\nconsole.log(price + tax);", "console.log(price * (100 + taxPercent) / 100);"],
        bads=[
            ("console.log(price * taxPercent);", "税額だけでなく、さらに price を掛けています。税込み価格は 価格 + 税額 です。"),
            ("console.log(price + taxPercent);", "taxPercent は割合（パーセント）です。価格に直接足すのではなく、価格 × 割合 ÷ 100 を足します。"),
        ],
        tests=[
            t_js_out("1100\n", setup="const price = 1000;\nconst taxPercent = 10;"),
            t_js_out("300\n", setup="const price = 200;\nconst taxPercent = 50;", visible=False),
            t_js_out("0\n", setup="const price = 0;\nconst taxPercent = 10;", visible=False),
            t_js_out("1078\n", setup="const price = 980;\nconst taxPercent = 10;", visible=False),
        ],
        why="税額は price × taxPercent ÷ 100 で、それを price に足すと税込み価格になるから。",
        expl="1000 円で 10% なら税額は 1000 × 10 ÷ 100 = 100 で、税込みは 1100 円です。計算は掛け算・割り算が先なので、( ) がなくても税額が先に計算されます。",
        concepts=["算術演算子", "計算の優先順位"], diff=3,
        hint="税額は price * taxPercent / 100 で求まります。",
        ok="正解！変数を使って税込み価格を求められました。",
        ng="惜しい！price と taxPercent を使った式になっているか確認しましょう。",
    ),
]
