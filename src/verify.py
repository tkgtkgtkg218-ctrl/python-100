"""全教材データの機械検証。コードを実際に実行して、正解・誤答・例題の整合性を確認する。

使い方: python src/verify.py   （結果は src/verify_results.json にも保存）
"""
import itertools
import json
import os
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build  # noqa: E402
from lib import grade, last_error_class, norm_output, run_tests, run_py  # noqa: E402

TIMEOUT = 3.0
REQUIRED = ["id", "stage_id", "stage_number", "number_in_stage", "title", "type", "answer_mode", "difficulty",
            "concepts", "preconditions", "prompt", "answer", "grading", "rationale", "explanation",
            "hint", "feedback_correct", "feedback_incorrect"]
TYPES = {"multiple_choice", "fill_blank", "predict_output", "bug_fix", "code_write"}


def run(code):
    return run_py(code, timeout=TIMEOUT)


def result_matches(code, expected_out=None, expected_err=None):
    out, err, rc, to = run(code)
    if expected_err == "Timeout":
        return to, "timeout" if to else "no-timeout(rc=%s)" % rc
    if expected_err:
        cls = last_error_class(err)
        return (rc != 0 and cls == expected_err), "err=%s" % cls
    return (rc == 0 and not to and norm_output(out) == norm_output(expected_out)), "out=%r err=%r" % (out, err[-80:])


def differs(code, expected_out):
    """コードの結果が expected_out と異なる（エラー・タイムアウト含む）ことを確認"""
    out, err, rc, to = run(code)
    return to or rc != 0 or norm_output(out) != norm_output(expected_out)


def structure_issues(q):
    issues = []
    for k in REQUIRED:
        if k not in q or q[k] in (None, "", []):
            issues.append("missing:" + k)
    if q["type"] not in TYPES:
        issues.append("bad type")
    if not (1 <= q["difficulty"] <= 5):
        issues.append("difficulty range")
    if q["answer_mode"] == "choice":
        ch = q.get("choices") or []
        ids = [c["id"] for c in ch]
        if len(ch) != 3:
            issues.append("choices != 3")
        if len(set(ids)) != len(ids):
            issues.append("dup choice id")
        if len({c["text"] for c in ch}) != len(ch):
            issues.append("dup choice text")
        cid = q["answer"].get("correct_choice_id")
        if cid not in ids:
            issues.append("correct id not in choices")
        wr = q.get("wrong_answer_reasons", {})
        if set(wr) != set(ids) - {cid}:
            issues.append("wrong reasons mismatch")
        if any(not v.strip() for v in wr.values()):
            issues.append("empty wrong reason")
    else:
        if q["type"] in ("predict_output", "fill_blank", "bug_fix") and not q.get("common_mistakes"):
            issues.append("no common_mistakes")
    for c in [q.get("code") or "", q.get("starter_code") or ""]:
        if re.search(r"\binput\s*\(", c):
            issues.append("uses input()")
    if q["type"] == "code_write":
        tests = q["grading"]["tests"]
        # 入力(setup)で結果が変わる問題は、ハードコード対策に隠しテストを3件以上要求する。固定出力の問題は対象外。
        if any(t.get("setup") for t in tests):
            if not any(not t["visible"] for t in tests):
                issues.append("no hidden tests")
            if len(tests) < 3:
                issues.append("fewer than 3 tests")
    return issues


def exec_checks(q):
    """実行による検証。[(name, ok, detail)] を返す"""
    res = []
    a = q["answer"]
    t = q["type"]

    if t == "predict_output":
        exp = a["expected_output"]
        ok, d = result_matches(q["code"], exp)
        res.append(("run_code_matches_expected_output", ok, d))
        if q["answer_mode"] == "choice":
            actual = run(q["code"])[0]
            for c in q["choices"]:
                if c["id"] != a["correct_choice_id"]:
                    res.append(("distractor_not_equal_actual:" + c["id"], norm_output(c["text"]) != norm_output(actual), c["text"]))
        else:
            actual = run(q["code"])[0]
            for m in q["common_mistakes"]:
                res.append(("wrong_answer_not_equal_actual", norm_output(m["answer"]) != norm_output(actual), m["answer"]))
            res.append(("grader_accepts_correct", grade(q, exp), ""))
            res.append(("grader_accepts_crlf_and_trailing_space", grade(q, exp.replace("\n", " \r\n") + "\n"), ""))
            for m in q["common_mistakes"]:
                res.append(("grader_rejects_wrong", not grade(q, m["answer"]), m["answer"]))

    elif t == "fill_blank":
        blanks = a["blanks"]
        combos = list(itertools.product(*[b["accepted"] for b in blanks]))[:200]
        for combo in combos:
            code = q["code"]
            for b, ans in zip(blanks, combo):
                code = code.replace(b["marker"], ans)
            ok, d = result_matches(code, a["expected_output"])
            res.append(("accepted_answer_runs_to_expected", ok, str(combo) + " " + d))
        first = {b["id"]: b["accepted"][0] for b in blanks}
        res.append(("grader_accepts_correct", grade(q, first), ""))
        for m in q["common_mistakes"]:
            ans = dict(first)
            ans[m["blank"]] = m["answer"]
            code = q["code"]
            for b in blanks:
                code = code.replace(b["marker"], ans[b["id"]])
            res.append(("wrong_pattern_really_wrong", differs(code, a["expected_output"]), m["answer"]))
            res.append(("grader_rejects_wrong", not grade(q, ans), m["answer"]))

    elif t == "bug_fix":
        buggy = q["code"]
        if "buggy_error" in a:
            ok, d = result_matches(buggy, None, a["buggy_error"])
            res.append(("buggy_code_raises:" + a["buggy_error"], ok, d))
        else:
            ok, d = result_matches(buggy, a["buggy_output"])
            res.append(("buggy_code_output_as_documented", ok, d))
            res.append(("buggy_output_differs_from_fixed", norm_output(a["buggy_output"]) != norm_output(a["expected_output"]), ""))
        ok, d = result_matches(a["fixed_code"], a["expected_output"])
        res.append(("fixed_code_runs_to_expected", ok, d))
        lines = buggy.split("\n")
        tl = a.get("target_line")
        if q["answer_mode"] == "text":
            def apply(repl):
                new = list(lines)
                indent = re.match(r"\s*", new[tl - 1]).group(0)
                new[tl - 1] = indent + repl.strip()
                return "\n".join(new)
            for acc in a["accepted"]:
                ok, d = result_matches(apply(acc), a["expected_output"])
                res.append(("accepted_fix_runs_to_expected", ok, acc + " " + d))
            for m in q["common_mistakes"]:
                res.append(("wrong_fix_really_wrong", differs(apply(m["answer"]), a["expected_output"]), m["answer"]))
                res.append(("grader_rejects_wrong", not grade(q, m["answer"]), m["answer"]))
            res.append(("grader_accepts_correct", grade(q, a["accepted"][0]), ""))
        elif tl:
            # 選択肢が「その行の置き換え」である場合
            for c in q["choices"]:
                new = list(lines)
                new[tl - 1] = c["text"]
                correct = c["id"] == a["correct_choice_id"]
                code = "\n".join(new)
                if correct:
                    ok, d = result_matches(code, a["expected_output"])
                    res.append(("correct_choice_fix_runs_to_expected", ok, d))
                else:
                    res.append(("wrong_choice_really_wrong", differs(code, a["expected_output"]), c["text"]))

    elif t == "code_write":
        g = q["grading"]
        starter_ok, _ = run_tests(q, q["starter_code"])
        res.append(("starter_code_does_not_pass", not starter_ok, ""))
        ok, det = run_tests(q, a["reference_solution"])
        res.append(("reference_solution_passes_all_tests", ok, str(det)))
        for i, alt in enumerate(a["alternative_solutions"]):
            ok, det = run_tests(q, alt)
            res.append(("alternative_solution_passes:%d" % i, ok, str(det)))
        for i, bad in enumerate(a["rejected_examples"]):
            ok, det = run_tests(q, bad["code"])
            res.append(("rejected_example_fails:%d" % i, not ok, str(det)))
        res.append(("grader_accepts_reference", grade(q, a["reference_solution"]), ""))
    elif t == "multiple_choice":
        res.append(("grader_accepts_correct", grade(q, a["correct_choice_id"]), ""))
        for c in q["choices"]:
            if c["id"] != a["correct_choice_id"]:
                res.append(("grader_rejects_wrong", not grade(q, c["id"]), c["id"]))
    return res


def check_examples(lessons):
    res = []
    for les in lessons["lessons"]:
        for sec in les["sections"]:
            for ex in sec["examples"]:
                if ex.get("expected_error"):
                    ok, d = result_matches(ex["code"], None, ex["expected_error"])
                else:
                    ok, d = result_matches(ex["code"], ex["expected_output"])
                res.append({"id": ex["id"], "ok": ok, "detail": d})
    return res


def main():
    curriculum, lessons, qdoc = build.write_all()
    questions = qdoc["questions"]
    out = {"questions": [], "examples": [], "global": []}

    def work(q):
        issues = structure_issues(q)
        ex = exec_checks(q)
        return q, issues, ex

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(work, questions))
    n_checks = 0
    n_fail = 0
    for q, issues, ex in results:
        fails = [(n, d) for n, ok, d in ex if not ok]
        n_checks += len(ex)
        n_fail += len(fails) + len(issues)
        out["questions"].append({"id": q["id"], "type": q["type"], "mode": q["answer_mode"], "issues": issues,
                                 "exec_checks": len(ex), "exec_failures": fails})
        if issues or fails:
            print("[NG]", q["id"], q["title"], issues, fails)
    out["examples"] = check_examples(lessons)
    for e in out["examples"]:
        if not e["ok"]:
            print("[NG example]", e)
            n_fail += 1

    # グローバル整合性
    glob = []
    ids = [q["id"] for q in questions]
    glob.append(("question ids unique", len(set(ids)) == len(ids)))
    glob.append(("question ids sequential", ids == ["PY-%03d" % i for i in range(1, len(ids) + 1)]))
    for st in curriculum["stages"]:
        glob.append(("plan matches questions " + st["id"], [p["question_id"] for p in st["question_plan"]] == [q["id"] for q in questions if q["stage_id"] == st["id"]]))
    lesson_ids = {l["stage_id"] for l in lessons["lessons"]}
    glob.append(("every stage has lesson", {s["id"] for s in curriculum["stages"]} == lesson_ids))
    titles = [q["title"] for q in questions]
    glob.append(("question titles unique", len(set(titles)) == len(titles)))
    prompts = [q["prompt"] + (q.get("code") or "") for q in questions]
    glob.append(("prompt+code unique", len(set(prompts)) == len(prompts)))
    for n, ok in glob:
        if not ok:
            print("[NG global]", n)
            n_fail += 1
    out["global"] = glob

    # 統計
    stats = {
        "questions": len(questions),
        "type_counts": dict(Counter(q["type"] for q in questions)),
        "mode_counts": dict(Counter(q["answer_mode"] for q in questions)),
        "difficulty_by_stage": {s["id"]: round(sum(q["difficulty"] for q in questions if q["stage_id"] == s["id"]) / 10, 1) for s in curriculum["stages"]},
        "correct_position": dict(Counter(
            [i for q in questions if q["answer_mode"] == "choice" for i, c in enumerate(q["choices"]) if c["id"] == q["answer"]["correct_choice_id"]])),
        "exec_checks_total": n_checks,
        "example_runs": len(out["examples"]),
        "failures": n_fail,
        "type_by_stage": {s["id"]: dict(Counter(q["type"] for q in questions if q["stage_id"] == s["id"])) for s in curriculum["stages"]},
    }
    out["stats"] = stats
    with open(os.path.join(HERE, "verify_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    print("FAILURES:", n_fail)
    return n_fail


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
