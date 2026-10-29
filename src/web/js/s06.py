from lib_web import mc, pred, fill, bugfix, write_js, t_js_out

STAGE = {
    "number": 6,
    "title": "オブジェクト",
    "subtitle": "プロパティ、ネスト、Object.keys、配列との組み合わせ",
    "goals": [
        "オブジェクトを作り、プロパティの読み出し・追加・更新・削除ができる",
        "ドット記法と角括弧記法を使い分けられる",
        "オブジェクトの中のオブジェクト（ネスト）や、オブジェクトの配列を扱える",
        "Object.keys で全プロパティを順に処理できる",
        "存在しないプロパティ（undefined）の中身を読むと TypeError になることを説明できる",
    ],
    "prerequisites": ["変数・演算子・if・for（ステージ1〜4）", "配列と for...of（ステージ5）"],
    "topics": [
        "オブジェクトリテラル { キー: 値 }",
        "ドット記法と角括弧記法",
        "プロパティの追加・更新・削除、in 演算子",
        "ネストしたオブジェクト、オブジェクトの配列",
        "Object.keys と JSON.stringify",
        "undefined のプロパティを読むエラー",
    ],
    "pitfalls": [
        "変数に入れたキー名で取り出すときは、user.key ではなく user[key]",
        "存在しないプロパティを読むと undefined。その中身をさらに読むと TypeError",
        "プロパティの存在確認に includes は使えない（in 演算子を使う）",
        "const のオブジェクトも、プロパティは変更できる",
    ],
    "next_links": ["処理に名前を付けて部品にする「関数」を学びます（ステージ7）"],
    "lesson": {
        "intro": "配列は「順番」でデータを並べました。オブジェクトは「名前（キー）」でデータを並べます。「名前は Hana、年齢は 12」のように、1つのものについての複数の情報をまとめられます。Webページの要素の情報や、サーバーから届くデータなど、JavaScript のあらゆる場面で使われます。",
        "sections": [
            {
                "id": "S06-L1",
                "title": "オブジェクトの基本",
                "read_minutes": 3,
                "body": [
                    "オブジェクトは { } の中に キー: 値 を , で区切って書きます。例: const user = { name: \"Hana\", age: 12 };。値は user.name のようにドット記法で、または user[\"name\"] のように角括弧記法で取り出します。存在しないキーを読むと undefined になります。",
                    "変数に入れたキー名で取り出したいときは、角括弧記法を使います。const key = \"age\"; user[key] は 12 ですが、user.key は「key という名前のプロパティ」を探すので undefined になります。",
                    "user.age = 13; で更新、user.city = \"東京\"; で追加、delete user.name; で削除です。\"age\" in user で、プロパティがあるかを true / false で調べられます。const のオブジェクトでも、プロパティの変更はできます。",
                    "JSON.stringify(オブジェクト) は、オブジェクトを JSON という文字列にします。console.log でオブジェクトの中身を確かめるときに便利です。",
                ],
                "glossary": [
                    {"term": "オブジェクト", "definition": "キーと値のペア（プロパティ）をまとめたデータ。"},
                    {"term": "プロパティ", "definition": "オブジェクトの中の、キーと値の1組。"},
                    {"term": "JSON", "definition": "データを文字列で表す形式。JSON.stringify でオブジェクトを変換できる。"},
                ],
                "examples": [
                    {
                        "id": "S06-E1", "title": "読み出し", "language": "javascript",
                        "code": '''const user = { name: "Hana", age: 12 };
console.log(user.name);
console.log(user["age"]);
console.log(user.city);
const key = "age";
console.log(user[key]);
console.log(user.key);
console.log("age" in user);''',
                        "expected_output": "Hana\n12\nundefined\n12\nundefined\ntrue",
                        "line_notes": ["4行目: 存在しないキーを読むと undefined です。", "6行目: 変数のキー名で取り出すには角括弧記法を使います。", "7行目: user.key は「key」という名前のプロパティを探すので undefined です。"],
                    },
                    {
                        "id": "S06-E2", "title": "追加・更新・削除", "language": "javascript",
                        "code": '''const user = { name: "Hana", age: 12 };
user.age = 13;
user.city = "東京";
delete user.name;
console.log(JSON.stringify(user));''',
                        "expected_output": "{\"age\":13,\"city\":\"東京\"}",
                        "line_notes": ["2行目: 既にあるプロパティは更新されます。", "3行目: ないプロパティは追加されます。", "4行目: delete でプロパティが削除されます。"],
                    },
                ],
            },
            {
                "id": "S06-L2",
                "title": "ネスト・オブジェクトの配列・Object.keys",
                "read_minutes": 3,
                "body": [
                    "オブジェクトの値には、別のオブジェクトや配列も入れられます（ネスト）。book.author.name のように、ドットをつなげて奥まで読みます。途中が undefined だと、その先を読んだときに TypeError（Cannot read properties of undefined）になります。",
                    "オブジェクトを要素にもつ配列は、ユーザー一覧や商品一覧によく使われます。users[1].name のように、添字とドットを組み合わせて読みます。",
                    "Object.keys(オブジェクト) は、キーの配列を返します。for (const key of Object.keys(obj)) と組み合わせると、すべてのプロパティを順に処理できます。値は obj[key] で取り出します。",
                ],
                "glossary": [
                    {"term": "ネスト", "definition": "入れ物の中に、さらに入れ物を入れること。"},
                    {"term": "Object.keys", "definition": "オブジェクトのキーを、配列として返す。"},
                ],
                "examples": [
                    {
                        "id": "S06-E3", "title": "ネストと配列", "language": "javascript",
                        "code": '''const book = { title: "JS入門", author: { name: "Taro", age: 30 } };
console.log(book.author.name);
const users = [{ name: "A", age: 20 }, { name: "B", age: 17 }];
console.log(users[1].name);
console.log(users.length);
console.log(users[0].age + users[1].age);''',
                        "expected_output": "Taro\nB\n2\n37",
                        "line_notes": ["2行目: ドットをつなげて、奥のプロパティを読みます。", "4行目: users[1] は2番目のオブジェクトです。"],
                    },
                    {
                        "id": "S06-E4", "title": "Object.keys でくり返す", "language": "javascript",
                        "code": '''const scores = { math: 80, english: 70 };
let total = 0;
for (const key of Object.keys(scores)) {
  console.log(key + ": " + scores[key]);
  total += scores[key];
}
console.log(total);''',
                        "expected_output": "math: 80\nenglish: 70\n150",
                        "line_notes": ["3行目: Object.keys(scores) は [\"math\", \"english\"] です。", "4行目: scores[key] で、そのキーの値を取り出します。"],
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "変数のキー名を user.key と書く", "wrong_code": "const key = \"age\";\nconsole.log(user.key);", "why": "user.key は、key という名前のプロパティを探します。変数の値をキー名にしたいときは user[key]。", "fix": "console.log(user[key]);"},
            {"title": "存在しないプロパティの中身を読む", "wrong_code": "console.log(user.address.city);", "why": "user.address が undefined なので、その中の city を読もうとして TypeError になります。", "fix": "address を持たせる、または存在を確認してから読む"},
            {"title": "プロパティの確認に includes を使う", "wrong_code": "user.includes(\"age\")", "why": "includes は配列・文字列のメソッドで、オブジェクトにはありません（TypeError）。in 演算子を使います。", "fix": "\"age\" in user"},
            {"title": "カウントの初期値", "wrong_code": "counts[ch] = 0;  // 初めて出てきた文字", "why": "初めて出てきた時点で1回出ているので、初期値は 1 です。", "fix": "counts[ch] = 1;"},
        ],
        "checkpoints": [
            "{ キー: 値 } で作り、ドット記法か角括弧記法で読む",
            "変数のキー名は角括弧記法で取り出す",
            "追加・更新は代入、削除は delete、存在確認は in",
            "存在しないプロパティは undefined、その中身を読むと TypeError",
            "Object.keys と for...of で全プロパティを処理できる",
            "オブジェクトの配列は users[0].name のように読む",
        ],
        "next_bridge": "オブジェクトで、「名前付きのデータ」を扱えるようになりました。問題で、プロパティの読み出しや、ネストした構造の扱いを確かめましょう。",
    },
}

QUESTIONS = [
    pred(
        title="プロパティの読み出し", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''const user = { name: "Hana", age: 12 };
console.log(user.name);
console.log(user["age"]);
console.log(user.city);''',
        choices=[
            ("Hana\n12\nエラー", "存在しないプロパティを読んでも、エラーにはならず undefined になります。"),
            ("name\nage\nundefined", "user.name は、キーの名前ではなく、そのキーに入っている値を返します。"),
            ("Hana\n12\nundefined", ""),
        ],
        correct=2,
        why="user.name は \"Hana\"、user[\"age\"] は 12、存在しない city は undefined になるから。",
        expl="ドット記法と角括弧記法は、どちらもプロパティの値を取り出します。存在しないキーを読んでも、エラーにはならず undefined になります。",
        concepts=["オブジェクト", "プロパティ", "undefined"], diff=1,
        hint="存在しないキーを読むと、どうなるでしょうか。",
        ok="正解！存在しないプロパティは undefined です。",
        ng="惜しい！値を取り出すこと、存在しないキーの扱いを確認しましょう。",
    ),
    pred(
        title="追加・更新・削除", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください。",
        code='''const user = { name: "Hana", age: 12 };
user.age = 13;
user.city = "東京";
delete user.name;
console.log(JSON.stringify(user));''',
        out='{"age":13,"city":"東京"}',
        wrong=[('{"name":"Hana","age":13,"city":"東京"}', "delete user.name で name のプロパティが削除されます。"), ('{"age":12,"city":"東京"}', "user.age = 13 で age は 12 から 13 に更新されます。")],
        why="age は更新、city は追加、name は削除されるから。",
        expl="オブジェクトは、代入でプロパティの更新・追加ができ、delete で削除できます。JSON.stringify は、キーも文字列は \" \" で囲んだ JSON という文字列にします。",
        concepts=["プロパティの追加・更新・削除", "JSON.stringify"], diff=2,
        hint="1行ずつ、user の中身がどう変わるか書き出しましょう。",
        ok="正解！プロパティの変化を追えました。",
        ng="惜しい！更新・追加・削除をそれぞれ確認しましょう。",
    ),
    mc(
        title="変数に入れたキー名で取り出す", lang="javascript",
        prompt="変数 key に \"age\" が入っています。オブジェクト user の age の値を、変数 key を使って取り出す正しい書き方はどれですか？",
        code='''const user = { name: "Hana", age: 12 };
const key = "age";''',
        fmt="code",
        choices=[
            ("user.key", "user.key は、key という名前のプロパティを探すので undefined になります。変数の中身は使われません。"),
            ("user[\"key\"]", "user[\"key\"] も、key という名前のプロパティを探します。変数ではなく文字列 \"key\" だからです。"),
            ("user[key]", ""),
        ],
        correct=2,
        why="角括弧の中に変数を書くと、その変数の値がキー名として使われるから。",
        expl="ドット記法の後ろは、そのままプロパティの名前です。変数の値をキー名にしたいときは、角括弧記法 user[key] を使います。Object.keys と組み合わせたくり返しでよく使います。",
        concepts=["角括弧記法", "ドット記法"], diff=2,
        hint="変数の値をキー名にするには、変数を [ ] の中に入れます。",
        ok="正解！変数をキー名に使うときは角括弧記法です。",
        ng="惜しい！ドット記法は、そのままの名前を探します。",
    ),
    fill(
        title="ネストしたプロパティ", lang="javascript",
        prompt="book の著者の名前（Taro）を表示します。【空欄1】に入れる式を答えてください。",
        code='''const book = { title: "JS入門", author: { name: "Taro" } };
console.log(book.__1__);''',
        blanks=[(["author.name", 'author["name"]'], True)],
        out="Taro",
        wrong=[("b1", "name", "book の直下には name というプロパティはありません。author の中にあるので、book.author.name と、ドットでつなぎます。")],
        why="ネストしたプロパティは、ドットをつなげて奥まで読むから。",
        expl="book.author で author のオブジェクトを取り出し、さらに .name でその中の name を読みます。book.name だと、book 直下に name はないので undefined です。",
        concepts=["ネスト"], diff=2,
        hint="author の中の name を、ドットでつないで読みます。",
        ok="正解！ドットをつなげて奥まで読みます。",
        ng="惜しい！book の直下ではなく、author の中にあります。",
    ),
    bugfix(
        title="undefined の中身を読むエラー", lang="javascript",
        prompt="user の住所の city を表示するはずが、TypeError になります。原因はどれですか？",
        code='''const user = { name: "Hana" };
console.log(user.address.city);''',
        fixed='''const user = { name: "Hana", address: { city: "東京" } };
console.log(user.address.city);''', out="東京", err="TypeError",
        choices=[
            ("city が JavaScript の予約語だから", "city は、プロパティ名として自由に使える普通の名前で、予約語ではありません。"),
            ("user.address が undefined なので、その中の city を読めないから", ""),
            ("console.log の括弧の書き方が間違っているから", "console.log の書き方は正しいです。エラーの原因は、読もうとしているプロパティの側にあります。"),
        ],
        correct=1, fmt="text",
        why="user に address というプロパティがなく undefined になり、その中身を読もうとして TypeError になるから。",
        expl="user.address は undefined です。undefined に対して .city と読もうとすると、読む対象がないため TypeError（Cannot read properties of undefined）になります。address を持たせるか、読む前に存在を確認します。",
        concepts=["undefined", "TypeError", "ネスト"], diff=3,
        hint="user に address プロパティはありますか？",
        ok="正解！undefined の中身は読めません。",
        ng="惜しい！user.address の値は何か考えてみましょう。",
    ),
    pred(
        title="Object.keys でくり返す", lang="javascript",
        prompt="次のコードを実行したとき、コンソールに表示される内容を入力してください。",
        code='''const scores = { math: 80, english: 70 };
let total = 0;
for (const key of Object.keys(scores)) {
  total += scores[key];
}
console.log(total);''',
        out="150",
        wrong=[("80", "くり返しは、キーの数（2回）だけ行われ、math と english の両方が足されます。"), ("math70", "total は数値で、値を足していきます。キーの文字は足されません。")],
        why="math と english の2つの値 80 と 70 が足されて 150 になるから。",
        expl="Object.keys(scores) は [\"math\", \"english\"] です。key が math のとき scores[key] は 80、english のとき 70 で、total に足されて 150 になります。",
        concepts=["Object.keys", "for...of", "角括弧記法"], diff=2,
        hint="key が各回で何になるか、書き出してみましょう。",
        ok="正解！キーと値を取り出して足せました。",
        ng="惜しい！くり返しごとの key と scores[key] を追いましょう。",
    ),
    pred(
        title="オブジェクトの配列", lang="javascript",
        prompt="次のコードを実行したとき、コンソールにはどう表示されますか？",
        code='''const users = [
  { name: "A", age: 20 },
  { name: "B", age: 17 },
];
console.log(users[1].name);
console.log(users.length);
console.log(users[0].age + users[1].age);''',
        choices=[
            ("A\n2\n37", "users[1] は添字 1、つまり2番目のオブジェクトで、name は \"B\" です。"),
            ("B\n2\n37", ""),
            ("B\n4\n3720", "length は配列の要素数（オブジェクトの数）なので 2 です。age は数値同士の足し算で 37 です。"),
        ],
        correct=1,
        why="users[1] は2番目の B で、要素数は 2、年齢の合計は 20 + 17 = 37 だから。",
        expl="オブジェクトの配列では、添字で何番目かを選び、ドットでプロパティを読みます。length は配列の要素数なので、プロパティの数は数えません。",
        concepts=["オブジェクトの配列", "length"], diff=2,
        hint="users[1] は、添字 0 から数えて何番目の要素でしょう？",
        ok="正解！添字とドットを組み合わせて読めました。",
        ng="惜しい！添字は 0 から始まります。",
    ),
    mc(
        title="プロパティの存在確認", lang="javascript",
        prompt="オブジェクト user に、age というプロパティがあるかどうかを調べる式はどれですか？",
        fmt="code",
        choices=[
            ('user.includes("age")', "includes は配列と文字列のメソッドです。オブジェクトにはないので、TypeError になります。"),
            ('"age" in user', ""),
            ("user.age()", "user.age() は、age の値を「関数」として呼び出そうとします。存在確認ではなく、値が関数でなければ TypeError になります。"),
        ],
        correct=1,
        why="in 演算子は、プロパティの存在を true / false で返すから。",
        expl="\"age\" in user は、user に age というプロパティがあれば true を返します。user.age !== undefined と書いて調べる方法もあります。",
        concepts=["in演算子"], diff=2,
        hint="「〜の中に」を意味する英単語を使う演算子です。",
        ok="正解！in 演算子で存在確認できます。",
        ng="惜しい！オブジェクトには includes がありません。",
    ),
    bugfix(
        title="数え方のミス", lang="javascript",
        prompt="文字の出現回数を数えるつもりが、結果が {\"a\":1,\"b\":0,\"c\":0} になります（正しくは {\"a\":2,\"b\":1,\"c\":1}）。4行目を正しく書き直して入力してください（4行目の内容だけを入力）。",
        code='''const counts = {};
for (const ch of ["a", "b", "c", "a"]) {
  if (counts[ch] === undefined) {
    counts[ch] = 0;
  } else {
    counts[ch] += 1;
  }
}
console.log(JSON.stringify(counts));''',
        fixed='''const counts = {};
for (const ch of ["a", "b", "c", "a"]) {
  if (counts[ch] === undefined) {
    counts[ch] = 1;
  } else {
    counts[ch] += 1;
  }
}
console.log(JSON.stringify(counts));''', out='{"a":2,"b":1,"c":1}', buggy_out='{"a":1,"b":0,"c":0}',
        target_line=4, accepted=["counts[ch] = 1;", "counts[ch]=1;", "counts[ch] = 1"],
        wrong=[("counts[ch] = 0;", "元のコードのままです。初めて出てきた文字は、その時点で1回出ているので、初期値は 1 です。")],
        why="初めて出てきた文字は、その時点で1回出現しているので、値を 1 にするから。",
        expl="if の側は「その文字が初めて出てきた」ときに実行されます。0 を入れると、初めの1回が数えられません。1 を入れ、2回目以降は += 1 で増やします。",
        concepts=["オブジェクト", "カウント", "論理エラー"], diff=3,
        hint="初めてその文字が出た時点で、出現回数はいくつですか？",
        ok="正解！初回を 1 として数えました。",
        ng="惜しい！「初めて出てきた」とき、すでに1回出ています。",
    ),
    write_js(
        title="買い物かごの合計金額", lang="javascript",
        prompt="配列 cart に、商品のオブジェクト（name・price・count）が入っています。価格 × 個数 の合計金額を console.log で表示するコードを書いてください。くり返し（for / while）を使うこと。",
        starter="// cart はあらかじめ用意されています\n",
        ref='''let total = 0;
for (const item of cart) {
  total += item.price * item.count;
}
console.log(total);''',
        alts=['''let total = 0;
for (let i = 0; i < cart.length; i++) {
  total = total + cart[i].price * cart[i].count;
}
console.log(total);'''],
        bads=[
            ('''let total = 0;
for (const item of cart) {
  total += item.price;
}
console.log(total);''', "個数（count）を掛けていません。りんごが2個なら、価格を2回足す必要があります。"),
            ('''let total = 0;
for (const item of cart) {
  total += item.price * item.count;
}''', "最後に console.log で合計を表示していません。"),
        ],
        req_any=[(r"\bfor\b", "for を使ってください"), (r"\bwhile\b", "while を使ってください")],
        tests=[
            t_js_out("320\n", setup='const cart = [{ name: "りんご", price: 120, count: 2 }, { name: "みかん", price: 80, count: 1 }];'),
            t_js_out("0\n", setup="const cart = [];", visible=False),
            t_js_out("500\n", setup='const cart = [{ name: "本", price: 500, count: 1 }];', visible=False),
            t_js_out("1000\n", setup='const cart = [{ name: "A", price: 100, count: 3 }, { name: "B", price: 50, count: 2 }, { name: "C", price: 200, count: 3 }];', visible=False),
        ],
        why="商品ごとに 価格 × 個数 を計算して、合計用の変数に足していくから。",
        expl="cart の要素はオブジェクトなので、item.price と item.count で値を取り出せます。空の cart のときは、くり返しが1回も行われず、合計は 0 のままです。",
        concepts=["オブジェクトの配列", "for...of", "累積"], diff=3,
        hint="合計用の変数を 0 で用意し、各商品の price * count を足します。",
        ok="正解！オブジェクトの配列を集計できました。",
        ng="惜しい！個数を掛けているか、空の cart でも動くかを確認しましょう。",
    ),
]
