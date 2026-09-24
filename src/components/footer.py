import streamlit as st
from src.ui.base_layout import theme_colors


def _render_footer():
    t = theme_colors()

    # NOTE: HTML lines start at column 0 on purpose — indenting them causes
    # Streamlit's Markdown parser to render raw text instead of HTML.
    html = f"""
<div style="margin-top:2.5rem; text-align:center; padding:1.2rem 0; border-top:1px solid {t['border']};">
<p style="font-family:'Inter', sans-serif; font-size:0.9rem; color:{t['text_secondary']}; margin-bottom:2px;">
Designed by <a href="https://p-vijay.vercel.app/" target="_blank" style="color:{t['accent']}; text-decoration:none; font-weight:600;">P-Vijay</a> with a cup of tea 🍵
</p>
</div>
"""
    # Add more links here as needed (keep every new line flush at column 0):
    #
    # html += """
    # <p style="margin-top:6px; font-size:0.8rem;">
    # <a href="https://github.com/your-repo" target="_blank">GitHub</a> ·
    # <a href="mailto:you@example.com">Contact</a>
    # </p>
    # """

    st.markdown(html, unsafe_allow_html=True)


def footer_home():
    _render_footer()


def footer_dashboard():
    _render_footer()
