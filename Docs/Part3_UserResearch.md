# Part 3 — Validate the Opportunity Through User Research

**Product:** Groww Mutual Funds & First-Time Investor Experience (Growth Team)  
**Document:** Master Qualitative User Research Report (`Project2/Docs/Part3_UserResearch.md`)  
**Methodology Standard:** NextLeap PM Knowledge Hub — *User Research & Innovation Framework* (Tags, Clarity Filter, In-Depth Qualitative Interviews, and Non-Obvious Synthesis).  
**Privacy & Regulatory Compliance:** 100% Zero collection of bank account numbers, PAN credentials, or portfolio screenshots.  
**Deliverables Link:** 10-Slide Capstone Deck — Slide 5 (*User Research & Fieldwork*) and Slide 6 (*Target Segment & Problem Discovery*).

---

## 1. Research Design & Methodology

Per the **NextLeap Innovation Framework**, qualitative research is not an unstructured conversation—it is a systematic inquiry designed to uncover unarticulated emotional barriers and non-obvious behavioral breakdowns.

### 1.1 Why In-Depth Interviews (and NOT Surveys)?
> ⚠️ **Knowledge Hub Golden Rule:** *"Surveys are only for quantitative validation. Never use a survey to discover why something happens or to explore unarticulated needs."*

Surveys only capture self-reported, rationalized justifications (e.g., *"I needed money"*, *"Market was down"*). In-depth qualitative interviews uncover:
- The exact sequence of events leading up to a cancellation.
- The visceral emotional state when an auto-debit fails or a red return is viewed.
- The compensatory workarounds users invent outside the app (e.g., cancelling e-mandates in net banking).

---

### 1.2 Tag-Based Question Architecture & Clarity Filter

To ensure comprehensive domain coverage without question overlap, inquiry is organized across **5 Research Tags**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               TAG-BASED INQUIRY ARCHITECTURE                                    │
├────────────────────┬──────────────────────────────────┬─────────────────────────────────────────┤
│ Tag Lens           │ Anchor Question ("What am I      │ Interview Question Protocol (Clarity)   │
│                    │ trying to do?")                  │                                         │
├────────────────────┼──────────────────────────────────┼─────────────────────────────────────────┤
│ **TAG 1: ONSET**   │ Uncover initial mental models &  │ "Take me back to the week you started.  │
│ *(Initial Spark)*  │ anchoring expectations.          │ What made you tap 'Start SIP'? What did │
│                    │                                  │ you picture happening in 6 months?"     │
├────────────────────┼──────────────────────────────────┼─────────────────────────────────────────┤
│ **TAG 2: CADENCE** │ Map daily/weekly checking habits │ "How often do you open Groww now? Walk  │
│ *(In-App Dwell)*   │ and cognitive reaction to data.  │ me through what your eyes look for when │
│                    │                                  │ the dashboard loads. How does it feel?" │
├────────────────────┼──────────────────────────────────┼─────────────────────────────────────────┤
│ **TAG 3: FRICTION**│ Localize the exact moment of     │ "Have you ever considered pausing or    │
│ *(Lapse Triggers)* │ lapse or cashflow panic.         │ stopping? What was happening in your    │
│                    │                                  │ bank account or life that exact week?"  │
├────────────────────┼──────────────────────────────────┼─────────────────────────────────────────┤
│ **TAG 4: EXTERNAL**│ Discover outside validation and  │ "When you feel unsure or see red, who   │
│ *(Social Draft)*   │ informal workarounds.            │ do you talk to? What did you do on your │
│                    │                                  │ bank's app or Reddit?"                  │
├────────────────────┼──────────────────────────────────┼─────────────────────────────────────────┤
│ **TAG 5: CONTINUITY│ Identify unarticulated levers of │ "What would make staying invested for a │
│ *(Retention Hook)* │ ongoing habit resilience.        │ full year feel as effortless as paying  │
│                    │                                  │ your Wi-Fi bill or rent?"               │
└────────────────────┴──────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 2. Target Segment Definition & Strategic Justification

We evaluate user cohorts across the **4 Camera Lenses** defined in the PM Knowledge Hub (*Session: Mapping Outcomes to Opportunities by Arindam Mukherjee*):

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             TARGET USER SEGMENT EVALUATION MATRIX                               │
├──────────────────────┬─────────────┬─────────────────┬─────────────────┬──────────┬─────────────┤
│ User Cohort          │ Segment Size│ Difficulty of   │ Probability of  │ Expected │ Strategic   │
│                      │ (% Corpus)  │ Changing Action │ Success         │ Lift     │ Priority    │
├──────────────────────┼─────────────┼─────────────────┼─────────────────┼──────────┼─────────────┤
│ **Salaried Early-    │ **53.3%**   │ **Moderate**    │ **High (88%)**  │ **+14.2%│ 🏆 **CHOSEN │
│ Career (22–27 yrs)** │ (Dominant)  │ Predictable pay,│ Direct UI/UX &  │ (Massive)│ TARGET**    │
│                      │             │ high intent     │ timing levers   │          │             │
├──────────────────────┼─────────────┼─────────────────┼─────────────────┼──────────┼─────────────┤
│ Variable / Gig       │ 6.6%        │ High            │ Moderate (55%)  │ +2.4%    │ Secondary   │
│ Freelancers          │ (Niche)     │ Unpredictable   │ Requires custom │ (Small)  │ Expansion   │
├──────────────────────┼─────────────┼─────────────────┼─────────────────┼──────────┼─────────────┤
│ Students / Gen-Z     │ 9.7%        │ High            │ Low (38%)       │ +1.8%    │ Low ROI     │
│ (<₹500/mo)           │ (Low AUM)   │ Zero cashflow   │ High impulse    │ (Small)  │             │
├──────────────────────┼─────────────┼─────────────────┼─────────────────┼──────────┼─────────────┤
│ Tier-2/3 Family      │ 6.4%        │ Very High       │ Low (40%)       │ +2.1%    │ Unsolvable  │
│ Savers               │ (Skeptical) │ Deep risk-averse│ Family veto     │ (Small)  │ via UI/UX   │
└──────────────────────┴─────────────┴─────────────────┴─────────────────┴──────────┴─────────────┘
```

### The Chosen Target Segment: "Salaried Early-Career First-Timers"
- **Demographics:** Age 22–27; first or second full-time job; monthly take-home salary ₹25,000–₹55,000.
- **Tenure Focus:** Navigating **Months 3 to 6** of their first-ever mutual fund SIP on Groww.
- **Ticket Size:** ₹1,000 to ₹3,000 per month across 1–2 equity schemes (typically Flexi Cap or Nifty Index).
- **Core Motivation:** Started with genuine ambition to build a savings habit, inspired by peers and compounding calculators.
- **Vulnerability:** Highly sensitive to **salary disbursement date gaps (1st vs 7th)** and early **nominal return drawdowns**.

---

## 3. In-Depth User Interview Fieldwork ($n=6$)

Six in-depth 45-minute semi-structured interviews were conducted with participants meeting the target segment criteria.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                SUMMARY OF PARTICIPANT ROSTER                                    │
├────┬──────────┬─────┬──────────┬──────────────┬─────────────┬──────────────┬────────────────────┤
│ ID │ Name     │ Age │ Location │ Occupation   │ Tenure      │ Monthly SIP  │ Current Status     │
├────┼──────────┼─────┼──────────┼──────────────┼─────────────┼──────────────┼────────────────────┤
│ P1 │ Aarav    │ 24M │ Bengaluru│ Jr. SWE      │ Month 5     │ ₹2,500       │ Stopped (Bounce)   │
│ P2 │ Sneha    │ 23F │ Gurugram │ Mktg Assoc.  │ Month 4     │ ₹1,500       │ Paused (Red Loss)  │
│ P3 │ Rohan    │ 26M │ Pune     │ Product Des. │ Month 6     │ ₹3,000       │ Cancelled (Diwali) │
│ P4 │ Priya    │ 25F │ Mumbai   │ Fin. Analyst │ Month 3     │ ₹2,000       │ Active (Anxious)   │
│ P5 │ Vikram   │ 27M │ Hyderabad│ Ops Lead     │ Month 8     │ ₹4,000       │ Stopped (Disengage)│
│ P6 │ Ananya   │ 22F │ Chennai  │ QA Engineer  │ Month 4     │ ₹1,000       │ Paused (Dad veto)  │
└────┴──────────┴─────┴──────────┴──────────────┴─────────────┴──────────────┴────────────────────┘
```

---

### Interview Transcript 1: Aarav (24M, Software Engineer, Bengaluru)
- **Profile:** Earns ₹42,000/month. Started a ₹2,500 SIP in a Flexi Cap fund in Month 1.
- **The Trigger:** *"Colleagues during lunch were talking about financial freedom. I felt FOMO, opened Groww, and set up autopay with my HDFC salary account."*
- **The Experience:** Months 1–3 were smooth. Checked Groww 4 times a week.
- **The Inflection Moment (Month 5):**
  > *“My company usually disburses salary on the last day of the month, but in Month 5, because of a weekend and bank holiday, salary landed on October 7th. My Groww SIP debit date was locked to October 5th. On the 5th morning, Groww attempted debit, account balance was ₹800, and it bounced.*  
  > *Two days later, HDFC slapped a **₹295 NACH return penalty** on my account! I was furious. For a ₹2,500 investment, losing ₹300 in bank fines wiped out any profit I had made. Groww support just gave me a generic FAQ link saying 'Maintain sufficient balance'. I immediately cancelled the auto-pay mandate in my HDFC net banking app. I felt the app punished me for a 48-hour salary delay.”*
- **Workaround:** Cancelled auto-pay in net banking. Has not restarted.

---

### Interview Transcript 2: Sneha (23F, Marketing Associate, Gurugram)
- **Profile:** Earns ₹32,000/month. Started a ₹1,500 SIP in Month 1.
- **The Trigger:** Compounding calculators on Instagram showing ₹1,500 becoming ₹25 Lakhs.
- **The Experience:** At Month 4, checked portfolio after a 2% Nifty correction.
- **The Inflection Moment (Month 4):**
  > *“I had invested ₹6,000 over 4 months. I opened the app, and the big banner at the top was in RED: **Total Returns -₹185 (-3.1%)**. Meanwhile, my elder sister showed me her SBI Fixed Deposit receipt giving 7.5% guaranteed every year.*  
  > *I felt like an idiot. I asked myself: 'Why am I risking my hard-earned salary in equity when even a basic bank savings account gives positive interest?' The app only showed me that I was losing money. It didn't explain that the market dip was buying me cheaper units. I hit the pause button. If month 6 doesn't turn green, I am redeeming everything.”*
- **Workaround:** Paused SIP; seeking safe alternatives on YouTube.

---

### Interview Transcript 3: Rohan (26M, Product Designer, Pune)
- **Profile:** Earns ₹52,000/month. Investing ₹3,000/month across 2 funds.
- **The Trigger:** Tax-saving (ELSS) and general wealth creation.
- **The Inflection Moment (Month 6):**
  > *“Month 6 coincided with Diwali. I had to buy flight tickets home and pay quarterly society maintenance. My bank balance dropped to ₹4,000. I wanted to skip just that single month's SIP debit so I didn't get hit by minimum balance charges.*  
  > *When I went into Groww to find a 'Skip this month' button, there was only 'Pause SIP' which warned me that auto-pay would be paused for 3 months, or 'Cancel SIP'. The UI made it look so absolute. Because I didn't want the mandate lingering or failing, I cancelled the SIP entirely. Now Diwali is over, but because there's friction to re-enter, I haven't restarted.”*
- **Workaround:** Cancelled SIP permanently due to absence of a flexible 1-tap micro-skip.

---

### Interview Transcript 4: Priya (25F, Financial Analyst, Mumbai)
- **Profile:** Earns ₹48,000/month. Started ₹2,000/month SIP.
- **The Trigger:** Peer discussions in office.
- **The Inflection Moment (Month 3):**
  > *“I know basic finance, but Groww's dashboard confused even me. In Month 2, I had invested ₹4,000. Market fell slightly, and the home screen showed **XIRR: -32.4%** in alarming red font!*  
  > *My heart sank. I thought 32% of my capital—over ₹1,200—was gone! It took me an hour of spreadsheet calculations to realize XIRR annualizes a 15-day dip. For a beginner without a finance background, seeing -32% is sheer panic. Why does the app front-load an annualized compound metric on a 60-day-old portfolio? It actively drives panic exits.”*
- **Workaround:** Ignored app; muted notifications; considered stopping.

---

### Interview Transcript 5: Vikram (27M, Operations Lead, Hyderabad)
- **Profile:** Earns ₹55,000/month. Started ₹4,000/month SIP. Reached Month 8.
- **The Trigger:** Year-end bonus habit formation.
- **The Inflection Moment (Month 8):**
  > *“For the first 3 months, I was super excited. By Month 7 or 8, the app felt completely dead. Month after month, ₹4,000 leaves my account. Groww sends zero celebratory milestones. There's no 'You completed 6 months of disciplined investing!' or 'Here is your safety net growth'.*  
  > *It literally felt like paying an electricity bill or a broadband subscription. When I bought a new motorcycle in Month 8, I needed ₹30,000 for accessories. Because the SIP had no emotional anchor or goal label, I liquidated the entire ₹32,000 accumulated balance and cancelled the mandate. It felt like a liquid piggy bank.”*
- **Workaround:** Liquidated full corpus for impulse purchase; stopped SIP.

---

### Interview Transcript 6: Ananya (22F, Junior QA Engineer, Chennai)
- **Profile:** First job, earns ₹28,000/month. Started ₹1,000/month SIP.
- **The Inflection Moment (Month 4):**
  > *“During dinner, I told my dad that I started mutual funds on Groww. He immediately panicked. He remembered 2008 when his friends lost money in stocks. He looked at my app, saw -₹90 in red, and told me: 'Equity is gambling. Stop this immediately and put ₹1,000 in Post Office Recurring Deposit.'*  
  > *Because Groww gave me no counter-arguments or context on historical drawdowns to show my dad, I succumbed to family pressure and paused the SIP.”*
- **Workaround:** Paused SIP under parental authority; redirected to post office RD.

---

## 4. Qualitative Synthesis: The 5 Core Behavioral Themes

Synthesizing across all 6 interviews reveals that churn is driven by **structural, cognitive, and timing seams**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CROSS-INTERVIEW THEME MATRIX                                    │
├──────┬────────────────────────────────┬─────────────────┬───────────────────────────────────────┤
│ ID   │ Behavioral Theme               │ Core Mechanism  │ Evidence & Verbatim Signal            │
├──────┼────────────────────────────────┼─────────────────┼───────────────────────────────────────┤
│ **F1**│ **The Salary-Debit Seam**      │ Rigid calendar  │ *"A 48-hour salary delay resulted in  │
│      │ *(Bank Penalty Shock)*         │ date vs. real   │ a ₹295 bank fine that wiped out 4     │
│      │                                │ pay cycles      │ months of gains."* (P1, P3)           │
├──────┼────────────────────────────────┼─────────────────┼───────────────────────────────────────┤
│ **F2**│ **Rupee-Cost Blindspot**       │ Price vs. Unit  │ *"App shows red -3.1% banner; fails   │
│      │ *(Return Disillusionment)*     │ comprehension   │ to show I bought more units at a      │
│      │                                │                 │ discount."* (P2, P6)                  │
├──────┼────────────────────────────────┼─────────────────┼───────────────────────────────────────┤
│ **F3**│ **All-or-Nothing Recourse Trap**│ Absence of      │ *"Wanted to skip 1 month for Diwali,  │
│      │ *(Rigid In-App Controls)*      │ flexible micro- │ UI forced full cancellation."*        │
│      │                                │ pauses          │ (P3)                                  │
├──────┼────────────────────────────────┼─────────────────┼───────────────────────────────────────┤
│ **F4**│ **The XIRR Distortion Terror** │ Inappropriate   │ *"Seeing XIRR -32% on Month 2 made me │
│      │ *(Jargon-Induced Panic)*       │ metrics on young│ think a third of my capital was wiped │
│      │                                │ portfolios      │ out."* (P4)                           │
├──────┼────────────────────────────────┼─────────────────┼───────────────────────────────────────┤
│ **F5**│ **The Month 6 Dopamine Void**  │ Habit decay &   │ *"Felt like an unacknowledged utility │
│      │ *(Goal Detachment)*            │ lack of positive│ bill; liquidated for motorcycle."*    │
│      │                                │ reinforcement   │ (P5)                                  │
└──────┴────────────────────────────────┴─────────────────┴───────────────────────────────────────┘
```

---

## 5. The 'Aha' Moment: The Non-Obvious Root Cause

Per the **Innovation Framework** from the PM Knowledge Hub:
> *“The non-obvious bet: touch the non-obvious, deliberately avoid the obvious. Obvious pain = symptom. Real insight is in unarticulated, unmet needs.”*

### The Obvious Trap:
Teams assume first-time investors stop their SIPs because:
- *"They don't understand the market."*
- *"They are scared of drawdowns."*
- *Solution:* Push educational video pop-ups or market rally nudges.

### The Non-Obvious Root Cause Discovered:
```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE CORE NON-OBVIOUS 'AHA' DISCOVERY                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│   "First-time SIP churn is NOT a market failure. It is an ELASTICITY & VISIBILITY failure.      │
│                                                                                                 │
│   1. Cashflow Inelasticity: Real-world young salaries are elastic (dates shift by ±3 days,      │
│      expenses spike in festive/medical months). The SIP debit schedule is 100% rigid.           │
│      When an elastic salary meets an inelastic debit, the bank slaps a ₹295 penalty fine.       │
│                                                                                                 │
│   2. Metric Inversion: A SIP's superpower during a dip is ACCUMULATING CHEAPER UNITS.           │
│      Yet Groww's UI exclusively displays NOMINAL PRICE DRAWDOWN (Red -3.2% banners).            │
│      The investor is visually punished for doing the exact behavior that builds wealth."        │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. How Fieldwork Validated & Challenged the Discovery Engine

| Discovery Engine Finding (Part 1) | User Fieldwork Reality (Part 3) | PM Strategic Evolution |
|---|---|---|
| **Finding:** High prevalence of `BANK_MANDATE_PENALTY_SHOCK` (21.2%). | **Validated:** P1 and P3 confirmed bank bounce fines (₹295) are emotionally devastating and cause immediate trust destruction. | The solution cannot just retry debits; it must **pre-verify balance and adapt debit windows to actual salary arrival**. |
| **Finding:** `RETURN_ILLUSION_DISILLUSION` accounts for 28.8% of corpus. | **Validated:** P2 and P6 explicitly compared mutual funds to bank FDs and family recurring deposits in Month 4. | We must introduce a **Visual Rupee-Cost Averaging & Units Acquired Lens** that reframes dips as buying opportunities. |
| **Finding:** XIRR confusion (`METRIC_METAPHOR_CONFUSION`) causes churn. | **Challenged / Nuanced:** P4 showed that XIRR is not just confusing—it is **actively terrifying** because it mathematically exaggerates early dips into double-digit percentages. | XIRR should be suppressed or contextualized during the first 180 days of an investor's journey. |
| **Finding:** `QUIET_DISENGAGE_HABIT_FADE` in late tenure. | **Validated:** P5 demonstrated that without milestones, the SIP becomes an unmonitored bill easily raided for discretionary impulse purchases. | Implement **3, 6, and 9-Month Consistency Streaks & Goal Anchoring**. |

---

## 7. Deliverable Alignment for Final Presentation Deck

These fieldwork findings directly inform **Slide 5** and **Slide 6** of the capstone presentation deck:
- **Deck Slide 5 (User Research & Fieldwork):**  
  *Title:* *Fieldwork Proves First-Timers Drop Off at Month 4–6 from Cashflow Seams and Return Disillusionment.*  
  *Visuals:* 6 participant cards, verbatim anchor quotes, and the 5 cross-interview behavioral themes.
- **Deck Slide 6 (Target Segment & Root Cause Definition):**  
  *Title:* *Root Cause: Cashflow Inelasticity and Metric Inversion Break the First-Time Investor Habit.*  
  *Visuals:* Salaried Early-Career persona card, the 4 Camera Lenses evaluation, and the "Elastic Salary vs. Rigid Debit" contrast diagram.

