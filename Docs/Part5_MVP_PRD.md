# Product Requirements Document (PRD) — Part 5: Groww PulseSIP (AI-Native MVP)

**Product:** Groww Mutual Funds & First-Time Investor Experience (Growth Team)  
**MVP Name:** **Groww PulseSIP — AI-Powered Cashflow Synchronizer & Unit Accumulator**  
**Document:** Product Requirements Document & Engineering Specification (`Project2/Docs/Part5_MVP_PRD.md`)  
**Methodology Standard:** NextLeap PM Fellowship Capstone Guidelines (Part 5)  
**Regulatory & Compliance Anchor:** SEBI Investment Advisers Regulations (100% Zero Specific Fund/Stock Recommendations, Zero FOMO/Urgency Nudges).  
**Core Deliverables:** Slide 7 (*Solution Rationale*) and Slide 8 (*MVP & User Testing*) of Capstone 10-Slide Deck.

---

## 1. Executive Summary & Product Vision

### 1.1 The Product in One Sentence
**Groww PulseSIP is an eval-gated AI companion that protects first-time investors from dropping out by dynamically flexing SIP commitments during seasonal cash crunches and reframing market drawdowns into visual unit accumulation.**

### 1.2 The Problem It Solves
Our Discovery Engine (891 records) and Qualitative Research ($n=6$) revealed that first-time investors abandon their SIPs primarily between **Months 4 and 6** due to two structural seams:
1. **Cashflow Inelasticity:** Salaries fluctuate by $\pm 3\text{ days}$ and seasonal cash crunches (festivals, rent, travel) strike, but SIP deductions are 100% rigid. Clash results in **₹295 bank NACH bounce fines** or forced cancellations.
2. **Metric Inversion:** When markets dip, Groww's UI exclusively displays alarming red nominal losses, concealing the mathematical superpower of a SIP: **buying more units at a discount**.

### 1.3 High-Level Solution Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                GROWW PULSESIP HYBRID ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  [USER INTENT / CONVERSATION]                [GROWW PORTFOLIO & RAILS]                          │
│  "Salary came 2 days late"                   Active SIP: ₹5,000/mo (Debit: 5th)                 │
│  "Diwali shopping, need cash"                Current Value: ₹19,815 (-₹185 in red)              │
│                           │                                  │                                  │
│                           ▼                                  ▼                                  │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    LAYER 1: PULSESIP INTENT & RECOGNITION ENGINE                          │  │
│  │  • Natural language parsing of cashflow distress, salary shifts, and return panic         │  │
│  │  • Contextual mapping: Salary Date Drift | Seasonal Squeeze | Drawdown Disillusion        │  │
│  └─────────────────────────────────────────────┬─────────────────────────────────────────────┘  │
│                                                │                                                │
│                                                ▼                                                │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    LAYER 2: EVAL-GATED COMPLIANCE & SAFETY FILTER                         │  │
│  │  • Gate 1: Zero-Stock/Fund Advice Check (SEBI compliance audit)                           │  │
│  │  • Gate 2: Mathematical Unit Accumulation Verification                                    │  │
│  │  • Safe Fallback: Declines speculative stock tips; redirects to discipline & habit rules  │  │
│  └─────────────────────────────────────────────┬─────────────────────────────────────────────┘  │
│                                                │                                                │
│                                                ▼                                                │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    LAYER 3: WORKFLOW EXECUTION & VISUAL LENS                              │  │
│  │  [Action A: Smart Flex & Defer]           [Action B: Unit Accumulation Lens]              │  │
│  │  • 1-Tap temporary amount dial-down       • Computes bonus units acquired at dip NAV      │  │
│  │    (₹5,000 → ₹1,500 for Diwali)           • Replaces red panic with discount insight      │  │
│  │  • 48-hr salary synchronization           • Habit Streak milestone badge (+Partner perk)  │  │
│  └───────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Where AI Genuinely Earns Its Place

Per capstone requirements, an AI-native product must prove **why a non-AI version falls short** and **where intelligence genuinely creates value**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              WHERE AI GENUINELY EARNS ITS PLACE                                 │
├───────────────────────────────┬───────────────────────────────┬─────────────────────────────────┤
│ Dimension                     │ Traditional Static UI (Non-AI)│ Groww PulseSIP (AI-Native)      │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────────────┤
│ **Cashflow Distress**         │ Rigid dropdowns: "Cancel SIP" │ Parses unstructured real-world  │
│                               │ or "Pause for 3 Months". 60%  │ human distress ("salary delayed │
│                               │ abandon and delete mandate.   │ by holiday", "Diwali crunch")   │
│                               │                               │ into instant 1-tap micro-flex.  │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────────────┤
│ **Drawdown Interpretation**   │ Rigid mathematical output:    │ Synthesizes personalized rupee- │
│                               │ -₹185 (-3.1%) in screaming    │ cost averaging context: shows   │
│                               │ red font. Amplifies fear.     │ exactly how many bonus units    │
│                               │                               │ were accumulated at a discount. │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────────────┤
│ **Regulatory Safety Gate**    │ Dumb static disclaimer        │ Real-time semantic inspection   │
│                               │ at bottom of screen.          │ that intercepts speculative     │
│                               │                               │ questions and executes a safe   │
│                               │                               │ compliance fallback.            │
├───────────────────────────────┼───────────────────────────────┼─────────────────────────────────┤
│ **Cognitive Adaptability**    │ One-size-fits-all statements. │ Adapts tone to first-timer      │
│                               │ User overwhelmed by XIRR.     │ anxiety; strips jargon.         │
└───────────────────────────────┴───────────────────────────────┴─────────────────────────────────┘
```

---

## 3. Core Feature Specifications

### 3.1 Feature 1: Smart Flex-SIP (Cashflow Elasticity)
- **User Problem:** Salaried users face temporary cash crunches (Diwali, medical, travel) or 48-hour salary delays. Fixed deductions trigger ₹295 bank penalties or force permanent cancellation.
- **Workflow:**
  1. User indicates cashflow constraint in natural language or via 1-click preset (*"Tight on cash this month"*).
  2. PulseSIP parses the request and presents **two safe, non-destructive options**:
     - **Option A (Micro-Flex):** Temporarily lower this single installment (e.g. pay ₹1,500 instead of ₹5,000) while keeping the mandate intact and maintaining the habit streak.
     - **Option B (Salary-Sync Snooze):** Defer debit date by 3 to 7 days to align with actual salary credit.
  3. Mandate executes seamlessly on the new schedule without bank return fees.

### 3.2 Feature 2: Visual Unit Accumulator (Metric Inversion Fix)
- **User Problem:** During market dips, dashboard shows alarming red numbers (`-₹185`, `-3.1%`), triggering family pressure to flee to Fixed Deposits.
- **Workflow:**
  1. When NAV declines, PulseSIP activates the **"Unit Accumulator Lens"**.
  2. Calculates:
     $$\text{Bonus Units Acquired} = \left(\frac{\text{SIP Amount}}{\text{Current Lower NAV}}\right) - \left(\frac{\text{SIP Amount}}{\text{Previous Higher NAV}}\right)$$
  3. Displays positive cognitive framing:
     > *"Market Dip Advantage: Your ₹5,000 bought **14.8 units** this month at ₹337/unit vs. 13.7 units at ₹365/unit last month. You accumulated **+1.1 bonus units at an 8% discount**."*
  4. Explicitly reframes price volatility from a "capital loss" into a "discount shopping event" for long-term wealth.

### 3.3 Feature 3: Habit Streaks & Milestone Rewards
- **User Problem:** Investing is a delayed-gratification slog. By Month 6, silent disengagement sets in.
- **Workflow:**
  1. Celebrates uninterrupted investing streaks at **Month 3 (Bronze)**, **Month 6 (Silver — The Inflection)**, and **Month 9 (Gold)**.
  2. Unlocks tangible, universal partner rewards (e.g., Zomato/Swiggy voucher, flight/hotel discount) to inject dopamine and positive reinforcement.

---

## 4. Eval-Gated Architecture & Safe Fallbacks

To ensure institutional safety and strict SEBI compliance, every user interaction passes through a **Dual-Layer Evaluation Gate**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                EVAL-GATED QUALITY ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  [User Query / Action]                                                                          │
│         │                                                                                       │
│         ▼                                                                                       │
│  [EVAL GATE 1: Zero-Advice Audit] ──► (Detects stock/fund picking intent)                        │
│         │                                   │                                                   │
│         │ (Passed - No advice)              ▼ (Violation detected)                              │
│         │                           [SAFE FALLBACK TRIGGERED]                                   │
│         │                           • Declines to recommend funds or stocks                     │
│         │                           • Cites SEBI Investment Adviser regulations                 │
│         │                           • Redirects to index principles & discipline                │
│         ▼                                                                                       │
│  [EVAL GATE 2: Mathematical Truth] ──► (Verifies unit formulas & mandate dates)                 │
│         │                                                                                       │
│         ▼                                                                                       │
│  [Render Safe, Verified Response] + [Mandatory Non-Advice Disclaimer]                           │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Safe Fallback Policies:
1. **Speculative Stock / Fund Picking Queries:**  
   - *Trigger:* User asks: *"Should I stop this fund and buy Tata Motors or Small Cap instead?"*  
   - *Safe Fallback Output:* *"Groww PulseSIP cannot provide specific fund or stock recommendations. Under SEBI regulations, scheme selection depends on your individual risk profile. We recommend focusing on consistent monthly asset allocation rather than chasing short-term sector trends."*
2. **Extreme Panic / Crisis Queries:**  
   - *Trigger:* User demands to redeem everything due to international war news or crash panic.  
   - *Safe Fallback Output:* Explains historical market drawdowns objectively without making market predictions; displays the 1-tap option to temporarily pause rather than irreversibly liquidate.

---

## 5. Technical Stack & Deployment Specification

- **Frontend & App Interface:** Streamlit (Python 3.12) with custom Groww theme styling (`.streamlit/config.toml`).
- **AI Engine:** Google Gemini 3.8 Flash (`google-genai` SDK) utilizing Pydantic structured output schemas (`types.GenerateContentConfig`).
- **Simulation Sandbox:** Interactive controls allowing mentors/evaluators to trigger:
  - Scenario 1: Salary Date Delay (+3 days)
  - Scenario 2: Seasonal Cash Crunch (Diwali Shopping)
  - Scenario 3: Market Dip (-3.5% Drawdown)
- **Deployment Platform:** Streamlit Community Cloud (via GitHub repository `groww-sip-mvp`).
- **Local URL:** `http://localhost:8502`

