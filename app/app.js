/* はじめの100問（Python / JavaScript / HTML・CSS）— 学習アプリ
 * 画面: コース選択 / ステージ一覧 / レッスン / 問題回答(+フィードバック) / ステージ結果 / 学習進捗
 * 自動採点: 全問題。コード作成は、Python は Pyodide（Web Worker）、JavaScript は Web Worker、HTML/CSS/DOM操作は sandbox 付き iframe で実行して採点する。 */
(function () {
  "use strict";
  const DATA = JSON.parse(document.getElementById("data").textContent);
  const DEFAULT_UI = {
    type_labels: { multiple_choice: "3択", predict_output: "実行結果の予測", fill_blank: "穴埋め", bug_fix: "間違い探し", code_write: "コード作成" },
    write_button: "回答する（自動採点）", run_button: "実行して試す", run_output_label: "実行結果",
  };
  const COURSES = DATA.courses.map((c) => ({
    key: c.key, tagline: c.tagline, curriculum: c.curriculum, lessons: c.lessons.lessons,
    questions: c.questions.questions, ui: Object.assign({}, DEFAULT_UI, c.curriculum.course.ui || {}),
  }));
  const COURSE_BY_KEY = Object.fromEntries(COURSES.map((c) => [c.key, c]));
  /* いま開いているコースに応じて切り替わる値 */
  let C = COURSES[0];
  let stages, lessonByStage, questions, qByStage, stageById, REQUIRED, STARS, TYPE_JA;
  function setCourse(key) {
    C = COURSE_BY_KEY[key] || COURSES[0];
    stages = C.curriculum.stages;
    lessonByStage = Object.fromEntries(C.lessons.map((l) => [l.stage_id, l]));
    questions = C.questions;
    qByStage = {};
    questions.forEach((q) => (qByStage[q.stage_id] = qByStage[q.stage_id] || []).push(q));
    stageById = Object.fromEntries(stages.map((s) => [s.id, s]));
    REQUIRED = stages[0].clear_condition.required_correct;
    STARS = stages[0].clear_condition.stars;
    TYPE_JA = C.ui.type_labels;
  }
  setCourse(COURSES[0].key);
  /* コースを含む移動先（例: #/js/lesson/S01/0）。path が空ならステージ一覧 */
  const H = (path) => "#/" + C.key + "/" + (path || "");

  /* ---------- 小さなDOMヘルパー ---------- */
  function h(tag, props, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(props || {})) {
      if (v == null || v === false) continue;
      if (k === "class") e.className = v;
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : v);
    }
    kids.flat(Infinity).forEach((c) => {
      if (c == null || c === false) return;
      e.append(c.nodeType ? c : document.createTextNode(String(c)));
    });
    return e;
  }
  const para = (t) => h("p", {}, t);
  const link = (href, text, cls) => h("a", { href, class: cls }, text);
  const code = (t, lang) => h("pre", { class: "code" + (lang ? " lang-" + lang : ""), "data-lang": lang || null }, h("code", {}, t));
  /* 表示用の iframe（sandbox 付き）。HTML・CSS・DOM操作のコードを、実際に表示して操作できる */
  function previewBlock(spec, label) {
    const f = WebRunner.preview(spec);
    if (spec.viewport) { f.style.width = spec.viewport + "px"; f.style.maxWidth = "100%"; }
    return h("div", { class: "previewbox" }, h("div", { class: "out-label" }, label || "表示結果（実際に操作できます）"), f);
  }

  /* ---------- 進捗の保存（localStorage。使えない環境ではメモリのみ） ---------- */
  const KEY = "pypath.v1";
  let state;
  function fresh() { return { courses: {}, unlockAll: false }; }
  function load() {
    try {
      const s = JSON.parse(localStorage.getItem(KEY));
      if (!s) return fresh();
      // 旧形式（Python のみ）の進捗を、コース別の形式へ移す
      if (s.stages && !s.courses) { s.courses = { py: { stages: s.stages } }; delete s.stages; }
      s.courses = s.courses || {};
      return s;
    } catch (e) { return fresh(); }
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* 保存できない環境では無視 */ } }
  state = load();
  function courseState(key) { return (state.courses[key] = state.courses[key] || { stages: {} }); }
  function ss(id) {
    const cs = courseState(C.key);
    if (!cs.stages[id]) cs.stages[id] = { answers: {}, cleared: false, bestStars: 0, attempts: 1 };
    return cs.stages[id];
  }
  const answeredCount = (id) => Object.keys(ss(id).answers).length;
  const correctCount = (id) => Object.values(ss(id).answers).filter((a) => a.firstCorrect).length;
  const starsFor = (n) => (n >= STARS["3"] ? 3 : n >= STARS["2"] ? 2 : n >= STARS["1"] ? 1 : 0);
  function unlocked(s) {
    if (state.unlockAll || s.number === 1) return true;
    return ss("S" + String(s.number - 1).padStart(2, "0")).cleared;
  }

  /* ---------- ルーティング ---------- */
  const app = document.getElementById("app");
  function go(hash) { location.hash = hash; }
  function render() {
    const raw = location.hash.replace(/^#\/?/, "");
    const parts = raw ? raw.split("/") : [];
    app.replaceChildren();
    let view;
    let inCourse = false;
    try {
      // 先頭がコースの名前（py / js / htmlcss）ならそのコース。昔の形式（#/lesson/… など）は Python として扱う
      if (parts[0] && COURSE_BY_KEY[parts[0]]) { setCourse(parts.shift()); inCourse = true; }
      else if (["lesson", "q", "result", "selftest"].includes(parts[0])) { setCourse("py"); inCourse = true; }
      if (inCourse) {
        if (parts[0] === "lesson") view = viewLesson(parts[1], parseInt(parts[2] || "0", 10));
        else if (parts[0] === "q") view = viewQuestion(parts[1], parseInt(parts[2] || "1", 10));
        else if (parts[0] === "result") view = viewResult(parts[1]);
        else if (parts[0] === "progress") view = viewProgress();
        else if (parts[0] === "selftest") view = viewSelfTest();
        else view = viewStages();
      } else if (parts[0] === "progress") view = viewAllProgress();
      else view = viewCourses();
    } catch (e) {
      view = h("div", { class: "card" }, h("h2", {}, "表示エラー"), para(String(e && e.message || e)), link("#/", "コース選択へ"));
      console.error(e);
    }
    app.append(view);
    window.scrollTo(0, 0);
    const nav = document.getElementById("nav-progress");
    nav.setAttribute("href", inCourse ? H("progress") : "#/progress");
    nav.setAttribute("aria-current", parts[0] === "progress" ? "page" : "false");
    document.title = inCourse ? C.curriculum.course.title : "はじめの100問";
  }
  window.addEventListener("hashchange", render);
  // インストール可能になったとき（または完了したとき）、コース選択を表示中なら案内を更新する
  window.addEventListener("pwa-installable", () => { if (!location.hash || location.hash === "#/") render(); });

  /* ---------- (0) コース選択 ---------- */
  function courseStats(c) {
    const cs = courseState(c.key);
    let done = 0, cleared = 0;
    c.curriculum.stages.forEach((s) => {
      const st = cs.stages[s.id];
      if (st) { done += Object.keys(st.answers).length; if (st.cleared) cleared += 1; }
    });
    return { done, cleared, total: c.questions.length };
  }
  function viewCourses() {
    const root = h("div", {});
    root.append(h("section", { class: "hero" }, h("h1", {}, "はじめの100問"), para("短い教科書を読んで、すぐ問題を解く。学ぶコースを選んでください。")));
    const pwa = window.__pwa || {};
    if (!pwa.standalone) {
      if (pwa.installEvent) {
        root.append(h("div", { class: "install" }, h("span", {}, "アプリとしてインストールすると、ホーム画面から開けて、オフラインでも学習できます。"),
          h("button", { class: "btn primary", type: "button", onclick: async () => { const ev = pwa.installEvent; pwa.installEvent = null; ev.prompt(); try { await ev.userChoice; } catch (e) { /* 無視 */ } render(); } }, "インストール")));
      } else if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
        root.append(h("div", { class: "install small" }, "iPhone / iPad では、共有ボタン →「ホーム画面に追加」でアプリとして使えます。"));
      }
    }
    const list = h("div", { class: "course-list" });
    COURSES.forEach((c) => {
      const s = courseStats(c);
      list.append(h("a", { class: "course-card course-" + c.key, href: "#/" + c.key + "/" },
        h("div", { class: "course-badge", "aria-hidden": "true" }, c.curriculum.course.language_display_name),
        h("div", { class: "course-body" },
          h("div", { class: "stage-title" }, c.curriculum.course.title),
          h("div", { class: "muted small" }, c.tagline),
          h("div", { class: "meter", role: "img", "aria-label": s.done + "問回答済み/" + s.total + "問" }, h("span", { style: "width:" + Math.round((s.done / s.total) * 100) + "%" })),
          h("div", { class: "small" }, "クリア " + s.cleared + "/10 ステージ ・ 回答済み " + s.done + "/" + s.total + " 問")
        )));
    });
    root.append(list);
    root.append(h("p", { class: "small muted" }, "※ HTML と CSS は、プログラミング言語ではなく、それぞれマークアップ言語・スタイルシート言語です。JavaScript はプログラミング言語です。この3つは役割の違う技術で、組み合わせて使います。"));
    return root;
  }

  /* ---------- (1) ステージ一覧 ---------- */
  function viewStages() {
    const total = questions.length;
    const done = stages.reduce((n, s) => n + answeredCount(s.id), 0);
    const cleared = stages.filter((s) => ss(s.id).cleared).length;
    const root = h("div", {});
    root.append(h("nav", { class: "crumb", "aria-label": "現在地" }, link("#/", "コース選択"), " › ", C.curriculum.course.language_display_name));
    root.append(
      h("section", { class: "hero" },
        h("h1", {}, C.curriculum.course.title),
        para("短い教科書を読んで、すぐ問題を解く。10ステージ・全" + total + "問。"),
        h("p", { class: "muted" }, "クリア " + cleared + "/10 ステージ ・ 回答済み " + done + "/" + total + " 問")
      )
    );
    const list = h("div", { class: "stage-list" });
    stages.forEach((s) => {
      const open = unlocked(s);
      const n = answeredCount(s.id);
      const st = ss(s.id);
      const status = st.cleared ? "クリア済み" : !open ? "ロック中" : n ? "学習中" : "未着手";
      const card = h(open ? "a" : "div", {
        class: "stage-card" + (open ? "" : " locked") + (st.cleared ? " cleared" : ""),
        href: open ? H("lesson/" + s.id + "/0") : null,
        "aria-disabled": open ? null : "true",
      },
        h("div", { class: "stage-num" }, String(s.number)),
        h("div", { class: "stage-body" },
          h("div", { class: "stage-title" }, s.title),
          h("div", { class: "muted small" }, s.subtitle),
          h("div", { class: "meter", role: "img", "aria-label": n + "問回答済み/10問" }, h("span", { style: "width:" + n * 10 + "%" })),
          h("div", { class: "small" }, status + " ・ " + n + "/10問" + (!open ? "（ステージ" + (s.number - 1) + "をクリアすると開きます）" : ""))
        ),
        h("div", { class: "stars", "aria-label": "星" + st.bestStars }, "★".repeat(st.bestStars) + "☆".repeat(3 - st.bestStars))
      );
      list.append(card);
    });
    root.append(list);
    const dev = h("label", { class: "dev" },
      h("input", { type: "checkbox", checked: state.unlockAll ? true : null, onchange: (e) => { state.unlockAll = e.target.checked; save(); render(); } }),
      " 開発用: すべてのステージを開く"
    );
    root.append(dev, h("p", { class: "small" }, link(H("selftest"), "開発用: コード採点の自己テスト")));
    return root;
  }

  /* ---------- (2) レッスン ---------- */
  function viewLesson(sid, idx) {
    const s = stageById[sid];
    if (!s) return viewStages();
    if (!unlocked(s)) return h("div", { class: "card" }, para("このステージはまだ開いていません。"), link(H(), "ステージ一覧へ"));
    const L = lessonByStage[sid];
    const sec = L.sections[idx];
    if (!sec) return viewLesson(sid, 0);
    const last = idx === L.sections.length - 1;
    const root = h("div", {});
    root.append(crumb(s, "教科書 " + (idx + 1) + "/" + L.sections.length));
    if (idx === 0) root.append(h("div", { class: "card intro" }, h("h3", {}, "この知識が役に立つ理由"), para(L.intro)));
    const c = h("div", { class: "card" }, h("h2", {}, sec.title), h("p", { class: "muted small" }, "読む目安: 約" + sec.read_minutes + "分"));
    sec.body.forEach((p) => c.append(para(p)));
    c.append(h("h3", {}, "用語"), h("dl", {}, sec.glossary.map((g) => [h("dt", {}, g.term), h("dd", {}, g.definition)])));
    sec.examples.forEach((ex) => {
      c.append(h("h3", {}, "コード例: " + ex.title));
      if (ex.context_html) c.append(h("p", { class: "small muted" }, "HTML（この例では、あらかじめ用意されています）"), code(ex.context_html, "html"));
      c.append(code(ex.code, ex.language));
      if (ex.expected_error) c.append(h("div", { class: "out err" }, h("b", {}, "エラーになります: "), ex.expected_error));
      else if (ex.language === "javascript" || (!ex.preview && ex.expected_output)) c.append(h("div", { class: "out" }, h("div", { class: "out-label" }, C.ui.run_output_label), h("pre", {}, ex.expected_output)));
      if (ex.preview) c.append(previewBlock(Object.assign({ student: ex.code, given_html: ex.preview.given_html || "" }, ex.preview)));
      c.append(h("ul", { class: "notes" }, ex.line_notes.map((n) => h("li", {}, n))));
    });
    root.append(c);
    if (last) {
      const m = h("div", { class: "card" }, h("h3", {}, "よくある間違い"));
      L.common_mistakes.forEach((x) =>
        m.append(h("div", { class: "mistake" }, h("b", {}, x.title), code(x.wrong_code), h("p", {}, "理由: " + x.why), h("p", {}, "直し方: " + x.fix)))
      );
      m.append(h("h3", {}, "理解度チェック"), h("ul", { class: "check" }, L.checkpoints.map((x) => h("li", {}, x))), para(L.next_bridge));
      root.append(m);
    }
    const nav = h("div", { class: "actions" });
    if (idx > 0) nav.append(link(H("lesson/" + sid + "/" + (idx - 1)), "← 前へ", "btn"));
    if (!last) nav.append(link(H("lesson/" + sid + "/" + (idx + 1)), "次へ →", "btn primary"));
    else nav.append(link(H("q/" + sid + "/" + firstUnanswered(sid)), "問題を解く →", "btn primary"));
    if (!last) nav.append(link(H("q/" + sid + "/" + firstUnanswered(sid)), "レッスンをスキップして問題へ", "btn ghost"));
    root.append(nav);
    return root;
  }
  function firstUnanswered(sid) {
    const a = ss(sid).answers;
    const q = qByStage[sid].find((x) => !a[x.id]);
    return q ? q.number_in_stage : 1;
  }
  function crumb(s, tail) {
    return h("nav", { class: "crumb", "aria-label": "現在地" }, link("#/", "コース選択"), " › ", link(H(), C.curriculum.course.language_display_name), " › ", "ステージ" + s.number + " " + s.title, tail ? " › " + tail : "");
  }

  /* ---------- (3)(4) 問題回答とフィードバック ---------- */
  function shuffled(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  }
  function record(sid, q, correct, last) {
    const a = ss(sid).answers;
    if (!a[q.id]) a[q.id] = { firstCorrect: correct, tries: 1, last: last };
    else { a[q.id].tries += 1; a[q.id].last = last; }
    save();
    return a[q.id];
  }

  /* コード作成の採点: エンジンはコースごとに違う（engine がなければ Python） */
  function gradeCodeFor(q, student) { return q.grading.engine ? WebRunner.grade(q, student) : PyRunner.gradeCode(q, student); }
  /* 表示・動きに関わる問題で、正しい答えを実際に表示するための指定（なければ null） */
  function previewForQuestion(q) {
    const ck = q.check;
    if (!ck || q.type === "code_write" || ck.format === "javascript") return null;
    let student;
    if (q.type === "predict_output") student = q.code;
    else if (q.type === "fill_blank") student = q.answer.blanks.reduce((c, b) => c.split(b.marker).join(b.accepted[0]), q.code);
    else if (q.type === "bug_fix") student = q.answer.fixed_code;
    else return null;
    return { format: ck.format, given_html: ck.given_html || "", student: student, viewport: ck.viewport };
  }

  function viewQuestion(sid, no) {
    const s = stageById[sid];
    if (!s) return viewStages();
    if (!unlocked(s)) return h("div", { class: "card" }, para("このステージはまだ開いていません。"), link(H(), "ステージ一覧へ"));
    const q = qByStage[sid][no - 1];
    if (!q) return viewResult(sid);
    const root = h("div", {});
    root.append(crumb(s, "問題 " + no + "/10"));
    root.append(h("div", { class: "meter big", role: "img", "aria-label": no + "問目/10問" }, h("span", { style: "width:" + (no - 1) * 10 + "%" })));

    const card = h("div", { class: "card question" });
    card.append(
      h("div", { class: "qmeta" },
        h("span", { class: "tag" }, q.id),
        h("span", { class: "tag" }, TYPE_JA[q.type]),
        h("span", { class: "tag", title: "難易度" }, "難易度 " + "●".repeat(q.difficulty) + "○".repeat(5 - q.difficulty))
      ),
      h("h2", {}, q.title)
    );
    q.prompt.split("\n").forEach((line) => card.append(line ? para(line.replace(/__(\d+)__/g, "【空欄$1】")) : h("div", { class: "gap" })));
    // HTML/CSS・DOM操作の問題: あらかじめ用意された HTML を、コードの前に見せる
    if (q.context_html && q.type !== "code_write") card.append(h("p", { class: "small muted" }, "HTML（あらかじめ用意されています）"), code(q.context_html, "html"));

    /* 回答UI（read: 回答の取得, lock: 入力の固定, mark: 結果の装飾） */
    const ui = buildAnswerUI(q);
    card.append(ui.node);

    const hintBox = h("div", { class: "hint", hidden: true }, h("b", {}, "ヒント: "), q.hint);
    const fb = h("div", { class: "feedback", "aria-live": "polite" });
    const actions = h("div", { class: "actions" });
    const hintBtn = h("button", { class: "btn ghost", type: "button", onclick: () => { hintBox.hidden = !hintBox.hidden; } }, "ヒント");
    const lessonBtn = link(H("lesson/" + sid + "/0"), "教科書を見る", "btn ghost");
    let submitBtn, fallbackBtn, runBtn;

    function nextTarget() { return no < 10 ? H("q/" + sid + "/" + (no + 1)) : H("result/" + sid); }

    function showFeedback(correct, info) {
      fb.replaceChildren();
      fb.className = "feedback " + (correct ? "ok" : "ng");
      fb.append(h("div", { class: "verdict" }, h("span", { class: "icon", "aria-hidden": "true" }, correct ? "○" : "×"), correct ? q.feedback_correct : q.feedback_incorrect));
      if (info.note) fb.append(h("p", { class: "small muted" }, info.note));
      if (!correct && info.shown) fb.append(h("div", { class: "answers" }, h("div", {}, h("b", {}, "あなたの回答: "), info.shown), h("div", {}, h("b", {}, "正解: "), info.right)));
      if (correct && info.right) fb.append(h("div", { class: "answers" }, h("div", {}, h("b", {}, "正解: "), info.right)));
      if (info.reason) fb.append(h("div", { class: "reason" }, h("b", {}, "この答えが違う理由: "), info.reason));
      fb.append(h("div", { class: "why" }, h("b", {}, "正解の根拠: "), q.rationale), h("div", { class: "expl" }, h("b", {}, "解説"), para(q.explanation)));
      if (info.extra) fb.append(info.extra);
      const pv = previewForQuestion(q);
      if (pv) {
        // 表示・動きの問題では、正しい答えの実際の表示（操作もできる）を、見られるようにする
        const d = h("details", { class: "actual" }, h("summary", {}, "実際の表示を見る"));
        d.addEventListener("toggle", () => { if (d.open && !d.dataset.done) { d.dataset.done = "1"; d.append(previewBlock(pv, "正しい答えのときの、実際の表示（操作できます）")); } });
        fb.append(d);
      }
      const row = h("div", { class: "actions" });
      if (!correct && (info.retry || info.retryFn)) row.append(h("button", { class: "btn", type: "button", onclick: info.retryFn || (() => render()) }, "もう一度挑戦"));
      row.append(link(nextTarget(), no < 10 ? "次の問題へ →" : "結果を見る →", "btn primary"));
      fb.append(row);
      fb.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }

    if (q.type === "code_write") {
      /* 採点は、コースに応じた隔離環境で test_cases を実行する:
       *   Python = Pyodide（Web Worker） / JavaScript = Web Worker / HTML・CSS・DOM操作 = sandbox 付き iframe */
      const isPy = !q.grading.engine;
      const status = h("p", { class: "small muted", role: "status" }, isPy ? "Python を準備しています…（初回のみ数秒かかります）" : (q.grading.engine === "js_worker" ? "JavaScript は、ブラウザの中の隔離された環境（Web Worker）で実行して採点します。" : "HTML・CSS・DOM操作のコードは、隔離された iframe に読み込んで、表示や動きを調べて採点します。"));
      const runOut = h("div", { class: "runout", hidden: true });
      submitBtn = h("button", { class: "btn primary", type: "button", disabled: isPy, onclick: () => autoGrade() }, C.ui.write_button);
      runBtn = h("button", { class: "btn", type: "button", disabled: isPy, onclick: () => tryIt() }, q.grading.engine === "page" && C.key === "js" ? "プレビューして試す" : C.ui.run_button);
      if (isPy) fallbackBtn = h("button", { class: "btn ghost", type: "button", hidden: true, onclick: () => { fallbackBtn.hidden = true; reveal(); } }, "自己採点に切り替える");
      ui.node.append(status, runOut);
      if (isPy) {
        PyRunner.ready().then((v) => {
          status.textContent = "Python " + v.python + " の準備ができました（Pyodide " + v.pyodide + "）";
          submitBtn.disabled = false; runBtn.disabled = false;
        }).catch((e) => {
          status.textContent = "Python を読み込めませんでした（" + e.message + "）。ネットワークを確認するか、自己採点に切り替えてください。";
          fallbackBtn.hidden = false;
        });
      }

      async function tryIt() {
        runBtn.disabled = true; submitBtn.disabled = true;
        runOut.hidden = false;
        const student = ui.read();
        if (q.grading.engine === "page") {
          // HTML / CSS / DOM操作: 実際に表示して見せる（操作もできる）
          runOut.replaceChildren(previewBlock({ format: q.answer_format, given_html: q.prefix_html || "", student: student, viewport: q.grading.viewport }, "プレビュー（実際に操作できます）"));
        } else {
          runOut.replaceChildren(h("p", { class: "small muted" }, "実行中…"));
          let r;
          if (q.grading.engine === "js_worker") {
            const w = await WebRunner.runJs(student, { setup: q.prefix_code || "", timeoutMs: (q.grading.timeout_sec || 3) * 1000 });
            r = { out: w.logs.join("\n"), error: w.timeout ? "時間切れ（無限ループの可能性があります）" : (w.error ? w.error.name + ": " + w.error.message : null) };
          } else r = await PyRunner.tryRun(q, student);
          const hintNone = q.grading.engine === "js_worker" ? "（出力はありません。関数を作る問題では、自分で console.log(関数名(...)) を書いて試せます）" : "（出力はありません。関数を作る問題では、自分で print(関数名(...)) を書いて試せます）";
          runOut.replaceChildren(
            h("div", { class: "out" }, h("div", { class: "out-label" }, C.ui.run_output_label), h("pre", {}, r.out || (r.error ? "" : hintNone))),
            r.error ? h("div", { class: "out err" }, h("b", {}, "エラー: "), r.error) : null
          );
        }
        runBtn.disabled = false; submitBtn.disabled = false;
      }

      async function autoGrade() {
        const student = ui.read();
        if (!student.trim()) { fb.className = "feedback"; fb.replaceChildren(h("p", { class: "small muted" }, "コードを書いてから「回答する」を押してください。")); return; }
        submitBtn.disabled = true; runBtn.disabled = true;
        fb.className = "feedback";
        fb.replaceChildren(h("p", { class: "small muted", role: "status" }, "採点しています…"));
        const g = await gradeCodeFor(q, student);
        record(sid, q, g.correct, "code");
        const a = q.answer;
        const lang = q.code_language;
        const rows = h("ul", { class: "tests" });
        let hiddenTotal = 0, hiddenOk = 0;
        g.results.forEach((r, i) => {
          if (!r.t.visible) { hiddenTotal += 1; if (r.ok) hiddenOk += 1; return; }
          const label = r.t.kind === "page" ? r.t.desc
            : r.t.kind === "stdout" ? "出力を確かめる" + (r.t.setup ? "（前提: " + r.t.setup.replace(/\n/g, "; ") + "）" : "")
            : r.t.call + " の結果";
          const li = h("li", { class: r.ok ? "t-ok" : "t-ng" }, h("b", {}, (r.ok ? "✓ " : "✗ ") + label));
          if (!r.ok) {
            if (r.error) li.append(h("div", { class: "small" }, "エラー: " + r.error));
            else if (r.t.kind === "page") li.append(h("div", { class: "small" }, "この条件を満たしていません。" + (r.pageErrors && r.pageErrors.length ? "（ページで起きたエラー: " + r.pageErrors.join(" / ") + "）" : "")));
            else if (r.t.kind === "stdout") li.append(h("div", { class: "small" }, "期待:"), h("pre", { class: "inline-pre" }, r.t.expected_stdout), h("div", { class: "small" }, "実際:"), h("pre", { class: "inline-pre" }, r.actual || "（出力なし）"));
            else li.append(h("div", { class: "small" }, "期待: " + r.t.expected + " ／ 実際: " + r.actual));
          }
          rows.append(li);
        });
        const detail = h("div", { class: "testdetail" });
        if (g.staticMessage) detail.append(h("div", { class: "out err" }, g.staticMessage));
        if (rows.children.length) detail.append(h("b", {}, "テスト結果"), rows);
        if (hiddenTotal) detail.append(h("p", { class: "small" }, "非公開テスト: " + hiddenOk + "/" + hiddenTotal + " 合格" + (hiddenOk < hiddenTotal ? (isPy ? "（別の入力でも確かめてみましょう。例: 0・1つだけ・大きな値）" : "（別の条件でも確かめてみましょう。例: 入力の値、データの数、画面の幅、操作の順番）") : "")));
        detail.append(h("details", {},
          h("summary", {}, g.correct ? "模範解答・別解・よくある不合格例を見る" : "模範解答を見る（見る前に、もう一度自分で考えてみましょう）"),
          h("b", {}, "模範解答"), code(a.reference_solution, lang),
          a.alternative_solutions.length ? [h("b", {}, "別解（これも正解です）"), a.alternative_solutions.map((c) => code(c, lang))] : null,
          g.correct ? [h("b", {}, "こう書くと不合格になります"), a.rejected_examples.map((r) => h("div", {}, code(r.code, lang), h("p", { class: "small" }, "理由: " + r.reason)))] : null
        ));
        showFeedback(g.correct, {
          extra: detail,
          retryFn: () => { fb.className = "feedback"; fb.replaceChildren(); submitBtn.disabled = false; runBtn.disabled = false; },
        });
        if (g.correct) { ui.lock(); hintBtn.disabled = true; }
        else { submitBtn.disabled = false; runBtn.disabled = false; }
      }

      function reveal() {
        ui.lock();
        submitBtn.disabled = true; runBtn.disabled = true;
        const a = q.answer;
        const wrap = h("div", { class: "feedback selfcheck" },
          h("div", { class: "verdict" }, "模範解答と見比べましょう"),
          h("p", { class: "small muted" }, "この環境では Python を実行できないため、自己採点です。"),
          h("b", {}, "模範解答"), code(a.reference_solution),
          a.alternative_solutions.length ? h("details", {}, h("summary", {}, "別解（これも正解です）"), a.alternative_solutions.map(code)) : null,
          h("details", {}, h("summary", {}, "よくある不合格例"), a.rejected_examples.map((r) => h("div", {}, code(r.code), h("p", { class: "small" }, "理由: " + r.reason)))),
          h("details", {}, h("summary", {}, "テストケース"), h("ul", {}, q.grading.tests.map((t) => h("li", {}, t.visible ? (t.kind === "stdout" ? "出力が " + JSON.stringify(t.expected_stdout) + (t.setup ? "（前提: " + t.setup.replace(/\n/g, "; ") + "）" : "") : t.call + " → " + t.expected) : "（非公開テスト）")))),
          h("div", { class: "why" }, h("b", {}, "正解の根拠: "), q.rationale), h("div", { class: "expl" }, h("b", {}, "解説"), para(q.explanation)),
          h("p", {}, "自分のコードはどうでしたか？"),
          h("div", { class: "actions" },
            h("button", { class: "btn primary", type: "button", onclick: () => selfGrade(true) }, "できた"),
            h("button", { class: "btn", type: "button", onclick: () => selfGrade(false) }, "できなかった"))
        );
        card.append(wrap);
        wrap.scrollIntoView({ block: "nearest", behavior: "smooth" });
        function selfGrade(ok) {
          record(sid, q, ok, "self");
          wrap.querySelector(".actions").replaceWith(h("div", { class: "actions" }, h("span", { class: "muted" }, ok ? "「" + q.feedback_correct + "」" : "「" + q.feedback_incorrect + "」"), link(nextTarget(), no < 10 ? "次の問題へ →" : "結果を見る →", "btn primary")));
        }
      }
    } else {
      submitBtn = h("button", { class: "btn primary", type: "button", onclick: () => submit() }, "回答する");
      function submit() {
        const ans = ui.read();
        if (ans === null) { fb.replaceChildren(h("p", { class: "small muted" }, "答えを入力・選択してから「回答する」を押してください。")); return; }
        const correct = Grader.grade(q, ans);
        record(sid, q, correct, ans);
        ui.lock();
        submitBtn.disabled = true;
        hintBtn.disabled = true;
        const info = ui.describe(ans, correct);
        showFeedback(correct, info);
      }
    }
    actions.append(submitBtn);
    if (runBtn) actions.append(runBtn);
    actions.append(hintBtn, lessonBtn);
    if (fallbackBtn) actions.append(fallbackBtn);
    card.append(hintBox, actions, fb);
    root.append(card);
    return root;
  }

  /* 回答UIを問題の answer_mode / type に応じて作る */
  function buildAnswerUI(q) {
    if (q.answer_mode === "choice") return choiceUI(q);
    if (q.type === "fill_blank") return fillUI(q);
    if (q.type === "predict_output") return predictUI(q);
    if (q.type === "bug_fix") return bugfixTextUI(q);
    if (q.type === "code_write") return codeUI(q);
    throw new Error("unsupported question UI: " + q.id);
  }

  function choiceUI(q) {
    const node = h("div", {});
    if (q.code) node.append(code(q.code, q.code_language));
    const group = h("div", { class: "choices", role: "radiogroup", "aria-label": "選択肢" });
    const letters = ["A", "B", "C"];
    shuffled(q.choices).forEach((c, i) => {
      const input = h("input", { type: "radio", name: "choice", value: c.id });
      group.append(h("label", { class: "choice", "data-id": c.id }, input, h("span", { class: "letter" }, letters[i]),
        h("span", { class: "ctext" + (q.choice_format === "code" || c.text.includes("\n") ? " mono" : "") }, c.text)));
    });
    node.append(group);
    return {
      node,
      read: () => { const r = group.querySelector("input:checked"); return r ? r.value : null; },
      lock: () => group.querySelectorAll("input").forEach((i) => (i.disabled = true)),
      describe: (ans, correct) => {
        group.querySelectorAll(".choice").forEach((l) => {
          if (l.dataset.id === q.answer.correct_choice_id) l.classList.add("right");
          else if (l.dataset.id === ans) l.classList.add("wrong");
        });
        const text = (id) => q.choices.find((c) => c.id === id).text;
        return { shown: text(ans), right: text(q.answer.correct_choice_id), reason: correct ? null : q.wrong_answer_reasons[ans], retry: true };
      },
    };
  }

  function fillUI(q) {
    const node = h("div", {});
    const pre = h("pre", { class: "code fill" });
    const inputs = {};
    q.code.split(/(__\d+__)/).forEach((part) => {
      const m = part.match(/^__(\d+)__$/);
      if (!m) { pre.append(part); return; }
      const id = "b" + m[1];
      const b = q.answer.blanks.find((x) => x.id === id);
      const width = Math.max(6, ...b.accepted.map((x) => x.length)) + 2;
      const input = h("input", { class: "blank", type: "text", autocomplete: "off", autocapitalize: "off", spellcheck: "false", style: "width:" + width + "ch", "aria-label": "空欄" + m[1] });
      inputs[id] = input;
      pre.append(input);
    });
    node.append(pre, h("p", { class: "small muted" }, "半角で入力してください（全角は自動で半角として判定します）。"));
    return {
      node,
      read: () => { const v = {}; let any = false; for (const [id, el] of Object.entries(inputs)) { v[id] = el.value; if (el.value.trim()) any = true; } return any ? v : null; },
      lock: () => Object.values(inputs).forEach((i) => (i.disabled = true)),
      describe: (ans, correct) => {
        q.answer.blanks.forEach((b) => {
          const ok = b.accepted.some((x) => Grader.normAnswer(x, b.quote_insensitive) === Grader.normAnswer(ans[b.id] || "", b.quote_insensitive));
          inputs[b.id].classList.add(ok ? "right" : "wrong");
        });
        const fmt = (o) => q.answer.blanks.map((b, i) => "空欄" + (i + 1) + " = " + (o[b.id] === undefined ? "" : o[b.id])).join(" ／ ");
        const rightObj = {};
        q.answer.blanks.forEach((b) => (rightObj[b.id] = b.accepted[0]));
        return { shown: fmt(ans), right: fmt(rightObj) + (q.answer.blanks.some((b) => b.accepted.length > 1) ? "（他の書き方も正解）" : ""), reason: correct ? null : Grader.matchMistake(q, ans), note: correct ? null : null, retry: true };
      },
    };
  }

  function predictUI(q) {
    const node = h("div", {});
    if (q.code) node.append(code(q.code, q.code_language));
    const ta = h("textarea", { class: "answer-ta", rows: Math.min(6, Math.max(2, q.answer.expected_output.split("\n").length + 1)), "aria-label": "答え", spellcheck: "false", placeholder: "答えを入力（複数行は改行して入力）" });
    node.append(ta, h("p", { class: "small muted" }, "行末の空白や末尾の改行は無視されます。大文字小文字・空白・記号は区別されます。"));
    return {
      node,
      read: () => (ta.value.trim() ? ta.value : null),
      lock: () => (ta.disabled = true),
      describe: (ans, correct) => {
        ta.classList.add(correct ? "right" : "wrong");
        return { shown: h("pre", { class: "inline-pre" }, ans), right: h("pre", { class: "inline-pre" }, q.answer.expected_output), reason: correct ? null : Grader.matchMistake(q, ans), retry: true };
      },
    };
  }

  function bugfixTextUI(q) {
    const node = h("div", {});
    const lines = q.code.split("\n");
    const tl = q.answer.target_line;
    const pre = h("pre", { class: "code fill" });
    let input;
    lines.forEach((ln, i) => {
      if (i + 1 === tl) {
        const indent = ln.match(/^\s*/)[0];
        const width = Math.max(10, ...q.answer.accepted.map((x) => x.length)) + 4;
        input = h("input", { class: "blank wide", type: "text", autocomplete: "off", autocapitalize: "off", spellcheck: "false", style: "width:" + width + "ch", "aria-label": tl + "行目を書き直す", value: ln.trim() });
        pre.append(indent, input);
      } else pre.append(ln);
      if (i < lines.length - 1) pre.append("\n");
    });
    node.append(pre, h("p", { class: "small muted" }, tl + "行目だけを書き直してください（字下げは自動で付きます）。"));
    return {
      node,
      read: () => (input.value.trim() ? input.value : null),
      lock: () => (input.disabled = true),
      describe: (ans, correct) => {
        input.classList.add(correct ? "right" : "wrong");
        return { shown: ans, right: q.answer.accepted[0] + (q.answer.accepted.length > 1 ? "（他の書き方も正解）" : ""), reason: correct ? null : Grader.matchMistake(q, ans), retry: true, extra: h("div", {}, h("b", {}, "直したコード全体"), code(q.answer.fixed_code, q.code_language)) };
      },
    };
  }

  function codeUI(q) {
    const node = h("div", {});
    if (q.prefix_code) node.append(h("p", { class: "small muted" }, "あらかじめ用意されているコード（変更不可）:"), code(q.prefix_code, q.code_language));
    if (q.prefix_html) node.append(h("p", { class: "small muted" }, "あらかじめ用意されている HTML（変更不可）:"), code(q.prefix_html, "html"));
    const ta = h("textarea", { class: "answer-ta mono", rows: 8, "aria-label": "コード", spellcheck: "false", value: q.starter_code });
    ta.value = q.starter_code;
    node.append(ta);
    return { node, read: () => ta.value, lock: () => (ta.readOnly = true), describe: () => ({}) };
  }

  /* ---------- (5) ステージ結果 ---------- */
  function viewResult(sid) {
    const s = stageById[sid];
    if (!s) return viewStages();
    const st = ss(sid);
    const n = correctCount(sid);
    const done = answeredCount(sid);
    const root = h("div", {});
    root.append(crumb(s, "結果"));
    if (done < 10) {
      root.append(h("div", { class: "card" }, h("h2", {}, "まだ全問に回答していません"), para("回答済み " + done + "/10 問。残りの問題に回答すると結果が出ます。"), link(H("q/" + sid + "/" + firstUnanswered(sid)), "続きの問題へ", "btn primary")));
      return root;
    }
    const clear = n >= REQUIRED;
    const stars = starsFor(n);
    if (clear) { st.cleared = true; st.bestStars = Math.max(st.bestStars, stars); save(); }
    const missed = qByStage[sid].filter((q) => !st.answers[q.id].firstCorrect);
    root.append(
      h("div", { class: "card result " + (clear ? "ok" : "ng") },
        h("h2", {}, clear ? "ステージクリア！" : "あと少し！もう一度挑戦しましょう"),
        h("div", { class: "bigstars", "aria-label": "星" + stars }, "★".repeat(stars) + "☆".repeat(3 - stars)),
        h("p", { class: "score" }, "1回目の正解 ", h("b", {}, n + "/10"), " 問"),
        para("クリア条件: 1回目の回答で" + REQUIRED + "問以上正解（★" + STARS["1"] + "問 / ★★" + STARS["2"] + "問 / ★★★" + STARS["3"] + "問）。再挑戦での正解は数えません。"),
        clear && s.number < 10 ? para("次のステージ「" + stages[s.number].title + "」が開きました。") : null
      )
    );
    if (missed.length) {
      root.append(h("div", { class: "card" }, h("h3", {}, "復習しよう（1回目に間違えた問題）"),
        h("ul", { class: "missed" }, missed.map((q) => h("li", {}, link(H("q/" + sid + "/" + q.number_in_stage), q.number_in_stage + ". " + q.title), h("span", { class: "muted small" }, " — " + q.concepts.join("、")))))));
    }
    const actions = h("div", { class: "actions" });
    if (clear && s.number < 10) actions.append(link(H("lesson/S" + String(s.number + 1).padStart(2, "0") + "/0"), "次のステージへ →", "btn primary"));
    actions.append(
      h("button", { class: "btn" + (clear ? "" : " primary"), type: "button", onclick: () => {
        if (!confirm("このステージの回答をリセットして、最初からやり直しますか？（クリア済みの記録は残ります）")) return;
        st.answers = {}; st.attempts += 1; save(); go(H("lesson/" + sid + "/0"));
      } }, "このステージをやり直す"),
      link(H(), "ステージ一覧へ", "btn ghost")
    );
    root.append(actions);
    return root;
  }

  /* ---------- 開発用: コード作成の採点テスト（#/selftest） ----------
   * 13問それぞれについて、模範解答・別解は合格、初期コード・不合格例は不合格になることを Pyodide 上で確認する。 */
  function viewSelfTest() { return C.key === "py" ? viewSelfTestPy() : viewSelfTestWeb(); }

  /* JavaScript / HTML・CSS コース: 全コード作成問題の模範解答・別解・不合格例・初期コードの判定と、隔離・制限の動作を確認する */
  function viewSelfTestWeb() {
    const root = h("div", {}, h("h1", {}, "コード採点の自己テスト（" + C.curriculum.course.language_display_name + "）"),
      para("全コード作成問題の、模範解答・別解・不合格例・初期コードを、実際に採点して、期待どおりの結果になるかを確認します。"));
    const status = h("p", { role: "status" }, "確認しています…");
    const table = h("table", { class: "tbl" }, h("thead", {}, h("tr", {}, ["問題", "ケース", "期待", "結果", "判定"].map((t) => h("th", {}, t)))));
    const tb = h("tbody", {});
    table.append(tb);
    const summary = h("p", { class: "score", id: "selftest-summary" });
    const extraBtn = h("button", { class: "btn", type: "button", disabled: true }, "隔離・制限のテストも実行（数秒）");
    const extra = h("div", { id: "selftest-extra" });
    root.append(status, summary, h("div", { class: "scroll" }, table), h("div", { class: "actions" }, extraBtn), extra);
    const add = (q, name, expect, got, ok) =>
      tb.append(h("tr", { class: ok ? "" : "t-ng" }, h("td", {}, q), h("td", {}, name), h("td", {}, expect ? "合格" : "不合格"), h("td", {}, got ? "合格" : "不合格"), h("td", {}, ok ? "OK" : "NG")));
    const writes = questions.filter((x) => x.type === "code_write");
    (async () => {
      let n = 0, bad = 0;
      for (const q of writes) {
        const cases = [["初期コード", q.starter_code, false], ["模範解答", q.answer.reference_solution, true]]
          .concat(q.answer.alternative_solutions.map((c, i) => ["別解" + (i + 1), c, true]))
          .concat(q.answer.rejected_examples.map((r, i) => ["不合格例" + (i + 1), r.code, false]));
        for (const [name, code, expect] of cases) {
          const g = await gradeCodeFor(q, code);
          n += 1; if (g.correct !== expect) bad += 1;
          add(q.id, name, expect, g.correct, g.correct === expect);
        }
      }
      status.textContent = "完了";
      summary.textContent = "結果: " + n + " 件中 " + (n - bad) + " 件が期待どおり（NG " + bad + " 件）";
      extraBtn.disabled = false;
    })();
    extraBtn.addEventListener("click", async () => {
      extraBtn.disabled = true;
      extra.replaceChildren(para("実行中…"));
      const isJs = C.key === "js";
      const cases = [];
      if (isJs) {
        const q = writes[0];
        cases.push(["無限ループは時間切れになる（Worker を強制終了）", async () => (await WebRunner.runJs("while (true) {}", { timeoutMs: 500 })).timeout === true]);
        cases.push(["時間切れのあとも、正しいコードは合格する", async () => (await gradeCodeFor(q, q.answer.reference_solution)).correct === true]);
        cases.push(["Worker の中では fetch（外部通信）が使えない", async () => (await WebRunner.runJs("console.log(typeof fetch)")).logs[0] === "undefined"]);
        cases.push(["Worker の中では document（画面）に触れない", async () => (await WebRunner.runJs("console.log(typeof document)")).logs[0] === "undefined"]);
        cases.push(["大量出力は 64KB で打ち切られる", async () => { const r = await WebRunner.runJs("for (let i = 0; i < 1000000; i++) console.log('x'.repeat(100));"); return !!r.error && /長すぎ/.test(r.error.message); }]);
      }
      const pageProbe = async (student, expr, fmt) => {
        const r = await WebRunner.runPage({ format: fmt || "html_body", student: student, exprs: [expr], timeoutMs: 4000 });
        return !r.timeout && WebRunner.truthy(r.values[0]);
      };
      cases.push(["iframe の中から、親のページ（parent.document）に触れない", () => pageProbe("<p>x</p>", "(function () { try { parent.document.title; return false; } catch (e) { return true; } })()")]);
      cases.push(["iframe の中から、localStorage（学習の記録）に触れない", () => pageProbe("<p>x</p>", "(function () { try { localStorage.getItem('pypath.v1'); return false; } catch (e) { return true; } })()")]);
      cases.push(["iframe の中のスクリプトの無限ループは、時間切れで打ち切られる", async () => { const r = await WebRunner.runPage({ format: "javascript_dom", given_html: "<p>x</p>", student: "while (true) {}", exprs: ["true"], timeoutMs: 1500 }); return r.timeout === true; }]);
      const t2 = h("table", { class: "tbl" }, h("thead", {}, h("tr", {}, ["確認項目", "判定"].map((t) => h("th", {}, t)))));
      let badX = 0;
      for (const [name, fn] of cases) {
        let ok = false;
        try { ok = !!(await fn()); } catch (e) { ok = false; }
        if (!ok) badX += 1;
        t2.append(h("tr", { class: ok ? "" : "t-ng" }, h("td", {}, name), h("td", {}, ok ? "OK" : "NG")));
      }
      extra.replaceChildren(h("p", { class: "score", id: "selftest-extra-summary" }, "隔離・制限の確認: " + (cases.length - badX) + "/" + cases.length + " 件OK"), h("div", { class: "scroll" }, t2));
    });
    return root;
  }

  function viewSelfTestPy() {
    const root = h("div", {}, h("h1", {}, "コード採点の自己テスト"), para("Pyodide 上で、全コード作成問題の模範解答・別解・不合格例・初期コードを採点して、期待どおりの結果になるかを確認します。"));
    const status = h("p", { role: "status" }, "Python を準備しています…");
    const table = h("table", { class: "tbl" }, h("thead", {}, h("tr", {}, ["問題", "ケース", "期待", "結果", "判定"].map((t) => h("th", {}, t)))));
    const tb = h("tbody", {});
    table.append(tb);
    const summary = h("p", { class: "score", id: "selftest-summary" });
    const timeoutBtn = h("button", { class: "btn", type: "button", disabled: true }, "時間切れ・禁止機能のテストも実行（約10秒）");
    const extra = h("div", { id: "selftest-extra" });
    root.append(status, summary, h("div", { class: "scroll" }, table), h("div", { class: "actions" }, timeoutBtn), extra);
    const add = (q, name, expect, got, ok) =>
      tb.append(h("tr", { class: ok ? "" : "t-ng" }, h("td", {}, q), h("td", {}, name), h("td", {}, expect ? "合格" : "不合格"), h("td", {}, got ? "合格" : "不合格"), h("td", {}, ok ? "OK" : "NG")));
    (async () => {
      let info;
      try { info = await PyRunner.ready(); } catch (e) { status.textContent = "Python を読み込めませんでした: " + e.message; return; }
      status.textContent = "Python " + info.python + "（Pyodide " + info.pyodide + "）で実行中…";
      let n = 0, bad = 0;
      for (const q of questions.filter((x) => x.type === "code_write")) {
        const cases = [["初期コード", q.starter_code, false], ["模範解答", q.answer.reference_solution, true]]
          .concat(q.answer.alternative_solutions.map((c, i) => ["別解" + (i + 1), c, true]))
          .concat(q.answer.rejected_examples.map((r, i) => ["不合格例" + (i + 1), r.code, false]));
        for (const [name, code, expect] of cases) {
          const g = await PyRunner.gradeCode(q, code);
          n += 1; if (g.correct !== expect) bad += 1;
          add(q.id, name, expect, g.correct, g.correct === expect);
        }
      }
      status.textContent = "Python " + info.python + "（Pyodide " + info.pyodide + "）";
      summary.textContent = "結果: " + n + " 件中 " + (n - bad) + " 件が期待どおり（NG " + bad + " 件）";
      timeoutBtn.disabled = false;
    })();
    timeoutBtn.addEventListener("click", async () => {
      timeoutBtn.disabled = true;
      extra.replaceChildren(para("実行中…"));
      const q = questions.find((x) => x.id === "PY-040");
      const q10 = questions.find((x) => x.id === "PY-010");
      const cases = [
        ["無限ループは時間切れで不合格", q, "n = 0\nwhile True:\n    n += 1\nfor i in range(1):\n    pass", (g) => !g.correct && g.results.some((r) => r.timeout)],
        ["時間切れの後も正しいコードは合格", q, q.answer.reference_solution, (g) => g.correct],
        ["import os は禁止", q10, "import os\nprint('こんにちは')\nprint('Python')", (g) => !g.correct && g.results.some((r) => /ImportError/.test(r.error || ""))],
        ["open は使えない", q10, "open('x')\nprint('こんにちは')\nprint('Python')", (g) => !g.correct],
        ["import js（外部通信の入口）は禁止", q10, "import js\nprint('こんにちは')\nprint('Python')", (g) => !g.correct],
        ["大量出力は64KBで打ち切り", q10, "for i in range(10**7):\n    print('x' * 100)", (g) => !g.correct && g.results.some((r) => /長すぎ/.test(r.error || ""))],
        ["random は使える", q10, "import random\nprint('こんにちは')\nprint('Python')", (g) => g.correct],
        ["テストごとに新しい名前空間（前のテストの状態を持ち越さない）", questions.find((x) => x.id === "PY-060"), "calls = []\ndef is_even(n):\n    calls.append(n)\n    return n % 2 == 0 and len(calls) == 1", (g) => g.correct],
      ];
      const t2 = h("table", { class: "tbl" }, h("thead", {}, h("tr", {}, ["確認項目", "判定"].map((t) => h("th", {}, t)))));
      let bad = 0;
      for (const [name, qq, code, check] of cases) {
        const g = await PyRunner.gradeCode(qq, code);
        const ok = !!check(g); if (!ok) bad += 1;
        t2.append(h("tr", { class: ok ? "" : "t-ng" }, h("td", {}, name), h("td", {}, ok ? "OK" : "NG")));
      }
      extra.replaceChildren(h("p", { class: "score", id: "selftest-extra-summary" }, "安全性・制限の確認: " + (cases.length - bad) + "/" + cases.length + " 件OK"), h("div", { class: "scroll" }, t2));
    });
    return root;
  }

  /* ---------- (6) 学習進捗 ---------- */
  function viewAllProgress() {
    const root = h("div", {});
    root.append(h("h1", {}, "学習進捗（すべてのコース）"));
    const tbl = h("table", { class: "tbl" }, h("thead", {}, h("tr", {}, ["コース", "クリア", "回答済み", "1回目の正答率"].map((t) => h("th", {}, t)))));
    const tb = h("tbody", {});
    COURSES.forEach((c) => {
      const s = courseStats(c);
      let right = 0;
      c.curriculum.stages.forEach((st) => { const x = courseState(c.key).stages[st.id]; if (x) right += Object.values(x.answers).filter((a) => a.firstCorrect).length; });
      tb.append(h("tr", {}, h("td", {}, link("#/" + c.key + "/progress", c.curriculum.course.title)), h("td", {}, s.cleared + "/10"), h("td", {}, s.done + "/" + s.total), h("td", {}, s.done ? Math.round((right / s.done) * 100) + "%" : "—")));
    });
    tbl.append(tb);
    root.append(h("div", { class: "card" }, h("div", { class: "scroll" }, tbl)));
    root.append(h("div", { class: "actions" }, link("#/", "コース選択へ", "btn"), h("button", { class: "btn ghost danger", type: "button", onclick: () => {
      if (!confirm("すべてのコースの学習の記録を消します。よろしいですか？")) return;
      state = fresh(); save(); go("#/"); render();
    } }, "すべての学習データを消去")));
    return root;
  }
  function viewProgress() {
    const root = h("div", {});
    root.append(h("nav", { class: "crumb", "aria-label": "現在地" }, link("#/", "コース選択"), " › ", link(H(), C.curriculum.course.language_display_name), " › 学習進捗"));
    root.append(h("h1", {}, "学習進捗（" + C.curriculum.course.language_display_name + "）"));
    const done = stages.reduce((n, s) => n + answeredCount(s.id), 0);
    const right = stages.reduce((n, s) => n + correctCount(s.id), 0);
    root.append(h("div", { class: "card" },
      h("p", {}, "クリアしたステージ: ", h("b", {}, stages.filter((s) => ss(s.id).cleared).length + "/10")),
      h("p", {}, "回答済みの問題: ", h("b", {}, done + "/" + questions.length), "　1回目の正答率: ", h("b", {}, done ? Math.round((right / done) * 100) + "%" : "—")),
      link("#/progress", "すべてのコースの進捗を見る")));
    const tbl = h("table", { class: "tbl" }, h("thead", {}, h("tr", {}, ["ステージ", "回答", "1回目の正解", "星", "状態"].map((t) => h("th", {}, t)))));
    const tb = h("tbody", {});
    stages.forEach((s) => {
      const st = ss(s.id);
      tb.append(h("tr", {}, h("td", {}, link(unlocked(s) ? H("lesson/" + s.id + "/0") : H(), s.number + ". " + s.title)), h("td", {}, answeredCount(s.id) + "/10"), h("td", {}, answeredCount(s.id) ? correctCount(s.id) + "/" + answeredCount(s.id) : "—"), h("td", {}, "★".repeat(st.bestStars) || "—"), h("td", {}, st.cleared ? "クリア" : unlocked(s) ? "学習可" : "ロック")));
    });
    tbl.append(tb);
    root.append(h("div", { class: "card" }, h("h3", {}, "ステージ別"), h("div", { class: "scroll" }, tbl)));
    const conc = {};
    questions.forEach((q) => {
      const a = ss(q.stage_id).answers[q.id];
      if (!a) return;
      q.concepts.forEach((c) => { conc[c] = conc[c] || { t: 0, r: 0 }; conc[c].t += 1; if (a.firstCorrect) conc[c].r += 1; });
    });
    const rows = Object.entries(conc).sort((x, y) => x[1].r / x[1].t - y[1].r / y[1].t || y[1].t - x[1].t);
    const weak = rows.filter(([, v]) => v.r < v.t).slice(0, 6);
    root.append(h("div", { class: "card" }, h("h3", {}, "復習のおすすめ（1回目に間違えた概念）"),
      weak.length ? h("ul", {}, weak.map(([k, v]) => h("li", {}, k + "（" + v.r + "/" + v.t + "）"))) : para(rows.length ? "間違えた概念はありません。" : "問題に回答すると、ここに表示されます。")));
    root.append(h("div", { class: "actions" }, h("button", { class: "btn ghost danger", type: "button", onclick: () => {
      if (!confirm("このコースの学習の記録を消します。よろしいですか？")) return;
      state.courses[C.key] = { stages: {} }; save(); render();
    } }, "このコースの学習データを消去")));
    return root;
  }

  render();
})();
