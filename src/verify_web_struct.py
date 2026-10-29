"""JavaScript / HTML・CSS コースのデータ構造チェック（コードの実行を伴わない部分）。
  python src/verify_web_struct.py
実行を伴う検証は  node src/web_verify_run.js courses/<コースID>  を使う。"""
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
COURSES = ["javascript-basics-ja", "htmlcss-basics-ja"]
REQUIRED = ["id", "stage_id", "stage_number", "number_in_stage", "title", "type", "answer_mode", "difficulty", "concepts", "preconditions",
            "prompt", "answer", "grading", "rationale", "explanation", "hint", "feedback_correct", "feedback_incorrect", "code_language"]
TYPES = {"multiple_choice", "fill_blank", "predict_output", "bug_fix", "code_write"}


def issues_for(q):
    out = []
    for k in REQUIRED:
        if k not in q or q[k] in (None, "", []):
            out.append("missing:" + k)
    if q.get("type") not in TYPES:
        out.append("bad type")
    if not (1 <= q.get("difficulty", 0) <= 5):
        out.append("difficulty")
    a = q.get("answer", {})
    if q.get("answer_mode") == "choice":
        ch = q.get("choices") or []
        ids = [c["id"] for c in ch]
        if len(ch) != 3 or len(set(ids)) != 3 or len({c["text"] for c in ch}) != 3:
            out.append("choices must be 3 distinct")
        if a.get("correct_choice_id") not in ids:
            out.append("correct id missing")
        wr = q.get("wrong_answer_reasons", {})
        if set(wr) != set(ids) - {a.get("correct_choice_id")} or any(not v.strip() for v in wr.values()):
            out.append("wrong reasons mismatch")
        ck = q.get("check")
        if q["type"] == "predict_output" and ck and ck.get("probe"):
            vals = ck.get("choice_values", {})
            if set(vals) != set(ids):
                out.append("choice_values mismatch")
            if len({json.dumps(v, ensure_ascii=False) for v in vals.values()}) != 3:
                out.append("choice_values not distinct")
    elif q.get("type") in ("predict_output", "fill_blank", "bug_fix") and not q.get("common_mistakes"):
        out.append("no common_mistakes")
    if q.get("type") == "fill_blank":
        for b in a["blanks"]:
            if b["marker"] not in q["code"]:
                out.append("marker not in code " + b["marker"])
    if q.get("type") == "code_write":
        g = q["grading"]
        if not a.get("alternative_solutions"):
            out.append("no alternative solution")
        if len(a.get("rejected_examples", [])) < 2:
            out.append("fewer than 2 rejected examples")
        tests = g["tests"]
        if len(tests) < 3 and g["engine"] == "js_worker" and any(t.get("setup") for t in tests):
            out.append("fewer than 3 tests")
        if g["engine"] == "js_worker" and any(t.get("setup") for t in tests) and not any(not t["visible"] for t in tests):
            out.append("no hidden tests")
    return out


def main():
    bad = 0
    for cid in COURSES:
        d = os.path.join(ROOT, "courses", cid)
        cur = json.load(open(os.path.join(d, "curriculum.json"), encoding="utf-8"))
        les = json.load(open(os.path.join(d, "lessons.json"), encoding="utf-8"))
        qs = json.load(open(os.path.join(d, "questions.json"), encoding="utf-8"))["questions"]
        problems = []
        for q in qs:
            for i in issues_for(q):
                problems.append((q["id"], i))
        ids = [q["id"] for q in qs]
        pre = cur["course"]["id"].split("-")[0]
        glob = {
            "100 questions": len(qs) == 100,
            "ids unique": len(set(ids)) == 100,
            "titles unique": len({q["title"] for q in qs}) == 100,
            "prompt+code unique": len({q["prompt"] + (q.get("code") or "") for q in qs}) == 100,
            "10 stages x 10": all(sum(1 for q in qs if q["stage_id"] == s["id"]) == 10 for s in cur["stages"]),
            "plan matches": all([p["question_id"] for p in s["question_plan"]] == [q["id"] for q in qs if q["stage_id"] == s["id"]] for s in cur["stages"]),
            "lesson per stage": {l["stage_id"] for l in les["lessons"]} == {s["id"] for s in cur["stages"]},
            "2 sections per lesson": all(len(l["sections"]) == 2 for l in les["lessons"]),
            "4 mistakes per lesson": all(len(l["common_mistakes"]) == 4 for l in les["lessons"]),
        }
        for k, v in glob.items():
            if not v:
                problems.append(("global", k))
        pos = Counter(i for q in qs if q["answer_mode"] == "choice" for i, c in enumerate(q["choices"]) if c["id"] == q["answer"]["correct_choice_id"])
        stats = {
            "types": dict(Counter(q["type"] for q in qs)),
            "modes": dict(Counter(q["answer_mode"] for q in qs)),
            "difficulty_avg": [round(sum(q["difficulty"] for q in qs if q["stage_id"] == s["id"]) / 10, 1) for s in cur["stages"]],
            "difficulty_dist": dict(sorted(Counter(q["difficulty"] for q in qs).items())),
            "correct_choice_position": dict(sorted(pos.items())),
            "code_write_per_stage": [sum(1 for q in qs if q["stage_id"] == s["id"] and q["type"] == "code_write") for s in cur["stages"]],
            "tests_total": sum(len(q["grading"]["tests"]) for q in qs if q["type"] == "code_write"),
            "tests_hidden": sum(1 for q in qs if q["type"] == "code_write" for t in q["grading"]["tests"] if not t["visible"]),
            "alternatives": sum(len(q["answer"]["alternative_solutions"]) for q in qs if q["type"] == "code_write"),
            "rejected_examples": sum(len(q["answer"]["rejected_examples"]) for q in qs if q["type"] == "code_write"),
        }
        print("==", cid, "problems:", len(problems))
        for p in problems[:30]:
            print("  [NG]", p)
        print(json.dumps(stats, ensure_ascii=False))
        bad += len(problems)
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
