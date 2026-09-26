// ====== YPDC Backend — Node.js + Express starter ======
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
  { id: 1, name: 'Ali Raza', email: 'volunteer@ypdc.org', role: 'student', password: bcrypt.hashSync('123456', 8) },
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
