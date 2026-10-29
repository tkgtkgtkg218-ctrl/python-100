/* 開発用: HTML/CSS/JS の断片をヘッドレス Chrome のページ（採点基盤と同じ仕組み）で読み込み、式の値を表示する。
 *   node src/web_eval.js <format> <コードのファイル> "<式1>" ["<式2>" ...]
 *   format: html_document | html_body | css | javascript_dom   （css / javascript_dom は環境変数 GIVEN_HTML で HTML を渡す） */
const { spawn } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");

const CHROME = process.env.CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const [, , format, file, ...exprs] = process.argv;
const PORT = 9355;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "webeval-"));
  const proc = spawn(CHROME, ["--headless=new", "--remote-debugging-port=" + PORT, "--user-data-dir=" + profile, "--no-first-run", "--allow-file-access-from-files", "about:blank"], { stdio: "ignore" });
  try {
    let list;
    for (let i = 0; i < 80; i++) { try { list = await (await fetch("http://127.0.0.1:" + PORT + "/json/list")).json(); if (list.find((t) => t.type === "page")) break; } catch (e) { /* 起動待ち */ } await sleep(250); }
    const ws = new WebSocket(list.find((t) => t.type === "page").webSocketDebuggerUrl);
    await new Promise((r) => (ws.onopen = r));
    let id = 0; const pending = new Map();
    ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
    const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
    await send("Page.navigate", { url: pathToFileURL(path.join(__dirname, "..", "app", "verify_web.html")).href });
    for (let i = 0; i < 80; i++) { await sleep(250); const r = await send("Runtime.evaluate", { expression: "typeof WebRunner !== 'undefined'", returnByValue: true }); if (r.result.result.value) break; }
    // 式が長い・引用符が多いときは、式の配列を JSON ファイルで渡せる（EXPRS_JSON=ファイルパス）
    const exprList = process.env.EXPRS_JSON ? JSON.parse(fs.readFileSync(process.env.EXPRS_JSON, "utf8")) : exprs;
    const spec = { format, given_html: process.env.GIVEN_HTML || "", student: fs.readFileSync(file, "utf8"), exprs: exprList, viewport: process.env.VIEWPORT ? Number(process.env.VIEWPORT) : undefined };
    const r = await send("Runtime.evaluate", { expression: "WebRunner.runPage(" + JSON.stringify(spec) + ")", awaitPromise: true, returnByValue: true });
    console.log(JSON.stringify(r.result.result.value ?? r.result, null, 1));
    ws.close();
  } finally { proc.kill(); }
})();
