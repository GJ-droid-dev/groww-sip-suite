import os
from pathlib import Path
from dotenv import load_dotenv

# Search for .env in current directory and parent directories up to workspace root
current_path = Path(__file__).resolve()
search_dir = current_path
while search_dir != search_dir.parent:
    env_file = search_dir / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        break
    search_dir = search_dir.parent

# Resolve API Key from Streamlit Secrets (for Streamlit Cloud) or os.environ
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
try:
    import streamlit as st
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

DEFAULT_MODEL = "gemini-3.8-flash"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
