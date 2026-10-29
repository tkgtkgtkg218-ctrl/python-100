/* PWA の実ブラウザ検証（ヘッドレス Chrome を DevTools Protocol で操作）。
 *   node src/pwa_test.js <phase> <profileDir> [url]
 *   phase1: オンラインで開く → Service Worker 登録・キャッシュ・インストール可否・Pyodide 採点
 *   phase2: サーバー停止＋ CDN 名前解決不能（--host-resolver-rules）で、同じプロファイルを開く → オフライン動作
 *   phase3: sw.js が更新された状態で開く → 更新バナーと古いキャッシュの削除
 * 使い捨てのプロファイル（--user-data-dir）を使うので、普段のブラウザには影響しない。 */
const { spawn } = require("child_process");

const CHROME = process.env.CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const [, , phase, profile, urlArg] = process.argv;
const URL_ = urlArg || "http://localhost:8766/";
const PORT = 9333;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.handlers = []; ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && this.pending.has(m.id)) { const { res, rej } = this.pending.get(m.id); this.pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); } else this.handlers.forEach((h) => h(m)); }; }
  send(method, params = {}) { const id = ++this.id; this.ws.send(JSON.stringify({ id, method, params })); return new Promise((res, rej) => this.pending.set(id, { res, rej })); }
  async eval(expression) { const r = await this.send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception ? r.exceptionDetails.exception.description : r.exceptionDetails.text); return r.result.value; }
}

async function main() {
  const extra = phase === "phase2" ? ["--host-resolver-rules=MAP cdn.jsdelivr.net ~NOTFOUND"] : [];
  const proc = spawn(CHROME, ["--headless=new", "--remote-debugging-port=" + PORT, "--user-data-dir=" + profile, "--no-first-run", "--no-default-browser-check", ...extra, "about:blank"], { stdio: "ignore" });
  const results = {};
  try {
    let list;
    for (let i = 0; i < 60; i++) { try { list = await (await fetch("http://127.0.0.1:" + PORT + "/json/list")).json(); if (list.find((t) => t.type === "page")) break; } catch (e) { /* 起動待ち */ } await sleep(250); }
    const target = list.find((t) => t.type === "page");
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((r) => (ws.onopen = r));
    const cdp = new CDP(ws);
    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");
    await cdp.send("Page.navigate", { url: URL_ });
    for (let i = 0; i < 60; i++) { await sleep(250); try { if ((await cdp.eval("document.querySelectorAll('.stage-card').length")) === 10) break; } catch (e) { /* 読み込み中 */ } }
    results.stageCards = await cdp.eval("document.querySelectorAll('.stage-card').length");
    results.title = await cdp.eval("document.title");
    // Service Worker が制御するまで待つ
    for (let i = 0; i < 80; i++) { if (await cdp.eval("!!navigator.serviceWorker.controller")) break; await sleep(250); }
    results.controlled = await cdp.eval("!!navigator.serviceWorker.controller");
    results.swState = await cdp.eval("navigator.serviceWorker.getRegistration().then(r => r && r.active ? r.active.state : null)");
    results.cacheKeys = await cdp.eval("caches.keys()");
    results.shellFiles = await cdp.eval("(async()=>{const k=(await caches.keys()).find(x=>x.startsWith('pypath-shell'));return k?(await (await caches.open(k)).keys()).map(r=>new URL(r.url).pathname):[]})()");

    if (phase === "phase1") {
      const inst = await cdp.send("Page.getInstallabilityErrors");
      results.installabilityErrors = inst.installabilityErrors.map((e) => e.errorId);
      const man = await cdp.send("Page.getAppManifest");
      results.manifestErrors = (man.errors || []).map((e) => e.message);
      results.manifestUrl = man.url;
      await cdp.eval("localStorage.setItem('pypath.v1', JSON.stringify({stages:{S01:{answers:{'PY-001':{firstCorrect:true,tries:1,last:'c2'}},cleared:false,bestStars:0,attempts:1}},unlockAll:false}))");
    }
    if (phase === "phase1" || phase === "phase2") {
      results.progressKept = await cdp.eval("JSON.parse(localStorage.getItem('pypath.v1')||'{}').stages?.S01?.answers?.['PY-001']?.firstCorrect === true");
      results.pyodide = await cdp.eval(`(async () => {
        const t0 = performance.now();
        const info = await PyRunner.ready();
        const q = JSON.parse(document.getElementById('data').textContent).questions.questions.find(x => x.id === 'PY-060');
        const g = await PyRunner.gradeCode(q, q.answer.reference_solution);
        const bad = await PyRunner.gradeCode(q, q.answer.rejected_examples[0].code);
        return { python: info.python, referencePasses: g.correct, rejectedFails: !bad.correct, ms: Math.round(performance.now() - t0) };
      })()`);
      results.pyodideCacheEntries = await cdp.eval("caches.open('pypath-pyodide-v0.26.4').then(c => c.keys()).then(k => k.map(r => r.url.split('/').pop()))");
    }
    if (phase === "phase2") {
      // CDN がこの環境から本当に届かないことの確認（SW がキャッシュしていない別URLは失敗するはず）
      results.cdnReallyBlocked = await cdp.eval("fetch('https://cdn.jsdelivr.net/npm/left-pad@1.3.0/index.js').then(() => false).catch(() => true)");
    }
    if (phase === "phase3") {
      for (let i = 0; i < 80; i++) { if (await cdp.eval("!document.getElementById('update-banner').hidden")) break; await sleep(250); }
      results.updateBannerShown = await cdp.eval("!document.getElementById('update-banner').hidden");
      await sleep(2000);
      results.cacheKeysAfterUpdate = await cdp.eval("caches.keys()");
    }
    ws.close();
  } catch (e) {
    results.error = String(e && e.stack || e);
  } finally {
    proc.kill();
  }
  console.log(JSON.stringify(results, null, 2));
}
main();
