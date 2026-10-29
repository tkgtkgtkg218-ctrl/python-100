# はじめの100問 — Python・JavaScript・HTML/CSS（学習アプリと教材データ）

初心者向けに、「短い教科書を読む → その場で問題を解く → 解説で理解する」を繰り返す学習アプリと、その教材データです。3コース × 10ステージ × 10問 = **全300問**。

| コース | 内容 | データ |
|---|---|---|
| Python | 基本構文・条件分岐・繰り返し・リスト・関数・エラー・辞書・ミニプログラム | ルートの `curriculum.json` / `lessons.json` / `questions.json`（`PY-001`〜`PY-100`） |
| JavaScript | ブラウザで動くプログラムを作る。変数・演算子・条件分岐・繰り返し・配列・オブジェクト・関数・DOM操作・イベント処理・簡単なWebアプリ | `courses/javascript-basics-ja/`（`JS-001`〜`JS-100`） |
| HTML/CSS | Webページの構造とデザイン。HTML の基本・文章・リンクと画像・リスト・フォーム・CSS・ボックスモデル・Flexbox・レスポンシブ | `courses/htmlcss-basics-ja/`（`HC-001`〜`HC-100`） |

HTML と CSS は、プログラミング言語ではなく、それぞれマークアップ言語・スタイルシート言語です（JavaScript はプログラミング言語）。

## アプリ
- 公開用の PWA 一式は `public/`（`index.html` / `manifest.webmanifest` / `sw.js` / `icons/`）。ビルド済みなので、そのまま静的ホスティングできます（`vercel.json` で `outputDirectory: public` を指定済み）。
- `app/index.html` は、ダブルクリックで開ける単一HTML（PWA 機能なし）です。
- 自動採点は全300問。コード作成は、**Python = Pyodide（Web Worker）**、**JavaScript = Web Worker**、**HTML/CSS・DOM操作 = sandbox 付き iframe** で、テストを実行して採点します。「実行して試す」「プレビューする」で、採点せずに結果を確認できます。
- 進捗は、ブラウザの localStorage にコース別に保存されます。
- 開発用画面: コースのステージ一覧の下の「コード採点の自己テスト」（`#/py/selftest` `#/js/selftest` `#/htmlcss/selftest`）。「すべてのステージを開く」でロックを外せます。
- 初回だけネットワークが必要なもの: Python のコード作成（jsDelivr から Pyodide を取得）。JavaScript・HTML/CSS コースは、初回の読み込み後、**オフラインでも**学習・採点できます。

## 公開する（GitHub + Vercel）
1. GitHub にリポジトリを作り、このフォルダを push する。
2. Vercel のダッシュボードで **Add New → Project** → そのリポジトリを **Import** → Framework Preset は **Other**（Build Command などは空のまま）→ **Deploy**。
3. 更新するとき: `python src/build_app.py` → `public/` ごとコミットして push → Vercel が自動で再デプロイ → 利用者の画面に「新しいバージョンがあります。［更新する］」が出る。学習の進捗は消えません。

## 教材データを直して作り直す
教材の**原本**は、Python = `src/s01.py`〜`s10.py`、JavaScript = `src/web/js/s01.py`〜、HTML/CSS = `src/web/htmlcss/s01.py`〜 です。JSON・`docs/`・`courses/*/docs/`・`public/` は生成物なので、直接編集せず、原本を直して再生成してください。

```bash
# Python コース
python src/verify.py && python src/claims.py && python src/check_scope.py && python src/gen_docs.py
# JavaScript / HTML・CSS コース（JSON を作る → 構造を確認 → ブラウザで実行検証 → 文書を作る）
python src/build_web.py
python src/verify_web_struct.py
node src/web_verify_run.js courses/javascript-basics-ja
node src/web_verify_run.js courses/htmlcss-basics-ja
python src/gen_docs.py courses/javascript-basics-ja && python src/gen_docs.py courses/htmlcss-basics-ja
# アプリを作り直す
python src/make_icons.py   # アイコン（初回のみ）
python src/build_app.py
```
`node src/web_verify_run.js` などのブラウザ検証には、Google Chrome（Windows の標準の場所）が必要です（`CHROME` 環境変数で場所を変えられます）。

## 確認用のスクリプト
| コマンド | 内容 |
|---|---|
| `python src/parity_test.py` | JavaScript の採点器（`app/grader.js`）と、Python の参照実装の判定が一致するか |
| `node src/app_e2e.js <URL> [py\|js\|htmlcss\|all]` | 実際の画面を操作して、全問題に、正解と誤答を入力（ヘッドレス Chrome） |
| `node src/pwa_test.js phase1\|phase2\|phase3 <プロファイル> <URL>` | PWA（Service Worker・インストール可否・オフライン・更新）の確認 |
| `node src/web_eval.js <format> <ファイル> "<式>"` | HTML/CSS/JS の断片を、採点基盤と同じ仕組みで読み込み、式の値を表示 |

## ドキュメント
| ファイル | 内容 |
|---|---|
| `docs/01_design_policy.md` 〜 `docs/09_final_checklist.md` | Python コースの、設計方針・カリキュラム・教科書・問題集・採点仕様・画面仕様・チェックリスト |
| `docs/10_web_courses.md` | JavaScript・HTML/CSS コースの、設計方針・仮定・用語の方針・採点の仕組み |
| `courses/<コース>/docs/` | 各コースの、カリキュラム一覧・教科書本文・全100問の問題集（解答つき） |
| `validation_report.md` | Python コースの検証レポート |
| `courses/validation_report_web.md` | JavaScript・HTML/CSS コースの検証レポート |
| `data_dictionary.md` | JSON データ仕様書（6 が追加コースの項目） |
