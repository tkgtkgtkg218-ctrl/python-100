/* 自動採点（docs/05_grading_spec.md の JavaScript 実装）
 * 対応: choice_id / output_compare / accepted_answers
 * 非対応: test_cases（Python の実行環境が必要。試作では自己採点にする） */
const Grader = (function () {
  function normOutput(s) {
    const lines = String(s).replace(/\r\n/g, "\n").replace(/\r/g, "\n").split("\n").map((l) => l.trimEnd());
    while (lines.length && lines[lines.length - 1] === "") lines.pop();
    return lines.join("\n");
  }

  function normAnswer(s, quoteInsensitive) {
    let t = String(s).normalize("NFKC").trim();
    if (quoteInsensitive) t = t.replace(/'/g, '"');
    return t;
  }

  /** 回答の形: choice=選択肢ID文字列 / 穴埋め={b1:"..."} / 入力式=文字列 */
  function grade(q, answer) {
    const a = q.answer;
    switch (q.grading.method) {
      case "choice_id":
        return answer === a.correct_choice_id;
      case "output_compare":
        return normOutput(answer) === normOutput(a.expected_output);
      case "accepted_answers":
        if (q.type === "fill_blank") {
          return a.blanks.every((b) => {
            const given = normAnswer(answer[b.id] || "", b.quote_insensitive);
            return b.accepted.some((x) => normAnswer(x, b.quote_insensitive) === given);
          });
        } else {
          const qi = !!a.quote_insensitive;
          const given = normAnswer(answer, qi);
          return a.accepted.some((x) => normAnswer(x, qi) === given);
        }
      default:
        throw new Error("unsupported grading method: " + q.grading.method);
    }
  }

  /** 不正解のとき、既知のよくある誤答に一致すればその理由を返す（なければ null） */
  function matchMistake(q, answer) {
    const list = q.common_mistakes || [];
    for (const m of list) {
      if (q.type === "fill_blank") {
        const b = q.answer.blanks.find((x) => x.id === m.blank);
        if (b && normAnswer(answer[m.blank] || "", b.quote_insensitive) === normAnswer(m.answer, b.quote_insensitive)) return m.reason;
      } else if (q.type === "predict_output") {
        if (normOutput(answer) === normOutput(m.answer)) return m.reason;
      } else if (q.type === "bug_fix") {
        const qi = !!q.answer.quote_insensitive;
        if (normAnswer(answer, qi) === normAnswer(m.answer, qi)) return m.reason;
      }
    }
    return null;
  }

  function isSupported(q) {
    return q.grading.method !== "test_cases";
  }

  return { normOutput, normAnswer, grade, matchMistake, isSupported };
})();

if (typeof module !== "undefined") module.exports = Grader;
