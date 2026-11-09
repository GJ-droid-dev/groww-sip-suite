# Groww: 12-Month Mutual Fund SIP Continuation Suite 🌱

An AI-native behavioral intelligence and product intervention platform engineered to eliminate the Month 4–6 drop-off cliff for first-time mutual fund investors on **Groww**.

---

## 🌟 Modules Included

### 1. 🚀 Groww PulseSIP (AI Growth MVP)
- **Salary-Sync Liquidity Guard:** Pre-debit balance sensing prevents ₹295 bank NACH bounce fees.
- **1-Tap Seasonal Micro-Flex:** Flexes instalment to ₹500 AMC floor or shifts debit date by ±4 days without cancelling mandates.
- **Unit Accumulation & NAV Discount Tracker:** Replaces alarming red negative return banners with tangible asset acquisition insights.
- **SEBI-Compliant Zero-Advice Conversational AI:** Deterministic regex evaluation gate (`eval_gate.py`) enforces strict SEBI RIA zero-recommendation compliance.

### 2. 🔬 Groww SIP AI Discovery Engine
- **Corpus Intelligence:** 891 deduplicated, normalized, PII-scrubbed records from Reddit r/personalfinanceindia, Google Play, App Store, and forums.
- **7-Category Lapse Taxonomy:** Empirical breakdown of why first-time investors churn.
- **Golden Benchmark Evaluation:** 20-record test set evaluated against Gemini 3.8 Flash with 100% agreement ($\kappa = 1.000$).
- **Live Diagnostic Sandbox:** Real-time analysis of investor sentiment and churn propensity.

---

## 🚀 One-Click Hosting on Streamlit Community Cloud

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Deploy Groww SIP Suite to Streamlit Cloud"
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/groww-sip-suite.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Click **New app**.
3. Fill in the deployment details:
   - **Repository:** `<YOUR_GITHUB_USERNAME>/groww-sip-suite`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Advanced settings** ➔ **Secrets**.
5. Paste your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key-here"
   ```
6. Click **Deploy!**

---

## 💻 Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the unified portal
streamlit run app.py

# Or run standalone modules
streamlit run groww-sip-mvp/app.py
streamlit run groww-sip-discovery-engine/app.py
```

