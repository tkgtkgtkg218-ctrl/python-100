"""s01.py〜s10.py から curriculum.json / lessons.json / questions.json を生成する。"""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

COURSE = {
    "id": "python-basics-ja",
    "language": "python",
    "language_display_name": "Python",
    "language_version_checked": "3.12.10",
    "language_version_policy": "Python 3.10 以上で同じ結果になる内容のみを使用",
    "locale": "ja-JP",
    "title": "Python はじめの100問",
    "schema_version": "1.0.0",
}

CLEAR_CONDITION = {
    "type": "first_attempt_correct_count",
    "required_correct": 7,
    "total_questions": 10,
    "description": "ステージ内の10問すべてに最後まで回答し、1回目の回答で7問以上正解するとクリア。",
    "stars": {"1": 7, "2": 9, "3": 10},
    "retry_policy": "不正解でも同じ問題に何度でも再挑戦できる（再挑戦での正解は学習履歴には残るが、クリア判定・星には数えない）。クリアできなかった場合は「ステージをやり直す」で新しい挑戦を始められる。",
    "unlock_next_stage": True,
}


def load_stages():
    mods = []
    for n in range(1, 11):
        try:
            mods.append(importlib.import_module("s%02d" % n))
        except ModuleNotFoundError as e:
            if e.name != "s%02d" % n:
                raise
            break
    return mods


def build():
    mods = load_stages()
    curriculum_stages, lesson_stages, questions = [], [], []
    qn = 0
    for m in mods:
        st = m.STAGE
        n = st["number"]
        sid = "S%02d" % n
        assert len(m.QUESTIONS) == 10, "stage %d has %d questions" % (n, len(m.QUESTIONS))
        plan = []
        for i, q in enumerate(m.QUESTIONS, 1):
            qn += 1
            q = dict(q)
            q["id"] = "PY-%03d" % qn
            q["course_id"] = COURSE["id"]
            q["language"] = COURSE["language"]
            q["stage_id"] = sid
            q["stage_number"] = n
            q["number_in_stage"] = i
            if q["preconditions"] == "このステージまでの内容のみ":
                scope = "ステージ1" if n == 1 else "ステージ1〜%d" % n
                q["preconditions"] = "%sで学習した内容のみを前提とする。import（ステージ9の random のみ例外）と標準入力(input)は使わない。" % scope
            if q["type"] == "code_write":
                q["prefix_code"] = q["grading"]["tests"][0].get("setup", "")
            # キー順を整える
            order = ["id", "course_id", "language", "stage_id", "stage_number", "number_in_stage", "title", "type", "answer_mode",
                     "difficulty", "concepts", "preconditions", "prompt", "code", "prefix_code", "starter_code", "choice_format", "choices",
                     "answer", "grading", "rationale", "explanation", "wrong_answer_reasons", "common_mistakes", "hint",
                     "feedback_correct", "feedback_incorrect"]
            q2 = {k: q[k] for k in order if k in q}
            for k in q:
                if k not in q2:
                    q2[k] = q[k]
            questions.append(q2)
            plan.append({
                "question_id": q["id"], "number_in_stage": i, "title": q["title"],
                "type": q["type"], "difficulty": q["difficulty"], "concepts": q["concepts"],
            })
        curriculum_stages.append({
            "id": sid, "number": n, "title": st["title"], "subtitle": st["subtitle"],
            "learning_goals": st["goals"], "prerequisite_knowledge": st["prerequisites"],
            "prerequisite_stage_ids": ["S%02d" % (n - 1)] if n > 1 else [],
            "topics": st["topics"], "common_pitfalls": st["pitfalls"],
            "lesson_id": "LESSON-" + sid, "question_plan": plan,
            "clear_condition": CLEAR_CONDITION, "leads_to": st["next_links"],
            "unlock_condition": None if n == 1 else {"type": "stage_cleared", "stage_id": "S%02d" % (n - 1)},
        })
        lesson_stages.append({
            "id": "LESSON-" + sid, "stage_id": sid, "title": st["title"],
            "intro": st["lesson"]["intro"], "sections": st["lesson"]["sections"],
            "common_mistakes": st["lesson"]["common_mistakes"],
            "checkpoints": st["lesson"]["checkpoints"],
            "next_bridge": st["lesson"]["next_bridge"],
        })
    curriculum = {"course": COURSE, "stages": curriculum_stages}
    lessons = {"course_id": COURSE["id"], "schema_version": COURSE["schema_version"], "lessons": lesson_stages}
    qdoc = {"course_id": COURSE["id"], "schema_version": COURSE["schema_version"], "question_count": len(questions), "questions": questions}
    return curriculum, lessons, qdoc


def write_all():
    c, l, q = build()
    for name, obj in [("curriculum.json", c), ("lessons.json", l), ("questions.json", q)]:
        with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return c, l, q


if __name__ == "__main__":
    c, l, q = write_all()
    print("stages:", len(c["stages"]), "questions:", q["question_count"])
