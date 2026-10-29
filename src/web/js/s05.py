from lib_web import mc, pred, fill, bugfix, write_js, t_js_out

STAGE = {
    "number": 5,
    "title": "配列",
    "subtitle": "配列の作り方・添字・追加と削除・for...of",
    "goals": [
        "配列を作り、添字（0 始まり）で要素を取り出したり置き換えたりできる",
        "length・push・pop・includes・indexOf・join・slice を使える",
        "範囲外の添字は undefined になる（エラーにならない）ことを理解する",
        "for と for...of で配列の要素を順に処理できる",
        "const の配列でも中身を変更できることを説明できる",
    ],
    "prerequisites": ["変数・データ型（ステージ1）", "演算子（ステージ2）", "if（ステージ3）", "for（ステージ4）"],
    "topics": [
        "配列リテラル [ ] と添字",
        "length と最後の要素",
        "要素の置き換え・push・pop",
        "includes・indexOf・join・slice",
        "for と for...of",
        "const と配列の関係",
    ],
    "pitfalls": [
        "添字は 0 から始まる。最後の要素は arr[arr.length - 1]",
        "範囲外の添字を読んでも undefined になる（エラーにならない）",
        "for の条件を i <= arr.length にすると、1つ多くまわってしまう",
        "push は ( )、添字は [ ]。arr.push[4] のように書き間違えない",
        "const の配列にも push できる（再代入だけが禁止）",
    ],
    "next_links": ["名前と値のセットをまとめる「オブジェクト」を学びます（ステージ6）"],
    "lesson": {
        "intro": "100 人分の点数を、100 個の変数に入れるのは大変です。配列を使うと、複数の値を1つの名前でまとめて扱えます。ステージ4の for と組み合わせると、データを順番に処理できます。Webページの中の「リスト」を扱うときにも欠かせません。",
        "sections": [
            {
                "id": "S05-L1",
                "title": "配列の基本",
                "read_minutes": 3,
                "body": [
                    "配列は、値を [ ] の中に , で区切って並べて作ります。例: const fruits = [\"りんご\", \"みかん\", \"ぶどう\"];。要素は番号（添字）で取り出し、番号は 0 から始まります。最初の要素は fruits[0] です。",
                    "fruits.length は要素の数（ここでは 3）で、最後の要素は fruits[fruits.length - 1] です。存在しない番号（fruits[5] など）を読んでも、エラーにはならず undefined になります。",
                    "fruits[1] = \"レモン\"; で要素を置き換え、push(値) で末尾に追加、pop() で末尾から取り出して削除します。const で宣言した配列にも、push などで中身を変更できます。const が禁止するのは、変数そのものへの再代入（fruits = [] など）だけです。",
                ],
                "glossary": [
                    {"term": "配列", "definition": "複数の値を順番に並べてまとめたデータ。"},
                    {"term": "要素", "definition": "配列の中の1つ1つの値。"},
                    {"term": "添字（インデックス）", "definition": "要素の位置を表す番号。0 から始まる。"},
                ],
                "examples": [
                    {
                        "id": "S05-E1", "title": "取り出しと長さ", "language": "javascript",
                        "code": '''const fruits = ["りんご", "みかん", "ぶどう"];
console.log(fruits[0]);
console.log(fruits[fruits.length - 1]);
console.log(fruits.length);
console.log(fruits[5]);''',
                        "expected_output": "りんご\nぶどう\n3\nundefined",
                        "line_notes": ["2行目: 添字 0 は最初の要素。", "3行目: 最後の要素の添字は length - 1。", "5行目: 範囲外はエラーにならず undefined になります。"],
                    },
                    {
                        "id": "S05-E2", "title": "置き換え・追加・削除", "language": "javascript",
                        "code": '''const nums = [10, 20, 30];
nums[1] = 99;
nums.push(40);
const last = nums.pop();
console.log(nums.join(","));
console.log(last);
console.log(nums.length);''',
                        "expected_output": "10,99,30\n40\n3",
                        "line_notes": ["4行目: pop() は末尾の要素を取り出して削除し、その値を返します。", "5行目: join(\",\") は、要素を , でつないだ文字列にします。"],
                    },
                ],
            },
            {
                "id": "S05-L2",
                "title": "配列を調べる・順に処理する",
                "read_minutes": 3,
                "body": [
                    "includes(値) は、その値が含まれているかを true / false で返します。indexOf(値) は、最初に見つかった位置を返し、なければ -1 を返します。slice(開始, 終了) は一部を新しい配列として取り出し、終了の位置の要素は含まれません。",
                    "配列の要素を1つずつ処理するには、添字を使う for のほか、for (const x of 配列) { ... } が使えます。for...of は、要素が順に x に入ります。添字で回すときは、i < arr.length と書きます（i <= arr.length だと1つ多くなります）。",
                    "console.log に配列をそのまま渡すと、配列全体が表示されます（表示の形式は環境によって少し違います）。このコースの問題では、join で文字列にして表示します。",
                ],
                "glossary": [
                    {"term": "for...of", "definition": "配列などの要素を、1つずつ取り出して処理する繰り返し。"},
                    {"term": "slice", "definition": "配列の一部を、新しい配列として取り出すメソッド。終了の位置は含まれない。"},
                ],
                "examples": [
                    {
                        "id": "S05-E3", "title": "includes・indexOf・slice", "language": "javascript",
                        "code": '''const colors = ["赤", "青", "緑", "黄"];
console.log(colors.includes("青"));
console.log(colors.indexOf("緑"));
console.log(colors.indexOf("白"));
console.log(colors.slice(1, 3).join("-"));''',
                        "expected_output": "true\n2\n-1\n青-緑",
                        "line_notes": ["4行目: 見つからないと -1 です。", "5行目: slice(1, 3) は添字 1 と 2 の2つだけ（3 は含まれません）。"],
                    },
                    {
                        "id": "S05-E4", "title": "for...of で合計", "language": "javascript",
                        "code": '''const scores = [70, 85, 90];
let total = 0;
for (const s of scores) {
  total += s;
}
console.log(total);
let count = 0;
for (let i = 0; i < scores.length; i++) {
  count++;
}
console.log(count);''',
                        "expected_output": "245\n3",
                        "line_notes": ["3行目: scores の要素が1つずつ s に入ります。", "8行目: 添字で回すときは i < scores.length と書きます。"],
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "1番目を [1] と思う", "wrong_code": "console.log(fruits[1]);  // 最初の要素のつもり", "why": "添字は 0 から始まります。fruits[1] は2番目の要素です。", "fix": "console.log(fruits[0]);"},
            {"title": "push を [ ] で書く", "wrong_code": "arr.push[4];", "why": "push は関数なので ( ) で呼びます。[ ] だと何も追加されず、エラーにもなりません。", "fix": "arr.push(4);"},
            {"title": "i <= arr.length", "wrong_code": "for (let i = 0; i <= arr.length; i++)", "why": "最後に arr[arr.length]（undefined）まで読んでしまい、合計が NaN になるなどのミスになります。", "fix": "for (let i = 0; i < arr.length; i++)"},
            {"title": "const の配列は変更できないと思う", "wrong_code": "const list = [1];\nlist.push(2);  // エラーになると思い込む", "why": "const は再代入を禁止するだけで、配列の中身の変更はできます。", "fix": "list = [3]; のような再代入が TypeError になる"},
        ],
        "checkpoints": [
            "添字は 0 から。最後は arr[arr.length - 1]",
            "範囲外の添字は undefined（エラーにならない）",
            "push は末尾に追加、pop は末尾から削除",
            "includes・indexOf（見つからないと -1）・join・slice",
            "for...of で要素を順に取り出せる",
            "const の配列にも push できる",
        ],
        "next_bridge": "配列で、順番のあるデータを扱えるようになりました。問題で、添字と範囲の扱いを確かめましょう。",
    },
}

QUESTIONS = [
    mc(
        title="最初の要素の取り出し方", lang="javascript",
        prompt="const colors = [\"赤\", \"青\", \"緑\"]; という配列から、最初の要素「赤」を取り出す式はどれですか？",
        fmt="code",
        choices=[
            ("colors[1]", "添字は 0 から始まります。colors[1] は2番目の要素「青」です。"),
            ("colors(0)", "要素の取り出しには [ ] を使います。( ) は関数を呼び出す記号で、colors は関数ではないので TypeError になります。"),
            ("colors[0]", ""),
        ],
        correct=2,
        why="配列の添字は 0 から始まり、取り出しには [ ] を使うから。",
        expl="colors[0] が「赤」、colors[1] が「青」、colors[2] が「緑」です。プログラミングでは、数え始めを 0 にするのが一般的です。",
        concepts=["配列", "添字"], diff=1,
        hint="数え始めは 0 です。",
        ok="正解！最初の要素は [0] です。",
        ng="惜しい！添字は 0 から始まり、取り出しには [ ] を使います。",
    ),
    pred(
        title="length と範囲外の添字", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''const nums = [4, 8, 15, 16];
console.log(nums.length);
console.log(nums[nums.length - 1]);
console.log(nums[4]);''',
        choices=[
            ("3\n16\nundefined", "length は最後の添字ではなく、要素の数です。要素は4つあるので 4 です。"),
            ("4\n16\nundefined", ""),
            ("4\n16\nエラー", "範囲外の添字を読んでも、JavaScript ではエラーにならず undefined になります（エラーになる言語もあるので注意）。"),
        ],
        correct=1,
        why="要素は4つで、最後の要素は添字 3 の 16、範囲外の添字 4 は undefined になるから。",
        expl="length は要素の数 4 を返します。最後の要素は nums[length - 1] = nums[3] で 16。nums[4] は存在しないので undefined です。",
        concepts=["length", "undefined", "範囲外"], diff=2,
        hint="添字は 0〜3 までです。4 はどうなるでしょう？",
        ok="正解！範囲外は undefined です。",
        ng="惜しい！length は個数、範囲外の添字は undefined です。",
    ),
    pred(
        title="置き換え・追加・削除", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''const nums = [10, 20, 30];
nums[1] = 99;
nums.push(40);
nums.pop();
console.log(nums.join(","));
console.log(nums.length);''',
        out="10,99,30\n3",
        wrong=[("10,20,30\n3", "nums[1] = 99 で、2つ目の要素（添字 1）が 99 に置き換わっています。"), ("10,99,30,40\n4", "最後の pop() が末尾の 40 を削除しています。")],
        why="2つ目が 99 に置き換わり、40 を追加したあと pop() で削除されるから。",
        expl="nums は [10, 20, 30] → [10, 99, 30] → [10, 99, 30, 40] → [10, 99, 30] と変わります。join(\",\") で , でつないだ文字列にして表示します。",
        concepts=["push", "pop", "要素の置き換え"], diff=2,
        hint="1行ずつ、配列の中身がどう変わるか書き出しましょう。",
        ok="正解！配列の中身の変化を追えました。",
        ng="惜しい！1行ずつ配列の中身を書き出しましょう。",
    ),
    bugfix(
        title="push の書き間違い", lang="javascript",
        prompt="配列 a に 4 を追加して、length の 4 を表示したいのに 3 と表示されます。2行目を直したものはどれですか？",
        code='''const a = [1, 2, 3];
a.push[4];
console.log(a.length);''',
        fixed='''const a = [1, 2, 3];
a.push(4);
console.log(a.length);''', out="4", buggy_out="3", target_line=2,
        choices=[
            ("a.add(4);", "配列に add というメソッドはありません。a.add is not a function という TypeError になります。"),
            ("a.push(4);", ""),
            ("a.push 4;", "メソッドを呼び出すときは ( ) が必要です。( ) がないと SyntaxError になります。"),
        ],
        correct=1, fmt="code",
        why="push はメソッドなので、( ) を付けて呼び出す必要があるから。",
        expl="a.push[4] は「push という値の、添字 4 の要素」を読み出しているだけで、何も追加されません。エラーにもならないので、気づきにくいミスです。呼び出しには ( ) を使います。",
        concepts=["push", "メソッド呼び出し"], diff=2,
        hint="関数やメソッドを呼び出すとき、使う記号は [ ] ですか？ ( ) ですか？",
        ok="正解！メソッドは ( ) で呼び出します。",
        ng="惜しい！呼び出しに使う記号を確認しましょう。",
    ),
    fill(
        title="配列の要素を順に足す", lang="javascript",
        prompt="配列 scores の点数を合計して 245 と表示したい。【空欄1】に入れるものを答えてください。",
        code='''const scores = [70, 85, 90];
let total = 0;
for (const s of __1__) {
  total += s;
}
console.log(total);''',
        blanks=[(["scores"], False)],
        out="245",
        wrong=[("b1", "scores[0]", "scores[0] は最初の要素 70（数値）で、数値は for...of で順に取り出せないため TypeError になります。配列そのものを書きます。")],
        why="for...of は、配列そのものを渡すと要素を1つずつ取り出してくれるから。",
        expl="for (const s of scores) と書くと、scores の要素 70, 85, 90 が順に s に入ります。total に足していくと 245 です。",
        concepts=["for...of", "累積"], diff=2,
        hint="of のあとには、取り出し元の配列の名前を書きます。",
        ok="正解！for...of で配列を順に処理できます。",
        ng="惜しい！取り出す元の配列そのものを書きましょう。",
    ),
    pred(
        title="includes と indexOf", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''const colors = ["赤", "青", "緑"];
console.log(colors.includes("青"));
console.log(colors.indexOf("緑"));
console.log(colors.indexOf("白"));''',
        out="true\n2\n-1",
        wrong=[("true\n3\n-1", "添字は 0 から始まるので、「緑」は3番目ですが添字は 2 です。"), ("true\n2\nundefined", "indexOf は、見つからないときに undefined ではなく -1 を返します。")],
        why="「青」は含まれて true、「緑」の添字は 2、「白」は見つからず -1 になるから。",
        expl="indexOf は、見つかった最初の位置の添字を返します。見つからないときの -1 は、「その位置はない」という目印として、if の条件などによく使われます。",
        concepts=["includes", "indexOf"], diff=2,
        hint="見つからないときの戻り値は、特別な数値です。",
        ok="正解！見つからないと -1 です。",
        ng="惜しい！添字は 0 から数えます。",
    ),
    mc(
        title="const の配列と push", lang="javascript",
        prompt="const nums = [1, 2]; と宣言した配列に、nums.push(3); を実行するとどうなりますか？",
        choices=[
            ("TypeError になる。const の配列は変更できない", "const が禁止するのは、変数 nums そのものへの再代入（nums = [] など）だけです。配列の中身の変更はできます。"),
            ("要素が追加される。const は変数への再代入を禁止するだけである", ""),
            ("新しい配列が作られ、変数 nums がそれを指すように変わる", "push は、元の配列そのものに要素を追加します。新しい配列は作られず、nums が指す先も変わりません。"),
        ],
        correct=1,
        why="const は再代入を禁止するだけで、配列の中身の変更までは禁止しないから。",
        expl="配列やオブジェクトは「中身を持つ入れ物」で、const の変数はその入れ物を指します。入れ物の中身を変えることはできますが、別の入れ物を指すように再代入することはできません。",
        concepts=["const", "push"], diff=3,
        hint="const が禁止しているのは「変数への再代入」です。",
        ok="正解！const でも中身は変更できます。",
        ng="惜しい！const が禁止するのは再代入だけです。",
    ),
    bugfix(
        title="1つ多くまわるループ", lang="javascript",
        prompt="点数の合計 245 を求めるつもりが、NaN と表示されます。2行目を正しく書き直して入力してください（2行目の内容だけを入力）。",
        code='''const scores = [70, 85, 90];
let total = 0;
for (let i = 0; i <= scores.length; i++) {
  total += scores[i];
}
console.log(total);''',
        fixed='''const scores = [70, 85, 90];
let total = 0;
for (let i = 0; i < scores.length; i++) {
  total += scores[i];
}
console.log(total);''', out="245", buggy_out="NaN",
        target_line=3, accepted=["for (let i = 0; i < scores.length; i++) {", "for (let i = 0; i < scores.length; i++){", "for (let i = 0; i <= scores.length - 1; i++) {"],
        wrong=[("for (let i = 0; i <= scores.length; i++) {", "元のコードのままです。i が 3 のとき scores[3] は undefined で、total += undefined が NaN になります。")],
        why="添字は 0〜length - 1 までなので、条件は i < scores.length にする必要があるから。",
        expl="i <= scores.length だと、i が 3 のときも続けます。scores[3] は undefined で、数値に undefined を足すと NaN になります。範囲外の読み取りがエラーにならないので、結果を見て気づく必要があります。",
        concepts=["for", "length", "NaN", "範囲外"], diff=3,
        hint="最後の添字は length より1つ小さい値です。",
        ok="正解！添字の範囲を正しくしました。",
        ng="惜しい！i が最後にいくつになるか確認しましょう。",
    ),
    pred(
        title="slice と join", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''const a = [1, 2, 3, 4, 5];
console.log(a.slice(1, 3).join("-"));
console.log(a.join(""));''',
        choices=[
            ("2-3-4\n12345", "slice(1, 3) の終わりの位置（3）の要素は含まれません。添字 1 と 2 の「2」と「3」だけです。"),
            ("2-3\n12345", ""),
            ("1-2\n1,2,3,4,5", "slice の開始は添字 1（2つ目の要素）です。また、join(\"\") は空の文字列でつなぐので、カンマは入りません。"),
        ],
        correct=1,
        why="slice(1, 3) は添字 1 と 2 の要素を取り出し、join(\"\") は区切りなしでつなぐから。",
        expl="slice(開始, 終了) は、開始の位置から、終了の位置の1つ手前までを取り出します（終了は含まれない）。join の引数に何も入れないつなぎ方（\"\"）だと、数字がそのまま並びます。",
        concepts=["slice", "join"], diff=3,
        hint="slice の終了の位置は含まれません。",
        ok="正解！slice の終了は含まれません。",
        ng="惜しい！slice の範囲と、join の区切りを確認しましょう。",
    ),
    write_js(
        title="偶数だけを集める", lang="javascript",
        prompt="配列 nums に整数が入っています。偶数だけを順番に集めて、, でつないだ文字列を console.log で表示するコードを書いてください（偶数がなければ空の行が表示されます）。くり返し（for / while）を使うこと。",
        starter="// nums はあらかじめ用意されています\n",
        ref='''const evens = [];
for (const n of nums) {
  if (n % 2 === 0) {
    evens.push(n);
  }
}
console.log(evens.join(","));''',
        alts=['''const evens = [];
for (let i = 0; i < nums.length; i++) {
  if (nums[i] % 2 === 0) evens.push(nums[i]);
}
console.log(evens.join(","));'''],
        bads=[
            ('''console.log(nums.join(","));''', "すべての要素を表示しています。偶数だけを集めるには、if で判定して push します。"),
            ('''const evens = [];
for (const n of nums) {
  if (n % 2 === 1) {
    evens.push(n);
  }
}
console.log(evens.join(","));''', "n % 2 === 1 は奇数の条件です。偶数は 2 で割った余りが 0 です。"),
        ],
        req_any=[(r"\bfor\b", "for を使ってください"), (r"\bwhile\b", "while を使ってください")],
        tests=[
            t_js_out("2,4,6\n", setup="const nums = [1, 2, 3, 4, 5, 6];"), t_js_out("2\n", setup="const nums = [2];", visible=False),
            t_js_out("\n", setup="const nums = [1, 3];", visible=False), t_js_out("10,20\n", setup="const nums = [10, 15, 20];", visible=False),
            t_js_out("0,-4\n", setup="const nums = [0, 3, -4];", visible=False),
        ],
        why="for で1つずつ調べ、偶数のときだけ別の配列に push し、最後に join でつなぐから。",
        expl="空の配列 evens を用意し、くり返しの中で n % 2 === 0 のときだけ push します。最後に evens.join(\",\") で文字列にします。偶数がないときは、空の配列の join が空の文字列になります。",
        concepts=["配列", "push", "for...of", "%", "join"], diff=3,
        hint="空の配列を用意し、条件に合う要素だけを push します。",
        ok="正解！条件に合う要素だけを集められました。",
        ng="惜しい！偶数がないときや、0・負の数のときの結果を確認しましょう。",
    ),
]
