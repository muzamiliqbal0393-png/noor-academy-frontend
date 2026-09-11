# -*- coding: utf-8 -*-
"""Report content: front matter, overview, scope, roles, architecture, workflows."""

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer, Table, TableStyle

FRAME_W = None  # set at build() time from the renderer module


# --------------------------------------------------------------------------- #
# helpers bound to the renderer module
# --------------------------------------------------------------------------- #
class R:
    """Renderer namespace, populated in build()."""
    pass


def _portal_header(no, title, subtitle):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    st_t = ParagraphStyle("pt", fontName=R.FONT_B, fontSize=15.5, leading=19,
                          textColor=R.WHITE, alignment=TA_LEFT, spaceAfter=1)
    st_s = ParagraphStyle("ps", fontName=R.FONT, fontSize=8.6, leading=11.5,
                          textColor=colors.HexColor("#CFE3EA"), alignment=TA_LEFT)
    t = Table([[[Paragraph("PORTAL %s" % no, ParagraphStyle(
        "pk", fontName=R.FONT_B, fontSize=7.2, leading=9,
        textColor=colors.HexColor("#8FD8D6"), alignment=TA_LEFT))]],
        [[Paragraph(title, st_t)]], [[Paragraph(subtitle, st_s)]]],
        colWidths=[R.FRAME_W], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), R.NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
        ("LINEBELOW", (0, -1), (-1, -1), 2.4, R.TEAL),
    ]))
    return [Spacer(1, 2), t, Spacer(1, 8)]


def module_table(rows):
    """rows = [(module, purpose, key functions, data entities)]"""
    w = [R.FRAME_W * x for x in (0.155, 0.275, 0.36, 0.21)]
    return R.make_table(["Module", "Purpose", "Key functions / rules", "Primary data entities"],
                        [[R.para("<b>%s</b>" % m, R.TC_B), p, k, d] for m, p, k, d in rows],
                        w, font_small=True)


def journey(steps, cols=3, caption=None, accent=None):
    fl = R.ChevronFlow(steps, cols=cols, accent=accent or R.TEAL)
    if caption:
        return R.figure(fl, caption)
    return R.KeepTogether([Spacer(1, 3), fl, Spacer(1, 6)])


def flow(nodes, caption):
    return R.figure(R.ProcessFlow(nodes), caption)


# ========================================================================== #
#  PORTAL DATA
# ========================================================================== #
PORTALS = {}

PORTALS["guest"] = dict(
    no="07", title="Guest / Public Portal",
    subtitle="Unauthenticated public interface - the discovery, credibility and entry point of YPDC",
    purpose=(
        "The Guest/Public Portal is the only fully public surface of the platform. It converts "
        "anonymous visitors into applicants, volunteers, partners and audiences. Everything here "
        "is published by the Admin Portal (Website Content module) and cached for performance; "
        "no personal data of members is exposed without explicit consent."),
    audience=("Public visitors, prospective students and members, parents, media, "
              "partner institutions, recruiters, alumni prospects."),
    access="Public - no login required. Write actions limited to forms (membership, volunteer, contact).",
    modules=[
        ("About YPDC",
         "Introduce the organisation, its history, mandate and structure.",
         "Static CMS page with rich media; history timeline; organogram; downloadable profile; "
         "last-updated stamp and page owner.",
         "ContentPage, MediaAsset"),
        ("Vision &amp; Mission",
         "Publish strategic intent and core values.",
         "Vision / mission / values blocks; strategic pillars; annual theme; print-ready version.",
         "ContentPage"),
        ("Leadership",
         "Show governance and patronage.",
         "Patron, president and office-bearer profiles with photo, tenure and portfolio; "
         "succession chronology.",
         "User, Profile, ContentPage"),
        ("Directorates",
         "Present all directorates as functional units.",
         "Directorate cards (name, mandate, director, team size); link to objectives and public "
         "activities; contact focal person.",
         "Directorate, Profile"),
        ("Projects",
         "Showcase ongoing and completed projects.",
         "Project listing with status, timeline, progress %, partner and impact metrics; "
         "detail page with gallery and reports.",
         "Project, ActivityReport"),
        ("Events",
         "Public event calendar and event detail pages.",
         "Upcoming / past split; filters (type, directorate, venue, month); event page with "
         "agenda, speakers, map; registration link where seats are public.",
         "Event, Registration"),
        ("News &amp; Updates",
         "Announcements, press releases and notices.",
         "Chronological feed; categories and tags; pinned notices; RSS / share links; "
         "publication date and author.",
         "ContentPage, MediaAsset"),
        ("Achievements",
         "Celebrate organisational and member achievements.",
         "Achievement cards (title, member/directorate, date, awarding body); consent-gated "
         "publishing; yearly archive.",
         "Achievement"),
        ("Gallery",
         "Visual record of activities.",
         "Albums by event; lazy loading; download with watermark; consent flag per image; "
         "moderation queue before publish.",
         "MediaAsset, Album"),
        ("Publications",
         "Repository of reports, newsletters and research.",
         "Document listing with type, year and file size; preview and download counters; "
         "access level (public / member-only).",
         "Document"),
        ("Membership",
         "Explain membership and accept applications.",
         "Tiers, eligibility, benefits, fee schedule and process diagram; online application "
         "form with document upload; application reference number issued instantly.",
         "Application, Document"),
        ("Volunteer Registration",
         "Capture public volunteers for YPDC activities.",
         "Multi-step form (personal, skills, availability, interests); CV upload; consent for "
         "data processing; auto-acknowledgement and reference ID.",
         "Application, User"),
        ("Contact Us",
         "Single entry point for enquiries.",
         "Enquiry form with category routing; department emails; office address and map; "
         "working hours; ticket ID returned to sender.",
         "Ticket"),
        ("FAQs",
         "Self-service answers to repeated questions.",
         "Categorised accordion; search; helpful / not-helpful vote; unanswered questions "
         "promoted to admin for new FAQ creation.",
         "ContentPage, Ticket"),
    ],
    journey=[
        ("Land on site", "Home page with value proposition, counters and latest activity"),
        ("Explore", "About, vision, leadership, directorates, projects, gallery, publications"),
        ("Check calendar", "Upcoming events, news and open calls"),
        ("Choose action", "Apply for membership, register as volunteer, or contact YPDC"),
        ("Submit form", "Form validation, document upload, consent capture"),
        ("Get reference", "Auto-acknowledgement with reference ID by e-mail / SMS"),
        ("Track status", "Status visible on the public 'Track Application' page"),
    ],
    cols=3,
)

PORTALS["student"] = dict(
    no="01", title="Student Portal",
    subtitle="Authenticated space for enrolled students - membership, participation, attendance and recognition",
    purpose=(
        "The Student Portal is the first authenticated experience of a YPDC participant. It is "
        "designed to be low-friction: a student logs in with an institutional or e-mail account, "
        "completes a profile, tracks membership status, registers for events and volunteer drives, "
        "and collects attendance, certificates and achievements that later support a full "
        "membership application."),
    audience="Enrolled students of partner institutions; prospective members.",
    access="Authenticated. Reads own records only; writes limited to own profile, registrations and feedback.",
    modules=[
        ("Profile",
         "Single source of truth for student identity and contact.",
         "Personal, academic and contact details; photo upload with auto-crop; institution, "
         "programme, semester; completion score; change history with audit trail.",
         "User, Profile"),
        ("Membership",
         "Show and progress the student's membership status.",
         "Status timeline (Not applied / Applied / Screening / Inducted / Suspended); "
         "eligibility checklist; fee and validity; renew and upgrade to full member.",
         "Membership, Application"),
        ("Events",
         "Discover events relevant to the student.",
         "Filter by type, directorate, date and eligibility; seat availability; waitlist; "
         "add-to-calendar and reminders.",
         "Event"),
        ("Event Registration",
         "Convert interest into a confirmed seat.",
         "Eligibility rule check (year, quota, prerequisites); duplicate control; QR e-pass on "
         "confirmation; cancellation before cut-off frees the seat.",
         "Registration, Event"),
        ("Volunteer Opportunities",
         "Open calls for student volunteers.",
         "Opportunity cards (role, shift, skill need, seats); apply with skill match score; "
         "accept / decline assignment; service-hours ledger.",
         "VolunteerOpportunity, Application"),
        ("Attendance",
         "Personal attendance record across all activities.",
         "Session-wise record with date, event, method and status; percentage by category; "
         "deficiency warning below threshold; self-mark with geo/photo proof where allowed.",
         "Attendance, Session"),
        ("Certificates",
         "Earned certificates and verification.",
         "Auto-issued on rule fulfilment; PDF download with serial number and QR; verification "
         "link; transcript-style consolidated statement.",
         "Certificate, Attendance"),
        ("Achievements",
         "Recognition beyond attendance.",
         "Badges and milestones (best volunteer, event lead, competition); leaderboard opt-out; "
         "publish-to-public-portal consent toggle.",
         "Achievement"),
        ("Notifications",
         "Timely, relevant communication.",
         "In-app bell, e-mail and SMS channels; preferences per category; digest mode; "
         "read receipts.",
         "Notification"),
        ("Feedback",
         "Capture experience after every activity.",
         "Post-event rating (1-5) with comments; complaint escalation; anonymity option; "
         "closure notification when resolved.",
         "Ticket, Feedback"),
    ],
    journey=[
        ("Log in", "SSO / e-mail OTP into the student workspace"),
        ("Complete profile", "Mandatory fields gate access to registration"),
        ("Verify membership", "Status, eligibility checklist, dues"),
        ("Browse events", "Filters, seats, waitlist"),
        ("Register", "Eligibility check, QR e-pass issued"),
        ("Volunteer", "Apply to an open call, accept a shift"),
        ("Attend", "Check-in by QR / geo-fence / manual list"),
        ("Get recognised", "Certificate and achievement auto-issued"),
        ("Give feedback", "Post-event rating, complaint if needed"),
    ],
    cols=3,
)

PORTALS["member"] = dict(
    no="02", title="Member Portal",
    subtitle="Working space of an inducted YPDC member - duties, tasks, performance and reporting",
    purpose=(
        "A member is a student who has completed induction and holds a Member ID with a "
        "directorate allocation. The Member Portal is transactional: it shows what the member "
        "owns (responsibilities, tasks, duties), records what the member did (attendance, "
        "activity logs) and reflects how the member is performing (score, report, certificate)."),
    audience="Inducted members, team leads within a directorate.",
    access="Authenticated. Full read/write on own records; read-only on directorate objectives and work plan.",
    modules=[
        ("Profile &amp; Member ID",
         "Verified identity and digital membership card.",
         "Auto-generated Member ID (format YPDC-YYYY-DIR-NNNN); QR card for check-in; profile "
         "verification badge; editable contact with admin re-verification for critical fields.",
         "User, Profile, Membership"),
        ("Directorate",
         "The member's organisational home.",
         "Assigned directorate with mandate and leadership; team roster; switching requires "
         "director approval; transfer history.",
         "Directorate, DirectorateMember"),
        ("Responsibilities",
         "Standing duties attached to the member's role.",
         "Role-based responsibility list; acceptance acknowledgement; review at induction and "
         "on role change; non-acceptance flagged to director.",
         "Responsibility, DirectorateMember"),
        ("Tasks",
         "Discrete assignments with owners and deadlines.",
         "Assigned / in-progress / submitted / approved states; file and link attachments; "
         "progress updates; overdue alerts to member and director.",
         "Task"),
        ("Events / Duties",
         "Duty roster for events and activities.",
         "Duty allocation with shift, venue and reporting officer; accept / request swap; "
         "duty report submission after the event.",
         "Event, DutyAssignment"),
        ("Attendance",
         "Attendance across sessions, events and duties.",
         "Category-wise percentage; minimum thresholds per category; deficiency notice and "
         "condonation request; export for personal record.",
         "Attendance, Session"),
        ("Certificates",
         "Participation, completion and merit certificates.",
         "Rule-based auto-issue; director recommendation for merit certificates; QR-verified "
         "PDF; renewal on repeated participation.",
         "Certificate"),
        ("Performance",
         "Objective, transparent performance standing.",
         "Score components (tasks 40%, attendance 25%, events 20%, conduct 15%); monthly and "
         "cumulative view; director comments; appeal within 7 days.",
         "Performance"),
        ("Reports",
         "Member-generated activity reporting.",
         "Activity / duty / incident report templates; draft and submit; director acknowledgement; "
         "history with reviewer remarks.",
         "ActivityReport"),
        ("Notifications",
         "Task, duty and approval alerts.",
         "Deadline reminders (T-3, T-1, overdue); duty roster published; approval outcomes; "
         "channel preferences.",
         "Notification"),
    ],
    journey=[
        ("Log in", "Member ID or e-mail with 2FA"),
        ("Read duties", "Responsibilities and task queue on the dashboard"),
        ("Execute tasks", "Update progress, attach evidence, submit"),
        ("Attend events", "Duty shift check-in and duty report"),
        ("File report", "Activity report submitted for director review"),
        ("Get reviewed", "Director rates, comments and approves"),
        ("See performance", "Score recalculated and published"),
        ("Earn certificate", "Auto-issued on rule fulfilment"),
    ],
    cols=3,
)

PORTALS["directorate"] = dict(
    no="03", title="Directorate Portal",
    subtitle="Management console for directors, assistant directors and team leads",
    purpose=(
        "Directorates are the delivery engine of YPDC. This portal lets a directorate plan "
        "(objectives, work plan), organise (team, tasks, duties), execute (events, activities) "
        "and prove its work (activity reports, achievements, performance). Every artefact created "
        "here feeds the Admin Portal's approvals, attendance and analytics modules."),
    audience="Director, Assistant Director, team leads of a directorate.",
    access="Authenticated, scoped to own directorate. Proposes and recommends; final approvals rest with Admin/Faculty per the approval matrix.",
    modules=[
        ("Directorate Profile",
         "Identity and mandate of the unit.",
         "Name, mandate, focus areas, established date, contact; public summary mirrored on the "
         "Guest Portal; edit requests routed to Admin.",
         "Directorate"),
        ("Director / Assistant Director",
         "Leadership record and delegation.",
         "Appointment with tenure; delegation matrix; acting arrangements; handover checklist "
         "on change of office.",
         "DirectorateMember, Role"),
        ("Team Members",
         "Roster management.",
         "Add / remove members with reason; skill and availability matrix; sub-team grouping; "
         "capacity limits per activity.",
         "DirectorateMember, User"),
        ("Objectives",
         "What the directorate must achieve.",
         "SMART objectives linked to the YPDC annual plan; owner, target value and due date; "
         "quarterly review status.",
         "Objective"),
        ("Work Plan",
         "Time-phased breakdown of objectives.",
         "Monthly / quarterly plan lines; milestones; dependency flags; variance against plan; "
         "faculty and admin visibility.",
         "WorkPlan, Objective"),
        ("Tasks",
         "Delegation and follow-up.",
         "Create and assign tasks with deadline and priority; sub-tasks; bulk assign to a "
         "sub-team; progress dashboard and escalation on delay.",
         "Task"),
        ("Events &amp; Activities",
         "Delivery calendar of the directorate.",
         "Activity register; owner, venue, budget, expected footfall; checklists (venue, media, "
         "logistics); post-activity closure.",
         "Event, Activity"),
        ("Event Proposals",
         "Formal request to hold an event.",
         "Proposal form (title, rationale, objectives, audience, budget, date, risk); document "
         "attachments; multi-level approval chain; status tracking with SLA timer.",
         "EventProposal, ApprovalWorkflow"),
        ("Attendance",
         "Attendance administration for the unit.",
         "Create session, generate QR / code; mark attendance from device; import manual list; "
         "excuse and condonation requests; reconciliation report.",
         "Attendance, Session"),
        ("Activity Reports",
         "Evidence of work done.",
         "Post-event report (summary, footfall, outcomes, budget used, media links, lessons); "
         "director sign-off; faculty review; publication to public portal.",
         "ActivityReport, MediaAsset"),
        ("Achievements",
         "Unit-level recognition.",
         "Log directorate and member achievements; recommendation to Admin for certificate; "
         "public display with consent.",
         "Achievement"),
        ("Documents",
         "Unit document repository.",
         "SOPs, templates, minutes, reports; folder structure with version control; "
         "access level (unit / member / admin); retention and disposal rules.",
         "Document"),
        ("Performance",
         "Unit and member performance oversight.",
         "Directorate scorecard against objectives; member ranking with justification; "
         "low-performer action plan; period comparison.",
         "Performance, Objective"),
    ],
    journey=[
        ("Director logs in", "Directorate scorecard and pending approvals"),
        ("Set objectives", "Align with YPDC annual plan"),
        ("Build work plan", "Quarterly lines, owners, milestones"),
        ("Assign work", "Tasks and duty roster to team members"),
        ("Propose event", "Proposal into the approval chain"),
        ("Execute activity", "Checklists, check-in, on-ground coordination"),
        ("Record attendance", "QR / code / manual with reconciliation"),
        ("Submit report", "Activity report with outcomes and media"),
        ("Rate performance", "Member scores, comments, recommendations"),
    ],
    cols=3,
)

PORTALS["faculty"] = dict(
    no="04", title="Faculty Portal",
    subtitle="Academic oversight, endorsement and approval layer between students and administration",
    purpose=(
        "Faculty members act as focal persons and endorsers. They do not run day-to-day "
        "operations; they verify academic legitimacy, approve proposals and recommendations, "
        "monitor student and member activity, and provide structured feedback to both the "
        "directorate and the administration."),
    audience="Faculty focal persons, department heads, faculty advisors.",
    access="Authenticated. Read across assigned directorates; approval and recommendation rights; no user administration.",
    modules=[
        ("Faculty Profile",
         "Academic identity and contact.",
         "Qualification, department, office hours, contact; assigned directorates and student "
         "groups; availability for approvals.",
         "User, Profile, FacultyRole"),
        ("Department / Designation",
         "Institutional position.",
         "Department, designation, tenure; mapping to YPDC scope of oversight; "
         "change notified to Admin for permission recalculation.",
         "FacultyRole"),
        ("YPDC Role",
         "Formal role inside YPDC.",
         "Focal person, advisor, patron or reviewer; scope (which directorates / events); "
         "deputy assignment; term dates.",
         "FacultyRole, Role"),
        ("Events",
         "Events requiring faculty oversight.",
         "Events of assigned directorates with proposal status; faculty comments; "
         "attendance as chief guest / judge; evaluation form after the event.",
         "Event, EventProposal"),
        ("Student / Member Activities",
         "Supervision view of activity records.",
         "Activity feed per student / member; attendance and task summary; risk flags "
         "(low attendance, overdue tasks); intervention note.",
         "Attendance, Task, ActivityReport"),
        ("Approvals",
         "Faculty-level approval queue.",
         "Queue with ageing; approve / return with reason; recommendation for membership, "
         "certificates and awards; bulk actions with per-item remarks.",
         "ApprovalWorkflow, Application"),
        ("Reports",
         "Reports requiring academic review.",
         "Activity and performance reports of assigned units; review comments; "
         "endorsement or rejection back to the directorate.",
         "ActivityReport, Performance"),
        ("Feedback",
         "Structured feedback to members and administration.",
         "Member feedback forms; directorate-level observations; policy suggestions; "
         "visibility control (to admin only / shared with directorate).",
         "Feedback"),
        ("Notifications",
         "Approval and review alerts.",
         "New approval SLA alerts; overdue reminders; report submitted; escalation notices.",
         "Notification"),
    ],
    journey=[
        ("Faculty logs in", "Approval queue with ageing indicators"),
        ("Check profile", "Assigned directorates and YPDC role"),
        ("Monitor activity", "Student and member attendance, tasks, flags"),
        ("Review proposals", "Event proposals and recommendations"),
        ("Approve / return", "Decision with mandatory reason"),
        ("Review reports", "Activity and performance reports"),
        ("Record feedback", "Observations to member and administration"),
    ],
    cols=3,
)

PORTALS["admin"] = dict(
    no="05", title="Admin Portal",
    subtitle="Central control room - users, content, approvals, attendance, certificates, analytics and permissions",
    purpose=(
        "The Admin Portal is the only place where the platform itself is configured and where "
        "cross-portal decisions are finalised. It owns identity, roles and permissions; it is the "
        "final authority in every approval chain; it publishes the public website; and it produces "
        "the analytics on which the executive committee reports."),
    audience="Super admin, admin officers, content managers, data / analytics officers.",
    access="Authenticated with 2FA. Full rights scoped by role and permission set; every action audit-logged.",
    modules=[
        ("Dashboard",
         "Single operational picture.",
         "KPI tiles (members, active events, pending approvals, attendance %, complaints); "
         "trend charts; directorate comparison; alerts and to-do queue.",
         "All (read)"),
        ("User Management",
         "Identity lifecycle for every portal user.",
         "Create / invite / suspend / delete accounts; role assignment; password reset and 2FA "
         "enforcement; bulk import from CSV; last-login and status reports.",
         "User, Role"),
        ("Member Management",
         "Membership lifecycle administration.",
         "Screen and approve applications; issue Member IDs; transfers between directorates; "
         "suspension / restoration with reason; renewal and expiry runs.",
         "Membership, Application, Profile"),
        ("Directorate Management",
         "Structure of the organisation.",
         "Create / merge / retire directorates; appoint directors and assistants; define "
         "mandate and capacity; reassign teams.",
         "Directorate, DirectorateMember"),
        ("Faculty Management",
         "Faculty onboarding and scope.",
         "Register faculty; assign department, designation and YPDC role; map to directorates; "
         "revoke on term end.",
         "User, FacultyRole"),
        ("Events Management",
         "Master event register and approvals.",
         "Approve / reject proposals; publish to public calendar; manage capacity, waitlist and "
         "cancellation; conflict detection on venue and date.",
         "Event, EventProposal"),
        ("Applications &amp; Approvals",
         "Unified approval engine.",
         "Configurable multi-level chains per form type; SLA timers with auto-escalation; "
         "approve / return / delegate; complete decision history.",
         "Application, ApprovalWorkflow"),
        ("Attendance",
         "Attendance governance.",
         "Approve sessions created by directorates; audit anomalies (duplicate, out-of-geo, "
         "late mark); grant condonation; lock periods for reporting.",
         "Attendance, Session"),
        ("Certificates",
         "Certificate authority of the platform.",
         "Design templates; approve auto-drafts; issue with unique serial and QR; revoke with "
         "reason; public verification endpoint.",
         "Certificate"),
        ("Reports &amp; Analytics",
         "Insight for decision-making.",
         "Membership funnel; event ROI (cost vs footfall); attendance heat map; directorate "
         "scorecards; scheduled exports (PDF / Excel) to stakeholders.",
         "All (aggregate)"),
        ("Notifications",
         "Broadcast and system messaging.",
         "Targeted broadcast by role, directorate or cohort; templates; scheduling; "
         "delivery and read analytics.",
         "Notification"),
        ("Website Content",
         "Content management for the public portal.",
         "Pages, news, FAQs, projects, gallery albums; rich editor with media library; "
         "draft / review / publish with reviewer; SEO fields and versioning.",
         "ContentPage, MediaAsset, Album"),
        ("Documents",
         "Central document repository.",
         "Policies, SOPs, forms, minutes; classification (public / member / admin); version "
         "history; access grants and download audit.",
         "Document"),
        ("Feedback / Complaints",
         "Grievance handling.",
         "Triage by category and priority; assignment with SLA; resolution notes; complainant "
         "satisfaction; monthly trend and root-cause report.",
         "Ticket, Feedback"),
        ("Roles &amp; Permissions",
         "Access control configuration.",
         "Define roles and permission sets (module x action); assign to users; segregation-of-duty "
         "rules; permission change audit and periodic access review.",
         "Role, Permission, UserRole"),
    ],
    journey=[
        ("Admin logs in", "KPI dashboard and pending approvals"),
        ("Manage users", "Create, assign roles, enforce 2FA"),
        ("Manage structure", "Directorates, faculty, membership lifecycle"),
        ("Process approvals", "Final authority in every chain"),
        ("Audit attendance", "Anomalies, condonation, period lock"),
        ("Issue certificates", "Approve drafts, serial and QR"),
        ("Publish content", "Public website pages, news, gallery"),
        ("Handle complaints", "Triage, assign, resolve, close"),
        ("Publish analytics", "Executive reports and exports"),
    ],
    cols=3,
)

PORTALS["alumni"] = dict(
    no="06", title="Alumni Portal",
    subtitle="Life after induction - network, mentorship, careers and giving back",
    purpose=(
        "Alumni remain the most valuable asset of YPDC. This portal keeps their profile current, "
        "connects them to each other and to current members through mentorship, routes career and "
        "volunteer opportunities both ways, and records their continued contribution."),
    audience="Graduated members, former office bearers, retired faculty advisors.",
    access="Authenticated. Own profile; network and mentorship by mutual consent; read access to public and alumni events.",
    modules=[
        ("Alumni Profile",
         "Current identity after graduation.",
         "Batch, Member ID retention, contact, city and country; privacy controls per field; "
         "verified alumni badge.",
         "User, Profile, AlumniProfile"),
        ("Academic Information",
         "Academic record preserved.",
         "Institution, programme, graduation year, CGPA (optional), academic achievements; "
         "YPDC tenure and directorates served.",
         "AcademicRecord, Membership"),
        ("Professional Information",
         "Career footprint.",
         "Current organisation, designation, industry, location; employment history; "
         "open-to-opportunity flag; LinkedIn sync (manual).",
         "ProfessionalRecord"),
        ("Skills",
         "Machine-readable expertise.",
         "Skill tags with proficiency level; endorsement by peers; used for mentorship and "
         "volunteer matching.",
         "Skill, AlumniProfile"),
        ("Alumni Network",
         "Directory and community.",
         "Searchable directory (opt-in); batch and city groups; message request with consent; "
         "alumni chapter pages.",
         "AlumniProfile, Network"),
        ("Mentorship",
         "Structured giving back.",
         "Mentor / mentee registration; matching by field, skill and availability; session log; "
         "mid-cycle review; closure with dual feedback.",
         "MentorshipPair, Session"),
        ("Events",
         "Alumni-focused and open events.",
         "Reunions, webinars, talks; alumni-only and open categories; registration and "
         "speaking-interest expression.",
         "Event, Registration"),
        ("Achievements",
         "Professional recognition.",
         "Awards, publications, certifications; YPDC alumni award nominations; consent-based "
         "public showcase.",
         "Achievement"),
        ("Career Opportunities",
         "Two-way job board.",
         "Alumni-posted openings; member applications with referral tag; YPDC internships; "
         "posting moderation by admin.",
         "JobPosting, Application"),
        ("Volunteer / Support Opportunities",
         "Non-financial and financial support.",
         "Guest speaker, judge, trainer, donor and in-kind support requests; commitment "
         "tracking; contribution ledger and appreciation certificate.",
         "VolunteerOpportunity, Contribution"),
    ],
    journey=[
        ("Alumni logs in", "Profile status and network highlights"),
        ("Update profile", "Professional and skill information"),
        ("Join network", "Opt-in directory, batch and city groups"),
        ("Give mentorship", "Register as mentor, accept a match"),
        ("Post opportunity", "Job or volunteer / support request"),
        ("Attend events", "Reunions, webinars, talks"),
        ("Get recognised", "Contribution ledger and appreciation"),
    ],
    cols=3,
)


# ========================================================================== #
#  CROSS-PORTAL WORKFLOWS
# ========================================================================== #
WF_ONBOARD = [
    ("start", "Application submitted", "Guest Portal \u2192 Membership or Volunteer Registration form is completed, documents uploaded and consent recorded. A reference ID is issued instantly."),
    ("step", "Completeness check (Admin)", "Automated validation of mandatory fields and readable documents; incomplete applications are returned to the applicant with the exact missing items."),
    ("decision", "Application complete?", None),
    ("no", "Returned to applicant", "Status set to 'Incomplete'; applicant notified by e-mail/SMS with a resubmission link. Auto-close after 14 days of no action."),
    ("yes", "Screening scheduled", "Application routed to the screening committee (Director + Faculty focal person) with a scheduled date."),
    ("step", "Screening / merit evaluation", "Committee assesses eligibility criteria, conducts interview or test where required, and records remarks against each criterion."),
    ("decision", "Recommendation", None),
    ("no", "Declined with reason", "Standard reason code plus free-text remark; applicant informed politely; may reapply after the defined cooling period."),
    ("yes", "Final approval (Admin)", "Admin verifies the recommendation, checks quota and duplicate membership, and approves."),
    ("step", "Member ID generated", "ID issued in the format YPDC-YYYY-DIR-NNNN, digital QR card created, directorate allocation confirmed."),
    ("step", "Induction & portal provisioning", "Welcome notification, portal credentials, responsibilities acceptance and orientation event invite."),
    ("end", "Active membership", "Record visible in Member Portal, directorate roster and admin analytics from this point onward."),
]

WF_EVENT = [
    ("start", "Event proposal raised", "Directorate Portal \u2192 Event Proposals: title, rationale, objectives, target audience, date, venue, budget, risk and checklist attached."),
    ("step", "Assistant Director review", "Operational feasibility, team availability and budget sanity check; may edit or return to the proposer."),
    ("step", "Director endorsement", "Strategic fit with directorate objectives; endorses or returns with remarks."),
    ("step", "Faculty focal person review", "Academic legitimacy, speaker suitability and compliance with institutional policy."),
    ("step", "Admin final approval", "Budget sanction, venue and date conflict check, security and permissions, publication decision."),
    ("decision", "Approved?", None),
    ("no", "Returned / rejected", "Decision with reason recorded at every level; proposer may revise and resubmit; full audit trail retained."),
    ("yes", "Event published", "Appears in the Guest Portal calendar and in Student/Member/Alumni event lists with eligibility rules."),
    ("parallel", "Parallel execution tracks", [
        "Registration & ticketing \u2014 seats, waitlist, QR e-pass, reminders",
        "Volunteer mobilisation \u2014 open call, screening, shift allocation, briefing",
        "Logistics & media \u2014 venue, equipment, coverage plan, guest handling",
    ]),
    ("step", "Event execution & attendance", "Check-in by QR, geo-fence, offline code or manual list; real-time headcount on the directorate dashboard."),
    ("step", "Post-event activity report", "Directorate submits summary, footfall, outcomes, budget used, media links and lessons learned within the defined SLA."),
    ("step", "Certificates & recognition", "Rule-based certificates issued to participants and volunteers; merit certificates on director recommendation and admin approval."),
    ("end", "Analytics & public archive", "Metrics pushed to Admin Reports & Analytics; approved content published to News, Gallery and Achievements."),
]

WF_APPROVAL = [
    ("start", "Initiator submits form", "Any portal: membership application, event proposal, certificate recommendation, leave/condonation, complaint, budget request."),
    ("step", "Validation & duplicate control", "Mandatory fields, attachments, eligibility rules and duplicate detection run before the request enters the chain."),
    ("step", "Approval chain resolved", "Engine reads the configured chain for the form type (levels, approvers, thresholds, SLA hours) and creates the first task."),
    ("step", "Level n review", "Approver sees the complete packet: form, attachments, history, prior remarks and any analytics relevant to the decision."),
    ("decision", "Decision at this level", None),
    ("yes", "Escalate to next level", "Moves to level n+1 with cumulative remarks; parallel approval where the chain is configured as joint."),
    ("no", "Return to initiator", "Reason code plus remark are mandatory; initiator may revise and resubmit, which restarts the chain."),
    ("parallel", "Terminal outcomes", [
        "Approved \u2014 downstream actions trigger automatically (ID issue, publication, certificate, payment)",
        "Deferred \u2014 parked with a review date and an owner",
        "Rejected \u2014 closed with reason; appeal window defined",
    ]),
    ("step", "Notification & audit", "Initiator and stakeholders notified; complete decision history stored immutably in the audit log."),
    ("end", "SLA governance", "Ageing tracked per level; auto-escalation and delegation on timeout; monthly SLA compliance report to the executive committee."),
]

WF_ATTEND = [
    ("start", "Session created", "Directorate creates a session for an event, meeting or duty with date, venue, expected participants and marking method."),
    ("step", "Check-in channels", "QR scan, geo-fenced self-mark with photo, offline numeric code, or manual marking by the duty officer."),
    ("step", "Attendance recorded", "Status set to Present / Late / Absent / Excused with timestamp, device, geo coordinates and marker identity."),
    ("step", "Reconciliation", "Duplicate, out-of-geo and after-window marks are flagged; the directorate confirms or corrects before lock."),
    ("step", "Admin audit & lock", "Admin samples anomalies, grants condonation on evidence, then locks the period for reporting."),
    ("decision", "Threshold met?", None),
    ("no", "Deficiency notice", "Member notified with the shortfall; condonation or make-up route offered; repeated shortfall affects performance and eligibility."),
    ("yes", "Eligibility established", "Attendance qualifies the member for certificates, awards and event eligibility rules."),
    ("end", "Feeds performance & certificates", "Weighted into the performance score and evaluated by the certificate rules engine."),
]

WF_VOLUNTEER = [
    ("start", "Public volunteer registration", "Guest Portal form captures personal details, skills, availability and interests with consent; a reference ID is issued."),
    ("step", "Admin screening", "Profile verification, duplicate check and skill validation; volunteer is placed in the talent pool with tags."),
    ("step", "Opportunity matching", "Open calls are matched by skill, availability and location; the volunteer sees a match score and applies."),
    ("step", "Selection & assignment", "Directorate shortlists, assigns role and shift; the volunteer accepts or declines within the response window."),
    ("step", "Briefing & deployment", "Pre-event briefing (in person or online), duty card issued, reporting officer named."),
    ("step", "Service recorded", "Attendance at duty, hours served and a duty report are logged against the volunteer's ledger."),
    ("step", "Feedback & appreciation", "Performance feedback from the duty officer; appreciation certificate and service-hours statement issued."),
    ("end", "Talent pool update", "Skills and reliability rating updated; high performers are invited to membership or leadership tracks."),
]

WF_COMPLAINT = [
    ("start", "Complaint received", "Any portal Feedback module or the public Contact Us form; optional anonymity is respected throughout."),
    ("step", "Triage (Admin)", "Categorised (harassment, event, service, academic, other), priority assigned (P1-P4) and an owner designated."),
    ("decision", "Priority P1 (sensitive / urgent)?", None),
    ("yes", "Immediate escalation", "Escalated to the grievance committee and patron within the defined hours; interim protective measures recorded."),
    ("no", "Standard routing", "Routed to the concerned directorate or faculty focal person with an SLA clock."),
    ("step", "Investigation", "Facts gathered, statements recorded, evidence attached; both sides heard where applicable."),
    ("step", "Resolution recorded", "Action taken, corrective measure and prevention step documented against the ticket."),
    ("step", "Complainant informed & satisfaction captured", "Outcome communicated; complainant rates the handling."),
    ("decision", "Satisfied?", None),
    ("no", "Escalate to higher authority", "Reopened at a higher level with the previous record visible; final decision is binding."),
    ("yes", "Closed", "Ticket closed; anonymised data added to the monthly trend and root-cause analysis report."),
]

WF_MENTOR = [
    ("start", "Request raised", "Member submits a mentorship request with field, goals, preferred frequency and duration."),
    ("step", "Mentor pool matching", "System matches alumni mentors by industry, skill, experience and availability; top candidates are proposed."),
    ("step", "Mutual acceptance", "Mentor accepts or declines; on decline the next candidate is offered; both sides confirm commitment."),
    ("step", "Pair created & plan agreed", "Pair record created with term, meeting cadence, goals and confidentiality acknowledgement."),
    ("step", "Sessions delivered & logged", "Each session is logged with date, duration, topics and next actions."),
    ("step", "Mid-cycle review", "Progress against goals reviewed; pair may adjust the plan or request re-matching."),
    ("step", "Closure with dual feedback", "Both mentor and mentee submit feedback; outcomes and testimonials recorded with consent."),
    ("end", "Contribution recorded", "Mentor hours credited in the alumni contribution ledger; appreciation certificate issued."),
]

WF_CERT = [
    ("start", "Trigger event", "Event completion, duty fulfilment, attendance threshold, training completion or merit decision."),
    ("step", "Rules engine evaluation", "Certificate rules (criteria, template, validity, signatories) evaluated against verified records."),
    ("step", "Draft generated", "Auto-draft created with member details, event, date and a pending serial number."),
    ("step", "Recommendation & approval", "Director recommends for merit certificates; Admin approves and confirms signatories."),
    ("step", "Issued with serial & QR", "Unique serial issued, QR verification code embedded, PDF generated and stored."),
    ("step", "Delivered & notified", "Certificate appears in the member's Certificates module; e-mail notification with verification link."),
    ("end", "Public verification", "Any third party can verify authenticity, holder and issue date through the public verification endpoint; revocation reflected immediately."),
]

WF_PERF = [
    ("start", "Objectives set", "Directorate defines SMART objectives aligned to the YPDC annual plan, with owners and target values."),
    ("step", "Work plan & task delegation", "Objectives broken into quarterly plan lines and assigned as tasks with deadlines and evidence requirements."),
    ("step", "Execution & evidence capture", "Members update progress, attach evidence, attend events and duties; attendance is marked."),
    ("step", "Data aggregation", "Tasks (40%), attendance (25%), event participation (20%) and conduct (15%) are aggregated per period."),
    ("step", "Director review", "Director validates scores, adds qualitative comments and adjusts with a recorded justification."),
    ("step", "Published to member", "Member sees the score, components and comments in the Member Portal."),
    ("decision", "Member appeal within 7 days?", None),
    ("yes", "Review committee", "Faculty plus Admin review the appeal; outcome recorded and score corrected if required."),
    ("no", "Score confirmed", "Score locked for the period and fed into awards, eligibility and the directorate scorecard."),
    ("end", "Executive reporting", "Aggregate performance analytics published to the Admin dashboard and periodic executive report."),
]


# ========================================================================== #
#  BUILD (part 1)
# ========================================================================== #
def build_part1(sec):
    F = []
    fw = R.FRAME_W

    # ---------------- Document control ---------------------------------- #
    F.append(sec.h1("Document Control", numbered=False))
    F.append(Spacer(1, 4))
    F.append(R.make_table(
        ["Attribute", "Detail", "Attribute", "Detail"],
        [
            ["Document title", "YPDC Website &amp; Portal System \u2014 Workflow Specification Report",
             "Document ID", "YPDC-DOC-WF-001"],
            ["Version", "1.0 \u2014 Draft for Approval", "Status", "For review by Executive Committee"],
            ["Date of issue", R.date.today().strftime("%d %B %Y"), "Classification", "Internal / Planning Use"],
            ["Prepared by", "YPDC Digital Secretariat", "Reviewed by", "Faculty Focal Persons / Directors"],
            ["Approved by", "Executive Committee (pending)", "Next review", "On approval, then quarterly"],
        ],
        [fw * 0.16, fw * 0.34, fw * 0.16, fw * 0.34], font_small=True))
    F.append(Spacer(1, 10))

    F.append(Paragraph("Revision history", R.H3))
    F.append(R.make_table(
        ["Version", "Date", "Author", "Summary of change"],
        [["0.1", "\u2014", "Digital Secretariat", "Portal list captured from stakeholder input (7 portals)."],
         ["0.9", "\u2014", "Digital Secretariat", "Module inventory, workflows and access matrix drafted."],
         ["1.0", R.date.today().strftime("%d %b %Y"), "Digital Secretariat",
          "Complete workflow specification issued for approval."]],
        [fw * 0.10, fw * 0.16, fw * 0.24, fw * 0.50], font_small=True))
    F.append(Spacer(1, 10))

    F.append(Paragraph("Approvals", R.H3))
    F.append(R.make_table(
        ["Role", "Name", "Purpose of approval", "Signature / date"],
        [["Project Sponsor", "", "Scope and budget acceptance", ""],
         ["Chairperson, YPDC", "", "Organisational acceptance", ""],
         ["Faculty Focal Person", "", "Academic and policy acceptance", ""],
         ["Technical Lead", "", "Feasibility and delivery plan acceptance", ""]],
        [fw * 0.22, fw * 0.24, fw * 0.34, fw * 0.20], font_small=True))
    F.append(Spacer(1, 8))
    F.append(R.callout(
        "Note on the name \u201cYPDC\u201d",
        "This document uses the abbreviation <b>YPDC</b> throughout. The full legal name is to be "
        "confirmed by the Executive Committee and substituted globally before external circulation.",
        "warn"))
    F.append(PageBreak())

    # ---------------- Table of contents --------------------------------- #
    F.append(Paragraph("Table of Contents", R.H1))
    F.append(Spacer(1, 6))
    toc = R.TableOfContents()
    toc.levelStyles = [
        R.ParagraphStyle(name="toc0", fontName=R.FONT_B, fontSize=9.6, leading=15,
                         textColor=R.NAVY, leftIndent=0, firstLineIndent=-16, spaceBefore=5),
        R.ParagraphStyle(name="toc1", fontName=R.FONT, fontSize=8.8, leading=13,
                         textColor=colors.HexColor("#3A4C5E"), leftIndent=18, firstLineIndent=-12),
    ]
    toc.dotsMinLevel = 0
    F.append(toc)
    F.append(PageBreak())

    # ---------------- Executive summary --------------------------------- #
    F.append(sec.h1("Executive Summary", numbered=False))
    F.append(Spacer(1, 4))
    F.append(R.para(
        "YPDC currently runs its activities \u2014 membership, directorates, events, attendance, "
        "reporting and recognition \u2014 through a mixture of registers, spreadsheets, messaging "
        "groups and paper approvals. Information about a single member is therefore scattered, "
        "attendance is difficult to verify, approvals move at the speed of whoever is available, "
        "and the executive committee has no reliable data on which to plan.", R.LEAD))
    F.append(R.para(
        "This specification defines a single web platform organised into <b>seven portals</b>, one "
        "for each audience: <b>Guest/Public</b>, <b>Student</b>, <b>Member</b>, <b>Directorate</b>, "
        "<b>Faculty</b>, <b>Admin</b> and <b>Alumni</b>. The seven portals share one database, one "
        "identity system and one approval engine; they differ only in what a user may see and do. "
        "Together they cover <b>81 modules</b> and <b>11 documented end-to-end workflows</b>."))
    F.append(Spacer(1, 3))

    F.append(Paragraph("What this report delivers", R.H3))
    F.extend(R.bullets([
        "<b>A complete module inventory</b> \u2014 all 81 modules grouped by portal, each with its purpose, key functions and the data it owns.",
        "<b>End-to-end workflows</b> \u2014 step-by-step flows for onboarding, event lifecycle, approvals, attendance, volunteer management, certificates, performance, complaints and mentorship.",
        "<b>A role-based access model</b> \u2014 who can create, read, update, approve and delete in every module group.",
        "<b>A data model outline</b> \u2014 the 25 core entities that all portals read from and write to.",
        "<b>A phased delivery roadmap</b> \u2014 six phases from foundation to optimisation, with acceptance criteria.",
        "<b>Risks, assumptions and open decisions</b> that require an Executive Committee decision before development starts.",
    ]))
    F.append(Spacer(1, 4))

    F.append(Paragraph("The seven portals at a glance", R.H3))
    F.append(R.make_table(
        ["#", "Portal", "Primary users", "Modules", "Core value delivered"],
        [["07", "Guest / Public", "Public, applicants, media, recruiters", "14",
          "Credibility, discovery and a single entry point for applications"],
         ["01", "Student", "Enrolled students, prospective members", "10",
          "Low-friction participation, attendance and early recognition"],
         ["02", "Member", "Inducted members, team leads", "10",
          "Task execution, duty record, performance visibility"],
         ["03", "Directorate", "Directors, assistant directors", "13",
          "Planning, delegation, execution and evidence of work"],
         ["04", "Faculty", "Focal persons, advisors", "9",
          "Academic oversight, endorsement and approval"],
         ["05", "Admin", "Admin officers, content and data officers", "15",
          "Control room: identity, approvals, content, analytics"],
         ["06", "Alumni", "Graduated members, mentors", "10",
          "Network, mentorship, careers and continued contribution"],
         ["", "<b>Total</b>", "", "<b>81</b>", ""]],
        [fw * 0.05, fw * 0.14, fw * 0.24, fw * 0.08, fw * 0.49],
        aligns=["C", "L", "L", "C", "L"], font_small=True))
    F.append(Spacer(1, 8))

    F.append(R.callout(
        "Decisions required from the Executive Committee",
        ["1. Confirm the full legal name of <b>YPDC</b> for the cover page and all templates.",
         "2. Approve the role and permission matrix in Section 5, particularly who holds final approval authority.",
         "3. Confirm the attendance verification method to be used on the ground (QR, geo-fence, offline code or manual).",
         "4. Approve the performance weighting (tasks 40% / attendance 25% / events 20% / conduct 15%).",
         "5. Confirm budget, hosting preference and the target launch date for Phase 2."],
        "info"))
    F.append(PageBreak())

    # ---------------- 1. Overview --------------------------------------- #
    F.append(sec.h1("Introduction &amp; Project Overview"))
    F.append(sec.h2("Background"))
    F.append(R.para(
        "YPDC operates through directorates, each led by a director and supported by faculty "
        "focal persons, with students progressing into full membership and, after graduation, "
        "into an alumni body. Every layer generates records \u2014 who joined, who attended, what "
        "was delivered, who performed well \u2014 but none of these records currently live in one "
        "place."))
    F.append(R.para(
        "The consequence is operational rather than cosmetic. Membership lists are reconciled by "
        "hand before every certificate run. Attendance disputes cannot be settled because the "
        "marking method leaves no evidence. An event proposal can sit with a single approver for "
        "weeks with no visibility for anyone else. And when the executive committee asks how many "
        "activities a directorate delivered last quarter, the answer has to be assembled manually."))
    F.append(R.para(
        "A single platform with role-scoped portals removes all of these frictions at once, "
        "because the same record that a member updates is the record a director reviews, a faculty "
        "member endorses and an administrator reports on."))

    F.append(sec.h2("Objectives"))
    F.append(R.make_table(
        ["#", "Objective", "How the platform achieves it", "Measure of success"],
        [["O1", "One trusted record per person",
          "A single identity across all seven portals, with a verified profile and a permanent Member ID.",
          "Zero duplicate member records at annual audit"],
         ["O2", "Faster, transparent approvals",
          "A configurable multi-level approval engine with SLA timers and auto-escalation.",
          "Average approval cycle time reduced to under 5 working days"],
         ["O3", "Verifiable attendance",
          "Session-based marking with method, timestamp, geo and marker identity; reconciliation before lock.",
          "Attendance disputes resolved from system evidence in under 48 hours"],
         ["O4", "Evidence-based performance",
          "Objective, task, attendance and event data aggregated into a published, appealable score.",
          "100% of members able to see their score and its components"],
         ["O5", "Professional public presence",
          "A CMS-driven public portal for content, events, gallery, publications and applications.",
          "All content published by the admin team without developer involvement"],
         ["O6", "Recognition at scale",
          "Rule-based certificate issuance with unique serials and public QR verification.",
          "Certificates issued within one working day of activity closure"],
         ["O7", "Data for decisions",
          "Analytics on membership funnel, event outcomes, attendance and complaints.",
          "Quarterly executive report generated from the system without manual collation"],
         ["O8", "Lifelong relationship",
          "An alumni portal for network, mentorship, careers and continued contribution.",
          "Active mentorship pairs and alumni-posted opportunities each quarter"]],
        [fw * 0.05, fw * 0.22, fw * 0.44, fw * 0.29],
        aligns=["C", "L", "L", "L"], font_small=True))
    F.append(Spacer(1, 6))

    F.append(sec.h2("Scope"))
    F.append(Paragraph("In scope", R.H3))
    F.extend(R.bullets([
        "Seven role-based portals sharing one database, one authentication service and one approval engine.",
        "The 81 functional modules inventoried in Section 8, including their workflows and data.",
        "Cross-portal workflows: onboarding, event lifecycle, approvals, attendance, volunteering, certificates, performance, complaints and mentorship.",
        "The role and permission model, audit logging, notifications and public certificate verification.",
        "Content management for the public website, including news, gallery, publications and FAQs.",
    ]))
    F.append(Paragraph("Out of scope (for this phase)", R.H3))
    F.extend(R.bullets([
        "Native mobile applications \u2014 the platform is responsive web first; native apps may follow once the workflow is stable.",
        "Full accounting and payroll systems \u2014 only budget capture and utilisation against events are in scope.",
        "Academic result management of the host institution \u2014 academic data is stored for context only.",
        "Biometric attendance hardware integration \u2014 the data model allows it, but no hardware is procured in this phase.",
        "Payment gateway integration \u2014 membership fees are recorded as paid/unpaid; online collection is a later phase.",
    ]))
    F.append(Spacer(1, 4))

    F.append(sec.h2("Key stakeholders"))
    F.append(R.make_table(
        ["Stakeholder", "Interest", "Primary portal", "What they need from this project"],
        [["Executive Committee / Patron", "Governance, reputation, assurance", "Admin (reports)",
          "Reliable reports, control over approvals and risk visibility"],
         ["Directors &amp; Assistant Directors", "Delivery of directorate objectives", "Directorate",
          "Planning, delegation and evidence with minimal paperwork"],
         ["Faculty focal persons", "Academic legitimacy and student welfare", "Faculty",
          "A light approval queue with full context, and oversight flags"],
         ["Members &amp; students", "Participation, recognition, growth", "Member / Student",
          "Clarity on duties, fair attendance and timely certificates"],
         ["Admin team", "Day-to-day operation of the platform", "Admin",
          "Control over users, content and approvals without developer help"],
         ["Alumni", "Connection, mentorship, giving back", "Alumni",
          "A current network and simple ways to contribute"],
         ["Public &amp; media", "Transparency and information", "Guest",
          "Accurate public information and easy application routes"]],
        [fw * 0.22, fw * 0.22, fw * 0.14, fw * 0.42], font_small=True))
    F.append(PageBreak())

    # ---------------- 2. Portal architecture ---------------------------- #
    F.append(sec.h1("Platform Architecture &amp; Portal Model"))
    F.append(sec.h2("One platform, seven views"))
    F.append(R.para(
        "The seven portals are <b>not seven systems</b>. They are seven permission-filtered views "
        "over a single data store. A record written by a member in the Member Portal is instantly "
        "visible \u2014 subject to permission \u2014 in the Directorate, Faculty, Admin and Alumni "
        "views. This single-source-of-truth design is what makes approvals fast, attendance "
        "verifiable and reporting automatic."))
    F.append(Spacer(1, 2))
    F.append(R.make_table(
        ["Layer", "Responsibility", "Key components", "Notes"],
        [["1. Presentation",
          "What each audience sees and can do",
          "Seven portal shells (public site + six authenticated workspaces), responsive layouts, "
          "role-driven navigation and dashboards",
          "One codebase; the portal rendered is decided by the user's roles at login"],
         ["2. Application / API",
          "Business rules and workflow orchestration",
          "AuthN/AuthZ service, approval engine, certificate rules engine, attendance service, "
          "notification service, CMS, analytics",
          "All portals call the same API; no portal owns private logic"],
         ["3. Data",
          "The single source of truth",
          "Relational store for the 25 core entities, object storage for files and media, "
          "audit log store, cache",
          "Soft delete and full history on every regulated entity"],
         ["4. Infrastructure",
          "Availability, security and delivery",
          "HTTPS everywhere, automated backup, CI/CD pipeline, monitoring and alerting, "
          "staging and production environments",
          "Hosting decision required \u2014 see Section 16, open items"]],
        [fw * 0.14, fw * 0.22, fw * 0.38, fw * 0.26], font_small=True))
    F.append(Spacer(1, 8))

    F.append(sec.h2("Shared platform services"))
    F.append(R.para(
        "Eight services are used by every portal. Building them once, centrally, is what prevents "
        "the seven portals from drifting into seven inconsistent experiences."))
    F.append(R.make_table(
        ["Service", "What it does", "Used by"],
        [["Identity &amp; authentication",
          "Single account per person; login by e-mail or Member ID with OTP/password; optional 2FA for staff roles; session and device management.",
          "All authenticated portals"],
         ["Authorisation (roles &amp; permissions)",
          "Module \u00d7 action permission sets attached to roles; evaluated on every request and used to render navigation.",
          "All portals"],
         ["Approval engine",
          "Configurable multi-level chains, SLA timers, auto-escalation, delegation and immutable decision history.",
          "Student, Member, Directorate, Faculty, Admin, Alumni"],
         ["Notification service",
          "In-app, e-mail and SMS delivery from templates; per-user preferences; digest and scheduling; delivery analytics.",
          "All portals"],
         ["Attendance service",
          "Session creation, multi-channel marking, anomaly detection, reconciliation, condonation and period lock.",
          "Student, Member, Directorate, Admin"],
         ["Certificate engine",
          "Rule evaluation, template rendering, unique serial and QR generation, issuance, revocation and public verification.",
          "Student, Member, Directorate, Admin, Alumni"],
         ["Content management (CMS)",
          "Pages, news, FAQs, projects, gallery albums and publications with draft \u2192 review \u2192 publish and versioning.",
          "Admin writes; Guest reads"],
         ["Audit &amp; analytics",
          "Immutable audit log of regulated actions; KPI computation; dashboards and scheduled exports.",
          "Admin primarily; scoped views elsewhere"]],
        [fw * 0.20, fw * 0.55, fw * 0.25], font_small=True))
    F.append(Spacer(1, 8))

    F.append(sec.h2("How the portals relate"))
    F.append(R.para(
        "The diagram below shows the flow of people and records between portals. Everything on the "
        "left enters through the public surface; everything on the right is governed centrally."))
    F.append(R.figure(
        R.ChevronFlow([
            ("Guest / Public", "Discovery, applications, volunteering, contact"),
            ("Student", "Participation, attendance, early recognition"),
            ("Member", "Duties, tasks, reports, performance"),
            ("Directorate", "Planning, delegation, execution, evidence"),
            ("Faculty", "Oversight, endorsement, approval"),
            ("Admin", "Identity, approvals, content, certificates, analytics"),
            ("Alumni", "Network, mentorship, careers, giving back"),
        ], cols=4),
        "Figure 1 \u2014 Portal progression: a visitor becomes a student, a member, a contributor, "
        "and eventually an alumnus, while the Directorate, Faculty and Admin portals govern the "
        "journey throughout."))

    F.append(sec.h2("Module inventory summary"))
    F.append(R.make_table(
        ["Portal", "Modules", "Modules that write data", "Modules that primarily approve / review",
         "Depends on approval engine"],
        [["Guest / Public", "14", "4 (forms, contact, FAQ vote)", "0", "Yes \u2014 applications"],
         ["Student", "10", "6", "0", "Yes \u2014 membership, complaints"],
         ["Member", "10", "7", "0", "Yes \u2014 condonation, certificates"],
         ["Directorate", "13", "11", "2 (attendance, activity reports)", "Yes \u2014 event proposals"],
         ["Faculty", "9", "1 (feedback)", "6", "Yes \u2014 approvals module"],
         ["Admin", "15", "13", "10", "Yes \u2014 final authority"],
         ["Alumni", "10", "8", "0", "Yes \u2014 mentorship, postings"],
         ["<b>Total</b>", "<b>81</b>", "<b>50</b>", "<b>18</b>", ""]],
        [fw * 0.19, fw * 0.10, fw * 0.22, fw * 0.28, fw * 0.21],
        aligns=["L", "C", "L", "L", "L"], font_small=True))
    F.append(PageBreak())

    return F


# ========================================================================== #
#  BUILD (part 2) - roles, permissions, cross-portal workflows
# ========================================================================== #
def build_part2(sec):
    F = []
    fw = R.FRAME_W

    # ---------------- 3. Roles & access --------------------------------- #
    F.append(sec.h1("User Roles &amp; Access Model"))
    F.append(sec.h2("Role definitions"))
    F.append(R.para(
        "A <b>role</b> is a bundle of permissions (module \u00d7 action). A user may hold several "
        "roles at once \u2014 for example a member who is also a team lead, or a faculty member "
        "who is also an alumni. The portal shown after login is determined by the user's highest "
        "privilege role, with a portal switcher available where multiple apply."))
    F.append(R.make_table(
        ["Role", "Who holds it", "Portal", "Scope of data visible", "Cannot do"],
        [["Guest", "Any public visitor", "Guest / Public",
          "Published content only", "See any member personal data"],
         ["Student", "Enrolled student / prospective member", "Student",
          "Own records; public events", "Approve anything; see other students' records"],
         ["Member", "Inducted member with Member ID", "Member",
          "Own records; own directorate's public plan and roster", "Edit objectives or work plan"],
         ["Team Lead", "Member with a sub-team", "Member + Directorate (limited)",
          "Own sub-team's tasks and attendance", "Approve event proposals or certificates"],
         ["Assistant Director", "Deputy head of a directorate", "Directorate",
          "Own directorate", "Final approval on budget and policy"],
         ["Director", "Head of a directorate", "Directorate",
          "Own directorate, full", "Manage users outside the directorate; change permissions"],
         ["Faculty", "Focal person / advisor", "Faculty",
          "Assigned directorates and student groups", "Administer users, roles or website content"],
         ["Alumni", "Graduated member", "Alumni",
          "Own profile; opted-in network", "See current members' private records"],
         ["Admin Officer", "Operations staff", "Admin",
          "All records", "Change own permission set (segregation of duty)"],
         ["Content Manager", "Communications team", "Admin (content modules)",
          "Content, media, publications", "Approve membership or edit users"],
         ["Super Admin", "Technical / secretariat head", "Admin (full)",
          "Everything including roles and audit log", "\u2014 (all actions are still audit-logged)"]],
        [fw * 0.15, fw * 0.20, fw * 0.15, fw * 0.26, fw * 0.24], font_small=True))
    F.append(Spacer(1, 8))

    F.append(sec.h2("Permission matrix"))
    F.append(R.para(
        "The matrix below is the authoritative summary of access rights. It is implemented as "
        "permission sets in the Admin Portal (Roles &amp; Permissions module) and enforced on every "
        "API request \u2014 not merely hidden in the user interface."))
    legend = ("<b>Legend:</b> &nbsp; &#9679; full rights (create / update / delete) &nbsp;&nbsp; "
              "&#9675; own or scoped records only &nbsp;&nbsp; &#9650; review / approve only "
              "&nbsp;&nbsp; &#8211; no access")
    F.append(Paragraph(legend, R.NOTE))
    F.append(Spacer(1, 3))
    hdr = ["Module group", "Guest", "Student", "Member", "A/D", "Director", "Faculty", "Admin", "Alumni"]
    matrix = [
        ["Public website content", "&#8211;", "R", "R", "R", "R", "R", "&#9679;", "R"],
        ["Applications (membership / volunteer)", "&#9679; own", "&#9679; own", "&#8211;", "&#9650;", "&#9650;", "&#9650;", "&#9679;", "&#8211;"],
        ["Own profile", "&#8211;", "&#9679;", "&#9679;", "&#9679;", "&#9679;", "&#9679;", "&#9679;", "&#9679;"],
        ["Other users' profiles", "&#8211;", "&#8211;", "&#9675; roster", "&#9675; unit", "&#9675; unit", "&#9675; assigned", "&#9679;", "&#9675; opted-in"],
        ["Membership lifecycle", "&#8211;", "&#9675;", "&#9675;", "&#9650;", "&#9650;", "&#9650;", "&#9679;", "&#8211;"],
        ["Directorate profile &amp; structure", "R", "R", "R", "&#9675;", "&#9679;", "R", "&#9679;", "R"],
        ["Objectives &amp; work plan", "&#8211;", "&#8211;", "R", "&#9675;", "&#9679;", "&#9650;", "&#9679;", "&#8211;"],
        ["Tasks", "&#8211;", "&#8211;", "&#9675;", "&#9675;", "&#9679;", "R", "&#9679;", "&#8211;"],
        ["Events &amp; activities", "R", "R", "R", "&#9675;", "&#9679;", "&#9650;", "&#9679;", "R"],
        ["Event proposals", "&#8211;", "&#8211;", "&#9675;", "&#9650;", "&#9679;", "&#9650;", "&#9679;", "&#8211;"],
        ["Registrations &amp; duty roster", "&#9679; own", "&#9679; own", "&#9679; own", "&#9679; unit", "&#9679; unit", "R", "&#9679;", "&#9679; own"],
        ["Attendance", "&#8211;", "&#9675;", "&#9675;", "&#9679; unit", "&#9679; unit", "R", "&#9679; audit", "&#8211;"],
        ["Activity reports", "&#8211;", "&#8211;", "&#9679; own", "&#9650;", "&#9650;", "&#9650;", "&#9679;", "&#8211;"],
        ["Certificates", "&#9650; verify", "&#9675;", "&#9675;", "&#9650; recommend", "&#9650; recommend", "&#9650;", "&#9679; issue", "&#9675;"],
        ["Performance", "&#8211;", "R rules", "&#9675;", "&#9679; unit", "&#9679; unit", "&#9650;", "&#9679;", "&#8211;"],
        ["Approvals queue", "&#8211;", "&#8211;", "&#8211;", "&#9650;", "&#9650;", "&#9650;", "&#9679;", "&#8211;"],
        ["Feedback &amp; complaints", "&#9679; raise", "&#9679; raise", "&#9679; raise", "&#9675; resolve", "&#9675; resolve", "&#9675; review", "&#9679; triage", "&#9679; raise"],
        ["User, role &amp; permission admin", "&#8211;", "&#8211;", "&#8211;", "&#8211;", "&#8211;", "&#8211;", "&#9679;", "&#8211;"],
        ["Reports &amp; analytics", "&#8211;", "&#8211;", "&#9675; own", "&#9675; unit", "&#9675; unit", "&#9675; assigned", "&#9679;", "&#8211;"],
        ["Alumni network &amp; mentorship", "&#8211;", "&#8211;", "&#9675; mentee", "&#8211;", "&#8211;", "R", "&#9679;", "&#9679; mentor"],
    ]
    F.append(R.make_table(hdr, matrix,
                          [fw * 0.265] + [fw * 0.0919] * 7,
                          aligns=["L"] + ["C"] * 7, font_small=True))
    F.append(Spacer(1, 6))
    F.append(R.callout(
        "Two rules that must never be relaxed",
        ["<b>Segregation of duty:</b> no user may approve a request they initiated, and no user may "
         "modify their own permission set. Both are enforced server-side.",
         "<b>Least privilege by default:</b> every new account starts with read access to its own "
         "records only. Additional rights are granted explicitly and reviewed each term."],
        "risk"))
    F.append(PageBreak())

    # ---------------- 4. Cross-portal workflows ------------------------- #
    F.append(sec.h1("Core End-to-End Workflows"))
    F.append(R.para(
        "This section documents the eleven workflows that cross portal boundaries. Each is written "
        "as it will be implemented: the trigger, every step, every decision point, both outcomes of "
        "each decision, and the record that is created. Sections 8.1 to 8.7 then describe the "
        "internal journey within each individual portal.", R.LEAD))
    F.append(Spacer(1, 4))
    F.append(R.make_table(
        ["#", "Workflow", "Triggered by", "Portals involved", "Primary owner"],
        [["W1", "Membership / volunteer onboarding", "Public application form", "Guest, Admin, Faculty, Directorate, Member", "Admin"],
         ["W2", "Event lifecycle", "Directorate event proposal", "Directorate, Faculty, Admin, Student, Member, Guest, Alumni", "Director"],
         ["W3", "Generic approval engine", "Any submitted form", "All authenticated portals", "Admin"],
         ["W4", "Attendance capture to certificate", "Session creation", "Directorate, Admin, Student, Member", "Director"],
         ["W5", "Volunteer registration to recognition", "Public volunteer form", "Guest, Admin, Directorate, Member", "Admin"],
         ["W6", "Feedback &amp; complaint handling", "Feedback / contact submission", "All portals, Admin", "Admin"],
         ["W7", "Alumni mentorship cycle", "Mentorship request", "Member, Alumni, Admin", "Alumni lead"],
         ["W8", "Certificate issuance &amp; verification", "Achievement trigger", "Directorate, Admin, Member, Student, Guest", "Admin"],
         ["W9", "Performance management cycle", "Period start (monthly / quarterly)", "Directorate, Member, Faculty, Admin", "Director"],
         ["W10", "Content publication to public site", "Content created by admin", "Admin, Guest", "Content Manager"],
         ["W11", "Notification &amp; communication flow", "Any system or human event", "All portals", "Admin"]],
        [fw * 0.05, fw * 0.25, fw * 0.19, fw * 0.34, fw * 0.17],
        aligns=["C", "L", "L", "L", "L"], font_small=True))
    F.append(Spacer(1, 8))

    F.append(sec.h2("W1 \u2014 Membership &amp; volunteer onboarding"))
    F.append(R.para(
        "The single most important workflow in the platform: it converts a stranger on the public "
        "website into a tracked, portal-enabled member with a permanent ID. It is deliberately "
        "staged so that an incomplete application never reaches a human reviewer."))
    F.append(flow(WF_ONBOARD,
                  "Figure 2 \u2014 Membership and volunteer onboarding. Two decision gates keep "
                  "reviewer time focused on genuine candidates; every outcome is notified to the "
                  "applicant with a reference ID."))
    F.append(Paragraph("Service levels and rules", R.H4))
    F.append(R.make_table(
        ["Control point", "Rule", "Owner"],
        [["Acknowledgement", "Reference ID issued instantly on submission; e-mail + SMS within 1 minute.", "System"],
         ["Completeness check", "Automated; incomplete files returned with the exact missing items.", "System"],
         ["Auto-close", "Incomplete applications close after 14 days without resubmission.", "System"],
         ["Screening SLA", "Scheduled within 10 working days of a complete application.", "Directorate"],
         ["Final approval SLA", "Within 3 working days of a positive recommendation.", "Admin"],
         ["Cooling period", "A declined applicant may reapply after the defined period, unless declined on conduct grounds.", "Admin"],
         ["Duplicate control", "Checked against national ID / institutional roll number / phone before approval.", "System + Admin"]],
        [fw * 0.24, fw * 0.56, fw * 0.20], font_small=True))
    F.append(PageBreak())

    F.append(sec.h2("W2 \u2014 Event lifecycle"))
    F.append(R.para(
        "Events are the main delivery mechanism of YPDC, so the event lifecycle touches every "
        "portal. The workflow separates <i>approval</i> (four levels, each with a distinct purpose) "
        "from <i>execution</i> (three parallel tracks) and <i>closure</i> (reporting, certificates "
        "and analytics)."))
    F.append(flow(WF_EVENT,
                  "Figure 3 \u2014 Event lifecycle from proposal to public archive. Approval levels "
                  "are sequential; execution tracks run in parallel; closure is not optional."))
    F.append(Paragraph("Approval levels \u2014 what each one actually decides", R.H4))
    F.append(R.make_table(
        ["Level", "Approver", "Decision focus", "Typical SLA", "Can they edit the proposal?"],
        [["1", "Assistant Director", "Operational feasibility, team and date availability", "2 working days", "Yes, minor edits"],
         ["2", "Director", "Strategic fit with directorate objectives and annual plan", "2 working days", "Yes, with remark"],
         ["3", "Faculty focal person", "Academic legitimacy, speaker suitability, institutional policy", "3 working days", "Comment only"],
         ["4", "Admin", "Budget sanction, venue and date conflict, security, publication", "3 working days", "No \u2014 approve or return"]],
        [fw * 0.06, fw * 0.17, fw * 0.39, fw * 0.14, fw * 0.24],
        aligns=["C", "L", "L", "C", "L"], font_small=True))
    F.append(Spacer(1, 6))
    F.append(Paragraph("Closure requirements (mandatory before an event can be marked complete)", R.H4))
    F.extend(R.bullets([
        "Attendance reconciled and confirmed for every session of the event.",
        "Activity report submitted: summary, actual footfall, outcomes, budget used, media links, lessons learned.",
        "Certificates drafted and sent for approval where the event type carries a certificate rule.",
        "Gallery and news content submitted for publication, with consent flags set per image.",
        "Budget variance recorded, and any unused allocation released back to the directorate.",
    ]))
    F.append(PageBreak())

    F.append(sec.h2("W3 \u2014 The generic approval engine"))
    F.append(R.para(
        "Rather than writing a separate approval routine for every form type, the platform "
        "implements one configurable engine. A new form type (for example a budget request or a "
        "condonation appeal) is added by configuration \u2014 defining its levels, approvers, "
        "thresholds and SLAs \u2014 without new development."))
    F.append(flow(WF_APPROVAL,
                  "Figure 4 \u2014 Generic approval engine. The same engine serves membership, "
                  "event proposals, certificates, condonation, complaints and budget requests."))
    F.append(Paragraph("Configured approval chains", R.H4))
    F.append(R.make_table(
        ["Form type", "Approval chain", "Parallel / sequential", "SLA (total)", "Escalation on timeout"],
        [["Membership application", "Director \u2192 Faculty \u2192 Admin", "Sequential", "10 working days", "To Super Admin"],
         ["Event proposal", "Assistant Director \u2192 Director \u2192 Faculty \u2192 Admin", "Sequential", "10 working days", "To Super Admin"],
         ["Merit certificate", "Director \u2192 Admin", "Sequential", "5 working days", "To Super Admin"],
         ["Attendance condonation", "Director \u2192 Admin", "Sequential", "5 working days", "To Faculty focal person"],
         ["Budget request", "Director \u2192 Admin (threshold-based second approver above limit)", "Sequential", "7 working days", "To Project Sponsor"],
         ["Complaint (P2\u2013P4)", "Admin triage \u2192 Assigned owner \u2192 Admin closure", "Sequential", "By priority", "To grievance committee"],
         ["Complaint (P1)", "Admin \u2192 Grievance committee \u2192 Patron", "Sequential", "48 hours", "Immediate to Patron"],
         ["Alumni job / support posting", "Admin moderation only", "Single level", "2 working days", "To Content Manager"],
         ["Mentorship match", "Mentor acceptance \u2192 Alumni lead confirmation", "Sequential", "7 working days", "Re-match to next candidate"]],
        [fw * 0.19, fw * 0.34, fw * 0.13, fw * 0.13, fw * 0.21], font_small=True))
    F.append(PageBreak())

    F.append(sec.h2("W4 \u2014 Attendance: capture to certificate"))
    F.append(R.para(
        "Attendance is the most disputed data in any membership organisation. This workflow makes "
        "every mark traceable to a method, a time, a location and a person, and inserts a "
        "reconciliation step before any period is locked for reporting."))
    F.append(flow(WF_ATTEND,
                  "Figure 5 \u2014 Attendance workflow. Note the reconciliation gate before the "
                  "period lock: once locked, corrections require an admin-level adjustment with a "
                  "recorded reason."))
    F.append(Paragraph("Marking methods and their controls", R.H4))
    F.append(R.make_table(
        ["Method", "How it works", "Fraud controls", "Best used for"],
        [["QR scan", "A session QR is displayed or printed; the participant scans it from the portal.",
          "Time-boxed QR refresh; single scan per user; scan location logged.", "Large events, seminars"],
         ["Geo-fenced self-mark", "Participant marks attendance from a phone within a radius of the venue.",
          "Radius check, optional photo, device and timestamp recorded.", "Outdoor activities, field visits"],
         ["Offline numeric code", "Duty officer announces a rotating code; participants enter it.",
          "Short code life; one use per user; attempts logged.", "Poor-connectivity venues"],
         ["Manual list", "Duty officer marks a printed or on-screen list.",
          "Marker identity recorded; reconciliation and admin sampling; two-person confirmation for large sessions.",
          "Small meetings, duty rosters"]],
        [fw * 0.17, fw * 0.31, fw * 0.32, fw * 0.20], font_small=True))
    F.append(Spacer(1, 6))
    F.append(R.callout(
        "Thresholds are configurable, not hard-coded",
        "Minimum attendance percentages, deficiency warning levels, condonation limits and the "
        "attendance lock window are stored as configuration in the Admin Portal so that policy "
        "changes never require a code release. The default starting point proposed here is: "
        "warning at 80%, deficiency below 75%, condonation limited to two per year on evidence.",
        "info"))
    F.append(PageBreak())

    F.append(sec.h2("W5 \u2014 Volunteer registration to recognition"))
    F.append(flow(WF_VOLUNTEER,
                  "Figure 6 \u2014 Volunteer journey. The volunteer never leaves the funnel: even a "
                  "declined assignment keeps the profile warm in the talent pool."))
    F.append(sec.h2("W6 \u2014 Feedback &amp; complaint handling"))
    F.append(R.para(
        "Complaints are the platform's early-warning system. The workflow guarantees that no "
        "complaint disappears: every ticket has an owner, an SLA, a recorded resolution and a "
        "satisfaction rating, and sensitive matters escalate immediately regardless of queue load."))
    F.append(flow(WF_COMPLAINT,
                  "Figure 7 \u2014 Complaint handling with a dedicated fast path for P1 (sensitive "
                  "or urgent) matters and a re-opening route when the complainant is not satisfied."))
    F.append(R.make_table(
        ["Priority", "Definition", "Response", "Resolution target", "Escalation"],
        [["P1", "Safety, harassment, discrimination, legal exposure", "Immediate", "48 hours", "Grievance committee + Patron"],
         ["P2", "Significant service failure affecting a group", "1 working day", "5 working days", "Admin head"],
         ["P3", "Individual service or event issue", "2 working days", "10 working days", "Directorate head"],
         ["P4", "Suggestion, minor observation, FAQ gap", "3 working days", "Next monthly review", "\u2014"]],
        [fw * 0.08, fw * 0.36, fw * 0.14, fw * 0.18, fw * 0.24],
        aligns=["C", "L", "C", "C", "L"], font_small=True))
    F.append(PageBreak())

    F.append(sec.h2("W7 \u2014 Alumni mentorship cycle"))
    F.append(flow(WF_MENTOR,
                  "Figure 8 \u2014 Mentorship cycle. Matching is proposal-based and requires mutual "
                  "acceptance; sessions are logged so that contribution can be recognised."))
    F.append(sec.h2("W8 \u2014 Certificate issuance &amp; public verification"))
    F.append(R.para(
        "A certificate is only valuable if a third party can trust it. This workflow separates the "
        "automatic rule evaluation from the human approval, assigns a unique serial at the point "
        "of issue, and exposes a public verification endpoint so that employers and institutions "
        "can confirm authenticity in seconds."))
    F.append(flow(WF_CERT,
                  "Figure 9 \u2014 Certificate issuance and verification. Revocation is immediate "
                  "and always reflected on the public verification endpoint."))
    F.append(R.make_table(
        ["Certificate type", "Trigger", "Approval needed", "Validity", "Serial pattern"],
        [["Participation", "Confirmed registration + verified attendance", "None (rule-based auto-issue)", "Permanent", "YPDC-PRT-YYYY-NNNNN"],
         ["Volunteer service", "Completed duty with a submitted duty report", "None (rule-based auto-issue)", "Permanent", "YPDC-VOL-YYYY-NNNNN"],
         ["Completion (training / programme)", "Attendance threshold + assessment where applicable", "Director recommendation", "Permanent", "YPDC-CMP-YYYY-NNNNN"],
         ["Merit / excellence", "Performance score or competition result", "Director + Admin", "Permanent", "YPDC-MRT-YYYY-NNNNN"],
         ["Appointment / office bearer", "Appointment to a role", "Admin", "Duration of tenure", "YPDC-APPT-YYYY-NNNNN"],
         ["Alumni contribution", "Mentorship hours or support delivered", "Alumni lead + Admin", "Permanent", "YPDC-ALM-YYYY-NNNNN"]],
        [fw * 0.20, fw * 0.26, fw * 0.19, fw * 0.13, fw * 0.22], font_small=True))
    F.append(PageBreak())

    F.append(sec.h2("W9 \u2014 Performance management cycle"))
    F.append(R.para(
        "Performance in YPDC must be objective and visible, otherwise it becomes a source of "
        "grievance rather than a tool for growth. Every component of the score is derived from "
        "records the member themselves created, and every score carries an appeal route."))
    F.append(flow(WF_PERF,
                  "Figure 10 \u2014 Performance cycle. The appeal window is the key control: it "
                  "converts a dispute into a documented, reviewable decision."))
    F.append(R.make_table(
        ["Component", "Weight", "Data source", "Notes"],
        [["Tasks completed", "40%", "Task module \u2014 status, timeliness and reviewer rating",
          "Late submission scored partially; overdue and unsubmitted scored zero"],
         ["Attendance", "25%", "Attendance service \u2014 reconciled and locked records",
          "Category-wise weighting (duties weigh more than general sessions)"],
         ["Event &amp; activity participation", "20%", "Event registrations, duty roster, activity reports",
          "Leadership roles (convener, team lead) earn a multiplier"],
         ["Conduct &amp; contribution", "15%", "Director comments, peer feedback, complaints upheld",
          "Any upheld P1/P2 complaint reduces this component to zero for the period"]],
        [fw * 0.24, fw * 0.09, fw * 0.33, fw * 0.34],
        aligns=["L", "C", "L", "L"], font_small=True))
    F.append(Spacer(1, 6))
    F.append(R.callout(
        "Fairness controls built into the score",
        ["Members see the score <b>and its components</b>, never a single opaque number.",
         "A director's manual adjustment <b>requires a written justification</b> that the member can read.",
         "The <b>7-day appeal window</b> is enforced by the system: after it closes, the period is locked.",
         "Periods in which a member had no assigned tasks are <b>excluded</b> rather than scored zero."],
        "ok"))
    F.append(PageBreak())

    F.append(sec.h2("W10 \u2014 Content publication to the public site"))
    F.append(R.para(
        "Everything the public sees is managed through the Admin Portal's Website Content module. "
        "The workflow enforces review before publication, keeps a version history, and never "
        "exposes member data without an explicit consent flag."))
    F.append(journey([
        ("Draft created", "Content manager writes a page, news item, project, FAQ or album"),
        ("Media attached", "Images and documents uploaded; consent flag set per image"),
        ("Review", "Second reviewer checks accuracy, tone, consent and SEO fields"),
        ("Approve / return", "Return with comments, or approve for publication"),
        ("Publish", "Goes live on the Guest Portal; cache refreshed"),
        ("Version stored", "Previous version retained for rollback and audit"),
        ("Engagement tracked", "Views, downloads and form conversions recorded"),
        ("Archive / refresh", "Outdated content archived or updated on schedule"),
    ], cols=4, caption="Figure 11 \u2014 Content publication workflow for the Guest/Public Portal."))

    F.append(sec.h2("W11 \u2014 Notification &amp; communication flow"))
    F.append(R.para(
        "Notifications are the mechanism that keeps every other workflow moving. They are always "
        "template-driven and preference-controlled, so that a member is never spammed and a "
        "deadline is never missed silently."))
    F.append(journey([
        ("Trigger", "A system event (deadline, approval, session) or a human broadcast"),
        ("Template resolved", "Template selected by event type and audience language"),
        ("Audience resolved", "Role, directorate or cohort targeting with consent filtering"),
        ("Preference applied", "Channel (in-app / e-mail / SMS) and digest settings per user"),
        ("Dispatched", "Queued and sent with retry on failure"),
        ("Tracked", "Delivery, open and read status recorded"),
        ("Analysed", "Delivery and engagement reported in the Admin dashboard"),
    ], cols=4, caption="Figure 12 \u2014 Notification flow from trigger to analytics."))
    F.append(R.make_table(
        ["Notification category", "Examples", "Default channels", "Who controls it"],
        [["Account &amp; security", "Welcome, password reset, new device login, role change", "E-mail (mandatory) + in-app", "System"],
         ["Membership", "Application received, screening date, approved, declined, expiring", "E-mail + SMS + in-app", "Admin"],
         ["Tasks &amp; duties", "Task assigned, deadline T-3 / T-1 / overdue, duty roster published", "In-app + e-mail", "Directorate"],
         ["Approvals", "New item in queue, SLA warning, decision recorded", "In-app + e-mail", "System"],
         ["Events", "Published, registration confirmed, reminder, cancelled, report due", "In-app + e-mail + SMS", "Directorate / Admin"],
         ["Attendance &amp; certificates", "Deficiency warning, condonation decision, certificate issued", "In-app + e-mail", "System / Admin"],
         ["Complaints", "Ticket received, assigned, resolved, satisfaction request", "E-mail + in-app", "Admin"],
         ["Broadcasts", "Announcements, campaigns, emergency notices", "Selected by sender", "Admin"],
         ["Alumni", "Mentorship match, opportunity posted, reunion invite", "E-mail + in-app", "Alumni lead"]],
        [fw * 0.22, fw * 0.40, fw * 0.20, fw * 0.18], font_small=True))
    F.append(PageBreak())

    return F


# ========================================================================== #
#  BUILD (part 3) - portal specifications
# ========================================================================== #
PORTAL_ORDER = ["guest", "student", "member", "directorate", "faculty", "admin", "alumni"]
FIG_NO = {"guest": 13, "student": 14, "member": 15, "directorate": 16,
          "faculty": 17, "admin": 18, "alumni": 19}


def _portal_section(sec, key):
    p = PORTALS[key]
    F = []
    fw = R.FRAME_W
    F.extend(_portal_header(p["no"], p["title"], p["subtitle"]))
    F.append(sec.h1("Portal Specification \u2014 %s" % p["title"], numbered=False))
    F.append(Spacer(1, 3))

    F.append(Paragraph("Purpose", R.H3))
    F.append(R.para(p["purpose"]))
    F.append(Spacer(1, 2))
    F.append(R.make_table(
        ["Attribute", "Detail"],
        [["Target users", p["audience"]],
         ["Access level", p["access"]],
         ["Modules", "%d (inventoried below)" % len(p["modules"])]],
        [fw * 0.18, fw * 0.82], font_small=True))
    F.append(Spacer(1, 8))

    F.append(Paragraph("Main user journey", R.H3))
    F.append(journey(p["journey"], cols=p["cols"],
                     caption="Figure %d \u2014 %s: principal user journey through the portal."
                             % (FIG_NO[key], p["title"])))

    F.append(Paragraph("Module inventory", R.H3))
    F.append(R.para(
        "Each module below is a screen group in the portal's navigation. \u201cPrimary data "
        "entities\u201d refers to the data model in Section 9."))
    F.append(module_table(p["modules"]))
    F.append(PageBreak())
    return F


def build_part3(sec):
    F = []
    F.append(sec.h1("Portal-by-Portal Module Specification"))
    F.append(R.para(
        "This section is the functional core of the report. For each of the seven portals it "
        "states the purpose, the audience, the access level, the main user journey as a flow, and "
        "a complete module inventory with purpose, key functions and the data each module owns. "
        "The order follows the user's progression through the organisation, beginning with the "
        "public surface.", R.LEAD))
    F.append(Spacer(1, 4))
    F.append(R.make_table(
        ["Portal", "Modules covered in this section"],
        [[R.para("<b>%s \u00b7 %s</b>" % (PORTALS[k]["no"], PORTALS[k]["title"]), R.TC_B),
          ", ".join(m[0].replace("&amp;", "&") for m in PORTALS[k]["modules"])] for k in PORTAL_ORDER],
        [R.FRAME_W * 0.24, R.FRAME_W * 0.76], font_small=True))
    F.append(PageBreak())
    for k in PORTAL_ORDER:
        F.extend(_portal_section(sec, k))
    return F


# ========================================================================== #
#  BUILD (part 4) - data model, security, NFR, roadmap, KPI, risk, appendix
# ========================================================================== #
def build_part4(sec):
    F = []
    fw = R.FRAME_W

    # ---------------- 9. Data model ------------------------------------- #
    F.append(sec.h1("Data Model Outline"))
    F.append(R.para(
        "All seven portals read from and write to the entities below. This is a logical model "
        "intended to guide detailed design, not a physical schema; field types, indexes and "
        "constraints are decided in the design phase."))
    F.append(sec.h2("Core entities"))
    F.append(R.make_table(
        ["#", "Entity", "Key attributes", "Relationships", "Written by"],
        [["1", "User", "id, full name, e-mail, phone, password hash, 2FA flag, status, created / last login",
          "1\u2013n UserRole, 1\u20131 Profile", "Admin / system"],
         ["2", "Profile", "photo, date of birth, address, institution, programme, verification status",
          "1\u20131 User", "User (self), Admin verifies"],
         ["3", "Role", "code, name, description, portal, permission set", "1\u2013n UserRole, 1\u2013n Permission", "Admin"],
         ["4", "Permission", "module, action (create / read / update / delete / approve)", "n\u2013n Role", "Admin"],
         ["5", "UserRole", "user, role, scope (directorate / department), valid from / to",
          "n\u20131 User, n\u20131 Role, n\u20131 Directorate", "Admin"],
         ["6", "Membership", "member ID, tier, status, join date, validity, directorate, dues status",
          "1\u20131 User, n\u20131 Directorate", "Admin"],
         ["7", "Application", "type (membership / volunteer / other), payload, documents, reference ID, status, decision",
          "n\u20131 User, 1\u20131 ApprovalWorkflow", "Guest / Student, Admin"],
         ["8", "Directorate", "name, mandate, focus areas, established date, status, public summary",
          "1\u2013n DirectorateMember, 1\u2013n Objective", "Admin"],
         ["9", "DirectorateMember", "directorate, member, role (director / assistant / lead / member), from / to, reason",
          "n\u20131 Directorate, n\u20131 User", "Director / Admin"],
         ["10", "Objective", "title, description, owner, target value, due date, linked plan, status",
          "n\u20131 Directorate, 1\u2013n WorkPlan", "Director"],
         ["11", "WorkPlan", "period, activity line, owner, milestone dates, status, variance",
          "n\u20131 Objective", "Director"],
         ["12", "Task", "title, description, assignee, assigner, due date, priority, status, evidence, rating",
          "n\u20131 Directorate, n\u20131 User", "Director / Member"],
         ["13", "Event", "title, type, date, venue, capacity, status, budget, owner directorate, publish flag",
          "n\u20131 Directorate, 1\u20131 EventProposal, 1\u2013n Registration, 1\u2013n Session", "Directorate / Admin"],
         ["14", "EventProposal", "rationale, objectives, audience, budget, date, risk, documents, status",
          "1\u20131 Event, 1\u20131 ApprovalWorkflow", "Directorate"],
         ["15", "Registration", "event, user, status (confirmed / waitlist / cancelled), e-pass code, checked in",
          "n\u20131 Event, n\u20131 User", "User / system"],
         ["16", "DutyAssignment", "event, member, role, shift, venue, reporting officer, acceptance, duty report",
          "n\u20131 Event, n\u20131 User", "Directorate"],
         ["17", "Session", "title, event, date, start / end, venue, geo, marking method, marking window, lock status",
          "n\u20131 Event, 1\u2013n Attendance", "Directorate"],
         ["18", "Attendance", "session, user, status, timestamp, method, geo, device, marked by, condonation",
          "n\u20131 Session, n\u20131 User", "Directorate / system"],
         ["19", "VolunteerOpportunity", "title, role, skills needed, shifts, seats, location, window, status",
          "n\u20131 Directorate, 1\u2013n Application", "Directorate / Admin"],
         ["20", "Certificate", "type, user, event, template, serial, QR token, issued by, issue date, status",
          "n\u20131 User, n\u20131 Event", "Admin / system"],
         ["21", "Achievement", "title, type, user or directorate, date, awarding body, publish flag, consent",
          "n\u20131 User or Directorate", "Directorate / Admin"],
         ["22", "Performance", "user, period, component scores, total, director comment, adjustment, appeal status",
          "n\u20131 User, n\u20131 Directorate", "System / Director"],
         ["23", "ActivityReport", "event or directorate, period, summary, outcomes, footfall, budget used, media, status",
          "n\u20131 Event or Directorate", "Member / Directorate"],
         ["24", "Ticket / Feedback", "type, category, priority, subject, body, anonymity flag, owner, SLA, status, resolution, rating",
          "n\u20131 User (optional), 1\u2013n TicketNote", "Any user / Admin"],
         ["25", "Notification", "template, recipient, channel, payload, status, sent / read timestamps",
          "n\u20131 User", "System / Admin"],
         ["26", "ContentPage", "slug, title, body, type (page / news / FAQ / project), SEO fields, status, version, owner",
          "1\u2013n MediaAsset", "Content Manager"],
         ["27", "MediaAsset / Album", "file, type, size, album, caption, consent flag, credit, publish flag",
          "n\u20131 Album, n\u20131 ContentPage or Event", "Content Manager"],
         ["28", "Document", "title, category, file, version, access level (public / member / admin), retention, uploaded by",
          "n\u20131 Directorate (optional)", "Admin / Directorate"],
         ["29", "ApprovalWorkflow", "form type, chain definition, current level, status, SLA due, delegation",
          "1\u20131 source record, 1\u2013n ApprovalStep", "System"],
         ["30", "ApprovalStep", "level, approver, action, remark, decided at, time taken",
          "n\u20131 ApprovalWorkflow", "Approver / system"],
         ["31", "AlumniProfile", "batch, graduation year, city, country, organisation, designation, open-to-opportunity",
          "1\u20131 User, 1\u2013n Skill", "Alumni (self)"],
         ["32", "MentorshipPair", "mentor, mentee, field, term, cadence, goals, status, closure feedback",
          "n\u20131 User (x2), 1\u2013n Session", "Alumni lead / system"],
         ["33", "JobPosting", "title, organisation, type, description, posted by, status, applications",
          "n\u20131 User (alumni), 1\u2013n Application", "Alumni / Admin"],
         ["34", "Contribution", "type (mentorship / speaker / donor / in-kind), user, hours or value, event, recognised",
          "n\u20131 User", "System / Admin"],
         ["35", "AuditLog", "actor, action, entity, entity id, before / after, IP, user agent, timestamp",
          "immutable, append-only", "System"]],
        [fw * 0.04, fw * 0.14, fw * 0.36, fw * 0.24, fw * 0.22],
        aligns=["C", "L", "L", "L", "L"], font_small=True))
    F.append(Spacer(1, 6))
    F.append(sec.h2("Data rules that apply across all entities"))
    F.extend(R.bullets([
        "<b>Soft delete:</b> records are never physically removed; a status flag and a deletion reason are stored instead.",
        "<b>Immutable audit:</b> every create, update, approve and delete on a regulated entity writes an AuditLog entry that cannot be edited.",
        "<b>Consent flags:</b> any personally identifiable record that may be shown publicly carries an explicit, revocable consent flag.",
        "<b>Retention:</b> academic and membership records are retained for the statutory period; media and logs follow the retention schedule in Section 10.",
        "<b>Ownership:</b> every record stores who created it and who last modified it, and these fields cannot be overwritten by a user.",
    ]))
    F.append(PageBreak())

    # ---------------- 10. Security -------------------------------------- #
    F.append(sec.h1("Security, Privacy &amp; Access Control"))
    F.append(sec.h2("Authentication &amp; session control"))
    F.append(R.make_table(
        ["Control", "Specification"],
        [["Account creation", "Admin-created or self-service with e-mail verification; institutional e-mail preferred where available."],
         ["Password policy", "Minimum 10 characters, complexity check, breach-list check, no reuse of the last 5 passwords."],
         ["Second factor", "OTP by e-mail or SMS for all staff roles (Director and above, Faculty, Admin); optional for members."],
         ["Session", "Idle timeout 30 minutes (staff) / 8 hours (members); concurrent-session limit; \u201csign out all devices\u201d available to the user."],
         ["Lockout", "5 failed attempts \u2192 15-minute lockout with notification; pattern-based attempts blocked."],
         ["Password reset", "Self-service via time-limited single-use token; never sent in plain text; admin reset requires a recorded reason."],
         ["Device audit", "New-device login recorded with IP, user agent and location, and notified to the user."]],
        [fw * 0.22, fw * 0.78], font_small=True))
    F.append(Spacer(1, 6))
    F.append(sec.h2("Authorisation &amp; segregation of duty"))
    F.extend(R.bullets([
        "Permissions are evaluated <b>server-side on every request</b>; hiding a button in the interface is not an access control.",
        "Row-level scope is enforced for directorate and faculty roles \u2014 a director cannot read another directorate's records even by editing a URL.",
        "A user may not approve a workflow they initiated, and may not modify their own role or permission set.",
        "Permission changes are effective immediately, audit-logged, and reviewed in a periodic access review each term.",
        "Bulk exports are restricted to Admin and Super Admin and are watermarked with the requesting user's identity.",
    ]))
    F.append(Spacer(1, 4))
    F.append(sec.h2("Data protection &amp; privacy"))
    F.append(R.make_table(
        ["Area", "Position"],
        [["Legal basis", "Consent is captured at every public form, with a plain-language statement of purpose and retention."],
        ["Data minimisation", "Only fields required for a stated purpose are collected; optional fields are clearly marked."],
        ["Anonymity", "Complaints may be filed anonymously; the system stores no identifier once anonymity is selected."],
        ["Public exposure", "Member names, photos and achievements appear publicly only where a consent flag is set."],
        ["Third parties", "No personal data is shared with third parties except where required by law, with a recorded decision."],
        ["Subject rights", "A member may request access to, correction of, or export of their own data from their profile page."],
        ["Retention", "Membership and academic records: statutory period. Media: 5 years. Audit logs: 3 years. Session logs: 90 days."],
        ["Breach response", "Defined incident procedure with notification obligations and a named responsible officer."]],
        [fw * 0.20, fw * 0.80], font_small=True))
    F.append(Spacer(1, 6))
    F.append(sec.h2("Technical controls"))
    F.extend(R.bullets([
        "HTTPS enforced everywhere; HTTP redirected; HSTS enabled; TLS 1.2 or higher.",
        "Protection against injection, cross-site scripting, CSRF and insecure direct object references (IDOR) as standard practice, verified by test.",
        "Uploaded files scanned, type-restricted and served from a separate, non-executable storage location.",
        "Rate limiting on authentication and public forms to blunt credential stuffing and spam.",
        "Daily encrypted backups with a tested restore procedure; separate staging and production environments.",
        "Centralised logging and alerting; monitoring of error rates, response times and failed-login spikes.",
    ]))
    F.append(PageBreak())

    # ---------------- 11. NFR ------------------------------------------- #
    F.append(sec.h1("Non-Functional Requirements"))
    F.append(R.make_table(
        ["Category", "Requirement", "Target", "How it is verified"],
        [["Performance", "Page load for authenticated portal pages on a 4G connection",
          "Under 2.5 seconds for first contentful paint", "Lighthouse / field measurement at acceptance"],
         ["Performance", "API response for standard list and detail endpoints", "p95 under 400 ms", "Load test report"],
         ["Capacity", "Concurrent users during a large event check-in window",
          "1,000 concurrent with no degradation", "Load test at 2\u00d7 target"],
         ["Availability", "Platform availability during working hours", "99.5% monthly", "Monitoring dashboard, monthly report"],
         ["Scalability", "Growth headroom without architectural change", "10\u00d7 current record volume", "Design review + capacity test"],
         ["Accessibility", "Usable by people with common impairments", "WCAG 2.1 AA on public pages", "Audit before public launch"],
         ["Usability", "A new member can register for an event unaided", "Under 60 seconds from login", "Usability test with 5 users"],
         ["Compatibility", "Browsers and devices", "Latest two versions of Chrome, Edge, Safari, Firefox; Android and iOS browsers", "Cross-browser test matrix"],
         ["Language", "Interface language support", "English first; Urdu strings prepared for later localisation", "String externalisation review"],
         ["Maintainability", "Adding a new approval form type", "By configuration only, no code release", "Demonstration at acceptance"],
         ["Observability", "Detecting a production incident", "Alert within 5 minutes of an error-rate spike", "Fault injection test"],
         ["Portability", "Data export", "Full export of any entity in CSV/Excel by an authorised admin", "Demonstration at acceptance"]],
        [fw * 0.14, fw * 0.32, fw * 0.27, fw * 0.27], font_small=True))
    F.append(PageBreak())

    # ---------------- 12. Roadmap --------------------------------------- #
    F.append(sec.h1("Delivery Roadmap"))
    F.append(R.para(
        "The platform is delivered in six phases. Each phase ends with something that can actually "
        "be used, so that value and feedback arrive early rather than at the end. Durations assume "
        "a small dedicated team and are indicative pending confirmation of resources."))
    F.append(journey([
        ("Phase 1", "Discovery, design, data model, UI framework"),
        ("Phase 2", "Public website, identity, admin core"),
        ("Phase 3", "Student + Member portals"),
        ("Phase 4", "Directorate + Faculty portals"),
        ("Phase 5", "Alumni, certificates, analytics"),
        ("Phase 6", "Hardening, launch, optimisation"),
    ], cols=3, accent=R.NAVY,
        caption="Figure 20 \u2014 Six-phase delivery sequence. Phases 2 and 3 already deliver a usable product."))
    F.append(R.make_table(
        ["Phase", "Duration", "Scope", "Key deliverables", "Acceptance criteria"],
        [["1. Foundation", "4\u20136 weeks",
          "Requirements confirmation, information architecture, data model, design system, environment setup",
          "Signed-off SRS, ERD, clickable prototype, CI/CD pipeline, staging environment",
          "Executive Committee approves scope; prototype walked through by directors and faculty"],
         ["2. Public + Admin core", "6\u20138 weeks",
          "Guest Portal (14 modules), authentication, user and role management, CMS, notifications",
          "Live public website, admin user administration, content publishing",
          "Content team publishes a page, news item and gallery album without developer help"],
         ["3. Student + Member", "6\u20138 weeks",
          "Student (10) and Member (10) portals, membership workflow, attendance service, basic certificates",
          "Working onboarding, event registration, attendance marking, certificate issue",
          "One real event run end-to-end on the platform with attendance and certificates"],
         ["4. Directorate + Faculty", "6\u20138 weeks",
          "Directorate (13) and Faculty (9) portals, approval engine, performance, activity reports",
          "Full approval chains, work plan and tasks, performance scoring",
          "An event proposal approved through all four levels inside the SLA"],
         ["5. Alumni + analytics", "4\u20136 weeks",
          "Alumni (10) portal, mentorship, career board, reporting and analytics dashboards",
          "Alumni network, mentorship matching, executive dashboard and scheduled exports",
          "Quarterly executive report generated entirely from system data"],
         ["6. Hardening &amp; launch", "4 weeks",
          "Load and security testing, accessibility audit, data migration, training, go-live",
          "Test reports, training material and sessions, migration report, production launch",
          "Load test at 2\u00d7 target passed; security findings closed; 80% of directors trained"]],
        [fw * 0.13, fw * 0.10, fw * 0.25, fw * 0.26, fw * 0.26], font_small=True))
    F.append(Spacer(1, 6))
    F.append(R.callout(
        "Sequencing logic",
        ["<b>Public website first</b> because it is visible, low-risk and immediately useful for applications.",
         "<b>Attendance before performance</b> because performance scoring depends on trustworthy attendance data.",
         "<b>Approvals before directorate planning</b> so that the directorate portal opens into a working approval chain rather than a dead end.",
         "<b>Alumni last</b> because it depends on member data that must already be clean."],
        "info"))
    F.append(PageBreak())

    # ---------------- 13. KPIs ------------------------------------------ #
    F.append(sec.h1("Success Measures &amp; KPIs"))
    F.append(R.make_table(
        ["Area", "KPI", "Definition", "Target (12 months after launch)", "Reported to"],
        [["Adoption", "Active member rate", "Members logging in at least once in 30 days \u00f7 total members",
          "70%", "Executive Committee, monthly"],
         ["Adoption", "Portal-driven applications", "Applications submitted online \u00f7 total applications", "95%", "Admin, monthly"],
         ["Efficiency", "Approval cycle time", "Median working days from submission to final decision",
          "Under 5 days", "Executive Committee, monthly"],
         ["Efficiency", "SLA compliance", "Approvals decided within SLA \u00f7 total approvals", "90%", "Admin, weekly"],
         ["Operations", "Event closure rate", "Events with a submitted activity report within SLA \u00f7 events held",
          "95%", "Directors, monthly"],
         ["Operations", "Attendance coverage", "Attendee records captured \u00f7 confirmed registrations", "90%", "Directors, per event"],
         ["Quality", "Attendance disputes", "Disputes raised per 1,000 attendance marks", "Under 10", "Admin, monthly"],
         ["Quality", "Complaint resolution", "Tickets resolved within SLA \u00f7 tickets received", "85%", "Executive Committee, monthly"],
         ["Quality", "Complainant satisfaction", "Average satisfaction rating on closed tickets (1\u20135)", "4.0+", "Admin, monthly"],
         ["Recognition", "Certificate turnaround", "Median days from event closure to certificate issue", "Under 2 days", "Admin, monthly"],
         ["Recognition", "Certificate verifications", "Public verification lookups per month", "Growing trend", "Admin, quarterly"],
         ["Engagement", "Volunteer conversion", "Volunteers deployed \u00f7 volunteer applications received", "60%", "Directorates, per event"],
         ["Engagement", "Alumni mentorship pairs", "Active mentorship pairs at period end", "25+", "Alumni lead, quarterly"],
         ["Engagement", "Public site reach", "Unique public visitors per month", "Growing trend", "Content Manager, monthly"],
         ["Platform health", "Uptime", "Availability during working hours", "99.5%", "Technical lead, monthly"],
         ["Platform health", "Incidents", "Severity-1 incidents per quarter", "0", "Technical lead, quarterly"]],
        [fw * 0.13, fw * 0.17, fw * 0.30, fw * 0.19, fw * 0.21], font_small=True))
    F.append(PageBreak())

    # ---------------- 14. Risks ----------------------------------------- #
    F.append(sec.h1("Risks &amp; Mitigations"))
    F.append(R.make_table(
        ["#", "Risk", "Likelihood", "Impact", "Mitigation", "Owner"],
        [["R1", "Personal data of members or students is exposed publicly",
          "Medium", "High",
          "Consent flags on every publishable record; default to private; access review each term; publication requires a second reviewer.",
          "Admin / Technical lead"],
         ["R2", "Low adoption \u2014 members and directors keep using spreadsheets",
          "High", "High",
          "Phase-wise rollout with champions in each directorate; make the platform the only route to certificates and approvals; short training sessions.",
          "Project Sponsor"],
         ["R3", "Attendance marking is abused or disputed",
          "Medium", "High",
          "Time-boxed QR, geo checks, marker identity, reconciliation before lock, admin sampling and a documented condonation route.",
          "Director / Admin"],
         ["R4", "Approval bottlenecks at the Admin level",
          "High", "Medium",
          "SLA timers with auto-escalation, delegation on leave, threshold-based routing, and a weekly pending-approvals report.",
          "Admin"],
         ["R5", "Performance scoring is perceived as unfair",
          "Medium", "High",
          "Published weights, visible components, mandatory justification for manual adjustment, 7-day appeal window, exclusion of unassigned periods.",
          "Director / Faculty"],
         ["R6", "Scope creep delays the launch",
          "High", "Medium",
          "This document as the agreed baseline; a formal change-request route; new requests logged for a later phase by default.",
          "Project Sponsor"],
         ["R7", "Content on the public site becomes stale or inaccurate",
          "Medium", "Medium",
          "Named owner per page, review-by date, quarterly content audit, last-updated stamp visible publicly.",
          "Content Manager"],
         ["R8", "Single-person dependency on the technical team",
          "Medium", "High",
          "Documentation, standard framework, code repository with review, and a support agreement covering the first year.",
          "Technical lead"],
         ["R9", "Hosting, cost or connectivity constraints",
          "Medium", "Medium",
          "Hosting decision in Phase 1; responsive design tested on low bandwidth; offline code fallback for attendance.",
          "Admin"],
         ["R10", "Data migration from existing registers is incomplete",
          "Medium", "Medium",
          "Migration plan with a data-cleaning sprint, duplicate resolution rules, and a parallel-run period before old registers are retired.",
          "Admin"]],
        [fw * 0.04, fw * 0.22, fw * 0.09, fw * 0.07, fw * 0.40, fw * 0.18],
        aligns=["C", "L", "C", "C", "L", "L"], font_small=True))
    F.append(PageBreak())

    # ---------------- 15. Assumptions & open items ---------------------- #
    F.append(sec.h1("Assumptions &amp; Open Items"))
    F.append(sec.h2("Assumptions on which this specification rests"))
    F.extend(R.bullets([
        "The abbreviation <b>YPDC</b> and the seven-portal structure reflect the intended organisational model; the full legal name is to be confirmed.",
        "Directorates, directors, assistant directors and faculty focal persons exist as described, and appointments are recorded formally.",
        "Members have access to a smartphone or shared device capable of running a modern browser.",
        "An administrative team is available to operate the Admin Portal on a routine basis.",
        "Membership fees, where applicable, are collected outside this system in this phase.",
        "Existing paper and spreadsheet records are available for migration in a readable form.",
        "Hosting, domain, e-mail and SMS gateway arrangements will be confirmed before Phase 2 begins.",
    ]))
    F.append(Spacer(1, 4))
    F.append(sec.h2("Open items requiring a decision"))
    F.append(R.make_table(
        ["#", "Open item", "Options", "Recommendation", "Needed by"],
        [["D1", "Full legal name of YPDC", "Confirm the expansion of the abbreviation",
          "Confirm and substitute globally before external circulation", "Before Phase 2"],
         ["D2", "Attendance marking method", "QR / geo-fence / offline code / manual", "Enable all four; make QR the default", "Phase 1"],
         ["D3", "Membership fee model", "Free / annual fee / tiered", "Decide before the membership workflow is configured", "Phase 2"],
         ["D4", "Performance weighting", "As proposed (40/25/20/15) or revised",
          "Adopt as proposed for the first two periods, then review with data", "Phase 4"],
         ["D5", "Hosting", "Institutional server / managed cloud / hybrid",
          "Managed cloud with daily backups, subject to policy approval", "Phase 1"],
         ["D6", "Urdu localisation", "Now or after stabilisation", "Externalise strings now; translate after Phase 3", "Phase 2"],
         ["D7", "Certificate signatories", "Who signs each certificate type", "Confirm the signatory matrix before certificate templates are built", "Phase 3"],
         ["D8", "Grievance committee composition", "Members, chair, quorum, P1 handling", "Formally constitute before the complaint workflow goes live", "Phase 3"]],
        [fw * 0.05, fw * 0.19, fw * 0.24, fw * 0.34, fw * 0.18],
        aligns=["C", "L", "L", "L", "C"], font_small=True))
    F.append(PageBreak())

    # ---------------- Appendix A: sitemap ------------------------------- #
    F.append(sec.h1("Appendix A \u2014 Complete Module Inventory (Sitemap)"))
    F.append(R.para(
        "The authoritative list of all 81 modules across the seven portals, in the order they will "
        "appear in each portal's navigation."))
    total = 0
    rows = []
    for k in PORTAL_ORDER:
        p = PORTALS[k]
        total += len(p["modules"])
        for i, m in enumerate(p["modules"], start=1):
            rows.append([R.para("<b>%s.%d</b>" % (p["no"], i), R.TC_B),
                         R.para("<b>%s</b>" % m[0].replace("&amp;", "&"), R.TC_B),
                         p["title"] if i == 1 else "",
                         m[1]])
    F.append(R.make_table(["Ref", "Module", "Portal", "Purpose"], rows,
                          [fw * 0.07, fw * 0.22, fw * 0.17, fw * 0.54], font_small=True))
    F.append(Spacer(1, 6))
    F.append(R.callout("Total modules", "This specification covers <b>%d modules</b> across "
                                       "<b>7 portals</b>, documented in <b>11 cross-portal workflows</b> and "
                                       "<b>20 figures</b>." % (total, ), "ok"))
    F.append(PageBreak())

    # ---------------- Appendix B: glossary ------------------------------ #
    F.append(sec.h1("Appendix B \u2014 Glossary"))
    F.append(R.make_table(["Term", "Meaning in this document"],
                          [["Assistant Director", "Deputy head of a directorate, with delegated authority within the unit."],
                           ["Approval chain", "The configured sequence of approvers a form must pass through, with SLA per level."],
                           ["Condonation", "A formally approved excuse for a shortfall in attendance, recorded with a reason and evidence."],
                           ["Directorate", "A functional unit of YPDC with its own mandate, leadership, objectives and team."],
                           ["Duty", "An assigned role at a specific event or activity, with a shift and a reporting officer."],
                           ["Faculty focal person", "The faculty member responsible for academic oversight of one or more directorates."],
                           ["Geo-fence", "A virtual perimeter around a venue used to validate a self-marked attendance."],
                           ["Member ID", "The permanent unique identifier issued on induction, formatted YPDC-YYYY-DIR-NNNN."],
                           ["Period lock", "The point after which attendance for a period can no longer be changed without an admin adjustment."],
                           ["Portal", "A permission-filtered view of the platform for a specific audience."],
                           ["Reconciliation", "The review step where flagged attendance marks are confirmed or corrected before locking."],
                           ["Segregation of duty", "The rule that a person cannot both initiate and approve the same request."],
                           ["SLA", "Service level agreement \u2014 the maximum time allowed for a step before escalation."],
                           ["Soft delete", "Marking a record inactive instead of removing it, preserving history."],
                           ["Work plan", "The time-phased breakdown of a directorate's objectives into activities and milestones."],
                           ["YPDC", "The organisation; the full legal name is to be confirmed by the Executive Committee (see D1)."]],
                          [fw * 0.24, fw * 0.76], font_small=True))
    F.append(Spacer(1, 10))
    F.append(R.HR())
    F.append(Paragraph(
        "<b>End of document.</b> This workflow specification is issued as version 1.0 for the "
        "approval of the Executive Committee. On approval it becomes the baseline against which "
        "all change requests are assessed.", R.NOTE))
    return F


# ========================================================================== #
#  ENTRY POINT
# ========================================================================== #
def build(sec, renderer):
    for k, v in renderer.items():
        setattr(R, k, v)
    R.date = __import__("datetime").date
    story = []
    story.extend(build_part1(sec))
    story.extend(build_part2(sec))
    story.extend(build_part3(sec))
    story.extend(build_part4(sec))
    return story
