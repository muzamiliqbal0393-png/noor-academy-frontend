#!/usr/bin/env python3
"""YPDC Integrated Portal System — Professional Report PDF Generator.
Uses fpdf2 + DejaVu fonts. Output: YPDC-Portal-System-Report.pdf
"""
from fpdf import FPDF, FontFace

# ---------------------------------------------------------------- palette
PRIMARY      = (11, 61, 46)     # deep green
PRIMARY_MID  = (14, 122, 92)
GOLD         = (201, 162, 39)
GOLD_DARK    = (150, 118, 22)
INK          = (20, 32, 27)
MUTED        = (91, 107, 100)
LINE         = (214, 226, 220)
LIGHT_BG     = (242, 247, 244)
WHITE        = (255, 255, 255)
DARK_BAR     = (8, 45, 34)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

HEAD_STYLE = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=PRIMARY)


def render_toc(pdf, outline):
    """Rendered automatically by insert_toc_placeholder with real page numbers."""
    pdf.set_y(28)
    pdf.set_font("DejaVu", "B", 17)
    pdf.set_text_color(*PRIMARY)
    pdf.cell(text="Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*GOLD)
    pdf.set_line_width(0.9)
    pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
    pdf.ln(8)
    for s in outline:
        level = s.level
        indent = "      " * level
        title = f"{indent}{s.name}"
        pg = str(s.page_number)
        if level == 0:
            pdf.set_font("DejaVu", "B", 10.5)
            pdf.set_text_color(*PRIMARY)
            pdf.ln(1.5) if outline.index(s) else None
        else:
            pdf.set_font("DejaVu", "", 9.5)
            pdf.set_text_color(*INK)
        # title left, page number right with dot leader
        x0 = pdf.l_margin + (8 if level else 0)
        pdf.set_x(x0)
        max_w = pdf.epw - (8 if level else 0) - 12
        # trim title to fit one line
        while pdf.get_string_width(title) > max_w and len(title) > 10:
            title = title[:-2]
        dots_w = max_w - pdf.get_string_width(title)
        n_dots = max(2, int(dots_w / pdf.get_string_width(".")))
        line = f"{title} {'.' * n_dots} {pg}"
        pdf.cell(text=line, new_x="LMARGIN", new_y="NEXT", h=6.4)
    pdf.set_text_color(*INK)


class Report(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(18, 18, 18)
        self.set_auto_page_break(True, margin=25)
        self.cover_pages = 1  # only the cover skips header/footer (absolute page numbering)
        self.sec_no = 0

    # ------------------------------------------------- header / footer
    def header(self):
        if self.page_no() <= self.cover_pages:
            return
        self.set_y(10.5)
        self.set_font("DejaVu", "B", 7.5)
        self.set_text_color(*MUTED)
        self.cell(w=self.epw - 28, h=4, text="YPDC  •  INTEGRATED PORTAL SYSTEM  •  SYSTEM REPORT  v1.0",
                  new_x="RIGHT", new_y="TOP", align="L")
        self.set_font("DejaVu", "", 7.5)
        self.cell(w=28, h=4, text="Confidential", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.line(self.l_margin, 15.5, self.w - self.r_margin, 15.5)
        self.set_y(19)

    def footer(self):
        if self.page_no() <= self.cover_pages:
            return
        self.set_y(-12)
        self.set_draw_color(*LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(w=self.epw - 32, text="YPDC Integrated Portal System — Official Report",
                  new_x="RIGHT", new_y="TOP", align="L")
        self.cell(w=32, text=f"Page {self.page_no()} / {{nb}}",
                  align="R", new_x="LMARGIN", new_y="NEXT")

    # ------------------------------------------------- building blocks
    def need(self, h=40):
        if self.get_y() + h > self.h - 22:
            self.add_page()

    def section(self, title):
        self.sec_no += 1
        full = f"{self.sec_no}.  {title}"
        self.need(30)
        self.start_section(full, level=0)
        y = self.get_y()
        self.set_fill_color(*PRIMARY)
        self.rect(self.l_margin, y, self.epw, 10.5, style="F")
        self.set_fill_color(*GOLD)
        self.rect(self.l_margin, y, 3.2, 10.5, style="F")
        self.set_xy(self.l_margin + 6, y + 1.6)
        self.set_font("DejaVu", "B", 12.5)
        self.set_text_color(255, 255, 255)
        self.cell(w=self.epw - 12, text=full, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*INK)
        self.set_y(y + 13.5)

    def sub(self, title, numbered=True):
        self.need(24)
        self.start_section(title, level=1)
        self.set_font("DejaVu", "B", 11)
        self.set_text_color(*PRIMARY)
        self.set_fill_color(*LIGHT_BG)
        self.cell(w=self.epw, text=f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT", h=7.5)
        self.set_text_color(*INK)
        self.ln(2)

    def sub2(self, title):
        self.need(18)
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(*PRIMARY_MID)
        self.cell(text=title, new_x="LMARGIN", new_y="NEXT", h=6)
        self.set_text_color(*INK)
        self.ln(1)

    def body(self, text, size=9.8, align="J", gap=2.5, bold=False):
        self.set_font("DejaVu", "B" if bold else "", size)
        self.set_text_color(*INK)
        self.multi_cell(w=0, text=text, align=align, markdown=True,
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(gap)

    def bullets(self, items, size=9.8, gap=1.2):
        self.set_font("DejaVu", "", size)
        self.set_text_color(*INK)
        for it in items:
            x = self.l_margin
            self.set_x(x)
            self.set_font("DejaVu", "B", size)
            self.set_text_color(*GOLD_DARK)
            self.write(5.2, "▸  ")
            self.set_font("DejaVu", "", size)
            self.set_text_color(*INK)
            self.multi_cell(w=self.epw - 7, text=it, markdown=True,
                            new_x="LMARGIN", new_y="NEXT")
            self.ln(gap)
        self.ln(1)

    def steps(self, items, size=9.8):
        self.set_text_color(*INK)
        for i, it in enumerate(items, 1):
            self.set_font("DejaVu", "B", size)
            self.set_text_color(*PRIMARY)
            self.write(5.2, f"{i}. ")
            self.set_font("DejaVu", "", size)
            self.set_text_color(*INK)
            self.multi_cell(w=self.epw - 8, text=it, markdown=True,
                            new_x="LMARGIN", new_y="NEXT")
            self.ln(1.2)
        self.ln(1)

    def info_box(self, title, text, size=9.5):
        self.need(28)
        y0 = self.get_y()
        self.set_font("DejaVu", "", size)
        # measure
        h_txt = 8 + 6
        self.set_fill_color(*LIGHT_BG)
        # draw after measuring via dry run is complex; use fixed approach:
        x, w = self.l_margin, self.epw
        self.set_xy(x + 8, y0 + 3)
        self.set_font("DejaVu", "B", size)
        self.set_text_color(*PRIMARY)
        self.multi_cell(w=w - 16, text=title, new_x="LMARGIN", new_y="NEXT")
        self.set_x(x + 8)
        self.set_font("DejaVu", "", size)
        self.set_text_color(*INK)
        self.multi_cell(w=w - 16, text=text, markdown=True,
                        new_x="LMARGIN", new_y="NEXT")
        y1 = self.get_y() + 3
        # background behind (draw first next time? draw now under by redrawing page region is hard)
        # Instead: draw frame around
        self.set_draw_color(*GOLD)
        self.set_line_width(0.6)
        self.rect(x, y0, w, y1 - y0, style="D")
        self.set_fill_color(*GOLD)
        self.rect(x, y0, 2.6, y1 - y0, style="F")
        self.set_y(y1 + 3)

    def mtable(self, headers, rows, widths=None, size=8.8, lh=5.4, align="LEFT"):
        """Styled table: dark-green header, grid, repeat headings."""
        if widths is None:
            n = len(headers)
            widths = [self.epw / n] * n
        total = sum(widths)
        widths = [w / total * self.epw for w in widths]
        align_map = {"LEFT": "LEFT", "CENTER": "CENTER", "RIGHT": "RIGHT"}
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*LINE)
        self.set_text_color(*INK)
        with self.table(col_widths=tuple(widths),
                        first_row_as_headings=True,
                        headings_style=HEAD_STYLE,
                        text_align="LEFT",
                        line_height=lh,
                        width=self.epw,
                        align=align_map.get(align, "LEFT")) as t:
            r = t.row()
            for h in headers:
                r.cell(h)
            self.set_font("DejaVu", "", size)
            for row in rows:
                rr = t.row()
                for c in row:
                    rr.cell(str(c))
        self.set_font("DejaVu", "", 9.8)
        self.ln(3)

    def kpi_strip(self, cards):
        """cards: list of (value, label). Draws 4 mini boxes in a row."""
        self.need(26)
        n = len(cards)
        gap = 3
        bw = (self.epw - gap * (n - 1)) / n
        y = self.get_y()
        x = self.l_margin
        for val, lab in cards:
            self.set_fill_color(*PRIMARY)
            self.rect(x, y, bw, 19, style="F")
            self.set_fill_color(*GOLD)
            self.rect(x, y, bw, 2.2, style="F")
            self.set_xy(x, y + 3.4)
            self.set_font("DejaVu", "B", 14)
            self.set_text_color(255, 255, 255)
            self.cell(w=bw, text=val, align="C", new_x="LEFT", new_y="NEXT")
            self.set_x(x)
            self.set_font("DejaVu", "", 7.5)
            self.set_text_color(235, 240, 237)
            self.cell(w=bw, text=lab, align="C", new_x="LMARGIN", new_y="NEXT")
            x += bw + gap
        self.set_y(y + 22)
        self.set_text_color(*INK)

    # ------------------------------------------------- cover
    def cover(self):
        self.add_page()
        # top gold bar
        self.set_fill_color(*GOLD)
        self.rect(0, 0, 210, 10, style="F")
        self.set_fill_color(*PRIMARY)
        self.rect(0, 10, 210, 3, style="F")
        self.ln(14)
        # badge
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(*GOLD_DARK)
        self.cell(w=self.epw, text="YOUTH  •  PEACE  •  DEVELOPMENT  •  COMMUNITY", align="C",
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        # emblem (badge with text inside the circle)
        cx = 105
        y0 = self.get_y()
        self.set_fill_color(*PRIMARY)
        self.set_draw_color(*GOLD)
        self.set_line_width(1.2)
        self.ellipse(cx - 17, y0, 34, 34, style="DF")
        self.set_xy(cx - 17, y0 + 7.5)
        self.set_font("DejaVu", "B", 15)
        self.set_text_color(255, 255, 255)
        self.cell(w=34, text="YPDC", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(cx - 17, y0 + 17.5)
        self.set_font("DejaVu", "", 6.5)
        self.set_text_color(255, 243, 205)
        self.cell(w=34, text="FOR YOUTH", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(cx - 17, y0 + 22)
        self.cell(w=34, text="EMPOWERMENT", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_y(y0 + 38)
        # title
        self.set_font("DejaVu", "B", 26)
        self.set_text_color(*PRIMARY)
        self.cell(w=self.epw, text="YPDC", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DejaVu", "B", 15)
        self.cell(w=self.epw, text="Integrated Portal System", align="C",
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        # gold rule
        self.set_draw_color(*GOLD)
        self.set_line_width(1)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(5)
        self.set_font("DejaVu", "", 11.5)
        self.set_text_color(*INK)
        self.cell(w=self.epw, text="Complete System Requirements, Functional Design", align="C",
                  new_x="LMARGIN", new_y="NEXT")
        self.cell(w=self.epw, text="& Implementation Report", align="C",
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        # portal band
        yb = self.get_y()
        self.set_fill_color(*LIGHT_BG)
        self.rect(self.l_margin, yb, self.epw, 9, style="F")
        self.set_fill_color(*GOLD)
        self.rect(self.l_margin, yb, self.epw, 1, style="F")
        self.set_xy(self.l_margin, yb + 2.4)
        self.set_font("DejaVu", "B", 7.5)
        self.set_text_color(*PRIMARY)
        self.cell(w=self.epw, text="STUDENT  \u2022  MEMBER  \u2022  DIRECTORATE  \u2022  FACULTY  \u2022  ADMIN  \u2022  ALUMNI  \u2022  PUBLIC",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_y(yb + 12)
        self.kpi_strip([("7", "PORTALS"), ("81", "MODULES"),
                        ("6", "USER ROLES"), ("v1.0", "VERSION")])
        self.ln(1)
        # meta table
        self.set_font("DejaVu", "", 9.5)
        meta = [
            ("Document Title", "YPDC Integrated Portal System — System Report"),
            ("Version", "1.0  •  Initial Release"),
            ("Date", "10 September 2026"),
            ("Classification", "Official — For YPDC Leadership & Development Team"),
            ("Coverage", "Student • Member • Directorate • Faculty • Admin • Alumni • Public"),
            ("Status", "Approved for Planning & Development"),
        ]
        row_h = 6.5
        yc = self.get_y()
        card_h = len(meta) * row_h + 6
        self.set_fill_color(*LIGHT_BG)
        self.rect(self.l_margin, yc, self.epw, card_h, style="F")
        self.set_draw_color(*LINE)
        self.set_line_width(0.4)
        self.rect(self.l_margin, yc, self.epw, card_h, style="D")
        self.set_fill_color(*GOLD)
        self.rect(self.l_margin, yc, 2.6, card_h, style="F")
        self.set_y(yc + 3)
        col1 = 50
        for k, v in meta:
            self.set_x(self.l_margin + 7)
            self.set_font("DejaVu", "B", 9)
            self.set_text_color(*PRIMARY)
            self.cell(w=col1, text=k, h=row_h, new_x="RIGHT", new_y="TOP")
            self.set_font("DejaVu", "", 8.6)
            self.set_text_color(*INK)
            self.cell(w=self.epw - col1 - 12, text=v, h=row_h, new_x="LMARGIN", new_y="NEXT")
        self.set_y(yc + card_h + 5)
        self.set_font("DejaVu", "", 8.5)
        self.set_text_color(*MUTED)
        self.multi_cell(w=0, align="C",
                        text=("This report defines the complete functional scope, module specifications, "
                              "roles & permissions, workflows, reporting framework and implementation "
                              "roadmap for the YPDC digital platform."))
        self.ln(3)
        self.set_font("DejaVu", "B", 8)
        self.set_text_color(*PRIMARY)
        self.multi_cell(w=0, align="C",
                        text=("Inside: Executive Summary  \u2022  7 Portal Specifications (81 modules)  \u2022  Roles & Workflows"
                              "  \u2022  Data Model  \u2022  Analytics  \u2022  Roadmap  \u2022  Checklists & Glossary"))
        self.ln(2)
        self.set_font("DejaVu", "B", 8)
        self.set_text_color(*GOLD_DARK)
        self.cell(w=self.epw, text="PREPARED FOR YPDC LEADERSHIP  \u2022  SEPTEMBER 2026", align="C",
                  new_x="LMARGIN", new_y="NEXT")
        # bottom bar (absolute-positioned art: suspend auto page-break)
        self.set_auto_page_break(False)
        self.set_fill_color(*PRIMARY)
        self.rect(0, 282, 210, 15, style="F")
        self.set_fill_color(*GOLD)
        self.rect(0, 282, 210, 2, style="F")
        self.set_xy(0, 286)
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(255, 255, 255)
        self.cell(w=210, text="YPDC  •  Empowering Youth  •  Building Peace  •  Driving Development",
                  align="C")
        self.set_auto_page_break(True, margin=25)


# ===================================================================== data
PORTALS = [
    {
        "n": "1", "name": "Student Portal",
        "tag": "For enrolled students — participation, learning & recognition",
        "objective": ("The Student Portal is the primary gateway for enrolled students to engage with YPDC. "
                      "It covers profile management, membership application, event discovery and registration, "
                      "volunteering, attendance tracking, certificates, achievements, notifications and feedback — "
                      "giving every student a single, transparent record of their YPDC journey."),
        "modules": [
            ("Profile", "Maintain personal, academic & contact information with photo and guardian details.",
             "Editable profile • Photo upload • Academic info • Verification status"),
            ("Membership", "Apply for YPDC membership and track the application lifecycle.",
             "Online application • Status tracking • Membership ID & card • Renewal history"),
            ("Events", "Discover all published events with schedules, venues and eligibility.",
             "Event catalogue • Search & filters • Event details • Calendar view"),
            ("Event Registration", "Register for events, receive e-tickets and manage bookings.",
             "One-click registration • QR e-ticket • Waitlist • Cancellation & history"),
            ("Volunteer Opportunities", "Browse and apply for volunteer roles linked to events & projects.",
             "Opportunity board • Applications • Hour logging • Supervisor confirmation"),
            ("Attendance", "View verified attendance across events and volunteer activities.",
             "Event-wise log • QR/biometric/manual marking • Attendance % • Download record"),
            ("Certificates", "Access and download verifiable e-certificates for participation & volunteering.",
             "Certificate wallet • QR verification code • PDF download • Share link"),
            ("Achievements", "Showcase badges, awards and leaderboard points earned through activities.",
             "Badges & trophies • Points system • Leaderboard • Public achievement wall (opt-in)"),
            ("Notifications", "Receive timely alerts for events, approvals, certificates and announcements.",
             "In-app + email/SMS • Preferences • Read/unread centre • Reminders"),
            ("Feedback", "Submit event feedback, ratings and suggestions to improve quality.",
             "Post-event forms • Star ratings • Suggestions box • Response visibility"),
        ],
        "workflows": [
            "**Membership journey:** Student applies → Admin verifies → ID issued → renewals tracked.",
            "**Event journey:** Browse → register → QR ticket → attend (QR scan) → feedback → certificate auto-issued.",
            "**Volunteer journey:** Apply → shortlisted → hours logged → supervisor approves → certificate + points.",
        ],
        "kpis": ["Active students", "Event registrations", "Volunteer hours", "Avg. feedback score"],
    },
    {
        "n": "2", "name": "Member Portal",
        "tag": "For registered YPDC members — duties, tasks & performance",
        "objective": ("The Member Portal serves officially inducted YPDC members working under directorates. "
                      "Beyond student features, it adds a digital Member ID, directorate affiliation, defined "
                      "responsibilities, task management, duty rosters, performance scoring and activity reporting — "
                      "making every member accountable, guided and recognised."),
        "modules": [
            ("Profile & Member ID", "Official member profile with a scannable digital ID card.",
             "Digital ID card with QR • Tenure & status • Renewal alerts • ID reprint request"),
            ("Directorate", "Shows the member's assigned directorate, hierarchy and teammates.",
             "Directorate info • Reporting line • Team directory • Transfer requests"),
            ("Responsibilities", "Clearly assigned role description, job duties and tenure goals.",
             "Role card & JD • Tenure objectives • Acknowledgement sign-off"),
            ("Tasks", "Personal to-do list with deadlines, priorities and submissions.",
             "Task inbox • Deadline reminders • File attachments • Status updates"),
            ("Events / Duties", "Event assignments and duty roster with check-in records.",
             "Duty calendar • Role in event • Check-in/out • Duty completion log"),
            ("Attendance", "Meeting and event attendance register with defaulter alerts.",
             "Attendance % • Meeting log • Leave requests • Warning flags"),
            ("Certificates", "Service, appreciation and training certificates issued to the member.",
             "Certificate wallet • Verification QR • Nomination-based awards"),
            ("Performance", "Monthly/quarterly performance score with lead ratings and self-review.",
             "Score dashboard • Lead ratings • Self-assessment • Improvement notes"),
            ("Reports", "Submit periodic activity reports and view submission history.",
             "Report templates • Draft/submit • Review comments • Archive"),
            ("Notifications", "Task, duty, meeting and performance alerts in one centre.",
             "Push/email/SMS • Priority flags • Action links (approve/submit)"),
        ],
        "workflows": [
            "**Task lifecycle:** Lead assigns → member accepts → submits evidence → lead reviews → scored.",
            "**Duty lifecycle:** Roster published → member checks in (QR) → duty logged → hours counted.",
            "**Performance cycle:** Monthly auto-score (tasks + attendance + duties) → lead review → published.",
        ],
        "kpis": ["Active members", "Task completion %", "Duty fulfilment %", "Avg. performance score"],
    },
    {
        "n": "3", "name": "Directorate Portal",
        "tag": "For directorate leadership & teams — planning, execution & accountability",
        "objective": ("Each YPDC directorate (e.g. Events, Media, Volunteer Management) operates as a semi-autonomous "
                      "unit. The Directorate Portal gives directors, assistant directors and team members shared tools "
                      "for identity, objectives, work planning, tasking, events, proposals, attendance, reporting, "
                      "documents and performance — so leadership always knows what is planned, what is done, and by whom."),
        "modules": [
            ("Directorate Profile", "Public-facing identity: mandate, scope, contact and branding.",
             "About & mandate • Logo/banner • Contact • Public page link"),
            ("Director / Assistant Director", "Leadership profiles, tenure, authority and contact.",
             "Leadership cards • Tenure dates • Delegation of authority"),
            ("Team Members", "Complete roster with roles, status and joining dates.",
             "Member directory • Role assignment • Active/inactive status"),
            ("Objectives", "Quarterly and annual objectives in OKR style with progress tracking.",
             "Objective setting • Key results • Progress % • Review cycle"),
            ("Work Plan", "Time-bound activity calendar with milestones and owners.",
             "Monthly/quarterly planner • Milestones • Owner mapping • Gantt-style view"),
            ("Tasks", "Create, assign and track tasks across the whole directorate team.",
             "Kanban board • Priorities & deadlines • Comments • Overdue escalation"),
            ("Events & Activities", "Directorate-owned events calendar with ownership and outcomes.",
             "Event pipeline • Ownership • Post-event summary • Media links"),
            ("Event Proposals", "Structured proposal submission routed to Admin for approval.",
             "Proposal form (budget, venue, plan) • Approval workflow • Revision requests"),
            ("Attendance", "Meeting and internal-activity attendance register.",
             "Meeting register • QR/manual marking • Absence reports"),
            ("Activity Reports", "Periodic (weekly/monthly) reports compiled and archived.",
             "Templates • Auto-aggregation of tasks/events • PDF export • Archive"),
            ("Achievements", "Directorate-level awards, milestones and success stories.",
             "Achievement log • Evidence attachments • Public showcase"),
            ("Documents", "Central repository: minutes, letters, plans, policies and MOUs.",
             "Folders & versioning • Access control • Search • Download log"),
            ("Performance", "Directorate scoreboard combining tasks, events, attendance and reports.",
             "Composite score • Trend charts • Inter-directorate ranking • Review notes"),
        ],
        "workflows": [
            "**Proposal flow:** Directorate drafts → Admin reviews → approved/revision → event published → executed → report filed.",
            "**Planning flow:** Objectives set → work plan derived → tasks assigned → weekly review → monthly report.",
            "**Governance flow:** Meetings logged → minutes uploaded → action items become tasks → tracked to closure.",
        ],
        "kpis": ["Objectives achieved %", "Events delivered", "Proposal approval rate", "Directorate score"],
    },
    {
        "n": "4", "name": "Faculty Portal",
        "tag": "For faculty mentors & advisors — guidance, supervision & approvals",
        "objective": ("Faculty members act as mentors, advisors, judges and approvers. The Faculty Portal recognises "
                      "their academic identity while defining their YPDC role, connecting them to events and student "
                      "activities, and routing approval requests (proposals, leaves, certificates) to them with full "
                      "context — respecting their time while keeping governance strong."),
        "modules": [
            ("Faculty Profile", "Academic and professional profile with photo and credentials.",
             "Qualifications • Experience • Expertise tags • Contact & availability"),
            ("Department / Designation", "Official department, designation and campus affiliation.",
             "Department linkage • Designation history • Campus/branch"),
            ("YPDC Role", "Defined YPDC responsibility: mentor, advisor, judge, patron or coordinator.",
             "Role assignment letter • Scope & tenure • Linked directorate(s)"),
            ("Events", "Invitations for guest sessions, judging panels, trainings and keynote slots.",
             "Invitations inbox • Accept/decline • Session materials • Honorarium record"),
            ("Student / Member Activities", "Supervision log for mentored students, members and projects.",
             "Mentee list • Mentoring sessions log • Project supervision • Remarks"),
            ("Approvals", "One-click approval queue with documents and history.",
             "Pending queue • Approve/return with remarks • E-signature • Audit trail"),
            ("Reports", "Submit mentor reports and view supervised-activity summaries.",
             "Mentor report forms • Supervision summary • Export PDF"),
            ("Feedback", "Give structured feedback on events, members and programs.",
             "Evaluation forms • Ratings • Confidential remarks channel"),
            ("Notifications", "Invitations, approval requests, reminders and announcements.",
             "Priority inbox • Calendar sync • Digest emails"),
        ],
        "workflows": [
            "**Approval flow:** Request raised → routed to mapped faculty → approve/return with remarks → audit logged.",
            "**Mentoring flow:** Mentees assigned → sessions logged → term report submitted → recognised.",
            "**Event flow:** Invitation → acceptance → materials shared → session delivered → feedback captured.",
        ],
        "kpis": ["Sessions delivered", "Approvals turnaround", "Mentees guided", "Mentor rating"],
    },
    {
        "n": "5", "name": "Admin Portal",
        "tag": "For system administrators — control tower of the entire platform",
        "objective": ("The Admin Portal is the command centre. It provides a real-time dashboard, complete user/member/"
                      "directorate/faculty management, event governance, a unified approvals inbox, attendance and "
                      "certificate control, analytics, notifications, website content, documents, complaints handling and "
                      "granular roles & permissions — everything needed to run YPDC digitally, transparently and at scale."),
        "modules": [
            ("Dashboard", "Real-time command view: counts, trends, pending items and alerts.",
             "KPI cards • Charts • Pending-approval widget • Quick actions • Activity feed"),
            ("User Management", "Master control of all accounts across every portal and role.",
             "Create/deactivate • Role assignment • Bulk import • Login & audit logs"),
            ("Member Management", "Full member lifecycle: application to induction, transfer, exit and renewal.",
             "Application queue • ID issuance • Transfers • Renewals • Exit & rejoin"),
            ("Directorate Management", "Create and govern directorates, leadership and structures.",
             "Create/merge units • Assign directors • Org chart • Performance comparison"),
            ("Faculty Management", "Onboard faculty, map YPDC roles and track engagement.",
             "Onboarding • Role mapping • Invitations • Engagement history"),
            ("Events Management", "Govern the full event lifecycle from proposal to certificate.",
             "Approve proposals • Publish/unpublish • Registrations • Attendance • Close-out"),
            ("Applications & Approvals", "Single unified queue for every request type in the system.",
             "Membership • Proposals • Leaves • Certificates • Custom forms • SLA tracking"),
            ("Attendance", "Organisation-wide attendance registers, policies and defaulter lists.",
             "Registers • QR/manual/biometric config • Policies • Defaulter reports"),
            ("Certificates", "Design templates, bulk-issue and verify all certificates.",
             "Template designer • Bulk issue • QR verification portal • Revocation"),
            ("Reports & Analytics", "Pre-built and custom reports with exports and scheduled digests.",
             "100+ KPIs • Custom builder • PDF/Excel export • Scheduled emails • Charts"),
            ("Notifications", "Broadcast and targeted multi-channel communication engine.",
             "Templates • Segments • Push/email/SMS • Delivery reports • Announcements"),
            ("Website Content", "Manage all public-portal content without developer help (CMS).",
             "Pages • News • Gallery • Publications • Banners • Menus • SEO fields"),
            ("Documents", "Central, access-controlled document library for the organisation.",
             "Folders • Versioning • Access rights • Retention • Audit of downloads"),
            ("Feedback / Complaints", "Grievance redressal with ticketing, SLA and escalation.",
             "Ticket queue • Categories • SLA timers • Escalation • Resolution & rating"),
            ("Roles & Permissions", "Granular, least-privilege access control for every module & action.",
             "Role builder • 200+ permissions • Delegation • Temporary access • Audit"),
        ],
        "workflows": [
            "**Approval triage:** All requests land in one queue → auto-routed by type → SLA-monitored → decided → notified.",
            "**Event governance:** Proposal → budget/venue check → approve → publish → monitor live → close with report & certificates.",
            "**Grievance flow:** Complaint ticketed → acknowledged in 24h → assigned → resolved → complainant rates resolution.",
        ],
        "kpis": ["Pending approvals", "SLA compliance %", "Grievance resolution time", "Platform adoption %"],
    },
    {
        "n": "6", "name": "Alumni Portal",
        "tag": "For graduates & former members — lifelong network & contribution",
        "objective": ("YPDC relationships should not end at graduation or tenure completion. The Alumni Portal keeps "
                      "alumni connected through rich profiles, a searchable network, mentorship programs, events, "
                      "achievements, career opportunities and structured ways to volunteer or support — turning former "
                      "members into lifelong ambassadors, mentors and partners."),
        "modules": [
            ("Alumni Profile", "Lifelong identity carrying forward the member/student history.",
             "Auto-carried history • Photo & bio • Privacy controls • Verified badge"),
            ("Academic Information", "Degrees, institutions, years and specialisations.",
             "Education timeline • Transcripts (optional) • Honours"),
            ("Professional Information", "Current organisation, designation, industry and experience.",
             "Employment timeline • Industry tags • Open-to-work flag"),
            ("Skills", "Searchable skill inventory powering mentoring and hiring matches.",
             "Skill tags • Endorsements • Proficiency levels"),
            ("Alumni Network", "Searchable directory with connection requests and groups.",
             "Directory & filters • Connect/follow • Batch & chapter groups • Messaging"),
            ("Mentorship", "Structured mentor matching between alumni and current students/members.",
             "Mentor registration • Matching • Session scheduling • Feedback & hours"),
            ("Events", "Reunions, networking meetups, talks and homecoming events.",
             "Alumni event calendar • RSVP • Reunion groups • Photo sharing"),
            ("Achievements", "Career and community milestones celebrated organisation-wide.",
             "Achievement posts • Verification • Featured alumni wall"),
            ("Career Opportunities", "Jobs, internships and referrals posted by alumni and partners.",
             "Job board • Referrals • Applications tracking • Employer profiles"),
            ("Volunteer / Support Opportunities", "Give-back channels: guest lectures, funding, CSR and volunteering.",
             "Support catalogue • Pledges • Fund tracking • Impact reports & receipts"),
        ],
        "workflows": [
            "**Mentorship flow:** Alumni registers as mentor → matching → sessions scheduled → hours & feedback logged.",
            "**Career flow:** Opportunity posted → screened → published → applications → shortlist → closure update.",
            "**Give-back flow:** Pledge made → acknowledged → utilised with evidence → impact report shared.",
        ],
        "kpis": ["Registered alumni", "Mentorship hours", "Jobs posted/filled", "Support contributions"],
    },
    {
        "n": "7", "name": "Guest / Public Portal",
        "tag": "For the world — YPDC's public face & front door",
        "objective": ("The Guest/Public Portal is YPDC's website — open to everyone without login. It communicates "
                      "identity (about, vision, leadership, directorates), showcases work (projects, events, news, "
                      "achievements, gallery, publications) and converts visitors into participants through membership "
                      "and volunteer registration, contact channels and FAQs. Everything here is managed via the Admin "
                      "CMS with zero coding."),
        "modules": [
            ("About YPDC", "Founding story, mandate, legal status and organisational overview.",
             "Story page • Facts & figures • Milestones timeline • Partners strip"),
            ("Vision & Mission", "Foundational statements plus values and strategic pillars.",
             "Vision/mission/values • Strategic pillars • SDG alignment"),
            ("Leadership", "Patrons, executives, directors and advisors with profiles.",
             "Leadership grid • Bios • Messages • Tenure info"),
            ("Directorates", "Public directory of all directorates with mandates and highlights.",
             "Directory cards • Mandates • Recent highlights • Contact links"),
            ("Projects", "Flagship and ongoing projects with objectives and progress.",
             "Project pages • Objectives • Timeline • Outcomes • Galleries"),
            ("Events", "Public events calendar: upcoming, ongoing and archived events.",
             "Calendar & list • Details & posters • Registration CTA • Archive"),
            ("News & Updates", "Press releases, announcements and newsletters.",
             "News listing • Article pages • Newsletter signup • Social sharing"),
            ("Achievements", "Organisation, team and individual honours with evidence.",
             "Honour wall • Categories • Evidence & media • Yearly roundups"),
            ("Gallery", "Photos and videos organised by event, project and year.",
             "Albums • Lightbox • Video embeds • Download (optional)"),
            ("Publications", "Reports, magazines, research and policy documents library.",
             "Document library • Categories • Preview & download • Citations"),
            ("Membership", "Public membership information: benefits, criteria, fees and process.",
             "Benefits • Eligibility • Fee table • How-to-apply • Apply CTA"),
            ("Volunteer Registration", "Open volunteer intake form with opportunity linkage.",
             "Registration form • Interest areas • Availability • Auto-acknowledgement"),
            ("Contact Us", "All contact channels plus location map and enquiry form.",
             "Form with ticket ID • Map • Directory • Office hours • Social links"),
            ("FAQs", "Searchable answers reducing support load and confusion.",
             "Categorised FAQs • Search • Ask-a-question • Helpful-vote tracking"),
        ],
        "workflows": [
            "**Conversion flow:** Visitor reads → CTA clicked → membership/volunteer form → ticketed → admin processes → welcome journey.",
            "**Publishing flow:** Admin drafts content in CMS → preview → publish/schedule → appears instantly on public site.",
            "**Enquiry flow:** Contact form → auto-ticket + acknowledgement → assigned → responded → feedback on response.",
        ],
        "kpis": ["Monthly visitors", "Membership applications", "Volunteer signups", "Content freshness"],
    },
]


# ===================================================================== build
def build(path):
    pdf = Report()
    pdf.add_font("DejaVu", "", FONT_REG)
    pdf.add_font("DejaVu", "B", FONT_BLD)
    pdf.add_font("DejaVu", "I", FONT_REG)
    pdf.add_font("DejaVu", "BI", FONT_BLD)
    pdf.set_font("DejaVu", "", 9.8)
    pdf.alias_nb_pages("{nb}")

    # ---------------- cover + TOC
    pdf.cover()
    pdf.add_page()
    pdf.insert_toc_placeholder(render_toc, pages=2, allow_extra_pages=False)

    # ---------------- 1. Executive Summary (TOC placeholder already ends on a fresh page)
    pdf.section("Executive Summary")
    pdf.body(("The **YPDC Integrated Portal System** unifies seven specialised portals — **Student, Member, "
              "Directorate, Faculty, Admin, Alumni and Guest/Public** — into one secure, role-based digital platform. "
              "Together they cover the complete lifecycle of engagement with YPDC: a visitor discovers the organisation "
              "on the public website, registers as a volunteer or member, participates in events, takes on directorate "
              "responsibilities, gets mentored by faculty, earns certificates and achievements, and finally continues "
              "as alumni — mentor, employer or supporter."))
    pdf.kpi_strip([("7", "PORTALS"), ("81", "MODULES"), ("15+", "WORKFLOWS"), ("100+", "REPORT KPIs")])
    pdf.body(("This report specifies all **81 functional modules**, the **roles & permissions model**, **cross-portal "
              "workflows** (membership, events, tasks, approvals, attendance, certificates, grievances), the **reporting "
              "framework**, **non-functional requirements** and a **phased implementation roadmap**. It is written to serve "
              "three audiences at once: **leadership** (for decisions), **developers** (for building), and **auditors** "
              "(for verification)."))
    pdf.sub("Key decisions this report enables")
    pdf.bullets([
        "**Scope lock:** exactly what each portal contains — no ambiguity during development.",
        "**Role model:** who can see and do what — enforced by 200+ granular permissions.",
        "**Workflow standards:** one approved way for proposals, approvals, attendance and certificates.",
        "**Build order:** Phase 1 (foundation + public site + admin) → Phase 4 (alumni & analytics) — value delivered early.",
    ])
    pdf.info_box("Reading guide",
                 ("Sections 2–3 give context and architecture. Sections 4–10 specify each portal module-by-module. "
                  "Sections 11–14 define cross-cutting systems, data, workflows and analytics. Sections 15–18 cover "
                  "quality, roadmap, risks and conclusions. Appendix A is the master 81-module checklist."))

    # ---------------- 2. About & Purpose
    pdf.section("About YPDC & Document Purpose")
    pdf.sub("About YPDC")
    pdf.body(("**YPDC (Youth Peace & Development Council)** is a youth-led organisation dedicated to peace-building, "
              "leadership development, community service and skills empowerment. It operates through specialised "
              "**directorates**, guided by **faculty mentors**, powered by **student and member volunteers**, and "
              "sustained by an **alumni network** — all visible to the public through an open, transparent platform."))
    pdf.sub("Vision & Mission (platform reflection)")
    pdf.bullets([
        "**Vision:** an empowered generation of youth leading peaceful, developed and inclusive communities.",
        "**Mission:** to organise, train and recognise youth through structured programs, transparent governance and digital-first operations.",
        "**Platform promise:** every contribution is recorded, every achievement is verifiable, every process is traceable.",
    ])
    pdf.sub("Document purpose & scope")
    pdf.body("In scope: all 7 portals, 81 modules, roles, workflows, reports, notifications, documents and grievance handling. "
             "Out of scope (for v1.0): mobile native apps (responsive web first), payroll/finance ERP, and third-party LMS integration — all planned as Phase-5 extensions.")
    pdf.sub("Stakeholders")
    pdf.mtable(["Stakeholder", "Interest & responsibility"],
              [["YPDC Leadership / Patrons", "Vision, approvals, strategic oversight"],
               ["Directors & Assistant Directors", "Directorate planning, tasking, event ownership"],
               ["Members & Students", "Participation, duties, volunteering, feedback"],
               ["Faculty Mentors / Advisors", "Guidance, supervision, approvals, evaluations"],
               ["Alumni", "Mentorship, careers, networking, support"],
               ["Admin / IT Team", "Platform operations, content, compliance, support"],
               ["Public / Guests", "Discovery, trust, registration, enquiries"]],
              widths=[52, 128])

    # ---------------- 3. System overview
    pdf.section("System Overview & Architecture")
    pdf.sub("The seven portals at a glance")
    pdf.mtable(["#", "Portal", "Primary users", "Modules", "Core purpose"],
              [["1", "Student Portal", "Enrolled students", "10", "Participate, volunteer, earn recognition"],
               ["2", "Member Portal", "Inducted members", "10", "Duties, tasks, performance & reporting"],
               ["3", "Directorate Portal", "Directors, ADs, teams", "13", "Plan, execute & govern directorate work"],
               ["4", "Faculty Portal", "Faculty / mentors", "9", "Guide, supervise & approve"],
               ["5", "Admin Portal", "Administrators", "15", "Operate, govern & analyse everything"],
               ["6", "Alumni Portal", "Graduates / ex-members", "10", "Network, mentor, hire & support"],
               ["7", "Guest / Public Portal", "Everyone (no login)", "14", "Showcase, inform & convert visitors"]],
              widths=[8, 40, 38, 16, 78])
    pdf.sub("Access model")
    pdf.bullets([
        "**Single Sign-On (SSO):** one account, multiple roles — a member who is also a student sees both portals via a role switcher.",
        "**Public by default, private by role:** Guest portal needs no login; all other portals enforce authentication + role checks on every page and API.",
        "**Digital identity:** every member/student carries a QR-coded digital ID; every certificate carries a verification code checked on the public site.",
    ])
    pdf.sub("High-level architecture (recommended)")
    pdf.steps([
        "**Presentation layer:** responsive web app (mobile-first) + public website sharing one design system; portals as role-routed workspaces.",
        "**Application layer:** modular services — Identity & Access, Membership, Events, Tasks, Attendance, Certificates, Notifications, CMS, Reports, Grievance.",
        "**Data layer:** relational database (primary records) + object storage (documents/media) + search index (directory, FAQs, publications).",
        "**Integration layer:** email/SMS/push gateways, QR generation & scanning, calendar feeds, export (PDF/Excel), and audit logging on every write.",
    ])
    pdf.sub("Recommended technology principles (stack-agnostic)")
    pdf.bullets([
        "Modern web framework with server-side rendering for the public site (SEO) and app-style routing for portals.",
        "REST/JSON APIs with token authentication; full audit trail; automated backups and role-based data isolation.",
        "Accessibility (WCAG 2.1 AA), Urdu + English bilingual UI, and print-friendly outputs for all official documents.",
    ])

    # ---------------- 4-10. Portals
    for p in PORTALS:
        pdf.section(f"Portal {p['n']} — {p['name']}")
        pdf.body(f"{p['tag']}  •  **{len(p['modules'])} modules**", align="L")
        pdf.body(p["objective"])
        pdf.sub2("Module specifications")
        rows = [(m, pu, kf) for (m, pu, kf) in p["modules"]]
        pdf.mtable(["Module", "Purpose", "Key features"], rows, widths=[38, 66, 76], size=8.4)
        pdf.sub2("Key workflows")
        pdf.bullets(p["workflows"])
        pdf.sub2("Portal success metrics")
        pdf.bullets(["**" + k + "** — monthly KPI on the Admin dashboard and digest reports." for k in p["kpis"]])

    # ---------------- 11. Cross-cutting
    pdf.section("Cross-Cutting Systems (used by all portals)")
    pdf.sub("Authentication, roles & permissions")
    pdf.body(("Access follows **least privilege**: every action maps to a permission; permissions bundle into roles; "
              "roles attach to users (a user may hold several, e.g. Member + Volunteer Lead). Sensitive actions "
              "(approvals, certificate issuance, data export) require explicit grants and leave an **immutable audit log**."))
    pdf.mtable(["Role", "Sees", "Can do (examples)"],
              [["Guest", "Public portal only", "Browse, register interest, verify certificates, contact"],
               ["Student", "Student portal", "Apply, register, volunteer, feedback, download own certificates"],
               ["Member", "Member + Student", "Duties, tasks, reports, duty check-in"],
               ["Director / AD", "Directorate + Member", "Plan, assign, propose events, review reports"],
               ["Faculty", "Faculty portal", "Mentor, approve, evaluate, report"],
               ["Alumni", "Alumni portal", "Network, mentor, post jobs, pledge support"],
               ["Admin", "Everything", "Configure, approve, publish, issue, analyse, delegate"]],
              widths=[30, 50, 100])
    pdf.sub("Events lifecycle (unified across portals)")
    pdf.steps([
        "**Propose:** Directorate submits proposal (objectives, budget, venue, team) → Admin review → approve / return with remarks.",
        "**Publish:** approved event published to Student/Member/Alumni/Public audiences with eligibility rules and seat caps.",
        "**Register:** one-click registration → QR e-ticket → waitlist when full → reminders before the event.",
        "**Execute:** QR/biometric/manual check-in → live attendance → duty roster enforcement → media capture.",
        "**Close:** attendance frozen → feedback forms opened → certificates auto-issued → activity report filed → analytics updated.",
    ])
    pdf.sub("Attendance system")
    pdf.bullets([
        "**Three capture modes:** QR scan (fast, offline-tolerant), manual register (fallback), biometric/API (where hardware exists).",
        "**Policy engine:** per-event and per-directorate rules — late thresholds, minimum % for certificates, defaulter flags.",
        "**Transparency:** every user sees their own log; leads see team registers; admin sees organisation-wide heatmaps.",
    ])
    pdf.sub("Certificates & achievements")
    pdf.bullets([
        "**Template designer:** admin creates branded templates with dynamic fields (name, event, date, grade, QR).",
        "**Issuance:** automatic (on attendance + feedback completion) or nominated (awards, service) with approval chain.",
        "**Verification:** any certificate verified publicly via QR/code — no login needed — with revocation support.",
        "**Gamification:** points + badges feed leaderboards at student, member and directorate levels.",
    ])
    pdf.sub("Notifications engine")
    pdf.bullets([
        "**Multi-channel:** in-app + push + email + SMS with per-user preferences and quiet hours.",
        "**Templated & translated:** every message type has Urdu + English templates with variable injection.",
        "**Actionable:** approval requests, task assignments and tickets carry deep links and one-click actions.",
        "**Accountable:** delivery reports per campaign; critical alerts (approvals, SLA breaches) escalate automatically.",
    ])
    pdf.sub("Feedback & grievance (complaints)")
    pdf.bullets([
        "**Event feedback:** structured forms (ratings + open text) open automatically after each event; results feed event scores.",
        "**Suggestions:** always-open box per portal; votable; admin triages monthly with public status updates.",
        "**Complaints:** ticketed grievance redressal — categories, SLA timers (acknowledge 24h), assignment, escalation, resolution and complainant rating.",
    ])
    pdf.sub("Documents & content governance")
    pdf.bullets([
        "**Single library** with folders, versioning, retention rules and access control; every download logged.",
        "**CMS:** all public-portal content editable by authorised admins with draft → preview → publish/schedule and full revision history.",
        "**Official outputs:** reports, ID cards, certificates and letters all print/PDF-ready on YPDC letterhead.",
    ])

    # ---------------- 12. Data entities
    pdf.section("Data Model — Core Entities (summary)")
    pdf.body(("The platform centres on **people, structure, work and proof**. The table below lists the primary entities; "
              "a full ERD with relationships is produced in the design phase. Every entity carries created/updated "
              "timestamps, ownership and an audit trail."))
    pdf.mtable(["Domain", "Core entities"],
              [["People", "User, StudentProfile, MemberProfile (ID, tenure, status), FacultyProfile, AlumniProfile, Guardian"],
               ["Structure", "Directorate, Role, Permission, TeamMembership, LeadershipTenure"],
               ["Engagement", "Event, Registration, Ticket, DutyRoster, VolunteerOpportunity, VolunteerApplication, HourLog"],
               ["Work", "Objective (OKR), WorkPlan, Milestone, Task (+comments, attachments), Meeting, Minute"],
               ["Proof", "AttendanceRecord, Certificate (+template, verification code), Badge, PointLedger, Achievement"],
               ["Governance", "Application/ApprovalRequest, Report, Document (+versions), FeedbackResponse, ComplaintTicket (+SLA)"],
               ["Outreach", "NewsPost, Project, Publication, GalleryAlbum, PageContent, FAQ, Enquiry, NewsletterSubscriber"],
               ["Career/ Alumni", "EmploymentRecord, Skill, Connection, Mentorship (+sessions), JobPost, JobApplication, Pledge"]],
              widths=[38, 142])
    pdf.info_box("Data integrity rules (enforced in v1.0)",
                 ("One person = one User record (CNIC/email unique). Member IDs are sequential and never reused. "
                  "Certificates are immutable once issued (revocation creates a new state, never edits). "
                  "Attendance freezes after event close; corrections need approval with reason. All deletes are soft-deletes."))

    # ---------------- 13. Workflows detail
    pdf.section("End-to-End Workflows (approval chains)")
    pdf.sub("W1 — Membership application")
    pdf.steps(["Guest/Student submits application (public or student portal) with documents.",
               "Admin verifies eligibility & documents; may request corrections.",
               "Approved → Member profile + digital ID issued → directorate allotted → welcome pack notified.",
               "Rejected → reason shared; re-application allowed after defined period."])
    pdf.sub("W2 — Event proposal to certificate")
    pdf.steps(["Directorate submits proposal → Admin (+ mapped Faculty where needed) approves/returns.",
               "Event published → registrations → ticketed → reminders.",
               "Check-in (QR) → attendance captured → event closed.",
               "Feedback collected → certificates auto-issued → report filed → analytics updated."])
    pdf.sub("W3 — Task & duty management")
    pdf.steps(["Lead creates task/duty with owner, deadline, evidence requirement.",
               "Owner accepts → executes → submits evidence → lead reviews → scored/closed.",
               "Overdue items escalate automatically; scores feed monthly performance."])
    pdf.sub("W4 — Approvals (generic)")
    pdf.steps(["Any request enters the unified queue with type, requester, documents and SLA clock.",
               "Auto-routed to the mapped approver (Admin/Faculty/Director) → approve / return with remarks.",
               "Requester notified at every state change; full history retained for audit."])
    pdf.sub("W5 — Complaint redressal")
    pdf.steps(["Complaint filed (any portal + public contact) → ticket ID + acknowledgement within 24 hours.",
               "Categorised and assigned → investigated → resolved → complainant rates the resolution.",
               "Breached SLAs auto-escalate; monthly grievance analytics reviewed by leadership."])

    # ---------------- 14. Reports & analytics
    pdf.section("Reports & Analytics Framework")
    pdf.body(("Every portal contributes data to a shared analytics layer. Admin gets the full catalogue; directors, "
              "faculty and members get role-filtered views of their own scope. All reports export to **PDF/Excel** and "
              "can be **scheduled by email** (daily/weekly/monthly)."))
    pdf.mtable(["Category", "Example reports / KPIs", "Audience"],
              [["Participation", "Registrations, footfall, volunteer hours, repeat-participation rate", "All leads, Admin"],
               ["Membership", "Applications funnel, approvals, renewals, drop-offs, ID issuance", "Admin, Directors"],
               ["Directorates", "Objective completion, work-plan adherence, event delivery, directorate ranking", "Leadership"],
               ["Tasks & duties", "Completion %, overdue, escalation count, evidence compliance", "Directors, Admin"],
               ["Attendance", "Event-wise %, member-wise %, defaulter lists, trend heatmaps", "Leads, Admin"],
               ["Certificates", "Issued/verified/revoked, pending nominations, verification hits", "Admin, Public verify"],
               ["Performance", "Member scores, faculty engagement, mentor hours, improvement deltas", "Leads, Faculty"],
               ["Grievance", "Tickets by category/SLA, resolution time, satisfaction rating", "Leadership"],
               ["Outreach", "Visitors, conversions, news reach, gallery/publication engagement", "Media, Admin"],
               ["Alumni & career", "Registrations, mentorship hours, jobs posted/filled, pledges & impact", "Leadership"]],
              widths=[32, 92, 56])
    pdf.info_box("Decision cadence (recommended)",
                 ("Weekly: pending approvals, overdue tasks, upcoming events. Monthly: directorate scorecards, "
                  "attendance & grievance review. Quarterly: OKR review, alumni & outreach analysis. Annually: impact "
                  "report compiled for patrons, partners and the public portal."))

    # ---------------- 15. NFRs
    pdf.section("Non-Functional Requirements")
    pdf.mtable(["Quality", "Requirement (v1.0 target)"],
              [["Performance", "Public pages < 2s; portal pages < 3s at 500 concurrent users; paginated lists everywhere"],
               ["Availability", "99.5% monthly; automated health checks; graceful degradation for QR/offline check-in"],
               ["Security", "Encrypted transport + hashed credentials; role checks server-side; audit logs; session controls; data backups daily"],
               ["Privacy", "Role-scoped data visibility; consent for public showcase; alumni/student privacy controls; retention policy"],
               ["Usability", "Mobile-first responsive; Urdu + English; accessible (WCAG 2.1 AA); max 3 clicks to core actions"],
               ["Reliability", "No silent failures — every submission returns a reference ID; retry-safe forms; idempotent issuance"],
               ["Scalability", "Modular services;Bulk operations (import, issue, notify) queued in background jobs"],
               ["Maintainability", "CMS-managed content; template-managed certificates/notifications; documented APIs for Phase-5 apps"],
               ["Auditability", "Immutable logs for approvals, issuance, permission changes and exports; monthly audit extract"]],
              widths=[34, 146])

    # ---------------- 16. Roadmap
    pdf.section("Implementation Roadmap (phased delivery)")
    pdf.body(("Delivery is phased so value reaches users early while foundations stay solid. Each phase ends with "
              "**user acceptance testing (UAT)** and training for the affected roles."))
    pdf.mtable(["Phase", "Duration*", "Delivers", "Users unblocked"],
              [["Phase 1 — Foundation & Public Face",
                "Weeks 1–6",
                "SSO + roles, Admin core (dashboard, users, roles), Guest/Public portal + CMS, contact/FAQ, certificate verification",
                "Public, Admin, Media team"],
               ["Phase 2 — Engagement Core",
                "Weeks 7–12",
                "Student portal, Events lifecycle (propose→publish→register→QR check-in), Attendance, Notifications, Feedback",
                "Students, Event teams"],
               ["Phase 3 — Governance & Work",
                "Weeks 13–18",
                "Member + Directorate portals (tasks, duties, work plans, proposals, meetings), Faculty approvals, Certificates & badges, Grievance",
                "Members, Directors, Faculty"],
               ["Phase 4 — Network & Intelligence",
                "Weeks 19–24",
                "Alumni portal (network, mentorship, jobs), full analytics catalogue, scheduled digests, documents hub, performance scorecards",
                "Alumni, Leadership"],
               ["Phase 5 — Extensions (optional)",
                "Post-launch",
                "Native mobile apps, LMS/payments integration, advanced BI, chatbot for FAQs",
                "All"]],
              widths=[34, 20, 80, 46])
    pdf.body("*Durations are indicative for a focused team and assume content (logos, copy, photos) is supplied on time. "
             "Each phase includes data migration of existing member/event records where available.", size=8.8)
    pdf.sub("Priority order if scope must be trimmed")
    pdf.steps(["Never cut: identity/roles, event registration + attendance, approvals, certificate verification.",
               "Defer first: gamification leaderboards, advanced custom-report builder, SMS (keep email + in-app).",
               "Protect: grievance SLA tracking and audit logs — these carry institutional trust."])

    # ---------------- 17. Estimates & governance
    pdf.section("Effort View & Governance")
    pdf.sub("Module count by portal")
    pdf.mtable(["Portal", "Modules", "Share"],
              [["Student Portal", "10", "12%"],
               ["Member Portal", "10", "12%"],
               ["Directorate Portal", "13", "16%"],
               ["Faculty Portal", "9", "11%"],
               ["Admin Portal", "15", "19%"],
               ["Alumni Portal", "10", "12%"],
               ["Guest / Public Portal", "14", "17%"],
               ["TOTAL", "81", "100%"]],
              widths=[70, 30, 80])
    pdf.sub("Suggested governance during build")
    pdf.bullets([
        "**Product owner (YPDC side):** one empowered decision-maker for scope, content and approvals.",
        "**Weekly demo:** working software shown every week; feedback logged as tickets, not messages.",
        "**Content owners:** one named owner per directorate/public-section for CMS content and media.",
        "**Data protection:** staging uses masked data; production access is role-based and logged.",
    ])
    pdf.sub("Risks & mitigations")
    pdf.mtable(["Risk", "Mitigation"],
              [["Scope creep from 81 modules", "This report = frozen scope for v1.0; changes via formal change log"],
               ["Content delays (photos, copy)", "CMS training early; placeholder content allowed; owners named upfront"],
               ["Low adoption / training gaps", "Role-based walkthroughs + Urdu video guides + helpdesk in first 60 days"],
               ["Event-day load spikes", "Queued bulk jobs; paginated scans; offline-tolerant QR check-in"],
               ["Data quality of legacy records", "Bulk-import templates with validation; verification step before go-live"]],
              widths=[55, 125])

    # ---------------- 18. Conclusion
    pdf.section("Conclusion & Recommendations")
    pdf.body(("The YPDC Integrated Portal System, as specified in this report, gives the organisation a **single source "
              "of truth** for people, work and proof — from a guest's first visit to an alumnus's lifelong contribution. "
              "The design balances **openness** (public showcase, verifiable certificates) with **discipline** (approvals, "
              "attendance, audit trails), and balances **ambition** (81 modules) with **pragmatism** (phased delivery, "
              "trim priorities)."))
    pdf.sub("Recommended next steps")
    pdf.steps([
        "**Approve this report (v1.0)** as the frozen functional scope and authorise Phase-1 kickoff.",
        "**Nominate owners:** product owner, one content owner per directorate, and the approvals matrix (who approves what).",
        "**Supply brand kit & content:** logo, colours, leadership bios/photos, directorate mandates, existing member/event lists.",
        "**Confirm policies:** membership criteria & fees, attendance thresholds, certificate rules, grievance SLAs, bilingual requirements.",
        "**Kick off Phase 1** with weekly demos; run UAT with real students/members before each phase goes live.",
    ])
    pdf.info_box("Sign-off block",
                 ("Prepared for: YPDC Leadership  •  Document: YPDC Integrated Portal System Report v1.0  •  Date: 10 September 2026\n"
                  "Approved by: ______________________    Date: __________\n"
                  "Product Owner: ______________________    Date: __________"))

    # ---------------- Appendix A
    pdf.section("Appendix A — Master Module Checklist (81 modules)")
    pdf.body("Use this table to track build & UAT status. Suggested status values: **Not started / In progress / In UAT / Live**.")
    master = []
    for p in PORTALS:
        for m, pu, kf in p["modules"]:
            master.append([f"P{p['n']}", p["name"].replace(" Portal", ""), m, "☐"])
    pdf.mtable(["ID", "Portal", "Module", "Live?"], master, widths=[14, 42, 104, 20], size=8.2, lh=5.0)

    # ---------------- Appendix B
    pdf.section("Appendix B — Glossary")
    pdf.mtable(["Term", "Meaning in this report"],
              [["YPDC", "Youth Peace & Development Council — the organisation this platform serves"],
               ["Directorate", "A specialised unit (e.g. Events, Media) with a director, team, objectives and work plan"],
               ["Member vs Student", "Student = enrolled participant; Member = inducted office-holder under a directorate"],
               ["Duty", "An assigned operational role in a specific event (usher, media, protocol, etc.)"],
               ["SLA", "Service-level agreement — e.g. acknowledge complaints within 24 hours"],
               ["OKR", "Objectives & Key Results — quarterly goal-setting method for directorates"],
               ["CMS", "Content Management System — no-code editing of the public website"],
               ["QR check-in", "Attendance marking by scanning ticket/ID QR codes at venues"],
               ["UAT", "User Acceptance Testing — formal sign-off by real users before go-live"]],
              widths=[36, 144])

    pdf.output(path)
    return path


if __name__ == "__main__":
    out = "ypdc-report/YPDC-Portal-System-Report.pdf"
    import os
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build(out)
    print("written:", out)
