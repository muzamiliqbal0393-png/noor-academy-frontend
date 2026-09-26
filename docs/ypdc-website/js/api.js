// ====== api.js — Backend se baat karne ka wrapper ======
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
