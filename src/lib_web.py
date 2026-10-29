"""JavaScript / HTML・CSS コース用の問題ビルダー（lib.py のビルダーを拡張）。

追加の考え方
- check: 「このコードを表示・実行したとき、こうなるはず」を機械で確かめるための指定。ブラウザで実行検証される。
    {"format": "html_document"|"html_body"|"css"|"javascript_dom", "given_html": "...",
     "expr": 正しい成果物でだけ true になる JavaScript の式,
     "probe": 表示結果を値として取り出す式（予測問題用）, "choice_values": {選択肢ID: 値}, "actions": [...], "viewport": 幅(px)}
- JavaScript の console.log だけで確かめられる問題は check 不要（expected_output を実行して比較する）。
- コード作成は engine を2種類持つ: js_worker（Worker で実行し console.log や関数の戻り値を比較）/ page（iframe に読み込み、式で判定）
"""
import lib
from lib import CHOICE_IDS


def _extra(q, k):
    q["code_language"] = k.get("lang")
    ck = k.get("check")
    if ck:
        q["check"] = ck
        if ck.get("given_html"):
            q["context_html"] = ck["given_html"]
    return q


def mc(**k):
    return _extra(lib.mc(**k), k)


def pred(**k):
    ck = k.get("check")
    if ck and "choices" in k:
        vals = {CHOICE_IDS[i]: c[2] for i, c in enumerate(k["choices"])}
        k = dict(k, check=dict(ck, choice_values=vals))
        q = lib.pred(**k)
        q["answer"].pop("expected_output", None)  # 選択肢の文章は表示結果の説明であり、出力そのものではない
        return _extra(q, k)
    return _extra(lib.pred(**k), k)


def fill(**k):
    ck = k.get("check")
    if ck:
        k = dict(k, out="")
    q = lib.fill(**k)
    if ck:
        q["answer"].pop("expected_output", None)
    return _extra(q, k)


def bugfix(**k):
    ck = k.get("check")
    if ck:
        k = dict(k, out="", buggy_out="")
    q = lib.bugfix(**k)
    if ck:
        q["answer"].pop("expected_output", None)
        q["answer"].pop("buggy_output", None)
    return _extra(q, k)


# ---------------------------------------------------------------- コード作成
def t_js_out(expected, setup="", visible=True):
    return {"kind": "stdout", "setup": setup, "expected_stdout": expected, "visible": visible}


def t_js_call(call, expected_json, setup="", visible=True):
    """call: 評価する式 / expected_json: 期待値を表す JSON 文字列（例 '5', '"abc"', '[1,2]', 'true'）"""
    return {"kind": "call", "setup": setup, "call": call, "expected": expected_json, "visible": visible}


def t_page(desc, expr, visible=True, actions=None, given_html=None, viewport=None):
    """ページに対する判定。expr は true を返す式。actions は expr の前に実行する式（数値は待ち時間ms）。
    given_html を指定すると、このテストだけ提示 HTML を差し替える（別の入力でも動くかの確認）。viewport は画面幅(px)"""
    t = {"kind": "page", "desc": desc, "expr": expr, "visible": visible}
    if actions:
        t["actions"] = actions
    if given_html is not None:
        t["given_html"] = given_html
    if viewport:
        t["viewport"] = viewport
    return t


def _write_common(k, fmt):
    q = lib._base("code_write", "code", k)
    q["starter_code"] = k.get("starter", "")
    q["answer_format"] = fmt
    q["answer"] = {
        "reference_solution": k["ref"],
        "alternative_solutions": k.get("alts", []),
        "rejected_examples": [{"code": c, "reason": r} for c, r in k["bads"]],
    }
    q["code_language"] = k.get("lang")
    return q


def _patterns(items):
    return [{"pattern": p, "message": m} for p, m in items]


def write_js(**k):
    """JavaScript（Worker で実行）。req/req_any/forbid は (正規表現, 不合格時のメッセージ) のリスト"""
    q = _write_common(k, "javascript")
    q["grading"] = {
        "method": "test_cases", "engine": "js_worker", "tests": k["tests"],
        "required_patterns": _patterns(k.get("req", [])),
        "required_any_patterns": _patterns(k.get("req_any", [])),
        "forbidden_patterns": _patterns(k.get("forbid", [])),
        "timeout_sec": 3, "normalize_stdout": ["crlf_to_lf", "rstrip_each_line", "strip_trailing_blank_lines"],
    }
    return q


def write_page(**k):
    """HTML/CSS/DOM操作（iframe に読み込んで式で判定）。fmt: html_document|html_body|css|javascript_dom。given_html: 提示済みの HTML"""
    q = _write_common(k, k["fmt"])
    if k.get("given_html"):
        q["prefix_html"] = k["given_html"]
    q["grading"] = {
        "method": "test_cases", "engine": "page", "tests": k["tests"],
        "required_patterns": _patterns(k.get("req", [])),
        "required_any_patterns": _patterns(k.get("req_any", [])),
        "forbidden_patterns": _patterns(k.get("forbid", [])),
        "timeout_sec": 4,
    }
    if k.get("viewport"):
        q["grading"]["viewport"] = k["viewport"]
    return q
