import sys
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_groww_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # DESIGN SYSTEM COLOR TOKENS (Groww Brand Palette + High Contrast)
    # =========================================================================
    BG_COLOR        = RGBColor(255, 255, 255) # Pure White Canvas
    TEXT_PRIMARY    = RGBColor(30, 34, 43)    # #1E222B Groww Charcoal / Dark Navy
    TEXT_SECONDARY  = RGBColor(68, 71, 91)    # #44475B Medium Slate
    TEXT_MUTED      = RGBColor(110, 115, 130) # #6E7382 Captions & Sources (strictly >= 14pt)
    
    # Groww Brand Accents
    BRAND_GREEN     = RGBColor(0, 208, 156)   # #00D09C Groww Emerald Green
    BRAND_NAVY      = RGBColor(30, 34, 43)    # #1E222B Deep Brand Navy
    ACCENT_INDIGO   = RGBColor(83, 103, 255)  # #5367FF Modern Tech Indigo / Blue
    ACCENT_AMBER    = RGBColor(242, 153, 74)  # #F2994A Gold / Warning
    ALERT_RED       = RGBColor(235, 87, 87)   # #EB5757 Risk / Churn Red
    
    # Card Backgrounds & Borders
    CARD_BG_WHITE   = RGBColor(255, 255, 255)
    CARD_BG_LIGHT   = RGBColor(248, 250, 252) # Soft Crisp Off-white
    CARD_BG_TINT    = RGBColor(240, 253, 249) # Soft Emerald Tint
    BORDER_SUBTLE   = RGBColor(226, 232, 240) # Slate Border
    BORDER_GREEN    = RGBColor(0, 208, 156)   # Emerald Highlight Border
    BORDER_INDIGO   = RGBColor(83, 103, 255)  # Indigo Highlight Border

    FONT_FAMILY = "Arial"

    # Set metadata to remain 100% anonymous (No fellow name in metadata)
    prs.core_properties.author = "Growth Team @ Groww"
    prs.core_properties.title = "Groww 12-Month SIP Continuation - PulseSIP"
    prs.core_properties.subject = "NextLeap PM Fellowship Capstone Presentation"

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, slide_num, category, title_text, subtitle_text=None):
        # 1. Category / Breadcrumb (14pt bold)
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.20), Inches(10.0), Inches(0.25))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = f"GROWW GROWTH TEAM  |  SLIDE {slide_num} OF 10  |  {category.upper()}"
        p_c.font.name = FONT_FAMILY
        p_c.font.size = Pt(14.0)
        p_c.font.bold = True
        p_c.font.color.rgb = BRAND_GREEN

        # 2. Groww Logo / Branding on Top Right
        logo_box = slide.shapes.add_textbox(Inches(10.8), Inches(0.20), Inches(1.733), Inches(0.28))
        tf_l = logo_box.text_frame
        tf_l.word_wrap = False
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.alignment = PP_ALIGN.RIGHT
        p_l.text = "GROWW •"
        p_l.font.name = FONT_FAMILY
        p_l.font.size = Pt(15.0)
        p_l.font.bold = True
        p_l.font.color.rgb = BRAND_GREEN

        # 3. Main Action-Oriented Title (20.5pt bold)
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.46), Inches(11.733), Inches(0.44))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = FONT_FAMILY
        p_t.font.size = Pt(20.5)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_PRIMARY

        # 4. Brand Color Accent Bar (Emerald, Indigo, Amber, Navy)
        bar_colors = [BRAND_GREEN, ACCENT_INDIGO, ACCENT_AMBER, BRAND_NAVY]
        bar_width = Inches(0.7)
        bar_height = Inches(0.04)
        for i, color in enumerate(bar_colors):
            b = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8 + i * 0.72), Inches(0.92), bar_width, bar_height)
            b.fill.solid()
            b.fill.fore_color.rgb = color
            b.line.fill.background()

        # 5. Subtitle / Context Line (14pt)
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.00), Inches(11.733), Inches(0.28))
            tf_s = sub_box.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            p_s.text = subtitle_text
            p_s.font.name = FONT_FAMILY
            p_s.font.size = Pt(14.0)
            p_s.font.color.rgb = TEXT_SECONDARY

    def add_footer(slide, slide_num, left_tag="NextLeap PM Capstone"):
        # Bottom left tag / pill
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(8.0), Inches(0.25))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = f"⚙ {left_tag}   |   Growth Team @ Groww"
        p_tag.font.name = FONT_FAMILY
        p_tag.font.size = Pt(14.0)
        p_tag.font.color.rgb = TEXT_MUTED

        # Bottom right slide number
        num_box = slide.shapes.add_textbox(Inches(11.0), Inches(7.08), Inches(1.533), Inches(0.25))
        tf_num = num_box.text_frame
        tf_num.word_wrap = False
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"Slide {slide_num} of 10"
        p_num.font.name = FONT_FAMILY
        p_num.font.size = Pt(14.0)
        p_num.font.bold = True
        p_num.font.color.rgb = TEXT_MUTED

    def create_card(slide, left, top, width, height, bg_color=CARD_BG_WHITE, border_color=BORDER_SUBTLE, border_width=Pt(1)):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = border_width
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: DECONSTRUCTING 12-MONTH SIP CONTINUATION (METRIC TREE & JOURNEY)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)
    add_header(slide1, 1, "Metric Decomposition & Journey Mapping",
               "Deconstructing 12-Month SIP Continuation into Core Behavioral Seams",
               "12-Month retention is a multiplicative chain of Intent, Liquidity, and Execution across the first-year journey")

    # Top Section: 3 Metric Cards (Matching Blueprint Slide 1)
    # Card 1: North Star Metric
    create_card(slide1, Inches(0.8), Inches(1.36), Inches(3.7), Inches(2.35), CARD_BG_TINT, BORDER_GREEN, Pt(1.5))
    star_badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(1.48), Inches(2.2), Inches(0.32))
    star_badge.fill.solid()
    star_badge.fill.fore_color.rgb = BRAND_GREEN
    star_badge.line.fill.background()
    tf_sb = star_badge.text_frame
    tf_sb.margin_left = tf_sb.margin_top = tf_sb.margin_right = tf_sb.margin_bottom = 0
    p_sb = tf_sb.paragraphs[0]
    p_sb.text = "★ NORTH STAR METRIC"
    p_sb.alignment = PP_ALIGN.CENTER
    p_sb.font.name = FONT_FAMILY
    p_sb.font.size = Pt(14.0)
    p_sb.font.bold = True
    p_sb.font.color.rgb = RGBColor(255, 255, 255)

    tb1 = slide1.shapes.add_textbox(Inches(0.95), Inches(1.88), Inches(3.4), Inches(1.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "% First-Timers Active at Month 12"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(16.0)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_PRIMARY
    
    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Target: ≥ 18.5% (Baseline: 12.0%, +6.5% pts lift)\nQualification: ≥ 1 successful debit in last 30 days & 12 calendar months elapsed since starting."
    p1_sub.font.name = FONT_FAMILY
    p1_sub.font.size = Pt(14.0)
    p1_sub.font.color.rgb = TEXT_SECONDARY

    # Card 2: Primary Metrics
    create_card(slide1, Inches(4.7), Inches(1.36), Inches(3.7), Inches(2.35), CARD_BG_WHITE, BORDER_SUBTLE)
    tb2 = slide1.shapes.add_textbox(Inches(4.85), Inches(1.48), Inches(3.4), Inches(2.1))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "PRIMARY COHORT METRICS"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(15.0)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_INDIGO

    p2_b = tf2.add_paragraph()
    p2_b.text = "• Mo 4–6 Survival: ≥ 58.0% (from 34.2%)\n• Active Lifespan: 8.9 mos (from 4.1 mos)\n• Bank Bounce Rate: < 3.0% (from 8.4%)\n• 12-Mo AUM Lift: ≥ +₹420 Cr cohort AUM"
    p2_b.font.name = FONT_FAMILY
    p2_b.font.size = Pt(14.0)
    p2_b.font.color.rgb = TEXT_SECONDARY

    # Card 3: L1 Multiplicative Gates
    create_card(slide1, Inches(8.6), Inches(1.36), Inches(3.933), Inches(2.35), CARD_BG_WHITE, BORDER_SUBTLE)
    tb3 = slide1.shapes.add_textbox(Inches(8.75), Inches(1.48), Inches(3.633), Inches(2.1))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = "L1 MULTIPLICATIVE GATES"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(15.0)
    p3.font.bold = True
    p3.font.color.rgb = BRAND_NAVY

    p3_b = tf3.add_paragraph()
    p3_b.text = "• P(Intent): Sustained faith in equity (≥85%)\n• P(Liquidity): Balance on debit day (≥90%)\n• P(Execution): Bank mandate success (≥96%)\n• P(Cycle) = P(Intent) × P(Liq) × P(Exec)"
    p3_b.font.name = FONT_FAMILY
    p3_b.font.size = Pt(14.0)
    p3_b.font.color.rgb = TEXT_SECONDARY

    # Bottom Section: 6-Column Journey Mapping Grid Table
    t_left = Inches(0.8)
    t_top = Inches(3.88)
    t_width = Inches(11.733)
    t_height = Inches(3.05)
    table_shape = slide1.shapes.add_table(3, 6, t_left, t_top, t_width, t_height)
    table = table_shape.table
    col_w = Inches(11.733 / 6)
    for i in range(6):
        table.columns[i].width = col_w

    stages = [
        "1. First Debit ➔",
        "2. Calm Drift ➔",
        "3. Salary Float ➔",
        "4. Market Dip ➔",
        "5. Cash Crunch ➔",
        "6. 12-Mo Retain"
    ]
    behaviours = [
        "Sets up SIP to beat inflation; expects 5-6% returns",
        "Checks app 1-2x/wk; portfolio hovers near NAV",
        "Salary delayed 2 days; bank debit date triggers early",
        "Market drops 2%; encounters alarming red loss banners",
        "Festive/family cash crunch; ₹5,000 feels heavy",
        "Discipline cemented; stays invested across cycles"
    ]
    outcomes = [
        "Anchor on long-term unit accumulation, not daily noise",
        "Reinforce discipline with DCA milestone badges",
        "Auto-adjust debit window to salary date without penalty",
        "Reframe dips as discounts: 'Bought 14 bonus units'",
        "1-tap Micro-Flex to ₹500 floor to protect streak",
        "Cohort 12-mo continuation lifts from 12.0% to ≥ 18.5%"
    ]

    for col_idx in range(6):
        # Row 0: Stage Header
        c0 = table.cell(0, col_idx)
        c0.fill.solid()
        c0.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = c0.text_frame.paragraphs[0]
        p.text = stages[col_idx]
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14.0)
        p.font.bold = True
        p.font.color.rgb = ACCENT_INDIGO

        # Row 1: Behaviour
        c1 = table.cell(1, col_idx)
        c1.fill.solid()
        c1.fill.fore_color.rgb = CARD_BG_WHITE
        p = c1.text_frame.paragraphs[0]
        p.text = behaviours[col_idx]
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14.0)
        p.font.color.rgb = TEXT_SECONDARY

        # Row 2: Desired Outcome
        c2 = table.cell(2, col_idx)
        c2.fill.solid()
        c2.fill.fore_color.rgb = CARD_BG_TINT
        p = c2.text_frame.paragraphs[0]
        p.text = outcomes[col_idx]
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14.0)
        p.font.bold = True
        p.font.color.rgb = BRAND_NAVY

    add_footer(slide1, 1, "Decomposition Framework")


    # =========================================================================
    # SLIDE 2: SECONDARY RESEARCH (AI DISCOVERY ENGINE & WHY SIPS FAIL)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, 2, "AI-Powered Discovery Engine",
               "Secondary Research: Inelastic Debits and Alarming Red Banners Cause SIP Drops",
               "AI-powered synthesis of 891 verified user reviews across Reddit r/personalfinanceindia, Play Store, Twitter & Support Forums")

    # Top Section: "WHY SIPS FAIL: TAXONOMY OF 891 VERIFIED RECORDS" (3 Cards)
    # Section Label Box
    lbl_box = slide2.shapes.add_textbox(Inches(0.8), Inches(1.36), Inches(11.733), Inches(0.28))
    tf_lbl = lbl_box.text_frame
    p_lbl = tf_lbl.paragraphs[0]
    p_lbl.text = "WHY SIPS FAIL: TAXONOMY OF 891 VERIFIED USER RECORDS"
    p_lbl.font.name = FONT_FAMILY
    p_lbl.font.size = Pt(15.0)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = ACCENT_INDIGO

    # Card 1: Inelastic Mandates
    create_card(slide2, Inches(0.8), Inches(1.70), Inches(3.7), Inches(2.2), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_c1 = slide2.shapes.add_textbox(Inches(0.95), Inches(1.82), Inches(3.4), Inches(1.95))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "Inelastic Mandates (28.5%)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED
    p_sub = tf_c1.add_paragraph()
    p_sub.text = "Fixed monthly deductions force all-or-nothing choices. When festivals or medical expenses hit, users cancel entirely because partial flex is absent."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Card 2: Alarming Red Loss Framing
    create_card(slide2, Inches(4.7), Inches(1.70), Inches(3.7), Inches(2.2), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_c2 = slide2.shapes.add_textbox(Inches(4.85), Inches(1.82), Inches(3.4), Inches(1.95))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "Red Loss Framing (26.5%)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED
    p_sub = tf_c2.add_paragraph()
    p_sub.text = "Daily negative returns in bright red trigger loss-aversion panic. First-timers interpret market dips as lost capital and flee to safe FDs and PPF."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Card 3: Mandate Bounce Shock
    create_card(slide2, Inches(8.6), Inches(1.70), Inches(3.933), Inches(2.2), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_c3 = slide2.shapes.add_textbox(Inches(8.75), Inches(1.82), Inches(3.633), Inches(1.95))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "Mandate Bounce Shock (26.8%)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED
    p_sub = tf_c3.add_paragraph()
    p_sub.text = "Salary float delays trigger ₹295 bank NACH bounce fees. Users perceive investing as punitive and delete the app in frustration."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Bottom Section: Split Cards (Left 3 Key Metrics, Right 3 Direct Verified Quotes)
    # Left: 3 Metric Badges
    create_card(slide2, Inches(0.8), Inches(4.08), Inches(3.7), Inches(2.85), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_m = slide2.shapes.add_textbox(Inches(0.95), Inches(4.18), Inches(3.4), Inches(2.65))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    
    pm1 = tf_m.paragraphs[0]
    pm1.text = "45.0% Cliff in Months 4–6"
    pm1.font.name = FONT_FAMILY
    pm1.font.size = Pt(16.0)
    pm1.font.bold = True
    pm1.font.color.rgb = ALERT_RED
    pm1_s = tf_m.add_paragraph()
    pm1_s.text = "Peak fatal churn inflection point across cohorts."
    pm1_s.font.name = FONT_FAMILY
    pm1_s.font.size = Pt(14.0)
    pm1_s.font.color.rgb = TEXT_SECONDARY

    pm2 = tf_m.add_paragraph()
    pm2.text = "₹295 Bank Bounce Penalty"
    pm2.font.name = FONT_FAMILY
    pm2.font.size = Pt(16.0)
    pm2.font.bold = True
    pm2.font.color.rgb = BRAND_NAVY
    pm2_s = tf_m.add_paragraph()
    pm2_s.text = "Unfair penalty destroys platform trust instantly."
    pm2_s.font.name = FONT_FAMILY
    pm2_s.font.size = Pt(14.0)
    pm2_s.font.color.rgb = TEXT_SECONDARY

    # Right: 3 Direct User Quotes
    create_card(slide2, Inches(4.7), Inches(4.08), Inches(7.833), Inches(2.85), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_q = slide2.shapes.add_textbox(Inches(4.85), Inches(4.18), Inches(7.533), Inches(2.65))
    tf_q = tb_q.text_frame
    tf_q.word_wrap = True
    
    pq1 = tf_q.paragraphs[0]
    pq1.text = "“Salary delayed 2 days due to long weekend. Groww presented debit on 2nd; HDFC slapped ₹295 bounce fee. Cancelled immediately.”"
    pq1.font.name = FONT_FAMILY
    pq1.font.size = Pt(14.0)
    pq1.font.bold = True
    pq1.font.color.rgb = TEXT_PRIMARY
    pq1_s = tf_q.add_paragraph()
    pq1_s.text = "— App Store Verified Review (Auto-Debit Penalty Shock)"
    pq1_s.font.name = FONT_FAMILY
    pq1_s.font.size = Pt(14.0)
    pq1_s.font.color.rgb = TEXT_MUTED

    pq2 = tf_q.add_paragraph()
    pq2.text = "“Invested ₹5,000/mo for 4 months. Yesterday my dashboard showed -₹450 in red. Parents told me to stop and put money in FD.”"
    pq2.font.name = FONT_FAMILY
    pq2.font.size = Pt(14.0)
    pq2.font.bold = True
    pq2.font.color.rgb = TEXT_PRIMARY
    pq2_s = tf_q.add_paragraph()
    pq2_s.text = "— Play Store Verified Review (Market Drawdown Panic)"
    pq2_s.font.name = FONT_FAMILY
    pq2_s.font.size = Pt(14.0)
    pq2_s.font.color.rgb = TEXT_MUTED

    add_footer(slide2, 2, "AI Discovery Engine")


    # =========================================================================
    # SLIDE 3: PRIMARY USER RESEARCH & FIELDWORK
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, 3, "Primary User Research & Fieldwork",
               "Fieldwork Validates: Users Start with High Intent but Face Rigid Debit Dates",
               "In-depth qualitative fieldwork (n=6) and live respondent validation uncovering real psychological triggers")

    # Layout: 3 Columns (Matching Blueprint Slide 3)
    # Column 1: What Investors Expect & Intend
    create_card(slide3, Inches(0.8), Inches(1.36), Inches(3.7), Inches(5.55), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_p1 = slide3.shapes.add_textbox(Inches(0.95), Inches(1.48), Inches(3.4), Inches(5.3))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True
    
    p = tf_p1.paragraphs[0]
    p.text = "WHAT USERS INTEND"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_GREEN

    p = tf_p1.add_paragraph()
    p.text = "• Beat Inflation: 78% started SIP to beat inflation without taking excessive stock market risk."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_p1.add_paragraph()
    p.text = "• 5%–6% Return Target: Pictured steady, modest growth in first 6 months down the line."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_p1.add_paragraph()
    p.text = "• Savings Account Home: Money previously sat idle in 3% bank savings accounts."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_p1.add_paragraph()
    p.text = "• Low-Stress Mindset: Defined success as steady growth without anxiety."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    # Column 2: Where Continuity Breaks
    create_card(slide3, Inches(4.7), Inches(1.36), Inches(3.7), Inches(5.55), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_p2 = slide3.shapes.add_textbox(Inches(4.85), Inches(1.48), Inches(3.4), Inches(5.3))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True
    
    p = tf_p2.paragraphs[0]
    p.text = "WHERE CONTINUITY BREAKS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED

    p = tf_p2.add_paragraph()
    p.text = "• Festive Cash Crunch: 53% face acute cash crunches during festivals (Diwali, weddings)."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_p2.add_paragraph()
    p.text = "• Alarming Red Loss: 47% feel unsettled by negative 1-day return banners & negative XIRR."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_p2.add_paragraph()
    p.text = "• Salary Float Lag: 41% face weekend salary delays; debits bounce if scheduled on 1st."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_p2.add_paragraph()
    p.text = "• Parental Pressure: Elders actively advise switching to FDs/PPF on market drops."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    # Column 3: What Users Actually Do & Quotes
    create_card(slide3, Inches(8.6), Inches(1.36), Inches(3.933), Inches(5.55), CARD_BG_TINT, BORDER_GREEN)
    tb_p3 = slide3.shapes.add_textbox(Inches(8.75), Inches(1.48), Inches(3.633), Inches(5.3))
    tf_p3 = tb_p3.text_frame
    tf_p3.word_wrap = True
    
    p = tf_p3.paragraphs[0]
    p.text = "WHAT USERS DO & SAY"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_NAVY

    p = tf_p3.add_paragraph()
    p.text = "• 75% Cancel When Tight: ₹5,000 feels heavy compared to ₹200–₹1,500 Netflix subscriptions."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_p3.add_paragraph()
    p.text = "“I paused my SIP because during festival periods I require more cash. ₹5k is a big burden compared to subscriptions.”"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY

    p = tf_p3.add_paragraph()
    p.text = "“If the app showed: 'Your ₹1,000 bought 15% more fund units at a discount', it would help me continue investing.”"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY

    p = tf_p3.add_paragraph()
    p.text = "“If Groww auto-adjusted debit dates when salary was delayed, it would increase my confidence to stay invested.”"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY

    add_footer(slide3, 3, "Primary Fieldwork")


    # =========================================================================
    # SLIDE 4: IDENTIFYING THE VULNERABLE USER SEGMENT
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, 4, "Target Segment & Persona Synthesis",
               "Identifying the Vulnerable First-Time Investor Segment",
               "Focusing on early-career salaried investors in Months 4–6 where churn concentrates and intervention ROI peaks")

    # Left Column: 2 Persona Cards (Matching Blueprint Slide 4)
    # Persona 1: Aarav
    create_card(slide4, Inches(0.8), Inches(1.36), Inches(5.6), Inches(2.65), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_pe1 = slide4.shapes.add_textbox(Inches(0.95), Inches(1.48), Inches(5.3), Inches(2.4))
    tf_pe1 = tb_pe1.text_frame
    tf_pe1.word_wrap = True
    p = tf_pe1.paragraphs[0]
    p.text = "Aarav Sharma, 24 | Junior Software Engineer"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p_sub = tf_pe1.add_paragraph()
    p_sub.text = "• Profile: Bengaluru | Salary: ₹42k/mo | SIP: ₹5,000/mo (Month 5)\n• Scheme: Parag Parikh Flexi Cap Fund\n• Pain Point: Salary delayed 2 days due to month-end weekend; debit hit on 1st, incurring ₹295 bank bounce penalty.\n• Behavioral Trigger: High intent, but traumatized by unfair banking penalties."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Persona 2: Sneha
    create_card(slide4, Inches(0.8), Inches(4.16), Inches(5.6), Inches(2.75), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_pe2 = slide4.shapes.add_textbox(Inches(0.95), Inches(4.28), Inches(5.3), Inches(2.5))
    tf_pe2 = tb_pe2.text_frame
    tf_pe2.word_wrap = True
    p = tf_pe2.paragraphs[0]
    p.text = "Sneha Patel, 26 | Associate Marketing Manager"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p_sub = tf_pe2.add_paragraph()
    p_sub.text = "• Profile: Mumbai | Salary: ₹48k/mo | SIP: ₹3,000/mo (Month 4)\n• Scheme: UTI Nifty 50 Index Fund\n• Pain Point: Portfolio down -2.8% in red; parents advised switching to PPF; Diwali shopping wiped out savings buffer.\n• Behavioral Trigger: Inelastic SIP forces all-or-nothing cancellation."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Right Column: TARGET SEGMENT (Prominent Green Border Card)
    create_card(slide4, Inches(6.6), Inches(1.36), Inches(5.933), Inches(5.55), CARD_BG_WHITE, BORDER_GREEN, Pt(2))
    
    # Target Segment Header
    tb_ts = slide4.shapes.add_textbox(Inches(6.8), Inches(1.48), Inches(5.533), Inches(0.65))
    tf_ts = tb_ts.text_frame
    tf_ts.word_wrap = True
    p = tf_ts.paragraphs[0]
    p.text = "TARGET SEGMENT: SALARIED FIRST-TIMERS IN MONTHS 4–6"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_GREEN
    p_sub = tf_ts.add_paragraph()
    p_sub.text = "Age 22–28  |  Salary ₹25k–₹60k  |  First-Time Mutual Fund SIP Journey"
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Nested Card 1: Why This Segment
    create_card(slide4, Inches(6.8), Inches(2.25), Inches(5.533), Inches(2.1), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_n1 = slide4.shapes.add_textbox(Inches(6.95), Inches(2.35), Inches(5.233), Inches(1.9))
    tf_n1 = tb_n1.text_frame
    tf_n1.word_wrap = True
    p = tf_n1.paragraphs[0]
    p.text = "WHY THIS SEGMENT?"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_NAVY
    p_sub = tf_n1.add_paragraph()
    p_sub.text = "• 45.0% Cohort Churn Cliff: Churn concentrates heavily in Months 4–6.\n• Fragile Mental Model: First exposure to festive cash shortages and red loss banners.\n• Thin Liquidity Cushion: ₹5k fixed SIP strains monthly discretionary cash."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Nested Card 2: Strategic Opportunity
    create_card(slide4, Inches(6.8), Inches(4.50), Inches(5.533), Inches(2.2), CARD_BG_TINT, BORDER_SUBTLE)
    tb_n2 = slide4.shapes.add_textbox(Inches(6.95), Inches(4.60), Inches(5.233), Inches(2.0))
    tf_n2 = tb_n2.text_frame
    tf_n2.word_wrap = True
    p = tf_n2.paragraphs[0]
    p.text = "STRATEGIC OPPORTUNITY"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_NAVY
    p_sub = tf_n2.add_paragraph()
    p_sub.text = "• 3.8x Survival Multiplier: Investors surviving past Month 6 are 3.8x more likely to reach Month 12.\n• Compounding Retention: Rescuing this cohort permanently expands Groww's active long-term investor base."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    add_footer(slide4, 4, "Target Segment Synthesis")


    # =========================================================================
    # SLIDE 5: DEFINING THE PROBLEM (NEXTLEAP 2x3 FRAMEWORK GRID)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, 5, "Problem Definition Framework",
               "Defining the Problem: The Elasticity & Visibility Breakdown",
               "Why first-time mutual fund investors abandon disciplined investing before compounding takes effect")

    # 2x3 Grid Layout (Matching Blueprint Slide 5)
    c_w = Inches(3.7)
    c_h = Inches(2.65)
    xs = [Inches(0.8), Inches(4.7), Inches(8.6)]
    ys = [Inches(1.36), Inches(4.20)]

    boxes = [
        # Row 1, Col 1: The Problem
        ("THE PROBLEM",
         "Inelastic commitments & alarming red loss banners:",
         "First-time investors abandon SIPs because rigid monthly deductions cannot flex during seasonal cash crunches, while alarming red return banners hide how price dips actually buy them more units at a discount.",
         BORDER_GREEN, CARD_BG_TINT),
        
        # Row 1, Col 2: Target Segment
        ("TARGET SEGMENT",
         "Salaried First-Timers in Months 4–6:",
         "Early-career salaried investors (age 22–28) facing their first seasonal cash crunch (Diwali) or market dip without emergency liquidity buffers.",
         BORDER_SUBTLE, CARD_BG_WHITE),

        # Row 1, Col 3: How We Know It's Real
        ("HOW DO WE KNOW IT IS REAL",
         "45% Cohort Cliff & 891 Verified Review Taxonomy:",
         "Data shows 45% of total drops hit in Months 4–6; 55% of review complaints cite rigid debits or red banner panic; 100% of interviewees confirmed festive cash strain.",
         BORDER_SUBTLE, CARD_BG_WHITE),

        # Row 2, Col 1: Value for Business
        ("VALUE FOR THE BUSINESS",
         "+₹420 Cr Retained AUM & Platform LTV Protection:",
         "Lifting 12-month retention from 12.0% to 18.5% protects ₹420+ Cr in cohort AUM, expands distribution margins, and drastically cuts customer acquisition churn.",
         BORDER_SUBTLE, CARD_BG_WHITE),

        # Row 2, Col 2: Value for Users
        ("VALUE FOR THE USERS",
         "Zero Bounce Penalties & Habit Protection:",
         "Eliminates ₹295 bounce charges, prevents all-or-nothing cancellations during festivals, and provides psychological peace of mind during market volatility.",
         BORDER_SUBTLE, CARD_BG_WHITE),

        # Row 2, Col 3: Why Solving Makes Sense
        ("WHY SOLVING MAKES SENSE",
         "Behavioral Moat in Wealth Democratization:",
         "As retail investing expands across Tier 2/3 India, solving behavioral retention differentiates Groww from traditional brokers into India's most trusted wealth partner.",
         BORDER_SUBTLE, CARD_BG_WHITE)
    ]

    idx = 0
    for r in range(2):
        for c in range(3):
            title, headline, body, b_col, bg_col = boxes[idx]
            create_card(slide5, xs[c], ys[r], c_w, c_h, bg_col, b_col, Pt(1.5) if b_col == BORDER_GREEN else Pt(1))
            tb = slide5.shapes.add_textbox(xs[c] + Inches(0.15), ys[r] + Inches(0.12), c_w - Inches(0.3), c_h - Inches(0.24))
            tf = tb.text_frame
            tf.word_wrap = True
            
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(14.0)
            p.font.bold = True
            p.font.color.rgb = BRAND_GREEN if b_col == BORDER_GREEN else ACCENT_INDIGO

            p = tf.add_paragraph()
            p.text = headline
            p.font.name = FONT_FAMILY
            p.font.size = Pt(14.0)
            p.font.bold = True
            p.font.color.rgb = TEXT_PRIMARY

            p = tf.add_paragraph()
            p.text = body
            p.font.name = FONT_FAMILY
            p.font.size = Pt(14.0)
            p.font.color.rgb = TEXT_SECONDARY
            idx += 1

    add_footer(slide5, 5, "Problem Definition")


    # =========================================================================
    # SLIDE 6: PICKING THE SOLUTION (GROWW PULSESIP & RICE MATRIX)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, 6, "Solution Prioritization (RICE Framework)",
               "Picking the Solution: Groww PulseSIP",
               "Prioritizing an AI-native elastic commitment and loss reframing engine via rigorous RICE evaluation")

    # Top Left: Winning Solution Card (Matching Blueprint Slide 6)
    create_card(slide6, Inches(0.8), Inches(1.36), Inches(5.6), Inches(3.2), CARD_BG_TINT, BORDER_GREEN, Pt(2))
    tb_win = slide6.shapes.add_textbox(Inches(0.95), Inches(1.48), Inches(5.3), Inches(2.95))
    tf_win = tb_win.text_frame
    tf_win.word_wrap = True
    p = tf_win.paragraphs[0]
    p.text = "👑 WINNING SOLUTION: GROWW PULSESIP"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_GREEN
    
    p = tf_win.add_paragraph()
    p.text = "AI-Guided Elastic SIP & Unit Accumulation Engine"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_NAVY

    p = tf_win.add_paragraph()
    p.text = "• Salary-Sync Buffer: Dynamically aligns debit date to salary deposit.\n• 1-Tap Micro-Flex: Flex to ₹500 floor or shift date ±4 days with 0 penalty.\n• Unit Accumulation View: Reframes dips into bonus units bought at discount.\n• Zero-Advice Guardrail: Deterministic SEBI RIA compliance filter.\n• Why PulseSIP? Attacks both liquidity shocks and emotional dip panic."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    # Top Right: Alternative Solutions (2 Cards)
    # Section Label Box
    lbl_alt = slide6.shapes.add_textbox(Inches(6.6), Inches(1.36), Inches(5.933), Inches(0.28))
    tf_alt = lbl_alt.text_frame
    p_alt = tf_alt.paragraphs[0]
    p_alt.text = "ALTERNATIVE SOLUTIONS CONSIDERED"
    p_alt.font.name = FONT_FAMILY
    p_alt.font.size = Pt(15.0)
    p_alt.font.bold = True
    p_alt.font.color.rgb = ACCENT_INDIGO

    # Alt Card 1: Automated Salary Account Pull
    create_card(slide6, Inches(6.6), Inches(1.70), Inches(5.933), Inches(1.35), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_a1 = slide6.shapes.add_textbox(Inches(6.75), Inches(1.78), Inches(5.633), Inches(1.15))
    tf_a1 = tb_a1.text_frame
    tf_a1.word_wrap = True
    p = tf_a1.paragraphs[0]
    p.text = "Alt 1: Automated Salary Account Pull (AA Mandate)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_NAVY
    p_sub = tf_a1.add_paragraph()
    p_sub.text = "Auto-debits percentage of salary via Account Aggregator. Rejected: High user privacy resistance; regulatory friction around variable payroll debits."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Alt Card 2: Gamified Habit Badges
    create_card(slide6, Inches(6.6), Inches(3.15), Inches(5.933), Inches(1.40), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_a2 = slide6.shapes.add_textbox(Inches(6.75), Inches(3.23), Inches(5.633), Inches(1.20))
    tf_a2 = tb_a2.text_frame
    tf_a2.word_wrap = True
    p = tf_a2.paragraphs[0]
    p.text = "Alt 2: Gamified Habit Badges & Streak Coupons"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_NAVY
    p_sub = tf_a2.add_paragraph()
    p_sub.text = "Rewards users with food/shopping vouchers. Rejected: Solves motivation but fails to solve underlying bank liquidity shortages and dip panic."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Bottom Left: RICE Prioritization Matrix Table
    t_left = Inches(0.8)
    t_top = Inches(4.75)
    t_width = Inches(8.5)
    t_height = Inches(2.15)
    table_shape = slide6.shapes.add_table(4, 6, t_left, t_top, t_width, t_height)
    table = table_shape.table
    widths = [Inches(2.5), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2)]
    for i, w in enumerate(widths):
        table.columns[i].width = w

    headers = ["Solution", "Reach", "Impact", "Confidence", "Effort", "RICE Score"]
    rows = [
        ("Groww PulseSIP (Winner)", "8", "3", "0.90", "3", "7.20"),
        ("Automated Salary Pull", "6", "3", "0.80", "4", "3.60"),
        ("Gamified Habit Badges", "7", "2", "0.75", "3", "3.50")
    ]

    for col_idx, h in enumerate(headers):
        c = table.cell(0, col_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14.0)
        p.font.bold = True
        p.font.color.rgb = BRAND_NAVY

    for row_idx, r_data in enumerate(rows):
        is_winner = (row_idx == 0)
        for col_idx, val in enumerate(r_data):
            c = table.cell(row_idx + 1, col_idx)
            c.fill.solid()
            c.fill.fore_color.rgb = CARD_BG_TINT if is_winner else CARD_BG_WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_FAMILY
            p.font.size = Pt(14.0)
            p.font.bold = is_winner
            p.font.color.rgb = BRAND_GREEN if is_winner else TEXT_SECONDARY

    # Bottom Right: Scale Callout Box
    create_card(slide6, Inches(9.5), Inches(4.75), Inches(3.033), Inches(2.15), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_scale = slide6.shapes.add_textbox(Inches(9.65), Inches(4.85), Inches(2.733), Inches(1.95))
    tf_scale = tb_scale.text_frame
    tf_scale.word_wrap = True
    p = tf_scale.paragraphs[0]
    p.text = "SCORING SCALE & LOGIC"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_NAVY
    p_sub = tf_scale.add_paragraph()
    p_sub.text = "• Reach: 1–10 (% cohort)\n• Impact: 1–3 (Retention lift)\n• Confidence: 0–1 (Research)\n• Effort: 1–5 (Dev months)\n• RICE = (R × I × C) / E"
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    add_footer(slide6, 6, "Solution Selection")


    # =========================================================================
    # SLIDE 7: HOW PULSESIP SOLVES THE DROP-OFF CLIFF (USER FLOW STORYBOARD)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, 7, "Product Mechanism & User Flow",
               "How PulseSIP Solves the Drop-off Cliff",
               "Transforming moments of cashflow friction and market panic into unbroken investing streaks")

    # 3 Chronological Flow Columns (Matching Blueprint Slide 7)
    col_w = Inches(3.7)
    col_h = Inches(4.0)
    xs = [Inches(0.8), Inches(4.7), Inches(8.6)]

    # Column 1: Salary-Sync & Liquidity Buffer
    create_card(slide7, xs[0], Inches(1.36), col_w, col_h, CARD_BG_WHITE, BORDER_SUBTLE)
    tb_f1 = slide7.shapes.add_textbox(xs[0] + Inches(0.15), Inches(1.48), col_w - Inches(0.3), col_h - Inches(0.24))
    tf_f1 = tb_f1.text_frame
    tf_f1.word_wrap = True
    p = tf_f1.paragraphs[0]
    p.text = "1. SALARY SYNCHRONIZATION"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO

    p = tf_f1.add_paragraph()
    p.text = "• Problem: Salary delayed by 2 days; fixed debit hits empty account.\n• PulseSIP Action: Pre-debit T-3 balance check detects tight cashflow.\n• Smart Buffer: Automatically shifts debit window to salary credit date.\n• Zero Penalty: Prevents ₹295 bank NACH bounce charges completely."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    # Caption Box 1
    create_card(slide7, xs[0], Inches(5.50), col_w, Inches(1.45), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_cap1 = slide7.shapes.add_textbox(xs[0] + Inches(0.15), Inches(5.60), col_w - Inches(0.3), Inches(1.25))
    tf_cap1 = tb_cap1.text_frame
    tf_cap1.word_wrap = True
    p = tf_cap1.paragraphs[0]
    p.text = "Salary Synchronization —"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p_sub = tf_cap1.add_paragraph()
    p_sub.text = "Proactive buffer synchronizes debit to salary arrival, eliminating bounce fee shock."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Connector 1 -> 2
    tb_arr1 = slide7.shapes.add_textbox(Inches(4.45), Inches(3.0), Inches(0.3), Inches(0.4))
    tf_arr1 = tb_arr1.text_frame
    p_arr1 = tf_arr1.paragraphs[0]
    p_arr1.text = "➔"
    p_arr1.font.name = FONT_FAMILY
    p_arr1.font.size = Pt(20.0)
    p_arr1.font.bold = True
    p_arr1.font.color.rgb = BRAND_GREEN

    # Column 2: 1-Tap Seasonal Micro-Flex
    create_card(slide7, xs[1], Inches(1.36), col_w, col_h, CARD_BG_WHITE, BORDER_SUBTLE)
    tb_f2 = slide7.shapes.add_textbox(xs[1] + Inches(0.15), Inches(1.48), col_w - Inches(0.3), col_h - Inches(0.24))
    tf_f2 = tb_f2.text_frame
    tf_f2.word_wrap = True
    p = tf_f2.paragraphs[0]
    p.text = "2. 1-TAP SEASONAL MICRO-FLEX"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_GREEN

    p = tf_f2.add_paragraph()
    p.text = "• Problem: Festive expenses leave user unable to pay ₹5,000.\n• PulseSIP Action: 1-tap option to flex instalment to ₹500 floor for 1 cycle.\n• Habit Shield: Keeps investing streak alive without breaking bank.\n• Auto-Restore: Default restores original ₹5,000 next cycle automatically."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    # Caption Box 2
    create_card(slide7, xs[1], Inches(5.50), col_w, Inches(1.45), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_cap2 = slide7.shapes.add_textbox(xs[1] + Inches(0.15), Inches(5.60), col_w - Inches(0.3), Inches(1.25))
    tf_cap2 = tb_cap2.text_frame
    tf_cap2.word_wrap = True
    p = tf_cap2.paragraphs[0]
    p.text = "1-Tap Micro-Flex —"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p_sub = tf_cap2.add_paragraph()
    p_sub.text = "Provides seasonal elasticity without breaking the investing habit or cancelling mandates."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Connector 2 -> 3
    tb_arr2 = slide7.shapes.add_textbox(Inches(8.35), Inches(3.0), Inches(0.3), Inches(0.4))
    tf_arr2 = tb_arr2.text_frame
    p_arr2 = tf_arr2.paragraphs[0]
    p_arr2.text = "➔"
    p_arr2.font.name = FONT_FAMILY
    p_arr2.font.size = Pt(20.0)
    p_arr2.font.bold = True
    p_arr2.font.color.rgb = BRAND_GREEN

    # Column 3: Unit Accumulation & Discount View
    create_card(slide7, xs[2], Inches(1.36), col_w, col_h, CARD_BG_TINT, BORDER_GREEN)
    tb_f3 = slide7.shapes.add_textbox(xs[2] + Inches(0.15), Inches(1.48), col_w - Inches(0.3), col_h - Inches(0.24))
    tf_f3 = tb_f3.text_frame
    tf_f3.word_wrap = True
    p = tf_f3.paragraphs[0]
    p.text = "3. UNIT ACCUMULATION VIEW"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_NAVY

    p = tf_f3.add_paragraph()
    p.text = "• Problem: Market drops 2%; red banner triggers panic exit.\n• PulseSIP Action: Replaces red banner with Unit Accumulator.\n• Discount Framing: 'Your ₹5,000 bought 62.5 units (+3.8 bonus units at 6.1% discount)'.\n• Compounding Faith: Turns market dips into grocery flash-sale moments."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    # Caption Box 3
    create_card(slide7, xs[2], Inches(5.50), col_w, Inches(1.45), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_cap3 = slide7.shapes.add_textbox(xs[2] + Inches(0.15), Inches(5.60), col_w - Inches(0.3), Inches(1.25))
    tf_cap3 = tb_cap3.text_frame
    tf_cap3.word_wrap = True
    p = tf_cap3.paragraphs[0]
    p.text = "Cognitive Loss Reframing —"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p_sub = tf_cap3.add_paragraph()
    p_sub.text = "Replaces red panic banners with unit accumulation math, turning market dips into flash sales."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    add_footer(slide7, 7, "Product Mechanism")


    # =========================================================================
    # SLIDE 8: HOW USERS RESPONDED TO GROWW PULSESIP (USER TESTING & ITERATIONS)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, 8, "Prototype Testing & Iterations",
               "How did Users feel about Groww PulseSIP",
               "Usability testing across 3 first-time SIP investors validating core hypotheses and informing v1 → v2 evolution")

    # Left Column (~55% width): 2 Prototype Mockup Cards with Captions (Matching Blueprint Slide 8)
    # Screen 1: Unit Accumulator
    create_card(slide8, Inches(0.8), Inches(1.36), Inches(3.2), Inches(3.8), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_sc1 = slide8.shapes.add_textbox(Inches(0.95), Inches(1.48), Inches(2.9), Inches(3.55))
    tf_sc1 = tb_sc1.text_frame
    tf_sc1.word_wrap = True
    p = tf_sc1.paragraphs[0]
    p.text = "SCREEN 1: DIPS AS DISCOUNTS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p_sub = tf_sc1.add_paragraph()
    p_sub.text = "• Header: Unit Accumulator\n• Badge: Nifty down -1.8%\n• Insight: Today's ₹5,000 bought 62.5 units (+3.8 bonus units at 6.1% discount)\n• Base NAV: ₹85.20 ➔ ₹80.00\n• Streak: Month 5/12 Protected"
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Caption Screen 1
    create_card(slide8, Inches(0.8), Inches(5.25), Inches(3.2), Inches(1.65), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_c1 = slide8.shapes.add_textbox(Inches(0.95), Inches(5.35), Inches(2.9), Inches(1.45))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "Loss Reframing View —"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p_sub = tf_c1.add_paragraph()
    p_sub.text = "Reframes market dips into tangible unit accumulation, removing panic."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Connector Arrow
    tb_arr8 = slide8.shapes.add_textbox(Inches(4.05), Inches(3.0), Inches(0.25), Inches(0.4))
    tf_arr8 = tb_arr8.text_frame
    p_arr8 = tf_arr8.paragraphs[0]
    p_arr8.text = "➔"
    p_arr8.font.name = FONT_FAMILY
    p_arr8.font.size = Pt(18.0)
    p_arr8.font.bold = True
    p_arr8.font.color.rgb = BRAND_GREEN

    # Screen 2: 1-Tap Micro-Flex Modal
    create_card(slide8, Inches(4.35), Inches(1.36), Inches(3.2), Inches(3.8), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_sc2 = slide8.shapes.add_textbox(Inches(4.50), Inches(1.48), Inches(2.9), Inches(3.55))
    tf_sc2 = tb_sc2.text_frame
    tf_sc2.word_wrap = True
    p = tf_sc2.paragraphs[0]
    p.text = "SCREEN 2: 1-TAP MICRO-FLEX"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_GREEN
    p_sub = tf_sc2.add_paragraph()
    p_sub.text = "• Header: Festive Cash Relief\n• Option A: Flex to ₹500 floor\n• Option B: Shift date by +4 days\n• Option C: Auto-resume next mo\n• Mandate: NPCI 0 fee cleared\n• Liquid Cash Kept: ₹4,500"
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Caption Screen 2
    create_card(slide8, Inches(4.35), Inches(5.25), Inches(3.2), Inches(1.65), CARD_BG_LIGHT, BORDER_SUBTLE)
    tb_c2 = slide8.shapes.add_textbox(Inches(4.50), Inches(5.35), Inches(2.9), Inches(1.45))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "1-Tap Micro-Flex Modal —"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p_sub = tf_c2.add_paragraph()
    p_sub.text = "User flexes to ₹500 floor; mandate auto-restores next cycle seamlessly."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Right Column (~45% width): Research Feedback Synthesis
    # Section Header & Usability Stat
    tb_rh = slide8.shapes.add_textbox(Inches(7.8), Inches(1.36), Inches(4.733), Inches(0.55))
    tf_rh = tb_rh.text_frame
    tf_rh.word_wrap = True
    p = tf_rh.paragraphs[0]
    p.text = "Summary of 3 User Tests with PulseSIP MVP"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p_sub = tf_rh.add_paragraph()
    p_sub.text = "SUS Usability Score: 86.7 / 100 (Grade A+)  |  Task Completion: 100%"
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.bold = True
    p_sub.font.color.rgb = BRAND_GREEN

    # Card 1: What Users Liked
    create_card(slide8, Inches(7.8), Inches(2.0), Inches(4.733), Inches(2.35), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_wl = slide8.shapes.add_textbox(Inches(7.95), Inches(2.1), Inches(4.433), Inches(2.15))
    tf_wl = tb_wl.text_frame
    tf_wl.word_wrap = True
    p = tf_wl.paragraphs[0]
    p.text = "WHAT USERS LIKED"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = BRAND_GREEN
    p_sub = tf_wl.add_paragraph()
    p_sub.text = "• Zero Penalty Relief: Salary-sync removed constant terror of ₹295 bank bounce fees.\n• Habit Preservation: Paying ₹500 during Diwali kept discipline alive without stress.\n• Reframing Dips: Bonus units made market drops feel like a flash-sale."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    # Card 2: What Didn't Work & Iterations
    create_card(slide8, Inches(7.8), Inches(4.45), Inches(4.733), Inches(2.45), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_ww = slide8.shapes.add_textbox(Inches(7.95), Inches(4.55), Inches(4.433), Inches(2.25))
    tf_ww = tb_ww.text_frame
    tf_ww.word_wrap = True
    p = tf_ww.paragraphs[0]
    p.text = "WHAT DIDN'T WORK & v1 ➔ v2 ITERATION"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED
    p_sub = tf_ww.add_paragraph()
    p_sub.text = "• v1 Flaw: Users questioned how the '4.1% discount' was calculated.\n• v2 Fix: Added 1-tap transparent tooltip: 90-day avg NAV vs today's NAV.\n• v1 Flaw: Users feared flexing to ₹500 would ruin long-term goals.\n• v2 Fix: Added Compounding Trajectory Visualizer showing nominal 4-day impact."
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14.0)
    p_sub.font.color.rgb = TEXT_SECONDARY

    add_footer(slide8, 8, "User Testing & Iterations")


    # =========================================================================
    # SLIDE 9: GTM STRATEGY AND SUCCESS METRICS
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, 9, "GTM Strategy & Success Metrics",
               "GTM Rollout Strategy and Success Framework",
               "A 4-phase horizon rollout strategy coupled with a multi-tier metric hierarchy to track business impact")

    # Layout: Two-Column Split (Matching Blueprint Slide 9)
    # Left Column: GTM Strategy (4 Stacked Phase Cards)
    tb_gh = slide9.shapes.add_textbox(Inches(0.8), Inches(1.36), Inches(5.6), Inches(0.28))
    tf_gh = tb_gh.text_frame
    p = tf_gh.paragraphs[0]
    p.text = "GTM ROLLOUT PHASES"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED

    phases = [
        ("Phase 1: Validation & Dogfooding (Month 1)",
         "Internal pilot across 500 Groww employees; stress-test eval-gate zero-advice filters on 10,000 synthetic queries."),
        ("Phase 2: Closed Beta Cohort (Months 2–3)",
         "Release to 10,000 first-time investors in Months 3–4; evaluate micro-flex adoption and mandate sync reliability."),
        ("Phase 3: Staged A/B Experiment (Months 4–6)",
         "50/50 randomized trial on 50,000 new SIP starters; measure Month 4 (C4) and Month 6 (C6) survival lift."),
        ("Phase 4: Full Scale & Platform Rollout (Months 7–12)",
         "100% rollout to all first-time mutual fund investors; integrate Account Aggregator APIs.")
    ]

    py = Inches(1.70)
    for p_title, p_desc in phases:
        create_card(slide9, Inches(0.8), py, Inches(5.6), Inches(1.22), CARD_BG_WHITE, BORDER_SUBTLE)
        tb = slide9.shapes.add_textbox(Inches(0.95), py + Inches(0.08), Inches(5.3), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14.0)
        p.font.bold = True
        p.font.color.rgb = ACCENT_INDIGO
        p_sub = tf.add_paragraph()
        p_sub.text = p_desc
        p_sub.font.name = FONT_FAMILY
        p_sub.font.size = Pt(14.0)
        p_sub.font.color.rgb = TEXT_SECONDARY
        py += Inches(1.30)

    # Right Column: Measuring Success (4 Metric Cards with Icons)
    tb_sh = slide9.shapes.add_textbox(Inches(6.8), Inches(1.36), Inches(5.733), Inches(0.28))
    tf_sh = tb_sh.text_frame
    p = tf_sh.paragraphs[0]
    p.text = "MEASURING SUCCESS FRAMEWORK"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED

    metric_cards = [
        ("★ NORTH STAR METRIC",
         "12-Month SIP Continuation Rate (C12): Target ≥ 18.5% (Baseline 12.0%, +6.5% pts lift; active debits in Month 12).",
         BRAND_GREEN, CARD_BG_TINT),
        (">> LEADING INDICATORS",
         "• Month 6 Survival (C6): ≥ 32.5% (Baseline 19.8%)\n• Micro-Flex Adoption: ≥ 45% choose flex over cancel\n• Dip View Rate: ≥ 68% view unit tracker on red days",
         ACCENT_INDIGO, CARD_BG_WHITE),
        ("<< LAGGING INDICATORS",
         "• Active SIP Lifespan: Increased from 4.1 to 8.9 months\n• Net Retained AUM: ≥ +₹420 Cr cohort AUM in Year 1\n• Customer LTV Lift: +24% increase in lifetime value",
         BRAND_NAVY, CARD_BG_WHITE),
        ("🛡️ GUARD RAIL METRICS",
         "• Bank NACH Bounce Rate: < 3.0% (down from 8.4%)\n• SEBI Advisory Breaches: Strictly 0.0% (Zero-tolerance)\n• Perpetual Undersizing: < 10% stay at ₹500 for > 90 days",
         ALERT_RED, CARD_BG_WHITE)
    ]

    my = Inches(1.70)
    for m_title, m_desc, m_col, m_bg in metric_cards:
        create_card(slide9, Inches(6.8), my, Inches(5.733), Inches(1.22), m_bg, BORDER_SUBTLE)
        tb = slide9.shapes.add_textbox(Inches(6.95), my + Inches(0.08), Inches(5.433), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14.0)
        p.font.bold = True
        p.font.color.rgb = m_col
        p_sub = tf.add_paragraph()
        p_sub.text = m_desc
        p_sub.font.name = FONT_FAMILY
        p_sub.font.size = Pt(14.0)
        p_sub.font.color.rgb = TEXT_SECONDARY
        my += Inches(1.30)

    add_footer(slide9, 9, "GTM & Metrics")


    # =========================================================================
    # SLIDE 10: MEASURING BUSINESS IMPACT AND RISKS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, 10, "Business Impact & Risk Management",
               "Measuring Business Impact and Risks",
               "Sizing the compounding business opportunity while deploying bulletproof regulatory and operational safeguards")

    # Layout: Two-Column Split (Matching Blueprint Slide 10)
    # Left Column: IMPACT SIZING (Full-Height Card Container)
    create_card(slide10, Inches(0.8), Inches(1.36), Inches(5.6), Inches(5.55), CARD_BG_WHITE, BORDER_SUBTLE)
    tb_imp = slide10.shapes.add_textbox(Inches(0.95), Inches(1.48), Inches(5.3), Inches(5.3))
    tf_imp = tb_imp.text_frame
    tf_imp.word_wrap = True
    
    p = tf_imp.paragraphs[0]
    p.text = "IMPACT SIZING & FINANCIAL MODEL"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO

    p = tf_imp.add_paragraph()
    p.text = "• 4.2M+ Annual First-Time Investors: Total addressable new mutual fund investors joining Indian fintech platforms each year."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_imp.add_paragraph()
    p.text = "• 45.0% Acute Churn Cliff: ~1.89M investors drop out during Months 4–6 due to cashflow timing mismatches and market dip panic."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_imp.add_paragraph()
    p.text = "• +661,000 Rescued Investors: Increasing 12-month continuation from 12.0% to 18.5% (+6.5% pts) retains ~273,000 incremental long-term SIP accounts."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_imp.add_paragraph()
    p.text = "• ₹420+ Cr Retained AuM: At an average SIP of ₹3,000/month, retains ₹420+ Cr in active compounding assets in Year 1."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf_imp.add_paragraph()
    p.text = "• ₹42 Cr Distribution Revenue Lift: Generates sustainable annualized distribution revenue while slashing customer re-acquisition costs."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14.0)
    p.font.color.rgb = TEXT_SECONDARY

    # Right Column: RISK & MITIGATION STRATEGIES (3 Stacked Cards)
    tb_rh10 = slide10.shapes.add_textbox(Inches(6.6), Inches(1.36), Inches(5.933), Inches(0.28))
    tf_rh10 = tb_rh10.text_frame
    p = tf_rh10.paragraphs[0]
    p.text = "RISK & MITIGATION STRATEGIES"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(15.0)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO

    risks = [
        ("SEBI RIA Regulatory Scrutiny:",
         "Conversational engine implies specific fund/stock advice, violating SEBI Investment Advisers Regulations.",
         "Deterministic 2-tier regex eval-gate (eval_gate.py) intercepts 100% of stock/fund queries before LLM generation; delivers purely mathematical rupee-cost averaging explanations."),
        
        ("Bank Mandate Clearing Latency:",
         "Bank payment gateways lag on flex updates, debiting on original date and incurring overdraft fees.",
         "Enforce T-3 day processing freeze window; for sub-72h requests, execute bilateral AMC postponement API, preventing premature bank hits."),
        
        ("Behavioral Inertia & Prolonged Undersizing:",
         "Users indefinitely keep SIP at ₹500 floor, eroding long-term compounding benefits.",
         "Default flex setting is '1-month only; auto-restore next cycle'; interactive Compounding Trajectory Visualizer demonstrates long-term wealth impact.")
    ]

    ry = Inches(1.70)
    for r_title, r_desc, m_desc in risks:
        create_card(slide10, Inches(6.6), ry, Inches(5.933), Inches(1.68), CARD_BG_WHITE, BORDER_SUBTLE)
        tb = slide10.shapes.add_textbox(Inches(6.75), ry + Inches(0.08), Inches(5.633), Inches(1.52))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = r_title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14.0)
        p.font.bold = True
        p.font.color.rgb = ALERT_RED
        
        p_desc_para = tf.add_paragraph()
        p_desc_para.text = r_desc
        p_desc_para.font.name = FONT_FAMILY
        p_desc_para.font.size = Pt(14.0)
        p_desc_para.font.color.rgb = TEXT_PRIMARY

        p_mit = tf.add_paragraph()
        p_mit.text = "Mitigation: " + m_desc
        p_mit.font.name = FONT_FAMILY
        p_mit.font.size = Pt(14.0)
        p_mit.font.color.rgb = ACCENT_INDIGO
        
        ry += Inches(1.78)

    add_footer(slide10, 10, "Impact & Risk Governance")

    # =========================================================================
    # SAVE PRESENTATION
    # =========================================================================
    out_dir = "c:/Users/jangr/Documents/NextLeap/Project/Project2/Deliverables"
    os.makedirs(out_dir, exist_ok=True)
    pptx_path = os.path.join(out_dir, "NL_Groww.pptx")
    prs.save(pptx_path)
    print(f"Presentation saved successfully to: {pptx_path}")

if __name__ == "__main__":
    create_groww_presentation()

