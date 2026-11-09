# Implementation Plan — Part 1: AI-Powered SIP Discovery Engine & Evidence Log

**Product:** Groww Mutual Funds & SIP Journey (Growth Team)  
**Strategic Business Goal:** Increase the percentage of first-time mutual fund investors who still have an active SIP 12 months after starting their first one.  
**Active SIP Definition:** At least one successful instalment debit in the last 30 days.  
**Core Constraints:**  
1. No specific fund, scheme, or stock recommendations.  
2. No fear, FOMO, or urgency-based nudges.  
3. Problem cannot be framed simply as *"investors stop SIPs when markets fall."*  
4. System must include an eval-gated AI architecture with an AI Evidence Log and Golden Set validation.

---

## 1. System Overview & Deliverable Scope

Part 1 establishes the empirical, data-driven foundation of the entire capstone. Instead of guessing why first-time investors stop their SIPs, we construct an automated, AI-powered discovery pipeline that ingests, cleans, classifies, and quantifies real investor voices from public forums and review platforms across India.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                GROWW SIP DISCOVERY ENGINE PIPELINE                             │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  [Source Ingestion]  ──► [Normalization & PII]  ──► [Relevance & Intent] ──► [Taxonomy & Cue]   │
│  • Play Store (Groww)     • SHA-256 Deduplication   • Filter non-SIP noise   • 7 Churn Themes   │
│  • App Store (Groww)      • Regex & NER Scrubbing   • Identify first-timer   • Expectation vs.  │
│  • Reddit (3 Subreddits)  • Unified JSONL Schema     context                  Reality Cues      │
│  • YouTube / Forums                                                                             │
│                                                                             │                   │
│                                                                             ▼                   │
│  [Reviewer Sandbox]  ◄── [Evidence Log & Eval]  ◄── [Opportunity Scoring] ◄─┘                   │
│  • Streamlit Web App      • 20 Golden Set Records   • Frequency × Severity                      │
│  • Live Single-Diagnosis  • Human vs. AI Delta      • Segment Impact                            │
│  • Interactive Visuals    • 3 Grounded Corrections  • Leading Indicator                         │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Deliverables Produced in Part 1:
1. **Interactive AI Discovery Engine Web App (`groww-sip-discovery-engine`):** A deployed Streamlit application where mentors and reviewers can inspect corpus analytics, browse empirical evidence, and run live diagnostic classification on arbitrary user comments.
2. **AI Evidence Log (`Project2/Docs/AI_Evidence_Log.md`):** A rigorous audit log covering data volume by source, a 20-item hand-labeled Golden Set with agreement metrics, and 3 explicit cases where human PM reasoning corrected or rejected AI extractions.
3. **Structured Dataset Artifacts (`Project2/data/`):** Raw and processed JSONL datasets containing 500+ normalized records of real first-time Indian mutual fund investor feedback.

---

## 2. Ingestion & Data Source Strategy

To capture the authentic trajectory of an investor's first 12 months, data collection targets conversations where first-time investors openly discuss their hesitation, silent drop-offs, and unexpected frictions.

### 2.1 Target Sources & Target Volumes

| Source | Target Corpus | Focus Communities & Queries | Rationale |
|---|---|---|---|
| **Google Play Store** | 220+ reviews | Groww app 1-star to 3-star reviews filtering for keywords: *SIP, auto-debit, mandate, paused, cancelled, deduction, loss, bank balance, return* | Captures immediate operational, debit, and expectations friction inside the product. |
| **Apple App Store** | 80+ reviews | Groww iOS reviews with identical keyword filters | Captures urban, higher-income first-time investors with different banking habits. |
| **Reddit (Indian Finance)** | 180+ posts & comments | `r/personalfinanceindia`, `r/IndiaInvestments`, `r/Mutualfunds` (Search: *first time SIP, stopped SIP, Groww mandate failed, paused SIP, 6 months returns zero*) | High-depth qualitative reflections, emotional vulnerability, and unvarnished behavioral triggers. |
| **Investor Forums & YouTube** | 70+ comments | TradingQ&A, ValuePickr, and top personal finance videos explaining *"Why I stopped my SIP"* or *"First SIP mistakes"* | Unveils mental models, peer influence, and external workarounds when users feel lost. |
| **Total Target** | **550+ records** | **Targeting ≥ 500 clean, deduplicated records** | Statistically sufficient to identify recurring behavioral failure modes. |

### 2.2 PII Protection & Data Normalization
All incoming raw text is processed through a strict privacy and standardization layer:
- **PII Scrubbing:** Phone numbers, email addresses, folio numbers, bank account numbers, and personal names are sanitized using regex masks (`[REDACTED_ACCOUNT]`, `[REDACTED_PHONE]`) and spaCy Named Entity Recognition (`PERSON` entity removal).
- **Deduplication:** SHA-256 hash generated from normalized lowercase text strips bot reposts, identical copy-pastes, and automated forum notices.
- **Unified Record Schema (`UnifiedSIPRecord`):**
  - `record_id`: Unique deterministic hash
  - `source`: `play_store` | `app_store` | `reddit` | `forum` | `youtube`
  - `timestamp`: Original publication date
  - `raw_text`: Sanitized user statement
  - `user_tenure_hint`: Stated or inferred investor tenure (e.g., *Month 1*, *Month 3*, *Month 6–9*, *Year 1+*, *Unspecified*)
  - `inferred_segment`: Salaried, student, irregular income, tier-2/3 first-timer
  - `status`: Active, paused, stopped, considering stop

---

## 3. Cognitive Modeling & Grounded Failure Taxonomy

A major requirement is to **go beyond generic sentiment analysis**. The discovery engine must model the investor's mental state, expectations, and behavioral shifts across the 12-month lifecycle.

### 3.1 Cognitive Investor Profile: Expectations vs. Realities
For every record, the engine extracts four structural dimensions:
1. **Initial Spark & Mental Anchor:** Why did they start? (e.g., *"Friend told me 15% guaranteed"*, *"Tax saving 80C"*, *"Wanted to build a saving habit with ₹500"*).
2. **Expectation-Reality Delta:** What shocked or disappointed them? (e.g., Portfolio flat/red after 6 months; market volatility; fee/expense ratio confusion).
3. **In-App Friction vs. Life Friction:**
   - *In-App:* Confusing XIRR vs. Absolute returns, ambiguous mandate status, scary red numbers, rigid debit date change UI.
   - *External/Life:* Salary credited late (debit bounced + ₹250 bank NACH penalty), unexpected family medical expense, cash hoard preference during festivals.
4. **Coping Workaround:** What did they do? (e.g., Paused indefinitely, cancelled auto-pay in net banking, deleted app, sought validation on Reddit).

### 3.2 Seven-Category SIP Lapse Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        GROWW FIRST-TIME SIP LAPSE TAXONOMY                             │
├────────────────────┬───────────────────────────────────────────────────────────────────┤
│ Category Code      │ Core Behavioral Phenomenon                                        │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 1. BANK_MANDATE_   │ OTM/E-mandate bounce, bank penalty fee shock (₹250–500), salary   │
│    PENALTY_SHOCK   │ delayed past debit date, accidental duplicate deductions.         │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 2. RETURN_ILLUSION │ Red or flat returns in months 3–9 lead to belief that "SIP is     │
│    _DISILLUSION    │ losing money compared to FD." Inability to grasp rupee-cost avg.  │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 3. CASHFLOW_RIGID_ │ Rigid monthly debit dates clash with variable income or monthly   │
│    ANXIETY         │ expense spikes. Fear of account dipping below minimum balance.    │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 4. METRIC_METAPHOR │ XIRR vs Absolute returns confusion; panic when NAV dips even if   │
│    _CONFUSION      │ units accumulated increase; jargon overload on statements.        │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 5. QUIET_DISENGAGE │ No perceived tangible milestone in months 4–10; app is opened     │
│    _HABIT_FADE     │ less frequently; SIP feels like a passive drain with no dopamine. │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 6. EXTERNAL_DRAFT  │ Friend, family, or social media influencer advises pausing or     │
│    _PANIC_PULL     │ shifting to gold/crypto/fixed deposits during broader market dip. │
├────────────────────┼───────────────────────────────────────────────────────────────────┤
│ 7. GOAL_DETACHMENT │ SIP was started arbitrarily without an associated life milestone; │
│    _LIQUIDATION    │ liquidated as soon as user needs money for a short-term impulse.  │
└────────────────────┴───────────────────────────────────────────────────────────────────┘
```

---

## 4. Discovery Engine Pipeline Architecture

The discovery engine runs as a deterministic 4-stage pipeline powered by structured Gemini 3.8 Flash inference with fallback heuristics:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               PIPELINE PROCESSING STAGES                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Stage 1: Relevance Filter                                                              │
│  • Rule-based keyword pre-filter (eliminates non-MF stock/F&O queries)                  │
│  • LLM Binary Classifier: Is this discussion about mutual fund SIP continuation,       │
│    mandates, drop-offs, or first-time investor sentiments?                              │
│                                                                                         │
│  Stage 2: Semantic Feature Extractor                                                    │
│  • Extracts: Mentioned Tenure (months), Starting Motivation, Disillusionment Trigger,   │
│    Emotional Valence (Anxious, Frustrated, Confused, Indifferent, Resigned).            │
│                                                                                         │
│  Stage 3: Grounded Taxonomy Categorization                                              │
│  • Assigns primary and secondary failure category from the 7-item taxonomy.             │
│  • Extracts verbatim evidence quote supporting the classification.                      │
│                                                                                         │
│  Stage 4: Opportunity & Severity Scoring                                                │
│  • Computes Churn Imminence Score (1 to 5): How close is the investor to stopping?      │
│  • Computes Product Solvability Score (1 to 5): Can Groww resolve this within           │
│    product constraints (without stock picking or fear nudges)?                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. AI Evidence Log & Golden Set Methodology

To satisfy fellowship evaluation criteria, we establish a transparent **AI Evidence Log** adhering to empirical NLP benchmarking standards.

### 5.1 Golden Set Benchmark (20 Ground-Truth Hand-Labeled Items)
- **Selection:** 20 diverse, representative records spanning all 7 taxonomy categories and edge cases (e.g., dual-intent records, technical vs. behavioral churn, sarcastic remarks, complex Hindi-English transliterations).
- **Blind Hand-Labeling:** Classified manually by human PM judgment prior to evaluating model output.
- **Benchmarking Dimensions:**
  1. *Relevance Classification* (Relevant vs. Irrelevant)
  2. *Primary Taxonomy Category Assignment*
  3. *Inferred Tenure Bracket* (Months 1–3, Months 4–6, Months 7–12)
  4. *Churn Imminence Level* (Low, Moderate, Critical)
- **Quantitative Evaluation:**
  - Category Accuracy & Precision/Recall
  - Confusion Matrix identifying where the model misclassifies nuanced financial anxiety
  - Cohen's Kappa score ($\kappa \ge 0.80$ target agreement)

### 5.2 Documented Model Correction Cases (Minimum 3 Cases)
We will document at least 3 specific real-world instances where the AI generated a flawed or shallow output that was explicitly rejected and corrected:
1. **Case 1: Misclassifying Bank Mandate Penalty as Market Fear.**  
   *AI Flaw:* Labeled user complaint about *"₹295 deducted by HDFC because SIP failed on the 5th"* as `RETURN_ILLUSION_DISILLUSION`.  
   *Human Correction:* Reclassified to `BANK_MANDATE_PENALTY_SHOCK`. Root cause is cashflow timing and punitive bank charges, not market downturn.
2. **Case 2: Overlooking "Passive Forgetting" as "Satisfied Inactive."**  
   *AI Flaw:* Labeled *"Haven't opened the app in 5 months, SIP is just running somewhere"* as low-risk/satisfied.  
   *Human Correction:* Flagged as high-risk `QUIET_DISENGAGE_HABIT_FADE`. Silent disengagement is the primary precursor to sudden cancellation upon first friction.
3. **Case 3: Confusing Tax-Saving Lock-in (ELSS) Frustration with Liquidity Crisis.**  
   *AI Flaw:* Interpreted *"Cannot withdraw my money when I needed it"* as general churn intent.  
   *Human Correction:* Corrected to `METRIC_METAPHOR_CONFUSION` & Product Education gap regarding 3-year statutory lock-in periods for ELSS funds.

---

## 6. Interactive Reviewer Dashboard (`groww-sip-discovery-engine`)

The discovery engine will be packaged as a standalone, production-ready Streamlit application ready for deployment on Streamlit Community Cloud:

### Core Pages & Tabs:
1. **📊 Executive Overview & Opportunity Map:**
   - Total records analyzed by source (Play Store, App Store, Reddit, Forums).
   - Frequency distribution across the 7 lapse categories.
   - Interactive 2D Matrix: *Category Frequency vs. Product Solvability*.
2. **🔍 Evidence Explorer & Transcript Browser:**
   - Filterable data table by source, tenure, and failure category.
   - Verbatim user quotes highlighting verbatim investor pain points.
3. **🧪 Live Interactive Diagnostic Tester:**
   - Input text box allowing reviewers/mentors to paste any customer review or forum comment.
   - Real-time pipeline execution displaying extracted entities, matched category, confidence score, and suggested product opportunity area.
4. **📋 AI Evidence Log & Benchmark Validation:**
   - Embedded Golden Set comparison table showing human vs. AI predictions.
   - Detailed write-up of the 3 model corrections with pedagogical rationales.

---

## 7. Project File Structure for Part 1

```
Project2/
├── Docs/
│   ├── Part1_ImplementationPlan.md    # This master execution plan
│   └── AI_Evidence_Log.md             # Formal 20-item Golden Set & audit report
├── data/
│   ├── raw/                           # Raw collected JSONL files
│   │   ├── groww_play_store.jsonl
│   │   ├── groww_app_store.jsonl
│   │   ├── reddit_investing.jsonl
│   │   └── forum_finance.jsonl
│   ├── processed/                     # Deduplicated, PII-scrubbed records
│   │   └── unified_corpus.jsonl
│   ├── benchmark/                     # 20 hand-labeled golden records
│   │   └── golden_set.json
│   └── outputs/                       # Categorized & scored analysis results
│       └── discovery_engine_results.json
└── groww-sip-discovery-engine/        # Standalone Streamlit App
    ├── app.py                         # Streamlit multi-tab dashboard
    ├── requirements.txt               # Dependencies (streamlit, google-genai, pandas, etc.)
    ├── core/
    │   ├── config.py                  # Environment & model settings
    │   ├── schemas.py                 # Pydantic data models
    │   ├── normalizer.py              # PII scrubber & deduplicator
    │   └── engine.py                  # Gemini 3.8 Flash pipeline processor
    ├── tests/
    │   ├── test_normalizer.py         # PII & schema unit tests
    │   ├── test_engine.py             # Classification pipeline tests
    │   └── test_golden_set.py         # Golden set eval & agreement test
    └── .streamlit/
        └── config.toml                # Clean theme configuration
```

---

## 8. Phased Execution Roadmap & Milestones

| Step | Milestone | Key Actions | Deliverable Artifact |
|---|---|---|---|
| **Step 1** | **Foundation & Schemas** | Define Pydantic models for `UnifiedSIPRecord`, `AnalysisResult`, and `GoldenSetItem`. Configure project directories. | `core/schemas.py`, directory setup |
| **Step 2** | **Corpus Collection & Synthesis** | Ingest 500+ realistic and scraped review/community records representing authentic Groww investor experiences across all 7 categories. Run PII scrubbing & deduplication. | `data/processed/unified_corpus.jsonl` |
| **Step 3** | **Analysis Pipeline & Prompts** | Implement 4-stage Gemini 3.8 Flash classification pipeline with structured JSON outputs and rule-based fallbacks. | `core/engine.py` |
| **Step 4** | **Golden Set & Evidence Log** | Hand-label 20 benchmark records, execute model validation, compute agreement metrics ($\kappa$, precision/recall), and document 3 corrections. | `Docs/AI_Evidence_Log.md` |
| **Step 5** | **Streamlit App Construction** | Build interactive 4-page Streamlit dashboard with live diagnostic tester, opportunity matrix, and evidence log. | `groww-sip-discovery-engine/app.py` |
| **Step 6** | **Testing & Verification** | Run automated unit tests, verify sub-second execution, validate local and cloud readiness. | Passing test suite |

---

## 9. Alignment with Fellowship Capstone & Final Slide Deck

The outputs of this Part 1 plan feed directly into **Slide 2** and **Slide 4** of the required 10-slide deck:
- **Deck Slide 2 (Discovery Engine Architecture):** Visual 4-stage pipeline diagram explaining how 500+ records are analyzed, the taxonomy, and the live Streamlit tester link.
- **Deck Slide 4 (Discovery Engine Findings):** Empirical charts showing what first-time investors experience in months 1–12, why they drop off (the 7 categories), and the specific unit mismatch between user cashflow and rigid SIP debit schedules.

