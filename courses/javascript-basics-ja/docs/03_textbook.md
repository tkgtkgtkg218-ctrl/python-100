# 各ステージの教科書本文


---

## ステージ1: 変数とデータ型

### 導入：この知識が何に役立つのか

Webページの文章や構造は HTML、見た目は CSS で作ります。そこに「動き」を足すのが JavaScript です。ボタンを押したら表示が変わる、入力内容をチェックする、といったことができます。まずはコードを書いて結果を確かめる基本の道具、console.log と変数から始めましょう。

### JavaScript と console.log（目安 3分）

JavaScript は、Webブラウザの中で動くプログラミング言語です。HTML がページの構造、CSS が見た目を担当し、JavaScript が動きや計算を担当します（HTML と CSS はプログラミング言語ではなく、それぞれマークアップ言語・スタイルシート言語と呼びます）。

コードを動かす場所は2つあります。1つは HTML の中の <script> タグ、もう1つはブラウザの開発者ツール（多くのブラウザで F12 キー）にある「コンソール」です。このコースの問題では、書いたコードが自動で実行されます。

console.log(値) と書くと、値が開発者ツールのコンソールに表示されます。ページの画面には表示されません。結果を確かめるときの一番基本の道具です。複数の値を , で区切ると、間に空白を入れて1行に表示されます。

// から行末まではコメントで、実行されません。文の終わりには ; （セミコロン）を付けるのが一般的です。JavaScript は大文字と小文字を区別します（console.log は正しく、Console.log はエラーです）。

**用語解説**
- **コンソール**: 開発者ツールの中にある、メッセージやエラーを確認する画面。
- **文**: 実行の1つのまとまり。ふつう ; で終える。
- **コメント**: // で始まる、人間向けのメモ。実行されない。

**コード例（S01-E1）: いちばん短いコード**

```javascript
console.log("Hello");
console.log(10);
console.log("a", "b");
```

実行結果:

```text
Hello
10
a b
```

コードの解説:
- 1行目: 文字列 Hello を表示します（引用符は表示されません）。
- 2行目: 数値は引用符なしで書けます。
- 3行目: カンマで区切ると、間に空白を入れて1行に表示されます。

**コード例（S01-E2）: HTMLの中に書く（script タグ）**

```html
<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>はじめて</title></head>
<body>
  <p>画面にはこの文章だけが表示されます</p>
  <script>
    console.log("コンソールに表示されます");
  </script>
</body>
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 6〜8行目: <script> タグの中に JavaScript を書きます。
- console.log の結果は画面ではなく、開発者ツールのコンソールに出ます。

**コード例（S01-E3）: コメント**

```javascript
// あいさつを表示する
console.log("Hi"); // 行の途中からでもOK
// console.log("Bye");
```

実行結果:

```text
Hi
```

コードの解説:
- // 以降は実行されません。3行目のようにコードを一時的に無効にするのにも使えます。

### 変数とデータ型（目安 3分）

変数は、値に付ける名前です。let 名前 = 値; で宣言して値を入れます。あとから値を変えたいときは、let の変数に再び = で代入します。値を変えない変数は const で宣言します。const の変数に再代入するとエラー（TypeError）になります。

変数名には英字・数字・_ ・$ が使えますが、数字で始められません。大文字と小文字は区別されます。単語をつなぐときは userName のように、2語目の頭を大文字にする書き方（キャメルケース）が一般的です。

値には種類（データ型）があります。数値は number、文字列は string（"" か '' か `` で囲む）、真偽値は boolean（true / false）です。値がまだ入っていない変数は undefined、「意図的に空」を表す値は null です。

typeof 値 で型を調べられます。"42" のように引用符で囲むと数値ではなく文字列です。

**用語解説**
- **変数**: 値に付けた名前。
- **宣言**: let や const で変数を作ること。
- **データ型**: 値の種類。number、string、boolean など。
- **undefined**: 値がまだ入っていないことを表す値。

**コード例（S01-E4）: let と const**

```javascript
let score = 50;
score = 80;
const name = "Hana";
console.log(score);
console.log(name);
```

実行結果:

```text
80
Hana
```

コードの解説:
- 2行目: let の変数には、あとから値を入れ直せます（上書き）。
- 3行目: const の変数は、あとから変更できません。

**コード例（S01-E5）: データ型を調べる**

```javascript
console.log(typeof 42);
console.log(typeof "42");
console.log(typeof true);
let x;
console.log(x);
console.log(typeof x);
console.log(typeof null);
```

実行結果:

```text
number
string
boolean
undefined
undefined
object
```

コードの解説:
- 2行目: 引用符で囲んだ "42" は文字列です。
- 4〜6行目: 値を入れていない変数は undefined です。
- 7行目: typeof null が "object" になるのは、JavaScript の歴史的な仕様です。null の型は覚えなくても構いません。

**コード例（S01-E6）: const に再代入するとエラー**

```javascript
const price = 100;
price = 200;
```

実行結果: `TypeError` が発生します（エラーになる例）

コードの解説:
- const の変数に再代入すると TypeError（Assignment to constant variable）になります。

### よくある間違い

- **const の変数を書き換える**

  ```
  const count = 0;
  count = 1;
  ```
  - 理由: const は再代入できず TypeError になります。書き換える変数は let で宣言します。
  - 直し方: let count = 0;

- **引用符を付け忘れる**

  ```
  let greeting = Hello;
  ```
  - 理由: 引用符がない Hello は変数名と見なされ、ReferenceError になります。
  - 直し方: let greeting = "Hello";

- **大文字・小文字の違い**

  ```
  let userName = "Hana";
  console.log(username);
  ```
  - 理由: userName と username は別の名前です。宣言されていない名前を使うと ReferenceError になります。
  - 直し方: console.log(userName);

- **同じ名前を二重に宣言する**

  ```
  let a = 1;
  let a = 2;
  ```
  - 理由: 同じスコープで let の同名宣言はできず、SyntaxError になります。2回目は代入だけにします。
  - 直し方: let a = 1;
a = 2;

### 理解度チェック
- [ ] JavaScript はブラウザで動くプログラミング言語（HTML・CSS とは役割が違う）
- [ ] console.log の出力はコンソールに出る
- [ ] let は再代入できる、const は再代入できない
- [ ] number / string / boolean / undefined / null
- [ ] typeof で型を調べられる
- [ ] 大文字と小文字は区別される

### 次の問題への導入

変数に値を入れられるようになりました。問題で、コードを読んで結果を予想したり、エラーの原因を探したりしてみましょう。


---

## ステージ2: 演算子

### 導入：この知識が何に役立つのか

変数に入れた値を、計算したり、つなげたり、比べたりするのが演算子です。次のステージの「条件分岐」は、ここで学ぶ比較演算子と論理演算子の結果を使って動きます。

### 計算・代入・文字列の連結（目安 3分）

算術演算子は + - * / % ** です。% は割った余り、** は累乗（べき乗）です。JavaScript の / は小数まで計算する割り算で、7 / 2 は 3.5 になります（整数の商を返す演算子はありません）。掛け算・割り算は足し算・引き算より先に計算され、( ) で順序を変えられます。

x += 5 は x = x + 5 の短い書き方です。-= *= /= も同様で、x++ は x に 1 を足す書き方です。

文字列同士を + でつなぐと、文字列の連結になります。文字列と数値を + でつなぐと、数値が文字列になって連結されます（"5" + 3 は "53"）。変数を文字列に埋め込むには、バッククォート ` で囲んだテンプレートリテラルの中に ${式} と書くのが読みやすい方法です。

**用語解説**
- **演算子**: + や * など、計算や比較を表す記号。
- **代入演算子**: = や += のように、変数に値を入れる演算子。
- **テンプレートリテラル**: バッククォート（`）で囲み、${ } で値を埋め込める文字列。

**コード例（S02-E1）: いろいろな計算**

```javascript
console.log(7 + 2);
console.log(7 / 2);
console.log(7 % 2);
console.log(2 ** 3);
console.log(2 + 3 * 4);
console.log((2 + 3) * 4);
```

実行結果:

```text
9
3.5
1
8
14
20
```

コードの解説:
- 2行目: / は小数も含めた割り算です。
- 3行目: % は余りです。
- 5〜6行目: 掛け算が先。( ) で順序を変えられます。

**コード例（S02-E2）: 代入演算子と文字列**

```javascript
let total = 10;
total += 5;
total++;
console.log(total);
const name = "Hana";
const age = 12;
console.log("名前: " + name);
console.log(`${name}さんは${age}歳です`);
console.log("5" + 3);
```

実行結果:

```text
16
名前: Hana
Hanaさんは12歳です
53
```

コードの解説:
- 2行目: total = total + 5 と同じ。3行目: ++ は 1 増やします。
- 8行目: テンプレートリテラルの ${ } の部分が変数の値に置き換わります。
- 9行目: 文字列と数値の + は連結になるので、結果は 8 ではなく "53" です。

### 比較・論理演算子と型変換（目安 3分）

比較演算子は結果が true か false になります。等しいかは === 、等しくないかは !== 、大小は < > <= >= です。= は代入なので、比較には使えません。

== も等しいかを調べますが、型が違うと自動で変換して比べるため、5 == "5" が true になるなど分かりにくい結果になります。=== は型も含めて比べるので、基本は === を使います。

論理演算子は && （かつ）、|| （または）、! （否定）です。a && b は両方 true のときだけ true、a || b はどちらか一方でも true なら true です。

- * / を使うと、文字列は数値に自動変換されます（"10" / 2 は 5）。数値にできない文字列だと NaN（Not a Number）になります。自分で変換するときは Number("10") を使います。

**用語解説**
- **===**: 型も含めて等しいかを調べる比較演算子（厳密等価）。
- **型変換**: 値のデータ型が、自動または Number() などで別の型に変わること。
- **NaN**: 数値として計算できなかったときの値（Not a Number）。typeof は number。

**コード例（S02-E3）: 比較と論理演算**

```javascript
console.log(5 === 5);
console.log(5 === "5");
console.log(5 == "5");
console.log(5 !== 3);
console.log(3 > 2 && 2 > 5);
console.log(3 > 2 || 2 > 5);
console.log(!true);
```

実行結果:

```text
true
false
true
true
false
true
false
```

コードの解説:
- 2行目: 数値の 5 と文字列の "5" は、=== では等しくありません。
- 3行目: == は型を変換して比べるので true になります（分かりにくいため使わないのが基本です）。

**コード例（S02-E4）: 型変換と NaN**

```javascript
console.log("10" / 2);
console.log("abc" * 2);
console.log(Number("10") + 5);
console.log("10" + 5);
console.log(typeof NaN);
```

実行結果:

```text
5
NaN
15
105
number
```

コードの解説:
- 1行目: / は文字列を数値に変換して計算します。
- 2行目: 数値にできない文字列との計算は NaN になります。
- 3〜4行目: Number() で数値にすると足し算になり、しないと連結になります。

### よくある間違い

- **= と === の取り違え**

  ```
  console.log(n = 5);
  ```
  - 理由: = は代入です。n に 5 を入れた結果（5）が表示されます。等しいかを調べるには ===。
  - 直し方: console.log(n === 5);

- **文字列と数値の足し算**

  ```
  console.log("3" + 4);
  ```
  - 理由: 文字列と数値を + でつなぐと、連結になり "34" になります。計算したいときは Number() で数値にします。
  - 直し方: console.log(Number("3") + 4);

- **テンプレートリテラルで引用符を使う**

  ```
  console.log("${name}さん");
  ```
  - 理由: " " の中では ${ } は展開されず、そのまま表示されます。バッククォート（`）で囲みます。
  - 直し方: console.log(`${name}さん`);

- **整数の割り算を期待する**

  ```
  console.log(7 / 2);  // 3 と思い込む
  ```
  - 理由: JavaScript の / は小数も計算し、3.5 になります。切り捨てたいときは Math.floor(7 / 2) を使います。
  - 直し方: console.log(Math.floor(7 / 2));

### 理解度チェック
- [ ] / は小数も計算する、% は余り、** は累乗
- [ ] += や ++ で変数を更新できる
- [ ] 文字列 + 数値 は連結になる
- [ ] 等しいかは ===（= は代入）
- [ ] && は かつ、|| は または、! は否定
- [ ] 数値にできない計算は NaN になる

### 次の問題への導入

比較や論理演算の結果は true / false になります。問題で、式の結果を正確に読み取る練習をしましょう。


---

## ステージ3: 条件分岐

### 導入：この知識が何に役立つのか

プログラムは、条件によって動きを変えられます。「80点以上なら合格」「入力が空なら警告を出す」のような判断を、if 文で書きます。Webページでも、フォームのチェックや表示の切り替えで毎日のように使います。

### if / else if / else（目安 3分）

if (条件) { ... } と書くと、条件が true のときだけ { } の中が実行されます。条件が false のときの処理は else { ... } に書きます。

3つ以上に分けたいときは else if (条件) { ... } を続けます。上から順に調べ、最初に条件が成り立ったブロックだけが実行され、残りは調べません。そのため、厳しい条件（例: 90点以上）から順に書きます。

条件には、ステージ2の比較演算子・論理演算子を使います。「60点以上」は score >= 60、境界の 60 点を含むかどうかは >= と > で変わります。{ } の中の行は、見やすくするために字下げ（インデント）しますが、JavaScript では字下げは動作に影響しません。

**用語解説**
- **条件分岐**: 条件によって、実行する処理を切り替えること。
- **ブロック**: { } で囲んだ、ひとまとまりの処理。
- **境界値**: ちょうど切り替わる値（60点以上なら 60 など）。

**コード例（S03-E1）: if と else**

```javascript
const score = 55;
if (score >= 60) {
  console.log("合格");
} else {
  console.log("不合格");
}
console.log("終わり");
```

実行結果:

```text
不合格
終わり
```

コードの解説:
- 2行目: score >= 60 が false なので、else 側が実行されます。
- 7行目: if 文の外にあるので、常に実行されます。

**コード例（S03-E2）: else if**

```javascript
const score = 85;
if (score >= 90) {
  console.log("A");
} else if (score >= 80) {
  console.log("B");
} else if (score >= 70) {
  console.log("C");
} else {
  console.log("D");
}
```

実行結果:

```text
B
```

コードの解説:
- 上から順に調べ、score >= 80 が最初に true になるので B を表示して終わります。score >= 70 も true ですが、調べられません。

### truthy / falsy・三項演算子・switch（目安 3分）

if の条件には、true / false 以外の値も書けます。その場合、値は真偽に変換されます。偽（falsy）として扱われるのは、false、0、""（空文字列）、null、undefined、NaN の6つだけで、それ以外は真（truthy）です。"0" や "false" のように、中身が空でない文字列は truthy です。

a && b、a || b は、true / false ではなく、どちらかの値そのものを返します。a || b は a が truthy なら a、そうでなければ b を返します（「a がなければ b」の意味で、初期値を決めるときに使います）。a && b は a が falsy なら a、そうでなければ b を返します。

条件 ? 値1 : 値2 は三項演算子で、条件が truthy なら値1、そうでなければ値2になります。短い if / else を1行で書きたいときに使います。

switch (式) { case 値: ... break; default: ... } は、1つの値によって分岐します。case の最後に break を書かないと、次の case の処理も続けて実行されます。

**用語解説**
- **truthy / falsy**: 条件に使ったとき、真として扱われる値 / 偽として扱われる値。
- **三項演算子**: 条件 ? A : B の形で、条件によって値を選ぶ演算子。
- **break**: switch や繰り返しから抜ける文。

**コード例（S03-E3）: falsy な値と || の動き**

```javascript
if (0) { console.log("a"); } else { console.log("b"); }
if ("") { console.log("c"); } else { console.log("d"); }
if ("0") { console.log("e"); } else { console.log("f"); }
console.log(0 || "初期値");
console.log("あり" && "続き");
```

実行結果:

```text
b
d
e
初期値
続き
```

コードの解説:
- 1行目: 0 は falsy なので else 側。
- 3行目: "0" は空でない文字列なので truthy です。
- 4行目: 0 は falsy なので、右の "初期値" が返ります。

**コード例（S03-E4）: 三項演算子と switch**

```javascript
const age = 20;
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
}
```

実行結果:

```text
成人
two
```

コードの解説:
- 2行目: 条件が true なので "成人" が選ばれます。
- 8〜9行目: n が 2 なので two を表示し、break で switch を抜けます。

### よくある間違い

- **if の条件で = を使う**

  ```
  if (n = 5) { ... }
  ```
  - 理由: = は代入です。n に 5 を入れ、その結果（5、truthy）で条件が常に真になります。エラーにならないので気づきにくいミスです。
  - 直し方: if (n === 5) { ... }

- **else if の順序**

  ```
  if (score >= 60) {...} else if (score >= 80) {...}
  ```
  - 理由: 上から順に調べるので、80点以上でも最初の条件が先に成り立ちます。厳しい条件から書きます。
  - 直し方: 先に score >= 80 を調べる

- **switch の break 忘れ**

  ```
  case 1:
    console.log("one");
  case 2:
    console.log("two");
  ```
  - 理由: break がないと、case 1 のあとも続けて case 2 の処理が実行されます。
  - 直し方: 各 case の最後に break; を書く

- **"0" は falsy だと思う**

  ```
  if ("0") { ... }
  ```
  - 理由: 空でない文字列は truthy です。falsy なのは数値の 0 です。
  - 直し方: 数値にしたいなら Number("0") を使う

### 理解度チェック
- [ ] if / else if / else は上から順に調べ、最初に成り立ったものだけ実行される
- [ ] 厳しい条件から書く。境界値は >= と > で変わる
- [ ] falsy は false・0・""・null・undefined・NaN
- [ ] a || b は「a がなければ b」
- [ ] 条件 ? A : B（三項演算子）
- [ ] switch は case の最後に break

### 次の問題への導入

条件分岐は、これから学ぶ繰り返しや関数と組み合わせて使います。まず問題で、条件の順序や境界値を正確に読む練習をしましょう。


---

## ステージ4: 繰り返し

### 導入：この知識が何に役立つのか

同じ処理を何十回、何百回とくり返すのは、コンピューターの得意技です。ページの中の複数の要素を順番に処理したり、リストを1つずつ画面に出したりするときにも使います。

### for 文と while 文（目安 3分）

for (初期化; 条件; 更新) { ... } は、決まった回数のくり返しに使います。例: for (let i = 0; i < 3; i++) は、i を 0 から始め、i < 3 の間、くり返すたびに i++ で 1 増やします。つまり i は 0, 1, 2 になり、3 回くり返します。i < 3 の 3 自体は含まれません。

while (条件) { ... } は、条件が true の間くり返します。回数が決まっていないときや、条件で終わりを決めたいときに使います。ループの中で、条件に使う変数を変化させないと、条件がずっと true のままになり、終わらなくなります（無限ループ）。

合計を求めるときは、ループの前に let total = 0; と用意し、ループの中で total += i; のように足していきます。

**用語解説**
- **ループ**: 同じ処理をくり返す仕組み。
- **無限ループ**: 終わる条件が成り立たず、いつまでも終わらないループ。
- **累積**: ループの中で値を足し込み、合計などを作ること。

**コード例（S04-E1）: for 文**

```javascript
for (let i = 0; i < 3; i++) {
  console.log(i);
}
let total = 0;
for (let i = 1; i <= 5; i++) {
  total += i;
}
console.log(total);
```

実行結果:

```text
0
1
2
15
```

コードの解説:
- 1行目: i は 0 → 1 → 2 と増え、3 になると条件が false になって終わります。
- 5行目: 1 から 5 まで含めるときは、i <= 5 と書きます。

**コード例（S04-E2）: while 文**

```javascript
let count = 3;
while (count > 0) {
  console.log(count);
  count--;
}
console.log("発射");
```

実行結果:

```text
3
2
1
発射
```

コードの解説:
- 4行目: count を減らさないと、条件がずっと true のままで無限ループになります。

### break・continue・入れ子のループ（目安 3分）

break は、その場でループ全体を終了します。continue は、その回の残りの処理を飛ばして、次の回へ進みます。

ループの中にさらにループを書くことができます（入れ子）。外側が 1 回進むたびに、内側のループは最初から最後まで回ります。文字を足し込んで図形を作る、表を作る、といった場面で使います。

**用語解説**
- **break**: ループ全体をその場で終了する。
- **continue**: その回の残りを飛ばして、次の回へ進む。
- **入れ子（ネスト）**: ループの中にループを書くこと。

**コード例（S04-E3）: continue と break**

```javascript
for (let i = 1; i <= 5; i++) {
  if (i === 3) {
    continue;
  }
  if (i === 5) {
    break;
  }
  console.log(i);
}
```

実行結果:

```text
1
2
4
```

コードの解説:
- i が 3 のとき: continue で console.log を飛ばし、次の回へ。
- i が 5 のとき: break でループを終了。5 は表示されません。

**コード例（S04-E4）: 入れ子のループ**

```javascript
for (let i = 1; i <= 3; i++) {
  let line = "";
  for (let j = 0; j < i; j++) {
    line += "*";
  }
  console.log(line);
}
```

実行結果:

```text
*
**
***
```

コードの解説:
- 外側の i が 1, 2, 3 と進むたびに、内側のループが i 回まわり、* を足します。
- line は外側のループの回ごとに空文字列に戻ります。

### よくある間違い

- **回数の数え間違い（i < 5）**

  ```
  for (let i = 1; i < 5; i++)  // 1〜5 のつもり
  ```
  - 理由: i < 5 は 5 を含みません（1〜4）。5 まで含めるには i <= 5 と書きます。
  - 直し方: for (let i = 1; i <= 5; i++)

- **while の更新忘れ**

  ```
  let n = 3;
  while (n > 0) {
    console.log(n);
  }
  ```
  - 理由: n が変わらないので条件がずっと true。ページが固まる無限ループになります。
  - 直し方: ループの中に n--; を書く

- **合計の初期化忘れ**

  ```
  let total;
  for (...) { total += i; }
  ```
  - 理由: total が undefined のまま足すと、結果は NaN になります。ループの前に 0 を入れます。
  - 直し方: let total = 0;

- **continue と break の取り違え**

  ```
  if (i === 3) { break; }  // 3 だけ飛ばしたい
  ```
  - 理由: break は 3 でループ全体が終わります。3 だけ飛ばしたいなら continue です。
  - 直し方: if (i === 3) { continue; }

### 理解度チェック
- [ ] for (初期化; 条件; 更新) の3つの役割
- [ ] i < 3 は 0・1・2 の3回（3 は含まれない）
- [ ] 合計は先に 0 を用意して += で足す
- [ ] while は条件が true の間くり返す。中で条件の変数を更新する
- [ ] break は終了、continue は次の回へ
- [ ] 入れ子では、外側が1回進むごとに内側が最初から回る

### 次の問題への導入

くり返しは、たくさんのデータに使うと本領を発揮します。まず問題で、回数や範囲を正確に追う練習をしましょう。


---

## ステージ5: 配列

### 導入：この知識が何に役立つのか

100 人分の点数を、100 個の変数に入れるのは大変です。配列を使うと、複数の値を1つの名前でまとめて扱えます。ステージ4の for と組み合わせると、データを順番に処理できます。Webページの中の「リスト」を扱うときにも欠かせません。

### 配列の基本（目安 3分）

配列は、値を [ ] の中に , で区切って並べて作ります。例: const fruits = ["りんご", "みかん", "ぶどう"];。要素は番号（添字）で取り出し、番号は 0 から始まります。最初の要素は fruits[0] です。

fruits.length は要素の数（ここでは 3）で、最後の要素は fruits[fruits.length - 1] です。存在しない番号（fruits[5] など）を読んでも、エラーにはならず undefined になります。

fruits[1] = "レモン"; で要素を置き換え、push(値) で末尾に追加、pop() で末尾から取り出して削除します。const で宣言した配列にも、push などで中身を変更できます。const が禁止するのは、変数そのものへの再代入（fruits = [] など）だけです。

**用語解説**
- **配列**: 複数の値を順番に並べてまとめたデータ。
- **要素**: 配列の中の1つ1つの値。
- **添字（インデックス）**: 要素の位置を表す番号。0 から始まる。

**コード例（S05-E1）: 取り出しと長さ**

```javascript
const fruits = ["りんご", "みかん", "ぶどう"];
console.log(fruits[0]);
console.log(fruits[fruits.length - 1]);
console.log(fruits.length);
console.log(fruits[5]);
```

実行結果:

```text
りんご
ぶどう
3
undefined
```

コードの解説:
- 2行目: 添字 0 は最初の要素。
- 3行目: 最後の要素の添字は length - 1。
- 5行目: 範囲外はエラーにならず undefined になります。

**コード例（S05-E2）: 置き換え・追加・削除**

```javascript
const nums = [10, 20, 30];
nums[1] = 99;
nums.push(40);
const last = nums.pop();
console.log(nums.join(","));
console.log(last);
console.log(nums.length);
```

実行結果:

```text
10,99,30
40
3
```

コードの解説:
- 4行目: pop() は末尾の要素を取り出して削除し、その値を返します。
- 5行目: join(",") は、要素を , でつないだ文字列にします。

### 配列を調べる・順に処理する（目安 3分）

includes(値) は、その値が含まれているかを true / false で返します。indexOf(値) は、最初に見つかった位置を返し、なければ -1 を返します。slice(開始, 終了) は一部を新しい配列として取り出し、終了の位置の要素は含まれません。

配列の要素を1つずつ処理するには、添字を使う for のほか、for (const x of 配列) { ... } が使えます。for...of は、要素が順に x に入ります。添字で回すときは、i < arr.length と書きます（i <= arr.length だと1つ多くなります）。

console.log に配列をそのまま渡すと、配列全体が表示されます（表示の形式は環境によって少し違います）。このコースの問題では、join で文字列にして表示します。

**用語解説**
- **for...of**: 配列などの要素を、1つずつ取り出して処理する繰り返し。
- **slice**: 配列の一部を、新しい配列として取り出すメソッド。終了の位置は含まれない。

**コード例（S05-E3）: includes・indexOf・slice**

```javascript
const colors = ["赤", "青", "緑", "黄"];
console.log(colors.includes("青"));
console.log(colors.indexOf("緑"));
console.log(colors.indexOf("白"));
console.log(colors.slice(1, 3).join("-"));
```

実行結果:

```text
true
2
-1
青-緑
```

コードの解説:
- 4行目: 見つからないと -1 です。
- 5行目: slice(1, 3) は添字 1 と 2 の2つだけ（3 は含まれません）。

**コード例（S05-E4）: for...of で合計**

```javascript
const scores = [70, 85, 90];
let total = 0;
for (const s of scores) {
  total += s;
}
console.log(total);
let count = 0;
for (let i = 0; i < scores.length; i++) {
  count++;
}
console.log(count);
```

実行結果:

```text
245
3
```

コードの解説:
- 3行目: scores の要素が1つずつ s に入ります。
- 8行目: 添字で回すときは i < scores.length と書きます。

### よくある間違い

- **1番目を [1] と思う**

  ```
  console.log(fruits[1]);  // 最初の要素のつもり
  ```
  - 理由: 添字は 0 から始まります。fruits[1] は2番目の要素です。
  - 直し方: console.log(fruits[0]);

- **push を [ ] で書く**

  ```
  arr.push[4];
  ```
  - 理由: push は関数なので ( ) で呼びます。[ ] だと何も追加されず、エラーにもなりません。
  - 直し方: arr.push(4);

- **i <= arr.length**

  ```
  for (let i = 0; i <= arr.length; i++)
  ```
  - 理由: 最後に arr[arr.length]（undefined）まで読んでしまい、合計が NaN になるなどのミスになります。
  - 直し方: for (let i = 0; i < arr.length; i++)

- **const の配列は変更できないと思う**

  ```
  const list = [1];
  list.push(2);  // エラーになると思い込む
  ```
  - 理由: const は再代入を禁止するだけで、配列の中身の変更はできます。
  - 直し方: list = [3]; のような再代入が TypeError になる

### 理解度チェック
- [ ] 添字は 0 から。最後は arr[arr.length - 1]
- [ ] 範囲外の添字は undefined（エラーにならない）
- [ ] push は末尾に追加、pop は末尾から削除
- [ ] includes・indexOf（見つからないと -1）・join・slice
- [ ] for...of で要素を順に取り出せる
- [ ] const の配列にも push できる

### 次の問題への導入

配列で、順番のあるデータを扱えるようになりました。問題で、添字と範囲の扱いを確かめましょう。


---

## ステージ6: オブジェクト

### 導入：この知識が何に役立つのか

配列は「順番」でデータを並べました。オブジェクトは「名前（キー）」でデータを並べます。「名前は Hana、年齢は 12」のように、1つのものについての複数の情報をまとめられます。Webページの要素の情報や、サーバーから届くデータなど、JavaScript のあらゆる場面で使われます。

### オブジェクトの基本（目安 3分）

オブジェクトは { } の中に キー: 値 を , で区切って書きます。例: const user = { name: "Hana", age: 12 };。値は user.name のようにドット記法で、または user["name"] のように角括弧記法で取り出します。存在しないキーを読むと undefined になります。

変数に入れたキー名で取り出したいときは、角括弧記法を使います。const key = "age"; user[key] は 12 ですが、user.key は「key という名前のプロパティ」を探すので undefined になります。

user.age = 13; で更新、user.city = "東京"; で追加、delete user.name; で削除です。"age" in user で、プロパティがあるかを true / false で調べられます。const のオブジェクトでも、プロパティの変更はできます。

JSON.stringify(オブジェクト) は、オブジェクトを JSON という文字列にします。console.log でオブジェクトの中身を確かめるときに便利です。

**用語解説**
- **オブジェクト**: キーと値のペア（プロパティ）をまとめたデータ。
- **プロパティ**: オブジェクトの中の、キーと値の1組。
- **JSON**: データを文字列で表す形式。JSON.stringify でオブジェクトを変換できる。

**コード例（S06-E1）: 読み出し**

```javascript
const user = { name: "Hana", age: 12 };
console.log(user.name);
console.log(user["age"]);
console.log(user.city);
const key = "age";
console.log(user[key]);
console.log(user.key);
console.log("age" in user);
```

実行結果:

```text
Hana
12
undefined
12
undefined
true
```

コードの解説:
- 4行目: 存在しないキーを読むと undefined です。
- 6行目: 変数のキー名で取り出すには角括弧記法を使います。
- 7行目: user.key は「key」という名前のプロパティを探すので undefined です。

**コード例（S06-E2）: 追加・更新・削除**

```javascript
const user = { name: "Hana", age: 12 };
user.age = 13;
user.city = "東京";
delete user.name;
console.log(JSON.stringify(user));
```

実行結果:

```text
{"age":13,"city":"東京"}
```

コードの解説:
- 2行目: 既にあるプロパティは更新されます。
- 3行目: ないプロパティは追加されます。
- 4行目: delete でプロパティが削除されます。

### ネスト・オブジェクトの配列・Object.keys（目安 3分）

オブジェクトの値には、別のオブジェクトや配列も入れられます（ネスト）。book.author.name のように、ドットをつなげて奥まで読みます。途中が undefined だと、その先を読んだときに TypeError（Cannot read properties of undefined）になります。

オブジェクトを要素にもつ配列は、ユーザー一覧や商品一覧によく使われます。users[1].name のように、添字とドットを組み合わせて読みます。

Object.keys(オブジェクト) は、キーの配列を返します。for (const key of Object.keys(obj)) と組み合わせると、すべてのプロパティを順に処理できます。値は obj[key] で取り出します。

**用語解説**
- **ネスト**: 入れ物の中に、さらに入れ物を入れること。
- **Object.keys**: オブジェクトのキーを、配列として返す。

**コード例（S06-E3）: ネストと配列**

```javascript
const book = { title: "JS入門", author: { name: "Taro", age: 30 } };
console.log(book.author.name);
const users = [{ name: "A", age: 20 }, { name: "B", age: 17 }];
console.log(users[1].name);
console.log(users.length);
console.log(users[0].age + users[1].age);
```

実行結果:

```text
Taro
B
2
37
```

コードの解説:
- 2行目: ドットをつなげて、奥のプロパティを読みます。
- 4行目: users[1] は2番目のオブジェクトです。

**コード例（S06-E4）: Object.keys でくり返す**

```javascript
const scores = { math: 80, english: 70 };
let total = 0;
for (const key of Object.keys(scores)) {
  console.log(key + ": " + scores[key]);
  total += scores[key];
}
console.log(total);
```

実行結果:

```text
math: 80
english: 70
150
```

コードの解説:
- 3行目: Object.keys(scores) は ["math", "english"] です。
- 4行目: scores[key] で、そのキーの値を取り出します。

### よくある間違い

- **変数のキー名を user.key と書く**

  ```
  const key = "age";
  console.log(user.key);
  ```
  - 理由: user.key は、key という名前のプロパティを探します。変数の値をキー名にしたいときは user[key]。
  - 直し方: console.log(user[key]);

- **存在しないプロパティの中身を読む**

  ```
  console.log(user.address.city);
  ```
  - 理由: user.address が undefined なので、その中の city を読もうとして TypeError になります。
  - 直し方: address を持たせる、または存在を確認してから読む

- **プロパティの確認に includes を使う**

  ```
  user.includes("age")
  ```
  - 理由: includes は配列・文字列のメソッドで、オブジェクトにはありません（TypeError）。in 演算子を使います。
  - 直し方: "age" in user

- **カウントの初期値**

  ```
  counts[ch] = 0;  // 初めて出てきた文字
  ```
  - 理由: 初めて出てきた時点で1回出ているので、初期値は 1 です。
  - 直し方: counts[ch] = 1;

### 理解度チェック
- [ ] { キー: 値 } で作り、ドット記法か角括弧記法で読む
- [ ] 変数のキー名は角括弧記法で取り出す
- [ ] 追加・更新は代入、削除は delete、存在確認は in
- [ ] 存在しないプロパティは undefined、その中身を読むと TypeError
- [ ] Object.keys と for...of で全プロパティを処理できる
- [ ] オブジェクトの配列は users[0].name のように読む

### 次の問題への導入

オブジェクトで、「名前付きのデータ」を扱えるようになりました。問題で、プロパティの読み出しや、ネストした構造の扱いを確かめましょう。


---

## ステージ7: 関数

### 導入：この知識が何に役立つのか

同じ処理を何度も書くのは大変で、間違いのもとです。処理に名前を付けて「部品」にしたものが関数です。ここまで使ってきた console.log や push も関数でした。ページのボタンを押したときの動き（ステージ9）は、関数を渡して書くので、この回の内容が土台になります。

### 関数を作って呼び出す（目安 3分）

function 関数名(引数) { ... } で関数を定義します。定義しただけでは実行されず、関数名(値) と書いて呼び出したときに実行されます。呼び出し時に渡す値を引数といい、関数の中では引数の名前で使えます。

return 値; は、結果を呼び出し元へ返して、関数を終了します。return がない関数の戻り値は undefined です。console.log は画面（コンソール）に表示するだけで、値は返しません。結果を別の計算に使うなら return を使います。

アロー関数 const add = (a, b) => a + b; は、関数を短く書く方法です。{ } で囲んだときは、結果を返すために return が必要です。引数にデフォルト値を決めたいときは、function power(base, exp = 2) のように = で書きます。

**用語解説**
- **関数**: 名前を付けた処理のまとまり。
- **引数**: 関数に渡す材料の値。
- **戻り値**: 関数が return で返す結果。
- **アロー関数**: => を使った、関数の短い書き方。

**コード例（S07-E1）: 引数と戻り値**

```javascript
function add(a, b) {
  return a + b;
}
console.log(add(3, 4));
console.log(add(3, 4) * 2);
function show(x) {
  console.log(x);
}
const r = show(5);
console.log(r);
```

実行結果:

```text
7
14
5
undefined
```

コードの解説:
- 5行目: 呼び出しは戻り値に置き換わって計算が進みます。
- 9〜10行目: show は何も返さないので、r は undefined です。

**コード例（S07-E2）: アロー関数とデフォルト引数**

```javascript
const double = (n) => n * 2;
console.log(double(4));
const add = (a, b) => {
  return a + b;
};
console.log(add(1, 2));
function power(base, exp = 2) {
  return base ** exp;
}
console.log(power(3));
console.log(power(2, 5));
```

実行結果:

```text
8
3
9
32
```

コードの解説:
- 1行目: { } がなければ、式の結果がそのまま戻り値になります。
- 3〜5行目: { } を使うときは return が必要です。
- 11行目: exp を省略すると、デフォルトの 2 が使われます。

### スコープとコールバック（目安 3分）

関数の中で宣言した変数は、その関数の中だけで使えます（ローカル変数）。同じ名前の外の変数とは別物で、外の値は変わりません。let / const は { } の中だけで有効な「ブロックスコープ」です。{ } の外から使うと ReferenceError になります。

関数は値として、別の関数に渡せます。渡された関数を、あとで呼び出してもらう仕組みをコールバックといいます。配列のメソッドの forEach（各要素に処理）、map（各要素を変換した新しい配列）、filter（条件に合う要素だけの新しい配列）は、コールバックを受け取ります。

ステージ9のイベント処理でも、「クリックされたらこの関数を呼んで」と、関数を渡します。このとき、関数名のあとに ( ) を付けない点に注意します。fn は関数そのもの、fn() は関数を呼び出した結果です。

**用語解説**
- **ローカル変数**: 関数やブロックの中だけで有効な変数。
- **コールバック**: あとで呼び出してもらうために、別の関数に渡す関数。
- **map / filter**: 配列の各要素を変換する / 条件に合う要素を選ぶメソッド。

**コード例（S07-E3）: スコープ**

```javascript
let x = 100;
function f() {
  let x = 10;
  return x + 1;
}
console.log(f());
console.log(x);
{
  let y = 1;
}
console.log(typeof y);
```

実行結果:

```text
11
100
undefined
```

コードの解説:
- 3行目: 関数の中の x は別の変数です。外の x は変わりません。
- 10行目: y は { } の中だけの変数なので、外では存在しません（typeof は undefined を返します）。

**コード例（S07-E4）: map・filter・forEach**

```javascript
const nums = [1, 2, 3, 4];
console.log(nums.map((n) => n * 2).join(","));
console.log(nums.filter((n) => n % 2 === 0).join(","));
nums.forEach((n) => {
  console.log("値: " + n);
});
```

実行結果:

```text
2,4,6,8
2,4
値: 1
値: 2
値: 3
値: 4
```

コードの解説:
- 2行目: map は、各要素を2倍にした新しい配列を返します。
- 3行目: filter は、関数が true を返した要素だけを集めます。
- 4行目: forEach は、各要素に対して関数を呼び出します（戻り値は使いません）。

### よくある間違い

- **定義しただけで呼び出さない**

  ```
  function greet() {
    console.log("hi");
  }
  ```
  - 理由: 定義だけでは何も起きません。greet() と呼び出します。
  - 直し方: greet();

- **return の代わりに console.log**

  ```
  function area(w, h) {
    console.log(w * h);
  }
  const x = area(3, 4) + 1;
  ```
  - 理由: area は何も返さない（undefined）ので、undefined + 1 は NaN になります。
  - 直し方: console.log を return に変える

- **アロー関数の { } で return を忘れる**

  ```
  const add = (a, b) => { a + b };
  ```
  - 理由: { } を使うと、return がないので undefined が返ります。
  - 直し方: const add = (a, b) => a + b;

- **return をループの中に書く**

  ```
  for (const n of nums) {
    s += n;
    return s;
  }
  ```
  - 理由: return でその場で関数が終了し、1回目で終わってしまいます。
  - 直し方: return s; をループの外に書く

### 理解度チェック
- [ ] 関数は定義だけでは実行されず、関数名() で呼び出す
- [ ] return は値を返して関数を終了する。なければ undefined
- [ ] console.log は表示するだけ。値は返さない
- [ ] アロー関数の { } では return が必要
- [ ] 関数の中の変数は外とは別物（ローカル変数）
- [ ] map・filter・forEach には関数を渡す（関数名のあとに ( ) は付けない）

### 次の問題への導入

関数が使えると、処理を部品として組み合わせられます。問題で、戻り値や return の働きを確かめましょう。


---

## ステージ8: DOM操作

### 導入：この知識が何に役立つのか

ここからが、JavaScript の本領です。ブラウザは、HTML を読み取ると、ページの内容を「要素の木」のようなデータ（DOM）に作り変えます。JavaScript は、この DOM を書き換えることで、ページの文字・見た目・構造を、あとから変えられます。この回では、「要素を取り出して、書き換える」基本の流れを学びます。

### DOM と要素の取得・書き換え（目安 3分）

DOM（Document Object Model）は、ブラウザが HTML をもとに作る、要素の木構造のデータです。JavaScript では document というオブジェクトを入り口にして、DOM の要素を読み書きします。DOM を書き換えても、HTML ファイルそのものは変わらず、いま表示しているページだけが変わります。

要素を取り出すには、CSS のセレクタを使います。document.querySelector("#title") は id が title の要素、document.querySelector(".note") は class が note の最初の1つです。該当するものすべては document.querySelectorAll(".note") で、配列に似た一覧が返ります（添字や for...of で扱えます）。見つからないと null になります。

要素の文字を変えるには textContent を使います。入力欄（input）の中身は value です。textContent に入れた文字列は、HTML ではなく、ただの文字として表示されます。HTML として解釈させる innerHTML は、ユーザーの入力を入れると、悪意のあるコードを実行される危険があるため、文字を入れたいときは textContent を使います。

<script> は、操作したい要素より後ろ（body の最後など）に書きます。ブラウザは HTML を上から順に読むので、要素がまだ作られていない位置のスクリプトからは、その要素を取得できません。

**用語解説**
- **DOM**: ブラウザが HTML から作る、要素の木構造のデータ。JavaScript から読み書きできる。
- **querySelector**: CSS のセレクタで、最初に見つかった要素を取り出すメソッド。
- **textContent**: 要素の中の文字列。書き換えると画面の文字が変わる。

**コード例（S08-E1）: 要素を取り出して書き換える**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 8行目: id が title の要素の文字を書き換えます。
- 9〜10行目: class が note の要素を、すべて取り出し、2つ目（添字 1）の文字を書き換えます。
- <script> は、要素より後ろに書かれているので、要素を取り出せます。

**コード例（S08-E2）: 入力欄の value**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- input の中身は、textContent ではなく value で読み書きします。

### class・style・要素の追加（目安 3分）

要素の class を操作するには classList を使います。classList.add("on") で追加、remove("on") で削除、toggle("on") で「あれば削除、なければ追加」、contains("on") で持っているかを調べます。見た目は CSS で class に書いておき、JavaScript では class を付け外しする方法が、保守しやすい基本の形です。

style プロパティで、直接スタイルを変えることもできます。CSS のプロパティ名のハイフンは取り除き、次の文字を大文字にします（background-color は el.style.backgroundColor）。属性は el.setAttribute("href", "b.html") や el.getAttribute("href") で扱います。

要素を新しく作って追加するには、document.createElement("li") で要素を作り、textContent などで中身を設定し、親要素.appendChild(要素) で追加します。要素を削除するには el.remove() です。配列のデータからリストを作るときに、for と組み合わせてよく使います。

**用語解説**
- **classList**: 要素の class を操作するための機能。add / remove / toggle / contains。
- **createElement**: 新しい要素を作るメソッド。作っただけでは画面に出ない。
- **appendChild**: 親要素の末尾に、子要素を追加するメソッド。

**コード例（S08-E3）: classList と style**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 10行目: class を付けると、CSS の .on のルールが適用されて赤くなります。
- 11行目: style で直接、文字の大きさを変えます（font-size → fontSize）。

**コード例（S08-E4）: 要素を作って追加する**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 10行目: li 要素を作ります（まだ画面には出ません）。
- 11行目: 中身の文字を設定します。
- 12行目: ul の末尾に追加すると、画面に表示されます。

### よくある間違い

- **セレクタの typo・# と . の取り違え**

  ```
  document.querySelector("#mgs").textContent = "OK";
  ```
  - 理由: 該当する要素がないと null が返り、null の textContent に代入しようとして TypeError になります。id は #、class は . です。
  - 直し方: document.querySelector("#msg")

- **style にハイフン付きの名前**

  ```
  box.style.background-color = "red";
  ```
  - 理由: ハイフンは引き算として読まれ、SyntaxError になります。backgroundColor と書きます。
  - 直し方: box.style.backgroundColor = "red";

- **input の値に textContent**

  ```
  input.textContent = "Hana";
  ```
  - 理由: input は中身を持たない要素なので、文字は表示されません。value を使います。
  - 直し方: input.value = "Hana";

- **ユーザーの入力を innerHTML に入れる**

  ```
  el.innerHTML = userInput;
  ```
  - 理由: 入力が HTML として解釈され、悪意のあるコードが実行される危険があります。
  - 直し方: el.textContent = userInput;

### 理解度チェック
- [ ] DOM は HTML から作られる要素の木。書き換えてもファイルは変わらない
- [ ] querySelector は最初の1つ、querySelectorAll は全部。見つからなければ null
- [ ] 文字は textContent、入力欄は value
- [ ] classList の add / remove / toggle / contains
- [ ] style は backgroundColor のようにキャメルケース
- [ ] createElement → 中身を設定 → appendChild

### 次の問題への導入

ページを書き換える方法が分かりました。問題では、実際の HTML と組み合わせたコードを読み、書いてみましょう。ボタンで動かす方法は、次のステージで学びます。


---

## ステージ9: イベント処理

### 導入：この知識が何に役立つのか

ボタンを押したとき、文字を入力したとき、フォームを送ったとき。ユーザーが何かしたときに動く処理を書くのが「イベント処理」です。前の回で書いた DOM の書き換えを、ユーザーの操作に結びつけると、動きのあるページになります。

### addEventListener と関数を渡すこと（目安 3分）

要素.addEventListener("イベント名", 関数) で、「そのイベントが起きたら、この関数を呼んでください」とブラウザに頼みます。クリックのイベント名は click です（onclick ではなく、on を付けません）。

関数には、関数名だけを書いて渡します。addEventListener("click", inc) と書くと、クリックされたときにブラウザが inc を呼び出します。inc() と ( ) を付けると、登録する時点で inc が実行され、その戻り値（undefined）が渡されてしまうため、クリックしても何も起きません。

関数は、イベントオブジェクト（慣習で e と書く）を受け取ります。e.target は、イベントが起きた要素です。入力欄の値は e.target.value で読めます。

querySelectorAll の結果（要素の一覧）には、addEventListener を直接呼べません。for...of などで、1つずつ取り出して付けます。

**用語解説**
- **イベント**: クリック、入力、送信など、ユーザーの操作やブラウザの出来事。
- **イベントリスナー**: イベントが起きたときに呼び出される関数。addEventListener で登録する。
- **e.target**: イベントが起きた要素。

**コード例（S09-E1）: クリックしたら数を増やす**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 10行目: "click" は、クリックのイベント名です。
- 10〜13行目: クリックのたびに、この関数が呼ばれ、count が1ずつ増えます。

**コード例（S09-E2）: 入力に反応する（input イベント）**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- input イベントは、入力欄の中身が変わるたびに起きます。
- e.target は入力欄の要素で、e.target.value が現在の入力内容です。

### いろいろなイベント・preventDefault・バブリング（目安 3分）

よく使うイベント: click（クリック）、input（入力のたび）、change（値が確定したとき）、submit（フォームの送信）、keydown（キーを押した）、DOMContentLoaded（HTML の読み込み完了）。

フォームの submit イベントは、そのままだとページを送信先へ移動（または再読み込み）します。それを止めて、JavaScript で処理したいときは、関数の中で e.preventDefault() を呼びます。

子要素で起きたイベントは、親要素へも伝わります（バブリング）。内側の要素のイベントリスナーが先、その外側の要素のものが後に呼ばれます。この性質を使って、親要素1つにリスナーを付け、e.target で「どの子がクリックされたか」を判断する方法をイベント委譲といいます。要素に data-名前="値" という属性を付けておくと、JavaScript では el.dataset.名前 で読めます。

**用語解説**
- **preventDefault**: イベントの標準の動作（フォーム送信によるページ移動など）を止めるメソッド。
- **バブリング**: 子要素で起きたイベントが、親要素へ順に伝わること。
- **イベント委譲**: 親要素にリスナーを付け、e.target で子要素を判断する書き方。

**コード例（S09-E3）: フォームと preventDefault**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 11行目: submit イベントで、ページ移動を止めて（preventDefault）、自分の処理を行います。

**コード例（S09-E4）: イベント委譲**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- ul に1つだけリスナーを付けています。li をクリックすると、バブリングで ul に伝わります。
- e.target は実際にクリックされた li で、data-name の値は dataset.name で読めます。

### よくある間違い

- **関数を渡さず、呼び出してしまう**

  ```
  btn.addEventListener("click", inc());
  ```
  - 理由: inc() は登録の時点で実行され、その戻り値（undefined）が渡されます。クリックしても何も起きません。
  - 直し方: btn.addEventListener("click", inc);

- **イベント名に on を付ける**

  ```
  btn.addEventListener("onclick", fn);
  ```
  - 理由: イベント名は click です。onclick というイベントはなく、何も起きません。
  - 直し方: btn.addEventListener("click", fn);

- **一覧にまとめて addEventListener**

  ```
  document.querySelectorAll(".btn").addEventListener("click", fn);
  ```
  - 理由: querySelectorAll の結果は要素の一覧で、addEventListener を持っていません（TypeError）。for...of で1つずつ付けます。
  - 直し方: for (const b of buttons) { b.addEventListener("click", fn); }

- **preventDefault を忘れる**

  ```
  form.addEventListener("submit", (e) => { ... });
  ```
  - 理由: 標準の動作（ページ移動・再読み込み）が起き、画面の書き換えが消えてしまいます。
  - 直し方: 関数の最初に e.preventDefault();

### 理解度チェック
- [ ] addEventListener("イベント名", 関数) で結びつける
- [ ] 関数は渡す（fn）。fn() は呼び出し
- [ ] イベント名は click・input・submit など（on を付けない）
- [ ] e.target は起きた要素、入力欄の値は e.target.value
- [ ] フォーム送信は preventDefault で止める
- [ ] イベントは子から親へ伝わる（バブリング）

### 次の問題への導入

「ユーザーの操作で動く」ページが書けるようになりました。問題で、イベント処理のコードを読み、書いてみましょう。


---

## ステージ10: 簡単なWebアプリ制作

### 導入：この知識が何に役立つのか

最後のステージです。新しい文法はほとんどありません。変数・配列・関数・DOM・イベントを組み合わせて、ページの中で動く小さなアプリを作ります。コツは、いきなり全部を書かず、「何を覚えておくか（データ）」「画面にどう見せるか（表示）」「どの操作で何が起きるか（イベント）」を分けて考えることです。

### アプリづくりの考え方（目安 3分）

アプリは、「データを更新する → 画面を書き換える」の繰り返しです。例えば、ToDo アプリでは、「項目の一覧」がデータで、画面の li の並びが表示です。データだけを書き換えても、画面は自動では変わりません。データを変えたあと、表示を書き換える処理（render など）を呼ぶ必要があります。

入力欄の value は、数字を入れていても文字列です。そのまま + で足すと連結になるので、計算に使うときは Number(文字列) で数値にします。

ユーザーは、想定外の入力をします。空の入力や、スペースだけの入力は、追加しない、のようにチェックしましょう。文字列の前後の空白は trim() で取り除けます。

作る順番は、(1) 表示だけ作る、(2) 1つのボタンの動きだけ作る、(3) 想定外の入力に対応する、と、少しずつ確かめながら進めるのが安全です。

**用語解説**
- **状態（データ）**: アプリが覚えておく値。数や配列など。
- **render（描画）**: データをもとに、画面（DOM）を書き換える処理。
- **trim**: 文字列の前後の空白を取り除くメソッド。

**コード例（S10-E1）: 入力値は文字列**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 11〜12行目: value は文字列なので、Number() で数値にしてから足します。
- Number() を付けないと、"1" + "2" が "12" になります。

**コード例（S10-E2）: ToDo の追加（空のチェックつき）**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 12行目: trim() で前後の空白を取り除きます。
- 13〜15行目: 空なら何も追加せず、return でこの関数を終わります。
- 20行目: 追加したあと、入力欄を空に戻します。

### いろいろなアプリの作り方（目安 3分）

タブの切り替えは、「どのパネルを見せるか」を切り替える処理です。各ボタンに data-target="p1" のように、対応するパネルの id を持たせておくと、クリックされたボタンの dataset.target で、見せるパネルが分かります。パネルは hidden 属性（el.hidden = true / false）で、表示と非表示を切り替えられます。

一覧の項目を、クリックで「完了」にするには、classList.toggle("done") を使います。残りの件数などは、クリックのたびに数え直して表示します。項目ごとにリスナーを付けるほか、親要素にまとめて付けて e.target で判断する（イベント委譲）書き方もあります。

削除ボタンつきのリストでは、li の中に button を作り、そのクリックで li.remove() を呼びます。追加と削除のたびに、件数の表示も更新します。

ここから先は、入力内容をブラウザに保存する localStorage、サーバーと通信する fetch、コードを複数ファイルに分けるモジュール、フレームワークなどへ進めます。このコースの範囲は、ここまでです。

**用語解説**
- **dataset**: data-名前="値" という属性を、JavaScript から el.dataset.名前 で読み書きする機能。
- **remove**: 要素を DOM から取り除くメソッド。

**コード例（S10-E3）: タブの切り替え**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 12行目: すべてのタブに、同じ処理のリスナーを付けています。
- 14〜15行目: クリックされたタブの data-target と同じ id のパネルだけを、表示します。

**コード例（S10-E4）: クリックで完了にして、残りの件数を表示**

```html
<!doctype html>
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
</html>
```

表示結果: アプリ内のプレビューで確認できます（実際に操作できます）。

コードの解説:
- 10〜18行目: done の class がない li を数えて、残りの件数を表示します。
- 21〜22行目: クリックで done を付け外しし、そのたびに件数を更新します。

### よくある間違い

- **入力値をそのまま足す**

  ```
  const a = document.querySelector("#a").value;
  const b = document.querySelector("#b").value;
  result.textContent = a + b;
  ```
  - 理由: value は文字列なので、"1" + "2" は "12" になります。Number() で数値にします。
  - 直し方: Number(a) + Number(b)

- **データだけ更新して画面を更新しない**

  ```
  todos.push(text);  // render() を呼ばない
  ```
  - 理由: 配列を変えても、画面の DOM は自動では変わりません。
  - 直し方: データを変えたあとに render() を呼ぶ

- **空の入力を追加してしまう**

  ```
  const text = input.value;
  const li = document.createElement("li");
  ```
  - 理由: 空やスペースだけの入力でも、空の項目が追加されます。trim() で取り除き、空なら return します。
  - 直し方: if (input.value.trim() === "") { return; }

- **削除のあとに件数を更新しない**

  ```
  del.addEventListener("click", () => { li.remove(); });
  ```
  - 理由: 項目は消えても、「N件」の表示は古いままです。
  - 直し方: li.remove(); updateTotal();

### 理解度チェック
- [ ] データを更新する → 画面を書き換える（render）
- [ ] input の value は文字列。計算には Number()
- [ ] 空の入力は trim() で確認して無視する
- [ ] 追加・削除のあとは、件数などの表示も更新する
- [ ] 表示の切り替えは hidden や class の付け外し
- [ ] 小さく作って、1つずつ確かめる

### 次の問題への導入

JavaScript の最後のステージです。読む問題と、自分でアプリを書く問題があります。1つの機能ずつ、確かめながら作っていきましょう。
