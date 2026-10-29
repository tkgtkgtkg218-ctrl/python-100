from lib_web import mc, pred, fill, bugfix, write_js, t_js_out, t_js_call

STAGE = {
    "number": 7,
    "title": "関数",
    "subtitle": "引数・戻り値・アロー関数・スコープ・コールバック",
    "goals": [
        "function とアロー関数で関数を定義し、呼び出せる",
        "引数・戻り値・デフォルト引数を使える",
        "return と console.log の違いを説明できる",
        "関数の中の変数（ローカル変数）とブロックスコープを理解する",
        "map・filter・forEach に関数を渡して、配列を処理できる",
    ],
    "prerequisites": ["変数・演算子・if・for（ステージ1〜4）", "配列とオブジェクト（ステージ5〜6）"],
    "topics": [
        "function による関数宣言と呼び出し",
        "引数・戻り値・デフォルト引数",
        "return がない関数の戻り値（undefined）",
        "アロー関数 ( ) => { }",
        "スコープ（関数・ブロックの中の変数）",
        "コールバック（map / filter / forEach）",
    ],
    "pitfalls": [
        "関数は定義しただけでは実行されない（関数名() で呼び出す）",
        "return を書かないと、戻り値は undefined になる",
        "アロー関数で { } を使うと、return を明示しないと undefined になる",
        "return は関数を終了する（ループの中に書くと1回で終わる）",
        "関数名だけを渡す（addEventListener(\"click\", fn)）と、関数名() で呼び出すは別",
    ],
    "next_links": ["関数をイベントに結びつける準備として、ステージ8でまず HTML の要素を操作します"],
    "lesson": {
        "intro": "同じ処理を何度も書くのは大変で、間違いのもとです。処理に名前を付けて「部品」にしたものが関数です。ここまで使ってきた console.log や push も関数でした。ページのボタンを押したときの動き（ステージ9）は、関数を渡して書くので、この回の内容が土台になります。",
        "sections": [
            {
                "id": "S07-L1",
                "title": "関数を作って呼び出す",
                "read_minutes": 3,
                "body": [
                    "function 関数名(引数) { ... } で関数を定義します。定義しただけでは実行されず、関数名(値) と書いて呼び出したときに実行されます。呼び出し時に渡す値を引数といい、関数の中では引数の名前で使えます。",
                    "return 値; は、結果を呼び出し元へ返して、関数を終了します。return がない関数の戻り値は undefined です。console.log は画面（コンソール）に表示するだけで、値は返しません。結果を別の計算に使うなら return を使います。",
                    "アロー関数 const add = (a, b) => a + b; は、関数を短く書く方法です。{ } で囲んだときは、結果を返すために return が必要です。引数にデフォルト値を決めたいときは、function power(base, exp = 2) のように = で書きます。",
                ],
                "glossary": [
                    {"term": "関数", "definition": "名前を付けた処理のまとまり。"},
                    {"term": "引数", "definition": "関数に渡す材料の値。"},
                    {"term": "戻り値", "definition": "関数が return で返す結果。"},
                    {"term": "アロー関数", "definition": "=> を使った、関数の短い書き方。"},
                ],
                "examples": [
                    {
                        "id": "S07-E1", "title": "引数と戻り値", "language": "javascript",
                        "code": '''function add(a, b) {
  return a + b;
}
console.log(add(3, 4));
console.log(add(3, 4) * 2);
function show(x) {
  console.log(x);
}
const r = show(5);
console.log(r);''',
                        "expected_output": "7\n14\n5\nundefined",
                        "line_notes": ["5行目: 呼び出しは戻り値に置き換わって計算が進みます。", "9〜10行目: show は何も返さないので、r は undefined です。"],
                    },
                    {
                        "id": "S07-E2", "title": "アロー関数とデフォルト引数", "language": "javascript",
                        "code": '''const double = (n) => n * 2;
console.log(double(4));
const add = (a, b) => {
  return a + b;
};
console.log(add(1, 2));
function power(base, exp = 2) {
  return base ** exp;
}
console.log(power(3));
console.log(power(2, 5));''',
                        "expected_output": "8\n3\n9\n32",
                        "line_notes": ["1行目: { } がなければ、式の結果がそのまま戻り値になります。", "3〜5行目: { } を使うときは return が必要です。", "11行目: exp を省略すると、デフォルトの 2 が使われます。"],
                    },
                ],
            },
            {
                "id": "S07-L2",
                "title": "スコープとコールバック",
                "read_minutes": 3,
                "body": [
                    "関数の中で宣言した変数は、その関数の中だけで使えます（ローカル変数）。同じ名前の外の変数とは別物で、外の値は変わりません。let / const は { } の中だけで有効な「ブロックスコープ」です。{ } の外から使うと ReferenceError になります。",
                    "関数は値として、別の関数に渡せます。渡された関数を、あとで呼び出してもらう仕組みをコールバックといいます。配列のメソッドの forEach（各要素に処理）、map（各要素を変換した新しい配列）、filter（条件に合う要素だけの新しい配列）は、コールバックを受け取ります。",
                    "ステージ9のイベント処理でも、「クリックされたらこの関数を呼んで」と、関数を渡します。このとき、関数名のあとに ( ) を付けない点に注意します。fn は関数そのもの、fn() は関数を呼び出した結果です。",
                ],
                "glossary": [
                    {"term": "ローカル変数", "definition": "関数やブロックの中だけで有効な変数。"},
                    {"term": "コールバック", "definition": "あとで呼び出してもらうために、別の関数に渡す関数。"},
                    {"term": "map / filter", "definition": "配列の各要素を変換する / 条件に合う要素を選ぶメソッド。"},
                ],
                "examples": [
                    {
                        "id": "S07-E3", "title": "スコープ", "language": "javascript",
                        "code": '''let x = 100;
function f() {
  let x = 10;
  return x + 1;
}
console.log(f());
console.log(x);
{
  let y = 1;
}
console.log(typeof y);''',
                        "expected_output": "11\n100\nundefined",
                        "line_notes": ["3行目: 関数の中の x は別の変数です。外の x は変わりません。", "10行目: y は { } の中だけの変数なので、外では存在しません（typeof は undefined を返します）。"],
                    },
                    {
                        "id": "S07-E4", "title": "map・filter・forEach", "language": "javascript",
                        "code": '''const nums = [1, 2, 3, 4];
console.log(nums.map((n) => n * 2).join(","));
console.log(nums.filter((n) => n % 2 === 0).join(","));
nums.forEach((n) => {
  console.log("値: " + n);
});''',
                        "expected_output": "2,4,6,8\n2,4\n値: 1\n値: 2\n値: 3\n値: 4",
                        "line_notes": ["2行目: map は、各要素を2倍にした新しい配列を返します。", "3行目: filter は、関数が true を返した要素だけを集めます。", "4行目: forEach は、各要素に対して関数を呼び出します（戻り値は使いません）。"],
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "定義しただけで呼び出さない", "wrong_code": "function greet() {\n  console.log(\"hi\");\n}", "why": "定義だけでは何も起きません。greet() と呼び出します。", "fix": "greet();"},
            {"title": "return の代わりに console.log", "wrong_code": "function area(w, h) {\n  console.log(w * h);\n}\nconst x = area(3, 4) + 1;", "why": "area は何も返さない（undefined）ので、undefined + 1 は NaN になります。", "fix": "console.log を return に変える"},
            {"title": "アロー関数の { } で return を忘れる", "wrong_code": "const add = (a, b) => { a + b };", "why": "{ } を使うと、return がないので undefined が返ります。", "fix": "const add = (a, b) => a + b;"},
            {"title": "return をループの中に書く", "wrong_code": "for (const n of nums) {\n  s += n;\n  return s;\n}", "why": "return でその場で関数が終了し、1回目で終わってしまいます。", "fix": "return s; をループの外に書く"},
        ],
        "checkpoints": [
            "関数は定義だけでは実行されず、関数名() で呼び出す",
            "return は値を返して関数を終了する。なければ undefined",
            "console.log は表示するだけ。値は返さない",
            "アロー関数の { } では return が必要",
            "関数の中の変数は外とは別物（ローカル変数）",
            "map・filter・forEach には関数を渡す（関数名のあとに ( ) は付けない）",
        ],
        "next_bridge": "関数が使えると、処理を部品として組み合わせられます。問題で、戻り値や return の働きを確かめましょう。",
    },
}

QUESTIONS = [
    pred(
        title="戻り値を計算に使う", lang="javascript",
        prompt="次のコードを実行したとき、コンソールには何が表示されますか？",
        code='''function add(a, b) {
  return a + b;
}
console.log(add(3, 4) * 2);''',
        choices=[
            ("7", "add(3, 4) が 7 を返したあと、さらに * 2 が計算されるので 14 になります。"),
            ("14", ""),
            ("add(3, 4) * 2", "console.log は式を計算した結果を表示します。コードの文字がそのまま表示されることはありません。"),
        ],
        correct=1,
        why="add(3, 4) が 7 を返し、それを2倍して 14 になるから。",
        expl="関数を呼び出した式は、その戻り値に置き換わって計算が進みます。add(3, 4) は 7 になるので、7 * 2 = 14 が console.log に渡されます。",
        concepts=["return", "戻り値"], diff=2,
        hint="まず add(3, 4) を 7 に置き換えて考えましょう。",
        ok="正解！呼び出しは戻り値に置き換わります。",
        ng="惜しい！関数呼び出しの部分を戻り値に置き換えてみましょう。",
    ),
    pred(
        title="return のない関数の戻り値", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''function show(x) {
  console.log(x);
}
const r = show(5);
console.log(r);''',
        out="5\nundefined",
        wrong=[("5", "r に入っているのは show の戻り値です。return がないので undefined で、それも console.log で表示されます。"), ("5\n5", "console.log は表示するだけで、値は返しません。r には 5 ではなく undefined が入ります。")],
        why="show は表示するだけで値を返さないため、r は undefined になるから。",
        expl="show(5) の実行中に 5 が表示されます。しかし return がないので戻り値は undefined になり、r = undefined です。最後の console.log(r) が undefined を表示します。",
        concepts=["return", "undefined", "console.log"], diff=3,
        hint="show は return していません。r には何が入るでしょう？",
        ok="正解！return がないと undefined になります。",
        ng="惜しい！r に入る値と、表示のタイミングを分けて考えましょう。",
    ),
    mc(
        title="定義しただけでは動かない", lang="javascript",
        prompt="次のコードだけを実行すると、コンソールには何が表示されますか？",
        code='''function greet() {
  console.log("hi");
}''',
        choices=[
            ("hi", "関数は、定義しただけでは実行されません。greet() と呼び出すと、はじめて hi が表示されます。"),
            ("何も表示されない", ""),
            ("SyntaxError が表示される", "書き方は正しいので、エラーにはなりません。"),
        ],
        correct=1,
        why="function は処理に名前を付けて定義するだけで、呼び出すまで実行されないから。",
        expl="関数の定義は「こういう部品を作ります」という宣言です。実行したいときは greet() のように呼び出します。",
        concepts=["関数の定義", "関数の呼び出し"], diff=2,
        hint="コードの最後に greet() という行はありますか？",
        ok="正解！定義だけでは実行されません。",
        ng="惜しい！呼び出しの行があるか確認しましょう。",
    ),
    fill(
        title="アロー関数の記号", lang="javascript",
        prompt="引数を2倍にして返すアロー関数です。8 と表示されるように、【空欄1】に入れる記号を答えてください。",
        code='''const double = (n) __1__ n * 2;
console.log(double(4));''',
        blanks=[(["=>"], False)],
        out="8",
        wrong=[("b1", "=", "= は代入です。アロー関数の矢印は => と書きます。= だけだと SyntaxError になります。")],
        why="アロー関数は、引数と本体を => でつないで書くから。",
        expl="(n) => n * 2 は、「n を受け取って n * 2 を返す関数」です。{ } がなければ、式の結果がそのまま戻り値になります。",
        concepts=["アロー関数"], diff=2,
        hint="等号（=）と大なり記号（>）を組み合わせた、矢印の形の記号です。",
        ok="正解！アロー関数は => で書きます。",
        ng="惜しい！矢印の形の記号を入力しましょう。",
    ),
    pred(
        title="デフォルト引数", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''function power(base, exp = 2) {
  return base ** exp;
}
console.log(power(3));
console.log(power(2, 5));''',
        choices=[
            ("6\n32", "** は累乗です。power(3) は 3 を2回かける 3 ** 2 = 9 で、3 × 2 = 6 ではありません。"),
            ("9\n32", ""),
            ("9\n10", "power(2, 5) は 2 ** 5 = 32 です。足し算の 2 + 5 でも 10 でもありません。"),
        ],
        correct=1,
        why="exp を省略すると 2 が使われ、渡すとその値が使われるから。",
        expl="power(3) は exp が省略されたので 2 が入り、3 ** 2 = 9。power(2, 5) は exp = 5 なので 2 ** 5 = 32 です。",
        concepts=["デフォルト引数", "**"], diff=2,
        hint="1回目は exp を省略しています。デフォルト値はいくつ？",
        ok="正解！省略するとデフォルト値が使われます。",
        ng="惜しい！省略したときの exp の値と、** の意味を見直しましょう。",
    ),
    bugfix(
        title="合計が1にしかならない", lang="javascript",
        prompt="[1, 2, 3] の合計 6 を返す関数のつもりが、1 が返ってきます。原因を正しく直す方法はどれですか？",
        code='''function total(nums) {
  let s = 0;
  for (const n of nums) {
    s += n;
    return s;
  }
}
console.log(total([1, 2, 3]));''',
        fixed='''function total(nums) {
  let s = 0;
  for (const n of nums) {
    s += n;
  }
  return s;
}
console.log(total([1, 2, 3]));''', out="6", buggy_out="1",
        choices=[
            ("let s = 0; の行を for の中に移す", "for の中に移すと、毎回 s が 0 に戻り、合計できません。"),
            ("return s; を for の外（ループが終わった後）に書く", ""),
            ("return を console.log に変える", "return がなくなると、戻り値は undefined になり、外側の console.log は undefined を表示します。"),
        ],
        correct=1, fmt="text",
        why="return は関数をその場で終了するため、ループの中に書くと1回で終わってしまうから。",
        expl="return を実行した時点で関数は終了します。for の中に書くと、1回目の足し算（s = 1）の直後に返ります。return をループの外へ出せば、足し算がすべて終わってから合計が返ります。",
        concepts=["return", "for", "ループ"], diff=3,
        hint="return を実行すると、その関数はどうなりますか？",
        ok="正解！return の位置が原因でした。",
        ng="惜しい！return を実行するとその場で関数が終わることを思い出しましょう。",
    ),
    pred(
        title="スコープ", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''let x = 100;
function f() {
  let x = 10;
  return x + 1;
}
console.log(f());
console.log(x);
{
  let y = 1;
}
console.log(typeof y);''',
        out="11\n100\nundefined",
        wrong=[("11\n11\nundefined", "関数の中の x は別の変数（ローカル変数）で、外の x の値は書き換わりません。"), ("101\n100\nnumber", "関数 f の中では x = 10 が使われます。また { } の中の y は、外からは見えません。")],
        why="関数の中の x は外の x と別物で、{ } の中の y は外では存在しないから。",
        expl="f() の中では x = 10 なので 11 を返します。外の x は 100 のままです。let は { } の中だけで有効なので、外から y を使おうとしても、存在しない変数として扱われます（typeof は undefined を返します）。",
        concepts=["スコープ", "ローカル変数", "ブロックスコープ"], diff=3,
        hint="関数の中の x と、外の x は同じものでしょうか？",
        ok="正解！ローカル変数は外に影響しません。",
        ng="惜しい！同じ名前でも、スコープが違えば別の変数です。",
    ),
    pred(
        title="map と filter", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''const nums = [1, 2, 3, 4];
console.log(nums.map((n) => n * 2).join(","));
console.log(nums.filter((n) => n % 2 === 0).join(","));''',
        choices=[
            ("2,4,6,8\n2,4", ""),
            ("2,4,6,8\n1,3", "filter は、関数が true を返した要素を集めます。n % 2 === 0 は偶数の条件なので、2 と 4 が残ります。"),
            ("1,2,3,4\n2,4", "map は、各要素を関数の結果に変えた新しい配列を作ります。n * 2 で2倍になるので、元の値のままではありません。"),
        ],
        correct=0,
        why="map は各要素を2倍にし、filter は偶数だけを残すから。",
        expl="map は「変換」、filter は「選別」です。どちらも元の配列は変えず、新しい配列を返します。",
        concepts=["map", "filter", "コールバック"], diff=3,
        hint="map は変換、filter は条件に合うものだけ残すメソッドです。",
        ok="正解！map は変換、filter は選別です。",
        ng="惜しい！map と filter の働きを区別しましょう。",
    ),
    bugfix(
        title="アロー関数の return 忘れ", lang="javascript",
        prompt="add(1, 2) の結果 3 を表示するつもりが、undefined と表示されます。1行目を正しく書き直して入力してください（1行目の内容だけを入力）。",
        code='''const add = (a, b) => { a + b };
console.log(add(1, 2));''',
        fixed='''const add = (a, b) => a + b;
console.log(add(1, 2));''', out="3", buggy_out="undefined",
        target_line=1, accepted=["const add = (a, b) => a + b;", "const add = (a, b) => { return a + b; };", "const add = (a, b) => {return a + b;};", "const add = (a, b) => (a + b);", "const add = (a,b) => a + b;", "const add = (a, b) => a + b"],
        wrong=[("const add = (a, b) => { a + b };", "元のコードのままです。{ } を使うと、return を書かない限り、戻り値は undefined です。")],
        why="アロー関数で { } を使うときは、return で値を返す必要があるから。",
        expl="=> のあとに { } を書くと、普通の関数と同じ扱いになり、return がなければ undefined が返ります。{ } を外して式だけにするか、{ return a + b; } と書きます。",
        concepts=["アロー関数", "return"], diff=3,
        hint="{ } の中の a + b の結果は、どこに行くでしょう？",
        ok="正解！戻り値を返すようにしました。",
        ng="惜しい！{ } を使うときは return が必要です。",
    ),
    write_js(
        title="平均を返す関数", lang="javascript",
        prompt="数値の配列 numbers を受け取り、平均（合計 ÷ 個数）を返す関数 average(numbers) を作ってください。（表示ではなく return で返すこと。numbers は1つ以上の要素を持ちます）",
        starter="function average(numbers) {\n  // ここに書きましょう\n}\n",
        ref='''function average(numbers) {
  let total = 0;
  for (const n of numbers) {
    total += n;
  }
  return total / numbers.length;
}''',
        alts=['''const average = (numbers) => {
  let total = 0;
  for (let i = 0; i < numbers.length; i++) {
    total += numbers[i];
  }
  return total / numbers.length;
};''', '''function average(numbers) {
  return numbers.reduce((a, b) => a + b, 0) / numbers.length;
}'''],
        bads=[
            ('''function average(numbers) {
  let total = 0;
  for (const n of numbers) {
    total += n;
  }
  console.log(total / numbers.length);
}''', "console.log は表示するだけで、値を返しません。呼び出し元には undefined が返ります。"),
            ('''function average(numbers) {
  let total = 0;
  for (const n of numbers) {
    total += n;
    return total / numbers.length;
  }
}''', "return がループの中にあるので、最初の1要素だけで関数が終わってしまいます。"),
        ],
        req_any=[(r"function\s+average|average\s*=\s*(\(|[a-z])", "average という名前の関数として書いてください")],
        tests=[t_js_call("average([70, 80, 90])", "80"), t_js_call("average([1, 2])", "1.5"), t_js_call("average([100])", "100", visible=False), t_js_call("average([2, 4, 6, 8])", "5", visible=False)],
        why="合計を個数で割った値を return で返す関数にするから。",
        expl="for...of で合計を求め、numbers.length で割って return します。reduce などで書く別解もありますが、まずは for で書けるようにしましょう。表示（console.log）ではなく return するのがポイントです。",
        concepts=["関数", "return", "配列", "for...of"], diff=3,
        hint="合計を求めて、個数（numbers.length）で割った値を return します。",
        ok="正解！値を返す関数が書けました。",
        ng="惜しい！console.log ではなく return で返しているか確認しましょう。",
    ),
]
