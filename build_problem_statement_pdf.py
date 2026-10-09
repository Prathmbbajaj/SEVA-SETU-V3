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
            self.drawString(36, 841.89 - 26, "SEVA SETU (सहकार सेवा) — OFFICIAL PROBLEM STATEMENT SPECIFICATION")
            self.drawRightString(595.27 - 36, 841.89 - 26, "MINISTRY OF COOPERATION • GOI")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 841.89 - 30, 595.27 - 36, 841.89 - 30)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 34, 595.27 - 36, 34)

        self.drawString(36, 22, "CONFIDENTIAL & PROPRIETARY — PREPARED FOR NATIONAL HACKATHON & MINISTRY EVALUATION")
        self.drawRightString(595.27 - 36, 22, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def create_callout_box(title, text, bg_hex="#eff6ff", border_hex="#2563eb", title_color="#1e3a8a"):
    title_p = Paragraph(f"<b><font color='{title_color}'>{title}</font></b>", ParagraphStyle(
        'CalloutTitle', fontName='Helvetica-Bold', fontSize=9.5, leading=13
    ))
    text_p = Paragraph(text, ParagraphStyle(
        'CalloutText', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#1e293b')
    ))
    t = Table([[title_p], [Spacer(1, 2)], [text_p]], colWidths=[523.27])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg_hex)),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(border_hex)),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def build_pdf(pdf_path="Seva_Setu_Problem_Statement_Specification.pdf"):
    # Page Setup: A4 Portrait (595.27 x 841.89 pt), Margins: 36 pt
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
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=10,
        spaceAfter=2.5
    )
    th_style = ParagraphStyle(
        'TH',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )
    td_bold = ParagraphStyle(
        'TDBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0f172a')
    )
    td_body = ParagraphStyle(
        'TDBody',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # =========================================================================
    # PAGE 1: CONTEXT, THE TRI-FOLD CRISIS & FORMAL PROBLEM STATEMENT
    # =========================================================================
    badge_table = Table([[
        Paragraph("<font color='#1e3a8a'><b>OFFICIAL PROBLEM STATEMENT SPECIFICATION</b></font>", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=8, leading=10)),
        Paragraph("<font color='#047857'><b>THEME: SAHAKAR SE SAMRIDDHI</b></font>", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=8, leading=10, alignment=2))
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

    story.append(Paragraph("Seva Setu (सहकार सेवा) — Sovereign Cooperative Digital Public Infrastructure", title_style))
    story.append(Paragraph("<b>Governing Authority:</b> Ministry of Cooperation, Government of India &bull; <b>Initiative:</b> National Cooperative Gig Economy Infrastructure &bull; <b>Document Version:</b> 1.0.0", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0'), spaceAfter=6))

    story.append(Paragraph("1. Executive Context &amp; Macroeconomic Reality", h1_style))
    story.append(Paragraph(
        "India's informal and gig economy encompasses over <b>500 million workers</b>, representing more than 90% of the nation's total labor force. Essential urban trades—electricians, plumbers, carpenters, sanitation technicians, and appliance mechanics—form the indispensable foundation of residential, institutional, and commercial life across tier-1, tier-2, and rural growth corridors.",
        body_style
    ))
    story.append(Paragraph(
        "While private venture-backed aggregators (e.g., Urban Company, TaskRabbit equivalents) succeeded in digitizing consumer discovery, they introduced a <b>centralized, commission-extractive marketplace model</b> engineered to maximize platform rent rather than worker welfare. Concurrently, India's network of over <b>100,000 Primary Agricultural Credit Societies (PACS)</b> and labor cooperatives remains completely unintegrated into the urban digital service economy, despite active government mandates under the Ministry of Cooperation to diversify PACS into multi-purpose service entities.",
        body_style
    ))

    story.append(Paragraph("2. The Core Tri-Fold Crisis", h1_style))
    
    crisis_cols = [
        [
            Paragraph("<b>PILLAR I: WORKER SQUEEZE</b>", ParagraphStyle('C1', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.HexColor('#b91c1c'))),
            Paragraph("• <b>20%–30% Platform Cut:</b> Extractive commissions on raw wages.<br/>• <b>Zero Social Safety Net:</b> No PMSBY health, life, or accident insurance.<br/>• <b>Algorithmic Penalties:</b> Deplatforming for vehicle breakdowns or delays.<br/>• <b>Depreciation Trap:</b> Worker absorbs all transit, tool, and fuel costs.", ParagraphStyle('C1Text', fontName='Helvetica', fontSize=7, leading=9.5, textColor=colors.HexColor('#334155')))
        ],
        [
            Paragraph("<b>PILLAR II: SOCIAL &amp; CONSUMER VOID</b>", ParagraphStyle('C2', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.HexColor('#b45309'))),
            Paragraph("• <b>0% Subsidies for NGOs:</b> Community clinics/schools pay commercial rates.<br/>• <b>Opaque Bundled Pricing:</b> Labor, tools, and commissions merged arbitrarily.<br/>• <b>Hardware Overcharging:</b> Untracked cash negotiations for spare parts.<br/>• <b>No Cooperative Vetting:</b> Basic private KYC without physical tool checks.", ParagraphStyle('C2Text', fontName='Helvetica', fontSize=7, leading=9.5, textColor=colors.HexColor('#334155')))
        ],
        [
            Paragraph("<b>PILLAR III: GOVERNANCE BLINDSPOT</b>", ParagraphStyle('C3', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.HexColor('#4338ca'))),
            Paragraph("• <b>PACS Excluded:</b> 100k cooperatives lack digital urban delivery layer.<br/>• <b>Zero Deficit Intelligence:</b> Ministries blind to district-level trade shortages.<br/>• <b>Untapped e-Shram:</b> Millions of registered workers lack organized jobs.<br/>• <b>Misaligned Cohorts:</b> ITI training deployed without real-time demand data.", ParagraphStyle('C3Text', fontName='Helvetica', fontSize=7, leading=9.5, textColor=colors.HexColor('#334155')))
        ]
    ]
    t_crisis = Table([
        [crisis_cols[0][0], crisis_cols[1][0], crisis_cols[2][0]],
        [crisis_cols[0][1], crisis_cols[1][1], crisis_cols[2][1]]
    ], colWidths=[174.4, 174.4, 174.4])
    t_crisis.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef2f2')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#fffbeb')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#eef2ff')),
        ('BOX', (0, 0), (0, -1), 0.5, colors.HexColor('#fca5a5')),
        ('BOX', (1, 0), (1, -1), 0.5, colors.HexColor('#fde68a')),
        ('BOX', (2, 0), (2, -1), 0.5, colors.HexColor('#c7d2fe')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_crisis)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Detailed Breakdown of Core Pain Points:</b>", h2_style))
    story.append(Paragraph("<b>1. Extractive Commission Trap:</b> Commercial platforms take 20% to 30% from the technician's earnings for marketplace matching. On an ₹800 plumbing repair, the worker loses up to ₹240 in fees despite providing their own motorcycle, tools, and labor.", bullet_style))
    story.append(Paragraph("<b>2. Total Institutional Exclusion:</b> Community clinics, orphanages, old-age homes, and public schools operating on shoestring budgets cannot afford commercial home-service rates. Aggregators have zero economic architecture to provide subsidies without slashing worker earnings.", bullet_style))
    story.append(Paragraph("<b>3. Macroeconomic Workforce Blindspot:</b> The government lacks real-time geospatial demand data on trade shortages (e.g., severe electrician deficits in District A alongside surplus in District B), causing ITI and NSDC vocational programs to run without spatial targeting.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Formal Problem Statement", h1_style))
    callout_statement = (
        "<i>\"How can the Government of India establish a sovereign, cooperative Digital Public Infrastructure (DPI) "
        "for home and institutional gig services that unbundles service economics to deliver guaranteed 100% net wages "
        "to certified technicians (0% platform commission), integrates Primary Agricultural Credit Societies (PACS) into "
        "urban service delivery, provides automated zero-loss subsidies for verified non-profits and public institutions, "
        "and delivers real-time district-level workforce deficit intelligence to national policymakers—all while operating "
        "on a self-sustaining, non-extractive financial model?\"</i>"
    )
    story.append(create_callout_box("PRIMARY PROBLEM DEFINITION", callout_statement, bg_hex="#eff6ff", border_hex="#2563eb", title_color="#1e3a8a"))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: MARKET FAILURE COMPARISON & PROPOSED SOLUTION PARADIGM
    # =========================================================================
    story.append(Paragraph("4. Why Conventional Market Solutions Fail (Structural Comparison)", h1_style))
    story.append(Paragraph(
        "Commercial aggregators cannot solve this dilemma because their business model relies on extracting maximum margin from worker labor. When private platforms offer promotional discounts, they shift the burden to the technician via reduced payouts.",
        body_style
    ))
    story.append(Spacer(1, 3))

    comp_table_data = [
        [
            Paragraph("System Dimension", th_style),
            Paragraph("Commercial Marketplace (Urban Co-Type)", th_style),
            Paragraph("Seva Setu Cooperative DPI Model", th_style)
        ],
        [
            Paragraph("<b>Worker Remuneration</b>", td_bold),
            Paragraph("Net wage = Gross Fare minus <b>20%–30% platform commission</b>", td_body),
            Paragraph("<b>100% of standard labor wage protected (0% commission)</b>", td_bold)
        ],
        [
            Paragraph("<b>Platform Revenue</b>", td_bold),
            Paragraph("High percentage cut levied directly on technician wage", td_body),
            Paragraph("Decoupled <b>3.5% tech fee</b> + B2B wholesale hardware margin + CSR admin", td_body)
        ],
        [
            Paragraph("<b>Social Welfare Pool</b>", td_bold),
            Paragraph("Voluntary, fragmented partner insurance schemes", td_body),
            Paragraph("<b>Mandatory 1.5% statutory cess</b> dedicated to PMSBY welfare &amp; accident pool", td_body)
        ],
        [
            Paragraph("<b>Social Sector Support</b>", td_bold),
            Paragraph("None; standard commercial profit maximization", td_body),
            Paragraph("<b>20% verified NGO subsidy</b> financed via commercial cross-pool &amp; CSR vouchers", td_body)
        ],
        [
            Paragraph("<b>Hardware Spare Parts</b>", td_bold),
            Paragraph("Unregulated on-site worker markup or captive private store", td_body),
            Paragraph("<b>B2B PACS wholesale QR pass</b> (0% retail markup to customer, verified GST bill)", td_body)
        ],
        [
            Paragraph("<b>Governance &amp; BI</b>", td_bold),
            Paragraph("Proprietary black-box; data withheld from government", td_body),
            Paragraph("<b>Ministry-level dashboard</b> with real-time district deficit heatmaps", td_body)
        ]
    ]

    t_comp = Table(comp_table_data, colWidths=[105, 209.13, 209.14])
    t_comp.setStyle(TableStyle([
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
    story.append(t_comp)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5. The Proposed Solution Paradigm: Seva Setu (सहकार सेवा)", h1_style))
    story.append(Paragraph(
        "Seva Setu resolves this crisis by establishing an unbundled, multi-stakeholder cooperative digital architecture structured on five interconnected operational pillars:",
        body_style
    ))
    story.append(Spacer(1, 2))

    sol_pillars = [
        ("Pillar 1: Decoupled 4-Layer Financial Architecture",
         "Every invoice is transparently itemized into base labor, transit tariff, toolkit charge, 1.5% statutory federation welfare cess, and a 3.5% tech fee. The worker's labor wage is 100% ring-fenced and disbursed instantly via UPI escrow upon END_OTP validation."),
        
        ("Pillar 2: Self-Funding Seva Subsidy Pool (Zero Worker Loss)",
         "Verified NGOs, community health centers, and public schools receive an automated 20% discount on services. This discount is never deducted from the worker's payout; it is funded through commercial emergency surge cross-subsidies (8%), corporate CSR maintenance vouchers (7%), and route density batching between 11 AM and 3 PM (5%)."),

        ("Pillar 3: Federated Cooperative Governance via PACS",
         "Integrates Primary Agricultural Credit Societies (PACS) to conduct physical tool inspections, provide decentralized dispute arbitration, and administer the PMSBY welfare cess fund, transforming PACS into active urban service hubs."),

        ("Pillar 4: B2B Wholesale Hardware Procurement QR Pass",
         "Eliminates informal material overcharging through pre-authorized digital QR passes honored at local PACS-affiliated hardware merchants at wholesale prices (0% retail customer markup, with a 3%–5% wholesale platform affiliate margin)."),

        ("Pillar 5: Macroeconomic Skill Deficit Engine & Training Cohorts",
         "Aggregates service demand and unmet requests across 750 districts into real-time geospatial heatmaps. Enables the Ministry of Cooperation and NSDC to deploy targeted vocational training cohorts directly into areas experiencing acute trade shortages.")
    ]

    for p_title, p_desc in sol_pillars:
        story.append(Paragraph(f"<b>{p_title}</b>", h2_style))
        story.append(Paragraph(p_desc, bullet_style))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: IMPACT SCORECARD, EVALUATION CRITERIA & 30-SEC PITCH
    # =========================================================================
    story.append(Paragraph("6. Target Beneficiaries &amp; 5-Year Measurable Impact Metrics", h1_style))
    
    impact_data = [
        [
            Paragraph("Metric Dimension", th_style),
            Paragraph("5-Year National DPI Target", th_style),
            Paragraph("Strategic Societal &amp; Economic Outcome", th_style)
        ],
        [
            Paragraph("<b>Active Certified Workforce</b>", td_bold),
            Paragraph("<b>500,000 Technicians</b>", td_bold),
            Paragraph("ITI/NSDC-certified technicians onboarded with verified e-Shram credentials.", td_body)
        ],
        [
            Paragraph("<b>Worker Wage Capital Retained</b>", td_bold),
            Paragraph("<b>₹750+ Crore Preserved</b>", td_bold),
            Paragraph("Capital retained by blue-collar workers that would otherwise be lost to 20%–30% platform commissions.", td_body)
        ],
        [
            Paragraph("<b>PACS Cooperative Societies</b>", td_bold),
            Paragraph("<b>10,000+ Societies Active</b>", td_bold),
            Paragraph("PACS diversified into high-margin urban service governance and hardware fulfillment.", td_body)
        ],
        [
            Paragraph("<b>Social Institutions Subsidized</b>", td_bold),
            Paragraph("<b>50,000+ NGOs &amp; Clinics</b>", td_bold),
            Paragraph("Community clinics, orphanages, and schools receiving 20% subsidized facility upkeep.", td_body)
        ],
        [
            Paragraph("<b>Statutory Welfare Cess Generated</b>", td_bold),
            Paragraph("<b>₹45+ Crore PMSBY Fund</b>", td_bold),
            Paragraph("Federation welfare pool funding universal health, life, and accident coverage for gig technicians.", td_body)
        ],
        [
            Paragraph("<b>Hardware Procurement Savings</b>", td_bold),
            Paragraph("<b>15%–20% Consumer Savings</b>", td_bold),
            Paragraph("Elimination of arbitrary worker markups on replacement spare parts via wholesale QR passes.", td_body)
        ]
    ]

    t_impact = Table(impact_data, colWidths=[120, 155, 248.27])
    t_impact.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#065f46')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_impact)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. National Evaluation &amp; Jury Rubric Alignment Matrix", h1_style))
    
    eval_matrix = [
        [
            Paragraph("Hackathon Rubric", th_style),
            Paragraph("Institutional Alignment Dimension", th_style),
            Paragraph("Seva Setu Architectural Implementation &amp; Defensibility", th_style)
        ],
        [
            Paragraph("<b>Innovation &amp; Uniqueness</b>", td_bold),
            Paragraph("Decoupled Cooperative Architecture", td_body),
            Paragraph("Separates worker wage from platform revenue (0% commission); self-funding Seva Subsidy pool.", td_body)
        ],
        [
            Paragraph("<b>Societal &amp; Economic Impact</b>", td_bold),
            Paragraph("Worker Welfare &amp; Public Equity", td_body),
            Paragraph("Retains ₹750+ Cr in workers' pockets; funds universal PMSBY insurance via 1.5% statutory cess.", td_body)
        ],
        [
            Paragraph("<b>Feasibility &amp; Technical Depth</b>", td_bold),
            Paragraph("DPI Integration &amp; Real-Time SLAs", td_body),
            Paragraph("PostGIS proximity radar, Redis Redlock concurrency, Digilocker KYC, and Police 112 ERSS webhook.", td_body)
        ],
        [
            Paragraph("<b>Financial Sustainability</b>", td_bold),
            Paragraph("Non-Extractive Revenue Model", td_body),
            Paragraph("3.5% tech fee, 3%–5% B2B hardware wholesale margin, and 2% CSR voucher administration fee.", td_body)
        ]
    ]

    t_eval = Table(eval_matrix, colWidths=[120, 155, 248.27])
    t_eval.setStyle(TableStyle([
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
    story.append(t_eval)
    story.append(Spacer(1, 6))

    story.append(Paragraph("8. The 30-Second Elevator Pitch Formulation", h1_style))
    pitch_statement = (
        "<b>Jury / Evaluator Hook:</b><br/>"
        "<i>\"Existing home-service platforms operate on an extractive commission model that takes 20% to 30% of blue-collar workers' wages while offering zero social security, opaque bundled pricing to consumers, and no affordable access for non-profits and community institutions. Meanwhile, India's 100,000 PACS cooperatives remain locked out of the digital services economy.<br/><br/>"
        "Seva Setu solves this by establishing a sovereign cooperative Digital Public Infrastructure that guarantees 100% net wages to certified technicians with zero commission, integrates PACS cooperatives for local vetting, self-funds a 20% discount for verified NGOs through commercial cross-subsidization, and delivers real-time district skill deficit heatmaps to the Ministry of Cooperation.\"</i>"
    )
    story.append(create_callout_box("30-SECOND JURY PITCH ANSWER", pitch_statement, bg_hex="#f8fafc", border_hex="#475569", title_color="#0f172a"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Problem Statement Specification PDF successfully compiled: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    out_pdf = "Seva_Setu_Problem_Statement_Specification.pdf"
    build_pdf(out_pdf)
