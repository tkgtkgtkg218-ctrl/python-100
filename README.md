# Python はじめの100問 — 教材データ一式

プログラミング学習アプリ用の、Python 初心者向け教材・問題・検証データです（10ステージ × 10問 = 100問）。

## アプリに取り込むファイル
| ファイル | 内容 |
|---|---|
| `curriculum.json` | ステージ構成（目標・前提・出題計画・クリア条件） |
| `lessons.json` | 各ステージの教科書（本文・コード例・解説・よくある間違い・理解度チェック） |
| `questions.json` | 全100問（`PY-001`〜`PY-100`）。正解・解説・誤答理由・ヒント・採点方法つき |
| `data_dictionary.md` | 上記3ファイルの項目仕様 |

## ブラウザ試作（`app/index.html`）
`app/index.html` をブラウザで開くだけで動きます（サーバー不要。データは埋め込み済み）。
- 画面: ステージ一覧 / 教科書 / 問題回答＋フィードバック / ステージ結果 / 学習進捗。進捗は localStorage に保存。
- 自動採点: 全100問。コード作成（13問）は **Pyodide（Python 3.12）を Web Worker で動かし、`test_cases` を実行して採点**します（「実行して試す」ボタンも使えます）。
- **注意**: コード作成の採点には、初回にネットワーク（jsDelivr から Pyodide を取得。サイズ・初回の読み込み時間は未計測）が必要です。読み込めない場合は、画面の案内に従って自己採点に切り替えられます。
- 開発用: ステージ一覧の下の「コード採点の自己テスト」（`#/selftest`）で、13問の模範解答・別解・不合格例・初期コードの判定と、時間切れ・禁止機能の動作を確認できます。
- 「開発用: すべてのステージを開く」で、ロックを外して全ステージを確認できます。
- 再ビルド: `python src/build_app.py`（`app/grader.js`・`app/app.js`・`app/style.css` を編集したあと）。
- 採点器の照合: `python src/parity_test.py`（JS 採点器と Python 参照実装の判定が一致するかを確認）。

## PWA として公開する（GitHub + Vercel）
`public/` が公開用のPWA一式です（`index.html` / `manifest.webmanifest` / `sw.js` / `icons/`）。ビルド済みなので、Vercel 側でビルドする必要はありません（`vercel.json` で `outputDirectory: public` を指定済み）。

1. GitHub に新しいリポジトリを作り、このフォルダを push する。
2. Vercel のダッシュボードで **Add New → Project** → GitHub のそのリポジトリを **Import** → Framework Preset は **Other**（Build Command などは空のまま）→ **Deploy**。
3. 発行された `https://<プロジェクト名>.vercel.app` を、スマホの Chrome / Safari で開く。Chrome は「インストール」ボタン、iPhone は「共有 → ホーム画面に追加」でアプリになる。
4. 更新するとき: 教材（`src/s01.py`〜）やアプリ（`app/*.js` など）を直す → `python src/build_app.py` → `public/` ごとコミットして push → Vercel が自動で再デプロイ → 利用者の画面に「新しいバージョンがあります。［更新する］」が出る。学習の進捗（localStorage）は更新しても消えない。

PWA の確認項目（ヘッドレス Chrome で実測。`node src/pwa_test.js`）: Service Worker の登録、インストール可否（エラー0件）、アプリ本体と Pyodide のキャッシュ、サーバー停止＋CDN 遮断でのオフライン起動と採点、更新バナーと古いキャッシュの削除。

## ドキュメント
| ファイル | 内容 |
|---|---|
| `docs/01_design_policy.md` | 1. 教材設計方針 |
| `docs/02_curriculum.md` | 2. カリキュラム一覧 |
| `docs/03_textbook.md` | 3. 教科書本文 |
| `docs/04_question_book.md` | 4. 全100問（解答・解説つき） |
| `docs/05_grading_spec.md` | 5. 採点仕様 |
| `validation_report.md` | 6. 事実確認・品質検証レポート |
| `data_dictionary.md` | 7. JSONデータ仕様書 |
| `docs/08_app_spec.md` | 8. Webアプリの画面・機能仕様 |
| `docs/09_final_checklist.md` | 9. 最終チェックリスト |

## 再生成・再検証（Python 3.10 以上。動作確認は 3.12.10）
`s01.py`〜`s10.py` が教材の原本です。JSONと `docs/02〜04` は生成物なので、直接編集せず原本を直して再生成してください。

```bash
python src/verify.py        # JSON生成 + 全問の実行検証
python src/claims.py        # 「○○Errorになる」という記述の実行検証
python src/check_scope.py   # 未習構文の混入チェック
python src/gen_docs.py      # docs/02〜04 を再生成
```
