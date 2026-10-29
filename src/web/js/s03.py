from lib_web import mc, pred, fill, bugfix, write_js, t_js_out

STAGE = {
    "number": 3,
    "title": "条件分岐",
    "subtitle": "if / else if / else、真偽の判定、三項演算子、switch",
    "goals": [
        "if / else if / else で処理を分岐できる",
        "条件の順序と境界値を意識して条件を書ける",
        "true / false 以外の値が条件で真偽に変換されるルール（truthy / falsy）を説明できる",
        "三項演算子と switch 文の基本形を書ける",
        "if の条件で = と === を取り違えるミスに気づける",
    ],
    "prerequisites": ["比較演算子・論理演算子（ステージ2）", "変数と console.log（ステージ1）"],
    "topics": [
        "if / else if / else と { }",
        "条件の順序と境界値",
        "truthy / falsy（真として扱われる値・偽として扱われる値）",
        "三項演算子（条件 ? A : B）",
        "switch と break",
        "&& と || の返す値",
    ],
    "pitfalls": [
        "if の条件に = を書くと代入になり、エラーにならずに常に動いてしまうことがある",
        "else if は上から順に調べ、最初に成り立ったものだけが実行される",
        "switch の case の最後に break を忘れると、次の case も実行される",
        "空でない文字列は \"0\" や \"false\" でも truthy",
        "「以上」と「より大きい」の境界（>= と >）",
    ],
    "next_links": ["同じ処理をくり返す「繰り返し」（ステージ4）へ進みます"],
    "lesson": {
        "intro": "プログラムは、条件によって動きを変えられます。「80点以上なら合格」「入力が空なら警告を出す」のような判断を、if 文で書きます。Webページでも、フォームのチェックや表示の切り替えで毎日のように使います。",
        "sections": [
            {
                "id": "S03-L1",
                "title": "if / else if / else",
                "read_minutes": 3,
                "body": [
                    "if (条件) { ... } と書くと、条件が true のときだけ { } の中が実行されます。条件が false のときの処理は else { ... } に書きます。",
                    "3つ以上に分けたいときは else if (条件) { ... } を続けます。上から順に調べ、最初に条件が成り立ったブロックだけが実行され、残りは調べません。そのため、厳しい条件（例: 90点以上）から順に書きます。",
                    "条件には、ステージ2の比較演算子・論理演算子を使います。「60点以上」は score >= 60、境界の 60 点を含むかどうかは >= と > で変わります。{ } の中の行は、見やすくするために字下げ（インデント）しますが、JavaScript では字下げは動作に影響しません。",
                ],
                "glossary": [
                    {"term": "条件分岐", "definition": "条件によって、実行する処理を切り替えること。"},
                    {"term": "ブロック", "definition": "{ } で囲んだ、ひとまとまりの処理。"},
                    {"term": "境界値", "definition": "ちょうど切り替わる値（60点以上なら 60 など）。"},
                ],
                "examples": [
                    {
                        "id": "S03-E1", "title": "if と else", "language": "javascript",
                        "code": '''const score = 55;
if (score >= 60) {
  console.log("合格");
} else {
  console.log("不合格");
}
console.log("終わり");''',
                        "expected_output": "不合格\n終わり",
                        "line_notes": ["2行目: score >= 60 が false なので、else 側が実行されます。", "7行目: if 文の外にあるので、常に実行されます。"],
                    },
                    {
                        "id": "S03-E2", "title": "else if", "language": "javascript",
                        "code": '''const score = 85;
if (score >= 90) {
  console.log("A");
} else if (score >= 80) {
  console.log("B");
} else if (score >= 70) {
  console.log("C");
} else {
  console.log("D");
}''',
                        "expected_output": "B",
                        "line_notes": ["上から順に調べ、score >= 80 が最初に true になるので B を表示して終わります。score >= 70 も true ですが、調べられません。"],
                    },
                ],
            },
            {
                "id": "S03-L2",
                "title": "truthy / falsy・三項演算子・switch",
                "read_minutes": 3,
                "body": [
                    "if の条件には、true / false 以外の値も書けます。その場合、値は真偽に変換されます。偽（falsy）として扱われるのは、false、0、\"\"（空文字列）、null、undefined、NaN の6つだけで、それ以外は真（truthy）です。\"0\" や \"false\" のように、中身が空でない文字列は truthy です。",
                    "a && b、a || b は、true / false ではなく、どちらかの値そのものを返します。a || b は a が truthy なら a、そうでなければ b を返します（「a がなければ b」の意味で、初期値を決めるときに使います）。a && b は a が falsy なら a、そうでなければ b を返します。",
                    "条件 ? 値1 : 値2 は三項演算子で、条件が truthy なら値1、そうでなければ値2になります。短い if / else を1行で書きたいときに使います。",
                    "switch (式) { case 値: ... break; default: ... } は、1つの値によって分岐します。case の最後に break を書かないと、次の case の処理も続けて実行されます。",
                ],
                "glossary": [
                    {"term": "truthy / falsy", "definition": "条件に使ったとき、真として扱われる値 / 偽として扱われる値。"},
                    {"term": "三項演算子", "definition": "条件 ? A : B の形で、条件によって値を選ぶ演算子。"},
                    {"term": "break", "definition": "switch や繰り返しから抜ける文。"},
                ],
                "examples": [
                    {
                        "id": "S03-E3", "title": "falsy な値と || の動き", "language": "javascript",
                        "code": '''if (0) { console.log("a"); } else { console.log("b"); }
if ("") { console.log("c"); } else { console.log("d"); }
if ("0") { console.log("e"); } else { console.log("f"); }
console.log(0 || "初期値");
console.log("あり" && "続き");''',
                        "expected_output": "b\nd\ne\n初期値\n続き",
                        "line_notes": ["1行目: 0 は falsy なので else 側。", "3行目: \"0\" は空でない文字列なので truthy です。", "4行目: 0 は falsy なので、右の \"初期値\" が返ります。"],
                    },
                    {
                        "id": "S03-E4", "title": "三項演算子と switch", "language": "javascript",
                        "code": '''const age = 20;
console.log(age >= 18 ? "成人" : "未成年");
const n = 2;
switch (n) {
  case 1:
    console.log("one");
    break;
  case 2:
    console.log("two");
    break;
  default:
    console.log("other");
}''',
                        "expected_output": "成人\ntwo",
                        "line_notes": ["2行目: 条件が true なので \"成人\" が選ばれます。", "8〜9行目: n が 2 なので two を表示し、break で switch を抜けます。"],
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "if の条件で = を使う", "wrong_code": "if (n = 5) { ... }", "why": "= は代入です。n に 5 を入れ、その結果（5、truthy）で条件が常に真になります。エラーにならないので気づきにくいミスです。", "fix": "if (n === 5) { ... }"},
            {"title": "else if の順序", "wrong_code": "if (score >= 60) {...} else if (score >= 80) {...}", "why": "上から順に調べるので、80点以上でも最初の条件が先に成り立ちます。厳しい条件から書きます。", "fix": "先に score >= 80 を調べる"},
            {"title": "switch の break 忘れ", "wrong_code": "case 1:\n  console.log(\"one\");\ncase 2:\n  console.log(\"two\");", "why": "break がないと、case 1 のあとも続けて case 2 の処理が実行されます。", "fix": "各 case の最後に break; を書く"},
            {"title": "\"0\" は falsy だと思う", "wrong_code": "if (\"0\") { ... }", "why": "空でない文字列は truthy です。falsy なのは数値の 0 です。", "fix": "数値にしたいなら Number(\"0\") を使う"},
        ],
        "checkpoints": [
            "if / else if / else は上から順に調べ、最初に成り立ったものだけ実行される",
            "厳しい条件から書く。境界値は >= と > で変わる",
            "falsy は false・0・\"\"・null・undefined・NaN",
            "a || b は「a がなければ b」",
            "条件 ? A : B（三項演算子）",
            "switch は case の最後に break",
        ],
        "next_bridge": "条件分岐は、これから学ぶ繰り返しや関数と組み合わせて使います。まず問題で、条件の順序や境界値を正確に読む練習をしましょう。",
    },
}

QUESTIONS = [
    pred(
        title="if と else の動き", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''const score = 55;
if (score >= 60) {
  console.log("合格");
} else {
  console.log("不合格");
}
console.log("終わり");''',
        out="不合格\n終わり",
        wrong=[("不合格", "最後の console.log(\"終わり\") は if 文の外にあるので、条件に関係なく必ず実行されます。"), ("合格\n終わり", "55 >= 60 は false なので、「合格」は表示されません。")],
        why="55 は 60 未満なので else 側が実行され、if 文の外の行は必ず実行されるから。",
        expl="score >= 60 は false なので、else の「不合格」が表示されます。7行目は if / else の { } の外にあるため、結果に関係なく最後に実行されます。",
        concepts=["if", "else", "ブロック"], diff=1,
        hint="条件が true か false かを先に決めましょう。{ } の外の行はいつ実行されますか？",
        ok="正解！{ } の外の行は常に実行されます。",
        ng="惜しい！条件の結果と、{ } の外の行の扱いを確認しましょう。",
    ),
    pred(
        title="else if は最初に成り立つ所まで", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''const score = 85;
if (score >= 90) {
  console.log("A");
} else if (score >= 80) {
  console.log("B");
} else if (score >= 70) {
  console.log("C");
} else {
  console.log("D");
}''',
        choices=[
            ("B\nC", "else if は、最初に条件が成り立ったブロックだけを実行します。B を表示したあと、次の条件は調べられません。"),
            ("B", ""),
            ("A", "85 >= 90 は false なので、A のブロックは実行されません。"),
        ],
        correct=1,
        why="85 >= 90 は false、85 >= 80 が最初に true になり、残りは調べないから。",
        expl="if / else if / else は上から順に条件を調べ、最初に true になったブロックだけを実行します。85 は 70 以上でもありますが、その手前で B が選ばれて終了します。",
        concepts=["else if", "条件の順序"], diff=2,
        hint="最初に true になる条件を、上から探しましょう。",
        ok="正解！最初に成り立った条件だけが実行されます。",
        ng="惜しい！上から順に、最初に true になる所を探しましょう。",
    ),
    mc(
        title="falsy な値", lang="javascript",
        prompt="次のうち、if の条件に使ったとき false（偽）として扱われる値はどれですか？",
        fmt="code",
        choices=[
            ('"0"（文字列のゼロ）', "空でない文字列は、中身が \"0\" でも truthy（真）として扱われます。"),
            ('"false"（文字列）', "空でない文字列は truthy です。中身が false という文字でも、文字列としては真になります。"),
            ("0（数値のゼロ）", ""),
        ],
        correct=2,
        why="数値の 0 は falsy で、空でない文字列は truthy だから。",
        expl="falsy は false・0・\"\"（空文字列）・null・undefined・NaN の6つだけです。見た目が 0 や false でも、引用符で囲んだ文字列は truthy です。",
        concepts=["truthy / falsy"], diff=2,
        hint="引用符で囲まれていない 0 に注目しましょう。",
        ok="正解！数値の 0 は falsy です。",
        ng="惜しい！文字列は空でなければ truthy です。",
    ),
    pred(
        title="文字列の真偽", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''if ("") { console.log("A"); } else { console.log("B"); }
if ("0") { console.log("C"); } else { console.log("D"); }''',
        choices=[
            ("B\nD", "\"0\" は空でない文字列なので truthy です。そのため D ではなく C が表示されます。"),
            ("A\nC", "空文字列 \"\" は falsy なので、1行目は A ではなく B です。"),
            ("B\nC", ""),
        ],
        correct=2,
        why="空文字列は falsy で B、\"0\" は空でない文字列なので truthy で C だから。",
        expl="空文字列だけが falsy で、\"0\" のような文字は truthy です。入力欄が空かどうかを調べるとき、この性質がよく使われます。",
        concepts=["truthy / falsy", "文字列"], diff=2,
        hint="文字列の真偽は「空かどうか」で決まります。",
        ok="正解！空の文字列だけが falsy です。",
        ng="惜しい！\"0\" は空の文字列ではありません。",
    ),
    fill(
        title="三項演算子", lang="javascript",
        prompt="score が 60 以上なら「合格」、そうでなければ「不合格」を表示する三項演算子です。【空欄1】に入れる記号を答えてください。",
        code='''const score = 70;
const label = score >= 60 __1__ "合格" : "不合格";
console.log(label);''',
        blanks=[(["?"], False)],
        out="合格",
        wrong=[("b1", ":", "三項演算子は 条件 ? A : B の形です。条件の直後には ? を書き、A と B の区切りに : を書きます。: だけでは SyntaxError になります。")],
        why="三項演算子は 条件 ? 値1 : 値2 の形で書くから。",
        expl="三項演算子は、短い if / else を1つの式で書く方法です。? の前が条件、? と : の間が条件が真のときの値、: の後ろが偽のときの値です。",
        concepts=["三項演算子"], diff=2,
        hint="条件のあとに付ける、疑問を表す記号です。",
        ok="正解！条件 ? A : B の形です。",
        ng="惜しい！条件のあとに付ける記号を思い出しましょう。",
    ),
    bugfix(
        title="条件の並べ順", lang="javascript",
        prompt="85 点なら \"B\" と表示するはずが \"C\" と表示されます。どう直すのが適切ですか？",
        code='''const score = 85;
let grade;
if (score >= 60) {
  grade = "C";
} else if (score >= 80) {
  grade = "B";
} else {
  grade = "D";
}
console.log(grade);''',
        fixed='''const score = 85;
let grade;
if (score >= 80) {
  grade = "B";
} else if (score >= 60) {
  grade = "C";
} else {
  grade = "D";
}
console.log(grade);''', out="B", buggy_out="C",
        choices=[
            ("else if をやめて、if を続けて書く", "if を続けると、85 は最初の if で C になったあと、次の if（80以上）でも B になり、最後は B になりますが、65 点では C のあとに else の D が実行されてしまいます。"),
            ("条件を厳しい順（80以上、60以上の順）に並べ替える", ""),
            ("score >= 60 を score === 60 に変える", "=== は「ちょうど60」のときだけ成り立つので、85 を含む多くの点数が当てはまらなくなります。"),
        ],
        correct=1, fmt="text",
        why="else if は上から順に調べ、最初に成り立ったものだけ実行するので、厳しい条件を先に書く必要があるから。",
        expl="85 は 60 以上でもあるため、最初の条件で \"C\" になり、80 以上かどうかは調べられません。80 以上を先に書けば、85 は \"B\"、65 は \"C\" と正しく分かれます。",
        concepts=["else if", "条件の順序"], diff=3,
        hint="85 は、最初の条件 score >= 60 を満たしますか？",
        ok="正解！条件は厳しい順に並べます。",
        ng="惜しい！上から順に調べ、最初に成り立った所で終わることを思い出しましょう。",
    ),
    pred(
        title="switch の break 忘れ", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''const n = 2;
switch (n) {
  case 1:
    console.log("one");
  case 2:
    console.log("two");
  case 3:
    console.log("three");
    break;
  default:
    console.log("other");
}''',
        choices=[
            ("two", "case 2 には break がないので、two を表示したあとも終わらず、次の case 3 の処理も実行されます。"),
            ("two\nthree", ""),
            ("one\ntwo\nthree", "n は 2 なので case 1 は実行されません。case 2 から始まり、break のある case 3 の最後で止まります。"),
        ],
        correct=1,
        why="case 2 から実行が始まり、break がないので case 3 も実行され、そこで break するから。",
        expl="switch は、一致した case から実行を始め、break に出会うまで下の case も続けて実行します（フォールスルー）。意図しないときは、各 case の最後に break を書きます。",
        concepts=["switch", "break"], diff=3,
        hint="n === 2 に一致するのは case 2 です。そのあと、break はありますか？",
        ok="正解！break がないと次の case も実行されます。",
        ng="惜しい！break のない case の動きを確認しましょう。",
    ),
    bugfix(
        title="条件に = を書いてしまった", lang="javascript",
        prompt="n は 3 なので「not five」と表示されるはずが、「five」と表示されてしまいます。2行目を正しく書き直して入力してください（2行目の内容だけを入力）。",
        code='''let n = 3;
if (n = 5) {
  console.log("five");
} else {
  console.log("not five");
}''',
        fixed='''let n = 3;
if (n === 5) {
  console.log("five");
} else {
  console.log("not five");
}''', out="not five", buggy_out="five",
        target_line=2, accepted=["if (n === 5) {", "if (n === 5){", "if(n === 5) {", "if (n===5) {"],
        wrong=[("if (n = 5) {", "元のコードのままです。n = 5 は代入で、n に 5 が入り、その結果（5）が truthy になって条件が真になります。")],
        why="条件では、代入の = ではなく、比較の === を使う必要があるから。",
        expl="if (n = 5) は、n に 5 を代入してから、その値 5 で真偽を判断します。5 は truthy なので、いつも「five」側が実行されます。エラーにならないため見つけにくいミスです。比較は ===。",
        concepts=["=", "===", "truthy / falsy"], diff=3,
        hint="条件の中では、代入ではなく比較をしたいのです。",
        ok="正解！条件では === で比較します。",
        ng="惜しい！= は代入、=== が比較です。",
    ),
    pred(
        title="&& と || が返す値", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''console.log(0 || "default");
console.log("a" && "b");
console.log(5 > 3 && "yes");''',
        out="default\nb\nyes",
        wrong=[("true\ntrue\ntrue", "&& と || は true / false ではなく、どちらかの値そのものを返します。"), ("0\na\nfalse", "0 は falsy なので || は右の値を返します。\"a\" は truthy なので && は右の値を返します。")],
        why="|| は左が falsy なら右の値、&& は左が truthy なら右の値を返すから。",
        expl="0 || \"default\" は、0 が falsy なので \"default\"。\"a\" && \"b\" は、\"a\" が truthy なので右の \"b\"。5 > 3 は true なので、&& は右の \"yes\" を返します。",
        concepts=["||", "&&", "truthy / falsy"], diff=4,
        hint="左の値が truthy か falsy かで、返す値が決まります。",
        ok="正解！&& と || は値そのものを返します。",
        ng="惜しい！左の値が真か偽かを先に判断しましょう。",
    ),
    write_js(
        title="点数から評価を決める", lang="javascript",
        prompt="変数 score に点数が入っています。90 点以上なら \"S\"、80 点以上なら \"A\"、70 点以上なら \"B\"、それ以外なら \"C\" を console.log で表示するコードを if / else if / else で書いてください。",
        starter="// score はあらかじめ用意されています\n",
        ref='''if (score >= 90) {
  console.log("S");
} else if (score >= 80) {
  console.log("A");
} else if (score >= 70) {
  console.log("B");
} else {
  console.log("C");
}''',
        alts=['''if (score < 70) {
  console.log("C");
} else if (score < 80) {
  console.log("B");
} else if (score < 90) {
  console.log("A");
} else {
  console.log("S");
}''', '''let result = "C";
if (score >= 70) result = "B";
if (score >= 80) result = "A";
if (score >= 90) result = "S";
console.log(result);'''],
        bads=[
            ('''if (score >= 70) {
  console.log("B");
} else if (score >= 80) {
  console.log("A");
} else if (score >= 90) {
  console.log("S");
} else {
  console.log("C");
}''', "条件の順序が逆です。90 点でも最初の score >= 70 が先に成り立って B になってしまいます。厳しい条件から書きます。"),
            ('''if (score > 90) {
  console.log("S");
} else if (score > 80) {
  console.log("A");
} else if (score > 70) {
  console.log("B");
} else {
  console.log("C");
}''', "境界値が違います。「90点以上」は >= 90 です。90 点ちょうどが S にならず A になってしまいます。"),
        ],
        req_any=[(r"\bif\b", "if を使ってください"), (r"\bswitch\b", "switch を使ってください")],
        tests=[
            t_js_out("S\n", setup="const score = 95;"), t_js_out("A\n", setup="const score = 85;"),
            t_js_out("S\n", setup="const score = 90;", visible=False), t_js_out("A\n", setup="const score = 80;", visible=False),
            t_js_out("B\n", setup="const score = 70;", visible=False), t_js_out("C\n", setup="const score = 69;", visible=False),
            t_js_out("C\n", setup="const score = 0;", visible=False),
        ],
        why="厳しい条件から順に調べ、境界の 90・80・70 を含めるために >= を使うから。",
        expl="if / else if は上から順に調べるので、90 以上 → 80 以上 → 70 以上の順に書きます。境界値（ちょうど 90 や 80 の点数）で正しく動くかを必ず確認しましょう。",
        concepts=["if", "else if", "境界値"], diff=3,
        hint="厳しい条件（90以上）から順に。「以上」は >= です。",
        ok="正解！境界値も正しく分けられました。",
        ng="惜しい！ちょうど 90 点・80 点・70 点のときの結果を確認しましょう。",
    ),
]
