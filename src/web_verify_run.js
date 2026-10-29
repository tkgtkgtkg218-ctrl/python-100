/* JavaScript / HTML・CSS コースの教材データを、ヘッドレス Chrome で実行検証する。
 *   node src/web_verify_run.js <コースのフォルダ> [問題IDの接頭辞や ID で絞り込み]
 * 使い捨てのプロファイルを使う。結果は <コースのフォルダ>/verify_results.json に保存し、失敗があれば終了コード1。 */
const { spawn } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");

const CHROME = process.env.CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const courseDir = path.resolve(process.argv[2]);
const only = process.argv[3] || "";
const PORT = 9344;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && this.pending.has(m.id)) { const { res, rej } = this.pending.get(m.id); this.pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); } }; }
  send(method, params = {}) { const id = ++this.id; this.ws.send(JSON.stringify({ id, method, params })); return new Promise((res, rej) => this.pending.set(id, { res, rej })); }
  async eval(expression) { const r = await this.send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception ? r.exceptionDetails.exception.description : r.exceptionDetails.text); return r.result.value; }
}

async function main() {
  const questions = JSON.parse(fs.readFileSync(path.join(courseDir, "questions.json"), "utf8")).questions.filter((q) => !only || q.id.startsWith(only));
  const lessons = JSON.parse(fs.readFileSync(path.join(courseDir, "lessons.json"), "utf8")).lessons;
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "webverify-"));
  const proc = spawn(CHROME, ["--headless=new", "--remote-debugging-port=" + PORT, "--user-data-dir=" + profile, "--no-first-run", "--no-default-browser-check", "--allow-file-access-from-files", "about:blank"], { stdio: "ignore" });
  const report = { course: path.basename(courseDir), questions: [], examples: [] };
  try {
    let list;
    for (let i = 0; i < 80; i++) { try { list = await (await fetch("http://127.0.0.1:" + PORT + "/json/list")).json(); if (list.find((t) => t.type === "page")) break; } catch (e) { /* 起動待ち */ } await sleep(250); }
    const ws = new WebSocket(list.find((t) => t.type === "page").webSocketDebuggerUrl);
    await new Promise((r) => (ws.onopen = r));
    const cdp = new CDP(ws);
    await cdp.send("Page.enable"); await cdp.send("Runtime.enable");
    const url = pathToFileURL(path.join(__dirname, "..", "app", "verify_web.html")).href;
    await cdp.send("Page.navigate", { url });
    for (let i = 0; i < 80; i++) { await sleep(250); try { if (await cdp.eval("typeof WebVerify !== 'undefined' && typeof WebRunner !== 'undefined'")) break; } catch (e) { /* 読み込み中 */ } }
    const CH = 6;
    for (let i = 0; i < questions.length; i += CH) {
      const chunk = questions.slice(i, i + CH);
      const r = await cdp.eval("WebVerify.verifyQuestions(" + JSON.stringify(chunk) + ")");
      report.questions.push(...r);
      process.stderr.write("\r" + Math.min(i + CH, questions.length) + "/" + questions.length);
    }
    process.stderr.write("\n");
    if (!only) report.examples = await cdp.eval("WebVerify.verifyExamples(" + JSON.stringify(lessons) + ")");
    const claimsPath = path.join(courseDir, "claims.json");
    if (!only && fs.existsSync(claimsPath)) report.claims = await cdp.eval("WebVerify.verifyClaims(" + JSON.stringify(JSON.parse(fs.readFileSync(claimsPath, "utf8"))) + ")");
    ws.close();
  } catch (e) {
    report.error = String((e && e.stack) || e);
  } finally {
    proc.kill();
  }
  const checks = report.questions.reduce((n, q) => n + q.checks, 0);
  const failed = report.questions.filter((q) => q.failures.length);
  const exFailed = report.examples.filter((e) => !e.ok);
  const claims = report.claims || [];
  const claimFailed = claims.filter((c) => !c.ok);
  report.summary = { questions: report.questions.length, checks, failedQuestions: failed.length, examples: report.examples.length, failedExamples: exFailed.length, claims: claims.length, failedClaims: claimFailed.length, error: report.error || null };
  claimFailed.forEach((c) => console.log("[NG claim]", JSON.stringify(c)));
  if (!only) fs.writeFileSync(path.join(courseDir, "verify_results.json"), JSON.stringify(report, null, 1));
  failed.forEach((q) => console.log("[NG]", q.id, JSON.stringify(q.failures)));
  exFailed.forEach((e) => console.log("[NG example]", JSON.stringify(e)));
  console.log(JSON.stringify(report.summary));
  process.exit(failed.length || exFailed.length || claimFailed.length || report.error ? 1 : 0);
}
main();
