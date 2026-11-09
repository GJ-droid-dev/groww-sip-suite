# Streamlit Community Cloud Deployment Guide

This guide walks you through deploying the **Groww SIP Discovery Engine & PulseSIP MVP** to **Streamlit Community Cloud** (free hosting).

---

## Prerequisites
1. A free [GitHub](https://github.com/) account.
2. A free [Streamlit Community Cloud](https://share.streamlit.io/) account (sign in with your GitHub).
3. A Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).

---

## Step 1: Create a GitHub Repository
1. Log in to [GitHub](https://github.com/) and click **New Repository** (or visit `https://github.com/new`).
2. Repository name: `groww-sip-suite` (or your preferred name).
3. Visibility: **Public** (or Private if your Streamlit Cloud account allows private repos).
4. Do **not** initialize with README, .gitignore, or license (we already have them).
5. Click **Create repository**.

---

## Step 2: Push Local Code to GitHub
Open PowerShell in `c:\Users\jangr\Documents\NextLeap\Project\Project2` and run:

```powershell
cd c:\Users\jangr\Documents\NextLeap\Project\Project2

# Initialize git if not already initialized
git init

# Add all files
git add .

# Create initial commit
git commit -m "Groww SIP Continuation: PulseSIP MVP & Discovery Engine"

# Set branch to main
git branch -M main

# Link to your remote GitHub repo (replace <USERNAME> and <REPO>)
git remote add origin https://github.com/<USERNAME>/groww-sip-suite.git

# Push to GitHub
git push -u origin main
```

---

## Step 3: Deploy on Streamlit Community Cloud
1. Navigate to [share.streamlit.io](https://share.streamlit.io).
2. Click **New app** (top right).
3. Fill in the fields:
   - **Repository:** `<USERNAME>/groww-sip-suite`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (optional):** e.g., `groww-pulsesip.streamlit.app`
4. Click **Advanced settings...** at the bottom.
5. In the **Secrets** text box, enter:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
   *(Paste your actual Gemini API Key from Google AI Studio)*
6. Click **Save** then **Deploy!**

---

## Step 4: Verification & Live Use
- Streamlit Cloud will automatically install packages from `requirements.txt`.
- Within 1–2 minutes, your live app will launch at `https://<your-app-name>.streamlit.app`.
- The sidebar allows any reviewer or evaluator to toggle between:
  1. **Groww PulseSIP (AI Growth MVP)**: Live portfolio, unit discount reframing, 1-tap micro-flex, and SEBI-compliant assistant.
  2. **Groww SIP AI Discovery Engine**: 891 review corpus explorer, 7-mode taxonomy, and Golden Benchmark evaluation.

