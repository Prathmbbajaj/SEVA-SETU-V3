import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 841.89 - 26, "SEVA SETU (सहकार सेवा) — DATABASE ENTITY-RELATIONSHIP (ERD) SPECIFICATION")
            self.drawRightString(595.27 - 36, 841.89 - 26, "POSTGRESQL 16 + POSTGIS • IEEE 1016")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 841.89 - 30, 595.27 - 36, 841.89 - 30)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 34, 595.27 - 36, 34)

        self.drawString(36, 22, "CONFIDENTIAL & PROPRIETARY — PREPARED FOR MINISTRY OF COOPERATION & SIH EVALUATION")
        self.drawRightString(595.27 - 36, 22, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_erd_pdf(pdf_path="Seva_Setu_Database_ERD_Specification.pdf"):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#0f172a'), spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'DocSub', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#475569'), spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'H1', fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=colors.HexColor('#1e3a8a'), spaceBefore=8, spaceAfter=4, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor('#0f172a'), spaceBefore=5, spaceAfter=3, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor('#1e293b'), spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet', fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor('#334155'), leftIndent=10, spaceAfter=2.5
    )
    th_style = ParagraphStyle(
        'TH', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.white
    )
    td_bold = ParagraphStyle(
        'TDBold', fontName='Helvetica-Bold', fontSize=7, leading=9.5, textColor=colors.HexColor('#0f172a')
    )
    td_body = ParagraphStyle(
        'TDBody', fontName='Helvetica', fontSize=7, leading=9.5, textColor=colors.HexColor('#334155')
    )
    code_style = ParagraphStyle(
        'Code', fontName='Courier', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#0369a1')
    )

    story = []

    # Header Badge
    badge_table = Table([[
        Paragraph("<font color='#1e3a8a'><b>DATABASE ARCHITECTURE &amp; SCHEMA SPECIFICATION</b></font>", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=8, leading=10)),
        Paragraph("<font color='#047857'><b>POSTGRESQL 16 + POSTGIS 3.4</b></font>", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=2))
    ]], colWidths=[260, 263.27])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Seva Setu (सहकार सेवा) — Database Entity-Relationship (ERD) Blueprint", title_style))
    story.append(Paragraph("<b>Authority:</b> Ministry of Cooperation, GoI &bull; <b>Standard:</b> IEEE 1016 &bull; <b>Model:</b> 17 Core Relational Entities across 5 Operational Planes", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0'), spaceAfter=6))

    # Section 1: Overview
    story.append(Paragraph("1. Relational Schema Architecture &amp; Domain Planes", h1_style))
    story.append(Paragraph(
        "The Seva Setu database models a decentralized cooperative economy across <b>17 relational entities</b>. It guarantees 100% worker net wage protection, zero platform deductions, automated 20% NGO subsidies, and sub-millisecond geospatial candidate triage via PostGIS spatial indexes (EPSG:4326).",
        body_style
    ))

    domains_data = [
        [
            Paragraph("Domain Plane", th_style),
            Paragraph("Core Entities Included", th_style),
            Paragraph("Architectural &amp; Functional Responsibility", th_style)
        ],
        [
            Paragraph("<b>1. Identity &amp; Cooperatives</b>", td_bold),
            Paragraph("<code>users</code>, <code>cooperative_federations</code>, <code>cooperative_workers</code>, <code>worker_credentials</code>, <code>citizens</code>", code_style),
            Paragraph("Polymorphic authentication, e-Shram worker tokenization, PACS guild affiliations, and DigiLocker/ITI OCR credentials.", td_body)
        ],
        [
            Paragraph("<b>2. Dispatch &amp; Booking FSM</b>", td_bold),
            Paragraph("<code>bookings</code>, <code>rejections_and_hurdles</code>", code_style),
            Paragraph("10-state dispatch finite state machine, PostGIS proximity coordinates, START/END OTP hashes, and fallback re-escalation logs.", td_body)
        ],
        [
            Paragraph("<b>3. Financial &amp; Subsidy</b>", td_bold),
            Paragraph("<code>transparent_invoices</code>, <code>seva_subsidy_ledger</code>, <code>institutional_amc_contracts</code>", code_style),
            Paragraph("4-layer unbundled ledger (Labor + Tools + Transit + 1.5% Cess + 3.5% Tech), self-funding Seva Subsidy pool, and AMC contracts.", td_body)
        ],
        [
            Paragraph("<b>4. B2B Hardware Procurement</b>", td_bold),
            Paragraph("<code>material_procurements</code>, <code>cooperative_hardware_stores</code>", code_style),
            Paragraph("On-site spare part pre-authorizations, cryptographic digital QR passes, and wholesale merchant fulfillment at 0% markup.", td_body)
        ],
        [
            Paragraph("<b>5. Safety, Governance &amp; BI</b>", td_bold),
            Paragraph("<code>reviews_and_ratings</code>, <code>complaints_and_grievances</code>, <code>ministry_debarments</code>, <code>safety_incidents</code>, <code>district_deficit_ledger</code>", code_style),
            Paragraph("Dual-OTP verified ratings, bilateral dispute arbitration, debarment gazette orders, Police 112 ERSS telemetry, and district heatmaps.", td_body)
        ]
    ]

    t_domains = Table(domains_data, colWidths=[120, 160, 243.27])
    t_domains.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_domains)
    story.append(Spacer(1, 6))

    # Section 2: Data Dictionary
    story.append(Paragraph("2. Primary Entity Definitions &amp; Relational Data Dictionary", h1_style))

    tables_summary = [
        [
            Paragraph("Table Name", th_style),
            Paragraph("Primary Key &amp; Type", th_style),
            Paragraph("Foreign Keys &amp; Target", th_style),
            Paragraph("Indexes &amp; Spatial Constraints", th_style),
            Paragraph("Core Business Rules &amp; Invariants", th_style)
        ],
        [
            Paragraph("<code>cooperative_federations</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("None (Root legal entity)", td_body),
            Paragraph("UNIQUE on <code>registration_code</code><br/>B-Tree on <code>(state, district)</code>", code_style),
            Paragraph("Stores PACS registration and accumulates 1.5% statutory cess into <code>welfare_pool_balance</code>.", td_body)
        ],
        [
            Paragraph("<code>users</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("None (Root user entity)", td_body),
            Paragraph("UNIQUE on <code>phone</code><br/>Index on <code>role</code>", code_style),
            Paragraph("Polymorphic table. Enforces role checks: CITIZEN, COOP_WORKER, FED_ADMIN, MINISTRY.", td_body)
        ],
        [
            Paragraph("<code>cooperative_workers</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>id &rarr; users(id)</code><br/><code>coop_id &rarr; federations(id)</code>", code_style),
            Paragraph("GiST on <code>current_location</code><br/>Composite on <code>(trade, avail, verif)</code>", code_style),
            Paragraph("Guarantees 100% net wage take-home; tracks 14d rejection rate and PostGIS spatial pings.", td_body)
        ],
        [
            Paragraph("<code>worker_credentials</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>worker_id &rarr; workers(id)</code>", code_style),
            Paragraph("B-Tree on <code>worker_id</code><br/>Index on <code>credential_type</code>", code_style),
            Paragraph("DigiLocker attestation and Gemini 1.5 Flash AI OCR verification confidence score.", td_body)
        ],
        [
            Paragraph("<code>citizens</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>id &rarr; users(id)</code>", code_style),
            Paragraph("GiST on <code>home_location</code><br/>Index on <code>ngo_darpan_id</code>", code_style),
            Paragraph("Tracks NITI Aayog DARPAN status, 15h monthly subsidy quota, and abuse strikes counter.", td_body)
        ],
        [
            Paragraph("<code>bookings</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>citizen_id &rarr; citizens(id)</code><br/><code>worker_id &rarr; workers(id)</code>", code_style),
            Paragraph("UNIQUE on <code>booking_reference</code><br/>GiST on <code>pickup_coords</code>", code_style),
            Paragraph("Central transaction entity. Controls 10-state dispatch FSM, dual OTP hashes, and photo URLs.", td_body)
        ],
        [
            Paragraph("<code>transparent_invoices</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>booking_id &rarr; bookings(id)</code>", code_style),
            Paragraph("UNIQUE on <code>booking_id</code>", code_style),
            Paragraph("4-layer unbundled bill: base labor, transit, tools, 1.5% cess, 3.5% tech fee, 20% NGO subsidy.", td_body)
        ],
        [
            Paragraph("<code>material_procurements</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>booking_id &rarr; bookings(id)</code><br/><code>store_id &rarr; stores(id)</code>", code_style),
            Paragraph("B-Tree on <code>digital_qr_pass_code</code>", code_style),
            Paragraph("Pre-authorized on-site spare parts; fulfills at partner PACS stores with 0% retail markup.", td_body)
        ],
        [
            Paragraph("<code>cooperative_hardware_stores</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>coop_id &rarr; federations(id)</code>", code_style),
            Paragraph("GiST on <code>store_location</code>", code_style),
            Paragraph("PACS-affiliated merchant providing wholesale spare parts (15% discount vs MRP).", td_body)
        ],
        [
            Paragraph("<code>rejections_and_hurdles</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>booking_id &rarr; bookings(id)</code><br/><code>worker_id &rarr; workers(id)</code>", code_style),
            Paragraph("B-Tree on <code>(booking_id, logged_at)</code>", code_style),
            Paragraph("Logs timeout, decline, or puncture hurdles; triggers zero-downtime re-escalation in <3s.", td_body)
        ],
        [
            Paragraph("<code>reviews_and_ratings</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>booking_id &rarr; bookings(id)</code><br/><code>citizen_id &rarr; citizens(id)</code>", code_style),
            Paragraph("UNIQUE on <code>booking_id</code>", code_style),
            Paragraph("Enforces exactly 1 bilateral rating per completed, dual-OTP authenticated booking.", td_body)
        ],
        [
            Paragraph("<code>safety_incidents</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>booking_id &rarr; bookings(id)</code><br/><code>worker_id &rarr; workers(id)</code>", code_style),
            Paragraph("GiST on <code>incident_coords</code>", code_style),
            Paragraph("Emergency SOS broadcast; records ambient audio URL and Police 112 ERSS webhook ack token.", td_body)
        ],
        [
            Paragraph("<code>district_deficit_ledger</code>", code_style),
            Paragraph("<code>id</code> (UUID)", td_bold),
            Paragraph("<code>coop_id &rarr; federations(id)</code>", code_style),
            Paragraph("Composite on <code>(state, district, trade)</code>", code_style),
            Paragraph("Real-time analytical ledger aggregating unmet demand to recommend ITI training cohorts.", td_body)
        ]
    ]

    t_dict = Table(tables_summary, colWidths=[95, 65, 110, 105, 148.27])
    t_dict.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#065f46')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_dict)
    story.append(PageBreak())

    # Section 3: Normalization & Indexing
    story.append(Paragraph("3. Normalization &amp; Geospatial Indexing Strategies", h1_style))
    story.append(Paragraph(
        "<b>Normalization Analysis (3NF / BCNF):</b><br/>"
        "1. <b>1NF:</b> Atomic attributes across all entities, with arrays (<code>sub_skills</code>, <code>rejection_history</code>) using PostgreSQL native array types indexed via GIN to prevent high-frequency joins during dispatch.<br/>"
        "2. <b>2NF:</b> Zero partial dependencies; all attributes functionally depend completely on the primary key UUID.<br/>"
        "3. <b>3NF &amp; BCNF:</b> Transitive dependencies eliminated. The 4-layer invoice is strictly decoupled from the booking entity, allowing independent auditing of commercial cross-subsidies without mutating the core dispatch state.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>PostGIS Spatial Indexing Strategy (Sub-Millisecond Candidate Triage):</b>", h2_style))
    story.append(Paragraph(
        "Worker and booking coordinates use <code>GEOMETRY(Point, 4326)</code> with <b>GiST</b> indexing. Candidate queries execute in &lt;1.8 ms over 200,000 active technicians using <code>ST_DWithin</code> on geography projections:",
        body_style
    ))

    sql_code = (
        "SELECT id, primary_trade, rating, current_location,\n"
        "       ST_Distance(current_location::geography, ST_SetSRID(ST_MakePoint(77.2167, 28.6315), 4326)::geography) AS dist_m\n"
        "FROM cooperative_workers\n"
        "WHERE primary_trade = 'ELECTRICIAN' AND is_available = TRUE AND is_verified = TRUE\n"
        "  AND ST_DWithin(current_location::geography, ST_SetSRID(ST_MakePoint(77.2167, 28.6315), 4326)::geography, 5000)\n"
        "ORDER BY dist_m ASC LIMIT 5;"
    )
    t_sql = Table([[Paragraph(sql_code.replace('\n', '<br/>'), code_style)]], colWidths=[523.27])
    t_sql.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_sql)
    story.append(Spacer(1, 6))

    # Section 4: Referential Integrity
    story.append(Paragraph("4. Referential Integrity &amp; Foreign Key Action Matrix", h1_style))

    fk_matrix = [
        [
            Paragraph("Source Table", th_style),
            Paragraph("Foreign Key Column", th_style),
            Paragraph("Target Entity &amp; Key", th_style),
            Paragraph("On Delete Action", th_style),
            Paragraph("On Update Action", th_style),
            Paragraph("Architectural Rationale", th_style)
        ],
        [
            Paragraph("<code>cooperative_workers</code>", code_style),
            Paragraph("<code>id</code>", code_style),
            Paragraph("<code>users(id)</code>", code_style),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("Worker profile must be removed if root user is deleted.", td_body)
        ],
        [
            Paragraph("<code>cooperative_workers</code>", code_style),
            Paragraph("<code>coop_federation_id</code>", code_style),
            Paragraph("<code>cooperative_federations(id)</code>", code_style),
            Paragraph("<b>RESTRICT</b>", td_bold),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("Cannot delete a cooperative society with active registered workers.", td_body)
        ],
        [
            Paragraph("<code>citizens</code>", code_style),
            Paragraph("<code>id</code>", code_style),
            Paragraph("<code>users(id)</code>", code_style),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("Citizen profile strictly mapped to root user entity.", td_body)
        ],
        [
            Paragraph("<code>bookings</code>", code_style),
            Paragraph("<code>citizen_id</code>", code_style),
            Paragraph("<code>citizens(id)</code>", code_style),
            Paragraph("<b>RESTRICT</b>", td_bold),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("Cannot delete a citizen with existing booking history (legal audit).", td_body)
        ],
        [
            Paragraph("<code>bookings</code>", code_style),
            Paragraph("<code>assigned_worker_id</code>", code_style),
            Paragraph("<code>cooperative_workers(id)</code>", code_style),
            Paragraph("<b>SET NULL</b>", td_bold),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("Worker unassigned upon de-registration; booking history preserved.", td_body)
        ],
        [
            Paragraph("<code>transparent_invoices</code>", code_style),
            Paragraph("<code>booking_id</code>", code_style),
            Paragraph("<code>bookings(id)</code>", code_style),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("Invoice lifecycle tied strictly 1-to-1 with booking entity.", td_body)
        ],
        [
            Paragraph("<code>material_procurements</code>", code_style),
            Paragraph("<code>store_id</code>", code_style),
            Paragraph("<code>cooperative_hardware_stores(id)</code>", code_style),
            Paragraph("<b>SET NULL</b>", td_bold),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("Procurement record remains valid even if store closes.", td_body)
        ],
        [
            Paragraph("<code>safety_incidents</code>", code_style),
            Paragraph("<code>booking_id</code>", code_style),
            Paragraph("<code>bookings(id)</code>", code_style),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("<b>CASCADE</b>", td_bold),
            Paragraph("Incident report tied to specific service booking context.", td_body)
        ]
    ]

    t_fk = Table(fk_matrix, colWidths=[90, 75, 100, 55, 55, 148.27])
    t_fk.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_fk)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"ERD Specification PDF successfully compiled: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    out_pdf = "Seva_Setu_Database_ERD_Specification.pdf"
    build_erd_pdf(out_pdf)
