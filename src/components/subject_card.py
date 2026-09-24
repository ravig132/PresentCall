import streamlit as st
from src.ui.base_layout import theme_colors


def subject_card(name, code, section, stats=None, footer_callback=None):
    t = theme_colors()

    html = f"""
<div style="background:{t['surface']}; border-left: 6px solid {t['accent']}; padding:24px; border-radius:20px; border-top:1px solid {t['border']}; border-right:1px solid {t['border']}; border-bottom:1px solid {t['border']}; margin-bottom:18px; box-shadow:{t['card_shadow']};">
<h3 style="margin:0; color:{t['text']}; font-size:1.4rem;">{name}</h3>
<p style="color:{t['text_secondary']}; margin:10px 0;">Code : <span style="background:{t['accent_soft']}; color:{t['accent']}; padding:2px 10px; border-radius:6px; font-weight:600;">{code}</span> &nbsp;|&nbsp; Section : {section}</p>
"""

    if stats:
        html += '<div style="display:flex; gap:8px; flex-wrap:wrap;">'
        for icon, label, value in stats:
            html += f'<div style="background:{t["accent_soft"]}; color:{t["text"]}; padding:5px 12px; border-radius:12px; font-size:0.9rem;">{icon} <b>{value}</b> {label}</div>'
        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
