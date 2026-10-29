// Python 参照実装との照合（src/parity_test.py から呼ばれる）
const fs = require("fs");
const path = require("path");
const Grader = require("./grader.js");
const qs = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "questions.json"), "utf8")).questions;
const byId = Object.fromEntries(qs.map((q) => [q.id, q]));
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, "parity_cases.json"), "utf8"));
let bad = 0;
for (const c of cases) {
  const got = Grader.grade(byId[c.id], c.answer);
  if (got !== c.expected) {
    bad++;
    if (bad <= 10) console.log("MISMATCH", c.id, JSON.stringify(c.answer), "py=" + c.expected, "js=" + got);
  }
}
console.log("parity mismatches:", bad);
process.exit(bad ? 1 : 0);
