import streamlit as st
from src.components.header import _logo

def _render_footer():
    html = f"""
    <div style="margin-top:3.5rem; text-align:center; padding:1.8rem 0 1rem 0; border-top:1px solid #E2E8F0;">
        <div style="display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:4px;">
            {_logo(24)}
            <span style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:0.95rem; color:#0F172A; letter-spacing:0.02em;">PRESENT CALL</span>
        </div>
        <p style="font-family:'Inter', sans-serif; font-size:0.8rem; color:#64748B; margin:2px 0 6px 0;">
            AI-powered attendance management system · Institutional Enterprise Edition
        </p>
        <div style="font-size:0.75rem; color:#94A3B8;">
            © Present Call · Designed for modern academic and enterprise institutions
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def footer_home():
    _render_footer()


def footer_dashboard():
    _render_footer()
