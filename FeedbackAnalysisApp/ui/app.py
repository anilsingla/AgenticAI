"""
FE-01: Streamlit app main entry point with sidebar navigation.
Run with: streamlit run ui/app.py
"""

import importlib
import sys
from pathlib import Path

import streamlit as st

# Ensure project root is on sys.path so config/agents imports work.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(
    page_title="SignalDesk - Feedback Analysis",
    page_icon=":clipboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = {
    "Dashboard": "pages.dashboard",
    "Run Pipeline": "pages.run_pipeline",
    "Flow Explorer": "pages.flow_explorer",
    "Manual Override": "pages.manual_override",
    "Analytics": "pages.analytics",
    "Processing Log": "pages.processing_log",
    "Configuration": "pages.configuration",
    "Product Docs": "pages.product_docs",
}

st.sidebar.title("SignalDesk")
st.sidebar.caption("Agentic Feedback Operations")
st.sidebar.divider()
selection = st.sidebar.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")

module_name = PAGES[selection]
full_module = f"ui.{module_name}"
try:
    page_module = importlib.import_module(full_module)
    page_module.render()
except Exception as e:
    st.error(f"Failed to load page **{selection}**: {e}")
    st.exception(e)

