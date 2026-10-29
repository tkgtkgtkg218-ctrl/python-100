"""JavaScript 採点器(app/grader.js)と Python 参照実装(lib.grade)が同じ判定をするかを、
正解・誤答・表記ゆれ（全角/空白/改行/引用符/大文字小文字）の入力で照合する。"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from lib import grade  # noqa: E402

FULL = {chr(c): chr(c + 0xFEE0) for c in range(0x21, 0x7F)}


def to_full(s):
    return "".join(FULL.get(ch, ch) for ch in s)


def variants(s):
    out = [s, s + "  ", "  " + s, s + "\n", s.replace("\n", "\r\n"), s.replace("\n", " \n"), to_full(s), s.upper(), s.lower(),
           s.replace("\"", "'"), s.replace("'", "\""), s.replace(" ", ""), s.replace(" ", "  "), "", " ", s + "x", s[:-1] if s else s,
           "　" + s + "　"]
    return list(dict.fromkeys(out))


def main():
    qs = json.load(open(os.path.join(ROOT, "questions.json"), encoding="utf-8"))["questions"]
    cases = []
    for q in qs:
        m = q["grading"]["method"]
        if m == "test_cases":
            continue
        a = q["answer"]
        if m == "choice_id":
            for c in q["choices"]:
                cases.append((q["id"], c["id"]))
            cases.append((q["id"], "zzz"))
        elif m == "output_compare":
            for v in variants(a["expected_output"]):
                cases.append((q["id"], v))
            for mm in q["common_mistakes"]:
                cases.append((q["id"], mm["answer"]))
        elif m == "accepted_answers" and q["type"] == "fill_blank":
            base = {b["id"]: b["accepted"][0] for b in a["blanks"]}
            cases.append((q["id"], base))
            for b in a["blanks"]:
                for acc in b["accepted"]:
                    for v in variants(acc):
                        d = dict(base)
                        d[b["id"]] = v
                        cases.append((q["id"], d))
            for mm in q["common_mistakes"]:
                d = dict(base)
                d[mm["blank"]] = mm["answer"]
                cases.append((q["id"], d))
        elif m == "accepted_answers":
            for acc in a["accepted"]:
                for v in variants(acc):
                    cases.append((q["id"], v))
            for mm in q["common_mistakes"]:
                cases.append((q["id"], mm["answer"]))
    byid = {q["id"]: q for q in qs}
    payload = [{"id": i, "answer": ans, "expected": bool(grade(byid[i], ans))} for i, ans in cases]
    path = os.path.join(ROOT, "app", "parity_cases.json")
    json.dump(payload, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    r = subprocess.run(["node", os.path.join(ROOT, "app", "parity_run.js")], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr)
    print("cases:", len(payload), "expected-true:", sum(p["expected"] for p in payload))
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
