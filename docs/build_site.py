"""Generates the complete YPDC static website (HTML/CSS/JS) into docs/ypdc-website/"""
import os, shutil, json

ROOT = "/home/user/noor-academy-frontend/docs/ypdc-website"
if os.path.exists(ROOT):
    shutil.rmtree(ROOT)
for d in ["css", "js", "assets", "student", "member", "directorate", "faculty", "admin", "alumni", "backend"]:
    os.makedirs(f"{ROOT}/{d}", exist_ok=True)

def slug(t):
    return (t.lower().replace("&", "and").replace("/", "-").replace(" ", "-")
            .replace("--", "-").replace("(", "").replace(")", "").replace(",", ""))

PUBLIC = ["Home", "About YPDC", "Vision & Mission", "Leadership", "Directorates", "Projects", "Events",
          "News & Updates", "Achievements", "Gallery", "Publications", "Membership", "Volunteer Registration",
          "Contact Us", "FAQs"]

PORTALS = {
    "student": ("Student Portal", "fa-user-graduate",
                ["Profile", "Membership", "Events", "Event Registration", "Volunteer Opportunities", "Attendance",
                 "Certificates", "Achievements", "Notifications", "Feedback"]),
    "member": ("Member Portal", "fa-id-badge",
               ["Profile & Member ID", "Directorate", "Responsibilities", "Tasks", "Events / Duties", "Attendance",
                "Certificates", "Performance", "Reports", "Notifications"]),
    "directorate": ("Directorate Portal", "fa-sitemap",
                    ["Directorate Profile", "Director / Assistant Director", "Team Members", "Objectives", "Work Plan",
                     "Tasks", "Events & Activities", "Event Proposals", "Attendance", "Activity Reports",
                     "Achievements", "Documents", "Performance"]),
    "faculty": ("Faculty Portal", "fa-chalkboard-teacher",
                ["Faculty Profile", "Department / Designation", "YPDC Role", "Events", "Student / Member Activities",
                 "Approvals", "Reports", "Feedback", "Notifications"]),
    "admin": ("Admin Portal", "fa-user-shield",
              ["Dashboard", "User Management", "Member Management", "Directorate Management", "Faculty Management",
               "Events Management", "Applications & Approvals", "Attendance", "Certificates", "Reports & Analytics",
               "Notifications", "Website Content", "Documents", "Feedback / Complaints", "Roles & Permissions"]),
    "alumni": ("Alumni Portal", "fa-user-tie",
               ["Alumni Profile", "Academic Information", "Professional Information", "Skills", "Alumni Network",
                "Mentorship", "Events", "Achievements", "Career Opportunities", "Volunteer / Support Opportunities"]),
}
ICONS = {"profile": "fa-user", "membership": "fa-id-card", "event": "fa-calendar", "volunteer": "fa-hands-helping",
         "attendance": "fa-clipboard-check", "certificate": "fa-certificate", "achievement": "fa-trophy",
         "notification": "fa-bell", "feedback": "fa-comment-dots", "directorate": "fa-sitemap", "task": "fa-tasks",
         "responsib": "fa-list-check", "performance": "fa-chart-line", "report": "fa-file-alt", "team": "fa-users",
         "objective": "fa-bullseye", "work plan": "fa-calendar-check", "proposal": "fa-lightbulb",
         "document": "fa-folder-open", "approval": "fa-check-double", "dashboard": "fa-gauge", "user": "fa-users-cog",
         "faculty": "fa-chalkboard-teacher", "content": "fa-globe", "complaint": "fa-comment-dots",
         "role": "fa-key", "academic": "fa-graduation-cap", "professional": "fa-briefcase", "skill": "fa-star",
         "network": "fa-network-wired", "mentor": "fa-handshake", "career": "fa-briefcase", "department": "fa-building",
         "director": "fa-user-tie", "activit": "fa-running", "analytics": "fa-chart-pie", "member": "fa-id-badge"}

def icon(name):
    n = name.lower()
    for k, v in ICONS.items():
        if k in n:
            return v
    return "fa-circle"

# ------------------------------------------------------------------ CSS
CSS = """/* ====== YPDC Global Styles ====== */
:root{--primary:#0B3D5C;--primary-dark:#082C43;--accent:#1B9AAA;--gold:#E8B04B;--bg:#F5F8FA;--card:#fff;
--text:#222;--muted:#5A6B77;--border:#D9E2E8;--success:#2E7D6B;--danger:#B3282D;--warning:#D98E04;--radius:12px;
--shadow:0 4px 18px rgba(11,61,92,.08);}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Poppins',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
a{color:var(--accent);text-decoration:none}
img{max-width:100%;display:block}
.container{width:min(1180px,92%);margin:auto}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 22px;border-radius:8px;border:0;cursor:pointer;
font-weight:600;font-family:inherit;font-size:.95rem;transition:.2s}
.btn-primary{background:var(--accent);color:#fff}.btn-primary:hover{background:#158593}
.btn-outline{border:2px solid #fff;color:#fff;background:transparent}.btn-outline:hover{background:#fff;color:var(--primary)}
.btn-gold{background:var(--gold);color:var(--primary)}
.btn-danger{background:var(--danger);color:#fff}.btn-sm{padding:6px 14px;font-size:.82rem}
/* Navbar */
.navbar{background:var(--primary);color:#fff;position:sticky;top:0;z-index:100;box-shadow:0 2px 10px rgba(0,0,0,.2)}
.navbar .container{display:flex;align-items:center;justify-content:space-between;height:68px}
.logo{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.35rem;color:#fff}
.logo span{background:var(--gold);color:var(--primary);padding:2px 9px;border-radius:6px}
.nav-links{display:flex;gap:4px;list-style:none;flex-wrap:wrap}
.nav-links a{color:#dbe8f0;padding:8px 11px;border-radius:6px;font-size:.88rem}
.nav-links a:hover,.nav-links a.active{background:rgba(255,255,255,.12);color:#fff}
.nav-toggle{display:none;background:none;border:0;color:#fff;font-size:1.5rem;cursor:pointer}
/* Hero */
.hero{background:linear-gradient(135deg,var(--primary),#124D70 60%,var(--accent));color:#fff;padding:90px 0;text-align:center}
.hero h1{font-size:2.8rem;line-height:1.2;margin-bottom:14px}
.hero p{font-size:1.15rem;opacity:.9;max-width:720px;margin:0 auto 28px}
.hero .actions{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.page-header{background:var(--primary);color:#fff;padding:48px 0;border-bottom:5px solid var(--gold)}
.page-header h1{font-size:2rem}.page-header p{opacity:.85}
section{padding:60px 0}
.section-title{text-align:center;margin-bottom:36px}
.section-title h2{font-size:1.9rem;color:var(--primary)}
.section-title p{color:var(--muted)}
.section-title::after{content:"";display:block;width:60px;height:4px;background:var(--gold);margin:12px auto 0;border-radius:2px}
.grid{display:grid;gap:22px}.grid-2{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.grid-3{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}.grid-4{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.card{background:var(--card);border-radius:var(--radius);padding:24px;box-shadow:var(--shadow);border:1px solid var(--border)}
.card h3{color:var(--primary);margin-bottom:8px;font-size:1.1rem}
.card .icon{width:52px;height:52px;border-radius:12px;background:#E6F4F6;color:var(--accent);display:grid;place-items:center;font-size:1.4rem;margin-bottom:14px}
.card p{color:var(--muted);font-size:.93rem}
.stat{text-align:center}.stat b{display:block;font-size:2.2rem;color:var(--accent)}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:600}
.badge-success{background:#E3F3EF;color:var(--success)}.badge-danger{background:#F9E4E5;color:var(--danger)}
.badge-warning{background:#FCF1DC;color:var(--warning)}.badge-info{background:#E6F4F6;color:var(--accent)}
/* Table */
.table-wrap{overflow-x:auto;background:#fff;border-radius:var(--radius);box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse;font-size:.9rem}
th{background:var(--primary);color:#fff;text-align:left;padding:12px 14px;font-weight:600}
td{padding:11px 14px;border-bottom:1px solid var(--border)}
tr:hover td{background:#F4F9FB}
/* Forms */
.form{display:grid;gap:16px}.form-row{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
label{font-weight:600;font-size:.88rem;color:var(--primary);display:block;margin-bottom:6px}
input,select,textarea{width:100%;padding:11px 13px;border:1.5px solid var(--border);border-radius:8px;font-family:inherit;font-size:.93rem;background:#fff}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(27,154,170,.15)}
.error{color:var(--danger);font-size:.8rem;margin-top:4px}
/* Footer */
footer{background:var(--primary-dark);color:#c9d8e2;padding:50px 0 20px;margin-top:40px}
footer .grid{margin-bottom:30px}footer h4{color:#fff;margin-bottom:12px}
footer a{color:#c9d8e2;display:block;font-size:.9rem;padding:3px 0}footer a:hover{color:var(--gold)}
.copyright{border-top:1px solid rgba(255,255,255,.1);padding-top:18px;text-align:center;font-size:.85rem}
/* Auth */
.auth-wrap{min-height:100vh;display:grid;place-items:center;background:linear-gradient(135deg,var(--primary),var(--accent));padding:20px}
.auth-card{background:#fff;width:100%;max-width:440px;padding:38px;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.25)}
.auth-card h2{color:var(--primary);text-align:center;margin-bottom:6px}.auth-card p.sub{text-align:center;color:var(--muted);margin-bottom:24px}
.demo{background:#FCF1DC;border-left:4px solid var(--gold);padding:10px 12px;font-size:.8rem;margin-top:16px;border-radius:6px}
/* Gallery / FAQ / Timeline */
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.gallery div{aspect-ratio:4/3;border-radius:10px;background:linear-gradient(135deg,#124D70,var(--accent));display:grid;place-items:center;color:#fff;font-weight:600}
.faq details{background:#fff;border-radius:10px;padding:16px 20px;margin-bottom:10px;box-shadow:var(--shadow)}
.faq summary{cursor:pointer;font-weight:600;color:var(--primary)}
.faq details p{margin-top:10px;color:var(--muted)}
.toast{position:fixed;bottom:24px;right:24px;background:var(--primary);color:#fff;padding:14px 20px;border-radius:10px;box-shadow:var(--shadow);z-index:999;animation:fade .3s}
.toast.success{background:var(--success)}.toast.error{background:var(--danger)}
@keyframes fade{from{opacity:0;transform:translateY(10px)}to{opacity:1}}
@media(max-width:900px){.nav-toggle{display:block}.nav-links{display:none;position:absolute;top:68px;left:0;right:0;background:var(--primary);flex-direction:column;padding:12px}
.nav-links.open{display:flex}.hero h1{font-size:2rem}}
"""

PORTAL_CSS = """/* ====== Portal Layout ====== */
.portal{display:flex;min-height:100vh}
.sidebar{width:260px;background:var(--primary);color:#fff;padding:20px 14px;position:fixed;top:0;bottom:0;overflow-y:auto;transition:.3s;z-index:50}
.sidebar .logo{margin-bottom:26px;padding:0 8px}
.sidebar .role{font-size:.72rem;letter-spacing:1px;text-transform:uppercase;color:var(--gold);padding:0 8px;margin-bottom:10px}
.sidebar a{display:flex;align-items:center;gap:12px;color:#dbe8f0;padding:10px 12px;border-radius:8px;margin-bottom:3px;font-size:.9rem}
.sidebar a i{width:20px;text-align:center}
.sidebar a:hover,.sidebar a.active{background:var(--accent);color:#fff}
.sidebar .logout{margin-top:20px;border-top:1px solid rgba(255,255,255,.12);padding-top:14px}
.main{margin-left:260px;flex:1;display:flex;flex-direction:column;min-width:0}
.topbar{background:#fff;height:66px;display:flex;align-items:center;justify-content:space-between;padding:0 28px;box-shadow:0 1px 8px rgba(0,0,0,.06);position:sticky;top:0;z-index:40}
.topbar h2{color:var(--primary);font-size:1.15rem}
.topbar .right{display:flex;align-items:center;gap:18px}
.topbar .bell{position:relative;font-size:1.15rem;color:var(--muted);cursor:pointer}
.topbar .bell span{position:absolute;top:-6px;right:-8px;background:var(--danger);color:#fff;font-size:.6rem;border-radius:10px;padding:1px 5px}
.avatar{width:38px;height:38px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;font-weight:700}
.content{padding:28px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:18px;margin-bottom:26px}
.stat-card{background:#fff;border-radius:12px;padding:20px;display:flex;align-items:center;gap:16px;box-shadow:var(--shadow);border-left:4px solid var(--accent)}
.stat-card i{font-size:1.6rem;color:var(--accent);background:#E6F4F6;width:52px;height:52px;border-radius:12px;display:grid;place-items:center}
.stat-card b{font-size:1.6rem;color:var(--primary);display:block;line-height:1.1}
.stat-card small{color:var(--muted)}
.panel{background:#fff;border-radius:12px;box-shadow:var(--shadow);margin-bottom:24px}
.panel-head{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-bottom:1px solid var(--border)}
.panel-head h3{color:var(--primary);font-size:1.05rem}
.panel-body{padding:20px}
.toolbar{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.toolbar input{max-width:280px}
.menu-btn{display:none;background:none;border:0;font-size:1.3rem;color:var(--primary);cursor:pointer}
.profile-head{display:flex;gap:20px;align-items:center;margin-bottom:20px}
.profile-head .avatar{width:80px;height:80px;font-size:1.8rem}
.chart-box{height:280px}
@media(max-width:900px){.sidebar{transform:translateX(-100%)}.sidebar.open{transform:none}.main{margin-left:0}.menu-btn{display:block}}
"""

# ------------------------------------------------------------------ JS
API_JS = """// ====== api.js — Backend se baat karne ka wrapper ======
const API_BASE = 'http://localhost:5000/api';   // production mein apna backend URL

async function apiRequest(path, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('ypdc_token');
  if (token) headers['Authorization'] = 'Bearer ' + token;
  try {
    const res = await fetch(API_BASE + path, { method, headers, body: body ? JSON.stringify(body) : null });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.message || 'Request failed');
    return data;
  } catch (err) {
    console.warn('API error (demo mode):', err.message);
    return null; // backend na ho to demo data use hoga
  }
}
const api = {
  get: (p) => apiRequest(p),
  post: (p, b) => apiRequest(p, 'POST', b),
  put: (p, b) => apiRequest(p, 'PUT', b),
  del: (p) => apiRequest(p, 'DELETE'),
};
"""

AUTH_JS = """// ====== auth.js — Login, role check, logout ======
const ROLE_HOME = {
  student: 'student/dashboard.html', member: 'member/dashboard.html', directorate: 'directorate/dashboard.html',
  faculty: 'faculty/dashboard.html', admin: 'admin/dashboard.html', alumni: 'alumni/dashboard.html'
};
// Demo accounts (backend ke bina test ke liye)
const DEMO_USERS = {
  'student@ypdc.org': { role: 'student', name: 'Ali Raza' },
  'member@ypdc.org': { role: 'member', name: 'Sara Khan' },
  'director@ypdc.org': { role: 'directorate', name: 'Hamza Ahmed' },
  'faculty@ypdc.org': { role: 'faculty', name: 'Dr. Ayesha Malik' },
  'admin@ypdc.org': { role: 'admin', name: 'Admin' },
  'alumni@ypdc.org': { role: 'alumni', name: 'Usman Tariq' },
};

async function login(email, password) {
  // 1) Real backend try karo
  const res = await api.post('/auth/login', { email, password });
  let user;
  if (res && res.token) {
    localStorage.setItem('ypdc_token', res.token);
    user = res.user;
  } else if (DEMO_USERS[email] && password === '123456') {
    user = { email, ...DEMO_USERS[email] };
    localStorage.setItem('ypdc_token', 'demo-token');
  } else {
    return { ok: false, message: 'Email ya password ghalat hai' };
  }
  localStorage.setItem('ypdc_user', JSON.stringify(user));
  return { ok: true, user };
}

function currentUser() {
  try { return JSON.parse(localStorage.getItem('ypdc_user')); } catch { return null; }
}

// Har portal page par call hota hai — role match na ho to login par bhej do
function requireRole(role) {
  const u = currentUser();
  if (!u || (u.role !== role && u.role !== 'admin')) {
    window.location.href = '../login.html';
    return null;
  }
  document.querySelectorAll('[data-user-name]').forEach(el => el.textContent = u.name);
  document.querySelectorAll('[data-user-initial]').forEach(el => el.textContent = u.name.charAt(0));
  return u;
}

function logout() {
  localStorage.removeItem('ypdc_token');
  localStorage.removeItem('ypdc_user');
  window.location.href = '../login.html';
}
"""

MAIN_JS = """// ====== main.js — Common UI helpers ======
function toast(msg, type = '') {
  const t = document.createElement('div');
  t.className = 'toast ' + type; t.textContent = msg;
  document.body.appendChild(t); setTimeout(() => t.remove(), 3000);
}
// Mobile nav toggle
document.addEventListener('click', e => {
  if (e.target.closest('.nav-toggle')) document.querySelector('.nav-links').classList.toggle('open');
  if (e.target.closest('.menu-btn')) document.querySelector('.sidebar').classList.toggle('open');
});
// Active link highlight
(function () {
  const here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .sidebar a').forEach(a => {
    if (a.getAttribute('href') === here) a.classList.add('active');
  });
})();
// Table search
function tableSearch(inputId, tableId) {
  const input = document.getElementById(inputId), rows = document.querySelectorAll('#' + tableId + ' tbody tr');
  if (!input) return;
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase();
    rows.forEach(r => r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none');
  });
}
// Export table to CSV
function exportCSV(tableId, filename = 'export.csv') {
  const rows = [...document.querySelectorAll('#' + tableId + ' tr')].map(tr =>
    [...tr.children].map(td => '"' + td.textContent.trim().replace(/"/g, '""') + '"').join(','));
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([rows.join('\\n')], { type: 'text/csv' }));
  a.download = filename; a.click();
}
// Simple form validation
function validateForm(form) {
  let ok = true;
  form.querySelectorAll('[required]').forEach(f => {
    const err = f.parentElement.querySelector('.error');
    if (err) err.remove();
    if (!f.value.trim()) {
      ok = false; const e = document.createElement('div'); e.className = 'error'; e.textContent = 'Ye field zaroori hai';
      f.parentElement.appendChild(e);
    }
  });
  return ok;
}
document.addEventListener('submit', e => {
  const f = e.target;
  if (f.matches('form[data-demo]')) {
    e.preventDefault();
    if (validateForm(f)) { toast(f.dataset.demo || 'Submit ho gaya!', 'success'); f.reset(); }
  }
});
"""

DATA_JS = """// ====== data.js — Demo data (backend connect hone par API se aayega) ======
const DEMO = {
  events: [
    { id: 1, title: 'Leadership Summit 2026', date: '2026-10-12', venue: 'Main Auditorium', type: 'Seminar', status: 'Approved', directorate: 'Training & Development' },
    { id: 2, title: 'Blood Donation Camp', date: '2026-10-20', venue: 'Campus Ground', type: 'Social', status: 'Approved', directorate: 'Community Service' },
    { id: 3, title: 'Career Counselling Week', date: '2026-11-03', venue: 'Block B', type: 'Workshop', status: 'Pending', directorate: 'Career Development' },
    { id: 4, title: 'Annual Sports Gala', date: '2026-11-18', venue: 'Sports Complex', type: 'Sports', status: 'Proposed', directorate: 'Sports & Culture' },
    { id: 5, title: 'Tech Hackathon', date: '2026-12-05', venue: 'IT Lab', type: 'Competition', status: 'Approved', directorate: 'IT & Media' },
  ],
  directorates: [
    { name: 'Training & Development', director: 'Hamza Ahmed', asst: 'Zainab Ali', members: 18 },
    { name: 'Community Service', director: 'Bilal Khan', asst: 'Hira Shah', members: 24 },
    { name: 'Career Development', director: 'Maryam Noor', asst: 'Ahmed Raza', members: 15 },
    { name: 'Sports & Culture', director: 'Saad Iqbal', asst: 'Fatima Jan', members: 20 },
    { name: 'IT & Media', director: 'Usama Butt', asst: 'Laiba Aziz', members: 12 },
    { name: 'Public Relations', director: 'Danish Ali', asst: 'Amna Riaz', members: 10 },
  ],
  tasks: [
    { title: 'Prepare event budget', assigned: 'Sara Khan', deadline: '2026-10-05', status: 'In Progress' },
    { title: 'Design summit banner', assigned: 'Laiba Aziz', deadline: '2026-10-08', status: 'Completed' },
    { title: 'Contact guest speakers', assigned: 'Ahmed Raza', deadline: '2026-10-10', status: 'Pending' },
    { title: 'Volunteer list finalize', assigned: 'Hira Shah', deadline: '2026-10-15', status: 'In Progress' },
  ],
  attendance: [
    { event: 'Orientation Session', date: '2026-09-02', status: 'Present' },
    { event: 'Monthly Meeting', date: '2026-09-10', status: 'Present' },
    { event: 'Tree Plantation Drive', date: '2026-09-18', status: 'Absent' },
    { event: 'Workshop: Public Speaking', date: '2026-09-24', status: 'Present' },
  ],
  certificates: [
    { no: 'YPDC-2026-0142', title: 'Certificate of Participation — Orientation', date: '2026-09-05' },
    { no: 'YPDC-2026-0219', title: 'Volunteer Appreciation — Plantation Drive', date: '2026-09-20' },
  ],
  notifications: [
    { msg: 'Leadership Summit registration open', time: '2 hours ago', type: 'info' },
    { msg: 'Your certificate has been issued', time: '1 day ago', type: 'success' },
    { msg: 'Task deadline tomorrow: Prepare event budget', time: '2 days ago', type: 'warning' },
  ],
  users: [
    { name: 'Ali Raza', email: 'student@ypdc.org', role: 'Student', status: 'Active' },
    { name: 'Sara Khan', email: 'member@ypdc.org', role: 'Member', status: 'Active' },
    { name: 'Hamza Ahmed', email: 'director@ypdc.org', role: 'Director', status: 'Active' },
    { name: 'Dr. Ayesha Malik', email: 'faculty@ypdc.org', role: 'Faculty', status: 'Active' },
    { name: 'Usman Tariq', email: 'alumni@ypdc.org', role: 'Alumni', status: 'Inactive' },
  ],
  applications: [
    { name: 'Hassan Ali', type: 'Membership', date: '2026-09-20', status: 'Pending' },
    { name: 'Tech Hackathon', type: 'Event Proposal', date: '2026-09-21', status: 'Pending' },
    { name: 'Noor Fatima', type: 'Volunteer', date: '2026-09-22', status: 'Approved' },
  ],
};
function badge(s) {
  const m = { Approved: 'success', Present: 'success', Completed: 'success', Active: 'success', Pending: 'warning',
              'In Progress': 'info', Proposed: 'info', Absent: 'danger', Rejected: 'danger', Inactive: 'danger' };
  return `<span class="badge badge-${m[s] || 'info'}">${s}</span>`;
}
function renderRows(tbodyId, rows, cols) {
  const tb = document.getElementById(tbodyId); if (!tb) return;
  tb.innerHTML = rows.map(r => '<tr>' + cols.map(c => `<td>${c === 'status' ? badge(r[c]) : r[c]}</td>`).join('') + '</tr>').join('');
}
"""

# ------------------------------------------------------------------ HTML helpers
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | YPDC</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<link rel="stylesheet" href="{base}css/style.css">
{extra_css}
</head>
<body>
"""

def public_nav():
    links = "".join(f'<li><a href="{ "index.html" if p=="Home" else slug(p)+".html"}">{p}</a></li>' for p in PUBLIC)
    return f"""<nav class="navbar"><div class="container">
  <a class="logo" href="index.html"><span>Y</span>YPDC</a>
  <button class="nav-toggle"><i class="fa fa-bars"></i></button>
  <ul class="nav-links">{links}<li><a href="login.html" class="btn btn-gold btn-sm" style="margin-left:6px"><i class="fa fa-sign-in-alt"></i> Login</a></li></ul>
</div></nav>"""

FOOTER = """<footer><div class="container">
 <div class="grid grid-4">
  <div><h4>YPDC</h4><p style="font-size:.9rem">Youth Professional Development Council — empowering youth through leadership, service and professional growth.</p></div>
  <div><h4>Quick Links</h4><a href="about-ypdc.html">About</a><a href="directorates.html">Directorates</a><a href="events.html">Events</a><a href="membership.html">Membership</a></div>
  <div><h4>Resources</h4><a href="publications.html">Publications</a><a href="gallery.html">Gallery</a><a href="news-and-updates.html">News</a><a href="faqs.html">FAQs</a></div>
  <div><h4>Contact</h4><a href="#"><i class="fa fa-envelope"></i> info@ypdc.org</a><a href="#"><i class="fa fa-phone"></i> +92 300 0000000</a><a href="#"><i class="fa fa-map-marker-alt"></i> Lahore, Pakistan</a></div>
 </div>
 <div class="copyright">&copy; 2026 YPDC. All rights reserved.</div>
</div></footer>
<script src="js/main.js"></script>
</body></html>"""

def public_page(name, body):
    title = name
    html = HEAD.format(title=title, base="", extra_css="") + public_nav()
    if name != "Home":
        html += f'<header class="page-header"><div class="container"><h1>{name}</h1><p>Youth Professional Development Council</p></div></header>'
    html += body + FOOTER
    fn = "index.html" if name == "Home" else slug(name) + ".html"
    open(f"{ROOT}/{fn}", "w").write(html)

def cards(items, cls="grid-3"):
    return f'<div class="grid {cls}">' + "".join(
        f'<div class="card"><div class="icon"><i class="fa {i}"></i></div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items) + "</div>"

# ------------------------------------------------------------------ PUBLIC PAGES
public_bodies = {
"Home": f"""
<section class="hero"><div class="container">
 <h1>Youth Professional Development Council</h1>
 <p>Building tomorrow's leaders today — through training, community service, events and professional growth opportunities.</p>
 <div class="actions"><a href="membership.html" class="btn btn-gold"><i class="fa fa-user-plus"></i> Become a Member</a><a href="events.html" class="btn btn-outline"><i class="fa fa-calendar"></i> Upcoming Events</a></div>
</div></section>
<section><div class="container"><div class="grid grid-4">
 <div class="card stat"><b>1200+</b>Members</div><div class="card stat"><b>6</b>Directorates</div>
 <div class="card stat"><b>150+</b>Events Held</div><div class="card stat"><b>40+</b>Projects</div>
</div></div></section>
<section style="padding-top:0"><div class="container">
 <div class="section-title"><h2>What We Do</h2><p>Our core focus areas</p></div>
 {cards([("fa-graduation-cap","Training & Development","Workshops, seminars and skill-building sessions for students."),
         ("fa-hands-helping","Community Service","Blood drives, plantation and welfare projects."),
         ("fa-briefcase","Career Development","Counselling, internships and industry linkages."),
         ("fa-trophy","Sports & Culture","Galas, competitions and cultural festivals."),
         ("fa-laptop-code","IT & Media","Digital campaigns, hackathons and media coverage."),
         ("fa-bullhorn","Public Relations","Partnerships, outreach and communication.")])}
</div></section>
<section style="background:#fff"><div class="container">
 <div class="section-title"><h2>Upcoming Events</h2></div>
 <div class="table-wrap"><table id="evTable"><thead><tr><th>Event</th><th>Date</th><th>Venue</th><th>Type</th></tr></thead><tbody id="homeEvents"></tbody></table></div>
 <p style="text-align:center;margin-top:20px"><a href="events.html" class="btn btn-primary">View All Events</a></p>
</div></section>
<section><div class="container">
 <div class="section-title"><h2>Our Portals</h2><p>Login to access your dashboard</p></div>
 {cards([("fa-user-graduate","Student Portal","Events, registration, attendance & certificates."),
         ("fa-id-badge","Member Portal","Tasks, duties, performance & reports."),
         ("fa-sitemap","Directorate Portal","Team, work plan, proposals & activity reports."),
         ("fa-chalkboard-teacher","Faculty Portal","Approvals, monitoring and reports."),
         ("fa-user-shield","Admin Portal","Full system management & analytics."),
         ("fa-user-tie","Alumni Portal","Network, mentorship & career opportunities.")])}
</div></section>
<script src="js/data.js"></script>
<script>renderRows('homeEvents', DEMO.events.filter(e=>e.status==='Approved'), ['title','date','venue','type']);</script>
""",
"About YPDC": """<section><div class="container grid grid-2">
 <div><h2 style="color:var(--primary)">Who We Are</h2><p style="margin:14px 0;color:var(--muted)">YPDC (Youth Professional Development Council) is a student-led council working under faculty supervision to develop leadership, professional and social skills among youth. Through six directorates we organize trainings, community projects, career events and cultural activities.</p>
 <p style="color:var(--muted)">Established with the vision to create responsible, skilled and confident professionals, YPDC provides a platform where students learn by doing — managing real events, leading teams and serving the community.</p></div>
 <div class="card"><h3>Key Facts</h3><ul style="margin:10px 0 0 18px;color:var(--muted);line-height:2"><li>Founded: 2018</li><li>Members: 1200+</li><li>Directorates: 6</li><li>Faculty Advisors: 8</li><li>Annual Events: 40+</li></ul></div>
</div></section>""",
"Vision & Mission": """<section><div class="container grid grid-2">
 <div class="card"><div class="icon"><i class="fa fa-eye"></i></div><h3>Our Vision</h3><p>To be a leading youth council that nurtures ethical, skilled and socially responsible professionals who lead positive change in society.</p></div>
 <div class="card"><div class="icon"><i class="fa fa-bullseye"></i></div><h3>Our Mission</h3><p>To empower students through structured training, leadership roles, community service and industry exposure — building competence, character and confidence.</p></div>
</div>
<div class="container" style="margin-top:40px"><div class="section-title"><h2>Core Values</h2></div>""" + cards([
 ("fa-heart","Integrity","Honesty and ethics in every action."),("fa-users","Teamwork","Collaboration across directorates."),
 ("fa-lightbulb","Innovation","Creative solutions to real problems."),("fa-hand-holding-heart","Service","Giving back to the community.")],"grid-4") + "</div></section>",
"Leadership": "<section><div class='container'>" + cards([
 ("fa-user-tie","Patron-in-Chief","Vice Chancellor — overall patronage of YPDC."),("fa-user-tie","Chief Advisor","Dean Student Affairs — strategic guidance."),
 ("fa-chalkboard-teacher","Faculty Coordinator","Dr. Ayesha Malik — supervision & approvals."),("fa-user","President","Hamza Ahmed — student leadership."),
 ("fa-user","Vice President","Sara Khan — operations & coordination."),("fa-user","General Secretary","Bilal Khan — records & communication.")]) + "</div></section>",
"Directorates": """<section><div class="container"><div class="section-title"><h2>Our Directorates</h2><p>Each directorate is led by a Director and Assistant Director</p></div>
<div class="table-wrap"><table><thead><tr><th>Directorate</th><th>Director</th><th>Assistant Director</th><th>Members</th></tr></thead><tbody id="dirs"></tbody></table></div></div></section>
<script src="js/data.js"></script><script>renderRows('dirs', DEMO.directorates, ['name','director','asst','members']);</script>""",
"Projects": "<section><div class='container'>" + cards([
 ("fa-tree","Green Campus Drive","5000+ trees planted across campus and city."),("fa-tint","Blood Donation Network","Regular camps in partnership with blood banks."),
 ("fa-book","Literacy Program","Weekend classes for underprivileged children."),("fa-laptop","Digital Skills Bootcamp","Free IT training for 300+ students."),
 ("fa-briefcase","Internship Bridge","Connecting students with 50+ companies."),("fa-female","Women Empowerment Series","Mentorship and skill sessions for female students.")]) + "</div></section>",
"Events": """<section><div class="container">
<div class="toolbar"><input id="q" placeholder="Search events..."><a href="login.html" class="btn btn-primary"><i class="fa fa-ticket"></i> Register (Login)</a></div>
<div class="table-wrap"><table id="evt"><thead><tr><th>Event</th><th>Date</th><th>Venue</th><th>Type</th><th>Directorate</th></tr></thead><tbody id="rows"></tbody></table></div></div></section>
<script src="js/data.js"></script><script>renderRows('rows', DEMO.events.filter(e=>e.status==='Approved'), ['title','date','venue','type','directorate']);tableSearch('q','evt');</script>""",
"News & Updates": "<section><div class='container'>" + cards([
 ("fa-newspaper","Leadership Summit 2026 announced","Registrations open from 1st October. Limited seats."),
 ("fa-newspaper","New Directorate: IT & Media","YPDC expands with a dedicated technology & media wing."),
 ("fa-newspaper","Blood Camp collects 320 bottles","Record participation in September camp."),
 ("fa-newspaper","Alumni Mentorship Program launched","50 alumni mentors on board for this semester.")],"grid-2") + "</div></section>",
"Achievements": "<section><div class='container'>" + cards([
 ("fa-trophy","Best Student Society 2025","Awarded by the University for outstanding contribution."),("fa-award","National Youth Award","Recognition for community service excellence."),
 ("fa-medal","5000 Trees Milestone","Green Campus Drive achievement."),("fa-star","100% Event Success Rate","All 42 planned events executed in 2025.")],"grid-2") + "</div></section>",
"Gallery": "<section><div class='container'><div class='gallery'>" + "".join(f"<div><i class='fa fa-image' style='margin-right:8px'></i>{t}</div>" for t in
 ["Leadership Summit","Blood Camp","Plantation Drive","Sports Gala","Hackathon","Career Fair","Cultural Night","Orientation","Award Ceremony"]) + "</div></div></section>",
"Publications": """<section><div class="container"><div class="table-wrap"><table><thead><tr><th>Title</th><th>Type</th><th>Year</th><th>Download</th></tr></thead><tbody>
<tr><td>YPDC Annual Report 2025</td><td>Report</td><td>2025</td><td><a href="#" class="btn btn-sm btn-primary"><i class="fa fa-download"></i> PDF</a></td></tr>
<tr><td>Youth Voice Magazine — Vol. 3</td><td>Magazine</td><td>2026</td><td><a href="#" class="btn btn-sm btn-primary"><i class="fa fa-download"></i> PDF</a></td></tr>
<tr><td>Leadership Handbook</td><td>Guide</td><td>2025</td><td><a href="#" class="btn btn-sm btn-primary"><i class="fa fa-download"></i> PDF</a></td></tr>
<tr><td>Community Service Newsletter</td><td>Newsletter</td><td>2026</td><td><a href="#" class="btn btn-sm btn-primary"><i class="fa fa-download"></i> PDF</a></td></tr>
</tbody></table></div></div></section>""",
"Membership": """<section><div class="container grid grid-2">
 <div><h2 style="color:var(--primary)">Join YPDC</h2><p style="color:var(--muted);margin:12px 0">Membership is open to all enrolled students. Members get access to trainings, leadership roles, certificates and a strong professional network.</p>
 <ul style="margin-left:18px;color:var(--muted);line-height:2"><li>Fill the application form</li><li>Admin review & interview</li><li>Approval & Member ID issued</li><li>Portal access via email</li></ul></div>
 <div class="card"><h3>Membership Application</h3><form class="form" data-demo="Application submitted! Aapko email par update milega." style="margin-top:12px">
  <div class="form-row"><div><label>Full Name</label><input required></div><div><label>Email</label><input type="email" required></div></div>
  <div class="form-row"><div><label>Phone</label><input required></div><div><label>Roll No / Reg No</label><input required></div></div>
  <div class="form-row"><div><label>Department</label><input required></div><div><label>Preferred Directorate</label><select><option>Training & Development</option><option>Community Service</option><option>Career Development</option><option>Sports & Culture</option><option>IT & Media</option><option>Public Relations</option></select></div></div>
  <div><label>Why do you want to join?</label><textarea rows="3" required></textarea></div>
  <button class="btn btn-primary">Submit Application</button></form></div>
</div></section>""",
"Volunteer Registration": """<section><div class="container" style="max-width:720px"><div class="card"><h3>Volunteer Registration</h3><p>Register as a volunteer for upcoming events and community projects.</p>
<form class="form" data-demo="Volunteer registration received. Shukriya!" style="margin-top:14px">
 <div class="form-row"><div><label>Full Name</label><input required></div><div><label>Email</label><input type="email" required></div></div>
 <div class="form-row"><div><label>Phone</label><input required></div><div><label>Availability</label><select><option>Weekdays</option><option>Weekends</option><option>Both</option></select></div></div>
 <div><label>Interested Event / Area</label><select><option>Leadership Summit 2026</option><option>Blood Donation Camp</option><option>Plantation Drive</option><option>Any</option></select></div>
 <div><label>Skills</label><input placeholder="e.g. Photography, Management, Design"></div>
 <button class="btn btn-primary">Register as Volunteer</button></form></div></div></section>""",
"Contact Us": """<section><div class="container grid grid-2">
 <div class="card"><h3>Send a Message</h3><form class="form" data-demo="Message bhej diya gaya!" style="margin-top:12px">
  <div class="form-row"><div><label>Name</label><input required></div><div><label>Email</label><input type="email" required></div></div>
  <div><label>Subject</label><input required></div><div><label>Message</label><textarea rows="4" required></textarea></div>
  <button class="btn btn-primary">Send Message</button></form></div>
 <div class="card"><h3>Contact Information</h3><p style="line-height:2.2;margin-top:10px"><i class="fa fa-map-marker-alt" style="color:var(--accent);width:24px"></i> YPDC Office, Student Affairs Block, Lahore<br>
 <i class="fa fa-envelope" style="color:var(--accent);width:24px"></i> info@ypdc.org<br><i class="fa fa-phone" style="color:var(--accent);width:24px"></i> +92 300 0000000<br>
 <i class="fa fa-clock" style="color:var(--accent);width:24px"></i> Mon–Fri, 9:00 AM – 4:00 PM</p></div>
</div></section>""",
"FAQs": "<section><div class='container faq' style='max-width:820px'>" + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in [
 ("Who can join YPDC?","Any enrolled student of the university can apply for membership through the Membership page."),
 ("Is there a membership fee?","No, YPDC membership is completely free."),
 ("How do I get certificates?","Certificates are auto-issued after attendance is marked for an event; download from your portal."),
 ("How are directorates assigned?","Based on your preference and interview, the admin assigns you to a directorate."),
 ("Can alumni stay connected?","Yes — the Alumni Portal offers networking, mentorship and career opportunities."),
 ("How do I verify a certificate?","Scan the QR on the certificate or use the certificate number on the verification page.")]) + "</div></section>",
}
for name, body in public_bodies.items():
    public_page(name, body)

# ------------------------------------------------------------------ LOGIN / REGISTER
LOGIN = HEAD.format(title="Login", base="", extra_css="") + """
<div class="auth-wrap"><div class="auth-card">
 <a class="logo" href="index.html" style="color:var(--primary);justify-content:center;margin-bottom:14px"><span>Y</span>YPDC</a>
 <h2>Portal Login</h2><p class="sub">Apni role ke mutabiq portal khulega</p>
 <form class="form" id="loginForm">
  <div><label>Email</label><input type="email" id="email" required placeholder="you@ypdc.org"></div>
  <div><label>Password</label><input type="password" id="password" required placeholder="••••••"></div>
  <button class="btn btn-primary" style="justify-content:center">Login <i class="fa fa-arrow-right"></i></button>
 </form>
 <p style="text-align:center;margin-top:14px;font-size:.9rem">New here? <a href="register.html">Register</a> · <a href="#" onclick="toast('Reset link email par bhej diya gaya','success');return false">Forgot password?</a></p>
 <div class="demo"><b>Demo accounts</b> (password: <code>123456</code>)<br>student@ypdc.org · member@ypdc.org · director@ypdc.org<br>faculty@ypdc.org · admin@ypdc.org · alumni@ypdc.org</div>
</div></div>
<script src="js/api.js"></script><script src="js/auth.js"></script><script src="js/main.js"></script>
<script>
document.getElementById('loginForm').addEventListener('submit', async e => {
  e.preventDefault();
  const r = await login(email.value.trim(), password.value);
  if (r.ok) { toast('Welcome ' + r.user.name, 'success'); setTimeout(() => location.href = ROLE_HOME[r.user.role], 600); }
  else toast(r.message, 'error');
});
</script></body></html>"""
open(f"{ROOT}/login.html", "w").write(LOGIN)

REGISTER = HEAD.format(title="Register", base="", extra_css="") + """
<div class="auth-wrap"><div class="auth-card" style="max-width:560px">
 <h2>Create Account</h2><p class="sub">Student / Alumni registration</p>
 <form class="form" data-demo="Account request submit ho gaya. Admin approval ke baad email aayega.">
  <div class="form-row"><div><label>Full Name</label><input required></div><div><label>Email</label><input type="email" required></div></div>
  <div class="form-row"><div><label>Register as</label><select><option>Student</option><option>Alumni</option></select></div><div><label>Department</label><input required></div></div>
  <div class="form-row"><div><label>Password</label><input type="password" required></div><div><label>Confirm Password</label><input type="password" required></div></div>
  <button class="btn btn-primary" style="justify-content:center">Register</button>
 </form>
 <p style="text-align:center;margin-top:14px;font-size:.9rem">Already have an account? <a href="login.html">Login</a></p>
</div></div><script src="js/main.js"></script></body></html>"""
open(f"{ROOT}/register.html", "w").write(REGISTER)

# ------------------------------------------------------------------ PORTAL PAGES
def portal_shell(role, title, page_title, body, extra_js=""):
    pname, picon, feats = PORTALS[role]
    links = f'<a href="dashboard.html"><i class="fa fa-gauge"></i> Dashboard</a>' if feats[0] != "Dashboard" else ""
    links += "".join(f'<a href="{slug(f)}.html"><i class="fa {icon(f)}"></i> {f}</a>' for f in feats)
    html = HEAD.format(title=f"{page_title} — {pname}", base="../", extra_css='<link rel="stylesheet" href="../css/portal.css">')
    html += f"""<div class="portal">
<aside class="sidebar">
 <a class="logo" href="../index.html"><span>Y</span>YPDC</a>
 <div class="role"><i class="fa {picon}"></i> {pname}</div>
 {links}
 <div class="logout"><a href="#" onclick="logout();return false"><i class="fa fa-sign-out-alt"></i> Logout</a></div>
</aside>
<div class="main">
 <header class="topbar"><div style="display:flex;align-items:center;gap:14px"><button class="menu-btn"><i class="fa fa-bars"></i></button><h2>{page_title}</h2></div>
  <div class="right"><a href="notifications.html" class="bell"><i class="fa fa-bell"></i><span>3</span></a><span data-user-name style="font-weight:600;color:var(--primary)"></span><div class="avatar" data-user-initial></div></div></header>
 <div class="content">{body}</div>
</div></div>
<script src="../js/api.js"></script><script src="../js/auth.js"></script><script src="../js/data.js"></script><script src="../js/main.js"></script>
<script>requireRole('{role}');{extra_js}</script>
</body></html>"""
    return html

def stat_cards(items):
    return '<div class="stats">' + "".join(f'<div class="stat-card"><i class="fa {i}"></i><div><b>{v}</b><small>{l}</small></div></div>' for i, v, l in items) + "</div>"

def panel(title, inner, action=""):
    return f'<div class="panel"><div class="panel-head"><h3>{title}</h3>{action}</div><div class="panel-body">{inner}</div></div>'

def table(tid, heads, tbody_id):
    return f'<div class="toolbar"><input id="{tid}_q" placeholder="Search..."><button class="btn btn-sm btn-primary" onclick="exportCSV(\'{tid}\')"><i class="fa fa-download"></i> Export</button></div><div class="table-wrap"><table id="{tid}"><thead><tr>' + "".join(f"<th>{h}</th>" for h in heads) + f'</tr></thead><tbody id="{tbody_id}"></tbody></table></div>'

def profile_body(role):
    fields = {"student": [("Roll No", "BSCS-2023-045"), ("Department", "Computer Science"), ("Semester", "5th"), ("Membership", "Active Member")],
              "member": [("Member ID", "YPDC-M-0231"), ("Directorate", "Training & Development"), ("Joined", "Sep 2024"), ("Status", "Active")],
              "directorate": [("Directorate", "Training & Development"), ("Role", "Director"), ("Team Size", "18"), ("Term", "2026")],
              "faculty": [("Designation", "Assistant Professor"), ("Department", "Management Sciences"), ("YPDC Role", "Faculty Coordinator"), ("Since", "2022")],
              "admin": [("Role", "Super Admin"), ("Access", "Full"), ("Last Login", "Today"), ("2FA", "Enabled")],
              "alumni": [("Batch", "2020"), ("Degree", "BBA"), ("Company", "Systems Ltd"), ("Position", "Product Manager")]}[role]
    info = "".join(f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in fields)
    form = """<form class="form" data-demo="Profile update ho gayi!"><div class="form-row"><div><label>Full Name</label><input data-user-name-input required></div><div><label>Email</label><input type="email" required></div></div>
    <div class="form-row"><div><label>Phone</label><input required></div><div><label>City</label><input></div></div><div><label>Bio</label><textarea rows="3"></textarea></div><button class="btn btn-primary">Save Changes</button></form>"""
    return f'<div class="profile-head"><div class="avatar" data-user-initial></div><div><h2 data-user-name style="color:var(--primary)"></h2><p style="color:var(--muted)">{PORTALS[role][0].replace(" Portal","")}</p></div></div><div class="grid grid-2">' + panel("Information", f'<table>{info}</table>') + panel("Edit Profile", form) + "</div>"

def generic_feature(role, f):
    """Return (body, js) for a feature page."""
    n = f.lower()
    if "profile" in n and "directorate" not in n:
        return profile_body(role), ""
    if n == "dashboard":
        return dashboard_body(role)
    if "event" in n and "proposal" not in n and "management" not in n:
        js = "renderRows('rows', DEMO.events, ['title','date','venue','type','status']);tableSearch('t_q','t');"
        act = '<button class="btn btn-sm btn-primary" onclick="toast(\'Event registration ho gayi!\',\'success\')"><i class="fa fa-ticket"></i> Register</button>' if role in ("student", "alumni") else ""
        return panel(f, table("t", ["Event", "Date", "Venue", "Type", "Status"], "rows"), act), js
    if "events management" in n:
        return panel("All Events", table("t", ["Event", "Date", "Venue", "Type", "Status"], "rows"), '<button class="btn btn-sm btn-primary" onclick="toast(\'Naya event add form (demo)\')"><i class="fa fa-plus"></i> Add Event</button>'), "renderRows('rows', DEMO.events, ['title','date','venue','type','status']);tableSearch('t_q','t');"
    if "proposal" in n:
        form = """<form class="form" data-demo="Proposal faculty approval ke liye bhej diya gaya."><div class="form-row"><div><label>Event Title</label><input required></div><div><label>Proposed Date</label><input type="date" required></div></div>
        <div class="form-row"><div><label>Venue</label><input required></div><div><label>Estimated Budget (PKR)</label><input type="number"></div></div><div><label>Objective / Description</label><textarea rows="3" required></textarea></div><button class="btn btn-primary">Submit Proposal</button></form>"""
        return panel("New Event Proposal", form) + panel("My Proposals", table("t", ["Event", "Date", "Venue", "Type", "Status"], "rows")), "renderRows('rows', DEMO.events.filter(e=>e.status!=='Approved'), ['title','date','venue','type','status']);"
    if "attendance" in n:
        act = '<button class="btn btn-sm btn-primary" onclick="toast(\'QR scanner open (demo)\')"><i class="fa fa-qrcode"></i> Mark via QR</button>' if role in ("student", "member", "alumni") else '<button class="btn btn-sm btn-primary" onclick="toast(\'QR code generate ho gaya (demo)\')"><i class="fa fa-qrcode"></i> Generate QR</button>'
        return stat_cards([("fa-check", "18", "Present"), ("fa-times", "2", "Absent"), ("fa-percent", "90%", "Attendance")]) + panel("Attendance Record", table("t", ["Event / Meeting", "Date", "Status"], "rows"), act), "renderRows('rows', DEMO.attendance, ['event','date','status']);tableSearch('t_q','t');"
    if "certificate" in n:
        rows = "".join(f"<tr><td>{c['no']}</td><td>{c['title']}</td><td>{c['date']}</td><td><button class='btn btn-sm btn-primary' onclick=\"toast('Certificate download (demo)','success')\"><i class='fa fa-download'></i></button> <button class='btn btn-sm btn-gold' onclick=\"toast('Verified: {c['no']}','success')\"><i class='fa fa-qrcode'></i></button></td></tr>" for c in
                       [{"no": "YPDC-2026-0142", "title": "Certificate of Participation — Orientation", "date": "2026-09-05"}, {"no": "YPDC-2026-0219", "title": "Volunteer Appreciation — Plantation Drive", "date": "2026-09-20"}])
        act = '<button class="btn btn-sm btn-primary" onclick="toast(\'Certificates issue ho gaye (demo)\',\'success\')"><i class="fa fa-certificate"></i> Issue Certificates</button>' if role in ("admin", "directorate") else ""
        return panel(f, f'<div class="table-wrap"><table><thead><tr><th>Certificate No</th><th>Title</th><th>Issued</th><th>Action</th></tr></thead><tbody>{rows}</tbody></table></div>', act), ""
    if "task" in n:
        act = '<button class="btn btn-sm btn-primary" onclick="toast(\'Assign task form (demo)\')"><i class="fa fa-plus"></i> Assign Task</button>' if role in ("directorate", "admin") else ""
        return stat_cards([("fa-tasks", "4", "Total"), ("fa-spinner", "2", "In Progress"), ("fa-check", "1", "Completed")]) + panel("Tasks", table("t", ["Task", "Assigned To", "Deadline", "Status"], "rows"), act), "renderRows('rows', DEMO.tasks, ['title','assigned','deadline','status']);tableSearch('t_q','t');"
    if "notification" in n:
        items = "".join(f"<div class='card' style='margin-bottom:10px;display:flex;gap:14px;align-items:center'><i class='fa fa-bell' style='color:var(--accent)'></i><div style='flex:1'><b>{x['msg']}</b><br><small style='color:var(--muted)'>{x['time']}</small></div></div>" for x in
                        [{"msg": "Leadership Summit registration open", "time": "2 hours ago"}, {"msg": "Your certificate has been issued", "time": "1 day ago"}, {"msg": "Task deadline tomorrow: Prepare event budget", "time": "2 days ago"}])
        act = '<button class="btn btn-sm btn-primary" onclick="toast(\'Notification bhej di gayi\',\'success\')"><i class="fa fa-paper-plane"></i> Send Notification</button>' if role == "admin" else ""
        return panel("Notifications", items, act), ""
    if "feedback" in n or "complaint" in n:
        if role in ("admin", "faculty"):
            rows = "<tr><td>Ali Raza</td><td>Feedback</td><td>Great summit, need more seats</td><td>2026-09-20</td><td>" + '<span class="badge badge-warning">Open</span>' + "</td></tr><tr><td>Sara Khan</td><td>Complaint</td><td>Attendance not marked</td><td>2026-09-22</td><td>" + '<span class="badge badge-success">Resolved</span>' + "</td></tr>"
            return panel(f, f'<div class="table-wrap"><table><thead><tr><th>From</th><th>Type</th><th>Message</th><th>Date</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>'), ""
        form = """<form class="form" data-demo="Feedback submit ho gaya. Shukriya!"><div class="form-row"><div><label>Type</label><select><option>Feedback</option><option>Suggestion</option><option>Complaint</option></select></div><div><label>Related Event</label><select><option>General</option><option>Leadership Summit 2026</option><option>Blood Donation Camp</option></select></div></div>
        <div><label>Rating</label><select><option>5 - Excellent</option><option>4 - Good</option><option>3 - Average</option><option>2 - Poor</option></select></div><div><label>Message</label><textarea rows="4" required></textarea></div><button class="btn btn-primary">Submit</button></form>"""
        return panel("Submit Feedback", form), ""
    if "achievement" in n:
        return cards([("fa-trophy", "Best Volunteer 2025", "Awarded for 120+ service hours."), ("fa-medal", "Event Excellence", "Leadership Summit organizing team."), ("fa-star", "Top Performer", "Highest task completion rate Q2 2026."), ("fa-award", "Community Hero", "Blood camp coordination.")], "grid-2"), ""
    if "performance" in n:
        return stat_cards([("fa-chart-line", "87%", "Overall Score"), ("fa-tasks", "92%", "Task Completion"), ("fa-clipboard-check", "90%", "Attendance"), ("fa-star", "4.6", "Rating")]) + panel("Performance Trend", '<div class="chart-box"><canvas id="perf"></canvas></div>'), \
               "new Chart(document.getElementById('perf'),{type:'line',data:{labels:['Apr','May','Jun','Jul','Aug','Sep'],datasets:[{label:'Score',data:[70,75,80,78,85,87],borderColor:'#1B9AAA',backgroundColor:'rgba(27,154,170,.15)',fill:true,tension:.4}]},options:{maintainAspectRatio:false}});"
    if "report" in n or "analytics" in n:
        act = '<button class="btn btn-sm btn-primary" onclick="toast(\'Report PDF export (demo)\',\'success\')"><i class="fa fa-file-pdf"></i> Export PDF</button>'
        return stat_cards([("fa-calendar", "42", "Events"), ("fa-users", "1200", "Members"), ("fa-certificate", "860", "Certificates"), ("fa-clipboard-check", "88%", "Avg Attendance")]) + '<div class="grid grid-2">' + panel("Events per Directorate", '<div class="chart-box"><canvas id="c1"></canvas></div>', act) + panel("Monthly Participation", '<div class="chart-box"><canvas id="c2"></canvas></div>') + "</div>", \
               "new Chart(document.getElementById('c1'),{type:'bar',data:{labels:DEMO.directorates.map(d=>d.name.split(' ')[0]),datasets:[{label:'Events',data:[9,12,7,6,5,3],backgroundColor:'#0B3D5C'}]},options:{maintainAspectRatio:false}});new Chart(document.getElementById('c2'),{type:'doughnut',data:{labels:['Students','Members','Alumni','Faculty'],datasets:[{data:[55,30,10,5],backgroundColor:['#1B9AAA','#0B3D5C','#E8B04B','#2E7D6B']}]},options:{maintainAspectRatio:false}});"
    if "document" in n or "publication" in n:
        rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td><button class='btn btn-sm btn-primary'><i class='fa fa-download'></i></button></td></tr>" for a, b, c in [("Work Plan 2026.pdf", "Plan", "2026-01-10"), ("Summit Budget.xlsx", "Finance", "2026-09-12"), ("Activity Report Aug.pdf", "Report", "2026-09-01"), ("Meeting Minutes.docx", "Minutes", "2026-09-15")])
        return panel("Documents", f'<div class="table-wrap"><table><thead><tr><th>File</th><th>Category</th><th>Uploaded</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>', '<button class="btn btn-sm btn-primary" onclick="toast(\'Upload dialog (demo)\')"><i class="fa fa-upload"></i> Upload</button>'), ""
    if "approval" in n or "application" in n:
        rows = "".join(f"<tr><td>{a['name']}</td><td>{a['type']}</td><td>{a['date']}</td><td>{{}}</td><td><button class='btn btn-sm btn-primary' onclick=\"toast('Approved','success')\"><i class='fa fa-check'></i></button> <button class='btn btn-sm btn-danger' onclick=\"toast('Rejected','error')\"><i class='fa fa-times'></i></button></td></tr>".replace("{}", f"<span class='badge badge-{'success' if a['status']=='Approved' else 'warning'}'>{a['status']}</span>") for a in
                       [{"name": "Hassan Ali", "type": "Membership", "date": "2026-09-20", "status": "Pending"}, {"name": "Tech Hackathon", "type": "Event Proposal", "date": "2026-09-21", "status": "Pending"}, {"name": "Noor Fatima", "type": "Volunteer", "date": "2026-09-22", "status": "Approved"}])
        return stat_cards([("fa-hourglass", "2", "Pending"), ("fa-check", "14", "Approved"), ("fa-times", "1", "Rejected")]) + panel(f, f'<div class="table-wrap"><table><thead><tr><th>Applicant / Item</th><th>Type</th><th>Date</th><th>Status</th><th>Action</th></tr></thead><tbody>{rows}</tbody></table></div>'), ""
    if "user management" in n or "member management" in n or "faculty management" in n or "team member" in n or "network" in n or "activities" in n:
        act = '<button class="btn btn-sm btn-primary" onclick="toast(\'Add form (demo)\')"><i class="fa fa-plus"></i> Add</button>' if role in ("admin", "directorate") else ""
        return panel(f, table("t", ["Name", "Email", "Role", "Status"], "rows"), act), "renderRows('rows', DEMO.users, ['name','email','role','status']);tableSearch('t_q','t');"
    if "directorate" in n:
        act = '<button class="btn btn-sm btn-primary" onclick="toast(\'Add directorate (demo)\')"><i class="fa fa-plus"></i> Add</button>' if role == "admin" else ""
        return panel(f, table("t", ["Directorate", "Director", "Assistant Director", "Members"], "rows"), act), "renderRows('rows', DEMO.directorates, ['name','director','asst','members']);tableSearch('t_q','t');"
    if "director" in n:
        return cards([("fa-user-tie", "Director — Hamza Ahmed", "Leads directorate strategy, approves tasks, reports to faculty coordinator."), ("fa-user", "Assistant Director — Zainab Ali", "Coordinates team, tracks attendance and work plan execution.")], "grid-2"), ""
    if "objective" in n or "responsib" in n or "role" in n and "permission" not in n or "designation" in n or "skill" in n or "academic" in n or "professional" in n:
        items = {"objective": ["Conduct 8 training workshops this year", "Achieve 85%+ member attendance", "Launch mentorship program", "Publish quarterly activity reports"],
                 "responsib": ["Attend monthly directorate meetings", "Complete assigned tasks before deadline", "Support event execution as duty officer", "Maintain code of conduct"],
                 "role": ["Faculty Coordinator — Training & Development", "Approve event proposals & budgets", "Supervise directorate performance", "Evaluate student/member activities"],
                 "designation": ["Assistant Professor", "Department of Management Sciences", "Office: Block C, Room 214", "Office hours: Mon–Wed 11–1"],
                 "skill": ["Project Management", "Public Speaking", "Data Analysis", "Team Leadership", "Digital Marketing"],
                 "academic": ["BBA (Hons) — 2016–2020, CGPA 3.7", "Final Year Project: Youth Engagement Study", "Dean's Honour List — 2019", "YPDC Member 2017–2020 (Director PR)"],
                 "professional": ["Product Manager — Systems Ltd (2023–Present)", "Business Analyst — Netsol (2020–2023)", "Certifications: PMP, Google PM"]}
        key = next(k for k in items if k in n)
        li = "".join(f"<li style='padding:10px 0;border-bottom:1px solid var(--border)'><i class='fa fa-check-circle' style='color:var(--success);margin-right:10px'></i>{x}</li>" for x in items[key])
        return panel(f, f"<ul style='list-style:none'>{li}</ul>", '<button class="btn btn-sm btn-primary" onclick="toast(\'Edit (demo)\')"><i class="fa fa-edit"></i> Edit</button>'), ""
    if "work plan" in n:
        rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{badge}</td></tr>" for a, b, c, badge in [("Q1", "Orientation & recruitment", "Jan–Mar", "<span class='badge badge-success'>Done</span>"), ("Q2", "Skill workshops series", "Apr–Jun", "<span class='badge badge-success'>Done</span>"), ("Q3", "Leadership Summit", "Jul–Sep", "<span class='badge badge-info'>In Progress</span>"), ("Q4", "Annual report & awards", "Oct–Dec", "<span class='badge badge-warning'>Planned</span>")])
        return panel("Annual Work Plan 2026", f'<div class="table-wrap"><table><thead><tr><th>Quarter</th><th>Activity</th><th>Timeline</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>'), ""
    if "volunteer" in n or "career" in n or "mentorship" in n:
        data = {"volunteer": [("Leadership Summit 2026", "Registration desk, 10 volunteers needed"), ("Blood Donation Camp", "Donor coordination, 15 volunteers"), ("Plantation Drive", "Field work, 30 volunteers")],
                "career": [("Software Engineer — Systems Ltd", "Lahore · Full-time · Apply by 15 Oct"), ("Marketing Intern — Nestlé", "Lahore · Internship · 3 months"), ("Business Analyst — Netsol", "Remote · Full-time")],
                "mentorship": [("Usman Tariq — Product Management", "Available: Weekends · 3 slots"), ("Amna Riaz — Marketing", "Available: Evenings · 2 slots"), ("Danish Ali — Software Engineering", "Available: Weekdays · 5 slots")]}
        key = next(k for k in data if k in n)
        return cards([("fa-hands-helping" if key == "volunteer" else "fa-briefcase" if key == "career" else "fa-handshake", t, d + '<br><br><button class="btn btn-sm btn-primary" onclick="toast(\'Request bhej di gayi\',\'success\')">Apply / Join</button>') for t, d in data[key]]), ""
    if "website content" in n:
        form = """<form class="form" data-demo="Content update ho gaya!"><div><label>Page</label><select><option>Home</option><option>About YPDC</option><option>Vision & Mission</option><option>News & Updates</option><option>Gallery</option><option>FAQs</option></select></div>
        <div><label>Title</label><input required></div><div><label>Content</label><textarea rows="6" required></textarea></div><div><label>Image</label><input type="file"></div><button class="btn btn-primary">Publish</button></form>"""
        return panel("Website Content Manager (CMS)", form), ""
    if "permission" in n:
        roles = ["Student", "Member", "Directorate", "Faculty", "Admin", "Alumni"]
        perms = ["View Events", "Register Events", "Manage Tasks", "Mark Attendance", "Issue Certificates", "Approve Proposals", "Manage Users", "Edit Website"]
        rows = "".join("<tr><td><b>" + p + "</b></td>" + "".join(f"<td><input type='checkbox' style='width:auto' {'checked' if (r=='Admin' or (i<2) or (r in ('Directorate','Member') and i==2) or (r=='Faculty' and i==5) or (r=='Directorate' and i==3)) else ''}></td>" for r in roles) + "</tr>" for i, p in enumerate(perms))
        return panel("Roles & Permissions", f'<div class="table-wrap"><table><thead><tr><th>Permission</th>' + "".join(f"<th>{r}</th>" for r in roles) + f'</tr></thead><tbody>{rows}</tbody></table></div><br><button class="btn btn-primary" onclick="toast(\'Permissions save ho gayi\',\'success\')">Save Changes</button>'), ""
    if "membership" in n:
        return stat_cards([("fa-id-card", "Active", "Status"), ("fa-calendar", "Sep 2024", "Member Since"), ("fa-sitemap", "T&D", "Directorate")]) + panel("Membership Details", "<p>Membership ID: <b>YPDC-M-0231</b><br>Type: Regular Member<br>Valid till: Dec 2026</p><br><button class='btn btn-primary' onclick=\"toast('Membership card download (demo)','success')\"><i class='fa fa-download'></i> Download Membership Card</button>"), ""
    return panel(f, "<p>Module content yahan aayega.</p>"), ""

def dashboard_body(role):
    stats = {"student": [("fa-calendar", "5", "Upcoming Events"), ("fa-clipboard-check", "90%", "Attendance"), ("fa-certificate", "2", "Certificates"), ("fa-trophy", "1", "Achievements")],
             "member": [("fa-tasks", "4", "My Tasks"), ("fa-calendar", "3", "Duties"), ("fa-clipboard-check", "92%", "Attendance"), ("fa-chart-line", "87%", "Performance")],
             "directorate": [("fa-users", "18", "Team Members"), ("fa-tasks", "12", "Active Tasks"), ("fa-calendar", "4", "Events"), ("fa-lightbulb", "2", "Proposals")],
             "faculty": [("fa-check-double", "3", "Pending Approvals"), ("fa-calendar", "6", "Events"), ("fa-users", "45", "Supervised Members"), ("fa-file-alt", "8", "Reports")],
             "admin": [("fa-users", "1240", "Total Users"), ("fa-id-badge", "860", "Members"), ("fa-calendar", "42", "Events"), ("fa-hourglass", "7", "Pending Approvals")],
             "alumni": [("fa-network-wired", "320", "Alumni Network"), ("fa-handshake", "3", "Mentees"), ("fa-briefcase", "12", "Job Openings"), ("fa-calendar", "2", "Alumni Events")]}[role]
    body = f"<h2 style='color:var(--primary);margin-bottom:4px'>Welcome, <span data-user-name></span> 👋</h2><p style='color:var(--muted);margin-bottom:22px'>Yahan aapka summary hai.</p>" + stat_cards(stats)
    body += '<div class="grid grid-2">' + panel("Upcoming Events", '<div class="table-wrap"><table><thead><tr><th>Event</th><th>Date</th><th>Status</th></tr></thead><tbody id="dEv"></tbody></table></div>')
    body += panel("Recent Notifications", "".join(f"<div style='padding:10px 0;border-bottom:1px solid var(--border)'><i class='fa fa-bell' style='color:var(--accent);margin-right:8px'></i>{m} <small style='color:var(--muted);float:right'>{t}</small></div>" for m, t in
                  [("Leadership Summit registration open", "2h"), ("Your certificate has been issued", "1d"), ("Task deadline tomorrow", "2d")])) + "</div>"
    if role in ("admin", "directorate", "faculty"):
        body += panel("Activity Overview", '<div class="chart-box"><canvas id="dc"></canvas></div>')
    js = "renderRows('dEv', DEMO.events.slice(0,4), ['title','date','status']);"
    if role in ("admin", "directorate", "faculty"):
        js += "new Chart(document.getElementById('dc'),{type:'bar',data:{labels:['Apr','May','Jun','Jul','Aug','Sep'],datasets:[{label:'Events',data:[4,6,5,7,8,9],backgroundColor:'#1B9AAA'},{label:'Participants',data:[120,180,150,220,260,300],backgroundColor:'#0B3D5C'}]},options:{maintainAspectRatio:false}});"
    return body, js

CHART = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
for role, (pname, picon, feats) in PORTALS.items():
    pages = list(feats) if feats[0] == "Dashboard" else ["Dashboard"] + list(feats)
    for f in pages:
        body, js = generic_feature(role, f)
        html = portal_shell(role, pname, f, body, js)
        if "Chart(" in js:
            html = html.replace('<script src="../js/api.js">', CHART + '<script src="../js/api.js">')
        open(f"{ROOT}/{role}/{slug(f)}.html", "w").write(html)
    if "Notifications" not in feats:  # bell icon target (not in sidebar)
        body, js = generic_feature(role, "Notifications")
        open(f"{ROOT}/{role}/notifications.html", "w").write(portal_shell(role, pname, "Notifications", body, js))

open(f"{ROOT}/css/style.css", "w").write(CSS)
open(f"{ROOT}/css/portal.css", "w").write(PORTAL_CSS)
open(f"{ROOT}/js/api.js", "w").write(API_JS)
open(f"{ROOT}/js/auth.js", "w").write(AUTH_JS)
open(f"{ROOT}/js/main.js", "w").write(MAIN_JS)
open(f"{ROOT}/js/data.js", "w").write(DATA_JS)

# ------------------------------------------------------------------ BACKEND (Node.js starter)
open(f"{ROOT}/backend/package.json", "w").write(json.dumps({
    "name": "ypdc-backend", "version": "1.0.0", "main": "server.js",
    "scripts": {"start": "node server.js", "dev": "nodemon server.js"},
    "dependencies": {"express": "^4.19.2", "cors": "^2.8.5", "jsonwebtoken": "^9.0.2", "bcryptjs": "^2.4.3", "dotenv": "^16.4.5", "pg": "^8.11.3"}
}, indent=2))
open(f"{ROOT}/backend/.env.example", "w").write("PORT=5000\nJWT_SECRET=change_this_secret\nDATABASE_URL=postgresql://user:password@localhost:5432/ypdc\n")
open(f"{ROOT}/backend/server.js", "w").write("""// ====== YPDC Backend — Node.js + Express starter ======
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const app = express();
app.use(cors());
app.use(express.json());
const SECRET = process.env.JWT_SECRET || 'dev_secret';

// ---- Demo in-memory data (PostgreSQL se replace karein: see schema.sql) ----
const users = [
  { id: 1, name: 'Ali Raza', email: 'student@ypdc.org', role: 'student', password: bcrypt.hashSync('123456', 8) },
  { id: 2, name: 'Sara Khan', email: 'member@ypdc.org', role: 'member', password: bcrypt.hashSync('123456', 8) },
  { id: 3, name: 'Hamza Ahmed', email: 'director@ypdc.org', role: 'directorate', password: bcrypt.hashSync('123456', 8) },
  { id: 4, name: 'Dr. Ayesha Malik', email: 'faculty@ypdc.org', role: 'faculty', password: bcrypt.hashSync('123456', 8) },
  { id: 5, name: 'Admin', email: 'admin@ypdc.org', role: 'admin', password: bcrypt.hashSync('123456', 8) },
  { id: 6, name: 'Usman Tariq', email: 'alumni@ypdc.org', role: 'alumni', password: bcrypt.hashSync('123456', 8) },
];
const events = [
  { id: 1, title: 'Leadership Summit 2026', date: '2026-10-12', venue: 'Main Auditorium', type: 'Seminar', status: 'Approved' },
  { id: 2, title: 'Blood Donation Camp', date: '2026-10-20', venue: 'Campus Ground', type: 'Social', status: 'Approved' },
];
const registrations = [], attendance = [], certificates = [];

// ---- Middleware ----
const auth = (roles = []) => (req, res, next) => {
  const token = (req.headers.authorization || '').replace('Bearer ', '');
  try {
    req.user = jwt.verify(token, SECRET);
    if (roles.length && !roles.includes(req.user.role)) return res.status(403).json({ message: 'Forbidden' });
    next();
  } catch { res.status(401).json({ message: 'Unauthorized' }); }
};

// ---- Auth ----
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  const u = users.find(x => x.email === email);
  if (!u || !bcrypt.compareSync(password, u.password)) return res.status(400).json({ message: 'Invalid credentials' });
  const token = jwt.sign({ id: u.id, role: u.role, name: u.name }, SECRET, { expiresIn: '1d' });
  res.json({ token, user: { id: u.id, name: u.name, email: u.email, role: u.role } });
});
app.post('/api/auth/register', (req, res) => {
  const { name, email, password, role = 'student' } = req.body;
  if (users.find(x => x.email === email)) return res.status(400).json({ message: 'Email exists' });
  const u = { id: users.length + 1, name, email, role, password: bcrypt.hashSync(password, 8) };
  users.push(u); res.status(201).json({ message: 'Registered', id: u.id });
});
app.get('/api/auth/me', auth(), (req, res) => res.json(req.user));

// ---- Users (admin) ----
app.get('/api/admin/users', auth(['admin']), (req, res) => res.json(users.map(({ password, ...u }) => u)));

// ---- Events ----
app.get('/api/events', (req, res) => res.json(events));
app.post('/api/events/proposals', auth(['directorate', 'admin']), (req, res) => {
  const e = { id: events.length + 1, ...req.body, status: 'Proposed', proposedBy: req.user.id };
  events.push(e); res.status(201).json(e);
});
app.put('/api/events/:id/approve', auth(['faculty', 'admin']), (req, res) => {
  const e = events.find(x => x.id == req.params.id); if (!e) return res.status(404).json({ message: 'Not found' });
  e.status = req.body.status || 'Approved'; res.json(e);
});
app.post('/api/events/:id/register', auth(), (req, res) => {
  registrations.push({ eventId: +req.params.id, userId: req.user.id, role: req.body.role || 'participant' });
  res.status(201).json({ message: 'Registered' });
});

// ---- Attendance ----
app.post('/api/attendance/mark', auth(['directorate', 'admin', 'faculty']), (req, res) => {
  attendance.push({ ...req.body, markedBy: req.user.id, time: new Date() }); res.status(201).json({ message: 'Marked' });
});
app.get('/api/attendance/user/:id', auth(), (req, res) => res.json(attendance.filter(a => a.userId == req.params.id)));

// ---- Certificates ----
app.post('/api/certificates/issue', auth(['admin', 'directorate']), (req, res) => {
  const c = { no: 'YPDC-' + new Date().getFullYear() + '-' + String(certificates.length + 1).padStart(4, '0'), ...req.body, issuedAt: new Date() };
  certificates.push(c); res.status(201).json(c);
});
app.get('/api/certificates/my', auth(), (req, res) => res.json(certificates.filter(c => c.userId == req.user.id)));
app.get('/api/verify/:no', (req, res) => {
  const c = certificates.find(x => x.no === req.params.no);
  c ? res.json({ valid: true, certificate: c }) : res.status(404).json({ valid: false });
});

// ---- Public forms ----
app.post('/api/public/contact', (req, res) => res.json({ message: 'Message received' }));
app.post('/api/public/volunteer', (req, res) => res.json({ message: 'Volunteer registered' }));
app.post('/api/public/membership', (req, res) => res.json({ message: 'Application submitted' }));

app.get('/api/reports/dashboard', auth(['admin', 'faculty', 'directorate']), (req, res) =>
  res.json({ users: users.length, events: events.length, registrations: registrations.length, certificates: certificates.length }));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log('YPDC API running on http://localhost:' + PORT));
""")
open(f"{ROOT}/backend/schema.sql", "w").write("""-- ====== YPDC PostgreSQL Schema ======
CREATE TABLE roles (id SERIAL PRIMARY KEY, name VARCHAR(30) UNIQUE NOT NULL);
INSERT INTO roles(name) VALUES ('student'),('member'),('directorate'),('faculty'),('admin'),('alumni');

CREATE TABLE users (
  id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(120) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL, role_id INT REFERENCES roles(id), phone VARCHAR(20),
  status VARCHAR(20) DEFAULT 'active', created_at TIMESTAMP DEFAULT NOW());

CREATE TABLE permissions (id SERIAL PRIMARY KEY, key VARCHAR(60) UNIQUE NOT NULL);
CREATE TABLE role_permissions (role_id INT REFERENCES roles(id), permission_id INT REFERENCES permissions(id), PRIMARY KEY(role_id, permission_id));

CREATE TABLE directorates (
  id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, description TEXT,
  director_id INT REFERENCES users(id), asst_director_id INT REFERENCES users(id),
  objectives TEXT, work_plan TEXT);

CREATE TABLE profiles (
  user_id INT PRIMARY KEY REFERENCES users(id), member_id VARCHAR(30) UNIQUE, roll_no VARCHAR(30),
  department VARCHAR(100), designation VARCHAR(100), directorate_id INT REFERENCES directorates(id),
  batch VARCHAR(10), company VARCHAR(100), position VARCHAR(100), skills TEXT, bio TEXT);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY, title VARCHAR(150) NOT NULL, description TEXT,
  assigned_to INT REFERENCES users(id), assigned_by INT REFERENCES users(id),
  directorate_id INT REFERENCES directorates(id), deadline DATE,
  status VARCHAR(20) DEFAULT 'pending', performance_score INT);

CREATE TABLE events (
  id SERIAL PRIMARY KEY, title VARCHAR(150) NOT NULL, description TEXT, type VARCHAR(50),
  event_date DATE, venue VARCHAR(150), budget NUMERIC, directorate_id INT REFERENCES directorates(id),
  proposed_by INT REFERENCES users(id), status VARCHAR(20) DEFAULT 'proposed',
  approved_by_faculty INT REFERENCES users(id), approved_by_admin INT REFERENCES users(id), created_at TIMESTAMP DEFAULT NOW());

CREATE TABLE event_registrations (
  id SERIAL PRIMARY KEY, event_id INT REFERENCES events(id), user_id INT REFERENCES users(id),
  role VARCHAR(20) DEFAULT 'participant', status VARCHAR(20) DEFAULT 'registered', UNIQUE(event_id, user_id));

CREATE TABLE attendance (
  id SERIAL PRIMARY KEY, event_id INT REFERENCES events(id), user_id INT REFERENCES users(id),
  marked_by INT REFERENCES users(id), method VARCHAR(10) DEFAULT 'manual', status VARCHAR(10) DEFAULT 'present',
  marked_at TIMESTAMP DEFAULT NOW());

CREATE TABLE certificates (
  id SERIAL PRIMARY KEY, certificate_no VARCHAR(30) UNIQUE NOT NULL, user_id INT REFERENCES users(id),
  event_id INT REFERENCES events(id), title VARCHAR(150), pdf_url TEXT, issued_at TIMESTAMP DEFAULT NOW());

CREATE TABLE achievements (id SERIAL PRIMARY KEY, owner_type VARCHAR(20), owner_id INT, title VARCHAR(150), description TEXT, achieved_on DATE);
CREATE TABLE reports (id SERIAL PRIMARY KEY, directorate_id INT REFERENCES directorates(id), created_by INT REFERENCES users(id), title VARCHAR(150), content TEXT, file_url TEXT, created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE documents (id SERIAL PRIMARY KEY, owner_type VARCHAR(20), owner_id INT, title VARCHAR(150), category VARCHAR(50), file_url TEXT, uploaded_at TIMESTAMP DEFAULT NOW());
CREATE TABLE notifications (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), message TEXT, type VARCHAR(20), read_at TIMESTAMP, created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE feedback (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), event_id INT, type VARCHAR(20), rating INT, message TEXT, status VARCHAR(20) DEFAULT 'open', created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE applications (id SERIAL PRIMARY KEY, type VARCHAR(30), applicant_name VARCHAR(100), email VARCHAR(120), data JSONB, status VARCHAR(20) DEFAULT 'pending', reviewed_by INT, created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE mentorships (id SERIAL PRIMARY KEY, mentor_id INT REFERENCES users(id), mentee_id INT REFERENCES users(id), area VARCHAR(100), status VARCHAR(20) DEFAULT 'active');
CREATE TABLE career_opportunities (id SERIAL PRIMARY KEY, title VARCHAR(150), company VARCHAR(100), type VARCHAR(30), location VARCHAR(100), posted_by INT, deadline DATE);
CREATE TABLE cms_content (id SERIAL PRIMARY KEY, page_key VARCHAR(50), title VARCHAR(150), content TEXT, media_url TEXT, updated_by INT, updated_at TIMESTAMP DEFAULT NOW());
""")

open(f"{ROOT}/README.md", "w").write("""# YPDC — Website & Portal System

Pure **HTML + CSS + JavaScript** frontend, **Node.js + Express** backend, **PostgreSQL** schema.

## Folder Structure
```
ypdc-website/
├── index.html, about-ypdc.html, events.html ...   → Public website (14 pages)
├── login.html, register.html                      → Auth
├── student/  member/  directorate/  faculty/  admin/  alumni/   → 6 Portals (har feature ka apna page)
├── css/   style.css (global), portal.css (dashboard layout)
├── js/    api.js (fetch wrapper), auth.js (login/role guard), main.js (UI helpers), data.js (demo data)
├── backend/  server.js (Express API), schema.sql (PostgreSQL), package.json
└── YPDC_Website_Report.pdf  → 5-page project report
```

## Frontend chalane ka tariqa
Koi bhi static server:
```bash
cd ypdc-website
python3 -m http.server 8080
```
Browser: http://localhost:8080

## Demo Login (backend ke bina bhi kaam karta hai)
Password sab ka: `123456`

| Portal | Email |
|---|---|
| Student | student@ypdc.org |
| Member | member@ypdc.org |
| Directorate | director@ypdc.org |
| Faculty | faculty@ypdc.org |
| Admin | admin@ypdc.org |
| Alumni | alumni@ypdc.org |

## Backend chalane ka tariqa
```bash
cd backend
npm install
cp .env.example .env
npm start          # http://localhost:5000
```
Frontend `js/api.js` mein `API_BASE` backend URL par set karein. PostgreSQL ke liye `schema.sql` run karein.
""")
shutil.copy("/home/user/noor-academy-frontend/docs/YPDC_Website_Report.pdf", f"{ROOT}/YPDC_Website_Report.pdf")
print("site built:", sum(len(f) for _, _, f in os.walk(ROOT)), "files")
