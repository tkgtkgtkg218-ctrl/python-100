/* 教材データ（JavaScript / HTML・CSS コース）の機械検証。ブラウザ内で、アプリと同じ実行基盤（webrunner.js）を使って
 * 正解・誤答・別解・不合格例・レッスンの例題が、記載どおりの結果になるかを確認する。
 * 使い方: verify_web.html を開き、WebVerify.verifyQuestions(questions) / verifyExamples(lessons) を呼ぶ（src/web_verify_run.js が自動実行）。 */
const WebVerify = (function () {
  const R = WebRunner;
  const G = Grader;

  function fillCode(q, answers) {
    let code = q.code;
    q.answer.blanks.forEach((b) => { code = code.split(b.marker).join(answers[b.id]); });
    return code;
  }
  function replaceLine(code, lineNo, text) {
    const lines = code.split("\n");
    const indent = (lines[lineNo - 1].match(/^\s*/) || [""])[0];
    lines[lineNo - 1] = indent + text.trim();
    return lines.join("\n");
  }
  const jsonKey = (v) => JSON.stringify({ t: "json", v: v });

  async function consoleRun(code) {
    const r = await R.runJs(code, { timeoutMs: 3000 });
    return { out: r.logs.join("\n"), error: r.error ? r.error.name : null, message: r.error ? r.error.message : null, timeout: !!r.timeout };
  }
  async function pageEval(ck, code, expr) {
    const r = await R.runPage({ format: ck.format, given_html: ck.given_html || "", student: code, actions: ck.actions, viewport: ck.viewport, exprs: [expr], timeoutMs: 4000 });
    if (r.timeout) return { timeout: true, ok: false, raw: null, errors: [] };
    return { timeout: false, ok: R.truthy(r.values[0]), raw: r.values[0], errors: r.errors };
  }

  async function verifyQuestion(q) {
    const res = [];
    const add = (name, ok, detail) => res.push({ name: name, ok: !!ok, detail: ok ? undefined : String(detail === undefined ? "" : detail).slice(0, 300) });
    const a = q.answer;
    const ck = q.check || null;
    const norm = G.normOutput;
    try {
      if (q.type === "multiple_choice") {
        add("grader_accepts_correct", G.grade(q, a.correct_choice_id));
        q.choices.filter((c) => c.id !== a.correct_choice_id).forEach((c) => add("grader_rejects_wrong", !G.grade(q, c.id), c.id));
      } else if (q.type === "predict_output") {
        if (ck && ck.probe) {
          const r = await R.runPage({ format: ck.format, given_html: ck.given_html || "", student: q.code, actions: ck.actions, viewport: ck.viewport, exprs: [ck.probe], timeoutMs: 4000 });
          const got = r.timeout ? "TIMEOUT" : (r.values[0].ok ? JSON.stringify(r.values[0].r) : "ERR " + r.values[0].error);
          if (q.answer_mode === "choice") {
            q.choices.forEach((c) => {
              const want = jsonKey(ck.choice_values[c.id]);
              if (c.id === a.correct_choice_id) add("probe_equals_correct_choice_value", got === want, got + " vs " + want);
              else add("probe_differs_from_distractor:" + c.id, got !== want, got);
            });
          } else {
            add("probe_equals_expected", got === jsonKey(ck.expected), got + " vs " + JSON.stringify(ck.expected));
          }
        } else {
          const r = await consoleRun(q.code);
          add("code_output_equals_expected", !r.error && !r.timeout && norm(r.out) === norm(a.expected_output), JSON.stringify(r));
          if (q.answer_mode === "choice") q.choices.filter((c) => c.id !== a.correct_choice_id).forEach((c) => add("distractor_differs_from_actual:" + c.id, norm(c.text) !== norm(r.out), c.text));
          else (q.common_mistakes || []).forEach((m) => add("wrong_answer_differs_from_actual", norm(m.answer) !== norm(r.out), m.answer));
        }
        if (q.answer_mode === "choice") {
          add("grader_accepts_correct", G.grade(q, a.correct_choice_id));
          q.choices.filter((c) => c.id !== a.correct_choice_id).forEach((c) => add("grader_rejects_wrong", !G.grade(q, c.id), c.id));
        } else {
          add("grader_accepts_correct", G.grade(q, a.expected_output));
          (q.common_mistakes || []).forEach((m) => add("grader_rejects_wrong", !G.grade(q, m.answer), m.answer));
        }
      } else if (q.type === "fill_blank") {
        const blanks = a.blanks;
        const evalOk = async (code) => {
          if (ck) { const r = await pageEval(ck, code, ck.expr); return { ok: r.ok, why: JSON.stringify(r.raw) + " " + JSON.stringify(r.errors) }; }
          const r = await consoleRun(code);
          return { ok: !r.error && !r.timeout && norm(r.out) === norm(a.expected_output), why: JSON.stringify(r) };
        };
        // 許容回答をすべて（空欄ごとに1つずつ入れ替えて）実行
        const base = {}; blanks.forEach((b) => (base[b.id] = b.accepted[0]));
        const trials = [base];
        blanks.forEach((b) => b.accepted.slice(1).forEach((acc) => trials.push(Object.assign({}, base, { [b.id]: acc }))));
        for (const t of trials) { const r = await evalOk(fillCode(q, t)); add("accepted_answer_gives_expected_result", r.ok, JSON.stringify(t) + " " + r.why); }
        add("grader_accepts_correct", G.grade(q, base));
        for (const m of q.common_mistakes || []) {
          const ans = Object.assign({}, base, { [m.blank]: m.answer });
          const r = await evalOk(fillCode(q, ans));
          add("wrong_pattern_really_wrong", !r.ok, m.answer + " " + r.why);
          add("grader_rejects_wrong", !G.grade(q, ans), m.answer);
        }
      } else if (q.type === "bug_fix") {
        const good = async (code) => {
          if (ck) { const r = await pageEval(ck, code, ck.expr); return { ok: r.ok, why: JSON.stringify(r.raw) + " " + JSON.stringify(r.errors) }; }
          const r = await consoleRun(code);
          return { ok: !r.error && !r.timeout && norm(r.out) === norm(a.expected_output), why: JSON.stringify(r) };
        };
        const bad = await good(q.code);
        if (!ck && a.buggy_error) {
          const r = await consoleRun(q.code);
          const want = a.buggy_error;
          add("buggy_code_raises:" + want, want === "Timeout" ? r.timeout : r.error === want, JSON.stringify(r));
        } else if (!ck && a.buggy_output !== undefined) {
          const r = await consoleRun(q.code);
          add("buggy_output_as_documented", !r.error && norm(r.out) === norm(a.buggy_output), JSON.stringify(r));
        } else add("buggy_code_does_not_satisfy_check", !bad.ok, bad.why);
        const fixedR = await good(a.fixed_code);
        add("fixed_code_satisfies_check", fixedR.ok, fixedR.why);
        if (q.answer_mode === "text") {
          for (const acc of a.accepted) { const r = await good(replaceLine(q.code, a.target_line, acc)); add("accepted_fix_works", r.ok, acc + " " + r.why); }
          for (const m of q.common_mistakes || []) {
            const r = await good(replaceLine(q.code, a.target_line, m.answer));
            add("wrong_fix_really_wrong", !r.ok, m.answer);
            add("grader_rejects_wrong", !G.grade(q, m.answer), m.answer);
          }
          add("grader_accepts_correct", G.grade(q, a.accepted[0]));
        } else if (a.target_line) {
          for (const c of q.choices) {
            const r = await good(replaceLine(q.code, a.target_line, c.text));
            if (c.id === a.correct_choice_id) add("correct_choice_fix_works", r.ok, c.text + " " + r.why);
            else add("wrong_choice_really_wrong", !r.ok, c.text);
          }
        }
        if (q.answer_mode === "choice") add("grader_accepts_correct", G.grade(q, a.correct_choice_id));
      } else if (q.type === "code_write") {
        const run = async (code) => R.grade(q, code);
        const s = await run(q.starter_code); add("starter_code_does_not_pass", !s.correct, JSON.stringify(s.results.map((x) => x.ok)));
        const ref = await run(a.reference_solution); add("reference_solution_passes_all_tests", ref.correct, ref.staticMessage || JSON.stringify(ref.results.map((x) => [x.ok, x.error, x.actual])));
        for (let i = 0; i < a.alternative_solutions.length; i++) { const r = await run(a.alternative_solutions[i]); add("alternative_solution_passes:" + i, r.correct, r.staticMessage || JSON.stringify(r.results.map((x) => [x.ok, x.error, x.actual]))); }
        for (let i = 0; i < a.rejected_examples.length; i++) { const r = await run(a.rejected_examples[i].code); add("rejected_example_fails:" + i, !r.correct, ""); }
      }
    } catch (e) {
      add("exception", false, (e && e.stack) || e);
    }
    return { id: q.id, checks: res.length, failures: res.filter((x) => !x.ok) };
  }

  async function verifyQuestions(list) {
    const out = [];
    for (const q of list) out.push(await verifyQuestion(q));
    return out;
  }

  async function verifyExamples(lessons) {
    const out = [];
    for (const les of lessons) {
      for (const sec of les.sections) {
        for (const ex of sec.examples) {
          let ok = true, detail = "";
          try {
            if (ex.verify) {
              const spec = ex.verify;
              const r = await R.runPage({ format: spec.format, given_html: spec.given_html || "", student: ex.code, actions: spec.actions, viewport: spec.viewport, exprs: [spec.expr], timeoutMs: 4000 });
              ok = !r.timeout && R.truthy(r.values[0]) && !(r.errors && r.errors.length && !spec.allow_errors);
              if (!ok) detail = JSON.stringify(r);
            } else if (ex.language === "javascript") {
              const r = await consoleRun(ex.code);
              if (ex.expected_error) { ok = r.error === ex.expected_error; }
              else ok = !r.error && !r.timeout && Grader.normOutput(r.out) === Grader.normOutput(ex.expected_output);
              if (!ok) detail = JSON.stringify(r);
            } else { ok = false; detail = "no verification"; }
          } catch (e) { ok = false; detail = String(e); }
          out.push({ id: ex.id, ok: ok, detail: detail });
        }
      }
    }
    return out;
  }

  /** 解説・よくある間違いに書いた「こうなる」という主張の実行確認。
   *  kind: "js" → code を実行して、error（エラー名。エラーなしは null）と一致するか / kind: "page" → 読み込んで expr が true になるか */
  async function verifyClaims(list) {
    const out = [];
    for (const c of list) {
      let ok = false, detail = "";
      try {
        if (c.kind === "js") {
          const r = await consoleRun(c.code);
          ok = (r.error || null) === c.error && !r.timeout;
          if (!ok) detail = JSON.stringify(r);
        } else {
          const r = await R.runPage({ format: c.format, given_html: c.given_html || "", student: c.code, viewport: c.viewport, exprs: [c.expr], timeoutMs: 4000 });
          ok = !r.timeout && R.truthy(r.values[0]);
          if (!ok) detail = JSON.stringify(r);
        }
      } catch (e) { detail = String(e); }
      out.push({ note: c.note, ok: ok, detail: detail });
    }
    return out;
  }

  return { verifyQuestion, verifyQuestions, verifyExamples, verifyClaims };
})();
