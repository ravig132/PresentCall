import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.system_bar import render_system_bar

LANDING_PAGE_URL = "https://present-call.vercel.app/"

def top_navbar():
    """
    Persistent enterprise navigation bar.
    Renders:
    1. The Deep Navy sidebar navigation (st.sidebar)
    2. The Top System Bar (🔒 app.presentcall.ai — Production Attendance Hub)
    """
    # 1. Render the professional deep navy sidebar
    render_sidebar()

    # 2. Render top production system status bar
    render_system_bar()
