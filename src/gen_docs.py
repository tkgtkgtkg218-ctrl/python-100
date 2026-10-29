"""JSON から人が読む用の Markdown（カリキュラム一覧・教科書本文・問題集）を生成する。内容はJSONと常に一致する。"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
os.makedirs(DOCS, exist_ok=True)

TYPE_JA = {"multiple_choice": "3択選択", "fill_blank": "コード穴埋め", "predict_output": "実行結果の予測", "bug_fix": "間違い探し", "code_write": "コード作成"}
METHOD_JA = {"choice_id": "選択肢ID一致", "accepted_answers": "許容回答リスト照合", "output_compare": "出力比較（正規化あり）", "test_cases": "テストケース実行"}


def load(n):
    return json.load(open(os.path.join(ROOT, n), encoding="utf-8"))


def fence(code, lang="python"):
    return "```%s\n%s\n```" % (lang, code)


def w(name, text):
    with open(os.path.join(DOCS, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def curriculum_md(c, q):
    out = ["# 全10ステージのカリキュラム一覧\n", "対象: %s（%s） / 全%d問\n" % (c["course"]["title"], c["course"]["language_display_name"], q["question_count"])]
    for s in c["stages"]:
        out.append("\n## %s ステージ%d: %s\n" % (s["id"], s["number"], s["title"]))
        out.append("*%s*\n" % s["subtitle"])
        out.append("### 学習目標\n" + "\n".join("- " + x for x in s["learning_goals"]))
        out.append("\n### 学習前に必要な知識\n" + "\n".join("- " + x for x in s["prerequisite_knowledge"]))
        out.append("\n### 教材で説明する項目\n" + "\n".join("- " + x for x in s["topics"]))
        out.append("\n### つまずきやすいポイント\n" + "\n".join("- " + x for x in s["common_pitfalls"]))
        out.append("\n### 10問の出題計画\n")
        out.append("| 問題ID | No. | タイトル | 形式 | 難易度 | 学習概念 |\n|---|---|---|---|---|---|")
        for p in s["question_plan"]:
            out.append("| %s | %d | %s | %s | %d | %s |" % (p["question_id"], p["number_in_stage"], p["title"], TYPE_JA[p["type"]], p["difficulty"], "、".join(p["concepts"])))
        cc = s["clear_condition"]
        out.append("\n### ステージクリアの条件\n- %s\n- 星: ★=%d問 / ★★=%d問 / ★★★=%d問（1回目の正解数）\n- %s" % (cc["description"], cc["stars"]["1"], cc["stars"]["2"], cc["stars"]["3"], cc["retry_policy"]))
        out.append("\n### 次のステージにつながる知識\n" + "\n".join("- " + x for x in s["leads_to"]))
    return "\n".join(out) + "\n"


def textbook_md(l, c):
    out = ["# 各ステージの教科書本文\n"]
    for les in l["lessons"]:
        st = next(s for s in c["stages"] if s["id"] == les["stage_id"])
        out.append("\n---\n\n## ステージ%d: %s\n" % (st["number"], les["title"]))
        out.append("### 導入：この知識が何に役立つのか\n\n" + les["intro"] + "\n")
        for sec in les["sections"]:
            out.append("### %s（目安 %d分）\n" % (sec["title"], sec["read_minutes"]))
            for p in sec["body"]:
                out.append(p + "\n")
            out.append("**用語解説**\n" + "\n".join("- **%s**: %s" % (g["term"], g["definition"]) for g in sec["glossary"]) + "\n")
            for ex in sec["examples"]:
                out.append("**コード例（%s）: %s**\n" % (ex["id"], ex["title"]))
                out.append(fence(ex["code"]))
                if ex.get("expected_error"):
                    out.append("\n実行結果: `%s` が発生します（エラーになる例）\n" % ex["expected_error"])
                else:
                    out.append("\n実行結果:\n\n" + fence(ex["expected_output"], "text") + "\n")
                out.append("コードの解説:\n" + "\n".join("- " + n for n in ex["line_notes"]) + "\n")
        out.append("### よくある間違い\n")
        for m in les["common_mistakes"]:
            out.append("- **%s**\n\n  ```python\n  %s\n  ```\n  - 理由: %s\n  - 直し方: %s\n" % (m["title"], m["wrong_code"].replace("\n", "\n  "), m["why"], m["fix"]))
        out.append("### 理解度チェック\n" + "\n".join("- [ ] " + x for x in les["checkpoints"]) + "\n")
        out.append("### 次の問題への導入\n\n" + les["next_bridge"] + "\n")
    return "\n".join(out)


def questions_md(q):
    out = ["# 全100問の問題集（解答・解説つき）\n", "※ 機械可読版は `questions.json`。ここは確認・レビュー用の一覧です。\n"]
    cur = None
    for x in q["questions"]:
        if x["stage_id"] != cur:
            cur = x["stage_id"]
            out.append("\n---\n\n## ステージ%d\n" % x["stage_number"])
        out.append("\n### %s ステージ%d-%d: %s\n" % (x["id"], x["stage_number"], x["number_in_stage"], x["title"]))
        out.append("- 形式: %s ／ 難易度: %d ／ 概念: %s ／ 採点: %s" % (TYPE_JA[x["type"]], x["difficulty"], "、".join(x["concepts"]), METHOD_JA[x["grading"]["method"]]))
        out.append("- 前提: " + x["preconditions"] + "\n")
        out.append("**問題**: " + x["prompt"].replace("\n", "  \n") + "\n")
        if x.get("prefix_code"):
            out.append("前提コード（変更不可）:\n\n" + fence(x["prefix_code"]) + "\n")
        if x.get("code"):
            out.append(fence(x["code"]) + "\n")
        if x.get("starter_code"):
            out.append("初期コード:\n\n" + fence(x["starter_code"]) + "\n")
        a = x["answer"]
        if x.get("choices"):
            for ch in x["choices"]:
                mark = " ✅" if ch["id"] == a["correct_choice_id"] else ""
                txt = ch["text"]
                if x["choice_format"] == "code" or "\n" in txt:
                    txt = "`" + txt.replace("\n", " ⏎ ") + "`"
                out.append("- %s) %s%s" % (ch["id"], txt, mark))
                if ch["id"] != a["correct_choice_id"]:
                    out.append("  - 誤りの理由: " + x["wrong_answer_reasons"][ch["id"]])
            out.append("")
        elif x["type"] == "fill_blank":
            out.append("**正解**: " + " / ".join("空欄%d = %s" % (i + 1, " | ".join("`%s`" % t for t in b["accepted"])) for i, b in enumerate(a["blanks"])))
            out.append("- 実行結果: `%s`" % a["expected_output"].replace("\n", " ⏎ "))
            for m in x["common_mistakes"]:
                out.append("- よくある誤答 `%s`: %s" % (m["answer"], m["reason"]))
            out.append("")
        elif x["type"] == "predict_output":
            out.append("**正解（出力）**:\n\n" + fence(a["expected_output"], "text") + "\n")
            for m in x["common_mistakes"]:
                out.append("- よくある誤答 `%s`: %s" % (m["answer"].replace("\n", " ⏎ "), m["reason"]))
            out.append("")
        elif x["type"] == "bug_fix":
            out.append("**正解（%d行目の置換候補）**: " % a["target_line"] + " / ".join("`%s`" % t for t in a["accepted"]))
            out.append("- 修正後の全体:\n\n" + fence(a["fixed_code"]) + "\n")
            for m in x["common_mistakes"]:
                out.append("- よくある誤答 `%s`: %s" % (m["answer"], m["reason"]))
            out.append("")
        elif x["type"] == "code_write":
            out.append("**模範解答**:\n\n" + fence(a["reference_solution"]) + "\n")
            for i, alt in enumerate(a["alternative_solutions"], 1):
                out.append("別解%d（合格）:\n\n%s\n" % (i, fence(alt)))
            for r in a["rejected_examples"]:
                out.append("不合格例:\n\n%s\n\n- 理由: %s\n" % (fence(r["code"]), r["reason"]))
            out.append("テストケース（%d件、うち非公開 %d件）:" % (len(x["grading"]["tests"]), sum(1 for t in x["grading"]["tests"] if not t["visible"])))
            for t in x["grading"]["tests"]:
                v = "公開" if t["visible"] else "非公開"
                if t["kind"] == "stdout":
                    out.append("- [%s] setup=`%s` → 標準出力 `%s`" % (v, t["setup"].replace("\n", "; "), t["expected_stdout"].replace("\n", " ⏎ ")))
                else:
                    out.append("- [%s] `%s` → `%s`" % (v, t["call"], t["expected"]))
            req = x["grading"]["required_ast_nodes"] + (["いずれか: " + "/".join(x["grading"]["required_any_ast_nodes"])] if x["grading"]["required_any_ast_nodes"] else [])
            out.append("- 構文チェック: " + (", ".join(req) if req else "なし"))
            out.append("")
        out.append("**正解の根拠**: " + x["rationale"] + "\n")
        out.append("**解説**: " + x["explanation"] + "\n")
        out.append("- ヒント: " + x["hint"])
        out.append("- 正解後: " + x["feedback_correct"])
        out.append("- 不正解後: " + x["feedback_incorrect"])
    return "\n".join(out) + "\n"


def main():
    c, l, q = load("curriculum.json"), load("lessons.json"), load("questions.json")
    w("02_curriculum.md", curriculum_md(c, q))
    w("03_textbook.md", textbook_md(l, c))
    w("04_question_book.md", questions_md(q))
    print("docs generated")


if __name__ == "__main__":
    main()
