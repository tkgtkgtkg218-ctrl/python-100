"""教材ビルド用の共通ライブラリ。

- 問題ビルダー（mc / pred / fill / bugfix / write）
- 参照実装の採点器（grade）  ※Webアプリ側(JS)で再実装する際の基準
- コード実行用の簡易サンドボックス（run_py）  ※検証専用。ローカルの教材検証にのみ使用する
"""
import ast
import os
import subprocess
import sys
import unicodedata

CHOICE_IDS = ["c1", "c2", "c3"]


# ---------------------------------------------------------------- 実行
def run_py(code, timeout=5.0, stdin=""):
    """別プロセスでPythonコードを実行する。(stdout, stderr, returncode, timed_out)を返す。"""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    try:
        p = subprocess.run(
            [sys.executable, "-I", "-X", "utf8", "-c", code],
            input=stdin, capture_output=True, text=True, encoding="utf-8",
            timeout=timeout, env=env,
        )
        return p.stdout, p.stderr, p.returncode, False
    except subprocess.TimeoutExpired as e:
        return (e.stdout or ""), (e.stderr or ""), -1, True


def last_error_class(stderr):
    lines = [l for l in stderr.strip().splitlines() if l.strip()]
    if not lines:
        return None
    return lines[-1].split(":")[0].strip()


# ---------------------------------------------------------------- 正規化
def norm_output(s):
    """出力比較用: 改行コードを統一し、各行の末尾空白と末尾の空行を除く。行頭・行内の空白は保持。"""
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = [l.rstrip() for l in s.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def norm_answer(s, quote_insensitive=False):
    """穴埋め比較用: 全角→半角(NFKC)、前後の空白除去。内部の空白は変更しない。"""
    s = unicodedata.normalize("NFKC", s).strip()
    if quote_insensitive:
        s = s.replace("'", '"')
    return s


# ---------------------------------------------------------------- 問題ビルダー
def _base(type_, mode, k):
    return {
        "type": type_,
        "answer_mode": mode,
        "title": k["title"],
        "difficulty": k["diff"],
        "concepts": k["concepts"],
        "preconditions": k.get("pre", "このステージまでの内容のみ"),
        "prompt": k["prompt"],
        "code": k.get("code"),
        "hint": k["hint"],
        "feedback_correct": k["ok"],
        "feedback_incorrect": k["ng"],
        "rationale": k["why"],
        "explanation": k["expl"],
    }


def _attach_choices(q, choices, correct, fmt):
    q["choice_format"] = fmt
    q["choices"] = [{"id": CHOICE_IDS[i], "text": c[0]} for i, c in enumerate(choices)]
    q["wrong_answer_reasons"] = {
        CHOICE_IDS[i]: c[1] for i, c in enumerate(choices) if i != correct
    }
    return CHOICE_IDS[correct]


def mc(**k):
    q = _base("multiple_choice", "choice", k)
    cid = _attach_choices(q, k["choices"], k["correct"], k.get("fmt", "text"))
    q["answer"] = {"correct_choice_id": cid}
    q["grading"] = {"method": "choice_id"}
    return q


def pred(**k):
    """実行結果の予測。choices があれば3択、なければ入力(output_compare)。"""
    if "choices" in k:
        q = _base("predict_output", "choice", k)
        cid = _attach_choices(q, k["choices"], k["correct"], "code")
        out = k["choices"][k["correct"]][0]
        q["answer"] = {"correct_choice_id": cid, "expected_output": out}
        q["grading"] = {"method": "choice_id"}
    else:
        q = _base("predict_output", "text", k)
        out = k["out"]
        q["answer"] = {"expected_output": out}
        q["common_mistakes"] = [{"answer": a, "reason": r} for a, r in k.get("wrong", [])]
        q["grading"] = {
            "method": "output_compare",
            "normalize": ["crlf_to_lf", "rstrip_each_line", "strip_trailing_blank_lines"],
            "case_sensitive": True,
        }
    return q


def fill(**k):
    """穴埋め。code 内の __1__, __2__ が空欄。blanks=[(accepted_list, quote_insensitive)]"""
    q = _base("fill_blank", "text", k)
    q["answer"] = {
        "blanks": [
            {"id": "b%d" % (i + 1), "marker": "__%d__" % (i + 1), "accepted": a, "quote_insensitive": qi}
            for i, (a, qi) in enumerate(k["blanks"])
        ],
        "expected_output": k["out"],
    }
    q["common_mistakes"] = [
        {"blank": b, "answer": a, "reason": r} for b, a, r in k.get("wrong", [])
    ]
    q["grading"] = {
        "method": "accepted_answers",
        "normalize": ["nfkc", "strip_outer_whitespace"],
        "keep_inner_whitespace": True,
    }
    return q


def bugfix(**k):
    """間違い探し。code=誤りを含むコード, fixed=修正後コード, out=修正後の出力。
    err=誤りコードのエラー名(実行時エラー/構文エラーの場合) または buggy_out=誤りコードの(誤った)出力。
    choice モード: choices/correct を指定。text モード: target_line(1始まり)と accepted(その行の置換候補)を指定。"""
    ans_extra = {"fixed_code": k["fixed"], "expected_output": k["out"]}
    if k.get("err"):
        ans_extra["buggy_error"] = k["err"]
    else:
        ans_extra["buggy_output"] = k["buggy_out"]
    if "choices" in k:
        q = _base("bug_fix", "choice", k)
        cid = _attach_choices(q, k["choices"], k["correct"], k.get("fmt", "code"))
        q["answer"] = dict(correct_choice_id=cid, **ans_extra)
        q["grading"] = {"method": "choice_id"}
        # 検証用: 選択肢が「修正行」の場合の置換行番号
        if "target_line" in k:
            q["answer"]["target_line"] = k["target_line"]
            q["answer"]["choice_is_replacement_line"] = True
    else:
        q = _base("bug_fix", "text", k)
        q["answer"] = dict(
            target_line=k["target_line"],
            accepted=k["accepted"],
            quote_insensitive=k.get("qi", False),
            **ans_extra,
        )
        q["common_mistakes"] = [{"answer": a, "reason": r} for a, r in k.get("wrong", [])]
        q["grading"] = {
            "method": "accepted_answers",
            "normalize": ["nfkc", "strip_outer_whitespace"],
            "keep_inner_whitespace": True,
            "scope": "target_line_replacement",
        }
    return q


def write(**k):
    """コード作成。tests=[dict], ref=模範解答, alts=別解(合格すべき), bads=不正解例(不合格であるべき)。"""
    q = _base("code_write", "code", k)
    q["starter_code"] = k.get("starter", "")
    q["answer"] = {
        "reference_solution": k["ref"],
        "alternative_solutions": k.get("alts", []),
        "rejected_examples": [{"code": c, "reason": r} for c, r in k["bads"]],
    }
    q["grading"] = {
        "method": "test_cases",
        "tests": k["tests"],
        "required_ast_nodes": k.get("req", []),
        "required_any_ast_nodes": k.get("req_any", []),
        "timeout_sec": 5,
        "execution": "sandboxed_worker",
        "normalize_stdout": ["crlf_to_lf", "rstrip_each_line", "strip_trailing_blank_lines"],
    }
    return q


def t_out(expected, setup="", visible=True):
    return {"kind": "stdout", "setup": setup, "expected_stdout": expected, "visible": visible}


def t_call(call, expected, setup="", visible=True):
    return {"kind": "call", "setup": setup, "call": call, "expected": expected, "visible": visible}


# ---------------------------------------------------------------- 採点（参照実装）
def build_test_program(test, student):
    if test["kind"] == "stdout":
        return test.get("setup", "") + "\n" + student + "\n"
    prog = (
        test.get("setup", "") + "\n" + student + "\n"
        "import ast as __ast\n"
        "__r = (" + test["call"] + ")\n"
        "print('__RESULT__' + str(repr(__r) == repr(__ast.literal_eval(" + repr(test["expected"]) + "))))\n"
    )
    return prog


def static_check(code, required_nodes, required_any=()):
    """required_nodes: すべて含むこと / required_any: そのうち1つ以上を含むこと"""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    present = {type(n).__name__ for n in ast.walk(tree)}
    if not all(r in present for r in required_nodes):
        return False
    return (not required_any) or any(r in present for r in required_any)


def run_tests(q, student):
    """test_cases 採点。(全合格か, 詳細リスト) を返す"""
    g = q["grading"]
    results = []
    if not static_check(student, g.get("required_ast_nodes", []), g.get("required_any_ast_nodes", [])):
        return False, [{"static_check": False}]
    for t in g["tests"]:
        out, err, rc, to = run_py(build_test_program(t, student), timeout=g.get("timeout_sec", 5))
        if t["kind"] == "stdout":
            ok = (not to) and rc == 0 and norm_output(out) == norm_output(t["expected_stdout"])
        else:
            ok = (not to) and rc == 0 and out.strip().splitlines()[-1:] == ["__RESULT__True"]
        results.append({"ok": ok, "timeout": to, "rc": rc})
    return all(r["ok"] for r in results), results


def grade(q, answer):
    """answer: choice=選択肢ID文字列 / fill=dict{b1:str} / text(pred,bugfix)=str / code=str"""
    m = q["grading"]["method"]
    a = q["answer"]
    if m == "choice_id":
        return answer == a["correct_choice_id"]
    if m == "output_compare":
        return norm_output(answer) == norm_output(a["expected_output"])
    if m == "accepted_answers":
        if q["type"] == "fill_blank":
            for b in a["blanks"]:
                given = norm_answer(answer.get(b["id"], ""), b["quote_insensitive"])
                ok = [norm_answer(x, b["quote_insensitive"]) for x in b["accepted"]]
                if given not in ok:
                    return False
            return True
        qi = a.get("quote_insensitive", False)
        given = norm_answer(answer, qi)
        return given in [norm_answer(x, qi) for x in a["accepted"]]
    if m == "test_cases":
        return run_tests(q, answer)[0]
    raise ValueError(m)
