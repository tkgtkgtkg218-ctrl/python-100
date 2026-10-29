"""JavaScript / HTML・CSS コースの原本（src/web/<course>/s01.py〜s10.py）から、
courses/<コースID>/{curriculum,lessons,questions}.json を生成する。構造チェックも行う。

  python src/build_web.py            # 2コースとも
  python src/build_web.py js         # 指定したコースだけ
"""
import importlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CLEAR_CONDITION = {
    "type": "first_attempt_correct_count",
    "required_correct": 7,
    "total_questions": 10,
    "description": "ステージ内の10問すべてに最後まで回答し、1回目の回答で7問以上正解するとクリア。",
    "stars": {"1": 7, "2": 9, "3": 10},
    "retry_policy": "不正解でも同じ問題に何度でも再挑戦できる（再挑戦での正解は学習履歴には残るが、クリア判定・星には数えない）。クリアできなかった場合は「ステージをやり直す」で新しい挑戦を始められる。",
    "unlock_next_stage": True,
}

COURSES = {
    "js": {
        "id": "javascript-basics-ja", "prefix": "JS", "language": "javascript", "language_display_name": "JavaScript",
        "subject_kind": "programming_language", "title": "JavaScript はじめの100問", "package": "web.js",
        "environment_checked": "Google Chrome（ヘッドレス）で実行検証",
        "scope": "ステージ1〜%dで学習した内容のみを前提とする。ブラウザ上で動く JavaScript（ES2015 以降）を扱い、Node.js 固有の機能や外部ライブラリは使わない。",
        "ui": {
            "type_labels": {"multiple_choice": "3択", "predict_output": "実行結果の予測", "fill_blank": "穴埋め", "bug_fix": "間違い探し", "code_write": "コード作成"},
            "write_button": "回答する（自動採点）", "run_button": "実行して試す", "run_output_label": "実行結果",
        },
    },
    "htmlcss": {
        "id": "htmlcss-basics-ja", "prefix": "HC", "language": "html-css", "language_display_name": "HTML/CSS",
        "subject_kind": "markup_and_stylesheet_languages", "title": "HTML/CSS はじめの100問", "package": "web.htmlcss",
        "environment_checked": "Google Chrome（ヘッドレス）で表示・計算値を検証",
        "scope": "ステージ1〜%dで学習した内容のみを前提とする。HTML（マークアップ言語）と CSS（スタイルシート言語）だけを扱い、JavaScript は使わない。",
        "ui": {
            "type_labels": {"multiple_choice": "3択", "predict_output": "表示の予測", "fill_blank": "穴埋め", "bug_fix": "間違い探し", "code_write": "HTML/CSSを書く"},
            "write_button": "回答する（自動採点）", "run_button": "プレビューする", "run_output_label": "表示結果",
        },
    },
}


def rebalance(questions, seed):
    """選択式問題の正解の位置（1番目・2番目・3番目）が偏らないよう、選択肢の並びを決定的に入れ替える。
    選択肢IDは並び順に c1,c2,c3 を振り直し、正解ID・誤答理由・check.choice_values のキーも付け替える。"""
    ids = [q for q in questions if q["answer_mode"] == "choice"]
    targets = ([0, 1, 2] * (len(ids) // 3 + 1))[: len(ids)]
    random.Random(seed).shuffle(targets)
    for q, target in zip(ids, targets):
        old_ids = [c["id"] for c in q["choices"]]
        cur = old_ids.index(q["answer"]["correct_choice_id"])
        others = [i for i in range(3) if i != cur]
        order = [cur if pos == target else others.pop(0) for pos in range(3)]  # order[新しい位置] = 古い位置
        new_ids = ["c1", "c2", "c3"]
        remap = {old_ids[order[pos]]: new_ids[pos] for pos in range(3)}
        q["choices"] = [{"id": new_ids[pos], "text": q["choices"][order[pos]]["text"]} for pos in range(3)]
        q["answer"]["correct_choice_id"] = remap[q["answer"]["correct_choice_id"]]
        q["wrong_answer_reasons"] = {remap[k]: v for k, v in q["wrong_answer_reasons"].items()}
        if q.get("check") and q["check"].get("choice_values"):
            q["check"]["choice_values"] = {remap[k]: v for k, v in q["check"]["choice_values"].items()}


def build_course(key):
    cfg = COURSES[key]
    mods = []
    for n in range(1, 11):
        name = "%s.s%02d" % (cfg["package"], n)
        try:
            mods.append(importlib.import_module(name))
        except ModuleNotFoundError as e:
            if e.name != name or not os.environ.get("PARTIAL"):
                raise
            break  # PARTIAL=1 のときは、書き終えたステージまでで試作ビルドする
    out_dir = os.path.join(ROOT, "courses", cfg["id"])
    os.makedirs(out_dir, exist_ok=True)
    stages, lessons, questions = [], [], []
    qn = 0
    for m in mods:
        st = m.STAGE
        n = st["number"]
        sid = "S%02d" % n
        assert len(m.QUESTIONS) == 10, "%s stage %d has %d questions" % (key, n, len(m.QUESTIONS))
        plan = []
        for i, q in enumerate(m.QUESTIONS, 1):
            qn += 1
            q = dict(q)
            q["id"] = "%s-%03d" % (cfg["prefix"], qn)
            q["course_id"] = cfg["id"]
            q["language"] = cfg["language"]
            q["stage_id"] = sid
            q["stage_number"] = n
            q["number_in_stage"] = i
            if q["preconditions"] == "このステージまでの内容のみ":
                q["preconditions"] = cfg["scope"] % n
            if q["type"] == "code_write" and q["grading"]["engine"] == "js_worker":
                q["prefix_code"] = q["grading"]["tests"][0].get("setup", "")
            order = ["id", "course_id", "language", "code_language", "stage_id", "stage_number", "number_in_stage", "title", "type", "answer_mode",
                     "difficulty", "concepts", "preconditions", "prompt", "code", "context_html", "prefix_code", "prefix_html", "starter_code",
                     "answer_format", "choice_format", "choices", "check", "answer", "grading", "rationale", "explanation",
                     "wrong_answer_reasons", "common_mistakes", "hint", "feedback_correct", "feedback_incorrect"]
            q2 = {k: q[k] for k in order if k in q}
            for k in q:
                if k not in q2:
                    q2[k] = q[k]
            questions.append(q2)
            plan.append({"question_id": q["id"], "number_in_stage": i, "title": q["title"], "type": q["type"], "difficulty": q["difficulty"], "concepts": q["concepts"]})
        stages.append({
            "id": sid, "number": n, "title": st["title"], "subtitle": st["subtitle"],
            "learning_goals": st["goals"], "prerequisite_knowledge": st["prerequisites"],
            "prerequisite_stage_ids": ["S%02d" % (n - 1)] if n > 1 else [],
            "topics": st["topics"], "common_pitfalls": st["pitfalls"], "lesson_id": "LESSON-" + sid,
            "question_plan": plan, "clear_condition": CLEAR_CONDITION, "leads_to": st["next_links"],
            "unlock_condition": None if n == 1 else {"type": "stage_cleared", "stage_id": "S%02d" % (n - 1)},
        })
        lessons.append({
            "id": "LESSON-" + sid, "stage_id": sid, "title": st["title"], "intro": st["lesson"]["intro"],
            "sections": st["lesson"]["sections"], "common_mistakes": st["lesson"]["common_mistakes"],
            "checkpoints": st["lesson"]["checkpoints"], "next_bridge": st["lesson"]["next_bridge"],
        })
    rebalance(questions, cfg["id"])
    course = {
        "id": cfg["id"], "language": cfg["language"], "language_display_name": cfg["language_display_name"],
        "subject_kind": cfg["subject_kind"], "environment_checked": cfg["environment_checked"],
        "locale": "ja-JP", "title": cfg["title"], "schema_version": "1.1.0", "ui": cfg["ui"],
    }
    docs = {
        "curriculum.json": {"course": course, "stages": stages},
        "lessons.json": {"course_id": cfg["id"], "schema_version": "1.1.0", "lessons": lessons},
        "questions.json": {"course_id": cfg["id"], "schema_version": "1.1.0", "question_count": len(questions), "questions": questions},
    }
    for name, obj in docs.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return out_dir, docs


def main():
    keys = sys.argv[1:] or list(COURSES)
    for k in keys:
        out_dir, docs = build_course(k)
        print(k, "->", out_dir, "questions:", docs["questions.json"]["question_count"])


if __name__ == "__main__":
    main()
