"""
app.py - Groww PulseSIP: AI-Native Cashflow Synchronizer & Unit Accumulator MVP.
NextLeap PM Fellowship Capstone | Growth Team @ Groww
"""

import sys
from pathlib import Path
import json
import streamlit as st
import pandas as pd
import altair as alt

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from mvp_core.schemas import PortfolioState, AssistantResponse
from mvp_core.assistant import PulseSIPEngine

try:
    st.set_page_config(
        page_title="Groww PulseSIP | AI-Native Growth MVP",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except Exception:
    pass

# Custom Styling mimicking Groww's modern clean interface
st.markdown("""
<style>
    .groww-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-streak {
        background-color: #FEF3C7;
        color: #92400E;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 13px;
        display: inline-block;
    }
    .badge-eval-pass {
        background-color: #DCFCE7;
        color: #166534;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
    }
    .badge-eval-fail {
        background-color: #FEE2E2;
        color: #991B1B;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
    }
    .unit-box {
        background-color: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 14px 16px;
        border-radius: 6px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_engine():
    return PulseSIPEngine()


def load_initial_portfolio() -> PortfolioState:
    data_file = BASE_DIR / "data" / "mock_portfolio.json"
    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            return PortfolioState.model_validate_json(f.read())
    return PortfolioState()


# Initialize session state
if "portfolio" not in st.session_state:
    st.session_state.portfolio = load_initial_portfolio()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "action_confirmed" not in st.session_state:
    st.session_state.action_confirmed = None

engine = get_engine()
p = st.session_state.portfolio

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
        <div style="background-color: #00D09C; width: 28px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 16px;">G</div>
        <span style="font-size: 24px; font-weight: 800; color: #1E222B; letter-spacing: -0.5px;">GROWW</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### **PulseSIP Companion**")
    st.caption("**Growth Team · AI-Native MVP (Part 5)**")
    st.markdown("---")

    st.markdown("#### 🧪 Evaluator Simulation Sandbox")
    st.caption("Click any preset below to simulate realistic user friction:")

    sim_query = None
    if st.button("⚡ Salary Delayed by 3 Days"):
        sim_query = "My company delayed salary to the 8th due to bank holiday. My debit is on the 5th, will it bounce?"
    if st.button("🪔 Diwali Cash Crunch (Need ₹4,000)"):
        sim_query = "I have high festive expenses for Diwali this month. Can I contribute less than ₹5,000 for just this one cycle?"
    if st.button("📉 Market Dip Anxiety (-3.5%)"):
        sim_query = "My portfolio is red and Nifty fell 3.5%. My father told me to stop mutual funds and start an FD. What should I do?"
    if st.button("🛑 Test: Solicit Stock Advice"):
        sim_query = "Should I stop this mutual fund and buy Tata Motors shares instead? Will it give 20% returns?"

    st.markdown("---")
    if st.button("🔄 Reset Portfolio to Baseline"):
        st.session_state.portfolio = load_initial_portfolio()
        st.session_state.action_confirmed = None
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.caption("🛡️ **Strict SEBI Compliance:** Zero stock/fund recommendations. Zero FOMO nudges.")


# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🌱 Groww PulseSIP — AI Companion")
    st.markdown(f"**Investor:** {p.user_name} · **Tenure:** Month {p.tenure_months} First-Timer · **Status:** `{p.status}`")
with col_h2:
    st.markdown("<div style='text-align: right; margin-top: 15px;'>", unsafe_allow_html=True)
    st.markdown(f"<span class='badge-streak'>🔥 {p.streak_count}-Month {p.streak_tier}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Main Layout
col_left, col_right = st.columns([1.1, 1.2])

# ==============================================================================
# LEFT COLUMN: GROWW INVESTOR DASHBOARD
# ==============================================================================
with col_left:
    st.subheader("📊 Your Investment Overview")

    # Card 1: Fund & Returns
    with st.container():
        st.markdown(f"""
        <div class="groww-card">
            <div style="font-size: 17px; font-weight: 700; color: #1E293B;">{p.scheme_name}</div>
            <div style="color: #64748B; font-size: 13px; margin-bottom: 12px;">Active Monthly SIP · Auto-Debit via {p.linked_bank}</div>
            <div style="display: flex; justify-content: space-between; border-top: 1px solid #F1F5F9; padding-top: 12px;">
                <div>
                    <div style="color: #64748B; font-size: 12px;">TOTAL INVESTED</div>
                    <div style="font-size: 19px; font-weight: 700; color: #0F172A;">₹{p.total_invested:,.0f}</div>
                </div>
                <div>
                    <div style="color: #64748B; font-size: 12px;">CURRENT VALUE</div>
                    <div style="font-size: 19px; font-weight: 700; color: #0F172A;">₹{p.current_value:,.0f}</div>
                </div>
                <div>
                    <div style="color: #64748B; font-size: 12px;">TOTAL RETURN</div>
                    <div style="font-size: 19px; font-weight: 700; color: #DC2626;">{p.nominal_return_abs:+,.0f} ({p.nominal_return_pct:.2f}%)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2: PulseSIP Unit Accumulator Lens
    st.subheader("🔍 PulseSIP Unit Accumulator Lens")
    st.caption("Re-framing price volatility: In a SIP, market dips mean you acquire **more asset units at a discount**.")

    cur_units = p.monthly_installment / p.latest_nav
    prev_units = p.monthly_installment / p.previous_month_nav
    bonus = max(0.0, cur_units - prev_units)
    discount = max(0.0, ((p.previous_month_nav - p.latest_nav) / p.previous_month_nav) * 100.0)

    st.markdown(f"""
    <div class="unit-box">
        <div style="font-weight: 700; color: #166534; font-size: 15px;">✨ Rupee-Cost Averaging Advantage</div>
        <div style="margin-top: 6px; font-size: 13.5px; color: #14532D; line-height: 1.5;">
            While the traditional dashboard highlights a <strong>{p.nominal_return_pct:.2f}% nominal dip</strong>, 
            your monthly ₹{p.monthly_installment:,.0f} acquired <strong>{cur_units:.2f} units</strong> at ₹{p.latest_nav:.1f}/unit 
            (compared to {prev_units:.2f} units last month).<br>
            <strong>You accumulated +{bonus:.2f} bonus units at a {discount:.1f}% discount!</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Card 3: Next Scheduled Debit & Habit Health
    with st.container():
        st.markdown(f"""
        <div class="groww-card">
            <div style="font-weight: 700; font-size: 15px; margin-bottom: 6px;">📅 Next Scheduled Debit</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 20px; font-weight: 800; color: #0072B2;">₹{p.monthly_installment:,.0f} on Nov {p.debit_date}th</div>
                    <div style="font-size: 13px; color: #64748B;">Auto-Pay Status: <strong>Active & Protected</strong></div>
                </div>
                <div>
                    <span class="badge-eval-pass">Zero Bounce Risk</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Card 4: Milestone Tracker
    st.subheader("🏆 Consistency Milestones")
    st.progress(p.streak_count / 12.0)
    st.caption(f"**{p.streak_count} of 12 Months Completed.** (1 Month remaining to unlock Silver Milestone Reward: Zomato Pro Voucher).")


# ==============================================================================
# RIGHT COLUMN: PULSESIP AI ASSISTANT PANEL
# ==============================================================================
with col_right:
    st.subheader("💬 PulseSIP Cashflow & Habit Shield")
    st.caption("Ask questions, sync salary dates, or flex installment amounts during tight months.")

    # Action Confirmation Banner if an action was executed
    if st.session_state.action_confirmed:
        st.success(st.session_state.action_confirmed)

    # Handle simulation input or direct user input
    user_query = st.chat_input("Ask PulseSIP (e.g. 'Salary delayed by 3 days' or 'Can I pay less this month?')")
    if sim_query:
        user_query = sim_query

    if user_query:
        with st.spinner("Evaluating compliance gate & generating assistance..."):
            response: AssistantResponse = engine.respond(user_query, p)
            st.session_state.chat_history.append((user_query, response))

    # Display Chat History & Assistant Responses
    if st.session_state.chat_history:
        for q, resp in reversed(st.session_state.chat_history[-3:]):
            with st.chat_message("user"):
                st.write(q)

            with st.chat_message("assistant"):
                # Compliance Gate Banner
                ev = resp.eval_gate
                badge_class = "badge-eval-pass" if ev.passed else "badge-eval-fail"
                status_text = "🛡️ SEBI Zero-Advice Gate: PASSED" if ev.passed else f"⚠️ Compliance Fallback: {ev.violation_type}"

                st.markdown(f"<span class='{badge_class}'>{status_text}</span>", unsafe_allow_html=True)
                st.caption(f"_{ev.explanation}_")

                st.markdown(resp.user_facing_message)

                if resp.unit_accumulation_insight:
                    st.info(resp.unit_accumulation_insight)

                # Interactive Action Trigger
                if resp.action_type == "FLEX_AMOUNT":
                    amt = resp.action_params.get("recommended_amount", 1500.0)
                    if st.button(f"✅ Confirm Smart Flex: Pay ₹{amt:,.0f} for Nov Cycle", key=f"btn_flex_{q[:10]}"):
                        p.monthly_installment = amt
                        st.session_state.action_confirmed = f"🎉 Smart Flex Activated! Your next debit on Nov {p.debit_date}th is adjusted to ₹{amt:,.0f}. Mandate & 5-month streak preserved!"
                        st.rerun()

                elif resp.action_type == "SNOOZE_DATE":
                    new_d = resp.action_params.get("new_date", p.debit_date + 4)
                    if st.button(f"✅ Confirm Salary-Sync: Defer to Nov {new_d}th", key=f"btn_snooze_{q[:10]}"):
                        p.debit_date = new_d
                        st.session_state.action_confirmed = f"🎉 Salary-Sync Activated! Next debit shifted to Nov {new_d}th. Zero bank penalty bounce risk!"
                        st.rerun()

    else:
        st.info("💡 Try clicking one of the simulator presets on the left sidebar, or type any cashflow or investment query above.")

# Footer Disclaimer
st.markdown("---")
st.caption(
    "⚠️ **SEBI Compliance Disclaimer:** Groww PulseSIP is an educational and behavioral workflow prototype. "
    "It does not provide investment, financial, or stock recommendations. Mutual fund investments are subject to market risks; "
    "read all scheme-related documents carefully."
)

