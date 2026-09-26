from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, KeepTogether)
from reportlab.lib.enums import TA_CENTER

PRIMARY = colors.HexColor("#0B3D5C")   # deep navy
ACCENT = colors.HexColor("#1B9AAA")    # teal
GOLD = colors.HexColor("#E8B04B")
LIGHT = colors.HexColor("#EEF5F8")
GREY = colors.HexColor("#5A6B77")
WHITE = colors.white

W, H = A4
OUT = "/home/user/noor-academy-frontend/docs/YPDC_Website_Report.pdf"

# ---------- styles ----------
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=20, textColor=PRIMARY, spaceAfter=4, leading=24)
sub = ParagraphStyle("sub", fontName="Helvetica", fontSize=10, textColor=GREY, spaceAfter=10)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12.5, textColor=WHITE, leading=15)
h3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10.5, textColor=PRIMARY, spaceBefore=4, spaceAfter=2)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=9, leading=12.5, textColor=colors.HexColor("#222"))
small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5)
cell = ParagraphStyle("cell", parent=body, fontSize=8.2, leading=10.5)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold", textColor=PRIMARY)
cellw = ParagraphStyle("cellw", parent=cell, fontName="Helvetica-Bold", textColor=WHITE)
center = ParagraphStyle("c", parent=body, alignment=TA_CENTER)


def section(title):
    t = Table([[Paragraph(title, h2)]], colWidths=[W - 3 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBEFORE", (0, 0), (0, -1), 4, GOLD),
    ]))
    return [t, Spacer(1, 6)]


def grid(rows, widths, header=True, zebra=True):
    data = []
    for i, r in enumerate(rows):
        st = cellw if (header and i == 0) else cell
        data.append([Paragraph(str(c), st) if not isinstance(c, Paragraph) else c for c in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D6DE")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), ACCENT))
    if zebra:
        for i in range(1 if header else 0, len(rows)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(style))
    return t


def portal_card(title, tagline, features, badge_color):
    """Two-column feature card for a portal."""
    n = (len(features) + 2) // 3
    cols = [features[i * n:(i + 1) * n] for i in range(3)]
    for c in cols: c += [""] * (n - len(c))
    rows = [[Paragraph(("&bull; " + x) if x else "", cell) for x in r] for r in zip(*cols)]
    inner = Table(rows, colWidths=[(W - 3 * cm - 12) / 3] * 3)
    inner.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                               ("LEFTPADDING", (0, 0), (-1, -1), 2)]))
    head = Table([[Paragraph(title, ParagraphStyle("pt", parent=cellb, fontSize=10, textColor=WHITE)),
                   Paragraph(tagline, ParagraphStyle("tg", parent=cell, textColor=WHITE, fontSize=7.8))]],
                 colWidths=[5.2 * cm, W - 3 * cm - 5.2 * cm])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), badge_color),
                              ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                              ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    outer = Table([[head], [inner]], colWidths=[W - 3 * cm])
    outer.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, badge_color),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return KeepTogether([outer, Spacer(1, 6)])


# ---------- page decorations ----------
def on_page(canvas, doc):
    canvas.saveState()
    # top bar
    canvas.setFillColor(PRIMARY); canvas.rect(0, H - 1.1 * cm, W, 1.1 * cm, stroke=0, fill=1)
    canvas.setFillColor(GOLD); canvas.rect(0, H - 1.2 * cm, W, 0.1 * cm, stroke=0, fill=1)
    canvas.setFillColor(WHITE); canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.5 * cm, H - 0.72 * cm, "YPDC  |  Youth Professional Development Council — Website System Report")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(W - 1.5 * cm, H - 0.72 * cm, "September 2026")
    # footer
    canvas.setFillColor(GREY); canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5 * cm, 0.7 * cm, "Confidential — Project Planning Document")
    canvas.drawRightString(W - 1.5 * cm, 0.7 * cm, f"Page {doc.page} of 5")
    canvas.setStrokeColor(ACCENT); canvas.setLineWidth(0.6)
    canvas.line(1.5 * cm, 1.0 * cm, W - 1.5 * cm, 1.0 * cm)
    canvas.restoreState()


def cover_page(canvas, doc):
    on_page(canvas, doc)
    canvas.saveState()
    top = H - 1.2 * cm; bh = 4.6 * cm
    canvas.setFillColor(PRIMARY); canvas.rect(0, top - bh, W, bh, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#124D70")); canvas.circle(W - 2.5 * cm, top - 0.5 * cm, 3 * cm, stroke=0, fill=1)
    canvas.setFillColor(GOLD); canvas.rect(0, top - bh, W, 0.12 * cm, stroke=0, fill=1)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 26); canvas.drawString(1.5 * cm, top - 1.3 * cm, "YPDC — Website & Portal System")
    canvas.setFont("Helvetica", 11); canvas.drawString(1.5 * cm, top - 2.0 * cm, "Youth Professional Development Council")
    canvas.setFont("Helvetica-Bold", 12); canvas.setFillColor(GOLD)
    canvas.drawString(1.5 * cm, top - 2.9 * cm, "Project Report: Features  ·  Frontend  ·  Backend  ·  Architecture")
    canvas.setFillColor(colors.HexColor("#B9D3E0")); canvas.setFont("Helvetica", 8.5)
    canvas.drawString(1.5 * cm, top - 3.6 * cm, "Portals: Student · Member · Directorate · Faculty · Admin · Alumni · Public   |   Version 1.0   |   September 2026")
    canvas.restoreState()
    return
    canvas.setFillColor(PRIMARY); canvas.rect(0, 0, W, H, stroke=0, fill=1)
    canvas.setFillColor(ACCENT); canvas.rect(0, H * 0.42, W, 0.25 * cm, stroke=0, fill=1)
    canvas.setFillColor(GOLD); canvas.rect(0, H * 0.42 - 0.12 * cm, W, 0.12 * cm, stroke=0, fill=1)
    # decorative circles
    canvas.setFillColor(colors.HexColor("#124D70"))
    canvas.circle(W - 3 * cm, H - 3 * cm, 5 * cm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#0E4666"))
    canvas.circle(2 * cm, 4 * cm, 4 * cm, stroke=0, fill=1)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 44); canvas.drawString(2 * cm, H * 0.66, "YPDC")
    canvas.setFont("Helvetica", 15); canvas.drawString(2 * cm, H * 0.66 - 0.9 * cm, "Youth Professional Development Council")
    canvas.setFont("Helvetica-Bold", 24); canvas.drawString(2 * cm, H * 0.54, "Website & Portal System")
    canvas.setFont("Helvetica", 13); canvas.setFillColor(GOLD)
    canvas.drawString(2 * cm, H * 0.54 - 0.9 * cm, "Project Report — Features, Frontend, Backend & Architecture")
    canvas.setFillColor(WHITE); canvas.setFont("Helvetica", 10.5)
    y = H * 0.36
    for line in ["Document Type : System Design & Feature Specification",
                 "Portals       : Student · Member · Directorate · Faculty · Admin · Alumni · Public",
                 "Version       : 1.0", "Date          : September 2026"]:
        canvas.drawString(2 * cm, y, line); y -= 0.65 * cm
    canvas.setFont("Helvetica-Oblique", 9); canvas.setFillColor(colors.HexColor("#B9D3E0"))
    canvas.drawString(2 * cm, 1.6 * cm, "Prepared as a professional planning report for website development.")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                      topMargin=1.7 * cm, bottomMargin=1.4 * cm, title="YPDC Website System Report",
                      author="YPDC")
frame = Frame(doc.leftMargin, doc.bottomMargin, W - 3 * cm, H - 3.1 * cm, id="f", leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
cframe = Frame(doc.leftMargin, doc.bottomMargin, W - 3 * cm, H - 3.1 * cm - 4.9 * cm, id="cf", leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="cover", frames=[cframe], onPage=cover_page),
                      PageTemplate(id="body", frames=[frame], onPage=on_page)])

S = []
from reportlab.platypus import NextPageTemplate
S.append(NextPageTemplate("body"))

# ================= PAGE 1: Overview + Student + Member =================
S.append(Paragraph("1. Project Overview", h1))
S.append(Paragraph("YPDC website ek complete web platform hai jis mein ek public website aur 6 role-based portals hain. "
                   "Har user apni role ke mutabiq login kar ke apna portal use karega.", sub))

ov = [["Item", "Detail"],
      ["Project", "YPDC Official Website + Multi-Portal Management System"],
      ["Users / Roles", "Student, Member, Directorate (Director / Asst. Director), Faculty, Admin, Alumni, Guest (Public)"],
      ["Core Modules", "Profiles, Membership, Events, Attendance, Certificates, Tasks, Reports, Notifications, Feedback"],
      ["Access Model", "Single login page -> role detect -> related portal dashboard open (Guest ko login ki zaroorat nahi)"]]
S.append(grid(ov, [3.5 * cm, W - 3 * cm - 3.5 * cm]))
S.append(Spacer(1, 10))

S.extend(section("2. Portals & Features"))
S.append(portal_card("1. Student Portal", "Students ke liye — events, volunteering, attendance aur certificates",
                     ["Profile", "Membership", "Events", "Event Registration", "Volunteer Opportunities",
                      "Attendance", "Certificates", "Achievements", "Notifications", "Feedback"], ACCENT))
S.append(portal_card("2. Member Portal", "Registered members — directorate work, tasks aur performance",
                     ["Profile & Member ID", "Directorate", "Responsibilities", "Tasks", "Events / Duties",
                      "Attendance", "Certificates", "Performance", "Reports", "Notifications"],
                     colors.HexColor("#2E7D6B")))
S.append(portal_card("3. Directorate Portal", "Director / Assistant Director — team, planning aur activity management",
                     ["Directorate Profile", "Director / Assistant Director", "Team Members", "Objectives", "Work Plan",
                      "Tasks", "Events & Activities", "Event Proposals", "Attendance", "Activity Reports",
                      "Achievements", "Documents", "Performance"], colors.HexColor("#5B4B9B")))
S.append(PageBreak())

# ================= PAGE 2: Remaining portals =================
S.append(Paragraph("2. Portals & Features (continued)", h1))
S.append(portal_card("4. Faculty Portal", "Faculty advisors — approvals, monitoring aur reports",
                     ["Faculty Profile", "Department / Designation", "YPDC Role", "Events",
                      "Student / Member Activities", "Approvals", "Reports", "Feedback", "Notifications"],
                     colors.HexColor("#B5651D")))
S.append(portal_card("5. Admin Portal", "Full control — poore system ka management",
                     ["Dashboard", "User Management", "Member Management", "Directorate Management",
                      "Faculty Management", "Events Management", "Applications & Approvals", "Attendance",
                      "Certificates", "Reports & Analytics", "Notifications", "Website Content", "Documents",
                      "Feedback / Complaints", "Roles & Permissions"], colors.HexColor("#B3282D")))
S.append(portal_card("6. Alumni Portal", "Purane members — network, mentorship aur career",
                     ["Alumni Profile", "Academic Information", "Professional Information", "Skills",
                      "Alumni Network", "Mentorship", "Events", "Achievements", "Career Opportunities",
                      "Volunteer / Support Opportunities"], colors.HexColor("#1F6FB2")))
S.append(portal_card("7. Guest / Public Portal (Website)", "Bina login — public information website",
                     ["About YPDC", "Vision & Mission", "Leadership", "Directorates", "Projects", "Events",
                      "News & Updates", "Achievements", "Gallery", "Publications", "Membership",
                      "Volunteer Registration", "Contact Us", "FAQs"], PRIMARY))

S.extend(section("Role Access Matrix"))
Y, N = "Yes", "-"
mat = [["Module", "Student", "Member", "Directorate", "Faculty", "Admin", "Alumni", "Guest"],
       ["Profile", Y, Y, Y, Y, Y, Y, N],
       ["Events (view / register)", Y, Y, Y, Y, Y, Y, "View"],
       ["Tasks / Work Plan", N, Y, Y, N, Y, N, N],
       ["Attendance", "Own", "Own", "Team", "View", "All", N, N],
       ["Certificates", "Own", "Own", "Team", N, "Issue", "Own", N],
       ["Approvals", N, N, "Propose", "Approve", "Final", N, N],
       ["Reports & Analytics", N, "Own", "Directorate", "View", "All", N, N],
       ["Website Content / CMS", N, N, N, N, "Full", N, N]]
cw = W - 3 * cm
S.append(grid(mat, [4.2 * cm] + [(cw - 4.2 * cm) / 7] * 7))

S.append(PageBreak())

# ================= PAGE 3: Frontend =================
S.append(Paragraph("3. Frontend — Website Kaisi Banegi (HTML, CSS, JavaScript)", h1))
S.append(Paragraph("Frontend pure HTML, CSS aur JavaScript mein banega — koi framework nahi. Simple, fast aur kisi bhi hosting par chal sakta hai.", sub))

S.extend(section("3.1 Technology Stack (Frontend)"))
fe = [["Layer", "Technology", "Kyun (Reason)"],
      ["Structure", "HTML5 (semantic tags)", "Har page ka structure: header, nav, sections, forms, tables"],
      ["Styling", "CSS3 (Flexbox, Grid, Variables, Media Queries)", "Professional responsive design bina kisi framework ke"],
      ["Interactivity", "Vanilla JavaScript (ES6+)", "Menus, tabs, modals, form validation, dynamic tables"],
      ["API Calls", "Fetch API (async/await) + JSON", "Backend se data lena/bhejna (login, events, attendance)"],
      ["Auth (client)", "JWT token in localStorage + role check on page load", "Sirf apni role ka portal khule, warna login par redirect"],
      ["Charts", "Chart.js (CDN)", "Admin dashboard analytics, performance graphs"],
      ["Extras", "QR code lib (CDN), jsPDF (certificate download), Font Awesome icons", "Attendance QR, certificates, icons"]]
S.append(grid(fe, [2.8 * cm, 6.2 * cm, cw - 9 * cm]))
S.append(Spacer(1, 8))

S.extend(section("3.2 Design System (Colors & UI)"))
pal = [["Purpose", "Color", "Hex", "Usage"],
       ["Primary", "", "#0B3D5C", "Navbar, headings, sidebar"],
       ["Accent", "", "#1B9AAA", "Buttons, links, active menu"],
       ["Highlight", "", "#E8B04B", "Badges, achievements, CTA"],
       ["Background", "", "#F5F8FA", "Page background, cards"],
       ["Success / Danger", "", "#2E7D6B / #B3282D", "Approved / Rejected, alerts"]]
pt = grid(pal, [3 * cm, 1.6 * cm, 3.6 * cm, cw - 8.2 * cm])
for i, c in enumerate([PRIMARY, ACCENT, GOLD, colors.HexColor("#F5F8FA"), colors.HexColor("#2E7D6B")], start=1):
    pt.setStyle(TableStyle([("BACKGROUND", (1, i), (1, i), c)]))
S.append(pt)
S.append(Spacer(1, 4))
S.append(Paragraph("Typography: Poppins / Inter (Google Fonts). Layout: Public website = top navbar + footer; "
                   "Portals = left sidebar + top bar + content cards. Ek common <b>style.css</b> (CSS variables se colors) "
                   "sab pages par use hogi. Fully responsive (mobile, tablet, desktop).", body))
S.append(Spacer(1, 8))

S.extend(section("3.3 Page / Screen Structure"))
pages = [["Area", "Main Screens"],
         ["Public Website", "Home, About, Vision & Mission, Leadership, Directorates, Projects, Events, News, Achievements, Gallery, Publications, Membership Form, Volunteer Registration, Contact, FAQs"],
         ["Auth", "Login, Register (Student / Member / Alumni), Forgot Password, Email Verification"],
         ["Portal Layout", "Dashboard (cards + quick stats), Sidebar menu (role-wise features), Profile, Notifications bell, Settings"],
         ["Reusable JS Modules", "table.js (search/filter/export), modal.js, form-validate.js, api.js (fetch wrapper), auth.js (token + role guard), notify.js (toasts)"]]
S.append(grid(pages, [3.2 * cm, cw - 3.2 * cm]))
S.append(Spacer(1, 8))

S.extend(section("3.4 Frontend Folder Structure"))
fs = ("frontend/\n"
      "  index.html, about.html, events.html, gallery.html, contact.html, faqs.html ...  -> public pages\n"
      "  login.html, register.html\n"
      "  student/    -> dashboard.html, events.html, attendance.html, certificates.html ...\n"
      "  member/  directorate/  faculty/  admin/  alumni/   -> har portal ke apne HTML pages\n"
      "  css/        -> style.css (global + variables), portal.css, responsive.css\n"
      "  js/         -> api.js, auth.js, main.js, table.js, modal.js, charts.js, portal-specific scripts\n"
      "  assets/     -> images, logo, icons, fonts")
S.append(Paragraph(fs.replace("\n", "<br/>").replace("  ", "&nbsp;&nbsp;"),
                   ParagraphStyle("code", parent=small, fontName="Courier", backColor=LIGHT, borderPadding=6, leading=11)))

S.append(PageBreak())

# ================= PAGE 4: Backend =================
S.append(Paragraph("4. Backend — Server & Database Kaisa Hoga", h1))
S.append(Paragraph("Backend data store karta hai, login/roles handle karta hai aur frontend ko REST APIs deta hai.", sub))

S.extend(section("4.1 Technology Stack (Backend)"))
be = [["Layer", "Technology", "Kyun (Reason)"],
      ["Runtime / Framework", "Node.js + Express.js (ya NestJS)", "JavaScript full-stack, fast APIs, bari community"],
      ["Database", "PostgreSQL (Prisma ORM)", "Relational data: users, roles, events, attendance — sab linked"],
      ["Authentication", "JWT (access + refresh token), bcrypt", "Secure login, role-based access (RBAC)"],
      ["File Storage", "Cloudinary / AWS S3", "Gallery images, documents, certificates"],
      ["Email / Notifications", "Nodemailer (SMTP) + in-app notifications table", "Approvals, event reminders, certificate issued"],
      ["Certificates", "PDFKit / Puppeteer + unique verification ID", "Auto-generate certificate PDF with QR verify link"],
      ["Security & Docs", "Zod/Joi, Helmet, CORS, Rate limiting, Swagger", "Safe APIs + API documentation"]]
S.append(grid(be, [3.2 * cm, 6 * cm, cw - 9.2 * cm]))
S.append(Spacer(1, 8))

S.extend(section("4.2 Database — Main Tables"))
db = [["Table", "Key Fields", "Related To"],
      ["users", "id, name, email, password_hash, role, status", "roles, profiles"],
      ["roles / permissions", "role_name, permission_key", "users (RBAC)"],
      ["students / members / alumni / faculty", "profile info, member_id, department, designation, skills", "users, directorates"],
      ["directorates", "name, director_id, asst_director_id, objectives, work_plan", "members, tasks, events"],
      ["tasks", "title, assigned_to, directorate_id, deadline, status, performance_score", "members, directorates"],
      ["events", "title, type, date, venue, directorate_id, status (proposed/approved)", "registrations, attendance"],
      ["event_registrations / volunteers", "event_id, user_id, role (participant/volunteer), status", "events, users"],
      ["attendance", "event_id / meeting_id, user_id, marked_by, method (QR/manual), time", "events, users"],
      ["certificates", "user_id, event_id, certificate_no, pdf_url, issued_at", "users, events"],
      ["achievements / reports / documents / notifications / feedback", "title, description, file_url, owner_id / message, read_at / rating, status", "users, directorates"],
      ["cms_content", "page_key (about, vision, news, gallery, faq...), content, media", "Public website"]]
S.append(grid(db, [4.6 * cm, 8.4 * cm, cw - 13 * cm]))
S.append(Spacer(1, 8))

S.extend(section("4.3 Main API Endpoints (REST)"))
api = [["Module", "Endpoints (examples)"],
       ["Auth", "POST /api/auth/register · POST /api/auth/login · POST /api/auth/refresh · GET /api/auth/me"],
       ["Users & Roles", "GET/PUT /api/users/:id · GET /api/admin/users · PUT /api/admin/roles/:id/permissions"],
       ["Directorates", "GET /api/directorates · POST /api/directorates · GET /api/directorates/:id/members · /objectives · /work-plan"],
       ["Events", "GET /api/events · POST /api/events/proposals · PUT /api/events/:id/approve · POST /api/events/:id/register"],
       ["Attendance", "POST /api/attendance/mark · GET /api/attendance/event/:id · GET /api/attendance/user/:id"],
       ["Certificates", "POST /api/certificates/issue · GET /api/certificates/my · GET /api/verify/:certificate_no"],
       ["Tasks & Reports", "POST /api/tasks · PUT /api/tasks/:id/status · GET /api/reports/dashboard · GET /api/reports/export?type=pdf"],
       ["CMS & Public", "GET /api/public/news · GET /api/public/gallery · POST /api/public/contact · POST /api/public/volunteer"]]
S.append(grid(api, [3 * cm, cw - 3 * cm]))


S.append(PageBreak())

# ================= PAGE 5: Architecture, Workflow, Plan =================
S.append(Paragraph("5. System Architecture, Workflow & Development Plan", h1))
S.append(Spacer(1, 4))

S.extend(section("5.1 Architecture (How it Works)"))
arch = [[Paragraph("<b>USER (Browser / Mobile)</b><br/>Student · Member · Faculty · Admin · Alumni · Guest", center),
         Paragraph("&#8594;", center),
         Paragraph("<b>FRONTEND</b><br/>HTML + CSS + JavaScript<br/>(Netlify / cPanel hosting)", center),
         Paragraph("&#8594;", center),
         Paragraph("<b>BACKEND API</b><br/>Node.js + Express<br/>JWT · RBAC · Services", center),
         Paragraph("&#8594;", center),
         Paragraph("<b>DATABASE & STORAGE</b><br/>PostgreSQL · Cloud Storage<br/>Email Service", center)]]
at = Table(arch, colWidths=[4.3 * cm, 0.8 * cm, 3.6 * cm, 0.8 * cm, 3.9 * cm, 0.8 * cm, cw - 14.2 * cm])
at.setStyle(TableStyle([
    ("BOX", (0, 0), (0, 0), 1, ACCENT), ("BOX", (2, 0), (2, 0), 1, ACCENT),
    ("BOX", (4, 0), (4, 0), 1, PRIMARY), ("BOX", (6, 0), (6, 0), 1, GOLD),
    ("BACKGROUND", (0, 0), (0, 0), LIGHT), ("BACKGROUND", (2, 0), (2, 0), LIGHT),
    ("BACKGROUND", (4, 0), (4, 0), colors.HexColor("#E3EEF4")), ("BACKGROUND", (6, 0), (6, 0), colors.HexColor("#FBF3E0")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
S.append(at)
S.append(Spacer(1, 4))
S.append(Paragraph("Hosting: Frontend -> Netlify / cPanel (static files); Backend -> Railway / Render / VPS (Docker); Database -> Supabase / Neon PostgreSQL; "
                   "Files -> Cloudinary. HTTPS, daily DB backup aur environment variables (.env) se secrets manage honge.", body))
S.append(Spacer(1, 8))

S.extend(section("5.2 Key Workflows"))
wf = [["Workflow", "Steps"],
      ["Membership Application", "Guest form submit -> Admin review -> Approve -> User account + Member ID create -> Email + Member Portal access"],
      ["Event Lifecycle", "Directorate proposes event -> Faculty approval -> Admin final approval -> Published on website -> Students register -> Attendance (QR) -> Certificates auto-issued -> Activity report"],
      ["Task Management", "Director assigns task -> Member updates status -> Director reviews -> Performance score -> Reflect in Member Performance & Directorate Report"],
      ["Certificate Verification", "Certificate PDF with unique number + QR -> anyone scans -> /verify/:no -> authenticity confirmed"],
      ["Notifications", "System events (approval, task, event reminder) -> in-app notification + email"]]
S.append(grid(wf, [3.6 * cm, cw - 3.6 * cm]))
S.append(Spacer(1, 8))

S.extend(section("5.3 Development Phases & Timeline"))
ph = [["Phase", "Work", "Duration"],
      ["Phase 1", "Requirements finalize, UI/UX design (Figma), database design", "2 weeks"],
      ["Phase 2", "Public website (HTML/CSS/JS) + Auth (login/register) + Admin Portal core (users, roles, CMS)", "3 weeks"],
      ["Phase 3", "Student, Member & Directorate Portals (events, tasks, attendance, certificates)", "4 weeks"],
      ["Phase 4", "Faculty & Alumni Portals, reports & analytics, notifications", "3 weeks"],
      ["Phase 5", "Testing, security review, deployment, training & documentation", "2 weeks"],
      ["Total", "", "~14 weeks"]]
pt2 = grid(ph, [2.4 * cm, cw - 5.4 * cm, 3 * cm])
pt2.setStyle(TableStyle([("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FBF3E0")),
                         ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold")]))
S.append(pt2)
S.append(Spacer(1, 8))

S.extend(section("5.4 Security & Quality Checklist"))
sec = [["Area", "Measures"],
       ["Security", "Password hashing (bcrypt), JWT expiry + refresh, role-based permissions, input validation, HTTPS, rate limiting, audit logs"],
       ["Performance", "API pagination, image optimization, minified CSS/JS, browser caching, CDN libraries"],
       ["Quality", "Responsive testing, API tests (Jest), Swagger docs, Git version control, staging + production environments"]]
S.append(grid(sec, [3 * cm, cw - 3 * cm]))
S.append(Spacer(1, 10))
S.append(Paragraph("<b>Conclusion:</b> Ye system YPDC ke tamam stakeholders — students, members, directorates, faculty, admin aur alumni — "
                   "ko ek platform par lata hai. HTML/CSS/JavaScript frontend, Node.js backend aur PostgreSQL database ke sath ye scalable, secure "
                   "aur asaan-maintain website banegi.", body))

doc.build(S)
print("done")
