"""解説文・誤答理由・よくある間違いに書かれた「このコードは○○Errorになる」という主張を実行して確かめる。"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib import last_error_class, run_py  # noqa: E402

# (コード, 期待するエラー名 / None=エラーなしで実行できる)
CLAIMS = [
    ("print(こんにちは)", "NameError"),
    ('print "こんにちは"', "SyntaxError"),
    ('Print("Hello")', "NameError"),
    ("print(Hello')", "SyntaxError"),
    ("print('Hello\")", "SyntaxError"),
    ('print("Hello\')', "SyntaxError"),
    ("print(Hello)", "NameError"),
    ('print（"Hello"）', "SyntaxError"),
    ("2score = 1", "SyntaxError"),
    ("2nd = 10", "SyntaxError"),
    ("my score = 80", "SyntaxError"),
    ("x = 10\nif x = 10:\n    pass", "SyntaxError"),
    ("x = 10\nif x === 10:\n    pass", "SyntaxError"),
    ("age = 1\nif age => 18:\n    pass", "SyntaxError"),
    ("age = 1\nif (age = 18):\n    pass", "SyntaxError"),
    ("score = 1\nif score >= 60\n    print(1)", "SyntaxError"),
    ('score = 70\nif score >= 60:\nprint("合格")', "IndentationError"),
    ("count = 1\nfor count > 0:\n    pass", "SyntaxError"),
    ("for i in range(1, 6):\n    total += i", "NameError"),
    ("colors = ['a']\ncolors(0)", "TypeError"),
    ("nums = [1, 2, 3]\nnums(3)", "TypeError"),
    ("nums = [1, 2, 3]\nprint(nums[3])", "IndexError"),
    ("nums = [1, 2, 3]\nprint(nums[4])", "IndexError"),
    ("def add(a, b):\n    return a + b\nadd(3)", "TypeError"),
    ("def add(a, b):\n    return a + b\nadd[3, 4]", "TypeError"),
    ("def area(w, h):\n    print(w * h)\nx = area(3, 4) + 1", "TypeError"),
    ('print("合計は" + 10)', "TypeError"),
    ("age = 20\nprint('a' + age)", "TypeError"),
    ("age = 20\nprint('a' + int(age) + 'b')", "TypeError"),
    ("age = 20\nprint('a' - age)", "TypeError"),
    ("print(10 / 0)", "ZeroDivisionError"),
    ('int("abc")', "ValueError"),
    ('int("3.5")', "ValueError"),
    ('try:\n    n = int("abc")\nexcept ZeroDivisionError:\n    n = 0', "ValueError"),
    ("def safe(a, b):\n    try:\n        return a / b\n    except ValueError:\n        return 0\nsafe(1, 0)", "ZeroDivisionError"),
    ('stock = {"apple": 3}\nstock["grape"]', "KeyError"),
    ('stock = {"apple": 3}\nstock("grape")', "TypeError"),
    ('stock = {"apple": 3}\nstock["grape", 0]', "KeyError"),
    ('"I like Java".upper("Java", "Python")', "TypeError"),
    ('stock = {"apple": 3, "banana": 5}\nfor name, count in stock.values():\n    pass', "TypeError"),
    ('stock = {"apple": 3, "banana": 5}\nfor name, count in stock:\n    pass', "ValueError"),
    ("import random\nprint(random.randint(1, 3) in (1, 2, 3))", None),
    ("print(10 / 2)", None),
    ("print(type(10 / 2))", None),
    ("print(bool(0))", None),
]


def main():
    bad = 0
    out = []
    for code, expect in CLAIMS:
        so, se, rc, to = run_py(code, timeout=3)
        got = last_error_class(se) if rc != 0 else None
        ok = (got == expect) and not to
        out.append({"code": code, "expected": expect, "got": got, "ok": ok})
        if not ok:
            bad += 1
            print("[NG]", repr(code), "expected", expect, "got", got)
    with open(os.path.join(HERE, "claims_results.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("claims checked:", len(CLAIMS), "failures:", bad)
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
