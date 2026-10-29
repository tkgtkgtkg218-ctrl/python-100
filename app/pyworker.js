/* 学習者のコードを実行する Web Worker（Pyodide）。
 * 主スレッド（画面）とは隔離され、DOM・localStorage には触れない。
 * 時間制限は主スレッド側のタイマー＋ Worker の terminate() で行う（pyrunner.js）。 */
let pyodide = null;
const OUTPUT_LIMIT = 64 * 1024; // 標準出力の上限（文字数）

const HELPER = `
import ast, json, sys, builtins, traceback

_ALLOWED_IMPORTS = {"random"}
_real_import = builtins.__import__

def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name.split(".")[0] not in _ALLOWED_IMPORTS:
        raise ImportError("この学習アプリでは " + name + " は使えません")
    return _real_import(name, globals, locals, fromlist, level)

def _make_ns():
    b = dict(vars(builtins))
    b["__import__"] = _safe_import
    for k in ("open", "input", "exec", "eval", "compile", "breakpoint", "exit", "quit", "help", "memoryview"):
        b.pop(k, None)
    return {"__name__": "__main__", "__builtins__": b}

def static_check(job_json):
    j = json.loads(job_json)
    try:
        tree = ast.parse(j["student"])
    except SyntaxError as e:
        return json.dumps({"ok": False, "message": "構文エラー（%s行目）: %s" % (e.lineno, e.msg)})
    present = {type(n).__name__ for n in ast.walk(tree)}
    missing = [r for r in j["required"] if r not in present]
    if missing:
        return json.dumps({"ok": False, "message": "この問題で使う必要がある書き方が含まれていません: " + ", ".join(missing)})
    if j["any"] and not any(r in present for r in j["any"]):
        return json.dumps({"ok": False, "message": "次のいずれかを使ってください: " + " / ".join(j["any"])})
    return json.dumps({"ok": True})

def _student_line(e, offset):
    tb = e.__traceback__
    line = None
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == "<student>":
            line = tb.tb_lineno - offset
        tb = tb.tb_next
    return line

def run_test(job_json):
    j = json.loads(job_json)
    offset = j["setup"].count("\\n") + 1
    ns = _make_ns()
    try:
        code = compile(j["setup"] + "\\n" + j["student"] + "\\n", "<student>", "exec")
        exec(code, ns)
        if j["kind"] == "call":
            r = eval(compile(j["call"], "<call>", "eval"), ns)
            actual = repr(r)
            ok = actual == repr(ast.literal_eval(j["expected"]))
            return json.dumps({"ok": ok, "actual": actual})
        return json.dumps({"ok": True})
    except SyntaxError as e:
        ln = (e.lineno - offset) if e.lineno else None
        return json.dumps({"ok": False, "error": "SyntaxError: %s%s" % (e.msg, "（%s行目）" % ln if ln and ln > 0 else "")})
    except BaseException as e:
        ln = _student_line(e, offset)
        return json.dumps({"ok": False, "error": "%s: %s%s" % (type(e).__name__, e, "（%s行目）" % ln if ln and ln > 0 else "")})
    finally:
        sys.stdout.flush()
`;

function lockDown() {
  // 学習者コードが js モジュール経由で外部通信できないようにする（core のみ使用するため、初期化後は不要）
  for (const name of ["fetch", "XMLHttpRequest", "WebSocket", "EventSource", "importScripts", "indexedDB", "caches"]) {
    try { Object.defineProperty(self, name, { value: undefined, configurable: false, writable: false }); } catch (e) { /* 無視 */ }
  }
}

self.onmessage = async (ev) => {
  const m = ev.data;
  if (m.type === "init") {
    try {
      importScripts(m.url + "pyodide.js");
      pyodide = await self.loadPyodide({ indexURL: m.url });
      pyodide.runPython(HELPER);
      const py = pyodide.runPython("import sys; sys.version.split()[0]");
      lockDown();
      self.postMessage({ type: "ready", python: py, pyodide: pyodide.version });
    } catch (e) {
      self.postMessage({ type: "initerror", message: String((e && e.message) || e) });
    }
    return;
  }
  if (m.type === "run") {
    let out = "";
    let truncated = false;
    // 前回の実行で出力の途中で打ち切られた場合に、残りの出力が今回に混ざらないよう捨てる
    pyodide.setStdout({ batched: () => {} });
    try { pyodide.runPython("import sys; sys.stdout.flush()"); } catch (e) { /* 無視 */ }
    pyodide.setStdout({
      batched: (s) => {
        if (out.length + s.length + 1 > OUTPUT_LIMIT) { truncated = true; throw new Error("出力が長すぎます（上限 64KB）"); }
        out += s + "\n";
      },
    });
    pyodide.setStderr({ batched: () => {} });
    let res;
    try {
      const fn = pyodide.globals.get(m.op === "static" ? "static_check" : "run_test");
      try { res = JSON.parse(fn(JSON.stringify(m.job))); } finally { fn.destroy(); }
    } catch (e) {
      res = { ok: false, error: String((e && e.message) || e) };
    }
    self.postMessage({ type: "result", id: m.id, res, out, truncated });
  }
};
