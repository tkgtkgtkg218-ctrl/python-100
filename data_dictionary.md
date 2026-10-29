# データ仕様書（Data Dictionary）

対象ファイル: Python コースの `curriculum.json` / `lessons.json` / `questions.json`（ルート。`schema_version` 1.0.0）、および JavaScript・HTML/CSS コースの同名3ファイル（`courses/javascript-basics-ja/`・`courses/htmlcss-basics-ja/`。`schema_version` 1.1.0）。UTF-8、コメント・末尾カンマなし。

> 追加コースで増えた項目は、**末尾の「6. JavaScript / HTML・CSS コースで追加された項目」**にまとめてあります（Python コースの項目は、すべてそのまま使えます）。

凡例: **必須**=常に存在 / 条件付=特定の `type`・`answer_mode` のときのみ / 任意=ないことがある。型: string, int, bool, array, object, null。

## 0. 全体の関係

```
curriculum.json ── stages[].id (S01..S10) ──┬─ lessons.json   lessons[].stage_id
                  stages[].lesson_id ───────┘                 lessons[].id = "LESSON-S01".."LESSON-S10"
                  stages[].question_plan[].question_id ────── questions.json questions[].id (PY-001..PY-100)
questions[].stage_id ───────────────────────────────────────── curriculum.json stages[].id
```

- ID は重複しない。`PY-001`〜`PY-100` は連番。ステージ n の問題は `PY-(10(n-1)+1)`〜`PY-(10n)`。
- 将来の言語追加: `course.language` と各問題の `language` を使い、`course.id` を別にして同じ構造のファイルを追加する（例: `javascript-basics-ja`）。`type`・`grading.method` は言語に依存しない名前にしてある。実行系だけ言語別のランナーを用意する。

## 1. curriculum.json

### ルート
| 項目 | 型 | 区分 | 意味 |
|---|---|---|---|
| `course` | object | 必須 | コース情報 |
| `stages` | array | 必須 | ステージ10件（番号順） |

### `course`
| 項目 | 型 | 区分 | 意味 / 例 |
|---|---|---|---|
| `id` | string | 必須 | コースID。`python-basics-ja` |
| `language` | string | 必須 | プログラミング言語の識別子。`python` |
| `language_display_name` | string | 必須 | 表示名。`Python` |
| `language_version_checked` | string | 必須 | 実際に動作確認したバージョン。`3.12.10` |
| `language_version_policy` | string | 必須 | 想定バージョンの方針 |
| `locale` | string | 必須 | 表示言語。`ja-JP` |
| `title` | string | 必須 | コース名 |
| `schema_version` | string | 必須 | データ形式のバージョン |

### `stages[]`
| 項目 | 型 | 区分 | 意味 |
|---|---|---|---|
| `id` | string | 必須 | `S01`〜`S10` |
| `number` | int | 必須 | 1〜10 |
| `title`, `subtitle` | string | 必須 | ステージ名、補足 |
| `learning_goals` | array<string> | 必須 | 学習目標 |
| `prerequisite_knowledge` | array<string> | 必須 | 学習前に必要な知識 |
| `prerequisite_stage_ids` | array<string> | 必須 | 直前のステージID（S01 は空配列） |
| `topics` | array<string> | 必須 | 教材で説明する項目 |
| `common_pitfalls` | array<string> | 必須 | つまずきやすいポイント |
| `lesson_id` | string | 必須 | `lessons.json` の `lessons[].id` への参照 |
| `question_plan` | array<object> | 必須 | 出題計画（10件）。`question_id`, `number_in_stage`, `title`, `type`, `difficulty`, `concepts`。`questions.json` から生成されるため常に一致 |
| `clear_condition` | object | 必須 | クリア条件（下記） |
| `leads_to` | array<string> | 必須 | 次のステージにつながる知識 |
| `unlock_condition` | object / null | 必須 | `{"type":"stage_cleared","stage_id":"S01"}`。S01 は `null` |

### `clear_condition`
| 項目 | 型 | 意味 |
|---|---|---|
| `type` | string | `first_attempt_correct_count`（1回目の回答での正解数） |
| `required_correct` | int | 7 |
| `total_questions` | int | 10 |
| `stars` | object | 星の条件 `{"1":7,"2":9,"3":10}` |
| `description`, `retry_policy` | string | 画面表示用の説明文 |
| `unlock_next_stage` | bool | クリア時に次のステージを解放するか |

## 2. lessons.json

ルート: `course_id`(string), `schema_version`(string), `lessons`(array)

### `lessons[]`
| 項目 | 型 | 区分 | 意味 |
|---|---|---|---|
| `id` | string | 必須 | `LESSON-S01` など |
| `stage_id` | string | 必須 | 所属ステージ |
| `title` | string | 必須 | ステージ名 |
| `intro` | string | 必須 | 導入（この知識が何に役立つか） |
| `sections` | array<object> | 必須 | 教科書のセクション（各ステージ2件） |
| `common_mistakes` | array<object> | 必須 | よくある間違い（各4件） |
| `checkpoints` | array<string> | 必須 | 理解度チェック |
| `next_bridge` | string | 必須 | 次の問題への導入 |

### `sections[]`
| 項目 | 型 | 区分 | 意味 |
|---|---|---|---|
| `id` | string | 必須 | `S01-L1` など |
| `title` | string | 必須 | セクション名 |
| `read_minutes` | int | 必須 | 読む時間の目安（分） |
| `body` | array<string> | 必須 | 本文（段落ごと） |
| `glossary` | array<object> | 必須 | `{term, definition}` 用語解説 |
| `examples` | array<object> | 必須 | コード例 |

### `examples[]`
| 項目 | 型 | 区分 | 意味 |
|---|---|---|---|
| `id` | string | 必須 | `S01-E1` など |
| `title` | string | 必須 | 見出し |
| `code` | string | 必須 | 実行できる Python コード（`\n` 区切り） |
| `expected_output` | string | 必須 | 標準出力（エラー例では空文字） |
| `expected_error` | string | 任意 | エラー例のとき発生するエラー名（例 `NameError`）。ある場合は出力ではなくエラーを表示する |
| `line_notes` | array<string> | 必須 | コードの解説 |

### `common_mistakes[]`
`title`, `wrong_code`（誤ったコード）, `why`（理由）, `fix`（直し方）— すべて string・必須。※ `wrong_code` は説明用で、実行を保証しない（一部は擬似的な断片）。

## 3. questions.json

ルート: `course_id`, `schema_version`, `question_count`(int, =100), `questions`(array)

### 共通項目（全問）
| 項目 | 型 | 区分 | 意味 / 例 |
|---|---|---|---|
| `id` | string | 必須 | `PY-001`〜`PY-100`（一意） |
| `course_id` | string | 必須 | `python-basics-ja` |
| `language` | string | 必須 | `python` |
| `stage_id` | string | 必須 | `S01`〜`S10` |
| `stage_number` | int | 必須 | 1〜10 |
| `number_in_stage` | int | 必須 | 1〜10 |
| `title` | string | 必須 | 問題タイトル（全問で重複なし） |
| `type` | string | 必須 | `multiple_choice` / `predict_output` / `fill_blank` / `bug_fix` / `code_write` |
| `answer_mode` | string | 必須 | `choice`（選択肢から選ぶ）/ `text`（文字入力）/ `code`（コードエディタ） |
| `difficulty` | int | 必須 | 1〜5 |
| `concepts` | array<string> | 必須 | 学習対象の概念 |
| `preconditions` | string | 必須 | 問題の前提条件（使ってよい範囲） |
| `prompt` | string | 必須 | 問題文 |
| `code` | string / null | 必須 | 提示コード。ない場合は `null`。穴埋めは `__1__` のような空欄マーカーを含む |
| `answer` | object | 必須 | 正解データ（下記の型別） |
| `grading` | object | 必須 | 採点方法（下記） |
| `rationale` | string | 必須 | 正解の根拠（1文） |
| `explanation` | string | 必須 | 初心者向けの詳しい解説 |
| `hint` | string | 必須 | ヒント（答えそのものは書かない） |
| `feedback_correct` | string | 必須 | 正解後に表示する短い文 |
| `feedback_incorrect` | string | 必須 | 不正解後に表示する短い文 |
| `wrong_answer_reasons` | object | 条件付 | `answer_mode=choice` のとき。`{選択肢ID: 誤りの理由}`（正解以外の2つ。**正解の選択肢IDは含まない**） |
| `common_mistakes` | array<object> | 条件付 | `answer_mode=text` の `predict_output`/`fill_blank`/`bug_fix`。よくある誤答と理由 |
| `choices` | array<object> | 条件付 | `choice` のとき `[{id, text}]` を3件。`id` は `c1`,`c2`,`c3` |
| `choice_format` | string | 条件付 | `text`（通常の文）/ `code`（等幅表示）。`choices` と同時に存在 |
| `starter_code` | string | 条件付 | `code_write` の初期コード |
| `prefix_code` | string | 条件付 | `code_write`。読み取り専用で先頭に付けるコード（最初の公開テストの `setup`）。空文字のこともある |

### `answer`（型別）
| `type` / `answer_mode` | 項目 |
|---|---|
| `multiple_choice` | `correct_choice_id`(string) |
| `predict_output` / `choice` | `correct_choice_id`, `expected_output`(string, 実際に実行して得た出力と一致することを検証済み) |
| `predict_output` / `text` | `expected_output` |
| `fill_blank` | `blanks`: `[{id:"b1", marker:"__1__", accepted:[string], quote_insensitive:bool}]`、`expected_output`（全空欄に正解を入れたときの出力） |
| `bug_fix` / `choice` | `correct_choice_id`, `fixed_code`, `expected_output`, `buggy_error`(string, 誤りコードが起こすエラー名。無限ループは `Timeout`) または `buggy_output`(string), `target_line`(int, 任意: 選択肢が1行の置き換えである場合)、`choice_is_replacement_line`(bool, `target_line` があるとき `true`。選択肢の text でその行を置き換えて実行できることを示す) |
| `bug_fix` / `text` | `target_line`(int, 1始まり), `accepted`(array<string>), `quote_insensitive`(bool), `fixed_code`, `expected_output`, `buggy_error` または `buggy_output` |
| `code_write` | `reference_solution`(string), `alternative_solutions`(array<string>, 合格すべき別解), `rejected_examples`(array<{code, reason}>, 不合格になるべき例) |

### `grading`
| 項目 | 型 | 対象 | 意味 |
|---|---|---|---|
| `method` | string | 全問 | `choice_id` / `output_compare` / `accepted_answers` / `test_cases` |
| `normalize` | array<string> | `output_compare`, `accepted_answers` | 適用する正規化の名前（`crlf_to_lf`, `rstrip_each_line`, `strip_trailing_blank_lines`, `nfkc`, `strip_outer_whitespace`） |
| `case_sensitive` | bool | `output_compare` | 常に `true` |
| `keep_inner_whitespace` | bool | `accepted_answers` | 常に `true`（内部の空白は変更しない） |
| `scope` | string | 入力式 `bug_fix` | `target_line_replacement` |
| `tests` | array<object> | `test_cases` | テストケース（下記） |
| `required_ast_nodes` | array<string> | `test_cases` | 学習者コードに**すべて**含まれるべき Python AST ノード名（例 `FunctionDef`, `If`, `For`, `Try`） |
| `required_any_ast_nodes` | array<string> | `test_cases` | **いずれか**が含まれるべきノード名（例 `["For","While"]`） |
| `timeout_sec` | int | `test_cases` | テスト1件の実行時間上限（5） |
| `execution` | string | `test_cases` | `sandboxed_worker`（隔離実行が必須であることを示す） |
| `normalize_stdout` | array<string> | `test_cases` | `stdout` 型テストの出力比較時の正規化 |

### `tests[]`
| 項目 | 型 | 意味 |
|---|---|---|
| `kind` | string | `stdout`（標準出力を比較）/ `call`（式を評価して比較） |
| `setup` | string | 学習者コードの**前**に実行するコード（入力変数の定義など） |
| `expected_stdout` | string | `stdout` 型の期待出力 |
| `call` | string | `call` 型で評価する式（例 `is_even(4)`） |
| `expected` | string | `call` 型の期待値を表す **Python リテラル文字列**（例 `'True'`, `"'大吉'"`）。`repr(結果) == repr(literal_eval(expected))` で比較 |
| `visible` | bool | `false` は非公開テスト（結果の詳細を学習者に見せない） |

## 4. 使用例（抜粋）

### 4.1 3択（PY-001）
```json
{
  "id": "PY-001", "type": "multiple_choice", "answer_mode": "choice",
  "choices": [{"id":"c1","text":"紙に文字を印刷する"},{"id":"c2","text":"画面に文字や数値を表示する"},{"id":"c3","text":"キーボードから文字を受け取る"}],
  "answer": {"correct_choice_id": "c2"},
  "wrong_answer_reasons": {"c1": "...", "c3": "..."},
  "grading": {"method": "choice_id"}
}
```
採点: `selected === answer.correct_choice_id`。

### 4.2 穴埋め（PY-008）
```json
{ "code": "print(__1__)",
  "answer": {"blanks":[{"id":"b1","marker":"__1__","accepted":["\"Python\""],"quote_insensitive":true}], "expected_output":"Python"},
  "grading": {"method":"accepted_answers", "normalize":["nfkc","strip_outer_whitespace"], "keep_inner_whitespace": true} }
```
採点: 回答 `{ "b1": "'Python'" }` → NFKC・前後空白除去・引用符統一 → `"Python"` と一致 → 正解。

### 4.3 コード作成（PY-060）
```json
{ "grading": {"method":"test_cases", "required_ast_nodes":["FunctionDef"],
    "tests":[{"kind":"call","setup":"","call":"is_even(4)","expected":"True","visible":true},
             {"kind":"call","setup":"","call":"is_even(0)","expected":"True","visible":false}]} }
```
採点: 静的チェック → 各テストを隔離環境で実行 → 全合格で正解。

## 5. 実装上の注意

- `choices` の表示順はランダム化してよい。判定は必ず `id` で行う。
- `explanation` 等はプレーンテキスト。改行は `\n`。HTML を含まない（表示時にエスケープすること）。
- `code` は `\n` を含む文字列。画面では等幅フォントで表示し、インデントを保持する。
- 入力式 `bug_fix` では、`code` の `target_line` 行の**インデントを保ったまま**、行の中身だけを学習者の入力で置き換えて表示・実行する。
- 進捗データ（回答履歴・クリア状況）は本データの外（アプリ側のストレージ）に持つ。推奨スキーマは `docs/08_app_spec.md` を参照。

## 6. JavaScript / HTML・CSS コースで追加された項目

ファイル構成・ID・参照関係は Python コースと同じです（ID の接頭辞は `JS-001`〜`JS-100`、`HC-001`〜`HC-100`。ステージ ID は各コース内で `S01`〜`S10`）。アプリは、3コースのデータを `public/index.html` に埋め込み、`{"courses": [{key, tagline, curriculum, lessons, questions}]}` の形で読み込みます（`key` は `py` / `js` / `htmlcss`）。

### 6.1 curriculum.json の `course`（追加項目）
| 項目 | 型 | 区分 | 意味 |
|---|---|---|---|
| `subject_kind` | string | 追加コースで必須 | `programming_language`（JavaScript）/ `markup_and_stylesheet_languages`（HTML/CSS）。**HTML と CSS はプログラミング言語ではない**ため、教材の用語・画面の文言がこれに従う |
| `environment_checked` | string | 追加コースで必須 | 実行検証に使った環境（例: Google Chrome（ヘッドレス））。Python コースの `language_version_checked` に相当 |
| `ui` | object | 追加コースで必須 | 画面の文言。`type_labels`（問題形式の表示名。HTML/CSS では `predict_output` が「表示の予測」、`code_write` が「HTML/CSSを書く」）、`write_button`、`run_button`（JavaScript は「実行して試す」、HTML/CSS は「プレビューする」）、`run_output_label` |

### 6.2 lessons.json の `examples[]`（追加項目）
| 項目 | 型 | 区分 | 意味 |
|---|---|---|---|
| `language` | string | 追加コースで必須 | `javascript` / `html` / `css`（コードの表示用） |
| `context_html` | string | 任意 | 例の CSS・JavaScript が対象にする HTML（コードの前に表示する） |
| `preview` | object / null | 任意 | 実際に表示して見せるための指定 `{format, given_html?, viewport?}`。`format` は 6.4 を参照。`null`・なしなら表示しない |
| `verify` | object | 任意 | 機械検証の指定 `{format, given_html?, actions?, viewport?, expr, allow_errors?}`。`expr` が true になることを、ブラウザで確認する |
| `expected_output` | string | 任意 | JavaScript の `console.log` の出力。HTML/CSS の例では空 |

### 6.3 questions.json の問題（追加項目）
| 項目 | 型 | 区分 | 意味 |
|---|---|---|---|
| `code_language` | string | 必須 | `javascript` / `html` / `css`。コードの表示用 |
| `context_html` | string | 任意 | 問題のコード（CSS・JavaScript）が対象にする HTML。`check.given_html` と同じ値が入る |
| `check` | object | 任意 | その問題の正解を、ブラウザで機械検証・プレビューするための指定（下記）。画面では、解答後に「実際の表示を見る」として使う |
| `prefix_html` | string | `code_write`（page エンジン）で任意 | 提示済みの HTML（CSS・DOM 操作の問題）。学習者のコードと組み合わせて読み込む |
| `answer_format` | string | `code_write` で必須 | 学習者のコードの種類。`javascript`（console.log・関数）/ `javascript_dom`（`prefix_html` の中で動く JavaScript）/ `html_document`（HTML 文書全体）/ `html_body`（body の中身）/ `css`（`prefix_html` に適用する CSS） |
| `grading.engine` | string | `code_write` で必須 | `js_worker`（Web Worker で JavaScript を実行）/ `page`（隔離した iframe に読み込んで式で判定）。Python コースにはなく、あれば Pyodide |
| `grading.required_patterns` / `required_any_patterns` / `forbidden_patterns` | array<{pattern, message}> | `code_write` で任意 | 学習者のコードに、正規表現で、含まれるべき（すべて / いずれか）・含まれてはいけない書き方を指定する |
| `grading.viewport` | int | 任意 | `page` エンジンで、iframe の幅（px）の既定値 |

`check`（検証・プレビュー用）:
| 項目 | 型 | 意味 |
|---|---|---|
| `format` | string | コードを読み込む方法（6.4）。`javascript` は、`console.log` の出力だけで確認する問題（この場合 `check` は付けず、`expected_output` を使う） |
| `given_html` | string | `css` / `javascript_dom` のときの、提示済みの HTML |
| `expr` | string | 穴埋め・間違い探しで、**正しい答え**のときだけ true になる式。誤答では false になることを確認している |
| `probe` / `choice_values` / `expected` | string / object / any | 予測問題で、表示結果を値として取り出す式（`probe`）。選択式は、選択肢ID → 正解となる値の対応（`choice_values`）、入力式は期待値（`expected`）。**選択肢の文章ではなく、ブラウザの実測値**と照合している |
| `actions` | array<string / number> | `expr` / `probe` の前に実行する操作（クリックなどを行う式。数値は待ち時間 ms） |
| `viewport` | int | 画面の幅（px）。メディアクエリの確認用 |

### 6.4 コードを読み込む方法（`format` / `answer_format`）
| 値 | 組み立て方 |
|---|---|
| `html_document` | 学習者のコードを、HTML 文書全体として読み込む（`<!doctype html>` の有無による標準/互換モードの違いも再現される） |
| `html_body` | `<!doctype html>`・`<html lang="ja">`・head（meta charset・title）を付けて、body の中に、学習者のコードを入れる |
| `css` | 上と同じ文書の head に `<style>` として学習者の CSS を入れ、body に `given_html` を入れる |
| `javascript_dom` | body に `given_html` を入れ、その後ろに `<script>` として学習者の JavaScript を入れる |

### 6.5 `grading.tests[]`（追加の種類）
| `kind` | 項目 | 意味 |
|---|---|---|
| `stdout` | `setup`, `expected_stdout`, `visible` | Python と同じ。`console.log` の出力（引数は空白で区切って1行、行ごとに改行）を、正規化して比較。`setup` は学習者のコードの前に実行する JavaScript |
| `call` | `call`, `expected`, `setup`, `visible` | `call` の式を評価した戻り値を JSON にし、`expected`（**JSON 文字列**。例 `"5"`, `"\"abc\""`, `"[1,2]"`）と、構造として同じか（オブジェクトのキーの順序は無視）で比較 |
| `page` | `desc`, `expr`, `actions?`, `given_html?`, `viewport?`, `visible` | `desc`（画面に出す説明文）。ページを読み込み、`actions` を順に実行したあと、`expr` が true になるかで判定。`given_html` / `viewport` をテストごとに指定すると、別の入力・画面幅でも動くかを確認できる（非公開テストでよく使う）。**同じ `actions`・`given_html`・`viewport` のテストは、1つの iframe にまとめて評価する** |

### 6.6 実装上の追加の注意
- 選択式の選択肢の順序は、データ作成時（`src/build_web.py`）に、正解の位置が偏らないよう、決定的に並べ替えてあります（JavaScript: 1番目16・2番目16・3番目15、HTML/CSS: 19・19・18）。選択肢ID（`c1`〜`c3`）は、並べ替え後の順に付け直されています。アプリは、表示時にもランダムに並べ替えます。
- `page` エンジンの学習者のコードは、**`sandbox="allow-scripts"` のみ**（`allow-same-origin` なし）の iframe で動かします。親ページの `localStorage`・DOM には触れません。HTML・CSS のみの問題でも、同じ仕組みで読み込みます。
- 画像（`img`）を使う問題は、通信を伴わないよう、画像ファイルの有無に依存しない出題（`alt`・属性の確認、データ URI の画像）にしてあります。
