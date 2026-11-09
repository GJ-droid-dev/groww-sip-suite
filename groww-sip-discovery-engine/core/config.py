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

# Directory Structure with robust fallback for Cloud / Local execution
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT2_DIR = BASE_DIR.parent

if (PROJECT2_DIR / "data").exists():
    DATA_DIR = PROJECT2_DIR / "data"
elif (BASE_DIR / "data").exists():
    DATA_DIR = BASE_DIR / "data"
else:
    DATA_DIR = PROJECT2_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
BENCHMARK_DIR = DATA_DIR / "benchmark"
OUTPUTS_DIR = DATA_DIR / "outputs"
DOCS_DIR = PROJECT2_DIR / "Docs" if (PROJECT2_DIR / "Docs").exists() else BASE_DIR / "Docs"

# Ensure runtime directories exist
for p in [RAW_DATA_DIR, PROCESSED_DATA_DIR, BENCHMARK_DIR, OUTPUTS_DIR, DOCS_DIR]:
    p.mkdir(parents=True, exist_ok=True)
