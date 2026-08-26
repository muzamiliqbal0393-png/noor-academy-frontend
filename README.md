# 🎓 Noor Academy — Frontend

**Islamabad Capital Territory (ICT) Police — UDC (Upper Division Clerk) Online Test Preparation Website**

## 📁 Structure

| File | Kaam |
|---|---|
| `index.html` | Landing page — subjects, paper pattern, preparation plan |
| `test.html` | Online Screening Test engine (mock test + subject tests + practice) |
| `css/style.css` | Landing page styles |
| `js/app.js` | Test engine (timer, scoring, subject-wise results, history) |
| `js/data.js` | 6000 MCQs data (12 subjects × 500, auto-generated) |

## 🚀 Chalane Ka Tariqa

```bash
python3 -m http.server 8080 --bind 0.0.0.0
```

Phir browser mein `http://localhost:8080` kholen.

## ✨ Features

- 🎯 Screening Mock Test — 100 MCQs, 90-minute timer, syllabus weightage ke mutabiq
- 📚 Subject-wise tests — koi bhi subject, 10/20/50/100 sawal
- 📖 Practice Mode — jawab foran check
- 📊 **Har subject ka result alag** (percentage + pass/fail)
- 🔍 Sawal-by-sawal review (sahi jawab ke sath)
- 💾 Result record browser (localStorage) mein save hota hai

## 🔗 Deep Links

- `test.html?mock=1` — Mock test (test mode)
- `test.html?mock=1&mode=practice` — Mock practice
- `test.html?subject=islamiat&mode=test` — Subject test
- `test.html?subject=islamiat&mode=practice` — Subject practice

**Subject IDs:** english-grammar, english-vocabulary, islamiat, pakistan-studies, general-knowledge, current-affairs, everyday-science, mathematics, computer-it, urdu, ict-police, iq
