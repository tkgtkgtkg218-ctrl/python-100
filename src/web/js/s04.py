from lib_web import mc, pred, fill, bugfix, write_js, t_js_out

STAGE = {
    "number": 4,
    "title": "繰り返し",
    "subtitle": "for、while、break / continue、入れ子のループ",
    "goals": [
        "for 文の3つの部分（初期化・条件・更新）の役割を説明できる",
        "for と while を使い分けて、決まった回数・条件付きの繰り返しを書ける",
        "合計を求めるなど、変数を更新しながら繰り返す書き方ができる",
        "break と continue の違いを説明できる",
        "無限ループの原因に気づける",
        "入れ子（ネスト）のループの動きを追える",
    ],
    "prerequisites": ["変数・演算子（ステージ1〜2）", "if と比較演算子（ステージ3）"],
    "topics": [
        "for 文（初期化 ; 条件 ; 更新）",
        "while 文",
        "合計を求める（累積）",
        "break と continue",
        "無限ループ",
        "入れ子のループ",
    ],
    "pitfalls": [
        "i < 5 は 0〜4（5 は含まれない）。5 回まわすには i < 5、1〜5 なら i <= 5",
        "while の中で条件に使う変数を更新し忘れると、終わらないループになる",
        "合計用の変数は、ループの前に 0 で用意する",
        "continue は「その回だけ飛ばす」、break は「ループ全体を終える」",
    ],
    "next_links": ["たくさんのデータをまとめて扱う「配列」と for を組み合わせます（ステージ5）"],
    "lesson": {
        "intro": "同じ処理を何十回、何百回とくり返すのは、コンピューターの得意技です。ページの中の複数の要素を順番に処理したり、リストを1つずつ画面に出したりするときにも使います。",
        "sections": [
            {
                "id": "S04-L1",
                "title": "for 文と while 文",
                "read_minutes": 3,
                "body": [
                    "for (初期化; 条件; 更新) { ... } は、決まった回数のくり返しに使います。例: for (let i = 0; i < 3; i++) は、i を 0 から始め、i < 3 の間、くり返すたびに i++ で 1 増やします。つまり i は 0, 1, 2 になり、3 回くり返します。i < 3 の 3 自体は含まれません。",
                    "while (条件) { ... } は、条件が true の間くり返します。回数が決まっていないときや、条件で終わりを決めたいときに使います。ループの中で、条件に使う変数を変化させないと、条件がずっと true のままになり、終わらなくなります（無限ループ）。",
                    "合計を求めるときは、ループの前に let total = 0; と用意し、ループの中で total += i; のように足していきます。",
                ],
                "glossary": [
                    {"term": "ループ", "definition": "同じ処理をくり返す仕組み。"},
                    {"term": "無限ループ", "definition": "終わる条件が成り立たず、いつまでも終わらないループ。"},
                    {"term": "累積", "definition": "ループの中で値を足し込み、合計などを作ること。"},
                ],
                "examples": [
                    {
                        "id": "S04-E1", "title": "for 文", "language": "javascript",
                        "code": '''for (let i = 0; i < 3; i++) {
  console.log(i);
}
let total = 0;
for (let i = 1; i <= 5; i++) {
  total += i;
}
console.log(total);''',
                        "expected_output": "0\n1\n2\n15",
                        "line_notes": ["1行目: i は 0 → 1 → 2 と増え、3 になると条件が false になって終わります。", "5行目: 1 から 5 まで含めるときは、i <= 5 と書きます。"],
                    },
                    {
                        "id": "S04-E2", "title": "while 文", "language": "javascript",
                        "code": '''let count = 3;
while (count > 0) {
  console.log(count);
  count--;
}
console.log("発射");''',
                        "expected_output": "3\n2\n1\n発射",
                        "line_notes": ["4行目: count を減らさないと、条件がずっと true のままで無限ループになります。"],
                    },
                ],
            },
            {
                "id": "S04-L2",
                "title": "break・continue・入れ子のループ",
                "read_minutes": 3,
                "body": [
                    "break は、その場でループ全体を終了します。continue は、その回の残りの処理を飛ばして、次の回へ進みます。",
                    "ループの中にさらにループを書くことができます（入れ子）。外側が 1 回進むたびに、内側のループは最初から最後まで回ります。文字を足し込んで図形を作る、表を作る、といった場面で使います。",
                ],
                "glossary": [
                    {"term": "break", "definition": "ループ全体をその場で終了する。"},
                    {"term": "continue", "definition": "その回の残りを飛ばして、次の回へ進む。"},
                    {"term": "入れ子（ネスト）", "definition": "ループの中にループを書くこと。"},
                ],
                "examples": [
                    {
                        "id": "S04-E3", "title": "continue と break", "language": "javascript",
                        "code": '''for (let i = 1; i <= 5; i++) {
  if (i === 3) {
    continue;
  }
  if (i === 5) {
    break;
  }
  console.log(i);
}''',
                        "expected_output": "1\n2\n4",
                        "line_notes": ["i が 3 のとき: continue で console.log を飛ばし、次の回へ。", "i が 5 のとき: break でループを終了。5 は表示されません。"],
                    },
                    {
                        "id": "S04-E4", "title": "入れ子のループ", "language": "javascript",
                        "code": '''for (let i = 1; i <= 3; i++) {
  let line = "";
  for (let j = 0; j < i; j++) {
    line += "*";
  }
  console.log(line);
}''',
                        "expected_output": "*\n**\n***",
                        "line_notes": ["外側の i が 1, 2, 3 と進むたびに、内側のループが i 回まわり、* を足します。", "line は外側のループの回ごとに空文字列に戻ります。"],
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "回数の数え間違い（i < 5）", "wrong_code": "for (let i = 1; i < 5; i++)  // 1〜5 のつもり", "why": "i < 5 は 5 を含みません（1〜4）。5 まで含めるには i <= 5 と書きます。", "fix": "for (let i = 1; i <= 5; i++)"},
            {"title": "while の更新忘れ", "wrong_code": "let n = 3;\nwhile (n > 0) {\n  console.log(n);\n}", "why": "n が変わらないので条件がずっと true。ページが固まる無限ループになります。", "fix": "ループの中に n--; を書く"},
            {"title": "合計の初期化忘れ", "wrong_code": "let total;\nfor (...) { total += i; }", "why": "total が undefined のまま足すと、結果は NaN になります。ループの前に 0 を入れます。", "fix": "let total = 0;"},
            {"title": "continue と break の取り違え", "wrong_code": "if (i === 3) { break; }  // 3 だけ飛ばしたい", "why": "break は 3 でループ全体が終わります。3 だけ飛ばしたいなら continue です。", "fix": "if (i === 3) { continue; }"},
        ],
        "checkpoints": [
            "for (初期化; 条件; 更新) の3つの役割",
            "i < 3 は 0・1・2 の3回（3 は含まれない）",
            "合計は先に 0 を用意して += で足す",
            "while は条件が true の間くり返す。中で条件の変数を更新する",
            "break は終了、continue は次の回へ",
            "入れ子では、外側が1回進むごとに内側が最初から回る",
        ],
        "next_bridge": "くり返しは、たくさんのデータに使うと本領を発揮します。まず問題で、回数や範囲を正確に追う練習をしましょう。",
    },
}

QUESTIONS = [
    pred(
        title="for 文の回数", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''for (let i = 0; i < 3; i++) {
  console.log(i);
}''',
        choices=[
            ("1\n2\n3", "i は 1 ではなく 0 から始まっています。初期化の部分 let i = 0 を確認しましょう。"),
            ("0\n1\n2", ""),
            ("0\n1\n2\n3", "条件は i < 3 なので、i が 3 になった時点でくり返しは終わり、3 は表示されません。"),
        ],
        correct=1,
        why="i は 0 から始まり、i < 3 が true の間、0・1・2 を表示するから。",
        expl="for (let i = 0; i < 3; i++) は「i を 0 にして、i が 3 未満の間、くり返し、1 回ごとに i を 1 増やす」という意味です。回数は 3 回で、3 自体は含まれません。",
        concepts=["for", "i++"], diff=1,
        hint="i の最初の値と、くり返しを続ける条件をそれぞれ確認しましょう。",
        ok="正解！i は 0 から始まり、3 未満の間くり返します。",
        ng="惜しい！初期化と条件の部分を確認しましょう。",
    ),
    pred(
        title="3ずつ増やす for 文", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''for (let i = 1; i <= 10; i += 3) {
  console.log(i);
}''',
        out="1\n4\n7\n10",
        wrong=[("1\n4\n7", "条件は i <= 10 なので、i が 10 のときもくり返します。10 は表示されます。"), ("1\n2\n3\n4", "更新の部分は i += 3 なので、1回ごとに 3 ずつ増えます。")],
        why="i は 1 から 3 ずつ増え、10 以下の間（1, 4, 7, 10）くり返すから。",
        expl="更新の部分は i++ だけでなく、i += 3 のように書くこともできます。1 → 4 → 7 → 10 → 13 となり、13 は条件 i <= 10 を満たさないので終わります。",
        concepts=["for", "+="], diff=2,
        hint="1 から 3 ずつ足して、10 以下かどうかを確認しましょう。",
        ok="正解！更新の式で増え方が決まります。",
        ng="惜しい！1, 4, 7 … と順に書き出してみましょう。",
    ),
    mc(
        title="for の条件の部分", lang="javascript",
        prompt="for (let i = 0; i < 5; i++) { ... } の「i < 5」の部分は、どんな役割ですか？",
        choices=[
            ("最初に1回だけ実行される、変数の準備", "それは最初の let i = 0 の部分（初期化）です。"),
            ("くり返しを続けるかどうかを、毎回判断する条件", ""),
            ("1回のくり返しが終わるごとに実行される、変数の更新", "それは最後の i++ の部分（更新）です。"),
        ],
        correct=1,
        why="2番目の部分は、くり返しのたびに調べられる、続行の条件だから。",
        expl="for の ( ) の中は、「初期化; 条件; 更新」の3つの部分です。初期化は最初に1回だけ、条件はくり返しの前に毎回、更新は1回のくり返しの後に毎回実行されます。",
        concepts=["for", "条件"], diff=2,
        hint="3つの部分は「初期化; 条件; 更新」の順です。",
        ok="正解！2番目は続行の条件です。",
        ng="惜しい！3つの部分の順番と役割を確認しましょう。",
    ),
    pred(
        title="while のカウントダウン", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''let n = 3;
while (n > 0) {
  console.log(n);
  n--;
}''',
        choices=[
            ("3\n2\n1\n0", "n が 0 になると、条件 n > 0 が false になり、くり返しに入りません。0 は表示されません。"),
            ("2\n1\n0", "console.log(n) を先に実行してから n を減らすので、最初に表示されるのは 3 です。"),
            ("3\n2\n1", ""),
        ],
        correct=2,
        why="表示してから n を減らし、n が 0 になると条件が false になって終わるから。",
        expl="n が 3 → 2 → 1 のときに、それぞれ表示されます。表示のあとで n-- されるので、n が 0 になった時点で条件が false になり、0 は表示されずに終了します。",
        concepts=["while", "n--"], diff=2,
        hint="n が 0 になったとき、n > 0 は true でしょうか？",
        ok="正解！条件が false になるまでくり返します。",
        ng="惜しい！n の値を1回ずつ追いましょう。",
    ),
    bugfix(
        title="終わらないループ", lang="javascript",
        prompt="n を 1 ずつ減らして 0 になったら終わるつもりが、このプログラムは終わりません。原因はどれですか？",
        code='''let n = 3;
while (n > 0) {
  n++;
}
console.log("終了");''',
        fixed='''let n = 3;
while (n > 0) {
  n--;
}
console.log("終了");''', out="終了", err="Timeout",
        choices=[
            ("while の条件 n > 0 の書き方が間違っている", "n > 0 は「n が 0 より大きい間」という正しい書き方です。問題は中で n が増えている点です。"),
            ("n++ で n が増え続け、条件がずっと true のままだから", ""),
            ("最後の console.log が { } の外にあるから", "{ } の外にある行は、ループが終わったあとに1回だけ実行される、正しい書き方です。"),
        ],
        correct=1, fmt="text",
        why="n が増える方向に更新されるため、n > 0 がいつまでも true だから。",
        expl="n は 3 → 4 → 5 と増え続け、0 以下になりません。n-- に直せば 3 → 2 → 1 → 0 と減って、条件が false になり、ループが終わります。",
        concepts=["無限ループ", "while"], diff=3,
        hint="1回ごとに n はどちらの方向に変わりますか？",
        ok="正解！更新の向きが逆でした。",
        ng="惜しい！ループの中で n がどう変わるか注目しましょう。",
    ),
    fill(
        title="合計を求める", lang="javascript",
        prompt="1 から 4 までの合計を求めます。10 と表示されるように、【空欄1】に入れる演算子を答えてください。",
        code='''let total = 0;
for (let i = 1; i <= 4; i++) {
  total __1__ i;
}
console.log(total);''',
        blanks=[(["+="], False)],
        out="10",
        wrong=[("b1", "=", "= は上書きなので、毎回 total が i に置き換わり、最後は 4 と表示されます。足し込むには += です。")],
        why="ループの中で total に i を足し込んでいくには、+= を使うから。",
        expl="total += i は total = total + i と同じです。1 + 2 + 3 + 4 = 10 になります。= だと、前の値が消えてしまいます。",
        concepts=["累積", "+="], diff=2,
        hint="「足して代入し直す」演算子です。",
        ok="正解！+= で足し込めます。",
        ng="惜しい！= だと上書きになります。",
    ),
    pred(
        title="continue と break", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''for (let i = 1; i <= 5; i++) {
  if (i === 2) {
    continue;
  }
  if (i === 4) {
    break;
  }
  console.log(i);
}''',
        out="1\n3",
        wrong=[("1\n2\n3", "i が 2 のときは continue で console.log を飛ばすので、2 は表示されません。"), ("1\n3\n5", "i が 4 のとき break でループ全体が終わるので、5 には到達しません。")],
        why="2 は continue で飛ばされ、4 で break してループが終わるから。",
        expl="i = 1 は表示。i = 2 は continue で次の回へ。i = 3 は表示。i = 4 で break し、ループそのものが終了します。そのため 1 と 3 だけが表示されます。",
        concepts=["continue", "break"], diff=3,
        hint="continue は「この回だけ飛ばす」、break は「ループを終える」です。",
        ok="正解！continue と break の違いを理解できています。",
        ng="惜しい！i の値ごとに、何が起きるか表に書いてみましょう。",
    ),
    pred(
        title="入れ子のループ", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください（複数行は改行して入力）。",
        code='''for (let i = 1; i <= 3; i++) {
  let line = "";
  for (let j = 0; j < i; j++) {
    line += "*";
  }
  console.log(line);
}''',
        out="*\n**\n***",
        wrong=[("***\n***\n***", "内側のループの回数は i です。i が 1, 2, 3 と増えるので、* の数も増えます。"), ("*\n*\n*", "内側のループの中で line に * を足し込むので、i が大きいほど * が増えます。")],
        why="外側の i が 1, 2, 3 と増え、内側で i 個の * が足されるから。",
        expl="i = 1 のとき内側は 1 回で \"*\"、i = 2 のとき 2 回で \"**\"、i = 3 のとき 3 回で \"***\"。line は外側の1回ごとに空文字列に戻り、そのたびに1行表示されます。",
        concepts=["入れ子のループ", "文字列の連結"], diff=3,
        hint="外側の i が1つ進むごとに、内側のループは最初から回ります。",
        ok="正解！入れ子のループを正確に追えました。",
        ng="惜しい！i ごとに内側が何回まわるかを確認しましょう。",
    ),
    bugfix(
        title="合計が合わない（範囲のミス）", lang="javascript",
        prompt="1 から 5 までの合計 15 を求めるつもりが、10 と表示されます。2行目を正しく書き直して入力してください（2行目の内容だけを入力）。",
        code='''let total = 0;
for (let i = 1; i < 5; i++) {
  total += i;
}
console.log(total);''',
        fixed='''let total = 0;
for (let i = 1; i <= 5; i++) {
  total += i;
}
console.log(total);''', out="15", buggy_out="10",
        target_line=2, accepted=["for (let i = 1; i <= 5; i++) {", "for (let i = 1; i < 6; i++) {", "for (let i = 1; i <= 5; i++){", "for (let i = 1; i < 6; i++){"],
        wrong=[("for (let i = 1; i < 5; i++) {", "元のコードのままです。i < 5 だと 5 は含まれず、1〜4 の合計 10 になります。")],
        why="5 まで含めるには、条件を i <= 5（または i < 6）にする必要があるから。",
        expl="i < 5 は、i が 5 になった時点で終わるため、5 を足せません。「以下」を表す <= を使って i <= 5 にします。回数の数え間違いは「オフバイワン」と呼ばれる、よくあるミスです。",
        concepts=["for", "オフバイワン", "比較演算子"], diff=3,
        hint="i が 5 のとき、条件 i < 5 は true でしょうか？",
        ok="正解！5 を含める条件にしました。",
        ng="惜しい！条件が i = 5 のときに true になるか確認しましょう。",
    ),
    write_js(
        title="1 から n までの合計", lang="javascript",
        prompt="変数 n に正の整数が入っています。1 から n までの整数の合計を、くり返し（for または while）を使って求め、console.log で表示するコードを書いてください。",
        starter="// n はあらかじめ用意されています\n",
        ref='''let total = 0;
for (let i = 1; i <= n; i++) {
  total += i;
}
console.log(total);''',
        alts=['''let total = 0;
let i = 1;
while (i <= n) {
  total += i;
  i++;
}
console.log(total);'''],
        bads=[
            ('''let total = 0;
for (let i = 1; i < n; i++) {
  total += i;
}
console.log(total);''', "i < n だと n が足されません。n まで含めるには i <= n です。"),
            ("console.log(15);", "決まった数値を書くと、n が変わったときに正しい結果になりません。くり返しで求めましょう。"),
        ],
        req_any=[(r"\bfor\b", "for を使ってください"), (r"\bwhile\b", "while を使ってください")],
        tests=[t_js_out("15\n", setup="const n = 5;"), t_js_out("1\n", setup="const n = 1;", visible=False), t_js_out("5050\n", setup="const n = 100;", visible=False), t_js_out("55\n", setup="const n = 10;", visible=False)],
        why="合計用の変数を 0 で用意し、1 から n までくり返して足し込むから。",
        expl="let total = 0; で用意し、i を 1 から n まで動かして total に足します。for の条件は i <= n と書くのがポイントです。n = 1 のときなど、端の値でも確かめましょう。",
        concepts=["for", "累積", "while"], diff=3,
        hint="合計用の変数を 0 で用意して、ループの中で足し込みます。条件は i <= n です。",
        ok="正解！くり返しで合計を求められました。",
        ng="惜しい！n = 1 のとき、n = 5 のときの結果を手計算して比べましょう。",
    ),
]
