// ====== auth.js — Login, role check, logout ======
const ROLE_HOME = {
  student: 'student/dashboard.html', member: 'member/dashboard.html', directorate: 'directorate/dashboard.html',
  faculty: 'faculty/dashboard.html', admin: 'admin/dashboard.html', alumni: 'alumni/dashboard.html'
};
// Demo accounts (backend ke bina test ke liye)
const DEMO_USERS = {
  'volunteer@ypdc.org': { role: 'student', name: 'Ali Raza' },
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
