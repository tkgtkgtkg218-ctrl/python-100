/* Pyodide を Web Worker で動かし、コード作成問題を test_cases で自動採点する（主スレッド側）。
 * - 初回のみ CDN（jsDelivr, バージョン固定）から Pyodide を読み込む。ネットワークがないと使えない。
 * - テスト1件ごとに新しい名前空間で実行。制限時間を超えたら Worker ごと terminate() して作り直す。 */
const PyRunner = (function () {
  const CDN = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
  const INIT_TIMEOUT_MS = 90000;
  let worker = null;
  let readyP = null;
  let seq = 0;
  const pending = new Map();

  function failAllPending(message) {
    pending.forEach((cb) => cb({ type: "result", res: { ok: false, error: message }, out: "", truncated: false }));
    pending.clear();
  }

  function start() {
    const src = document.getElementById("pyworker").textContent;
    const blobUrl = URL.createObjectURL(new Blob([src], { type: "text/javascript" }));
    const w = new Worker(blobUrl);
    worker = w;
    readyP = new Promise((resolve, reject) => {
      const timer = setTimeout(() => { w.terminate(); reject(new Error("Python の読み込みがタイムアウトしました")); }, INIT_TIMEOUT_MS);
      w.onmessage = (ev) => {
        const m = ev.data;
        if (m.type === "ready") {
          clearTimeout(timer);
          w.onmessage = (e2) => {
            const r = e2.data;
            if (r.type === "result") { const cb = pending.get(r.id); if (cb) { pending.delete(r.id); cb(r); } }
          };
          resolve({ python: m.python, pyodide: m.pyodide });
        } else if (m.type === "initerror") { clearTimeout(timer); reject(new Error(m.message)); }
      };
      w.onerror = (e) => { clearTimeout(timer); const msg = (e && e.message) || "Worker エラー"; reject(new Error(msg)); failAllPending(msg); };
      w.postMessage({ type: "init", url: CDN });
    });
    readyP.catch(() => { if (worker === w) { worker = null; readyP = null; } });
    return readyP;
  }

  function ready() { return readyP || start(); }

  /** op: "static" | "test"。制限時間超過なら {timeout:true} を返し、Worker を作り直す。 */
  async function run(op, job, timeoutMs) {
    await ready();
    const w = worker;
    const id = ++seq;
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        pending.delete(id);
        w.terminate();
        if (worker === w) { worker = null; readyP = null; }
        resolve({ timeout: true });
      }, timeoutMs);
      pending.set(id, (m) => { clearTimeout(timer); resolve(m); });
      w.postMessage({ type: "run", id, op, job });
    });
  }

  /** 採点: 静的チェック → 各テスト。onProgress(done, total) は任意。 */
  async function gradeCode(q, student, onProgress) {
    const g = q.grading;
    const limit = (g.timeout_sec || 5) * 1000;
    const sc = await run("static", { student, required: g.required_ast_nodes, any: g.required_any_ast_nodes }, limit);
    if (sc.timeout) return { correct: false, staticMessage: "チェックに時間がかかりすぎました", results: [] };
    if (!sc.res.ok) return { correct: false, staticMessage: sc.res.message, results: [] };
    const results = [];
    for (let i = 0; i < g.tests.length; i++) {
      const t = g.tests[i];
      const r = await run("test", { student, setup: t.setup || "", kind: t.kind, call: t.call || "", expected: t.expected || "" }, limit);
      const row = { t, ok: false, timeout: !!r.timeout, error: null, actual: null, out: "" };
      if (r.timeout) { row.error = "時間切れ（" + g.timeout_sec + "秒）。無限ループになっていないか確認しましょう。"; }
      else {
        row.out = r.out;
        if (r.res.error) row.error = r.res.error;
        else if (t.kind === "stdout") { row.ok = Grader.normOutput(r.out) === Grader.normOutput(t.expected_stdout); row.actual = r.out; }
        else { row.ok = !!r.res.ok; row.actual = r.res.actual; }
        if (r.truncated) row.error = "出力が長すぎます（上限 64KB）";
        if (r.truncated) row.ok = false;
      }
      results.push(row);
      if (onProgress) onProgress(i + 1, g.tests.length);
      if (r.timeout) {
        // 時間切れのたびに Worker の作り直しが必要なので、残りのテストは実行せず不合格として扱う
        for (let k = i + 1; k < g.tests.length; k++) results.push({ t: g.tests[k], ok: false, timeout: false, skipped: true, error: "前のテストが時間切れだったため実行していません", actual: null, out: "" });
        break;
      }
    }
    return { correct: results.every((x) => x.ok), staticMessage: null, results };
  }

  /** 「実行して試す」: 前提コード＋学習者コードを実行し、出力かエラーを返す */
  async function tryRun(q, student) {
    const r = await run("test", { student, setup: q.prefix_code || "", kind: "stdout", call: "", expected: "" }, (q.grading.timeout_sec || 5) * 1000);
    if (r.timeout) return { error: "時間切れ（無限ループの可能性があります）", out: "" };
    return { error: r.res.error || (r.truncated ? "出力が長すぎます（上限 64KB）" : null), out: r.out };
  }

  return { ready, run, gradeCode, tryRun };
})();

if (typeof module !== "undefined") module.exports = PyRunner;
