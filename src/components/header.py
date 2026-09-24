import streamlit as st
from src.ui.base_layout import theme_colors

LOGO_SVG = """
<svg width="{size}" height="{size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<rect x="4" y="4" width="92" height="92" rx="26" fill="{bg}" stroke="{accent}" stroke-width="4"/>
<path d="M27 51 L43 67 L74 33" stroke="{accent}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def _logo(size=90):
    t = theme_colors()
    return LOGO_SVG.format(size=size, bg=t['bg'], accent=t['accent'])


def hero_header():
    """Big landing-page hero. Used only on the Home screen - every other
    screen uses the compact top_navbar() instead."""
    t = theme_colors()
    html = f"""
<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:8px; margin-top:6px">
{_logo(84)}
<h1 style="text-align:center; color:{t['text']}; margin-top:12px; margin-bottom:0;">PRESENT CALL</h1>
<p style="text-align:center; letter-spacing:3px; text-transform:uppercase; font-size:0.78rem; color:{t['text_secondary']}; margin-top:2px; font-weight:600;">AI Intelligent Attendance System</p>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)
