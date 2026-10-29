/* アプリの通し確認（ヘッドレス Chrome）。実際の画面を操作して、全コース・全問題を回答する。
 *   node src/app_e2e.js <アプリのURL> [コース名: py | js | htmlcss | all]
 * 各問題で「正解を入力 → ○になる」「誤答を入力 → ×になる」を確かめ、レッスンの表示（プレビューの iframe を含む）も確認する。
 * 使い捨てのプロファイルを使うので、普段のブラウザには影響しない。 */
const { spawn } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const CHROME = process.env.CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const URL_ = process.argv[2] || "http://localhost:8767/";
const which = process.argv[3] || "all";
const PORT = 9366;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const DRIVER = `
window.__e2e = async function (key) {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const D = JSON.parse(document.getElementById('data').textContent);
  const course = D.courses.find((c) => c.key === key);
  const qs = course.questions.questions.filter((q) => !window.__only || window.__only.includes(q.id));
  const res = { key, tested: 0, ok: 0, fails: [], previews: 0, lessonErrors: [], lessons: 0, iframes: 0 };
  async function open(q) {
    for (let attempt = 0; attempt < 2; attempt++) {
      location.hash = '#/'; await sleep(90); // Chrome は短時間の大量の hash 変更を無視する（200回/10秒）ため、間隔をあける
      location.hash = '#/' + key + '/q/' + q.stage_id + '/' + q.number_in_stage;
      for (let i = 0; i < 150; i++) { await sleep(20); const t = document.querySelector('.question .qmeta .tag'); if (t && t.textContent === q.id && !document.querySelector('.feedback.ok, .feedback.ng')) return true; }
    }
    return false;
  }
  const btn = (re) => [...document.querySelectorAll('#app button')].find((b) => re.test(b.textContent));
  async function waitFb(ms) {
    for (let i = 0; i < ms / 50; i++) { const f = document.querySelector('.feedback'); if (f && /\\b(ok|ng)\\b/.test(f.className)) return f.className; await sleep(50); }
    return '';
  }
  function setAnswer(q, right) {
    const app = document.getElementById('app');
    if (q.answer_mode === 'choice') {
      const wrong = q.choices.find((c) => c.id !== q.answer.correct_choice_id).id;
      app.querySelector('input[name=choice][value=' + (right ? q.answer.correct_choice_id : wrong) + ']').click();
      return;
    }
    const inputs = [...app.querySelectorAll('input.blank')];
    if (q.type === 'fill_blank') q.answer.blanks.forEach((b, i) => { inputs[i].value = right ? b.accepted[0] : 'zzz'; });
    else if (q.type === 'predict_output') app.querySelector('textarea').value = right ? q.answer.expected_output : 'zzz';
    else if (q.type === 'bug_fix') inputs[0].value = right ? q.answer.accepted[0] : 'zzz';
    else if (q.type === 'code_write') app.querySelector('textarea.answer-ta').value = right ? q.answer.reference_solution : q.answer.rejected_examples[0].code;
  }
  for (const q of qs) {
    for (const right of [false, true]) {
      try {
        if (!(await open(q))) { res.fails.push(q.id + ' not opened'); continue; }
        if (q.type === 'code_write') { for (let i = 0; i < 400; i++) { const b = btn(/回答する/); if (b && !b.disabled) break; await sleep(50); } }
        setAnswer(q, right);
        btn(/^回答する/).click();
        const cls = await waitFb(q.type === 'code_write' ? 40000 : 1500);
        res.tested++;
        const want = right ? 'ok' : 'ng';
        if (new RegExp('\\\\b' + want + '\\\\b').test(cls)) res.ok++; else res.fails.push(q.id + (right ? ' right' : ' wrong') + ' -> "' + cls + '"');
        if (right && q.check && q.type !== 'code_write' && q.check.format !== 'javascript') { if (document.querySelector('details.actual')) res.previews++; else res.fails.push(q.id + ' no preview'); }
      } catch (e) { res.fails.push(q.id + ' EXC ' + e.message); }
    }
  }
  // レッスンの表示（各ステージの2セクション）
  for (const s of course.curriculum.stages) {
    for (let idx = 0; idx < 2; idx++) {
      location.hash = '#/'; await sleep(90);
      location.hash = '#/' + key + '/lesson/' + s.id + '/' + idx;
      const want = course.lessons.lessons.find((l) => l.stage_id === s.id).sections[idx].title;
      for (let i = 0; i < 250; i++) { await sleep(20); const h = document.querySelector('#app h2'); if (h && h.textContent === want) break; }
      res.lessons++;
      const app = document.getElementById('app');
      const sec = course.lessons.lessons.find((l) => l.stage_id === s.id).sections[idx];
      const expectedFrames = sec.examples.filter((e) => e.preview).length;
      for (let i = 0; i < 150 && app.querySelectorAll('iframe.preview-frame').length !== expectedFrames; i++) await sleep(20);
      const frames = app.querySelectorAll('iframe.preview-frame').length;
      res.iframes += frames;
      if (/表示エラー/.test(app.innerText) || !app.querySelector('h2')) res.lessonErrors.push(s.id + '/' + idx + ' render error');
      if (frames !== expectedFrames) res.lessonErrors.push(s.id + '/' + idx + ' iframes ' + frames + ' != ' + expectedFrames + ' hash=' + location.hash + ' text=' + app.innerText.slice(0, 120).replace(/\\n/g, ' | ') + ' boxes=' + app.querySelectorAll('.previewbox').length + ' html=' + (app.querySelector('.previewbox') ? app.querySelector('.previewbox').outerHTML.slice(0, 200) : ''));
    }
  }
  return res;
};
true`;

async function main() {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "appe2e-"));
  const proc = spawn(CHROME, ["--headless=new", "--remote-debugging-port=" + PORT, "--user-data-dir=" + profile, "--no-first-run", "about:blank"], { stdio: "ignore" });
  const out = { results: [], consoleErrors: [] };
  try {
    let list;
    for (let i = 0; i < 80; i++) { try { list = await (await fetch("http://127.0.0.1:" + PORT + "/json/list")).json(); if (list.find((t) => t.type === "page")) break; } catch (e) { /* 起動待ち */ } await sleep(250); }
    const ws = new WebSocket(list.find((t) => t.type === "page").webSocketDebuggerUrl);
    await new Promise((r) => (ws.onopen = r));
    let id = 0; const pending = new Map();
    ws.onmessage = (e) => {
      const m = JSON.parse(e.data);
      if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
      else if (m.method === "Runtime.exceptionThrown") out.consoleErrors.push(m.params.exceptionDetails.exception ? m.params.exceptionDetails.exception.description : m.params.exceptionDetails.text);
    };
    const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
    const ev = async (expression) => { const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true }); if (r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails.exception || r.result.exceptionDetails)); return r.result.result.value; };
    await send("Page.enable"); await send("Runtime.enable");
    await send("Page.navigate", { url: URL_ });
    for (let i = 0; i < 80; i++) { await sleep(250); if (await ev("document.querySelectorAll('.course-card').length").catch(() => 0)) break; }
    out.courseCards = await ev("document.querySelectorAll('.course-card').length");
    await ev("localStorage.setItem('pypath.v1', JSON.stringify({courses:{},unlockAll:true})); true");
    await send("Page.navigate", { url: URL_ });
    for (let i = 0; i < 80; i++) { await sleep(250); if (await ev("document.querySelectorAll('.course-card').length").catch(() => 0)) break; }
    await ev(DRIVER);
    if (process.argv[4]) await ev('window.__only = ' + JSON.stringify(process.argv[4].split(',')) + '; true');
    for (const key of which === "all" ? ["py", "js", "htmlcss"] : [which]) {
      const r = await ev("window.__e2e('" + key + "')");
      out.results.push(r);
      console.log(key, JSON.stringify({ tested: r.tested, ok: r.ok, previews: r.previews, lessons: r.lessons, iframes: r.iframes, fails: r.fails.length, lessonErrors: r.lessonErrors.length }));
      r.fails.slice(0, 10).forEach((f) => console.log("  [NG]", f));
      r.lessonErrors.slice(0, 10).forEach((f) => console.log("  [NG lesson]", f));
    }
    ws.close();
  } catch (e) {
    out.error = String((e && e.stack) || e);
    console.log("ERROR", out.error);
  } finally { proc.kill(); }
  console.log("page exceptions:", out.consoleErrors.length);
  out.consoleErrors.slice(0, 5).forEach((m) => console.log("  ", m));
  const bad = out.error || out.consoleErrors.length || out.results.some((r) => r.fails.length || r.lessonErrors.length);
  process.exit(bad ? 1 : 0);
}
main();
