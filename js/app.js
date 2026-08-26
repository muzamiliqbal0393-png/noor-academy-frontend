/* ===== ICT Police UDC — Screening Test Engine (Noor Academy) ===== */

const MOCK = [
  ["english-grammar", 10],
  ["english-vocabulary", 10],
  ["islamiat", 20],
  ["pakistan-studies", 15],
  ["general-knowledge", 15],
  ["current-affairs", 5],
  ["everyday-science", 10],
  ["mathematics", 10],
  ["computer-it", 5]
]; // Total = 100 MCQs (syllabus weightage ke mutabiq)
const MOCK_TIME = 90 * 60; // 90 minutes

let state = { view: "home" };
let timerInt = null;

const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function subjectById(id) { return MCQ_DATA.find(s => s.id === id); }
function fmtTime(sec) {
  const m = Math.floor(sec / 60), s = sec % 60;
  return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
}
function clearTimer() { if (timerInt) { clearInterval(timerInt); timerInt = null; } }
function getHistory() { try { return JSON.parse(localStorage.getItem("udc_test_history") || "[]"); } catch (e) { return []; } }
function saveHistory(entry) {
  const h = getHistory();
  h.unshift(entry);
  localStorage.setItem("udc_test_history", JSON.stringify(h.slice(0, 200)));
}

/* ============ HOME ============ */
function renderHome() {
  clearTimer();
  state.view = "home";
  const cards = MCQ_DATA.filter(s => s.questions.length > 0).map(s => `
    <div class="card subject-card">
      <h3>📘 ${s.name}</h3>
      <p class="count">${s.questions.length} MCQs available</p>
      <select id="sel-${s.id}" class="sel">
        <option value="10">10 Sawal (Quick)</option>
        <option value="20" selected>20 Sawal</option>
        <option value="50">50 Sawal</option>
        <option value="100">100 Sawal</option>
      </select>
      <div class="row">
        <button class="btn primary" onclick="startSubject('${s.id}', false)">✍️ Test Shuru</button>
        <button class="btn ghost" onclick="startSubject('${s.id}', true)">📖 Practice</button>
      </div>
    </div>`).join("");

  app.innerHTML = `
    <div class="hero card">
      <h2>🎯 Screening Mock Test — (Full Paper)</h2>
      <p>100 MCQs • 90 Minutes • English/Islamiat/Pak Studies/GK/Science/Math/Computer — <b>result har subject ka alag</b></p>
      <button class="btn big" onclick="startMock(false)">🚀 Mock Test Shuru Karein</button>
      <div style="margin-top:8px"><button class="btn ghost" onclick="startMock(true)">📖 Mock Practice Mode (foran jawab)</button></div>
    </div>
    <h2 class="sec-title">📚 Subject-wise Test (past paper MCQs)</h2>
    <div class="grid">${cards}</div>
    <div class="row center">
      <button class="btn gold" onclick="renderHistory()">📊 Mera Result Record</button>
    </div>`;
}

/* ============ TEST BUILD ============ */
function pickQuestions(list, n) { return shuffle(list).slice(0, Math.min(n, list.length)); }

function buildTest(questions, label, practice, timeSec, source) {
  state.test = {
    questions, label, practice, source,
    idx: 0,
    answers: Array(questions.length).fill(null),
    marked: Array(questions.length).fill(false),
    timeLeft: timeSec,
    totalTime: timeSec
  };
  startTimer();
  renderTest();
}

function startSubject(id, practice, nOverride) {
  const s = subjectById(id);
  if (!s) return;
  const sel = $("#sel-" + id);
  const n = nOverride || (sel ? parseInt(sel.value || "20", 10) : 20);
  const qs = pickQuestions(s.questions, n).map(q => ({ ...q, subject: s.name }));
  if (!qs.length) { alert("Is subject ke MCQs available nahi hain!"); return; }
  buildTest(qs, s.name, practice, Math.round(qs.length * 90), { type: "subject", id, practice });
}

function startMock(practice) {
  let qs = [];
  MOCK.forEach(([id, n]) => {
    const s = subjectById(id);
    if (!s) return;
    pickQuestions(s.questions, n).forEach(q => qs.push({ ...q, subject: s.name }));
  });
  if (!qs.length) { alert("Data load nahi hua!"); return; }
  qs = shuffle(qs);
  buildTest(qs, "Screening Mock Test (Full Paper)", practice, MOCK_TIME, { type: "mock", practice });
}

/* ============ TEST VIEW ============ */
function startTimer() {
  clearTimer();
  timerInt = setInterval(() => {
    const t = state.test;
    if (!t) return;
    t.timeLeft--;
    const el = $("#timer");
    if (el) {
      el.textContent = "⏱ " + fmtTime(Math.max(0, t.timeLeft));
      if (t.timeLeft <= 60) el.classList.add("warn");
    }
    if (t.timeLeft <= 0) { clearTimer(); submitTest(true); }
  }, 1000);
}

function renderTest() {
  const t = state.test;
  if (!t) { renderHome(); return; }
  const q = t.questions[t.idx];
  const chosen = t.answers[t.idx];

  const opts = q.o.map((opt, i) => {
    const letter = String.fromCharCode(65 + i);
    let cls = "option";
    if (t.practice && chosen) cls += (letter === q.a) ? " correct" : " wrong";
    else if (chosen === letter) cls += " chosen";
    return `<label class="${cls}"><input type="radio" name="opt" value="${letter}" ${chosen === letter ? "checked" : ""} onchange="selectOption('${letter}')"><span><b>${letter}.</b> ${opt}</span></label>`;
  }).join("");

  const palette = t.questions.map((_, i) => {
    let c = "pal";
    if (i === t.idx) c += " current";
    else if (t.answers[i]) c += " answered";
    else if (t.marked[i]) c += " marked";
    return `<button class="${c}" onclick="goto(${i})">${i + 1}</button>`;
  }).join("");

  const fb = (t.practice && chosen)
    ? (chosen === q.a
        ? `<div class="fb ok">✅ Sahih jawab! (${q.a})</div>`
        : `<div class="fb no">❌ Ghalat — Sahih jawab: ${q.a}. ${q.o[q.a.charCodeAt(0) - 65] || ""}</div>`)
    : "";

  app.innerHTML = `
    <div class="test-head">
      <div><b>${t.label}</b> ${t.practice ? '<span class="subj-tag">PRACTICE</span>' : ""}</div>
      <div class="timer" id="timer">⏱ ${fmtTime(Math.max(0, t.timeLeft))}</div>
    </div>
    <div class="test-meta">
      <span>Sawal <b>${t.idx + 1}</b> / ${t.questions.length}</span>
      <span class="subj-tag">${q.subject}</span>
      <label class="marklbl"><input type="checkbox" ${t.marked[t.idx] ? "checked" : ""} onchange="toggleMark()"> ⭐ Mark for Review</label>
    </div>
    <div class="card qcard">
      <h3>${t.idx + 1}. ${q.q}</h3>
      <div class="options">${opts}</div>
      ${fb}
    </div>
    <div class="navrow">
      <button class="btn" onclick="goto(${t.idx - 1})" ${t.idx === 0 ? "disabled" : ""}>⬅ Pichla</button>
      <button class="btn" onclick="goto(${t.idx + 1})" ${t.idx === t.questions.length - 1 ? "disabled" : ""}>Agla ➡</button>
      <button class="btn danger" onclick="submitTest(false)">✅ Test Submit</button>
    </div>
    <div class="card palette"><b>Sawalaat:</b> ${palette}</div>`;
}

function selectOption(letter) {
  const t = state.test;
  t.answers[t.idx] = letter;
  if (t.practice) renderTest();
  else {
    // palette update only
    $$(".pal").forEach((b, i) => {
      b.className = "pal" + (i === t.idx ? " current" : t.answers[i] ? " answered" : t.marked[i] ? " marked" : "");
    });
    $$(".option").forEach(l => { l.classList.remove("chosen"); });
    const chosen = $$(".option input").find(r => r.value === letter);
    if (chosen) chosen.closest("label").classList.add("chosen");
  }
}
function toggleMark() {
  const t = state.test;
  t.marked[t.idx] = !t.marked[t.idx];
  renderTest();
}
function goto(i) {
  const t = state.test;
  if (i < 0 || i >= t.questions.length) return;
  t.idx = i;
  renderTest();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ============ SUBMIT + RESULTS ============ */
function submitTest(auto) {
  const t = state.test;
  if (!t) return;
  const unanswered = t.answers.filter(a => !a).length;
  if (!auto && unanswered > 0 && !confirm(`${unanswered} sawal attempt nahi hue — phir bhi submit karein?`)) return;
  clearTimer();

  const total = t.questions.length;
  let correct = 0;
  const per = {};
  t.questions.forEach((q, i) => {
    const key = q.subject;
    per[key] = per[key] || { c: 0, t: 0 };
    per[key].t++;
    if (t.answers[i] === q.a) { correct++; per[key].c++; }
  });
  const pct = total ? Math.round((correct / total) * 100) : 0;
  const entry = {
    label: t.label, practice: !!t.practice,
    date: new Date().toLocaleString("en-GB"),
    total, correct, pct, per,
    time: fmtTime(t.totalTime - Math.max(0, t.timeLeft))
  };
  saveHistory(entry);
  renderResults(entry, t);
  state.view = "results";
}

function renderResults(entry, t) {
  const pass = entry.pct >= 50;
  const rows = Object.entries(entry.per).map(([subj, d]) => {
    const sp = d.t ? Math.round((d.c / d.t) * 100) : 0;
    return `<tr><td style="text-align:left">${subj}</td><td>${d.t}</td><td>${d.c}</td><td>${sp}%</td>
      <td>${sp >= 50 ? "✅" : "❌"}</td></tr>`;
  }).join("");

  const review = t.questions.map((q, i) => {
    const u = t.answers[i];
    const ok = u === q.a;
    const opts = q.o.map((o, j) => {
      const letter = String.fromCharCode(65 + j);
      let cls = "opt";
      if (letter === q.a) cls += " right";
      if (u === letter && !ok) cls += " mine";
      return `<div class="${cls}"><b>${letter}.</b> ${o} ${letter === q.a ? "✔" : ""} ${(u === letter && !ok) ? "← aap ka jawab" : ""}</div>`;
    }).join("");
    return `<details class="review-item"><summary>${ok ? "✅" : "❌"} Sawal ${i + 1} — <span class="tag">${q.subject}</span></summary>
      <div class="review-body"><b>${q.q}</b>${opts}<div style="margin-top:6px"><b>Sahih jawab: ${q.a}</b> ${u ? "• Aap ka jawab: " + u : "• Aap ne attempt nahi kiya"}</div></div></details>`;
  }).join("");

  app.innerHTML = `
    <div class="card score-wrap">
      <h2 style="color:var(--green)">📋 Result — ${entry.label}</h2>
      <div class="circle" style="--p:${entry.pct}"><div class="circle-inner"><span class="pct">${entry.pct}%</span><span>${entry.correct}/${entry.total}</span></div></div>
      <div class="verdict ${pass ? "pass" : "fail"}">${pass ? "🎉 PASS (50%+) — Shabash!" : "😞 50% se kam — dobara practice karein!"}</div>
      <p style="color:var(--muted);font-size:.85rem">Waqt: ${entry.time} • ${entry.practice ? "Practice Mode" : "Test Mode"} • ${entry.date}</p>
    </div>
    <div class="card">
      <h3 style="color:var(--green);margin-bottom:8px">📊 Subject-wise Result (alag-alag)</h3>
      <table><tr><th>Subject</th><th>Kul Sawal</th><th>Sahih</th><th>%</th><th>Status</th></tr>${rows}</table>
    </div>
    <div class="card">
      <h3 style="color:var(--green);margin-bottom:8px">🔍 Sawal-by-Sawal Review</h3>
      ${review}
    </div>
    <div class="navrow">
      <button class="btn primary" onclick="retry()">🔁 Dobara Test</button>
      <button class="btn ghost" onclick="renderHome()">🏠 Home</button>
      <button class="btn gold" onclick="renderHistory()">📊 Record</button>
    </div>`;
}

function retry() {
  const src = state.test.source;
  if (src.type === "mock") startMock(src.practice);
  else startSubject(src.id, src.practice);
}

/* ============ HISTORY ============ */
function renderHistory() {
  clearTimer();
  state.view = "history";
  const h = getHistory();
  const rows = h.map((e, i) => {
    const per = Object.entries(e.per).map(([s, d]) => `${s}: ${d.c}/${d.t}`).join(" • ");
    return `<tr><td>${i + 1}</td><td>${e.date}</td><td>${e.label}${e.practice ? " (Practice)" : ""}</td>
      <td><b>${e.correct}/${e.total}</b></td><td><b>${e.pct}%</b></td><td>${e.time}</td></tr>
      <tr><td colspan="6" style="text-align:left;font-size:.75rem;color:var(--muted)">${per}</td></tr>`;
  }).join("");
  app.innerHTML = `
    <div class="card">
      <h2 style="color:var(--green);margin-bottom:10px">📊 Mera Result Record (${h.length} attempts)</h2>
      ${h.length ? `<table><tr><th>#</th><th>Date</th><th>Test</th><th>Score</th><th>%</th><th>Waqt</th></tr>${rows}</table>`
        : "<p style='color:var(--muted)'>Abhi koi test nahi diya — upar se test shuru karein!</p>"}
      ${h.length ? '<div class="row" style="margin-top:12px"><button class="btn danger" onclick="clearHistory()">🗑 Record Delete Karein</button></div>' : ""}
      <div class="row" style="margin-top:10px"><button class="btn primary" onclick="renderHome()">🏠 Home</button></div>
    </div>`;
}
function clearHistory() {
  if (confirm("Pura record delete karna hai?")) {
    localStorage.removeItem("udc_test_history");
    renderHistory();
  }
}

/* ============ INIT ============ */
const app = document.getElementById("app");
if (typeof MCQ_DATA === "undefined" || !MCQ_DATA.length) {
  app.innerHTML = '<div class="card"><h2>❌ Data load nahi hua — data.js missing hai.</h2></div>';
} else {
  // Deep links from landing page: ?mock=1 | ?mock=1&mode=practice | ?subject=islamiat&mode=test/practice
  const params = new URLSearchParams(location.search);
  if (params.has("mock")) {
    startMock(params.get("mode") === "practice");
  } else if (params.get("subject")) {
    startSubject(params.get("subject"), params.get("mode") === "practice", 20);
  } else {
    renderHome();
  }
}
