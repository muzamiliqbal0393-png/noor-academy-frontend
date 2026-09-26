// ====== data.js — Demo data (backend connect hone par API se aayega) ======
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
    { name: 'Ali Raza', email: 'volunteer@ypdc.org', role: 'Volunteer', status: 'Active' },
    { name: 'Sara Khan', email: 'member@ypdc.org', role: 'General Member', status: 'Active' },
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
