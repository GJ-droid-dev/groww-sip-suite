"""
app.py - Master Unified Portal: Groww PulseSIP MVP & AI Discovery Engine.
NextLeap PM Fellowship Capstone | Growth Team @ Groww
"""

import sys
import os
from pathlib import Path
import runpy
import streamlit as st

# Root directory configuration
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Master Page Config (Only called once at root level)
try:
    st.set_page_config(
        page_title="Groww 12-Month SIP Continuation Suite",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except Exception:
    pass

# Custom Groww Branding CSS
st.markdown("""
<style>
    .portal-banner {
        background: linear-gradient(90deg, #00D09C 0%, #1E222B 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-weight: 600;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Top Sidebar Navigation
with st.sidebar:
    st.image("https://assets-netstorage.groww.in/web-assets/big_groww_logo.png", width=160)
    st.markdown("### **Groww SIP Retention Suite**")
    st.caption("**12-Month Mutual Fund Continuation · Growth Team**")
    st.markdown("---")
    
    app_choice = st.radio(
        "**Choose Application / Module:**",
        [
            "🚀 Groww PulseSIP (AI Growth MVP)",
            "🔬 SIP AI Discovery Engine"
        ],
        index=0,
        help="Switch between the production-ready PulseSIP intervention MVP and the empirical 891-record Discovery Engine."
    )
    st.markdown("---")

# Execution Dispatcher
if "PulseSIP" in app_choice:
    mvp_dir = BASE_DIR / "groww-sip-mvp"
    if str(mvp_dir) not in sys.path:
        sys.path.insert(0, str(mvp_dir))
    mvp_script = mvp_dir / "app.py"
    runpy.run_path(str(mvp_script), run_name="__main__")

else:
    discovery_dir = BASE_DIR / "groww-sip-discovery-engine"
    if str(discovery_dir) not in sys.path:
        sys.path.insert(0, str(discovery_dir))
    discovery_script = discovery_dir / "app.py"
    runpy.run_path(str(discovery_script), run_name="__main__")
