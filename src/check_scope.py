"""各ステージのコードに、そのステージで未学習の構文・関数が含まれていないかをAST解析で確認する。"""
import ast
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NODE_STAGE = {
    "Assign": 2, "AugAssign": 2, "BinOp": 2, "JoinedStr": 2,
    "If": 3, "Compare": 3, "BoolOp": 3,
    "For": 4, "While": 4, "Break": 4, "Continue": 4,
    "List": 5, "Subscript": 5, "Slice": 5,
    "FunctionDef": 6, "Return": 6,
    "Try": 7, "ExceptHandler": 7,
    "Dict": 8, "Import": 9,
}
CALL_STAGE = {
    "print": 1, "type": 2, "range": 4, "len": 5, "sum": 5, "max": 5, "min": 5,
    "int": 7, "float": 7, "str": 7,
}
ATTR_STAGE = {"append": 5, "strip": 8, "upper": 8, "lower": 8, "replace": 8, "split": 8, "join": 8, "count": 8,
              "get": 8, "items": 8, "keys": 8, "values": 8, "randint": 9}
# 学習範囲外でも、採点用テスト式にだけ現れるもの・別解にだけ現れるものは除外対象
ALLOWED_EXTRA = {"sorted", "repr", "list", "bool"}


def scan(code, stage):
    issues = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return issues  # 誤りを含むコードは対象外
    nested = False
    for node in ast.walk(tree):
        n = type(node).__name__
        if n in NODE_STAGE and NODE_STAGE[n] > stage:
            issues.append("%s (ステージ%dで学習)" % (n, NODE_STAGE[n]))
        if n == "Call":
            f = node.func
            if isinstance(f, ast.Name) and f.id in CALL_STAGE and CALL_STAGE[f.id] > stage:
                issues.append("%s() (ステージ%d)" % (f.id, CALL_STAGE[f.id]))
            if isinstance(f, ast.Name) and f.id not in CALL_STAGE and f.id not in ALLOWED_EXTRA:
                pass  # ユーザー定義関数
            if isinstance(f, ast.Attribute) and f.attr in ATTR_STAGE and ATTR_STAGE[f.attr] > stage:
                issues.append(".%s() (ステージ%d)" % (f.attr, ATTR_STAGE[f.attr]))
        if n == "For":
            for sub in ast.walk(node):
                if sub is not node and isinstance(sub, (ast.For, ast.While)) and stage < 10:
                    issues.append("入れ子ループ (ステージ10で学習)")
        if n == "Slice" and node.step is not None:
            issues.append("拡張スライス [::step] (範囲外。別解のみ許可)")
    return sorted(set(issues))


def main():
    q = json.load(open(os.path.join(ROOT, "questions.json"), encoding="utf-8"))["questions"]
    l = json.load(open(os.path.join(ROOT, "lessons.json"), encoding="utf-8"))["lessons"]
    found = []
    for x in q:
        st = x["stage_number"]
        codes = []
        if x.get("code"):
            code = x["code"]
            code = re.sub(r"__\d+__", "0", code) if x["type"] == "fill_blank" else code
            codes.append(("code", code))
        a = x["answer"]
        if "fixed_code" in a:
            codes.append(("fixed", a["fixed_code"]))
        if x["type"] == "code_write":
            codes.append(("ref", a["reference_solution"]))
            for i, alt in enumerate(a["alternative_solutions"]):
                codes.append(("alt%d" % i, alt))
        if x["type"] == "fill_blank":
            for b in a["blanks"]:
                pass
        for kind, c in codes:
            for iss in scan(c, st):
                found.append((x["id"], kind, iss))
    for les in l:
        st = int(les["stage_id"][1:])
        for sec in les["sections"]:
            for ex in sec["examples"]:
                for iss in scan(ex["code"], st):
                    found.append((ex["id"], "lesson-example", iss))
    for f in found:
        print(f)
    print("scope findings:", len(found))


if __name__ == "__main__":
    main()
