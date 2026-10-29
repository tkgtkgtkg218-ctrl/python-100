# 10. 追加コース（JavaScript / HTML・CSS）の設計方針

Python コース（全10ステージ・全100問）と同じ「短い教科書 → すぐ問題 → 解説」の学習体験で、**JavaScript** と **HTML/CSS** の2コースを追加しました。各コースは 10ステージ × 10問 = **100問**、教科書は各ステージ2セクション。データは `courses/javascript-basics-ja/`・`courses/htmlcss-basics-ja/`、各コースの一覧・教科書・問題集（Markdown）は、それぞれの `docs/` にあります。

## 10.1 置いた仮定（確認質問で止まらず、仮定して進めたこと）

1. 問題数は Python コースに合わせ、各コース100問（10ステージ × 10問）、クリア条件も同じ（1回目の回答で7問以上正解）。
2. JavaScript は「ブラウザの上で動くプログラム」を目的とし、Node.js 固有の機能・外部ライブラリは使わない。ES2015 以降（let / const・アロー関数・テンプレートリテラル・for...of）を使い、`var` は、教えない（let / const を基本とする）。
3. HTML/CSS は、JavaScript を使わない。CSS は、レイアウトに Flexbox まで（Grid・アニメーション・CSS 変数は扱わない）。
4. 動作確認は **Google Chrome（ヘッドレス）のみ**。画面の計算値（`getComputedStyle`・寸法）は、ブラウザの標準スタイル（文字 16px、body の余白 8px など）に依存するため、他のブラウザでは未確認。
5. 画像・外部ファイル・通信は、採点に使わない（オフラインでも、同じ結果になるように）。`localStorage` / `fetch` は、隔離環境（sandbox）で動かせないため、扱わない（JavaScript の次の一歩として、教科書の最後で名前だけ紹介）。

## 10.2 カリキュラム

### JavaScript（目標: ブラウザで動くプログラムを作れる）
| ステージ | 内容 |
|---|---|
| 1 変数とデータ型 | console.log・コメント・let / const・number / string / boolean / undefined / null・typeof |
| 2 演算子 | 算術・代入・文字列の連結・テンプレートリテラル・=== と ==・&& \|\| !・型変換と NaN |
| 3 条件分岐 | if / else if / else・truthy / falsy・三項演算子・switch・条件の順序と境界値 |
| 4 繰り返し | for・while・累積・break / continue・入れ子・無限ループ |
| 5 配列 | 添字・length・push / pop・includes / indexOf / slice / join・for...of・const の配列 |
| 6 オブジェクト | プロパティの読み書き・ネスト・Object.keys・オブジェクトの配列・JSON.stringify |
| 7 関数 | 引数・戻り値・アロー関数・デフォルト引数・スコープ・map / filter / forEach |
| 8 DOM操作 | querySelector・textContent / value・classList・style・createElement / appendChild・innerHTML との安全性の違い |
| 9 イベント処理 | addEventListener・イベントオブジェクト・input / submit・preventDefault・バブリング |
| 10 簡単なWebアプリ制作 | データと表示の分離・入力値の型変換・空の入力・カウンター / ToDo / タブ / 文字数カウンター |

### HTML/CSS（目標: Webページの構造とデザインを理解し、簡単なページを自分で作れる）
| ステージ | 内容 |
|---|---|
| 1 HTMLの基本構造 | マークアップ言語・要素 / タグ / 属性・doctype・html / head / body・空白と改行・コメント |
| 2 見出し・段落・テキスト | h1〜h6・p・br / hr・strong / em・div / span・ブロックとインライン・文字参照 |
| 3 リンクと画像 | a・href・相対パス・ページ内リンク・target / rel・img・alt・width / height・figure |
| 4 リストとページ構造 | ul / ol / li・入れ子・header / nav / main / footer / article / section |
| 5 フォーム | form・input の type・name・label・radio / checkbox / select / textarea・required・入力チェック |
| 6 CSSの基本 | ルールの構文・セレクタ・プロパティ・値・適用方法・color / background-color・詳細度・継承 |
| 7 文字と色の装飾 | 色の指定方法・font-size と単位（px / em / rem / %）・line-height・text-align・子孫 / 子 / グループセレクタ・:hover |
| 8 ボックスモデル | content / padding / border / margin・box-sizing・margin の省略記法と相殺・margin: 0 auto・display |
| 9 Flexbox | display: flex・主軸と交差軸・justify-content / align-items・gap・flex-wrap・flex: 1 |
| 10 レスポンシブデザインと簡単なページ制作 | viewport・max-width・メディアクエリ・モバイルファースト・ページを組み立てる |

## 10.3 用語の方針（HTML/CSS はプログラミング言語ではない）

- HTML は「**マークアップ言語**」、CSS は「**スタイルシート言語**」、JavaScript は「**プログラミング言語**」と書き分ける。HTML・CSS を「プログラミング言語」「コード（を実行する）」とは呼ばない。
- HTML/CSS では「実行」ではなく「**表示する・読み込む・ブラウザが解釈する**」、問題の形式は「実行結果の予測」ではなく「**表示の予測**」、「コード作成」ではなく「**HTML/CSSを書く**」、ボタンは「実行して試す」ではなく「**プレビューする**」と表記する（`course.ui` で切り替え）。
- 構成の用語は、**要素・開始タグ・終了タグ・内容・属性・属性値・空要素・文書型宣言**（HTML）、**ルール（ルールセット）・セレクタ・宣言（ブロック）・プロパティ・値・詳細度・継承・疑似クラス・メディアクエリ**（CSS）、**Flex コンテナ / Flex アイテム・主軸 / 交差軸**（Flexbox）を、正式な名前で使う。
- コース選択画面と、HTML/CSS ステージ1・6 の教科書に、「HTML と CSS はプログラミング言語ではない」ことを明記している。
- ※ 用語や仕様の記述を、HTML Living Standard・CSS 仕様・MDN などの一次資料で照合する作業は、**この作業では行っていません**（検証は、Chrome での実測に基づく。`courses/validation_report_web.md` を参照）。

## 10.4 採点の仕組み（詳細は `docs/05_grading_spec.md` の 5.9）

| 問題 | 方法 |
|---|---|
| 選択・穴埋め・間違い探し（選択式 / 入力式） | Python コースと同じ（`choice_id` / `accepted_answers` / `output_compare`） |
| JavaScript のコード作成 | Web Worker で実行し、`console.log` の出力・関数の戻り値を、テストと比較（`engine: js_worker`） |
| DOM操作・イベント処理・HTML・CSS | 隔離した iframe に読み込み、操作（クリックなど）を実行して、「この条件を満たすか」を式で判定（`engine: page`） |

HTML/CSS では、**ブラウザの実測値**（文書の互換モード、`getComputedStyle`・`getBoundingClientRect`・`validity` など）で判定します。そのため、「HTML を正規表現で調べる」不確かな採点を避け、**書き方が違っても、同じ表示になる別解を正解にできます**。

## 10.5 学習者のコードの安全性

- JavaScript は Worker の中で実行（DOM・localStorage に触れない。`fetch` 等は無効化）。時間切れ（3秒）で Worker を強制終了。出力は 64KB で打ち切り。
- HTML/CSS/DOM は `sandbox="allow-scripts"` の iframe（`allow-same-origin` なし。**親ページの localStorage・DOM に触れない**）。時間切れ（4秒）で iframe を取り除く。`while (true)` などの明らかな無限ループは、DOM 操作の問題で、実行前に止める。
- Chrome では、iframe の無限ループが親ページを止めないことを確認（時間切れで打ち切られる）。**他のブラウザでは未確認**。
