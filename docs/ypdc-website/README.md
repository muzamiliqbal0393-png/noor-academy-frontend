# YPDC — Website & Portal System

Pure **HTML + CSS + JavaScript** frontend, **Node.js + Express** backend, **PostgreSQL** schema.

## Folder Structure
```
ypdc-website/
├── index.html, about-ypdc.html, events.html ...   → Public website (14 pages)
├── login.html, register.html                      → Auth
├── student/ (Volunteer)  member/ (General Member)  directorate/  faculty/  admin/  alumni/   → 6 Portals (har feature ka apna page)
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
| Volunteer | volunteer@ypdc.org |
| General Member | member@ypdc.org |
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
