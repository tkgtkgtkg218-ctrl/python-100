/* JavaScript / HTML / CSS コースの実行・採点基盤（ブラウザ内）。
 *  - runJs : JavaScript を Web Worker で実行（console.log を収集、時間切れは terminate）。DOM は使えない。
 *  - runPage : HTML/CSS/DOM操作を sandbox 付き iframe（allow-scripts のみ。親ページの localStorage や DOM には触れない）に読み込み、
 *              条件式（expr）を評価して結果を返す。テストごとに新しい iframe を使う。
 *  - grade : 問題の grading.tests を実行して合否を返す（engine: "js_worker" | "page"）。
 *  - preview : 学習者向けの表示用 iframe を作る（採点用の仕掛けなし）。 */
const WebRunner = (function () {
  const OUTPUT_LIMIT = 64 * 1024;
  const SCRIPT_END = "<" + "/script>";

  /* ---------------- JavaScript（Worker） ---------------- */
  const WORKER_SRC = `
  const LIMIT = ${OUTPUT_LIMIT};
  function q(s){ return "'" + s.replace(/\\\\/g, "\\\\\\\\").replace(/'/g, "\\\\'") + "'"; }
  function fmt(v, top, depth) {
    depth = depth || 0;
    if (typeof v === "string") return top ? v : q(v);
    if (typeof v === "number") return Object.is(v, -0) ? "-0" : String(v);
    if (typeof v === "bigint") return v + "n";
    if (v === null || v === undefined || typeof v === "boolean") return String(v);
    if (typeof v === "symbol") return v.toString();
    if (typeof v === "function") return "[Function" + (v.name ? ": " + v.name : " (anonymous)") + "]";
    if (Array.isArray(v)) {
      if (depth > 2) return "[Array]";
      return v.length ? "[ " + v.map(function (x) { return fmt(x, false, depth + 1); }).join(", ") + " ]" : "[]";
    }
    if (v instanceof Error) return v.name + ": " + v.message;
    if (typeof v === "object") {
      if (depth > 2) return "[Object]";
      var keys = Object.keys(v);
      if (!keys.length) return "{}";
      return "{ " + keys.map(function (k) { return (/^[A-Za-z_$][\\w$]*$/.test(k) ? k : q(k)) + ": " + fmt(v[k], false, depth + 1); }).join(", ") + " }";
    }
    return String(v);
  }
  self.onmessage = function (e) {
    var m = e.data, logs = [], size = 0, out = { logs: logs, error: null, value: null };
    ["fetch", "XMLHttpRequest", "WebSocket", "importScripts", "EventSource", "indexedDB", "caches"].forEach(function (n) {
      try { Object.defineProperty(self, n, { value: undefined, configurable: false, writable: false }); } catch (x) {}
    });
    function push() {
      var s = Array.prototype.map.call(arguments, function (a) { return fmt(a, true); }).join(" ");
      size += s.length + 1;
      if (size > LIMIT) throw new Error("出力が長すぎます（上限 64KB）");
      logs.push(s);
    }
    var con = { log: push, info: push, warn: push, error: push, debug: push };
    try {
      var body = (m.setup ? m.setup + "\\n" : "") + m.code + "\\n" + (m.call ? "return JSON.stringify((" + m.call + "));" : "");
      var fn = new Function("console", body);
      var v = fn(con);
      out.value = v === undefined ? null : v;
    } catch (err) {
      out.error = { name: (err && err.name) || "Error", message: String((err && err.message) || err) };
    }
    postMessage(out);
  };`;
  let workerUrl = null;

  function runJs(code, opts) {
    opts = opts || {};
    if (!workerUrl) workerUrl = URL.createObjectURL(new Blob([WORKER_SRC], { type: "text/javascript" }));
    return new Promise(function (resolve) {
      const w = new Worker(workerUrl);
      const timer = setTimeout(function () { w.terminate(); resolve({ timeout: true, logs: [], error: null, value: null }); }, opts.timeoutMs || 3000);
      w.onmessage = function (ev) { clearTimeout(timer); w.terminate(); resolve(Object.assign({ timeout: false }, ev.data)); };
      w.onerror = function (ev) { clearTimeout(timer); w.terminate(); resolve({ timeout: false, logs: [], error: { name: "Error", message: String(ev.message || "Worker error") }, value: null }); };
      w.postMessage({ code: code, setup: opts.setup || "", call: opts.call || "" });
    });
  }

  /* ---------------- ページ（iframe） ---------------- */
  const PRE = "<script>window.__errs=[];window.addEventListener('error',function(e){window.__errs.push(((e.error&&e.error.name)||'Error')+': '+e.message)});" + SCRIPT_END;

  // iframe の中で動く採点用コード（関数の中身が文字列化されて埋め込まれる）
  function harness(cfg) {
    var me = document.currentScript;
    if (me && me.parentNode) me.parentNode.removeChild(me);
    window.__errs = window.__errs || [];
    function ser(v) {
      if (v === undefined) return { t: "undefined" };
      if (v instanceof Element) return { t: "element", v: v.tagName };
      try { return { t: "json", v: JSON.parse(JSON.stringify(v)) }; } catch (e) { return { t: "string", v: String(v) }; }
    }
    function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
    async function go() {
      var values = [];
      try {
        var acts = cfg.actions || [];
        for (var i = 0; i < acts.length; i++) {
          if (typeof acts[i] === "number") await sleep(acts[i]);
          else (0, eval)(acts[i]);
        }
      } catch (e) {
        window.__errs.push("アクション実行エラー: " + ((e && e.name) || "Error") + ": " + (e && e.message));
      }
      for (var j = 0; j < cfg.exprs.length; j++) {
        try { values.push({ ok: true, r: ser((0, eval)(cfg.exprs[j])) }); }
        catch (e) { values.push({ ok: false, error: ((e && e.name) || "Error") + ": " + (e && e.message) }); }
      }
      parent.postMessage({ webrunner: true, id: cfg.id, errors: window.__errs || [], values: values }, "*");
    }
    function start() { setTimeout(function () { if (document.body) void document.body.offsetHeight; go(); }, 30); }
    if (document.readyState === "complete") start(); else window.addEventListener("load", start);
  }

  function assemble(spec, instrument, cfg) {
    const student = spec.student;
    const given = spec.given_html || "";
    const post = instrument ? "<script>(" + harness.toString() + ")(" + JSON.stringify(cfg).replace(/</g, "\\u003c") + ");" + SCRIPT_END : "";
    const pre = instrument ? PRE : "";
    const head = '<meta charset="utf-8"><title>page</title>';
    switch (spec.format) {
      case "html_document":
        return student + post;
      case "html_body":
        return "<!doctype html><html lang=\"ja\"><head>" + head + pre + "</head><body>" + student + post + "</body></html>";
      case "css":
        return "<!doctype html><html lang=\"ja\"><head>" + head + pre + "<style>" + student + "</style></head><body>" + given + post + "</body></html>";
      case "javascript_dom":
        return "<!doctype html><html lang=\"ja\"><head>" + head + pre + "</head><body>" + given + "<script>" + student + SCRIPT_END + post + "</body></html>";
      default:
        throw new Error("unknown format: " + spec.format);
    }
  }

  let seq = 0;
  const waiting = new Map();
  window.addEventListener("message", function (ev) {
    const d = ev.data;
    if (d && d.webrunner && waiting.has(d.id)) { const cb = waiting.get(d.id); waiting.delete(d.id); cb(d, ev.source); }
  });
  let holder = null;
  function getHolder() {
    if (!holder) {
      holder = document.createElement("div");
      holder.setAttribute("aria-hidden", "true");
      // 画面外に出すと、ブラウザが描画を省略して計測結果が不安定になるため、画面内に置いて透明にする
      holder.style.cssText = "position:fixed;left:0;top:0;width:0;height:0;opacity:0;pointer-events:none;z-index:-1";
      document.body.appendChild(holder);
    }
    return holder;
  }

  /** spec: {format, given_html, student, actions, viewport, exprs:[string], timeoutMs} → {timeout, errors, values} */
  function runPage(spec) {
    const id = "wr" + (++seq) + "_" + Math.random().toString(36).slice(2);
    const cfg = { id: id, actions: spec.actions || [], exprs: spec.exprs || [] };
    return new Promise(function (resolve) {
      const f = document.createElement("iframe");
      f.setAttribute("sandbox", "allow-scripts");
      f.style.cssText = "border:0;width:" + (spec.viewport || 800) + "px;height:600px";
      // srcdoc の文書は doctype がなくても標準モードになる仕様のため、blob URL で読み込む（互換モードの再現に必要）
      const blobUrl = URL.createObjectURL(new Blob([assemble(spec, true, cfg)], { type: "text/html;charset=utf-8" }));
      const done = function (r) { clearTimeout(timer); waiting.delete(id); URL.revokeObjectURL(blobUrl); if (f.parentNode) f.parentNode.removeChild(f); resolve(r); };
      const timer = setTimeout(function () { done({ timeout: true, errors: [], values: [] }); }, spec.timeoutMs || 4000);
      waiting.set(id, function (d) { done({ timeout: false, errors: d.errors, values: d.values }); });
      f.src = blobUrl;
      getHolder().appendChild(f);
    });
  }

  /** 値の比較用に、結果を JSON 文字列へ */
  function valueKey(v) { return v && v.ok ? JSON.stringify(v.r) : "ERR:" + (v && v.error); }
  const truthy = (v) => !!(v && v.ok && v.r && v.r.t === "json" && v.r.v === true);

  /* ---------------- 採点 ---------------- */
  function deepEqual(a, b) {
    if (a === b) return true;
    if (typeof a !== typeof b || a === null || b === null || typeof a !== "object") return false;
    if (Array.isArray(a) !== Array.isArray(b)) return false;
    const ka = Object.keys(a), kb = Object.keys(b);
    if (ka.length !== kb.length) return false;
    return ka.every((k) => Object.prototype.hasOwnProperty.call(b, k) && deepEqual(a[k], b[k]));
  }

  function staticCheck(g, code) {
    const must = g.required_patterns || [];
    for (const p of must) if (!new RegExp(p.pattern).test(code)) return p.message;
    const any = g.required_any_patterns || [];
    if (any.length && !any.some((p) => new RegExp(p.pattern).test(code))) return any.map((p) => p.message).join(" または ");
    const forbid = g.forbidden_patterns || [];
    for (const p of forbid) if (new RegExp(p.pattern).test(code)) return p.message;
    return null;
  }

  /** q: 問題, student: 学習者のコード。戻り値 {correct, staticMessage, results:[{t, ok, error, actual, timeout}]} */
  async function grade(q, student, onProgress) {
    const g = q.grading;
    const msg = staticCheck(g, student);
    if (msg) return { correct: false, staticMessage: msg, results: [] };
    // DOM操作（iframe 内でスクリプトを実行）では、あからさまな無限ループは実行前に止める
    // （Chrome では iframe が別プロセスで動くが、ほかのブラウザでは、画面全体が固まるおそれがあるため）
    if (q.answer_format === "javascript_dom" && /\bwhile\s*\(\s*(true|1)\s*\)|\bfor\s*\(\s*;\s*;\s*\)/.test(student)) {
      return { correct: false, staticMessage: "無限ループになる書き方（while (true) など）は、この採点では使えません。", results: [] };
    }
    const results = new Array(g.tests.length);
    if (g.engine === "js_worker") {
      for (let i = 0; i < g.tests.length; i++) {
        const t = g.tests[i];
        const r = await runJs(student, { setup: t.setup || "", call: t.kind === "call" ? t.call : "", timeoutMs: (g.timeout_sec || 3) * 1000 });
        const row = { t: t, ok: false, error: null, actual: null, timeout: !!r.timeout };
        if (r.timeout) row.error = "時間切れ（" + (g.timeout_sec || 3) + "秒）。無限ループになっていないか確認しましょう。";
        else if (r.error) row.error = r.error.name + ": " + r.error.message;
        else if (t.kind === "stdout") {
          row.actual = r.logs.join("\n");
          row.ok = Grader.normOutput(row.actual) === Grader.normOutput(t.expected_stdout);
        } else {
          let got = null;
          try { got = r.value === null ? undefined : JSON.parse(r.value); } catch (e) { got = r.value; }
          let exp; try { exp = JSON.parse(t.expected); } catch (e) { exp = t.expected; }
          row.actual = r.value === null ? "undefined" : r.value;
          row.ok = got !== undefined && deepEqual(got, exp);
        }
        results[i] = row;
        if (onProgress) onProgress(i + 1, g.tests.length);
        if (r.timeout) { for (let k = i + 1; k < g.tests.length; k++) results[k] = { t: g.tests[k], ok: false, skipped: true, error: "前のテストが時間切れだったため実行していません" }; break; }
      }
    } else {
      // page: アクションが同じテストは1つの iframe にまとめて評価する
      // （テストごとに given_html を差し替えて、別の入力でも動くかを確かめられる）
      const groups = new Map();
      g.tests.forEach((t, i) => { const key = JSON.stringify([t.actions || [], t.given_html == null ? null : t.given_html, t.viewport || null]); if (!groups.has(key)) groups.set(key, []); groups.get(key).push(i); });
      let done = 0;
      for (const [key, idxs] of groups) {
        const [acts, givenOverride, vp] = JSON.parse(key);
        const r = await runPage({ format: q.answer_format, given_html: givenOverride == null ? (q.prefix_html || "") : givenOverride, student: student, actions: acts, viewport: vp || g.viewport, exprs: idxs.map((i) => g.tests[i].expr), timeoutMs: (g.timeout_sec || 4) * 1000 });
        idxs.forEach((i, n) => {
          const row = { t: g.tests[i], ok: false, error: null, actual: null, timeout: !!r.timeout };
          if (r.timeout) row.error = "時間切れです。無限ループになっていないか確認しましょう。";
          else {
            const v = r.values[n];
            if (!v.ok) row.error = v.error;
            else row.ok = truthy(v);
            if (r.errors && r.errors.length) { row.pageErrors = r.errors; }
          }
          results[i] = row;
          done += 1;
          if (onProgress) onProgress(done, g.tests.length);
        });
      }
    }
    return { correct: results.every((x) => x.ok), staticMessage: null, results: results };
  }

  /* ---------------- 学習者向けの表示用 iframe ---------------- */
  /** spec: {format, given_html, student, viewport}。返り値は iframe 要素（親ページには触れられない sandbox） */
  function preview(spec) {
    const f = document.createElement("iframe");
    f.setAttribute("sandbox", "allow-scripts");
    f.setAttribute("title", "表示結果のプレビュー");
    f.className = "preview-frame";
    f.srcdoc = assemble(spec, false, null);
    return f;
  }

  return { runJs, runPage, grade, preview, assemble, staticCheck, valueKey, truthy, deepEqual };
})();

if (typeof module !== "undefined") module.exports = WebRunner;
